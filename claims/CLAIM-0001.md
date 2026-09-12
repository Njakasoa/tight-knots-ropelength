# CLAIM-0001 — Shell-specific toroidal separation

**Exact statement:** The explicit doubled shell family of proofs/THEOREM_001.md proves limsup Rop(T(M,M))/[M(M−1)]^(3/4) ≤ α1, where α1=l0/(√2 q0^(3/2)) is defined there. The audited interval calculation gives α1<11.406.
**Knot/link family:** All integer M→∞, full-twist T(M,M), up to a common mirror.
**Ropelength convention:** Tube radius; total length of all components.
**Proof level:** Level 5: independently reviewed analytic construction and independent implementation/certificate review.
**Numerical evidence:** α1≈11.4050092899 is diagnostic; the accepted outward upper endpoint is 11.40519894659519 (see certificate rational endpoints for exact comparisons). Finite generators include certified capacity floors and interval lengths.
**Topology verification:** Zero-framed configuration-space full rotation; matching internal/mutual signs in Hopf doubling; deleting strands preserves full twist. Pairwise linking alone is not the proof.
**Thickness verification:** Exact harmonic separation bound, curvature ≤11/16 and self-critical chords ≥80/33; all cross-bundle distances ≥2.
**Counterexample search:** Independent all-pair numerical attacks and finite checks; see proofs/ADVERSARIAL_REVIEW_001.md, proofs/CERTIFICATE_IMPLEMENTATION_REVIEW.md and benchmarks/M1_REVIEW.md.
**Closest literature:** Klotz 2026, DOI 10.1088/1751-8121/ae862e; Klotz–Thompson 2025, DOI 10.1098/rspa.2025.0319. Toroidal shells and doubling are prior art.
**Independent derivation:** Independent Astra analytic derivation and separate 224-bit integral implementation in results/reviewer_certificate_check.py.
**Novelty status:** VERIFIED RESULT mathematically; POSSIBLY NOVEL, provisional, as a publication contribution. See references/FOCUSED_NOVELTY_AUDIT.md.
**Open objections:** Bounded novelty audit cannot establish priority. This is an asymptotic constructive upper bound, not a finite-M bound with the same constant, an optimum, or a universal lower bound.
