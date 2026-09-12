"""Finite shell-specific and common-hole toroidal bundle constructions.

The analytic theorem gives two conservative integer rules.  For
``R = 4*T + 2`` and ``r_i = 2*i`` the shell-specific rule uses
``h_i = R-r_i``; the earlier common-hole comparison uses
``h_common = R-2*T`` for every shell.  In both cases the capacity is evaluated
with Arb and the population is accepted only after Arb certifies
``floor(A) <= A < floor(A)+1``.

The geometry writer below is deliberately a sampled export for inspection and
for the existing polygon tools.  Its metadata always says that sampled
coordinates are diagnostic; the clearance and topology claims come from the
analytic construction in the proof note.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from .arb_backend import arb, arb_precision, arb_record, exact_integer, positive


@dataclass(frozen=True)
class ShellPopulation:
    shell: int
    radius: int
    hole_radius: int
    capacity: arb
    capacity_floor: int
    population: int
    rule: str


@dataclass(frozen=True)
class StaggeredShellPopulation:
    shell: int
    block_start: int
    radius: arb
    hole_radius: arb
    capacity_radius: arb
    capacity_hole_radius: arb
    capacity: arb
    capacity_floor: int
    population: int
    phase_offset: arb
    rule: str


def _as_arb(value: int | arb) -> arb:
    if isinstance(value, arb):
        return value
    if isinstance(value, int):
        return exact_integer(value)
    raise TypeError(f"expected an int or Arb value, got {type(value).__name__}")


def capacity(radius: int | arb, hole_radius: int | arb, *, pi: arb | None = None) -> arb:
    """Evaluate ``A = pi*r*h/sqrt(r^2+h^2)`` with Arb arithmetic."""

    pi = arb.pi() if pi is None else pi
    r = _as_arb(radius)
    h = _as_arb(hole_radius)
    if not bool(r.lower() > arb(0)) or not bool(h.lower() > arb(0)):
        raise ValueError("shell radius and hole radius must be positive")
    return pi * r * h / (r * r + h * h).sqrt()


def certified_floor(value: arb, *, label: str = "capacity") -> int:
    """Return ``floor(value)`` only when Arb certifies its integer interval.

    Arb's lower and upper endpoint operations are directed.  If their floors
    differ, the current precision does not establish the integer and the
    caller must rerun with more bits instead of silently rounding a float.
    """

    lower_floor = value.lower().floor().unique_fmpz()
    upper_floor = value.upper().floor().unique_fmpz()
    if lower_floor is None or upper_floor is None or int(lower_floor) != int(upper_floor):
        raise ArithmeticError(
            f"{label} straddles an integer at Arb precision; rerun with more precision: {value!s}"
        )
    result = int(lower_floor)
    # These comparisons are a second, explicit check of the floor assertion.
    if not bool(value.lower() >= arb(result)) or not bool(value.upper() < arb(result + 1)):
        raise ArithmeticError(f"{label} floor certificate failed at current precision: {value!s}")
    return result


def _population(
    shell: int,
    radius: int,
    hole_radius: int,
    *,
    pi: arb,
    precision_bits: int,
    rule: str,
) -> ShellPopulation:
    a = capacity(radius, hole_radius, pi=pi)
    floor_a = certified_floor(a, label=f"shell {shell} capacity")
    population = floor_a - 1
    if population < 3:
        raise ValueError(
            f"population rule requires N>=3, but shell {shell} gives N={population}"
        )
    return ShellPopulation(shell, radius, hole_radius, a, floor_a, population, rule)


def populations_for_t(
    t_shells: int,
    *,
    mode: str = "shell_specific",
    precision_bits: int = 192,
) -> list[ShellPopulation]:
    """Generate certified populations for one finite shell bundle."""

    if not isinstance(t_shells, int) or t_shells <= 0:
        raise ValueError("t_shells must be a positive integer")
    if mode not in {"shell_specific", "common_hole"}:
        raise ValueError("mode must be 'shell_specific' or 'common_hole'")
    with arb_precision(precision_bits):
        pi = arb.pi()
        R = 4 * t_shells + 2
        h_common = R - 2 * t_shells
        records: list[ShellPopulation] = []
        for i in range(1, t_shells + 1):
            radius = 2 * i
            h = R - radius if mode == "shell_specific" else h_common
            rule = "N=floor(A_i)-1, A_i=pi*r_i*h_i/sqrt(r_i^2+h_i^2)"
            if mode == "common_hole":
                rule = "N=floor(A_i)-1, A_i=pi*r_i*h_common/sqrt(r_i^2+h_common^2)"
            records.append(
                _population(
                    i,
                    radius,
                    h,
                    pi=pi,
                    precision_bits=precision_bits,
                    rule=rule,
                )
            )
        return records


def staggered_populations_for_t(
    t_shells: int,
    *,
    precision_bits: int = 192,
) -> tuple[arb, list[StaggeredShellPopulation]]:
    """Generate Theorem 002's certified equal-population block data.

    The square-root quantities are Arb values.  Only the block size
    ``floor(sqrt(T))`` is an integer combinatorial index and is computed with
    :func:`math.isqrt`, which is exact for the integer ``T``.
    """

    if not isinstance(t_shells, int) or t_shells <= 0:
        raise ValueError("t_shells must be a positive integer")
    block_size = math.isqrt(t_shells)
    if block_size <= 0:  # defensive; positive T already implies this
        raise ValueError("block size must be positive")
    with arb_precision(precision_bits):
        pi = arb.pi()
        delta = arb(3).sqrt()
        two = arb(2)

        def radius(index: int) -> arb:
            block_start = 1 + block_size * ((index - 1) // block_size)
            block_number = 1 + (index - 1) // block_size
            return delta * arb(index) + (two - delta) * arb(block_number)

        outer_radius = radius(t_shells)
        R = two * outer_radius + two
        records: list[StaggeredShellPopulation] = []
        for i in range(1, t_shells + 1):
            block_start = 1 + block_size * ((i - 1) // block_size)
            r_i = radius(i)
            r_first = radius(block_start)
            h_i = R - r_i
            h_first = R - r_first
            a = capacity(r_first, h_first, pi=pi)
            floor_a = certified_floor(a, label=f"staggered block {block_start} capacity")
            population = floor_a - 1
            if population < 3:
                raise ValueError(
                    f"staggered population rule requires N>=3, but block {block_start} gives N={population}"
                )
            parity = (i - block_start) % 2
            offset = arb(0) if parity == 0 else pi / arb(population)
            records.append(
                StaggeredShellPopulation(
                    shell=i,
                    block_start=block_start,
                    radius=r_i,
                    hole_radius=h_i,
                    capacity_radius=r_first,
                    capacity_hole_radius=h_first,
                    capacity=a,
                    capacity_floor=floor_a,
                    population=population,
                    phase_offset=offset,
                    rule=(
                        "N=floor(A(r_block_start,R-r_block_start))-1; "
                        "phase offset alternates 0,pi/N within block"
                    ),
                )
            )
        return R, records


def shell_speed_squared(major_radius: int | arb, minor_radius: int | arb, t: arb) -> arb:
    """Squared speed of one p=1 toroidal helix at parameter ``t``."""

    R = _as_arb(major_radius)
    r = _as_arb(minor_radius)
    c = t.cos()
    return (R + r * c) * (R + r * c) + r * r


def shell_length(
    major_radius: int | arb,
    minor_radius: int | arb,
    *,
    angular_cells: int = 512,
    precision_bits: int = 192,
) -> arb:
    """Certify one shell component length by midpoint quadrature.

    For ``g=(R+r*cos(t))^2+r^2``, the displayed bound

    ``B = r*(R+r)/(R-r) + r^2*(R+r)^2/(R-r)^3``

    bounds ``|d^2 sqrt(g)/dt^2|``.  The returned Arb interval is the midpoint
    sum enlarged by the corresponding composite-midpoint error.  This is a
    finite-size length estimate; the geometric thickness and isotopy facts
    remain analytic proof obligations supplied by the construction note.
    """

    if angular_cells <= 0:
        raise ValueError("angular_cells must be positive")
    with arb_precision(precision_bits):
        pi = arb.pi()
        R = _as_arb(major_radius)
        r = _as_arb(minor_radius)
        if not bool(r.lower() > arb(0)) or not bool(R.lower() > r.upper()):
            raise ValueError("need major_radius > minor_radius > 0")
        h = R - r
        nodes = [pi * (arb(2 * j + 1) / arb(angular_cells)) for j in range(angular_cells)]
        total = arb(0)
        for t in nodes:
            total += shell_speed_squared(major_radius, minor_radius, t).sqrt()
        ht = arb(2) * pi / arb(angular_cells)
        midpoint = total * ht

        # This is an Arb expression.  The denominator h is a lower bound for
        # sqrt(g), so using h here is conservative.
        b_second = r * (R + r) / h + r * r * (R + r) * (R + r) / (h * h * h)
        error = (arb(2) * pi) / arb(24) * b_second * ht * ht
        positive(error, label="finite shell length error")
        return midpoint + arb(0, error.upper())


def core_length(major_radius: int | arb, *, precision_bits: int = 192) -> arb:
    """Arb enclosure of the round core length ``2*pi*R``."""

    with arb_precision(precision_bits):
        return arb(2) * arb.pi() * _as_arb(major_radius)


def _length_sum(
    t_shells: int,
    populations: Sequence[ShellPopulation],
    *,
    major_radius: int | arb | None = None,
    angular_cells: int,
    precision_bits: int,
) -> arb:
    with arb_precision(precision_bits):
        R: int | arb = 4 * t_shells + 2 if major_radius is None else major_radius
        total = core_length(R, precision_bits=precision_bits)
        for item in populations:
            total += arb(item.population) * shell_length(
                R,
                item.radius,
                angular_cells=angular_cells,
                precision_bits=precision_bits,
            )
        return total


def _ratio(length: arb, component_count: int, *, precision_bits: int) -> arb:
    with arb_precision(precision_bits):
        m = exact_integer(component_count)
        denominator = m * m.sqrt()
        positive(denominator, label="component_count^(3/2)")
        return length / denominator


def _population_record(item: ShellPopulation, *, digits: int) -> dict[str, Any]:
    return {
        "shell": item.shell,
        "radius": item.radius,
        "hole_radius": item.hole_radius,
        "capacity": arb_record(item.capacity, digits=digits, label=f"A_{item.shell}"),
        "capacity_floor": item.capacity_floor,
        "population": item.population,
        "rule": item.rule,
        "floor_certificate": {
            "statement": f"{item.capacity_floor} <= A_{item.shell} < {item.capacity_floor + 1}",
            "downward_rounding": "certified by Arb lower/upper endpoint floors",
        },
    }


def _phase_list(populations: Sequence[ShellPopulation]) -> list[dict[str, Any]]:
    phases: list[dict[str, Any]] = []
    for item in populations:
        phases.append(
            {
                "shell": item.shell,
                "population": item.population,
                "phase_formula": "2*pi*j/N_i",
                "phase_indices": [0, item.population - 1],
                "phase_endpoint_note": "indices describe the deterministic equal-spacing rule; no sampled phase is a certificate",
            }
        )
    return phases


def finite_family_record(
    t_shells: int,
    *,
    angular_cells: int = 512,
    precision_bits: int = 192,
    output_digits: int = 60,
) -> dict[str, Any]:
    """Generate one finite shell-family comparison record."""

    if not isinstance(t_shells, int) or t_shells <= 0:
        raise ValueError("t_shells must be a positive integer")
    with arb_precision(precision_bits):
        R = 4 * t_shells + 2
        h_common = R - 2 * t_shells
        shell_specific = populations_for_t(
            t_shells, mode="shell_specific", precision_bits=precision_bits
        )
        common = populations_for_t(t_shells, mode="common_hole", precision_bits=precision_bits)
        q_specific = 1 + sum(item.population for item in shell_specific)
        q_common = 1 + sum(item.population for item in common)
        m_specific = 2 * q_specific
        m_common = 2 * q_common

        length_specific = arb(2) * _length_sum(
            t_shells,
            shell_specific,
            angular_cells=angular_cells,
            precision_bits=precision_bits,
        )
        length_common = arb(2) * _length_sum(
            t_shells,
            common,
            angular_cells=angular_cells,
            precision_bits=precision_bits,
        )
        ratio_specific = _ratio(length_specific, m_specific, precision_bits=precision_bits)
        ratio_common = _ratio(length_common, m_common, precision_bits=precision_bits)

        by_shell = []
        for s, c in zip(shell_specific, common):
            by_shell.append(
                {
                    "shell": s.shell,
                    "radius": s.radius,
                    "h_shell_specific": s.hole_radius,
                    "h_common": c.hole_radius,
                    "population_shell_specific": s.population,
                    "population_common": c.population,
                    "population_gain": s.population - c.population,
                }
            )

        return {
            "family": {
                "name": "finite shell-specific toroidal bundles",
                "status": "analytic geometric construction; finite arithmetic reproduction",
                "normalization": "radius-one tube; total centerline length",
                "t_shells": t_shells,
                "major_radius_R": R,
                "outer_minor_radius": 2 * t_shells,
                "common_hole_radius": h_common,
                "component_topology": f"T({m_specific},{m_specific})",
                "common_hole_component_topology": f"T({m_common},{m_common})",
                "bundle_components_Q_shell_specific": q_specific,
                "bundle_components_Q_common": q_common,
                "total_components_M_shell_specific": m_specific,
                "total_components_M_common": m_common,
                "proper_rotation": "P(x,y,z)=(R+x,-z,y), determinant +1",
                "cross_bundle_clearance_lower_bound": "R-4*T=2",
                "same_shell_clearance_rule": "N=floor(A)-1 with certified Arb floor",
                "inter_shell_clearance_rule": "radial spacing r_(i+1)-r_i=2",
                "topology_label": "T(2Q,2Q) via full-twist cabling proof route; sampled export is not a topology certificate",
            },
            "parameters": {
                "angular_cells_for_finite_lengths": angular_cells,
                "precision_bits": precision_bits,
                "output_digits": output_digits,
                "seeds": None,
            },
            "shell_specific_populations": [
                _population_record(item, digits=output_digits) for item in shell_specific
            ],
            "common_hole_populations": [
                _population_record(item, digits=output_digits) for item in common
            ],
            "comparison_by_shell": by_shell,
            "phases_shell_specific_bundle_1": _phase_list(shell_specific),
            "phases_common_bundle_1": _phase_list(common),
            "length_shell_specific": arb_record(
                length_specific, digits=output_digits, label="length_shell_specific"
            ),
            "length_common_hole": arb_record(length_common, digits=output_digits, label="length_common_hole"),
            "coefficient_shell_specific": arb_record(
                ratio_specific, digits=output_digits, label="coefficient_shell_specific"
            ),
            "coefficient_common_hole": arb_record(
                ratio_common, digits=output_digits, label="coefficient_common_hole"
            ),
            "published_model_references": {
                "Klotz_13_38": {
                    "coefficient": "13.38",
                    "label": "published-model reference: reported parameter-free toroidal construction coefficient",
                    "status": "reported model/numerical reference; not this certificate",
                    "source": "references/RECENT_TORUS_AUDIT.md, Klotz 2026 Sections III.1 and III.3",
                    "normalization": "radius-one tube",
                },
                "Klotz_11_68": {
                    "coefficient": "11.68",
                    "label": "published-model reference: conditional optimized-shell coefficient under stated no-overlap assumption",
                    "status": "conditional published model; not a certified bound here",
                    "source": "references/RECENT_TORUS_AUDIT.md, Klotz 2026 Section III.3",
                    "normalization": "radius-one tube",
                },
            },
        }


def _staggered_population_record(item: StaggeredShellPopulation, *, digits: int) -> dict[str, Any]:
    return {
        "shell": item.shell,
        "block_start": item.block_start,
        "radius": arb_record(item.radius, digits=digits, label=f"r_{item.shell}"),
        "hole_radius": arb_record(item.hole_radius, digits=digits, label=f"h_{item.shell}"),
        "capacity_radius": arb_record(
            item.capacity_radius, digits=digits, label=f"r_block_{item.block_start}"
        ),
        "capacity_hole_radius": arb_record(
            item.capacity_hole_radius, digits=digits, label=f"h_block_{item.block_start}"
        ),
        "capacity": arb_record(item.capacity, digits=digits, label=f"A_block_{item.block_start}"),
        "capacity_floor": item.capacity_floor,
        "population": item.population,
        "phase_offset": arb_record(item.phase_offset, digits=digits, label=f"offset_{item.shell}"),
        "rule": item.rule,
        "floor_certificate": {
            "statement": f"{item.capacity_floor} <= A(r_{item.block_start}) < {item.capacity_floor + 1}",
            "downward_rounding": "certified by Arb lower/upper endpoint floors",
        },
    }


def staggered_family_record(
    t_shells: int,
    *,
    angular_cells: int = 512,
    precision_bits: int = 192,
    output_digits: int = 60,
) -> dict[str, Any]:
    """Generate one finite record for the reviewed staggered-block candidate."""

    with arb_precision(precision_bits):
        R, populations = staggered_populations_for_t(
            t_shells, precision_bits=precision_bits
        )
        q = 1 + sum(item.population for item in populations)
        m = 2 * q
        length = arb(2) * _length_sum(
            t_shells,
            populations,
            major_radius=R,
            angular_cells=angular_cells,
            precision_bits=precision_bits,
        )
        ratio = _ratio(length, m, precision_bits=precision_bits)
        block_size = math.isqrt(t_shells)
        block_records: list[dict[str, Any]] = []
        seen: set[int] = set()
        for item in populations:
            if item.block_start in seen:
                continue
            seen.add(item.block_start)
            block_records.append(
                {
                    "block_start": item.block_start,
                    "block_end": min(item.block_start + block_size - 1, t_shells),
                    "population": item.population,
                    "phase_offsets": "0, pi/N alternating by shell parity within block",
                }
            )
        return {
            "family": {
                "name": "finite staggered equal-population shell blocks",
                "status": "reviewed mathematical candidate; finite arithmetic reproduction",
                "normalization": "radius-one tube; total centerline length",
                "theorem_reference": "proofs/THEOREM_002.md",
                "t_shells": t_shells,
                "block_size_floor_sqrt_T": block_size,
                "radial_gap_within_block": "sqrt(3)",
                "radial_gap_between_blocks": "2",
                "major_radius_R": arb_record(R, digits=output_digits, label="R"),
                "outer_radius": arb_record(populations[-1].radius, digits=output_digits, label="r_outer"),
                "component_topology": f"T({m},{m})",
                "bundle_components_Q": q,
                "total_components_M": m,
                "proper_rotation": "P(x,y,z)=(R+x,-z,y), determinant +1",
                "cross_bundle_clearance_lower_bound": "R-2*r_outer=2",
                "same_shell_clearance_rule": "N=floor(A(r_block_start,R-r_block_start))-1 with certified Arb floor",
                "phase_rule": "offset 0 and pi/N alternating within each block; strand phase 2*pi*j/N",
                "topology_label": "T(2Q,2Q) via reviewed full-twist configuration proof; sampled export is not a topology certificate",
            },
            "parameters": {
                "angular_cells_for_finite_lengths": angular_cells,
                "precision_bits": precision_bits,
                "output_digits": output_digits,
                "seeds": None,
            },
            "blocks": block_records,
            "populations": [
                _staggered_population_record(item, digits=output_digits) for item in populations
            ],
            "length": arb_record(length, digits=output_digits, label="staggered_length"),
            "coefficient": arb_record(ratio, digits=output_digits, label="staggered_coefficient"),
            "published_model_references": {
                "Klotz_13_38": {
                    "coefficient": "13.38",
                    "label": "published-model reference: reported parameter-free toroidal construction coefficient",
                    "status": "reported model/numerical reference; not this certificate",
                    "source": "references/RECENT_TORUS_AUDIT.md, Klotz 2026 Sections III.1 and III.3",
                    "normalization": "radius-one tube",
                },
                "Klotz_11_68": {
                    "coefficient": "11.68",
                    "label": "published-model reference: conditional optimized-shell coefficient under stated no-overlap assumption",
                    "status": "conditional published model; not a certified bound here",
                    "source": "references/RECENT_TORUS_AUDIT.md, Klotz 2026 Section III.3",
                    "normalization": "radius-one tube",
                },
            },
        }


def _sample_component(
    t_shells: int,
    *,
    radius: int | float | arb | None,
    phase: float,
    parameter_count: int,
    proper_rotation: bool,
    major_radius: float | None = None,
) -> list[tuple[float, float, float]]:
    """Sample one analytic component for a diagnostic VECT export."""

    R = float(4 * t_shells + 2) if major_radius is None else float(major_radius)
    out: list[tuple[float, float, float]] = []
    for k in range(parameter_count):
        t = 2.0 * math.pi * k / parameter_count
        if radius is None:
            x = R * math.cos(t)
            y = R * math.sin(t)
            z = 0.0
        else:
            r = float(radius)
            theta = t + phase
            x = (R + r * math.cos(t)) * math.cos(theta)
            y = (R + r * math.cos(t)) * math.sin(theta)
            z = r * math.sin(t)
        if proper_rotation:
            x, y, z = R + x, -z, y
        out.append((x, y, z))
    return out


def write_sampled_geometry(
    output_path: str | Path,
    t_shells: int,
    populations: Sequence[ShellPopulation],
    *,
    parameter_count: int = 64,
    major_radius: float | None = None,
) -> dict[str, Any]:
    """Write a deterministic diagnostic JSON geometry export.

    JSON is used instead of pretending that decimal VECT coordinates are an
    interval object.  The file includes all component formulas and the
    sampled coordinates so reviewers can inspect or feed them into polygon
    tools without confusing the sample with the analytic certificate.
    """

    if parameter_count < 4:
        raise ValueError("parameter_count must be at least four")
    output = Path(output_path)
    components: list[dict[str, Any]] = []
    component_index = 0
    is_staggered = any(isinstance(getattr(item, "radius", None), arb) for item in populations)
    for bundle, rotated in ((1, False), (2, True)):
        components.append(
            {
                "component": component_index,
                "bundle": bundle,
                "role": "core",
                "shell": None,
                "strand": None,
                "phase": "0",
                "formula": "C(t)=(R*cos(t),R*sin(t),0), then P for bundle 2",
                "sampled_coordinates": _sample_component(
                    t_shells,
                    radius=None,
                    phase=0.0,
                    parameter_count=parameter_count,
                    proper_rotation=rotated,
                    major_radius=major_radius,
                ),
            }
        )
        component_index += 1
        for item in populations:
            for strand in range(item.population):
                phase_offset = float(getattr(item, "phase_offset", 0.0))
                phase = 2.0 * math.pi * strand / item.population + phase_offset
                radius_value = (
                    float(item.radius) if isinstance(getattr(item, "radius", None), arb) else item.radius
                )
                components.append(
                    {
                        "component": component_index,
                        "bundle": bundle,
                        "role": "shell",
                        "shell": item.shell,
                        "radius": radius_value,
                        "strand": strand,
                        "phase": f"2*pi*{strand}/{item.population}",
                        "phase_decimal": phase,
                        "phase_offset_decimal": phase_offset,
                        "formula": "F_j(t)=((R+r*cos(t))*cos(t+phase),(R+r*cos(t))*sin(t+phase),r*sin(t)), then P for bundle 2",
                        "sampled_coordinates": _sample_component(
                            t_shells,
                            radius=item.radius,
                            phase=phase,
                            parameter_count=parameter_count,
                            proper_rotation=rotated,
                            major_radius=major_radius,
                        ),
                    }
                )
                component_index += 1
    record = {
        "geometry": {
            "name": (
                "finite staggered-block doubled bundle diagnostic geometry"
                if is_staggered
                else "finite shell-specific doubled bundle diagnostic geometry"
            ),
            "t_shells": t_shells,
            "major_radius_R": 4 * t_shells + 2 if major_radius is None else major_radius,
            "component_count": len(components),
            "proper_rotation": "P(x,y,z)=(R+x,-z,y), det=+1",
            "analytic_topology": f"T({len(components)},{len(components)}) by construction route",
            "sampled_coordinates_are_certificate": False,
            "sample_parameter_count": parameter_count,
        },
        "components": components,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(__import__("json").dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


__all__ = [
    "ShellPopulation",
    "StaggeredShellPopulation",
    "capacity",
    "certified_floor",
    "core_length",
    "finite_family_record",
    "populations_for_t",
    "staggered_family_record",
    "staggered_populations_for_t",
    "shell_length",
    "write_sampled_geometry",
]
