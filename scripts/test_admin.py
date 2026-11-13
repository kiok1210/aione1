import unittest,tempfile,threading,json,hashlib,urllib.request,urllib.error
from pathlib import Path
from unittest.mock import patch
import admin_server as a
class AdminTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.private=self.base/'private';self.private.mkdir()
  self.patchers=[patch.object(a,'PRIVATE',self.private),patch.object(a,'CONFIG',self.private/'routes.json'),patch.object(a,'AUTH',self.private/'admin.json'),patch.object(a,'ROUTES',self.base/'routes.conf')]
  for p in self.patchers:p.start()
  a.SESSIONS.clear();a.FAILURES.clear()
  salt=b'test-salt';auth={'salt':salt.hex(),'hash':hashlib.pbkdf2_hmac('sha256',b'test-password',salt,600000).hex()};a.AUTH.write_text(json.dumps(auth))
  self.server=a.ThreadingHTTPServer(('127.0.0.1',0),a.Handler);self.port=self.server.server_port
  self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):
  self.server.shutdown();self.server.server_close()
  for p in self.patchers:p.stop()
  self.tmp.cleanup()
 def request(self,path,data=None,headers=None):
  h={'X-Real-IP':'127.0.0.1','X-Forwarded-Host':f'127.0.0.1:{self.port}','Origin':f'http://127.0.0.1:{self.port}'}
  if headers:h.update(headers)
  if data is not None:h['Content-Type']='application/json'
  req=urllib.request.Request(f'http://127.0.0.1:{self.port}'+path,data=json.dumps(data).encode() if data is not None else None,headers=h)
  try:r=urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:r=e
  return r.status,json.loads(r.read()),r.headers
 def login(self):
  status,data,h=self.request('/session',{'password':'test-password'});self.assertEqual(status,200)
  self.assertIn('HttpOnly',h['Set-Cookie']);self.assertIn('SameSite=Strict',h['Set-Cookie'])
  return {'Cookie':h['Set-Cookie'].split(';')[0],'X-CSRF-Token':data['csrf']}
 def test_auth_required(self):
  self.assertEqual(self.request('/config')[0],401)
  self.assertEqual(self.request('/preview',a.default_config())[0],401)
 def test_public_http_login_blocked(self):
  status,data,h=self.request('/session',{'password':'test-password'},{'X-Real-IP':'198.51.100.5','X-Forwarded-Proto':'http'})
  self.assertEqual(status,403);self.assertNotIn('Set-Cookie',h)
 def test_login_preview_csrf_logout(self):
  h=self.login();self.assertEqual(self.request('/config',headers=h)[0],200)
  bad={**h,'X-CSRF-Token':'invalid'}
  self.assertEqual(self.request('/apply',a.default_config(),bad)[0],403)
  status,data,_=self.request('/preview',a.default_config(),h)
  self.assertEqual(status,200);self.assertIn('alias /opt/aione1/current/apps/music/',data['nginx']);self.assertFalse(a.ROUTES.exists())
  self.assertEqual(self.request('/logout',{},h)[0],200)
  self.assertEqual(self.request('/config',headers=h)[0],401)
 def test_login_throttled(self):
  for _ in range(6):self.assertEqual(self.request('/session',{'password':'wrong'})[0],401)
  self.assertEqual(self.request('/session',{'password':'test-password'})[0],429)
 def test_route_injection_rejected(self):
  for field,value in [('id','music;return 200;'),('mode','proxy;'),('port','8787;')]:
   data=a.default_config();data['routes'][0][field]=value
   with self.assertRaises(ValueError):a.render(data)
  data=a.default_config();data['routes'][0]['port']=9180
  with self.assertRaises(ValueError):a.render(data)
 def test_failed_nginx_rolls_back(self):
  a.ROUTES.write_text('# original config')
  class Result:
   returncode=1;stderr='invalid configuration'
  with patch.object(a.subprocess,'run',return_value=Result()):
   with self.assertRaises(ValueError):a.apply(a.default_config())
  self.assertEqual(a.ROUTES.read_text(),'# original config');self.assertFalse(a.CONFIG.exists())
 def test_external_destination_is_restricted(self):
  data=a.default_config();row=next(r for r in data['routes'] if r['id']=='qingdeng')
  self.assertIn('return 302 http://8.133.244.26:4317/',a.render(data))
  row['port']=8787
  with self.assertRaises(ValueError):a.render(data)
  row['port']=4317;row['id']='music'
  with self.assertRaises(ValueError):a.render(data)
if __name__=='__main__':unittest.main(verbosity=2)
