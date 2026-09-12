"""Independent arithmetic audit; run from tight-knots-lab with .venv/bin/python."""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction
from flint import arb,ctx
ctx.prec=224
N,M=512,1024
started=time.perf_counter()
pi=arb.pi()
xvalues=[arb(2*i+1)/arb(2*N) for i in range(N)]
densities=[2*pi*x*(2-x)/(x*x+(2-x)*(2-x)).sqrt() for x in xvalues]
mesh=arb(0)
for j in range(M):
 c=(pi*arb(2*j+1)/arb(M)).cos()
 row=arb(0)
 for x,n in zip(xvalues,densities):
  row+=n*((4+2*x*c)**2+4*x*x).sqrt()
 mesh+=row
mesh*=2*pi/arb(N*M)
error=(2*pi)/24*(arb(600)/arb(N*N)+60*(2*pi/arb(M))**2)
length=mesh+arb(0,error.upper())
q=pi*(3*arb(1).asinh()/arb(2).sqrt()-1)
a1=length/(arb(2).sqrt()*q*q.sqrt())
a2=(arb(3).sqrt()/2).sqrt()*a1
source=Path('results/certificate_shell_N512M1024_noguard')
cert=json.loads((source/'certificate.json').read_text())
def endpoint(record,side):
 d=record[side]
 return Fraction(int(d['numerator']),int(d['denominator']))
def own(v,side):
 q=getattr(v,side)().fmpq()
 return Fraction(int(q.numerator),int(q.denominator))
checks={}
for k,v,r in [('q0',q,cert['q0']),('l0',length,cert['l0']),('alpha1',a1,cert['alpha']),('alpha2',a2,cert['optional_staggered_rescaling']['alpha2'])]:
 checks[k]={'independent_lower':str(own(v,'lower')),'independent_upper':str(own(v,'upper')),'independent_display':v.str(35),'overlap':own(v,'lower')<=endpoint(r,'upper') and endpoint(r,'lower')<=own(v,'upper')}
checks['threshold']={'stored_upper_lt_10_614_exact_rational':endpoint(cert['optional_staggered_rescaling']['alpha2'],'upper')<Fraction(10614,1000),'independent_upper_lt_10_614':bool(a2.upper()<arb('10.614'))}
manifest=json.loads((source/'manifest.json').read_text())
checks['hashes']={'sources_match':all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in manifest['source_hashes'].items()),'outputs_match':all(hashlib.sha256((source/p).read_bytes()).hexdigest()==h for p,h in manifest['outputs_sha256'].items()),'manifest_detached_match':hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest()==(source/'manifest.sha256').read_text().split()[0]}
checks['runtime']={'precision_bits':224,'N':N,'M':M,'elapsed_seconds':time.perf_counter()-started,'implementation':'independent angular-outer tensor loop, no production certificate helper imports'}
Path('results/reviewer_certificate_check.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
