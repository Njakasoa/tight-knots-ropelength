"""Rigorous arithmetic and finite-family reproduction for the shell candidate."""

from .arb_backend import arb_record, arb_precision, validate_backend
from .integrals import certify_integrals
from .shell_family import finite_family_record, populations_for_t, write_sampled_geometry

__all__ = [
    "arb_precision",
    "arb_record",
    "certify_integrals",
    "finite_family_record",
    "populations_for_t",
    "validate_backend",
    "write_sampled_geometry",
]
