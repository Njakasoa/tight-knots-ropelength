# Independent adversarial review 001

Date: 2026-09-13. Reviewer: delegated Astra mathematical reviewer.

Scope: `TOROIDAL_SHELL_SEPARATION.md`, `POSITIVE_CONTROLS.md`,
`CLAIM-0001.md`, and the pertinent part of `RECENT_TORUS_AUDIT.md`.
The proof note was read including its final explicit twist-sign check.
The review started by assuming the proposed construction could be false.
No construction or certificate implementation was reused. The calculations
below were independently derived and checked with NumPy/SciPy/SymPy in the
project virtual environment; those floating computations are diagnostic,
not interval certificates. No source proof files were modified.

## Verdict

**PASS for the mathematical construction and exact integral upper bound,
with the topology and uniform limiting details supplied below.** No geometric
or topological counterexample was found. The existing proof note contains
the right ingredients; several sections still describe completed obligations
as pending. Its theorem statement and claim ledger should be synchronized
after incorporating this review and the independent arithmetic certificate.

**CONDITIONAL for a rounded numerical upper bound.** The value
11.40500928987144 is independently reproduced, but digits from SciPy are not
certified inequalities. At the time of this review, the proposed midpoint
ball-arithmetic calculation had not been supplied for inspection. The exact
integral expression itself defines a rigorous real constant without numerical
quadrature. One may state the theorem with that exact expression now; do not
state that the limsup is at most the displayed rounded decimal as though that
decimal were an outward upper endpoint.

**CONDITIONAL for publication novelty.** The bounded primary-source comparison
supports a difference from Klotz's inspected 2026 construction, not a claim of
priority over all literature. Neither this review nor the construction proves
global optimality, an attained minimum, or a matching lower bound.

| Obligation | Verdict | Qualification |
|---|---|---|
| Exact same-shell distance identity | PASS | All phases and parameters covered |
| Harmonic lower bound and condition (S) | PASS | Retain the stated sum-of-squares hypothesis |
| Integer population rule | PASS | Every chosen shell actually has at least four strands |
| Cross-shell and core clearance | PASS | Requires the common major radius and positive radial coordinates |
| Curvature and self DCSD | PASS | Taylor argument is valid for the shorter cyclic interval |
| Double-bundle geometric clearance | PASS | Explicit proper rigid motion gives the required round Hopf cores |
| Single-bundle full-twist topology | PASS | Configuration-space isotopy argument below |
| Doubled topology and signs | PASS | Zero framing plus block-rotation factorization below |
| Length formula and exact population integral | PASS | Independent derivation below |
| Uniform errors and all-integer limsup | PASS | Uniform estimates and monotonicity below |
| Midpoint derivative/error bounds | PASS | Proposed constants are conservative |
| Numerical interval endpoint | CONDITIONAL | Requires running and reviewing rigorous ball arithmetic |
| Circle and round Hopf controls | PASS | Hopf optimum is not proved by the supplied note |
| Novelty/best-known/global-optimum claim | CONDITIONAL / not established | Bounded review only |

## 1. Same-shell separation

Put `rho(t)=R+r cos(t)>0`, `d=t-s`, and `Delta=phi_j-phi_k`.
Expanding the planar distance in cylindrical coordinates gives

```
distance² = (rho(t)-rho(s))² + r²(sin(t)-sin(s))²
            + 4 rho(t)rho(s) sin²((d+Delta)/2)
          = 4r² sin²(d/2)
            + 4 rho(t)rho(s) sin²((d+Delta)/2).
```

Replacing the positive product by `(R-r)²=h²` is valid for all `s,t`.
Writing the resulting expression as a constant minus a cosine with one
amplitude proves exactly

```
D² = 2(S - sqrt(S²-4P)),
S = r²+h²,       P = r²h² sin²(Delta/2).
```

For `S>=2`, `D²>=4` is equivalent to `sqrt(S²-4P)<=S-2`, hence to
`P>=S-1`. Squaring is legitimate because the right side is nonnegative.
The radicand is nonnegative because `4P<=4r²h²<=S²`.
The least nonzero equally spaced angular separation gives
`sin²(Delta/2)>=sin²(pi/N)`. There is no restriction to adjacent parameters
or to a local stationary point.

The sine estimate in the note is valid for `N>=3`: use
`sin x>=x-x³/6` at `x=pi/N`, followed by
`pi²(N+1)<=6N²`. The latter follows from `pi²<10` and positivity/increase
of `6N²-10N-10` from `N=3` onward. Thus `N=floor(A)-1` works.

For the actual construction, `r>=2`, `h>=4`, and `A=pi*r*h/hypot(r,h)`
is increasing in each positive argument. Therefore
`A>=8pi/sqrt(20)>5`, so `N>=4`; no small-shell exception is missing.
The rule is deliberately sufficient, not an exact occupancy maximum.

An independent numerical attack also minimized over the midpoint angle
analytically before numerically minimizing over `d`. With `m=(s+t)/2`,
the radial product equals

```
R² + 2Rr cos(m)cos(d/2) + r²(cos²(m)-sin²(d/2)).
```

Its minimum occurs at
`cos(m)=clip(-R*cos(d/2)/r,-1,1)`. This reduces the actual same-shell
distance minimization to one dimension without using the proof's `h²`
replacement. An 8193-point bracket search on `[-pi,pi]` followed by bounded
scalar minimization gave these representative distances:

| T | shell i | N | Analytic lower bound | Numerical actual minimum |
|---:|---:|---:|---:|---:|
| 1 | 1 | 4 | 2.6486137874 | 2.6833177226 |
| 2 | 2 | 9 | 2.3063033845 | 2.3198186795 |
| 5 | 5 | 23 | 2.0968507314 | 2.0991770566 |
| 20 | 20 | 89 | 2.0447887241 | 2.0449473984 |
| 100 | 50 | 297 | 2.0082861245 | 2.0082891097 |
| 100 | 100 | 445 | 2.0067066522 | 2.0067129022 |

These diagnostics did not find a counterexample and are not needed to
establish the analytic inequality.

## 2. Self-thickness and distances between components

The derivative components in the rotating cylindrical frame are

```
F'  = (-r sin t, R+r cos t, r cos t),
F'' = (-(R+2r cos t), -2r sin t, -r sin t).
```

Consequently `|F'|²=(R+r cos t)²+r²>=h²` and
`|F''|<=R+sqrt(5)r=M`. The triangle inequality used for the latter is
valid: the variable vector has squared norm
`r²(4 cos²t+5 sin²t)<=5r²`.

Under `R>=2r+2`, `r>=2`, one has `h>=4`, `r<=h-2`, and
`M<=17h/4-6`. The function `17/(4h)-6/h²` is decreasing for `h>=4`
and equals `11/16` at four. Therefore curvature is at most
`M/h²<=11/16<1`.

For any distinct doubly critical pair choose its cyclic ordering so the
forward parameter difference is `0<d<=pi`. Taylor's integral remainder
has norm at most `Md²/2`, proving

```
(F(s+d)-F(s)) dot F'(s)
  >= d |F'(s)| (|F'(s)|-Md/2).
```

Criticality forces `d>=2h/M`. The same-component exact distance identity
then gives `distance>=2h sin(d/2)>=2h sin(h/M)`, because sine is
increasing on `[0,pi/2]`. Since `0<h/M<1`,
`sin(h/M)>=(5/6)h/M`. The stated bound
`distance>=(5/3)h²/M>=80/33>2` follows. This is a valid DCSD argument;
near-diagonal chords have not been incorrectly treated as struts. The
standard smooth-curve thickness formula, minimum of curvature radius and
half DCSD, completes this obligation. The parameterization is embedded:
its longitude traverses the circle once and its cylindrical radius is positive.

For unequal shell radii, the same expansion instead has first term
`|r_i exp(it)-r_j exp(is)|²>=(r_i-r_j)²`; the remaining term is
nonnegative. Thus spacing two works for arbitrary inter-shell phases.
The distance from a shell point to the core circle is exactly its minor
radius, so the nearest shell has core clearance two.

For equal Hopf core radii `R`, direct expansion gives

```
|C_1(u)-C_2(v)|² = R²[1+2(1-cos u)(1+cos v)] >= R².
```

Every shell point is at most `2T` from its own core. Hence every
cross-bundle distance is at least `R-4T=2`. This covers all parameters
and shells, including core components, not merely prospective contact pairs.
The motion `P(x,y,z)=(R+x,-z,y)` has determinant +1 and gives the claimed
second core. Disjoint tube interiors and thickness at least one follow;
boundary contacts at distance two are allowed.

## 3. Constructive topology and framing

### One bundle

The standard tubular embedding is

```
E(u,a+ib)=((R+a)cos u,(R+a)sin u,b),     |a+ib|<R.
```

After writing `u=t+phi_j`, each component is
`E(u,exp(iu)w_j)` with `w_j=r_j exp(-i phi_j)`, and the core is
`w_j=0`. All `w_j` are distinct. Every continuous path of configurations
of distinct disk points `w_j(v)` produces a continuous family of embedded
links `E(u,exp(iu)w_j(v))`; positive cylindrical radii and injectivity
of each disk fiber exclude all collisions. A compact such path may be
chosen in a disk strictly smaller than radius `R`. Isotopy extension then
gives an ambient isotopy. No tube-clearance claim is needed during this
topological isotopy.

Move the initial configuration to equally spaced points on one small
circle. The resulting curves are the standard common-slope torus curves,
i.e. the closure of one full twist, `T(Q,Q)` or its common mirror.
Equivalently, rigid disk rotation is the central full-twist braid.
The included center point causes no exception: it can be moved along
with the other points. This proves more than pairwise linking.

The frame `(e_radial,e_vertical)` is the zero framing of the oriented
round core. A fixed nonzero normal displacement gives a parallel planar
circle, with linking number zero. Framings of the unknot are classified
by this integer, so it is the same framing as the preferred zero framing
in the standard closed-braid cabling picture.

### Two bundles

Here is a direct justification of the block full-twist identity, rather
than an inference from linking numbers. Place `Q` points in each of two
small disjoint disks. Rotate the entire configuration once. In coordinates
the point paths are

```
exp(iu)(c_b+w_bj),        b=1,2.
```

There are two motions: centers `c_b` make a full two-strand twist, and
the offsets `w_bj` rotate once inside each disk. Their simultaneous
execution is homotopic to sequential execution, staying in the space of
disjoint point configurations: let the center-rotation and offset-rotation
angles vary independently over the square `[0,2pi]²`. Disks remain
disjoint because their centers stay a fixed distance apart, and rotation
preserves their radii. The square diagonal is homotopic to its two edges.

Thus the full twist on `2Q` points factors as a full twist in each
`Q`-point block and the mutual full twist of two blocks whose disk frames
do not rotate. The latter is exactly the zero-framed parallel cabling
of the two-strand Hopf braid. Its closure, with the two internal full
twists added, is therefore `T(2Q,2Q)` up to the common mirror convention.
This argument applies to any finite block configurations; equal shell
populations or particular phases are not a hidden assumption.

To apply that factorization, one must match signs in the preferred zero
frames. The explicit proof note does so correctly. The first helix crosses
the first core's oriented spanning disk only at its inner equatorial
point, with negative vertical velocity, giving internal linking -1.
The second oriented core `P(C_1)` crosses that disk at the origin with
negative vertical velocity, giving mutual linking -1. The proper motion
preserves the second bundle's internal sign. Since each cable winds once
along its core, these are precisely the relative internal and mutual
twist signs in the factorization, not arbitrary choices of component
orientations. All signs agree. A common mirror leaves length and thickness
unchanged and gives whichever chirality the notation `T(M,M)` specifies.

For completeness, the displayed orthogonal two-circle core arrangement
is the standard Hopf link, rather than a link identified solely through
its linking number. One may isotope it to the closure of the full twist
on two strands while carrying its preferred zero framings. This framing
transport introduces no unrecorded integer twist because its zero linking
push-offs remain zero linking push-offs under the isotopy.

## 4. Length, population, and all-integer asymptotics

The exact length of one component is

```
ell(R,r)=integral_0^(2pi) sqrt((R+r cos t)²+r²) dt.
```

Its independence of component phase follows directly from the speed.
With `x=i/T`, `R=4T+2`, `r_i=2i`, define

```
n(x)=2pi*x*(2-x)/sqrt(x²+(2-x)²),
e(x)=integral_0^(2pi) sqrt((4+2x cos t)²+4x²) dt.
```

The count and length errors are uniform even near the innermost shell.
Indeed, for `A(r,h)=pi*r*h/sqrt(r²+h²)`,
`0<partial_h A=pi*r³/(r²+h²)^(3/2)<=pi`.
Changing `h` by two changes `A` by at most `2pi`; flooring and
subtracting one change it by less than two. Thus
`N_i=T*n(i/T)+O(1)` with an absolute uniform constant.
Also `|partial_R ell|<=2pi`, so
`ell(4T+2,2i)=T*e(i/T)+O(1)` uniformly. The functions `n,e`
are continuously differentiable on the full closed interval. Riemann sums
therefore have error `O(1/T)` after normalization. Summing and including
the single core of length `2pi R` proves

```
Q(T)=q0*T²+O(T),
L(T)=l0*T³+O(T²),
q0=integral_0^1 n(x)dx,
l0=integral_0^1 n(x)e(x)dx.
```

Set `y=1-x`. Then
`n=√2*pi*(1-y²)/sqrt(1+y²)`, and elementary integration gives exactly

```
q0=pi*(3*asinh(1)/sqrt(2)-1)>0.
```

Independent quadrature gave `q0=2.732166854279056`,
`l0=72.84025687265839` and
`l0/(sqrt(2)*q0^(3/2))=11.405009289871444`.
Finite full doubled constructions gave `L/M^(3/2)` approximately
12.46429, 12.11742, 11.72311, 11.50377, and 11.41750 at
`T=1,2,8,32,256`. These are convergence checks, not error bounds.

For fixed `i`, increasing `T` increases `h_i` by four, so each existing
capacity is nondecreasing. A newly added shell has positive population;
the total `M_T=2Q(T)` is strictly increasing. The preceding derivative
bound shows each existing integer population grows by at most `4pi+1`,
and the new shell population is at most `2pi(T+1)`. Thus
`M_(T+1)-M_T=O(T)` explicitly, without subtracting two unspecified
asymptotic remainders.

For any integer `M` between consecutive full populations, take the next
larger construction and delete components. Deleting any subset of a rigid
full-rotation configuration leaves the full rotation of the remaining
points, hence the link `T(M,M)` up to the same mirror. Distances cannot
decrease, and deleting components cannot worsen the reach of the surviving
union here (its component curvature and pairwise distance requirements
are unchanged or removed). Length cannot increase. Since
`M_next/M=1+O(1/T)`, the next-full-population bound yields

```
limsup_(M->infinity) Rop(T(M,M))/M^(3/2)
    <= l0/(sqrt(2)*q0^(3/2)).
```

The finitely many integers below the first full population have no effect.
Using the crossing normalization `[M(M-1)]^(3/4)` instead has the same
limiting coefficient. This is an upper bound on an infimum, not an assertion
that these geometric representatives minimize ropelength.

## 5. Midpoint certificate bounds

The proposed `g=(4+2x cos t)²+4x²` satisfies `8<=g<=40`.
For its minimum, first minimize over `cos t` at -1, then minimize
`16-16x+8x²` on `[0,1]`; its minimum is eight. The maximum forty is
immediate. Direct differentiation proves all proposed bounds:

```
|g_x|<=32, |g_xx|<=16, |g_t|<=24, |g_tt|<=24.
```

The transformed density gives stronger bounds than required:

```
n'(x)=√2*pi*y*(3+y²)/(1+y²)^(3/2),
n''(x)=-3√2*pi*(1-y²)/(1+y²)^(5/2),
0<=n<=√2*pi<5,  0<=n'<=2pi<14,  |n''|<=3√2*pi<40.
```

For `f=n sqrt(g)`, the chain rule and the proposed looser constants give

```
|f_xx| <= 40√40 + 14*32/√8
          +5[16/(2√8)+32²/(4*8^(3/2))]
        < 483 < 600,
|f_tt| <= 5[24/(2√8)+24²/(4*8^(3/2))]
        < 54 < 60.
```

The standard one-dimensional composite midpoint error, applied first in
one variable and then in the other, therefore proves the stated tensor
bound

```
E <= (2pi)/24 * [600/N²+60*(2pi/M)²].
```

There is no missing mixed-derivative term. At `N=256,M=512`,
`E≈0.004762436158462352` for the length integral. The actual certificate
must evaluate midpoint nodes, trigonometric functions, square roots,
weights, this error term, `q0`, and the final quotient using enclosing
arithmetic. In particular, binary floating midpoints multiplied by a
non-enclosed value of pi do not meet that requirement. The denominator
must be certified positive. The valid error bound alone does not certify
the SciPy decimal. A mesh of this size should be sufficient for a strict
outward upper threshold such as 11.406, but only an actual interval output
may establish that threshold.

## 6. Exact positive controls

The unit circle proof passes: its reach is one, length is `2pi`, and
Fenchel together with curvature at most one proves that no admissible
unknot has smaller length. The claimed scaling is correct. This is a
known optimum.

For the round Hopf example the distance expansion in the note is exact.
Each circle has reach two; the intercomponent minimum is two, so the
union has reach one. The total length is `8pi`. The two continuous strut
families listed in the note follow from the two vanishing factors in
the expansion. Every such pair is critical in both parameters. The
circles are disjoint, and the explicit arrangement is the standard Hopf
link. The proof establishes its length and an upper bound, and correctly
does not claim a general Hopf lower bound. A finite contact graph cannot
represent its complete smooth strut locus.

Machin's identity and alternating rational arctangent remainders can
certify `2pi` and `8pi`, but an implementation still needs review of
the signed combination of intervals. This arithmetic task is separate
from the already valid geometric proofs.

## 7. Literature and claim limitations

The bounded comparison inspected [Klotz 2026 v2](https://arxiv.org/html/2603.02416v2),
especially sections III.1 and III.3. Its equation (19) uses the common hole
radius `h=2T`; the present density instead uses each shell's own
`h_i=R-r_i`. The source also describes the double-torus operation and
warns that mirroring only one bundle can change the link type. Its
11.68 construction retains an explicitly stated approximation assumption.
The present exact harmonic lower bound and larger inner-shell populations
are therefore a substantive difference from those inspected formulas.

This is evidence of a useful result relative to the nearest audited
construction. It is not a complete prior-art search and does not prove
that 11.406, once certified, is the best published upper bound. The claim
should separate: an independently reviewed mathematical theorem with an
exact integral constant; a subsequently certified numerical upper endpoint;
and a still-provisional novelty assessment. No optimizer or finite mesh
can settle the global minimum from the evidence reviewed here.
