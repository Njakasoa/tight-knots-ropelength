"""Scientific figure from archived finite search; plotted constants are diagnostic."""
from pathlib import Path
import argparse, json, os
os.environ.setdefault('MPLCONFIGDIR','/tmp/tight-knots-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=Path(__file__).parent);args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
 search=json.loads((ROOT/'results/discovery_blocks_20260912T221841Z/discovery.json').read_text())
 constants=json.loads((ROOT/'results/reviewer003_independent.json').read_text())
 T=np.array([r['T'] for r in search['best']]); b=np.array([r['block_size'] for r in search['best']]);cstar=constants['cstar']
 fig,axes=plt.subplots(1,2,figsize=(10.5,4.1),layout='constrained')
 ax=axes[0];ax.plot(T,b,'o-',label='Exhaustive finite winner',color='#146f86');ax.plot(T,cstar*np.sqrt(T),'--',label=r'$c_*\sqrt{T}$',color='#c16639');ax.set(xscale='log',yscale='log',xlabel='Number of shells T',ylabel='Block size b');ax.legend(frameon=False,fontsize=9);ax.grid(alpha=.15)
 c=np.linspace(.15,1.25,400);beta=constants['alpha2']*(constants['a']/c+constants['d']*c)
 ax=axes[1];ax.plot(c,beta,color='#146f86');ax.scatter([cstar,1],[constants['beta_opt'],constants['beta_one']],color=['#c16639','#555555']);ax.annotate(r'$c_*\approx0.4228$',(cstar,constants['beta_opt']),xytext=(.55,3.7),arrowprops={'arrowstyle':'-','color':'#888888'});ax.set(xlabel='Fixed block multiplier c',ylabel=r'First correction $\beta(c)$',ylim=(3.5,8));ax.grid(alpha=.15)
 for ext in ('pdf','png'):fig.savefig(args.output_dir/f'block_discovery.{ext}',dpi=180)
 plt.close(fig)
if __name__=='__main__':main()
