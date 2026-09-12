"""Constructive torus invariants and optional knot-library cross-checks."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np

from .projection import ProjectionResult, linking_matrix, projected_crossings


@dataclass
class TopologyReport:
    name: str
    component_count: int
    constructive: dict[str, Any] = field(default_factory=dict)
    projection: dict[str, Any] = field(default_factory=dict)
    invariants: dict[str, Any] = field(default_factory=dict)
    sampled_type_certified: bool = False
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        return self.as_dict()[key]


def determinant_from_projection(projection: ProjectionResult | list[Any], *, component: int = 0) -> int | None:
    """Compute a knot determinant from a projected crossing diagram.

    At ``t=-1`` the Fox/Alexander coloring relation at a crossing is
    ``2*over-under_in-under_out=0``.  We assign arcs by walking the sampled
    component and cutting at undercrossings, then take a reduced integer
    determinant.  This is an independent diagram calculation; it is only
    attempted for a one-component, transverse projection with one occurrence
    of each undercrossing.
    """

    crossings = projection.crossings if isinstance(projection, ProjectionResult) else list(projection)
    crossings = [item for item in crossings if getattr(item, "component_a", None) == component and getattr(item, "component_b", None) == component]
    if not crossings or any(not getattr(item, "transverse", True) or getattr(item, "over", "ambiguous") == "ambiguous" for item in crossings):
        return None
    under_events: list[tuple[float, int, float]] = []
    over_parameters: list[float] = []
    for index, crossing in enumerate(crossings):
        if crossing.over == "a":
            under_parameter = float(crossing.parameter_b)
            over_parameter = float(crossing.parameter_a)
        elif crossing.over == "b":
            under_parameter = float(crossing.parameter_a)
            over_parameter = float(crossing.parameter_b)
        else:
            return None
        under_events.append((under_parameter % 1.0, index, over_parameter % 1.0))
        over_parameters.append(over_parameter % 1.0)
    under_events.sort(key=lambda item: item[0])
    n = len(under_events)
    if n < 1:
        return None
    # Every crossing of a regular knot diagram contributes exactly one
    # undercrossing event.  Duplicate parameters indicate a non-generic or
    # under-resolved polygon and are rejected instead of guessed.
    if any(abs(under_events[i][0] - under_events[(i + 1) % n][0]) <= 1e-10 for i in range(n - 1)):
        return None
    crossing_to_under_index = {crossing_index: event_index for event_index, (_, crossing_index, _) in enumerate(under_events)}

    def arc_containing(parameter: float) -> int:
        parameter %= 1.0
        starts = [item[0] for item in under_events]
        # The last start before the overcrossing owns the arc until the next
        # undercrossing, with wraparound handled by modulo.
        index = int(np.searchsorted(starts, parameter, side="right") - 1)
        return index % n

    matrix = np.zeros((n, n), dtype=int)
    for _, crossing_index, over_parameter in under_events:
        under_index = crossing_to_under_index[crossing_index]
        incoming_arc = (under_index - 1) % n
        outgoing_arc = under_index
        over_arc = arc_containing(over_parameter)
        matrix[ crossing_index % n, over_arc] += 2
        matrix[ crossing_index % n, incoming_arc] -= 1
        matrix[ crossing_index % n, outgoing_arc] -= 1
    if n == 1:
        return 0
    reduced = matrix[:-1, :-1].tolist()
    if not reduced:
        return 0
    # Fraction-free Bareiss elimination keeps this a genuinely integer
    # calculation even when a projection has more than a handful of crossings.
    sign = 1
    previous_pivot = 1
    size = len(reduced)
    for pivot_index in range(size - 1):
        pivot_row = next((row for row in range(pivot_index, size) if reduced[row][pivot_index] != 0), None)
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            reduced[pivot_index], reduced[pivot_row] = reduced[pivot_row], reduced[pivot_index]
            sign *= -1
        pivot = reduced[pivot_index][pivot_index]
        if pivot == 0:
            return 0
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = reduced[row][column] * pivot - reduced[row][pivot_index] * reduced[pivot_index][column]
                if previous_pivot != 1:
                    if numerator % previous_pivot:
                        return None
                    numerator //= previous_pivot
                reduced[row][column] = numerator
            reduced[row][pivot_index] = 0
        previous_pivot = pivot
    determinant = sign * reduced[-1][-1]
    return abs(int(determinant))


def torus_crossing_number(p: int, q: int) -> int:
    """Minimal crossing number formula for a coprime torus knot."""

    p, q = abs(int(p)), abs(int(q))
    if p == 0 or q == 0 or p == 1 or q == 1:
        return 0
    if np.gcd(p, q) != 1:
        raise ValueError("crossing number formula here is for torus knots (gcd=1)")
    return min(p * (q - 1), q * (p - 1))


def torus_alexander_coefficients(p: int, q: int) -> dict[int, int]:
    """Return Laurent coefficients of the torus-knot Alexander polynomial.

    Coefficients are represented by integer exponent keys.  The polynomial is
    normalized up to multiplication by ``±t^k``; this routine chooses the
    symmetric normalization generated by the standard product formula.
    """

    p, q = abs(int(p)), abs(int(q))
    if p == 0 or q == 0 or p == 1 or q == 1:
        return {0: 1}
    if np.gcd(p, q) != 1:
        raise ValueError("Alexander polynomial formula here is for gcd(p,q)=1")
    # Use integer polynomial long division for
    #   (t^(pq)-1)(t-1) / ((t^p-1)(t^q-1)).
    numerator: dict[int, int] = {p * q + 1: 1, p * q: -1, 1: -1, 0: 1}
    denominator: dict[int, int] = {p + q: 1, p: -1, q: -1, 0: 1}
    quotient: dict[int, int] = {}
    remainder = dict(numerator)
    lead_den = max(denominator)
    while remainder:
        degree = max(remainder)
        coefficient = remainder[degree]
        if coefficient == 0:
            remainder.pop(degree)
            continue
        shift = degree - lead_den
        if shift < 0:
            raise ArithmeticError("torus Alexander numerator is not divisible by denominator")
        quotient[shift] = quotient.get(shift, 0) + coefficient
        for exponent, value in denominator.items():
            target = exponent + shift
            remainder[target] = remainder.get(target, 0) - coefficient * value
            if remainder[target] == 0:
                remainder.pop(target)
    if remainder:
        raise ArithmeticError(f"nonzero remainder in torus Alexander division: {remainder}")
    # Remove zeroes and centre the Laurent polynomial.
    quotient = {int(exponent): int(value) for exponent, value in quotient.items() if value}
    if not quotient:
        return {0: 1}
    centre = (min(quotient) + max(quotient)) / 2.0
    if centre.is_integer():
        centred = {int(exponent - int(centre)): coefficient for exponent, coefficient in quotient.items()}
    else:
        centred = quotient
    # The long division can differ by an overall sign depending on ordering;
    # normalize the highest coefficient positive for deterministic output.
    lead = centred[max(centred)]
    if lead < 0:
        centred = {exponent: -coefficient for exponent, coefficient in centred.items()}
    return dict(sorted(centred.items()))


def torus_alexander_polynomial(p: int, q: int) -> str:
    coefficients = torus_alexander_coefficients(p, q)
    terms: list[str] = []
    for exponent, coefficient in sorted(coefficients.items(), reverse=True):
        if coefficient == 0:
            continue
        magnitude = abs(coefficient)
        if exponent == 0:
            monomial = str(magnitude)
        elif exponent == 1:
            monomial = ("" if magnitude == 1 else str(magnitude)) + "t"
        else:
            monomial = ("" if magnitude == 1 else str(magnitude)) + f"t^{exponent}"
        if not terms:
            terms.append(("-" if coefficient < 0 else "") + monomial)
        else:
            terms.append((" - " if coefficient < 0 else " + ") + monomial)
    return "".join(terms) or "1"


def torus_invariants(p: int, q: int) -> dict[str, Any]:
    p, q = int(p), int(q)
    d = int(np.gcd(abs(p), abs(q)))
    if d == 1:
        coefficients = torus_alexander_coefficients(p, q)
        determinant = abs(sum(value * (-1) ** exponent for exponent, value in coefficients.items()))
        return {
            "family": "torus knot",
            "torus_type": [p, q],
            "components": 1,
            "crossing_number": torus_crossing_number(p, q),
            "alexander_coefficients": {str(key): value for key, value in coefficients.items()},
            "alexander_polynomial": torus_alexander_polynomial(p, q),
            "determinant": int(determinant),
            "route": "constructive torus formula",
        }
    reduced_p, reduced_q = p // d, q // d
    pairwise = int(reduced_p * reduced_q)
    return {
        "family": "torus link",
        "torus_type": [p, q],
        "components": d,
        "reduced_winding": [reduced_p, reduced_q],
        "pairwise_linking_number": pairwise,
        "route": "constructive torus parameterization",
    }


def _metadata_torus(value: Any) -> tuple[int, int] | None:
    metadata = getattr(value, "metadata", {}) or {}
    torus_type = metadata.get("torus_type")
    if torus_type is None and hasattr(value, "p") and hasattr(value, "q"):
        torus_type = [value.p, value.q]
    if isinstance(torus_type, (list, tuple)) and len(torus_type) == 2:
        return int(torus_type[0]), int(torus_type[1])
    return None


def spherogram_invariants(name: str) -> dict[str, Any]:
    """Try an optional spherogram lookup without making Sage a dependency."""

    try:
        from spherogram import Link

        link = Link(name)
    except Exception as error:
        return {"name": name, "available": False, "error": str(error)}
    result: dict[str, Any] = {"name": name, "available": True}
    for attribute in ("determinant", "alexander_polynomial", "jones_polynomial", "linking_matrix"):
        function = getattr(link, attribute, None)
        if function is None:
            continue
        try:
            value = function()
            result[attribute] = str(value) if attribute != "linking_matrix" else value
        except Exception as error:
            result[f"{attribute}_error"] = str(error)
    return result


def topology_report(value: Any, *, samples: int = 512, view: Any = None, tolerance: float = 1e-9) -> TopologyReport:
    projection_kwargs = {"samples": int(samples), "tolerance": float(tolerance)}
    if view is not None:
        projection_kwargs["view"] = view
    projection = projected_crossings(value, **projection_kwargs)
    matrix = linking_matrix(value, **projection_kwargs)
    constructive: dict[str, Any] = {}
    invariants: dict[str, Any] = {}
    torus_type = _metadata_torus(value)
    if torus_type is not None:
        p, q = torus_type
        constructive = {
            "family": "standard torus",
            "torus_type": [p, q],
            "components": int(np.gcd(abs(p), abs(q))),
            "isotopy_certificate": getattr(value, "metadata", {}).get("isotopy_certificate", "standard torus parameterization"),
        }
        invariants = torus_invariants(p, q)
    metadata = getattr(value, "metadata", {}) or {}
    if metadata.get("kind") == "hopf":
        constructive = {
            "family": "round Hopf link",
            "components": 2,
            "isotopy_certificate": "two explicit linked round circles",
        }
        invariants = {"pairwise_linking_number": 1, "route": "disk piercing plus projected check"}
    projection_dict = projection.as_dict()
    projection_dict["linking_matrix"] = matrix.tolist()
    diagram_determinant = determinant_from_projection(projection)
    projection_dict["determinant_at_minus_one"] = diagram_determinant
    if diagram_determinant is not None:
        invariants["projection_determinant_at_minus_one"] = diagram_determinant
    notes = ["projection is a sampled generic check; it does not certify the analytic isotopy"]
    if diagram_determinant is None and projection.component_count == 1:
        notes.append("diagram determinant unavailable for this sampled projection")
    return TopologyReport(
        name=getattr(value, "name", "sampled geometry"),
        component_count=projection.component_count,
        constructive=constructive,
        projection=projection_dict,
        invariants=invariants,
        sampled_type_certified=False,
        notes=notes,
    )


def identify_topology(value: Any, **kwargs: Any) -> TopologyReport:
    return topology_report(value, **kwargs)


__all__ = [
    "TopologyReport",
    "determinant_from_projection",
    "identify_topology",
    "spherogram_invariants",
    "topology_report",
    "torus_alexander_coefficients",
    "torus_alexander_polynomial",
    "torus_crossing_number",
    "torus_invariants",
]
