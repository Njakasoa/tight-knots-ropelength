"""Sampling-based diagnostics for analytic curves.

This module is intentionally labelled an estimate.  Curvature is evaluated
from analytic derivatives, while doubly-critical separation is searched over a
sampled parameter grid.  It is useful for controls and for locating likely
contacts, but it is not a smooth thickness certificate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np

try:  # support both ``PYTHONPATH=repo`` and ``PYTHONPATH=repo/src``
    from curves.base import Curve
except ImportError:  # pragma: no cover - package-layout fallback
    from src.curves.base import Curve


@dataclass
class SmoothThicknessEstimate:
    thickness: float
    curvature_radius: float
    dcsd: float
    length: float
    samples: int
    complete: bool = False
    method: str = "analytic curvature + sampled pair-distance diagnostic"
    limiting: str = "estimate"
    notes: list[str] = field(default_factory=list)
    normalization: str = "radius"

    @property
    def dcsd_half(self) -> float:
        return 0.5 * self.dcsd

    @property
    def ropelength(self) -> float:
        return self.length / self.thickness if self.thickness > 0 else float("inf")

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["dcsd_half"] = self.dcsd_half
        out["ropelength"] = self.ropelength
        return out


def _component_list(value: Any, samples: int):
    if isinstance(value, Curve):
        return list(value.components)
    raise TypeError("smooth thickness expects an analytic Curve")


def _periodic_gap(a: float, b: float, period: float) -> float:
    delta = abs(float(a) - float(b))
    return min(delta, period - delta)


def _stationary_dcsd(components: list[Any], *, samples: int, min_parameter_gap: int) -> tuple[float, int, list[str]]:
    """Search the doubly-critical equations from deterministic starts.

    For components ``x(t)`` and ``y(s)`` the equations are
    ``(x-y).x'(t)=0`` and ``(x-y).y'(s)=0``.  Solving these equations avoids
    the invalid shortcut of treating the nearest pair of sampled points as a
    DCSD candidate.  A finite start grid still makes the result an estimate,
    hence the caller marks it incomplete.
    """

    try:
        from scipy.optimize import root
    except Exception:  # pragma: no cover - scipy is a project dependency
        return float("inf"), 0, ["scipy.optimize.root unavailable; no smooth DCSD estimate"]
    starts_count = min(32, max(8, int(samples)))
    best_distance = float("inf")
    roots_found = 0
    notes: list[str] = []
    for ai, first in enumerate(components):
        period_a = float(first.period)
        for bi in range(ai, len(components)):
            second = components[bi]
            period_b = float(second.period)
            starts_a = np.linspace(0.0, period_a, starts_count, endpoint=False)
            starts_b = np.linspace(0.0, period_b, starts_count, endpoint=False)
            seen: set[tuple[int, int]] = set()

            def equations(parameters):
                ta = float(parameters[0]) % period_a
                tb = float(parameters[1]) % period_b
                difference = first.evaluate(ta) - second.evaluate(tb)
                return np.array([np.dot(difference, first.d1(ta)), np.dot(difference, second.d1(tb))], dtype=float)

            for ta in starts_a:
                for tb in starts_b:
                    # The diagonal root is the coincident-parameter limit,
                    # not a self-distance.  Exclude only close same-component
                    # starts; all roots are filtered again after convergence.
                    if ai == bi and _periodic_gap(ta, tb, period_a) <= period_a * int(min_parameter_gap) / samples:
                        continue
                    try:
                        solved = root(equations, np.array([ta, tb], dtype=float), method="hybr", options={"xtol": 1e-10, "maxfev": 200})
                    except Exception:
                        continue
                    if not solved.success or not np.all(np.isfinite(solved.x)):
                        continue
                    ta_root = float(solved.x[0]) % period_a
                    tb_root = float(solved.x[1]) % period_b
                    if ai == bi and _periodic_gap(ta_root, tb_root, period_a) <= period_a * int(min_parameter_gap) / samples:
                        continue
                    residual = np.linalg.norm(equations((ta_root, tb_root)))
                    if residual > 1e-6:
                        continue
                    key = (int(round(ta_root / period_a * 1000000.0)) % 1000000, int(round(tb_root / period_b * 1000000.0)) % 1000000)
                    if key in seen:
                        continue
                    seen.add(key)
                    roots_found += 1
                    distance = float(np.linalg.norm(first.evaluate(ta_root) - second.evaluate(tb_root)))
                    if distance > 1e-10:
                        best_distance = min(best_distance, distance)
    notes.append(f"stationary-root search found {roots_found} distinct numerical roots from a {starts_count}x{starts_count} deterministic grid")
    notes.append("finite root starts and floating residuals leave smooth DCSD incomplete")
    return best_distance, roots_found, notes


def smooth_thickness(value: Curve, *, samples: int = 256, min_parameter_gap: int = 2) -> SmoothThicknessEstimate:
    """Compute a derivative-based smooth thickness diagnostic.

    Curvature is evaluated from the supplied analytic derivatives.  DCSD is
    estimated only from stationary-root solves; nearest sampled point pairs
    are never treated as doubly critical.
    """

    components = _component_list(value, int(samples))
    if int(samples) < 8:
        raise ValueError("smooth thickness requires at least eight samples")
    samples = int(samples)
    curvature_radius = float("inf")
    curvature_values: list[np.ndarray] = []
    for component in components:
        parameters = np.linspace(0.0, component.period, samples, endpoint=False)
        positions = component.evaluate(parameters)
        d1 = component.d1(parameters)
        d2 = component.d2(parameters)
        speed = np.linalg.norm(d1, axis=1)
        cross = np.linalg.norm(np.cross(d1, d2), axis=1)
        curvature = np.divide(cross, speed**3, out=np.full_like(cross, np.inf), where=speed > 1e-15)
        radii = np.divide(1.0, curvature, out=np.full_like(curvature, np.inf), where=curvature > 1e-15)
        curvature_values.append(radii)
        curvature_radius = min(curvature_radius, float(np.min(radii)))
    best_distance, _, notes = _stationary_dcsd(components, samples=samples, min_parameter_gap=min_parameter_gap)
    notes.insert(0, "dcsd is estimated from stationary equations; sampled distances are not used as DCSD")
    dcsd_half = 0.5 * best_distance
    thickness = min(curvature_radius, dcsd_half)
    if not np.isfinite(thickness):
        notes.append("no finite sampled pair distance")
    limiting = "curvature" if curvature_radius <= dcsd_half else "sampled dcsd"
    return SmoothThicknessEstimate(float(thickness), float(curvature_radius), float(best_distance), float(value.length()), samples, False, notes=notes, limiting=limiting)


def analytic_thickness(value: Curve, **kwargs: Any) -> SmoothThicknessEstimate:
    return smooth_thickness(value, **kwargs)


__all__ = ["SmoothThicknessEstimate", "analytic_thickness", "smooth_thickness"]
