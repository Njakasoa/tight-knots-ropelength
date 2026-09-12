"""Adversarial review probes; checks fixes without importing project tests."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,'src')
import numpy as np
from thickness import polygon_thickness
from topology import topology_report, projected_crossings
from curves import torus_link,exact_hopf_control,exact_circle_control
out={}
polys={
'scaled_crossing':np.array([[0,0,0],[1,0,0],[.5,-1,0],[.5,1,0]],float)*1e-7,
'near_endpoint_collision':np.array([[0,0,0],[1,0,0],[1,-1,0],[5e-9,-1,0],[5e-9,1,0],[-1,1,0]],float)}
for key,p in polys.items():
 r=polygon_thickness(p)
 out[key]={'thickness':r.thickness,'complete':r.complete,'degenerate':r.degenerate,'notes':r.notes,'passed':r.thickness==0 or not r.complete}
pts=torus_link(2,3,major_radius=3,minor_radius=1).components[0].sample(48)
for scale in [1,1e-5,1e-7,1e5]:
 try:
  r=topology_report(pts*scale)
  determinant=r.invariants.get('projection_determinant_at_minus_one')
  out[f'topology_scale_{scale}']={'determinant':determinant,'generic':r.projection['generic'],'passed':determinant==3 or not r.projection['generic']}
 except ValueError as e:
  out[f'topology_scale_{scale}']={'unresolved':str(e),'passed':True}
# Projection of the xy circle edge-on is a collapsed/overlapped diagram.
theta=np.arange(24)*2*np.pi/24
r=projected_crossings(np.column_stack([np.cos(theta),np.sin(theta),np.zeros(24)]),view=[1,0,0])
out['nongeneric_projection']={'generic':r.generic,'notes':r.notes,'passed':not r.generic}
for terms in [12,40]:
 r=exact_hopf_control(terms=terms)
 bounds=r['ropelength_rational_endpoints']
 lo,hi=[Fraction(int(b['numerator']),int(b['denominator'])) for b in bounds]
 pilo,pihi=[Fraction(int(b['numerator']),int(b['denominator'])) for b in r['pi_rational_endpoints']]
 directed=Fraction(r['ropelength_interval'][0])<=lo<=hi<=Fraction(r['ropelength_interval'][1])
 out[f'exact_hopf_{terms}']={'record':r,'directed_decimal_verified':directed,'passed':r['ropelength_exact_expression']=='8*pi' and lo==8*pilo and hi==8*pihi and directed}
out['source_hashes']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['src/thickness/polygon.py','src/topology/projection.py','src/curves/exact.py']}
out['all_passed']=all(v.get('passed',True) for v in out.values() if isinstance(v,dict))
Path('results/reviewer_geometry_regressions.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a!='record'} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
