"""Meaningful smoke and positive-control tests for the independent engine."""

from __future__ import annotations

import math
from decimal import Decimal

import numpy as np

from contacts import extract_contacts
from curves import circle, hopf_link, read_vect, torus_link, write_vect
from curves.exact import machin_pi_interval
from thickness import polygon_thickness, smooth_thickness
from topology import linking_matrix, topology_report, torus_invariants


def test_circle_analytic_derivatives_and_length():
    curve = circle()
    assert np.allclose(curve.evaluate(0.0), [1.0, 0.0, 0.0])
    assert np.allclose(curve.d1(0.0), [0.0, 1.0, 0.0])
    assert np.allclose(curve.d2(0.0), [-1.0, 0.0, 0.0])
    assert math.isclose(curve.length(), 2.0 * math.pi, rel_tol=0, abs_tol=1e-14)
    diagnostic = smooth_thickness(curve, samples=16)
    assert math.isclose(diagnostic.curvature_radius, 1.0, rel_tol=1e-12)
    assert math.isclose(diagnostic.dcsd, 2.0, rel_tol=1e-10)
    assert math.isclose(diagnostic.thickness, 1.0, rel_tol=1e-10)
    assert not diagnostic.complete


def test_polygon_checker_ignores_adjacent_edges():
    square = np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [-1.0, -1.0, 0.0], [1.0, -1.0, 0.0]])
    result = polygon_thickness(square, include_rejected=True)
    # Rawdon MinRad uses the shorter adjacent edge and tangent-disk angle.
    assert math.isclose(result.minrad, 1.0, rel_tol=1e-12)
    assert math.isclose(result.dcsd, 2.0, rel_tol=1e-12)
    assert math.isclose(result.thickness, 1.0, rel_tol=1e-12)
    assert all(candidate.distance > 0 for candidate in result.candidates)
    assert not any(candidate.kind == "edge-edge" and candidate.distance == 0 for candidate in result.candidates)


def test_hopf_analytic_and_projected_linking():
    link = hopf_link()
    assert len(link) == 2
    assert math.isclose(link.length(), 8.0 * math.pi, rel_tol=1e-12)
    assert math.isclose(smooth_thickness(link, samples=16).thickness, 1.0, rel_tol=1e-9)
    matrix = linking_matrix(link, samples=128)
    assert np.allclose(np.abs(matrix[0, 1]), 1.0)
    report = topology_report(link, samples=128)
    assert report.invariants["pairwise_linking_number"] == 1


def test_torus_components_and_trefoil_invariants():
    link = torus_link(4, 4, major_radius=3.0, minor_radius=1.0)
    assert len(link) == 4
    assert all(component.closed for component in link.components)
    assert torus_invariants(2, 3)["determinant"] == 3
    trefoil = torus_link(2, 3, major_radius=3.0, minor_radius=1.0)
    report = topology_report(trefoil, samples=128)
    assert report.invariants["crossing_number"] == 3
    assert report.invariants["determinant"] == 3
    assert report.invariants["projection_determinant_at_minus_one"] == 3
    assert report.projection["crossing_count"] >= 3


def test_torus_alexander_formula_matches_sympy_for_small_knots():
    import sympy as sp

    variable = sp.symbols("t")
    from topology import torus_alexander_coefficients

    for p, q in [(2, 3), (3, 4), (2, 5)]:
        coefficients = torus_alexander_coefficients(p, q)
        # Multiply the centred Laurent form by t^degree to compare ordinary
        # polynomial values without relying on string formatting.
        expression = sum(value * variable**exponent for exponent, value in coefficients.items())
        expected = sp.cancel((variable ** (p * q) - 1) * (variable - 1) / ((variable**p - 1) * (variable**q - 1)))
        ratio = sp.cancel(expression / expected)
        assert ratio == variable ** (-max(coefficients))


def test_vect_round_trip_and_closedness(tmp_path):
    path = tmp_path / "hopf.vect"
    original = hopf_link()
    write_vect(path, original, samples=32, overwrite=False)
    loaded = read_vect(path)
    assert len(loaded) == 2
    assert loaded.closed
    assert loaded.length() > 0
    assert path.read_text().startswith("VECT")


def test_contact_graph_is_finite_and_tolerance_explicit():
    graph = extract_contacts(circle().sample(24), tolerance=1e-4)
    assert graph.summary["contact_count"] == len(graph.contacts)
    assert graph.summary["distance_threshold"] > 0
    assert "continuum" in graph.summary["discretization"]


def test_machin_interval_contains_pi():
    lower, upper = machin_pi_interval(10)
    assert lower < upper
    # At high series order both rational endpoints can round to the same
    # binary float as ``math.pi``; compare decimal text for this smoke test.
    pi_decimal = Decimal(str(math.pi))
    assert Decimal(lower.numerator) / Decimal(lower.denominator) < pi_decimal
    assert pi_decimal < Decimal(upper.numerator) / Decimal(upper.denominator)
