"""Reproduce the two autoscaled Ridgerunner controls in a fresh output directory."""
import datetime, hashlib, json, platform, re, shutil, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def collect(out,commands):
 cli=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
 records=[]
 for label,command in commands.items():
  initial=out/(label+'.vect');final=out/(label+'.rr')/(label+'.final.vect')
  logfile=out/(label+'.run.log');text=logfile.read_text()
  metrics={role:float(subprocess.check_output([str(cli),'-q',str(path)],text=True).strip()) for role,path in [('initial',initial),('final',final)]}
  records.append({'label':label,'command':command,'seed_logged':re.search(r'with seed ([-\d]+)',text).group(1),'seed_policy':'upstream seeds from OS; no CLI override; no mangling requested','ropelength_polygonal':metrics,'final_geometry':str(final.relative_to(out)),'final_sha256':digest(final),'status':'bounded numerical refinement, not global optimum','normalization':'length / polygonal thickness (rope radius)','knot_type_status':'input source plus independent geometry checks required'})
 manifest={'experiment_id':out.name,'utc_recorded':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'hardware':platform.platform(),'optimizer':'Ridgerunner 2.3.1 / tsnnls2.5.1','records':records,'files':{str(p.relative_to(out)):digest(p) for p in out.rglob('*') if p.is_file() and p.name!='manifest.json'}}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return manifest
def main():
 out=ROOT/'results'/('ridgerunner_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));out.mkdir()
 commands={}
 for label,source,steps in [('trefoil47','trefoil_3.1_ridgerunner.vect',5000),('trefoil400','trefoil_3.1_plcurve_kl400.vect',1000)]:
  shutil.copy2(ROOT/'data/reference'/source,out/(label+'.vect'))
  command=[str(ROOT/'scripts/software/ridgerunner-local'),label+'.vect','-a','-s',str(steps),'--StopTime=2','--NoPNGOutput','--NoOutputFiles','--NoLsqrLog']
  commands[label]=command
  with (out/(label+'.run.log')).open('w') as f:subprocess.run(command,cwd=out,stdout=f,stderr=subprocess.STDOUT,check=True)
 collect(out,commands);print(out)
if __name__=='__main__':main()
