# Reviewed results

The main laboratory objective has produced three independently reviewed
mathematical results and a local publication candidate. The broader research
programme remains a source of follow-up questions; global optimality and
publication priority have not been established.

## Constructive torus-link upper bound

In the convention thickness=rope radius, with total component length,

    limsup_{M→∞} Rop(T(M,M)) / [M(M−1)]^(3/4) ≤ alpha2 <10.614.

Here alpha2=√(√3/2) l0/(√2 q0^(3/2)), with explicit elementary/integral
constants in proofs/THEOREM_001.md and THEOREM_002.md. The accepted outward
endpoint is10.613733558728498…; the smaller approximate value10.6135570633…
is diagnostic. An unstaggered construction gives the intermediate coefficient
alpha1<11.406. These are asymptotic upper bounds; no matching lower bound or
minimum is asserted. Arbitrary integersM are covered by deleting components
from a slightly larger full-twist construction.

Proof obligations covered: exact same/cross-shell distance inequalities,
curvature and all self-critical chords, proper Hopf-core doubling, full-twist
framing/signs, all-integer limiting passage, interval integral error and exact
rational endpoints. Independent proof and arithmetic reviews all pass.

## First correction inside the block grammar

For the exact constructed length F(T,b), as b→∞ andb/T→0,

    F(T,b)=alpha2[1+a/b+d*b/T+O(b^-2+(b/T)^2+T^-1)].

Among fixedc>0 withb=floor(c√T), the first correction is uniquely minimized at
c*=√(a/d)≈.4227848052. The exact inequalityd>a proves c*<1 and strict
improvement overc=1 without decimals. This is not an equal-M comparison, an
exact finite-T argmin or an optimum over arbitrary schedules.

Exhaustive finite block searches supplied the observed smaller prefactor;
the analytic expansion explains it. All1024 population floors forT1024,b13
are independently certified, giving4,976,348 components. Finite searched
lengths are kept separate from the asymptotic certificate.

## Laboratory and discovery validation

M1 and the bounded M2 shell-discovery engine passed independent review.
The final geometry suite has65 passing tests, including17 focused independent
M2 tests. Actual Ridgerunner/plCurve controls and upstream builds were run;
this is not a mock optimization environment. The T44 supplied coordinates
agree with plCurve at77.97687288, while their companion table says77.47;
that discrepancy remains explicit and is not used by the new proofs.

The generator varies shell count, populations, radii, periodic shell pitch,
phase, single/double closure and positive ambient scaling. Its exact smooth
isotopy proof is distinct from its numerical thickness objectives. Three
multistart final polygons also have dedicated exact-input topology certificates:
rigorous analytic sampling bounds followed by explicit alternative PL isotopies
cover all165024 nonadjacent edge pairs and576 corners per configuration.
These certify the endpoint link type, not the actual solver history or a
ropelength optimum. Full witnesses can be replayed.

## Publication and novelty

The local manuscript is publication/main.tex, with the compiled PDF at
publication/build/main.pdf. CONTRIBUTION_REVIEW.md and VALIDATION.md record
its scope; BUILD_STATUS.md records the typesetting/visual check. Reproduce from
the lab root using `.venv/bin/python publication/reproduce.py --full`.

Mathematical verification and novelty have different statuses: these are
VERIFIED RESULTS within the stated assumptions, while the proposed publication
contribution remains POSSIBLY NOVEL after bounded primary-source audits.
Toroidal helices, hexagonal packing, doubling, equal-population shells and
reciprocal-linear square-root balancing are prior art. The possible contribution
is the precise shell-specific/staggered construction and its exact boundary
correction. No external submission/contact has occurred.

For physical radiusr, a certified construction of unit-thickness lengthL
scales to total contour lengthrL forM separate closed filaments. It gives
sufficient length for existence, not a free-energy minimum for a single chain.
