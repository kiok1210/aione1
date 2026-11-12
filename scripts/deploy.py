"""Deploy static dist and one Python administrator to the existing Linux VPS."""
from pathlib import Path
import argparse,datetime,tarfile,subprocess,json,secrets,hashlib,io
from admin_server import default_config,render
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--key',required=True);p.add_argument('--host',default='root@8.133.244.26');p.add_argument('--skip-downloads',action='store_true');a=p.parse_args()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
private=ROOT/'local-private';private.mkdir(exist_ok=True)
authfile=private/'admin.json'
if not authfile.exists():
 password=secrets.token_urlsafe(24);salt=secrets.token_bytes(24)
 auth={'salt':salt.hex(),'hash':hashlib.pbkdf2_hmac('sha256',password.encode(),salt,600000).hex()}
 authfile.write_text(json.dumps(auth),encoding='utf-8')
 (ROOT/'local-admin-credentials.md').write_text('# AIONE1 管理员凭据\n\n管理员口令：'+password+'\n\n仅保存在本机，不提交 GitHub；服务器仅保存 PBKDF2 哈希。\n\n未启用 HTTPS 前使用 SSH 隧道：\n\nssh -i C:\\Users\\Administrator\\.ssh\\vinylbox_server -L 18081:127.0.0.1:80 root@8.133.244.26\n\n访问 http://127.0.0.1:18081/admin/ 。\n',encoding='utf-8')
archive=ROOT/'site-release.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
 for f in (ROOT/'dist').rglob('*'):
  if f.is_file() and f.relative_to(ROOT/'dist').parts[0]!='media':tar.add(f,arcname=Path('dist')/f.relative_to(ROOT/'dist'))
 tar.add(ROOT/'scripts'/'admin_server.py',arcname='admin_server.py')
 tar.add(authfile,arcname='admin.json')
 source=ROOT/'local-repositories'/'digital-human'
 for f in source.rglob('*'):
  if f.is_file() and '.git' not in f.relative_to(source).parts:tar.add(f,arcname=Path('digital-human')/f.relative_to(source))
 for f in Path(r'D:\AIPROJECT\douyin\assets\avatars').glob('*.png'):
  tar.add(f,arcname=Path('digital-human/assets/avatars')/f.name)
 for name,text in [('routes.json',json.dumps(default_config(),ensure_ascii=False)),('routes.conf',render(default_config()))]:
  b=text.encode();info=tarfile.TarInfo(name);info.size=len(b);tar.addfile(info,io.BytesIO(b))
base=['-i',a.key,'-o','BatchMode=yes','-o','ConnectTimeout=20']
def run(args,**kwargs):return subprocess.run(args,check=True,**kwargs)
print('Uploading website release '+stamp,flush=True)
run(['scp',*base,str(archive),a.host+':/tmp/aione1-release.tar.gz'])
script=r"""set -eu
BASE=/opt/aione1
RELEASE="$BASE/releases/STAMP"
mkdir -p "$RELEASE" "$BASE/downloads" "$BASE/private"
mkdir -p "$BASE/media"
chmod 700 "$BASE/private"
tar -xzf /tmp/aione1-release.tar.gz -C "$RELEASE"
test -s "$RELEASE/dist/tools/lumen/index.html"
test -s "$RELEASE/dist/admin/index.html"
cp "$RELEASE/admin_server.py" "$BASE/admin_server.py"
if [ ! -f "$BASE/private/admin.json" ]; then cp "$RELEASE/admin.json" "$BASE/private/admin.json"; fi
if [ ! -f "$BASE/private/routes.json" ]; then cp "$RELEASE/routes.json" "$BASE/private/routes.json"; fi
if [ ! -f "$BASE/routes.conf" ]; then cp "$RELEASE/routes.conf" "$BASE/routes.conf"; fi
chmod 600 "$BASE/private/"*.json
ln -s "$RELEASE/dist" "$BASE/current-STAMP"
mv -Tf "$BASE/current-STAMP" "$BASE/current"
ln -sfn "$BASE/media" "$BASE/current/media"
mkdir -p "$BASE/digital-human"
cp -a "$RELEASE/digital-human/." "$BASE/digital-human/"
mkdir -p "$BASE/digital-human/outputs"
chown -R nginx:nginx "$BASE/digital-human/outputs"
cp /opt/budayang-comics/nginx.conf /opt/budayang-comics/nginx.conf.before-aione1-STAMP
python3 - <<'PY'
from pathlib import Path
p=Path('/opt/budayang-comics/nginx.conf')
text=p.read_text()
if 'AIONE1-PORTAL' not in text:
 assert text.count(' server {')==1, 'Unexpected Nginx config'
 text=text[:text.index(' server {')]+'''
 # AIONE1-PORTAL
 server {
  listen 80;
  server_name aione1.com www.aione1.com 8.133.244.26;
  root /opt/aione1/current;
  index index.html;
  charset utf-8;
  add_header X-Content-Type-Options nosniff always;
  add_header Referrer-Policy strict-origin-when-cross-origin always;
  location / { try_files $uri $uri/ =404; }
  location = /liubao { return 301 /liubao/; }
  location ^~ /liubao/ { alias /opt/budayang-comics/current/; index index.html; }
  location ^~ /downloads/ {
   alias /opt/aione1/downloads/;
   add_header Content-Disposition attachment;
   add_header X-Content-Type-Options nosniff;
  }
  location = /admin { return 301 /admin/; }
  location ^~ /admin/api/ {
   proxy_pass http://127.0.0.1:9180/;
   proxy_set_header Host $http_host;
   proxy_set_header X-Forwarded-Host $http_host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-Proto $scheme;
   proxy_buffering off;
  }
  location = /data.json { root /opt/budayang-comics/current; }
  location ~ ^/assets/(00|01|02|03|04|05|poetry-01)/ { root /opt/budayang-comics/current; }
  include /opt/aione1/routes.conf;
  error_page 404 /404.html;
  location = /404.html { internal; }
 }
}
'''
 p.write_text(text)
PY
cat > /etc/systemd/system/aione1-admin.service <<'UNIT'
[Unit]
Description=AIONE1 Nginx Administrator
After=network.target
[Service]
Type=simple
WorkingDirectory=/opt/aione1
ExecStart=/usr/bin/python3 /opt/aione1/admin_server.py
Restart=on-failure
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
[Install]
WantedBy=multi-user.target
UNIT
cat > /etc/systemd/system/aione1-avatar.service <<'UNIT'
[Unit]
Description=AIONE1 Digital Human Python Backend
After=network.target
[Service]
Type=simple
User=nginx
Group=nginx
WorkingDirectory=/opt/aione1/digital-human
ExecStart=/usr/bin/python3 /opt/aione1/digital-human/app.py --host 127.0.0.1 --port 7860 --no-browser
Restart=on-failure
NoNewPrivileges=true
PrivateTmp=true
[Install]
WantedBy=multi-user.target
UNIT
python3 - <<'PY'
import sys,json
from pathlib import Path
sys.path.insert(0,'/opt/aione1')
import admin_server
path=Path('/opt/aione1/private/routes.json')
data=json.loads(path.read_text())
for row in data['routes']:
 if row['id']=='avatar' and row['mode']=='intro':row['mode']='static'
Path('/opt/aione1/routes.conf').write_text(admin_server.render(data))
path.write_text(json.dumps(data,ensure_ascii=False))
PY
if ! /usr/sbin/nginx -t -c /opt/budayang-comics/nginx.conf; then
 cp /opt/budayang-comics/nginx.conf.before-aione1-STAMP /opt/budayang-comics/nginx.conf
 exit 1
fi
systemctl daemon-reload
systemctl enable aione1-admin
systemctl restart aione1-admin
systemctl enable aione1-avatar
systemctl restart aione1-avatar
systemctl reload budayang-comics
for i in 1 2 3 4 5; do
 if curl -fsS http://127.0.0.1:9180/session -o /dev/null; then break; fi
 sleep 1
done
curl -fsS http://127.0.0.1/ | grep -q AIONE1
curl -fsS http://127.0.0.1/tools/lumen/ | grep -q 'lumen remote'
curl -fsS http://127.0.0.1/liubao/data.json -o /dev/null
curl -fsS http://127.0.0.1/apps/music/ | grep -q musicForYou
curl -fsS -H 'Host: aione1.com' http://127.0.0.1/about.html | grep -q AIONE1
if [ -f "$BASE/downloads/SHA256SUMS.txt" ]; then
 sed -i 's/\r$//' "$BASE/downloads/SHA256SUMS.txt"
 (cd "$BASE/downloads" && sha256sum -c SHA256SUMS.txt)
fi
test "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/admin/api/config)" = 401
echo 'DEPLOYED http://8.133.244.26/'
for i in $(seq 1 20); do
 if curl -fsS http://127.0.0.1:7860/api/ping; then break; fi
 sleep 1
done
curl -fsS http://127.0.0.1:7860/api/ping
""".replace('STAMP',stamp)
print('Activating Linux release and validating Nginx',flush=True)
run(['ssh',*base,a.host,'bash -s'],input=script.encode())
if not a.skip_downloads:
 downloads=ROOT/'downloads-release.tar.gz'
 with tarfile.open(downloads,'w') as tar:
  for f in (ROOT/'local-downloads').iterdir():
   if f.is_file():tar.add(f,arcname=f.name)
 print('Uploading actual installation files',flush=True)
 run(['scp',*base,str(downloads),a.host+':/tmp/aione1-downloads.tar'])
 run(['ssh',*base,a.host,'tar -xf /tmp/aione1-downloads.tar -C /opt/aione1/downloads && cd /opt/aione1/downloads && sha256sum -c SHA256SUMS.txt'])
print('Release complete '+stamp,flush=True)
