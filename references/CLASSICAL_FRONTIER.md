# Ropelength literature audit (cutoff 2026-09-12)

This is a primary-source audit for the Tight Knots Lab. “Ropelength” is
ambiguous by a factor of two in this literature; the convention used by each
entry is recorded in [NORMALIZATION.md](../NORMALIZATION.md). A number below is
called **rigorous** only when the cited paper proves it for the stated class.
Numerical tightening, a geometric construction, or a stationary point is an
upper bound/candidate and does not prove the infimum.

## Result table

| Family or claim | Rigorous lower bound | Rigorous upper bound | Method and hypothesis | Remaining gap |
|---|---:|---:|---|---|
| Any nontrivial knot K | `2π(2+√2)=21.45…` (radius-one) [CKS, Thm. 7.1](https://arxiv.org/html/math/0103224#S7) | none uniform in crossing number | `C^{1,1}`, unit **radius** thickness; cone angle `4π`; parallel overcrossing number `PC(K)≥2` | Diao’s crossing bound and the quadrisecant bound improve the universal lower; exact minima unknown. |
| Any nontrivial knot, crossing number c | `L(L−17.334)≥16πc`, hence `L>24`, radius-one [Diao (2003)](https://doi.org/10.1142/S0218216503002275) | none uniform | Unit disk/tube radius; crossing number only. Equivalently `L≥(17.334+sqrt(17.334²+64πc))/2`. | It is a family bound, not a value for a particular knot; compare with `c^(3/4)` below. |
| Any knot/link, crossing number c | `L≥(4πc/11)^(3/4)=1.105… c^(3/4)`, radius-one [Buck (1998)](https://doi.org/10.1038/32561), [Buck--Simon (1999)](https://doi.org/10.1016/S0166-8641(97)00211-3) | `L≤a c log^5(c)` for a universal a>0, [Diao--Ernst--Por--Ziegler (2019)](https://doi.org/10.1142/S0218216519500858) | Average-crossing-number/area inequality for the lower bound; cubic-lattice projection and separator construction for the upper bound | Exponent gap 3/4 versus 1 (up to logarithms), and no sharp universal coefficient. |
| Any alternating knot, crossing number c | `L>(c+2)/56>c/56`, radius convention as stated by Diao, [Diao (2024)](https://doi.org/10.1017/S0305004124000288) | General `a c log^5(c)` upper above | Reverse-parallel link braid-index theorem plus Diao’s lattice braid-index inequality. The theorem is for **knots**, not alternating links. | Constant 1/56 may improve (the paper remarks 1/48 as a possible direction); alternating links with at least two components remain open there. |
| Any nontrivial `C^{1,1}` knot | `15.66…`, diameter-one, [Denne--Diao--Sullivan (2006), Thms. 9.4--9.7](https://arxiv.org/html/math/0408026#S9) | none | Every nontrivial knot has an essential alternating quadrisecant; its cone/arc estimates yield the bound. | This is `31.32…` after radius conversion; it still does not identify a minimizer. |
| K with crossing number c≤20 | Diao formula above (e.g. c=3: L>23.697; c=20: L>41.537), radius-one | Numerical/constructive values only; no general certified smooth upper table | Diao’s theorem is rigorous; values from tight-knot computations are feasible embeddings | For each small knot, a safe smooth embedding gives an upper bound; a numerical vertex list alone does not prove the global minimum. |
| Hopf chain of k≥2 rings | Equals the explicit lower bound in CKS | Exact: `(4π+4)k−8`, radius-one [CKS, §3](https://arxiv.org/html/math/0103224#S3) | Each component links the required neighbours; CKS disk-hull bound is sharp for n≤5 and the stadium construction realizes it | This exact family calibrates conventions; it does not transfer to arbitrary links. |
| `T(Q,Q)` torus links (Q components; Q≥3) | For Q≤6, `Q(4π+2(Q−1))` from CKS’s disk-hull theorem; Klotz gives a Wegner formula for all Q in the p=1 case, [Klotz (2026), §II](https://arxiv.org/html/2603.02416v2#S2) | Parameter-free helical construction `<13.39 C^(3/4)`; `11.68 C^(3/4)` uses a conjectural approximation; numerical tightening for Q≤20 | For `T(pQ,Q)`, each component links the other Q−1 components with total linking p(Q−1). CKS Theorem 10 (published numbering; Theorem 3.5 in arXiv HTML) applies directly only when the Q−1 punctures can be represented by disjoint unit disks. Klotz explicitly warns the Wegner extension may fail for p>1. | The true `T(Q,Q)` infimum and sharp asymptotic coefficient remain unknown; Klotz’s lower hull is unattainable as a whole link, which affects sharpness, not the stated p=1 implication. |
| `T(pQ,Q)`, p>1 | Safe CKS isoperimetric bound `L>2πQ(1+sqrt(p(Q−1)))` (radius-one); do not silently promote Klotz’s Wegner formula | Helical/toroidal constructions in Klotz’s earlier and 2026 work | CKS Theorem 11 (arXiv Theorem 4.1) uses only total signed linking number. The stronger disk-packing argument requires the needed punctures to be disjoint; Klotz says this is not guaranteed for p>1. | Establish the missing puncture/disjoint-disk lemma or retain only the isoperimetric lower in software. |
| Prime families with linear growth | Any realization has `L=Ω(c)` for the prime family in [Diao--Ernst--Thistlethwaite (2003)](https://doi.org/10.1142/S0218216503002615) | No matching universal sharp constant | Constructed prime knots; theorem is family-specific | Does not say every prime family is linear, nor identify tight configurations. |
| Families with 3/4≤p≤1 | Not a universal lower for each family | There exist infinite families with `L=O(c^p)`, [Diao--Ernst (2004)](https://www.math.uncc.edu/preprint/2003/2003_04.pdf); CKS give `T(k,k−1)` examples with `c^(3/4)` scaling, [Nature (1998)](https://doi.org/10.1038/32558) | Constructive/topological families; `O(·)` is an upper-growth statement | “Realizable exponent” is not an exact asymptotic equality; constants and finite-c minima remain open. |

## What the classical papers actually establish

**Gonzalez--Maddocks.** Gonzalez and Maddocks, [PNAS 96 (1999),
4769--4773](https://doi.org/10.1073/pnas.96.9.4769), define the global radius
of curvature as the infimum of circumradii over all triples and define
thickness as the minimum of local curvature radius and half the doubly
critical self-distance. Their thickness is a tube **radius**. The paper’s
constant-global-radius observation is a necessary condition for an ideal
shape (away from straight pieces), not an existence, uniqueness, or global
minimality theorem.

**Existence and regularity.** Cantarella--Kusner--Sullivan (CKS), [Inventiones
150 (2002), 257--286](https://doi.org/10.1007/s00222-002-0234-y), prove that
every tame link type has a ropelength minimizer and that every minimizer is
(C^{1,1}) with bounded curvature. Their Lemma 1.1 identifies thickness with
the minimum of curvature radius and half the doubly-critical self-distance;
Lemma 1.3 identifies it with reach/normal injectivity radius. The result is
existence and regularity, not a computable formula for a given knot.

**CKS disk-hull and linking theorems (hypotheses matter).** In the arXiv
HTML, the published paper’s Theorem 10 appears as Theorem 3.5. For a
unit-radius-thickness link, if one component (K) has the other components
partitioned into (n) sublinks, each sublink topologically linked to (K),
then

\[
\operatorname{Len}(K)\ge 2\pi+P_n,
\]

where (P_n) is the minimum perimeter of a planar curve enclosing (n)
pairwise disjoint unit disks. This is stronger than a mere linking-number
count when (n\le5), where (P_n=2\pi+2n). It depends on actual disjoint
punctures of a cone, obtained from the topological-linking hypothesis.

CKS Theorem 11 (arXiv Theorem 4.1) is weaker but more general: if (J) is
any union of other components and (\operatorname{Lk}(J,K)) is the chosen
orientation’s total linking number, then

\[
\operatorname{Len}(K)\ge2\pi+2\pi\sqrt{\operatorname{Lk}(J,K)}.
\]

It is a signed-flux argument and does not supply (n) disjoint unit disks.
For (T(pQ,Q)), the safe substitution is
\(\operatorname{Lk}=p(Q-1)\), giving the isoperimetric bound in the table.

**Klotz’s 2026 (T(Q,Q)) audit.** Klotz’s [arXiv:2603.02416v2](https://arxiv.org/html/2603.02416v2)
states that (T(pQ,Q)) has (Q) components and each component links the
other (Q-1) with total linking (p(Q-1)). For (p=1), CKS Theorem 10
does apply with (n=Q-1): each singleton other component is a linked
sublink, so CKS gives a genuine lower bound by (P_{Q-1}). Replacing the
unknown (P_N) by a proved lower bound (W(N)) for the convex-hull packing
perimeter gives a genuine lower bound for the link class. The lower bound
does not require the minimizing hull to be realizable simultaneously by all
components. Klotz correctly flags that non-realizability prevents equality
and that finite-(N) Wegner values can be non-optimal.

For (p>1), however, Klotz explicitly says the formal Wegner derivation may
not apply: CKS’s cone argument guarantees signed/intersection multiplicity,
not the required collection of disjoint punctures. Treat Klotz’s equation
(8) as a proved (p=1) family lower and as a conditional/model estimate for
(p>1) until that missing topological-geometric step is supplied. Equation
(2), from CKS Theorem 11, remains the rigorous (p>1) fallback.

**Crossing-number frontier.** Buck’s [four-thirds law](https://doi.org/10.1038/32561)
and Buck--Simon’s thickness paper prove the (1.105,c^{3/4}) lower in the
radius convention. Diao’s 2003 quadratic bound is stronger at small and
moderate (c). Diao--Ernst--Por--Ziegler prove a general (O(c\log^5c)
upper. Diao’s 2024 paper proves a linear lower for alternating **knots**;
its proof and statement should not be generalized to alternating links.

**Criticality is not optimality.** Cantarella--Fu--Kusner--Sullivan,
[Ropelength criticality (2014)](https://arxiv.org/html/1102.3234), give
necessary and sufficient first-order balance/Kuhn--Tucker conditions for
strong criticality under the thickness constraint. The theorem applies to
the stated (C^{1,1})/measure framework and classifies several local
configurations. A balanced numerical conformation can still be a saddle or
local minimum; it is not a proof of the knot-type infimum. They also leave
regularity conjectures (for example, balanced versus regularly balanced) in
general form.

**Rawdon and computation.** Rawdon’s [“Approximating smooth thickness”
(2000)](https://doi.org/10.1142/S0218216500000062) proves convergence of a
correct polygonal thickness model under an inscribing algorithm. Rawdon’s
[“Can Computers Discover Ideal Knots?” (2003)](https://eudml.org/doc/51725),
Ashton--Cantarella--Piatek--Rawdon’s [self-contact computations
(2005)](https://arxiv.org/abs/math/0508248), and subsequent SONO/
gradient-descent work provide feasible candidates and numerical upper
bounds. They do not certify the global smooth minimum unless a separate
geometric certificate is supplied.

## Actionable gaps for the lab

1. Store every bound with an explicit `normalization = radius|diameter` field;
   reject mixed-convention comparisons at parse time.
2. For (T(Q,Q)), implement the CKS (P_{Q-1}) lower for (p=1) and the
   CKS Theorem 11 isoperimetric lower for (p>1). Label the Klotz-Wegner
   (p>1) expression `conditional` until a disjoint-puncture proof exists.
3. Treat constrained-gradient output as a feasible upper candidate. Report
   mesh/inscription error and a separate numerical stationarity score; never
   call it “exact” from criticality alone.
4. Recompute all small-knot gaps in one convention. A reported trefoil value
   near (32.743) is radius-one; the same geometry is near (16.372) in
   diameter-one units.

## Primary references

- [Gonzalez--Maddocks, PNAS 96 (1999), DOI 10.1073/pnas.96.9.4769](https://doi.org/10.1073/pnas.96.9.4769)
- [Cantarella--Kusner--Sullivan, Invent. Math. 150 (2002), DOI 10.1007/s00222-002-0234-y](https://doi.org/10.1007/s00222-002-0234-y) · [arXiv HTML](https://arxiv.org/html/math/0103224)
- [Buck, Nature 392 (1998), DOI 10.1038/32561](https://doi.org/10.1038/32561)
- [Cantarella--Kusner--Sullivan, Nature 392 (1998), DOI 10.1038/32558](https://doi.org/10.1038/32558)
- [Diao, JKTR 12 (2003), DOI 10.1142/S0218216503002275](https://doi.org/10.1142/S0218216503002275)
- [Diao--Ernst--Thistlethwaite, JKTR 12 (2003), DOI 10.1142/S0218216503002615](https://doi.org/10.1142/S0218216503002615)
- [Diao--Ernst, JPJGT 4 (2004), author PDF](https://www.math.uncc.edu/preprint/2003/2003_04.pdf)
- [Denne--Diao--Sullivan, Geom. Topol. 10 (2006), DOI 10.2140/gt.2006.10.1](https://doi.org/10.2140/gt.2006.10.1) · [arXiv HTML](https://arxiv.org/html/math/0408026)
- [Diao--Ernst--Por--Ziegler, JKTR 28 (2019), DOI 10.1142/S0218216519500858](https://doi.org/10.1142/S0218216519500858)
- [Diao, JKTR 29 (2020), arXiv:1901.10663](https://arxiv.org/abs/1901.10663)
- [Diao, Math. Proc. Cambridge Philos. Soc. (2024), DOI 10.1017/S0305004124000288](https://doi.org/10.1017/S0305004124000288)
- [Rawdon, JKTR 9 (2000), DOI 10.1142/S0218216500000062](https://doi.org/10.1142/S0218216500000062)
- [Ashton--Cantarella--Piatek--Rawdon, arXiv:math/0508248](https://arxiv.org/abs/math/0508248)
- [Cantarella--Fu--Kusner--Sullivan, Geom. Topol. 18 (2014), DOI 10.2140/gt.2014.18.1973](https://doi.org/10.2140/gt.2014.18.1973) · [arXiv HTML](https://arxiv.org/html/1102.3234)
- [Klotz, arXiv:2603.02416v2 (2026)](https://arxiv.org/html/2603.02416v2)

Audit limit: this file records sources located and checked through the
requested cutoff. It is not a claim that no later preprint exists, nor a
substitute for rechecking a paper’s final journal pagination or any erratum.
