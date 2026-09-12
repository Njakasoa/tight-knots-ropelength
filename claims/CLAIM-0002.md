# CLAIM-0002 — Staggered shell blocks

**Exact statement:** Equal-population blocks with alternating phases allow √3 radial gaps, with gap 2 at block boundaries. The doubled family proves limsup Rop(T(M,M))/[M(M−1)]^(3/4) ≤ α2=√(√3/2) α1<10.614.
**Knot/link family:** T(M,M) for all integers M→∞, via component deletion from the next qualifying full construction.
**Ropelength convention:** Tube radius; total component length.
**Proof level:** Level 5: exact geometry and limiting proof reviewed independently; Arb endpoint and independent finite implementation reviewed PASS.
**Numerical evidence:** α2≈10.6135570633 is diagnostic. Accepted interval upper endpoint 10.613733558728498 is below 10.614; use stored rational endpoints for exact comparisons.
**Topology verification:** Inherited zero-framed full-twist proof applies to arbitrary fixed distinct cross-section points; see proofs/ADVERSARIAL_REVIEW_002.md.
**Thickness verification:** Cross-shell harmonic inequality supplies >1 squared transverse clearance for adjacent equal-N shells, added to radial squared gap 3. Nonadjacent shells, block boundaries, cores and doubled bundles are separately covered; curvature/DCSD inherited.
**Counterexample search:** Independent finite tests through T=1024 and certificate checks; benchmarks/M1_REVIEW.md and proofs/CERTIFICATE_IMPLEMENTATION_REVIEW.md.
**Closest literature:** Klotz 2026 shell constructions; older equal-population and hexagonal/toroidal packing. Exact comparisons in references/FOCUSED_NOVELTY_AUDIT.md.
**Independent derivation:** Astra separation and full-twist derivation plus independent 224-bit coefficient computation; no reliance on a sampled minimum as a proof.
**Novelty status:** VERIFIED RESULT mathematically; POSSIBLY NOVEL, provisional, for publication novelty.
**Open objections:** No proof of publication priority, global/family optimum, matching lower bound or universal best constant. Published finite coefficient near 10.02 concerns a different family/scope. Numerical T44 reference-table discrepancy is explicitly unresolved and is not used in this proof.
