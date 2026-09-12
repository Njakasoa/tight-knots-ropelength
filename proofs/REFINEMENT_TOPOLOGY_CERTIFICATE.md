# A certificate for the topology of sampled and refined polygons

Scope: prove the initial and final stored M2 polygons have type T(12,12), up
to a common mirror. This is a sufficient explicit alternative isotopy between
endpoints. It does not certify Ridgerunner's actual numerical path, its
continuous thickness, convergence, criticality or optimality.

The two analytic bundles are already classified by
VARIABLE_PITCH_TOPOLOGY.md and its independent review. This note supplies the
two missing bridges: analytic curve to exact stored polygon, then initial
polygon to final polygon. All decimals in VECT are read directly as exact
rational numbers. JSON parameters and witness axes are decoded as binary64
and then interpreted as exact binary rationals; that choice is explicit.
Arb bounds enclose every proof inequality. Floating optimizers propose
witnesses only.

## 1. Analytic input to sampled polygon

Undo the positive ambient diagonal scaling, and on the second bundle undo
P(x,y,z)=(R+x,-z,y). In the base toroidal coordinates, write

    gamma(u)=E(u,w(u)),   w(u)=r exp(i[u+beta sin(u)-phi]),
    E(u,a+ib)=((R+a)cosu,(R+a)sinu,b).

The core hasr=0. Put L=1+|beta| and h=R-r. Since |theta'|≤L and
|theta''|≤|beta|, the rotating-frame second derivative is bounded by

    |gamma''| ≤ B = R+r+2rL+r(L²+|beta|).

The radial term contributes at mostR+r, the two frame-derivative terms at
most2rL, and the meridional second derivative at mostr(L²+|beta|).
Use48 equally spaced exact parameters u_k=2πk/48. For every exact rational
stored vertex, independently evaluate gamma(u_k) in Arb after the inverse
maps and verify Euclidean error<epsilon=10^-10. This is checked against the
stored coordinates; it is not an assumption about floating accuracy.

Let Delta=2π/48. Linear interpolation between stored vertices differs from
gamma at the linearly interpolated parameter by at most

    eta=B Delta²/8+epsilon.

The standard second-derivative interpolation bound gives the first term;
convexity bounds interpolation of endpoint errors byepsilon. We requireh>eta.
The map (x,y,z)→(sqrt(x²+y²)-R,z) is1-Lipschitz. The longitude drift between
the interpolant and gamma is at mosteta/(h-eta), by integrating the gradient
ofarg along the connecting segment, which stays at radius≥h-eta.
Reparameterizing the polygon by its actual longitude therefore gives a
transverse error bounded by

    e=eta+rL eta/(h-eta).

That reparameterization exists: vertex longitude errors are at most
v=epsilon/(h-epsilon). The certificate checks Delta-2v>0 and
Delta+2v<π. Thus the vertex angles follow the exact cyclic grid once, with
strict increments smaller thanπ. Each projected chord between positive-radius
endpoints has strictly monotone longitude. The entire polygon is therefore
a graph overlongitude, just as the analytic curve is.

At a common longitude, reference fiber points have separations at least
2r_i sin(π/N_i) on one shell, |r_i-r_j| on distinct shells, andr_i from
the core. Independent periodic pitch does not alter these radial lower bounds
or the equal-shell phase differences. Let emax be the maximum of the rigorously
computed upper endpoints, compared as exact endpoints. If every reference
separation is>2emax, linear interpolation of the reference and polygon fiber
points cannot collide. This defines an isotopy of the single bundle.

Throughout that isotopy each bundle stays in its round core tube of radius
rmax+emax. Checking R>2(rmax+emax) keeps the two supporting tubes disjoint.
The two isotopies can run simultaneously. Restore the positive ambient
scaling to obtain the initial stored polygon's full-twist type.

## 2. Initial polygon to final polygon

First apply an arbitrary positive homothety and translation to the initial
polygon. Their exact binary-rational coefficients are frozen in the certificate.
This alignment is itself an ambient isotopy; onlypositive homothety is used,
so no straight-path assumption for a general GL+ matrix is needed.

Match vertices component by component, with the same cyclic indexing and
counts, and move every aligned initial vertex linearly to its exact final
rational vertex. The resulting moving edges are bilinear in time and edge
parameter. For every pair of nonadjacent cyclic edges, including every
intercomponent pair, cover[0,1] by a finite partition of dyadic time cells.
On each cell choose a fixed rational directionn. Every point on the moving
edge lies in the convex hull of its four endpoint/time corners. Consequently
its projection onto n lies between those corner projections.

If the two corner projection intervals are strictly separated, the edges
cannot intersect anywhere in that whole time cell. Arb verifies this strict
inequality using exact rational coordinates, time endpoints andaxis. A
floating closest-segment computation only chooses the axis. Its accuracy is
irrelevant once the separating inequality has been checked.

Adjacent edges already share one vertex and are excluded from the pair test.
For each vertex, let incoming/outgoing edge vectors be linear functions of
time. Dot their cross product with a fixed rational normal. This is a
quadratic polynomial. On a time cell its Bernstein coefficients are

    f(left),  2f(mid)-(f(left)+f(right))/2,  f(right).

If all three are strictly positive, the cross product never vanishes there.
Thus neither incident edge collapses and the adjacent edges cannot overlap
or fold back onto one another. A dyadic partition covers all vertices and
alltimes; failure of this sufficient test is reported as inconclusive, never
as a change of topology.

Together the pair and corner tests prove every intermediate closed polygon
is embedded. The finite piecewise-linear isotopy extends to an ambient
isotopy, so the final polygon has the same link type as the initial one.

## 3. Executable witness and independent replay

`experiments/certify_refinement_topology.py` stores exact-input hashes,
alignment coefficients, analytic sampling bounds and compressed witness
arrays. Pair rows contain edge indices, dyadic time-cell index/depth andaxis;
corner rows contain vertex index, time cell andnormal. Float64 array entries
for axes are interpreted as exact binary rationals; index columns must be
integers. The replay mode checks every inequality again, all required edge
pairs/vertices, and a gap-free, overlap-free partition of[0,1] for each.
It never accepts the storedPASS status as evidence. Empty or unknown seed
selections are rejected. Optimized Python (-O/-OO), which would strip proof
assertions, is rejected explicitly before the checker can run. VECT trailing
tokens and color-row lengths are validated; the parser cannot silently ignore
unrecognized extra data.

This certificate closes the endpoint topology obligation for these specific
M2 geometries. It supplies no ropelength or smooth-thickness certificate for
the refined polygons, which remain numerical geometry outputs.
