# Independent contribution and manuscript review

Date: 13 September 2026. Reviewer: delegated Astra adversarial reviewer.
Scope: `publication/main.tex`, compared with Theorems 001–003, their passed
adversarial reviews, the main certificate implementation review, and both
bounded novelty audits. No manuscript or production source was edited by this
reviewer. Source hashes are in
`results/reviewer_publication_source_snapshot.json`.

## Verdict

**PASS for the mathematical contribution and its stated scope in the revised
source.** The condensed argument preserves the hypotheses and error orders of
the reviewed proofs. No new mathematical obstruction was found. This is a
review of a local candidate, not external peer review, verified novelty,
global optimality, or completion of the broader M2 discovery program.

**All source corrections raised by this review are resolved.** The separate
boundary-certificate review also passed and its artifact is present. This
review assesses mathematical source and contribution scope; the subsequent
PDF build and visual checks are recorded separately in `BUILD_STATUS.md`.
The findings below retain the initial review history, with their resolution
recorded in the final source closure.

## Mathematical obligations

| Source location | Result | Review evidence |
|---|---|---|
| Abstract; conventions; Theorem `upper` | PASS | Tube radius and total component length are explicit. Crossing normalization is M(M−1), and the all-integer upper bound is a limsup. |
| Lemma `same`, lines 64–96 | PASS | Conservative capacity, harmonic separation, curvature estimate and doubly critical self-distance estimate retain the assumptions r≥2 and R≥2r+2. Longitude injectivity gives embeddedness. |
| Lemma `cross`, lines 99–129 | PASS after correction | The block clause now explicitly assumes 0<r0≤u≤v<R/2 and N≥3. The half-grid separation bound applies to all odd phase differences, rather than only matched component indices. |
| Construction; Proposition `finite`, lines 132–185 | PASS | First radius is two; every block has one conservative population; phases alternate; boundary gaps are two; nonadjacent gaps suffice. Cross-bundle clearance follows from core distance R and R−2rT=2. |
| Proposition `finite`, topology proof | PASS | Configuration-space isotopy and zero framing establish the full twist. The doubling argument includes internal/mutual twist sign compatibility and a proper rigid motion. It does not infer link type merely from pairwise linking numbers. |
| Theorem `correction`, equation `expansion` | PASS | The regime b→∞, b/T→0 is explicit. Bounded ceiling offsets, uniform capacity/length estimates, incomplete blocks, population floors and the actual outer radius all have the reviewed error orders. |
| Weighted lag and quotient calculations | PASS | The weighted derivative is n'e, not (ne)'. Core terms are below first order. The two bundles, lambda scaling and M−1 crossing correction yield the stated alpha and d. Q comparable to T² is properly restricted to b/T→0. |
| Strict improvement in Theorem `correction` | PASS | The exact integral bounds prove d>1/8>a>0, so c*<1 and beta*<beta(1) without relying on numerical signs. Optimization is only over fixed c in b=floor(c sqrt(T)). |
| Theorem `upper`, all-integer deletion | PASS | The least qualifying T argument does not assume monotonic component counts. The count discrepancy is O(T^(3/2)); deletion preserves thickness and leaves a full twist on the surviving strands. Only the leading all-M limit is claimed. |
| Main certificate, lines 295–313 | PASS | Derivative bounds and the tensor midpoint error agree with the independently reviewed implementation. The exact rational alpha endpoint is below 10.613734 and therefore below 10.614. Diagnostic midpoints do not establish the inequality. |
| Discovery and limitations, lines 324–366 | PASS | Exhaustive finite winners are reported as diagnostics. The text expressly excludes fixed-M optimization, arbitrary schedules, an exact finite argmin, a subleading deletion theorem, global ropelength optimality and unsupported wider-grammar reach. |

The abstract initially omitted the asymptotic regime; the initial standalone
block lemma also omitted its positive-radius and population hypotheses. Both
were corrected during this review and independently reread. These are resolved
findings, not current objections.

## Contribution and prior-art scope

The manuscript correctly cites the direct reciprocal-plus-linear optimization
in Klotz–Thompson's arXiv v1 Eqs. (17)–(18). That antecedent means the generic
balancing mechanism and square-root optimizer cannot be presented as the new
result. The possible contribution is the exact admissible staggered shell
construction and its geometry-specific uniform expansion, including the
population-locking term J and discrete-block remainder. The source now makes
that distinction and keeps the bounded audit's **possibly novel** verdict.

The common-hole comparison near 11.68 preserves the earlier source's
no-overlap qualification. No exact reproduction of its separate T(4,4) table
entry 77.47, no best-known record across other families, and no lower-bound
improvement are asserted here. The physical paragraph correctly describes
separate closed filaments and a sufficient-length upper construction; it does
not turn ropelength into a polymer free-energy model.

## Bibliographic check

The initial `kt25` entry incorrectly named W. A. Thompson and used a descriptive
placeholder title. The revised entry correctly names **F. Thompson (Finn
Thompson)** and gives *Ropelength-minimizing concentric helices and
non-alternating torus knots*. It explicitly identifies arXiv v1 for the cited
equation numbers. This was checked against the [primary manuscript
record](https://arxiv.org/abs/2504.00861).

The revised Klotz 2026 title matches the [primary v2
record](https://arxiv.org/abs/2603.02416v2). Remaining bibliography polish:

- `klotz26`, initial lines 383–385: add journal year 2026 and make the URL
  explicitly end in `2603.02416v2` to agree with its displayed version label.
- `ob12`, initial line 386: add *Geometry of the toroidal N-helix:
  optimal-packing and zero-twist*, verified at the authors' [official DTU
  record](https://orbit.dtu.dk/en/publications/geometry-of-the-toroidal-n-helix-optimal-packing-and-zero-twist/).
- `star06`, initial line 388: add *On the perfect hexagonal packing of rods*,
  verified in the [author repository](https://discovery.ucl.ac.uk/id/eprint/1762/).
- `atkinson19`, initial lines 390–392: optionally complete the publication
  details as New Journal of Physics 21 (2019), 062001,
  [DOI 10.1088/1367-2630/ab1c2d](https://doi.org/10.1088/1367-2630/ab1c2d).
  The existing author names and title match the [primary
  record](https://arxiv.org/abs/1902.06325).

## Bundle checks and initially requested factual edits

The new `publication/reproduce.py`, endpoint checker, pinned input list and
figure files exist. I independently ran the dependency-free endpoint checker
using `.venv/bin/python`: all four input hashes and exact Fraction inequalities
passed. Its source correctly distinguishes checking stored enclosures from
proving their validity. The recorded default reproduction at
`results/publication_reproduction_20260912T223709466785Z` reports three
successful subprocesses, including a fresh N512/H1024 shell certificate with
staggered alpha upper 10.613733558728498… . This review inspected its logs and
scripts; it did not duplicate the full certificate run already covered by the
independent certificate review.

1. Initial lines 308–309 say “every exact rational node.” The radial nodes
   are rational; angular nodes are rational multiples of an enclosed pi.
   Say that explicitly to avoid an inaccurate arithmetic description.
2. Initial lines 348–349 say “Tests and new solver runs are explicit
   additional modes.” The actual `--full` option runs tests, boundary
   certification and finite block search. It does not launch ridgerunner.
   Describe the implemented operations directly.
3. Initial lines 315–318 refer to a completed boundary-certificate review.
   Retain that statement once its independently checked report is present,
   or describe it as pending. The exact-integral theorem and main 10.614
   upper bound do not depend on certification of the displayed diagnostic
   decimal c* and beta values.

These were local factual edits, not failures of the mathematical results,
and were subsequently resolved. Reproducibility was demonstrated in the
existing pinned environment. This source review did not perform a fresh
environment installation or a PDF rendering check; subsequent build work is
reported separately in `BUILD_STATUS.md`.

## Final source closure

The author subsequently corrected all factual and bibliographic items above.
I reread the revised `main.tex`: the angular-node description is accurate,
the reproduction modes match their implementation, all requested titles and
version links are present, and `proofs/BOUNDARY_CERTIFICATE_REVIEW.md` now
records **PASS** for the independent 224-bit, 1024-by-2048 rectangle audit.
Its frozen output is `results/reviewer_boundary_20260913.json`; it also
establishes unambiguous capacity floors for all 1,024 selected shells and
the corresponding component count 4,976,348. I inspected that report and its
machine-readable findings; this is not a claim to have performed a third
independent boundary integration.

The boundary review uses the regenerated certificate dated 22:39:17 UTC;
the publication checker currently pins the earlier 22:23:41 certificate.
Direct JSON comparison found differences only in `experiment_id` and
`runtime_seconds`: all integral and derived rational endpoints agree exactly.
The endpoint checker was rerun successfully. Thus this archival difference
does not leave an arithmetic discrepancy.

**Final verdict: PASS for the local mathematical source and reviewed
contribution scope, with no outstanding source correction from this review.**
The earlier pending-item list is preserved as review history and is closed
by this paragraph. PDF/build review, fresh-environment installation, external
peer review, publication priority and the broader M2 program remain outside
this verdict. Final source and evidence hashes are recorded separately in
`results/reviewer_publication_closure.json`.
