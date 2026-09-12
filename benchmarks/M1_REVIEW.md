# M1 independent adversarial review

Date: 2026-09-13. Reviewer: delegated Astra reviewer. The audit began by assuming
the implementations and claimed M1 completion could be wrong. Production files
were read, not edited by this reviewer. Root implemented the reported fixes.

## Verdict

**PASS for M1: a reproducible geometry laboratory within the numerical and
analytic-certification scopes described below.** Every mandatory acceptance row
has stored evidence. The repaired implementation passes the fresh full suite
(27 tests, including 12 independent tests), and the reviewer verified its test,
runner, result-manifest and reviewed geometry-source hashes. No concrete blocking
implementation defect remains from this bounded audit.

This verdict relies on actual Ridgerunner runs, source-coordinate checks,
independent thickness comparisons, constructive topology proofs, a reviewed
interval certificate, and stored contact extraction. The test count alone would
not establish M1: the defects below survived earlier green suites. M2 may start
with these documented limits. This is not a publication or global-optimality gate.

## Acceptance audit

| Mandatory item | Inspected evidence | Review status |
|---|---|---|
| Environment audit | ENVIRONMENT_AUDIT; BUILD_PROVENANCE; real upstream tsnnls and Ridgerunner suite logs | PASS; genuine build and upstream 4/4 plus 11/11 test logs |
| Normalization | NORMALIZATION; smooth proofs; corrected exact control helper | PASS after Hopf reporting repair |
| Current bibliography | STATE_OF_THE_ART; primary-source audit records and version labels | PASS for current source audit; novelty assessment remains separate |
| Ridgerunner reproduction | actual autoscaled trefoil47/400 run directories, logs, final VECT files and manifest | PASS; actual final-coordinate three-crossing determinants verified |
| Independent thickness | independent parser/length/DCSD/plCurve comparisons; reviewer collision probes | PASS for a numerical checker; fresh independent suite and adversarial repairs |
| Topology | constructive full-twist proofs; geometry-based projected linking and Fox determinant paths | PASS for M1 controls; coordinate-based final checks and constructive families |
| Unknot | exact 2pi proof and rational control; resolution/scaling experiment | PASS; fresh stored controls inspected |
| Trefoil | sourced 47/400 references, plCurve metrics and genuine optimizer results | PASS as a numerical control; final invariants verified |
| Simple torus link | Hopf constructive proof, noncoprime torus tests, recent T44 supplied geometry | PASS; fresh symmetric matrix and contact artifact |
| Certified upper demo | N512/M1024 Arb certificate, exact rational endpoints, independent 224-bit rerun | PASS; see CERTIFICATE_IMPLEMENTATION_REVIEW |
| Contact extraction | finite vv/ve/ee pairs and kink records with explicit tolerance in T44 inspection | PASS for finite extraction; refreshed artifact inspected |
| Independent reviewer | this report, reviewer probe scripts/results, certificate review | PASS; findings resolved and final evidence verified |

## Findings and their resolution

1. **Scaled self-intersection received positive thickness.** The closed polygon
   `1e-7 * [(0,0,0),(1,0,0),(.5,-1,0),(.5,1,0)]` has an exact crossing, but
   originally returned thickness `1.3196601125010505e-8`, DCSD infinity and
   `complete=True`. Squared lengths were compared to an unsquared degeneracy
   tolerance. The segment closest-point routine also mixed degeneracy and
   parallel thresholds. Root separated squared tolerances and replaced its
   fixed clamping iteration by interior stationary plus boundary-face minimizers.
   The reviewed result now reports thickness zero, a collision and incompleteness.

2. **Endpoint tolerance swallowed an exact collision.** The closed polygon
   `[(0,0,0),(1,0,0),(1,-1,0),(5e-9,-1,0),(5e-9,1,0),(-1,1,0)]` crosses on
   edges 0 and 3, yet returned positive thickness `2.5e-9` and complete true.
   Testing zero distance before endpoint class filtering and using the actual
   interior partition fixes the counterexample. It now returns zero thickness.

3. **Projection invariants changed under simple scaling.** A sampled trefoil
   had three crossings and determinant 3 at unit scale, but zero crossings
   and generic true at scale `1e-5`. A determinant threshold with an absolute
   floor suppressed the crossings. Relative scale tests and centered projection
   coordinates repair this. Determinant 3 now survives scales `1e-7,1e-5,1,1e5`.
   A collapsed edge-on circle now correctly gives a nongeneric projection.
   Linking matrices are symmetric after repair and refuse nongeneric diagrams.

4. **Hopf exact-control output was off by two.** The helper's own total length
   `4pi R` and thickness `R/2` imply `8pi`; its output said `16pi`. The helper
   now reports `8pi`. Its original nearest-rounded decimal-only endpoints
   could also cease to enclose the exact interval. Rational endpoint payloads
   and directed integer decimal rounding now pass checks at 12 and 40 terms.

5. **Stale result evidence remains distinct from corrected source.** The earlier
   T44 inspection contains an antisymmetric linking matrix and earlier controls
   contain the erroneous Hopf expression. They should remain historical failed
   artifacts, with fresh runs cited as authoritative. The control manifest's
   old `source_engine` field hashed a descriptive literal rather than source
   bytes; the authoritative fresh manifest now hashes the actual source files.

Original falsifying outputs are preserved in `results/reviewer_m1_probes.json`.
Post-repair outputs and source hashes are in `results/reviewer_geometry_regressions.json`;
the independent runnable probe is `results/reviewer_geometry_regressions.py`.


## Refreshed evidence inspected

- `results/reviewer_final_test_snapshot/` freezes the final validation JSON,
  27-test full-suite stdout, 12-test independent-suite stdout and original hash
  manifests from `results/independent_final/`. The reviewer added hashes of all
  current Python source/test files. Result and detached-manifest hashes, tester
  and runner hashes, and reviewed production hashes matched before freezing;
  see `results/reviewer_final_gate_hashes.json`.

- `results/controls/controls_20260912T220626013170Z_c06ce8d71d.json` and its
  manifest: corrected 8pi Hopf control; real per-source hashes and output hash match.
- `results/recent_T44_20260912T220613Z/inspection.json` and manifest: symmetric
  linking matrix with every off-diagonal entry -1, polygonal ropelength
  77.9768728808478 versus plCurve 77.97687288084772, and 1,011 finite contacts.
  Source and output hashes match the inspected files. The companion published
  table gives 77.47; that value is **not reproduced** by the supplied VECT. The
  discrepancy is 0.50687288, about 0.6543%, and is explicitly retained rather
  than explained away by normalization. M1 accepts reproduction of the actual
  geometry and independent software agreement, not confirmation of 77.47.
- `results/reviewer_ridgerunner_final_topology.json` and its reproduction script:
  both actual final VECT outputs admit three-crossing projections with Fox
  determinant 3; minimum projected crossing depth gap exceeds 1.005. Geometry
  hashes, view directions and independent-helper hash are preserved.

The additional continuum reproduction at `results/klotz_limits_20260912T221239Z`
computes 13.377596407953076 and 11.685949053273111 by integrating the displayed
population densities and toroidal speed, at two quadrature tolerances. Inspection
confirms that the script does not substitute printed correction constants. These
are numerical reproductions of the cited continuum models, not certificates of
the paper's finite occupancy rule. The second value is consistent with a coarse
reported 11.68, but it rounds conventionally to 11.69 at two decimals. None of
these distinctions invalidates the separately proved shell certificate.

## Scientific scope and limitations

The polygon checker enumerates vertex/vertex, vertex/edge and interior edge/edge
local-minimum candidates and uses Rawdon MinRad, not the circumradius of three
successive vertices. These are the relevant finite closest-point classes.
The new segment routine minimizes the convex quadratic over the parameter
rectangle using every boundary face and any interior stationary point. A separate
500-case comparison against SciPy bounded linear least squares (seed 917) found
maximum distance discrepancy 9.12e-13; see `results/reviewer_segment_faces.json`. Tests
against independent plCurve/octrope provide meaningful numerical validation.
However, this floating routine is an estimator, not a certified Rawdon solver:
finite tolerances and floating predicates are not a proof of candidate completeness.
Its `complete` flag must be read only in that limited enumerative sense.
It does not certify the reach of an analytic curve sampled into a polygon.

The smooth checker explicitly marks itself incomplete and uses finite-start
stationary-root searches. It cannot exclude missed smooth struts or certify
arbitrary analytic geometry. The shell theorem instead uses a separate proof
covering all parameter pairs and curvature, so the theorem does not inherit
this sampling limitation.

Projected linking numbers and determinant checks are computed from coordinates,
not merely copied from knot metadata. A determinant alone is not a complete
knot classifier, and pairwise linking alone does not identify a full torus link.
For the parametric families the constructive full-twist proof supplies what
those numerical invariants cannot. Imported tight-knot controls combine source
provenance and actual-coordinate diagnostics; they are not a general formal
isotopy certifier for arbitrary future optimizer trajectories.

Contact graphs are finite tolerance-dependent extractions. They preserve pairs,
parameters and kink records; kink records include an active flag. A count of all
kink records is not the count of active curvature constraints. Continuous strut
families, exact multiplicities/symmetries and force-balance criticality do not
follow from a finite graph and remain outside this M1 extraction claim.

The actual 47-vertex run improves about 36.66704 to 33.14902; the 400-vertex
reference improves about 32.74903 to 32.74879. These support functioning external
optimization and reference reproduction, not a record trefoil, a certified smooth
upper endpoint, or a global optimum. Upstream test counts support the external
software build; they do not replace these geometric checks.

The shell certificate separately gives alpha2 < 10.614 for the reviewed
all-integer limsup construction. That result does not settle publication novelty
or any lower/upper equality. The M1 evidence conditions are now closed; future
candidates still require their own topology, thickness and novelty reviews.
