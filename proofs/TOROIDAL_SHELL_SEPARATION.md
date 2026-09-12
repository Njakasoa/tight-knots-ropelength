# Toroidal shell separation — analytic proof candidate, UNREVIEWED

This note targets a sufficient constraint, not a global optimum or a new best
ropelength bound. It was derived independently while auditing Klotz 2026 §III.3:
https://arxiv.org/html/2603.02416v1 . Novelty remains unaudited.

Let R>r>0, h=R-r, N>=2 integer, and define
F_j(t)=((R+r cos t) cos(t+2pi j/N),
        (R+r cos t) sin(t+2pi j/N), r sin t).
These are the p=1 toroidal helices of the cited paper.

For two components, write d=t-s and Delta=2pi(j-k)/N. Exactly,

|F_j(t)-F_k(s)|² = 4r² sin²(d/2)
                 +4(R+r cos t)(R+r cos s) sin²((d+Delta)/2).

Thus it is >= 4r² sin²(d/2)+4h² sin²((d+Delta)/2).
Minimizing this last expression over all d by combining two cosines gives

D²(Delta) = 2(r²+h² - sqrt((r²+h²)²-4r²h² sin²(Delta/2))).

All distinct components are therefore separated by at least D(2pi/N), since
sin²(pi(j-k)/N)>=sin²(pi/N). No point sampling or root search occurs here.
Provided r²+h²>=2, the sufficient condition D²>=4 is equivalent to

    r² h² sin²(pi/N) >= r²+h²-1.                 (S)

This does not assert that D is the actual separation: replacing the two radial
factors by h² loses information. Equality in that replacement and in the
one-variable minimization need not be simultaneous.

For distinct shells of radii r_i,r_j with a common R, the first squared term
is |r_i exp(it)-r_j exp(is)|² >= (r_i-r_j)². Hence radial spacing >=2
suffices for inter-shell clearance, independently of phase and population.
A core circle has clearance r_i from shell i. These facts cover intercomponent
clearance only; self-thickness and complete isotopy must be separately proved.

## A simple integer population rule

For integer N>=3, sin(pi/N)>=pi/(N+1). Proof: on [0,pi/3],
sin x >= x-x³/6; it is enough that pi²(N+1)<=6N². At N=3 this follows
from pi²<10, and the polynomial 6N²-10N-10 increases for N>=3.
Let A=pi r h/sqrt(r²+h²). If N+1<=A and N>=3, then

r²h² sin²(pi/N) >= r²h² pi²/(N+1)² >= r²+h² > r²+h²-1.

So N=floor(A)-1 is sufficient whenever it is >=3. This costs at most two
strands relative to A and avoids a cubic stationary-root approximation.
With r_i=2i, R=4T+2, h_i=R-r_i, one may either use h_i individually
or the common conservative h=R-2T=2T+2. Population rounding costs O(T)
strands among O(T²) strands; that fact alone does not certify the full
ropelength asymptotic or the doubled-torus construction.

## Remaining proof obligations

* Same-component DCSD and curvature >= unit tube clearance.
* Constructive isotopy for arbitrary shell populations and phases.
* For any doubled construction, all inter-torus pairs and orientation/framing.
* Length integral with certified error; limsup across missing Q values.
* Independent adversarial implementation and review.
* Literature novelty search for this sufficient inequality.

## Closing the self-thickness obligation for R>=2r+2, r>=2

For one component v=|F'|>=h=R-r and |F''|<=M=R+sqrt(5)r.
The latter follows by expressing F'' in its rotating cylindrical frame:
components are -(R+2r cos t), -2r sin t, -r sin t, and the triangle inequality.
Thus curvature <=M/h². Since r<=h-2 and sqrt(5)<9/4,
M <=17h/4-6, h>=4, whence M/h²<=11/16<1.

For two parameters with shorter cyclic separation d in (0,pi], Taylor's
integral remainder at s gives

(F(s+d)-F(s)) dot F'(s) >= d |F'(s)| (|F'(s)|-Md/2).

A doubly critical pair must therefore have d>=2h/M. The exact distance
identity with Delta=0 gives distance>=2h sin(d/2)>=2h sin(h/M).
Because 0<h/M<=1, sin(h/M)>=(5/6)(h/M), so every such chord has length
at least (5/3)h²/M >=80/33>2. Hence each component has thickness >=1.
The core circle has radius R>=6 and also meets the curvature/self-distance
conditions. Together with intercomponent bounds, this establishes unit
thickness of a single shell bundle once (S) is satisfied on every shell.

## Shell-specific constraint release — candidate asymptotic improvement

Choose r_i=2i, R=4T+2, **h_i=R-r_i** for shell i, i=1,...,T.
Use N_i=floor(pi r_i h_i/sqrt(r_i²+h_i²))-1 (>=3), and one core circle.
This releases the common h=R-r_outer assumption: inner shells may hold more
strands because their own minimum distance from the axis is larger.

With x=i/T, the shell population density tends to
n(x)=2pi x(2-x)/sqrt(x²+(2-x)²). Thus

q0 = integral_0^1 n(x) dx,
l0 = integral_0^1 n(x) integral_0^(2pi)
          sqrt((4+2x cos t)²+4x²) dt dx.

Q(T)=q0 T²+O(T), length(T)=l0 T³+O(T²). Numerical quadrature (not a
certificate) gives q0=2.732166854279056, l0=72.8402568726584,
and alpha_single=l0/q0^(3/2)=16.129118816727342.

For two copies arranged about the two round Hopf core circles of radius R
and center separation R, each component is within 2T of its core. The core
circles have mutual distance R, so all cross-bundle centerline distances are
at least R-4T=2 by the triangle inequality. Proper rotations preserve
within-bundle clearance. This certifies geometric separation of the doubled
construction. The matching framing/chirality needed for T(2Q,2Q) still needs
an independent constructive topology argument; pairwise linking is insufficient.

If that topology is proved, the candidate leading coefficient is
l0/(sqrt(2)*q0^(3/2))=11.405009289871446. DO NOT call this a certified
ropelength upper bound until topology, limiting passage, length integral
certificate and independent review are completed. No novelty assertion yet.

## Integral certificate plan (root derivation)

The first integral is exactly
q0 = pi*(3 asinh(1)/sqrt(2)-1).
Let f(x,t)=n(x)*sqrt(g(x,t)),
g=16+16x cos t+4x² cos² t+4x², x in [0,1]. Then 8<=g<=40.
Conservative derivative bounds are |n|<=5, |n'|<=14, |n''|<=40,
|g_x|<=32, |g_xx|<=16, |g_t|<=24, |g_tt|<=24. Thus
|f_xx|<=600 and |f_tt|<=60. These constants require independent checking.
A tensor composite midpoint rule with N x-cells and M angular cells has error

 E <= (2pi)/24 * (600/N² + 60*(2pi/M)²).

Use rigorous ball evaluations of each midpoint and sum, then add [-E,E].
With N=256,M=512 the discretization enclosure is already useful; every
floating evaluation must itself be enclosed. The final coefficient is
l0/(sqrt(2)*q0^(3/2)). A looser alternative via Jensen is
l0<=2pi integral_0^1 n(x)*sqrt(16+6x²) dx, formally giving alpha<=11.651,
which can be certified in one dimension at lower cost.

## Constructive topology route for independent reviewer

Reparameterize each component by longitude u=t+phi_j. Its cross-section point
is z_j(u)=r_j exp(i(u-phi_j)); the core corresponds to z=0. The radial/vertical
normal frame of the unknotted circular core has zero framing (a constant
radial displacement has linking number zero with the core). Thus the bundle
is the closure of the rigid full-rotation loop of Q distinct disk points,
namely the full twist braid Delta_Q², up to common mirror convention.
Its closure is T(Q,Q). Moving initial points by a planar isotopy conjugates
this central braid and does not change its closure.

For the doubled construction, the two zero-framed cores form a Hopf link.
Cable each core with Q points and give each bundle one full internal twist.
The braid identity decomposes the full twist on 2Q strands into the full
twist on each Q-strand block followed by the full mutual block twist:

Delta_(2Q)² = (Delta_Q² tensor Delta_Q²) * (full twist of the two blocks).

The cabled Hopf core provides the latter factor. Consequently the resulting
closure is T(2Q,2Q), **provided the signs of internal and mutual twists agree**.
This last sign must be checked for the explicit proper-rotation placement;
if necessary reverse the helical winding choice in both bundles. Mirroring
the entire configuration preserves ropelength, but changing only one
bundle's handedness can change the link type (as Klotz explicitly warns).
The braid identity, normal framing and sign check require independent review.

## Missing Q values

Let M_T=2Q(T) be total doubled population. The explicit smooth capacity
function gives M_T=q* T²+O(T), so gaps M_(T+1)-M_T=O(T) if monotonicity is
established (each shell capacity increases with R). For intermediate M,
remove M_T-M components from the next larger full-twist link. Deleting
strands from the full twist gives T(M,M); separation cannot decrease and
length cannot increase. With M_T/M=1+O(1/T), the same leading coefficient
bounds limsup across all M, not just the subsequence M_T. Must use the
next *larger* link and retain at least the desired number of components.

## Explicit twist-sign check

For the first oriented core C(t)=(R cos t,R sin t,0), its spanning disk has
normal +z. A helical component (positive meridional sin t as above) meets
z=0 at t=0 and pi. The first crossing is at radius R+r outside the disk;
the second is at radius R-r inside, with z-velocity -r. Its linking with
C is therefore -1 in the usual oriented-disk convention.

Place the second bundle by the proper rigid motion
P(x,y,z)=(R+x,-z,y). Its oriented core is (R+R cos t,0,R sin t).
It crosses the first core's disk at t=pi at the origin with z-velocity -R,
while t=0 lies at (2R,0,0) outside. The core Hopf linking number is also -1.
Proper motion preserves each bundle's internal handedness. Thus internal
and mutual twist signs agree for this explicit placement. A global mirror
converts the common sign if the notation T(Q,Q) uses the opposite convention.
This analytic sign check supplements, rather than replaces, the full-twist
cabling argument; pairwise linking alone would not determine link type.
