"""M2 exhaustive finite block-size search inside the proved shell grammar.

The objective is a construction's crossing-normalized length, not comparison
of the true minima of different link types. Block sizes are exhaustively varied;
the script does not encode a preferred size or exponent.
"""
from pathlib import Path
import datetime, hashlib, json, platform, subprocess, time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def candidate(T,b,nodes,weights):
 i=np.arange(1,T+1);first=1+b*((i-1)//b)
 delta=np.sqrt(3)
 radius=delta*i+(2-delta)*(1+(i-1)//b)
 inner=delta*first+(2-delta)*(1+(first-1)//b)
 R=2*radius[-1]+2
 capacity=np.pi*inner*(R-inner)/np.hypot(inner,R-inner)
 populations=np.floor(capacity).astype(int)-1
 if np.min(populations)<3:raise ValueError('inadmissible shell population')
 length=np.sqrt((R+radius[:,None]*np.cos(nodes))**2+radius[:,None]**2)@weights
 components=int(2*(1+populations.sum()))
 total=float(2*(2*np.pi*R+populations@length))
 return {'T':T,'block_size':b,'components':components,'major_radius':float(R),'total_length':total,'coefficient':total/(components*(components-1))**.75,'minimum_floor_margin':float(np.min(np.minimum(capacity-np.floor(capacity),np.ceil(capacity)-capacity)))}
def main():
 gate=ROOT/'benchmarks/M1_REVIEW.md'
 if '**PASS for M1:' not in gate.read_text():raise SystemExit('M1 must pass before M2')
 out=ROOT/'results'/('discovery_blocks_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));out.mkdir()
 x,w=np.polynomial.legendre.leggauss(48);nodes=np.pi*(x+1);weights=np.pi*w
 xx,ww=np.polynomial.legendre.leggauss(96)
 start=time.monotonic();all_rows=[];best=[]
 for T in [8,16,32,64,128,256,512,1024]:
  rows=[candidate(T,b,nodes,weights) for b in range(1,T+1)]
  all_rows.extend(rows);winner=min(rows,key=lambda r:r['coefficient'])
  finer=candidate(T,winner['block_size'],np.pi*(xx+1),np.pi*ww)
  winner=dict(winner,coefficient_96_nodes=finer['coefficient'],quadrature_change=abs(finer['coefficient']-winner['coefficient']))
  best.append(winner);print(winner,flush=True)
 logT=np.log([r['T'] for r in best[-5:]]);logb=np.log([r['block_size'] for r in best[-5:]])
 slope,intercept=np.polyfit(logT,logb,1)
 result={'experiment_id':out.name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'M1_review_sha256':hashlib.sha256(gate.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'platform':platform.platform(),'numpy':np.__version__,'runtime_seconds':time.monotonic()-start,'method':'exhaustive b=1..T; Gauss-Legendre48 with96-node winner check','optimizer':'finite exhaustive enumeration; deterministic, no seed','grammar':{'family':'T(M,M)','pitch_winding':1,'radial_gap_within_blocks':'sqrt(3)','radial_gap_between_blocks':2,'phase_rule':'alternating0,pi/N','population':'floor(inner block capacity)-1','closure':'doubled Hopf-core motion, R=2r_outer+2','free_parameters':['T','block size','induced populations','induced radii','induced M']},'observations':{'fitted_power_last_five':float(slope),'fitted_multiplier':float(np.exp(intercept)),'fit_is_proof':False,'message':'The block exponent and multiplier are inferred from winners, not supplied to the search.'},'best':best,'all_candidates':all_rows,'scope':'floating candidate discovery; no interval floor/length certificate for new block sizes; comparison normalizes different finite link types and is not a same-M optimum'}
 p=out/'discovery.json';p.write_text(json.dumps(result,indent=2)+'\n')
 (out/'manifest.json').write_text(json.dumps({'discovery_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n');print(out,flush=True)
if __name__=='__main__':main()
