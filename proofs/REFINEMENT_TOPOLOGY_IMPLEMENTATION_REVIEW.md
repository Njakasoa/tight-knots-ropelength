# Independent implementation review: refinement topology certificate

Date: 2026-09-13. Reviewer: independent validation worker.

## Verdict

The hardened refinement-topology implementation and the canonical certificates
for seeds 1729, 2718, and 3141 pass independent replay. The independent audit
reconstructed the analytic samples from the defining coordinates, parsed VECT
coordinate tokens as exact `Fraction` values, interpreted JSON parameters and
witness axes as exact binary64 rationals, and checked the finite dyadic witness
coverage independently. The reviewed claim is limited to the stored endpoint
polygons' link type through the explicit alternative isotopy described in
`proofs/REFINEMENT_TOPOLOGY_CERTIFICATE.md`.

It does not certify the Ridgerunner trajectory, smooth reach, polygonal
thickness, ropelength, criticality, convergence, or optimality.

## Frozen artifacts and hashes

The canonical hardened directory is
`results/topology_path_20260912T231158562188Z`. Its summary reports PASS for
all three records, with source-search SHA-256
`7107b746b09fbe339644bbf9f1dd9e5e24dd2cdd76fba52337e795647dd07496` and
certificate-script SHA-256
`0b16a0f951bcad2a0c00b012434181909c268cae399460a4856ef376e287c14a`.

| Artifact | SHA-256 |
|---|---|
| `experiments/certify_refinement_topology.py` | `0b16a0f951bcad2a0c00b012434181909c268cae399460a4856ef376e287c14a` |
| `results/variable_pitch_20260912T224501767133Z/search.json` | `7107b746b09fbe339644bbf9f1dd9e5e24dd2cdd76fba52337e795647dd07496` |
| `results/topology_path_20260912T231158562188Z/summary.json` | `ea16a50d394007fbbb8cb70deba3ddc27e6caec3803017147c78986971c02346` |
| `results/topology_path_20260912T231158562188Z/seed1729.npz` | `c1ff3b6f553649e0bb6205f2153fcb7f78611e40ca950f9fc63156a289b35055` |
| `results/topology_path_20260912T231158562188Z/seed2718.npz` | `62458eeed8407dc3e925f8003980fc176f76b6303184b2695692849361272ab8` |
| `results/topology_path_20260912T231158562188Z/seed3141.npz` | `51da94094e4edaca13f4591afc417336105a596d522bfa9580df65a44607f6da` |
| `results/reviewer_refinement_20260913.py` | `502803649dfbce1679c52dcc0e9ed29266cb9d055e075d29ce8b1c230f57c432` |
| `results/reviewer_refinement_20260913.json` | `29a70ca17819aeeed52a93a543d66ac0610d84c8a89253b30672e05670a5293b` |

The three certificate JSON files also carry the same current checker hash.
Their endpoint hashes are:

| Seed | Initial VECT | Final VECT |
|---:|---|---|
| 1729 | `342c6833ec356d3b83a543bc124cefd22b56f120f9c117d750a9fef9179363d6` | `6775a6b498a279a39a5f9a3b53cba3fc289722deb356c7fe948ac9b4d17b3f5a` |
| 2718 | `f86bd1bc3c1aaa13038fbaa4b6b75d8d8a8d2359eed8d80568baed151aac19c8` | `c1ccf0924832ec83435394ce24c60df8d86caa0fdeb1117f58e9f6e44e34e736` |
| 3141 | `87bac12e0bfc7a85d56eb81bf3c9e905bc0881f7a7ace17b257fe37b52f57f4` | `245b621ee02215090507c1d60cd8fb957c079989492c6a1a5100f6263ad275fe` |

## Independent analytic reconstruction

The audit command was:

```text
.venv/bin/python results/reviewer_refinement_20260913.py
```

For each seed it independently parsed all 576 coordinates from each endpoint,
converted every decimal token directly to a rational, undid the second-bundle
proper motion and the stored positive z scale, and evaluated

```text
E(u, r exp(i*(u + beta*sin(u) - phi)))
```

at the 48 exact grid parameters using 192-bit Arb. JSON parameters were
decoded by Python as binary64 and then converted with `Fraction.from_float`;
the mathematical `pi` remained an Arb constant. All 576 squared vertex errors
per seed were strictly below the exact Arb enclosure of `10^-20`.

| Seed | Maximum squared-error upper bound | Maximum transverse error upper bound | Minimum separation minus `2*emax` | Double-tube gap |
|---:|---:|---:|---:|---:|
| 1729 | `3.6954408009629885e-29` | `0.060623136007345758...` | `0.859288074603027916...` | `0.144365853751987292...` |
| 2718 | `4.413715003095171e-29` | `0.052757355337814978...` | `0.889565129358717951...` | `0.282709490009530215...` |
| 3141 | `4.6306381120633214e-29` | `0.048473210218338884...` | `0.891753894800291005...` | `0.547399446996892039...` |

The independent lower margins are all positive. The recomputed least-squares
positive homothety and translation agree bit-for-bit with every stored
alignment; every alignment coefficient is a finite exact binary64 rational
and the scale is positive.

## Witness enumeration and exact replay

For 12 closed components of 48 vertices, the independent required-pair count
is

```text
576*575/2 - 12*48 = 165024.
```

Each seed contains exactly 165,024 pair rows and 576 adjacent-corner rows.
Independent enumeration confirms that every intercomponent pair and every
within-component nonadjacent cyclic pair occurs exactly once, while all 576
vertices occur in the corner set. Every row has integral index/time columns,
finite axes, dyadic time endpoints, and exact gap-free coverage of `[0,1]`.
The maximum pair and corner subdivision depth is zero for every seed, so each
stored row covers the full time interval. Every witness hash matches its
certificate JSON.

The all-seed command replayed the current artifacts as follows:

```text
.venv/bin/python experiments/certify_refinement_topology.py \
  results/variable_pitch_20260912T224501767133Z \
  --verify results/topology_path_20260912T231158562188Z

1729 REPLAY_PASS
2718 REPLAY_PASS
3141 REPLAY_PASS
```

Replay uses exact Arb inequalities for each stored projection interval and all
three Bernstein coefficients of each adjacent-corner quadratic. It does not
trust the stored PASS fields.

The `PathCheck` cache was independently exercised at equivalent dyadic times:
`(1,1)` and `(2,2)` share the canonical `t=1/2` entry, and `(2,1)` reuses the
canonical `t=1` endpoint. No duplicate cache entry or endpoint-range issue was
observed in valid replay.

## Tamper and parser checks

Copies of the seed-1729 witness were modified and their certificate hash was
updated, so hash-only rejection could not account for the results. Under the
normal interpreter, all of these were rejected:

| Modification | Result |
|---|---|
| Remove the entire NPZ | `FileNotFoundError` |
| Remove one required pair row | `pair/corner coverage mismatch` |
| Replace a separating axis with zero | `pair witness failed` |
| Remove one corner row | `pair/corner coverage mismatch` |
| Put `num=1` in a depth-0 endpoint cell | assertion on time bounds |
| Replace an edge index by `0.5` | assertion on integer witness index |
| Run the missing-pair case under `python -O` | explicit `RuntimeError`; optimized verification is refused |
| Append one token after the declared RGBA color values | `ValueError` on unexpected trailing VECT tokens |

The parser also rejects a truncated coordinate row. As a separate canonical
zero-colour check, the source parser and the independent exact parser both
read `data/reference/cantarella-atlas/knots/prime/3-10/3_1.vect` as one closed
component with 2,400 vertices and zero colors; the atlas VECT SHA-256 is
`892a10e01a90b3491c2c7f6c7a5e70f3b5f93293c06083240c13136fa11b1482`.

## Claim limits

The evidence establishes a finite, explicit alternative PL isotopy between the
stored initial and final polygons for these three variable-pitch outputs. The
analytic sampling bridge establishes their common construction-level
full-twist label `T(12,12)`, up to a common mirror, subject to the hypotheses
and bounds in the formal certificate.

It does not establish that the numerical Ridgerunner trajectory itself stays
embedded, that any refined polygon has certified reach or thickness, or that a
reported ropelength is a smooth upper bound. It also does not prove a global
optimum, finite-`M` optimum, solver convergence, or a publication novelty
claim. The witness axes are floating proposals whose stored binary64 values are
reinterpreted exactly; acceptance comes only from the replayed Arb inequalities.
