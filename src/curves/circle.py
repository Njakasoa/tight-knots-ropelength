"""Exact circular curves and the round Hopf link."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .base import Curve, CurveComponent, Link


def _plane_basis(normal: Sequence[float] | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if normal is None:
        return np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])
    n = np.asarray(normal, dtype=float)
    if n.shape != (3,) or not np.all(np.isfinite(n)):
        raise ValueError("normal must be a finite 3-vector")
    norm = np.linalg.norm(n)
    if norm == 0:
        raise ValueError("normal must be nonzero")
    n = n / norm
    trial = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.8 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(n, trial)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    return e1, e2, n


class Circle(Curve):
    """A circle with exact analytic derivatives.

    ``parameter`` is an angle in radians.  The default is the unit circle in
    the xy plane.  ``normal`` can be supplied to orient the disk in an
    arbitrary plane; ``phase`` rotates the starting point in that plane.
    """

    def __init__(
        self,
        radius: float = 1.0,
        center: Sequence[float] = (0.0, 0.0, 0.0),
        *,
        normal: Sequence[float] | None = None,
        phase: float = 0.0,
        name: str = "circle",
    ):
        radius = float(radius)
        center_array = np.asarray(center, dtype=float)
        if radius <= 0 or not np.isfinite(radius):
            raise ValueError("radius must be positive and finite")
        if center_array.shape != (3,) or not np.all(np.isfinite(center_array)):
            raise ValueError("center must be a finite 3-vector")
        e1, e2, n = _plane_basis(normal)
        phase = float(phase)

        def position(t):
            t = np.asarray(t)
            a = t + phase
            return center_array + radius * (np.cos(a)[..., None] * e1 + np.sin(a)[..., None] * e2)

        def derivative(t):
            t = np.asarray(t)
            a = t + phase
            return radius * (-np.sin(a)[..., None] * e1 + np.cos(a)[..., None] * e2)

        def second_derivative(t):
            t = np.asarray(t)
            a = t + phase
            return radius * (-np.cos(a)[..., None] * e1 - np.sin(a)[..., None] * e2)

        metadata = {
            "kind": "circle",
            "radius": radius,
            "center": center_array.tolist(),
            "normal": n.tolist(),
            "phase": phase,
            "exact_length": 2.0 * math.pi * radius,
            "curvature": 1.0 / radius,
            "known_thickness": radius,
            "construction": "exact circle",
        }
        super().__init__(
            [
                CurveComponent(
                    position,
                    derivative,
                    second_derivative,
                    period=2.0 * math.pi,
                    closed=True,
                    component=0,
                    name=name,
                    metadata=metadata,
                )
            ],
            name=name,
            metadata=metadata,
        )
        self.radius = radius
        self.center = center_array
        self.normal = n
        self.phase = phase


def circle(
    radius: float = 1.0,
    center: Sequence[float] = (0.0, 0.0, 0.0),
    *,
    normal: Sequence[float] | None = None,
    phase: float = 0.0,
    name: str = "circle",
) -> Circle:
    """Construct an exact circular curve."""

    return Circle(radius, center, normal=normal, phase=phase, name=name)


class HopfLink(Link):
    """The standard round Hopf arrangement.

    For circle radius ``a``,

    ``A(u)=(a cos u,a sin u,0)`` and
    ``B(v)=(a+a cos v,0,a sin v)``.

    At ``a=2`` the union has reach one and total length ``8*pi``.  The
    construction metadata records that fact; numerical topology and
    thickness routines still operate on sampled data independently.
    """

    def __init__(self, radius: float = 2.0, *, name: str = "round Hopf link"):
        a = float(radius)
        if a <= 0 or not np.isfinite(a):
            raise ValueError("radius must be positive and finite")

        def apos(t):
            t = np.asarray(t)
            return np.stack((a * np.cos(t), a * np.sin(t), np.zeros_like(t)), axis=-1)

        def ad1(t):
            t = np.asarray(t)
            return np.stack((-a * np.sin(t), a * np.cos(t), np.zeros_like(t)), axis=-1)

        def ad2(t):
            t = np.asarray(t)
            return np.stack((-a * np.cos(t), -a * np.sin(t), np.zeros_like(t)), axis=-1)

        def bpos(t):
            t = np.asarray(t)
            return np.stack((a + a * np.cos(t), np.zeros_like(t), a * np.sin(t)), axis=-1)

        def bd1(t):
            t = np.asarray(t)
            return np.stack((-a * np.sin(t), np.zeros_like(t), a * np.cos(t)), axis=-1)

        def bd2(t):
            t = np.asarray(t)
            return np.stack((-a * np.cos(t), np.zeros_like(t), -a * np.sin(t)), axis=-1)

        common = {"kind": "hopf", "radius": a, "curvature": 1.0 / a, "known_thickness": a / 2.0}
        components = [
            CurveComponent(
                apos,
                ad1,
                ad2,
                period=2.0 * math.pi,
                component=0,
                name="A",
                metadata={**common, "component_role": "A", "exact_length": 2.0 * math.pi * a},
            ),
            CurveComponent(
                bpos,
                bd1,
                bd2,
                period=2.0 * math.pi,
                component=1,
                name="B",
                metadata={**common, "component_role": "B", "exact_length": 2.0 * math.pi * a},
            ),
        ]
        metadata = {
            **common,
            "component_count": 2,
            "pairwise_linking": [[0, 1], [1, 0]],
            "construction": "round Hopf link",
            "exact_total_length": 4.0 * math.pi * a,
            "exact_intercomponent_distance": a,
            "topology": "Hopf link",
        }
        super().__init__(components, name=name, metadata=metadata)
        self.radius = a


def hopf_link(radius: float = 2.0, *, name: str = "round Hopf link") -> HopfLink:
    return HopfLink(radius, name=name)


def round_hopf(radius: float = 2.0, *, name: str = "round Hopf link") -> HopfLink:
    """Alias matching the terminology used in the positive-control proof."""

    return HopfLink(radius, name=name)


__all__ = ["Circle", "circle", "HopfLink", "hopf_link", "round_hopf"]
