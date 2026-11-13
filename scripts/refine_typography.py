"""Keep presentation readable: 16px body copy and a 14px minimum for supporting text."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1];D=R/'dist'
MARK='/* AIONE1 readable typography */'
def enlarge(match):
    text=match.group(0)
    return re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)px',lambda n:str(max(14,float(n[1]))).removesuffix('.0')+'px',text)
def contrast(match):
    selector,body=match[1],match[2]
    if re.search(r'code|terminal|mini-screen|brand-symbol|primary|album-play|a\.download',selector):return match[0]
    def color(m):
        value=m[1]
        if len(value) not in {4,7}:return m[0]
        h=value[1:];h=''.join(c*2 for c in h) if len(h)==3 else h
        rgb=[int(h[i:i+2],16)/255 for i in [0,2,4]]
        lin=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        lum=sum(v*w for v,w in zip(lin,[.2126,.7152,.0722]))
        return 'color:#53624d' if .18<lum<.85 else m[0]
    body=re.sub(r'(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,8})',color,body)
    return selector+'{'+body+'}'
extras={
 'site.css':'''
:root{--muted:#53624d}
body{font-size:16px;line-height:1.8;font-family:"Microsoft YaHei UI","Microsoft YaHei","PingFang SC","Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:auto}
.intro,.card-description,.card-title,.about-strip p:not(.eyebrow),.essay p:not(.eyebrow),.section-heading>p{font-size:16px;line-height:1.9;color:#4e5d48}
.header nav,.primary,.text-link,.card-bottom a,.back-collection{font-size:16px}
.serif{font-weight:500}.eyebrow{letter-spacing:1.3px;color:#4f6048}
.brand small{letter-spacing:.5px;color:#53624d}.visual-number{opacity:.8}.art-caption{letter-spacing:1px;color:#526448;text-align:center}
.tags span,.card-meta,.card-bottom,.collection-note,.hero-foot,footer p,.footer-brand span{font-size:14px;line-height:1.8}
.search input{width:165px;font-size:16px}.search kbd{font-size:14px}.card-description{min-height:90px}
.about-layout aside{font-size:16px}.signature small{font-size:14px}.signature a,.blog-contact a{font-size:16px;text-decoration:underline;text-underline-offset:4px}
@media(max-width:700px){.header{height:auto;min-height:112px;padding:20px 0;flex-wrap:wrap;gap:18px}.header nav{width:100%;gap:24px;flex-wrap:wrap}.header nav a{font-size:16px;padding:5px 0}.brand small{font-size:14px}.brand{font-size:23px}.categories{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.categories button{font-size:16px;padding:11px}.hero-actions{flex-wrap:wrap;gap:16px}.hero h1{font-size:34px;line-height:1.6}.search input{width:100%}.hero-foot{gap:12px;flex-wrap:wrap}.section-heading>p{margin-top:18px}.collection-note{align-items:flex-start;gap:12px}footer{align-items:flex-start;flex-wrap:wrap;gap:20px}footer>div{text-align:left}.art-label{display:none}.art-caption{max-width:100%;font-size:14px}.card-description{min-height:0}.about-layout aside{gap:16px;line-height:1.8}}
''',
 'products.css':'''
.product-intro,.product-features p,.progress-panel p,.product-next p,.use-note p,.use-hero>p:not(.eyebrow),.setup-steps article p,.download-panel p{font-size:16px;line-height:1.9;color:#4e5d48}
.breadcrumbs,.product-status,.source-footer,.download-meta a,.download-panel>div>span{font-size:14px;line-height:1.8}
.product-features h3,.project-timeline h3,.use-note h3{font-size:18px;line-height:1.7}.product-art>span{font-size:14px;letter-spacing:1px}
.product-actions{flex-wrap:wrap}.product-art-type{overflow-wrap:anywhere}
@media(max-width:700px){.source-footer{flex-direction:column;gap:12px}.product-hero h1{font-size:32px;line-height:1.7}.download-panel .primary{white-space:normal}}
''',
 'apps.css':'''
body{font-size:16px;line-height:1.8;font-family:"Microsoft YaHei UI","Microsoft YaHei","PingFang SC","Segoe UI",system-ui,sans-serif}
.lead,.hint,.notice,.status,.queue small,.route p,header a{font-size:14px;color:#4e6048;line-height:1.8}
label,input,select,button{font-size:16px}.login{max-width:560px}.login .lead{font-size:16px}.login label{font-size:16px}
.code{font-size:14px;line-height:1.8}.route h3{font-size:18px}.route-fields label{font-size:16px}.actions{align-items:center;flex-wrap:wrap}
.notice pre{font-size:14px;white-space:pre-wrap;overflow-wrap:anywhere}
''',
 'library.css':'''
.library-hero .lead,.library-note{font-size:16px;line-height:1.8}.library-hero .hint,.library-summary span,.album-body p,.album-body small,.playing-info small,.rate-label{font-size:14px;color:#4e6048}
.album-body h2{font-size:17px;line-height:1.7;min-height:58px}.album-body{min-height:180px}.album-body small{display:block;padding-right:28px}
.library-tools button,.playing-info b,.transport button{font-size:16px}.album-badge{font-size:14px}.playing-info b{line-height:1.6}.library-tools input{font-size:16px}
.player-bar{padding-top:20px;padding-bottom:20px}.rate-label select{font-size:16px}
@media(max-width:550px){.library-hero{align-items:flex-start;gap:16px}.library-hero h1{font-size:28px}.library-hero h1>span{font-size:16px}.library-summary b{font-size:36px}.album-grid{grid-template-columns:1fr}.album-art{height:190px}.album-body{min-height:145px}.album-body h2{font-size:18px;min-height:0;-webkit-line-clamp:3}.library-hero .hint{font-size:14px;letter-spacing:.4px}.playing-info b{font-size:14px}.playing-info small{font-size:14px}.transport button{font-size:14px;padding:6px 8px}.player-bar{padding:16px 12px;gap:10px}.library-app{padding-bottom:210px}}
'''}
for name,extra in extras.items():
 p=D/'assets'/name
 text=p.read_text('utf-8').split(MARK)[0]
 text=re.sub(r'(?<![-\w])font(?:-size)?\s*:[^;{}]+',enlarge,text)
 text=re.sub(r'([^{}]+)\{([^{}]*)\}',contrast,text)
 p.write_text(text.rstrip()+'\n'+MARK+'\n'+extra,encoding='utf-8')
p=D/'apps'/'avatar'/'styles.css'
text=p.read_text('utf-8').split(MARK)[0]
text=re.sub(r'(?<![-\w])font(?:-size)?\s*:[^;{}]+',enlarge,text)
text+='\n'+MARK+'\nbody{font-size:16px;line-height:1.8}.studio-v2 .hint,.studio-v2 .health-pill{font-size:14px;line-height:1.8}.studio-v2 input,.studio-v2 textarea,.studio-v2 select{font-size:16px}.studio-v2 .hero p{font-size:17px;line-height:1.9}\n'
p.write_text(text,encoding='utf-8')
print('Applied 16px reading text, 14px minimum labels, clearer contrast and responsive navigation.')
