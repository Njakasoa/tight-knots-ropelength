# Research log

## 2026-09-12 UTC — initialization

Created requested laboratory as a nested standalone Git repository because the
outer desktop workspace .git is mounted read-only. Saved full user mission.
Read available local and shared continuity. Started three actual Luna agents.
System Python initially has no scientific dependencies. Sandbox DNS failed;
explicitly authorized public Git download succeeded with reviewed network access.
Scientific principle: no sample-based distance estimate is a thickness certificate.

## 2026-09-12 21:10 UTC — analytic candidate

Derived exact toroidal same-shell squared-distance lower bound and integer
population rule in proofs/TOROIDAL_SHELL_SEPARATION.md. This differs from a
cylindrical approximation: all toroidal point pairs are bounded. The obvious
release is to use each shell's h_i=R-r_i, instead of the outer shell's common h.
Proof candidate includes curvature and same-component DCSD estimates, cross-shell
spacing, two-torus triangle bound and full-twist braid topology route.

Exploratory SciPy quadratures (deterministic, default quad tolerances, no seed)
give q0≈2.732166854279056, l0≈72.8402568726584 and formal doubled
coefficient≈11.405009289871446. These are scratch calculations, not accepted
experiment records or certified bounds. Worker must persist a reproducible run
and tester/reviewer must check the proof. No improvement claim is accepted yet.

An initial ratio R/T sweep (4,4.05,4.1,4.2,4.5,5,6,8) gives formal alpha
(11.4050,11.5061,11.6079,11.8138,12.4471,13.5434,15.8342,20.6089).
This suggests the minimal admissible major-radius ratio 4 within this class;
it is not a monotonicity or optimality proof. M2 remains gated by M1 review.

## 2026-09-12 21:18 UTC — independent review in progress

Astra reviewer independently reports the geometric inequalities hold and
reproduces the candidate integral coefficient. This is interim evidence, not a
completed milestone or novelty decision. The derivative constants for a rigorous
midpoint enclosure were also checked independently. A dedicated certificate
implementation remains required.

Primary PDF downloads succeeded via reviewed network access after the initial
sandbox DNS failure: Klotz 2026 v2, Klotz–Thompson 2025, CKS 2002. Their
URLs, byte counts and SHA-256 hashes are stored in papers/DOWNLOAD_MANIFEST.json.

## 2026-09-12 21:50 UTC — executable controls and adversarial regressions

Maintained tsnnls2.5.1 and Ridgerunner2.3.1 now build with actual local Fortran,
OpenBLAS and LAPACKE; 11/11 and 4/4 upstream tests pass. The POSIX-shell test
harness patch is recorded in the build script. Actual autoscaled trefoil runs
reduce the 47-vertex input to33.14901732 and the 400-vertex input to32.74879268.
A pinned CC0 author atlas supplies six small knots and Hopf coordinates.

Independent testing exposed wrong smooth near-diagonal handling, repeated
non-coprime torus component parameterization, missing zero-distance contacts,
and a circumradius formula substituted for Rawdon MinRad. Root additionally
found an incorrect Alexander numerator and unchecked polynomial remainder.
Worker fixes are under independent regression testing; M1 is not yet PASS.
Both exact shell theorem drafts passed adversarial mathematical reviews; the
interval implementation and novelty still require their distinct reviews.

## 2026-09-12 22:10 UTC — independent certificate PASS; M1 audit fixes

A fresh continuation had actual agent capacity; independent Astra reviewed the
executable certificate, reconstructed the integral at224 bits and checked exact
rational endpoints. The all-integer limsup upper coefficient below10.614 passed.
M1 review found genuine bugs surviving earlier green tests: small-scale and
near-endpoint polygon collisions, absolute projection thresholds, antisymmetric
linking matrix, and16pi instead of8pi in exact Hopf reporting. Root fixed them;
independent reviewer probes now pass. Machin output preserves rational endpoints
and outward decimal bounds. Actual-source hashes replace a descriptive literal
hash in the control manifest. New controls and T44 contact records are indexed
in results/INDEX.md; old failed records remain explicitly historical.

The user withdrew prior AGENTS.md instructions during continuation. The original
research mission, authorized local technical work and active goal remain intact.
No new permission or external contact is needed for these local corrections.

## 2026-09-13 — Discovery-to-proof and publication candidate integration

M2 exhaustive block enumeration selected a smaller block multiplier; the exact
uniform expansion F=alpha2[1+a/b+d*b/T+O(b^-2+(b/T)^2+T^-1)] passed Astra
review. Its fixed-c optimum c*=sqrt(a/d) is strictly below1 by an analytic
inequality d>a, independently supplied by the reviewer. Boundary Arb code and
all1024 floors forT1024,b13 passed a second independent implementation; component
count4,976,348 is certified, while the finite length remains diagnostic.

Focused boundary novelty audit found an important antecedent: Klotz–Thompson
2025 Eq17–18 already balance reciprocal and linear terms and derive a square-root
optimizer. Only the geometry-specific expansion/coefficients and discrete-error
control are possible contributions. Claims0000–0003 now separate verified
mathematics from provisional novelty; old certificate-ledger bytes are archived
by SHA and a fresh main certificate binds the updated ledger.

The phase engine completed16 cases with freephase[0,1], independent uniform-grid
checks and finite-pair Arb certificates. All foundhalfphase; larger populations
approach gap sqrt3. A broader smooth generator now varies shell count, population,
radius, periodic pitch, phase, single/double closure and positiveambientscaling.
Its constructive isotopy passed review, up to a common mirror; thickness is not
inherited for arbitrary new parameters.

Three bounded DE starts with independent shell pitch modes were refined by300
actual Ridgerunner steps each. Final numerical values702.797075,716.108417,
746.879334 are retained alongside every start and trial. Two projected linking
checks each giveabs1 for all66pairs; independent polygon thickness agrees with
plCurve within5e-16relative. Finite contact-spectrum clustering distinguishes
allthree at both testedtolerances; no continuum contact phase is inferred.

Atlas expansion exposed a canonical zero-color VECT parser bug, corrected with
two regression tests. Six source-labelled small-knot coordinate rows are now
exported with numerical values, hashes, known lower-source metadata and explicit
missing certification/contact fields. This does not turn coordinates into
certified smooth upper bounds or a best-record table.

After exact results survived, publication/main.tex and a reproduction bundle
were written. The source passed adversarial mathematical review; the default
reproduction and rationalendpoint checker pass. Publication novelty remains
POSSIBLY NOVEL. No external submission/contact is authorized or performed.

## 2026-09-13 — Closing the numerical endpoint topology gap

The M2 reviewer correctly rejected two linking projections as a complete
endpoint topology certificate. A new explicit bridge now certifies every
initial48-point polygon against its variable-pitch analytic full twist using
rigorous sample-rounding, interpolation and normal-fiber bounds. After a
positive homothety/translation, all initial vertices move linearly to their
stored final vertices. Arb separating-axis tests certify all165024 nonadjacent
edge pairs over the entire time interval for each seed; quadratic Bernstein
cross-product tests certify576 adjacent corners. Allthree runs pass with no
time subdivision needed. Witness arrays retain every exact-binary-rational
axis and all dyadic cells for independent replay and coverage checks.

This proves the three final polygons are T(12,12), up to common mirror, by an
explicit alternative isotopy. It does not certify Ridgerunner's actual path,
its numerical thickness values or any global minimum. Exact VECT decimal
coordinates, not rounded parsed floats, enter the proof inequalities. The
math review passes; independent replay/tamper review is recorded separately.

Final independent refinement review PASS: all three analytic reconstructions, full witness replays, complete coverage and eight tamper/input/runtime rejection cases. The hardened checker rejects Python -O and malformed trailing VECT data. The final full publication reproduction passes all seven commands; the PDF compiles cleanly and all seven pages were visually inspected after fixing the abstract clipping. Main M1–M4 deliverables are complete within the explicitly documented scope; follow-up research remains in NEXT.md.

## 2026-09-13 — generalizing staggering

Derived an arbitrary-phase finite separation construction and an exact
all-period mean-gap optimum for the saturated equal-population row test.
Even optimal motifs repeat period two; odd p has mean gap
sqrt(3)+(2-sqrt(3))/p and benefits from a single larger defect gap.
Certified 21 finite periodic examples and five nonuniform-radius constructions
at unchanged M,R,populations,phases. The latter reduce baseline lengths by
approximately 0.76707%, 0.37470%, 0.20308%, 0.12839%, and 0.06950%.
The 26 exact-input certificates replay, code hashes match, and the full suite
passes 96 tests. Proof and scope audit: STAGGERING_GENERALIZATION.md and
STAGGERING_GENERALIZATION_VALIDATION.md. This is a root-derived follow-up,
not an independently refereed result or a new asymptotic coefficient.
