# Universal versus family-specific coefficient map

Convention: thickness is radius; sum component lengths. Sources and exact
hypotheses are audited in references/CLASSICAL_FRONTIER.md and
references/RECENT_TORUS_AUDIT.md. This map makes no unqualified best-in-all-
literature assertion beyond that bounded primary-source audit.

| Statement | Audited information | Effect of this project |
|---|---|---|
| Universal crossing lower bound | Buck/Buck–Simon baseline coefficient (4π/11)^(3/4)≈1.105 in the audited radius convention; other bounds can dominate for particular crossing ranges/classes | No improved universal lower coefficient proved |
| Alternating knots | Linear lower bounds change the asymptotic scale; do not silently extend knot hypotheses to all links | Not the targeted finite c^(3/4) coefficient family |
| Full-twist links T(M,M) | Known convex-hull/packing lower leading coefficient sqrt(8πsqrt3)≈6.598, with the p=1 disjoint-puncture hypothesis | New explicit construction gives limsup≤alpha2<10.614 |
| T(pQ,Q), p>1 | CKS safe bound2πQ(1+sqrt(p(Q−1))); stronger multiplicity-to-disjoint-disk step is not established by the inspected argument | No new p>1 lower theorem |
| All links, hypothetical best universal coefficient | Any proven explicit family gives an upper restriction on a coefficient required to hold for every link | Our family implies such a coefficient is at most alpha2; we do not claim this improves all known obstruction families |
| Knots only, hypothetical best universal coefficient | A multi-component T(M,M) family does not by itself constrain a knots-only constant | No knots-only obstruction follows without an additional controlled connection construction |

For the full-twist family, the justified asymptotic interval is

    sqrt(8πsqrt3) ≤ liminf Rop(T(M,M))/[M(M−1)]^(3/4)
                  ≤ limsup Rop(T(M,M))/[M(M−1)]^(3/4) ≤ alpha2 <10.614.

This does not prove the limit exists, asymptotic equality, or sharpness. The
leading lower coefficient is known; the correction audit in
proofs/WEGNER_EXPANSION_AUDIT.md prevents using a rounded subleading term or
an unknown-sign remainder as a finite inequality.

A finite numerical coefficient around10.02 in another published family is
not automatically a rigorous obstruction or a competing all-integer asymptotic
theorem. Conversely our10.614 is not a finite-M inequality with the same
coefficient. Every comparison must retain family, quantifier and proof level.

The first target remains T(M,M): it combines a substantial known gap, exact
full-twist topology and continuously certifiable separation. Its physical
meaning is several closed thick filaments and total contour length. An upper
construction gives sufficient length; a lower bound gives necessary length.
