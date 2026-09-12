"""Reproduce local publication evidence without network access or overwrite.

Default: verify pinned rational certificates, rerun the shell certificate, draw
the figure. --full adds the complete test suite, boundary certificate, finite
block search and replay of the three endpoint topology certificates. Requires the lab repository and its pinned Python environment.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');p.add_argument('--check-only',action='store_true');args=p.parse_args()
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
 out=ROOT/'results'/('publication_reproduction_'+stamp);out.mkdir()
 commands=[[sys.executable,'publication/checkers/check_endpoints.py']]
 if not args.check_only:
  commands.extend([[sys.executable,'experiments/certify_shell_bound.py','--N','512','--M','1024','--output-dir',str(out/'shell_certificate')],[sys.executable,'publication/figures/make_figures.py','--output-dir',str(out/'figures')]])
 if args.full:
  commands.extend([[sys.executable,'-m','pytest','-q'],[sys.executable,'experiments/certify_block_boundary.py'],[sys.executable,'experiments/discover_block_sizes.py'],[sys.executable,'experiments/certify_refinement_topology.py','results/variable_pitch_20260912T224501767133Z','--verify','results/topology_path_20260912T231158562188Z']])
 records=[]
 for i,cmd in enumerate(commands):
  result=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
  (out/f'step_{i:02d}.log').write_text(result.stdout+'\n'+result.stderr)
  records.append({'command':cmd,'returncode':result.returncode})
  if result.returncode:break
 files=[Path(__file__),ROOT/'publication/main.tex',ROOT/'publication/checkers/check_endpoints.py',ROOT/'publication/figures/make_figures.py']
 record={'commands':records,'success':all(r['returncode']==0 for r in records),'utc':stamp,'source_hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
 (out/'reproduction.json').write_text(json.dumps(record,indent=2)+'\n');print(out);print('success',record['success']);return 0 if record['success'] else 1
if __name__=='__main__':raise SystemExit(main())
