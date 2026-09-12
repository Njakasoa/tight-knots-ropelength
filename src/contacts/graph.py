"""Finite contact and kink extraction from the polygon thickness search."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np

try:  # support both ``PYTHONPATH=repo`` and ``PYTHONPATH=repo/src``
    from thickness.polygon import ThicknessResult, polygon_thickness
except ImportError:  # pragma: no cover - package-layout fallback
    from src.thickness.polygon import ThicknessResult, polygon_thickness


@dataclass
class Contact:
    component_a: int
    index_a: int
    parameter_a: float
    component_b: int
    index_b: int
    parameter_b: float
    distance: float
    kind: str
    tolerance: float
    active: bool = True
    criticality: str = "verified"
    note: str = ""

    @property
    def components(self) -> tuple[int, int]:
        return self.component_a, self.component_b

    @property
    def indices(self) -> tuple[int, int]:
        return self.index_a, self.index_b

    @property
    def parameters(self) -> tuple[float, float]:
        return self.parameter_a, self.parameter_b

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Kink:
    component: int
    index: int
    parameter: float
    minrad: float
    turning_angle: float
    active: bool
    tolerance: float
    note: str = "polygon vertex curvature"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ContactGraph:
    contacts: list[Contact]
    kinks: list[Kink]
    nodes: list[tuple[Any, ...]]
    edges: list[dict[str, Any]]
    summary: dict[str, Any]
    tolerance: float
    thickness_result: ThicknessResult
    notes: list[str] = field(default_factory=list)

    @property
    def struts(self) -> list[Contact]:
        return self.contacts

    @property
    def contact_count(self) -> int:
        return len(self.contacts)

    def as_dict(self) -> dict[str, Any]:
        return {
            "contacts": [contact.as_dict() for contact in self.contacts],
            "kinks": [kink.as_dict() for kink in self.kinks],
            "nodes": [list(node) for node in self.nodes],
            "edges": self.edges,
            "summary": self.summary,
            "tolerance": self.tolerance,
            "thickness": self.thickness_result.as_dict(),
            "notes": self.notes,
        }


def _component_data(value: Any, samples: int):
    try:
        from thickness.polygon import _coerce_components
    except ImportError:  # pragma: no cover - package-layout fallback
        from src.thickness.polygon import _coerce_components

    return _coerce_components(value, samples=samples)


def _kinks(value: Any, thickness: float, tolerance: float, samples: int):
    components = _component_data(value, samples)
    output: list[Kink] = []
    for component in components:
        n = component.n_vertices
        if not component.closed:
            indices = range(1, max(1, n - 1))
        else:
            indices = range(n)
        for index in indices:
            if component.closed:
                previous = component.vertices[(index - 1) % n]
                point = component.vertices[index]
                following = component.vertices[(index + 1) % n]
            else:
                previous = component.vertices[index - 1]
                point = component.vertices[index]
                following = component.vertices[index + 1]
            back = point - previous
            forward = following - point
            back_length = float(np.linalg.norm(back))
            forward_length = float(np.linalg.norm(forward))
            if back_length <= 1e-14 or forward_length <= 1e-14:
                radius = 0.0
                angle = float("nan")
            else:
                tangent_in = back / back_length
                tangent_out = forward / forward_length
                dot = float(np.clip(np.dot(tangent_in, tangent_out), -1.0, 1.0))
                angle = float(np.arccos(dot))
                turn_half = float(np.tan(0.5 * angle))
                radius = min(back_length, forward_length) / (2.0 * turn_half) if turn_half > 1e-14 else float("inf")
            output.append(Kink(component.component, index, float(index), radius, angle, radius <= thickness + tolerance, tolerance))
    return output


def extract_contacts(
    value: Any,
    *,
    thickness_result: ThicknessResult | None = None,
    tolerance: float = 1e-6,
    distance_threshold: float | None = None,
    samples: int = 256,
    include_kinks: bool = True,
) -> ContactGraph:
    """Extract a finite strut/kink graph with explicit discretization data."""

    tolerance = float(tolerance)
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError("tolerance must be finite and nonnegative")
    if thickness_result is None:
        thickness_result = polygon_thickness(value, samples=samples, include_rejected=True)
    if distance_threshold is None:
        distance_threshold = 2.0 * thickness_result.thickness + tolerance
    distance_threshold = float(distance_threshold)
    contacts: list[Contact] = []
    seen: set[tuple[Any, ...]] = set()
    for candidate in thickness_result.candidates:
        if candidate.distance > distance_threshold:
            continue
        key = (
            candidate.kind,
            candidate.component_a,
            candidate.index_a,
            candidate.component_b,
            candidate.index_b,
            round(candidate.parameter_a, 12),
            round(candidate.parameter_b, 12),
        )
        if key in seen:
            continue
        seen.add(key)
        contacts.append(Contact(candidate.component_a, candidate.index_a, candidate.parameter_a, candidate.component_b, candidate.index_b, candidate.parameter_b, candidate.distance, candidate.kind, tolerance, candidate.distance <= distance_threshold, candidate.criticality, candidate.note))
    contacts.sort(key=lambda item: (item.distance, item.component_a, item.index_a, item.component_b, item.index_b))
    kinks = _kinks(value, thickness_result.thickness, tolerance, samples) if include_kinks else []
    nodes: set[tuple[Any, ...]] = set()
    edges: list[dict[str, Any]] = []
    for contact in contacts:
        node_a = ("component", contact.component_a, contact.index_a)
        node_b = ("component", contact.component_b, contact.index_b)
        nodes.update((node_a, node_b))
        edges.append({"a": list(node_a), "b": list(node_b), "kind": contact.kind, "distance": contact.distance})
    for kink in kinks:
        nodes.add(("component", kink.component, kink.index))
    degrees: dict[str, int] = {}
    for node in nodes:
        degrees[repr(node)] = 0
    for edge in edges:
        degrees[repr(tuple(edge["a"]))] = degrees.get(repr(tuple(edge["a"])), 0) + 1
        degrees[repr(tuple(edge["b"]))] = degrees.get(repr(tuple(edge["b"])), 0) + 1
    pair_counts: dict[str, int] = {}
    for contact in contacts:
        pair = f"{contact.component_a}-{contact.component_b}"
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    summary = {
        "contact_count": len(contacts),
        "kink_count": len(kinks),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "component_pair_counts": pair_counts,
        "degree": degrees,
        "distance_threshold": distance_threshold,
        "discretization": "candidate pairs from supplied polygon; continuum struts are not reconstructed",
    }
    notes = ["finite contact graph; absence of a record does not prove absence of a continuum contact"]
    return ContactGraph(contacts, kinks, sorted(nodes, key=repr), edges, summary, tolerance, thickness_result, notes)


def contact_graph(value: Any, **kwargs: Any) -> ContactGraph:
    return extract_contacts(value, **kwargs)


def active_contacts(value: Any, **kwargs: Any) -> list[Contact]:
    return extract_contacts(value, **kwargs).contacts


__all__ = ["Contact", "ContactGraph", "Kink", "active_contacts", "contact_graph", "extract_contacts"]
