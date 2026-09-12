"""Adversarial M1 checks with independent geometry references.

The reference paths in this module deliberately do not call the project's
thickness, projection, curve-length, or topology helpers.  They are compact
implementations of the definitions used for comparison, so a regression in a
worker routine is visible even when the worker's own tests share its algebra.

The assertions deliberately retain source blockers when they appear (for
example, a non-coprime torus period or an invalid interval enclosure).  A
failed run is evidence that M1 cannot yet be called PASS, rather than a reason
to loosen tolerances.  The circle, Rawdon MinRad, and zero-distance controls
also remain in the suite so a later regression is caught.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import mpmath as mp
import numpy as np
import pytest
from scipy.integrate import quad


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from curves import circle, hopf_link, torus_knot, torus_link  # noqa: E402
from curves.vect import read_vect  # noqa: E402
from thickness import ThicknessTolerances, polygon_thickness, smooth_thickness  # noqa: E402
from topology.projection import projected_crossings  # noqa: E402


ROPELENGTH = ROOT / "vendor" / "deps" / "libplcurve-10.1.0" / "build" / "bin" / "ropelength"
TREFOIL_47 = ROOT / "data" / "reference" / "trefoil_3.1_ridgerunner.vect"
TREFOIL_400 = ROOT / "data" / "reference" / "trefoil_3.1_plcurve_kl400.vect"
RIDGERUNNER_47_FINAL = ROOT / "results" / "ridgerunner_autoscaled_20260913" / "trefoil47.rr" / "trefoil47.final.vect"
RIDGERUNNER_400_FINAL = ROOT / "results" / "ridgerunner_autoscaled_20260913" / "trefoil400.rr" / "trefoil400.final.vect"
ATLAS_ROOT = ROOT / "data" / "reference" / "cantarella-atlas"
ATLAS_FILES = (
    ATLAS_ROOT / "knots" / "prime" / "3-10" / "3_1.vect",
    ATLAS_ROOT / "knots" / "prime" / "3-10" / "4_1.vect",
    ATLAS_ROOT / "knots" / "prime" / "3-10" / "5_1.vect",
    ATLAS_ROOT / "links" / "prime" / "2-9" / "2_2_1.vect",
)


@dataclass(frozen=True)
class RawVect:
    components: tuple[np.ndarray, ...]
    closed: tuple[bool, ...]
    vertex_counts: tuple[int, ...]


@dataclass(frozen=True)
class _ProjectedCrossing:
    """Geometry-only crossing record used by the independent diagram check."""

    component_a: int
    edge_a: int
    parameter_a: float
    component_b: int
    edge_b: int
    parameter_b: float
    depth_a: float
    depth_b: float
    sign: int

    @property
    def over(self) -> str:
        if self.depth_a > self.depth_b:
            return "a"
        if self.depth_b > self.depth_a:
            return "b"
        return "ambiguous"


def _raw_vect(path: Path) -> RawVect:
    """Parse only the numeric VECT geometry needed by this test reference.

    This parser is intentionally separate from ``curves.vect.read_vect``.  It
    accepts the two checked-in reference forms and checks all header counts,
    but does not import or call the production parser.
    """

    tokens: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        body = line.split("#", 1)[0].strip()
        if body:
            tokens.extend(body.split())
    if len(tokens) < 4 or tokens[0].upper() != "VECT":
        raise ValueError(f"invalid VECT header in {path}")
    n_components, n_vertices, n_colors = (int(tokens[i]) for i in (1, 2, 3))
    cursor = 4
    signed_counts = tuple(int(token) for token in tokens[cursor : cursor + n_components])
    cursor += n_components
    if len(signed_counts) != n_components or sum(abs(x) for x in signed_counts) != n_vertices:
        raise ValueError(f"VECT component count mismatch in {path}")
    # Geomview VECT carries one per-component color-count row even when the
    # header has n_colors=0 (the atlas uses a literal ``0`` row).  Consume it
    # unconditionally so a no-color file cannot shift coordinates by one
    # token.
    color_counts = tuple(int(token) for token in tokens[cursor : cursor + n_components])
    cursor += n_components
    if len(color_counts) != n_components or sum(color_counts) != n_colors:
        raise ValueError(f"VECT color count mismatch in {path}")
    raw = np.asarray([float(token) for token in tokens[cursor : cursor + 3 * n_vertices]], dtype=float)
    if raw.size != 3 * n_vertices:
        raise ValueError(f"VECT coordinate count mismatch in {path}")
    points = raw.reshape(n_vertices, 3)
    components: list[np.ndarray] = []
    offset = 0
    for signed in signed_counts:
        count = abs(signed)
        components.append(points[offset : offset + count].copy())
        offset += count
    return RawVect(tuple(components), tuple(x < 0 for x in signed_counts), tuple(abs(x) for x in signed_counts))


def _polyline_length(points: np.ndarray, closed: bool = True) -> float:
    deltas = np.roll(points, -1, axis=0) - points if closed else np.diff(points, axis=0)
    return float(np.linalg.norm(deltas, axis=1).sum())


def _rawdon_minrad(points: np.ndarray, closed: bool = True) -> float:
    """Independent Rawdon/libplCurve MinRad, including unequal edge lengths."""

    if not closed:
        indices = range(1, len(points) - 1)
    else:
        indices = range(len(points))
    values: list[float] = []
    n = len(points)
    for i in indices:
        previous = points[(i - 1) % n]
        point = points[i]
        following = points[(i + 1) % n]
        incoming = point - previous
        outgoing = following - point
        norm_in = float(np.linalg.norm(incoming))
        norm_out = float(np.linalg.norm(outgoing))
        cross = float(np.linalg.norm(np.cross(incoming, outgoing)))
        if min(norm_in, norm_out) <= 1e-14 or cross <= 1e-14:
            continue
        radius_factor = (norm_in * norm_out + float(np.dot(incoming, outgoing))) / (2.0 * cross)
        values.append(min(norm_in, norm_out) * radius_factor)
    return min(values) if values else float("inf")


def _endpoint_cone(vector: np.ndarray, tangent_in: np.ndarray, tangent_out: np.ndarray, tol: float = 1e-8) -> bool:
    return bool(np.dot(vector, tangent_out) >= -tol and np.dot(vector, tangent_in) <= tol)


def _segment_distance(
    a0: np.ndarray, a1: np.ndarray, b0: np.ndarray, b1: np.ndarray
) -> tuple[float, float, float]:
    """Independent closest points on two segments.

    The active-set candidates (unconstrained point and each four boundary
    faces) avoid copying the production routine's iterative clamp logic.
    """

    u = a1 - a0
    v = b1 - b0
    w = a0 - b0
    aa = float(np.dot(u, u))
    bb = float(np.dot(u, v))
    cc = float(np.dot(v, v))
    dd = float(np.dot(u, w))
    ee = float(np.dot(v, w))
    candidates: list[tuple[float, float]] = []
    denominator = aa * cc - bb * bb
    if denominator > 1e-14 * max(aa * cc, 1.0):
        candidates.append(((bb * ee - cc * dd) / denominator, (aa * ee - bb * dd) / denominator))
    for s in (0.0, 1.0):
        candidates.append((s, (ee + bb * s) / cc if cc > 1e-14 else 0.0))
    for t in (0.0, 1.0):
        candidates.append(((bb * t - dd) / aa if aa > 1e-14 else 0.0, t))
    if not candidates:
        candidates = [(0.0, 0.0)]
    best = (float("inf"), 0.0, 0.0)
    for s, t in candidates:
        s = float(np.clip(s, 0.0, 1.0))
        t = float(np.clip(t, 0.0, 1.0))
        distance = float(np.linalg.norm(a0 + s * u - b0 - t * v))
        if distance < best[0]:
            best = (distance, s, t)
    return best


def _vertex_tangents(points: np.ndarray, index: int, closed: bool = True) -> tuple[np.ndarray, np.ndarray] | None:
    n = len(points)
    if not closed and (index == 0 or index == n - 1):
        return None
    prev = points[(index - 1) % n]
    current = points[index]
    following = points[(index + 1) % n]
    incoming = current - prev
    outgoing = following - current
    a = np.linalg.norm(incoming)
    b = np.linalg.norm(outgoing)
    if a <= 1e-14 or b <= 1e-14:
        return None
    return incoming / a, outgoing / b


def _edge_incident(vertex: int, edge: int, n: int, closed: bool) -> bool:
    if closed:
        return edge == vertex or edge == (vertex - 1) % n
    return edge == vertex or edge == vertex - 1


def _independent_dcsd(raw: RawVect) -> tuple[float, str]:
    """Enumerate vv/ve/ee interiors independently of ``thickness.polygon``."""

    best = (float("inf"), "none")
    components = raw.components
    # Vertex--vertex, with the two one-sided normal-cone tests.
    for ai, a in enumerate(components):
        for bi in range(ai, len(components)):
            b = components[bi]
            for i in range(len(a)):
                start = i + 1 if ai == bi else 0
                for j in range(start, len(b)):
                    if ai == bi and min(j - i, len(a) - (j - i)) <= 1:
                        continue
                    ta = _vertex_tangents(a, i, raw.closed[ai])
                    tb = _vertex_tangents(b, j, raw.closed[bi])
                    if ta is None or tb is None:
                        continue
                    vector = a[i] - b[j]
                    distance = float(np.linalg.norm(vector))
                    if distance > 1e-14 and _endpoint_cone(vector, *ta) and _endpoint_cone(-vector, *tb):
                        if distance < best[0]:
                            best = distance, "vertex-vertex"
    # Vertex--edge, requiring an interior orthogonal projection and a normal
    # cone at the vertex.  Both component orientations are visited.
    for vi, vertices in enumerate(components):
        for i in range(len(vertices)):
            tangents = _vertex_tangents(vertices, i, raw.closed[vi])
            if tangents is None:
                continue
            for ej, edges in enumerate(components):
                edge_count = len(edges) if raw.closed[ej] else len(edges) - 1
                for j in range(edge_count):
                    if vi == ej and _edge_incident(i, j, len(vertices), raw.closed[ej]):
                        continue
                    start = edges[j]
                    direction = edges[(j + 1) % len(edges)] - start
                    denominator = float(np.dot(direction, direction))
                    if denominator <= 1e-14:
                        continue
                    fraction = float(np.dot(vertices[i] - start, direction) / denominator)
                    if not 1e-8 < fraction < 1.0 - 1e-8:
                        continue
                    difference = vertices[i] - (start + fraction * direction)
                    distance = float(np.linalg.norm(difference))
                    if distance > 1e-14 and _endpoint_cone(difference, *tangents):
                        if distance < best[0]:
                            best = distance, "vertex-edge"
    # Edge--edge, with both closest points in their interiors.  Pairs whose
    # closest point is an endpoint are covered by vv/ve above.
    for ai, a in enumerate(components):
        count_a = len(a) if raw.closed[ai] else len(a) - 1
        for bi in range(ai, len(components)):
            b = components[bi]
            count_b = len(b) if raw.closed[bi] else len(b) - 1
            for i in range(count_a):
                for j in range(count_b):
                    if ai == bi:
                        gap = min(abs(j - i), len(a) - abs(j - i)) if raw.closed[ai] else abs(j - i)
                        if j <= i or gap <= 1:
                            continue
                    distance, s, t = _segment_distance(a[i], a[(i + 1) % len(a)], b[j], b[(j + 1) % len(b)])
                    if 1e-8 < s < 1.0 - 1e-8 and 1e-8 < t < 1.0 - 1e-8 and distance < best[0]:
                        best = distance, "edge-edge"
    return best


def _projection_basis(view: Sequence[float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    direction = np.asarray(view, dtype=float)
    direction = direction / np.linalg.norm(direction)
    helper = np.array([0.0, 0.0, 1.0]) if abs(direction[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
    first = np.cross(direction, helper)
    first /= np.linalg.norm(first)
    second = np.cross(direction, first)
    return first, second, direction


def _det2(a: np.ndarray, b: np.ndarray) -> float:
    return float(a[0] * b[1] - a[1] * b[0])


def _projected_invariants(components: Sequence[np.ndarray], closed: Sequence[bool], view: Sequence[float]) -> dict[str, object]:
    e1, e2, direction = _projection_basis(view)
    projected = [np.column_stack((points @ e1, points @ e2)) for points in components]
    depths = [points @ direction for points in components]
    crossings: list[_ProjectedCrossing] = []
    matrix = np.zeros((len(components), len(components)), dtype=float)
    for ai, points_a in enumerate(projected):
        n_a = len(points_a)
        count_a = n_a if closed[ai] else n_a - 1
        for bi in range(ai, len(projected)):
            points_b = projected[bi]
            n_b = len(points_b)
            count_b = n_b if closed[bi] else n_b - 1
            for i in range(count_a):
                a0 = points_a[i]
                vector_a = points_a[(i + 1) % n_a] - a0
                for j in range(count_b):
                    if ai == bi:
                        if j <= i:
                            continue
                        gap = min(abs(j - i), n_a - abs(j - i)) if closed[ai] else abs(j - i)
                        if gap <= 1:
                            continue
                    b0 = points_b[j]
                    vector_b = points_b[(j + 1) % n_b] - b0
                    denominator = _det2(vector_a, vector_b)
                    if abs(denominator) <= 1e-12:
                        continue
                    offset = b0 - a0
                    ta = _det2(offset, vector_b) / denominator
                    tb = _det2(offset, vector_a) / denominator
                    if not (1e-9 < ta < 1.0 - 1e-9 and 1e-9 < tb < 1.0 - 1e-9):
                        continue
                    depth_a = float(depths[ai][i] + ta * (depths[ai][(i + 1) % n_a] - depths[ai][i]))
                    depth_b = float(depths[bi][j] + tb * (depths[bi][(j + 1) % n_b] - depths[bi][j]))
                    # An oriented link crossing uses both the projected
                    # tangent orientation and the over/under ordering.  A
                    # denominator-only sign makes the two crossings of a
                    # Hopf link cancel and is therefore only a crossing
                    # count, not a linking-number computation.
                    depth_gap = depth_a - depth_b
                    sign = 1 if denominator * depth_gap > 0 else -1
                    crossings.append(
                        _ProjectedCrossing(
                            ai,
                            i,
                            (i + ta) / n_a,
                            bi,
                            j,
                            (j + tb) / n_b,
                            depth_a,
                            depth_b,
                            sign,
                        )
                    )
                    if ai != bi:
                        matrix[ai, bi] += 0.5 * sign
                        # Linking number is symmetric in the two oriented
                        # components.  Reversing either component flips both
                        # off-diagonal entries; it does not transpose with a
                        # minus sign.
                        matrix[bi, ai] += 0.5 * sign
    return {
        "crossing_count": len(crossings),
        "self_crossing_count": sum(item.component_a == item.component_b for item in crossings),
        "linking_matrix": matrix,
        "depth_gap_min": min((abs(item.depth_a - item.depth_b) for item in crossings), default=float("inf")),
        "crossings": crossings,
        "view": tuple(float(x) for x in direction),
    }


def _generic_projection(components: Sequence[np.ndarray], closed: Sequence[bool], *, target_crossings: int | None = None) -> dict[str, object]:
    """Choose a generic view by geometry-only deterministic search."""

    # Include simple Cartesian views first, then an RNG stream whose seed is
    # part of this test algorithm, not a topology label or a lookup table.
    views: list[np.ndarray] = [
        np.array([1.0, 2.0, -1.0]),
        np.array([1.0, -2.0, 3.0]),
        np.array([-2.0, 1.0, 1.0]),
    ]
    rng = np.random.default_rng(20260913)
    views.extend(rng.normal(size=(256, 3)))
    for view in views:
        result = _projected_invariants(components, closed, view)
        if float(result["depth_gap_min"]) <= 1e-8:
            continue
        if target_crossings is None or result["crossing_count"] == target_crossings:
            return result
    raise AssertionError(f"could not find a generic projection (target={target_crossings})")


def _independent_diagram_determinant(crossings: Iterable[_ProjectedCrossing], *, component: int = 0) -> int | None:
    """Compute the t=-1 Fox coloring determinant from projected geometry.

    The input is a one-component transverse diagram.  The component is cut at
    each undercrossing, and each crossing contributes the integer relation
    ``2*over - under_in - under_out = 0``.  A reduced determinant is the knot
    determinant.  This implementation deliberately has no dependency on the
    production projection or invariant code.
    """

    selected = [
        crossing
        for crossing in crossings
        if crossing.component_a == component and crossing.component_b == component
    ]
    if not selected or any(crossing.over == "ambiguous" for crossing in selected):
        return None

    under_events: list[tuple[float, int, float]] = []
    for index, crossing in enumerate(selected):
        if crossing.over == "a":
            under_parameter, over_parameter = crossing.parameter_b, crossing.parameter_a
        elif crossing.over == "b":
            under_parameter, over_parameter = crossing.parameter_a, crossing.parameter_b
        else:  # pragma: no cover - guarded by the ambiguity check above
            return None
        under_events.append((under_parameter % 1.0, index, over_parameter % 1.0))
    under_events.sort(key=lambda item: item[0])
    count = len(under_events)
    if count < 1:
        return None
    if any(
        under_events[(index + 1) % count][0] - under_events[index][0] <= 1e-10
        if index < count - 1
        else under_events[0][0] + 1.0 - under_events[-1][0] <= 1e-10
        for index in range(count)
    ):
        return None

    crossing_to_under = {
        crossing_index: event_index
        for event_index, (_, crossing_index, _) in enumerate(under_events)
    }
    starts = [event[0] for event in under_events]

    def arc_containing(parameter: float) -> int:
        return int(np.searchsorted(starts, parameter % 1.0, side="right") - 1) % count

    matrix = np.zeros((count, count), dtype=int)
    for _, crossing_index, over_parameter in under_events:
        under_index = crossing_to_under[crossing_index]
        incoming_arc = (under_index - 1) % count
        outgoing_arc = under_index
        over_arc = arc_containing(over_parameter)
        matrix[crossing_index, over_arc] += 2
        matrix[crossing_index, incoming_arc] -= 1
        matrix[crossing_index, outgoing_arc] -= 1

    reduced = matrix[:-1, :-1].tolist()
    if not reduced:
        return 0
    sign = 1
    previous_pivot = 1
    size = len(reduced)
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if reduced[row][pivot_index] != 0),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            reduced[pivot_index], reduced[pivot_row] = reduced[pivot_row], reduced[pivot_index]
            sign *= -1
        pivot = reduced[pivot_index][pivot_index]
        if pivot == 0:
            return 0
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = reduced[row][column] * pivot - reduced[row][pivot_index] * reduced[pivot_index][column]
                if previous_pivot != 1:
                    if numerator % previous_pivot:
                        return None
                    numerator //= previous_pivot
                reduced[row][column] = numerator
            reduced[row][pivot_index] = 0
        previous_pivot = pivot
    return abs(int(sign * reduced[-1][-1]))


def _analytic_torus_length(p: int, q: int, major: float, minor: float) -> float:
    d = math.gcd(abs(p), abs(q))
    period = 2.0 * math.pi / d
    integrand = lambda t: math.sqrt(p * p * (major + minor * math.cos(q * t)) ** 2 + (minor * q) ** 2)
    return float(d * quad(integrand, 0.0, period, epsabs=2e-11, epsrel=2e-11, limit=500)[0])


def _finite_difference_curvature(p: int, q: int, major: float, minor: float, period: float, count: int = 1200) -> float:
    """Curvature radius from a separately coded position and 5-point stencil."""

    def position(t: float) -> np.ndarray:
        theta = p * t
        phi = q * t
        radial = major + minor * math.cos(phi)
        return np.array([radial * math.cos(theta), radial * math.sin(theta), minor * math.sin(phi)])

    h = 1e-4
    radii: list[float] = []
    for t in np.linspace(0.0, period, count, endpoint=False):
        f0 = position(float(t))
        fm1 = position(float(t - h))
        fm2 = position(float(t - 2.0 * h))
        fp1 = position(float(t + h))
        fp2 = position(float(t + 2.0 * h))
        first = (fm2 - 8.0 * fm1 + 8.0 * fp1 - fp2) / (12.0 * h)
        second = (-fp2 + 16.0 * fp1 - 30.0 * f0 + 16.0 * fm1 - fm2) / (12.0 * h * h)
        curvature = np.linalg.norm(np.cross(first, second)) / np.linalg.norm(first) ** 3
        radii.append(1.0 / curvature)
    return min(radii)


def _cli_metrics(path: Path) -> tuple[float, float, float, float]:
    if not ROPELENGTH.exists():
        pytest.fail(f"required independent executable is missing: {ROPELENGTH}")
    quiet = subprocess.run([str(ROPELENGTH), "--quiet", str(path)], check=True, capture_output=True, text=True)
    ropelength = float(quiet.stdout.strip().splitlines()[-1])
    full = subprocess.run([str(ROPELENGTH), str(path)], check=True, capture_output=True, text=True).stdout
    thickness = float(re.search(r"Thickness:\s*([0-9.eE+-]+)", full).group(1))
    minrad = float(re.search(r"minRad:\s*([0-9.eE+-]+)", full).group(1))
    minstrut = float(re.search(r"minStrut:\s*([0-9.eE+-]+)", full).group(1))
    return ropelength, thickness, minrad, minstrut


def test_reference_vect_parser_and_explicit_lengths() -> None:
    for path, expected_vertices in ((TREFOIL_47, 47), (TREFOIL_400, 400)):
        raw = _raw_vect(path)
        assert raw.vertex_counts == (expected_vertices,)
        assert raw.closed == (True,)
        own_length = _polyline_length(raw.components[0])
        parsed = read_vect(path)
        assert parsed.component_count == 1
        assert parsed.component(0).vertex_count == expected_vertices
        assert parsed.length() == pytest.approx(own_length, rel=0.0, abs=2e-12)


def test_polygon_engine_matches_independent_plcurve_metrics() -> None:
    """Compare explicit sums and vv/ve/ee references to libplCurve 10.1.0."""

    for path in (TREFOIL_47, TREFOIL_400):
        raw = _raw_vect(path)
        points = raw.components[0]
        own_length = _polyline_length(points)
        own_minrad = _rawdon_minrad(points)
        own_dcsd, own_kind = _independent_dcsd(raw)
        cli_rope, cli_thickness, cli_minrad, cli_minstrut = _cli_metrics(path)
        engine = polygon_thickness(points, include_rejected=True)

        assert own_kind == "edge-edge"
        assert own_length / min(own_minrad, own_dcsd / 2.0) == pytest.approx(cli_rope, rel=2e-7, abs=2e-6)
        assert own_length == pytest.approx(engine.length, rel=0.0, abs=2e-12)
        assert cli_minstrut == pytest.approx(own_dcsd, rel=0.0, abs=5e-6)
        assert cli_minrad == pytest.approx(own_minrad, rel=0.0, abs=5e-6)
        assert cli_thickness == pytest.approx(min(own_minrad, own_dcsd / 2.0), rel=0.0, abs=5e-6)
        assert engine.dcsd == pytest.approx(own_dcsd, rel=0.0, abs=5e-6)
        # The reference catches a distinct MinRad implementation, even when
        # the particular trefoil is strut-limited and total thickness agrees.
        assert engine.minrad == pytest.approx(own_minrad, rel=0.0, abs=5e-6)


def test_circle_and_hopf_length_curvature_and_scaling() -> None:
    for radius in (0.5, 1.0, 2.0):
        curve = circle(radius=radius)
        assert curve.length() == pytest.approx(2.0 * math.pi * radius, rel=0.0, abs=2e-13)
        estimate = smooth_thickness(curve, samples=128, min_parameter_gap=2)
        assert estimate.curvature_radius == pytest.approx(radius, rel=0.0, abs=2e-12)
        # The circle's exact nonlocal DCSD is its antipodal chord, 2r.  A
        # sample nearest neighbour must never masquerade as a DCSD.
        assert estimate.dcsd == pytest.approx(2.0 * radius, rel=0.0, abs=1e-8)
        assert estimate.thickness >= 0.95 * radius

    for scale in (0.5, 1.0, 2.0):
        link = hopf_link(radius=2.0 * scale)
        expected_length = 4.0 * math.pi * 2.0 * scale
        expected_thickness = 1.0 * scale
        assert link.length() == pytest.approx(expected_length, rel=0.0, abs=3e-12)
        estimate = smooth_thickness(link, samples=128, min_parameter_gap=2)
        assert estimate.curvature_radius == pytest.approx(2.0 * scale, rel=0.0, abs=3e-11)
        assert estimate.dcsd >= 1.9 * scale
        assert estimate.thickness >= 0.95 * expected_thickness


def test_torus_length_period_and_projected_invariants() -> None:
    # Coprime T(2,3) has one component and gives a 3-crossing projection.
    knot = torus_knot(2, 3, major_radius=3.0, minor_radius=1.0)
    assert knot.length() == pytest.approx(_analytic_torus_length(2, 3, 3.0, 1.0), rel=0.0, abs=2e-9)
    finite_difference_radius = _finite_difference_curvature(2, 3, 3.0, 1.0, 2.0 * math.pi)
    estimate = smooth_thickness(knot, samples=512, min_parameter_gap=8)
    assert estimate.curvature_radius == pytest.approx(finite_difference_radius, rel=2e-4, abs=2e-4)
    projection = _generic_projection([knot.component(0).sample(512)], [True], target_crossings=3)
    assert projection["crossing_count"] == 3
    assert projection["self_crossing_count"] == 3
    assert float(projection["depth_gap_min"]) > 1e-6

    # A non-coprime T(2,2) has two singly traced components.  The half-period
    # sample is a geometry-only duplicate test for the common implementation
    # error of integrating each component over 2*pi.
    link = torus_link(2, 2, major_radius=3.0, minor_radius=1.0)
    expected_link_length = _analytic_torus_length(2, 2, 3.0, 1.0)
    assert link.component_count == 2
    assert link.length() == pytest.approx(expected_link_length, rel=0.0, abs=2e-9)
    samples = [component.sample(256) for component in link.components]
    for points in samples:
        assert np.linalg.norm(points[0] - points[128]) > 1e-5
    projection = _generic_projection(samples, [True, True])
    matrix = np.asarray(projection["linking_matrix"])
    assert np.allclose(np.abs(matrix[np.triu_indices(2, 1)]), 1.0, atol=1e-8)
    # The integer is invariant under generic view changes and changes sign
    # when exactly one oriented component is reversed.
    for view in ([1.0, 2.0, -1.0], [1.0, -2.0, 3.0], [-2.0, 1.0, 1.0]):
        view_result = _projected_invariants(samples, [True, True], view)
        view_matrix = np.asarray(view_result["linking_matrix"])
        assert np.allclose(np.abs(view_matrix[np.triu_indices(2, 1)]), 1.0, atol=1e-8)
    reversed_samples = [samples[0], samples[1][::-1].copy()]
    reversed_result = _projected_invariants(reversed_samples, [True, True], [1.0, 2.0, -1.0])
    reversed_matrix = np.asarray(reversed_result["linking_matrix"])
    assert reversed_matrix[0, 1] == pytest.approx(-matrix[0, 1], abs=1e-8)
    assert reversed_matrix[1, 0] == pytest.approx(-matrix[1, 0], abs=1e-8)

    # The constructive T(3,3) family has three components and unit pairwise
    # linking.  The matrix is obtained from projected crossings only.
    triple = torus_link(3, 3, major_radius=4.0, minor_radius=1.0)
    assert triple.component_count == 3
    assert triple.length() == pytest.approx(_analytic_torus_length(3, 3, 4.0, 1.0), rel=0.0, abs=3e-9)
    triple_projection = _generic_projection([component.sample(192) for component in triple.components], [True] * 3)
    triple_matrix = np.asarray(triple_projection["linking_matrix"])
    assert np.allclose(np.abs(triple_matrix[np.triu_indices(3, 1)]), 1.0, atol=1e-8)


def test_independent_projected_trefoil_data_without_name_lookup() -> None:
    for path in (TREFOIL_47, TREFOIL_400):
        raw = _raw_vect(path)
        result = _generic_projection(raw.components, raw.closed, target_crossings=3)
        assert result["crossing_count"] == 3
        assert result["self_crossing_count"] == 3
        assert float(result["depth_gap_min"]) > 1e-6
        # A 3-crossing one-component diagram is the constructive trefoil
        # control up to mirror/orientation; no filename or knot-library query
        # participates in this assertion.


def test_independent_projected_trefoil_determinant() -> None:
    """Recover the determinant from the actual projection, independently."""

    for path in (TREFOIL_47, TREFOIL_400, RIDGERUNNER_47_FINAL, RIDGERUNNER_400_FINAL):
        assert path.is_file()
        raw = _raw_vect(path)
        result = _generic_projection(raw.components, raw.closed, target_crossings=3)
        determinant = _independent_diagram_determinant(result["crossings"])
        assert determinant == 3

        # Reversing the polygon orientation preserves this unoriented
        # invariant while forcing the under/over events through a new
        # parameter ordering.
        reversed_result = _generic_projection([raw.components[0][::-1].copy()], [True], target_crossings=3)
        assert _independent_diagram_determinant(reversed_result["crossings"]) == 3


def test_cantarella_atlas_multiple_native_controls() -> None:
    """Run the independent parser and plCurve CLI on several atlas VECTs."""

    missing = [path for path in ATLAS_FILES if not path.is_file()]
    if missing:
        pytest.fail("atlas controls missing: " + ", ".join(str(path) for path in missing))
    for path in ATLAS_FILES:
        raw = _raw_vect(path)
        assert sum(raw.vertex_counts) > 100
        assert all(raw.closed)
        own_length = sum(_polyline_length(points, closed) for points, closed in zip(raw.components, raw.closed))
        cli_rope, cli_thickness, _, _ = _cli_metrics(path)
        assert math.isfinite(cli_rope) and cli_rope > 0.0
        assert math.isfinite(cli_thickness) and cli_thickness > 0.0
        # This relation is checked from raw coordinates and CLI output; it
        # does not reuse the project's length or thickness routines.
        assert cli_rope * cli_thickness == pytest.approx(own_length, rel=2e-6, abs=2e-5)


def test_ridgerunner_autoscaled_controls_are_real_and_reproducible() -> None:
    run_root = ROOT / "results" / "ridgerunner_autoscaled_20260913"
    cases = (
        (run_root / "trefoil47.run.log", run_root / "trefoil47.rr" / "trefoil47.final.vect", 47, 33.149017),
        (run_root / "trefoil400.run.log", run_root / "trefoil400.rr" / "trefoil400.final.vect", 400, 32.748793),
    )
    for log_path, final_path, expected_vertices, expected_rope in cases:
        assert log_path.is_file() and final_path.is_file()
        log = log_path.read_text(encoding="utf-8")
        for marker in ("Ridgerunner 2.3.1", "plCurve Version: 10.1.0", "Octrope Version: 10.1.0", "tsnnls Version: 2.5.1", "Autoscale selftest ok"):
            assert marker in log
        raw = _raw_vect(final_path)
        assert raw.vertex_counts == (expected_vertices,)
        cli_rope, cli_thickness, _, _ = _cli_metrics(final_path)
        assert cli_thickness > 0.0
        assert cli_rope == pytest.approx(expected_rope, abs=3e-5)
        own_length = _polyline_length(raw.components[0])
        assert own_length == pytest.approx(cli_rope * cli_thickness, rel=2e-6, abs=2e-5)


def test_polygon_failure_controls_and_candidate_classes() -> None:
    # Bow-tie self-intersection: an interior edge-edge pair is exactly zero.
    bow_tie = np.array([[-1.0, -1.0, 0.0], [1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [1.0, -1.0, 0.0]])
    result = polygon_thickness(bow_tie, include_rejected=True)
    assert result.thickness <= 1e-12
    assert any(candidate.kind == "edge-edge" and candidate.distance <= 1e-12 for candidate in result.candidates)

    # Two open components exercise an interior vertex-edge and an interior
    # edge-edge strut without relying on a closed-endpoint convention.
    from curves.vect import PolygonComponent, PolygonLink

    vertex_edge = PolygonLink(
        [
            PolygonComponent([[-1.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 1.0]], closed=False),
            PolygonComponent([[-1.0, -1.0, 0.0], [1.0, -1.0, 0.0]], closed=False),
        ]
    )
    ve_result = polygon_thickness(vertex_edge, include_rejected=True)
    assert any(candidate.kind == "vertex-edge" for candidate in ve_result.candidates)

    edge_edge = PolygonLink(
        [
            PolygonComponent([[-1.0, 0.0, 1.0], [1.0, 0.0, 1.0]], closed=False),
            PolygonComponent([[0.0, -1.0, 0.0], [0.0, 1.0, 0.0]], closed=False),
        ]
    )
    ee_result = polygon_thickness(edge_edge, include_rejected=True)
    assert any(candidate.kind == "edge-edge" for candidate in ee_result.candidates)

    # Exact cross-component vertex contact is zero reach even though neither
    # component has a degenerate edge.
    triangle = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
    shifted = triangle + np.array([0.0, 0.0, 0.0])
    contact = polygon_thickness([triangle, shifted], include_rejected=True)
    assert contact.thickness <= 1e-12

    # A near-zero edge is surfaced and cannot produce a positive certificate.
    near_degenerate = np.array([[0.0, 0.0, 0.0], [1e-14, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    degenerate = polygon_thickness(near_degenerate, include_rejected=True)
    assert degenerate.degenerate
    assert degenerate.thickness == 0.0
    assert any("zero/near-zero edge" in note for note in degenerate.notes)


def test_adversarial_collision_and_scale_regressions() -> None:
    """Retain zero-thickness collisions and preserve projections under scale."""

    collision_cases = (
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, -1.0, 0.0], [0.5, 1.0, 0.0]]),
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [5e-9, -1.0, 0.0], [5e-9, 1.0, 0.0]]),
        np.array([[0.0, 0.0, 0.0], [1e-7, 0.0, 0.0], [5e-8, -1e-7, 0.0], [5e-8, 1e-7, 0.0]]),
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [5e-9, -1.0, 0.0], [5e-9, 1.0, 0.0], [-1.0, 1.0, 0.0]]),
    )
    for vertices in collision_cases:
        result = polygon_thickness(vertices, include_rejected=True)
        assert result.thickness == 0.0
        assert result.dcsd == 0.0
        assert result.degenerate
        assert not result.complete
        assert any(candidate.distance == 0.0 for candidate in result.candidates)

    raw = _raw_vect(TREFOIL_47)
    for scale in (1.0, 1e-5, 1e5):
        projection = projected_crossings(raw.components[0] * scale)
        assert projection.generic
        assert projection.crossing_count == 3


def _fraction(record: dict[str, str]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def _decimal_interval_contains_fraction(record: dict[str, object]) -> bool:
    """Check rational endpoint ordering, independent of readable decimals."""

    return _fraction(record["lower"]) <= _fraction(record["upper"])


def test_arb_certificate_endpoints_midpoint_constant_and_reproducibility() -> None:
    from certification.arb_backend import arb, arb_precision
    from certification.integrals import certify_integrals
    from certification.shell_family import certified_floor

    with arb_precision(192):
        first = certify_integrals(256, 512, precision_bits=192, output_digits=50)
        second = certify_integrals(256, 512, precision_bits=192, output_digits=50)
        assert first["alpha"] == second["alpha"]
        assert first["l0"] == second["l0"]
        # Every rational interval is ordered, and the mesh+error enclosure is
        # strictly wider than the midpoint mesh value.
        for key in ("q0", "midpoint_sum", "discretization_error", "l0", "denominator", "alpha"):
            assert _decimal_interval_contains_fraction(first[key])
        assert _fraction(first["l0"]["lower"]) <= _fraction(first["midpoint_sum"]["lower"])
        assert _fraction(first["l0"]["upper"]) >= _fraction(first["midpoint_sum"]["upper"])

        # The floor helper must reject an interval crossing an integer instead
        # of rounding downward or upward based on a midpoint.
        with pytest.raises(ArithmeticError):
            certified_floor(arb("2 +/- 0.1"), label="adversarial straddle")

    # Recompute the midpoint error expression with an independent Decimal
    # value of pi and verify that the recorded Arb interval contains it.
    with localcontext() as context:
        context.prec = 90
        mp.mp.dps = 100
        pi = Decimal(str(mp.pi))
        expected_error = (Decimal(2) * pi) / Decimal(24) * (Decimal(600) / Decimal(256**2) + Decimal(60) * (Decimal(2) * pi / Decimal(512)) ** 2)
        error_record = first["discretization_error"]
        lower = Decimal(error_record["lower"]["numerator"]) / Decimal(error_record["lower"]["denominator"])
        upper = Decimal(error_record["upper"]["numerator"]) / Decimal(error_record["upper"]["denominator"])
        assert lower <= expected_error <= upper

    # Independent high-precision quadrature of the exact integrals must lie in
    # the certificate's alpha interval.  The certificate's midpoint rule is
    # still the SUT; this is a separate numerical path.
    mp.mp.dps = 50
    mpi = mp.pi
    n = lambda x: 2 * mpi * x * (2 - x) / mp.sqrt(x * x + (2 - x) * (2 - x))
    e = lambda x, t: mp.sqrt((4 + 2 * x * mp.cos(t)) ** 2 + 4 * x * x)
    q0 = mpi * (3 * mp.asinh(1) / mp.sqrt(2) - 1)
    l0 = mp.quad(lambda x: mp.quad(lambda t: n(x) * e(x, t), [0, 2 * mpi]), [0, 1])
    alpha = l0 / (mp.sqrt(2) * q0 ** mp.mpf("1.5"))
    lo = mp.mpf(first["alpha"]["lower"]["numerator"]) / mp.mpf(first["alpha"]["lower"]["denominator"])
    hi = mp.mpf(first["alpha"]["upper"]["numerator"]) / mp.mpf(first["alpha"]["upper"]["denominator"])
    assert lo <= alpha <= hi


def test_provenance_versions_and_reference_hashes() -> None:
    software = (ROOT / "references" / "SOFTWARE_DATA.md").read_text(encoding="utf-8")
    assert subprocess.run(["git", "-C", str(ROOT / "vendor" / "plcurve"), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip() == "28c1ab74c02baab71ac77cd851e9163875c137a3"
    assert subprocess.run(["git", "-C", str(ROOT / "vendor" / "ridgerunner"), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip() == "4ee3199e737dcd3580d8bfc5deb031cd53f5f554"
    expected_hashes = {
        TREFOIL_47: "809cdd9141ee4f118e01301648d7b47daf9a2d7c7683ba42e0f424e50e6405a1",
        TREFOIL_400: "a7c002b1499207bd39a187952d567fe70b86f79b51099cfc6d28f992b990d5fd",
    }
    for path, expected in expected_hashes.items():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == expected
    assert "plCurve" in software
    assert "Ridgerunner" in software
    # The checked-out source is the maintained 2.3.1 release at the pinned
    # commit.  Keep this check independent of the prose table so a stale
    # version claim in the audit is visible to the report.
    configure = (ROOT / "vendor" / "ridgerunner" / "configure.ac").read_text(encoding="utf-8")
    assert "AC_INIT(ridgerunner,2.3.1" in configure
