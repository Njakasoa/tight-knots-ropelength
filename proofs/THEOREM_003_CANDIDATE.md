# Theorem 003 — asymptotically optimal block size within the staggered grammar

Status: inferred after M2 exhaustive block-size search; exact theorem passed
independent adversarial review in ADVERSARIAL_REVIEW_003.md. The filename is
retained for provenance. A separate Arb coefficient certificate passed independent review in
BOUNDARY_CERTIFICATE_REVIEW.md.
This optimizes the first correction for this explicit construction, not the
ropelength infimum or all possible block schedules.

Let delta=sqrt3, g=2-delta. For T shells and an arbitrary integer block size
1≤b≤T set j(i)=1+b floor((i-1)/b),

```
r_i=delta*i+g*ceil(i/b),    R=2*r_T+2,
N_i=floor(A(r_j,R-r_j))-1,
A(r,h)=pi*r*h/sqrt(r²+h²).
```

Alternate phases0,pi/N within each block, retain the round core and the same
proper Hopf doubling as Theorem002. Its geometric proof uses only equal block
populations, within-block gapsqrt3 and boundarygap2; it holds for everyb.
LetQ=1+sumN_i, M=2Q, Ltotal the exact total analytic length, and
F(T,b)=Ltotal/[M(M-1)]^(3/4).

Use the smooth functions from Theorem001 on0≤x≤1:

```
n(x)=2pi*x*(2-x)/sqrt(x²+(2-x)²),
e(x)=integral_0^(2pi) sqrt((4+2x cos t)²+4x²) dt,
q0=integral n, l0=integral n*e, n1=n(1)=sqrt2*pi,
J=integral_0^1 n'(x)e(x) dx,
a=g/(2delta)=1/sqrt3-1/2,
d=3*n1/(4*q0)-J/(2*l0),
alpha2=sqrt(delta/2)*l0/(sqrt2*q0^(3/2)).
```

For b→infinity and b/T→0, the uniform expansion is

```
F(T,b)=alpha2*[1+a/b+d*b/T+O(b^(-2)+(b/T)^2+T^(-1))].
```

Consequently if b(T)=floor(c*sqrtT), with fixedc>0,

```
F(T,b(T))=alpha2+alpha2*(a/c+d*c)/sqrtT+O(T^(-1)).
```

The correction coefficient is uniquely minimized among fixedc>0 at
c*=sqrt(a/d), with minimum2*alpha2*sqrt(a*d). This is a statement about these
constructed sequence values, where M varies withT,b. It is not a fixed-M
comparison and does not claim an optimized all-integerM subleading term after
component deletion.

## Derivation with error orders

Put lambda=delta+g/b. Uniformly ini,

```
r_i=lambda*i+O(1),  R=2lambda*T+O(1),
N_i=(lambda*T/2)*n(j(i)/T)+O(1),
length(shell i)=(lambda*T/2)*e(i/T)+O(1).
```

Constants can be chosen uniformly for1≤b≤T: delta≤lambda≤2, the major/minor
ratio stays in the compact scaled region with hole radius bounded below by
delta*T. The capacity and speed integral are smooth homogeneous functions
there, with bounded first derivatives. Floors and the subtraction1 costO(1)
per shell. The core adds1 toQ andO(T) to single-bundle length.

For everyC² functionf on[0,1], with lag_i=i-j(i), Taylor expansion gives

```
f(j(i)/T)=f(i/T)-(lag_i/T)*f'(i/T)+O(b²/T²).
```

On complete blocks, lag_i averages(b-1)/2. Replacing f'(i/T) by its value at
one endpoint of a block gives total discrepancyO(b²), because each block
contributesO(b³/T) and there areO(T/b) blocks. The final incomplete block
also costsO(b²). Hence

```
sum lag_i*f'(i/T) = (b/2)*T*integral f' + O(T+b²).
```

Euler sum estimates and the Taylor remainder imply

```
sum n(j(i)/T) = T*q0-(b/2)*n1+O(1+b²/T),
sum n(j(i)/T)*e(i/T) = T*l0-(b/2)*J+O(1+b²/T).
```

The second line uses the same lag calculation on the smooth functionn'e,
not on(ne)'. Therefore

```
Q=(lambda/2)*[q0*T²-(b/2)*n1*T]+O(T+b²),
Lbundle=(lambda²/4)*[l0*T³-(b/2)*J*T²]+O(T²+b²*T).
```

After doubling, expand1/[M(M-1)]^(3/4). TheM-1 correction isO(T^-2)
relative because Q is comparable to T² in the regime b/T→0. This comparability
is not asserted uniformly for every b≤T. The quotient expansion yields

```
F=sqrt(lambda/2)*alpha1*[1+d*b/T+O(T^-1+(b/T)^2)].
```

Finally sqrt(lambda/2)=sqrt(delta/2)[1+a/b+O(b^-2)]. The cross term
(1/b)*(b/T) isO(T^-1), giving the formula. Replacingc sqrtT by
its floor affects1/b andb/T only at orderT^-1.

## Strict positivity and class optimum

n'(x)=4pi*(1-x)*(x²-2x+4)/(x²+(2-x)²)^(3/2)≥0.
The integral triangle inequality gives e(x)≥8pi; Jensen's inequality gives
e(x)≤2pi sqrt(16+6x²)≤2pi sqrt22. Thus

```
J≤2pi sqrt22*n1,  l0≥8pi*q0,
d≥(n1/q0)*(6-sqrt22)/8>0.
```

Alsoa>0. The functiona/c+dc has derivative-a/c²+d, positive second derivative
2a/c³, and diverges at both ends ofc>0; its unique minimizer is sqrt(a/d).

There is also an exact strict improvement over c=1. Since n is nondecreasing,
q0≤n1. Since sqrt22<5, the displayed bound gives d>1/8. Also sqrt3>5/3
gives a<1/10. Therefore d>a, c*<1, and

```
beta_c=1-beta_opt=alpha2*(sqrt(d)-sqrt(a))²>0.
```

This additional inequality was independently derived by the Astra reviewer.

## Numerical evidence and open checks

The exhaustive search in results/discovery_blocks_20260912T221841Z searches
allb=1..T at T=8..1024 with48-node quadrature and96-node winner checks. It
finds b=(1,2,2,4,5,7,9,13). No preferred block size or exponent is in the
search objective. These were floating candidate values. A subsequent independent Arb audit
certified all 1,024 population floors for the selected T=1024,b=13 construction,
confirming M=4,976,348; its finite length remains a numerical diagnostic.

Separate scratch quadratures predict J≈114.63135637, d≈0.4327360619,
c*≈0.4227848052, beta_opt≈3.8835903551, versus beta_c=1≈5.4138303824.
These displayed approximate decimals remain diagnostic. An independent Arb
rectangle certificate and its review provide separate outward enclosures.
The exact theorem statements use integrals, not these rounded numbers.
