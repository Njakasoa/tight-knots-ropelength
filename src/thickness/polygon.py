"""Independent polygonal thickness and doubly-critical search.

The implementation enumerates the actual candidate classes used by the
polygonal reach model:

* vertex--vertex pairs with both endpoint normal-cone conditions;
* vertex--edge pairs with an interior orthogonal projection and an endpoint
  normal-cone condition; and
* edge--edge pairs whose closest points lie in both edge interiors.

Adjacent portions of one closed component are excluded before distance tests.
Their small distances describe local arclength, not doubly-critical
self-distance (DCSD).  Degenerate edges and candidates near a tolerance
boundary are surfaced in the result instead of being presented as a
certificate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Sequence

import numpy as np

try:  # support both ``PYTHONPATH=repo`` and ``PYTHONPATH=repo/src``
    from curves.base import Curve
    from curves.vect import PolygonComponent, PolygonLink
except ImportError:  # pragma: no cover - package-layout fallback
    from src.curves.base import Curve
    from src.curves.vect import PolygonComponent, PolygonLink


@dataclass(frozen=True)
class ThicknessTolerances:
    """Absolute numerical tolerances used by the polygon search."""

    distance: float = 1e-9
    relative_distance: float = 1e-9
    orthogonality: float = 1e-8
    endpoint: float = 1e-8
    degeneracy: float = 1e-12

    def __post_init__(self) -> None:
        if any(float(value) < 0 or not np.isfinite(float(value)) for value in asdict(self).values()):
            raise ValueError("thickness tolerances must be finite and nonnegative")


@dataclass
class DoublyCriticalCandidate:
    kind: str
    distance: float
    component_a: int
    index_a: int
    parameter_a: float
    component_b: int
    index_b: int
    parameter_b: float
    is_doubly_critical: bool = True
    criticality: str = "verified"
    orthogonality_residual: float = 0.0
    endpoint_margin: float | None = None
    note: str = ""

    @property
    def type(self) -> str:
        return self.kind

    @property
    def parameters(self) -> tuple[float, float]:
        return self.parameter_a, self.parameter_b

    @property
    def components(self) -> tuple[int, int]:
        return self.component_a, self.component_b

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class KinkGeometry:
    component: int
    index: int
    parameter: float
    minrad: float
    turning_angle: float
    edge_lengths: tuple[float, float]
    degenerate: bool = False


@dataclass
class ThicknessResult:
    thickness: float
    minrad: float
    dcsd: float
    candidates: list[DoublyCriticalCandidate] = field(default_factory=list)
    rejected_candidates: list[DoublyCriticalCandidate] = field(default_factory=list)
    complete: bool = True
    degenerate: bool = False
    length: float = float("nan")
    limiting: str = "none"
    tolerances: ThicknessTolerances = field(default_factory=ThicknessTolerances)
    component_count: int = 1
    notes: list[str] = field(default_factory=list)
    normalization: str = "radius"
    method: str = "polygon DCSD vv/ve/ee enumeration"

    @property
    def min_rad(self) -> float:
        return self.minrad

    @property
    def dcsd_half(self) -> float:
        return 0.5 * self.dcsd

    @property
    def value(self) -> float:
        return self.thickness

    @property
    def ropelength(self) -> float:
        return self.length / self.thickness if self.thickness > 0 else float("inf")

    @property
    def doubly_critical_candidates(self) -> list[DoublyCriticalCandidate]:
        return self.candidates

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["tolerances"] = asdict(self.tolerances)
        result["ropelength"] = self.ropelength
        result["dcsd_half"] = self.dcsd_half
        return result


@dataclass
class _ComponentData:
    vertices: np.ndarray
    closed: bool
    component: int

    @property
    def n_vertices(self) -> int:
        return int(self.vertices.shape[0])

    @property
    def n_edges(self) -> int:
        return self.n_vertices if self.closed else max(0, self.n_vertices - 1)

    def edge(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        return self.vertices[index], self.vertices[(index + 1) % self.n_vertices]


def _coerce_components(value: Any, *, samples: int) -> list[_ComponentData]:
    if isinstance(value, PolygonLink):
        return [_ComponentData(item.vertices.copy(), item.closed, index) for index, item in enumerate(value.components)]
    if isinstance(value, PolygonComponent):
        return [_ComponentData(value.vertices.copy(), value.closed, 0)]
    if isinstance(value, Curve):
        return [_ComponentData(item.sample(samples), item.closed, index) for index, item in enumerate(value.components)]
    if isinstance(value, np.ndarray):
        array = np.asarray(value, dtype=float)
        if array.ndim != 2 or array.shape[1] != 3:
            raise ValueError("vertices must have shape (n,3)")
        return [_ComponentData(array.copy(), True, 0)]
    if isinstance(value, (list, tuple)):
        # A rectangular list is one component; a ragged sequence is a link.
        try:
            array = np.asarray(value, dtype=float)
        except (TypeError, ValueError):
            array = np.asarray([], dtype=float)
        if array.ndim == 2 and array.shape[1] == 3:
            return [_ComponentData(array.copy(), True, 0)]
        components: list[_ComponentData] = []
        for index, item in enumerate(value):
            array = np.asarray(item, dtype=float)
            if array.ndim != 2 or array.shape[1] != 3:
                raise ValueError("each polygon component must have shape (n,3)")
            components.append(_ComponentData(array.copy(), True, index))
        if components:
            return components
    raise TypeError(f"cannot coerce {type(value).__name__} to polygon vertices")


def _edge_lengths(component: _ComponentData) -> np.ndarray:
    if component.n_edges == 0:
        return np.empty(0, dtype=float)
    ends = np.roll(component.vertices, -1, axis=0) if component.closed else component.vertices[1:]
    starts = component.vertices if component.closed else component.vertices[:-1]
    return np.linalg.norm(ends - starts, axis=1)


def _vertex_tangents(component: _ComponentData, index: int, lengths: np.ndarray, tol: float) -> tuple[np.ndarray, np.ndarray, bool]:
    n = component.n_vertices
    if component.closed:
        prev_index = (index - 1) % n
        next_index = index % n
        prev_point = component.vertices[prev_index]
        point = component.vertices[index]
        next_point = component.vertices[(index + 1) % n]
        back_length = lengths[prev_index]
        forward_length = lengths[next_index]
    else:
        if index == 0 or index == n - 1:
            return np.zeros(3), np.zeros(3), True
        prev_point = component.vertices[index - 1]
        point = component.vertices[index]
        next_point = component.vertices[index + 1]
        back_length = lengths[index - 1]
        forward_length = lengths[index]
    if back_length <= tol or forward_length <= tol:
        return np.zeros(3), np.zeros(3), True
    tangent_in = (point - prev_point) / back_length
    tangent_out = (next_point - point) / forward_length
    return tangent_in, tangent_out, False


def _endpoint_normal_condition(vector_from_other: np.ndarray, tangent_in: np.ndarray, tangent_out: np.ndarray, tol: float) -> bool:
    """Test the one-sided local-minimum cone at a polygon vertex."""

    return bool(np.dot(vector_from_other, tangent_out) >= -tol and np.dot(vector_from_other, tangent_in) <= tol)


def _cyclic_edge_distance(i: int, j: int, n: int, closed: bool) -> int:
    delta = abs(int(i) - int(j))
    return min(delta, n - delta) if closed else delta


def _edges_are_adjacent(a: _ComponentData, i: int, b: _ComponentData, j: int) -> bool:
    if a.component != b.component:
        return False
    return _cyclic_edge_distance(i, j, a.n_vertices, a.closed) <= 1


def _vertex_edge_incident(vertex: int, edge: int, component: _ComponentData) -> bool:
    if component.closed:
        return edge == vertex or edge == (vertex - 1) % component.n_vertices
    return edge == vertex or edge == vertex - 1


def _vertices_adjacent(a: _ComponentData, i: int, b: _ComponentData, j: int) -> bool:
    if a.component != b.component:
        return False
    if a.closed:
        return _cyclic_edge_distance(i, j, a.n_vertices, True) <= 1
    return abs(i - j) <= 1


def _segment_closest(a0: np.ndarray, a1: np.ndarray, b0: np.ndarray, b1: np.ndarray, tol: float) -> tuple[float, float, float, float, float]:
    """Minimize squared distance on the parameter rectangle by active faces.

    The quadratic minimum lies at an interior stationary point or on a face.
    Length degeneracy and the dimensionless parallel condition are distinct.
    Cross-product formulas avoid cancellation in aa*bb-ab**2.
    """
    u, v, w = a1-a0, b1-b0, a0-b0
    aa, bb = float(u@u), float(v@v)
    length_sq_tol = float(tol)**2
    choices = []
    if aa <= length_sq_tol and bb <= length_sq_tol:
        choices.append((0.0, 0.0))
    elif aa <= length_sq_tol:
        choices.append((0.0, float(np.clip((w@v)/bb, 0, 1))))
    elif bb <= length_sq_tol:
        choices.append((float(np.clip(-(w@u)/aa, 0, 1)), 0.0))
    else:
        cross_uv = np.cross(u, v)
        denominator = float(cross_uv@cross_uv)
        if denominator > 0.0:
            ss = float(np.dot(np.cross(v, w), cross_uv)/denominator)
            tt = float(np.dot(np.cross(u, w), cross_uv)/denominator)
            if 0.0 <= ss <= 1.0 and 0.0 <= tt <= 1.0:
                choices.append((ss, tt))
        for ss in (0.0, 1.0):
            choices.append((ss, float(np.clip(((w+ss*u)@v)/bb, 0, 1))))
        for tt in (0.0, 1.0):
            choices.append((float(np.clip(((tt*v-w)@u)/aa, 0, 1)), tt))
        if denominator == 0.0:
            # A flat minimum may have interior struts even if an endpoint is
            # also a minimizer. Include midpoint representatives of overlap.
            projections = sorted((float((-w)@u/aa), float((v-w)@u/aa)))
            left, right = max(0.0, projections[0]), min(1.0, projections[1])
            if left <= right:
                ss = (left+right)/2
                choices.insert(0, (ss, float(np.clip(((w+ss*u)@v)/bb, 0, 1))))
    def distance_squared(pair):
        delta = w+pair[0]*u-pair[1]*v
        return float(delta@delta)
    s, t = min(choices, key=distance_squared)
    difference = w+s*u-t*v
    distance = float(np.linalg.norm(difference))
    ra = abs(float(difference@u))/np.sqrt(aa) if aa > length_sq_tol else 0.0
    rb = abs(float(difference@v))/np.sqrt(bb) if bb > length_sq_tol else 0.0
    return float(s), float(t), distance, float(ra), float(rb)


def _candidate_sort_key(candidate: DoublyCriticalCandidate):
    return candidate.distance, candidate.kind, candidate.component_a, candidate.index_a, candidate.component_b, candidate.index_b


def polygon_thickness(
    value: Any,
    *,
    samples: int = 256,
    tolerances: ThicknessTolerances | None = None,
    tol: float | None = None,
    include_rejected: bool = False,
) -> ThicknessResult:
    """Estimate radius thickness of a polygonal curve or link.

    ``samples`` only affects analytic inputs; polygon input is used as given.
    The result is a numerical polygon-model estimate.  ``complete`` means all
    finite vv/ve/ee pairs in the supplied polygon were enumerated, not that a
    sampled polygon certifies the underlying smooth curve.
    """

    if tolerances is None:
        tolerances = ThicknessTolerances(
            distance=float(tol) if tol is not None else 1e-9,
            relative_distance=float(tol) if tol is not None else 1e-9,
            orthogonality=max(1e-8, float(tol)) if tol is not None else 1e-8,
            endpoint=max(1e-8, float(tol)) if tol is not None else 1e-8,
            degeneracy=max(1e-12, float(tol)) if tol is not None else 1e-12,
        )
    components = _coerce_components(value, samples=int(samples))
    for component in components:
        if component.vertices.ndim != 2 or component.vertices.shape[1] != 3:
            raise ValueError("all vertices must have shape (n,3)")
        if not np.all(np.isfinite(component.vertices)):
            raise ValueError("all vertices must be finite")
        if component.n_vertices < (3 if component.closed else 2):
            raise ValueError("component has too few vertices")

    kink_geometry: list[KinkGeometry] = []
    minrad = float("inf")
    degenerate = False
    notes: list[str] = []
    all_lengths: list[np.ndarray] = []
    for component in components:
        lengths = _edge_lengths(component)
        all_lengths.append(lengths)
        if np.any(lengths <= tolerances.degeneracy):
            degenerate = True
            notes.append(f"component {component.component} contains a zero/near-zero edge")
        if component.closed:
            vertex_indices = range(component.n_vertices)
        else:
            vertex_indices = range(1, component.n_vertices - 1)
        for index in vertex_indices:
            tangent_in, tangent_out, bad = _vertex_tangents(component, index, lengths, tolerances.degeneracy)
            if bad:
                radius = 0.0
                angle = float("nan")
            else:
                dot = float(np.clip(np.dot(tangent_in, tangent_out), -1.0, 1.0))
                angle = float(np.arccos(dot))
                cross_norm = float(np.linalg.norm(np.cross(tangent_in, tangent_out)))
                side_a = float(lengths[(index - 1) % component.n_vertices]) if component.closed else float(lengths[index - 1])
                side_b = float(lengths[index % component.n_vertices]) if component.closed else float(lengths[index])
                if cross_norm <= tolerances.degeneracy:
                    # Straight collinear vertices have infinite local radius;
                    # a tangent reversal is a genuine zero-radius kink.
                    radius = 0.0 if dot < 0.0 else float("inf")
                else:
                    # Rawdon's polygonal MinRad is the radius of the largest
                    # tangent disk at the vertex, not the circumradius of the
                    # three vertices.  With turning angle theta this is
                    # min(|e_-|,|e_+|)/(2 tan(theta/2)).
                    tangent_half = float(np.tan(0.5 * angle))
                    radius = min(side_a, side_b) / (2.0 * tangent_half) if tangent_half > tolerances.degeneracy else float("inf")
                if radius < minrad:
                    minrad = radius
            kink_geometry.append(KinkGeometry(component.component, index, float(index), radius, angle, (float(lengths[(index - 1) % component.n_vertices]) if component.closed else float(lengths[index - 1]), float(lengths[index % component.n_vertices]) if component.closed else float(lengths[index])), bad))
    if not kink_geometry and any(not component.closed for component in components):
        minrad = float("inf")
    if degenerate:
        minrad = 0.0

    candidates: list[DoublyCriticalCandidate] = []
    rejected: list[DoublyCriticalCandidate] = []
    # Vertex--vertex.
    for a in components:
        for b in components:
            if a.component > b.component:
                continue
            for ia in range(a.n_vertices):
                start_ib = ia + 1 if a.component == b.component else 0
                for ib in range(start_ib, b.n_vertices):
                    if _vertices_adjacent(a, ia, b, ib):
                        continue
                    point_a = a.vertices[ia]
                    point_b = b.vertices[ib]
                    vector_a = point_a - point_b
                    distance = float(np.linalg.norm(vector_a))
                    ta_in, ta_out, bad_a = _vertex_tangents(a, ia, all_lengths[a.component], tolerances.degeneracy)
                    tb_in, tb_out, bad_b = _vertex_tangents(b, ib, all_lengths[b.component], tolerances.degeneracy)
                    if distance <= tolerances.degeneracy:
                        # A nonadjacent coincident vertex is a geometric
                        # collision even when its one-sided normal cones do
                        # not make it a regular DCSD stationary point.
                        degenerate = True
                        collision = DoublyCriticalCandidate("vertex-vertex", distance, a.component, ia, float(ia), b.component, ib, float(ib), True, "zero-distance collision", 0.0, None, "nonadjacent coincident vertices force zero thickness")
                        candidates.append(collision)
                        notes.append(f"nonadjacent coincident vertices at ({a.component},{ia}) and ({b.component},{ib})")
                        continue
                    critical = not bad_a and not bad_b and distance > tolerances.degeneracy and _endpoint_normal_condition(vector_a, ta_in, ta_out, tolerances.orthogonality) and _endpoint_normal_condition(-vector_a, tb_in, tb_out, tolerances.orthogonality)
                    candidate = DoublyCriticalCandidate("vertex-vertex", distance, a.component, ia, float(ia), b.component, ib, float(ib), critical, "verified" if critical else "endpoint normal-cone condition failed", 0.0, None)
                    (candidates if critical else rejected).append(candidate)

    # Vertex--edge, including both orientations so a candidate is labelled
    # with the actual vertex and edge roles.
    for vertex_component in components:
        for vertex_index in range(vertex_component.n_vertices):
            point = vertex_component.vertices[vertex_index]
            tangent_in, tangent_out, bad_vertex = _vertex_tangents(vertex_component, vertex_index, all_lengths[vertex_component.component], tolerances.degeneracy)
            for edge_component in components:
                for edge_index in range(edge_component.n_edges):
                    if vertex_component.component == edge_component.component and _vertex_edge_incident(vertex_index, edge_index, edge_component):
                        continue
                    edge_start, edge_end = edge_component.edge(edge_index)
                    edge_vector = edge_end - edge_start
                    edge_length_sq = float(np.dot(edge_vector, edge_vector))
                    if edge_length_sq <= tolerances.degeneracy**2:
                        continue
                    projection = float(np.dot(point - edge_start, edge_vector) / edge_length_sq)
                    if projection <= 0.0 or projection >= 1.0:
                        continue
                    closest = edge_start + projection * edge_vector
                    difference = point - closest
                    distance = float(np.linalg.norm(difference))
                    if distance <= tolerances.degeneracy:
                        degenerate = True
                        collision = DoublyCriticalCandidate("vertex-edge", distance, vertex_component.component, vertex_index, float(vertex_index), edge_component.component, edge_index, float(edge_index + projection), True, "zero-distance collision", 0.0, min(projection, 1.0 - projection), "nonadjacent vertex on edge forces zero thickness")
                        candidates.append(collision)
                        notes.append(f"nonadjacent vertex-edge collision at ({vertex_component.component},{vertex_index})/({edge_component.component},{edge_index})")
                        continue
                    residual = abs(float(np.dot(difference, edge_vector / np.sqrt(edge_length_sq))))
                    critical = not bad_vertex and distance > tolerances.degeneracy and residual <= tolerances.orthogonality and _endpoint_normal_condition(difference, tangent_in, tangent_out, tolerances.orthogonality)
                    candidate = DoublyCriticalCandidate("vertex-edge", distance, vertex_component.component, vertex_index, float(vertex_index), edge_component.component, edge_index, float(edge_index + projection), critical, "verified" if critical else "vertex normal-cone condition failed", residual, min(projection, 1.0 - projection))
                    (candidates if critical else rejected).append(candidate)

    # Edge--edge interiors.  Endpoint solutions are already covered by vv/ve
    # and are intentionally not duplicated here.
    for ai, a in enumerate(components):
        for bi in range(ai, len(components)):
            b = components[bi]
            for ia in range(a.n_edges):
                for ib in range(b.n_edges):
                    if a.component == b.component and ia >= ib:
                        continue
                    if _edges_are_adjacent(a, ia, b, ib):
                        continue
                    a0, a1 = a.edge(ia)
                    b0, b1 = b.edge(ib)
                    s, t, distance, residual_a, residual_b = _segment_closest(a0, a1, b0, b1, tolerances.degeneracy)
                    if distance <= tolerances.degeneracy:
                        degenerate = True
                        candidates.append(DoublyCriticalCandidate("edge-edge", distance, a.component, ia, float(ia+s), b.component, ib, float(ib+t), True, "zero-distance collision", max(residual_a,residual_b), None, "nonadjacent segment intersection forces zero thickness"))
                        notes.append(f"nonadjacent edge collision at ({a.component},{ia})/({b.component},{ib})")
                        continue
                    interior = 0.0 < s < 1.0 and 0.0 < t < 1.0
                    residual = max(residual_a, residual_b)
                    if not interior:
                        continue
                    critical = residual <= tolerances.orthogonality
                    candidate = DoublyCriticalCandidate("edge-edge", distance, a.component, ia, float(ia + s), b.component, ib, float(ib + t), critical, "verified" if critical else "orthogonality residual above tolerance", residual, min(s, 1.0 - s, t, 1.0 - t))
                    (candidates if critical else rejected).append(candidate)

    candidates.sort(key=_candidate_sort_key)
    rejected.sort(key=_candidate_sort_key)
    if candidates:
        dcsd = float(candidates[0].distance)
    else:
        dcsd = float("inf")
        notes.append("no verified nonadjacent doubly-critical candidate was found")
    dcsd_half = 0.5 * dcsd
    thickness = min(float(minrad), dcsd_half)
    if not np.isfinite(thickness):
        thickness = float("inf")
    if degenerate:
        thickness = 0.0
    if minrad <= dcsd_half:
        limiting = "minrad"
    elif np.isfinite(dcsd_half):
        limiting = "dcsd"
    else:
        limiting = "none"
    total_length = float(sum(float(np.linalg.norm(np.roll(item.vertices, -1, axis=0) - item.vertices, axis=1).sum()) if item.closed else float(np.linalg.norm(np.diff(item.vertices, axis=0), axis=1).sum()) for item in components))
    result = ThicknessResult(thickness, float(minrad), dcsd, candidates, rejected if include_rejected else [], not degenerate, degenerate, total_length, limiting, tolerances, len(components), notes)
    return result


def estimate_polygon_thickness(value: Any, **kwargs: Any) -> ThicknessResult:
    return polygon_thickness(value, **kwargs)


def polygon_minrad(value: Any, **kwargs: Any) -> float:
    return polygon_thickness(value, **kwargs).minrad


def doubly_critical_candidates(value: Any, **kwargs: Any) -> list[DoublyCriticalCandidate]:
    return polygon_thickness(value, **kwargs).candidates


__all__ = [
    "DoublyCriticalCandidate",
    "KinkGeometry",
    "ThicknessResult",
    "ThicknessTolerances",
    "doubly_critical_candidates",
    "estimate_polygon_thickness",
    "polygon_minrad",
    "polygon_thickness",
]
