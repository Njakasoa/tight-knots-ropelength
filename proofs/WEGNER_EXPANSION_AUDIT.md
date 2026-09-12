# Audit of the published lower-bound expansion

This is an algebraic audit of an existing bound, not a new stronger lower bound.
Source: Klotz 2026, arXiv:2603.02416v2 Eq. (6)–(8),
https://arxiv.org/html/2603.02416v2 . Radius convention, p=1, Q components.

Write a=2sqrt(3), b=(2-sqrt(3))*sqrt(12)=4sqrt(3)-6. The expression
inside the square root in the disk-area bound is

    a(Q-2)+(2-sqrt(3))*ceil(sqrt(12Q-15)-3)+pi
    = aQ+b sqrt(Q)+O(1).

The ceiling contributes a bounded term, so it does not affect the first two
coefficients. Set alpha=sqrt(4pi a)=sqrt(8pi sqrt(3)). Expanding the bound gives

    Q[2pi+sqrt(4pi(aQ+b sqrt(Q)+O(1)))]
      = alpha Q^(3/2)+(2pi+2pi b/alpha)Q+O(sqrt(Q)).

Since [Q(Q-1)]^(3/4)=Q^(3/2)(1+O(1/Q)), its normalized expansion is

    alpha + B/sqrt(Q)+O(1/Q),
    B=2pi+2pi b/alpha=2pi+sqrt(2pi(7sqrt(3)-12)).

Numerically B≈7.1671, not 7.61. This correction follows from the exact
formula; it does not improve that formula or certify the sign of the
O(1/Q) remainder. In particular, a series with an unspecified remainder
must not be used as a pointwise finite-Q lower bound. Software should
use the original ceiling expression with validated arithmetic.

Status: independently derived algebra, awaiting reviewer confirmation.
The main candidate upper bound does not depend on this correction.
