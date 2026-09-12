"""Compare finite component-contact graphs of preserved multistart outcomes.

Permutation-invariant weighted graph spectra support exploratory clustering;
no continuum contact topology or physical phase transition is inferred.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys,time
import numpy as np
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.spatial.distance import pdist,squareform
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.curves import read_vect
from src.thickness import polygon_thickness
from src.contacts import extract_contacts
from src.topology import linking_matrix
CLI=ROOT/'vendor/deps/libplcurve-10.1.0/build/bin/ropelength'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('search_dir',type=Path);args=parser.parse_args();source=args.search_dir.resolve();search=json.loads((source/'search.json').read_text())
 out=ROOT/'results'/('contact_clusters_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir();start=time.monotonic();records=[]
 for run in search['records']:
  if not run['final']:continue
  path=source/run['final'];link=read_vect(path);thi=polygon_thickness(link);m=len(link.components)
  projections=[]
  for direction in [(1.,.371,.813),(.231,1.,.491)]:
   try:matrix=linking_matrix(link,view=direction);projections.append({'direction':direction,'generic':True,'matrix':matrix.tolist(),'all_pair_abs_one':bool(np.allclose(np.abs(matrix-np.diag(np.diag(matrix))),np.ones((m,m))-np.eye(m)))})
   except ValueError as exc:projections.append({'direction':direction,'generic':False,'reason':str(exc)})
  features=[]
  for relative_tol in [1e-4,1e-3]:
   graph=extract_contacts(link,thickness_result=thi,tolerance=relative_tol*thi.thickness)
   weights=np.zeros((m,m))
   for contact in graph.contacts:
    a,b=sorted((contact.component_a,contact.component_b));weights[a,b]+=1
    if a!=b:weights[b,a]+=1
   norm=weights/max(1,np.linalg.norm(weights));spectrum=np.linalg.eigvalsh(norm)
   features.append({'relative_tolerance':relative_tol,'contact_count':len(graph.contacts),'active_kink_count':sum(k.active for k in graph.kinks),'component_weight_matrix':weights.tolist(),'normalized_spectrum':spectrum.tolist()})
   (out/f'seed{run["seed"]}_contacts_tol{relative_tol}.json').write_text(json.dumps(graph.as_dict(),indent=2)+'\n')
  cli=float(subprocess.check_output([str(CLI),'-q',str(path)],text=True));record={'seed':run['seed'],'geometry':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'components':m,'vertices':sum(c.vertex_count for c in link.components),'length':thi.length,'thickness_polygonal':thi.thickness,'ropelength_independent_engine':thi.ropelength,'ropelength_plcurve':cli,'relative_ropelength_difference':abs(cli-thi.ropelength)/cli,'projections':projections,'features':features};records.append(record)
  print('seed',run['seed'],'rope',thi.ropelength,'contacts',[f['contact_count'] for f in features],flush=True)
 clusters=[]
 for i,tol in enumerate([1e-4,1e-3]):
  x=np.asarray([r['features'][i]['normalized_spectrum'] for r in records]);dist=pdist(x)
  labels=fcluster(linkage(dist,method='average'),t=.1,criterion='distance') if len(records)>1 else np.ones(len(records),dtype=int)
  clusters.append({'relative_tolerance':tol,'method':'average linkage of Frobenius-normalized symmetric component-contact spectra','cut_distance':.1,'distance_matrix':squareform(dist).tolist(),'labels':labels.tolist(),'seed_order':[r['seed'] for r in records],'scope':'exploratory finite graph similarity; spectral equality is not graph isomorphism'})
 result={'experiment_id':out.name,'source_search':str(source.relative_to(ROOT)),'source_search_sha256':hashlib.sha256((source/'search.json').read_bytes()).hexdigest(),'runtime_seconds':time.monotonic()-start,'records':records,'clusters':clusters,'claim_boundary':'two projection linking matrices are necessary consistency checks, not complete isotopy certificates; topology of free vertex solver paths remains numerical; no smooth upper bound or continuum phase claim'}
 (out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');(out/'manifest.json').write_text(json.dumps({'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}},indent=2)+'\n');print(out,flush=True)
if __name__=='__main__':main()
