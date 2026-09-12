"""Immutable run metadata and SHA-256 manifest helpers."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import flint
from flint import ctx


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_metadata(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    result: dict[str, Any] = {"commit": None, "dirty": None}
    try:
        result["commit"] = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        result["dirty"] = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    except (OSError, subprocess.CalledProcessError):
        pass
    return result


def runtime_metadata(*, precision_bits: int) -> dict[str, Any]:
    packages: dict[str, str] = {"python-flint": getattr(flint, "__version__", "unknown")}
    for module_name in ("numpy", "scipy"):
        try:
            module = __import__(module_name)
            packages[module_name] = getattr(module, "__version__", "unknown")
        except ImportError:
            packages[module_name] = "unavailable"
    return {
        "python": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": packages,
        "arb_precision_bits": precision_bits,
        "arb_context_precision_at_metadata": int(ctx.prec),
    }


def source_hashes(root: str | Path, paths: Iterable[str]) -> dict[str, str]:
    root = Path(root)
    records: dict[str, str] = {}
    for relative in paths:
        path = root / relative
        if path.is_file():
            records[relative] = sha256_file(path)
        else:
            records[relative] = "MISSING"
    return records


def json_dump(path: str | Path, value: Mapping[str, Any]) -> None:
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_manifest(
    output_dir: str | Path,
    *,
    root: str | Path,
    run_id: str,
    command: str,
    parameters: Mapping[str, Any],
    source_paths: Iterable[str],
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Write a manifest and its detached hash into an already-created run dir.

    The manifest intentionally excludes ``manifest.json`` and
    ``manifest.sha256`` from its output table; the detached hash covers the
    complete manifest bytes and is written after the manifest itself.
    """

    output = Path(output_dir)
    files: dict[str, str] = {}
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name in {"manifest.json", "manifest.sha256"}:
            continue
        files[str(path.relative_to(output))] = sha256_file(path)
    manifest: dict[str, Any] = {
        "manifest_version": 1,
        "run_id": run_id,
        "created_utc": utc_now(),
        "command": command,
        "git": git_metadata(root),
        "source_hashes": source_hashes(root, source_paths),
        "runtime": runtime_metadata(precision_bits=int(parameters.get("precision_bits", ctx.prec))),
        "parameters": dict(parameters),
        "seeds": None,
        "outputs_sha256": files,
    }
    if extra:
        manifest.update(extra)
    manifest_path = output / "manifest.json"
    json_dump(manifest_path, manifest)
    digest = sha256_file(manifest_path)
    (output / "manifest.sha256").write_text(f"{digest}  manifest.json\n", encoding="utf-8")
    manifest["manifest_sha256"] = digest
    return manifest


__all__ = [
    "git_metadata",
    "json_dump",
    "runtime_metadata",
    "sha256_file",
    "source_hashes",
    "utc_now",
    "write_manifest",
]
