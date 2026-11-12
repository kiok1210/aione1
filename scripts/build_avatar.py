from pathlib import Path
import shutil,os
R=Path(__file__).resolve().parents[1];D=R/'dist'/'apps'/'avatar';D.mkdir(parents=True,exist_ok=True)
source=Path(os.environ.get('AIONE_AVATAR_WEB',r'D:\AIPROJECT\douyin\web'))
if not source.exists():source=D
for f in source.iterdir():
 if f.is_file() and f.resolve()!=(D/f.name).resolve():shutil.copy2(f,D/f.name)
p=D/'index.html';text=p.read_text('utf-8').replace('href="/styles.css"','href="styles.css"').replace('<script src="/app.js">','<script src="prefix.js"></script><script src="app.js">')
if '../../tools/avatar/' not in text:text=text.replace('<nav class="tabs">','<nav class="tabs"><a class="tab" href="../../tools/avatar/" style="text-decoration:none">← AIONE1</a>')
text=text.replace('照片与文案<br>只在本机处理','照片与文案<br>由所连接后端处理')
text=text.replace('输入照片与文案，本地自动完成','输入照片与文案，由已配置的后端完成')
p.write_text(text,encoding='utf-8')
(D/'prefix.js').write_text("""(()=>{const native=window.fetch.bind(window);function fix(v){if(typeof v==='string'&&(v.startsWith('/assets/')||v.startsWith('/outputs/')))return '/apps/avatar'+v;if(Array.isArray(v))return v.map(fix);if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,fix(x)]));return v}window.fetch=async(input,init)=>{const request=typeof input==='string'&&input.startsWith('/api/')?'/apps/avatar'+input:input;const res=await native(request,init);if(typeof request==='string'&&request.startsWith('/apps/avatar/api/')&&(res.headers.get('content-type')||'').includes('application/json')){return new Response(JSON.stringify(fix(await res.json())),{status:res.status,statusText:res.statusText,headers:res.headers})}return res}})();""",encoding='utf-8')
print('Built actual digital-human studio frontend')
