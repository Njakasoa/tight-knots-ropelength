#!/usr/bin/env python3
"""Search relative phase versus radial gap for adjacent toroidal shells.

The command is deliberately gated on the reviewed M1 PASS record. It writes a
new immutable result directory containing every optimizer trial, uniform phase
seed, constraint expression, independent high-resolution phase-grid check, and
an Arb certificate for a conservatively rounded selected pair.

Example:

    .venv/bin/python experiments/discover_phase_packing.py \
      --output-dir results/discovery_phase_20260913

The output concerns the reviewed pairwise lower bound only. It does not certify
a full bundle, a link closure, a ropelength, or a global optimum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.certification.provenance import git_metadata, json_dump, utc_now, write_manifest  # noqa: E402
from src.discovery.phase_search import (  # noqa: E402
    DEFAULT_A_FRACTIONS,
    DEFAULT_T_VALUES,
    build_pair_spec,
    search_pair,
)


def read_m1_pass_gate(path: str | Path) -> dict[str, Any]:
    """Read the authoritative M1 PASS heading before any search is run."""

    gate_path = Path(path)
    if not gate_path.is_file():
        return {
            "status": "MISSING",
            "passed": False,
            "path": str(gate_path),
            "reason": "M1 review file is missing",
        }
    text = gate_path.read_text(encoding="utf-8")
    verdict = text.split("## Verdict", 1)[1] if "## Verdict" in text else ""
    passed = bool(re.search(r"\*\*PASS for M1:", verdict))
    return {
        "status": "PASS" if passed else "NOT_PASS",
        "passed": passed,
        "path": str(gate_path),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "reason": (
            "authoritative M1 review contains PASS for M1"
            if passed
            else "authoritative M1 review does not contain PASS for M1"
        ),
    }


def _default_output() -> Path:
    stamp = utc_now().replace("-", "").replace(":", "").replace("T", "_").replace("Z", "")
    candidate = ROOT / "results" / f"discovery_phase_{stamp}_{os.getpid()}"
    suffix = 1
    while candidate.exists():
        suffix += 1
        candidate = ROOT / "results" / f"discovery_phase_{stamp}_{os.getpid()}_{suffix}"
    return candidate


def _fraction_list(values: list[str]) -> list[Fraction]:
    try:
        parsed = [Fraction(value) for value in values]
    except (ValueError, ZeroDivisionError) as exc:
        raise SystemExit(f"invalid --a-fraction value: {exc}") from exc
    if len(set(parsed)) != len(parsed):
        raise SystemExit("a-fraction values must be unique")
    return parsed


def _fraction_filename(value: Fraction) -> str:
    return f"{value.numerator}_{value.denominator}"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, nargs="+", default=list(DEFAULT_T_VALUES))
    parser.add_argument(
        "--a-fraction",
        "--a-fractions",
        dest="a_fractions",
        nargs="+",
        default=[f"{item.numerator}/{item.denominator}" for item in DEFAULT_A_FRACTIONS],
        help="fractions of the admissible inner-radius maximum",
    )
    parser.add_argument("--delta-lower", type=float, default=1.001)
    parser.add_argument("--delta-upper", type=float, default=2.2)
    parser.add_argument("--grid-points", type=int, default=10001)
    parser.add_argument("--de-maxiter", type=int, default=80)
    parser.add_argument("--de-popsize", type=int, default=8)
    parser.add_argument("--uniform-seeds", type=int, default=9)
    parser.add_argument("--seed", type=int, default=7013)
    parser.add_argument("--precision-bits", type=int, default=224)
    parser.add_argument("--digits", type=int, default=50)
    parser.add_argument("--no-certify", action="store_true")
    parser.add_argument(
        "--m1-review",
        type=Path,
        default=ROOT / "benchmarks" / "M1_REVIEW.md",
        help="M1 PASS gate file (read before output creation)",
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    gate = read_m1_pass_gate(args.m1_review)
    if not gate["passed"]:
        raise SystemExit(
            f"M1 PASS gate required before phase search: {gate['reason']} ({gate['path']})"
        )

    if any(value <= 0 for value in args.T):
        raise SystemExit("T values must be positive")
    if len(set(args.T)) != len(args.T):
        raise SystemExit("T values must be unique")
    fractions = _fraction_list(args.a_fractions)
    output = args.output_dir
    if output is None:
        output = _default_output()
    elif not output.is_absolute():
        output = ROOT / output
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing immutable result directory: {output}")
    output.mkdir(parents=True, exist_ok=False)

    started = time.monotonic()
    records: list[dict[str, Any]] = []
    for t_index, t_shells in enumerate(args.T):
        for fraction_index, fraction in enumerate(fractions):
            spec = build_pair_spec(
                t_shells,
                fraction,
                delta_lower=args.delta_lower,
                delta_upper=args.delta_upper,
            )
            result = search_pair(
                spec,
                seed=args.seed + 1009 * t_index + 97 * fraction_index,
                de_maxiter=args.de_maxiter,
                de_popsize=args.de_popsize,
                uniform_seed_count=args.uniform_seeds,
                grid_points=args.grid_points,
                precision_bits=args.precision_bits,
                output_digits=args.digits,
                certify=not args.no_certify,
            )
            records.append(result)
            pair_path = output / (
                f"pair_T{t_shells}_a{_fraction_filename(fraction)}.json"
            )
            json_dump(pair_path, result)

    observed_by_population = []
    for result in records:
        selected = result["selected"]
        grid = result["grid_crosscheck"]
        observed_by_population.append(
            {
                "T": result["pair"]["T_shells"],
                "a_fraction": result["pair"]["a_fraction_of_admissible_inner_radius"],
                "N": result["pair"]["population_N"],
                "fopt_machine_observed": selected["phase_fraction"],
                "delta_min_machine_observed": selected["radial_gap_delta"],
                "grid_f_machine_observed": grid["phase_fraction_min_observed"],
                "grid_delta_min_machine_observed": grid["minimal_delta_observed"],
                "optimizer_minus_grid_delta": grid[
                    "optimizer_selected_delta_minus_grid_delta"
                ],
                "arb_status": result["arb_certificate"]["status"],
                "selected_margin_squared": selected["constraint_margin_squared"],
            }
        )

    aggregate = {
        "schema": "discovery-phase-packing-sweep-v1",
        "run_id": output.name,
        "created_utc": utc_now(),
        "result_status": "PASS finite pairwise phase-gap observations",
        "m1_gate": gate,
        "scientific_scope": (
            "Machine search of a conservative adjacent-shell lower bound. "
            "No full-bundle certificate, closure/isotopy proof, ropelength result, "
            "global optimum, or publication novelty claim."
        ),
        "family_registry": {
            "family": "T(Q,Q) p=1 adjacent equal-population toroidal-shell pair",
            "Q": (
                "N per shell for this pair; each record exposes its derived N; "
                "full-link Q is unsupported by this diagnostic"
            ),
            "shell_count": 2,
            "populations": "inner_N=outer_N=N from the safe inner-shell floor",
            "pitch": "fixed p=1 toroidal pitch; not varied",
            "radii": "a and b=a+delta inside fixed R=4*T+2",
            "phase": "relative fraction f in [0,1] on equal N-gon grids; no target seeded",
            "closure": "R >= 2*b+2 checked for all requested deltas",
            "symmetry": "equal N-gon phase grids; relative phase only is searched",
            "free_search_fields": ["phase_fraction_f", "radial_gap_delta"],
            "sweep_fields": ["T_shells", "a_fraction"],
            "fixed_fields": [
                "p=1 winding",
                "equal population on the adjacent pair",
                "R=4*T+2 major-radius rule",
                "safe same-shell capacity floor",
            ],
            "unsupported_fields": [
                "full-bundle Q",
                "non-adjacent-shell phases",
                "pitch optimization",
                "full-link closure/isotopy",
                "ropelength",
            ],
        },
        "parameters": {
            "T": args.T,
            "a_fractions": [_fraction_filename(value) for value in fractions],
            "delta_lower": args.delta_lower,
            "delta_upper": args.delta_upper,
            "grid_points": args.grid_points,
            "de_maxiter": args.de_maxiter,
            "de_popsize": args.de_popsize,
            "uniform_seed_count": args.uniform_seeds,
            "seed": args.seed,
            "precision_bits": args.precision_bits,
            "output_digits": args.digits,
            "certify": not args.no_certify,
        },
        "observed_by_population": observed_by_population,
        "records": records,
        "runtime_seconds": round(time.monotonic() - started, 3),
        "git": git_metadata(ROOT),
    }
    json_dump(output / "search.json", aggregate)
    json_dump(
        output / "summary_by_population.json",
        {
            "schema": "discovery-phase-summary-v1",
            "claim_boundary": aggregate["scientific_scope"],
            "observed_by_population": observed_by_population,
        },
    )

    source_paths = [
        "benchmarks/M1_REVIEW.md",
        "proofs/THEOREM_002.md",
        "proofs/ADVERSARIAL_REVIEW_002.md",
        "src/discovery/phase_search.py",
        "src/certification/arb_backend.py",
        "src/certification/shell_family.py",
        "src/certification/provenance.py",
        "experiments/discover_phase_packing.py",
        "tests/test_discovery.py",
    ]
    write_manifest(
        output,
        root=ROOT,
        run_id=output.name,
        command=" ".join([sys.executable, *sys.argv]),
        parameters=aggregate["parameters"],
        source_paths=source_paths,
        extra={
            "scientific_status": aggregate["scientific_scope"],
            "m1_gate_status": gate["status"],
            "observed_output": "summary_by_population.json",
        },
    )
    print(f"run={output}")
    for row in observed_by_population:
        print(
            f"T={row['T']} a={row['a_fraction']} N={row['N']} "
            f"f_obs={row['fopt_machine_observed']:.10f} "
            f"delta_obs={row['delta_min_machine_observed']:.10f} "
            f"grid_delta={row['grid_delta_min_machine_observed']:.10f} "
            f"arb={row['arb_status']}"
        )
    print(f"summary={output / 'summary_by_population.json'}")
    print(f"manifest={output / 'manifest.json'}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
