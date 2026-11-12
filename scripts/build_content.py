"""Materialize complete static content into dist without copying account settings."""
from pathlib import Path
import os,shutil
R=Path(__file__).resolve().parents[1];D=R/'dist'
for source,target in [(Path(os.environ.get('AIONE_COMICS_DIST',r'D:\AI-lingchong\不打烊成语漫画网站\dist')),D/'liubao'),(R/'local-downloads',D/'downloads')]:
 if not source.exists():continue
 for f in source.rglob('*'):
  if not f.is_file():continue
  dest=target/f.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   try:os.link(f,dest)
   except OSError:shutil.copy2(f,dest)
print('Assembled local comic library and actual download files in dist')
