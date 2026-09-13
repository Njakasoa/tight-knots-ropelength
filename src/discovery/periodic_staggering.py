"""Periodic phases and finite nonuniform radii; see STAGGERING_GENERALIZATION.md.

Search uses floats. Certificates reconstruct rational inputs with Arb and check
every shell pair. No numerical optimizer is trusted by the certificate.
"""
from __future__ import annotations

from fractions import Fraction
import math

import numpy as np
from scipy.optimize import brentq

from src.certification.arb_backend import arb, arb_precision, arb_record
from src.certification.shell_family import capacity, certified_floor, shell_length


def phase_distance(a: Fraction, b: Fraction) -> Fraction:
    d = (a - b) % 1
    return min(d, 1 - d)


def grid_phase_distance(n: int, offset: Fraction, m: int,
                        other_offset: Fraction) -> Fraction:
    """Exact minimum distance in turns between two complete uniform grids.

    Offsets are in turns, not fractions of one population's mesh.
    """
    if not isinstance(n, int) or not isinstance(m, int) or min(n, m) < 1:
        raise ValueError("positive integer populations required")
    if not isinstance(offset, Fraction) or not isinstance(other_offset, Fraction):
        raise TypeError("offsets must be exact Fractions")
    multiple = math.lcm(n, m)
    return phase_distance(multiple * offset, multiple * other_offset) / multiple


def flat_gap(f):
    """Sufficient radial gap in the saturated, equal-population row model."""
    f = np.asarray(f, dtype=float)
    d = np.abs((f + 0.5) % 1 - 0.5)
    return 2 * np.sqrt(1 - d * d)


def exact_period_mean(period: int) -> float:
    if not isinstance(period, int) or period < 1:
        raise ValueError("positive integer period required")
    return math.sqrt(3) + (2 - math.sqrt(3)) * (period % 2) / period


def periodic_grid_search(period: int, grid: int = 240) -> dict:
    """Global dynamic program on a finite phase grid, including closing edge.

    Phase 0 is fixed by rotation invariance. No prescribed staggering pattern
    enters the search. The analytic all-real-phase result is a separate proof.
    """
    if period < 1 or grid < 2:
        raise ValueError("invalid period or grid")
    phases = np.arange(grid) / grid
    costs = flat_gap(phases[:, None] - phases[None, :])
    dp = np.full(grid, np.inf)
    dp[0] = 0
    parents = []
    for _ in range(period):
        candidate = dp[:, None] + costs
        parent = np.argmin(candidate, axis=0)
        dp = candidate[parent, np.arange(grid)]
        parents.append(parent)
    node = 0
    path = [node]
    for parent in reversed(parents):
        node = int(parent[node])
        path.append(node)
    path.reverse()
    return {"period": period, "grid": grid, "mean_gap": float(dp[0] / period),
            "phases_including_closure": [f"{k}/{grid}" for k in path],
            "analytic_minimum_diagnostic": exact_period_mean(period),
            "scope": "global on the finite phase grid; period may divide requested period"}


def _ar(q: Fraction):
    return arb(q.numerator) / arb(q.denominator)


def _ceil_fraction(x: float, denominator: int = 10**8) -> Fraction:
    return Fraction(math.ceil(x * denominator), denominator)


def _harmonic(a: float, b: float, R: float) -> float:
    u, v = a * b, (R - a) * (R - b)
    return u * v / (u + v)


def propose_nonuniform(t_shells: int, block_size: int | None = None) -> dict:
    """Greedy compression at the SAME populations, R and phases as baseline.

    A floor of 1.000001 on neighboring gaps ensures two-step radial clearance.
    Block interfaces retain gap >=2. Individual same-shell clearance is checked
    directly, allowing the population-rule slack to be used for compression.
    The output is a proposal until certify_nonuniform succeeds.
    """
    if not isinstance(t_shells, int) or t_shells < 2:
        raise ValueError("at least two shells required")
    b = math.isqrt(t_shells) if block_size is None else block_size
    if not isinstance(b, int) or not 1 <= b <= t_shells:
        raise ValueError("invalid block size")
    with arb_precision(192):
        delta = arb(3).sqrt()
        baseline = [delta * (i + 1) + (2 - delta) * ((i // b) + 1)
                    for i in range(t_shells)]
        # An exact rational major radius, certified outside the baseline tube.
        R = _ceil_fraction(float((2 * baseline[-1] + 2).upper())) + Fraction(1, 10**7)
        if not bool(_ar(R) > 2 * baseline[-1] + 2):
            raise ArithmeticError("major-radius padding insufficient")
        populations = [certified_floor(capacity(baseline[(i // b) * b],
                                                _ar(R) - baseline[(i // b) * b])) - 1
                       for i in range(t_shells)]
    radii = []
    for i, n in enumerate(populations):
        if n < 3:
            raise ValueError("baseline population below three")
        lower = Fraction(2) if i == 0 else radii[-1] + (
            Fraction(2) if i % b == 0 else Fraction(1000001, 1000000))
        def margin(x):
            same = 4 * _harmonic(x, x, float(R)) * math.sin(math.pi / n)**2 - 4
            cross = 10.0 if i == 0 or i % b == 0 else (
                (x - float(radii[-1]))**2
                + 4 * _harmonic(float(radii[-1]), x, float(R))
                * math.sin(math.pi / (2 * n))**2 - 4)
            return min(same, cross)
        if margin(float(lower)) > 1e-9:
            r = lower
        else:
            root = brentq(margin, float(lower), float((R - 2) / 2), xtol=1e-12)
            r = _ceil_fraction(root) + Fraction(1, 10**7)
        radii.append(r)
    return {"T": t_shells, "block_size": b, "R": str(R),
            "radii": [str(r) for r in radii], "populations": populations,
            "offsets_turns": [str(Fraction((i % b) % 2, 2 * n))
                              for i, n in enumerate(populations)],
            "algorithm": "greedy float roots, rational upward padding, independent all-pairs Arb check",
            "status": "PROPOSAL"}


def certify_geometry(proposal: dict, *, precision_bits: int = 192) -> dict:
    """All-pairs certificate for arbitrary rational uniform shell grids.

    No block, period, minimum neighboring gap, or baseline is assumed here.
    """
    R = Fraction(proposal["R"])
    radii = [Fraction(x) for x in proposal["radii"]]
    ns = proposal["populations"]
    offsets = [Fraction(x) for x in proposal["offsets_turns"]]
    T = len(radii)
    def require(condition, reason):
        if not condition:
            raise ValueError(reason)
    require(T > 0 and len(ns) == len(offsets) == T, "dimension mismatch")
    require(all(isinstance(n, int) and not isinstance(n, bool) and n >= 3 for n in ns),
            "invalid populations")
    require(all(r >= 2 for r in radii), "core clearance fails")
    require(all(x < y for x, y in zip(radii, radii[1:])), "radii not increasing")
    require(R >= 2 * max(radii) + 2, "Hopf separation/self-reach hypotheses fail")
    with arb_precision(precision_bits):
        Ar = [_ar(r) for r in radii]
        AR, pi = _ar(R), arb.pi()
        def lower(a, c, rho):
            u, v = a * c, (AR - a) * (AR - c)
            difference = a - c
            sine = (pi * _ar(rho)).sin()
            return difference * difference + 4 * u * v / (u + v) * sine * sine
        same_margins = []
        for i, (r, n) in enumerate(zip(Ar, ns)):
            value = lower(r, r, Fraction(1, n)) - 4
            require(bool(value > 0), f"same-shell clearance not certified: {i}")
            same_margins.append(value)
        radial_pairs, phase_pairs, pair_records = 0, 0, []
        for i in range(T):
            for j in range(i + 1, T):
                if radii[j] - radii[i] >= 2:
                    radial_pairs += 1
                    continue
                rho = grid_phase_distance(ns[i], offsets[i], ns[j], offsets[j])
                margin = lower(Ar[i], Ar[j], rho) - 4
                require(bool(margin > 0), f"cross-shell clearance not certified: {i},{j}")
                phase_pairs += 1
                pair_records.append({"shells": [i + 1, j + 1], "phase_distance_turns": str(rho),
                                     "margin_squared": arb_record(margin, digits=24)})
        return {"status": "PASS", "same_shell_checks": T,
                "radial_pair_checks": radial_pairs, "phase_pair_checks": phase_pairs,
                "expected_shell_pairs": T * (T - 1) // 2,
                "phase_pairs": pair_records,
                "minimum_same_shell_margin_squared": arb_record(
                    min(same_margins, key=lambda x: float(x.lower())), digits=24),
                "scope": "all component clearances; self-reach and full-twist type use Theorem 001"}


def propose_periodic(period: int, *, t_shells: int = 36, block_size: int = 12,
                     pattern: str = "optimized") -> dict:
    """Finite instantiation of the analytic arbitrary-phase gap lemma."""
    if not isinstance(period, int) or period < 1:
        raise ValueError("invalid period")
    if t_shells < 1 or not 1 <= block_size <= t_shells:
        raise ValueError("invalid shell/block count")
    if pattern == "optimized":
        phases = [Fraction(i % 2, 2) for i in range(period)]
    elif pattern == "constant_step":
        step = Fraction(period // 2, period)
        phases = [(i * step) % 1 for i in range(period)]
    elif pattern == "equally_spaced":
        phases = [Fraction(i, period) for i in range(period)]
    else:
        raise ValueError("unknown pattern")
    radii = [Fraction(2)]
    selected = [phases[(i % block_size) % period] for i in range(t_shells)]
    for i in range(1, t_shells):
        gap = Fraction(2) if i % block_size == 0 else (
            _ceil_fraction(float(flat_gap(float(selected[i] - selected[i - 1]))))
            + Fraction(1, 10**7))
        radii.append(radii[-1] + gap)
    R = 2 * radii[-1] + 2
    with arb_precision(192):
        ns = [certified_floor(capacity(_ar(radii[(i // block_size) * block_size]),
                                      _ar(R - radii[(i // block_size) * block_size]))) - 1
              for i in range(t_shells)]
    return {"T": t_shells, "block_size": block_size, "requested_period": period,
            "pattern": pattern, "phase_fractions": [str(x) for x in phases],
            "R": str(R), "radii": [str(x) for x in radii], "populations": ns,
            "offsets_turns": [str(f / n) for f, n in zip(selected, ns)],
            "status": "PROPOSAL"}


def certify_nonuniform(proposal: dict, *, angular_cells: int = 512,
                       precision_bits: int = 192) -> dict:
    """Fail closed; validate full finite family and a SAME-M length comparison.

    Uses harmonic lower bounds, never sampled distances. Exact phase-grid
    differences cover every component pair, including different populations.
    Self-reach and Hopf doubling are the analytic lemmas of Theorem 001.
    """
    def require(condition, reason):
        if not condition:
            raise ValueError(reason)
    T, b = proposal["T"], proposal["block_size"]
    require(isinstance(T, int) and T >= 2 and isinstance(b, int) and 1 <= b <= T,
            "invalid dimensions")
    require(isinstance(angular_cells, int) and angular_cells > 0, "invalid quadrature size")
    R = Fraction(proposal["R"])
    radii = [Fraction(x) for x in proposal["radii"]]
    ns = proposal["populations"]
    offsets = [Fraction(x) for x in proposal["offsets_turns"]]
    require(len(radii) == len(ns) == len(offsets) == T, "dimension mismatch")
    require(all(isinstance(n, int) and not isinstance(n, bool) and n >= 3 for n in ns),
            "invalid populations")
    require(all(r >= 2 for r in radii), "core clearance fails")
    require(all(x < y for x, y in zip(radii, radii[1:])), "radii not increasing")
    require(R >= 2 * max(radii) + 2, "Hopf separation/self-reach hypotheses fail")
    geometry = certify_geometry(proposal, precision_bits=precision_bits)
    with arb_precision(precision_bits):
        Ar = [_ar(r) for r in radii]
        AR, pi = _ar(R), arb.pi()
        delta = arb(3).sqrt()
        baseline = [delta * (i + 1) + (2 - delta) * ((i // b) + 1) for i in range(T)]
        require(bool(AR > 2 * baseline[-1] + 2), "baseline closure not certified")
        expected_ns = [certified_floor(capacity(baseline[(i // b) * b],
                                                AR - baseline[(i // b) * b])) - 1
                       for i in range(T)]
        require(ns == expected_ns, "populations differ from comparison baseline")
        require(all(offsets[i] % 1 == Fraction((i % b) % 2, 2 * ns[i]) for i in range(T)),
                "offsets differ from comparison baseline")
        require(radii[0] == 2, "comparison expects first shell unchanged")
        require(all(bool(baseline[i] > Ar[i]) for i in range(1, T)),
                "not all remaining shells strictly compressed")
        base_length, new_length = 2 * pi * AR, 2 * pi * AR
        for n, old, new in zip(ns, baseline, Ar):
            base_length += n * shell_length(AR, old, angular_cells=angular_cells,
                                            precision_bits=precision_bits)
            new_length += n * shell_length(AR, new, angular_cells=angular_cells,
                                           precision_bits=precision_bits)
        base_length *= 2
        new_length *= 2
        improvement = base_length - new_length
        require(bool(improvement > 0), "length improvement intervals overlap")
        M = 2 * (1 + sum(ns))
        denominator = (arb(M * (M - 1)).sqrt()).sqrt()**3
        gain = 100 * improvement / base_length
        return {**geometry, "status": "PASS", "T": T, "block_size": b, "M": M,
                "precision_bits": precision_bits, "angular_cells": angular_cells,
                "baseline_length": arb_record(base_length, digits=30),
                "nonuniform_length": arb_record(new_length, digits=30),
                "length_reduction": arb_record(improvement, digits=30),
                "reduction_percent": arb_record(gain, digits=24),
                "baseline_normalized_length": arb_record(base_length / denominator, digits=24),
                "nonuniform_normalized_length": arb_record(new_length / denominator, digits=24),
                "minimum_gap_diagnostic": float(min(y - x for x, y in zip(radii, radii[1:]))),
                "maximum_gap_diagnostic": float(max(y - x for x, y in zip(radii, radii[1:]))),
                "scope": "unit-thickness T(M,M) construction, conditional on Theorem 001 analytic lemmas; same M,R,phases,populations as baseline; no optimality claim"}
