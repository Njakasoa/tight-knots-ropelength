# Adversarial review of the refinement topology certificate

Date: 13 September 2026. Reviewer: delegated Astra adversarial reviewer.
Scope: sampling argument, `experiments/certify_refinement_topology.py`,
canonical witnesses and independent replay. **PASS for the mathematical
argument and the three certified initial/final endpoint link types.** The
source issues found during review have been corrected. Historical stages are
retained below; the final closure identifies the current evidence.

## Mathematical method: PASS

The method can establish the topology of the stored initial and final
polygons by an explicit alternative isotopy. It does not certify the actual
ridgerunner time history, smooth reach, a ropelength upper bound, criticality
or optimality.

### Smooth curve to exact stored polygon

Undo the positive ambient diagonal map and, for the second bundle, the proper
Hopf rigid motion in the correct reverse order. Direct exact-decimal VECT
parsing and Arb evaluation establish that each resulting stored vertex is
within epsilon of the exact analytic curve at u_k=2pi k/n. The JSON parameters
are interpreted as the exact rationals represented by their binary64 values;
mathematical pi is used in the analytic curve. This convention is legitimate
because the actual coordinate discrepancy is separately bounded.

Let r be the component radius, h=R−r, L=1+|beta| and

    B = R+r+2rL+r(L²+|beta|).

Writing the curve as rho(u)e_r(u)+z(u)e_z, the radial rotation terms in its
second derivative have total norm at most R+r+2rL, and the remaining
normal-disk derivative norm is at most r(L²+|beta|). Thus B bounds |F''|.
The linear chord error is at most eta=B(Delta u)²/8+epsilon, including the
closing segment.

The map (x,y,z)→(sqrt(x²+y²)−R,z) is 1-Lipschitz. If h>eta, integrating
the angular derivative along the straight segment from F(u) to the polygon
point bounds angular drift by eta/(h−eta). Since the analytic normal-disk
point is rL-Lipschitz in longitude, its difference from the polygon's
normal-disk point at that polygon point's actual longitude is at most

    e = eta + rL eta/(h−eta).

At vertices the sharper drift epsilon/(h−epsilon) shows that lifted successive
angular increments lie in (0,pi), using the script's two strict inequalities.
Consequently the polygon longitude is a homeomorphism of circles: each chord
has strictly increasing angle and the total winding is one. The fiber
interpolation from its normal-disk graph to the analytic graph is well-defined.

At any longitude, reference components are separated by at least r_i from
the core, |r_i−r_j| on distinct shells, and 2r_i sin(pi/N_i) within a shell.
If e_i+e_j is strictly smaller than that separation, the fiber interpolation
never collides. The conservative 2 max(e_i) condition used by the script is
sufficient. R>2(rmax+max(e_i)) keeps the two enlarged core tubes disjoint
throughout this interpolation. Positive ambient scaling then transports the
isotopy back to the stored polygon.

### Stored initial polygon to stored final polygon

A positive homothety and translation of the initial polygon is explicitly
isotopic to identity. Their coefficients are frozen as exact binary rationals.
No general linear interpolation through potentially singular matrices is used.
Every aligned vertex then moves linearly to its corresponding final vertex.

For each pair of nonadjacent edges and each certified time interval, a fixed
exact rational axis strictly separates the projections of their endpoint/time
corners. A moving edge point is bilinear in time and its segment parameter,
so its axis projection lies in the convex hull of the four corner projections.
This excludes every intersection of that pair during the whole time interval.
The enumeration includes every intercomponent pair and all cyclic
nonadjacent pairs within a component.

Adjacent edges share their prescribed vertex. Their oriented cross product,
dotted with a fixed axis, is quadratic in time. The script evaluates its two
endpoints and midpoint and uses the correct quadratic Bernstein middle
coefficient 2f_mid−(f_0+f_1)/2. Strict positivity of all three coefficients
excludes both edge collapse and adjacent foldback throughout the interval.

The exact rational time-coverage check verifies contiguous coverage of [0,1]
for every required pair and corner. The resulting continuous family consists
entirely of embedded tame polygons, so isotopy extension gives an ambient
isotopy. Thus the final polygon has the reviewed analytic full-twist type
T(12,12), up to a common mirror, without classifying it from linking numbers.

## Implementation findings before certificate freeze

The major logical checks implement the preceding sufficient proof. Float
optimization supplies axes only; exact rational/Arb checks decide acceptance.
Direct VECT decimal parsing avoids proving a claim about rounded replacement
vertices. The initial code had two small issues communicated to the root:

1. `max(bounds,key=float)` could select a smaller rigorous upper endpoint when
   distinct endpoints have the same float conversion. Use exact endpoint
   comparison or a rigorous hull for the maximum.
2. An empty or nonexistent requested seed list could yield a vacuous summary
   `PASS`. Require nonempty selected records and account for every explicitly
   requested seed.

The initial seed-1729 artifact contains 165,024 required edge pairs, one time
cell for each pair, and 576 certified adjacent corners. Its stated sampling
error upper is approximately 0.06062314 and its enlarged double-tube gap is
approximately 0.14436585. These are promising artifact checks, not by
themselves a final implementation/replay verdict for all three seeds.

## Initial evidence status (historical)

Pending the two small source fixes, complete certificates for the selected
three seeds, the formal proof note, and the independent witness replay.
The mathematical method PASS above must not be mistaken for completed
three-output certification. Final closure should be appended with hashes and
the precise independently replayed claim.

## Source and canonical artifact update

The two reported code issues are corrected: rigorous upper endpoints are
compared directly, and empty/unknown seed selections are rejected. Witness
index and time-depth columns now also require integral entries and the
declared finite depth range. I reread the full formal note
`REFINEMENT_TOPOLOGY_CERTIFICATE.md`; it agrees with the independent
derivation above and explicitly limits its conclusion to endpoint link type.

The canonical run is `results/topology_path_20260912T230219109163Z`, with
certificates for all three seeds 1729, 2718 and 3141. Each contains 165,024
required edge-pair time cells and 576 adjacent-corner cells. Every successful
time cell spans [0,1]; subdivision was not needed for these geometries.
I independently checked each initial/final coordinate hash, witness hash and
certificate script hash against the actual files. They all match the current
script SHA-256
`ba207ced6d2c2f2f103e8ce671759f85e6fbc8c626cd9b20fa5a58789afa1a53`.
The separate artifact audit is `results/reviewer_refinement_artifact_hashes.json`.

**Mathematical argument and implementation inspection: PASS.** The later
independent replay and hardening described below close the initial pending
evidence item.

## Final independent replay and implementation closure

The validation worker's independent audit in
`results/reviewer_refinement_20260913.json` recomputed the analytic sampling
bridge for every seed, including exact stored-decimal parsing, actual vertex
error, longitude margins, fiber separation and disjoint enlarged core tubes.
It independently checked all witness index coverage and exact dyadic time
partitions. Corrupt-witness tests rejected missing pair/corner entries,
invalid time cells, nonintegral indices and a zero separating axis under
normal execution.

That audit found a real checker invocation problem: Python `-O` removes
assertions and could bypass checks. The source now rejects optimized mode
explicitly before imports. It also rejects unexpected trailing VECT tokens.
I inspected both fixes and verified the optimized-mode rejection directly;
the evidence is in `results/reviewer_refinement_final_replay.json`. The
certifying inequalities themselves were unchanged.

My independent exact-Fraction implementation checks every pair/corner index
and deterministically samples 97 pair inequalities plus 41 corner Bernstein
inequalities per seed, all successfully. That supporting check is
`results/reviewer_refinement_fraction_spotcheck.py` and its JSON output;
its scope is explicitly a spot check, not a substitute for complete replay.
I additionally ran the actual checker over every inequality for all three
seeds, obtaining `REPLAY_PASS` for each with exit code zero.

The source frozen for final replay has SHA-256
`0b16a0f951bcad2a0c00b012434181909c268cae399460a4856ef376e287c14a`.
The canonical hardened bundle is
`results/topology_path_20260912T231158562188Z`; the earlier 23:02:19 bundle is
valid historical evidence. The final replay and per-artifact hashes are
recorded in `results/reviewer_refinement_final_replay_v2.json`.

**Final verdict: PASS.** All three stored initial and final polygons have the
analytic T(12,12) type up to a common mirror, proved through an explicit
alternative isotopy. The actual ridgerunner history, continuous thickness,
smooth ropelength upper bounds and optimality remain outside this theorem.
