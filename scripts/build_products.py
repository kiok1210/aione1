from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1]; D=R/'dist'
items=json.loads((D/'tools.json').read_text('utf-8'))
details={
 'qingdeng': [('把故事继续写下去','青灯是 AI 辅助小说写作工具，现有书房已经在 Linux 服务器运行。'),('进入已有书房','点击进入青灯，使用原有登录方式打开实际工作台。')],
 'music': [('一台属于你的虚拟唱机','搜索或粘贴 YouTube 链接，把喜欢的声音缓存到本地；转动的黑胶唱片和唱臂，让聆听多一点仪式感。'),('歌词与聆听一起前进','逐行歌词、非中文歌词翻译、单曲与列表循环。听书时可调倍速，也可以设置睡眠定时。'),('把音乐库留在手边','分类、收藏、下载队列与播放进度记忆，帮助你整理真正想反复听的内容。')],
 'podcast': [('听节目，也可以看视频','中文播客、英文播客、长视频和短视频，切换内容模式，找到适合此刻的内容。'),('把一集节目听完整','本地缓存、倍速、睡眠定时和断点续听。通勤没听完，下一次接着来。'),('让文字成为聆听的线索','逐字稿支持点行跳转，附中文对照；也可以关闭字幕，专注声音。')],
 'video': [('画面与声音，一起留下','选择屏幕或窗口，录制系统声音和麦克风，按需要调整分辨率与帧率。'),('演示时，把重点讲清楚','实时滤镜、文字贴图、摄像头画中画与鼠标高亮，帮助观众跟上每一步。'),('录完，就收进作品库','支持暂停、继续与快捷键。完成后直接回放，找到文件，再开始下一次表达。')],
 'avatar': [('从照片与文案开始','选择形象、写入文案，工作流串联语音合成、口型驱动和竖屏输出。'),('配音与口型可以组合','本地配音、SadTalker 与 FFmpeg 为基础；也提供可自行配置的云端引擎接口。'),('让成片少一点重复操作','多镜头切分、字幕、转场与背景音乐由工作流统一处理。具体运行能力取决于本机环境与已安装模型。')],
 'liubao': [('跟六宝，走进文学里的世界','不打烊潮玩店的六个小伙伴，陪你从日常的小问题走进成语典故和古诗词。'),('漫画、故事、原文，一起读','在画面里看见故事，在正文里理解情节，再回到作品原文与文学小卡。'),('按自己的节奏慢慢读','支持夜间阅读、字号切换、大图阅读和本机进度记忆。手机上也能展开目录挑选作品。')]
}
steps={
 'music':['下载 Windows 安装包，在本机完成安装。','首次打开按提示初始化下载组件，或配置本机已有组件。','搜索歌曲或粘贴 YouTube 链接；相关在线内容需要可用的网络环境。','缓存完成后，在音乐库离线播放。'],
 'podcast':['下载 Windows 安装包并在本机安装。','选择中文播客、英文播客或视频模式。','搜索节目或添加频道链接，开始播放或缓存。','查看逐字稿、收藏与本地库，下次从上次的位置继续。'],
 'video':['下载 Windows 安装包并安装录屏工坊。','选择屏幕或窗口，打开需要的系统声音与麦克风。','按需要添加滤镜、文字或画中画，开始录制。','停止后在作品库回放和定位视频文件。'],
 'avatar':['下载工作流源码包并解压到本地目录。','运行 setup.bat，按脚本安装运行环境与模型。首次安装需要网络与足够的磁盘空间。','运行 start.bat，浏览器会打开本机创作台 http://127.0.0.1:7860 。','上传已获授权的照片、填写文案，选择已配置引擎生成视频。']}
files={'music':('MusicForYou-0.6.5-win-x64-setup.exe','Windows 安装包 · v0.6.5'),'podcast':('EchoPod-0.1.0-win-x64.exe','Windows 安装包 · v0.1.0'),'video':('VideoForYou-0.1.1-win-x64-setup.exe','Windows 安装包 · v0.1.1'),'avatar':('digital-human-source.zip','本地部署源码包')}
nav='''<header class="header"><a class="brand" href="./"><span class="brand-symbol">a<span>i</span></span><span>AIONE<span class="one">1</span><small>姚毛毛的工具与创作</small></span></a><nav aria-label="主导航"><a href="./#tools">工具目录</a><a href="about.html">关于自己</a><a class="blog-link" href="https://www.cnblogs.com/yaomaomao" target="_blank" rel="noopener noreferrer">博客园 ↗</a></nav></header>'''
foot='''<footer><a class="footer-brand" href="./">AIONE1<span>一个人，也可以把想法做出来。</span></a><div><a href="about.html">关于姚毛毛 ↗</a><p>© 2026 AIONE1 · 姚毛毛</p></div></footer>'''
def page(path,title,body):
 p=D/path;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="../../"><title>{title} · AIONE1</title><meta name="description" content="{title}：功能介绍、使用方式与项目进展。"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/products.css"></head><body><a class="skip" href="#main">跳到正文</a><div class="shell">{nav}<main id="main">{body}</main>{foot}</div></body></html>',encoding='utf-8')

for t in items:
 id=t['id'];pending=t['status']=='源码待上传';label='项目介绍' if pending else '功能与使用'
 hero=f'''<a class="breadcrumbs" href="./#tools">← 全部工具 <span>/ {t['name']}</span></a><section class="product-hero"><div><p class="eyebrow">{t['category']} / {t['kind']}</p><div class="product-name">{t['name']}</div><h1 class="serif">{t['title']}</h1><p class="product-intro">{t['description']}</p><div class="product-actions">'''
 if pending:hero+='<a class="primary" href="tools/'+id+'/#progress">了解项目进展 ↓</a><span class="product-status">○ 源码待上传</span>'
 else:hero+=f'<a class="primary" href="{("liubao/" if id=="liubao" else "use/"+id+"/")}">{("进入在线故事馆" if id=="liubao" else "部署与使用")} <span>↗</span></a><a class="text-link" href="tools/{id}/#features">了解功能 ↓</a>'
 hero+='</div></div><div class="product-art '+t['visual']+'">'
 if id=='liubao':hero+='<img src="assets/liubao-cover.webp" alt="六宝文学漫画作品预览">'
 else:hero+=f'<div class="product-art-type">{t["name"]}</div><span>{"COMING TO LIFE" if pending else "MADE FOR YOUR EVERYDAY"}</span>'
 hero+='</div></section>'
 if pending:
  body=hero+f'''<section id="progress" class="progress-panel"><p class="eyebrow">IN THE MAKING / 正在生长</p><h2>先为这个想法，留一个位置。</h2><p>{t['name']} 是我的{t['kind']}项目。这个页面是它在 AIONE1 的独立介绍页，项目仓库已经准备好，源码将从其他设备接入。</p><div class="project-timeline"><div class="done"><b>01</b><h3>项目收录</h3><p>已建立独立页面，纳入 AIONE1 统一目录。</p></div><div class="current"><b>02</b><h3>源码接入</h3><p>等待作者上传现有项目，随后核对实际功能。</p></div><div><b>03</b><h3>开放使用</h3><p>完成部署与验证后，在此提供真实可用的入口。</p></div></div><p class="pending-note">当前尚未开放体验与下载。开放时，这里会直接接入使用页面。</p></section>'''
 else:
  body=hero+'<section id="features" class="product-features"><p class="eyebrow">THOUGHTFULLY MADE / 具体能做什么</p><h2>把需要的事情，做得顺手一点。</h2><div>'+''.join(f'<article><span>0{i+1}</span><h3>{a}</h3><p>{b}</p></article>' for i,(a,b) in enumerate(details[id]))+'</div></section>'
  body+=f'''<section class="product-next"><div><p class="eyebrow">READY WHEN YOU ARE</p><h2>{'打开故事，慢慢读。' if id=='liubao' else '从这里，开始使用。'}</h2><p>{'无需安装，直接进入完整阅读站。' if id=='liubao' else '查看真实下载与本地部署步骤，按自己的节奏开始。'}</p></div><a class="primary" href="{'liubao/' if id=='liubao' else 'use/'+id+'/'}">{'进入故事馆' if id=='liubao' else '部署与使用'} ↗</a></section>'''
 body+=f'<div class="source-footer"><span>作者：姚毛毛 · AIONE1</span><a href="https://github.com/kiok1210/{t["repo"]}" target="_blank" rel="noopener">开发者：查看源码 ↗</a></div>'
 page(Path('tools')/id/'index.html',t['name']+' · '+label,body)
 if id in files:
  file,flabel=files[id]
  body=f'''<a class="breadcrumbs" href="tools/{id}/">← {t['name']} 项目介绍</a><section class="use-hero"><p class="eyebrow">GET STARTED / 部署与使用</p><h1>{t['name']}</h1><p>{'在你的电脑上部署，浏览器访问本机创作台。' if id=='avatar' else '下载桌面应用，在你的电脑上开始使用。'}</p><div class="download-panel"><div><span>{flabel}</span><p>{'源码、环境脚本与使用说明；不包含模型与个人数据。' if id=='avatar' else '文件由 AIONE1 服务器提供。请在 Windows 10 / 11 x64 上安装。'}</p></div><a class="primary" href="downloads/{file}" download>下载{('源码包' if id=='avatar' else '安装包')} ↓</a></div><p class="download-meta"><a href="downloads/SHA256SUMS.txt">查看文件 SHA-256 校验值</a></p></section><section class="setup-steps"><p class="eyebrow">STEP BY STEP</p><h2>{'本地部署步骤' if id=='avatar' else '从安装到第一次使用'}</h2>{''.join(f'<article><span>0{i+1}</span><p>{s}</p></article>' for i,s in enumerate(steps[id]))}</section><div class="use-note"><h3>{'关于运行环境' if id=='avatar' else '桌面应用的使用方式'}</h3><p>{'数字人口播需要在本机安装推理环境和模型。这个页面提供真实项目源码与部署脚本，当前未将推理服务部署在公网服务器。默认本地引擎在本机处理，选择云端引擎时按配置调用第三方服务。' if id=='avatar' else '此项目以桌面客户端运行，网站负责介绍、下载与安装指引。浏览器内不会启动你电脑上的应用；下载后请从本机打开。'}</p></div><div class="source-footer"><a href="tools/{id}/">返回产品介绍</a><a href="https://github.com/kiok1210/{t['repo']}" target="_blank" rel="noopener">开发者：查看源码 ↗</a></div>'''
  page(Path('use')/id/'index.html',t['name']+' · 部署与使用',body)

p=D/'tools'/'qingdeng'/'index.html'
text=p.read_text('utf-8').replace('href="use/qingdeng/"','href="http://8.133.244.26:4317/"').replace('部署与使用','进入青灯书房').replace('查看真实下载与本地部署步骤，按自己的节奏开始。','已接入现有 Linux 服务，进入后使用青灯自己的登录页。').replace('开发者：查看源码 ↗','项目仓库 ↗')
p.write_text(text,encoding='utf-8')
p=D/'apps'/'qingdeng';p.mkdir(parents=True,exist_ok=True)
(p/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta http-equiv="refresh" content="0;url=http://8.133.244.26:4317/"><title>进入青灯书房</title></head><body style="font:18px/1.8 sans-serif;padding:40px"><a href="http://8.133.244.26:4317/">进入青灯书房 →</a></body></html>',encoding='utf-8')

for id in ['music','podcast','video']:
 p=D/'tools'/id/'index.html'
 text=p.read_text('utf-8')
 text=text.replace('href="use/'+id+'/">部署与使用', 'href="apps/'+id+'/">打开网页版')
 text=text.replace('href="use/'+id+'/">部署与使用 ↗','href="apps/'+id+'/">打开网页版 ↗')
 text=text.replace('查看真实下载与本地部署步骤，按自己的节奏开始。','网页版由 Nginx 静态托管，可跨 Linux / Windows 浏览器使用；完整桌面版另附下载与安装指引。')
 p.write_text(text,encoding='utf-8')
 p=D/'use'/id/'index.html';text=p.read_text('utf-8').replace('<section class="use-hero">','<section class="use-hero"><a class="primary" href="apps/'+id+'/">打开跨平台网页版 ↗</a><p class="hint">网页版提供基础播放或录屏能力；完整功能请使用下面的桌面客户端。</p>');p.write_text(text,encoding='utf-8')
for p in [D/'tools'/'avatar'/'index.html',D/'use'/'avatar'/'index.html']:
 text=p.read_text('utf-8').replace('href="use/avatar/">部署与使用','href="apps/avatar/">打开口播工作台')
 text=text.replace('<section class="use-hero">','<section class="use-hero"><a class="primary" href="apps/avatar/">打开真实口播工作台 ↗</a><p class="hint">工作台显示所连接后端的实际模型与引擎状态；生成前请确认已就绪。</p>')
 p.write_text(text,encoding='utf-8')
home=(D/'index.html').read_text('utf-8')
for t in items:
 home=home.replace(f'href="{t["url"]}" target="_blank" rel="noopener"',f'href="tools/{t["id"]}/"')
 home=home.replace(f'href="{t["url"]}" ',f'href="tools/{t["id"]}/" ')
 # The secondary source link remains optional on the product page only.
 home=home.replace('<a class="source-link" href="https://github.com/kiok1210/liubao" target="_blank" rel="noopener">创作资源与源码 ↗</a>','')
 home=home.replace(t['action']+'：'+t['name'],'了解'+t['name'])
 home=home.replace('>'+t['action']+' ↗</a>','>了解工具 ↗</a>')
home=home.replace('桌面工具请前往项目页下载或查看运行说明；「源码待上传」的项目已预留仓库，后续继续更新。','每个工具都有独立介绍页。可用项目提供真实的阅读、下载或部署入口，尚在准备的项目展示最新进展。')
(D/'index.html').write_text(home,encoding='utf-8')
for file in [D/'index.html',D/'about.html']:
 text=file.read_text('utf-8').replace('<div><a href="about.html">关于姚毛毛 ↗</a>','<div><a href="admin/">Nginx 管理 ↗</a> · <a href="about.html">关于姚毛毛 ↗</a>')
 file.write_text(text,encoding='utf-8')
(D/'404.html').write_text('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>稍稍迷路了 · AIONE1</title><style>body{background:#f8f9f5;color:#2b5947;font:16px/2 "Microsoft YaHei",sans-serif;max-width:640px;margin:15vh auto;padding:30px}h1{font-size:34px;font-weight:400}a{color:inherit}</style></head><body><p>AIONE1 / 姚毛毛的工具与创作</p><h1>好奇心，换个方向继续。</h1><p>这个地址还没有内容，工具与项目的介绍都收在目录里。</p><a href="/">回到工具目录 →</a></body></html>''',encoding='utf-8')
print('Built 8 product pages and 4 usage pages')
