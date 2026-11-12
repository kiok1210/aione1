from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
def run(args,cwd):
    result=subprocess.run(args,cwd=cwd,check=True,text=True,encoding='utf-8',errors='replace',capture_output=True)
    return result.stdout.strip()
descriptions={'aione1':'AIONE1 · 姚毛毛的工具与创作，统一工具目录与个人网站','digital-human':'数字人口播：本地照片、文案、配音、口型与自动剪辑工作流','liubao':'六宝文学漫画 · 不打烊成语与诗词故事馆、创作资源','lumen-remote':'lumen remote 远程桌面工具（源码待上传）','dukou':'渡口 SSH 连接工具（源码待上传）','qingdeng':'青灯 AI 辅助小说写作工具（源码待上传）'}
for repo in ['lumen-remote','dukou','qingdeng','digital-human','liubao','aione1']:
    cwd=ROOT if repo=='aione1' else ROOT/'local-repositories'/repo
    if not (cwd/'.git').exists():
        run(['git','init','-b','main'],cwd)
        run(['git','add','.'],cwd)
        run(['git','commit','-m','Create AIONE1 tool collection' if repo=='aione1' else 'Publish selected project source and documentation'],cwd)
    exists=subprocess.run(['gh','repo','view',f'kiok1210/{repo}','--json','name'],capture_output=True).returncode==0
    if not exists:
        run(['gh','repo','create',f'kiok1210/{repo}','--public','--description',descriptions[repo],'--source','.','--remote','origin','--push'],cwd)
    else:
        remotes=run(['git','remote'],cwd).splitlines()
        if 'origin' not in remotes: run(['git','remote','add','origin',f'https://github.com/kiok1210/{repo}.git'],cwd)
        run(['git','push','-u','origin','main'],cwd)
    print(f'PUBLISHED https://github.com/kiok1210/{repo}',flush=True)
