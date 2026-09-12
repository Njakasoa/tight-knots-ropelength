"""Standalone scientific figure from one immutable T44 contact inspection."""
from pathlib import Path
import collections, hashlib, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.curves import read_vect
def main():
 source=ROOT/'results/recent_T44_20260912T220613Z/inspection.json'
 data=json.loads(source.read_text());link=read_vect(ROOT/data['input'])
 out=ROOT/'geometry/recent_T44_contacts';out.mkdir(parents=True,exist_ok=False)
 fig=plt.figure(figsize=(10,4.5),layout='constrained')
 ax=fig.add_subplot(121,projection='3d')
 palette=['#2563eb','#e87928','#169873','#a855b7']
 for k,c in enumerate(link.components):
  v=np.vstack((c.vertices,c.vertices[0]));ax.plot(*v.T,color=palette[k],lw=3,label=str(k+1))
 allpoints=np.concatenate([c.vertices for c in link.components]);center=allpoints.mean(axis=0);radius=np.ptp(allpoints,axis=0).max()/2
 ax.set(xlim=(center[0]-radius,center[0]+radius),ylim=(center[1]-radius,center[1]+radius),zlim=(center[2]-radius,center[2]+radius))
 ax.set_box_aspect((1,1,1));ax.view_init(elev=26,azim=37);ax.set_axis_off();ax.set_title('Reference T(4,4) — centerlines',loc='left',fontsize=12)
 matrix=np.zeros((4,4),dtype=int)
 for c in data['contact_graph']['contacts']:
  a,b=c['component_a'],c['component_b'];matrix[a,b]+=1
  if a!=b:matrix[b,a]+=1
 bx=fig.add_subplot(122);bx.imshow(matrix,cmap='Blues',vmin=0)
 for (i,j),v in np.ndenumerate(matrix):bx.text(j,i,str(v),ha='center',va='center',color='white' if v>180 else '#172435',fontsize=13)
 bx.set_xticks(range(4),range(1,5));bx.set_yticks(range(4),range(1,5));bx.set_xlabel('Component');bx.set_ylabel('Component');bx.set_title('Contacts by component pair',loc='left',fontsize=12)
 fig.suptitle('Numerical reproduction of Klotz (2026)',x=.05,ha='left',fontsize=16)
 fig.text(.03,.005,'Finite polygon graph · 1,011 contacts · distance tolerance 10⁻⁴ · no continuum multiplicity claim',fontsize=9,color='#526174')
 fig.savefig(out/'contacts.png',dpi=180);fig.savefig(out/'contacts.pdf');plt.close(fig)
 (out/'manifest.json').write_text(json.dumps({'inspection':str(source.relative_to(ROOT)),'inspection_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}},indent=2)+'\n')
 print(out)
if __name__=='__main__':main()
