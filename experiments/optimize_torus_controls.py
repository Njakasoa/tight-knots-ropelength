"""Initial bounded parameter searches, before M1; no optimality/certificate claim.

Uses actual octrope/plCurve as numerical objective, SciPy as our optimizer.
The analytic torus is embedded for R>1 and positive vertical scale; its type
is preserved by the positive ambient z scaling. The sampled polygons require
separate topology checks. Every accepted final geometry and evaluation is kept.
"""
from pathlib import Path
import datetime, hashlib, json, platform, subprocess, sys, tempfile, time
import numpy as np
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.curves import torus_link, write_vect
CLI=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
def main():
 out=ROOT/'results'/('torus_search_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
 out.mkdir()
 start=time.monotonic(); records=[]
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 for p,q in [(2,3),(2,5),(3,4),(2,2)]:
  for seed in [1729,2718]:
   history=[]
   def geometry(x,n):
    curve=torus_link(p,q,major_radius=float(x[0]),minor_radius=1)
    return [c.sample(n)*np.array([1.,1.,float(x[1])]) for c in curve.components]
   with tempfile.TemporaryDirectory(prefix='torus-search-') as td:
    path=Path(td)/'candidate.vect'
    def evaluate(x,n=96):
     write_vect(path,geometry(x,n))
     value=float(subprocess.check_output([str(CLI),'-q',str(path)],text=True).strip())
     if n==96:history.append({'R':float(x[0]),'z_scale':float(x[1]),'polygon_ropelength':value})
     return value
    baseline=evaluate([2,1])
    solution=differential_evolution(evaluate,[(1.05,5),(.3,3)],seed=seed,popsize=6,maxiter=14,tol=1e-5,polish=False,workers=1)
    convergence=[{'samples_per_component':n,'polygon_ropelength':evaluate(solution.x,n)} for n in [192,384]]
   path=out/f'T{p}_{q}_seed{seed}.vect';write_vect(path,geometry(solution.x,384),overwrite=False)
   record={'torus_type':[p,q],'seed':seed,'optimizer':'scipy differential_evolution','bounds':[[1.05,5],[.3,3]],'maxiter':14,'popsize':6,'tol':1e-5,'polish':False,'baseline_R2_z1':baseline,'best_parameters':solution.x.tolist(),'coarse_ropelength':float(solution.fun),'resolution_checks':convergence,'termination':str(solution.message),'evaluations':history,'geometry':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'proof_level':1,'analytic_topology':'standard T(p,q), R>1, followed by positive invertible z scaling','sampled_topology_status':'requires independent projection/invariants; not certified','thickness_status':'numerical Rawdon/octrope; not smooth reach certificate'}
   records.append(record)
   (out/'search.json').write_text(json.dumps({'experiment_id':out.name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'hardware':platform.platform(),'runtime_seconds':time.monotonic()-start,'cli_sha256':hashlib.sha256(CLI.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'records':records},indent=2)+'\n')
   print(p,q,seed,solution.x,solution.fun,convergence,flush=True)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(out,flush=True)
if __name__=='__main__':main()
