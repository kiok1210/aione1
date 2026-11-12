from pathlib import Path
import json,urllib.request,urllib.error,http.cookiejar,argparse,datetime
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--public',default='http://8.133.244.26');p.add_argument('--tunnel',default='http://127.0.0.1:18081');a=p.parse_args()
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public':a.public,'checks':[]}
DIRECT=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def request(url,data=None,opener=None,headers=None,method=None):
 h=headers or {}
 if data is not None:h={**h,'Content-Type':'application/json'}
 req=urllib.request.Request(url,data=json.dumps(data).encode() if data is not None else None,headers=h,method=method)
 try:response=(opener or DIRECT).open(req,timeout=30)
 except urllib.error.HTTPError as e:response=e
 with response:return response.status,response.read()
paths=['/','/about.html','/admin/','/liubao/','/liubao/data.json','/apps/music/','/apps/podcast/','/apps/video/']+['/tools/'+id+'/' for id in ['music','podcast','video','avatar','qingdeng','liubao','lumen','dukou']]
for path in paths:
 status,body=request(a.public+path);assert status==200,(path,status)
 report['checks'].append({'path':path,'status':status})
status,_=request(a.public+'/admin/api/config');assert status==401;report['unauthenticated_config_status']=status
status,_=request(a.public+'/admin/api/session',{'password':'not-a-secret'},headers={'Origin':a.public});assert status==403;report['public_http_login_status']=status
jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(jar))
password=next(line.split('：',1)[1] for line in (R/'local-admin-credentials.md').read_text('utf-8').splitlines() if line.startswith('管理员口令：'))
status,body=request(a.tunnel+'/admin/api/session',{'password':password},opener,{'Origin':a.tunnel});assert status==200
csrf=json.loads(body)['csrf'];headers={'Origin':a.tunnel,'X-CSRF-Token':csrf}
status,body=request(a.tunnel+'/admin/api/config',opener=opener);assert status==200
config=json.loads(body)['config']
status,body=request(a.tunnel+'/admin/api/preview',config,opener,headers);assert status==200
status,body=request(a.tunnel+'/admin/api/apply',config,opener,headers);assert status==200,body.decode()
assert json.loads(body)['ok'];report['authenticated_preview_and_nginx_apply']='passed'
status,body=request(a.tunnel+'/admin/api/logout',{},opener,headers);assert status==200
status,_=request(a.tunnel+'/admin/api/config',opener=opener);assert status==401;report['logout_invalidation']='passed'
for file in ['MusicForYou-0.6.5-win-x64-setup.exe','EchoPod-0.1.0-win-x64.exe','VideoForYou-0.1.1-win-x64-setup.exe','digital-human-source.zip','SHA256SUMS.txt']:
 status,_=request(a.public+'/downloads/'+file,method='HEAD');report['checks'].append({'path':'/downloads/'+file,'status':status})
report['all_downloads_available']=all(x['status']==200 for x in report['checks'])
status,body=request(a.public+'/apps/avatar/api/ping')
report['digital_human_backend_status']=status
assert status==200,('digital human backend',status)
audio_checks=[]
for app in ['music','podcast']:
 status,body=request(a.public+'/apps/'+app+'/library.json');assert status==200
 catalog=json.loads(body)
 for item in catalog['items']:
  url=a.public+'/media/'+app+'/audio/'+item['url'].split('/')[-1]
  status,_=request(url,headers={'Range':'bytes=0-1023'});assert status==206,(app,status)
  audio_checks.append({'app':app,'id':item['id'],'range_status':status})
report['audio_checks']=audio_checks
(R/'docs'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verified pages, login restrictions, authenticated Nginx preview/apply, logout. Downloads available:',report['all_downloads_available'])
