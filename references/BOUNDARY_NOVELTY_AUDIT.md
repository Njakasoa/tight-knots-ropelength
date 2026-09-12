# Focused novelty audit — block boundary correction

Cutoff: 12 September 2026. Audit date: 13 September 2026. Scope: Theorem 003's
uniform first correction for equal-population staggered toroidal shell blocks.
This is a bounded primary-source comparison, separate from the mathematical
PASS in `proofs/ADVERSARIAL_REVIEW_003.md`. No publication or external contact
was made. Existing broader construction context is in `FOCUSED_NOVELTY_AUDIT.md`.

## Verdict

**POSSIBLY NOVEL, provisional, for the exact geometry-specific correction and
its uniform error estimate.** No inspected source gives this particular
staggered-block expansion with these coefficients and remainder. That negative
finding does not establish priority over all literature.

**KNOWN for the reciprocal-versus-linear balancing principle and square-root
optimizer.** The closest prior helix paper already uses precisely that algebraic
pattern. A broad claim to discovering square-root optimization of concentric
helical arrangements would therefore be misleading. The potential contribution
is an exact asymptotic refinement of the specified construction, best presented
as a companion result to its geometry and clearance theorem.

## Direct antecedent in the closest paper

Klotz–Thompson's 2025 paper considers equal populations across concentric shells.
In its arXiv v1 §V, Eq. (17), the ropelength-per-crossing upper expression is

```
L_beta/C < 2*pi*S/Q + 4/S,
```

where S denotes their total shell count (renamed here to avoid confusing it
with our T). They minimize at S=sqrt(2Q/pi), obtaining Eq. (18). This is an
explicit reciprocal-plus-linear balance in the same helix-packing research
program, not merely a distant analogy. Their S and Q differ from our block
length b and total shell count T; their expression controls a leading model
bound, whereas ours refines a fixed limiting coefficient. Their later infilling
and integer-shell discussion also predate this project. The paper does not give
the exact correction audited here. [Klotz–Thompson 2025, §V, Eqs. (14)–(19)](https://arxiv.org/html/2504.00861v1#S5),
[published article](https://doi.org/10.1098/rspa.2025.0319).

Independent of any citation, the identity

```
a/c+d*c-2*sqrt(a*d) = (sqrt(a/c)-sqrt(d*c))^2
```

shows that the optimizer sqrt(a/d) follows immediately once a,d>0 have been
established. That elementary minimization is not a substantive standalone
novelty claim. The scientific work lies in deriving the applicable expansion.

## Narrow statement not found in the inspected sources

The potential new result concerns the explicitly admissible geometry with
within-block radial gap sqrt(3), boundary gap 2, alternating half-grid phase,
and population fixed at each block's innermost capacity. With the project's
n,e,q0,l0 and J=integral(n'e), its statement is

```
F(T,b)=alpha2*[1+a/b+d*b/T
              +O(b^-2+(b/T)^2+T^-1)],
a=1/sqrt(3)-1/2,
d=3*n(1)/(4*q0)-J/(2*l0),
```

uniformly as b→infinity and b/T→0, including integer floors and incomplete
terminal blocks. These details are the candidate distinction:

- The enlarged gaps between blocks change the mean radial spacing to
  lambda=sqrt(3)+(2-sqrt(3))/b, producing the exact coefficient a.
- Population locking changes both total strand count and length. Its net
  normalized correction is d; keeping only population loss would miss the
  weighted term involving J. The derivative in J is n'e, not (ne)'.
- The remainder controls the incomplete block, the actual ceiling-defined
  outer radius, integer population floors, and crossing-number normalization.
- Positivity of d is proved analytically; fixed-c optimization therefore has
  a rigorous basis without inferring a sign from fitted data.

These are claims about this construction. Since its total component count
varies with T and b, the optimum is not an equal-component-count comparison.
It does not yet establish the asymptotics of the exact finite integer argmin
across every possible block schedule, or a subleading all-M ropelength bound.
A fitted exponent or agreement of finite winners with c*sqrt(T) is supporting
numerical evidence, not a separate novelty claim.

## Other primary-source comparisons

| Source inspected | Related established content | Boundary of this audit's comparison |
|---|---|---|
| [Klotz 2026, §III.2–III.3](https://arxiv.org/html/2603.02416v2#S3.SS2), [published DOI](https://doi.org/10.1088/1751-8121/ae862e) | Toroidal length corrections, outer-shell filling effects, integer occupancy adjustments, and common-hole continuum limits. | The paper already studies finite-size efficiencies. Its discussed corrections are not this repeated-block gap/population-locking expansion, and the inspected text supplies no a/b+d*b/T formula for staggered blocks. Its occupancy-based asymptotic claim retains a stated no-overlap assumption. |
| [Starostin 2006, author repository](https://discovery.ucl.ac.uk/id/eprint/1762/), [DOI](https://doi.org/10.1088/0953-8984/18/14/S04) | Hexagonal packing of curved rods, closure constraints, toroidal arrangements and elastic energy. | Strong prior context for curved hexatic bundles; neither its stated scope nor the earlier local full-text audit identifies the present discrete block correction. This turn reopened the repository record; its PDF tool request failed, so this is not a new full-text exclusion. |
| [Atkinson–Santangelo–Grason 2019, primary manuscript record](https://arxiv.org/abs/1902.06325), [DOI](https://doi.org/10.1088/1367-2630/ab1c2d) | Equidistant filament families and spacing variation in bent/twisted toroidal bundles. | Relevant geometry of packing frustration, distinct from locking integer populations in radial blocks. The primary abstract was inspected; full-text retrieval failed in this turn, so no exhaustive negative claim about its equations is made. |
| [Connelly–Funkhouser–Kuperberg–Solomonides 2016, v2 record](https://arxiv.org/abs/1512.08762v2) | Boundary-related convergence of disk-packing density: planar-square error of order N^-1/2 versus order N^-1 in their flat square-torus examples. | Confirms that square-root finite-size penalties in packing are established context. Its flat two-dimensional quotient is not the embedded three-dimensional toroidal helix construction; it supplies no identified match to the coefficients here. Abstract-level scope check. |
| [Bagchi 2026, v1 full text](https://arxiv.org/html/2603.27485v1) | Thickness-controlled and interaction-registry mechanisms for helix formation; bending/contact energies and morphological crossovers. | A current primary preprint surfaced by commensurability searches. Its inspected section structure and models concern physical polymer stabilization, not a ropelength correction for equal-population toroidal shell blocks. No matching theorem identified. |

“Boundary correction” is broad terminology. Elastic shell boundary layers,
thermal-fluid helical tubes and protein helix packing appeared in search results
but concern different objects and objectives; they were not treated as evidence
for or against this mathematical theorem. No secondary summary was used as the
basis for the direct antecedent identified above.

## Search and version record

The main fresh full-text comparisons used arXiv:2504.00861v1, §V and its
neighboring construction/closure sections, and arXiv:2603.02416v2, §III.2–III.3.
The publication DOIs are supplied as bibliographic records; equation numbering
above refers specifically to the inspected arXiv versions. The local Klotz PDFs
and hashes are recorded in `papers/DOWNLOAD_MANIFEST.json`. Primary records were
checked for source dates; search-engine crawl labels were not used to decide
whether a paper met the cutoff.

Queries included the following combinations, followed by inspection of primary
hits or exclusion of obviously unrelated fields:

- `ropelength torus links shells equal populations blocks boundary correction square root`
- `"concentric helices" "equal" shells`
- `"concentric helices" "blocks"`
- `"ropelength" "boundary correction"`, `"ropelength" "first correction"`
- `"ropelength" "block size"`, `"ropelength" "equal-population" block`
- `"toroidal" "staggered" "shells"`
- `"helical packing" "commensurate"`
- `"packing" "boundary" "square-root" filaments`
- `"helical bundles" "boundary layer"`, `"toroidal bundles" "finite size"`

No matching exact expansion was identified. Search terms can miss differently
named constructions, theses, supplements, nonindexed work or prior calculations
embedded in another argument. This audit therefore does not upgrade the result
to STRONG NOVELTY EVIDENCE or claim first publication.

## Appropriate local-candidate language

A defensible contribution statement is:

> We derive a uniform first-correction expansion for an explicit staggered
> toroidal-shell construction and determine its optimal constant in the
> block-size regime b=floor(c sqrt(T)). The balancing mechanism has a direct
> antecedent in concentric-helix bounds; the proposed contribution is the
> geometry-specific coefficients and the uniform treatment of discrete blocks.

The local manuscript should cite the direct Eq. (17) antecedent next to the
block-size discussion. It can report the mathematical PASS separately from
this provisional novelty assessment. “New square-root law,” “optimal helical
packing,” “best possible block schedule,” and a numerical priority record would
all exceed the evidence. Theorem 003 is potentially a useful rigorous refinement
of Theorem 002, whose construction novelty remains separately provisional.
