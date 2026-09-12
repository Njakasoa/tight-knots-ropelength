"""Recompute the smallest supplied 2026 link and extract its numerical contacts."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.curves import read_vect
from src.thickness import polygon_thickness
from src.contacts import extract_contacts
from src.topology import linking_matrix
def main():
 source=ROOT/'data/reference/aae862esupp1/T44.vect'
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 out=ROOT/'results'/('recent_T44_'+stamp);out.mkdir()
 start=time.monotonic();link=read_vect(source)
 thi=polygon_thickness(link)
 graph=extract_contacts(link,thickness_result=thi,tolerance=1e-4)
 cli=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
 cli_value=float(subprocess.check_output([str(cli),'-q',str(source)],text=True))
 record={'experiment_id':out.name,'utc':stamp,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'input':str(source.relative_to(ROOT)),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source':'Klotz2026 DOI10.1088/1751-8121/ae862e supplement','vertices':[c.vertex_count for c in link.components],'length':thi.length,'thickness_polygonal':thi.thickness,'ropelength_polygonal':thi.ropelength,'plcurve_ropelength':cli_value,'linking_matrix_projected':linking_matrix(link).tolist(),'contact_graph':graph.as_dict(),'runtime_seconds':time.monotonic()-start,'claim_boundary':'numerical reproduction and finite contact graph; pairwise linking does not completely identify the link; no smooth/global certificate'}
 (out/'inspection.json').write_text(json.dumps(record,indent=2)+'\n')
 source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*.py'))}
 (out/'manifest.json').write_text(json.dumps({'inspection_sha256':hashlib.sha256((out/'inspection.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_hashes':source_hashes,'cli_sha256':hashlib.sha256(cli.read_bytes()).hexdigest()},indent=2)+'\n')
 print(out,thi.ropelength,cli_value,'contacts',graph.contact_count,flush=True)
if __name__=='__main__':main()
