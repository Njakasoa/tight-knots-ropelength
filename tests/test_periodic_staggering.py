"""Falsification tests for generalized staggering and its all-pairs verifier."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import math

import numpy as np
import pytest
from scipy.integrate import quad

from src.discovery.periodic_staggering import (
    certify_geometry, certify_nonuniform, exact_period_mean, flat_gap,
    grid_phase_distance, periodic_grid_search, propose_nonuniform, propose_periodic,
)


def test_lcm_phase_reduction_against_explicit_component_enumeration():
    for n, m in product(range(3, 15), repeat=2):
        a, b = Fraction(2, 17), Fraction(3, 23)
        differences = [(a + Fraction(j, n) - b - Fraction(k, m)) % 1
                       for j in range(n) for k in range(m)]
        brute = min(min(x, 1 - x) for x in differences)
        assert grid_phase_distance(n, a, m, b) == brute


@pytest.mark.parametrize("p", range(1, 17))
def test_cycle_closure_and_all_period_formula(p):
    r = periodic_grid_search(p, 60)
    phases = [Fraction(x) for x in r["phases_including_closure"]]
    assert len(phases) == p + 1 and phases[0] == phases[-1] == 0
    assert abs(r["mean_gap"] - exact_period_mean(p)) < 2e-14
    independent_cost = sum(2 * math.sqrt(1 - min((a-b) % 1, (b-a) % 1)**2)
                           for a, b in zip(phases, phases[1:])) / p
    assert abs(independent_cost - r["mean_gap"]) < 2e-14


def test_dynamic_program_against_exhaustive_cycles():
    for p in [3, 4, 5]:
        best = float("inf")
        for middle in product(range(8), repeat=p-1):
            phases = np.array([0, *middle, 0]) / 8
            best = min(best, float(np.sum(flat_gap(np.diff(phases))) / p))
        assert abs(periodic_grid_search(p, 8)["mean_gap"] - best) < 1e-14


@pytest.mark.parametrize("p", [3, 4, 5, 7, 12])
def test_full_finite_periodic_construction(p):
    for pattern in ["optimized", "constant_step", "equally_spaced"]:
        q = propose_periodic(p, pattern=pattern)
        c = certify_geometry(q)
        assert c["status"] == "PASS"
        assert c["phase_pair_checks"] + c["radial_pair_checks"] == 36 * 35 // 2


def test_nonadjacent_collision_is_rejected_despite_good_adjacent_pairs():
    proposal = {"R": "100", "radii": ["10", "52/5", "54/5"],
                "populations": [3, 3, 3], "offsets_turns": ["0", "1/6", "0"]}
    with pytest.raises(ValueError, match="cross-shell.*0,2"):
        certify_geometry(proposal)


@pytest.fixture(scope="module")
def finite():
    p = propose_nonuniform(9)
    return p, certify_nonuniform(p, angular_cells=512)


def endpoint(record, side):
    r = record[side]
    return Fraction(int(r["numerator"]), int(r["denominator"]))


def test_same_M_strict_improvement_with_independent_length_quadrature(finite):
    p, c = finite
    assert c["M"] == 356
    assert endpoint(c["length_reduction"], "lower") > 0
    R = float(Fraction(p["R"]))
    total = 4 * math.pi * R
    for r, n in zip(p["radii"], p["populations"]):
        radius = float(Fraction(r))
        value, _ = quad(lambda t: math.hypot(R + radius * math.cos(t), radius),
                        0, 2 * math.pi, epsabs=1e-9, epsrel=1e-12)
        total += 2 * n * value
    assert float(endpoint(c["nonuniform_length"], "lower")) < total
    assert total < float(endpoint(c["nonuniform_length"], "upper"))
    assert c["phase_pair_checks"] + c["radial_pair_checks"] == 36


@pytest.mark.parametrize("kind", ["phase", "radius", "population", "closure", "dimension"])
def test_tampering_is_rejected(finite, kind):
    p = deepcopy(finite[0])
    if kind == "phase":
        p["offsets_turns"][1] = "0"
    elif kind == "radius":
        p["radii"][1] = "201/100"
    elif kind == "population":
        p["populations"][1] = 1000000
    elif kind == "closure":
        p["R"] = "20"
    else:
        p["radii"].pop()
    with pytest.raises(ValueError):
        certify_nonuniform(p, angular_cells=64)


def test_general_harmonic_bound_against_actual_toroidal_distances():
    rng = np.random.default_rng(1789)
    def F(r, R, t, phase):
        return np.array([(R+r*math.cos(t))*math.cos(t+phase),
                         (R+r*math.cos(t))*math.sin(t+phase), r*math.sin(t)])
    for _ in range(500):
        a, b = sorted(rng.uniform(2, 25, 2))
        R = 2*b+2
        t, s, phase = rng.uniform(0, 2*math.pi, 3)
        u, v = a*b, (R-a)*(R-b)
        lower = (a-b)**2 + 4*u*v/(u+v)*math.sin(phase/2)**2
        d = F(a, R, t, 0) - F(b, R, s, phase)
        assert np.dot(d, d) >= lower - 1e-9
