"""Upload allowlisted media/cover files in bounded parallel archives; no application settings."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import tarfile,subprocess,argparse,json,hashlib
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--key',required=True);a=p.parse_args()
media=R/'dist'/'media';parts=R/'local-media-upload';parts.mkdir(exist_ok=True)
files=sorted([f for f in media.rglob('*') if f.is_file()],key=lambda f:f.stat().st_size,reverse=True)
bins=[[] for _ in range(4)];sizes=[0]*4
for f in files:
 index=sizes.index(min(sizes));bins[index].append(f);sizes[index]+=f.stat().st_size
archives=[]
for i,group in enumerate(bins):
 path=parts/('media-part-'+str(i)+'.tar')
 with tarfile.open(path,'w') as tar:
  for f in group:tar.add(f,arcname=f.relative_to(media))
 archives.append(path)
print('Uploading',len(files),'media/cover files;',round(sum(sizes)/1e6,1),'MB in 4 parts',flush=True)
base=['-i',a.key,'-o','BatchMode=yes','-o','ConnectTimeout=20']
def upload(path):
 subprocess.run(['scp',*base,str(path),'root@8.133.244.26:/tmp/'+path.name],check=True)
 print('Uploaded',path.name,flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:
 for future in as_completed([pool.submit(upload,p) for p in archives]):future.result()
script='set -eu\nmkdir -p /opt/aione1/media\n'
for path in archives:script+='tar -xf /tmp/'+path.name+' -C /opt/aione1/media\n'
script+='ln -sfn /opt/aione1/media /opt/aione1/current/media\n'
script+='find /opt/aione1/media -type f | wc -l\n'
subprocess.run(['ssh',*base,'root@8.133.244.26','bash -s'],input=script.encode(),check=True)
print('MEDIA SYNC COMPLETE',flush=True)
