# Certificate implementation review

Date: 2026-09-13. Reviewer: independent delegated Astra reviewer. Scope is the
implementation and stored arithmetic evidence, assuming the proposed certificate
could be false. This review did not edit production code or re-audit novelty.

## Verdict

**PASS for the shell integral certificate and its linkage to Theorems 001/002.**
The stored certificate at `results/certificate_shell_N512M1024_noguard` establishes
`alpha2 < 10.614`. Together with the independently reviewed geometric and
all-integer limiting arguments in Theorem 002, it gives

```
limsup_(M -> infinity) Rop(T(M,M)) / [M(M-1)]^(3/4) <= alpha2 < 10.614.
```

This is a radius-normalized constructive upper bound. It is not a finite-M
bound with coefficient 10.614, a matching lower bound, an equality for the
class infimum, a global optimum, or a novelty determination. Passing this
certificate does not automatically pass the independent M1 geometry gate.

## Arithmetic audit

The reviewed run uses N=512, M=1024 and 192-bit Arb arithmetic. Its source
hashes, output hash and detached manifest hash all matched the files inspected.
The dirty Git flag is disclosed; exact source hashes identify the arithmetic
implementation beyond that commit. The 53-bit context recorded after the run
is the restored global context, not the precision used during certification.

I inspected `src/certification/arb_backend.py`, `integrals.py`, `shell_family.py`,
`provenance.py`, and `experiments/certify_shell_bound.py`. Midpoint nodes are
formed from integer Arb operands; pi, cosine, roots, weights, error and quotient
remain enclosed. The analytic error is added using an outward upper radius.
The positive denominator is checked. Authoritative endpoints are serialized as
exact rational pairs; the human decimal is not used to establish the threshold.
No unexplained floating epsilon remains in this path.

The code evaluates precisely the n, q0, l0 and alpha1 expressions in Theorem 001,
then multiplies alpha1 by the enclosed positive factor sqrt(sqrt(3)/2) specified
in Theorem 002. Review 001 §5 independently proves the derivative bounds 600
and 60 and the tensor-midpoint error without a missing mixed derivative term.
The derivative bounds apply on the full integration domain including x=0.
The optional rescaling field is therefore more than multiplication of a rounded
exploratory number.

I independently implemented the tensor sum with angular index outermost,
cached density values, and 224-bit precision, importing no production certificate
helpers. The resulting q0, l0, alpha1 and alpha2 intervals overlap the stored
intervals. Both the independent Arb inequality and a Python Fraction comparison
of the stored alpha2 upper endpoint prove the strict 10.614 threshold. Stored
upper decimal: approximately 10.613733558728. Full exact evidence and a runnable
independent script are `results/reviewer_certificate_check.json` and
`results/reviewer_certificate_check.py`. Reproduce from the lab directory with
`.venv/bin/python results/reviewer_certificate_check.py`.

Overlap alone would not certify a result; here the proof follows from the
independently checked analytic error and enclosing arithmetic. The second
implementation is a falsification/reproduction check of that chain.

## Finite generator and theorem linkage

The finite shell generator uses Arb-certified capacity floors and subtracts one,
matching the sufficient population rule. In the staggered generator,
`math.isqrt(T)` is exact, the radius expression has sqrt(3) internal gaps and
two-unit block gaps, each block uses its innermost capacity, and phase offsets
alternate zero and pi/N. Major radius is twice outer radius plus two. Finite
length integration uses the correct phase-independent speed and an enclosing
midpoint error. The doubled total length and component count use the same factor
two, and the diagnostic export uses the proper rotation P(x,y,z)=(R+x,-z,y).

The proof is attached to these explicit analytic curves. Floating sampled
coordinates are correctly labeled diagnostic. A certificate for their polygonal
interpolants is neither implied nor required for this analytic construction.
Full-twist topology, self-thickness, all-pair separation, block asymptotics and
component-deletion interpolation are supplied by Theorems 001/002 and reviews
001/002; the finite output count is not mistaken for proof over every integer M.

## Separate findings

The M1 audit identified errors in the ordinary floating polygon/topology checker
and the exact Hopf-control reporting helper. Those routines are not imported by
the shell integral certificate and do not invalidate its independent proof chain.
Their resolution and the full M1 verdict are recorded in `benchmarks/M1_REVIEW.md`.
The source derivation note still contains historical wording that certain now
reviewed obligations are pending; the final theorem/review documents govern the
status. Keeping that history clearly labeled would improve readability.
