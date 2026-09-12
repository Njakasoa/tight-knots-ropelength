"""Analytic and polygonal curve generators used by Tight Knots Lab."""

from .base import Curve, CurveComponent, Link
from .circle import Circle, HopfLink, circle, hopf_link, round_hopf
from .exact import exact_circle_control, exact_hopf_control, machin_pi_interval
from .torus import TorusLink, TorusParameters, torus_component, torus_curve, torus_knot, torus_link
from .vect import PolygonComponent, PolygonLink, VECTParseError, read_VECT, read_vect, write_VECT, write_vect

__all__ = [
    "Circle",
    "Curve",
    "CurveComponent",
    "HopfLink",
    "Link",
    "PolygonComponent",
    "PolygonLink",
    "TorusLink",
    "TorusParameters",
    "VECTParseError",
    "circle",
    "exact_circle_control",
    "exact_hopf_control",
    "hopf_link",
    "machin_pi_interval",
    "read_VECT",
    "read_vect",
    "round_hopf",
    "torus_component",
    "torus_curve",
    "torus_knot",
    "torus_link",
    "write_VECT",
    "write_vect",
]
