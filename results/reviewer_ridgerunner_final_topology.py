"""Check actual Ridgerunner final coordinates using independent tester helpers."""
import importlib.util,sys,json,hashlib
from pathlib import Path
p=Path('tests/independent/test_independent_validation.py')
spec=importlib.util.spec_from_file_location('reviewer_independent_helper',p)
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
spec.loader.exec_module(module)
out={}
for label in ['trefoil47','trefoil400']:
 path=Path(f'results/ridgerunner_autoscaled_20260913/{label}.rr/{label}.final.vect')
 raw=module._raw_vect(path)
 projection=module._generic_projection(raw.components,raw.closed,target_crossings=3)
 det=module._independent_diagram_determinant(projection['crossings'])
 out[label]={'input':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'crossing_count':projection['crossing_count'],'depth_gap_min':projection['depth_gap_min'],'view':projection['view'],'determinant':det,'passed':det==3}
out['helper_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
Path('results/reviewer_ridgerunner_final_topology.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
