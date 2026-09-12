"""Enclose candidate003 boundary constants by direct Arb interval integration.

Rectangle range enclosures need no derivative-error assertion. This is separate
from the theorem's asymptotic argument and from a claim of publication novelty.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, sys, time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.certification.arb_backend import arb,arb_precision,arb_record
def enclosure(record):
 def endpoint(x):return arb(int(x['numerator']))/arb(int(x['denominator']))
 return endpoint(record['lower']).union(endpoint(record['upper']))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--N',type=int,default=512);parser.add_argument('--M',type=int,default=1024);args=parser.parse_args()
 if args.N<1 or args.M<1:raise ValueError('positive cell counts required')
 out=ROOT/'results'/('boundary_certificate_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));out.mkdir()
 source=ROOT/'results/certificate_shell_N512M1024_noguard/certificate.json';base=json.loads(source.read_text());start=time.monotonic()
 with arb_precision(192):
  pi=arb.pi();dx=arb(1)/args.N;dt=2*pi/args.M
  cosines=[((2*j+1)*pi/args.M+arb(0,(dt/2).upper())).cos() for j in range(args.M)]
  total=arb(0)
  for i in range(args.N):
   x=arb(2*i+1)/(2*args.N)+arb(0,(dx/2).upper())
   v2=x*x+(2-x)*(2-x)
   dn=4*pi*(1-x)*(x*x-2*x+4)/(v2*v2.sqrt())
   for cosine in cosines:
    speed=((4+2*x*cosine)**2+4*x*x).sqrt()
    total+=dn*speed
  J=total*dx*dt
  q0=enclosure(base['q0']);l0=enclosure(base['l0']);alpha2=enclosure(base['optional_staggered_rescaling']['alpha2'])
  n1=arb(2).sqrt()*pi;a=1/arb(3).sqrt()-arb(1)/2
  d=3*n1/(4*q0)-J/(2*l0)
  if not d>0:raise ArithmeticError('mesh does not certify d>0')
  c=(a/d).sqrt();beta=2*alpha2*(a*d).sqrt();baseline_beta=alpha2*(a+d)
  result={'experiment_id':out.name,'N':args.N,'M':args.M,'precision_bits':192,'method':'sum of Arb ranges over all exact parameter rectangles; no midpoint truncation error assumption','J':arb_record(J),'a':arb_record(a),'d':arb_record(d),'optimal_c':arb_record(c),'optimal_beta':arb_record(beta),'baseline_c1_beta':arb_record(baseline_beta),'checks':{'d_positive':bool(d>0),'c_less_than_one':bool(c<1),'beta_below_baseline':bool(beta.upper()<baseline_beta.lower())},'scope':'interval constants for theorem003 candidate; theorem/asymptotic validity requires independent proof review','runtime_seconds':time.monotonic()-start}
 p=out/'certificate.json';p.write_text(json.dumps(result,indent=2)+'\n')
 files=[Path(__file__),ROOT/'src/certification/arb_backend.py',ROOT/'proofs/THEOREM_003_CANDIDATE.md',source]
 manifest={'output_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inputs':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(out);print('c',result['optimal_c']['arb']);print('beta',result['optimal_beta']['arb']);print(result['checks'])
if __name__=='__main__':main()
