# Exact positive controls — proof candidates for independent review

Convention: thickness is reach, hence tube radius. Curves are closed smooth
embeddings. For links, length sums all components and thickness uses the union.
These are KNOWN constructions, not novelty claims.

## Circle

C(t)=(cos t,sin t,0), t in R/(2 pi Z). Speed=1, curvature=1.
Its only distinct doubly critical pairs are antipodes, separated by 2. Thus
thickness=1 and length=2 pi. Fenchel gives total curvature >=2 pi for any
closed regular curve, so length >=2 pi when curvature <=1. The unknot optimum
is exactly 2 pi. Scaling by s>0 scales both length and thickness by s.

## Round Hopf link

A(u)=(2 cos u,2 sin u,0), B(v)=(2+2 cos v,0,2 sin v).
Both circles have curvature 1/2 and individual reach 2. Direct expansion gives

    |A(u)-B(v)|^2 = 4 + 8(1-cos u)(1+cos v) >= 4.

Equality occurs whenever u=0 or v=pi. Therefore intercomponent distance=2,
union thickness=1, total length=8 pi. Neither component intersects the other.
This is the standard round Hopf arrangement. The disk bounded by A is pierced
transversely once by B: v=pi gives (0,0,0), while v=0 gives (4,0,0), outside
the disk. This computes absolute linking number 1; linking number alone is
not in general a complete link-type certificate. Here the explicit two-circle
arrangement additionally identifies the standard Hopf isotopy class.

The construction proves the upper bound 8 pi; no general Hopf lower bound is
proved by this note. A sourced optimality result must be cited separately.

## Contact structure

The smooth Hopf strut set contains two continuous one-parameter families:
A(0) against every B(v), and every A(u) against B(pi). Their intersection is
one pair. Any finite contact graph is a discretization, not the full strut set.
The curvature constraint is inactive at tube radius 1. Count contacts only
with the discretization and tolerance explicitly stated.

## Certification design

Geometry and thickness above are analytic. Rational interval enclosures of
length can be obtained from Machin's identity
pi = 16 atan(1/5) - 4 atan(1/239), using alternating rational series with a
rigorous next-term bound. This certifies a number only in conjunction with
the geometric proof; arithmetic precision cannot validate topology by itself.
