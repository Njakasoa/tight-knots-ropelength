# Independent review of variable-pitch topology

Date: 13 September 2026. Reviewer: delegated Astra adversarial reviewer.
Scope: `VARIABLE_PITCH_TOPOLOGY.md` and the corresponding exact formulas and
validator in `src/discovery/grammar.py`. This review does not certify finite
polygon sampling, ridgerunner trajectories, thickness, ropelength or contacts.

## Verdict

**PASS for the exact smooth isotopy that removes all finite shell-dependent
pitch modulations.** The hypotheses suffice without any smallness bound on
beta. The full-twist labels inherit the earlier theorem **up to a common
mirror**; the initial note and metadata should include that qualification
unless a specific chirality convention is proved and declared.

## Independent argument

Choose rho=r_max<R. On the solid torus |w|≤rho, cylindrical radius is at
least R−rho>0. An image point of E(u,w) therefore determines longitude u
modulo 2pi and then uniquely determines w. The angular component of the
velocity of E(u,w(u)) has magnitude R+Re(w(u))≥R−rho, so every strand is
regular regardless of whether 1+beta_i cos(u) vanishes or becomes negative.

During beta_i→lambda beta_i, every same-shell normal-disk configuration is
rotated by one common angle. Its N_i phase points remain distinct. Different
shells have different positive norms; the optional core has norm zero. Thus
no two components meet at a common longitude. Longitude injectivity excludes
all remaining coincidences. This is a smooth family of embeddings of a finite
disjoint union of circles; the smooth isotopy extension theorem promotes it
to an ambient isotopy. The same reasoning covers arbitrary phase offsets,
unsorted distinct radii and population one.

In double mode, R>2rho ensures that the two entire radius-rho core tubes are
disjoint: their core distance is R, and the triangle inequality gives pair
distance at least R−2rho>0. This bound holds at every homotopy parameter.
The proper rigid motion P transports the second isotopy and preserves its
handedness relative to the first. A positive diagonal D is joined to identity
through positive diagonal matrices, each an ambient diffeomorphism. Applying
D after P preserves the result. The validator enforces exactly the needed
positive scales, distinct positive radii, and stronger double-mode radius
condition.

After beta=0 the family is the reviewed rotating disk-point construction.
Disk configurations may be moved through distinct points within the same
radius-rho disk; points need not retain shell radii during this auxiliary
isotopy. The longitude argument still gives embedding. Full-twist
classification and the matching internal/mutual Hopf signs then follow from
`THEOREM_002.md` and `ADVERSARIAL_REVIEW_002.md`, specifically their zero-frame
and full-twist cabling argument. Including or deleting the central point
causes no difficulty. The count is Q=1_core+sum N_i for one bundle and 2Q for
two bundles.

The net 2pi normal rotation mentioned in the note is corroborating data;
net winding alone would not classify an arbitrary multi-strand braid. Here
classification follows from the explicit collision-free removal of beta
and the already reviewed baseline configuration-space proof. That distinction
is essential and is satisfied by this construction.

## Small source corrections requested

1. At the full-twist labels T(Q,Q), T(2Q,2Q), and in generator topology
   metadata, state “up to a common mirror,” matching the inherited theorem.
   This preserves the valid unoriented/mirror-qualified conclusion without
   silently selecting the wrong handedness under another torus-link convention.
2. Link the exact baseline theorem and review for the doubled cabling claim;
   the word “standard” by itself is less precise than the available proof.
3. The displayed homotopy initially has `-phi_{ij}` instead of `-\phi_{ij}`;
   correct that typographical defect. Likewise render the same-shell term
   as beta_i sin(u), with the sine operator explicit.

These do not undermine the proved smooth isotopy. No sampled-polygon label
or numerical solver output is upgraded by this review; an inscribed polygon
can need its own isotopy and reach check even when the parent smooth family
is embedded.

## Scope correction verified

The writer added the common-mirror qualification to both full-twist statements
and to the generator's topology metadata, together with precise links to
review 001 §3 and review 002 §5. I reread these changes. The substantive scope
and reference corrections are resolved; **the exact smooth topology review is
PASS**. The two notation typos listed above are editorial and do not change
the explicitly defined phase or the homotopy argument.
