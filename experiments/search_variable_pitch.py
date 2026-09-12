"""M2 numerical shell-pitch release followed by unrestricted vertex refinement.

The smooth input family has a constructive isotopy. Polygon sampling and the
Ridgerunner path are numerical diagnostics, requiring independent topology
checks. No numerical result here is promoted to a smooth upper certificate.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,platform,re,subprocess,sys,tempfile,time
import numpy as np
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.discovery.grammar import ShellGrammarConfig,build_shell_grammar
from src.curves import write_vect
CLI=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def config(x):
 return ShellGrammarConfig(major_radius=float(x[0]),shell_radii=(float(x[1]),2.),shell_populations=(2,3),phase_offsets=(0.,float(x[4])),pitch_modulations=(float(x[2]),float(x[3])),core_included=True,closure_mode='double_hopf',ambient_axis_scale=(1.,1.,float(x[5])))
def sample(x,n):
 model=build_shell_grammar(config(x));u=np.linspace(0,2*np.pi,n,endpoint=False)
 return [np.asarray(model.evaluate(u,component=k)) for k in range(model.component_count)]
def value(path):return float(subprocess.check_output([str(CLI),'-q',str(path)],text=True).strip())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--seeds',nargs='+',type=int,default=[1729,2718,3141]);parser.add_argument('--iterations',type=int,default=8);parser.add_argument('--rr-steps',type=int,default=300);args=parser.parse_args()
 gate=(ROOT/'benchmarks/M1_REVIEW.md').read_text()
 if 'PASS' not in gate:raise RuntimeError('M1 gate has not passed')
 out=ROOT/'results'/('variable_pitch_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir();start=time.monotonic()
 bounds=[(4.1,8),(.5,1.7),(-.7,.7),(-.7,.7),(0,2*np.pi/3),(.6,1.4)]
 records=[]
 def save():
  artifact={'experiment_id':out.name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'hardware':platform.platform(),'runtime_seconds':time.monotonic()-start,'family':'smooth T(12,12) up to mirror','free_parameters':['major radius','inner shell radius','independent periodic pitch of both shells','relative shell phase','ambient z scale'],'fixed_parameters':{'populations':[2,3],'outer_radius':2,'closure':'double_hopf','core':True,'optimizer_samples_per_component':24},'bounds':bounds,'records':records,'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'src/discovery/grammar.py',CLI]},'claim_boundary':'numerical polygon experiments, not a certified smooth bound; isotopy of underlying analytic inputs follows grammar proof; polygon/solver path needs separate validation'}
  (out/'search.json').write_text(json.dumps(artifact,indent=2)+'\n')
 for seed in args.seeds:
  history=[]
  with tempfile.TemporaryDirectory(prefix='shell-pitch-') as td:
   path=Path(td)/'candidate.vect'
   def objective(x):
    write_vect(path,sample(x,24));val=value(path)
    history.append({'parameters':list(map(float,x)),'polygon_ropelength':val});return val
   baseline=objective([6,1,0,0,0,1])
   solution=differential_evolution(objective,bounds,seed=seed,maxiter=args.iterations,popsize=4,tol=1e-5,polish=False,workers=1)
  label=f'seed{seed}';initial=out/(label+'.vect');write_vect(initial,sample(solution.x,48),overwrite=False)
  fine=out/(label+'.96.vect');write_vect(fine,sample(solution.x,96),overwrite=False)
  command=[str(ROOT/'scripts/software/ridgerunner-local'),initial.name,'-a','-s',str(args.rr_steps),'--StopTime=1','--NoPNGOutput','--NoOutputFiles','--NoLsqrLog']
  with (out/(label+'.run.log')).open('w') as log:
   result=subprocess.run(command,cwd=out,stdout=log,stderr=subprocess.STDOUT)
  final=out/(label+'.rr')/(label+'.final.vect')
  logtext=(out/(label+'.run.log')).read_text();seedmatch=re.search(r'with seed ([-\d]+)',logtext)
  record={'seed':seed,'baseline_coarse':baseline,'parameters':solution.x.tolist(),'coarse_ropelength':float(solution.fun),'at48':value(initial),'at96':value(fine),'termination':str(solution.message),'optimizer':'DE popsize4, no polish','iterations':args.iterations,'trials':history,'initial':initial.name,'fine_analytic_sample':fine.name,'ridgerunner_command':command,'ridgerunner_returncode':result.returncode,'ridgerunner_seed':seedmatch.group(1) if seedmatch else None,'ridgerunner_seed_policy':'upstream OS seed; no mangling requested','final':str(final.relative_to(out)) if final.exists() else None,'final_ropelength':value(final) if final.exists() else None,'initial_sha256':sha(initial),'final_sha256':sha(final) if final.exists() else None}
  records.append(record);save();print(label,'initial',record['at48'],'final',record['final_ropelength'],'parameters',solution.x,flush=True)
 (out/'manifest.json').write_text(json.dumps({str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='manifest.json'},indent=2)+'\n');print(out,flush=True)
if __name__=='__main__':main()
