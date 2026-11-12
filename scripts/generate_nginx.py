"""Generate a portable static Nginx config; Linux production admin is separate."""
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output',required=True);p.add_argument('--port',type=int,default=8080);a=p.parse_args()
root=Path(a.root).resolve().as_posix()
if any(c in root for c in '"\r\n;{}'):raise SystemExit('Unsupported root path')
if not 1024<=a.port<=65535:raise SystemExit('Port must be 1024–65535')
text='''worker_processes 1;
error_log logs/error.log;
pid logs/nginx.pid;
events { worker_connections 1024; }
http {
 include mime.types;
 default_type application/octet-stream;
 sendfile on;
 server {
  listen PORT;
  server_name localhost;
  root "ROOT";
  index index.html;
  charset utf-8;
  location / { try_files $uri $uri/ =404; }
  error_page 404 /404.html;
  location = /404.html { internal; }
 }
}
'''.replace('ROOT',root).replace('PORT',str(a.port))
Path(a.output).write_text(text,encoding='utf-8');print('Generated',a.output)
