# Engine contract

Implement independent numerical routines; never advertise floating point as interval.

* src/curves: exact-form circle, round Hopf, standard torus T(p,q) components
  and first/second analytic derivatives; VECT reader/writer with closedness checked.
* src/thickness: polygon MinRad and doubly-critical candidate enumeration with
  interior edge-edge, vertex-edge and vertex-vertex cases. Nonadjacent edge distances
  alone are invalid (nearby arclength produces false thickness). Numeric tolerances,
  incomplete search and degeneracy must be explicit. Smooth roots are estimates.
* src/topology: constructive standard torus parameterization with d=gcd(p,q)
  components, plus independent generic-projection linking/invariant checks when feasible.
  Invariants do not uniquely identify general knots. A sampled polygon's type is not
  automatically certified by the analytic curve it samples.
* src/contacts: active pair records with component/index/parameter, tolerance,
  curvature kinks and graph summary; no implied complete continuum contact set.
* experiments: immutable JSON outputs with timestamps, source commit, parameters,
  seed, tolerances, hardware/runtime and input/output hashes in a separate manifest.

Positive controls and exact certificate design are in proofs/POSITIVE_CONTROLS.md.
