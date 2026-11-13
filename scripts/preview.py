"""Complete local preview: portal, comic library, real downloads and digital studio."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import urllib.request,urllib.error,os
R=Path(__file__).resolve().parents[1]
COMICS=Path(r'D:\AI-lingchong\不打烊成语漫画网站\dist')
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(R/'dist'),**kwargs)
 def translate_path(self,path):
  parts=urlsplit(path).path
  for prefix,root in [('/liubao/',COMICS),('/downloads/',R/'local-downloads')]:
   if parts.startswith(prefix):
    rel=super().translate_path('/'+parts[len(prefix):]);return str(root/Path(rel).relative_to(R/'dist'))
  return super().translate_path(path)
 def proxy(self):
  route=urlsplit(self.path).path
  if route.startswith('/apps/avatar/') and any(route.startswith('/apps/avatar/'+p) for p in ['api/','assets/','outputs/']):
   target='http://127.0.0.1:7860/'+self.path[len('/apps/avatar/'):]
  elif route.startswith('/admin/api/'):
   target=os.environ.get('AIONE_ADMIN_ORIGIN','http://127.0.0.1:18082')+self.path
  else:return False
  body=self.rfile.read(int(self.headers.get('Content-Length',0))) if self.command=='POST' else None
  headers={k:v for k,v in self.headers.items() if k.lower() not in {'connection','content-length','accept-encoding'}}
  request=urllib.request.Request(target,data=body,headers=headers,method=self.command)
  try:
   opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
   try:res=opener.open(request,timeout=300)
   except urllib.error.HTTPError as e:res=e
   with res:
    self.send_response(res.status)
    for k,v in res.headers.items():
     if k.lower() not in {'transfer-encoding','connection','server','date'}:self.send_header(k,v)
    self.end_headers()
    if self.command!='HEAD':
     while chunk:=res.read(256*1024):self.wfile.write(chunk)
  except OSError:
   payload=b'{"error":"Backend is not running. Start the Python studio service."}'
   self.send_response(503);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
  return True
 def do_GET(self):
  if not self.proxy():super().do_GET()
 def do_POST(self):
  if not self.proxy():self.send_error(404)
 def do_DELETE(self):
  if not self.proxy():self.send_error(404)
ThreadingHTTPServer(('127.0.0.1',5178),Handler).serve_forever()
