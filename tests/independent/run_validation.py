"""Run the independent M1 suite and store an immutable evidence bundle.

The runner intentionally invokes the project's virtual-environment Python by
absolute path and records the exact command, source state, dependency
versions, reference hashes, and complete pytest output.  A run directory is
never reused: pass ``--output-dir`` for a reviewable, named evidence bundle.
"""

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


ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / ".venv" / "bin" / "python"
TEST_FILE = ROOT / "tests" / "independent" / "test_independent_validation.py"
ROPELENGTH = ROOT / "vendor" / "deps" / "libplcurve-10.1.0" / "build" / "bin" / "ropelength"
REFERENCE_FILES = (
    ROOT / "data" / "reference" / "trefoil_3.1_ridgerunner.vect",
    ROOT / "data" / "reference" / "trefoil_3.1_plcurve_kl400.vect",
    ROOT / "data" / "reference" / "cantarella-atlas" / "MANIFEST.json",
    ROOT / "results" / "ridgerunner_autoscaled_20260913" / "trefoil47.rr" / "trefoil47.final.vect",
    ROOT / "results" / "ridgerunner_autoscaled_20260913" / "trefoil400.rr" / "trefoil400.final.vect",
)


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(*args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def _version_probe() -> dict[str, str]:
    code = (
        "import platform,sys; "
        "print('python='+sys.version.replace('\\n',' ')); "
        "print('platform='+platform.platform()); "
        "mods=('numpy','scipy','mpmath','flint','pytest'); "
        "\nfor name in mods:\n"
        " try:\n  module=__import__(name); print(name+'='+str(getattr(module,'__version__','unknown')))\n"
        " except Exception as exc: print(name+'=ERROR:'+type(exc).__name__)"
    )
    try:
        completed = subprocess.run(
            [str(PYTHON), "-c", code], cwd=ROOT, check=True, capture_output=True, text=True
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return {"probe_error": type(exc).__name__}
    versions: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        key, separator, value = line.partition("=")
        if separator:
            versions[key] = value
    return versions


def _default_output_dir() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = ROOT / "results" / "independent" / f"validation_{stamp}"
    suffix = 1
    while candidate.exists():
        suffix += 1
        candidate = ROOT / "results" / "independent" / f"validation_{stamp}_{suffix}"
    return candidate


def _summary(output: str) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for label in ("passed", "failed", "skipped", "xfailed", "xpassed", "error"):
        match = re.search(rf"(\d+)\s+{label}", output)
        if match:
            counts[label] = int(match.group(1))
    failed_tests = sorted(set(re.findall(r"FAILED\s+([^\s]+)", output)))
    return {"counts": counts, "failed_tests": failed_tests}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="new evidence directory (default: UTC timestamp under results/independent)",
    )
    args = parser.parse_args()
    output_dir = (ROOT / args.output_dir if args.output_dir and not args.output_dir.is_absolute() else args.output_dir) or _default_output_dir()
    if output_dir.exists():
        raise SystemExit(f"refusing to overwrite existing evidence directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)

    command = [str(PYTHON), "-m", "pytest", "-q", str(TEST_FILE.relative_to(ROOT))]
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except OSError as exc:
        returncode = 127
        stdout = ""
        stderr = f"runner could not execute pytest: {exc}\n"
    elapsed = time.monotonic() - started
    (output_dir / "pytest.stdout.txt").write_text(stdout, encoding="utf-8")
    (output_dir / "pytest.stderr.txt").write_text(stderr, encoding="utf-8")

    # Keep a repository-wide check beside the focused independent run.  The
    # two outputs are separate so a focused green result cannot hide a failure
    # in another test module.
    full_command = [str(PYTHON), "-m", "pytest", "-q"]
    full_started = time.monotonic()
    try:
        full_completed = subprocess.run(full_command, cwd=ROOT, capture_output=True, text=True, check=False)
        full_returncode = full_completed.returncode
        full_stdout = full_completed.stdout
        full_stderr = full_completed.stderr
    except OSError as exc:
        full_returncode = 127
        full_stdout = ""
        full_stderr = f"runner could not execute full pytest: {exc}\n"
    full_elapsed = time.monotonic() - full_started
    (output_dir / "pytest_full.stdout.txt").write_text(full_stdout, encoding="utf-8")
    (output_dir / "pytest_full.stderr.txt").write_text(full_stderr, encoding="utf-8")
    overall_returncode = returncode if returncode else full_returncode

    evidence: dict[str, Any] = {
        "schema": "independent-validation-v1",
        "status": "PASS" if overall_returncode == 0 else "FAIL",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": round(elapsed + full_elapsed, 3),
        "command": command,
        "working_directory": str(ROOT),
        "returncode": overall_returncode,
        "pytest": _summary(stdout + "\n" + stderr),
        "full_pytest": {
            "command": full_command,
            "duration_seconds": round(full_elapsed, 3),
            "returncode": full_returncode,
            "summary": _summary(full_stdout + "\n" + full_stderr),
        },
        "python": str(PYTHON),
        "versions": _version_probe(),
        "host": {"platform": platform.platform(), "machine": platform.machine()},
        "source": {
            "repository_commit": _git("rev-parse", "HEAD"),
            "working_tree_status": _git("status", "--short"),
            "test_sha256": _sha256(TEST_FILE),
            "runner_sha256": _sha256(Path(__file__)),
        },
        "external_tools": {
            "ropelength": str(ROPELENGTH),
            "ropelength_sha256": _sha256(ROPELENGTH),
            "plcurve_commit": _git("-C", str(ROOT / "vendor" / "plcurve"), "rev-parse", "HEAD"),
            "ridgerunner_commit": _git("-C", str(ROOT / "vendor" / "ridgerunner"), "rev-parse", "HEAD"),
        },
        "reference_sha256": {str(path.relative_to(ROOT)): _sha256(path) for path in REFERENCE_FILES},
        "known_interpretation": (
            "A nonzero return code is retained as evidence. The independent suite "
            "must pass before M1 can be called complete; a torus non-coprime period "
            "failure is a source blocker rather than a tolerance choice."
        ),
    }
    serialized = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    (output_dir / "validation.json").write_text(serialized, encoding="utf-8")
    manifest: dict[str, Any] = {
        "schema": "independent-validation-manifest-v1",
        "files": {},
        "validation_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
    }
    for path in sorted(output_dir.iterdir()):
        if path.name == "manifest.json" or path.name == "manifest.sha256":
            continue
        manifest["files"][path.name] = _sha256(path)
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (output_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")
    (output_dir / "manifest.sha256").write_text(
        hashlib.sha256(manifest_text.encode("utf-8")).hexdigest() + "  manifest.json\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": evidence["status"], "output_dir": str(output_dir), "pytest": evidence["pytest"], "full_pytest": evidence["full_pytest"]}, indent=2, sort_keys=True))
    return overall_returncode


if __name__ == "__main__":
    raise SystemExit(main())
