"""Focused tests for the Arb certificate and finite shell reproduction."""

from __future__ import annotations

import json

from src.certification.arb_backend import arb, arb_precision, arb_record, validate_backend
from src.certification.integrals import certify_integrals, midpoint_error
from src.certification.shell_family import (
    certified_floor,
    finite_family_record,
    populations_for_t,
    staggered_family_record,
    staggered_populations_for_t,
    write_sampled_geometry,
)


def test_arb_backend_endpoint_contract() -> None:
    evidence = validate_backend()
    assert evidence["backend"] == "python-flint Arb"
    assert evidence["checks"]["directed_lower_upper"]
    assert evidence["checks"]["exact_fmpq_endpoints"]
    with arb_precision(128):
        value = arb(1) / arb(3)
        record = arb_record(value, digits=30)
        assert int(record["lower"]["numerator"]) * int(record["upper"]["denominator"]) <= int(
            record["upper"]["numerator"]
        ) * int(record["lower"]["denominator"])


def test_midpoint_error_expression_is_arb_and_positive() -> None:
    with arb_precision(192):
        error = midpoint_error(256, 512)
        assert error.lower() > arb(0)
        # This is the analytic E from the proof note, not a floating-point
        # regression target.  The rational decimal threshold is only a sanity
        # check that the requested mesh is in the intended scale.
        assert error.upper() < arb("0.005")


def test_default_certificate_clears_requested_threshold() -> None:
    result = certify_integrals(256, 512, precision_bits=192, output_digits=40)
    assert result["alpha_upper_lt_11_407"] is True
    assert result["q0_exact_expression"] == "pi*(3*asinh(1)/sqrt(2)-1)"
    assert result["method"]["derivative_bounds"] == {"abs_f_xx": "600", "abs_f_tt": "60"}
    assert result["l0"]["lower"]["numerator"]
    assert result["l0"]["upper"]["denominator"]


def test_capacity_floor_is_certified_without_float_rounding() -> None:
    with arb_precision(192):
        value = arb("5.61985178483258111452509971456")
        assert certified_floor(value, label="test capacity") == 5


def test_shell_specific_has_at_least_common_population() -> None:
    specific = populations_for_t(8, mode="shell_specific", precision_bits=192)
    common = populations_for_t(8, mode="common_hole", precision_bits=192)
    assert all(a.population >= b.population for a, b in zip(specific, common))
    assert all(item.population >= 3 for item in specific)
    assert 1 + sum(item.population for item in specific) > 1 + sum(item.population for item in common)


def test_finite_record_and_proper_rotation_geometry(tmp_path) -> None:
    record = finite_family_record(2, angular_cells=32, precision_bits=128, output_digits=30)
    assert record["family"]["component_topology"] == "T(30,30)"
    assert record["family"]["proper_rotation"].startswith("P(x,y,z)")
    assert record["published_model_references"]["Klotz_13_38"]["coefficient"] == "13.38"
    assert record["published_model_references"]["Klotz_11_68"]["status"].startswith("conditional")

    geometry_path = tmp_path / "geometry.json"
    populations = populations_for_t(1, mode="shell_specific", precision_bits=128)
    write_sampled_geometry(geometry_path, 1, populations, parameter_count=8)
    geometry = json.loads(geometry_path.read_text(encoding="utf-8"))
    assert geometry["geometry"]["sampled_coordinates_are_certificate"] is False
    core1 = geometry["components"][0]["sampled_coordinates"][0]
    core2 = next(
        component["sampled_coordinates"][0]
        for component in geometry["components"]
        if component["bundle"] == 2 and component["role"] == "core"
    )
    assert core1 == [6.0, 0.0, 0.0]
    assert core2 == [12.0, 0.0, 0.0]


def test_staggered_blocks_use_reviewed_indexing_and_half_phase() -> None:
    with arb_precision(192):
        major_radius, populations = staggered_populations_for_t(4, precision_bits=192)
        assert populations[0].block_start == 1
        assert populations[1].block_start == 1
        assert populations[2].block_start == 3
        assert populations[0].population == populations[1].population
        assert populations[0].phase_offset == arb(0)
        assert populations[1].phase_offset > arb(0)
        assert major_radius > arb(16)
    record = staggered_family_record(4, angular_cells=32, precision_bits=128, output_digits=30)
    assert record["family"]["component_topology"] == "T(82,82)"
    assert record["family"]["radial_gap_within_block"] == "sqrt(3)"
    assert record["populations"][1]["phase_offset"]["upper"]["numerator"]
