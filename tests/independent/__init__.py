"""Adversarial validation that keeps reference calculations outside ``src``.

The tests in this package intentionally implement their own polygon, length,
projection, and interval checks.  Production routines are used only as the
system under test, or for a side-by-side comparison with the independently
built plCurve executable.
"""

