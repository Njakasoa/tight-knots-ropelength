# Environment audit

Audit date: 2026-09-13.  Host: Ubuntu 24.04.3 LTS under WSL2 on x86-64
(`Linux Zah 6.18.33.2-microsoft-standard-WSL2`).  The audit was run in the
project checkout and did not modify system packages or configuration.

## Usable interpreter and Python stack

The system interpreter is `/usr/bin/python3` (CPython 3.12.3, GCC 13.3.0).
The project-local interpreter is
[`./.venv/bin/python`](.venv/bin/python), which is the available interpreter
for numerical work.  Its installed versions are pinned in
[`scripts/software/requirements-scientific.txt`](scripts/software/requirements-scientific.txt)
and are:

| Package | Version | Check |
| --- | ---: | --- |
| numpy | 2.5.3 | import succeeds |
| scipy | 1.18.1 | import succeeds |
| sympy | 1.14.0 | import succeeds |
| mpmath | 1.3.0 | import succeeds |
| matplotlib | 3.11.2 | import succeeds; Tk GUI is unavailable |
| pytest | 9.1.1 | import succeeds |
| intvalpy | 2.0.3 | import succeeds; interval arithmetic |
| python-flint (`flint`) | 0.9.0 | import succeeds; Arb ball arithmetic |
| SnapPy (`snappy`) | 3.3.2 | import succeeds |
| Spherogram | 2.4.1 | import succeeds |

`pyinterval` was also checked but could not be installed on CPython 3.12:
its `crlibm` 1.0.3 dependency imports the removed
`distutils.command.upload` during setup.  `intvalpy` and `python-flint` are
the usable interval alternatives.  The system Python initially had none of
these scientific packages; all entries above are confined to `.venv`.

SnapPy/Spherogram smoke tests succeeded.  `Link('3_1')` produced PD code
`[(5, 2, 0, 3), (3, 0, 4, 1), (1, 4, 2, 5)]` and DT code `[(4, 6, 2)]`;
`snappy.Manifold('3_1')` produced 2 tetrahedra, volume 0, and homology `Z`.
Some Spherogram polynomial methods require SageMath and raise
`SageNotAvailable`; this is expected.  SageMath, Julia, Octave, VTK, and
PyVista are absent.  Matplotlib's noninteractive rendering remains usable.

## Native tools, libraries, and hardware

GCC and G++ 13.3.0, GNU Make 4.3, and Git 2.43.0 are present.  `gfortran`,
CMake, `pkg-config`, Autoconf, Automake, and Libtool are absent.  The
available system BLAS/LAPACK entries are the runtime SONAMEs
`libblas.so.3` and `liblapack.so.3`; there is no detected OpenBLAS and no
unversioned development `-lblas`/`-llapack` link name.  GSL, CBLAS headers,
and system argtable2 are absent, so project-local static builds were used.

The machine reports an AMD Ryzen 7 5800X (8 cores / 16 threads), about 42 GiB
RAM, and ample local disk.  `nvidia-smi` is present under WSL but reports
“GPU access blocked by the operating system”; no CUDA or usable GPU was
claimed by this audit.  No visualization application or VTK backend was
found.

## Local source builds and outcomes

Sources and point releases are kept under [`vendor/`](vendor/), with fetched
archives under [`vendor/deps/`](vendor/deps/).  The following outcomes are
reproducible with the local GCC/Make toolchain:

| Component | Result | Evidence / limitation |
| --- | --- | --- |
| GSL 2.8 | built and installed locally | static `libgsl.a` and `libgslcblas.a` under `vendor/deps/gsl-2.8/build/lib` |
| argtable2 2.13 | built and installed locally | static `libargtable2.a` under `vendor/deps/argtable2-13/build/lib` |
| tsnnls distribution | library built | bundled `libblaslinux.a` is incompatible/malformed on this host; bundled test link fails with `cannot find -lblaslinux` and malformed `libf77blas.a` |
| libplCurve 10.1.0 | core library and tools built | optional `tools/diagram_to_img` target has no generated Makefile, so the aggregate `make` exits 2; `make -C src install` succeeds |
| liboctrope 2.0.0 | library built and installed locally | demo links omit `-lplCurve`, so aggregate `make` exits 2; `liboctrope.a` itself installs successfully |
| Ridgerunner 2.0.0 | blocked | configure reaches the Fortran compiler test and fails because `gfortran`/`g77` is absent; current source additionally expects OpenBLAS and pkg-config |

The successful plCurve install provides
`vendor/deps/libplcurve-10.1.0/build/bin/ropelength`.  Running it on the
copied Ridgerunner trefoil input gave a real numerical result:

```text
$ vendor/deps/libplcurve-10.1.0/build/bin/ropelength -q \
    data/reference/trefoil_3.1_ridgerunner.vect
36.66704093664804
```

The non-quiet run reports ropelength 36.667041, thickness 1.547943,
diameter ropelength 18.333520, diameter thickness 3.095885, minimum radius
3.156630, minimum strut 3.095885, and 47 edges.  This is the measured input
polygon, not a claim that it is an ideal or converged tight trefoil.

For a higher-resolution comparison, the plCurve source tree also bundles
`data/kl_3_1_I.vect` (400 vertices).  It was copied to
`data/reference/trefoil_3.1_plcurve_kl400.vect` and measures
`32.74902840544252` with the same command.  Its bundled filename has no
separate paper citation in the checkout, so it is recorded as a plCurve
tight-candidate reference rather than asserted to be a final optimum.

`scripts/software/fake-gfortran` is a deliberately tiny configure probe
shim.  It emits C objects containing only the symbols used by Autoconf's
name-mangling test; it is **not a Fortran compiler**, does not synthesize
objects from Fortran source, and must never be used as evidence of a
Ridgerunner build.  Even with this shim, the Fortran test program and
libtool FC test fail.  A genuine Ridgerunner build therefore remains
blocked until a Fortran compiler and compatible BLAS/OpenBLAS development
library are available.

## Provenance and reproducibility

The trefoil and supplementary-data hashes, source commits, commands, and
URLs are recorded in [`references/SOFTWARE_DATA.md`](references/SOFTWARE_DATA.md).
The DOI archive was downloaded using the signed URL embedded in the DOI
supplement page and extracted locally; no paid service or system install was
used.

## Maintained solver build completed — 2026-09-13 local / September 12 UTC

This update supersedes the earlier failed legacy build attempts. Actual GNU
Fortran 13.3, OpenBLAS 0.3.26, LAPACKE, ncurses and autotools were downloaded
as Ubuntu packages and extracted inside `vendor/toolchain`; no system install
or configure-only compiler shim was used for the accepted builds.

- Maintained libtsnnls **2.5.1**: build/install succeeded; **11/11 tests passed**.
- Maintained Ridgerunner **2.3.1**, commit `4ee3199e737dcd3580d8bfc5deb031cd53f5f554`:
  build/install succeeded; **4/4 tests passed** (constraint stepping, curvature
  gradients, strut gradients, row numbering).
- Linked plCurve/octrope **10.1.0**. The old 2.0.0 release was an unsuccessful
  alternative, not the installed maintained solver version.
- Reproduce via `scripts/software/build_current.py`; run through
  `scripts/software/ridgerunner-local`, which supplies project-local dynamic
  dependency paths and one OpenBLAS thread.
- Upstream tsnnls test drivers used Bash-only `test ==` under `/bin/sh`.
  The build script changes this to quoted POSIX `test =`; it changes no solver
  code, expected solution, or numerical tolerance.
- Source commits, package hashes, and copied upstream test summaries:
  `benchmarks/software/BUILD_PROVENANCE.json` and adjoining logs.

Actual runs are stored in `results/ridgerunner_autoscaled_20260913`: the
47-vertex input decreases from 36.66704094 to 33.14901732 after 5000 steps;
the 400-vertex near-tight input decreases from 32.74902841 to 32.74879268
after 1000 steps. These are polygonal numerical values, not smooth certified
upper bounds or proofs of optimality. The initial 250-step run without forced
scaling remains archived as an insufficient convergence attempt.
