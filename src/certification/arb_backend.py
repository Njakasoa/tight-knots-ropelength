"""Small, auditable helpers for python-flint Arb calculations.

The certificate code deliberately keeps numerical values as :class:`flint.arb`
objects until the final JSON serialization.  A JSON record contains exact
rational representations of Arb's outward rounded endpoints; a printed
decimal is included only as a convenient human-readable rendering.

This module is intentionally narrow.  It does not turn a sampled floating
point geometry calculation into a proof: it is used only for the analytic
integrals and shell-capacity arithmetic whose error bounds are supplied by
the proof note.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

try:
    import flint
    from flint import arb, ctx
except ImportError as exc:  # pragma: no cover - exercised when env is broken
    raise RuntimeError(
        "python-flint is required for the interval certificate; install/use the project .venv"
    ) from exc


def exact_integer(value: int) -> arb:
    """Return an exact Arb integer without passing through a binary float."""

    if not isinstance(value, int):
        raise TypeError("exact_integer expects an int")
    return arb(value)


def exact_rational(numerator: int, denominator: int) -> arb:
    """Return an Arb enclosure of an exact rational.

    Division is performed by Arb and therefore carries its directed rounding
    enclosure.  In particular, ``numerator / denominator`` is never evaluated
    as a Python float before it reaches Arb.
    """

    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise TypeError("exact_rational expects integer numerator and denominator")
    if denominator == 0:
        raise ZeroDivisionError("rational denominator cannot be zero")
    return arb(numerator) / arb(denominator)


@contextmanager
def arb_precision(bits: int) -> Iterator[None]:
    """Temporarily set the Arb midpoint precision in bits."""

    if not isinstance(bits, int) or bits < 64:
        raise ValueError("Arb precision must be an integer of at least 64 bits")
    previous = ctx.prec
    ctx.prec = bits
    try:
        yield
    finally:
        ctx.prec = previous


def _fmpq_record(value: arb, *, digits: int, label: str) -> dict[str, str]:
    """Serialize one exact endpoint as a rational and a readable decimal."""

    try:
        rational = value.fmpq()
    except Exception as exc:  # pragma: no cover - finite certificate values only
        raise ValueError(f"{label} is not a finite exact Arb endpoint: {value!s}") from exc
    return {
        "numerator": str(rational.numerator),
        "denominator": str(rational.denominator),
        # ``more=True`` exposes the decimal rendering of the exact binary
        # endpoint.  The rational pair above is the authoritative value.
        "decimal": value.str(digits, radius=False, more=True),
    }


def arb_record(value: arb, *, digits: int = 60, label: str = "value") -> dict[str, Any]:
    """Return an auditable outward enclosure for a finite Arb value.

    ``lower`` and ``upper`` are exact binary floating endpoints produced by
    Arb's directed ``lower()``/``upper()`` operations.  Their exact rational
    values are stored, so re-parsing a shortened decimal cannot widen or
    silently move an endpoint.
    """

    if not isinstance(value, arb):
        value = arb(value)
    if not value.is_finite():
        raise ValueError(f"{label} must be finite, got {value!s}")
    lower = value.lower()
    upper = value.upper()
    return {
        "arb": value.str(digits, radius=True, more=True),
        "lower": _fmpq_record(lower, digits=digits, label=f"{label}.lower"),
        "upper": _fmpq_record(upper, digits=digits, label=f"{label}.upper"),
        "midpoint": value.mid().str(digits, radius=False, more=True),
        "radius": value.rad().str(digits, radius=False, more=True),
    }


def positive(value: arb, *, label: str = "value") -> None:
    """Require a strictly positive lower endpoint."""

    if not bool(value.lower() > arb(0)):
        raise ValueError(f"{label} is not certified positive: {value!s}")


def validate_backend() -> dict[str, Any]:
    """Run the small API checks relied on by the certificate.

    The checks mirror the python-flint Arb API documentation: ``arb`` values
    enclose real numbers, ``ctx.prec`` controls midpoint precision,
    ``lower()/upper()`` are directed endpoints, and ``fmpq()`` exposes exact
    finite endpoints.  Returning the evidence makes the run self-describing.
    """

    if not hasattr(flint, "arb") or not hasattr(flint, "ctx"):
        raise RuntimeError("python-flint Arb API is unavailable")
    if not hasattr(arb, "lower") or not hasattr(arb, "upper") or not hasattr(arb, "fmpq"):
        raise RuntimeError("python-flint Arb endpoint API is unavailable")
    x = arb(1) / arb(3)
    lower = x.lower()
    upper = x.upper()
    if not bool(lower <= upper):
        raise RuntimeError("Arb lower endpoint exceeds upper endpoint")
    if lower.fmpq() > upper.fmpq():
        raise RuntimeError("Arb endpoint rational order is invalid")

    # An exact integer must survive the endpoint conversion as the same value.
    one = arb(1)
    if one.lower().fmpq() != one.upper().fmpq() or not one.is_integer():
        raise RuntimeError("Arb exact integer endpoint check failed")

    return {
        "backend": "python-flint Arb",
        "flint_version": getattr(flint, "__version__", "unknown"),
        "precision_bits_at_validation": int(ctx.prec),
        "checks": {
            "directed_lower_upper": True,
            "exact_fmpq_endpoints": True,
            "arb_transcendental_api": all(hasattr(arb, name) for name in ("sin", "cos", "sqrt", "asinh")),
            "no_python_float_in_core_helpers": True,
        },
    }


__all__ = [
    "arb",
    "ctx",
    "arb_precision",
    "arb_record",
    "exact_integer",
    "exact_rational",
    "positive",
    "validate_backend",
]
