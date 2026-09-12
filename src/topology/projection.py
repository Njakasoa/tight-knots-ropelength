"""Generic projected-crossing and linking checks for sampled geometry."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Sequence

import numpy as np

try:
    from curves.base import Curve
    from curves.vect import PolygonComponent, PolygonLink
except ImportError:  # pragma: no cover - package-layout fallback
    from src.curves.base import Curve
    from src.curves.vect import PolygonComponent, PolygonLink


DEFAULT_VIEW = np.array([0.3713906763541037, 0.5570860145311556, 0.7427813527082074], dtype=float)


@dataclass
class ProjectionCrossing:
    component_a: int
    edge_a: int
    parameter_a: float
    component_b: int
    edge_b: int
    parameter_b: float
    planar_parameter_a: float
    planar_parameter_b: float
    depth_a: float
    depth_b: float
    over: str
    sign: int
    transverse: bool = True

    @property
    def components(self) -> tuple[int, int]:
        return self.component_a, self.component_b

    @property
    def edges(self) -> tuple[int, int]:
        return self.edge_a, self.edge_b

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProjectionResult:
    crossings: list[ProjectionCrossing]
    view: tuple[float, float, float]
    component_count: int
    sample_count: int
    tolerance: float
    generic: bool
    notes: list[str] = field(default_factory=list)

    @property
    def crossing_count(self) -> int:
        return len(self.crossings)

    @property
    def ambiguous_crossings(self) -> int:
        return sum(not crossing.transverse for crossing in self.crossings)

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["crossing_count"] = self.crossing_count
        out["ambiguous_crossings"] = self.ambiguous_crossings
        return out


@dataclass
class _SampledComponents:
    points: list[np.ndarray]
    closed: list[bool]
    metadata: dict[str, Any]


def _sample_components(value: Any, samples: int) -> _SampledComponents:
    if isinstance(value, PolygonLink):
        return _SampledComponents([item.sample(None) for item in value.components], [item.closed for item in value.components], dict(value.metadata))
    if isinstance(value, PolygonComponent):
        return _SampledComponents([value.sample(None)], [value.closed], dict(value.metadata))
    if isinstance(value, Curve):
        return _SampledComponents([component.sample(samples) for component in value.components], [component.closed for component in value.components], dict(value.metadata))
    if isinstance(value, np.ndarray):
        array = np.asarray(value, dtype=float)
        if array.ndim != 2 or array.shape[1] != 3:
            raise ValueError("points must have shape (n,3)")
        return _SampledComponents([array], [True], {})
    if isinstance(value, (list, tuple)):
        try:
            array = np.asarray(value, dtype=float)
        except (ValueError, TypeError):
            array = np.asarray([], dtype=float)
        if array.ndim == 2 and array.shape[1] == 3:
            return _SampledComponents([array], [True], {})
        arrays = [np.asarray(item, dtype=float) for item in value]
        if not arrays or any(item.ndim != 2 or item.shape[1] != 3 for item in arrays):
            raise ValueError("each component must have shape (n,3)")
        return _SampledComponents(arrays, [True] * len(arrays), {})
    raise TypeError(f"cannot sample {type(value).__name__}")


def _basis(view: Sequence[float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    direction = np.asarray(view, dtype=float)
    if direction.shape != (3,) or not np.all(np.isfinite(direction)):
        raise ValueError("view must be a finite 3-vector")
    norm = np.linalg.norm(direction)
    if norm <= 0:
        raise ValueError("view must be nonzero")
    direction = direction / norm
    helper = np.array([0.0, 0.0, 1.0]) if abs(direction[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(direction, helper)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(direction, e1)
    return e1, e2, direction


def _cross2(a: np.ndarray, b: np.ndarray) -> float:
    return float(a[0] * b[1] - a[1] * b[0])


def _intersection(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, tolerance: float) -> tuple[float, float] | None:
    r = b - a
    s = d - c
    denominator = _cross2(r, s)
    scale = max(np.linalg.norm(r) * np.linalg.norm(s), 1.0)
    if abs(denominator) <= tolerance * scale:
        return None
    delta = c - a
    t = _cross2(delta, s) / denominator
    u = _cross2(delta, r) / denominator
    if t <= tolerance or t >= 1.0 - tolerance or u <= tolerance or u >= 1.0 - tolerance:
        return None
    return float(t), float(u)


def _edges_adjacent(component_a: int, edge_a: int, n_a: int, closed_a: bool, component_b: int, edge_b: int, n_b: int, closed_b: bool) -> bool:
    if component_a != component_b:
        return False
    if closed_a and closed_b:
        delta = abs(edge_a - edge_b)
        return min(delta, n_a - delta) <= 1
    return abs(edge_a - edge_b) <= 1


def projected_crossings(
    value: Any,
    *,
    samples: int = 512,
    view: Sequence[float] = DEFAULT_VIEW,
    tolerance: float = 1e-9,
) -> ProjectionResult:
    """Compute proper crossings of a generic orthogonal projection.

    Crossings at polygon vertices, projected tangencies and adjacent pieces of
    one component are omitted.  The returned diagram is an independent check
    on a sampled polygon; it does not by itself certify an analytic isotopy.
    """

    sampled = _sample_components(value, int(samples))
    e1, e2, direction = _basis(view)
    projected = [np.column_stack((points @ e1, points @ e2)) for points in sampled.points]
    depths = [points @ direction for points in sampled.points]
    crossings: list[ProjectionCrossing] = []
    for ai, points_a in enumerate(projected):
        n_a = len(points_a)
        edge_count_a = n_a if sampled.closed[ai] else n_a - 1
        for bi in range(ai, len(projected)):
            points_b = projected[bi]
            n_b = len(points_b)
            edge_count_b = n_b if sampled.closed[bi] else n_b - 1
            for edge_a in range(edge_count_a):
                a0 = points_a[edge_a]
                a1 = points_a[(edge_a + 1) % n_a]
                for edge_b in range(edge_count_b):
                    if ai == bi and edge_a >= edge_b:
                        continue
                    if _edges_adjacent(ai, edge_a, n_a, sampled.closed[ai], bi, edge_b, n_b, sampled.closed[bi]):
                        continue
                    b0 = points_b[edge_b]
                    b1 = points_b[(edge_b + 1) % n_b]
                    hit = _intersection(a0, a1, b0, b1, float(tolerance))
                    if hit is None:
                        continue
                    ta, tb = hit
                    depth_a = float(depths[ai][edge_a] + ta * (depths[ai][(edge_a + 1) % n_a] - depths[ai][edge_a]))
                    depth_b = float(depths[bi][edge_b] + tb * (depths[bi][(edge_b + 1) % n_b] - depths[bi][edge_b]))
                    tangent_a = points_a[(edge_a + 1) % n_a] - points_a[edge_a]
                    tangent_b = points_b[(edge_b + 1) % n_b] - points_b[edge_b]
                    sign_value = _cross2(tangent_a, tangent_b)
                    depth_gap = depth_a - depth_b
                    depth_tol = float(tolerance) * max(1.0, np.linalg.norm(points_a, axis=1).max(), np.linalg.norm(points_b, axis=1).max())
                    if abs(depth_gap) <= depth_tol:
                        over = "ambiguous"
                        transverse = False
                    elif depth_gap > 0:
                        over = "a"
                        transverse = True
                    else:
                        over = "b"
                        transverse = True
                    # The oriented crossing sign uses the over-strand first.
                    # The component/edge ordering is fixed separately, so a
                    # crossing where b is over reverses the raw a x b sign.
                    sign = 1 if sign_value > 0 else -1
                    if over == "b":
                        sign = -sign
                    crossings.append(
                        ProjectionCrossing(
                            ai,
                            edge_a,
                            (edge_a + ta) / n_a,
                            bi,
                            edge_b,
                            (edge_b + tb) / n_b,
                            ta,
                            tb,
                            depth_a,
                            depth_b,
                            over,
                            sign,
                            transverse,
                        )
                    )
    notes: list[str] = []
    if not crossings:
        notes.append("no proper crossings for this projection")
    if any(not crossing.transverse for crossing in crossings):
        notes.append("some projected crossings have unresolved depth ties")
    return ProjectionResult(crossings, tuple(float(item) for item in direction), len(sampled.points), int(samples), float(tolerance), not any(not item.transverse for item in crossings), notes)


def crossing_count(value: Any, **kwargs: Any) -> int:
    return projected_crossings(value, **kwargs).crossing_count


def linking_matrix(value: Any, **kwargs: Any) -> np.ndarray:
    """Return the signed linking matrix from projected intercomponent crossings."""

    result = projected_crossings(value, **kwargs)
    matrix = np.zeros((result.component_count, result.component_count), dtype=float)
    for crossing in result.crossings:
        i, j = crossing.component_a, crossing.component_b
        if i == j:
            continue
        # The enumeration stores i <= j.  The sign is the oriented crossing
        # sign for tangent_i followed by tangent_j; divide by two after the
        # signed crossing sum, as in the usual linking-number formula.
        matrix[i, j] += crossing.sign / 2.0
        matrix[j, i] -= crossing.sign / 2.0
    return matrix


def linking_numbers(value: Any, **kwargs: Any) -> dict[tuple[int, int], float]:
    matrix = linking_matrix(value, **kwargs)
    return {(i, j): float(matrix[i, j]) for i in range(len(matrix)) for j in range(i + 1, len(matrix))}


__all__ = ["DEFAULT_VIEW", "ProjectionCrossing", "ProjectionResult", "crossing_count", "linking_matrix", "linking_numbers", "projected_crossings"]
