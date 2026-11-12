from pathlib import Path
import zipfile, shutil,hashlib,json,datetime,sys
R=Path(__file__).resolve().parents[1]
out=R/'local-downloads';out.mkdir(exist_ok=True)
sources=[(Path(r'D:\AIPROJECT\musicForYou\release\MusicForYou-0.6.5-win-x64-setup.exe'),'MusicForYou-0.6.5-win-x64-setup.exe'),(Path(r'D:\AIPROJECT\bokeForYou\release-app\EchoPod-0.1.0-win-x64.exe'),'EchoPod-0.1.0-win-x64.exe'),(Path(r'D:\AIPROJECT\videoForYou\release\VideoForYou-0.1.1-win-x64-setup.exe'),'VideoForYou-0.1.1-win-x64-setup.exe')]
for source,name in sources:
 if not source.exists() and 'bokeForYou' in str(source):source=Path(r'D:\AIPROJECT\bokeForYou\release\EchoPod-0.1.0-win-x64.exe')
 if source.exists() and not (out/name).exists():shutil.copy2(source,out/name)
 if not (out/name).exists():raise SystemExit('Missing actual download: '+name)
with zipfile.ZipFile(out/'digital-human-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 source=R/'local-repositories'/'digital-human'
 for f in source.rglob('*'):
  if f.is_file() and '.git' not in f.relative_to(source).parts:z.write(f,Path('digital-human')/f.relative_to(source))
hashes=[]
for f in sorted(out.iterdir()):
 if f.name=='SHA256SUMS.txt':continue
 hashes.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name)
(out/'SHA256SUMS.txt').write_bytes(('\n'.join(hashes)+'\n').encode('utf-8'))
bundles=R/'local-packages';bundles.mkdir(exist_ok=True)
with zipfile.ZipFile(bundles/'aione1-dist.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in (R/'dist').rglob('*'):
  if f.is_file() and f.relative_to(R/'dist').parts[0] not in {'media','liubao','downloads'}:z.write(f,Path('dist')/f.relative_to(R/'dist'))
if '--with-content' in sys.argv:
 with zipfile.ZipFile(bundles/'aione1-complete-dist.zip','w',zipfile.ZIP_STORED) as z:
  for f in (R/'dist').rglob('*'):
   if f.is_file():z.write(f,Path('dist')/f.relative_to(R/'dist'))
print('Packaged static dist and actual downloads:',len(hashes))
