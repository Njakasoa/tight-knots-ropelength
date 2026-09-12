"""Freeze independent M2 grammar and repository-suite evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "bin" / "python"
FOCUSED = ROOT / "tests" / "independent" / "test_discovery_grammar_independent.py"
ZERO_COLOUR = ROOT / "tests" / "test_vect_zero_colors.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def counts(output: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for label in ("passed", "failed", "skipped", "xfailed", "xpassed", "error"):
        match = re.search(rf"(\d+)\s+{label}", output)
        if match:
            result[label] = int(match.group(1))
    return result


def run(command: list[str]) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "counts": counts(completed.stdout + "\n" + completed.stderr),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "reviewer_m2_20260913.json")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing evidence: {output}")

    focused = run([str(PYTHON), "-m", "pytest", "-q", str(FOCUSED.relative_to(ROOT)), str(ZERO_COLOUR.relative_to(ROOT))])
    full = run([str(PYTHON), "-m", "pytest", "-q"])
    prefix = output.with_suffix("")
    focused_stdout = prefix.with_name(prefix.name + ".focused.stdout.txt")
    focused_stderr = prefix.with_name(prefix.name + ".focused.stderr.txt")
    full_stdout = prefix.with_name(prefix.name + ".full.stdout.txt")
    full_stderr = prefix.with_name(prefix.name + ".full.stderr.txt")
    focused_stdout.write_text(focused["stdout"], encoding="utf-8")
    focused_stderr.write_text(focused["stderr"], encoding="utf-8")
    full_stdout.write_text(full["stdout"], encoding="utf-8")
    full_stderr.write_text(full["stderr"], encoding="utf-8")

    variable_dir = ROOT / "results" / "variable_pitch_20260912T224501767133Z"
    cluster_dir = ROOT / "results" / "contact_clusters_20260912T224627301208Z"
    variable = json.loads((variable_dir / "search.json").read_text(encoding="utf-8"))
    clusters = json.loads((cluster_dir / "comparison.json").read_text(encoding="utf-8"))
    records = []
    for item in variable["records"]:
        records.append(
            {
                "seed": item["seed"],
                "parameters": item["parameters"],
                "baseline_coarse": item["baseline_coarse"],
                "coarse_ropelength": item["coarse_ropelength"],
                "at48": item["at48"],
                "at96": item["at96"],
                "ridgerunner_returncode": item["ridgerunner_returncode"],
                "final": item["final"],
                "final_ropelength": item["final_ropelength"],
            }
        )
    cluster_records = []
    for item in clusters["records"]:
        cluster_records.append(
            {
                "seed": item["seed"],
                "geometry": item["geometry"],
                "geometry_sha256": item["sha256"],
                "components": item["components"],
                "vertices": item["vertices"],
                "thickness_polygonal": item["thickness_polygonal"],
                "ropelength_independent_engine": item["ropelength_independent_engine"],
                "ropelength_plcurve": item["ropelength_plcurve"],
                "relative_ropelength_difference": item["relative_ropelength_difference"],
                "projection_checks": [
                    {"direction": p["direction"], "generic": p["generic"], "all_pair_abs_one": p.get("all_pair_abs_one")}
                    for p in item["projections"]
                ],
                "contact_counts": [f["contact_count"] for f in item["features"]],
                "active_kink_counts": [f["active_kink_count"] for f in item["features"]],
            }
        )

    source_paths = [
        FOCUSED,
        ZERO_COLOUR,
        ROOT / "src" / "discovery" / "grammar.py",
        ROOT / "experiments" / "search_variable_pitch.py",
        ROOT / "experiments" / "cluster_pitch_contacts.py",
        ROOT / "src" / "curves" / "vect.py",
        ROOT / "proofs" / "VARIABLE_PITCH_TOPOLOGY.md",
        ROOT / "results" / "discovery_phase_20260913_v1" / "search.json",
        variable_dir / "search.json",
        cluster_dir / "comparison.json",
        ROOT / "data" / "reference" / "cantarella-atlas" / "knots" / "prime" / "3-10" / "3_1.vect",
        ROOT / "data" / "reference" / "cantarella-atlas" / "knots" / "prime" / "3-10" / "3_1.tsv",
        ROOT / "data" / "reference" / "cantarella-atlas" / "MANIFEST.json",
    ]
    phase_search = json.loads((ROOT / "results" / "discovery_phase_20260913_v1" / "search.json").read_text())
    evidence = {
        "schema": "independent-m2-validation-v1",
        "status": "PASS" if focused["returncode"] == 0 and full["returncode"] == 0 else "FAIL",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "focused_pytest": {
            "command": focused["command"],
            "returncode": focused["returncode"],
            "duration_seconds": focused["duration_seconds"],
            "counts": focused["counts"],
            "stdout_file": focused_stdout.name,
            "stderr_file": focused_stderr.name,
        },
        "full_pytest": {
            "command": full["command"],
            "returncode": full["returncode"],
            "duration_seconds": full["duration_seconds"],
            "counts": full["counts"],
            "stdout_file": full_stdout.name,
            "stderr_file": full_stderr.name,
        },
        "independent_checks": {
            "derivatives": "independent coordinate formula plus five-point finite differences for first and second derivatives",
            "homotopies": ["beta to zero", "phase offsets to zero", "positive diagonal scale to identity"],
            "proper_doubling": "det(P)=+1 and sampled core separation lower bound checked",
            "failure_paths": "invalid configurations, indices, nonfinite parameters, unsupported orders, samples, homotopy fractions, bundles, and scales",
            "canonical_zero_colour_atlas": "3_1.vect parsed after consuming its zero per-component colour row and compared exactly to independently parsed 3_1.tsv",
        },
        "variable_pitch_search": {
            "source_dir": str(variable_dir.relative_to(ROOT)),
            "source_search_sha256": sha256(variable_dir / "search.json"),
            "records": records,
            "claim_boundary": variable["claim_boundary"],
        },
        "contact_clusters": {
            "source_dir": str(cluster_dir.relative_to(ROOT)),
            "source_comparison_sha256": sha256(cluster_dir / "comparison.json"),
            "records": cluster_records,
            "clusters": clusters["clusters"],
            "claim_boundary": clusters["claim_boundary"],
        },
        "phase_search_context": {
            "source": "results/discovery_phase_20260913_v1/search.json",
            "source_sha256": sha256(ROOT / "results" / "discovery_phase_20260913_v1" / "search.json"),
            "scientific_status": phase_search.get("scientific_status", phase_search.get("scientific_scope")),
        },
        "source_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in source_paths},
        "environment": {"python": sys.version.replace("\n", " "), "platform": platform.platform(), "machine": platform.machine()},
        "claim_boundary": "This evidence validates the grammar formulas, derivative implementation against an independent reference, construction-level homotopy hypotheses, failure-path rejection, and repository regressions. It does not certify polygonal reach/thickness, solver paths, a smooth ropelength bound, finite-M optimality, or a global topology/optimization claim.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    output.write_text(serialized, encoding="utf-8")
    manifest = {
        "schema": "independent-m2-validation-manifest-v1",
        "evidence_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "runner_sha256": sha256(Path(__file__)),
        "files": {},
    }
    for path in sorted(output.parent.glob(output.stem + ".*")):
        if path.name in {output.name, output.with_name(output.stem + ".manifest.json").name, output.with_name(output.stem + ".manifest.sha256").name}:
            continue
        manifest["files"][path.name] = sha256(path)
    manifest_path = output.with_name(output.stem + ".manifest.json")
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    detached = output.with_name(output.stem + ".manifest.sha256")
    detached.write_text(hashlib.sha256(manifest_text.encode("utf-8")).hexdigest() + "  " + manifest_path.name + "\n", encoding="utf-8")
    print(json.dumps({"status": evidence["status"], "focused": evidence["focused_pytest"], "full": evidence["full_pytest"], "output": str(output)}, indent=2, sort_keys=True))
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
