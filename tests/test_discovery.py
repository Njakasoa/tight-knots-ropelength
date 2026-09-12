"""Tests for the automated adjacent-shell phase discovery engine."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import numpy as np

from experiments.discover_phase_packing import read_m1_pass_gate
from src.discovery.phase_search import (
    arb_certify_pair,
    build_pair_spec,
    capacity_monotonicity_check,
    conservative_rounded_inputs,
    cross_shell_bound_components,
    cross_shell_lower_bound_sq,
    independent_grid_crosscheck,
    search_pair,
)


ROOT = Path(__file__).resolve().parents[1]


def test_m1_pass_gate_is_read_from_authoritative_review() -> None:
    gate = read_m1_pass_gate(ROOT / "benchmarks" / "M1_REVIEW.md")
    assert gate["passed"] is True
    assert gate["status"] == "PASS"


def test_pair_spec_obeys_closure_and_capacity_reuse_conditions() -> None:
    spec = build_pair_spec(8, Fraction(1, 2))
    assert spec.population >= 3
    assert spec.major_radius >= 2 * spec.b_at_upper + 2
    assert spec.b_at_upper <= spec.major_radius / 2
    assert capacity_monotonicity_check(spec.a, spec.b_at_upper, spec.major_radius)
    assert spec.capacity_b_at_upper >= spec.capacity_a


def test_stable_lower_bound_agrees_with_direct_subtraction_at_finite_scale() -> None:
    spec = build_pair_spec(32, Fraction(3, 4))
    components = cross_shell_bound_components(
        spec.a, spec.a + 1.83, spec.major_radius, spec.population, 0.37
    )
    u = components["U_ab"]
    v = components["V_hahb"]
    s_value = components["S"]
    sine_sq = components["sine_squared"]
    direct = (1.83**2) + 2.0 * (
        s_value - np.sqrt(s_value * s_value - 4.0 * u * v * sine_sq)
    )
    assert np.isclose(components["lower_bound_squared"], direct, rtol=1e-12, atol=1e-12)


def test_grid_crosscheck_has_explicit_phase_and_delta_observations() -> None:
    spec = build_pair_spec(8, Fraction(1, 2))
    grid = independent_grid_crosscheck(spec, grid_points=401)
    assert grid["phase_grid_includes_endpoints"] is True
    assert 0.0 <= grid["phase_fraction_min_observed"] <= 1.0
    assert spec.delta_lower <= grid["minimal_delta_observed"] <= spec.delta_upper
    assert grid["upper_endpoint_feasible_for_all_grid_phases"] is True
    assert grid["monotonicity_probe"]["passes_on_this_grid"] is True


def test_search_records_uniform_seeds_and_does_not_require_a_target_phase() -> None:
    spec = build_pair_spec(8, Fraction(1, 2))
    result = search_pair(
        spec,
        seed=19,
        de_maxiter=8,
        de_popsize=5,
        uniform_seed_count=5,
        grid_points=401,
        precision_bits=128,
        output_digits=25,
        certify=False,
    )
    selected = result["selected"]
    assert len(result["trials"]) >= 6
    assert len(result["optimizer"]["initial_seeds"]) == 5
    assert all(0.0 <= item["phase_fraction"] <= 1.0 for item in result["trials"])
    assert all(
        spec.delta_lower <= item["radial_gap_delta"] <= spec.delta_upper
        for item in result["trials"]
    )
    assert selected["feasible_with_1e-8_tolerance"] is True
    assert result["grid_crosscheck"]["upper_endpoint_feasible_for_all_grid_phases"] is True
    assert result["family_metadata"]["shell_count"] == 2
    assert result["family_metadata"]["Q_per_shell"] == spec.population
    assert result["family_metadata"]["winding"] == "fixed p=1 toroidal winding"
    assert "phase_fraction_f" in result["family_metadata"]["varied_fields"]
    assert result["family_metadata"]["pitch"].startswith("fixed")


def test_arb_certificate_proves_a_rounded_finite_pair_margin() -> None:
    spec = build_pair_spec(8, Fraction(1, 2))
    phase, delta = conservative_rounded_inputs(0.37, 2.0, places=8, padding_ticks=1)
    certificate = arb_certify_pair(
        spec,
        phase_fraction=phase,
        radial_gap=delta,
        precision_bits=160,
        output_digits=25,
    )
    assert certificate["status"] == "PASS"
    assert certificate["expected_population_rule_matches"] is True
    assert certificate["outer_population_is_at_least_inner"] is True
    assert certificate["capacity_monotonicity_certified"] is True
    assert certificate["closure_condition"]["passes"] is True
    assert int(certificate["constraint_margin_squared"]["lower"]["numerator"])


def test_cross_shell_bound_feasible_at_safe_two_unit_gap() -> None:
    spec = build_pair_spec(8, Fraction(1, 4))
    lower_sq = cross_shell_lower_bound_sq(
        spec.a, spec.a + 2.0, spec.major_radius, spec.population, 0.13
    )
    assert lower_sq >= 4.0 - 1e-12
