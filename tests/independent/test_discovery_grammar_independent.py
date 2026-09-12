"""Independent checks for the variable-pitch shell discovery grammar.

The test reference below is written from the coordinate definitions rather
than calling the generator's derivative implementation.  Finite differences
of sampled positions provide a second check on both derivative orders.  The
tests cover the smooth construction hypotheses and deliberately keep sampled
polygons separate from any claim about reach, thickness, or isotopy.
"""

from __future__ import annotations

import importlib
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pytest

from src.discovery.grammar import (
    ShellGrammarConfig,
    apply_positive_axis_scaling,
    build_shell_grammar,
)
from src.curves.vect import read_vect


ROOT = Path(__file__).resolve().parents[2]


def _config(
    *,
    closure_mode: str = "double_hopf",
    phase_offsets: tuple[float, ...] = (0.17, -0.63, 1.11),
    pitch_modulations: tuple[float, ...] = (0.43, -1.37, 2.15),
    ambient_axis_scale: tuple[float, float, float] = (1.23, 0.81, 1.47),
) -> ShellGrammarConfig:
    return ShellGrammarConfig(
        major_radius=8.7,
        shell_radii=(0.9, 1.8, 2.6),
        shell_populations=(2, 3, 4),
        phase_offsets=phase_offsets,
        pitch_modulations=pitch_modulations,
        core_included=True,
        closure_mode=closure_mode,
        ambient_axis_scale=ambient_axis_scale,
    )


def _reference_position(
    config: ShellGrammarConfig,
    *,
    bundle: int,
    role: str,
    radius: float,
    phase: float,
    beta: float,
    u: float | np.ndarray,
) -> np.ndarray:
    """Independent coordinate formula from the grammar's definition."""

    parameter = np.asarray(u, dtype=float)
    if role == "core":
        radius = 0.0
        phase = 0.0
        beta = 0.0
    psi = parameter + beta * np.sin(parameter) - phase
    radial = config.major_radius + radius * np.cos(psi)
    values = np.stack(
        (radial * np.cos(parameter), radial * np.sin(parameter), radius * np.sin(psi)),
        axis=-1,
    )
    if bundle == 2:
        x, y, z = (values[..., index] for index in range(3))
        values = np.stack((config.major_radius + x, -z, y), axis=-1)
    return values * np.asarray(config.ambient_axis_scale, dtype=float)


def _reference_for_component(model, component: int, u: float | np.ndarray) -> np.ndarray:
    spec = model.component_spec(component)
    phase = spec.strand_phase + spec.phase_offset if spec.role == "shell" else 0.0
    return _reference_position(
        model.config,
        bundle=spec.bundle,
        role=spec.role,
        radius=spec.radius,
        phase=phase,
        beta=spec.beta,
        u=u,
    )


def _finite_first(model, component: int, u: float, h: float = 1.0e-4) -> np.ndarray:
    values = [model.evaluate(u + offset * h, component=component) for offset in (-2, -1, 1, 2)]
    return (values[0] - 8.0 * values[1] + 8.0 * values[2] - values[3]) / (12.0 * h)


def _finite_second(model, component: int, u: float, h: float = 2.5e-3) -> np.ndarray:
    values = [model.evaluate(u + offset * h, component=component) for offset in (-2, -1, 0, 1, 2)]
    return (-values[0] + 16.0 * values[1] - 30.0 * values[2] + 16.0 * values[3] - values[4]) / (12.0 * h * h)


def _minimum_pair_distance(points: np.ndarray) -> float:
    minimum = float("inf")
    for i in range(len(points)):
        for j in range(i):
            minimum = min(minimum, float(np.linalg.norm(points[i] - points[j])))
    return minimum


def test_coordinate_formula_and_analytic_derivatives_match_independent_references() -> None:
    model = build_shell_grammar(_config())
    parameters = np.array([0.173, 1.207, 2.631, 4.811, 6.021])
    for component in range(model.component_count):
        np.testing.assert_allclose(
            model.evaluate(parameters, component=component),
            _reference_for_component(model, component, parameters),
            rtol=0.0,
            atol=2.0e-13,
        )
    for component in (0, 1, 5, 10, 16, 19):
        for parameter in (0.173, 1.207, 2.631, 4.811):
            first_error = np.max(np.abs(model.d1(parameter, component=component) - _finite_first(model, component, parameter)))
            second_error = np.max(np.abs(model.d2(parameter, component=component) - _finite_second(model, component, parameter)))
            assert first_error < 2.0e-7, (component, parameter, first_error)
            assert second_error < 2.0e-5, (component, parameter, second_error)


def test_periodicity_and_regular_longitude_hold_for_large_nonmonotone_pitch() -> None:
    model = build_shell_grammar(_config(pitch_modulations=(2.7, -4.2, 7.5)))
    closure = model.periodic_closure_report()
    assert closure["analytic_periodic_formula"] is True
    assert closure["max_position_sup_norm_error"] < 2.0e-13
    assert closure["max_first_derivative_sup_norm_error"] < 2.0e-12
    assert closure["max_second_derivative_sup_norm_error"] < 2.0e-11
    # The independent formula has a positive cylindrical-radius margin, which
    # is the hypothesis used to recover longitude modulo 2*pi.
    assert model.config.major_radius - model.config.r_max > 0.0
    for parameter in np.linspace(0.0, 2.0 * math.pi, 13, endpoint=False):
        points = np.asarray([model.evaluate(parameter, component=i) for i in range(model.component_count)])
        assert _minimum_pair_distance(points) > 1.0e-6


def test_beta_phase_and_positive_scale_homotopies_preserve_configuration_separation() -> None:
    base = _config()
    model = build_shell_grammar(base)
    assert model.topology_label == "T(20,20)"
    report = model.noncollision_report()
    assert report["analytic_curve_only"] is True
    assert report["finite_sample_reach_or_isotopy_certificate"] is False
    assert report["positive_axis_scaling_is_invertible"] is True
    assert report["double_hopf_core_distance_lower_bound"] == base.major_radius
    assert report["double_hopf_tube_separation_margin_R_minus_2_r_max"] > 0.0
    for fraction in np.linspace(0.0, 1.0, 5):
        beta_model = model.beta_homotopy(float(fraction))
        assert beta_model.config.phase_offsets == base.phase_offsets
        assert beta_model.config.pitch_modulations == tuple(fraction * value for value in base.pitch_modulations)
        for parameter in (0.0, 0.71, 2.4, 5.9):
            points = beta_model.cross_section_points(parameter, bundle=1)
            assert _minimum_pair_distance(points) > 1.0e-6
    # Phase offsets may be moved shell by shell through the same distinct
    # disk-point configurations; test that path independently of beta_homotopy.
    for fraction in np.linspace(0.0, 1.0, 5):
        phase_model = build_shell_grammar(
            ShellGrammarConfig(
                major_radius=base.major_radius,
                shell_radii=base.shell_radii,
                shell_populations=base.shell_populations,
                phase_offsets=tuple(fraction * value for value in base.phase_offsets),
                pitch_modulations=base.pitch_modulations,
                core_included=base.core_included,
                closure_mode=base.closure_mode,
                ambient_axis_scale=base.ambient_axis_scale,
            )
        )
        assert _minimum_pair_distance(phase_model.cross_section_points(1.2, bundle=1)) > 1.0e-6
    for fraction in np.linspace(0.0, 1.0, 5):
        scaled = model.axis_scale_at(float(fraction))
        assert all(value > 0.0 for value in scaled)
        scaled_model = build_shell_grammar(
            ShellGrammarConfig(
                major_radius=base.major_radius,
                shell_radii=base.shell_radii,
                shell_populations=base.shell_populations,
                phase_offsets=base.phase_offsets,
                pitch_modulations=base.pitch_modulations,
                core_included=base.core_included,
                closure_mode=base.closure_mode,
                ambient_axis_scale=scaled,
            )
        )
        assert _minimum_pair_distance(scaled_model.cross_section_points(2.7, bundle=1)) > 1.0e-6


def test_proper_hopf_motion_and_component_accounting_are_independent_checks() -> None:
    config = _config(ambient_axis_scale=(1.0, 1.0, 1.0))
    model = build_shell_grammar(config)
    assert model.Q == 10
    assert model.component_count == 20
    assert [spec.bundle for spec in model.component_specs[:10]] == [1] * 10
    assert [spec.bundle for spec in model.component_specs[10:]] == [2] * 10
    linear_part = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])
    assert np.isclose(np.linalg.det(linear_part), 1.0, rtol=0.0, atol=1.0e-14)
    first_core = np.asarray([model.evaluate(u, component=0) for u in np.linspace(0.0, 2.0 * math.pi, 129)])
    second_core = np.asarray([model.evaluate(v, component=10) for v in np.linspace(0.0, 2.0 * math.pi, 129)])
    distances = np.linalg.norm(first_core[:, None, :] - second_core[None, :, :], axis=-1)
    assert float(np.min(distances)) >= config.major_radius - 1.0e-12
    assert model.topology_label == "T(20,20)"
    single = build_shell_grammar(
        ShellGrammarConfig(
            major_radius=config.major_radius,
            shell_radii=config.shell_radii,
            shell_populations=config.shell_populations,
            phase_offsets=config.phase_offsets,
            pitch_modulations=config.pitch_modulations,
            core_included=config.core_included,
            closure_mode="single_torus",
            ambient_axis_scale=config.ambient_axis_scale,
        )
    )
    assert single.component_count == single.Q == 10
    assert single.topology_label == "T(10,10)"


def test_mapping_aliases_and_record_scope_are_explicit() -> None:
    model = build_shell_grammar(
        {
            "T": 3,
            "R": 8.7,
            "shell_radii": (0.9, 1.8, 2.6),
            "shell_populations": (2, 3, 4),
            "phase_offsets": (0.17, -0.63, 1.11),
            "pitch_modulations": (0.43, -1.37, 2.15),
            "core_included": True,
            "closure": "double",
            "axis_scale": (1.23, 0.81, 1.47),
        }
    )
    record = model.to_record(sample_count=8, include_endpoint=False, include_derivatives=True)
    assert record["schema"] == "periodic-variable-pitch-shell-grammar-v1"
    assert record["configuration"]["T_shells"] == 3
    assert record["topology_scope"]["selected_topology_label"] == "T(20,20)"
    assert record["topology_scope"]["sample_scope"].startswith("sampled polygons")
    assert record["topology_scope"]["thickness_scope"].startswith("no new")
    assert all(component["sampled_coordinates_are_certificate"] is False for component in record["components"])


def test_search_script_uses_valid_variable_pitch_family_without_solver_assumptions() -> None:
    search = importlib.import_module("experiments.search_variable_pitch")
    parameters = np.array([6.4, 1.2, 0.55, -0.42, 0.37, 1.18])
    config = search.config(parameters)
    assert config.closure_mode == "double_hopf"
    assert config.shell_populations == (2, 3)
    assert config.pitch_modulations == (0.55, -0.42)
    assert config.major_radius > 2.0 * max(config.shell_radii)
    samples = search.sample(parameters, 24)
    assert len(samples) == 12
    assert all(array.shape == (24, 3) and np.all(np.isfinite(array)) for array in samples)
    assert "not a certified smooth bound" in (ROOT / "experiments" / "search_variable_pitch.py").read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        search.config([math.nan, 1.2, 0.55, -0.42, 0.37, 1.18])


def _read_tsv_components(path: Path) -> list[np.ndarray]:
    """Read the atlas TSV independently of the production VECT reader."""

    components: list[list[list[float]]] = [[]]
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            if components[-1]:
                components.append([])
            continue
        values = [float(token) for token in stripped.split()]
        assert len(values) == 3
        components[-1].append(values)
    if components and not components[-1]:
        components.pop()
    return [np.asarray(component, dtype=float) for component in components]


def test_canonical_zero_colour_atlas_vect_matches_its_tsv_coordinates() -> None:
    vect_path = ROOT / "data" / "reference" / "cantarella-atlas" / "knots" / "prime" / "3-10" / "3_1.vect"
    tsv_path = vect_path.with_suffix(".tsv")
    link = read_vect(vect_path)
    tsv_components = _read_tsv_components(tsv_path)
    assert link.component_count == len(tsv_components) == 1
    assert link.components[0].colors is None
    assert link.components[0].closed is True
    assert link.components[0].vertex_count == len(tsv_components[0]) == 2400
    np.testing.assert_array_equal(link.components[0].vertices, tsv_components[0])
    conversion = json.loads(
        (vect_path.parents[3] / "VECT_CONVERSION.json").read_text(encoding="utf-8")
    )
    expected = next(item["sha256"] for item in conversion if item["output"] == str(vect_path.relative_to(ROOT)))
    assert hashlib.sha256(vect_path.read_bytes()).hexdigest() == expected


@pytest.mark.parametrize(
    "bad_config",
    [
        {"major_radius": 2.0, "shell_radii": (2.0,), "shell_populations": (1,)},
        {"major_radius": 9.0, "shell_radii": (1.0, 1.0), "shell_populations": (1, 1)},
        {"major_radius": 9.0, "shell_radii": (1.0,), "shell_populations": (0,)},
        {"major_radius": 9.0, "shell_radii": (1.0,), "shell_populations": (1,), "ambient_axis_scale": (1.0, 0.0, 1.0)},
        {"major_radius": 4.0, "shell_radii": (2.1,), "shell_populations": (1,), "closure_mode": "double_hopf"},
        {"major_radius": 9.0, "shell_radii": (1.0,), "shell_populations": (1,), "closure_mode": "not_a_closure"},
        {"major_radius": 9.0, "shell_radii": (1.0,), "shell_populations": (1,), "t_shells": 2},
    ],
)
def test_configuration_failure_paths_remain_rejected(bad_config: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        ShellGrammarConfig(**bad_config)


def test_runtime_failure_paths_are_rejected_without_silent_geometry_changes() -> None:
    model = build_shell_grammar(_config())
    with pytest.raises((IndexError, ValueError)):
        model.component_spec(-1)
    with pytest.raises(ValueError):
        model.component_spec(True)
    with pytest.raises(ValueError):
        model.evaluate(float("nan"), component=0)
    with pytest.raises(ValueError):
        model.derivative(0.2, order=3, component=0)
    with pytest.raises(ValueError):
        model.sample(3)
    with pytest.raises(ValueError):
        model.beta_homotopy(-0.01)
    with pytest.raises(ValueError):
        model.axis_scale_at(1.01)
    with pytest.raises(ValueError):
        model.cross_section_points(0.2, bundle=3)
    single = build_shell_grammar(_config(closure_mode="single_torus"))
    with pytest.raises(ValueError):
        single.cross_section_points(0.2, bundle=2)
    with pytest.raises(ValueError):
        apply_positive_axis_scaling(np.zeros((2, 2)), scales=(1.0, 1.0, 1.0))
    with pytest.raises(ValueError):
        apply_positive_axis_scaling(np.zeros((2, 3)), scales=(1.0, -1.0, 1.0))
