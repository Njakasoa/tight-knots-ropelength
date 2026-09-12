"""Standard torus knots and links with analytic derivatives."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from .base import Curve, CurveComponent, Link


def _validate_torus_parameters(p: int, q: int, major_radius: float, minor_radius: float) -> tuple[int, int, float, float, int]:
    p = int(p)
    q = int(q)
    if p == 0 and q == 0:
        raise ValueError("at least one torus winding number must be nonzero")
    R = float(major_radius)
    r = float(minor_radius)
    if R <= 0 or r <= 0 or not np.isfinite(R) or not np.isfinite(r):
        raise ValueError("torus radii must be positive and finite")
    if R <= r:
        raise ValueError("standard embedded torus requires major_radius > minor_radius")
    d = math.gcd(abs(p), abs(q))
    if d == 0:
        d = abs(p) if p else abs(q)
    return p, q, R, r, d


def _bezout(a: int, b: int) -> tuple[int, int, int]:
    """Return ``x,y,g`` with ``a*x+b*y=g=gcd(a,b)``."""

    old_r, r = abs(int(a)), abs(int(b))
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s * (1 if a >= 0 else -1), old_t * (1 if b >= 0 else -1), old_r


def _component_phase_offsets(p: int, q: int, d: int) -> list[tuple[float, float]]:
    """Choose d distinct torus phase pairs for primitive windings.

    A theta-only shift can duplicate components when the primitive meridional
    winding shares a factor with d.  A Bezout pair ``a,b`` with
    ``q*a-p*b=1`` gives the invariant class increment
    ``q*theta_phase-p*phi_phase=2*pi/d`` for every successive component.
    """

    if d <= 1:
        return [(0.0, 0.0)]
    a, b, g = _bezout(p, q)
    if g != 1:  # primitive p,q should be coprime; retain a defensive fallback.
        raise ValueError("component phase construction requires primitive windings")
    return [(2.0 * math.pi * b * k / d, -2.0 * math.pi * a * k / d) for k in range(d)]


@dataclass(frozen=True)
class TorusParameters:
    p: int
    q: int
    major_radius: float
    minor_radius: float
    components: int

    @property
    def reduced_p(self) -> int:
        return self.p // self.components

    @property
    def reduced_q(self) -> int:
        return self.q // self.components


def _component_functions(p: int, q: int, R: float, r: float, phase: float, phase_phi: float):
    def position(t):
        t = np.asarray(t)
        theta = p * t + phase
        phi = q * t + phase_phi
        radial = R + r * np.cos(phi)
        return np.stack((radial * np.cos(theta), radial * np.sin(theta), r * np.sin(phi)), axis=-1)

    def derivative(t):
        t = np.asarray(t)
        theta = p * t + phase
        phi = q * t + phase_phi
        radial = R + r * np.cos(phi)
        radial_d = -r * q * np.sin(phi)
        return np.stack(
            (
                radial_d * np.cos(theta) - radial * p * np.sin(theta),
                radial_d * np.sin(theta) + radial * p * np.cos(theta),
                r * q * np.cos(phi),
            ),
            axis=-1,
        )

    def second_derivative(t):
        t = np.asarray(t)
        theta = p * t + phase
        phi = q * t + phase_phi
        radial = R + r * np.cos(phi)
        radial_d = -r * q * np.sin(phi)
        radial_dd = -r * q * q * np.cos(phi)
        return np.stack(
            (
                radial_dd * np.cos(theta) - 2.0 * radial_d * p * np.sin(theta) - radial * p * p * np.cos(theta),
                radial_dd * np.sin(theta) + 2.0 * radial_d * p * np.cos(theta) - radial * p * p * np.sin(theta),
                -r * q * q * np.sin(phi),
            ),
            axis=-1,
        )

    return position, derivative, second_derivative


def torus_component(
    p: int,
    q: int,
    *,
    major_radius: float = 3.0,
    minor_radius: float = 1.0,
    phase: float = 0.0,
    phase_phi: float = 0.0,
    component: int = 0,
    name: str | None = None,
) -> CurveComponent:
    """Construct one standard torus component.

    The component is parameterised by ``t in [0,2*pi]`` as

    ``((R+r*cos(q*t+phase_phi))*cos(p*t+phase),
      (R+r*cos(q*t+phase_phi))*sin(p*t+phase), r*sin(q*t+phase_phi))``.

    For a link with ``d=gcd(p,q)`` components, use phases ``2*pi*k/d``.
    """

    full_p, full_q, R, r, d = _validate_torus_parameters(p, q, major_radius, minor_radius)
    # A component of a non-coprime T(p,q) closes after one primitive winding,
    # not after tracing the same component d times.  The phase selects which
    # of the d components is being parameterised.
    p, q = full_p // d, full_q // d
    phase = float(phase)
    phase_phi = float(phase_phi)
    if not np.isfinite(phase) or not np.isfinite(phase_phi):
        raise ValueError("phase must be finite")
    pos, d1, d2 = _component_functions(p, q, R, r, phase, phase_phi)
    parameters = TorusParameters(full_p, full_q, R, r, d)
    metadata: dict[str, Any] = {
        "kind": "torus",
        "torus_type": [full_p, full_q],
        "component_winding": [p, q],
        "component": int(component),
        "component_count": d,
        "phase": phase,
        "phase_phi": phase_phi,
        "phase_pair": [phase, phase_phi],
        "major_radius": R,
        "minor_radius": r,
        "reduced_winding": [parameters.reduced_p, parameters.reduced_q],
        "construction": "standard torus parameterization",
    }
    if d == 1:
        metadata["topology"] = f"torus knot T({full_p},{full_q})"
    else:
        metadata["topology"] = f"torus link T({full_p},{full_q}), {d} components"
    # The speed has a simple scalar formula, but the length is generally
    # elliptic/numerical.  Store the integrand for callers that want to audit
    # quadrature independently.
    metadata["speed_squared"] = "p^2 (R+r cos(qt))^2 + (r q)^2"
    return CurveComponent(
        pos,
        d1,
        d2,
        period=2.0 * math.pi,
        closed=True,
        component=int(component),
        name=name or f"T({p},{q}) component {component}",
        metadata=metadata,
    )


class TorusLink(Link):
    """Constructive standard ``T(p,q)`` torus knot/link.

    The ``d=gcd(p,q)`` phase offsets give disjoint components on the same
    embedded torus.  This is an explicit isotopy/construction fact; sampled
    polygons returned by ``sample`` still need their own topology checks.
    """

    def __init__(
        self,
        p: int,
        q: int,
        *,
        major_radius: float = 3.0,
        minor_radius: float = 1.0,
        name: str | None = None,
    ):
        p, q, R, r, d = _validate_torus_parameters(p, q, major_radius, minor_radius)
        primitive_p, primitive_q = p // d, q // d
        phase_pairs = _component_phase_offsets(primitive_p, primitive_q, d)
        components = [
            torus_component(
                p,
                q,
                major_radius=R,
                minor_radius=r,
                phase=phase_pairs[k][0],
                phase_phi=phase_pairs[k][1],
                component=k,
                name=f"T({p},{q}) component {k}",
            )
            for k in range(d)
        ]
        parameters = TorusParameters(p, q, R, r, d)
        metadata: dict[str, Any] = {
            "kind": "torus",
            "torus_type": [p, q],
            "components": d,
            "gcd": d,
            "major_radius": R,
            "minor_radius": r,
            "reduced_winding": [parameters.reduced_p, parameters.reduced_q],
            "phase_offsets": [list(pair) for pair in phase_pairs],
            "construction": "standard torus parameterization with gcd phase components",
            "isotopy_certificate": {
                "type": "standard torus link",
                "winding_numbers": [p, q],
                "components": d,
                "note": "constructive parameterization; sampled polygon type is checked independently",
            },
            "pairwise_linking_number": (p * q) // (d * d),
        }
        if d == 1:
            metadata["topology"] = f"torus knot T({p},{q})"
        else:
            metadata["topology"] = f"torus link T({p},{q})"
        super().__init__(components, name=name or metadata["topology"], metadata=metadata)
        self.p = p
        self.q = q
        self.major_radius = R
        self.minor_radius = r
        self.gcd = d
        self.parameters = parameters


def torus_link(
    p: int,
    q: int,
    *,
    major_radius: float = 3.0,
    minor_radius: float = 1.0,
    name: str | None = None,
) -> TorusLink:
    return TorusLink(p, q, major_radius=major_radius, minor_radius=minor_radius, name=name)


def torus_knot(
    p: int,
    q: int,
    *,
    major_radius: float = 3.0,
    minor_radius: float = 1.0,
    name: str | None = None,
) -> TorusLink:
    """Construct a coprime torus knot and reject non-knot inputs."""

    if math.gcd(abs(int(p)), abs(int(q))) != 1:
        raise ValueError("torus_knot requires gcd(p,q)=1; use torus_link for multiple components")
    return TorusLink(p, q, major_radius=major_radius, minor_radius=minor_radius, name=name)


def torus_curve(
    p: int,
    q: int,
    *,
    major_radius: float = 3.0,
    minor_radius: float = 1.0,
    phase: float = 0.0,
) -> Curve | CurveComponent:
    """Compatibility helper returning a component for coprime inputs.

    For non-coprime winding numbers a ``TorusLink`` is returned so no
    components are silently merged.
    """

    if math.gcd(abs(int(p)), abs(int(q))) == 1:
        component = torus_component(p, q, major_radius=major_radius, minor_radius=minor_radius, phase=phase)
        return Curve([component], name=f"T({p},{q})", metadata=dict(component.metadata))
    return torus_link(p, q, major_radius=major_radius, minor_radius=minor_radius)


__all__ = ["TorusParameters", "TorusLink", "torus_component", "torus_curve", "torus_knot", "torus_link"]
