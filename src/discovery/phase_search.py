"""Automated phase--radial-gap search for adjacent toroidal shells.

This module searches only the reviewed conservative pairwise bound. It does
not build a full link, certify smooth reach, prove an isotopy, or optimize
ropelength. The phase variable is free on the full interval [0, 1] and the
optimizer receives no half-phase target or symmetry reward.

For equal populations N on adjacent shells of radii a and b=a+delta inside a
torus of major radius R, the reviewed lower bound is

    d2 >= (a-b)^2 + 2*(S - sqrt(S^2 - 4*a*b*h_a*h_b*sin^2(Delta/2))),
    S = a*b + h_a*h_b,
    h_a = R-a, h_b = R-b,
    Delta = 2*pi*min(f, 1-f)/N.

The implementation evaluates the second term through

    8*a*b*h_a*h_b*sin^2(Delta/2) / (S + sqrt(...))

to avoid cancellation. The vectorized grid check is a separate numerical code
path from the scalar optimizer objective.
"""

from __future__ import annotations

import hashlib
import math
import platform
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy.optimize import NonlinearConstraint, differential_evolution, minimize


DELTA_LOWER = 1.001
DELTA_UPPER = 2.2
DELTA_UPPER_FRACTION = Fraction(11, 5)
DEFAULT_T_VALUES = (8, 32, 128, 512)
DEFAULT_A_FRACTIONS = (
    Fraction(1, 4),
    Fraction(1, 2),
    Fraction(3, 4),
    Fraction(9, 10),
)


def _coerce_fraction(value: Fraction | int | float | str) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("fraction value must be finite")
        return Fraction(str(value))
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"expected a Fraction, int, float, or string, got {type(value).__name__}")


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _fraction_float(value: Fraction) -> float:
    return value.numerator / value.denominator


@dataclass(frozen=True)
class PairSpec:
    """Finite two-shell parameters used by the phase search."""

    t_shells: int
    a_fraction: Fraction
    major_radius: int
    a_exact: Fraction
    a_max_exact: Fraction
    population: int
    delta_lower: float
    delta_upper: float
    capacity_a: float
    capacity_b_at_upper: float

    @property
    def a(self) -> float:
        return _fraction_float(self.a_exact)

    @property
    def b_at_upper(self) -> float:
        return self.a + self.delta_upper

    def record(self) -> dict[str, Any]:
        b_upper = self.b_at_upper
        return {
            "T_shells": self.t_shells,
            "a_fraction_of_admissible_inner_radius": _fraction_text(self.a_fraction),
            "major_radius_R": self.major_radius,
            "inner_radius_a": self.a,
            "inner_radius_a_exact": _fraction_text(self.a_exact),
            "admissible_inner_radius_max_exact": _fraction_text(self.a_max_exact),
            "population_N": self.population,
            "delta_bounds": [self.delta_lower, self.delta_upper],
            "outer_radius_at_delta_upper": b_upper,
            "closure_condition_at_delta_upper": {
                "statement": "R >= 2*b + 2",
                "left_R": float(self.major_radius),
                "right_2b_plus_2": 2.0 * b_upper + 2.0,
                "passes": bool(self.major_radius + 1e-12 >= 2.0 * b_upper + 2.0),
            },
            "half_plane_condition_at_delta_upper": {
                "statement": "b <= R/2",
                "b": b_upper,
                "R_over_2": self.major_radius / 2.0,
                "passes": bool(b_upper <= self.major_radius / 2.0 + 1e-12),
            },
            "capacity_rule": "N=floor(pi*a*(R-a)/sqrt(a^2+(R-a)^2))-1",
            "capacity_at_a": self.capacity_a,
            "capacity_at_b_upper": self.capacity_b_at_upper,
            "capacity_monotonicity": {
                "condition": "0 < a <= b <= R/2",
                "derivative_sign_argument": (
                    "d/dr [r*(R-r)/sqrt(r^2+(R-r)^2)] has sign R-2*r"
                ),
                "checked_at_upper_endpoint": bool(
                    self.capacity_b_at_upper + 1e-12 >= self.capacity_a
                ),
            },
        }


def shell_capacity(radius: float, hole_radius: float) -> float:
    """Return pi*r*h/sqrt(r^2+h^2) using ordinary floats for exploration."""

    if not (radius > 0.0 and hole_radius > 0.0):
        raise ValueError("radius and hole_radius must be positive")
    return math.pi * radius * hole_radius / math.hypot(radius, hole_radius)


def shell_capacity_at_radius(radius: float, major_radius: float) -> float:
    if not (0.0 < radius < major_radius):
        raise ValueError("radius must lie strictly inside the major radius")
    return shell_capacity(radius, major_radius - radius)


def safe_population(inner_radius: float, major_radius: float) -> int:
    """Use the reviewed sufficient same-shell rule at the inner radius."""

    capacity = shell_capacity_at_radius(inner_radius, major_radius)
    population = math.floor(capacity) - 1
    if population < 3:
        raise ValueError(f"safe population is too small for the phase grid: {population}")
    return population


def build_pair_spec(
    t_shells: int,
    a_fraction: Fraction | int | float | str,
    *,
    delta_lower: float = DELTA_LOWER,
    delta_upper: float = DELTA_UPPER,
) -> PairSpec:
    """Build an admissible pair with R=4*T+2 and derived equal population."""

    if not isinstance(t_shells, int) or t_shells <= 0:
        raise ValueError("t_shells must be a positive integer")
    if not (math.isfinite(delta_lower) and math.isfinite(delta_upper)):
        raise ValueError("delta bounds must be finite")
    if delta_lower <= 0.0 or delta_upper < delta_lower:
        raise ValueError("delta bounds must satisfy 0 < lower <= upper")
    fraction = _coerce_fraction(a_fraction)
    if not (Fraction(0, 1) < fraction <= Fraction(1, 1)):
        raise ValueError("a_fraction must lie in (0, 1]")

    major_radius = 4 * t_shells + 2
    upper_fraction = _coerce_fraction(delta_upper)
    a_max_exact = (Fraction(major_radius - 2, 1) - upper_fraction) / 2
    a_exact = fraction * a_max_exact
    a = _fraction_float(a_exact)
    b_upper = a + delta_upper
    if major_radius + 1e-12 < 2.0 * b_upper + 2.0:
        raise ValueError("admissible inner radius violates R >= 2*b+2")
    if b_upper > major_radius / 2.0 + 1e-12:
        raise ValueError("admissible inner radius violates b <= R/2")

    population = safe_population(a, float(major_radius))
    return PairSpec(
        t_shells=t_shells,
        a_fraction=fraction,
        major_radius=major_radius,
        a_exact=a_exact,
        a_max_exact=a_max_exact,
        population=population,
        delta_lower=float(delta_lower),
        delta_upper=float(delta_upper),
        capacity_a=shell_capacity_at_radius(a, float(major_radius)),
        capacity_b_at_upper=shell_capacity_at_radius(b_upper, float(major_radius)),
    )


def _phase_fraction(fraction: float) -> float:
    if not math.isfinite(fraction) or fraction < 0.0 or fraction > 1.0:
        raise ValueError("phase fraction must lie in [0, 1]")
    return min(fraction, 1.0 - fraction)


def cross_shell_bound_components(
    a: float,
    b: float,
    major_radius: float,
    population: int,
    phase_fraction: float,
) -> dict[str, float]:
    """Return the stable scalar evaluation of the reviewed lower bound."""

    if not (0.0 < a <= b < major_radius):
        raise ValueError("need 0 < a <= b < R")
    if not isinstance(population, int) or population <= 0:
        raise ValueError("population must be positive")
    f = _phase_fraction(float(phase_fraction))
    h_a = major_radius - a
    h_b = major_radius - b
    u = a * b
    v = h_a * h_b
    s_value = u + v
    sine = math.sin(math.pi * f / population)
    sine_sq = sine * sine
    radicand = s_value * s_value - 4.0 * u * v * sine_sq
    scale = max(s_value * s_value, 1.0)
    if radicand < 0.0 and radicand >= -1e-14 * scale:
        radicand = 0.0
    if radicand < 0.0:
        raise ArithmeticError("cross-shell square-root radicand became negative")
    root = math.sqrt(radicand)
    # This is 2*(S-sqrt(S^2-X)) with X=4*u*v*sin^2, evaluated without
    # cancellation. Delta/2 is pi*min(f,1-f)/N.
    stable_transverse = 8.0 * u * v * sine_sq / (s_value + root)
    radial_sq = (a - b) * (a - b)
    lower_sq = radial_sq + stable_transverse
    return {
        "phase_fraction_reduced": f,
        "phase_angle_half": math.pi * f / population,
        "sine_squared": sine_sq,
        "radial_gap": b - a,
        "radial_squared": radial_sq,
        "h_a": h_a,
        "h_b": h_b,
        "U_ab": u,
        "V_hahb": v,
        "S": s_value,
        "radicand": radicand,
        "stable_transverse_term": stable_transverse,
        "lower_bound_squared": lower_sq,
        "lower_bound_distance": math.sqrt(max(lower_sq, 0.0)),
        "constraint_margin_squared": lower_sq - 4.0,
    }


def cross_shell_lower_bound_sq(
    a: float,
    b: float,
    major_radius: float,
    population: int,
    phase_fraction: float,
) -> float:
    return cross_shell_bound_components(
        a, b, major_radius, population, phase_fraction
    )["lower_bound_squared"]


def capacity_monotonicity_check(a: float, b: float, major_radius: float) -> bool:
    """Check the admissible monotonicity used to reuse the inner population."""

    if not (0.0 < a <= b <= major_radius / 2.0):
        return False
    return shell_capacity_at_radius(b, major_radius) + 1e-12 >= shell_capacity_at_radius(
        a, major_radius
    )


def _vectorized_lower_bound_sq(
    phases: np.ndarray,
    deltas: np.ndarray | float,
    *,
    a: float,
    major_radius: float,
    population: int,
) -> np.ndarray:
    """Independent vectorized implementation used only by the grid check."""

    f_array = np.asarray(phases, dtype=float)
    f = np.minimum(f_array, 1.0 - f_array)
    delta = np.asarray(deltas, dtype=float)
    b = a + delta
    h_a = major_radius - a
    h_b = major_radius - b
    u = a * b
    v = h_a * h_b
    s_value = u + v
    sine_sq = np.sin(np.pi * f / population) ** 2
    radicand = np.maximum(0.0, s_value * s_value - 4.0 * u * v * sine_sq)
    return (a - b) ** 2 + 8.0 * u * v * sine_sq / (s_value + np.sqrt(radicand))


def independent_grid_crosscheck(spec: PairSpec, *, grid_points: int = 10001) -> dict[str, Any]:
    """Minimize over a high-resolution phase grid without the optimizer."""

    if not isinstance(grid_points, int) or grid_points < 101:
        raise ValueError("grid_points must be an integer >= 101")
    phases = np.linspace(0.0, 1.0, grid_points, dtype=float)
    delta_lo = float(spec.delta_lower)
    delta_hi = float(spec.delta_upper)

    # Probe monotonicity in delta numerically before using bisection. The
    # result is evidence about this finite grid, not a theorem about all data.
    probe_deltas = np.linspace(delta_lo, delta_hi, 17, dtype=float)
    probe_values = np.vstack(
        [
            _vectorized_lower_bound_sq(
                phases,
                value,
                a=spec.a,
                major_radius=float(spec.major_radius),
                population=spec.population,
            )
            for value in probe_deltas
        ]
    )
    violations = int(np.count_nonzero(np.diff(probe_values, axis=0) < -1e-10))

    values_lo = _vectorized_lower_bound_sq(
        phases,
        delta_lo,
        a=spec.a,
        major_radius=float(spec.major_radius),
        population=spec.population,
    )
    values_hi = _vectorized_lower_bound_sq(
        phases,
        delta_hi,
        a=spec.a,
        major_radius=float(spec.major_radius),
        population=spec.population,
    )
    if bool(np.any(values_hi < 4.0 - 1e-10)):
        raise RuntimeError("delta upper bound does not make every phase feasible")

    lo = np.full(phases.shape, delta_lo, dtype=float)
    hi = np.full(phases.shape, delta_hi, dtype=float)
    feasible_at_lower = values_lo >= 4.0
    for _ in range(56):
        mid = (lo + hi) / 2.0
        values = _vectorized_lower_bound_sq(
            phases,
            mid,
            a=spec.a,
            major_radius=float(spec.major_radius),
            population=spec.population,
        )
        feasible = values >= 4.0
        hi = np.where(feasible, mid, hi)
        lo = np.where(feasible, lo, mid)
    roots = np.where(feasible_at_lower, delta_lo, hi)
    index = int(np.argmin(roots))
    delta_min = float(roots[index])
    phase_min = float(phases[index])
    lower_sq = float(
        _vectorized_lower_bound_sq(
            np.asarray([phase_min]),
            delta_min,
            a=spec.a,
            major_radius=float(spec.major_radius),
            population=spec.population,
        )[0]
    )
    return {
        "grid_points": grid_points,
        "phase_grid_includes_endpoints": True,
        "phase_fraction_min_observed": phase_min,
        "minimal_delta_observed": delta_min,
        "lower_bound_squared_at_grid_min": lower_sq,
        "constraint_margin_squared_at_grid_min": lower_sq - 4.0,
        "monotonicity_probe": {
            "delta_samples": len(probe_deltas),
            "violations_below_minus_1e-10": violations,
            "passes_on_this_grid": violations == 0,
        },
        "upper_endpoint_feasible_for_all_grid_phases": bool(
            np.all(values_hi >= 4.0 - 1e-10)
        ),
    }


def _trial_record(
    result: Any,
    *,
    spec: PairSpec,
    method: str,
    seed: int | None,
    initial_seed: dict[str, float] | None = None,
) -> dict[str, Any]:
    x = np.asarray(result.x, dtype=float)
    phase = float(np.clip(x[0], 0.0, 1.0))
    delta = float(np.clip(x[1], spec.delta_lower, spec.delta_upper))
    components = cross_shell_bound_components(
        spec.a,
        spec.a + delta,
        float(spec.major_radius),
        spec.population,
        phase,
    )
    constraint_violation = getattr(result, "constraint_violation", None)
    if constraint_violation is not None:
        try:
            constraint_violation = float(np.asarray(constraint_violation).max())
        except (TypeError, ValueError):
            constraint_violation = None
    return {
        "method": method,
        "seed": seed,
        "initial_seed": initial_seed,
        "phase_fraction": phase,
        "radial_gap_delta": delta,
        "objective_value_delta": delta,
        "lower_bound_squared": components["lower_bound_squared"],
        "lower_bound_distance": components["lower_bound_distance"],
        "constraint_margin_squared": components["constraint_margin_squared"],
        "feasible_without_tolerance": components["constraint_margin_squared"] >= 0.0,
        "feasible_with_1e-8_tolerance": components["constraint_margin_squared"] >= -1e-8,
        "result": {
            "success": bool(getattr(result, "success", False)),
            "status": int(getattr(result, "status", -1)),
            "message": str(getattr(result, "message", "")),
            "nfev": int(getattr(result, "nfev", 0) or 0),
            "nit": int(getattr(result, "nit", 0) or 0),
            "fun": float(getattr(result, "fun", delta)),
            "constraint_violation": constraint_violation,
        },
        "bound_components": components,
    }


def _ceil_decimal_fraction(value: float, places: int) -> Fraction:
    scale = 10**places
    scaled = (Decimal(str(value)) * Decimal(scale)).to_integral_value(rounding=ROUND_CEILING)
    return Fraction(int(scaled), scale)


def _floor_decimal_fraction(value: float, places: int) -> Fraction:
    scale = 10**places
    scaled = (Decimal(str(value)) * Decimal(scale)).to_integral_value(rounding=ROUND_FLOOR)
    return Fraction(int(scaled), scale)


def conservative_rounded_inputs(
    phase_fraction: float,
    radial_gap: float,
    *,
    places: int = 8,
    padding_ticks: int = 100,
) -> tuple[Fraction, Fraction]:
    """Round phase away from the beneficial midpoint and delta upward."""

    if not (0.0 <= phase_fraction <= 1.0):
        raise ValueError("phase fraction must lie in [0,1]")
    if radial_gap <= 0.0:
        raise ValueError("radial gap must be positive")
    if phase_fraction <= 0.5:
        phase = _floor_decimal_fraction(phase_fraction, places)
    else:
        phase = _ceil_decimal_fraction(phase_fraction, places)
    delta = _ceil_decimal_fraction(radial_gap, places)
    delta += Fraction(padding_ticks, 10**places)
    phase = max(Fraction(0, 1), min(Fraction(1, 1), phase))
    return phase, delta


def arb_certify_pair(
    spec: PairSpec,
    *,
    phase_fraction: Fraction | int | float | str,
    radial_gap: Fraction | int | float | str,
    precision_bits: int = 224,
    output_digits: int = 50,
) -> dict[str, Any]:
    """Certify one rounded finite pair with Arb, including its margin.

    The certificate covers the displayed conservative pairwise lower bound and
    the two capacity floors. It does not certify a full shell bundle or link.
    """

    try:
        from src.certification.arb_backend import (
            arb,
            arb_precision,
            arb_record,
            exact_rational,
        )
        from src.certification.shell_family import certified_floor
    except Exception as exc:  # pragma: no cover - exercised only without flint
        return {
            "status": "UNAVAILABLE",
            "error": f"{type(exc).__name__}: {exc}",
            "scope": "Arb finite pair lower-bound certificate only",
        }

    phase = _coerce_fraction(phase_fraction)
    delta = _coerce_fraction(radial_gap)
    if not (Fraction(0, 1) <= phase <= Fraction(1, 1)):
        raise ValueError("phase fraction must lie in [0,1]")
    if delta <= 0:
        raise ValueError("radial gap must be positive")
    reduced_phase = min(phase, Fraction(1, 1) - phase)

    with arb_precision(precision_bits):
        ar = lambda value: exact_rational(value.numerator, value.denominator)
        pi = arb.pi()
        a = ar(spec.a_exact)
        R = arb(spec.major_radius)
        b = a + ar(delta)
        h_a = R - a
        h_b = R - b
        u = a * b
        v = h_a * h_b
        s_value = u + v
        angle = pi * ar(reduced_phase) / arb(spec.population)
        sine_sq = angle.sin() * angle.sin()
        radicand = s_value * s_value - arb(4) * u * v * sine_sq
        if bool(radicand.upper() < arb(0)):
            return {
                "status": "FAIL",
                "error": "Arb radicand is strictly negative",
                "radicand": arb_record(radicand, digits=output_digits, label="radicand"),
            }
        root = radicand.sqrt()
        stable_transverse = arb(8) * u * v * sine_sq / (s_value + root)
        d2 = (a - b) * (a - b) + stable_transverse
        margin = d2 - arb(4)

        capacity_a = pi * a * h_a / (a * a + h_a * h_a).sqrt()
        capacity_b = pi * b * h_b / (b * b + h_b * h_b).sqrt()
        floor_a = certified_floor(capacity_a, label="Arb pair inner capacity")
        floor_b = certified_floor(capacity_b, label="Arb pair outer capacity")
        monotone_certified = bool(capacity_b.lower() >= capacity_a.upper())
        status = "PASS" if bool(margin.lower() > arb(0)) else "FAIL"
        return {
            "status": status,
            "scope": "Arb finite pair lower-bound and capacity-floor certificate only",
            "precision_bits": precision_bits,
            "inputs": {
                "T_shells": spec.t_shells,
                "R": spec.major_radius,
                "a_exact": _fraction_text(spec.a_exact),
                "b_exact": _fraction_text(spec.a_exact + delta),
                "phase_fraction_exact": _fraction_text(phase),
                "reduced_phase_fraction_exact": _fraction_text(reduced_phase),
                "delta_exact": _fraction_text(delta),
                "population_N": spec.population,
            },
            "d2_lower_bound": arb_record(d2, digits=output_digits, label="d2_lower_bound"),
            "constraint_margin_squared": arb_record(
                margin, digits=output_digits, label="constraint_margin_squared"
            ),
            "capacity_a": arb_record(capacity_a, digits=output_digits, label="capacity_a"),
            "capacity_b": arb_record(capacity_b, digits=output_digits, label="capacity_b"),
            "capacity_floor_a": floor_a,
            "capacity_floor_b": floor_b,
            "expected_population_rule_matches": floor_a - 1 == spec.population,
            "outer_population_is_at_least_inner": floor_b >= floor_a,
            "capacity_monotonicity_certified": monotone_certified,
            "closure_condition": {
                "statement": "R >= 2*b + 2",
                "passes": bool(R.lower() >= arb(2) * b.upper() + arb(2)),
            },
        }


def _certify_selected_pair(
    spec: PairSpec,
    selected: dict[str, Any],
    *,
    precision_bits: int,
    output_digits: int,
) -> dict[str, Any]:
    raw_phase = float(selected["phase_fraction"])
    raw_delta = float(selected["radial_gap_delta"])
    attempts: list[dict[str, Any]] = []
    for padding_ticks in (1, 10, 100, 1000, 10000):
        phase, delta = conservative_rounded_inputs(
            raw_phase,
            raw_delta,
            places=8,
            padding_ticks=padding_ticks,
        )
        certificate = arb_certify_pair(
            spec,
            phase_fraction=phase,
            radial_gap=delta,
            precision_bits=precision_bits,
            output_digits=output_digits,
        )
        attempt = {
            "padding_ticks": padding_ticks,
            "phase_fraction_exact": _fraction_text(phase),
            "radial_gap_exact": _fraction_text(delta),
            "certificate_status": certificate.get("status"),
            "certificate": certificate,
        }
        attempts.append(attempt)
        if certificate.get("status") in {"PASS", "UNAVAILABLE"}:
            return {
                "status": certificate.get("status"),
                "raw_optimizer_inputs": {
                    "phase_fraction": raw_phase,
                    "radial_gap": raw_delta,
                },
                "rounding_policy": (
                    "phase rounded away from f=1/2 at 8 decimal places; "
                    "delta rounded upward with the smallest passing padding"
                ),
                "selected_attempt": attempt,
                "attempts": attempts,
            }
    return {
        "status": "FAIL",
        "raw_optimizer_inputs": {
            "phase_fraction": raw_phase,
            "radial_gap": raw_delta,
        },
        "rounding_policy": (
            "phase rounded away from f=1/2 at 8 decimal places; "
            "delta rounded upward through all attempted paddings"
        ),
        "attempts": attempts,
    }


def search_pair(
    spec: PairSpec,
    *,
    seed: int = 7013,
    de_maxiter: int = 80,
    de_popsize: int = 8,
    uniform_seed_count: int = 9,
    grid_points: int = 10001,
    precision_bits: int = 224,
    output_digits: int = 50,
    certify: bool = True,
) -> dict[str, Any]:
    """Search free phase and radial gap for one finite equal-population pair."""

    if de_maxiter <= 0 or de_popsize <= 0 or uniform_seed_count <= 0:
        raise ValueError("optimizer iteration, population, and seed counts must be positive")
    if not capacity_monotonicity_check(
        spec.a, spec.b_at_upper, float(spec.major_radius)
    ):
        raise ValueError("pair spec failed the larger-radius capacity monotonicity check")

    def constraint_value(x: Sequence[float]) -> float:
        phase, delta = float(x[0]), float(x[1])
        return (
            cross_shell_lower_bound_sq(
                spec.a,
                spec.a + delta,
                float(spec.major_radius),
                spec.population,
                phase,
            )
            - 4.0
        )

    def objective(x: Sequence[float]) -> float:
        # The only objective is radial gap. Feasibility is supplied separately
        # by the exact reviewed lower-bound constraint.
        return float(x[1])

    bounds = [(0.0, 1.0), (spec.delta_lower, spec.delta_upper)]
    constraint = NonlinearConstraint(constraint_value, 0.0, np.inf)
    trials: list[dict[str, Any]] = []
    initial_seeds = [
        {
            "method": "SLSQP",
            "phase_fraction": float(value),
            "radial_gap_delta": spec.delta_upper,
        }
        for value in np.linspace(0.0, 1.0, uniform_seed_count, endpoint=False)
    ]
    de_error: str | None = None
    try:
        de_result = differential_evolution(
            objective,
            bounds,
            constraints=(constraint,),
            seed=seed,
            maxiter=de_maxiter,
            popsize=de_popsize,
            tol=1e-10,
            polish=True,
            updating="immediate",
            workers=1,
        )
        trials.append(
            _trial_record(
                de_result,
                spec=spec,
                method="differential_evolution",
                seed=seed,
            )
        )
    except Exception as exc:
        de_error = f"{type(exc).__name__}: {exc}"

    for index, initial in enumerate(initial_seeds):
        local_result = minimize(
            objective,
            np.asarray([initial["phase_fraction"], initial["radial_gap_delta"]], dtype=float),
            method="SLSQP",
            bounds=bounds,
            constraints={"type": "ineq", "fun": constraint_value},
            options={"maxiter": max(300, de_maxiter * 4), "ftol": 1e-12, "disp": False},
        )
        trials.append(
            _trial_record(
                local_result,
                spec=spec,
                method="SLSQP",
                seed=index,
                initial_seed=initial,
            )
        )

    feasible_trials = [
        item for item in trials if item["constraint_margin_squared"] >= -1e-8
    ]
    if not feasible_trials:
        raise RuntimeError("no feasible optimizer trial found in the requested delta range")
    selected = min(
        feasible_trials,
        key=lambda item: (float(item["radial_gap_delta"]), -float(item["constraint_margin_squared"])),
    )
    selected = dict(selected)
    selected["selection_reason"] = (
        "minimum observed radial gap among optimizer trials with margin >= -1e-8"
    )
    grid = independent_grid_crosscheck(spec, grid_points=grid_points)
    grid["optimizer_selected_delta_minus_grid_delta"] = float(
        selected["radial_gap_delta"] - grid["minimal_delta_observed"]
    )
    grid["optimizer_selected_phase"] = selected["phase_fraction"]
    arb_certificate = (
        _certify_selected_pair(
            spec,
            selected,
            precision_bits=precision_bits,
            output_digits=output_digits,
        )
        if certify
        else {"status": "NOT_REQUESTED"}
    )

    return {
        "schema": "discovery-phase-packing-v1",
        "result_status": "finite adjacent-shell pair search",
        "scientific_scope": (
            "Pairwise conservative toroidal separation diagnostic. "
            "No full-bundle thickness, isotopy, topology, ropelength, or global optimum claim."
        ),
        "family_metadata": {
            "family": "adjacent equal-population p=1 toroidal-shell pair",
            "target_context": "T(Q,Q) p=1 toroidal-link family",
            "component_role": "two adjacent equal-population shells",
            "Q_per_shell": spec.population,
            "Q_status": "pair-level population; no full-bundle Q is constructed here",
            "shell_count": 2,
            "winding": "fixed p=1 toroidal winding",
            "pitch": "fixed by the p=1 toroidal parametrization; no pitch parameter varied",
            "radii": {
                "inner": "a",
                "outer": "b=a+delta",
                "major": "R=4*T+2",
                "finite_pair_values": {
                    "a": spec.a,
                    "outer_at_delta_upper": spec.b_at_upper,
                    "R": spec.major_radius,
                },
            },
            "populations": {
                "inner_N": spec.population,
                "outer_N": spec.population,
                "rule": "N derived at inner shell and reused at b by capacity monotonicity",
            },
            "phase": {
                "inner_grid": "2*pi*j/N",
                "outer_grid": "2*pi*j/N+2*pi*f/N",
                "free_parameter": "f in [0,1]",
            },
            "closure": {
                "major_radius_rule": "R=4*T+2",
                "condition": "R >= 2*b+2 checked throughout the search range",
            },
            "closure_R": "R >= 2*b+2 checked throughout the search range",
            "symmetry": {
                "phase_grids": "equal N-gon grids",
                "varied_symmetry_parameter": "relative phase f only",
            },
            "free_search_fields": ["phase_fraction_f", "radial_gap_delta"],
            "sweep_fields": ["T_shells", "a_fraction"],
            "unsupported_fields": [
                "full-bundle Q and shell populations beyond this pair",
                "non-adjacent-shell phase optimization",
                "pitch optimization",
                "full-link closure or isotopy certification",
                "ropelength optimization",
            ],
            "varied_fields": [
                "T_shells",
                "a_fraction",
                "phase_fraction_f",
                "radial_gap_delta",
            ],
            "fixed_constraints": [
                "p=1 winding",
                "equal population N on the adjacent pair",
                "safe same-shell population floor at a",
                "R=4*T+2",
                "delta in [1.001,2.2]",
            ],
            "objective_and_seeds": (
                "minimize delta subject to the reviewed lower-bound constraint; "
                "uniform phase seeds and differential evolution; no half-phase target or reward"
            ),
        },
        "pair": spec.record(),
        "inequalities": {
            "lower_bound": (
                "d2_lower=(a-b)^2+2*(S-sqrt(S^2-4*a*b*(R-a)*(R-b)*sin^2(Delta/2)))"
            ),
            "stable_evaluation": (
                "stable_transverse=8*a*b*(R-a)*(R-b)*sin^2(Delta/2)"
                "/(S+sqrt(S^2-4*a*b*(R-a)*(R-b)*sin^2(Delta/2)))"
            ),
            "phase_angle": "Delta/2=pi*min(f,1-f)/N",
            "feasibility": "d2_lower >= 4 (equivalently lower distance >= 2)",
            "capacity": "N=floor(pi*a*(R-a)/sqrt(a^2+(R-a)^2))-1",
            "capacity_reuse_condition": "0 < a <= b <= R/2",
        },
        "optimizer": {
            "bounds": {
                "phase_fraction": [0.0, 1.0],
                "radial_gap_delta": [spec.delta_lower, spec.delta_upper],
            },
            "seed": seed,
            "differential_evolution": {
                "maxiter": de_maxiter,
                "popsize": de_popsize,
                "polish": True,
                "termination_error": de_error,
            },
            "uniform_phase_seed_count": uniform_seed_count,
            "initial_seeds": initial_seeds,
        },
        "trials": trials,
        "selected": selected,
        "grid_crosscheck": grid,
        "arb_certificate": arb_certificate,
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
    }


def source_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


__all__ = [
    "DEFAULT_A_FRACTIONS",
    "DEFAULT_T_VALUES",
    "DELTA_LOWER",
    "DELTA_UPPER",
    "PairSpec",
    "arb_certify_pair",
    "build_pair_spec",
    "capacity_monotonicity_check",
    "conservative_rounded_inputs",
    "cross_shell_bound_components",
    "cross_shell_lower_bound_sq",
    "independent_grid_crosscheck",
    "safe_population",
    "search_pair",
    "shell_capacity",
    "shell_capacity_at_radius",
    "source_sha256",
]
