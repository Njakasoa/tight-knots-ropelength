"""Geomview VECT polygon input/output.

The reader accepts the VECT files emitted by plCurve/Ridgerunner, including
comments and per-component RGBA colours.  A negative vertex count denotes a
closed polyline in the VECT convention.  Closed input is never repaired by
silently joining unrelated endpoints; an optional repeated endpoint is
removed only after the closure has been checked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from .base import Curve, CurveComponent, Link


class VECTParseError(ValueError):
    """Raised for malformed or non-closed VECT input."""


@dataclass
class PolygonComponent:
    vertices: np.ndarray
    closed: bool = True
    component: int = 0
    name: str = "polygon component"
    colors: np.ndarray | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        values = np.asarray(self.vertices, dtype=float)
        if values.ndim != 2 or values.shape[1] != 3:
            raise ValueError("vertices must have shape (n,3)")
        if values.shape[0] < (3 if self.closed else 2):
            raise ValueError("a polygon component has too few vertices")
        if not np.all(np.isfinite(values)):
            raise ValueError("vertices must be finite")
        self.vertices = values.copy()
        self.closed = bool(self.closed)
        if self.colors is not None:
            colours = np.asarray(self.colors, dtype=float)
            if colours.ndim == 1:
                colours = colours[None, :]
            if colours.shape[1] not in (3, 4):
                raise ValueError("colors must have 3 or 4 channels")
            self.colors = colours.copy()

    @property
    def vertex_count(self) -> int:
        return int(self.vertices.shape[0])

    @property
    def edge_count(self) -> int:
        return self.vertex_count if self.closed else self.vertex_count - 1

    def edge(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        index = int(index)
        if index < 0 or index >= self.edge_count:
            raise IndexError(index)
        return self.vertices[index], self.vertices[(index + 1) % self.vertex_count]

    def length(self) -> float:
        if self.closed:
            differences = np.roll(self.vertices, -1, axis=0) - self.vertices
        else:
            differences = np.diff(self.vertices, axis=0)
        return float(np.linalg.norm(differences, axis=1).sum())

    @property
    def total_length(self) -> float:
        return self.length()

    def sample(self, count: int | None = None, *, include_endpoint: bool = False) -> np.ndarray:
        """Return polygon vertices or a linearly resampled polygon.

        ``count=None`` returns a copy of the stored vertices.  Resampling is
        useful for projection routines and preserves the component boundary
        convention without duplicating closed endpoints by default.
        """

        if count is None or int(count) == self.vertex_count:
            out = self.vertices.copy()
            if include_endpoint and self.closed:
                return np.vstack((out, out[0]))
            return out
        count = int(count)
        if count < (3 if self.closed else 2):
            raise ValueError("resampled component has too few points")
        edge_vectors = (np.roll(self.vertices, -1, axis=0) - self.vertices) if self.closed else np.diff(self.vertices, axis=0)
        edge_lengths = np.linalg.norm(edge_vectors, axis=1)
        cumulative = np.concatenate(([0.0], np.cumsum(edge_lengths)))
        total = float(cumulative[-1])
        if total <= 0:
            raise ValueError("cannot resample a zero-length component")
        endpoint = self.closed and not include_endpoint
        positions = np.linspace(0.0, total, count, endpoint=not endpoint)
        edge_indices = np.searchsorted(cumulative, positions, side="right") - 1
        edge_indices = np.clip(edge_indices, 0, len(edge_lengths) - 1)
        local = positions - cumulative[edge_indices]
        fractions = np.divide(local, edge_lengths[edge_indices], out=np.zeros_like(local), where=edge_lengths[edge_indices] > 0)
        out = self.vertices[edge_indices] + fractions[:, None] * edge_vectors[edge_indices]
        if include_endpoint and self.closed:
            out = np.vstack((out, out[0]))
        return out


class PolygonLink:
    """A finite collection of polygon components parsed from or written to VECT."""

    def __init__(self, components: Iterable[PolygonComponent], *, name: str = "polygon link", metadata: dict[str, Any] | None = None):
        values = tuple(components)
        if not values:
            raise ValueError("a polygon link must contain at least one component")
        for index, component in enumerate(values):
            if not isinstance(component, PolygonComponent):
                raise TypeError("components must be PolygonComponent instances")
            component.component = index
        self.components = values
        self.name = name
        self.metadata = dict(metadata or {})
        self.metadata.setdefault("component_count", len(values))

    def __iter__(self):
        return iter(self.components)

    def __len__(self) -> int:
        return len(self.components)

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def closed(self) -> bool:
        return all(component.closed for component in self.components)

    def component(self, index: int = 0) -> PolygonComponent:
        return self.components[int(index)]

    @property
    def vertices(self) -> np.ndarray:
        if len(self.components) != 1:
            raise AttributeError("vertices is only unambiguous for a one-component polygon")
        return self.components[0].vertices

    def sample(self, count: int | None = None, *, component: int | None = None, include_endpoint: bool = False):
        if component is not None:
            return self.component(component).sample(count, include_endpoint=include_endpoint)
        arrays = [item.sample(count, include_endpoint=include_endpoint) for item in self.components]
        return arrays[0] if len(arrays) == 1 else arrays

    def sample_components(self, count: int | None = None, *, include_endpoint: bool = False) -> list[np.ndarray]:
        return [item.sample(count, include_endpoint=include_endpoint) for item in self.components]

    def length(self, component: int | None = None) -> float:
        if component is None:
            return float(sum(item.length() for item in self.components))
        return self.component(component).length()

    @property
    def total_length(self) -> float:
        return self.length()


def _numeric_tokens(path: Path) -> list[str]:
    tokens: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.split("#", 1)[0].strip()
            if line:
                tokens.extend(line.split())
    return tokens


def _read_int(token: str, *, what: str) -> int:
    try:
        value = int(token)
    except ValueError as error:
        raise VECTParseError(f"invalid {what}: {token!r}") from error
    return value


def read_vect(path: str | Path, *, require_closed: bool = True, closure_tolerance: float = 1e-10) -> PolygonLink:
    """Read a Geomview VECT file and validate component closure metadata."""

    path = Path(path)
    tokens = _numeric_tokens(path)
    if not tokens or tokens[0].upper() != "VECT":
        raise VECTParseError(f"{path} does not start with VECT")
    if len(tokens) < 4:
        raise VECTParseError("VECT header is incomplete")
    n_components = _read_int(tokens[1], what="component count")
    n_vertices = _read_int(tokens[2], what="vertex count")
    n_colors = _read_int(tokens[3], what="color count")
    if n_components <= 0 or n_vertices < 0 or n_colors < 0:
        raise VECTParseError("VECT header counts must be nonnegative and component count positive")
    cursor = 4
    if len(tokens) < cursor + n_components:
        raise VECTParseError("missing per-component vertex counts")
    vertex_counts_signed = [_read_int(tokens[cursor + i], what="vertices per component") for i in range(n_components)]
    cursor += n_components
    if any(count == 0 for count in vertex_counts_signed):
        raise VECTParseError("zero-vertex components are not supported")
    closed_flags = [count < 0 for count in vertex_counts_signed]
    vertex_counts = [abs(count) for count in vertex_counts_signed]
    if sum(vertex_counts) != n_vertices:
        raise VECTParseError(f"header reports {n_vertices} vertices but component counts sum to {sum(vertex_counts)}")
    if require_closed and not all(closed_flags):
        raise VECTParseError("VECT input contains an open component while require_closed=True")

    # VECT always has one colour-count integer per component, including zero
    # colour files. Skipping this row shifts every coordinate by one token.
    if len(tokens) < cursor + n_components:
        raise VECTParseError("missing per-component color counts")
    color_counts = [_read_int(tokens[cursor + i], what="colors per component") for i in range(n_components)]
    cursor += n_components
    if any(value < 0 for value in color_counts) or sum(color_counts) != n_colors:
        raise VECTParseError("per-component color counts do not match VECT color count")

    coordinates_needed = 3 * n_vertices
    if len(tokens) < cursor + coordinates_needed:
        raise VECTParseError("VECT file ends before all coordinates")
    coordinates = np.asarray([float(token) for token in tokens[cursor : cursor + coordinates_needed]], dtype=float).reshape((-1, 3))
    cursor += coordinates_needed

    # Geomview examples use RGBA quadruples.  Be permissive with RGB triples
    # from older files while retaining all colour values in metadata.
    colours: list[np.ndarray] = []
    if n_colors:
        remaining = len(tokens) - cursor
        channels = 4 if remaining >= 4 * n_colors else 3 if remaining >= 3 * n_colors else 0
        if channels == 0:
            raise VECTParseError("VECT file ends before all color values")
        for count in color_counts:
            if count:
                size = count * channels
                values = np.asarray([float(token) for token in tokens[cursor : cursor + size]], dtype=float).reshape((count, channels))
                cursor += size
                colours.append(values)
            else:
                colours.append(np.empty((0, channels), dtype=float))
    if cursor != len(tokens):
        raise VECTParseError(f"unexpected trailing VECT tokens starting at {tokens[cursor]!r}")

    components: list[PolygonComponent] = []
    offset = 0
    for index, (count, closed) in enumerate(zip(vertex_counts, closed_flags)):
        values = coordinates[offset : offset + count].copy()
        offset += count
        if closed and len(values) >= 2 and np.linalg.norm(values[0] - values[-1]) <= closure_tolerance:
            values = values[:-1]
            if len(values) < 3:
                raise VECTParseError("closed component collapses after removing repeated endpoint")
        component_colours = colours[index] if colours else None
        components.append(PolygonComponent(values, closed=closed, component=index, name=f"component {index}", colors=component_colours))
    return PolygonLink(components, name=path.stem, metadata={"source": str(path), "format": "Geomview VECT"})


def _coerce_polygon_link(value: Any, *, samples: int = 256) -> PolygonLink:
    if isinstance(value, PolygonLink):
        return value
    if isinstance(value, PolygonComponent):
        return PolygonLink([value])
    if isinstance(value, Curve):
        components = [PolygonComponent(component.sample(samples), closed=component.closed, component=index) for index, component in enumerate(value.components)]
        return PolygonLink(components, name=value.name, metadata=dict(value.metadata))
    try:
        array = np.asarray(value, dtype=float)
    except (TypeError, ValueError):
        array = np.asarray([], dtype=float)
    if array.ndim == 2 and array.shape[1] == 3:
        return PolygonLink([PolygonComponent(array, closed=True)])
    if isinstance(value, (list, tuple)):
        try:
            components = [PolygonComponent(np.asarray(item, dtype=float), closed=True, component=index) for index, item in enumerate(value)]
            return PolygonLink(components)
        except (TypeError, ValueError) as error:
            raise TypeError("cannot coerce value to polygon components") from error
    raise TypeError(f"cannot coerce {type(value).__name__} to PolygonLink")


def write_vect(
    path: str | Path,
    value: PolygonLink | PolygonComponent | Curve | np.ndarray | Sequence[np.ndarray],
    *,
    samples: int = 256,
    precision: int = 17,
    colors: Sequence[Sequence[float]] | None = None,
    overwrite: bool = True,
) -> Path:
    """Write a polygon or analytic curve in a Ridgerunner compatible VECT form."""

    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(path)
    polygon = _coerce_polygon_link(value, samples=samples)
    n_components = polygon.component_count
    n_vertices = sum(item.vertex_count for item in polygon.components)
    if colors is None:
        rgba = [np.array([0.0, 1.0, 0.0, 1.0], dtype=float) for _ in range(n_components)]
    else:
        if len(colors) != n_components:
            raise ValueError("colors must contain one RGB/RGBA value per component")
        rgba = []
        for color in colors:
            value_array = np.asarray(color, dtype=float)
            if value_array.shape == (3,):
                value_array = np.r_[value_array, 1.0]
            if value_array.shape != (4,):
                raise ValueError("each color must have 3 or 4 channels")
            rgba.append(value_array)
    lines = ["VECT", f"{n_components} {n_vertices} {n_components}"]
    lines.append(" ".join(str(-item.vertex_count if item.closed else item.vertex_count) for item in polygon.components))
    lines.append(" ".join("1" for _ in polygon.components))
    for item in polygon.components:
        lines.extend(" ".join(format(float(number), f".{int(precision)}g") for number in vertex) for vertex in item.vertices)
    lines.append("# Colors (red green blue alpha)")
    for index, color in enumerate(rgba):
        lines.append(f"# Component {index}")
        lines.append(" ".join(format(float(number), f".{int(precision)}g") for number in color))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


read_VECT = read_vect
write_VECT = write_vect


__all__ = ["PolygonComponent", "PolygonLink", "VECTParseError", "read_vect", "read_VECT", "write_vect", "write_VECT"]
