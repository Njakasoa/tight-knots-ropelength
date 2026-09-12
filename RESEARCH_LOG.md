# Research log

## 2026-09-12 UTC — initialization

Created requested laboratory as a nested standalone Git repository because the
outer desktop workspace .git is mounted read-only. Saved full user mission.
Read available local and shared continuity. Started three actual Luna agents.
System Python initially has no scientific dependencies. Sandbox DNS failed;
explicitly authorized public Git download succeeded with reviewed network access.
Scientific principle: no sample-based distance estimate is a thickness certificate.

## 2026-09-12 21:10 UTC — analytic candidate

Derived exact toroidal same-shell squared-distance lower bound and integer
population rule in proofs/TOROIDAL_SHELL_SEPARATION.md. This differs from a
cylindrical approximation: all toroidal point pairs are bounded. The obvious
release is to use each shell's h_i=R-r_i, instead of the outer shell's common h.
Proof candidate includes curvature and same-component DCSD estimates, cross-shell
spacing, two-torus triangle bound and full-twist braid topology route.

Exploratory SciPy quadratures (deterministic, default quad tolerances, no seed)
give q0≈2.732166854279056, l0≈72.8402568726584 and formal doubled
coefficient≈11.405009289871446. These are scratch calculations, not accepted
experiment records or certified bounds. Worker must persist a reproducible run
and tester/reviewer must check the proof. No improvement claim is accepted yet.

An initial ratio R/T sweep (4,4.05,4.1,4.2,4.5,5,6,8) gives formal alpha
(11.4050,11.5061,11.6079,11.8138,12.4471,13.5434,15.8342,20.6089).
This suggests the minimal admissible major-radius ratio 4 within this class;
it is not a monotonicity or optimality proof. M2 remains gated by M1 review.

## 2026-09-12 21:18 UTC — independent review in progress

Astra reviewer independently reports the geometric inequalities hold and
reproduces the candidate integral coefficient. This is interim evidence, not a
completed milestone or novelty decision. The derivative constants for a rigorous
midpoint enclosure were also checked independently. A dedicated certificate
implementation remains required.

Primary PDF downloads succeeded via reviewed network access after the initial
sandbox DNS failure: Klotz 2026 v2, Klotz–Thompson 2025, CKS 2002. Their
URLs, byte counts and SHA-256 hashes are stored in papers/DOWNLOAD_MANIFEST.json.

## 2026-09-12 21:50 UTC — executable controls and adversarial regressions

Maintained tsnnls2.5.1 and Ridgerunner2.3.1 now build with actual local Fortran,
OpenBLAS and LAPACKE; 11/11 and 4/4 upstream tests pass. The POSIX-shell test
harness patch is recorded in the build script. Actual autoscaled trefoil runs
reduce the 47-vertex input to33.14901732 and the 400-vertex input to32.74879268.
A pinned CC0 author atlas supplies six small knots and Hopf coordinates.

Independent testing exposed wrong smooth near-diagonal handling, repeated
non-coprime torus component parameterization, missing zero-distance contacts,
and a circumradius formula substituted for Rawdon MinRad. Root additionally
found an incorrect Alexander numerator and unchecked polynomial remainder.
Worker fixes are under independent regression testing; M1 is not yet PASS.
Both exact shell theorem drafts passed adversarial mathematical reviews; the
interval implementation and novelty still require their distinct reviews.

## 2026-09-12 22:10 UTC — independent certificate PASS; M1 audit fixes

A fresh continuation had actual agent capacity; independent Astra reviewed the
executable certificate, reconstructed the integral at224 bits and checked exact
rational endpoints. The all-integer limsup upper coefficient below10.614 passed.
M1 review found genuine bugs surviving earlier green tests: small-scale and
near-endpoint polygon collisions, absolute projection thresholds, antisymmetric
linking matrix, and16pi instead of8pi in exact Hopf reporting. Root fixed them;
independent reviewer probes now pass. Machin output preserves rational endpoints
and outward decimal bounds. Actual-source hashes replace a descriptive literal
hash in the control manifest. New controls and T44 contact records are indexed
in results/INDEX.md; old failed records remain explicitly historical.

The user withdrew prior AGENTS.md instructions during continuation. The original
research mission, authorized local technical work and active goal remain intact.
No new permission or external contact is needed for these local corrections.
