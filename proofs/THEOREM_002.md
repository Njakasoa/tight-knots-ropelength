# Theorem 002 — staggered shell blocks

Status: exact mathematical construction independently reviewed PASS in
ADVERSARIAL_REVIEW_002.md. Numerical enclosure and implementation are separate
obligations. Novelty remains provisional. M1 infrastructure gate remains separate.

With q0,l0,alpha1 as in THEOREM_001.md, let s=sqrt(3)/2 and
alpha2=sqrt(s)*alpha1. Then, in the tube-radius convention,

    limsup_(M→infinity) Rop(T(M,M)) / [M(M-1)]^(3/4) <= alpha2.

Diagnostic quadrature gives alpha2≈10.6135570633. No truncated decimal
is asserted as an upper endpoint without the interval certificate.

## Finite construction

Given T>=1, set b=floor(sqrt(T)), delta=sqrt(3),

    r_i=delta*i+(2-delta)*(1+floor((i-1)/b)),  i=1,...,T,
    R=2*r_T+2.

Each consecutive block of b shells (last block possibly shorter) has
constant population N=floor(A(r_first))-1, where
A(r)=pi*r*(R-r)/sqrt(r²+(R-r)²). Alternate shell phase offsets 0 and
pi/N within a block. The first radius is 2, gaps inside blocks are sqrt(3),
and gaps between blocks are 2. Include the core circle and double by the
same proper Hopf-core motion P(x,y,z)=(R+x,-z,y) as in Theorem 001.

## Separation lemma

For shell radii a<=b<R/2, set
K=ab(R-a)(R-b)/(ab+(R-a)(R-b)). The exact toroidal distance identity and
harmonic minimization give, for every pair of parameters,

    distance² >= (a-b)²+4K sin²(Delta/2).

The reciprocal 1/K=1/(ab)+1/((R-a)(R-b)) decreases with b in this range;
K(a,a) also increases with a. Thus K is at least its diagonal value at
the block's innermost radius. Across neighboring equal-population shells,
every phase difference is an odd multiple of pi/N. Consequently

    4K sin²(Delta/2) >= 4(N+1)²/(2N+1)² >1.

The radial squared gap is 3, giving clearance above 2. Same-shell pairs
satisfy the previous population lemma; non-neighboring shells have radial
gap at least 2sqrt(3), and block boundaries have gap 2. The core clearance
is 2. Since R>=2r_i+2, self-thickness and cross-bundle clearance follow
from Theorem 001. Its full-twist proof applies to arbitrary fixed distinct
cross-section points, so staggered phases and blocks preserve the link type.

## Limiting passage

Uniformly r_i=sqrt(3)*i+O(sqrt(T)) and R=2sqrt(3)*T+O(sqrt(T)).
Each population is evaluated at a radius only O(sqrt(T)) below its shell
radius. Bounded derivatives of the capacity and length functions therefore
give, with x=i/T,

    N_i=s*T*n(x)+O(sqrt(T)),
    ell_i=s*T*e(x)+O(sqrt(T)).

Summing yields Q(T)=s*q0*T²+O(T^(3/2)) and
L_bundle(T)=s²*l0*T³+O(T^(5/2)). After doubling, the leading coefficient
is sqrt(s)*alpha1. For arbitrary desired M, choose the least index T with
M_T>=M and delete excess components. Although M_T need not be monotone,
minimality gives M_(T-1)<M; the asymptotic estimates imply
M_T-M=O(T^(3/2)) and M_T/M→1. Deletion preserves the full-twist type and
unit thickness. This proves the all-integer limsup bound.

Full independent details and finite stress tests are in
ADVERSARIAL_REVIEW_002.md. Source discovery note: STAGGERED_BLOCKS_CANDIDATE.md.
This is a constructive upper bound, not an asymptotic equality for the true
minimum, and it does not improve a universal lower coefficient.
