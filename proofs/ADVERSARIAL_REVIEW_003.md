# Independent adversarial review 003 — block-size first correction

Date: 2026-09-13. Reviewer: delegated Astra mathematical reviewer. Reviewed
`THEOREM_003_CANDIDATE.md`, the inherited geometric proof in Theorem 002 and
review 002, and independent finite constructions. The review assumed the
candidate could be false. No candidate or production files were edited.

## Verdict

**PASS for the exact-integral uniform expansion and the unique optimal fixed
constant c in b=floor(c sqrt(T)).** The incomplete final block, integer
population floors, exact outer radius and Hopf doubling all have the asserted
error orders. No missing first-order contribution was found.

**CONDITIONAL for certified decimal intervals:** the independent numerical
values below are diagnostics. They corroborate the formulas but do not certify
rounded endpoints. A separate interval implementation is still needed for any
rigorous decimal enclosure of c*, d or the correction coefficients.

This result optimizes the coefficient of T^(-1/2) among fixed c>0 within the
specified equal-block staggered construction. It does not identify the exact
finite-T minimizing integer b, compare equal-M configurations, optimize arbitrary
block schedules, establish a subleading bound after all-M component deletion,
or prove an optimum for ropelength. Publication novelty was not audited here.

| Obligation | Verdict | Reason |
|---|---|---|
| Geometry for arbitrary integer b | PASS | Inherited separation/topology proof uses no sqrt(T) restriction |
| Exact radii and outer-radius offsets | PASS | Extraction of lambda leaves a bounded error, including last block |
| Integer population rounding | PASS | Uniform O(1) per shell, subleading to the claimed correction |
| Smooth expansions near the core | PASS | Hole radius stays of order T; no singular derivative appears at x=0 |
| Incomplete final block | PASS | Lag discrepancy O(b²), giving O((b/T)²) relative error |
| Weighted population-length sum | PASS | Correct derivative is n'e, not (ne)' |
| Normalization and doubling | PASS | d=3n1/(4q0)-J/(2l0); crossing correction is O(T^-2) |
| Uniform stated asymptotic regime | PASS | b→infinity and b/T→0 |
| Strict d>0 and unique fixed-c optimum | PASS | Analytic bounds suffice; no numerical positivity assumption |
| Certified decimals | CONDITIONAL | Independent floating quadrature only in this review |
| Global/fixed-M/arbitrary-schedule optimum | NOT CLAIMED | No such conclusion follows from this expansion |

## 1. Geometry does not select a block size

For any integers 1<=b<=T, the first shell radius is delta+g=2. Consecutive
radii differ by delta=sqrt(3) inside a block and delta+g=2 at a boundary.
R=2r_T+2 gives R>=2r_i+2 for every shell. Each block has one population
computed from its innermost radius, and alternating phase offsets 0 and pi/N.
These are precisely the hypotheses of review 002's all-pair separation proof.
Neither that proof nor its full-twist isotopy argument requires b=floor(sqrt(T)).

The same-shell capacity rule also has no small-T exception: r>=2, h>=4 give
A>=8pi/sqrt(20)>5 and N=floor(A)-1>=4. Core clearance, self-thickness, boundary
clearance and cross-bundle clearance remain valid. Thus the candidate's finite
objects exist throughout the stated integer parameter domain.

## 2. Extracting the boundary-gap density

Put lambda=delta+g/b. The elementary identity

```
r_i-lambda*i = g*(ceil(i/b)-i/b)
```

lies in [0,g). In particular

```
r_i=lambda*i+O(1),
R=2lambda*T+O(1),
R-r_i=lambda*(2T-i)+O(1),
```

with constants independent of T,b,i. The final incomplete block changes only
the bounded quantity ceil(T/b)-T/b; it cannot introduce an additional term of
size b in R. This is the main potentially dangerous outer-radius effect.

Let A(r,h)=pi*r*h/sqrt(r²+h²). Its first derivatives on the positive quadrant
have absolute values at most pi. The component length

```
ell(R,r)=integral_0^(2pi) sqrt((R+r cos t)²+r²) dt
```

has |partial_R ell|<=2pi and |partial_r ell|<=2pi sqrt(2), directly from the
norm of the two-vector (R+r cos t,r). These Lipschitz estimates remain valid
near the innermost shell. No expansion in a reciprocal small radius is needed.
Homogeneity consequently gives, uniformly in i,

```
N_i=(lambda*T/2)*n(j(i)/T)+O(1),
ell_i=(lambda*T/2)*e(i/T)+O(1).
```

For the first line, flooring and subtracting one contribute an error in
(-2,-1], independent of how close a capacity is to an integer. For the second,
actual R and r_i differ by bounded amounts from their homogeneous approximants.
Since delta<=lambda<=2, these estimates have uniform constants.

## 3. Lag sums, including the last incomplete block

Write lag_i=i-j(i). For an arbitrary C¹ function h on [0,1], complete blocks
have the exact unweighted average (b-1)/2. Inside a complete block, replacing
h(i/T) by its value at one block endpoint changes the lag-weighted sum by at
most O(b³/T). There are at most T/b such blocks, so the combined error is
O(b²). On the final incomplete block both the actual lag sum and the putative
complete-block average contribution are bounded by O(b²). Thus

```
sum_i lag_i*h(i/T)
 = ((b-1)/2)*sum_i h(i/T)+O(b²)
 = (b*T/2)*integral_0^1 h(x)dx+O(T+b²).
```

The last equality uses the C¹ Riemann-sum error O(1), the replacement of b-1
by b, and b<=T. This estimate explicitly covers b not dividing T.

Taylor expansion of n at i/T, with a bounded second derivative, gives

```
n(j(i)/T)=n(i/T)-(lag_i/T)*n'(i/T)+O(b²/T²).
```

Summing first without, and then with, the bounded weight e(i/T), yields

```
sum_i n(j(i)/T)=T*q0-(b/2)*n1+O(1+b²/T),
sum_i n(j(i)/T)*e(i/T)=T*l0-(b/2)*J+O(1+b²/T).
```

Here n(0)=0 is essential in the first expression. For the second expression
the lag lemma is applied to h=n'e. The length is evaluated at the actual
shell i, so it is correct that e is not differentiated in this lag term.
Replacing J by integral (ne)' would introduce a false first correction.

## 4. Counts, lengths and the quotient

The bounded errors in N_i sum to O(T). Multiplying a bounded population error
by an O(T) component length and summing costs O(T²). The analogous errors from
component length approximation have the same order. Core count and core length
are smaller. Therefore

```
Q=(lambda/2)*[q0*T²-(b/2)*n1*T]+O(T+b²),
Lbundle=(lambda²/4)*[l0*T³-(b/2)*J*T²]+O(T²+b²*T).
```

In the theorem's regime b/T→0, these imply Q is bounded above and below by
positive multiples of T². This comparability is **not** uniform over every
1<=b<=T: for b=T there is one block with bounded population and Q=O(T).
The candidate's final asymptotic theorem does not use that excluded regime.
The pre-quotient absolute-error formulas remain uniform, but the quotient
expansion must explicitly be read in b/T→0, or for b/T sufficiently small.

Put epsilon=b/T. Doubling gives M=2Q and Ltotal=2Lbundle. Expanding the quotient
at positive q0 yields

```
Ltotal/M^(3/2)
 = sqrt(lambda/2)*alpha1*
   [1+(3n1/(4q0)-J/(2l0))*epsilon+O(T^-1+epsilon²)].
```

The numerator contributes -J/(2l0), while the exponent -3/2 on the population
factor contributes +3n1/(4q0). Keeping both factors of two gives the displayed
sqrt(lambda/2)*alpha1, not the single-bundle coefficient.

Since

```
[M(M-1)]^(3/4)=M^(3/2)*(1-1/M)^(3/4),
```

the crossing-number denominator changes the quotient only by relative
O(M^-1)=O(T^-2). It cannot affect either displayed first correction.
Finally

```
sqrt(lambda/2)=sqrt(delta/2)*[1+g/(2delta*b)+O(b^-2)].
```

The product of 1/b and b/T is 1/T. Combining the preceding estimates proves
exactly

```
F(T,b)=alpha2*[1+a/b+d*b/T+O(b^-2+(b/T)²+T^-1)].
```

All constants can be chosen independent of integer T,b once b is sufficiently
large and b/T is sufficiently small. The functions involved are smooth on the
compact normalized domain. For fixed c>0, substituting b=floor(c sqrt(T))
changes 1/b and b/T by O(T^-1) and proves the stated fixed-c expansion.

## 5. Positivity, uniqueness and an exact strict improvement over c=1

The derivative n' is nonnegative, and integral n'=n1. The triangle inequality
for the integrated speed vector gives e>=8pi. Concavity of the square root
and the mean value of cosine give e<=2pi sqrt(16+6x²)<=2pi sqrt(22).
Consequently

```
J<=2pi sqrt(22)*n1,
l0>=8pi*q0,
d>=n1/q0*(6-sqrt(22))/8>0.
```

This proves the sign of d without a numerical integral evaluation. Since a>0,
a/c+dc is strictly convex on c>0, diverges at both endpoints and has its unique
minimum at sqrt(a/d). The minimum value is 2sqrt(ad), as claimed.

A useful stronger consequence is already analytic. Since n is nondecreasing,
q0<=n1. Since sqrt(22)<5, the bound gives d>1/8. Also sqrt(3)>5/3 implies
a=1/sqrt(3)-1/2<1/10. Hence d>a, so c*<1 and

```
beta_(c=1)-beta_opt = alpha2*(sqrt(d)-sqrt(a))² > 0.
```

Thus improvement of this first correction over the original choice c=1 does
not depend on treating a diagnostic decimal as a certified value. This still
says nothing about equal-M finite comparisons or arbitrary block schedules.

## 6. Independent numerical attempts to falsify the expansion

`results/reviewer003_independent.py` constructs the exact stated index/radius
and population formulas independently with NumPy and integrates shell lengths
by 96-point Gauss-Legendre quadrature. It imports no production generator,
certificate or optimization helper. Separate SciPy integrations compute n, n'e
and the toroidal speed integrals. These floating computations are diagnostic;
integer floors and length evaluations are not interval-certified here.

The independent values are

```
q0       = 2.732166854279056
l0       = 72.84025687265839
J        = 114.6313563669178
d        = 0.43273606192045955
c*       = 0.422784805211815
beta_opt = 3.8835903551038586
beta_1   = 5.413830382425291
```

Finite constructions were evaluated for c=.2,c*,1,2 at
T=128,257,1024,4099,16384,65539, including many incomplete terminal blocks.
For c* the scaled residual T*(F-alpha2-beta_opt/sqrt(T)) was approximately
-0.894,-0.992,-0.757,-0.862,-0.328,-0.788. The other fixed-c sequences also
had bounded-looking residuals, including the larger floor sensitivity at c=.2.
These samples are compatible with O(T^-1); they do not prove that order.

Additional tests used b=floor(T^p), p=.25,.4,.6,.75 at T=257,4099,65539.
The maximum observed absolute residual divided by
b^-2+(b/T)²+T^-1 was below 0.400 after normalizing F by alpha2. No tested
incomplete-block or unbalanced-scale sequence contradicted the uniform formula.
Full parameters, capacity-to-integer diagnostic gaps and results are preserved
in `results/reviewer003_independent.json`, together with the candidate hash.

The exhaustive M2 winners motivate the conjecture but are not used as proof.
In particular, convergence of finite integer argmin(b) to c*sqrt(T) over all
possible b would need an additional global comparison argument excluding other
scalings. The theorem as stated correctly confines its unique optimization
claim to the asymptotic correction among fixed c>0.
