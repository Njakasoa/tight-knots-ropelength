# CLAIM-0001 — Shell-specific toroidal separation

**Exact statement:** The inequality (S) and integer population rule in
proofs/TOROIDAL_SHELL_SEPARATION.md suffice for intercomponent clearance 2;
R>=2r+2, r>=2 also suffice for each component's unit self-thickness.
**Family:** Concentric p=1 toroidal helices, potential doubled T(Q,Q) family.
**Convention:** Radius thickness, total component length.
**Proof level:** Level 4 analytic proof with independent Astra review PASS. Canonical statement: proofs/THEOREM_001.md. Level 5 awaits independent implementation/testing.
**Numerical evidence:** Exploratory SciPy quadrature alpha_double≈11.40500929.
This decimal is not yet a certified ropelength bound.
**Topology verification:** PASS in proofs/ADVERSARIAL_REVIEW_001.md, via zero-framed cluster full-rotation factorization, beyond pairwise linking.
**Thickness verification:** Analytic argument independently reviewed PASS; executable checks pending.
**Counterexample search:** Reviewer independently stress-tested same-shell distances through T=100; independent implementation tester pending.
**Closest literature:** Klotz 2026 arXiv:2603.02416; Klotz–Thompson 2025
arXiv:2504.00861. Need latest-version and novelty audit.
**Independent derivation:** Exact toroidal distance identity, harmonic minimization,
sine concavity, Taylor remainder, and shell-specific inner radius.
**Novelty status:** POSSIBLY NOVEL, provisional and unaudited; not VERIFIED RESULT.
**Open objections:** Integral arithmetic certificate; independent implementation/test; prior art; comparison to rigorous vs conditional upper bounds. Analytic topology, thickness and all-Q limsup passed independent review.
