# Independent validation evidence

Validation date: 2026-09-12 UTC (local date 2026-09-13).  The focused
independent suite passed **12 tests**, and the repository-wide suite passed
**27 tests**.  Both commands returned status 0.  This report records the
bounded evidence; it does not by itself declare M1 complete.

## Reproduction and frozen bundle

Run from the `tight-knots-lab` directory with the project interpreter:

```text
.venv/bin/python tests/independent/run_validation.py \
  --output-dir results/independent_final
```

The runner executed and retained both commands:

```text
.venv/bin/python -m pytest -q tests/independent/test_independent_validation.py
.venv/bin/python -m pytest -q
```

The focused output is in
[`results/independent_final/pytest.stdout.txt`](../results/independent_final/pytest.stdout.txt)
(`12 passed in 29.45s`); the full-suite output is in
[`results/independent_final/pytest_full.stdout.txt`](../results/independent_final/pytest_full.stdout.txt)
(`27 passed in 30.91s`).  Both stderr files are empty.  The machine-readable
record is [`validation.json`](../results/independent_final/validation.json),
with detached manifest files
[`manifest.json`](../results/independent_final/manifest.json) and
[`manifest.sha256`](../results/independent_final/manifest.sha256).

The bundle records commit
`2235217a5e6f1a54afbe38029218faa65fea527d` plus a dirty working-tree status.
The source hashes that identify this tester and its runner are:

| Artifact | SHA-256 |
|---|---|
| `tests/independent/test_independent_validation.py` | `6175f60a59e0f14af9fa2ff06e602479fa53d3625f6be7f66788b6921cf5bf4f` |
| `tests/independent/run_validation.py` | `fb897cc54ff3ad4a4b588f24484b5ba3377120a7f747fc6a78146ed91d427d37` |
| `results/independent_final/pytest.stdout.txt` | `b2a9f8d020814f8f732859ae3c3521c83cca897c4157a279c3b509baa454d27f` |
| `results/independent_final/pytest_full.stdout.txt` | `b5a8c8e147a6bc6f8b2ba966cd9b49ca5568f38b4c8b8f392e2a608c03fecb1d` |
| `results/independent_final/validation.json` | `b7ba670ef3d9750a9c833f5c2b45acc6d2b782f8612252ec3e34e72376a9b55a` |
| `results/independent_final/manifest.json` | `bc90efb42ad6bfa3e7064cb03be5932aaa6b5b10b37cbb2d50cdd38f181c51f0` |
| `results/independent_final/manifest.sha256` | `4b0b1c4daab99a7eaf9dbd3c23c4dcd0a99c69a48b7b5354c44a3099a7f2ba14` |

The recorded environment is CPython 3.12.3 on WSL2 x86-64, with NumPy
2.5.3, SciPy 1.18.1, mpmath 1.3.0, python-flint 0.9.0, and pytest 9.1.1.
The independently invoked plCurve executable is
`vendor/deps/libplcurve-10.1.0/build/bin/ropelength`, SHA-256
`7fc54850258d4ea4c8ff4070aa128e50626e3d2833ec20922bd739b3f91607c2`.
The source commits recorded by the runner are plCurve
`28c1ab74c02baab71ac77cd851e9163875c137a3` and Ridgerunner
`4ee3199e737dcd3580d8bfc5deb031cd53f5f554`.

## Results

The raw VECT parser independently checks component counts, closure signs,
color-count rows, and coordinate counts.  Explicit polyline sums agree with
the project parser and with plCurve/liboctrope metrics.  The direct CLI values
for the two source and two final controls are:

| Geometry | Vertices | Ropelength | Thickness | MinRad | MinStrut |
|---|---:|---:|---:|---:|---:|
| Ridgerunner source | 47 | `36.66704093664804` | `1.547943` | `3.156630` | `3.095885` |
| plCurve source | 400 | `32.74902840544252` | `0.999950` | `0.999958` | `1.999900` |
| Ridgerunner final | 47 | `33.14901731963343` | `0.499994` | `0.567392` | `0.999987` |
| Ridgerunner final | 400 | `32.74879268133495` | `0.499996` | `0.499996` | `0.999992` |

The checked-in source hashes are `809cdd9141ee4f118e01301648d7b47daf9a2d7c7683ba42e0f424e50e6405a1`
(47 vertices) and `a7c002b1499207bd39a187952d567fe70b86f79b51099cfc6d28f992b990d5fd`
(400 vertices).  The actual final VECT output hashes are
`544e879142b32674fa7e4c45961d5dfc82d29ffa5ad981ef0119889ef96807d7` (47)
and `4b769612a303bf19b8694aff2bac1ab119fe3c55353fede9dfde201922178200`
(400).  These outputs, rather than their filenames, are the inputs to the
geometry-only topology check.

The independent projected-diagram implementation records segment parameters,
over/under depth, and oriented crossing sign, then computes the reduced
integer Fox relation matrix at (t=-1) with fraction-free elimination.  It
recovers determinant 3 from a generic three-crossing projection of each source
polygon and each actual Ridgerunner final polygon.  The final geometries have
minimum absolute depth gaps `1.0050735540709475` and `1.0069196513503917` in
their selected views.  Reversing each polygon orientation preserves the
determinant.  The same independent projection checks show three crossings for
T(2,3), unit absolute pairwise linking for T(2,2), and unit absolute pairwise
linking for all three pairs of T(3,3), with the expected view and orientation
behavior.

The analytic controls also pass.  Circle length, curvature radius, and the
nonlocal control satisfy `length = 2*pi*r`, curvature radius `r`, and exact
DCSD `2*r` at radii 0.5, 1, and 2.  The explicit Hopf link scales with length
`8*pi*r` and thickness `r`.  The independent torus length quadrature catches
the gcd-reduced period for T(2,2), and half-period samples of its two
components are distinct.

The four adversarial polygon collision probes all return thickness 0, DCSD 0,
`degenerate=True`, `complete=False`, and a surfaced zero-distance candidate.
This includes the near-endpoint collision and the uniformly scaled crossing.
Projection of the 47-vertex trefoil remains generic with three crossings at
scales 1, `1e-5`, and `1e5`.  These checks retain the corrected zero-collision,
scale handling, circle DCSD, Rawdon MinRad, depth-aware crossing sign, and
symmetric linking-matrix behavior.

The raw Cantarella atlas controls are also parsed and measured directly:

| Atlas file | Component vertices | CLI ropelength |
|---|---:|---:|
| `3_1.vect` | 2400 | `32.74366549969402` |
| `4_1.vect` | 400 | `42.09702880992264` |
| `5_1.vect` | 392 | `47.21488738316189` |
| `2_2_1.vect` | 101 + 101 | `25.14141773337161` |

The pinned atlas manifest has SHA-256
`a3dfe6346f5b8256ec803f7110257a0ec4f08db9ba89a0ab310f0d04a41ece17`.
The parser consumes one per-component color-count row even when the header
reports zero total colors, as required by these native files.

## Arithmetic evidence

The 192-bit Arb certificate at `N=512`, `M=1024` is retained in
[`results/certificate_shell_N512M1024_noguard`](../results/certificate_shell_N512M1024_noguard).
Its primary alpha upper endpoint is
`11.40519894659519195556640625 < 11.407`; the optional reviewed staggered
rescaling has upper endpoint
`10.61373355872849806604623979 < 10.614`.  The certificate JSON SHA-256 is
`513f888d7ee019578cd03a68d0910c682449d62082fac992b4a6b9ee75f3095e`.

The separate 224-bit angular-outer recomputation in
[`results/reviewer_certificate_check.json`](../results/reviewer_certificate_check.json)
has SHA-256 `2e2ec7e21c9e0ea199e99b7fdd1cb34370bcbe354467f73d23316d1b5ccfb75e`.
It overlaps the stored rational endpoints for `q0`, `l0`, alpha, and the
optional alpha2 value, verifies the detached output hash, and independently
checks alpha2's exact rational upper endpoint below 10.614.  The focused test
also recomputes the midpoint error with an independent Decimal value of pi and
uses independent high-precision quadrature; it compares rational endpoints,
so a rounded display decimal is never treated as the Arb enclosure.

## Claim limits

The determinant is a meaningful invariant of each sampled generic polygon
diagram, but it does not prove an analytic isotopy for a smooth family or a
global knot classification from arbitrary sampling.  Polygon `complete=False`
on collisions and `complete=True` on ordinary cases describe enumeration of
the supplied finite polygon; they do not turn a sampled geometry into a smooth
reach certificate.

The Ridgerunner values are bounded, seed-logged numerical refinements with
finite stop times.  They are reproducible polygonal diagnostics and are not
global optima, smooth upper-bound certificates, or convergence proofs.  The
atlas coordinates are CC0 reference controls pinned by their manifest, not
exact minimizers.  The Arb records certify the stated integral arithmetic and
endpoint comparisons only; topology, geometric clearance, global optimality,
and publication novelty remain separate claims.  Independent Astra/M1 review
is recorded separately from this tester result.
