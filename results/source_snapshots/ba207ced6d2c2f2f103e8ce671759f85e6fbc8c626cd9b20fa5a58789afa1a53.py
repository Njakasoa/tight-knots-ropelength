"""Certify analytic sampling and explicit PL isotopies for the three M2 outputs.

Arb checks all inequalities. Floating computations propose separating axes only;
each axis is then interpreted as an exact binary rational. Stored NPZ witnesses
can be replayed with --verify without optimization or trusting recorded PASS.
This certifies link type, not smooth reach or the actual Ridgerunner trajectory.
"""
from pathlib import Path
from fractions import Fraction
import argparse,datetime,hashlib,json,sys,time
import numpy as np
from flint import arb,ctx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.certification.arb_backend import arb_record

def A(value):
    f=Fraction(float(value)) if isinstance(value,(float,np.floating)) else Fraction(value)
    return arb(f.numerator)/arb(f.denominator)
def dot(x,y):return sum((a*b for a,b in zip(x,y)),arb(0))
def sub(x,y):return [a-b for a,b in zip(x,y)]
def add(x,y):return [a+b for a,b in zip(x,y)]
def scale(x,s):return [a*s for a in x]
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def parse_vect(path):
    tokens=[]
    for line in path.read_text().splitlines():tokens+=line.split('#',1)[0].split()
    assert tokens[0]=='VECT';m,v,colors=map(int,tokens[1:4]);counts=list(map(int,tokens[4:4+m]));assert all(n<0 for n in counts) and sum(-n for n in counts)==v
    cc=list(map(int,tokens[4+m:4+2*m]));assert min(cc)>=0 and sum(cc)==colors
    raw=tokens[4+2*m:4+2*m+3*v];assert len(raw)==3*v
    points=[[A(raw[3*i+j]) for j in range(3)] for i in range(v)]
    floats=np.array([[float(raw[3*i+j]) for j in range(3)] for i in range(v)])
    return points,floats,[-n for n in counts]

def sampling_proof(points,counts,parameters):
    assert counts==[48]*12
    R,ri,beta0,beta1,offset,zs=map(A,parameters)
    radii=[ri,A(2)];betas=[beta0,beta1];offsets=[A(0),offset];populations=[2,3]
    assert R>4 and 0<ri<2 and zs>0
    eps=A('0.0000000001');du=2*arb.pi()/48;bounds=[];max_vertex_error=arb(0)
    # Explicit component order is core, inner strands, outer strands, repeated.
    specs=[(A(0),A(0),A(0))]
    for r,beta,off,N in zip(radii,betas,offsets,populations):
        specs += [(r,beta,2*arb.pi()*j/N+off) for j in range(N)]
    for ci in range(12):
        r,beta,phi=specs[ci%6];L=1+abs(beta);h=R-r
        B=R+r+2*r*L+r*(L*L+abs(beta))
        eta=B*du*du/8+eps
        assert h>eta
        transverse=eta+r*L*eta/(h-eta)
        drift=eps/(h-eps)
        assert du-2*drift>0 and du+2*drift<arb.pi()
        for k in range(48):
            xyz=[points[ci*48+k][0],points[ci*48+k][1],points[ci*48+k][2]/zs]
            if ci>=6:xyz=[xyz[0]-R,xyz[2],-xyz[1]]
            u=du*k;theta=u+beta*u.sin()-phi
            expected=[(R+r*theta.cos())*u.cos(),(R+r*theta.cos())*u.sin(),r*theta.sin()]
            diff=sub(xyz,expected);err=dot(diff,diff)
            assert err<eps*eps, f'vertex mismatch component{ci} sample{k}'
            if err.upper()>max_vertex_error:max_vertex_error=err.upper()
        bounds.append(transverse.upper())
    emax=max(bounds);separations=[ri,A(2),A(2)-ri,2*ri*(arb.pi()/2).sin(),4*(arb.pi()/3).sin()]
    assert all(sep>2*emax for sep in separations)
    assert R>2*(2+emax)
    return {'status':'PASS','vertex_error_allowance':arb_record(eps),'maximum_squared_vertex_error_upper':arb_record(max_vertex_error),'maximum_transverse_error_upper':arb_record(emax),'double_tube_gap_lower':arb_record(R-2*(2+emax)),'sampling_count':48,'component_count':12,'parameter_semantics':'JSON numbers decoded as binary64, then interpreted as exact rationals; mathematical pi in analytic curves','proof':'proofs/REFINEMENT_TOPOLOGY_CERTIFICATE.md'}

class PathCheck:
    def __init__(self,initial,final,counts,alignment):
        self.counts=counts;self.n=len(initial);s=A(alignment['scale']);shift=list(map(A,alignment['translation']));assert s>0
        self.start=[add(scale(p,s),shift) for p in initial];self.end=final
        self.cache={(0,1):self.start,(1,1):self.end};self.next=[];self.previous=[];self.component=[];base=0
        for ci,n in enumerate(counts):
            self.next += [base+(i+1)%n for i in range(n)];self.previous += [base+(i-1)%n for i in range(n)];self.component += [ci]*n;base+=n
        self.next=np.array(self.next);self.previous=np.array(self.previous)
        self.start_float=np.array([[float(v) for v in p] for p in self.start]);self.end_float=np.array([[float(v) for v in p] for p in self.end])
        self.required=[(i,j) for i in range(self.n) for j in range(i+1,self.n) if not (self.component[i]==self.component[j] and (self.next[i]==j or self.next[j]==i))]
    def positions(self,num,depth):
        t=Fraction(int(num),2**int(depth));key=(t.numerator,t.denominator)
        if key not in self.cache:
            q=A(t);self.cache[key]=[add(scale(x,1-q),scale(y,q)) for x,y in zip(self.start,self.end)]
        return self.cache[key]
    def pair(self,i,j,num,depth,axis):
        n=list(map(A,axis));left=self.positions(num,depth);right=self.positions(num+1,depth)
        pa=[dot(n,pos[k]) for pos in (left,right) for k in (i,self.next[i])]
        pb=[dot(n,pos[k]) for pos in (left,right) for k in (j,self.next[j])]
        # All points in a moving segment project inside these corner extrema.
        alo=min(v.lower() for v in pa);ahi=max(v.upper() for v in pa);blo=min(v.lower() for v in pb);bhi=max(v.upper() for v in pb)
        return bool(alo>bhi or blo>ahi)
    def corner(self,k,num,depth,axis):
        n=list(map(A,axis));values=[]
        for q,d in [(num,depth),(2*num+1,depth+1),(num+1,depth)]:
            pos=self.positions(q,d);incoming=sub(pos[k],pos[self.previous[k]]);outgoing=sub(pos[self.next[k]],pos[k]);values.append(dot(n,cross(incoming,outgoing)))
        f0,fm,f1=values;b1=2*fm-(f0+f1)/2
        return bool(f0>0 and b1>0 and f1>0)
    def floats(self,num,depth):
        t=(num+.5)/2**depth;return (1-t)*self.start_float+t*self.end_float

def propose_axes(a0,a1,b0,b1):
    u=a1-a0;v=b1-b0;w=a0-b0
    aa=np.einsum('ij,ij->i',u,u);bb=np.einsum('ij,ij->i',u,v);cc=np.einsum('ij,ij->i',v,v);dd=np.einsum('ij,ij->i',u,w);ee=np.einsum('ij,ij->i',v,w)
    den=aa*cc-bb*bb
    with np.errstate(divide='ignore',invalid='ignore'):
        ss=(bb*ee-cc*dd)/den;tt=(aa*ee-bb*dd)/den
        candidates=[(np.zeros(len(u)),np.clip(ee/cc,0,1)),(np.ones(len(u)),np.clip((ee+bb)/cc,0,1)),(np.clip(-dd/aa,0,1),np.zeros(len(u))),(np.clip((bb-dd)/aa,0,1),np.ones(len(u))),(ss,tt)]
    vectors=np.stack([w+s[:,None]*u-t[:,None]*v for s,t in candidates]);dists=np.einsum('kij,kij->ki',vectors,vectors)
    good=(den>0)&(ss>=0)&(ss<=1)&(tt>=0)&(tt<=1);dists[-1,~good]=np.inf
    return vectors[np.argmin(dists,axis=0),np.arange(len(u))]

def certify_path(check):
    pair_rows=[];tasks=[(i,j,0,0) for i,j in check.required]
    while tasks:
        # Group equal time cells to reuse approximate and exact positions.
        groups={}
        for i,j,num,depth in tasks:groups.setdefault((num,depth),[]).append((i,j))
        tasks=[]
        for (num,depth),pairs in groups.items():
            arr=np.array(pairs,dtype=int);pos=check.floats(num,depth);i,j=arr[:,0],arr[:,1]
            axes=propose_axes(pos[i],pos[check.next[i]],pos[j],pos[check.next[j]])
            for (ii,jj),axis in zip(pairs,axes):
                if np.all(np.isfinite(axis)) and check.pair(ii,jj,num,depth,axis):pair_rows.append([ii,jj,num,depth,*axis])
                elif depth<14:tasks.extend([(ii,jj,2*num,depth+1),(ii,jj,2*num+1,depth+1)])
                else:raise ArithmeticError(f'uncertified edge pair {ii},{jj} at depth{depth}')
    corner_rows=[];tasks=[(k,0,0) for k in range(check.n)]
    while tasks:
        k,num,depth=tasks.pop();pos=check.floats(num,depth);axis=np.cross(pos[k]-pos[check.previous[k]],pos[check.next[k]]-pos[k])
        if check.corner(k,num,depth,axis):corner_rows.append([k,num,depth,*axis])
        elif depth<14:tasks.extend([(k,2*num,depth+1),(k,2*num+1,depth+1)])
        else:raise ArithmeticError(f'uncertified adjacent corner{k}')
    return np.array(pair_rows),np.array(corner_rows)

def coverage(rows,required,key_columns):
    intervals={}
    for row in rows:
        assert all(float(x).is_integer() for x in row[:key_columns+2]), "noninteger witness index"
        key=tuple(int(x) for x in row[:key_columns]);num,depth=map(int,row[key_columns:key_columns+2]);assert 0<=depth<=14 and 0<=num<2**depth
        intervals.setdefault(key,[]).append((Fraction(num,2**depth),Fraction(num+1,2**depth)))
    assert set(intervals)==set(required), 'pair/corner coverage mismatch'
    for cells in intervals.values():
        previous=Fraction(0)
        for lo,hi in sorted(cells):assert lo==previous,'time gap/overlap';previous=hi
        assert previous==1

def replay(check,pairs,corners):
    coverage(pairs,check.required,2);coverage(corners,[(k,) for k in range(check.n)],1)
    for row in pairs:
        i,j,num,depth=map(int,row[:4]);assert check.pair(i,j,num,depth,row[4:]),'pair witness failed'
    for row in corners:
        k,num,depth=map(int,row[:3]);assert check.corner(k,num,depth,row[3:]),'corner witness failed'

def run_record(source,run,out,verify=None):
    initial=source/run['initial'];final=source/run['final'];a,af,counts=parse_vect(initial);b,bf,counts_b=parse_vect(final);assert counts==counts_b
    sample=sampling_proof(a,counts,run['parameters'])
    if verify:
        cert=json.loads(verify.read_text());assert digest(initial)==cert['initial_sha256'] and digest(final)==cert['final_sha256'];alignment=cert['alignment'];witness=verify.with_suffix('.npz');assert digest(witness)==cert['witness_sha256'];z=np.load(witness,allow_pickle=False);check=PathCheck(a,b,counts,alignment);replay(check,z['pairs'],z['corners']);return {'seed':run['seed'],'status':'REPLAY_PASS'}
    ac=af-af.mean(0);bc=bf-bf.mean(0);s=float((ac*bc).sum()/(ac*ac).sum());alignment={'scale':s,'translation':(bf.mean(0)-s*af.mean(0)).tolist(),'semantics':'positive homothety and translation; coefficients are exact binary64 rationals'}
    check=PathCheck(a,b,counts,alignment);pairs,corners=certify_path(check);coverage(pairs,check.required,2);coverage(corners,[(k,) for k in range(check.n)],1)
    witness=out/f'seed{run["seed"]}.npz';np.savez_compressed(witness,pairs=pairs,corners=corners)
    cert={'seed':run['seed'],'status':'PASS','initial':str(initial.relative_to(ROOT)),'final':str(final.relative_to(ROOT)),'initial_sha256':digest(initial),'final_sha256':digest(final),'parameters':run['parameters'],'alignment':alignment,'sampling_certificate':sample,'edge_pairs_required':len(check.required),'pair_time_cells':len(pairs),'corner_time_cells':len(corners),'maximum_pair_subdivision_depth':int(pairs[:,3].max()),'witness_sha256':digest(witness),'witness_semantics':'float64 entries; indices/time exponents exact integers, axes interpreted as exact binary rationals','precision_bits':ctx.prec,'script_sha256':digest(Path(__file__)),'claim':'Stored initial and final closed polygons have the analytic full-twist type T(12,12), up to common mirror. Certificate follows an explicit alternative isotopy, not the actual Ridgerunner trajectory. No smooth reach or ropelength bound.'}
    (out/f'seed{run["seed"]}.json').write_text(json.dumps(cert,indent=2)+'\n');return cert

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--seeds',nargs='+',type=int);p.add_argument('--verify',type=Path);args=p.parse_args();ctx.prec=192
    source=args.source.resolve();search=json.loads((source/'search.json').read_text());start=time.monotonic()
    available={r['seed'] for r in search['records']}
    if not available or (args.seeds is not None and (not args.seeds or not set(args.seeds)<=available)):
        raise ValueError('requested seed set must be nonempty and contained in the source search')
    out=args.verify.resolve() if args.verify else ROOT/'results'/('topology_path_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    if not args.verify:out.mkdir()
    records=[]
    for run in search['records']:
        if args.seeds and run['seed'] not in args.seeds:continue
        record=run_record(source,run,out,out/f'seed{run["seed"]}.json' if args.verify else None);records.append(record);print(run['seed'],record['status'],flush=True)
    assert records, 'cannot certify an empty result set'
    summary={'status':'PASS','records':[{'seed':r['seed'],'status':r['status']} for r in records],'runtime_seconds':time.monotonic()-start,'source_search':str(source.relative_to(ROOT)),'source_search_sha256':digest(source/'search.json'),'script_sha256':digest(Path(__file__))}
    if not args.verify:(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(out,summary['runtime_seconds'],flush=True)
if __name__=='__main__':main()
