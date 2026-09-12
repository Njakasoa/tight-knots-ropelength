"""Independent exact-Fraction witness spot check; full index coverage checked.
Does not replace the complete independent replay of every inequality.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,numpy as np
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'results/topology_path_20260912T230219109163Z'
def read(p):
 t=[]
 for line in p.read_text().splitlines():t.extend(line.split('#',1)[0].split())
 assert t.pop(0)=='VECT';m,n,c=map(int,t[:3]);counts=list(map(int,t[3:3+m]));assert counts==[-48]*12 and n==576
 start=3+2*m;v=[[F(t[start+3*i+j]) for j in range(3)] for i in range(n)];return v
def prod(n,p):return sum((x*y for x,y in zip(n,p)),F(0))
def minus(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
nxt=lambda i:48*(i//48)+(i+1)%48
prev=lambda i:48*(i//48)+(i-1)%48
expected={(i,j) for i in range(576) for j in range(i+1,576) if not (i//48==j//48 and (nxt(i)==j or nxt(j)==i))}
rows=[]
for p in sorted(DIR.glob('seed*.json')):
 j=json.loads(p.read_text());a=read(ROOT/j['initial']);b=read(ROOT/j['final']);s=F(j['alignment']['scale']);q=list(map(F,j['alignment']['translation']));assert s>0;a=[[s*x+y for x,y in zip(v,q)] for v in a]
 z=np.load(p.with_suffix('.npz'),allow_pickle=False);pairs=z['pairs'];corners=z['corners'];assert np.all(pairs[:,:4]==np.floor(pairs[:,:4]));assert np.all(corners[:,:3]==np.floor(corners[:,:3]));assert np.all(pairs[:,2:4]==0) and np.all(corners[:,1:3]==0)
 assert len(pairs)==len(expected) and set(map(tuple,pairs[:,:2].astype(int)))==expected
 assert len(corners)==576 and set(corners[:,0].astype(int))==set(range(576))
 margins=[]
 for row in pairs[np.linspace(0,len(pairs)-1,97,dtype=int)]:
  i,k=map(int,row[:2]);n=list(map(F,row[4:]));left=[prod(n,ps[v]) for ps in [a,b] for v in [i,nxt(i)]];right=[prod(n,ps[v]) for ps in [a,b] for v in [k,nxt(k)]];gap=max(min(left)-max(right),min(right)-max(left));assert gap>0;margins.append(float(gap))
 corner_min=[]
 mid=[[(x+y)/2 for x,y in zip(v,w)] for v,w in zip(a,b)]
 for row in corners[np.linspace(0,575,41,dtype=int)]:
  k=int(row[0]);n=list(map(F,row[3:]));vals=[prod(n,cross(minus(ps[k],ps[prev(k)]),minus(ps[nxt(k)],ps[k]))) for ps in [a,mid,b]];coefs=[vals[0],2*vals[1]-(vals[0]+vals[2])/2,vals[2]];assert min(coefs)>0;corner_min.append(float(min(coefs)))
 rows.append({'seed':j['seed'],'full_exact_index_coverage':True,'pair_exact_fraction_spotchecks':97,'corner_exact_fraction_spotchecks':41,'minimum_spotcheck_axis_gap':min(margins),'minimum_spotcheck_Bernstein_coefficient':min(corner_min)})
result={'status':'PASS','scope':'complete witness index coverage and deterministic exact-Fraction inequality spot checks; not full replay','records':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
