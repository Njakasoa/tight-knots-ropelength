"""Small exact arithmetic helpers for the positive controls.

Machin's formula is particularly convenient here because both arctangents
have alternating rational series with a simple next-term bound.  The
functions below certify an interval for ``pi`` as a rational calculation; the
geometric statements that turn it into a ropelength upper bound remain the
analytic constructions recorded in ``proofs/POSITIVE_CONTROLS.md``.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Any


def _atan_series_interval(denominator: int, terms: int) -> tuple[Fraction, Fraction]:
    if denominator <= 1:
        raise ValueError("Machin denominators must exceed one")
    if terms < 1:
        raise ValueError("terms must be positive")
    partial = Fraction(0, 1)
    for k in range(int(terms)):
        partial += Fraction((-1) ** k, (2 * k + 1) * denominator ** (2 * k + 1))
    next_term = Fraction(1, (2 * terms + 1) * denominator ** (2 * terms + 1))
    if terms % 2:
        # An odd number of terms ends above the positive alternating sum; the
        # next (negative) term supplies a rigorous lower endpoint.
        return partial - next_term, partial
    # An even number of terms ends below the sum and the next positive term
    # supplies a rigorous upper endpoint.
    return partial, partial + next_term


def machin_pi_interval(terms: int = 12) -> tuple[Fraction, Fraction]:
    """Return a rational lower/upper enclosure of pi.

    ``pi = 16 atan(1/5) - 4 atan(1/239)``.  The interval endpoints are exact
    ``fractions.Fraction`` objects.
    """

    atan5_lo, atan5_hi = _atan_series_interval(5, int(terms))
    atan239_lo, atan239_hi = _atan_series_interval(239, int(terms))
    return 16 * atan5_lo - 4 * atan239_hi, 16 * atan5_hi - 4 * atan239_lo


def fraction_decimal(value: Fraction, digits: int = 20) -> str:
    with localcontext() as context:
        context.prec = int(digits) + 8
        return format(Decimal(value.numerator) / Decimal(value.denominator), f".{int(digits)}f")


def _decimal_bound(value: Fraction, *, upper: bool, digits: int = 20) -> str:
    """Round a rational outwards using integer arithmetic only."""
    scale = 10**digits
    quotient = -((-value.numerator*scale)//value.denominator) if upper else (value.numerator*scale)//value.denominator
    sign = "-" if quotient < 0 else ""
    whole, fractional = divmod(abs(quotient), scale)
    return f"{sign}{whole}.{fractional:0{digits}d}"


def _interval_record(lower: Fraction, upper: Fraction) -> tuple[list[str], list[dict[str, str]]]:
    return ([_decimal_bound(lower, upper=False), _decimal_bound(upper, upper=True)],
            [{"numerator":str(x.numerator), "denominator":str(x.denominator)} for x in (lower,upper)])


def exact_circle_control(*, radius: Fraction | int | float = 1, terms: int = 12) -> dict[str, Any]:
    """Exact positive-control record for a circle of the given radius."""

    radius_fraction = radius if isinstance(radius, Fraction) else Fraction(radius)
    if radius_fraction <= 0:
        raise ValueError("radius must be positive")
    pi_lo, pi_hi = machin_pi_interval(terms)
    length_lo, length_hi = 2 * radius_fraction * pi_lo, 2 * radius_fraction * pi_hi
    lengths, lengths_exact = _interval_record(length_lo,length_hi)
    ropes, ropes_exact = _interval_record(2*pi_lo,2*pi_hi)
    pis, pis_exact = _interval_record(pi_lo,pi_hi)
    return {
        "construction": "unit circle" if radius_fraction == 1 else "circle",
        "normalization": "radius",
        "radius": str(radius_fraction),
        "thickness": str(radius_fraction),
        "length_interval": lengths,
        "length_rational_endpoints": lengths_exact,
        "ropelength_interval": ropes,
        "ropelength_rational_endpoints": ropes_exact,
        "ropelength_exact_expression": "2*pi",
        "pi_interval": pis,
        "pi_rational_endpoints": pis_exact,
        "terms": int(terms),
        "status": "analytic_control; rational arithmetic for pi only",
    }


def exact_hopf_control(*, circle_radius: Fraction | int | float = 2, terms: int = 12) -> dict[str, Any]:
    """Exact positive-control record for the round Hopf arrangement."""

    radius_fraction = circle_radius if isinstance(circle_radius, Fraction) else Fraction(circle_radius)
    if radius_fraction <= 0:
        raise ValueError("circle_radius must be positive")
    pi_lo, pi_hi = machin_pi_interval(terms)
    length_lo, length_hi = 4 * radius_fraction * pi_lo, 4 * radius_fraction * pi_hi
    thickness = radius_fraction / 2
    lengths, lengths_exact = _interval_record(length_lo,length_hi)
    ropes, ropes_exact = _interval_record(8*pi_lo,8*pi_hi)
    pis, pis_exact = _interval_record(pi_lo,pi_hi)
    return {
        "construction": "round Hopf link",
        "normalization": "radius",
        "circle_radius": str(radius_fraction),
        "thickness": str(thickness),
        "length_interval": lengths,
        "length_rational_endpoints": lengths_exact,
        "ropelength_interval": ropes,
        "ropelength_rational_endpoints": ropes_exact,
        "ropelength_exact_expression": "8*pi",
        "pi_interval": pis,
        "pi_rational_endpoints": pis_exact,
        "linking_number": 1,
        "terms": int(terms),
        "status": "analytic upper-control; rational arithmetic for pi only",
    }


__all__ = ["exact_circle_control", "exact_hopf_control", "fraction_decimal", "machin_pi_interval"]
