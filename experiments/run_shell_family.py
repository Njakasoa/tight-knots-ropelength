#!/usr/bin/env python3
"""Reproduce finite shell-family populations and diagnostic geometries.

Example::

    .venv/bin/python experiments/run_shell_family.py \
      --T 1 2 4 8 16 --output-dir results/finite_shell_20260913

The population capacities and finite length estimates use Arb.  The geometry
JSON files contain decimal samples solely for inspection by polygon tools and
are explicitly marked as non-certifying samples.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.certification.arb_backend import arb_precision, validate_backend  # noqa: E402
from src.certification.integrals import certify_integrals  # noqa: E402
from src.certification.provenance import json_dump, sha256_file, utc_now, write_manifest  # noqa: E402
from src.certification.shell_family import (  # noqa: E402
    finite_family_record,
    populations_for_t,
    staggered_family_record,
    staggered_populations_for_t,
    write_sampled_geometry,
)


def _default_output() -> tuple[Path, str]:
    stamp = utc_now().replace("-", "").replace(":", "").replace("T", "_").replace("Z", "")
    run_id = f"finite_shell_family_{stamp}_{os.getpid()}"
    return ROOT / "results" / run_id, run_id


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, nargs="+", default=[1, 2, 4, 8, 16])
    parser.add_argument("--length-cells", type=int, default=512)
    parser.add_argument("--geometry-samples", type=int, default=64)
    parser.add_argument("--precision-bits", type=int, default=192)
    parser.add_argument("--digits", type=int, default=60)
    parser.add_argument(
        "--include-staggered",
        action="store_true",
        help="also reproduce reviewed Theorem 002 equal-population blocks",
    )
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
    if any(t <= 0 for t in args.T) or args.length_cells <= 0 or args.geometry_samples < 4:
        raise SystemExit("T values and length-cells must be positive; geometry-samples must be >= 4")
    if len(set(args.T)) != len(args.T):
        raise SystemExit("T values must be unique")
    output.mkdir(parents=True)

    with arb_precision(args.precision_bits):
        backend = validate_backend()
    staggered_rescaling = (
        certify_integrals(
            256,
            512,
            precision_bits=args.precision_bits,
            output_digits=args.digits,
        )
        if args.include_staggered
        else None
    )
    finite_records = []
    staggered_records = []
    for t_shells in args.T:
        record = finite_family_record(
            t_shells,
            angular_cells=args.length_cells,
            precision_bits=args.precision_bits,
            output_digits=args.digits,
        )
        finite_records.append(record)
        json_dump(output / f"shell_T{t_shells}.json", record)
        populations = populations_for_t(
            t_shells,
            mode="shell_specific",
            precision_bits=args.precision_bits,
        )
        write_sampled_geometry(
            output / "geometry" / f"shell_T{t_shells}.json",
            t_shells,
            populations,
            parameter_count=args.geometry_samples,
        )
        if args.include_staggered:
            staggered = staggered_family_record(
                t_shells,
                angular_cells=args.length_cells,
                precision_bits=args.precision_bits,
                output_digits=args.digits,
            )
            staggered_records.append(staggered)
            json_dump(output / f"staggered_T{t_shells}.json", staggered)
            staggered_R, staggered_populations = staggered_populations_for_t(
                t_shells, precision_bits=args.precision_bits
            )
            write_sampled_geometry(
                output / "geometry" / f"staggered_T{t_shells}.json",
                t_shells,
                staggered_populations,
                parameter_count=args.geometry_samples,
                major_radius=float(staggered_R),
            )

    aggregate = {
        "run_id": default_run_id,
        "created_utc": utc_now(),
        "result_status": "finite_shell_family_reproduction_with_Arb_populations_and_lengths",
        "claim_boundary": "Finite samples do not certify geometry or topology; analytic proof obligations and labels are retained.",
        "arb_backend_validation": backend,
        "parameters": {
            "T": args.T,
            "length_cells": args.length_cells,
            "geometry_samples": args.geometry_samples,
            "precision_bits": args.precision_bits,
            "output_digits": args.digits,
            "seeds": None,
            "include_staggered": args.include_staggered,
        },
        "records": [
            {
                "T": item["family"]["t_shells"],
                "Q_shell_specific": item["family"]["bundle_components_Q_shell_specific"],
                "M_shell_specific": item["family"]["total_components_M_shell_specific"],
                "Q_common": item["family"]["bundle_components_Q_common"],
                "M_common": item["family"]["total_components_M_common"],
                "coefficient_shell_specific": item["coefficient_shell_specific"],
                "coefficient_common_hole": item["coefficient_common_hole"],
            }
            for item in finite_records
        ],
        "published_model_references": finite_records[0]["published_model_references"] if finite_records else {},
        "staggered_records": [
            {
                "T": item["family"]["t_shells"],
                "Q": item["family"]["bundle_components_Q"],
                "M": item["family"]["total_components_M"],
                "coefficient": item["coefficient"],
            }
            for item in staggered_records
        ],
        "staggered_status": (
            "included; finite candidate follows proofs/THEOREM_002.md and its numerical coefficient remains conditional"
            if args.include_staggered
            else "not requested"
        ),
        "staggered_asymptotic_rescaling": (
            staggered_rescaling["optional_staggered_rescaling"] if staggered_rescaling else None
        ),
    }
    json_dump(output / "shell_family.json", aggregate)

    source_paths = [
        "proofs/TOROIDAL_SHELL_SEPARATION.md",
        "proofs/ADVERSARIAL_REVIEW_001.md",
        "proofs/THEOREM_002.md",
        "proofs/ADVERSARIAL_REVIEW_002.md",
        "claims/CLAIM-0001.md",
        "claims/CLAIM-0002.md",
        "NORMALIZATION.md",
        "src/certification/arb_backend.py",
        "src/certification/shell_family.py",
        "src/certification/integrals.py",
        "src/certification/provenance.py",
        "src/certification/ARB_API_NOTES.md",
        "experiments/run_shell_family.py",
    ]
    write_manifest(
        output,
        root=ROOT,
        run_id=default_run_id,
        command=" ".join([sys.executable, *sys.argv]),
        parameters=aggregate["parameters"],
        source_paths=source_paths,
        extra={
            "scientific_status": (
                "finite reproduction; shell-specific rule is an analytic sufficient rule, not an occupancy optimum; "
                "staggered block candidate is reviewed mathematically but its finite coefficient remains conditional"
                if args.include_staggered
                else "finite reproduction; shell-specific rule is an analytic sufficient rule, not an occupancy optimum"
            ),
            "output_manifest_hash_file": "manifest.sha256",
        },
    )
    print(f"run={output}")
    for item in aggregate["records"]:
        print(
            f"T={item['T']} M_specific={item['M_shell_specific']} "
            f"M_common={item['M_common']} "
            f"specific_alpha_upper={item['coefficient_shell_specific']['upper']['decimal']}"
        )
    for item in aggregate["staggered_records"]:
        print(
            f"T={item['T']} staggered_M={item['M']} "
            f"staggered_alpha_upper={item['coefficient']['upper']['decimal']}"
        )
    if aggregate["staggered_asymptotic_rescaling"] is not None:
        print(
            "optional_staggered_alpha2_upper="
            + aggregate["staggered_asymptotic_rescaling"]["alpha2_upper_decimal"]
        )
    print(f"manifest={output / 'manifest.json'}")
    print(f"manifest_sha256={sha256_file(output / 'manifest.json')}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
