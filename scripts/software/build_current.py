#!/usr/bin/env python3
"""Build inspected maintained sources with project-local Ubuntu tool dependencies.
No system install. Archives must first be extracted to vendor/toolchain.
"""
import os, subprocess, sys, json, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[2]
tc=root/'vendor/toolchain'; prefix=root/'vendor/local-current'
logs=root/'vendor/build-logs'; logs.mkdir(exist_ok=True)
env=os.environ.copy()
env['PATH']=str(tc/'usr/bin')+os.pathsep+env['PATH']
libdirs=[tc/'usr/lib/x86_64-linux-gnu/openblas-pthread',tc/'usr/lib/x86_64-linux-gnu',prefix/'lib']
env['LD_LIBRARY_PATH']=os.pathsep.join(map(str,libdirs))
env['PERL5LIB']=os.pathsep.join(str(tc/'usr/share'/p) for p in ['autoconf','automake-1.16'])
env['autom4te_perllibdir']=str(tc/'usr/share/autoconf')
env['AC_MACRODIR']=str(tc/'usr/share/autoconf')
env['trailer_m4']=str(tc/'usr/share/autoconf/autoconf/trailer.m4')
env['AUTOMAKE_LIBDIR']=str(tc/'usr/share/automake-1.16')
env['ACLOCAL_AUTOMAKE_DIR']=str(tc/'usr/share/aclocal-1.16')
env['ACLOCAL_PATH']=str(tc/'usr/share/aclocal')
# Ubuntu separates libtool m4 and auxiliary data; relocate its installed defaults.
relocated_libtool=logs/'libtoolize-relocated'
relocated_libtool.write_text((tc/'usr/bin/libtoolize').read_text().replace('"/usr/share/', '"'+str(tc)+'/usr/share/'))
relocated_libtool.chmod(0o755)
for key,prog in {'AUTOCONF':'autoconf','AUTOHEADER':'autoheader','AUTOM4TE':'autom4te','AUTOMAKE':'automake-1.16','ACLOCAL':'aclocal-1.16','LIBTOOLIZE':'libtoolize','M4':'m4','PKG_CONFIG':'pkgconf'}.items():env[key]=str(tc/'usr/bin'/prog)
cfg=logs/'autom4te-relocated.cfg';cfg.write_text((tc/'usr/share/autoconf/autom4te.cfg').read_text().replace('/usr/share/autoconf',str(tc/'usr/share/autoconf')))
env['AUTOM4TE_CFG']=str(cfg)
env['LIBTOOLIZE']=str(relocated_libtool)
env['PKG_CONFIG_PATH']=str(root/'vendor/local/lib/pkgconfig')
incs=[prefix/'include',tc/'usr/include',tc/'usr/include/x86_64-linux-gnu/openblas-pthread']
for dep in ['libplcurve-10.1.0','gsl-2.8','argtable2-13']:
 incs.append(root/'vendor/deps'/dep/'build/include');libdirs.append(root/'vendor/deps'/dep/'build/lib')
env['CPPFLAGS']=' '.join('-I'+str(p) for p in incs)
env['LDFLAGS']=' '.join('-L'+str(p) for p in libdirs)+' '+' '.join('-Wl,-rpath,'+str(p) for p in libdirs[:3])
env['LIBS']='-llapacke -lopenblas -lgsl -lgslcblas -lm'
env['CC']='gcc';env['CFLAGS']='-O2 -g'
env['FC']=env['F77']=str(root/'scripts/software/gfortran-local')
env['OPENBLAS_NUM_THREADS']='1'
name=sys.argv[1]
if name not in ['tsnnls','ridgerunner']:raise SystemExit('expected tsnnls or ridgerunner')
source=root/'vendor'/name
if name == 'tsnnls':
 # Upstream /bin/sh tests use Bash-only ==; dash selects the wrong CLI branch.
 # Fix syntax only: preserve every solver, reference vector, and tolerance.
 for testfile in [source/'tsnnls/testfull', *sorted((source/'tsnnls').glob('sp_test*.sh')), source/'tsnnls/rrtest.sh']:
  original=testfile.read_text()
  testfile.write_text(original.replace('test $argtable == 1', 'test "${argtable:-0}" = 1'))
for helper in ['config.guess','config.sub']:
 if not (source/helper).is_file():shutil.copy2(root/'vendor/deps/libplcurve-10.1.0'/helper,source/helper)
steps=[('autogen',['sh','autogen.sh']),('configure',['./configure','--prefix='+str(prefix),'--disable-shared']),('make',['make','-j4']),('check',['make','check']),('install',['make','install'])]
(logs/(name+'-environment.json')).write_text(json.dumps({k:env[k] for k in ['CPPFLAGS','LDFLAGS','LIBS','CC','CFLAGS','FC','PKG_CONFIG_PATH']},indent=2))
for stage,cmd in steps:
 path=logs/(name+'-'+stage+'.log')
 with path.open('w') as f: result=subprocess.run(cmd,cwd=source,env=env,stdout=f,stderr=subprocess.STDOUT)
 print(name,stage,'exit',result.returncode,flush=True)
 if result.returncode:
  print(path.read_text()[-6000:]);raise SystemExit(result.returncode)
