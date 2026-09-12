# Software and reference data

Audit and acquisition date: 2026-09-13.  All paths below are relative to
the `tight-knots-lab` directory.

## Source provenance

| Item | Source / version | Local provenance |
| --- | --- | --- |
| plCurve | [designbynumbers/plcurve](https://github.com/designbynumbers/plcurve), commit `28c1ab74c02baab71ac77cd851e9163875c137a3` (2026-07-01) | `vendor/plcurve`; point-release archive `vendor/deps/libplcurve-10.1.0.tar.gz` |
| Ridgerunner | [designbynumbers/ridgerunner](https://github.com/designbynumbers/ridgerunner), commit `4ee3199e737dcd3580d8bfc5deb031cd53f5f554` (2026-07-01) | `vendor/ridgerunner`; point-release archive `vendor/deps/ridgerunner-2.0.0.tar.gz` |
| Octrope | [liboctrope documentation and source](https://jasoncantarella.com/downloads/liboctrope.html), 2.0.0 | `vendor/deps/liboctrope-2.0.0.tar.gz`; static library built locally |
| GSL | GNU Scientific Library 2.8 | `vendor/deps/gsl-2.8.tar.gz`; static local install |
| argtable2 | [argtable2 documentation](https://argtable.sourceforge.io/doc/argtable2.html), 2.13 | `vendor/deps/argtable2-13.tar.gz`; static local install |
| tsnnls | [tsnnls distribution](https://jasoncantarella.com/downloads/tsnnls_dist.tar.gz) | `vendor/deps/tsnnls_dist`; source archive's old bundled BLAS cannot link on this host |
| SnapPy | [official installation docs](https://snappy.computop.org/installing.html), 3.3.2 | project `.venv`; import and manifold smoke test pass |

The plCurve point release was configured against the locally built GSL and
its core install completed.  Its optional image tool target is incomplete in
the release Makefile.  Octrope's library completed, while two demos fail at
link time because their release Makefile omits the plCurve library.  These
are recorded as bounded build limitations rather than hidden or repaired by
system changes.

## Trefoil reference

[`data/reference/trefoil_3.1_ridgerunner.vect`](../data/reference/trefoil_3.1_ridgerunner.vect)
is an exact copy of `vendor/ridgerunner/data/3.1.vect`, the official
Ridgerunner sample input from the software repository.  SHA-256 for both
files is:

```text
809cdd9141ee4f118e01301648d7b47daf9a2d7c7683ba42e0f424e50e6405a1
```

It is a Geomview VECT file with one component and 47 vertices/edges.  The
geometry is an initial polygon supplied for optimization.  It is not a
published final tight shape.  The official Ridgerunner page
([software page](https://jasoncantarella.com/wordpress/software/ridgerunner/))
shows the same workflow and reports a 100-step example ending at
ropelength `34.95934049672`; the local plCurve measurement of the unoptimized
47-edge input is `36.66704093664804`.

The independently runnable local command is:

```text
vendor/deps/libplcurve-10.1.0/build/bin/ropelength -q \
  data/reference/trefoil_3.1_ridgerunner.vect
```

plCurve's tool is version 1.17 and uses the default `lambda=1`; its output
uses the polygon's radius/thickness convention.  The full non-quiet result
is retained in the environment audit.  It should be compared as a polygon
diagnostic, not substituted for a converged ideal-rope ropelength.

There is also a 400-vertex trefoil candidate bundled in the checked-out
plCurve tree as `vendor/plcurve/data/kl_3_1_I.vect`.  The exact copy
[`data/reference/trefoil_3.1_plcurve_kl400.vect`](../data/reference/trefoil_3.1_plcurve_kl400.vect)
has SHA-256
`a7c002b1499207bd39a187952d567fe70b86f79b51099cfc6d28f992b990d5fd` and
measures `32.74902840544252`:

```text
vendor/deps/libplcurve-10.1.0/build/bin/ropelength -q \
  data/reference/trefoil_3.1_plcurve_kl400.vect
```

The file's only provenance in the checked-out source is that plCurve data
path (commit listed above); its short name does not identify a publication
or optimization run.  It is therefore a useful higher-resolution tight
candidate for regression comparisons, with that provenance limitation made
explicit.

## DOI supplementary VECT data

The requested supplementary data for Klotz, “Tight bounds for tight links:
ropelength of T(Q,Q) torus links,” Journal of Physics A 59 (2026) 285201,
online 2026-07-14, DOI
[`10.1088/1751-8121/ae862e`](https://doi.org/10.1088/1751-8121/ae862e), was
downloaded from the signed archive URL embedded in the publisher's
[supplement page](https://doi.org/10.1088/1751-8121/ae862e/data1).

| Artifact | Location | SHA-256 |
| --- | --- | --- |
| Publisher supplement HTML | `data/reference/doi_10.1088_1751-8121_ae862e_data1` | `985b3f0096c1c54f91275837a0c19cfaef152c848d1d8363307c074d9e0b40ee` |
| Signed ZIP | `data/reference/aae862esupp1.zip` | `27d9c8afad321cbf4e7b189d5a2349cedda89fae51ffe28c351615fcec1f00d3` |
| Dataset text | `data/reference/aae862esupp1/DataTightLinksKlotz26.txt` | `34e05b430ba40d3dd246a2d0152fb993baf21a288e8db79b40a7aa91eab7d17b` |

The extracted archive contains `DataTightLinksKlotz26.txt` and VECT files
`T44.vect`, `T55.vect`, ..., `T2020.vect` (the diagonal sequence from 4 to
20).  Their sizes and the original ZIP are kept unchanged for reproducible
provenance.  These are torus-link supplementary geometries, not a trefoil
replacement; the supplied Ridgerunner 3.1 file remains the local trefoil
reference.

## Topological cross-check

With the project interpreter, Spherogram gives the trefoil fingerprints

```text
PD [(5, 2, 0, 3), (3, 0, 4, 1), (1, 4, 2, 5)]
DT [(4, 6, 2)]
```

and SnapPy's `Manifold('3_1')` has 2 tetrahedra, volume 0, and homology `Z`.
SageMath is not installed, so Spherogram methods that explicitly require
Sage (for example some Alexander-polynomial helpers) were not reported as
available.

## Known comparison context

The [earlier ropelength paper](https://jasoncantarella.com/downloads/papers/ropelength/ropelen.pdf)
reports SONO experiments near 32.66 for a tight trefoil, while later work
gives rigorous bounds and numerical values in the low 30s.  Those literature
values are context only.  No local run here claims to reproduce an ideal
trefoil optimizer because Ridgerunner is blocked by the missing Fortran and
OpenBLAS development toolchain.

## Accepted maintained builds and primary atlas acquisition

The accepted installed Ridgerunner is **2.3.1**, source commit
`4ee3199e737dcd3580d8bfc5deb031cd53f5f554`; its four upstream tests passed.
It links maintained libtsnnls **2.5.1**, whose eleven upstream tests passed.
Earlier 2.0.0/legacy build failure descriptions above document unsuccessful
attempts and do not describe the accepted binaries. See the final section of
`ENVIRONMENT_AUDIT.md` and `benchmarks/software/BUILD_PROVENANCE.json`.

The author-maintained public repository
https://github.com/designbynumbers/ropelength-minimizing-knots provides CC0
approximately tight coordinates computed by Ridgerunner. A pinned subset is
stored in `data/reference/cantarella-atlas`: 3_1 (2400 vertices), 4_1, 5_1,
6_1, 8_19, 10_124, and the Hopf link. `MANIFEST.json` stores the exact commit,
source URLs and hashes. `scripts/software/fetch_atlas.py` downloads and converts
the TSVs to closed VECT components without changing coordinate strings;
`VECT_CONVERSION.json` stores output hashes. The 2400-vertex trefoil has
polygonal ropelength 32.74366549969402 according to the actual plCurve CLI.
This is sourced reference geometry, not a proof of the trefoil minimum.

## Supplied T(4,4) coordinates versus summary table

The exact supplied `aae862esupp1/T44.vect` yields polygonal ropelength
**77.9768728808478** with our checker and **77.97687288084772** with the actual
plCurve CLI. The accompanying `DataTightLinksKlotz26.txt` lists **77.47** forQ4.
The difference is0.50687288 (about0.6543%). The supplement explicitly labels its
ropelengths as radius normalized and its coordinate tubes as unit diameter;
our length/thickness ratio already handles that scaling, so a factor-two
conversion does not explain this small discrepancy. A difference in saved
optimization state, curvature convention or another source detail is possible,
but is not established. We reproduce the supplied geometry and report the table
mismatch; we do not claim to have reproduced77.47 from these coordinates.
