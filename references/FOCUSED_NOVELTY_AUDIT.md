# Focused novelty audit: doubled toroidal-shell families

**Cutoff:** 12 September 2026. **Scope:** primary-source comparison for the
candidate all-integer $T(Q,Q)$ construction in
[`proofs/THEOREM_001.md`](../proofs/THEOREM_001.md) and
[`proofs/THEOREM_002.md`](../proofs/THEOREM_002.md). This is a bounded literature
audit, not an exhaustive search or a novelty determination by a publisher.

## Finding

No inspected primary source reproduces the candidate's full combination of

1. the exact $p=1$ concentric toroidal-helix model with a shell-dependent
   inner-hole parameter $h_i=R-r_i$;
2. equal-population blocks whose adjacent shells are shifted by a half phase
   $\pi/N$, allowing radial gap $\sqrt3$ inside a block and gap $2$ at
   block boundaries; and
3. the resulting explicit doubled full-twist $T(Q,Q)$ all-integer limsup
   passage with candidate coefficient
   $\alpha_2=\sqrt{\sqrt3/2}\,\alpha_1\approx10.6135570633$.

The correct status is **POSSIBLY NOVEL, provisional**. The search supports a
focused claim about this exact construction after the recorded proof,
implementation, and interval reviews. A no-hit search cannot prove that the
combination has never appeared, and the candidate should not be described as a
global optimum, a universal obstruction, or a record for all torus links.

The local exact geometry and subsequent independent implementation/Arb reviews
now pass. The certified outward bound is α2<10.614; the approximate decimal
10.6135570633 is still diagnostic. See proofs/CERTIFICATE_IMPLEMENTATION_REVIEW.md.
These mathematical checks do not strengthen the publication novelty verdict.

## What the candidate actually adds

Theorem 001 takes $r_i=2i$, $R=4T+2$, and uses

\[
h_i=R-r_i,
\qquad
N_i=\left\lfloor\frac{\pi r_i h_i}{\sqrt{r_i^2+h_i^2}}\right\rfloor-1.
\]

The same-shell toroidal distance identity gives the population rule, while
shells separated by $2$ have clearance $2$. The entire bundle is doubled by
the explicit proper Hopf-core motion and identified with a full twist, giving a
candidate $T(M,M)$ family. Its formal coefficient is

\[
\alpha_1=\frac{l_0}{\sqrt2\,q_0^{3/2}}\approx11.4050092899.
\]

The potentially differentiating point is that $h_i$ is evaluated for the
actual shell. This is a shell-specific capacity rule, rather than the common
inner-hole parameter used in Klotz's optimized construction below.

Theorem 002 groups consecutive shells into blocks of size
$b=\lfloor\sqrt T\rfloor$. Within one block all shells have the same
population $N$, and successive shells alternate phase $0,\pi/N$. Thus every phase difference between
adjacent shells within a block is an odd multiple of $\pi/N$. The harmonic
lower bound then supplies more than one unit of squared transverse clearance;
with radial squared gap $3$, the Euclidean centerline distance exceeds $2$.
The block boundary is given radial gap $2$, where the ordinary radial bound is
used. The proof then deletes excess components from the least larger finite
construction and claims the all-integer limsup. The formal rescaling is

\[
\alpha_2=\sqrt{s}\,\alpha_1,
\qquad s=\sqrt3/2,
\]

with the diagnostic value $10.6135570633$.

Equal shell populations alone are prior art; the focused candidate claim is the
phase lock, the $\sqrt3$ spacing inequality, and its integration into this
full-twist all-$Q$ construction.

## Closest primary sources and exact boundary

| Primary source | What it establishes | Exact distinction from the candidate |
|---|---|---|
| [Klotz, *J. Phys. A* (2026), DOI 10.1088/1751-8121/ae862e](https://doi.org/10.1088/1751-8121/ae862e); [arXiv:2603.02416v2 full text](https://arxiv.org/html/2603.02416v2), §III.1–III.3, Eqs. (9)–(23), Appendix VII.2 Eqs. (26)–(36) | Gives the same $p=1$ toroidal helix equation and same-shell no-overlap condition (Eq. 10); concentric shells are separated radially by at least $2$. It discusses doubling a bundle through the torus hole to obtain $T(2Q,2Q)$. Its optimized shell model uses radii $2i$, a common hole parameter $h=2T$, shell capacity $N_a=h\pi r/\sqrt{h^2+r^2}$, and reverse-Jenga/outer deletion. | Klotz's optimized capacity uses one common $h$ for all shells; it does not state the candidate's $h_i=R-r_i$ capacity rule. It does not give the candidate's equal-$N$ blocks, $\pi/N$ alternating phase, $\sqrt3$ inter-shell gap, or the candidate's quantified all-integer block-deletion argument. Klotz's doubling operation is prior art, so doubling alone is not novel here. |
| [Klotz–Thompson, *Proc. Roy. Soc. A* (2025), DOI 10.1098/rspa.2025.0319](https://doi.org/10.1098/rspa.2025.0319); [arXiv:2504.00861](https://arxiv.org/abs/2504.00861), §§IV–VI (the inspected article PDF), Eqs. (8), (11), (14), and (23)–(24) | Develops concentric multihelices around a central rod, shell separation $2$, finite shell compositions, equal-population shell variants, increment-4/5 infilling, and reverse-Jenga removal. It bends constructions into torus links, with the headline large construction mainly for $T(3Q,Q)$. | Equal populations, concentric shells, shell gap $2$, and deletion are not candidate novelties by themselves. The paper does not state a half-phase $\pi/N$ stagger between equal adjacent shells, does not use the candidate's sub-$2$ radial gap $\sqrt3$ clearance lemma, and does not give this doubled all-$Q$ $T(Q,Q)$ theorem or coefficient. |
| [Olsen–Bohr, *New J. Phys.* 14 (2012) 023063, DOI 10.1088/1367-2630/14/2/023063](https://doi.org/10.1088/1367-2630/14/2/023063), §2 Eqs. (2)–(3), §5, §6 | Provides the earlier circular/toroidal helix parametrizations and analyzes contacts and packing for general $N$, including zero-twist limits. | It is prior art for toroidal-helix geometry and contact analysis, but does not present the candidate's concentric multi-shell capacity asymptotics, equal-population block staggering, Hopf-doubled $T(Q,Q)$ limsup, or coefficient. It supplies no basis for calling those older toroidal-helix ingredients new. |
| [Huh et al., *J. Phys. A* 49 (2016) 415205, DOI 10.1088/1751-8113/49/41/415205](https://doi.org/10.1088/1751-8113/49/41/415205) | Proves the unique ropelength-minimizing θ-spun double helix and derives its exact transcendental contact equation. | This is a same-shell/double-helix result. It is relevant precedent for exact phase/contact constraints, but contains no multiple-shell block construction, shell-specific hole capacity, or all-$Q$ doubled torus family. |
| [Starostin, *J. Phys.: Condens. Matter* 18 (2006) S187–S204, DOI 10.1088/0953-8984/18/14/S04](https://doi.org/10.1088/0953-8984/18/14/S04); [open manuscript record](https://discovery.ucl.ac.uk/id/eprint/1762/) | Studies perfect hexagonal packing of curved rods, including closed/cycled and toroidal-like bundles; closure acts through automorphisms of the cross-sectional hexagonal lattice. | This is the strongest warning against a broad “nested toroidal/hexagonal packing is new” statement. Its bundles are a perfect hexatic rod packing with closure constraints and elastic-energy analysis, not the candidate's discrete circular toroidal helices with shell-dependent populations, $\pi/N$ phase offsets, $\sqrt3$ radial spacing, or ropelength $T(Q,Q)$ coefficient. No matching candidate theorem was found in the inspected text. |
| [Pereira–Williams, *Europhys. Lett.* 50 (2000) 559–564, DOI 10.1209/epl/i2000-00306-3](https://doi.org/10.1209/epl/i2000-00306-3) | Analyzes a single semiflexible polymer toroidal globule with hexagonally ordered packing, closed shells, circuit-number jumps, and major-radius transitions. | It concerns one polymer chain/spool and an energetic toroidal-globule model, not a multi-component thick link, toroidal-helix phase matching, Hopf doubling, or the candidate's asymptotic coefficient. “Closed hexagonal toroidal shells” should be treated as prior language. |
| [Starostin, *A formula for the minimal coordination number of a parallel bundle* (2008), DOI 10.1063/1.2991413](https://doi.org/10.1063/1.2991413); [arXiv:0810.0976](https://arxiv.org/abs/0810.0976) | Gives exact coordination/shell counts for parallel rod bundles, including hexagonal and square lattices. | It is a discrete parallel-bundle result, not a toroidal-helix clearance or link-rope-length theorem. It does not supply the candidate's cross-shell harmonic phase bound or block/all-$Q$ construction. |
| [Atkinson–Santangelo–Grason, *Constant spacing in filament bundles* (2019), arXiv:1902.06325](https://arxiv.org/abs/1902.06325) | Shows the geometric frustration of simultaneously bent and twisted bundles and studies longitudinal spacing variation in twisted toroidal bundles. | It is a continuum spacing/metric analysis, not a discrete unit-thickness toroidal-link construction. It is useful context for why the candidate needs a clearance inequality, but does not disclose the candidate's capacity or block rule. |

## Known versus potentially differentiating ingredients

The following ingredients are established before this project: circular and
toroidal helix parametrizations; same-shell phase/contact minimization;
concentric shell constructions; a radial clearance-(2) rule; shell population
optimization in a common-hole model; equal-population shell variants; deletion
of outer strands; hexagonal/closed toroidal rod-bundle language; and torus-hole
doubling ideas. The candidate should describe these as inherited geometry or
context.

The potentially differentiating mathematical combination is narrower:

- evaluating the capacity with the actual $h_i=R-r_i$ of each shell in this
  exact $p=1$ toroidal family;
- locking equal adjacent populations and alternating their phases by exactly
  $\pi/N$, so the nearest phase mismatch is controlled uniformly;
- proving that this mismatch pays for reducing the radial gap from $2$ to
  $\sqrt3$, with gap $2$ retained at block boundaries; and
- carrying those finite blocks through a quantified all-integer deletion/
  limsup argument for the doubled full twist.

The searched papers do not report this exact combination. That supports
“possibly novel construction” after the remaining checks, not “first ever” or
“new optimal record.”

## Conditional comparison and proof-status flags

Klotz 2026's optimized numerical value near $11.68$ is **conditional**. In
§III.3 and Appendix VII.2, the paper derives a cubic approximation to the exact
transcendental no-overlap equation and explicitly makes the asymptotic claim
conditional on that approximation not producing overlaps. The reported tests
go to $T=100$, $Q=52,203$, with sampled points per helix; they are not a
proof of the full transcendental constraint. The candidate audit must preserve
that assumption whenever it compares against (11.68).

Theorem 002's geometry, topology, all-integer limiting argument and subsequent
independent implementation/Arb review pass. The certified bound is $<10.614$.
The numerical and analytic review evidence is separate from this prior-art
audit. The finite published numerical value around $10.02$ belongs to a
different torus configuration and to the discussion of limits on a purported
universal obstruction; it is not a proof of a universal obstruction and neither
certifies nor invalidates the candidate's asymptotic constructive bound.

## Search record and limits

The bounded search used the DOI/publisher records and primary full texts or
author/arXiv manuscripts above, with queries combining `toroidal helix`,
`nested toroidal helix`, `concentric toroidal shells`, `hexagonal packing`,
`equal population`, `phase stagger`, `half phase`, `T(Q,Q)`, and `ropelength`.
The local PDFs [`papers/klotz-2026-v2.pdf`](../papers/klotz-2026-v2.pdf) and
[`papers/klotz-thompson-2025.pdf`](../papers/klotz-thompson-2025.pdf) were read
alongside the linked texts. No source was found that states the complete
candidate theorem. This is negative evidence with a finite scope; it is not a
proof of absence from all literature, preprints, theses, unpublished notes, or
future publications.

## Audit conclusion

The novelty log may safely record the candidate as **POSSIBLY NOVEL,
provisional** at the level of the exact combined construction. It should cite
Klotz 2026 as the closest ropelength construction and explicitly distinguish its
common-$h$, conditional $11.68$ model from the candidate's shell-specific
$h_i$, staggered blocks, $\sqrt3$ spacing, and all-$Q$ proof. It should cite
Olsen–Bohr, Huh et al., Starostin, and Pereira–Williams as prior geometry and
packing context, and should avoid any global universal obstruction or record
claim.
