"""Arb midpoint certificate for the shell-specific asymptotic constant.

The proof note supplies the analytic identity

``q0 = pi * (3*asinh(1)/sqrt(2) - 1)``

and the derivative bounds ``|f_xx| <= 600`` and ``|f_tt| <= 60`` for

``f(x,t) = n(x) * sqrt((4+2*x*cos(t))**2 + 4*x**2)``.

This file implements exactly the tensor composite midpoint rule from that
note.  It evaluates the exact rational midpoint locations and all subsequent
operations as Arb balls.  The returned ``l0`` ball is the mesh ball enlarged
by a symmetric Arb ball whose radius is the directed upper endpoint of the
analytic error expression.  No Python float enters the certificate path.
"""

from __future__ import annotations

from typing import Any

from .arb_backend import arb, arb_precision, arb_record, exact_rational, positive


DEFAULT_N = 256
DEFAULT_M = 512
DEFAULT_PRECISION_BITS = 192
DEFAULT_OUTPUT_DIGITS = 60


def density(x: arb, pi: arb | None = None) -> arb:
    """Evaluate the shell population density ``n(x)`` with Arb arithmetic."""

    pi = arb.pi() if pi is None else pi
    two = arb(2)
    return two * pi * x * (two - x) / (x * x + (two - x) * (two - x)).sqrt()


def length_integrand(x: arb, t: arb, pi: arb | None = None) -> arb:
    """Evaluate the two-variable length integrand ``f(x,t)``."""

    n = density(x, pi)
    two = arb(2)
    four = arb(4)
    c = t.cos()
    g = (four + two * x * c) * (four + two * x * c) + four * x * x
    return n * g.sqrt()


def exact_q0(pi: arb | None = None) -> arb:
    """Evaluate the exact closed form for ``q0`` as an Arb enclosure."""

    pi = arb.pi() if pi is None else pi
    return pi * (arb(3) * arb(1).asinh() / arb(2).sqrt() - arb(1))


def midpoint_sum_l0(n_cells: int, m_cells: int, *, pi: arb | None = None) -> arb:
    """Return the Arb tensor midpoint approximation before the analytic error."""

    if not isinstance(n_cells, int) or n_cells <= 0:
        raise ValueError("n_cells must be a positive integer")
    if not isinstance(m_cells, int) or m_cells <= 0:
        raise ValueError("m_cells must be a positive integer")
    pi = arb.pi() if pi is None else pi

    # Each node is built from integer Arb values.  In particular, ``/`` below
    # is Arb division and does not call Python float division.
    angular_nodes = [pi * exact_rational(2 * j + 1, m_cells) for j in range(m_cells)]
    total = arb(0)
    for i in range(n_cells):
        x = exact_rational(2 * i + 1, 2 * n_cells)
        n_x = density(x, pi)
        for t in angular_nodes:
            c = t.cos()
            two_x_c = arb(2) * x * c
            g = (arb(4) + two_x_c) * (arb(4) + two_x_c) + arb(4) * x * x
            total += n_x * g.sqrt()

    hx = exact_rational(1, n_cells)
    ht = arb(2) * pi / arb(m_cells)
    return total * hx * ht


def midpoint_error(n_cells: int, m_cells: int, *, pi: arb | None = None) -> arb:
    """Return the analytic tensor midpoint error expression ``E``."""

    if n_cells <= 0 or m_cells <= 0:
        raise ValueError("midpoint cell counts must be positive")
    pi = arb.pi() if pi is None else pi
    nx_term = arb(600) / (arb(n_cells) * arb(n_cells))
    mt = arb(2) * pi / arb(m_cells)
    t_term = arb(60) * mt * mt
    return (arb(2) * pi) / arb(24) * (nx_term + t_term)


def symmetric_error_ball(error_bound: arb) -> arb:
    """Create a symmetric Arb ball enclosing ``[-error_bound,error_bound]``."""

    positive(error_bound, label="midpoint error bound")
    # The radius argument is an Arb interval; the constructor rounds it
    # outward.  Passing the directed upper endpoint makes the enclosure
    # explicit even if the expression itself has a tiny rounding radius.
    return arb(0, error_bound.upper())


def certify_integrals(
    n_cells: int = DEFAULT_N,
    m_cells: int = DEFAULT_M,
    *,
    precision_bits: int = DEFAULT_PRECISION_BITS,
    output_digits: int = DEFAULT_OUTPUT_DIGITS,
) -> dict[str, Any]:
    """Compute and serialize the rigorous ``q0``, ``l0`` and alpha enclosure."""

    with arb_precision(precision_bits):
        pi = arb.pi()
        q0 = exact_q0(pi)
        positive(q0, label="q0")
        mesh = midpoint_sum_l0(n_cells, m_cells, pi=pi)
        error = midpoint_error(n_cells, m_cells, pi=pi)
        error_ball = symmetric_error_ball(error)
        l0 = mesh + error_ball

        denominator = arb(2).sqrt() * q0 * q0.sqrt()
        positive(denominator, label="sqrt(2)*q0^(3/2)")
        alpha = l0 / denominator
        staggered_scale = (arb(3).sqrt() / arb(2)).sqrt()
        staggered_alpha = alpha * staggered_scale

        return {
            "method": {
                "quadrature": "tensor composite midpoint rule",
                "x_interval": ["0", "1"],
                "t_interval": ["0", "2*pi"],
                "n_cells": n_cells,
                "m_cells": m_cells,
                "derivative_bounds": {"abs_f_xx": "600", "abs_f_tt": "60"},
                "error_formula": "(2*pi)/24 * (600/N^2 + 60*(2*pi/M)^2)",
                "midpoint_nodes": "exact rational x nodes and Arb pi-rational t nodes",
                "arithmetic": "python-flint Arb balls for every node and operation",
                "precision_bits": precision_bits,
            },
            "q0_exact_expression": "pi*(3*asinh(1)/sqrt(2)-1)",
            "q0": arb_record(q0, digits=output_digits, label="q0"),
            "midpoint_sum": arb_record(mesh, digits=output_digits, label="midpoint_sum_l0"),
            "discretization_error": arb_record(error, digits=output_digits, label="E"),
            "l0": arb_record(l0, digits=output_digits, label="l0"),
            "l0_lower_positive": bool(l0.lower() > arb(0)),
            "denominator": arb_record(denominator, digits=output_digits, label="denominator"),
            "alpha_exact_expression": "l0/(sqrt(2)*q0^(3/2))",
            "alpha": arb_record(alpha, digits=output_digits, label="alpha"),
            "alpha_upper_decimal": alpha.upper().str(output_digits, radius=False, more=True),
            "alpha_upper_lt_11_407": bool(alpha.upper() < arb("11.407")),
            "optional_staggered_rescaling": {
                "status": "reviewed candidate rescaling; no new geometry claim is made by this arithmetic field",
                "factor_exact_expression": "sqrt(sqrt(3)/2)",
                "factor": arb_record(staggered_scale, digits=output_digits, label="staggered_scale"),
                "alpha2_exact_expression": "sqrt(sqrt(3)/2)*l0/(sqrt(2)*q0^(3/2))",
                "alpha2": arb_record(staggered_alpha, digits=output_digits, label="alpha2"),
                "alpha2_upper_decimal": staggered_alpha.upper().str(output_digits, radius=False, more=True),
                "alpha2_upper_lt_10_615": bool(staggered_alpha.upper() < arb("10.615")),
                "alpha2_upper_lt_10_614": bool(staggered_alpha.upper() < arb("10.614")),
            },
        }


__all__ = [
    "DEFAULT_M",
    "DEFAULT_N",
    "DEFAULT_PRECISION_BITS",
    "certify_integrals",
    "density",
    "exact_q0",
    "length_integrand",
    "midpoint_error",
    "midpoint_sum_l0",
]
