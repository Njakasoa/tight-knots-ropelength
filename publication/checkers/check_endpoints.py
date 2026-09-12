"""Dependency-free rational verification of the bundled certificate thresholds.

This checks exact stored enclosures and their integrity, not the analytic proof
or the correctness of Arb. Reproduction and independent reviews address those.
"""
if not __debug__:
    raise RuntimeError('proof checker requires assertions; optimized Python is unsupported')

from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
def frac(point):return Fraction(int(point['numerator']),int(point['denominator']))
def check():
 pins=json.loads((ROOT/'publication/PINNED_INPUTS.json').read_text())
 for name,digest in pins.items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise AssertionError(f'input hash mismatch: {name}')
 base=json.loads((ROOT/'results/certificate_shell_N512M1024_noguard/certificate.json').read_text())
 alpha=base['optional_staggered_rescaling']['alpha2']
 assert 0<frac(alpha['lower'])<=frac(alpha['upper'])<Fraction('10.614')
 boundary=json.loads((ROOT/'results/boundary_certificate_20260912T222341Z/certificate.json').read_text())
 c=boundary['optimal_c'];beta=boundary['optimal_beta'];baseline=boundary['baseline_c1_beta']
 assert Fraction('.4205')<frac(c['lower'])<=frac(c['upper'])<Fraction('.4252')
 assert 0<frac(boundary['d']['lower'])
 assert frac(beta['upper'])<frac(baseline['lower'])
 return {'pinned_inputs':len(pins),'alpha_below_10_614':True,'c_between_0_4205_and_0_4252':True,'strict_correction_improvement':True}
if __name__=='__main__':print(json.dumps(check(),indent=2))
