# Initial parameter searches before M1 review

The bounded SciPy differential-evolution runs in
`results/torus_search_20260912T214900Z/search.json` vary major/minor radius ratio
and positive vertical stretch, with fixed primitive torus windings. Seeds1729
and2718, 96 samples/component during search, 192/384 at final checks; all
trial values and both final geometries per family are stored. Objective is
actual plCurve/octrope polygonal ropelength. No result is a smooth certificate.

| Family | Best retained 384-point value | Interpretation |
|---|---:|---|
| T(2,3) |34.321366|Above the sourced approximately tight trefoil32.743665; restricted family is limiting.|
| T(2,5) |49.638498|Parameter search only; compare sourced5_1 reference separately.|
| T(3,4) |64.948891|Vertical stretch near1.25 in both runs; an observation, not an exact ratio or optimum.|
| T(2,2) |28.429300|Above round Hopf8π≈25.132741; standard torus geometry misses the known optimum.|

Mesh errors have different signs across the families. Coarse sampled objectives
must not be used as smooth upper bounds. Fixed-radius scaling is removed because
ropelength is scale invariant. R>1 and positive vertical stretch preserve the
analytic torus type; the polygons still need independent projection checks.
The 14-generation stopping limits were reached, so these are bounded searches,
not convergence proofs. M2's required autonomous structural discovery remains
pending the M1 gate; this file records the user's requested initial experiments.
