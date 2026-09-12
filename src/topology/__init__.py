"""Independent topology checks for constructive and sampled geometry."""

from .invariants import (
    TopologyReport,
    determinant_from_projection,
    identify_topology,
    spherogram_invariants,
    topology_report,
    torus_alexander_coefficients,
    torus_alexander_polynomial,
    torus_crossing_number,
    torus_invariants,
)
from .projection import (
    DEFAULT_VIEW,
    ProjectionCrossing,
    ProjectionResult,
    crossing_count,
    linking_matrix,
    linking_numbers,
    projected_crossings,
)

__all__ = [
    "DEFAULT_VIEW",
    "determinant_from_projection",
    "ProjectionCrossing",
    "ProjectionResult",
    "TopologyReport",
    "crossing_count",
    "identify_topology",
    "linking_matrix",
    "linking_numbers",
    "projected_crossings",
    "spherogram_invariants",
    "topology_report",
    "torus_alexander_coefficients",
    "torus_alexander_polynomial",
    "torus_crossing_number",
    "torus_invariants",
]
