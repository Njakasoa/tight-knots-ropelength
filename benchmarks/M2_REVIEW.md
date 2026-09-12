# Independent M2 milestone review

Date: 13 September 2026. Reviewer: delegated Astra adversarial reviewer.
Reviewed the mission's §§23, 31, 35–38; `M2_DISCOVERY.md`; actual generator,
search and clustering implementations; preserved results; the passed geometry,
first-correction and variable-pitch topology reviews; and
`UNIVERSAL_COEFFICIENT_MAP.md`.

## Verdict and gate

**PASS for M2's bounded automated shell-discovery grammar.** Independent
current-source validation passed 65 repository-wide and 17 focused tests,
including the post-M1 zero-color VECT fix; its hashes were independently
checked. This verdict does not claim completion of every secondary
research axis in the mission, arbitrary topology/closure optimization, certified
free-vertex solver trajectories, a global optimum, or established publication
novelty. A separately reviewed and replayed certificate now establishes the
full-twist type of all three stored initial/final polygons by an explicit
alternative isotopy. The actual ridgerunner trajectories remain uncertified.

M2 is justified by a working parameterized search and an observation not
prescribed to that search, followed by an independently reviewed explanation.
A test count alone would not justify this gate.

## Parameter coverage against §38

| Required parameter | Implemented and reviewed coverage | Boundary |
|---|---|---|
| Family | Standard T(p,q) generator plus single and doubled full-twist shell grammars | Several explicit families; no arbitrary-link grammar |
| Q | Positive integer populations and optional core determine an explicit count; single/double closure is recorded | Changing populations changes link type and requires a fresh geometric objective |
| Shell count | Any finite nonempty list of distinct positive radii | No automated search over all possible numbers at once is claimed |
| Shell populations | Independent integer entries; equal-population blocks form the rigorously separated subset | Arbitrary entries do not inherit the block reach certificate |
| Pitch | Independent finite beta_i sin(u) normal-angle modulation | Meridional winding remains one; no arbitrary helical winding or endpoint surgery |
| Radii | Independent radii and major radius with validated embedding constraints | R>rmax single, R>2rmax double |
| Phase | Shell offsets, plus a separate continuous adjacent-pair phase search | Equal angular spacing within each shell retained |
| Closure geometry | Single torus and proper Hopf doubling; positive ambient scaling | Other closure shapes remain unsupported |
| Symmetry | Shell populations/offsets and independent positive axis scaling | Does not span arbitrary nonsymmetric curves |

This is genuine variation in the implemented formulas, not merely metadata.
The broad six-variable numerical experiment fixes the outer shell radius,
populations, shell count and double closure while releasing the major radius,
inner radius, both pitch coefficients, relative phase and vertical scale.
Its smaller experimental slice must not be confused with exhaustive coverage
of the generator's entire parameter domain.

The exact smooth topology scope passed its own adversarial review. Removing
beta through a smooth noncollision homotopy and using positive ambient
scaling preserves the baseline full twist, up to a common mirror. That proof
does not apply automatically to the inscribed polygon or a later solver path.
The additional refinement-topology certificate now supplies the missing
endpoint bridge for the three selected runs.

## Initial experiments A–E

| Mission experiment | Evidence and acceptance | Remaining limit |
|---|---|---|
| A: recent construction | Actual supplied T(4,4) VECT geometry reproduced against plCurve; two published continuum integral models independently recomputed | The separate table value 77.47 remains discrepant with supplied geometry's 77.97687288; no exact table reproduction claim |
| B: pitch/radius release | Three seeded DE searches over six real parameters, with 217 retained objective evaluations per seed | Finite polygon objective and bounded search; no converged or global optimum |
| C: boundary packing | Exhaustive b=1..T at eight T values, with the observed winners subsequently explained by Theorem 003 | The exact theorem optimizes the first correction over fixed c, not fixed M or arbitrary schedules |
| D: multistart free-vertex refinement | Three actual ridgerunner runs; all stored start/final polygons now certified as T(12,12) up to a common mirror through an explicit alternative isotopy | Actual solver trajectories, continuous thickness and convergence remain uncertified |
| E: contact comparison | Six full contact records at two tolerances; symmetric component weights, normalized graph spectra and declared clustering cut | Exploratory finite graph similarity; neither graph isomorphism nor a continuum contact phase |

The initial D review correctly rejected two projected linking matrices as a
complete identification: distinct links can share all 66 pairwise linking
numbers. That endpoint-class obligation is now closed by the independently
reviewed sampling and polygon-path certificate, replayed for all three seeds.
It proves that the stored initial and final polygons are in the same full-twist
class through an explicit alternative isotopy. It does not certify the actual
ridgerunner trajectory or a smooth ropelength upper bound. The rigorous
asymptotic result and M2's structural observation continue to come from the
separately proved block grammar; no arbitrary free-vertex candidate inherits
the new endpoint certificate.

The three 48-sample starting polygon ropelengths and refined values are
726.402599→702.797075, 730.547841→716.108417, and
755.884021→746.879334. The 96-sample analytic starts are respectively
723.265683, 729.257873 and 751.791778: the visible mesh dependence is another
reason not to treat the coarse objective as a certified smooth value.
The recorded independent polygon engine/plCurve agreement below 5e−16 is
valuable cross-validation of those polygon values, not a mesh-error bound.

Contact counts at relative tolerances 1e−4 and 1e−3 are (31,31,41) and
(35,72,56). All three spectral clusters are separate at the declared cut 0.1;
seeds 2718 and 3141 are closer in this selected feature space. Tolerance
dependence and the very small sample are explicitly acknowledged.

## Uninjected structural observation

I inspected the exhaustive search source and independently checked that its
archived candidate rows contain exactly every integer b=1..T, with winners
(T,b)=(8,1),(16,2),(32,2),(64,4),(128,5),(256,7),(512,9),(1024,13).
The objective does not receive a target exponent or block multiplier. The
staggered block grammar itself is a supplied hypothesis; the preferred smaller
block sizes are an output. A finite fitted exponent near 0.425 is correctly
not promoted to a square-root asymptotic theorem.

The subsequent exact expansion explains the tradeoff through a/b+d b/T,
including population floors, incomplete final blocks and crossing
normalization. The independently reviewed exact positivity argument and
boundary integral certificate establish c*=sqrt(a/d)<1 and strict improvement
of the fixed-c first correction. The 1,024 selected capacity floors are also
independently certified. This satisfies the mission's requested
observation-to-explanation route without requiring an invented new packing
principle or an unproved global optimum.

The additional 16-case phase/gap search rediscovers half-phase staggering with
an objective free over f in [0,1]. Its optimizer outputs can have small
constraint violations; the separate Arb step uses explicitly rounded/padded
rational inputs and certifies those nearby pairs. The two objects should
remain distinct. Finite pair feasibility does not certify all pair types of a
full bundle. The core M2 observation does not depend on claiming novelty for
this classical staggering principle or for reciprocal/linear balancing.

## Reproducibility and independent inspection

`results/reviewer_m2_artifact_audit.json` records this review's checks. All 94
files in the variable-pitch manifest and all seven contact-output files match
their recorded hashes. Every contact comparison refers to the same final
geometry hash as the search. I independently recomputed the weighted graph
spectra and pairwise spectral distances from the stored matrices; they agree.
Every DE trial after the separately documented baseline lies within its stated
bounds, and each run retains 217 evaluations including that baseline.

The earlier M1 snapshot remains historical. The new zero-color reader fix is
appropriate: VECT's per-component color-count row must still be consumed when
the total is zero. Its regression tests check exact coordinate retention and
malformed count rejection. The independent final report covers the current
parser, grammar, phase search and tests; acceptance does not reuse the old
27-test M1 result.

## Universal coefficient map

**PASS for the map's quantifiers and scope distinctions.** It labels the
audited universal crossing lower coefficient as a baseline, without claiming
an exhaustive best-constant theorem. The known full-twist lower leading
coefficient and the new all-integer limsup upper bound give an interval for
liminf/limsup; they do not imply an existing limit or asymptotic equality.
The p>1 multiplicity/disjoint-puncture caveat is retained.

If A is required to satisfy Rop(K)≥A c(K)^(3/4) for every link, then applying
that inequality to the full-twist sequence gives A≤alpha2. This is an upper
restriction on a hypothetical universal lower coefficient, not an improvement
of a proved lower bound. Since the sequence consists of links with growing
component count, it does not constrain a knots-only coefficient without an
additional controlled connection construction. A numerical finite-family
value near 10.02 is likewise not automatically a competing rigorous
all-integer theorem. These distinctions are correctly preserved.

## Final integration closure

`M2_INDEPENDENT_VALIDATION.md` now records 17 focused tests and 65
repository-wide tests passing. I independently checked its evidence and
manifest hashes, all 13 recorded source hashes against the current files,
the captured test output hashes, and the detached manifest hash. No mismatch
was found; the commands returned zero. The focused tests include an
independent derivative/position reference, large-beta cases and the canonical
2,400-vertex zero-color atlas file compared directly with its TSV coordinates.
The independent evidence is `results/reviewer_m2_20260913.json`; my separate
gate hash check is `results/reviewer_m2_gate_hashes.json`.

I additionally checked all 18 phase output hashes and the exact stored
rational lower distance endpoints of all 16 selected padded pairs. Each is
strictly above four for squared distance. Fourteen raw optimizer winners had
small negative tolerated margins, confirming why the padded inputs must be
distinguished from raw optima. This endpoint/hash audit is recorded in
`results/reviewer_m2_phase_endpoints.json`; it is not a third independent
Arb integration or a full-bundle certificate.

**Final M2 verdict: PASS for the bounded automated discovery grammar of
mission §38.** The initially pending integration condition is closed. The
parameter coverage, genuinely uninjected block observation, independent exact
explanation and current-source validation together justify this verdict.
The initial endpoint-topology residual in experiment D has subsequently been
closed by the complete certificate and review described below. Actual solver
trajectories and smooth thickness bounds remain outside this verdict.

## Endpoint topology closure

`proofs/REFINEMENT_TOPOLOGY_MATH_REVIEW.md` passes the complete analytic-to-
polygon bridge and the explicit aligned-initial-to-final polygon isotopy.
The canonical witnesses are in `results/topology_path_20260912T231158562188Z`.
For each of the three seeds, all 165,024 nonadjacent edge pairs and 576
adjacent corners are checked over the entire time interval. Input/output
coordinate hashes and witness hashes match the archived search geometries.

The independent validation worker recomputed the analytic sampling bounds,
checked all pair/corner index coverage, and tested corrupt witnesses. I also
performed independent exact-Fraction spot checks and ran complete replay for
all three witnesses. The final replay returned three `REPLAY_PASS` results
and exit zero against unchanged source SHA-256
`0b16a0f951bcad2a0c00b012434181909c268cae399460a4856ef376e287c14a`.
The checker rejects Python optimized mode, preventing disabled assertions
from bypassing proof checks. Evidence is recorded in
`results/reviewer_refinement_final_replay_v2.json` and the separate math review.

Thus the stored initial and final polygons have type T(12,12), up to a common
mirror. This is an endpoint topology certificate through an alternative path;
it does not certify the actual ridgerunner history, polygon-to-smooth
ropelength conversion, optimality or contact criticality.
