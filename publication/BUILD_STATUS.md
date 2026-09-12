# Publication build status

**Status: PASS (final local PDF generated and visually checked).**
`publication/main.tex` was compiled with the official Tectonic 0.17.0 Linux
x86_64 release on 13 September 2026 UTC. After visual inspection identified
right-edge clipping in the earlier abstract, a formatting-only correction was
made: the abstract bound was moved to display math, curve equation (1) was
split across aligned rows, and the long definition of $F(T,b)$ was moved to a
display. No mathematical content or value changed. The earlier PDF is
superseded by the final artifact below.

## Compiler provenance

- Release: [Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0)
- Asset URL: `https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-unknown-linux-gnu.tar.gz`
- Downloaded archive SHA-256:
  `1a715688baf591e650c8aeb160ae934e181685eecbb38b317de30b269ac5d606`
- Extracted executable SHA-256:
  `2b3a86250906c92ed0a3ae8aaa454ec55bd6cede8593b3e549640177f6aecaa3`
- Executable check: `ELF 64-bit LSB pie executable, x86-64`; reported version
  `Tectonic 0.17.0`.
- TeX support bundle: Tectonic's default `default_bundle_v33` cache, fetched
  through its official relay and reused for the repeated builds. The local
  cache index used for this run has SHA-256
  `0fb434b0fa5fdebea7f767ed9c31939c99a780d6f95cd3f540aae55910bb5697`.
  The cache is outside the repository and is therefore not treated as a
  checked-in source artifact.

## Commands and attempts

The final command was run from `publication/` with a writable task-local
cache:

```text
XDG_CACHE_HOME=/tmp/tight-knots-tectonic-cache \
  ../vendor/latex/tectonic-0.17.0 -X compile \
  --outdir build --outfmt pdf --print --untrusted \
  --keep-intermediates --keep-logs main.tex
```

The first local attempt failed before compilation because the default cache
location was read-only. The first network-enabled attempt then reached the
official relay but encountered a transient DNS failure while fetching one
hyphenation file. A retry reused the partially populated cache and completed;
the later repeated runs also completed. The retained logs are:

- [`tectonic-pass1.log`](build/tectonic-pass1.log): initial cache/network
  failure path;
- [`tectonic-pass2.log`](build/tectonic-pass2.log): successful compile with
  TeX rerun;
- [`tectonic-pass3.log`](build/tectonic-pass3.log): successful repeat;
- [`tectonic-pass4.log`](build/tectonic-pass4.log): successful run retaining
  auxiliary files;
- [`tectonic-pass5.log`](build/tectonic-pass5.log) and
  [`tectonic-pass6.log`](build/tectonic-pass6.log): successful repeated runs.

The bundled LaTeX workflow was also exercised with the project-local binary on
`PATH`; its machine-readable successful run is
[`latex-compile.json`](build/latex-compile.json).

The final formatting-only rebuild used the cached local executable with the
same command shown above. Its retained transcript is
[`tectonic-format-fix-final.log`](build/tectonic-format-fix-final.log). The
earlier formatting attempt is retained as
[`tectonic-format-fix.log`](build/tectonic-format-fix.log).

## Output and checks

- [`main.pdf`](build/main.pdf) is the final seven-page PDF, 115,457 bytes,
  SHA-256
  `44b3e71d97fca820f28199b69a57dc0fbd0ee535894e0dd81024515d96ff2986`.
- Retained auxiliary files are [`main.aux`](build/main.aux),
  [`main.out`](build/main.out), and [`main.log`](build/main.log).
- The final auxiliary file contains all theorem labels and bibliography
  entries. The combined Tectonic transcript retains expected first-pass
  unresolved-reference and rerun notices, while the final `main.log` has no
  undefined-reference or overfull-box entries. The final engine transcript has
  no fatal error.
- Source hashes at build time:
  - `publication/main.tex`:
    `272b07f846248a67f627efae4f822e989fca9554e50d1461f5c3dd43e5274b02`
  - `publication/figures/block_discovery.pdf`:
    `68edd278111179a5095c5284b3853aa8f120a79b5543946d99ffce361cf83d87`

The successful workflow report itself has SHA-256
`62253705b6aa371d4e130fa04e106ff0deac5ec930e76a90dbb82dc85d2b79ee`.

Repeated Tectonic writes produced the same page count and byte size; the PDF
hash can vary between writes because the XDV/PDF conversion does not promise
bit-for-bit deterministic object serialization. The final PDF above is the
artifact currently retained in `publication/build/`.

## Visual boundary check

The final PDF was rendered at 2x with the system PyMuPDF renderer. All seven
pages were inspected individually and in
[`contact-sheet.png`](build/visual/contact-sheet.png). Each rendered page is
1224 by 1584 pixels; the measured ink bounding boxes were:

| Page | Ink bounding box | Right margin |
| --- | --- | ---: |
| 1 | `(144,229)`--`(1079,1499)` | 144 px |
| 2 | `(144,146)`--`(1080,1499)` | 143 px |
| 3 | `(144,146)`--`(1080,1500)` | 143 px |
| 4 | `(144,149)`--`(1082,1499)` | 141 px |
| 5 | `(144,146)`--`(1079,1500)` | 144 px |
| 6 | `(144,150)`--`(1079,1500)` | 144 px |
| 7 | `(144,150)`--`(1080,1500)` | 143 px |

The earlier pre-correction page 1 had a visibly clipped abstract line at the
right edge; that result is not treated as a successful visual check. The final
render has the complete bound and preserves a full right margin on every page.
