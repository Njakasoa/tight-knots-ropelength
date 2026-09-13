# Validation and scope audit — generalized staggering

2026-09-13. Root-agent mathematical audit and executed checks; no independent
referee report for this follow-up. Original reviewed lemmas are unchanged.

## Objective coverage

| User question | Evidence | Conclusion |
|---|---|---|
| Can period 3, 4, ... staggering be built? | Generalization note sections 1–2: exact all-parameter finite separation and arbitrary phase sequences; 21 finite Arb examples, including genuine period 4 | Yes, for every fixed finite period |
| Can a longer phase period reduce the sufficient mean gap? | Section 3: signed-increment parity, concavity inequality, and explicit equality configurations, valid for all positive integer p | Exact solved optimum in the specified row test; even minimizers repeat period 2, odd periods incur a defect |
| Can nonuniform spacing help? | Section 3: strict odd-period improvement over common gaps; section 5: five fixed-M finite toroidal constructions with positive outward lower bounds on length savings | Yes, for odd-period mean gaps and for the explicit finite comparisons |
| Does this improve the leading ropelength coefficient? | Section 4: fixed-period limiting passage; finite computations alone do not establish a new asymptotic law | No improvement established; no claim of full-grammar optimality |

The objective is an investigation of generalizability, not a request for a
complete global classification of thick-link minimizers. The results above
answer both branches with proofs and constructive finite examples. Arbitrary
angular phase sets are covered by the lemma but have not been optimized.

## Executed verification

- Full suite: **96 passed**, including 31 new tests. One existing SciPy
  quasi-Newton warning in the phase-search test; no test failure.
- All 21 periodic and five nonuniform configurations pass all shell-pair
  checks. Same-shell clearance uses exact phase-grid spacing; cross-shell
  checks use exact LCM phase reduction or rational radial clearance.
- All **26 saved rational-input certificates replay exactly** without search.
  Source hashes match the recorded implementation. See `replay.json`.
- The finite length comparisons use 4096-cell midpoint integration with an
  explicit analytic error bound and 192-bit Arb arithmetic. The archived
  intervals enclose the full sum, including both cores and both bundles.
- Separate adaptive quadrature agrees with the finite interval check. LCM
  reduction is compared against enumeration; the dynamic program is compared
  against exhaustive cycles and the all-period analytic formula.
- Tests reject phase/radius/population/closure/dimension tampering and a
  nonadjacent-shell collision whose adjacent pairs pass. A checker that only
  considered neighbors would fail this case.
- The verifier uses explicit exceptions, not Python assertions, for its
  mathematical gates. An initial Arb zero-containing generic-power issue was
  detected by the first run and corrected to interval multiplication before
  the canonical archive and successful tests were generated.
- `periodic_patterns.png` was rendered and visually inspected. It depicts
  the frozen local disk model, not an actual 3D tube or a ropelength minimizer.

## Mathematical audit

The finite pair lemma is a lower bound on actual squared distances for all
curve parameters. Its scalar harmonic minimization and topology/self-reach
dependencies are explicitly traced to Theorems 001–002. The mean-gap
optimality theorem is only for the sufficient test g(d)=2sqrt(1-d²);
using a sufficient inequality as a necessary physical condition would be
invalid, and neither note nor result summary does so.

Odd-period closure is essential: all signed increments sum to an integer;
with odd p their half-step signs sum to a half-integer. This gives the missing
half-step deficit and the concavity bound. The exhibited one-defect motif
attains that bound. Even equality forces all differences to be half-steps,
so a nominal period-four optimizer is correctly identified as period two.
Genuine period-four feasibility is tested separately.

Each finite length comparison keeps M, R, all N_i and all phase grids equal.
Only radii change. The reference major radius is the same slightly padded
rational R as the candidate, not exactly the original irrational R.
Strict radius compression also implies strict length reduction analytically
by the even, strictly convex component-length function. The outward integral
comparison independently quantifies the improvement. No best-known record,
novelty, finite-M global optimum, or new leading bound is claimed.

## Reproduction

```
.venv/bin/python experiments/generalize_staggering.py --angular-cells 4096
.venv/bin/python experiments/replay_staggering_generalization.py
.venv/bin/python -m pytest -q
MPLCONFIGDIR=/tmp/tight-knots-mpl .venv/bin/python experiments/plot_staggering_generalization.py
```

Evidence directory: `results/staggering_generalization_20260913/`.
The earlier publication PDF remains the original reviewed manuscript; this
follow-up is documented separately pending mathematical review and integration.
