# Generalizing staggering: all periods and nonuniform spacing

Date: 2026-09-13. Status: explicit derivations and machine-checked finite
examples. This note has not received an independent mathematical referee report.
It extends the existing shell grammar, not the full class of thick links.
Tube radius is one; lengths include every component of both bundles.

## Answer and scope

Yes: phase motifs of every finite period, nonperiodic phase sequences,
nonuniform radial gaps, and even nonuniform angular point sets admit a common
separation test. Generalization does not automatically improve density.

For the saturated equal-population row model underlying Theorem 002, the
optimal mean sufficient radial gap for a closed period p is exactly

    mu_p = sqrt(3)                                  if p is even,
    mu_p = ((p-1)*sqrt(3)+2)/p                       if p is odd.

This allows nonuniform gaps. Even periods attain equality only by repeating
the original period-two alternation. Genuine higher even periods have the
same infimum, approached by small perturbations, but cannot attain it.
Odd periods have one unavoidable phase defect; optimizing its placement
improves on uniform-gap odd motifs but cannot beat period two.

At finite size, the unrounded harmonic separation test has extra slack.
Certified nonuniform radii exploit it and give strict length reductions at
the SAME component count, major radius, populations and phase grids as a
slightly enlarged-major-radius version of the Theorem 002 construction.
The examples below do not prove a smaller leading coefficient than alpha2.

## 1. General finite separation lemma

Keep the component parametrization of Theorem 001:

    F(r,phi;t) = ((R+r cos t) cos(t+phi),
                 (R+r cos t) sin(t+phi), r sin t).

Let r_i>=2 and R>=2 max(r_i)+2. With a=r_i, b=r_j, h_a=R-a,
h_b=R-b, U=ab, V=h_a h_b and K=UV/(U+V), the exact distance identity gives

    |F(a,phi;t)-F(b,psi;s)|²
      >= (a-b)² + 4U sin²((t-s)/2)
                  + 4V sin²((t-s+phi-psi)/2)
      >= (a-b)² + 4K sin²((phi-psi)/2).                  (1)

For the first step, the toroidal cross-section distance is
(a-b)²+4ab sin²((t-s)/2); the remaining cylindrical longitude term has
coefficient (R+a cos t)(R+b cos s)>=h_a h_b. Minimization of the two
sine terms gives 2[S-sqrt(S²-4UV sin²((phi-psi)/2))], S=U+V.
Rationalizing and using sqrt(S²-X)<=S proves the last step.

Consequently, checking the last expression >=4 for every distinct component
pair certifies their separation for ALL parameters, not just sampled points.
The core separation is r_i. The self-reach, embedding and Hopf-doubling
lemmas of Theorem 001 apply unchanged under the displayed radius hypotheses.
Arbitrary distinct cross-section points still make a full twist. The doubled
configuration therefore has type T(M,M), up to common mirror, with reach>=1.

For uniform phase grids with N_i and N_j points and offsets o_i,o_j in TURNS,
their differences form a grid of mesh 1/L, where L=lcm(N_i,N_j). Hence the
smallest phase distance in turns is exactly

    rho_ij = dist(L*(o_i-o_j), Z)/L.                    (2)

Use sin²(pi*rho_ij) in (1). On a single uniform shell, use rho=1/N_i.
All pairs whose radial gap is already >=2 can instead use that exact fact.
This is the verifier implemented in certify_geometry. In particular, it
checks non-neighboring shells when gaps are small.

Equation (2) also exposes a limitation of varying populations. Even the best
relative offset has rho<=1/(2L). To pass (1), necessarily

    (a-b)² >= 4 - 4K*sin²(pi/(2L)).

If neighboring populations are coprime and both of order T, then L is of
order T² while K is of order T² in the scaled interior. The available
angular clearance in this certificate is then O(T^-2): the radial gap must
be at least 2-O(T^-2). Equal populations avoid this arithmetic obstruction.
This is a limitation of uniform phase grids and the chosen sufficient test,
not a universal physical non-overlap theorem.

For arbitrary angular point sets, replace (2) by the minimum circular
distance over the actual two finite phase sets, and check the circular gaps
within each shell as well. The geometric lemma still applies. This note
does not report an optimization over arbitrary angular point sets.

## 2. Arbitrary phases within equal-population blocks

Within a block use the Theorem 002 population

    N = floor(pi*a0*(R-a0)/sqrt(a0²+(R-a0)²))-1 >=3

at its first radius a0. Write phase offsets as 2pi*f_i/N, f_i in R/Z,
and d_i=dist(f_{i+1}-f_i,Z) in [0,1/2]. Monotonicity of K on
a0<=a<=b<R/2 gives K(a,b)>=K(a0,a0). The population lemma gives

    sqrt(K(a0,a0))*sin(pi/N) >=1.

Concavity of sine on [0,pi/N] implies
sin(pi*d_i/N)>=d_i*sin(pi/N). Thus the angular term in (1) is
at least 4*d_i², and the sufficient neighboring gap is

    g(d_i) = 2 sqrt(1-d_i²).                           (3)

This works for every sequence of phases, whether periodic or not. These gaps
are >=sqrt(3), so non-neighbors are radially separated by >2. Keep gap 2
between population blocks. This proves the finite generalization, without
requiring a numerical search.

Equation (3) is a conservative, scale-independent sufficient test. It is not
a necessary finite-torus separation condition. The finite gains in section 5
use (1) directly and therefore do not contradict bounds for (3).

## 3. Exact optimization for EVERY closed period

Let f_p=f_0 modulo one. Select signed increments u_i in [-1/2,1/2]
representing f_{i+1}-f_i; then sum u_i is an integer. Put d_i=|u_i|.

For even p, g(d_i)>=sqrt(3) term by term, with equality only if
d_i=1/2 for every i. Such increments force f_i=f_0+i/2 modulo one,
so the minimizing pattern is period two (which also has every even period).

For odd p, choose signs epsilon_i=+/-1 with u_i=epsilon_i*d_i, allowing
either sign when u_i=0, and set e_i=1/2-d_i. Then

    sum epsilon_i*e_i = (sum epsilon_i)/2 - sum u_i

is a half-integer, so its absolute value is at least 1/2. Therefore
sum e_i>=1/2 and sum d_i<=(p-1)/2. The strictly concave function
g(d)=2sqrt(1-d²) lies above its endpoint chord on [0,1/2]:

    g(d) >= 2 - 2*(2-sqrt(3))*d.

Summing proves

    sum g(d_i) >= (p-1)*sqrt(3)+2.

Equality is attained by f_i=(i mod 2)/2, i=0,...,p-1, followed by
closure to f_0: p-1 half-step edges and one zero-step edge. Strict
concavity also proves these edge magnitudes are necessary for equality.
The resulting phase/gap sequence has genuine minimal period p when p is odd.

If a COMMON radial gap is required, minimize max_i g(d_i) instead. For odd p,
some d_i<=(p-1)/(2p), and equality for every i is realized by the constant
step f_{i+1}-f_i=(p-1)/(2p) modulo one. Thus the best common gap is

    delta_uniform,p = sqrt(4-(1-1/p)²)      (odd p),
    delta_uniform,p = sqrt(3)              (even p).

For odd p>1, this is strictly larger than mu_p. This is a precise sense in
which nonuniform spacing improves an odd-period construction.

| p | Best common gap | Best mean with variable gaps | Minimizing motif |
|---|---:|---:|---|
| 2 | 1.732051 | 1.732051 | 0, 1/2 |
| 3 | 1.885618 | 1.821367 | 0, 1/2, 0; closing gap 2 |
| 4 | 1.732051 | 1.732051 | repeated period 2 |
| 5 | 1.833030 | 1.785641 | four half-step edges, one defect |
| 6 | 1.732051 | 1.732051 | repeated period 2 |
| 7 | 1.807016 | 1.770329 | six half-step edges, one defect |

Displayed decimals are diagnostics, not rigorous rounded bounds.
In particular a true period-four example 0,1/4,1/2,3/4 has common gap
sqrt(15)/2≈1.936492 and is feasible, but less compact. Small nonzero
perturbations of the alternating four-term pattern approach sqrt(3).

## 4. Passage back to the asymptotic shell family

Fix p and a periodic phase/gap motif satisfying (3), with mean gap mu.
Let the population blocks have size floor(sqrt(T)), with boundary gap 2.
The first radius is 2. Within a block the discrepancy between a partial sum
of gaps and mu times its length is O(p); there are O(sqrt(T)) blocks.
Consequently r_i=mu*i+O_p(sqrt(T)) and R=2mu*T+O_p(sqrt(T)).
Population lag inside a block is O(sqrt(T)). The same bounded-derivative
Riemann-sum argument as Theorem 002 yields

    Q(T)=(mu/2)*q0*T²+O_p(T^(3/2)),
    L_bundle(T)=(mu²/4)*l0*T³+O_p(T^(5/2)),
    alpha(mu)=sqrt(mu/2)*alpha1.

The least-index/deletion argument of Theorem 002 again yields the all-integer
limsup upper bound. Thus optimized fixed odd periods have the WORSE
constructed coefficient sqrt(mu_p/sqrt(3))*alpha2; even periods reproduce
alpha2. For arbitrary nonperiodic sequences satisfying (3), every gap is
>=sqrt(3); they cannot improve the mean gap by this test. These observations
do not prove optimality among different radial density profiles or other
geometric grammars, or cover p growing with T without additional error control.

Changing uniform angular spacing or allowing arbitrary point arrangements
leads to a broader packing problem. In a frozen planar unit-disk packing,
the classical density bound is pi/sqrt(12), so nonuniformity alone cannot
exceed triangular packing density. This planar theorem is relevant context,
NOT a proof of a global obstruction for curved toroidal links.

## 5. Certified finite nonuniform radii at fixed M

The reproducible experiment starts from Theorem 002 radii r_i and blocks
b=floor(sqrt(T)), and chooses an exact rational R just above 2*r_T+2
(less than 1.2e-7 above, checked by Arb). BOTH comparison geometries use
this same R. Their integer populations come from its certified baseline
block capacities. The first shell remains at radius 2.

A greedy search moves each subsequent shell inward while enforcing its own
harmonic same-shell clearance, previous-shell harmonic clearance, gaps at
least 1.000001 inside blocks and 2 between blocks. Root results are rounded
up and padded as exact rationals. This search is only a proposal generator.
The independent-from-search Arb code reconstructs those rationals and checks
every shell pair, the baseline population floors, closure, and strict radius
compression. This is one codebase with separate numerical and verification
paths, not an independent referee or independently implemented verifier.

The analytic length function is

    ell(R,r)=integral_0^(2pi) sqrt((R+r cos t)²+r²) dt.

It is even in r by t -> t+pi. Its second derivative in r has integrand
R²/[(R+r cos t)²+r²]^(3/2)>0. Hence it is strictly increasing for r>0.
All radii except the first shrink strictly, so the total length decreases
strictly at the same R and M. Additionally, midpoint quadrature with an
explicit second-derivative error bound encloses both full lengths and their
difference with Arb. This supplies quantitative intervals, not sampled-length
estimates. Normalization uses [M(M-1)]^(3/4), unchanged in each comparison.

The canonical output is
`results/staggering_generalization_20260913/investigation.json`.
It contains exact rational inputs and outward endpoints, 21 finite periodic
examples, grid searches for periods 1 through 16, and five fixed-M comparisons.
The finite periodic examples include genuine periods 3,4,5,... via the
equally-spaced phase pattern as well as optimized and constant-step patterns.

Approximate length reductions, relative to that fixed-M baseline:

| Shells T | Components M | Reduction |
|---:|---:|---:|
| 9 | 356 | 0.76707% |
| 16 | 1,114 | 0.37470% |
| 36 | 5,678 | 0.20308% |
| 64 | 18,162 | 0.12839% |
| 128 | 73,986 | 0.06950% |

These are improvements to explicit upper-bound constructions, not proven
reductions of the unknown minimal ropelength. They are not comparisons to
every optimized block size or to Ridgerunner minima. R is fixed, not jointly
optimized. Gaps close to 1 occur in underpopulated parts of a block, followed
by larger gaps as the next population increases. The smaller finite gains
observed with growing T do not by themselves establish any asymptotic law.

## 6. Reproduction, falsification, and remaining questions

From the lab root:

```
.venv/bin/python experiments/generalize_staggering.py --angular-cells 4096
.venv/bin/python experiments/replay_staggering_generalization.py
.venv/bin/python -m pytest -q
```

The phase-grid dynamic program optimizes closed cycles without a prescribed
half-step target. It agrees with the all-real-phase theorem for p=1,...,16.
That numerical agreement supports but does not replace section 3's proof.
Tests compare its output to exhaustive enumeration, compare LCM phase
reduction to explicit component enumeration, check real toroidal sampled
distances against (1), and compare interval lengths to separate adaptive
quadrature. Deliberate collisions between non-neighboring shells and tampered
phases, radii, populations, closure and dimensions must be rejected.

Promising extensions are optimization at fixed M with varying populations,
nonuniform block schedules, and joint R/radius optimization, followed by the
same all-pairs certificate. Improving the true leading constant requires a
new argument beyond the solved fixed-period saturated-row optimization.

## Sources and attribution

The proof infrastructure and inherited topology are in Theorems 001 and 002;
the bounded novelty audit is `references/FOCUSED_NOVELTY_AUDIT.md`.
No new literature-priority claim is made for this extension.

- [Klotz, Tight Bounds for Tight Links (2026), arXiv:2603.02416v2](https://arxiv.org/abs/2603.02416v2),
  [published version](https://doi.org/10.1088/1751-8121/ae862e): prior toroidal
  shell and doubled-bundle constructions. The present phase extension is
  derived from this lab's reviewed separation lemma.
- [Chang and Wang, A Simple Proof of Thue's Theorem on Circle Packing](https://arxiv.org/abs/1009.4322):
  planar disk-density context, not a curved-link optimality theorem.
- [Connelly and Dickinson, Periodic Planar Disk Packings](https://arxiv.org/abs/1201.5965):
  periodic packing and jamming context. Periodic motifs and triangular packing
  should not be presented as new general concepts.
