# Provisional target and three controlled generalizations

Initial target selection was prepared before M1. M1 now passes and M2 searches
have run; see M2_DISCOVERY.md. Current source and
normalization details are in STATE_OF_THE_ART.md and references/RECENT_TORUS_AUDIT.md.

| Target | Gap and structure | First decision |
|---|---|---|
| T(Q,Q) | Family lower coefficient sqrt(8πsqrt3)≈6.598; published shell coefficient13.38, conditional optimized11.68. Explicit full-twist geometry and length integrals. | Highest priority: all-Q constructions with continuously proved clearance. |
| T(pQ,Q), p>1 | More closure freedom, but disk-hull strengthening cannot count linking multiplicities as separate disks automatically. | Second stage after p=1; use safe CKS bound initially. |
| Alternating T(2,q) | Linear crossing-number lower bounds imply the c^(3/4)-normalized ratio grows; different asymptotic target. | Useful numerical controls, lower priority for a finite3/4 coefficient. |
| Non-alternating torus knots | Rich nested helical structure, less simple closure and knot-type checks. | Preserve data and compare after torus-link proof infrastructure. |
| Selected small knots | Trefoil gap between general31.32 lower and numerical≈32.74 upper; contact patterns available. | Controls and contact studies; exact minimum currently less tractable. |

The choice is based on proofability and available geometry, not simply gap size.
A new upper construction restricts sufficient filament length for existence; a
lower bound restricts necessary length. Neither proves a physical energy minimum.

The inspected constructions fix circular torus cross-sections, uniform angular
speed/pitch, discrete shell radii with radial spacing2, common angular clearance
based on the outer shell's inner torus radius, equally spaced same-shell phases,
mostly uncoordinated phases across unequal shell populations, and a conservative
major radius/closure envelope. Some of these protect the topology or clearance;
releasing them requires new arguments.

Three minimal releases:

1. Use each shell's own inner radius in its population constraint. All geometry
   stays unchanged; THEOREM_001 proves its conservative capacity and clearance.
2. Lock populations within growing blocks and alternate half-step phases. Reduce
   within-block radial spacing to sqrt3, retain spacing2 at block boundaries.
   THEOREM_002 proves separation and controls the subleading population loss.
3. Keep the topological full twist and optimize the outer few shell radii,
   populations and phases under exact continuous pair-separation constraints.
   Treat the major radius and boundary gaps as variables. This remains a proposal;
   numerical feasibility alone will not be promoted to a bound.

A variable-pitch release requires a periodic monotone phase map with total one
turn, common control of closure, and a fresh curvature/DCSD proof. It is a later
extension, not a harmless free parameter. Elliptical deformation similarly
preserves topology for a positive ambient scaling but changes the reach proof.

Initial bounded parameter optimization on ordinary torus embeddings has run;
see INITIAL_PARAMETER_SEARCH.md. The shell-family experiments reproduce the
common-hole model and both new capacity rules with interval lengths. The exact recent-paper contact comparison and independent M1 review now pass;
see M1_REVIEW.md. The current target retains a known lower coefficient near6.598
and a certified constructive upper coefficient below10.614, without proving equality.

Physical interpretation is made explicit in proofs/PHYSICAL_INTERPRETATION.md:
T(M,M) hasM separate closed filaments, and the upper theorem bounds sufficient
total contour length, while the lower theorem bounds necessary total length.
It is not automatically a statement about one knotted molecular chain.
