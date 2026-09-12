# Ropelength normalization ledger

The literature uses “thickness” for either a tube radius or a tube diameter.
The quotient changes by exactly two. This ledger is the canonical convention
for the Tight Knots Lab.

## Definitions

For a (C^{1,1}) embedded curve (K), let

\[
r(K)=\operatorname{reach}(K)
 =\min\left\{\frac1{\kappa_{\max}(K)},
                 \frac{\operatorname{dcsd}(K)}2\right\},
\]

where `dcsd` is the infimum of doubly-critical self-distance. Gonzalez--
Maddocks and Cantarella--Kusner--Sullivan use this radius quantity. For a
curve of length (ell), define

\[
 R_{\rm rad}=\frac{\ell}{r(K)},\qquad
 R_{\rm diam}=\frac{\ell}{2r(K)}=\frac12R_{\rm rad}.
\]

The underlying geometric curve is unchanged; only the unit used to report
the tube size changes.

| Name in this ledger | Unit tube | Curvature cap | Critical separation | Reported quotient |
|---|---:|---:|---:|---:|
| **radius-one** | radius (r=1), diameter (2) | (kappa\le1) | distance (ge2) | (R_{\rm rad}=\ell) |
| **diameter-one** | diameter (2r=1), radius (1/2) | (kappa\le2) | distance (ge1) | (R_{\rm diam}=\ell) |

Conversion is therefore

\[
R_{\rm rad}=2R_{\rm diam},\qquad
R_{\rm diam}=R_{\rm rad}/2.
\]

Crossing number, knot type, linking number, and all dimensionless topology
are unchanged. A bound written as (a\,c^p) has coefficient (a) doubled
when moving from diameter-one to radius-one.

## Source audit

- **Gonzalez--Maddocks (1999).** Their (η) is the largest embedded normal
  tube **radius** and is the minimum of local radius of curvature and half
  the doubly-critical distance. Their “ideal shape” calculations are
  radius-normalized.
- **CKS (2002).** Their (τ(L)) is the normal injectivity radius/reach;
  “unit thickness” means the unit-radius tube. Their main universal knot
  lower bound is therefore (2\pi(2+\sqrt2)=21.45\ldots).
- **Denne--Diao--Sullivan (2006).** They explicitly define thickness as twice
  the infimal circumradius and say that for a (C^1) curve it is the
  supremal **tube diameter**. Their “unit thickness” means diameter one,
  curvature at most two. Their universal alternating-quadrisecant lower
  `15.66…` is diameter-one.
- **Cantarella--Fu--Kusner--Sullivan (2014).** Their ropelength problem is a
  diameter-one tube; the reach is at least (1/2). Any number quoted from
  that paper is diameter-one unless explicitly rescaled.
- **Diao (2003),** in the disk-thickness formulation, uses unit tube radius
  (diameter two). The theorem (L(L-17.334)\ge16\pi\,\mathrm{Cr}) and
  (L>24) are radius-one. This is why older papers quote the same universal
  trefoil lower as (>12) in diameter-one units.
- **Klotz (2021, 2026)** writes “unit-thickness tube” while using centerline
  separation (2) in the construction equations; the tabulated values and
  coefficients are radius-one. Verify against the source equation before
  importing any individual data value.

## Sanity conversions

| Statement in source convention | Radius-one form | Diameter-one form |
|---|---:|---:|
| CKS universal knot lower | 21.45… | 10.726… |
| Denne--Diao--Sullivan alternating-quadrisecant lower | 31.32… | 15.66… |
| Diao crossing theorem universal (L>24) | (>24) | (>12) |
| Diao crossing theorem | (L(L-17.334)\ge16\pi c) | (L(L-8.667)\ge4\pi c) |
| Numerical trefoil near (32.743) | (32.743) | (16.3715) |
| CKS Hopf chain ((4\pi+4)k-8) | as written | (((4\pi+4)k-8)/2) |

Do not infer that a value near 10.7 “beats” 21.45: those are the same CKS
bound under diameter and radius normalization.

## Circumradius versus tube radius

For three non-collinear points (x,y,z), let (ho(x,y,z)) be the
circumradius. Gonzalez--Maddocks define the global radius of curvature by

\[
\rho_G(x)=\inf_{y,z}\rho(x,y,z),
\]

and the global minimum by the infimum over all triples. At a smooth point,
the coincident-limit value is the local curvature radius (1/\kappa). A
global thickness/tube radius also has the doubly-critical distance term:

\[
\operatorname{thickness}(K)
 =\min\{\inf 1/\kappa,\;\tfrac12\inf\operatorname{dcsd}\}.
\]

Thus the circumradius is a radius, not a diameter; multiplying it by two is
required only when the surrounding tube is reported by diameter. Mixing the
two is the source of several apparent factor-of-two discrepancies in early
quadrisecant and criticality papers.

## Implementation rules

1. Every imported bound must carry `normalization: "radius"` or
   `normalization: "diameter"` and a source URL.
2. Convert only at the boundary of reporting. Keep geometric constraints in
   physical units (`tube_radius`, `min_separation`, `curvature_max`) so a
   radius-one and diameter-one run cannot be compared accidentally.
3. A diameter-one candidate with length (ell) corresponds to the same
   physical shape scaled by two in radius-one coordinates and has reported
   length (2ell). Conversely, divide radius-one lengths by two for
   diameter-one tables.
4. Label numerical or stationary values as `candidate_upper`; reserve
   `rigorous_upper` for an explicitly verified embedded smooth construction.
5. CKS disk-hull bounds use disjoint unit-radius disks in radius-one units.
   If implementing a diameter-one version, the disks have radius (1/2),
   all lengths are halved, and the topological hypotheses are unchanged.

Audit limit: these conversions were checked against the cited primary papers
through 2026-09-12. If a future source changes terminology, preserve the
source’s native value and add a conversion row rather than overwriting it.
