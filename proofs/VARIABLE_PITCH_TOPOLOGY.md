# Variable-pitch shell grammar: finite topology scope

This note records the construction-level topology of the configurable
generator in [`src/discovery/grammar.py`](../src/discovery/grammar.py).  It is
an exact formula and isotopy note for finite smooth curves.  It does not add a
thickness, reach, ropelength, or polygonal isotopy certificate.

## Configuration and exact formula

Choose a common major radius (R), distinct positive shell radii

\[
  0<r_i<R,
  \qquad i=1,\ldots,T,
\]

positive integer populations (N_i), phase offsets (eta_i), and finite
pitch coefficients (eta_i).  The normal-disk embedding is

\[
 E(u,w)=((R+\operatorname{Re}w)\cos u,
         (R+\operatorname{Re}w)\sin u,
         \operatorname{Im}w),
 \qquad u\in\mathbb R/(2\pi\mathbb Z).
\]

For strand (j=0,\ldots,N_i-1), set

\[
 \phi_{ij}=2\pi j/N_i+\eta_i,
 \qquad
 w_{ij}(u)=r_i\exp\!\bigl(i[u+\beta_i\sin u-\phi_{ij}]\bigr),
 \qquad
 F_{ij}(u)=E(u,w_{ij}(u)).
\]

The optional core is (C(u)=E(u,0)=(R\cos u,R\sin u,0)).  A positive
ambient diagonal map

\[
 D(x,y,z)=(s_xx,s_yy,s_zz),
 \qquad s_x,s_y,s_z>0,
\]

is applied to the coordinates after the formula above.  In double mode the
second copy is first formed with

\[
 P(x,y,z)=(R+x,-z,y),
 \qquad \det DP=+1,
\]

and then receives the same (D).  The implementation writes the complete
configuration, formula strings, component descriptors, and optional finite
coordinates to JSON.

The parameter (eta_i) is a shell-dependent pitch modulation.  It changes
the angular speed of the normal-disk point but not its radius:

\[
 |w_{ij}(u)|=r_i,
 \qquad
 u+\beta_i\sin u\big|_{u=0}^{u=2\pi}=2\pi.
\]

No bound such as (|\beta_i|<1) is required for this finite smooth embedding.
The longitude derivative has a nonzero angular component because
(R-r_{\max}>0), even if (1+\beta_i\cos u) vanishes at an isolated
parameter value.

## Periodicity and noncollision

Every formula is (2\pi)-periodic, including its first and second
derivatives.  The endpoint comparisons emitted by the generator are floating
diagnostics of that exact periodic identity.

For the analytic curves, (R>r_{\max}) implies that the cylindrical radius
(R+\operatorname{Re}w) is positive.  Consequently the cylindrical angle of
an image point recovers (u) modulo (2\pi).  Equality of two points first
forces equal longitude and then equal normal-disk coordinate.  At a fixed
longitude, distinct strands on one shell differ by equally spaced phase
angles, and a common (eta_isin u) term only rotates all of them together.
Distinct shell radii have distinct normal-disk norms, and the optional core
has norm zero.  Thus the finite smooth family is embedded for every allowed
configuration.

The linear homotopy

\[
 w_{ij}^{(\lambda)}(u)=r_i\exp\!\bigl(i[u+\lambda\beta_i\sin u-\phi_{ij}]\bigr),
 \qquad 0\leq\lambda\leq1,
\]

preserves those same facts at every (lambda).  It is therefore a
constructive smooth isotopy from the variable-pitch curves to the
(eta_i=0) curves.  This argument uses distinct radii and common
same-shell rotation; it is not a sampled-polygon reach test.

For `double_hopf`, the two virtual core circles are (C(u)) and (P(C(v))).
Their minimum distance is (R).  Each shell point lies within (r_{max}) of
its corresponding core, so the sufficient ambient separation condition is

\[
 R>2r_{\max}.
\]

The configuration validator enforces this stronger condition in double mode.
The positive diagonal map (D) is invertible and is connected to the identity
by (D_\lambda=\operatorname{diag}(1+\lambda(s_k-1))), whose entries remain
positive.  It therefore preserves the ambient isotopy class and cannot
create a collision.

## Full-twist labels

Let

\[
 Q=\mathbf 1_{\{\text{core included}\}}+\sum_{i=1}^T N_i.
\]

In tubular coordinates around the core, the cross-sectional configuration
returns after one longitude period with net normal-disk rotation (2\pi):

\[
 [u+\beta_i\sin u]_{0}^{2\pi}=2\pi.
\]

The phase offsets and distinct radii can be moved through configurations of
distinct disk points to the reference arrangement, while the preceding
noncollision argument keeps the motion embedded.  The one-bundle construction
therefore has the construction-level full-twist label

\[
 T(Q,Q).
\]

This label is **up to a common mirror**; the grammar does not fix an
orientation sign.  The inherited full-twist and framing argument is reviewed
in [`ADVERSARIAL_REVIEW_001.md` §3](ADVERSARIAL_REVIEW_001.md#3-constructive-topology-and-framing).

Applying the proper Hopf motion (P) gives two linked core circles.  The
standard full-twist cabling/factorization used for the doubled shell family
then gives the label

\[
 T(2Q,2Q).
\]

This doubled label is likewise **up to a common mirror**, with no separate
sign convention asserted here.  The inherited two-block cabling factorization
is recorded in [`ADVERSARIAL_REVIEW_002.md` §5](ADVERSARIAL_REVIEW_002.md#5-inherited-geometry-and-topology)
and its underlying two-bundle argument in [`ADVERSARIAL_REVIEW_001.md` §3](ADVERSARIAL_REVIEW_001.md#3-constructive-topology-and-framing).

These are finite smooth construction labels.  The generator records both
labels and marks the selected closure mode; it does not infer a knot type from
sampled coordinates.

## Scope of numerical output

The optional coordinate and derivative arrays are finite samples for numerical
multistart, contact clustering, or visualization.  They are explicitly marked
as non-certifying in the JSON record.  Polygon samples have no automatic
reach, thickness, or isotopy certificate, and this grammar introduces no new
analytic thickness claim.  Any later thickness or topology conclusion must be
checked by the independent tools appropriate to that question.
