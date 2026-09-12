#!/usr/bin/env python3
"""Run the rigorous Arb shell-integral certificate.

Example::

    .venv/bin/python experiments/certify_shell_bound.py \
      --output-dir results/certificate_shell_20260913

The command refuses to overwrite an existing output directory.  Every output
record contains exact rational Arb endpoint data and the detached manifest
hash, while the final prose summary is deliberately limited to this
construction's certified integral constant.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.certification.arb_backend import arb, arb_precision, validate_backend  # noqa: E402
from src.certification.integrals import (  # noqa: E402
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_OUTPUT_DIGITS,
    DEFAULT_PRECISION_BITS,
    certify_integrals,
)
from src.certification.provenance import (  # noqa: E402
    json_dump,
    sha256_file,
    utc_now,
    write_manifest,
)


def _default_output() -> tuple[Path, str]:
    stamp = utc_now().replace("-", "").replace(":", "").replace("T", "_").replace("Z", "")
    run_id = f"certificate_shell_{stamp}_{os.getpid()}"
    return ROOT / "results" / run_id, run_id


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=DEFAULT_N, dest="n_cells", help="x midpoint cells")
    parser.add_argument("--M", type=int, default=DEFAULT_M, dest="m_cells", help="angular midpoint cells")
    parser.add_argument("--precision-bits", type=int, default=DEFAULT_PRECISION_BITS)
    parser.add_argument("--digits", type=int, default=DEFAULT_OUTPUT_DIGITS)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output, default_run_id = _default_output()
    if args.output_dir is not None:
        output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
        default_run_id = output.name
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing immutable run directory: {output}")
    if args.n_cells <= 0 or args.m_cells <= 0 or args.precision_bits < 64 or args.digits < 20:
        raise SystemExit("N, M, precision-bits and digits must be positive (digits >= 20; precision >= 64)")
    output.mkdir(parents=True)

    with arb_precision(args.precision_bits):
        backend = validate_backend()
    result = certify_integrals(
        args.n_cells,
        args.m_cells,
        precision_bits=args.precision_bits,
        output_digits=args.digits,
    )
    result.update(
        {
            "run_id": default_run_id,
            "created_utc": utc_now(),
            "arb_backend_validation": backend,
            "result_status": "rigorous_integral_certificate_for_shell_candidate",
            "claim_boundary": "This certifies the displayed integral arithmetic only; topology, geometry and global optimality retain the proof-note labels.",
            "threshold_check": {
            "requested": "alpha_upper < 11.407",
                "passed": result["alpha_upper_lt_11_407"],
                "upper_endpoint_decimal": result["alpha_upper_decimal"],
            },
        }
    )
    json_dump(output / "certificate.json", result)

    source_paths = [
        "proofs/TOROIDAL_SHELL_SEPARATION.md",
        "proofs/ADVERSARIAL_REVIEW_001.md",
        "proofs/STAGGERED_BLOCKS_CANDIDATE.md",
        "proofs/THEOREM_002.md",
        "proofs/ADVERSARIAL_REVIEW_002.md",
        "claims/CLAIM-0001.md",
        "claims/CLAIM-0002.md",
        "NORMALIZATION.md",
        "src/certification/arb_backend.py",
        "src/certification/integrals.py",
        "src/certification/provenance.py",
        "src/certification/ARB_API_NOTES.md",
        "experiments/certify_shell_bound.py",
    ]
    manifest = write_manifest(
        output,
        root=ROOT,
        run_id=default_run_id,
        command=" ".join([sys.executable, *sys.argv]),
        parameters={
            "N": args.n_cells,
            "M": args.m_cells,
            "precision_bits": args.precision_bits,
            "output_digits": args.digits,
            "seed": None,
        },
        source_paths=source_paths,
        extra={
            "scientific_status": "rigorous arithmetic certificate; no global-optimum or novelty assertion",
            "output_manifest_hash_file": "manifest.sha256",
        },
    )
    print(f"certificate={output / 'certificate.json'}")
    print(f"alpha_upper={result['alpha_upper_decimal']}")
    print(f"optional_staggered_alpha2_upper={result['optional_staggered_rescaling']['alpha2_upper_decimal']}")
    print(f"manifest={output / 'manifest.json'}")
    print(f"manifest_sha256={sha256_file(output / 'manifest.json')}")
    print(f"threshold_passed={result['threshold_check']['passed']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
