# Arb backend validation

The certificate uses `python-flint` 0.9.x through `from flint import arb, ctx`.
An Arb value is a real ball containing its represented real number. The
certificate sets `ctx.prec` in bits for each run, and uses only integer Arb
constructors, Arb division, and Arb elementary functions after that point.

The endpoint contract used by the implementation is:

* `x.lower()` returns an exact Arb value rounded toward negative infinity;
* `x.upper()` returns an exact Arb value rounded toward positive infinity;
* `x.lower().fmpq()` and `x.upper().fmpq()` expose those finite binary endpoints
  as exact rational numbers;
* `x.str(..., more=True)` is only a readable rendering. The rational endpoint
  pairs in each JSON record are authoritative.

`validate_backend()` checks the endpoint ordering, exact integer conversion,
and availability of `sin`, `cos`, `sqrt`, and `asinh`. The certificate output
stores that evidence under `arb_backend_validation`. It also stores the
python-flint version, precision, source hashes, runtime information, and a
detached SHA-256 hash for the manifest.

This design follows the installed python-flint API documentation and its
docstrings. It does not serialize `float(arb_value)` anywhere in the proof
path. Sampled geometry exports use ordinary decimal coordinates and are
explicitly marked as non-certifying diagnostics.
