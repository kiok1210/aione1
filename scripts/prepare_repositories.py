"""Prepare explicitly selected source snapshots; never copy local credentials or runtime data."""
from pathlib import Path
import shutil, re, subprocess, json

ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/'local-repositories'; STAGE.mkdir(exist_ok=True)
def copy_file(source,target):
    target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target)
def copy_tree(source,target,extensions=None):
    for f in source.rglob('*'):
        if not f.is_file() or any(p in {'.git','__pycache__','node_modules','.pytest_cache'} for p in f.relative_to(source).parts): continue
        if extensions and f.suffix not in extensions: continue
        copy_file(f,target/f.relative_to(source))

for repo,title,description in [('lumen-remote','lumen remote','远程桌面工具'),('dukou','渡口','SSH 连接工具'),('qingdeng','青灯','AI 辅助小说写作工具')]:
    out=STAGE/repo; out.mkdir(exist_ok=True)
    (out/'README.md').write_text(f'''# {title}

{description} · 姚毛毛 / AIONE1

**项目仓库已创建，源码待作者从其他设备上传。当前不提供安装包或在线运行功能。**

统一目录：https://aione1.com
主站源码：https://github.com/kiok1210/aione1

## 后续接入

将实际项目源码上传到本仓库，补充环境要求、运行步骤、功能说明与许可证。安装包可通过 GitHub Releases 发布。完成后更新主站 `scripts/build_site.py` 中本项目的状态和链接。

上传前请排除 `.env`、API 密钥、SSH 私钥、连接配置、会话数据库及个人数据。
''',encoding='utf-8')
    (out/'.gitignore').write_text('.env\n.env.*\n!.env.example\nnode_modules/\ndist/\nbuild/\ntarget/\n__pycache__/\n*.pem\n*.key\n*.p12\n*.keystore\n*.log\n',encoding='utf-8')

source=Path(r'D:\AIPROJECT\douyin'); out=STAGE/'digital-human'; out.mkdir(exist_ok=True)
for name in ['app.py','README.md','THIRD_PARTY.md','requirements-kokoro.txt','requirements-sadtalker.txt','setup.bat','start.bat','数字人-start.bat','.env.example']:
    copy_file(source/name,out/name)
for name in ['pipeline','web','tests']:
    copy_tree(source/name,out/name,{'.py','.js','.html','.css','.json'})
for name in ['setup.ps1','start-all.ps1']:
    copy_file(source/'scripts'/name,out/'scripts'/name)
for f in (source/'assets').rglob('README.md'): copy_file(f,out/f.relative_to(source))
ignore=(source/'.gitignore').read_text(encoding='utf-8')+'\n.fish-runtime/\n.mamba-fish/\nartifacts/\n.tmp-assets/\n*.pem\n*.key\n'
(out/'.gitignore').write_text(ignore,encoding='utf-8')

out=STAGE/'liubao'; out.mkdir(exist_ok=True)
source=Path(r'D:\AI-lingchong\不打烊成语漫画网站')
for name in ['index.html','styles.css','app.js','timeline.js']:
    copy_file(source/name,out/'site'/name)
copy_file(source/'dist'/'data.json',out/'site'/'data.json')
copy_tree(Path(r'D:\AI-lingchong\liubao-skill'),out/'liubao-skill')
copy_file(ROOT/'dist'/'assets'/'liubao-cover.webp',out/'site'/'preview.webp')
(out/'README.md').write_text('''# 六宝 · 不打烊文学故事馆

姚毛毛的文学漫画项目。六个小伙伴走进成语典故与古诗词，包含漫画、故事和原文阅读。

在线阅读：https://aione1.com/liubao/
服务器备用入口：http://8.133.244.26/
统一工具目录：https://github.com/kiok1210/aione1

## 目录

- `site/`：已发布阅读站的前端源码和作品索引。
- `liubao-skill/`：六宝系列创作技能、人物参考与资源。

本仓库不包含全部漫画高清原图。`site/data.json` 中的 `assets/` 路径由现有服务器 `/opt/budayang-comics/current/assets/` 提供。运行完整阅读站时，请将作者的漫画资源放入 `site/assets/`；仅查看源码无需下载全部资源。

```powershell
python -m http.server 5180 --directory site
```

角色、故事、参考图与漫画属于作者的创作资源；未附统一开源许可证，不代表自动授权商业使用。
''',encoding='utf-8')
(out/'.gitignore').write_text('__pycache__/\n.env\n*.pem\n*.key\nsite/assets/\n',encoding='utf-8')

patterns=[re.compile(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----'),re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{25,})\b')]
hits=[]
for repo in STAGE.iterdir():
    for f in repo.rglob('*'):
        if not f.is_file():continue
        if f.name=='.env': hits.append(str(f));continue
        if f.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.ico'}:continue
        text=f.read_text(encoding='utf-8',errors='ignore')
        if any(p.search(text) for p in patterns): hits.append(str(f))
if hits: raise SystemExit('Potential credential content; review files: '+json.dumps(hits))
print('Prepared and scanned:', ', '.join(p.name for p in STAGE.iterdir()))
