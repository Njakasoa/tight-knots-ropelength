# Independent M2 validation: variable-pitch discovery grammar

Date: 2026-09-13. Reviewer: independent validation worker.

## Verdict

The current variable-pitch grammar and its bounded numerical consumers passed
the independent checks. The focused run passed 17 tests and the repository-wide
run passed 65 tests. The evidence is frozen in
`results/reviewer_m2_20260913.json`, with separate captured stdout/stderr,
manifest, and detached manifest hash.

The audit covers the smooth coordinate formula, first and second derivatives,
periodic closure, the beta/phase/positive-scale homotopies, proper Hopf
doubling, configuration and runtime failure paths, the variable-pitch search
and contact-clustering metadata, and the post-M1 zero-colour VECT parser fix.
It does not promote polygon or Ridgerunner output to a smooth thickness or
ropelength certificate.

## Frozen evidence and source hashes

| Artifact | SHA-256 |
|---|---|
| `tests/independent/test_discovery_grammar_independent.py` | `9f3855270390e2e3984098eceeca666690f8292c46af2430195be3d5b81e2049` |
| `tests/test_vect_zero_colors.py` | `af45a614b7f8dd5887fd4b9a24f7afb1781699cd7f66f0705e583e9d862183ae` |
| `results/reviewer_m2_20260913.py` | `c0177ca9c7edbf1b11c4b990b72778dcdc9a8ed8e8db6f84d0aed7a20a174d83` |
| `results/reviewer_m2_20260913.json` | `b8ad43091d6372dac0d624edcd9aa4c78bc97da89abfcd40e6d36efc4de29cb6` |
| `results/reviewer_m2_20260913.manifest.json` | `5dce7efa4c19b4d69914415f21477238d315541afbe64f66ce0604390996a0cb` |
| `results/reviewer_m2_20260913.manifest.sha256` | `3c626be9850330b2eb8dc1383100f0864eec40cbeda40ae30b45d700e265af82` |
| `results/reviewer_m2_metrics_20260913.json` | `ccbea9fb22196990a4da0ce457b09824266a7fa39d723cb9a3b366f6cde9ba26` |
| `src/discovery/grammar.py` | `df403a5d03fbc997b5e9a6676ef9b7f0d5297a71d41fb4fb416df209058a53ff` |
| `experiments/search_variable_pitch.py` | `7fae556e2fcfe5a9b0e0efdc9b1169db991bcdef9c8c0f5aa271e72b9110848e` |
| `experiments/cluster_pitch_contacts.py` | `15d5c16a09285d34117fe203de18776a3e08021cd825a987e3cdf418533d9681` |
| `src/curves/vect.py` | `438e3d85cee81bf99c4d6191a9eaf2554d2682295622c910debb368fb6b0358f` |
| `proofs/VARIABLE_PITCH_TOPOLOGY.md` | `0fbc7fa7e72688846a2a33fe23cabc56a2dffc3c30778565624f837a8df5aa94` |

The frozen runner records the exact virtual-environment commands. The focused
command was:

```text
.venv/bin/python -m pytest -q \
  tests/independent/test_discovery_grammar_independent.py \
  tests/test_vect_zero_colors.py
```

It reported `17 passed`. The full command `.venv/bin/python -m pytest -q`
reported `65 passed, 1 warning in 31.216s`; the warning was SciPy's
`delta_grad == 0.0` notice in an existing phase-search test.

## Independent derivative and coordinate audit

The test reference implements the defining normal-disk embedding directly,
including the proper map `P(x,y,z)=(R+x,-z,y)` and the final positive diagonal
scale. It does not call the production derivative to form its reference. The
production `d1` and `d2` values are compared with five-point central finite
differences of independently sampled positions. For

```text
R=8.7, radii=(0.9,1.8,2.6), populations=(2,3,4),
phases=(0.17,-0.63,1.11), beta=(0.43,-1.37,2.15),
double_hopf, scale=(1.23,0.81,1.47),
```

the coordinate reference maximum error was 0.0 in the sampled float arrays.
The largest first-derivative error was `4.794209473857336e-11` with
`h=1e-4`; the largest second-derivative error was `6.202704128099867e-09`
with `h=2.5e-3`. The endpoint comparison for all 20 components gave maximum
position, first-derivative, and second-derivative errors of respectively
`3.9968028886505635e-15`, `1.4210854715202004e-14`, and
`4.618527782440651e-14`.

A second configuration used beta values `(2.7,-4.2,7.5)`, including
non-monotone angular phase maps. It retained periodic closure and positive
sampled cross-section separation. This checks the stated finite smooth
embedding condition without adding an unclaimed bound such as `|beta|<1`.

## Topology hypotheses and ambient transformations

The independent tests exercise the hypotheses recorded in
`proofs/VARIABLE_PITCH_TOPOLOGY.md`:

- `R > max(r_i)` keeps the cylindrical radius positive, so analytic image
  equality recovers longitude modulo `2*pi`; distinct normal-disk radii and
  equally spaced same-shell phases then give noncollision.
- The beta-to-zero path preserves every radius and applies a common rotation
  to the equally spaced points of each shell. An independently constructed
  phase-offset path and the positive diagonal scale path were also sampled.
  Their minimum cross-section separations in the metrics artifact were 0.9031,
  0.8179, and 0.9000 respectively for beta, phase, and scale homotopies.
- The double configuration has `Q=10`, 20 components, and label `T(20,20)`;
  the single configuration has `Q=10` and label `T(10,10)`. The independent
  linear matrix of `P` has determinant `+1`. At identity scale, the sampled
  two-core minimum was at least `R=8.7`, while the grammar enforces the
  stronger general separation condition `R > 2*max(r_i)` for double mode.

These checks support the construction-level full-twist and isotopy hypotheses
for the analytic formulas. They do not certify isotopy of a finite polygon
sample.

## Variable-pitch search and contact clustering

The three-seed search record is
`results/variable_pitch_20260912T224501767133Z/search.json` with SHA-256
`7107b746b09fbe339644bbf9f1dd9e5e24dd2cdd76fba52337e795647dd07496`.
Its generator hash matches the current `src/discovery/grammar.py` hash above.
The search fixes populations `(2,3)`, outer radius 2, a core, double Hopf
closure, and 24-point optimizer samples while varying major radius, inner
radius, both pitch coefficients, relative phase, and positive z scale. Each
Ridgerunner run returned zero and produced 12-component, 576-vertex final
geometry. The final reported ropelengths were 702.797074809106,
716.108417224441, and 746.8793338131616 for seeds 1729, 2718, and 3141.

The contact comparison is
`results/contact_clusters_20260912T224627301208Z/comparison.json` with
SHA-256 `1940e21ee5c65ecb8861059da68247028d073aa78f36a5d38923cff60d5c0c8f`.
Both independent generic projections gave a full off-diagonal absolute-one
linking matrix for all three final geometries, and the independent polygon
ropelength engine agreed with plCurve to relative differences at most
`4.86e-16`. Contact counts were `(31,35)`, `(31,72)`, and `(41,56)` at the
two tolerances for seeds 1729, 2718, and 3141. These are finite geometric
diagnostics; contact-graph spectra do not prove graph isomorphism or a
continuum phase transition.

The earlier phase-search record
`results/discovery_phase_20260913_v1/search.json` has SHA-256
`6ee72a33e11e8fa600e70ed1c0d8e7f4ad0daf6f49d268313aa4768ca557b6eb` and
explicitly describes a machine search of a conservative adjacent-shell pair
bound. It uses fixed p=1 toroidal pitch and a pair-level Arb certificate. It
does not provide a full-bundle variable-pitch thickness certificate, so it is
context for discovery rather than evidence for the broader grammar.

## Canonical zero-colour VECT regression

The post-M1 parser change in `src/curves/vect.py` always consumes and validates
one per-component colour-count row, including when the VECT header has
`n_colors=0`. The independent regression parses the canonical atlas
`data/reference/cantarella-atlas/knots/prime/3-10/3_1.vect`, independently
parses its `3_1.tsv` coordinate rows, and obtains one closed component with
2,400 vertices in both forms. The coordinate maximum absolute difference is
0.0. The VECT file hash is
`892a10e01a90b3491c2c7f6c7a5e70f3b5f93293c06083240c13136fa11b1482`; the TSV
hash is `e649e6d41a9d0a76bf6be1a93c6eed483ac3c949b6677f3f59520d0e958e8c3c`.
The companion negative test rejects a nonzero component colour count under a
zero-colour header. This fix is included in the 65-test full-suite evidence.

## Claim limits

This validation supports the implementation of the finite smooth grammar and
the stated construction-level homotopy hypotheses. It does not certify
polygonal reach or thickness, a Ridgerunner solver path, a smooth ropelength
upper bound for variable pitch or anisotropic scale, a finite-M optimum, a
global optimum over schedules or grammars, or publication novelty. The old
constant-pitch shell thickness certificates cannot be transferred to the new
variable-pitch search without a separate reach analysis. The search and
contact records remain numerical diagnostics, and all topology labels retain
the analytic-versus-sampled distinction in the grammar metadata.
