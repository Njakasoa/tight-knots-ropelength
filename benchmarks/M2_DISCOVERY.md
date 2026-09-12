# M2 discovery evidence and scope

M1 passed before these searches. This record supplies evidence for independent
M2 review; it does not substitute for that review.

## Supported parameter space

| Required dimension | Implemented variation | Mathematical scope |
|---|---|---|
| Family | Standard T(p,q) generator; single full-twist shell bundle; doubled Hopf-core bundle | Standard torus construction or reviewed smooth full-twist isotopy, up to common mirror |
| Q / component count | Integer shell populations and optional core; doubled or single closure | Count explicit; arbitrary prescribed Q can be composed from populations |
| Number of shells | Arbitrary finite distinct positive radii | Checked configuration constraints |
| Shell populations | Independent positive integers; certified block-capacity rule is a subset | General populations require a fresh thickness calculation |
| Pitch | Independent periodic beta_i sin(u) modulation | One total meridional turn; no nonintegral winding/endpoint mismatch |
| Radii | Independent shell radii and major radius | R>rmax for one bundle, R>2rmax for double |
| Phase | Independent shell offsets; continuous pair search | Equal angular spacing within a shell is retained |
| Closure geometry | Single circular torus or orthogonal round Hopf doubling; positive ambient scaling | Other closure shapes are unsupported |
| Symmetry | Shell populations/phases and positive independent ambient axis scaling | Does not cover arbitrary nonsymmetric infinite-dimensional curves |

Implementation: src/discovery/grammar.py. The topology proof and independent
review are proofs/VARIABLE_PITCH_TOPOLOGY.md and its REVIEW. The smooth isotopy
proof is separate from reach certification. The three final polygons now have separate endpoint topology certificates.
Ridgerunner's actual trajectory and thickness values remain numerical.

## Required initial experiments

| Experiment | Evidence | Outcome / limit |
|---|---|---|
| A: reproduce recent construction | results/recent_T44_20260912T220613Z; results/klotz_limits_20260912T221239Z | Actual T44 coordinates agree with plCurve at77.97687288; companion77.47 remains discrepant. Continuum13.3776/11.68595 integrals reproduced numerically. |
| B: release pitch/radius per shell | results/variable_pitch_20260912T224501767133Z | Two independent periodic pitch modes, shell radius, major radius, relative phase and ambient stretch searched with3 DE seeds; full histories retained. |
| C: boundary block packing | results/discovery_blocks_20260912T221841Z; Theorem003 | Exhaustive all integerb=1..T revealed smaller preferred blocks; analytic first correction explains the prefactor. |
| D: multistart unrestricted refinement | Same variable-pitch directory, three .rr subdirectories | Each independently optimized start passed to300 steps of actual Ridgerunner, releasing vertex positions. Endpoint types are separately certified by an explicit alternative isotopy; the actual solver trajectory is not certified. |
| E: contact comparison/clustering | results/contact_clusters_20260912T224627301208Z | Two tolerance levels, full contacts, permutation-invariant component spectra and exploratory clustering. No continuum phase claim. |

For the three seeds1729/2718/3141, 48-point-per-component starting polygons
had ropelength726.402599/730.547841/755.884021 and final Ridgerunner values
702.797075/716.108417/746.879334. The independent thickness engine agrees
with plCurve to relative error below5e-16. Two generic projections of each
final configuration give absolute linking number1 for all66 component pairs.
These projection data are consistency checks. The subsequent certificate in
results/topology_path_20260912T231158562188Z proves the complete endpoint type
via analytic-to-polygon sampling bounds and an explicit alternative PL isotopy.
Each seed covers all165024 nonadjacent edge pairs and576 corners. This is not
an assertion about the actual Ridgerunner trajectory or its thickness.
All starts, intermediate solver outputs, stopping reasons and final geometries
are preserved. The bounded runs do not establish converged local minima.

At relative contact tolerances1e-4 and1e-3, the three contact counts are
(31,31,41) and(35,72,56). Spectral clustering at the declared cut.1 separates
all three at both tolerances. Seeds2718 and3141 are closer to each other in
that feature space. Three finite samples do not prove a contact phase transition.

## Structural observation not supplied to the search

The exhaustive block search enumerated every b=1..T for T=8..1024. It was
not given a power law, target exponent or preferred multiplier. Winners were
1,2,2,4,5,7,9,13. AtT1024, b13 improves the normalized construction value
relative to the initially chosen b32. The data suggested a smaller multiplier;
it did not establish an asymptotic exponent (a finite fit gave~.425).

The subsequent independently reviewed derivation proves

    F(T,b)=alpha2[1+a/b+d*b/T+O(b^-2+(b/T)^2+T^-1)],
    c*=sqrt(a/d)≈.4227848052 for b=floor(c*sqrtT).

This is the pattern-to-proof route. All1024 capacity floors of the selected
T1024,b13 configuration are independently certified. Neither a finite optimum
nor an equal-M improvement is claimed. The exact geometry-specific coefficients
are possibly novel; square-root reciprocal/linear balancing already occurs in
the nearest2025 paper and receives no novelty claim.

A separate 16-case phase/gap search over all f∈[0,1] found f≈1/2 without
hardcoding it into seeds or objective targets. Its grid cross-check and Arb
finite-pair certificates pass; the large-population gaps approach sqrt3.
This rediscovers a known geometric staggering principle and is useful engine
validation. Pair feasibility is not a certificate for an entire bundle.

## Post-M1 integration correction

The atlas extension exposed a VECT reader bug: zero total colors still require
one color-count entry per component. The reader now consumes that row and two
new regressions cover canonical multi-component zero-color input and malformed
counts. The old M1 snapshot remains historical; final independent testing must
include this correction and the M2 additions.
