# Tight Knots Lab

Reproducible research on thick knots and links. Thickness means rope **radius**;
ropelength is total component length divided by thickness. Start with
[NORMALIZATION.md](NORMALIZATION.md) and [STATE_OF_THE_ART.md](STATE_OF_THE_ART.md).
The full programme is [RESEARCH_MISSION.md](RESEARCH_MISSION.md).

M1 passed the independent [review](benchmarks/M1_REVIEW.md):27 tests, including
12 independent tests, with actual solver runs and audited proof/certificate paths.
M2 has started with automated phase and finite block-size searches; it is not
yet declared complete.

A mathematical result has passed separate adversarial proof and implementation
reviews: the explicit staggered shell family satisfies

```
limsup_{M→∞} Rop(T(M,M)) / [M(M−1)]^(3/4) < 10.614.
```

See [Theorem002](proofs/THEOREM_002.md),
[geometric review](proofs/ADVERSARIAL_REVIEW_002.md), and
[certificate review](proofs/CERTIFICATE_IMPLEMENTATION_REVIEW.md).
The coefficient is an asymptotic constructive upper bound. It is not a finite-M
bound with the same coefficient, a matching lower bound, or an exact optimum.
Publication novelty is still under audit.

The actual maintained Ridgerunner2.3.1 and tsnnls2.5.1 builds passed4/4 and11/11
upstream tests. Two archived trefoil refinements and a pinned author atlas give
numerical controls. The independent geometry engine estimates polygonal Rawdon
thickness and extracts finite contacts; its smooth root search is explicitly
incomplete and is not a certificate.

Reproduce in the project-local scientific environment:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python experiments/run_controls.py
.venv/bin/python experiments/run_ridgerunner_controls.py
.venv/bin/python experiments/inspect_recent_link.py
.venv/bin/python experiments/certify_shell_bound.py --N 512 --M 1024
.venv/bin/python experiments/run_shell_family.py --T 1 2 4 8 16 --include-staggered
```

Software build instructions and limitations are in
[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md); pinned Python packages are in
[scripts/software/requirements-scientific.txt](scripts/software/requirements-scientific.txt).
Each runner creates a fresh output or refuses overwrite. Earlier failed and
superseded experiments remain archived; consult the latest review and result
index before using a number. No external publication or paid compute is assumed.
