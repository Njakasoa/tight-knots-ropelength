"""Numerically reproduce the two 2026 continuum shell coefficients.

This computes the toroidal length integral rather than multiplying printed
rounded correction factors. It does not certify Klotz's finite epsilon rule.
"""
import datetime, hashlib, json, platform, subprocess, time
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
def main():
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 out=ROOT/'results'/('klotz_limits_'+stamp);out.mkdir()
 start=time.monotonic();records=[]
 for model,density,q0,formula in [('constant_increment',lambda x:4*x,2.,'n(x)=4x; q0=2'),('common_hole_maximum',lambda x:2*np.pi*x/np.sqrt(1+x*x),2*np.pi*(np.sqrt(2)-1),'n(x)=2pi*x/sqrt(1+x^2); q0=2pi*(sqrt2-1)')]:
  values=[]
  for tolerance in [1e-8,1e-11]:
   inner_errors=[]
   def integrand(x):
    length,error=quad(lambda t:np.sqrt((4+2*x*np.cos(t))**2+4*x*x),0,2*np.pi,epsabs=tolerance,epsrel=tolerance)
    inner_errors.append(error)
    return density(x)*length
   l0,error=quad(integrand,0,1,epsabs=tolerance,epsrel=tolerance)
   values.append({'epsabs_epsrel':tolerance,'l0':l0,'outer_error_estimate':error,'max_inner_error_estimate':max(inner_errors),'alpha':l0/(np.sqrt(2)*q0**1.5)})
  records.append({'model':model,'population_density':formula,'q0':q0,'runs':values})
 record={'experiment_id':out.name,'utc':stamp,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source':'Klotz2026 arXiv2603.02416v2 SecIII','formula':'e(x)=integral_0^(2pi) sqrt((4+2x*cos(t))^2+4x^2) dt; alpha=integral(n*e)/(sqrt2*q0^(3/2))','source_pdf_sha256':hashlib.sha256((ROOT/'papers/klotz-2026-v2.pdf').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'runtime_seconds':time.monotonic()-start,'platform':platform.platform(),'scipy':scipy.__version__,'numpy':np.__version__,'status':'numerical quadrature reproduction; error estimates are not rigorous bounds; finite occupancy clearance proof not implied','records':records}
 target=out/'reproduction.json';target.write_text(json.dumps(record,indent=2)+'\n')
 (out/'manifest.json').write_text(json.dumps({'reproduction_sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2)+'\n')
 print(out)
 for r in records:print(r['model'],r['runs'][-1]['alpha'])
if __name__=='__main__':main()
