"""Configurable periodic shell grammars for finite geometry experiments.

The generator in this module is intentionally a geometry and topology
*grammar*.  It is useful to hand analytic coordinates to a numerical
thickness or contact search, but it does not certify reach, polygonal
thickness, or an isotopy of a sampled polygon.

For a major radius ``R`` and a shell point ``w`` in the normal disk of the
longitude ``u``, use

``E(u, w) = ((R + Re(w))*cos(u), (R + Re(w))*sin(u), Im(w)).``

The ``j``-th point on shell ``i`` is

``w_ij(u) = r_i*exp(i*(u + beta_i*sin(u) - phi_ij)),``

where ``phi_ij = 2*pi*j/N_i + phase_offset_i``.  Thus ``beta_i`` changes the
pitch around a shell while preserving ``|w_ij(u)| = r_i`` and periodicity.
The optional core is ``E(u, 0)``.  In ``double_hopf`` mode the second copy is
the proper rigid motion ``P(x,y,z) = (R+x, -z, y)``.  A positive diagonal
ambient scaling is applied after that motion.

The constructive topology scope is a full twist ``T(Q,Q)`` for one bundle
and ``T(2Q,2Q)`` after the Hopf doubling, where ``Q`` counts the optional
core and all shell strands in one bundle.  The proof-level assumptions and
the distinction between analytic curves and finite samples are recorded in
the returned metadata and in ``proofs/VARIABLE_PITCH_TOPOLOGY.md``.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


TWO_PI = 2.0 * math.pi
SCHEMA = "periodic-variable-pitch-shell-grammar-v1"


def _as_float(value: Any, *, label: str) -> float:
    """Coerce a scalar to a finite float without accepting booleans."""

    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{label} must be a finite real number")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{label} must be a finite real number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _float_tuple(values: Sequence[Any], *, label: str) -> tuple[float, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be a sequence of numbers")
    try:
        items = tuple(values)
    except TypeError as exc:
        raise ValueError(f"{label} must be a sequence of numbers") from exc
    return tuple(_as_float(value, label=f"{label}[{index}]") for index, value in enumerate(items))


def _positive_scale(values: Sequence[Any]) -> tuple[float, float, float]:
    values_tuple = _float_tuple(values, label="ambient_axis_scale")
    if len(values_tuple) != 3:
        raise ValueError("ambient_axis_scale must contain exactly three positive values")
    if any(value <= 0.0 for value in values_tuple):
        raise ValueError("ambient_axis_scale values must be strictly positive")
    return values_tuple  # type: ignore[return-value]


def _population_tuple(values: Sequence[Any]) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError("shell_populations must be a sequence of positive integers")
    try:
        items = tuple(values)
    except TypeError as exc:
        raise ValueError("shell_populations must be a sequence of positive integers") from exc
    result: list[int] = []
    for index, value in enumerate(items):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"shell_populations[{index}] must be a positive integer")
        try:
            integer = int(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"shell_populations[{index}] must be a positive integer") from exc
        if integer != value or integer <= 0:
            raise ValueError(f"shell_populations[{index}] must be a positive integer")
        result.append(integer)
    return tuple(result)


def _normalise_closure_mode(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("closure_mode must be 'single_torus' or 'double_hopf'")
    key = value.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "single": "single_torus",
        "single_bundle": "single_torus",
        "single_torus": "single_torus",
        "double": "double_hopf",
        "double_bundle": "double_hopf",
        "double_hopf": "double_hopf",
    }
    try:
        return aliases[key]
    except KeyError as exc:
        raise ValueError("closure_mode must be 'single_torus' or 'double_hopf'") from exc


@dataclass(frozen=True)
class ShellGrammarConfig:
    """Validated finite parameters for the periodic shell grammar.

    ``t_shells`` is optional convenience metadata.  When supplied it must
    equal the number of shell radius/population entries; the canonical ``T``
    property always derives from those entries.  Phase offsets are in radians
    and ``pitch_modulations`` are dimensionless coefficients in
    ``u + beta_i*sin(u)``.  No smallness assumption on ``beta_i`` is needed for
    smoothness or closure; the longitudinal angle still makes the curve
    regular when ``R > max(r_i)``.
    """

    major_radius: float
    shell_radii: Sequence[float]
    shell_populations: Sequence[int]
    phase_offsets: Sequence[float] | None = None
    pitch_modulations: Sequence[float] | None = None
    core_included: bool = True
    closure_mode: str = "single_torus"
    ambient_axis_scale: Sequence[float] = (1.0, 1.0, 1.0)
    t_shells: int | None = None

    def __post_init__(self) -> None:
        R = _as_float(self.major_radius, label="major_radius")
        if R <= 0.0:
            raise ValueError("major_radius must be positive")

        radii = _float_tuple(self.shell_radii, label="shell_radii")
        populations = _population_tuple(self.shell_populations)
        if not radii:
            raise ValueError("at least one shell radius is required")
        if len(radii) != len(populations):
            raise ValueError("shell_radii and shell_populations must have the same length")
        if any(radius <= 0.0 for radius in radii):
            raise ValueError("shell_radii must be strictly positive")
        if len(set(radii)) != len(radii):
            raise ValueError("shell_radii must be pairwise distinct")
        if not R > max(radii):
            raise ValueError("require major_radius > max(shell_radii) > 0")

        closure_mode = _normalise_closure_mode(self.closure_mode)
        if closure_mode == "double_hopf" and not R > 2.0 * max(radii):
            raise ValueError(
                "double_hopf requires major_radius > 2*max(shell_radii) "
                "for the proper-doubling ambient separation argument"
            )

        if not isinstance(self.core_included, (bool, np.bool_)):
            raise ValueError("core_included must be boolean")

        phase_offsets = (
            tuple(0.0 for _ in radii)
            if self.phase_offsets is None
            else _float_tuple(self.phase_offsets, label="phase_offsets")
        )
        pitch_modulations = (
            tuple(0.0 for _ in radii)
            if self.pitch_modulations is None
            else _float_tuple(self.pitch_modulations, label="pitch_modulations")
        )
        if len(phase_offsets) != len(radii):
            raise ValueError("phase_offsets must have one entry per shell")
        if len(pitch_modulations) != len(radii):
            raise ValueError("pitch_modulations must have one entry per shell")

        if self.t_shells is None:
            t_shells = len(radii)
        else:
            if isinstance(self.t_shells, (bool, np.bool_)) or not isinstance(self.t_shells, (int, np.integer)):
                raise ValueError("t_shells must be a positive integer")
            t_shells = int(self.t_shells)
            if t_shells <= 0 or t_shells != len(radii):
                raise ValueError("t_shells must equal the number of shell entries")

        scale = _positive_scale(self.ambient_axis_scale)
        object.__setattr__(self, "major_radius", R)
        object.__setattr__(self, "shell_radii", radii)
        object.__setattr__(self, "shell_populations", populations)
        object.__setattr__(self, "phase_offsets", phase_offsets)
        object.__setattr__(self, "pitch_modulations", pitch_modulations)
        object.__setattr__(self, "core_included", bool(self.core_included))
        object.__setattr__(self, "closure_mode", closure_mode)
        object.__setattr__(self, "ambient_axis_scale", scale)
        object.__setattr__(self, "t_shells", t_shells)

    @property
    def T(self) -> int:
        """Number of shells, exposed using the notation of the proofs."""

        return int(self.t_shells)

    @property
    def r_max(self) -> float:
        return max(self.shell_radii)

    @property
    def Q(self) -> int:
        """One-bundle component count, including the optional core."""

        return (1 if self.core_included else 0) + sum(self.shell_populations)

    def as_record(self) -> dict[str, Any]:
        """Return JSON-ready configuration data with no hidden parameters."""

        return {
            "T_shells": self.T,
            "major_radius_R": self.major_radius,
            "shell_radii": list(self.shell_radii),
            "shell_populations": list(self.shell_populations),
            "phase_offsets_radians": list(self.phase_offsets or ()),
            "pitch_modulations_beta": list(self.pitch_modulations or ()),
            "core_included": self.core_included,
            "closure_mode": self.closure_mode,
            "ambient_axis_scale": list(self.ambient_axis_scale),
            "r_max": self.r_max,
            "one_bundle_component_count_Q": self.Q,
            "proper_double_requires_R_gt_2_r_max": self.closure_mode == "double_hopf",
        }


@dataclass(frozen=True)
class ShellComponentSpec:
    """Descriptor for one generated analytic component."""

    component: int
    bundle: int
    role: str
    shell_index: int | None
    strand_index: int | None
    radius: float
    population: int | None
    phase_offset: float
    strand_phase: float
    beta: float

    def as_record(self) -> dict[str, Any]:
        return {
            "component": self.component,
            "bundle": self.bundle,
            "role": self.role,
            "shell_index": self.shell_index,
            "strand_index": self.strand_index,
            "radius": self.radius,
            "population": self.population,
            "phase_offset_radians": self.phase_offset,
            "strand_phase_radians": self.strand_phase,
            "beta": self.beta,
        }


def apply_positive_axis_scaling(
    coordinates: np.ndarray | Sequence[Sequence[float]],
    scales: Sequence[float] = (1.0, 1.0, 1.0),
) -> np.ndarray:
    """Apply an invertible positive diagonal ambient map to coordinates."""

    scale = np.asarray(_positive_scale(scales), dtype=float)
    values = np.asarray(coordinates, dtype=float)
    if values.shape[-1:] != (3,):
        raise ValueError("coordinates must have a final dimension of length three")
    if not np.all(np.isfinite(values)):
        raise ValueError("coordinates must be finite")
    return values * scale


def _config_from_mapping(config: Mapping[str, Any]) -> ShellGrammarConfig:
    data = dict(config)
    if "t_shells" not in data and "T" in data:
        data["t_shells"] = data.pop("T")
    if "major_radius" not in data and "R" in data:
        data["major_radius"] = data.pop("R")
    if "closure" in data and "closure_mode" not in data:
        data["closure_mode"] = data.pop("closure")
    if "axis_scale" in data and "ambient_axis_scale" not in data:
        data["ambient_axis_scale"] = data.pop("axis_scale")
    return ShellGrammarConfig(**data)


class ShellGrammar:
    """Analytic family and diagnostic finite samples for one configuration."""

    def __init__(self, config: ShellGrammarConfig | Mapping[str, Any]):
        if not isinstance(config, ShellGrammarConfig):
            if not isinstance(config, Mapping):
                raise TypeError("config must be ShellGrammarConfig or a mapping")
            config = _config_from_mapping(config)
        self.config = config
        self._base_specs = self._make_specs(bundle=1, component_start=0)
        if config.closure_mode == "double_hopf":
            self._specs = self._base_specs + self._make_specs(
                bundle=2, component_start=len(self._base_specs)
            )
        else:
            self._specs = self._base_specs

    def _make_specs(self, *, bundle: int, component_start: int) -> tuple[ShellComponentSpec, ...]:
        specs: list[ShellComponentSpec] = []
        component = component_start
        if self.config.core_included:
            specs.append(
                ShellComponentSpec(
                    component=component,
                    bundle=bundle,
                    role="core",
                    shell_index=None,
                    strand_index=None,
                    radius=0.0,
                    population=None,
                    phase_offset=0.0,
                    strand_phase=0.0,
                    beta=0.0,
                )
            )
            component += 1
        for shell_index, (radius, population, offset, beta) in enumerate(
            zip(
                self.config.shell_radii,
                self.config.shell_populations,
                self.config.phase_offsets or (),
                self.config.pitch_modulations or (),
            ),
            start=1,
        ):
            for strand_index in range(population):
                specs.append(
                    ShellComponentSpec(
                        component=component,
                        bundle=bundle,
                        role="shell",
                        shell_index=shell_index,
                        strand_index=strand_index,
                        radius=radius,
                        population=population,
                        phase_offset=offset,
                        strand_phase=TWO_PI * strand_index / population,
                        beta=beta,
                    )
                )
                component += 1
        return tuple(specs)

    @property
    def component_specs(self) -> tuple[ShellComponentSpec, ...]:
        return self._specs

    @property
    def component_count(self) -> int:
        return len(self._specs)

    @property
    def Q(self) -> int:
        return self.config.Q

    @property
    def q(self) -> int:
        return self.Q

    @property
    def topology_label(self) -> str:
        if self.config.closure_mode == "double_hopf":
            return f"T({2 * self.Q},{2 * self.Q})"
        return f"T({self.Q},{self.Q})"

    def component_spec(self, component: int) -> ShellComponentSpec:
        if isinstance(component, (bool, np.bool_)):
            raise ValueError("component must be a valid integer index")
        try:
            index = int(component)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("component must be a valid integer index") from exc
        if index != component or not 0 <= index < self.component_count:
            raise IndexError(f"component index {component!r} out of range")
        return self._specs[index]

    @staticmethod
    def _validate_parameter_array(parameter: Any) -> np.ndarray:
        values = np.asarray(parameter, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("parameter values must be finite")
        return values

    def _base_values(
        self,
        parameter: Any,
        spec: ShellComponentSpec,
        *,
        order: int,
    ) -> np.ndarray:
        u = self._validate_parameter_array(parameter)
        if order not in {0, 1, 2}:
            raise ValueError("only derivatives of order 0, 1, and 2 are available")
        if spec.role == "core":
            radius = 0.0
            beta = 0.0
            phase = 0.0
        else:
            radius = spec.radius
            beta = spec.beta
            phase = spec.strand_phase + spec.phase_offset

        psi = u + beta * np.sin(u) - phase
        q = 1.0 + beta * np.cos(u)
        q_prime = -beta * np.sin(u)
        radial = self.config.major_radius + radius * np.cos(psi)
        radial_prime = -radius * np.sin(psi) * q
        radial_second = -radius * (np.cos(psi) * q * q + np.sin(psi) * q_prime)

        if order == 0:
            x = radial * np.cos(u)
            y = radial * np.sin(u)
            z = radius * np.sin(psi)
        elif order == 1:
            x = radial_prime * np.cos(u) - radial * np.sin(u)
            y = radial_prime * np.sin(u) + radial * np.cos(u)
            z = radius * np.cos(psi) * q
        else:
            x = radial_second * np.cos(u) - 2.0 * radial_prime * np.sin(u) - radial * np.cos(u)
            y = radial_second * np.sin(u) + 2.0 * radial_prime * np.cos(u) - radial * np.sin(u)
            z = radius * (-np.sin(psi) * q * q + np.cos(psi) * q_prime)
        return np.stack((x, y, z), axis=-1)

    def _transform(self, values: np.ndarray, *, bundle: int, order: int) -> np.ndarray:
        transformed = np.asarray(values, dtype=float)
        if bundle == 2:
            # P(x,y,z)=(R+x,-z,y).  Translation affects positions only.
            x = transformed[..., 0]
            y = transformed[..., 1]
            z = transformed[..., 2]
            if order == 0:
                transformed = np.stack((self.config.major_radius + x, -z, y), axis=-1)
            else:
                transformed = np.stack((x, -z, y), axis=-1)
        return apply_positive_axis_scaling(transformed, self.config.ambient_axis_scale)

    def evaluate(self, parameter: Any, component: int = 0) -> np.ndarray:
        """Evaluate one analytic component at scalar or array ``u``."""

        spec = self.component_spec(component)
        return self._transform(
            self._base_values(parameter, spec, order=0), bundle=spec.bundle, order=0
        )

    position = evaluate

    def derivative(self, parameter: Any, order: int = 1, component: int = 0) -> np.ndarray:
        """Evaluate an analytic first or second derivative."""

        spec = self.component_spec(component)
        return self._transform(
            self._base_values(parameter, spec, order=order), bundle=spec.bundle, order=order
        )

    def d1(self, parameter: Any, component: int = 0) -> np.ndarray:
        return self.derivative(parameter, order=1, component=component)

    def d2(self, parameter: Any, component: int = 0) -> np.ndarray:
        return self.derivative(parameter, order=2, component=component)

    def sample(
        self,
        sample_count: int = 128,
        *,
        include_endpoint: bool = False,
    ) -> list[np.ndarray]:
        """Sample every component; samples are diagnostic polygon vertices."""

        if isinstance(sample_count, (bool, np.bool_)) or int(sample_count) != sample_count:
            raise ValueError("sample_count must be an integer")
        sample_count = int(sample_count)
        if sample_count < 4:
            raise ValueError("sample_count must be at least four")
        parameters = np.linspace(0.0, TWO_PI, sample_count, endpoint=include_endpoint)
        return [self.evaluate(parameters, component=index) for index in range(self.component_count)]

    def sample_components(self, sample_count: int = 128, *, include_endpoint: bool = False) -> list[np.ndarray]:
        return self.sample(sample_count, include_endpoint=include_endpoint)

    def cross_section_points(self, parameter: float, *, bundle: int = 1) -> np.ndarray:
        """Return all one-bundle cross-sectional points at a longitude.

        The points are returned in core-first order when the core is enabled.
        This is a useful finite diagnostic for contact clustering; the
        analytic noncollision argument is independent of the sample grid.
        """

        if bundle not in {1, 2}:
            raise ValueError("bundle must be 1 or 2")
        if bundle == 2 and self.config.closure_mode != "double_hopf":
            raise ValueError("bundle 2 is available only in double_hopf mode")
        indices = [
            spec.component
            for spec in self._specs
            if spec.bundle == bundle
        ]
        return np.asarray([self.evaluate(parameter, component=index) for index in indices], dtype=float)

    def periodic_closure_report(self) -> dict[str, Any]:
        """Compare values and stored derivatives at the two period endpoints."""

        rows: list[dict[str, Any]] = []
        max_position = 0.0
        max_first = 0.0
        max_second = 0.0
        for spec in self._specs:
            position_error = float(np.max(np.abs(self.evaluate(TWO_PI, spec.component) - self.evaluate(0.0, spec.component))))
            first_error = float(np.max(np.abs(self.d1(TWO_PI, spec.component) - self.d1(0.0, spec.component))))
            second_error = float(np.max(np.abs(self.d2(TWO_PI, spec.component) - self.d2(0.0, spec.component))))
            max_position = max(max_position, position_error)
            max_first = max(max_first, first_error)
            max_second = max(max_second, second_error)
            rows.append(
                {
                    "component": spec.component,
                    "bundle": spec.bundle,
                    "role": spec.role,
                    "position_sup_norm_error": position_error,
                    "first_derivative_sup_norm_error": first_error,
                    "second_derivative_sup_norm_error": second_error,
                }
            )
        return {
            "analytic_periodic_formula": True,
            "period": TWO_PI,
            "max_position_sup_norm_error": max_position,
            "max_first_derivative_sup_norm_error": max_first,
            "max_second_derivative_sup_norm_error": max_second,
            "components": rows,
            "numeric_endpoint_comparison_is_diagnostic": True,
        }

    def noncollision_report(self) -> dict[str, Any]:
        """Record the constructive noncollision checks for the analytic family."""

        same_shell: list[dict[str, Any]] = []
        for shell_index, (radius, population) in enumerate(
            zip(self.config.shell_radii, self.config.shell_populations), start=1
        ):
            # For N=1 there is no distinct same-shell pair.  Positive counts
            # are permitted by the grammar, so report the vacuous case
            # explicitly rather than manufacturing a distance.
            separation = None if population == 1 else 2.0 * radius * math.sin(math.pi / population)
            same_shell.append(
                {
                    "shell_index": shell_index,
                    "population": population,
                    "minimum_same_shell_disk_separation": separation,
                    "positive_for_distinct_strands": population == 1 or bool(separation and separation > 0.0),
                }
            )
        radius_separations = [
            abs(left - right)
            for index, left in enumerate(self.config.shell_radii)
            for right in self.config.shell_radii[index + 1 :]
        ]
        min_radius_separation = min(radius_separations) if radius_separations else None
        double_core_distance = self.config.major_radius if self.config.closure_mode == "double_hopf" else None
        double_margin = (
            self.config.major_radius - 2.0 * self.config.r_max
            if self.config.closure_mode == "double_hopf"
            else None
        )
        return {
            "status": "PASS constructive analytic noncollision scope",
            "analytic_curve_only": True,
            "longitudinal_injectivity_reason": (
                "R>r_max keeps cylindrical radius positive, so equality of points "
                "forces equal longitude modulo 2*pi"
            ),
            "same_shell_common_rotation_reason": (
                "beta_i*sin(u) is common to one shell; equally spaced phases remain distinct"
            ),
            "distinct_radius_reason": "different positive |w| values cannot coincide in one normal disk",
            "same_shell_checks": same_shell,
            "minimum_distinct_shell_radius_gap": min_radius_separation,
            "core_shell_radius_gap": min(self.config.shell_radii) if self.config.core_included else None,
            "double_hopf_core_distance_lower_bound": double_core_distance,
            "double_hopf_tube_separation_margin_R_minus_2_r_max": double_margin,
            "positive_axis_scaling_is_invertible": all(value > 0.0 for value in self.config.ambient_axis_scale),
            "finite_sample_reach_or_isotopy_certificate": False,
            "thickness_claim": "none; this grammar does not implement an analytic reach bound",
        }

    def beta_homotopy(self, fraction: float) -> "ShellGrammar":
        """Return the member at ``fraction`` of the beta-to-zero homotopy."""

        fraction = _as_float(fraction, label="homotopy fraction")
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("homotopy fraction must lie in [0,1]")
        beta = tuple(float(fraction) * value for value in (self.config.pitch_modulations or ()))
        config = ShellGrammarConfig(
            major_radius=self.config.major_radius,
            shell_radii=self.config.shell_radii,
            shell_populations=self.config.shell_populations,
            phase_offsets=self.config.phase_offsets,
            pitch_modulations=beta,
            core_included=self.config.core_included,
            closure_mode=self.config.closure_mode,
            ambient_axis_scale=self.config.ambient_axis_scale,
            t_shells=self.config.T,
        )
        return ShellGrammar(config)

    def axis_scale_at(self, fraction: float) -> tuple[float, float, float]:
        """Return the positive diagonal isotopy from identity to the configured scale."""

        fraction = _as_float(fraction, label="axis-scale homotopy fraction")
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("axis-scale homotopy fraction must lie in [0,1]")
        return tuple(1.0 + fraction * (value - 1.0) for value in self.config.ambient_axis_scale)  # type: ignore[return-value]

    def to_record(
        self,
        sample_count: int = 0,
        *,
        include_endpoint: bool = False,
        include_derivatives: bool = False,
    ) -> dict[str, Any]:
        """Return configuration, formulas, topology scope, and optional samples."""

        if sample_count < 0:
            raise ValueError("sample_count must be nonnegative")
        samples = self.sample(sample_count, include_endpoint=include_endpoint) if sample_count else None
        derivative_first = None
        derivative_second = None
        if include_derivatives and sample_count:
            parameters = np.linspace(0.0, TWO_PI, int(sample_count), endpoint=include_endpoint)
            derivative_first = [self.d1(parameters, component=index).tolist() for index in range(self.component_count)]
            derivative_second = [self.d2(parameters, component=index).tolist() for index in range(self.component_count)]

        components: list[dict[str, Any]] = []
        for index, spec in enumerate(self._specs):
            row = spec.as_record()
            if spec.role == "core":
                row["exact_formula"] = "C(u)=E(u,0)=(R*cos(u),R*sin(u),0)"
            else:
                shell = int(spec.shell_index or 0)
                row["exact_formula"] = (
                    "E(u,w_ij(u)), w_ij(u)=r_i*exp(i*(u+beta_i*sin(u)-"
                    "(2*pi*j/N_i+phase_offset_i)))"
                )
                row["shell_formula_indices"] = {
                    "i": shell,
                    "j": int(spec.strand_index or 0),
                    "N_i": spec.population,
                }
            if samples is not None:
                row["sampled_coordinates"] = samples[index].tolist()
                row["sampled_coordinates_are_certificate"] = False
                if include_derivatives:
                    row["sampled_first_derivative"] = derivative_first[index]
                    row["sampled_second_derivative"] = derivative_second[index]
            components.append(row)

        return {
            "schema": SCHEMA,
            "configuration": self.config.as_record(),
            "exact_formula": {
                "normal_disk_embedding": (
                    "E(u,w)=((R+Re(w))*cos(u),(R+Re(w))*sin(u),Im(w))"
                ),
                "shell_point": (
                    "w_ij(u)=r_i*exp(i*(u+beta_i*sin(u)-phi_ij)), "
                    "phi_ij=2*pi*j/N_i+phase_offset_i"
                ),
                "core": "C(u)=E(u,0)",
                "proper_hopf_doubling": "P(x,y,z)=(R+x,-z,y), det(DP)=+1",
                "ambient_axis_scaling": "D(x,y,z)=(s_x*x,s_y*y,s_z*z), s_x,s_y,s_z>0",
                "parameter_period": "u modulo 2*pi",
            },
            "topology_scope": {
                "one_bundle_Q": self.Q,
                "single_bundle_full_twist": f"T({self.Q},{self.Q}) up to a common mirror",
                "double_bundle_full_twist": f"T({2 * self.Q},{2 * self.Q}) up to a common mirror",
                "selected_closure_mode": self.config.closure_mode,
                "selected_topology_label": self.topology_label,
                "mirror_convention": "up to a common mirror; no orientation sign is fixed by this grammar",
                "inherited_cabling_review": [
                    "proofs/ADVERSARIAL_REVIEW_001.md §3",
                    "proofs/ADVERSARIAL_REVIEW_002.md §5",
                ],
                "beta_homotopy": (
                    "beta_i is homotoped linearly to zero; radii stay distinct and "
                    "same-shell phase points undergo a common rotation"
                ),
                "positive_axis_scaling": (
                    "positive diagonal maps are orientation-preserving and isotopic "
                    "to identity through positive diagonal maps"
                ),
                "analytic_scope": "constructive full-twist/isotopy statement for finite smooth formulas",
                "sample_scope": "sampled polygons have no automatic reach or isotopy certificate",
                "thickness_scope": "no new analytic thickness or reach claim is implemented",
            },
            "free_fixed_unsupported": {
                "free_parameters": [
                    "T_shells / shell count",
                    "major radius R subject to inequalities",
                    "distinct positive shell radii r_i",
                    "positive shell populations N_i",
                    "phase offsets",
                    "shell pitch modulations beta_i",
                    "core_included",
                    "closure_mode",
                    "positive ambient axis scale",
                    "finite sample count",
                ],
                "fixed_by_grammar": [
                    "p=1 longitude u with period 2*pi",
                    "equally spaced phases 2*pi*j/N_i within each shell",
                    "normal-disk embedding E and optional proper map P",
                    "one common major radius for all shells",
                ],
                "unsupported_or_not_claimed": [
                    "optimization of beta, phases, radii, or populations",
                    "analytic reach/thickness certificate",
                    "automatic topology certification of sampled polygons",
                    "full finite-M ropelength bound",
                ],
            },
            "periodic_closure": self.periodic_closure_report(),
            "noncollision_scope": self.noncollision_report(),
            "components": components,
        }


def build_shell_grammar(config: ShellGrammarConfig | Mapping[str, Any]) -> ShellGrammar:
    """Build an analytic shell grammar from a config object or mapping."""

    return ShellGrammar(config)


def generate_shell_grammar(
    config: ShellGrammarConfig | Mapping[str, Any],
    *,
    sample_count: int = 0,
    include_endpoint: bool = False,
    include_derivatives: bool = False,
) -> dict[str, Any]:
    """Generate a JSON-ready record with optional finite coordinates."""

    return build_shell_grammar(config).to_record(
        sample_count,
        include_endpoint=include_endpoint,
        include_derivatives=include_derivatives,
    )


def write_shell_grammar(
    output_path: str | Path,
    config: ShellGrammarConfig | Mapping[str, Any] | ShellGrammar,
    *,
    sample_count: int = 128,
    include_endpoint: bool = False,
    include_derivatives: bool = False,
) -> dict[str, Any]:
    """Write one diagnostic grammar record as JSON and return it."""

    model = config if isinstance(config, ShellGrammar) else build_shell_grammar(config)
    record = model.to_record(
        sample_count,
        include_endpoint=include_endpoint,
        include_derivatives=include_derivatives,
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


# Descriptive aliases make the grammar discoverable to the numerical runners
# without duplicating implementation or hiding the canonical names above.
generate_shell_geometry = generate_shell_grammar
write_shell_geometry = write_shell_grammar


__all__ = [
    "SCHEMA",
    "ShellComponentSpec",
    "ShellGrammar",
    "ShellGrammarConfig",
    "apply_positive_axis_scaling",
    "build_shell_grammar",
    "generate_shell_geometry",
    "generate_shell_grammar",
    "write_shell_geometry",
    "write_shell_grammar",
]
