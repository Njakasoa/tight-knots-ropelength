#!/usr/bin/env python3
"""Run reproducible circle, Hopf and torus-trefoil controls.

Each invocation writes a fresh JSON record and a separate hash manifest.  The
writer never replaces an earlier record, which keeps exploratory runs and
their exact parameters auditable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "src"))

from contacts import extract_contacts
from curves import exact_circle_control, exact_hopf_control, hopf_link, circle, torus_link
from thickness import polygon_thickness, smooth_thickness
from topology import topology_report


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _git_commit() -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _git_status() -> str | None:
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=REPOSITORY, check=True, capture_output=True, text=True)
        return result.stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return "inf" if value > 0 else "-inf" if value < 0 else "nan"
    return value


def _record_component(value: Any, *, resolution: int, scale: float) -> dict[str, Any]:
    arrays = [component.sample(resolution) * float(scale) for component in value.components]
    polygon_input = arrays[0] if len(arrays) == 1 else arrays
    thickness = polygon_thickness(polygon_input)
    graph = extract_contacts(polygon_input, thickness_result=thickness, tolerance=1e-3)
    return {
        "resolution": int(resolution),
        "scale": float(scale),
        "polygon_length": float(thickness.length),
        "polygon_thickness": thickness.as_dict(),
        "contacts": graph.summary,
    }


def _curve_record(name: str, curve: Any, *, resolutions: list[int], scales: list[float]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for scale in scales:
        smooth = smooth_thickness(curve, samples=max(resolutions))
        for resolution in resolutions:
            item = _record_component(curve, resolution=resolution, scale=scale)
            item["smooth_diagnostic"] = {
                **smooth.as_dict(),
                "length": smooth.length * float(scale),
                "thickness": smooth.thickness * float(scale),
                "curvature_radius": smooth.curvature_radius * float(scale),
                "dcsd": smooth.dcsd * float(scale),
                "ropelength": smooth.ropelength,
            }
            records.append(item)
    exact: dict[str, Any] | None = None
    if name == "circle":
        exact = exact_circle_control(radius=1, terms=12)
    elif name == "hopf":
        exact = exact_hopf_control(circle_radius=2, terms=12)
    topology = topology_report(curve, samples=max(resolutions))
    return {
        "name": name,
        "analytic_length": float(curve.length()),
        "analytic_metadata": _json_safe(curve.metadata),
        "exact_control": exact,
        "topology": topology.as_dict(),
        "resolutions": records,
    }


def run_controls(*, resolutions: list[int], scales: list[float], seed: int | None, output_dir: Path) -> tuple[Path, Path]:
    started = time.perf_counter()
    if not resolutions or any(int(item) < 8 for item in resolutions):
        raise ValueError("resolutions must contain integers >= 8")
    if not scales or any(float(item) <= 0 for item in scales):
        raise ValueError("scales must be positive")
    if seed is not None:
        np.random.default_rng(seed)  # Explicitly record the seed even though controls are deterministic.
    curves = {
        "circle": circle(radius=1),
        "hopf": hopf_link(radius=2),
        "trefoil_torus_2_3": torus_link(2, 3, major_radius=3, minor_radius=1),
    }
    data = {
        "schema": "tight-knots-lab/control-run/v1",
        "started_utc": _utc_now(),
        "source_commit": _git_commit(),
        "working_tree_status": _git_status(),
        "parameters": {
            "resolutions": [int(item) for item in resolutions],
            "scales": [float(item) for item in scales],
            "seed": seed,
            "normalization": "radius",
            "tolerances": {
                "polygon": {
                    "distance": 1e-9,
                    "relative_distance": 1e-9,
                    "orthogonality": 1e-8,
                    "endpoint": 1e-8,
                    "degeneracy": 1e-12,
                },
                "projection": 1e-9,
                "contacts": 1e-3,
            },
        },
        "controls": {
            name: _curve_record(name, curve, resolutions=resolutions, scales=scales) for name, curve in curves.items()
        },
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "numpy": np.__version__,
        },
    }
    data["finished_utc"] = _utc_now()
    data["runtime"]["elapsed_seconds"] = time.perf_counter() - started
    payload = (json.dumps(_json_safe(data), sort_keys=True, indent=2) + "\n").encode("utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = f"controls_{stamp}_{uuid.uuid4().hex[:10]}"
    output_path = output_dir / f"{stem}.json"
    manifest_path = output_dir / f"{stem}.manifest.json"
    # O_EXCL semantics avoid replacing an old record if a clock/UUID collision occurs.
    with output_path.open("xb") as handle:
        handle.write(payload)
    input_hashes = {
        "control_parameters": _sha256_bytes(json.dumps(data["parameters"], sort_keys=True).encode("utf-8")),
    }
    for source in sorted((REPOSITORY / "src").rglob("*.py")):
        input_hashes[str(source.relative_to(REPOSITORY))] = _sha256_file(source)
    input_hashes["experiments/run_controls.py"] = _sha256_file(Path(__file__))
    reference = REPOSITORY / "data" / "reference" / "trefoil_3.1_ridgerunner.vect"
    if reference.exists():
        input_hashes[str(reference.relative_to(REPOSITORY))] = _sha256_file(reference)
    manifest = {
        "schema": "tight-knots-lab/control-run-manifest/v1",
        "created_utc": _utc_now(),
        "output_file": output_path.name,
        "output_sha256": _sha256_bytes(payload),
        "input_hashes": input_hashes,
        "source_commit": data["source_commit"],
    }
    with manifest_path.open("xb") as handle:
        handle.write((json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    return output_path, manifest_path


def _parse_int_list(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def _parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolutions", default="32,64", help="comma-separated samples per component")
    parser.add_argument("--scales", default="0.5,1,2", help="comma-separated geometric scale factors")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", type=Path, default=REPOSITORY / "results" / "controls")
    args = parser.parse_args(argv)
    output, manifest = run_controls(resolutions=_parse_int_list(args.resolutions), scales=_parse_float_list(args.scales), seed=args.seed, output_dir=args.output_dir)
    print(json.dumps({"output": str(output), "manifest": str(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
