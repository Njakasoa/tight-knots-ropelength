"""Independent numerical attacks on Candidate003; no production helpers."""
from pathlib import Path
import json,math,time,hashlib
import numpy as np
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
start=time.perf_counter();pi=math.pi;delta=math.sqrt(3);gap=2-delta
n=lambda x:2*pi*x*(2-x)/math.sqrt(x*x+(2-x)**2)
nd=lambda x:4*pi*(1-x)*(x*x-2*x+4)/(x*x+(2-x)**2)**1.5
def e(x):return quad(lambda t:math.sqrt((4+2*x*math.cos(t))**2+4*x*x),0,2*pi,epsabs=2e-11,epsrel=2e-13)[0]
q=quad(n,0,1,epsabs=1e-12)[0];l=quad(lambda x:n(x)*e(x),0,1,epsabs=1e-10)[0];j=quad(lambda x:nd(x)*e(x),0,1,epsabs=1e-10)[0]
a=gap/(2*delta);d=3*n(1)/(4*q)-j/(2*l);alpha=math.sqrt(delta/2)*l/(math.sqrt(2)*q**1.5);cstar=math.sqrt(a/d)
z,w=leggauss(96);cs=np.cos(pi*(z+1))
def finite(T,b):
 i=np.arange(1,T+1,dtype=np.int64);block=((i-1)//b);first=1+b*block
 radii=delta*i+gap*(block+1);R=2*radii[-1]+2
 rf=delta*first+gap*(block+1)
 cap=pi*rf*(R-rf)/np.hypot(rf,R-rf)
 pop=np.floor(cap).astype(np.int64)-1
 Q=1+int(pop.sum());length=2*pi*R
 # Batches avoid an unnecessarily large temporary array.
 for k in range(0,T,1024):
  rr=radii[k:k+1024,None]
  lengths=np.sqrt((R+rr*cs)**2+rr*rr)@(pi*w)
  length+=float(pop[k:k+1024]@lengths)
 M=2*Q;F=2*length/(float(M*(M-1))**.75)
 return F,Q,float(np.min(np.abs(cap-np.rint(cap))))
rows=[]
for c in [.2,cstar,1.,2.]:
 beta=alpha*(a/c+d*c)
 for T in [128,257,1024,4099,16384,65539]:
  b=max(1,int(c*math.sqrt(T)))
  F,Q,margin=finite(T,b)
  rows.append({'T':T,'b':b,'c':c,'remainder_shells':T%b,'F':F,'Q':Q,'sqrtT_correction':math.sqrt(T)*(F-alpha),'predicted_beta':beta,'T_scaled_residual':T*(F-alpha-beta/math.sqrt(T)),'nearest_capacity_integer_gap_diagnostic':margin})
uniform=[]
for T in [257,4099,65539]:
 for power in [.25,.4,.6,.75]:
  b=max(1,int(T**power));F,Q,margin=finite(T,b)
  error=F/alpha-1-a/b-d*b/T;scale=1/b**2+(b/T)**2+1/T
  uniform.append({'T':T,'b':b,'power':power,'remainder_shells':T%b,'normalized_error':error/scale})
record={'scope':'diagnostic independent floating construction and quadrature; not a floor/length certificate','q0':q,'l0':l,'J':j,'a':a,'d':d,'alpha2':alpha,'cstar':cstar,'beta_opt':2*alpha*math.sqrt(a*d),'beta_one':alpha*(a+d),'d_analytic_lower':n(1)/q*(6-math.sqrt(22))/8,'fixed_c_tests':rows,'uniform_tests':uniform,'elapsed_seconds':time.perf_counter()-start,'candidate_sha256':hashlib.sha256(Path('proofs/THEOREM_003_CANDIDATE.md').read_bytes()).hexdigest()}
Path('results/reviewer003_independent.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['fixed_c_tests','uniform_tests']},indent=2))
for c in [.2,cstar,1.,2.]:
 r=[r for r in rows if r['c']==c];print('c',c,'scaled residues',[round(x['T_scaled_residual'],6) for x in r])
print('uniform normalized residual max',max(abs(x['normalized_error']) for x in uniform))
