# Theorem 001 — a constructive torus-link limsup bound

Status: analytic proof independently reviewed (ADVERSARIAL_REVIEW_001.md).
An implementation/interval endpoint and publication novelty are separate checks.
This is not a claim of a global minimum or asymptotic equality for the infimum.

Let ropelength use tube radius and total link length. Define

    n(x)=2pi*x*(2-x)/sqrt(x²+(2-x)²),
    e(x)=integral_0^(2pi) sqrt((4+2x cos t)²+4x²) dt,
    q0=integral_0^1 n(x) dx = pi*(3 asinh(1)/sqrt(2)-1),
    l0=integral_0^1 n(x)e(x) dx,
    alpha1=l0/(sqrt(2)*q0^(3/2)).

Then

    limsup_(M→infinity) Rop(T(M,M)) / [M(M-1)]^(3/4) <= alpha1.

Diagnostic quadrature gives alpha1≈11.4050092899. This decimal is not an
upper endpoint until the separate arithmetic certificate provides one.

## Explicit construction

For integer T>=1 take R=4T+2, r_i=2i, h_i=R-r_i, and

    N_i=floor(pi*r_i*h_i/sqrt(r_i²+h_i²))-1,    i=1,...,T.

Every N_i>=4. Include a core circle C(t)=(R cos t,R sin t,0). Shell i has
components j=0,...,N_i-1 with phase phi_j=2pi j/N_i:

    F_ij(t)=((R+r_i cos t)cos(t+phi_j),
             (R+r_i cos t)sin(t+phi_j), r_i sin t).

Duplicate the entire bundle with proper rigid motion
P(x,y,z)=(R+x,-z,y). Let Q(T)=1+sum_i N_i and M_T=2Q(T).

## Thickness

For same-shell component phases separated by Delta, all pairs satisfy

    |F_j(t)-F_k(s)|² >= 4r² sin²((t-s)/2)
                         +4h² sin²((t-s+Delta)/2).

Minimizing the right side over t-s gives

    2[S-sqrt(S²-4r²h² sin²(Delta/2))],   S=r²+h².

Its minimum over distinct component pairs is at |Delta|=2pi/N. For S>=2
this bound is at least 4 whenever r²h² sin²(pi/N)>=S-1.
The elementary inequality sin(pi/N)>=pi/(N+1), N>=3, and the chosen
N+1<=pi*r*h/sqrt(S) give the stronger right side S.

For unequal shells the squared transverse term alone is at least
(r_i-r_j)²; shell spacing two therefore gives clearance two. The core
has distance exactly r_i from shell i. The two Hopf core circles have
minimum separation R. All component points are within 2T of their core,
so cross-bundle distances are at least R-4T=2.

For self-thickness, |F'|>=h and |F''|<=B=R+sqrt(5)r. Since R>=2r+2,
r>=2, we have h>=4 and B/h²<=11/16. Curvature is at most 11/16.
If a doubly critical chord has shorter cyclic parameter separation d,
Taylor's integral remainder implies d>=2h/B. Its distance is at least
2h sin(d/2)>=2h sin(h/B)>=(5/3)h²/B>=80/33>2.
The core's reach is R. The smooth thickness formula now gives reach at
least one for the full union. The curves are embedded because longitude
is one-to-one modulo 2pi and the cylindrical radius is positive.

## Topology

In the zero-framed tubular coordinates of the core, reparameterization
u=t+phi_j gives cross-section points exp(iu)w_j, with fixed distinct
w_j=r_i exp(-i phi_j), together with w=0 for the core. Rigid rotation of
a disk-point configuration is a full twist. Moving the distinct initial
points by a disk isotopy identifies the bundle with T(Q,Q), up to mirror.

A full rotation of two disjoint clusters factors into full rotation within
each cluster and the mutual full rotation of their centers with fixed disk
frames. The latter is the zero-framed cabling of a Hopf link. Thus the two
bundles form the full twist on 2Q strands. The explicit placement has
matching internal and mutual signs: both pierce the first core's spanning
disk downward once. This proves T(2Q,2Q), up to a common mirror, which does
not change ropelength. The full configuration-space factorization and
framing verification are detailed in ADVERSARIAL_REVIEW_001.md §3;
pairwise linking is not used as a complete invariant.

## Limiting passage

Uniformly for i=1,...,T,

    N_i=T*n(i/T)+O(1),
    ell(R,r_i)=T*e(i/T)+O(1).

For the first estimate, |partial_h(pi*r*h/sqrt(r²+h²))|<=pi controls
the finite +2 offset and flooring costs less than two. The second follows
from |partial_R ell|<=2pi. Since n,e are smooth on [0,1], Riemann sums give

    Q(T)=q0*T²+O(T),     L_bundle(T)=l0*T³+O(T²).

Doubling gives the coefficient alpha1. The population M_T is increasing:
all existing capacities increase with T and a positive shell is added.
The same derivative bound gives M_(T+1)-M_T=O(T). For intermediate M,
delete components from the next larger full construction. The full twist
restricts to a full twist on the surviving strands, so the type is T(M,M).
Thickness cannot decrease and length cannot increase. Since M_next/M→1,
the same limsup holds over all integers. Finally [M(M-1)]^(3/4)~M^(3/2).

## Provenance and scope

Root derivation: TOROIDAL_SHELL_SEPARATION.md. Independent review:
ADVERSARIAL_REVIEW_001.md. Closest audited construction:
[Klotz 2026](https://doi.org/10.1088/1751-8121/ae862e), with common hole
radius h; this construction uses each shell's h_i. The geometric ideas of
concentric toroidal shells and Hopf doubling are prior work and receive no
novelty claim here. CLAIM-0001 tracks the remaining checks.
