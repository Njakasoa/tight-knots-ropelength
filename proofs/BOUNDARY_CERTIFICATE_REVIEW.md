# Independent review of the Theorem 003 boundary certificate

Date: 2026-09-13 (UTC). Reviewer: independent validation worker.

## Verdict

The independent audit passed. It checked the regenerated source certificate
`results/boundary_certificate_20260912T223917Z/certificate.json`, whose
manifest records the current Theorem 003 hash. It re-computed the weighted
integral `J = integral_0^1 n'(x)e(x) dx` with direct `python-flint` Arb rectangles
at a finer mesh and higher precision than the source experiment, re-parsed
the exact rational endpoints, and re-evaluated the derived inequalities.

The frozen audit output is
`results/reviewer_boundary_20260913.json` with status `PASS`. Its independent
review script is `results/reviewer_boundary_20260913.py`; it does not import
the project certificate helper or the source experiment and uses the opposite
loop ordering (outer `t`, inner `x`).

## Inputs and hashes

The source certificate was regenerated with the source experiment at
(N=512), (M=1024), 192 Arb bits. Its source manifest binds the output to
the following files:

| File | SHA-256 |
|---|---|
| `results/boundary_certificate_20260912T223917Z/certificate.json` | `13577c491d2c2810f30aea4c5d99f23235f7db517bf61e70db1a2fa98a99ed7b` |
| `results/boundary_certificate_20260912T223917Z/manifest.json` | `e6ea8a3d4d4853e235f72d9f9e5f86ebb2077cb84d8a5c3e8d464c827e932ee8` |
| `experiments/certify_block_boundary.py` | `dc7dfdf993df15e3a4a0f2027d235c0901df0cc946bdaa12fef74a6fec0574a0` |
| `src/certification/arb_backend.py` | `05bcc541d44e29e06f56dc40ebd09e790155851e37f937b187c691bfc57a21ce` |
| `proofs/THEOREM_003_CANDIDATE.md` | `0a9f44f8c42d027cd73f58508e338b1dbd30a4d3c2416667747ac5dcea33c216` |
| `results/certificate_shell_N512M1024_noguard/certificate.json` | `513f888d7ee019578cd03a68d0910c682449d62082fac992b4a6b9ee75f3095e` |
| `results/certificate_shell_N512M1024_noguard/manifest.json` | `cf16967e356cf352aec86166108385caa5f3bd761ddec043bd71fbf0e24c8ae5` |

The source boundary manifest contains the certificate output hash and input
hashes, but no detached `manifest.sha256` file. The independent bundle does
include a detached manifest. Its hashes are:

| File | SHA-256 |
|---|---|
| `results/reviewer_boundary_20260913.py` | `66ffcb4b5e6deaf8f7bb46f1ccb9bfc75267a96023c0ca7c9b809b4999752c24` |
| `results/reviewer_boundary_20260913.json` | `107b538ad17295e8d6fdb6cdea6a0bd012ce3c58db439c7b216bd50b1fdef852` |
| `results/reviewer_boundary_20260913.manifest.json` | `5f55de012f8dea2cf77570cbd152aae49308066c109c65d24745a39d20315064` |
| `results/reviewer_boundary_20260913.manifest.sha256` | `120553005aced23a470ec7d2029bd14d3235c9d94f3dd781f39963df743bd64b` |

The audit was run as:

```text
.venv/bin/python results/reviewer_boundary_20260913.py \
  --boundary-dir results/boundary_certificate_20260912T223917Z \
  --output results/reviewer_boundary_20260913.json
```

## Independent interval calculation

The source uses `J`'s sum of Arb ranges over `512 x 1024` parameter
rectangles at 192 bits. The independent calculation used `1024 x 2048`
rectangles at 224 bits. Each cell covers its complete `x` and `t` interval,
with `t in [0, 2*pi]`, and the sum is multiplied by the exact cell widths.
The calculation uses the source formula

```text
n'(x) = 4*pi*(1-x)*(x*x - 2*x + 4)
         / (x*x + (2-x)*(2-x))^(3/2)
speed(x,t) = sqrt((4 + 2*x*cos(t))^2 + 4*x^2)
```

The independent interval for `J` was

```text
[114.6317164497860082862514687123466584022685949512932577381559650366826 +/- 0.343]
```

It overlaps the stored source interval

```text
[114.632798100930534566526360110788123997994224923762425053619 +/- 0.686].
```

Using the source shell's exact rational enclosures for `q0`, `l0`, and
`alpha2`, the independent recomputation produced:

| Quantity | Independent Arb enclosure (midpoint/radius display) |
|---|---|
| `a` | `[0.07735026918962576450914878050195745564760175127012687601860232648394762 +/- 6.19e-68]` |
| `d` | `[0.4327337716244993596225498568171127545005025250013375170965446159243584 +/- 2.37e-3]` |
| `c_*` | `[0.42279066331684589385986328125 +/- 1.16e-3]` |
| `beta_*` | `[3.883566650566555062186694903463043244094821115908189312904141843318939 +/- 0.0107]` |
| `beta_1` | `[5.413807588984125437045747512672904917997363416990928983035608826806798 +/- 0.0252]` |
| `beta_1 - beta_*` from `alpha2*(sqrt(d)-sqrt(a))^2` | `[1.530206608532355750079571304153000343321491458638689725355305633261949 +/- 0.0146]` |

The stored rational endpoints were parsed as integer numerator/positive
denominator pairs. All six source boundary interval records and all eight
shell interval records had valid endpoints with lower ≤ upper. Displayed
decimal strings were checked for finite decimal parsing, but were not treated
as authoritative bounds: the exact rational endpoints control every comparison.
This avoids requiring a rounded decimal rendering of π to lie inside an Arb
interval endpoint.

The exact checks all passed: `q0`, `l0`, `a`, `d`, `c_*`, `beta_*`, and `beta_1`
are positive; `c_* < 1`; the stored rational upper endpoint of `beta_*` is
below the stored rational lower endpoint of `beta_1`; and the independently
computed Arb upper endpoint of `beta_*` is below the independently computed
Arb lower endpoint of `beta_1`. All six recomputed derived intervals overlap
their stored source intervals. The direct rectangle partition is contiguous
and covers `x in [0,1]` and `t/pi in [0,2]`.

The formula also gives the integrand signs directly on this domain:
`1-x >= 0`, `x^2 - 2*x + 4 = (x-1)^2 + 3 > 0`, and the denominator is
positive, so `n'(x) >= 0`. The speed radicand is strictly positive; its smallest computed
Arb lower endpoint was the positive rational

```text
42493757352140394995759880692495766289/5316911983139663491615228241121378304.
```

The smallest computed lower endpoint for (n') was a tiny negative value
(`-583127/68719476736`) caused by outward interval rounding at the endpoint;
it was not used as a sign certificate. The analytic factorization above is
the sign check, and the resulting whole (J) interval is strictly positive.

## Discovery floor audit

The source discovery record is
`results/discovery_blocks_20260912T221841Z/discovery.json` (SHA-256
`660afe43a918d481cb2c4562a9da19fbeb9773cbf8d9eb47eb1783b7e1090d26`),
generated by `experiments/discover_block_sizes.py` (SHA-256
`85b54dea912524b6ccf102d4414c25c14fc5e7315392ce8bf8eefeaaef72b42b`).
The selected row is (T=1024,b=13), with 4,976,348 components.

At 224 Arb bits the independent audit recomputed every one of the 1,024
capacity intervals used by the selected row, using the exact `sqrt(3)`-based
radii, block-start inner radius, and outer radius. Every
interval had the same floor at both endpoints: ambiguous floor count 0; floor
range 6 through 3,988. Subtracting one from each population and applying the
doubling rule gives population sum 2,488,173 and component count 4,976,348,
matching the discovery record. The minimum exact distance from a capacity
interval to the nearest integer occurred at shell 170 and was

```text
77627447699390804826060340592969752782955239432078063510592047
/13164036458569648337239753460458804039861886925068638906788872192
= 0.005896933508479928...
```

This agrees with the discovery floating diagnostic
`0.005896933508438451` to the audit tolerance. This is a selected-floor
check only. It is not a finite total-length certificate for every candidate
or for the complete construction.

## Claim limits

This review certifies the stated rational interval arithmetic, the independent
rectangle enclosure of `J`, the signs and strict interval inequality used
for the displayed coefficient comparison, and the selected `T=1024, b=13`
floor decisions. It does not reprove the asymptotic expansion, the geometric
separation or topology argument, the full finite construction, any finite
total-length certificate, a fixed-`M` or arbitrary-schedule optimum, the
ropelength infimum, or publication novelty. Those claims require the scoped
mathematical and geometric reviews cited by Theorem 003. The source and this
review use rounded decimal strings for presentation only; the exact rational
records and formulas are the evidence.
