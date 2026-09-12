"""Build a source-labelled small-knot numerical atlas from pinned coordinates."""
from pathlib import Path
import csv,datetime,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.curves import read_vect
CLI=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
def main():
 out=ROOT/'results'/('small_atlas_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir();rows=[]
 search=json.loads((ROOT/'results/torus_search_20260912T214900Z/search.json').read_text())
 mapping={'3_1':[2,3],'5_1':[2,5],'8_19':[3,4]}
 for path in sorted((ROOT/'data/reference/cantarella-atlas/knots/prime/3-10').glob('*.vect')):
  knot=path.stem;curve=read_vect(path);vals=[r['resolution_checks'][-1]['polygon_ropelength'] for r in search['records'] if r['torus_type']==mapping.get(knot)]
  if knot=='3_1':vals+=[32.74879268133495,33.14901731963343]
  rows.append({'knot':knot,'crossing_number':int(knot.split('_')[0]),'source_polygon_ropelength':float(subprocess.check_output([str(CLI),'-q',str(path)],text=True)),'our_numeric_refinement_or_family_value':min(vals) if vals else None,'known_smooth_lower_radius':31.32,'lower_source':'Denne-Diao-Sullivan: nontrivial knot lower (diameter15.66 converted to radius31.32)','best_known_smooth_upper':'not established by this coordinate-only extraction','our_certified_smooth_upper':None,'vertices':sum(c.vertex_count for c in curve.components),'contact_graph':'not extracted for this atlas row; separate accepted controls retain contacts','symmetry':'not certified','local_minima_status':'pinned source configuration; no global assertion','coordinate_source':str(path.relative_to(ROOT)),'coordinate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'type_status':'source-labelled; broad knot identification of all rows not independently certified','normalization':'radius; numerical Rawdon polygon thickness'})
 (out/'atlas.json').write_text(json.dumps(rows,indent=2)+'\n')
 with (out/'atlas.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'manifest.json').write_text(json.dumps({'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cli_sha256':hashlib.sha256(CLI.read_bytes()).hexdigest(),'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()},'scope':'coordinate atlas, incomplete contact/type/record audit; polygon estimates are not certified smooth upper bounds'},indent=2)+'\n');print(out)
if __name__=='__main__':main()
