# Recent construction reproduction and limits

The supplied2026 T(4,4) geometry is audited in
`results/recent_T44_20260912T220613Z/inspection.json`. Our independent numerical
engine and actual plCurve agree to about1e-13 on polygonal ropelength77.97687288.
All six pairwise linking numbers are-1, and the finite graph at tolerance1e-4
has1011 contacts. The visual in `geometry/recent_T44_contacts` aggregates contacts
by unordered component pair. Linking and contact counts are numerical diagnostics.

The companion summary table gives77.47, which is **not** reproduced from the
supplied coordinates. See references/SOFTWARE_DATA.md for the measured discrepancy
and explicit normalization. The current record is a coordinate reproduction,
not confirmation of every printed numerical value in the article.

The shell-family runner separately reproduces a conservative common-hole model
and compares it with shell-specific and staggered population rules. Its common
model uses R=4T+2,h=2T+2 and floor(A)-1. These finite safety margins differ from
Klotz's proposed maximum-occupancy epsilon rule; they have the same leading
continuum population density but are not an exact finite reproduction of that
conditional rule. Printed13.38/11.68 entries in output are literature references,
not numbers recomputed by the certified integral routine.

This distinction matters for M2: compare like normalization, topology and
continuous clearance, retain original/reference data, and never count a hardcoded
literature decimal as experimental reproduction.

## Direct continuum coefficient reproduction

`experiments/reproduce_klotz_limits.py` now evaluates both population densities
against the toroidal length integral, without inserting printed correction
factors. The immutable run `results/klotz_limits_20260912T221239Z` gives
13.377596407953076 for n(x)=4x and11.685949053273111 for
n(x)=2πx/sqrt(1+x²). Two quadrature tolerances1e-8 and1e-11 agree. These reproduce
the reported approximate13.38 and11.68 continuum values (the latter is a coarse
printed approximation; ordinary two-decimal rounding of this integral is11.69).
SciPy error estimates are diagnostic, not certified intervals. This run does not
supply the missing proof for the paper's proposed finite epsilon occupancy rule.
