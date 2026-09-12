# Staggered equal-population blocks — UNREVIEWED second candidate

Derived during M1 mathematical exploration. This is a proof sketch, not an
accepted result and not a declaration that M2 has passed. Depends on the
single-component and doubled-core lemmas in TOROIDAL_SHELL_SEPARATION.md.

## Why arbitrary phases do not immediately yield hexagonal packing

For adjacent shells with uniform populations N and M, their phase differences
form a grid of spacing 2pi/lcm(N,M). If N,M are coprime and large, even the
best offset leaves a phase difference O(1/(NM)); radial spacing cannot then
be reduced by a fixed amount using that offset alone. This suggests locking
nearby populations into equal-population blocks and staggering their phases.

## Exact cross-shell bound

For two shell radii a,b and h_a=R-a,h_b=R-b, the toroidal distance identity
implies, with d=t-s and phase difference Delta,

 distance² >= (a-b)² +4ab sin²(d/2)+4h_a h_b sin²((d+Delta)/2)
           >= (a-b)² +4K sin²(Delta/2),
 K=ab h_a h_b/(ab+h_a h_b).

The second inequality follows from minimizing the two cosines and
1-sqrt(1-z)>=z/2 for z in [0,1]. It holds for every d.
For 0<a<=b<=R/2,

 1/K=1/(ab)+1/((R-a)(R-b))

is nonincreasing in b, because its derivative is
-1/(ab²)+1/((R-a)(R-b)²)<=0. Consequently
K>=a²(R-a)²/(a²+(R-a)²). The latter also increases in a on (0,R/2].

## Block rule

Take a block of adjacent shells all with N strands, alternating offsets
0 and pi/N. The least absolute phase difference across neighbors is pi/N.
Let a0 be the innermost block radius, h0=R-a0, and
A0=pi a0 h0/sqrt(a0²+h0²). Choose N=floor(A0)-1>=3.
For any two neighboring shells in the block, K>=A0²/pi², hence

 4K sin²(pi/(2N)) >= 4(A0/pi)² [pi/(2N+1)]² > 1,

using sin(pi/m)>=pi/(m+1), m=2N, and A0>=N+1.
Therefore a radial gap sqrt(3) suffices for clearance strictly above 2.
Same-shell clearance follows from the earlier integer population lemma.
Non-neighboring shells are radially separated by at least 2sqrt(3)>2.
Between blocks use radial gap 2, so no phase/population compatibility is needed.
The first shell starts at radius 2 and the core circle is included.
Choose R=2r_outer+2; all single-component and doubled-core bounds apply.

## Asymptotic block scaling

For T shells, choose block size floor(sqrt(T)), with the last block possibly
shorter. The O(sqrt(T)) block boundaries cost only O(sqrt(T)) in outer radius
relative to a uniform sqrt(3)-spaced array. Locking each block population to
its inner-shell capacity changes each shell population by O(sqrt(T)), for
total O(T^(3/2)) versus total population of order T². These losses vanish in
the leading coefficient. Need explicit uniform estimates in a full proof.

Relative to the earlier r_i=2i construction, the leading radial scale is
s=sqrt(3)/2. The population coefficient is s*q0, and length coefficient is
s²*l0. After doubling, the candidate coefficient becomes

 alpha_staggered=sqrt(s)*l0/(sqrt(2)*q0^(3/2))
               =sqrt(sqrt(3)/2)*alpha_shell_specific
               ≈10.613557063258954 (unverified numerical quadrature).

This is NOT a universal lower coefficient, NOT a global optimum, and NOT an
exact asymptotic for the true link infimum. Potential conclusion is only a
constructive limsup upper for T(Q,Q), if all proof obligations survive.

## Outstanding

Independent proof review; explicit finite-T generator and interval checks;
all-Q deletion argument when block size changes (monotonicity not automatic,
but a sequence with relative successive sizes→1 suffices); topology retained
under staggered phases via full-twist point-configuration argument; exact
coefficient enclosure; detailed novelty search (hexagonal packing is known).
