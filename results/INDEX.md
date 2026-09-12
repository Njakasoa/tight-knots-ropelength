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
