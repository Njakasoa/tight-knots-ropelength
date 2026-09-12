# Independent adversarial review 002 — staggered blocks

Date: 2026-09-13. Reviewer: delegated Astra mathematical reviewer.

Scope: `STAGGERED_BLOCKS_CANDIDATE.md`, `CLAIM-0002.md`, the inherited
lemmas reviewed in `ADVERSARIAL_REVIEW_001.md`, and the optional algebra
check in `WEGNER_EXPANSION_AUDIT.md`. No source proofs or construction
implementation were edited. No broad novelty search was performed.

## Verdict

**PASS for the mathematical construction and exact integral limsup upper
bound**, after incorporating the explicit indexing, uniform estimates,
and all-integer argument supplied here. No counterexample was found.
The source's outstanding uniformity and nonmonotonic-population questions
can be closed analytically; they are not intrinsic blockers.

**CONDITIONAL for a numerical upper endpoint and implementation.** A
rigorous ball-arithmetic enclosure of the rescaled constant and a tested
finite generator remain separate obligations. The proposed decimal is
consistent with independent calculations, but is an approximation rather
than an outward inequality. **Novelty remains unassessed/provisional.**
This is not a global optimum or a lower bound.

| Obligation | Verdict | Reason |
|---|---|---|
| Exact cross-shell harmonic inequality | PASS | Valid for all parameter pairs |
| Monotonicity of K in the admissible range | PASS | Both radii lie strictly below R/2 |
| Half-phase sine estimate and integer rounding | PASS | Gives a strict excess over one |
| All strand-pair phase differences | PASS | Equal N gives an odd half-grid across neighbors |
| All component pairs, including boundaries/core | PASS | Adjacent pairs use the staggered bound; others use radial clearance |
| Inherited self-thickness and doubled clearance | PASS | R=2r_outer+2 satisfies their exact hypotheses |
| Inherited full-twist topology | PASS | Phases and population changes preserve the configuration-space proof |
| Block loss and limiting coefficient | PASS | Uniform estimates below give explicit error orders |
| All-integer interpolation without monotonicity | PASS | First passage to a larger population suffices |
| Certified decimal and tested implementation | CONDITIONAL | Not inspected in this review |
| Publication novelty / best known status | NOT ESTABLISHED | Outside this bounded review |
| Wegner expansion correction | PASS | B=7.167125130743448… |

## 1. Exact cross-shell separation

Let `a,b>0`, `R>max(a,b)`, `h_a=R-a`, and `h_b=R-b`.
For the two phases let `Delta=phi_j-phi_k`, and let `d=t-s`.
Direct cylindrical-coordinate expansion gives

```
distance² = (a-b)²+4ab sin²(d/2)
            +4(R+a cos t)(R+b cos s)sin²((d+Delta)/2).
```

The radial factors are positive and bounded below by `h_a,h_b`.
Put `U=ab`, `V=h_a*h_b`, and `S=U+V`. The minimum over `d`
of the resulting last two terms is

```
2[S-sqrt(S²-4UV sin²(Delta/2))].
```

Since `z=4UV sin²(Delta/2)/S²` lies in `[0,1]`,
`1-sqrt(1-z)>=z/2` proves the global lower bound

```
distance² >= (a-b)²+4K sin²(Delta/2),
K=UV/(U+V).
```

No small-angle approximation, local minimizer assumption, or untested
range restriction enters this step.

For `0<a<=b<=R/2`,

```
partial_b(1/K) = -1/(a*b²)+1/((R-a)*(R-b)²) <= 0,
```

because `a<=R-a` and `b<=R-b`. Hence `K(a,b)>=K(a,a)`.
For the diagonal value,

```
1/K(a,a)=1/a²+1/(R-a)²,
d/da[1/K(a,a)]=-2/a³+2/(R-a)³ <= 0.
```

Thus `K(a,a)` is nondecreasing up to `R/2`. This proves both
monotonicity assertions used in the source. They need not hold for arbitrary
radii beyond `R/2`, but those radii never occur in this construction.

## 2. Phase coverage and finite block validity

In one block set the longitude phases on alternating shells to

```
{2pi*j/N : 0<=j<N},
{2pi*j/N+pi/N : 0<=j<N}.
```

For any strand on one shell and any strand on its neighboring shell,
the phase difference is an odd multiple of `pi/N` modulo `2pi`.
Consequently its sine square is at least `sin²(pi/(2N))`. This
includes all `N²` pairs, not only a chosen matching of neighbors.
The parity of `N` does not alter that conclusion.

If `a0` is the innermost block radius, put
`A0=pi*a0*(R-a0)/sqrt(a0²+(R-a0)²)` and choose
`N=floor(A0)-1`. Then `A0>=N+1`. The established sine lemma
at the integer `m=2N>=6` gives

```
4K sin²(pi/(2N))
 >= 4(A0/pi)²[pi/(2N+1)]²
 >= 4(N+1)²/(2N+1)²
 > 1.
```

The last step is strict even if `A0=N+1`, so rounding does not lose
the needed margin. With radial gap `sqrt(3)`, the total squared distance
is strictly greater than four.

The capacity `A(r)=pi*sqrt(K(r,r))` increases for `r<=R/2`.
Thus a population chosen from the innermost shell also satisfies the
previous same-shell population lemma on all other shells in that block.
All actual radii obey `r<=r_outer=(R-2)/2<R/2`.

Adjacent shells in different blocks have radial gap two, making phases
and population equality irrelevant there. Any two shells separated by
at least one intervening shell have radial gap at least `2sqrt(3)>2`.
The first radius is two, so all shells clear the core. This exhausts
all component pairs in a bundle.

The lower count restriction has no missing small-T case. Throughout
the construction `a0>=2`, `R-a0>=4`; the function
`pi*r*h/sqrt(r²+h²)` increases in each positive argument. Hence
`A0>=8pi/sqrt(20)>5` and `N>=4` for every block, including `T=1`.

The observation concerning unequal populations is also correct:
the subgroup generated by `1/N` and `1/M` modulo one has spacing
`1/lcm(N,M)`. Any offset of that uniform phase grid has a point at
circular distance at most `pi/lcm(N,M)` from zero. For coprime
populations this is `O(1/(NM))`. This observation motivates equal
populations, but is not required for the validity proof.

## 3. Explicit indexing and uniform asymptotics

The source should specify the finite radii explicitly. One valid convention,
consistent with its prose, is as follows. For each integer `T>=1`, write

```
delta=sqrt(3),     b_T=floor(sqrt(T)),
k(i)=1+b_T*floor((i-1)/b_T),       1<=i<=T,
r_i=delta*i+(2-delta)[1+floor((i-1)/b_T)],
R_T=2r_T+2,
N_i=floor(A(r_(k(i)),R_T-r_(k(i))))-1,
A(r,h)=pi*r*h/sqrt(r²+h²).
```

The first shell has radius two. Within a block the gap is `delta`;
crossing a block boundary adds `delta+(2-delta)=2`. All shells in
a block have the same integer population. Offsets can be chosen from
the parity of `i-k(i)`, restarting at zero in each block. No compatibility
condition is needed when the population changes at a boundary.

Since `b_T` is comparable to `sqrt(T)`, uniformly in `1<=i<=T`,

```
r_i=delta*i+O(sqrt(T)),
R_T=2delta*T+O(sqrt(T)),
0<=r_i-r_(k(i))<delta*b_T=O(sqrt(T)).
```

These bounds remain valid when `b_T` jumps at a square. They control
the short last block as well as every full block.

The capacity is uniformly Lipschitz on the positive quadrant:

```
partial_r A=pi*h³/(r²+h²)^(3/2),
partial_h A=pi*r³/(r²+h²)^(3/2),
0<partial_r A, partial_h A<=pi.
```

Let `s=delta/2=sqrt(3)/2`, and use the functions `n(x),e(x)`
and constants `q0,l0` from review 001. Homogeneity and the preceding
uniform estimates imply

```
N_i=s*T*n(i/T)+O(sqrt(T)).
```

This is uniform even near the core: Lipschitz control was in `(r,h)`,
not a Taylor expansion dividing by a possibly small normalized radius.
Flooring and subtracting one contribute less than two additional units.

The exact single-component length is

```
ell(R,r)=integral_0^(2pi) sqrt((R+r cos t)²+r²)dt.
```

The triangle inequality for the integrand's two-vector gives
`|partial_R ell|<=2pi` and `|partial_r ell|<=2pi*sqrt(2)`.
Therefore, again uniformly,

```
ell(R_T,r_i)=s*T*e(i/T)+O(sqrt(T)).
```

Both leading terms are `O(T)`. Multiplying their expansions and
summing T shells gives errors `O(T^(5/2))` for length. The Riemann
sum errors of the smooth densities are smaller. Including the core yields

```
Q_T=s*q0*T²+O(T^(3/2)),
L_T=s²*l0*T³+O(T^(5/2)).
```

Here `Q_T,L_T` refer to one bundle. This both proves the claimed
block loss is subleading and supplies the missing uniform estimates.
After doubling, `M_T=2Q_T`, `D_T=2L_T`, and

```
D_T/M_T^(3/2)
 -> sqrt(s)*l0/(sqrt(2)*q0^(3/2)).
```

The formula in the candidate is therefore correct. The extra block-boundary
gaps and locking at inner-shell capacity do not change that coefficient.

## 4. All-integer filling without a monotonicity hypothesis

It is unnecessary to prove that `M_T` is monotone. Write
`c=2s*q0>0`; the proved estimate gives
`M_T=cT²+O(T^(3/2))`, so `M_T` tends to infinity and
`M_T/M_(T-1)` tends to one, irrespective of possible local decreases.

For a target integer `M` choose the least index `T` with `M_T>=M`.
For large M this index exists and tends to infinity. Minimality implies
`M_(T-1)<M<=M_T`. Thus

```
1 <= M_T/M < M_T/M_(T-1) -> 1.
```

Equivalently the relative overshoot is `O(T^(-1/2))`, which suffices.
Take the full doubled link at this index and delete `M_T-M` components.
The full-twist configuration-space proof identifies the surviving sublink
as `T(M,M)` up to the common mirror, and deleting components preserves
the established tube-clearance bounds while reducing length. Consequently

```
Rop(T(M,M))/M^(3/2)
 <= [D_T/M_T^(3/2)] * (M_T/M)^(3/2),
```

and passage to the limsup proves the desired upper bound across every
integer M. The same coefficient holds for the crossing normalization
`[M(M-1)]^(3/4)`. This addresses the square-index changes in block size
without assuming the resulting finite counts are monotone.

## 5. Inherited geometry and topology

Every shell still has `r>=2` and `R_T>=2r+2`, exactly the hypotheses
of the curvature/DCSD lemma independently reviewed in review 001.
The two round Hopf cores have distance `R_T`; every point in each
bundle is at most `r_T` from its core. The distance between bundles
is therefore at least `R_T-2r_T=2`.

For topology, the initial normal-disk points have polar radii `r_i`
and phases equal to the selected staggered grids. They are all distinct,
since different shells have different radii. Each normal configuration
undergoes the same full rigid rotation as before. Neither the configuration
isotopy proof nor the two-block full-twist factorization requires uniform
population across shells, constant radial gaps, or any special phase.
The explicit proper motion and the internal/mutual twist signs are
unchanged. Thus the single bundle is the appropriate full-twist closure,
and the doubled link is `T(2Q_T,2Q_T)` up to a global mirror.

## 6. Independent numerical attempts to falsify the construction

The reviewer generated the explicit radii and populations above independently
with NumPy, using floating arithmetic only as a diagnostic. Counts and
the adjacent-shell lower bound were checked near several block-size jumps,
including `T=3,4,8,9,15,16,24,25,99,100,101,255,256,1023,1024`.
No failed distance inequality or inadmissible population appeared.

Some representative results are:

| T | Doubled count M_T | D_T/M_T^(3/2) | Minimum adjacent extra term 4K sin²(pi/(2N)) |
|---:|---:|---:|---:|
| 4 | 82 | 12.47720277 | 1.33204595 |
| 9 | 356 | 12.33782805 | 1.19953657 |
| 25 | 2732 | 11.68470456 | 1.05921850 |
| 100 | 44782 | 11.16896870 | 1.01193903 |
| 256 | 298818 | 10.95866766 | 1.00340992 |
| 1024 | 4865730 | not evaluated | 1.00093601 |

The finite coefficients fluctuate at square indices and converge slowly;
the limit should not be advertised as a finite-M upper bound.

The actual two-parameter squared distance, rather than only the harmonic
bound, was independently minimized for four adjacent-shell pairs using
SciPy differential evolution with seed 194, tolerance `1e-11`, and
polishing. The observed distances were 2.39953027, 2.22021767,
2.15500358, and 2.01994629 for first-shell indices 1,5,14,88 at
`T=4,9,25,100`, respectively. Each pair had radial gap `sqrt(3)`
and the odd half-grid phase separation. These searches did not find a
counterexample; they are not a replacement for the all-parameter proof.

## 7. Remaining numerical and novelty limits

The exact coefficient is

```
sqrt(sqrt(3)/2)*l0/(sqrt(2)*q0^(3/2)),
q0=pi*(3asinh(1)/sqrt(2)-1).
```

Rescaling review 001's independently computed approximation gives
approximately 10.61355706326, consistent with the candidate. A rigorous
upper endpoint for this constant requires enclosed square roots and an
enclosed positive quotient, in addition to the first coefficient's
certificate. It is not enough to multiply a rounded midpoint.

In particular, `alpha_1<11.406` only yields
`alpha_2<10.614480`, so it does **not** certify `alpha_2<10.614`.
That latter threshold requires the certified `alpha_1` upper endpoint
to be below `10.614/sqrt(sqrt(3)/2)`, approximately 11.4054853.
The coarse `256 by 512` midpoint grid in review 001 is unlikely to meet
this stronger threshold with its proposed error estimate. A `512 by 1024`
grid quarters the discretization error and should suffice, subject to the
actual ball-arithmetic output. A looser threshold 10.615 avoids needing
that refinement. Exact endpoints should be selected from completed
certificates, rather than rounding the exploratory number downward.

The finite generator must implement the block's common population, alternating
offsets, and larger boundary gaps exactly as specified. The analytic theorem
does not need a software implementation, but an implementation can still fail
to instantiate it correctly. This review has not audited such code.

No novelty claim follows merely from obtaining a lower coefficient than the
nearest inspected construction. Triangular packing, staggered shells, and
commensurate helical populations have substantial potential prior art. The
bounded task deliberately leaves that literature question open.

## 8. Optional Wegner expansion check

The expansion in `WEGNER_EXPANSION_AUDIT.md` passes independently.
The ceiling differs from its argument by a bounded quantity, so its
effect is `O(1)` before the outer square root. With
`a=2sqrt(3)`, `b=4sqrt(3)-6`, and
`alpha=sqrt(4pi a)`, the constant term of the square root is
`alpha*b/(2a)=2pi*b/alpha`. Thus the coefficient of Q in the
unnormalized expression, and of `Q^(-1/2)` after normalization, is

```
B=2pi+2pi*b/alpha
 =2pi+sqrt(2pi*(7sqrt(3)-12))
 =7.167125130743448… .
```

The normalization by `[Q(Q-1)]^(3/4)` changes only the subsequent
`O(1/Q)` term. The note correctly retains an unsigned remainder and does
not convert this expansion into a pointwise finite-Q lower bound. This
correction is algebraic and does not strengthen the original exact
ceiling formula or establish any missing geometric hypothesis of that
formula's application.
