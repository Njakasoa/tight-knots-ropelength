# M1 acceptance gate — PASS

Independent final decision: [M1_REVIEW.md](M1_REVIEW.md). Evidence is frozen in
results/reviewer_final_test_snapshot and results/reviewer_final_gate_hashes.json.
The 27 tests included 12 independent tests. Later M2 work is separate from this snapshot.

| Mandatory requirement | Accepted evidence | Status |
|---|---|---|
| Environment audit | ENVIRONMENT_AUDIT.md, software/BUILD_PROVENANCE.json | PASS |
| Normalization | NORMALIZATION.md, exact radius controls | PASS |
| Current bibliography | STATE_OF_THE_ART.md, primary-source audits through 12 September 2026 | PASS |
| Ridgerunner reproduction | Real 47/400-vertex runs; upstream 4/4 and tsnnls 11/11 tests | PASS |
| Independent thickness | Independent formulas and collision/scale/active-face regressions | PASS |
| Topology | Full-twist proofs; signed projections; final trefoil Fox determinant 3 | PASS |
| Unknot control | Exact 2π, scaling/resolution checks | PASS |
| Trefoil control | Pinned tight coordinates, actual refinement and topology checks | PASS |
| Simple torus link | Exact Hopf 8π, torus-family tests and actual T44 geometry | PASS |
| Certified upper demo | Machin rational controls, Arb shell integral and independent checker | PASS |
| Contact extraction | Stored struts/kinks/tolerances, current T44 artifact and figure | PASS |
| Independent reviewer | Astra M1 review after resolving reported failures | PASS |

Scope: reproducible numerical polygon geometry and separate analytic/interval
proof paths. General smooth root isolation is incomplete. Actual T44 coordinates
reproduce 77.97687288, while the companion table says 77.47; the discrepancy is
recorded, not called a successful reproduction of the table. M2 began only after
this PASS. A passed infrastructure gate does not establish novelty or optimality.
