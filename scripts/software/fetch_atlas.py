"""Download a small, commit-pinned subset of Cantarella's public CC0 atlas."""
import base64, datetime, hashlib, json, time, urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=root/'data/reference/cantarella-atlas'; out.mkdir(exist_ok=True)
def fetch(url):
 for attempt in range(5):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'TightKnotsLab-reproducibility'}),timeout=60) as r:return r.read()
  except Exception:
   if attempt==4:raise
   time.sleep(2**attempt)
repo='designbynumbers/ropelength-minimizing-knots'
manifest=out/'MANIFEST.json'
if manifest.exists():m=json.loads(manifest.read_text())
else:
 sha=json.loads(fetch('https://api.github.com/repos/'+repo+'/commits/main'))['sha']
 m={'repository':'https://github.com/'+repo,'commit':sha,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
 manifest.write_text(json.dumps(m,indent=2)+'\n')
paths=['README.md','LICENSE.txt']+['knots/prime/3-10/'+name+'.tsv' for name in ['3_1','4_1','5_1','6_1','8_19','10_124']]+['links/prime/2-9/2_2_1.tsv']
for path in paths:
 target=out/path;target.parent.mkdir(parents=True,exist_ok=True)
 url='https://raw.githubusercontent.com/'+repo+'/'+m['commit']+'/'+path
 if not target.exists():
  payload=json.loads(fetch('https://api.github.com/repos/'+repo+'/contents/'+path+'?ref='+m['commit']))
  target.write_bytes(base64.b64decode(payload['content']))
 entry={'path':path,'url':url,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 m['files']=[e for e in m['files'] if e['path']!=path]+[entry]
 manifest.write_text(json.dumps(m,indent=2)+'\n'); print(path,entry['bytes'],flush=True)
records=[]
for path in sorted(out.rglob('*.tsv')):
 components=[part.splitlines() for part in path.read_text().strip().split('\n\n')]
 components=[[line.strip() for line in part if line.strip()] for part in components]
 target=path.with_suffix('.vect')
 lines=['VECT',f'{len(components)} {sum(map(len,components))} 0',' '.join(str(-len(c)) for c in components),' '.join('0' for c in components)]
 for component in components:lines.extend(component)
 target.write_text('\n'.join(lines)+'\n')
 records.append({'input':str(path.relative_to(root)),'output':str(target.relative_to(root)),'components':len(components),'vertices':list(map(len,components)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(out/'VECT_CONVERSION.json').write_text(json.dumps(records,indent=2)+'\n')
