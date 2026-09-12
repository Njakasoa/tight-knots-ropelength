"""Focused tests for the configurable variable-pitch shell grammar."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from src.discovery.grammar import (
    ShellGrammar,
    ShellGrammarConfig,
    apply_positive_axis_scaling,
    build_shell_grammar,
    generate_shell_grammar,
    write_shell_grammar,
)


def _single_config(**overrides) -> ShellGrammarConfig:
    values = {
        "major_radius": 9.0,
        "shell_radii": (1.0, 2.5),
        "shell_populations": (3, 4),
        "phase_offsets": (0.17, -0.31),
        "pitch_modulations": (0.23, -0.37),
        "core_included": True,
        "closure_mode": "single_torus",
        "ambient_axis_scale": (1.2, 0.8, 1.1),
    }
    values.update(overrides)
    return ShellGrammarConfig(**values)


def test_periodic_closure_and_analytic_derivatives() -> None:
    model = build_shell_grammar(_single_config())
    assert model.config.T == 2
    assert model.Q == 8  # core + 3 + 4 strands
    assert model.component_count == 8

    closure = model.periodic_closure_report()
    assert closure["analytic_periodic_formula"] is True
    assert closure["max_position_sup_norm_error"] < 2e-13
    assert closure["max_first_derivative_sup_norm_error"] < 2e-12
    assert closure["max_second_derivative_sup_norm_error"] < 2e-11

    u = 0.713
    h = 1e-6
    finite_difference = (
        model.evaluate(u + h, component=2) - model.evaluate(u - h, component=2)
    ) / (2.0 * h)
    assert np.allclose(finite_difference, model.d1(u, component=2), rtol=1e-9, atol=1e-8)


def test_beta_zero_agrees_with_independent_normal_disk_formula() -> None:
    config = _single_config(
        major_radius=8.0,
        shell_radii=(2.0,),
        shell_populations=(3,),
        phase_offsets=(0.37,),
        pitch_modulations=(0.0,),
        core_included=False,
        ambient_axis_scale=(1.0, 1.0, 1.0),
    )
    model = ShellGrammar(config)
    u = np.array([0.0, 0.21, 1.4, 2.0 * math.pi - 0.11])
    strand = 1
    phase = 2.0 * math.pi * strand / 3.0 + 0.37
    cross_section_angle = u - phase
    expected = np.stack(
        (
            (8.0 + 2.0 * np.cos(cross_section_angle)) * np.cos(u),
            (8.0 + 2.0 * np.cos(cross_section_angle)) * np.sin(u),
            2.0 * np.sin(cross_section_angle),
        ),
        axis=-1,
    )
    assert np.allclose(model.evaluate(u, component=strand), expected, rtol=0.0, atol=2e-14)


def test_beta_homotopy_preserves_periodicity_and_cross_section_noncollision() -> None:
    model = build_shell_grammar(_single_config(ambient_axis_scale=(1.0, 1.0, 1.0)))
    for fraction in (0.0, 0.25, 0.75, 1.0):
        member = model.beta_homotopy(fraction)
        assert member.periodic_closure_report()["max_position_sup_norm_error"] < 2e-13
        points = member.cross_section_points(1.17)
        pairwise = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
        positive_off_diagonal = pairwise[np.triu_indices_from(pairwise, k=1)]
        assert np.all(positive_off_diagonal > 1e-10)
        assert member.noncollision_report()["status"].startswith("PASS")


def test_double_hopf_is_proper_and_positive_scaling_preserves_coordinates_relation() -> None:
    config = _single_config(
        major_radius=8.0,
        closure_mode="double_hopf",
        ambient_axis_scale=(1.3, 0.7, 1.1),
    )
    model = ShellGrammar(config)
    assert model.Q == 8
    assert model.component_count == 16
    assert model.topology_label == "T(16,16)"
    assert model.noncollision_report()["double_hopf_tube_separation_margin_R_minus_2_r_max"] == 3.0

    # Undo the configured positive scaling to test the exact rigid-motion
    # relation P between corresponding unscaled bundle components.
    scale = np.asarray(config.ambient_axis_scale)
    for index in range(model.Q):
        first = model.evaluate(0.83, component=index) / scale
        second = model.evaluate(0.83, component=index + model.Q) / scale
        expected = np.array([config.major_radius + first[0], -first[2], first[1]])
        assert np.allclose(second, expected, rtol=0.0, atol=2e-13)


def test_record_contains_coordinates_formula_scope_and_free_fixed_registry(tmp_path: Path) -> None:
    config = _single_config(closure_mode="double_hopf")
    record = generate_shell_grammar(config, sample_count=8, include_endpoint=True, include_derivatives=True)
    assert record["schema"].startswith("periodic-variable-pitch-shell-grammar")
    assert record["configuration"]["T_shells"] == 2
    assert record["exact_formula"]["shell_point"].startswith("w_ij(u)=")
    assert record["topology_scope"]["single_bundle_full_twist"] == "T(8,8) up to a common mirror"
    assert record["topology_scope"]["double_bundle_full_twist"] == "T(16,16) up to a common mirror"
    assert "proofs/ADVERSARIAL_REVIEW_001.md §3" in record["topology_scope"]["inherited_cabling_review"]
    assert record["topology_scope"]["sample_scope"].startswith("sampled polygons")
    assert "shell pitch modulations beta_i" in record["free_fixed_unsupported"]["free_parameters"]
    assert "analytic reach/thickness certificate" in record["free_fixed_unsupported"]["unsupported_or_not_claimed"]
    assert len(record["components"]) == 16
    assert len(record["components"][0]["sampled_coordinates"]) == 8
    assert record["components"][0]["sampled_coordinates_are_certificate"] is False
    assert len(record["components"][0]["sampled_first_derivative"]) == 8

    path = tmp_path / "grammar.json"
    written = write_shell_grammar(path, config, sample_count=6)
    assert json.loads(path.read_text(encoding="utf-8"))["configuration"] == written["configuration"]


def test_mapping_aliases_and_scaling_validation() -> None:
    model = build_shell_grammar(
        {
            "T": 1,
            "R": 7,
            "shell_radii": [2],
            "shell_populations": [3],
            "closure": "single-torus",
            "axis_scale": [2, 3, 4],
        }
    )
    assert model.config.T == 1
    assert np.allclose(model.evaluate(0.0, component=1), apply_positive_axis_scaling([9.0, 0.0, 0.0], [2, 3, 4]))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"shell_radii": (1.0, 1.0), "shell_populations": (3, 4)},
        {"major_radius": 2.0, "shell_radii": (2.0,), "shell_populations": (3,)},
        {"shell_radii": (1.0, 2.0), "shell_populations": (3,)},
        {"shell_radii": (1.0,), "shell_populations": (0,)},
        {"shell_radii": (1.0,), "shell_populations": (3,), "phase_offsets": (0.0, 0.1)},
        {"shell_radii": (1.0,), "shell_populations": (3,), "pitch_modulations": (float("nan"),)},
        {"shell_radii": (1.0,), "shell_populations": (3,), "ambient_axis_scale": (1.0, 0.0, 1.0)},
        {
            "major_radius": 3.0,
            "shell_radii": (2.0,),
            "shell_populations": (3,),
            "closure_mode": "double_hopf",
        },
    ],
)
def test_malformed_configurations_are_rejected(kwargs) -> None:
    values = {
        "major_radius": 9.0,
        "shell_radii": (1.0, 2.5),
        "shell_populations": (3, 4),
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        ShellGrammarConfig(**values)
