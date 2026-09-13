"""Reproduce periodic-phase and same-M nonuniform-spacing investigations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.discovery.periodic_staggering import (
    certify_geometry, certify_nonuniform, periodic_grid_search,
    propose_nonuniform, propose_periodic,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "results/staggering_generalization_20260913")
    parser.add_argument("--angular-cells", type=int, default=1024)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {"python": platform.python_version(), "periodic_grid": [],
              "finite_periodic": [], "nonuniform": [],
              "scope": "finite certified constructions and analytic row-model theorem; no global ropelength optimum or novelty claim"}
    for p in range(1, 17):
        report["periodic_grid"].append(periodic_grid_search(p))
    for p in [3, 4, 5, 6, 7, 8, 12]:
        for pattern in ["optimized", "constant_step", "equally_spaced"]:
            proposal = propose_periodic(p, pattern=pattern)
            certificate = certify_geometry(proposal)
            report["finite_periodic"].append({"proposal": proposal, "certificate": certificate})
    for T in [9, 16, 36, 64, 128]:
        proposal = propose_nonuniform(T)
        certificate = certify_nonuniform(proposal, angular_cells=args.angular_cells)
        report["nonuniform"].append({"proposal": proposal, "certificate": certificate})
        print(f"T={T} M={certificate['M']} gain(%)={certificate['reduction_percent']['arb']}", flush=True)
    report["code_sha256"] = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [Path(__file__).resolve(), ROOT / "src/discovery/periodic_staggering.py",
                  ROOT / "src/certification/shell_family.py",
                  ROOT / "src/certification/arb_backend.py"]}
    path = args.output / "investigation.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
