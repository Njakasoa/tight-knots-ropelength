# State of the art — cutoff 12 September 2026

All values in this overview use **tube radius**, with total length for links.
Primary-source details and limitations are in references/CLASSICAL_FRONTIER.md
and references/RECENT_TORUS_AUDIT.md. A bibliography audit is not a proof of
exhaustiveness. Historical bounds below are not automatically current records.

| Object/family | Rigorous lower | Upper / numerical evidence | Optimum? | Method/source | Remaining issue |
|---|---|---|---|---|---|
| Unknot | 2pi | 2pi, exact circle | Yes | Fenchel + explicit geometry; our positive control | Validate implementation |
| Hopf | 8pi | 8pi, round circles | Yes, known | [CKS 2002](https://arxiv.org/abs/math/0103224), disk-hull bound | Independent reproduction |
| Trefoil | General nontrivial-knot bound >31.32 | Tight numerical geometry about 32.74; import exact dataset value separately | Exact minimum not established here | [DDS](https://arxiv.org/abs/math/0408026), [Ashton et al.](https://arxiv.org/abs/math/0508248) | Polygon-to-smooth certificate and source-specific coordinates |
| Nontrivial knots | (4pi/11)^(3/4) c^(3/4), coefficient about 1.105 | General O(c log^5 c) construction | No | [Buck](https://doi.org/10.1038/32561), [Diao et al.](https://doi.org/10.1142/S0218216519500858) | Different asymptotic powers; no universal sharp coefficient |
| Alternating knots | (c+2)/56, per audited Diao statement | General construction bound | No | [Diao 2024](https://doi.org/10.1017/S0305004124000288) | Do not extend knot theorem to all links |
| T(Q,Q), Q=3..6 | Q(4pi+2(Q-1)) | Numerical toroidal/gibbous constructions and Ridgerunner | No | [Klotz 2026](https://doi.org/10.1088/1751-8121/ae862e) building on CKS | Hull lower not simultaneously realizable by all components |
| T(Q,Q), large Q | liminf coefficient >=sqrt(8pi sqrt(3))≈6.598 | Reported construction coefficient ≈13.38; optimized-shell ≈11.68 includes a stated no-overlap assumption | No | [Klotz full text v2](https://arxiv.org/html/2603.02416v2), §II–III | Certify continuous geometry and asymptotic passage |
| T(pQ,Q), p>1 | Safe CKS bound 2pi Q(1+sqrt(p(Q-1))) | Helical constructions, finite numerical searches | No | [Klotz–Thompson 2025](https://doi.org/10.1098/rspa.2025.0319) | Stronger multiplicity-based disk packing needs extra hypothesis |
| Physical filaments | Geometric contour lower r*Rop(type) if hard circular radius r | Elastic/contact equilibria differ from geometric minimizers | Different problem | Recent physical sources in RECENT_TORUS_AUDIT | Do not identify bending/free-energy minimum with ropelength |

## Distinctions that control research decisions

* The quadrisecant paper reports about 15.66 in **diameter** units, hence
  about 31.32 here. Criticality papers also need explicit conversion.
* A numerical configuration can suggest an upper bound, but the smooth
  embedding, topology and thickness must be justified before calling it rigorous.
* The universal coefficient, a family-specific lower bound and the coefficient
  of one constructed family are three different quantities.
* For a link with arbitrarily many split trivial components, crossing number
  alone cannot give the same upper formula without further hypotheses.
* An asymptotic limsup upper bound does not establish an asymptotic equality
  for the true class infimum.

## Most attackable gap: provisional choice

Prioritize continuous certification and shell population constraints for doubled
T(Q,Q) toroidal bundles. They have a controlled braid description, an explicit
length integral and a reported lower/upper coefficient gap about 6.60 to 11.68.
This is more tractable initially than a new universal lower coefficient or
proving the exact trefoil minimum. The current independent proof candidate
releases the common inner-radius constraint; see CLAIM-0001. It remains
unreviewed and is not added to the established results table.

Other torus families introduce closure/puncture multiplicity issues. Alternating
T(2,q) families have linear rather than 3/4 asymptotic scaling, so their normalized
ratio diverges and they are a different target. Small knots offer excellent
controls but a less transparent route to a family theorem.

## Version warning

The 2026 paper has a published July version (J. Phys. A 59, 285201,
DOI 10.1088/1751-8121/ae862e). The audit must record which equations were
read in arXiv v1/v2 and which in the published article. Published numerical
examples may improve on numbers retained in the abstract; they remain
numerical examples and do not certify a universal sharp coefficient.

The printed finite-size decimal `7.61/sqrt(Q)` must not be hard-coded.
Expansion of the exact p=1 ceiling formula gives
`B=2pi+sqrt(2pi*(7sqrt(3)-12))≈7.1671`; see
proofs/WEGNER_EXPANSION_AUDIT.md. Use the original expression for finite Q,
because the asymptotic remainder has not been assigned a sign here.
