"""Single stdlib Python admin service. Public pages remain static Nginx files."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json,secrets,hashlib,hmac,time,threading,subprocess,os

BASE=Path(os.environ.get('AIONE_BASE','/opt/aione1'))
PRIVATE=BASE/'private'
CONFIG=PRIVATE/'routes.json'
AUTH=PRIVATE/'admin.json'
ROUTES=BASE/'routes.conf'
SESSIONS={}; FAILURES={}; LOCK=threading.RLock()
IDS={'music','podcast','video','avatar','qingdeng','liubao','lumen','dukou'}
NAMES={'music':'musicForYou','podcast':'bokeForYou','video':'videoForYou','avatar':'数字人口播','qingdeng':'青灯','liubao':'六宝','lumen':'lumen remote','dukou':'渡口'}
def default_config():
 return {'routes':[{'id':id,'name':NAMES[id],'mode':'static' if id in {'music','podcast','video','liubao','avatar'} else 'intro','port':7860 if id=='avatar' else 8787} for id in NAMES]}
def validate(data):
 if not isinstance(data,dict) or not isinstance(data.get('routes'),list) or len(data['routes'])!=8:raise ValueError('需要且只能配置 8 个工具')
 result=[];seen=set()
 for row in data['routes']:
  id=row.get('id');mode=row.get('mode');port=row.get('port',8787)
  if id not in IDS or id in seen:raise ValueError('工具标识无效或重复')
  if mode not in {'intro','static','proxy'}:raise ValueError('不支持的部署方式')
  if mode=='static' and id not in {'music','podcast','video','liubao','avatar'}:raise ValueError(NAMES[id]+' 尚无可运行静态构建，请使用宣传页或配置后端')
  if type(port) is not int or not 1024<=port<=65535 or port in {9180}:raise ValueError('后端端口必须为 1024–65535，且不能指向管理服务')
  seen.add(id);result.append({'id':id,'name':NAMES[id],'mode':mode,'port':port})
 return {'routes':result}
def render(data):
 data=validate(data);lines=['# Managed by AIONE1 visual administrator. Included inside server {}.']
 for r in data['routes']:
  id=r['id'];url='/apps/'+id+'/'
  lines.append('location = /apps/'+id+' { return 301 '+url+'; }')
  if r['mode']=='intro':lines.append('location ^~ '+url+' { return 302 /tools/'+id+'/; }')
  elif id=='liubao' and r['mode']=='static':lines.append('location ^~ '+url+' { return 302 /liubao/; }')
  elif r['mode']=='static':
   if id=='avatar':
    for sub in ['api','assets','outputs']:
     lines.extend(['location ^~ '+url+sub+'/ {',' proxy_pass http://127.0.0.1:'+str(r['port'])+'/'+sub+'/;',' proxy_set_header Host $host;',' proxy_set_header X-Real-IP $remote_addr;',' client_max_body_size 40m;',' proxy_read_timeout 300s;','}'])
   lines.append('location ^~ '+url+' { alias /opt/aione1/current/apps/'+id+'/; index index.html; }')
  else:
   lines.extend(['location ^~ '+url+' {',' proxy_pass http://127.0.0.1:'+str(r['port'])+'/;',' proxy_http_version 1.1;',' proxy_set_header Host $host;',' proxy_set_header X-Real-IP $remote_addr;',' proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;',' proxy_set_header X-Forwarded-Proto $scheme;',' proxy_buffering off;',' proxy_read_timeout 300s;',' client_max_body_size 40m;','}'])
 return '\n'.join(lines)+'\n'
def atomic_write(path,text):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(text,encoding='utf-8');os.chmod(temp,0o600 if path.parent==PRIVATE else 0o644);os.replace(temp,path)
def apply(data):
 text=render(data)
 with LOCK:
  previous=ROUTES.read_text() if ROUTES.exists() else ''
  atomic_write(ROUTES,text)
  try:
   check=subprocess.run(['/usr/sbin/nginx','-t','-c','/opt/budayang-comics/nginx.conf'],capture_output=True,text=True,timeout=20)
   if check.returncode:raise ValueError('Nginx 校验失败：'+check.stderr[-1500:])
   reload=subprocess.run(['systemctl','reload','budayang-comics'],capture_output=True,text=True,timeout=25)
   if reload.returncode:raise ValueError('Nginx 重载失败：'+reload.stderr[-1000:])
   atomic_write(CONFIG,json.dumps(data,ensure_ascii=False,indent=2))
  except Exception:
   atomic_write(ROUTES,previous)
   subprocess.run(['systemctl','reload','budayang-comics'],capture_output=True,timeout=25)
   raise
 return text
class Handler(BaseHTTPRequestHandler):
 server_version='AIONE1Admin/1'
 def log_message(self,fmt,*args):pass
 def respond(self,status,data,cookie=None):
  payload=json.dumps(data,ensure_ascii=False).encode()
  self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
  if cookie:self.send_header('Set-Cookie',cookie)
  self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
 def body(self):
  n=int(self.headers.get('Content-Length','0'))
  if n<1 or n>16384:raise ValueError('请求长度无效')
  if self.headers.get('Content-Type','').split(';')[0]!='application/json':raise ValueError('只接受 JSON')
  return json.loads(self.rfile.read(n))
 def session(self):
  from http.cookies import SimpleCookie
  c=SimpleCookie();c.load(self.headers.get('Cookie',''));key=c.get('aione_session');key=key.value if key else ''
  with LOCK:
   now=time.time()
   for old in list(SESSIONS):
    if SESSIONS[old]['expires']<now:del SESSIONS[old]
   return SESSIONS.get(hashlib.sha256(key.encode()).hexdigest())
 def secure_transport(self):
  return self.headers.get('X-Forwarded-Proto')=='https' or self.headers.get('X-Real-IP') in {'127.0.0.1','::1'}
 def origin_ok(self):
  origin=self.headers.get('Origin')
  return bool(origin and urlsplit(origin).netloc==self.headers.get('X-Forwarded-Host',self.headers.get('Host')))
 def cookie(self,value,expire=False):
  return 'aione_session='+value+'; HttpOnly; SameSite=Strict; Path=/admin/api/; Max-Age='+('0' if expire else '28800')+('; Secure' if self.headers.get('X-Forwarded-Proto')=='https' else '')
 def do_GET(self):
  route=urlsplit(self.path).path
  if route=='/session':
   session=self.session();self.respond(200,{'authenticated':bool(session),'csrf':session['csrf'] if session else None,'transportAllowed':self.secure_transport()});return
  session=self.session()
  if not session:self.respond(401,{'error':'请先登录管理员'});return
  if route=='/config':
   with LOCK:data=json.loads(CONFIG.read_text()) if CONFIG.exists() else default_config()
   self.respond(200,{'config':data,'nginx':render(data)})
  else:self.respond(404,{'error':'接口不存在'})
 def do_POST(self):
  route=urlsplit(self.path).path
  try:
   if not self.origin_ok():self.respond(403,{'error':'请求来源无效'});return
   if not self.secure_transport():self.respond(403,{'error':'请通过 HTTPS 或 SSH 隧道访问管理页后登录'});return
   data=self.body()
   if route=='/session':
    ip=self.headers.get('X-Real-IP','unknown');now=time.time()
    with LOCK:
     failures=[t for t in FAILURES.get(ip,[]) if now-t<600];FAILURES[ip]=failures
     if len(failures)>=6:self.respond(429,{'error':'尝试次数过多，请 10 分钟后再试'});return
    auth=json.loads(AUTH.read_text());password=data.get('password','')
    if not isinstance(password,str) or len(password)>1024:raise ValueError('口令格式无效')
    candidate=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(auth['salt']),600000).hex()
    if not hmac.compare_digest(candidate,auth['hash']):
     with LOCK:FAILURES[ip].append(now)
     self.respond(401,{'error':'口令不正确'});return
    token=secrets.token_urlsafe(32);csrf=secrets.token_urlsafe(24)
    with LOCK:
     if len(SESSIONS)>1000:SESSIONS.clear()
     SESSIONS[hashlib.sha256(token.encode()).hexdigest()]={'csrf':csrf,'expires':now+28800};FAILURES.pop(ip,None)
    self.respond(200,{'authenticated':True,'csrf':csrf},self.cookie(token));return
   session=self.session()
   if not session:self.respond(401,{'error':'会话过期，请重新登录'});return
   if not hmac.compare_digest(self.headers.get('X-CSRF-Token',''),session['csrf']):self.respond(403,{'error':'会话校验失败，请刷新后重试'});return
   if route=='/logout':
    with LOCK:
     for key,value in list(SESSIONS.items()):
      if value is session:del SESSIONS[key]
    self.respond(200,{'ok':True},self.cookie('',True));return
   if route not in {'/preview','/apply'}:self.respond(404,{'error':'接口不存在'});return
   config=validate(data)
   text=apply(config) if route=='/apply' else render(config)
   self.respond(200,{'ok':True,'config':config,'nginx':text,'message':'配置已校验并生效' if route=='/apply' else '预览已生成，尚未修改服务器'})
  except (ValueError,json.JSONDecodeError) as e:self.respond(400,{'error':str(e)})
  except Exception:self.respond(500,{'error':'操作失败，服务器配置已保留或回滚，请检查服务日志'})
if __name__=='__main__':
 PRIVATE.mkdir(mode=0o700,parents=True,exist_ok=True)
 if not CONFIG.exists():atomic_write(CONFIG,json.dumps(default_config(),ensure_ascii=False))
 ThreadingHTTPServer(('127.0.0.1',9180),Handler).serve_forever()
