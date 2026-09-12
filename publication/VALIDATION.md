# Publication candidate validation

The self-contained mathematical source passed the independent Astra review in
CONTRIBUTION_REVIEW.md. This is an internal AI-assisted adversarial review,
not external peer review, a formal proof-assistant verification, or an assertion
of publication novelty. No submission/contact has occurred.

| Obligation | Evidence | Status |
|---|---|---|
| Smooth self-thickness and all-pair clearance | proofs/ADVERSARIAL_REVIEW_001.md and002.md | PASS |
| Full-twist topology, framing, doubling and deletion | Same independent proof reviews | PASS |
| All-integer leading asymptotic bound | Theorem002 and its review | PASS |
| Uniform block correction and fixed-c optimum | proofs/ADVERSARIAL_REVIEW_003.md | PASS |
| Main Arb derivative/rounding/endpoint implementation | proofs/CERTIFICATE_IMPLEMENTATION_REVIEW.md | PASS |
| Boundary integral and selected integer floors | proofs/BOUNDARY_CERTIFICATE_REVIEW.md | PASS |
| Publication mathematical condensation | CONTRIBUTION_REVIEW.md | PASS |
| Pinned output integrity and exact decimal inequalities | checkers/check_endpoints.py, independent reviewer closure | PASS |
| Local full reproduction | results/publication_reproduction_20260912T231317912269Z | PASS: 65 tests, coefficients, block search and all endpoint replays |
| Exact endpoint topology bridge | proofs/REFINEMENT_TOPOLOGY_MATH_REVIEW.md and proofs/REFINEMENT_TOPOLOGY_IMPLEMENTATION_REVIEW.md | PASS: three inputs/finals, full witnesses, tamper tests |
| Figure | figures/make_figures.py | Generated and visually inspected |
| Publication novelty | references/FOCUSED_NOVELTY_AUDIT.md, BOUNDARY_NOVELTY_AUDIT.md | POSSIBLY NOVEL, provisional |
| Typeset PDF | BUILD_STATUS.md | Compiled; final visual check recorded there |

Canonical refreshed main coefficient run:
results/certificate_shell_final_20260913/certificate.json. It binds current
claim ledgers to unchanged reviewed arithmetic and proves alpha2<10.614.
The original noguard certificate remains pinned for the publication checker
and independent-review linkage; exact old claim bytes are saved by SHA-256 in
results/source_snapshots. Refreshing status prose does not rewrite old results.

The refreshed boundary run results/boundary_certificate_20260912T224451Z
uses1024×2048 direct interval rectangles. The independently reviewed192-bit
source run and224-bit independent finer calculation are recorded separately.
All quoted tight diagnostic decimals are distinguished from rational outward
endpoints. No finite sampled geometry is used as proof of smooth thickness.

Reproduce from the lab root with its Python3.12 environment:

```bash
.venv/bin/python publication/reproduce.py
.venv/bin/python publication/reproduce.py --full
```

The default verifies pins/exact rational thresholds, recomputes the leading
certificate and figure into a new result directory. Full mode adds the tests,
boundary certificate, finite block search and replay of the three endpoint
topology certificates. Ridgerunner is an independent
optional lab experiment, not a hidden prerequisite for the analytic theorem.
The pinned Python dependency set is requirements-lock.txt. The publication
folder requires the accompanying lab repository; it is not a self-contained
standalone Python package.

Limits: no exact finite-T block argmin, no equal-M correction comparison, no
arbitrary schedule/global optimum, no matching lower bound, no universal lower
coefficient improvement. The broader variable-pitch engine has an exact smooth
isotopy proof but its free vertex refinement lengths remain numerical diagnostics and
do not enter the publication theorem. The three final polygon link types are
now independently certified by the separate endpoint-isotopy bundle.
