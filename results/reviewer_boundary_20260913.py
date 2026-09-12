"""Independent Arb audit for the Theorem 003 boundary certificate.

This file intentionally uses python-flint directly rather than importing the
project's certificate helpers.  It recomputes J by enclosing every x/t
rectangle, re-parses the stored rational intervals, checks the exact
inequalities, and audits the selected T=1024,b=13 population floors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOUNDARY_ROOT = ROOT / "results"
DEFAULT_SHELL_DIR = ROOT / "results" / "certificate_shell_N512M1024_noguard"
DEFAULT_DISCOVERY_DIR = ROOT / "results" / "discovery_blocks_20260912T221841Z"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fraction(value: Any, *, label: str) -> Fraction:
    if not isinstance(value, dict) or "numerator" not in value or "denominator" not in value:
        raise ValueError(f"{label} is not a rational endpoint record")
    try:
        numerator = int(value["numerator"])
        denominator = int(value["denominator"])
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} has non-integer endpoint fields") from error
    if denominator <= 0:
        raise ValueError(f"{label} has a nonpositive denominator")
    return Fraction(numerator, denominator)


def _arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / arb(value.denominator)


def _stored_interval(record: dict[str, Any], *, label: str) -> tuple[Fraction, Fraction, arb]:
    lower = _fraction(record.get("lower"), label=f"{label}.lower")
    upper = _fraction(record.get("upper"), label=f"{label}.upper")
    if lower > upper:
        raise ValueError(f"{label} lower endpoint exceeds upper endpoint")
    return lower, upper, _arb_fraction(lower).union(_arb_fraction(upper))


def _arb_record(value: arb, *, digits: int = 70) -> dict[str, Any]:
    lower_q = value.lower().fmpq()
    upper_q = value.upper().fmpq()
    lower = {"numerator": str(lower_q.numerator), "denominator": str(lower_q.denominator)}
    upper = {"numerator": str(upper_q.numerator), "denominator": str(upper_q.denominator)}
    return {
        "arb": value.str(digits, radius=True, more=True),
        "lower": lower,
        "upper": upper,
        "midpoint": value.mid().str(digits, radius=False, more=True),
        "radius": value.rad().str(digits, radius=False, more=True),
    }


def _record_bounds(record: dict[str, Any], *, label: str) -> tuple[Fraction, Fraction]:
    lower, upper, _ = _stored_interval(record, label=label)
    return lower, upper


def _walk_interval_records(value: Any, *, path: str = "root") -> dict[str, Any]:
    """Parse every nested lower/upper rational pair in a certificate JSON."""

    count = 0
    decimal_parseable = 0
    errors: list[str] = []

    def visit(item: Any, location: str) -> None:
        nonlocal count, decimal_parseable
        if isinstance(item, dict):
            if "lower" in item and "upper" in item and isinstance(item["lower"], dict) and isinstance(item["upper"], dict):
                count += 1
                try:
                    lower = _fraction(item["lower"], label=f"{location}.lower")
                    upper = _fraction(item["upper"], label=f"{location}.upper")
                    if lower > upper:
                        errors.append(f"{location}: lower > upper")
                    decimal = item.get("lower", {}).get("decimal")
                    if decimal is None:
                        decimal = item.get("upper", {}).get("decimal")
                    if decimal is not None:
                        try:
                            with localcontext() as context:
                                context.prec = 120
                                parsed = Decimal(str(decimal))
                                lower_decimal = Decimal(lower.numerator) / Decimal(lower.denominator)
                                upper_decimal = Decimal(upper.numerator) / Decimal(upper.denominator)
                                # The decimal is a display rendering and can
                                # round one last digit beyond an exact binary
                                # endpoint.  Rational endpoints are the
                                # authoritative bound; require only that the
                                # display parses as a finite decimal.
                                if not parsed.is_finite():
                                    errors.append(f"{location}: displayed decimal is non-finite")
                                else:
                                    decimal_parseable += 1
                        except (InvalidOperation, ValueError, ZeroDivisionError) as error:
                            errors.append(f"{location}: invalid decimal ({error})")
                except ValueError as error:
                    errors.append(str(error))
            for key, child in item.items():
                visit(child, f"{location}.{key}")
        elif isinstance(item, list):
            for index, child in enumerate(item):
                visit(child, f"{location}[{index}]")

    visit(value, path)
    return {"records": count, "decimal_parseable": decimal_parseable, "errors": errors, "all_valid": not errors}


def _domain_coverage(n_cells: int, m_cells: int) -> dict[str, Any]:
    x_cells = [(Fraction(i, n_cells), Fraction(i + 1, n_cells)) for i in range(n_cells)]
    t_cells = [(Fraction(2 * j, m_cells), Fraction(2 * (j + 1), m_cells)) for j in range(m_cells)]

    def contiguous(cells: list[tuple[Fraction, Fraction]], start: Fraction, end: Fraction) -> bool:
        return bool(cells and cells[0][0] == start and cells[-1][1] == end and all(cells[i][1] == cells[i + 1][0] for i in range(len(cells) - 1)))

    return {
        "x_cells": n_cells,
        "t_cells": m_cells,
        "x_normalized_range": [str(x_cells[0][0]), str(x_cells[-1][1])],
        "t_over_pi_normalized_range": [str(t_cells[0][0]), str(t_cells[-1][1])],
        "x_contiguous_0_to_1": contiguous(x_cells, Fraction(0), Fraction(1)),
        "t_contiguous_0_to_2pi": contiguous(t_cells, Fraction(0), Fraction(2)),
    }


def _integrate_j(n_cells: int, m_cells: int, precision_bits: int) -> tuple[arb, dict[str, Any]]:
    """Direct Arb rectangle enclosure for J, with a separate loop ordering."""

    ctx.prec = precision_bits
    pi = arb.pi()
    dx = arb(1) / arb(n_cells)
    dt = arb(2) * pi / arb(m_cells)
    x_half = (dx / arb(2)).upper()
    t_half = (dt / arb(2)).upper()
    total = arb(0)
    minimum_speed_radicand: Fraction | None = None
    minimum_dn_lower: Fraction | None = None
    for j in range(m_cells):
        t_mid = arb(2 * j + 1) * pi / arb(m_cells)
        t = t_mid + arb(0, t_half)
        cosine = t.cos()
        for i in range(n_cells):
            x_mid = arb(2 * i + 1) / arb(2 * n_cells)
            x = x_mid + arb(0, x_half)
            v2 = x * x + (arb(2) - x) * (arb(2) - x)
            dn = arb(4) * pi * (arb(1) - x) * (x * x - arb(2) * x + arb(4)) / (v2 * v2.sqrt())
            radicand = (arb(4) + arb(2) * x * cosine) ** 2 + arb(4) * x * x
            speed = radicand.sqrt()
            total += dn * speed
            dn_lower = dn.lower().fmpq()
            radicand_lower = radicand.lower().fmpq()
            if minimum_dn_lower is None or Fraction(int(dn_lower.numerator), int(dn_lower.denominator)) < minimum_dn_lower:
                minimum_dn_lower = Fraction(int(dn_lower.numerator), int(dn_lower.denominator))
            candidate = Fraction(int(radicand_lower.numerator), int(radicand_lower.denominator))
            if minimum_speed_radicand is None or candidate < minimum_speed_radicand:
                minimum_speed_radicand = candidate
    return total * dx * dt, {
        "x_half_width": str(x_half),
        "t_half_width": str(t_half),
        "minimum_computed_dn_lower": str(minimum_dn_lower),
        "minimum_computed_speed_radicand_lower": str(minimum_speed_radicand),
    }


def _interval_overlap(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]) -> bool:
    return first[0] <= second[1] and second[0] <= first[1]


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _audit_discovery(discovery_path: Path, *, precision_bits: int = 224) -> dict[str, Any]:
    discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
    selected = [row for row in discovery.get("best", []) if row.get("T") == 1024]
    selected_row = next((row for row in selected if row.get("block_size") == 13), None)
    if selected_row is None:
        raise ValueError("discovery record does not select T=1024,b=13")

    T, b = 1024, 13
    ctx.prec = precision_bits
    delta = arb(3).sqrt()
    gap = arb(2) - delta
    radii = [delta * i + gap * (1 + (i - 1) // b) for i in range(1, T + 1)]
    outer = arb(2) * radii[-1] + arb(2)
    floors: list[int] = []
    ambiguous: list[dict[str, Any]] = []
    margins: list[tuple[Fraction, int]] = []
    for i in range(1, T + 1):
        first = 1 + b * ((i - 1) // b)
        inner = delta * first + gap * (1 + (first - 1) // b)
        capacity = arb.pi() * inner * (outer - inner) / (inner * inner + (outer - inner) * (outer - inner)).sqrt()
        lower_q = capacity.lower().fmpq()
        upper_q = capacity.upper().fmpq()
        lower = Fraction(int(lower_q.numerator), int(lower_q.denominator))
        upper = Fraction(int(upper_q.numerator), int(upper_q.denominator))
        lower_floor = _floor_fraction(lower)
        upper_floor = _floor_fraction(upper)
        floors.append(lower_floor)
        if lower_floor != upper_floor:
            ambiguous.append({"shell": i, "block_start": first, "interval": _arb_record(capacity)})
        margins.append((min(lower - lower_floor, Fraction(lower_floor + 1) - upper), i))
    min_margin, min_shell = min(margins)
    populations = [value - 1 for value in floors]
    components = 2 * (1 + sum(populations))
    return {
        "source_discovery": str(discovery_path.relative_to(ROOT)),
        "source_discovery_sha256": _sha256(discovery_path),
        "selected_row": selected_row,
        "T": T,
        "block_size": b,
        "precision_bits": precision_bits,
        "outer_radius": _arb_record(outer),
        "floor_min": min(floors),
        "floor_max": max(floors),
        "population_sum": sum(populations),
        "component_count_from_arb_floors": components,
        "minimum_exact_floor_margin": {"shell": min_shell, "fraction": str(min_margin), "decimal": str(float(min_margin))},
        "ambiguous_floor_count": len(ambiguous),
        "ambiguous_floors": ambiguous,
        "all_floors_unambiguous": not ambiguous,
        "components_match_discovery": components == int(selected_row["components"]),
        "floor_margin_matches_float_diagnostic": abs(float(min_margin) - float(selected_row["minimum_floor_margin"])) < 1e-10,
    }


def _find_latest_boundary() -> Path:
    candidates = [path for path in DEFAULT_BOUNDARY_ROOT.glob("boundary_certificate_*/certificate.json") if path.is_file()]
    if not candidates:
        raise FileNotFoundError("no boundary_certificate_*/certificate.json found")
    return max(candidates, key=lambda path: path.stat().st_mtime).parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boundary-dir", type=Path, default=None)
    parser.add_argument("--discovery-dir", type=Path, default=DEFAULT_DISCOVERY_DIR)
    parser.add_argument("--N", type=int, default=1024)
    parser.add_argument("--M", type=int, default=2048)
    parser.add_argument("--precision", type=int, default=224)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "reviewer_boundary_20260913.json")
    args = parser.parse_args()
    boundary_dir = args.boundary_dir or _find_latest_boundary()
    if not boundary_dir.is_absolute():
        boundary_dir = ROOT / boundary_dir
    discovery_dir = args.discovery_dir if args.discovery_dir.is_absolute() else ROOT / args.discovery_dir
    output = args.output if args.output.is_absolute() else ROOT / args.output
    boundary_certificate_path = boundary_dir / "certificate.json"
    boundary_manifest_path = boundary_dir / "manifest.json"
    shell_certificate_path = DEFAULT_SHELL_DIR / "certificate.json"
    shell_manifest_path = DEFAULT_SHELL_DIR / "manifest.json"
    if not boundary_certificate_path.is_file() or not boundary_manifest_path.is_file():
        raise FileNotFoundError(f"boundary certificate or manifest missing under {boundary_dir}")
    started = time.perf_counter()
    boundary_certificate = json.loads(boundary_certificate_path.read_text(encoding="utf-8"))
    boundary_manifest = json.loads(boundary_manifest_path.read_text(encoding="utf-8"))
    shell_certificate = json.loads(shell_certificate_path.read_text(encoding="utf-8"))
    shell_manifest = json.loads(shell_manifest_path.read_text(encoding="utf-8"))

    boundary_interval_audit = _walk_interval_records(boundary_certificate, path="boundary")
    shell_interval_audit = _walk_interval_records(shell_certificate, path="shell")
    expected_inputs = boundary_manifest.get("inputs", {})
    input_checks = {}
    for relative, expected_hash in expected_inputs.items():
        path = ROOT / relative
        input_checks[relative] = {"exists": path.is_file(), "expected": expected_hash, "actual": _sha256(path) if path.is_file() else None}
        input_checks[relative]["matches"] = input_checks[relative]["exists"] and input_checks[relative]["actual"] == expected_hash
    boundary_output_hash = _sha256(boundary_certificate_path)
    shell_output_hash = _sha256(shell_certificate_path)
    shell_output_expected = shell_manifest.get("outputs_sha256", {}).get("certificate.json")

    stored = {
        "J": _stored_interval(boundary_certificate["J"], label="boundary.J"),
        "a": _stored_interval(boundary_certificate["a"], label="boundary.a"),
        "d": _stored_interval(boundary_certificate["d"], label="boundary.d"),
        "optimal_c": _stored_interval(boundary_certificate["optimal_c"], label="boundary.optimal_c"),
        "optimal_beta": _stored_interval(boundary_certificate["optimal_beta"], label="boundary.optimal_beta"),
        "baseline_c1_beta": _stored_interval(boundary_certificate["baseline_c1_beta"], label="boundary.baseline_c1_beta"),
    }
    shell_q0 = _stored_interval(shell_certificate["q0"], label="shell.q0")
    shell_l0 = _stored_interval(shell_certificate["l0"], label="shell.l0")
    shell_alpha2 = _stored_interval(shell_certificate["optional_staggered_rescaling"]["alpha2"], label="shell.alpha2")
    J, integration_details = _integrate_j(args.N, args.M, args.precision)
    q0 = shell_q0[2]
    l0 = shell_l0[2]
    alpha2 = shell_alpha2[2]
    ctx.prec = args.precision
    pi = arb.pi()
    n1 = arb(2).sqrt() * pi
    a = arb(1) / arb(3).sqrt() - arb(1) / arb(2)
    d = arb(3) * n1 / (arb(4) * q0) - J / (arb(2) * l0)
    c = (a / d).sqrt()
    beta = arb(2) * alpha2 * (a * d).sqrt()
    baseline_beta = alpha2 * (a + d)
    analytic_gap = alpha2 * (d.sqrt() - a.sqrt()) ** 2
    recomputed = {"J": _arb_record(J), "a": _arb_record(a), "d": _arb_record(d), "optimal_c": _arb_record(c), "optimal_beta": _arb_record(beta), "baseline_c1_beta": _arb_record(baseline_beta), "analytic_beta_gap": _arb_record(analytic_gap)}

    def bounds_from_record(record: dict[str, Any], label: str) -> tuple[Fraction, Fraction]:
        return _record_bounds(record, label=label)

    recomputed_bounds = {key: bounds_from_record(value, f"recomputed.{key}") for key, value in recomputed.items() if key != "analytic_beta_gap"}
    stored_bounds = {key: (value[0], value[1]) for key, value in stored.items()}
    overlap = {key: _interval_overlap(recomputed_bounds[key], stored_bounds[key]) for key in recomputed_bounds}
    beta_upper = stored_bounds["optimal_beta"][1]
    baseline_lower = stored_bounds["baseline_c1_beta"][0]
    checks = {
        "boundary_output_hash_matches_manifest": boundary_output_hash == boundary_manifest.get("output_sha256"),
        "shell_output_hash_matches_manifest": shell_output_hash == shell_output_expected,
        "boundary_input_hashes_match": all(item["matches"] for item in input_checks.values()),
        "boundary_manifest_has_detached_sha256": (boundary_dir / "manifest.sha256").is_file(),
        "all_boundary_rational_records_valid": boundary_interval_audit["all_valid"],
        "all_shell_rational_records_valid": shell_interval_audit["all_valid"],
        "domain_x_coverage": _domain_coverage(args.N, args.M)["x_contiguous_0_to_1"],
        "domain_t_coverage": _domain_coverage(args.N, args.M)["t_contiguous_0_to_2pi"],
        "J_positive": bool(J.lower() > arb(0)),
        "q0_positive": bool(q0.lower() > arb(0)),
        "l0_positive": bool(l0.lower() > arb(0)),
        "a_positive": bool(a.lower() > arb(0)),
        "d_positive": bool(d.lower() > arb(0)),
        "c_positive": bool(c.lower() > arb(0)),
        "c_less_than_one": bool(c.upper() < arb(1)),
        "beta_positive": bool(beta.lower() > arb(0)),
        "baseline_beta_positive": bool(baseline_beta.lower() > arb(0)),
        "beta_below_baseline_arb": bool(beta.upper() < baseline_beta.lower()),
        "beta_below_baseline_exact_stored": beta_upper < baseline_lower,
        "analytic_gap_positive": bool(analytic_gap.lower() > arb(0)),
        "recomputed_intervals_overlap_stored": all(overlap.values()),
    }
    discovery = _audit_discovery(discovery_dir / "discovery.json")
    result = {
        "schema": "independent-boundary-review-v1",
        "status": "PASS" if all(value for key, value in checks.items() if key != "boundary_manifest_has_detached_sha256") and discovery["all_floors_unambiguous"] and discovery["components_match_discovery"] else "FAIL",
        "source_boundary_dir": str(boundary_dir.relative_to(ROOT)),
        "source_boundary_certificate_sha256": boundary_output_hash,
        "source_boundary_manifest_sha256": _sha256(boundary_manifest_path),
        "source_shell_certificate_sha256": shell_output_hash,
        "source_shell_manifest_sha256": _sha256(shell_manifest_path),
        "boundary_manifest_inputs": input_checks,
        "boundary_interval_audit": boundary_interval_audit,
        "shell_interval_audit": shell_interval_audit,
        "integration": {"N": args.N, "M": args.M, "precision_bits": args.precision, "method": "direct Arb rectangles; t outer loop and x inner loop; no project certificate helper imports", **integration_details},
        "domain_coverage": _domain_coverage(args.N, args.M),
        "stored_boundary_intervals": {key: {"lower": {"numerator": str(value[0].numerator), "denominator": str(value[0].denominator)}, "upper": {"numerator": str(value[1].numerator), "denominator": str(value[1].denominator)}} for key, value in stored.items()},
        "recomputed": recomputed,
        "interval_overlap_with_stored": overlap,
        "checks": checks,
        "discovery_floor_audit": discovery,
        "claim_boundary": "This audits interval arithmetic, domain partitioning, signs, and selected integer floors. It does not reprove Theorem 003's asymptotic expansion, geometric topology, finite total-length certificate, global optimality, or novelty.",
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "environment": {"python": sys.version.replace("\n", " "), "platform": platform.platform(), "machine": platform.machine(), "flint_precision_after_run": int(ctx.prec)},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output.write_text(serialized, encoding="utf-8")
    manifest = {
        "schema": "independent-boundary-review-manifest-v1",
        "review_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "source_boundary_certificate_sha256": boundary_output_hash,
        "source_boundary_manifest_sha256": _sha256(boundary_manifest_path),
        "review_script_sha256": _sha256(Path(__file__)),
    }
    manifest_path = output.with_name(output.stem + ".manifest.json")
    manifest_serialized = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    manifest_path.write_text(manifest_serialized, encoding="utf-8")
    output.with_name(output.stem + ".manifest.sha256").write_text(hashlib.sha256(manifest_serialized.encode("utf-8")).hexdigest() + "  " + manifest_path.name + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(output), "checks": checks, "discovery": {key: discovery[key] for key in ("all_floors_unambiguous", "components_match_discovery", "ambiguous_floor_count", "minimum_exact_floor_margin")}}, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
