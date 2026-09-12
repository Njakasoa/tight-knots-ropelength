"""Independent audit harness for the explicit endpoint topology certificates.

This file intentionally reconstructs the analytic coordinates and witness
coverage from the serialized inputs.  It imports the certificate module only
to exercise its CLI and to probe its cache/parser boundary; no production
geometry derivative or topology helper is used to form the analytic
reference.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "certify_refinement_topology.py"
SOURCE = ROOT / "results" / "variable_pitch_20260912T224501767133Z"
CERTS = ROOT / "results" / "topology_path_20260912T231158562188Z"
SEEDS = (1729, 2718, 3141)
EPS = Fraction(1, 10**10)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / arb(value.denominator)


def dyadic(value: float) -> bool:
    if not math.isfinite(float(value)):
        return False
    denominator = Fraction.from_float(float(value)).denominator
    return denominator > 0 and denominator & (denominator - 1) == 0


def exact_vect(path: Path) -> tuple[list[list[Fraction]], np.ndarray, list[int], dict[str, Any]]:
    """Parse VECT independently, rejecting any token after coordinates."""

    tokens: list[str] = []
    for line in path.read_text().splitlines():
        tokens.extend(line.split("#", 1)[0].split())
    if len(tokens) < 4 or tokens[0] != "VECT":
        raise ValueError("bad VECT header")
    m, v, colors = (int(item) for item in tokens[1:4])
    if m <= 0 or v <= 0 or colors < 0:
        raise ValueError("invalid VECT sizes")
    cursor = 4
    if len(tokens) < cursor + 2 * m + 3 * v:
        raise ValueError("truncated VECT")
    counts = [int(item) for item in tokens[cursor : cursor + m]]
    cursor += m
    if any(item >= 0 for item in counts) or sum(-item for item in counts) != v:
        raise ValueError("open or inconsistent VECT components")
    color_counts = [int(item) for item in tokens[cursor : cursor + m]]
    cursor += m
    if any(item < 0 for item in color_counts) or sum(color_counts) != colors:
        raise ValueError("inconsistent VECT colour counts")
    raw = tokens[cursor : cursor + 3 * v]
    cursor += 3 * v
    # The canonical writer places RGB(A) values after all coordinates.  They
    # are metadata for this topology audit, but their declared extent still
    # belongs to the VECT grammar and must be consumed before the strict
    # trailing-token check.
    color_channels = 0
    color_raw: list[str] = []
    if colors:
        remaining = len(tokens) - cursor
        color_channels = 4 if remaining >= 4 * colors else 3 if remaining >= 3 * colors else 0
        if color_channels == 0:
            raise ValueError("truncated VECT colors")
        color_raw = tokens[cursor : cursor + color_channels * colors]
        cursor += color_channels * colors
    if cursor != len(tokens):
        raise ValueError("trailing VECT tokens")
    # Parse colour strings too, so malformed values cannot hide behind the
    # fact that coordinates are the only data used by the certificate.
    if color_raw:
        [Fraction(item) for item in color_raw]
    coords = [[Fraction(raw[3 * i + j]) for j in range(3)] for i in range(v)]
    floats = np.asarray([[float(value) for value in row] for row in coords], dtype=float)
    return coords, floats, [-item for item in counts], {
        "vertices": v,
        "components": m,
        "colors": colors,
        "color_channels": color_channels,
        "tokens": len(tokens),
        "coordinate_tokens_exact": True,
    }


def import_certificate_module():
    spec = importlib.util.spec_from_file_location("refinement_certificate_under_audit", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import certificate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analytic_audit(seed: int, module: Any) -> dict[str, Any]:
    run = next(item for item in json.loads((SOURCE / "search.json").read_text())["records"] if item["seed"] == seed)
    initial = SOURCE / run["initial"]
    coords, floats, counts, parse_meta = exact_vect(initial)
    parameters = run["parameters"]
    R, inner, beta0, beta1, offset, zs = (arb_fraction(Fraction.from_float(float(x))) for x in parameters)
    pi = arb.pi()
    du = 2 * pi / 48
    eps = arb_fraction(EPS)
    specs: list[tuple[arb, arb, arb, int]] = [(arb(0), arb(0), arb(0), 0)]
    for radius, beta, phase_offset, population in (
        (inner, beta0, arb(0), 2),
        (arb(2), beta1, arb_fraction(Fraction.from_float(float(offset))), 3),
    ):
        for strand in range(population):
            specs.append((radius, beta, 2 * pi * strand / population + phase_offset, population))

    max_error = arb(0)
    max_error_index: list[int] | None = None
    max_transverse = arb(0)
    min_h_eta = None
    min_sep_margin = None
    angle_lower_margin = None
    angle_upper_margin = None
    for component in range(12):
        radius, beta, phase, _population = specs[component % 6]
        L = arb(1) + abs(beta)
        h = R - radius
        B = R + radius + 2 * radius * L + radius * (L * L + abs(beta))
        eta = B * du * du / 8 + eps
        transverse = eta + radius * L * eta / (h - eta)
        max_transverse = max(max_transverse, transverse.upper())
        min_h_eta = h - eta if min_h_eta is None else min(min_h_eta, h - eta)
        drift = eps / (h - eps)
        angle_lower_margin = du - 2 * drift if angle_lower_margin is None else min(angle_lower_margin, du - 2 * drift)
        angle_upper_margin = math.pi - float(du + 2 * drift) if angle_upper_margin is None else min(angle_upper_margin, math.pi - float(du + 2 * drift))
        for k in range(48):
            raw = [arb_fraction(coords[component * 48 + k][j]) for j in range(3)]
            raw[2] = raw[2] / zs
            if component >= 6:
                raw = [raw[0] - R, raw[2], -raw[1]]
            u = du * k
            theta = u + beta * u.sin() - phase
            expected = [
                (R + radius * theta.cos()) * u.cos(),
                (R + radius * theta.cos()) * u.sin(),
                radius * theta.sin(),
            ]
            error = sum((left - right) * (left - right) for left, right in zip(raw, expected))
            if error.upper() > max_error:
                max_error = error.upper()
                max_error_index = [component, k]
            if not bool(error < eps * eps):
                raise AssertionError(f"independent analytic sample mismatch seed={seed} component={component} k={k}")

    separations = [inner, arb(2), arb(2) - inner, 2 * inner * (pi / 2).sin(), 4 * (pi / 3).sin()]
    min_sep_margin = min(separation - 2 * max_transverse for separation in separations)
    tube_gap = R - 2 * (arb(2) + max_transverse)
    if not bool(R > 4 and inner > 0 and inner < 2 and zs > 0 and min_h_eta > 0):
        raise AssertionError(f"sampling hypotheses failed seed={seed}")
    if not bool(min_sep_margin > 0 and tube_gap > 0):
        raise AssertionError(f"sampling separation failed seed={seed}")

    # Recompute the binary64 alignment from exact-decimal coordinates.  This
    # is independent of the certificate's stored alignment values.
    final_path = SOURCE / run["final"]
    _final_coords, final_float, final_counts, final_meta = exact_vect(final_path)
    if counts != final_counts:
        raise AssertionError("endpoint component counts differ")
    centered_initial = floats - floats.mean(axis=0)
    centered_final = final_float - final_float.mean(axis=0)
    scale = float((centered_initial * centered_final).sum() / (centered_initial * centered_initial).sum())
    translation = (final_float.mean(axis=0) - scale * floats.mean(axis=0)).tolist()
    cert = json.loads((CERTS / f"seed{seed}.json").read_text())
    alignment = cert["alignment"]
    alignment_bits_match = (
        float(scale).hex() == float(alignment["scale"]).hex()
        and all(float(a).hex() == float(b).hex() for a, b in zip(translation, alignment["translation"]))
    )
    return {
        "seed": seed,
        "initial_sha256": sha(initial),
        "final_sha256": sha(final_path),
        "counts": counts,
        "analytic_reference": "independent direct E(u,w) formula with exact Fraction VECT tokens and 192-bit Arb",
        "maximum_squared_vertex_error_upper_arb": str(max_error),
        "maximum_squared_vertex_error_upper_float": float(max_error),
        "maximum_error_component_k": max_error_index,
        "maximum_transverse_error_upper_arb": str(max_transverse),
        "minimum_h_minus_eta_lower_arb": str(min_h_eta),
        "minimum_separation_minus_2_emax_lower_arb": str(min_sep_margin),
        "double_tube_gap_lower_arb": str(tube_gap),
        "angle_lower_margin_float": float(angle_lower_margin),
        "angle_upper_margin_float": float(angle_upper_margin),
        "alignment_recomputed_binary64_bits_match": alignment_bits_match,
        "alignment_scale_positive": float(alignment["scale"]) > 0.0,
        "alignment_coefficients_dyadic": all(
            dyadic(value) for value in [alignment["scale"], *alignment["translation"]]
        ),
        "initial_parse": parse_meta,
        "final_parse": final_meta,
    }


def required_pairs(counts: list[int]) -> set[tuple[int, int]]:
    nxt: list[int] = []
    component: list[int] = []
    base = 0
    for ci, size in enumerate(counts):
        nxt.extend(base + (i + 1) % size for i in range(size))
        component.extend([ci] * size)
        base += size
    return {
        (i, j)
        for i in range(len(nxt))
        for j in range(i + 1, len(nxt))
        if not (component[i] == component[j] and (nxt[i] == j or nxt[j] == i))
    }


def independent_witness_audit(seed: int) -> dict[str, Any]:
    cert = json.loads((CERTS / f"seed{seed}.json").read_text())
    run = next(item for item in json.loads((SOURCE / "search.json").read_text())["records"] if item["seed"] == seed)
    _coords, _floats, counts, _meta = exact_vect(SOURCE / run["initial"])
    witness = CERTS / f"seed{seed}.npz"
    with np.load(witness, allow_pickle=False) as arrays:
        pairs = np.asarray(arrays["pairs"])
        corners = np.asarray(arrays["corners"])
    required = required_pairs(counts)
    keys = {(int(row[0]), int(row[1])) for row in pairs}
    corner_keys = {int(row[0]) for row in corners}
    integer_columns = all(
        all(float(value).is_integer() for value in row[:4]) for row in pairs
    ) and all(all(float(value).is_integer() for value in row[:3]) for row in corners)
    depth_bounds = (
        all(0 <= int(row[3]) <= 14 and 0 <= int(row[2]) < 2 ** int(row[3]) for row in pairs)
        and all(0 <= int(row[2]) <= 14 and 0 <= int(row[1]) < 2 ** int(row[2]) for row in corners)
    )
    time_coverage = True
    pair_cells_by_key: dict[tuple[int, int], list[tuple[Fraction, Fraction]]] = {}
    for row in pairs:
        key = (int(row[0]), int(row[1]))
        depth = int(row[3])
        num = int(row[2])
        pair_cells_by_key.setdefault(key, []).append((Fraction(num, 2**depth), Fraction(num + 1, 2**depth)))
    for cells in pair_cells_by_key.values():
        previous = Fraction(0)
        for lower, upper in sorted(cells):
            time_coverage &= lower == previous
            previous = upper
        time_coverage &= previous == 1
    corner_cells_by_key: dict[int, list[tuple[Fraction, Fraction]]] = {}
    for row in corners:
        key = int(row[0])
        depth = int(row[2])
        num = int(row[1])
        corner_cells_by_key.setdefault(key, []).append((Fraction(num, 2**depth), Fraction(num + 1, 2**depth)))
    for cells in corner_cells_by_key.values():
        previous = Fraction(0)
        for lower, upper in sorted(cells):
            time_coverage &= lower == previous
            previous = upper
        time_coverage &= previous == 1
    axes_finite = bool(np.all(np.isfinite(pairs[:, 4:7])) and np.all(np.isfinite(corners[:, 3:6])))
    axes_dyadic = bool(
        all(dyadic(value) for value in pairs[:, 4:7].ravel())
        and all(dyadic(value) for value in corners[:, 3:6].ravel())
    )
    return {
        "seed": seed,
        "witness_sha256": sha(witness),
        "certificate_witness_sha256_matches": sha(witness) == cert["witness_sha256"],
        "pairs_shape": list(pairs.shape),
        "corners_shape": list(corners.shape),
        "required_pairs": len(required),
        "pair_keys": len(keys),
        "pair_keys_exact": keys == required,
        "corner_keys": len(corner_keys),
        "corner_keys_exact": corner_keys == set(range(sum(counts))),
        "integer_index_columns": integer_columns,
        "time_depth_bounds": depth_bounds,
        "gap_free_exact_dyadic_coverage": time_coverage,
        "axes_finite": axes_finite,
        "axes_exact_binary64_dyadic": axes_dyadic,
        "maximum_pair_depth": int(pairs[:, 3].max()),
        "maximum_corner_depth": int(corners[:, 2].max()),
    }


def update_witness_hash(directory: Path, seed: int, pairs: np.ndarray | None = None, corners: np.ndarray | None = None) -> None:
    witness = directory / f"seed{seed}.npz"
    with np.load(witness, allow_pickle=False) as arrays:
        old_pairs = np.asarray(arrays["pairs"])
        old_corners = np.asarray(arrays["corners"])
    np.savez_compressed(witness, pairs=old_pairs if pairs is None else pairs, corners=old_corners if corners is None else corners)
    cert_path = directory / f"seed{seed}.json"
    cert = json.loads(cert_path.read_text())
    cert["witness_sha256"] = sha(witness)
    cert_path.write_text(json.dumps(cert, indent=2) + "\n")


def run_verify(directory: Path, seed: int | None, optimized: bool = False) -> dict[str, Any]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command += [str(SCRIPT), str(SOURCE)]
    if seed is not None:
        command += ["--seeds", str(seed)]
    command += ["--verify", str(directory)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {
        "returncode": result.returncode,
        "accepted": result.returncode == 0,
        "stdout": result.stdout[-1000:],
        "stderr": result.stderr[-1600:],
        "command": command,
    }


def tamper_audit(module: Any) -> dict[str, Any]:
    seed = 1729
    base = CERTS
    with tempfile.TemporaryDirectory(prefix="refinement-topology-review-") as temporary:
        temp_root = Path(temporary)
        cases: dict[str, dict[str, Any]] = {}

        missing_witness = temp_root / "missing-witness"
        missing_witness.mkdir()
        for suffix in ("json",):
            shutil.copy2(base / f"seed{seed}.{suffix}", missing_witness / f"seed{seed}.{suffix}")
        cases["missing_npz"] = run_verify(missing_witness, seed)

        with np.load(base / f"seed{seed}.npz", allow_pickle=False) as arrays:
            original_pairs = np.asarray(arrays["pairs"])
            original_corners = np.asarray(arrays["corners"])

        def make_case(name: str, pairs: np.ndarray, corners: np.ndarray = original_corners) -> Path:
            directory = temp_root / name
            directory.mkdir()
            shutil.copy2(base / f"seed{seed}.json", directory / f"seed{seed}.json")
            shutil.copy2(base / f"seed{seed}.npz", directory / f"seed{seed}.npz")
            update_witness_hash(directory, seed, pairs=pairs, corners=corners)
            return directory

        cases["missing_pair_row"] = run_verify(make_case("missing-pair", original_pairs[1:]), seed)
        zero_axis = original_pairs.copy()
        zero_axis[0, 4:7] = 0.0
        cases["zero_separating_axis"] = run_verify(make_case("zero-axis", zero_axis), seed)
        cases["missing_corner_row"] = run_verify(make_case("missing-corner", original_pairs, original_corners[1:]), seed)
        bad_endpoint = original_pairs.copy()
        bad_endpoint[0, 2] = 1.0
        cases["endpoint_num_out_of_range"] = run_verify(make_case("bad-endpoint", bad_endpoint), seed)
        noninteger = original_pairs.copy()
        noninteger[0, 0] = 0.5
        cases["noninteger_edge_index"] = run_verify(make_case("noninteger-index", noninteger), seed)
        optimized_missing_pair = make_case("optimized-missing-pair", original_pairs[1:])
        cases["missing_pair_under_python_O"] = run_verify(optimized_missing_pair, seed, optimized=True)

        # Exercise the module parser with a syntactically valid canonical file
        # plus one trailing token.  Canonical inputs are checked independently
        # above; this is a hardening probe for the implementation boundary.
        trailing_source = temp_root / "trailing.vect"
        trailing_source.write_text((SOURCE / "seed1729.vect").read_text() + "\n0\n")
        try:
            module.parse_vect(trailing_source)
        except Exception as exc:  # noqa: BLE001 - evidence records exact failure class
            trailing = {"accepted": False, "exception": type(exc).__name__, "message": str(exc)}
        else:
            trailing = {"accepted": True, "exception": None, "message": ""}

        missing_source = temp_root / "missing-coordinate.vect"
        missing_source.write_text("VECT 1 1 0\n-1\n0\n0\n0\n")
        try:
            module.parse_vect(missing_source)
        except Exception as exc:  # noqa: BLE001
            missing_coordinate = {"accepted": False, "exception": type(exc).__name__}
        else:
            missing_coordinate = {"accepted": True, "exception": None}

    return {
        "normal_rejection_cases": cases,
        "trailing_token_parser_probe": trailing,
        "truncated_coordinate_parser_probe": missing_coordinate,
        "normal_rejection_all_failed": all(not item["accepted"] for item in cases.values() if item is not cases["missing_pair_under_python_O"]),
        "python_O_missing_pair_bypass_observed": cases["missing_pair_under_python_O"]["accepted"],
    }


def cache_audit(module: Any) -> dict[str, Any]:
    seed = 1729
    run = next(item for item in json.loads((SOURCE / "search.json").read_text())["records"] if item["seed"] == seed)
    initial, _floats, counts, _meta = exact_vect(SOURCE / run["initial"])
    final, _final_floats, _final_counts, _final_meta = exact_vect(SOURCE / run["final"])
    initial_arb = [[arb_fraction(value) for value in row] for row in initial]
    final_arb = [[arb_fraction(value) for value in row] for row in final]
    cert = json.loads((CERTS / f"seed{seed}.json").read_text())
    check = module.PathCheck(initial_arb, final_arb, counts, cert["alignment"])
    before = len(check.cache)
    half_a = check.positions(1, 1)
    after_half_a = len(check.cache)
    half_b = check.positions(2, 2)
    after_half_b = len(check.cache)
    endpoint = check.positions(2, 1)
    after_endpoint = len(check.cache)
    return {
        "initial_cache_size": before,
        "half_time_adds_one_entry": after_half_a == before + 1,
        "equivalent_half_times_share_object": half_a is half_b,
        "equivalent_half_time_does_not_add_entry": after_half_b == after_half_a,
        "endpoint_time_reuses_canonical_entry": endpoint is check.cache[(1, 1)],
        "endpoint_does_not_add_entry": after_endpoint == after_half_b,
        "cache_keys": sorted([list(key) for key in check.cache]),
    }


def main() -> None:
    ctx.prec = 192
    module = import_certificate_module()
    result: dict[str, Any] = {
        "review": "independent refinement-topology implementation audit",
        "date": "2026-09-13",
        "python": sys.version,
        "precision_bits": ctx.prec,
        "script_sha256": sha(SCRIPT),
        "search_sha256": sha(SOURCE / "search.json"),
        "canonical_summary_sha256": sha(CERTS / "summary.json"),
        "canonical_summary": json.loads((CERTS / "summary.json").read_text()),
        "reviewer_harness_sha256": sha(Path(__file__)),
        "canonical_cli_replay_all_seeds": run_verify(CERTS, None),
        "analytic_audits": [analytic_audit(seed, module) for seed in SEEDS],
        "witness_audits": [independent_witness_audit(seed) for seed in SEEDS],
        "cache_audit": cache_audit(module),
        "tamper_audit": tamper_audit(module),
        "zero_colour_atlas": None,
    }
    atlas = ROOT / "data" / "reference" / "cantarella-atlas" / "knots" / "prime" / "3-10" / "3_1.vect"
    atlas_coords, _atlas_float, atlas_counts, atlas_meta = exact_vect(atlas)
    source_points, _source_float, source_counts = module.parse_vect(atlas)
    source_matches_exact = all(
        0 in (source_points[i][j] - arb_fraction(atlas_coords[i][j]))
        for i in range(len(atlas_coords))
        for j in range(3)
    )
    result["zero_colour_atlas"] = {
        "path": str(atlas.relative_to(ROOT)),
        "sha256": sha(atlas),
        "header_components": atlas_meta["components"],
        "header_vertices": atlas_meta["vertices"],
        "header_colors": atlas_meta["colors"],
        "counts": atlas_counts,
        "source_parser_counts": source_counts,
        "source_parser_matches_independent_exact_tokens": source_matches_exact,
    }
    output = ROOT / "results" / "reviewer_refinement_20260913.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(output)
    print(json.dumps({
        "canonical_replay_returncode": result["canonical_cli_replay_all_seeds"]["returncode"],
        "python_O_missing_pair_bypass": result["tamper_audit"]["python_O_missing_pair_bypass_observed"],
        "trailing_parser_accepted": result["tamper_audit"]["trailing_token_parser_probe"]["accepted"],
        "seeds": [item["seed"] for item in result["analytic_audits"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
