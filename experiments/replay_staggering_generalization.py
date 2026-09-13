"""Replay archived exact inputs without invoking the floating search."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.discovery.periodic_staggering import certify_geometry, certify_nonuniform


def main():
    path = ROOT / "results/staggering_generalization_20260913/investigation.json"
    data = json.loads(path.read_text())
    for name, digest in data["code_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Source code changed: {name}")
    for entry in data["finite_periodic"]:
        if certify_geometry(entry["proposal"]) != entry["certificate"]:
            raise ValueError("Periodic replay differs from archived certificate")
    for entry in data["nonuniform"]:
        c = entry["certificate"]
        replay = certify_nonuniform(entry["proposal"], angular_cells=c["angular_cells"],
                                    precision_bits=c["precision_bits"])
        if replay != c:
            raise ValueError("Nonuniform replay differs from archived certificate")
    n, m = len(data["finite_periodic"]), len(data["nonuniform"])
    report = {"status": "PASS", "saved_input_replays": n + m, "periodic": n,
              "nonuniform": m, "code_hashes_match": True,
              "source_result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    path.with_name("replay.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {n+m} exact-input replays; source hashes match")


if __name__ == "__main__":
    main()
