# CLAIM-0003 — Optimal first block correction in a fixed grammar

**Exact statement:** In the staggered construction with arbitrary block size b, F(T,b)=Ltotal/[M(M−1)]^(3/4)=α2[1+a/b+d b/T+O(b^(-2)+(b/T)^2+T^(-1))] as b→∞, b/T→0. Here a=1/√3−1/2 and d=3n(1)/(4q0)−J/(2l0), J=∫n'e. Among b=floor(c√T) with fixed c>0, the first correction is uniquely minimized at c*=√(a/d). Analytically d>a>0, so c*<1 and the correction is strictly better than c=1.
**Knot/link family:** Explicit T(M(T,b),M(T,b)) sequences; M varies with both T and b.
**Ropelength convention:** Tube radius; total length; construction value, not the ropelength infimum.
**Proof level:** Exact analytic theorem passed independent Astra review; independent boundary interval implementation review is separately tracked in proofs/BOUNDARY_CERTIFICATE_REVIEW.md when available.
**Numerical evidence:** Exhaustive b=1..T search at T=8..1024 selected b=(1,2,2,4,5,7,9,13), without hardcoding a power-law target. Diagnostic c*≈0.4227848052 and optimal correction≈3.8835903551, versus≈5.4138303824 at c=1.
**Topology verification:** Arbitrary-b construction inherits the reviewed full twist and deletion-free sequence topology.
**Thickness verification:** All blocks retain the same proven gaps and phase inequalities; b need not equal floor(√T).
**Counterexample search:** Independent reconstruction at T through 65539, c=.2,c*,1,2 and powers .25,.4,.6,.75; incomplete blocks and rounding explicitly stressed. The tests support but do not prove the analytic remainder.
**Closest literature:** Same shell sources as CLAIM-0002; focused boundary audit in references/BOUNDARY_NOVELTY_AUDIT.md when available. Balancing reciprocal and linear errors is a standard method, not itself a novelty claim.
**Independent derivation:** proofs/ADVERSARIAL_REVIEW_003.md independently derives both coefficients, lag averages, incomplete-block errors, radius offsets and quotient normalization.
**Novelty status:** Exact theorem mathematically reviewed; POSSIBLY NOVEL, provisional, as a geometry-specific contribution.
**Open objections:** No exact finite-T argmin theorem, no comparison at equal M, no arbitrary-block-schedule optimum and no all-M subleading improvement after deletion. No global ropelength optimality or publication priority claim.
