# Result evidence index

Use the selected records below. Older runs are retained for the audit trail and
are not silently upgraded when source bugs are fixed.

| Evidence | Selected record | Scope |
|---|---|---|
| Reviewed asymptotic certificate | certificate_shell_N512M1024_noguard/certificate.json | Arb alpha2 upper10.613733558728<10.614; linked to Theorem002 |
| Independent arithmetic implementation | reviewer_certificate_check.py and reviewer_certificate_check.json |224-bit independent sum and rational endpoint checks |
| Repaired engine counterexamples | reviewer_geometry_regressions.py and reviewer_geometry_regressions.json | scaled/near-endpoint collisions, projection scaling, exact controls |
| Original falsifying probes | reviewer_m1_probes.json | historical failures; never current positive evidence |
| Positive controls | controls/controls_20260912T220626013170Z_c06ce8d71d.json and matching manifest | corrected Hopf8pi, real source hashes, resolution/scaling |
| Actual Ridgerunner refinements | ridgerunner_autoscaled_20260913/manifest.json |47/400-vertex trefoil numerical refinement |
| Final-coordinate topology | reviewer_ridgerunner_final_topology.json | geometric three-crossing diagrams and determinant3 for both final results |
| Recent-paper reproduction | recent_T44_20260912T220613Z/inspection.json | plCurve comparison, symmetric linking matrix,1011 finite contacts |
| Initial standard-torus searches | torus_search_20260912T214900Z/search.json | two seeds/family, radius/stretch searches; numerical only |
| Finite shell diagnostic exports | finite_shell_family_staggered_20260913_v4/shell_family.json | interval lengths and floors; sampled geometry is not a certificate |

Earlier positive-control records contain the old Hopf16pi reporting error and/or
lack actual source hashes. Earlier T44 inspections either predate the symmetric
linking fix or lack source hashes. Certificate runs with the1e-15 guard are
superseded by the unguarded run; the guard only widened the interval, so its
removal is an audit simplification rather than a stronger analytic premise.
The initial250-step Ridgerunner run lacked forced scaling and did not converge
sufficiently; it is not the accepted tight-trefoil reproduction.

The independent validator's latest report and M1_REVIEW select the authoritative
full-suite run; results/independent_final is an earlier10-test run and must not
be mistaken for the final expanded regression suite.

Direct numerical reconstruction of both2026 continuum constants is stored in
`klotz_limits_20260912T221239Z/reproduction.json`:13.377596407953076 and
11.685949053273111. It uses the actual length integrals, not hardcoded rounded
correction factors, and does not claim interval certification.

## M2 and reviewed boundary correction

| Evidence | Selected record | Scope |
|---|---|---|
| Refreshed main certificate | certificate_shell_final_20260913/certificate.json | Same reviewed arithmetic; current ledger hashes; alpha2<10.614 |
| Independent boundary certificate | reviewer_boundary_20260913.json/.py and manifest |224-bit1024×2048 direct ranges, exact endpoints, selectedfloors |
| Refreshed boundary certificate | boundary_certificate_20260912T224451Z/certificate.json |1024×2048 rectangles with current theorem-status snapshot |
| Exhaustive block discovery | discovery_blocks_20260912T221841Z/discovery.json | Allb1..T, no supplied target exponent; finite lengths numerical |
| Independent asymptotic stress | reviewer003_independent.json/.py | Exact-integral derivation separately reviewed; numeric checks toT65539 |
| Free phase search | discovery_phase_20260913_v1 |16cases, independent grids, finitepairArb certificates |
| Variablepitch / multistart | variable_pitch_20260912T224501767133Z/search.json |3DEstarts and3actual boundedRR refinements; numerical only |
| Contact comparison | contact_clusters_20260912T224627301208Z/comparison.json |2tolerances, fullcontacts, projections, independentthickness comparison |
| Small coordinate atlas | small_atlas_20260912T224716782669Z/atlas.csv and.json |6source-labelled knots; explicit unfilledcertification/record fields |
| Publication reproduction | publication_reproduction_20260912T223709466785Z/reproduction.json |Defaultexactthresholdchecker/maincertificate/figure success |

Historical source snapshots for changed claim prose are in source_snapshots,
keyed by SHA-256. The original reviewednoguardcertificate stays pinned; changing
statusprose does not silently rewrite the historical manifest or its review.

## Endpoint topology bridge

`topology_path_20260912T230219109163Z` is the canonical three-seed certificate
bundle. Each seed stores165024 nonadjacent-edge separating witnesses and576
adjacent-corner witnesses, plus rigorous analytic sampling bounds. All three
pass at192-bit Arb precision. Replay via experiments/certify_refinement_topology.py
checks inequalities and complete pair/time coverage. This proves final endpoint
full-twist types using an explicit alternative isotopy; it does not certify the
actual Ridgerunner path or smooth ropelength. The earlier one-seed bundle
predates two checker-hardening changes and is historical.

The final hardened endpoint-topology bundle is
`topology_path_20260912T231158562188Z`, regenerated after independent tamper
checks. The checker explicitly rejects optimized Python (which strips asserts)
and malformed trailing VECT data. The preceding all-three bundle remains valid
in normal mode but predates these input/runtime guards. The publication full
reproduction now replays the hardened bundle.

Final full publication reproduction: `publication_reproduction_20260912T231317912269Z`, all seven commands returned0, including65 tests and all three hardened endpoint witness replays. Independent refinement review and tamper evidence: `reviewer_refinement_20260913.json` and `proofs/REFINEMENT_TOPOLOGY_IMPLEMENTATION_REVIEW.md`.
