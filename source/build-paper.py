from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import html,re
site=Path(__file__).resolve().parent.parent
# Read only the supplied document's content; preserve its order and wording.
with ZipFile('/Users/jiangcai/Desktop/MA ISD UNIT3/-10.01 英文.docx') as z:
 root=E.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs=[]
for para in root.findall('.//w:body/w:p',ns):
 text=''.join(t.text or '' for t in para.findall('.//w:t',ns))
 if text.strip():paragraphs.append((text,para))
headings={text for text,p in paragraphs[1:] if len(text)<100 and not text.endswith('?') and not text.endswith('.')}
subheadings={'Recognition and Judgment of Everyday Experience','Asymmetry in Decision-Making Power'}
body=[];sections=[];in_questions=False;in_refs=False
for i,(text,para) in enumerate(paragraphs):
 if i==0:continue
 if text in headings:
  if in_questions:body.append('</ol>');in_questions=False
  slug=re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')
  tag='h3' if text in subheadings else 'h2'
  if tag=='h2':sections.append((text,slug))
  in_refs=text=='References';body.append(f'<{tag} id="{slug}">{html.escape(text)}</{tag}>');continue
 if 12<=i<=16:
  if not in_questions:body.append('<ol class="questions">');in_questions=True
  body.append('<li>'+html.escape(text)+'</li>');continue
 if in_questions:body.append('</ol>');in_questions=False
 runs=[]
 for run in para.findall('.//w:r',ns):
  rt=''.join(t.text or '' for t in run.findall('w:t',ns))
  if not rt:continue
  encoded=html.escape(rt);props=run.find('w:rPr',ns)
  if props is not None:
   italic=props.find('w:i',ns);bold=props.find('w:b',ns)
   if italic is not None and italic.get('{'+ns['w']+'}val') not in ('0','false'):encoded='<em>'+encoded+'</em>'
   if bold is not None and bold.get('{'+ns['w']+'}val') not in ('0','false'):encoded='<strong>'+encoded+'</strong>'
  runs.append(encoded)
 content=''.join(runs) or html.escape(text)
 if in_refs:
  def link_reference(match):
   raw=match.group(0);url=raw.rstrip('.')
   url={'https://doi.org/10.1177/146613810343007':'https://emmawitkowski.com/wp-content/uploads/2017/11/street-phenomenology_kusenbach_2003_the-go-along-as-ethno-tool.pdf'}.get(url,url)
   return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'+raw[len(raw.rstrip('.')):]
  content=re.sub(r'https?://[^\s<>]+',link_reference,content)
  if text.startswith('LSE Cities (n.d.)'):
   content='LSE Cities (n.d.) <em>Ordinary Streets: An ethnography from local to global</em>. Available at: <a href="https://www.lse.ac.uk/cities/research/cities-space-and-society/Ordinary-Streets" target="_blank" rel="noopener noreferrer">https://www.lse.ac.uk/cities/research/cities-space-and-society/Ordinary-Streets</a> (Accessed: 29 September 2026).'
 body.append('<p'+(' class="reference"' if in_refs else '')+'>'+content+'</p>')
nav=''.join(f'<a href="#{slug}">{html.escape(text)}</a>' for text,slug in sections)
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A paper on everyday experience, visibility and publicness at shopfronts on Rye Lane."><title>The Everyday Visibility and Publicness of Shopfronts — Paper</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:100px}body{margin:0;background:#fff;color:#161616}header{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);border-bottom:1px solid #eee;font:12px Arial,sans-serif;padding:20px 5vw;display:flex;justify-content:space-between;gap:20px}a{color:inherit;text-underline-offset:4px}header a{text-decoration:none}a:hover{color:#008a52}article{max-width:780px;margin:70px auto 100px;padding:0 30px}.kicker{font:11px Arial,sans-serif;letter-spacing:.2em;margin-bottom:25px}h1{font:500 clamp(30px,4.4vw,54px)/1.12 Arial,sans-serif;letter-spacing:-.035em;margin:0 0 55px}h2{font:500 25px/1.35 Arial,sans-serif;letter-spacing:-.02em;margin:56px 0 20px;scroll-margin-top:90px}p,li{font:18px/1.85 Georgia,"Times New Roman",serif;margin:0 0 24px}nav{padding:24px 0;border-top:1px solid #ddd;border-bottom:1px solid #ddd;margin-bottom:48px}nav summary{font:12px Arial,sans-serif;cursor:pointer}nav .links{display:grid;gap:12px;margin-top:20px;font:13px/1.5 Arial,sans-serif}nav a{text-decoration:none}.reference{font-size:14px;line-height:1.7;overflow-wrap:anywhere;padding-left:24px;text-indent:-24px}li{padding-left:8px}.questions{padding-left:25px}footer{border-top:1px solid #ddd;padding-top:28px;margin-top:60px;font:12px Arial,sans-serif}@media(max-width:600px){header{padding:17px 22px}article{margin-top:44px;padding:0 22px}p,li{font-size:17px;line-height:1.8}h1{margin-bottom:38px}h2{font-size:23px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{header,nav,footer{display:none}article{max-width:none;margin:0}h2{break-after:avoid}a{text-decoration:none}}
</style></head><body><header><a href="index.html?start=street">← Back to street</a><span>RYE LANE / RESEARCH PAPER</span><a href="scenes.html" target="_top">Other scenes ↗</a></header><article><div class="kicker">RYE LANE · EVERYDAY EXPERIENCE</div><h1>'''+html.escape(paragraphs[0][0])+'''</h1><nav aria-label="Paper contents"><details><summary>Contents</summary><div class="links">'''+nav+'''</div></details></nav>'''+''.join(body)+'''<footer><a href="index.html?start=street">← Back to street</a></footer></article></body></html>'''
page=page.replace('@media(max-width:600px){header{','@media(max-width:600px){header span{display:none}header{')
# One static reading page per chapter; no manuscript content is removed.
chapter_chunks=[chunk for chunk in re.split(r'(?=<h2 id=")',''.join(body)) if chunk.strip()]
files=['paper.html','paper-02.html','paper-03.html','paper-04.html','paper-05.html','paper-07.html','paper-09.html','paper-10.html']
start=page[:page.index('<h2 id=')]
end=page[page.rindex('<footer>'):]
start=start.replace('font:500 clamp(30px,4.4vw,54px)/1.12','font:500 clamp(28px,3.1vw,38px)/1.2')
start=start.replace('</style>','[aria-current="page"]{color:#008a52;text-decoration:underline}.chapter-count{font:11px Arial,sans-serif;letter-spacing:.12em;color:#777;margin:0 0 24px}.chapter-pagination{display:flex;justify-content:space-between;gap:30px;border-top:1px solid #ddd;padding:28px 0;margin-top:50px;font:13px/1.6 Arial,sans-serif}.chapter-pagination a{max-width:46%;text-decoration:none}.chapter-pagination a:last-child{text-align:right}h3{font:500 21px/1.4 Arial,sans-serif;margin:42px 0 20px;scroll-margin-top:90px}h2{margin-top:20px}h1{margin-bottom:34px}nav{margin-bottom:32px}</style>')
for index,chunk in enumerate(chapter_chunks):
 current_start=start.replace('href="#references"',f'href="{files[-1]}#references"')
 for i,(name,slug) in enumerate(sections):
  current_start=current_start.replace(f'href="#{slug}"',f'href="{files[i]}#{slug}"'+(' aria-current="page"' if i==index else ''))
 current_start=current_start.replace('<title>The Everyday Visibility and Publicness of Shopfronts — Paper</title>',f'<title>{html.escape(sections[index][0])} — Shopfronts</title>')
 before=f'<div class="chapter-count">CHAPTER {index+1:02d} / {len(sections):02d}</div>'
 previous=f'<a rel="prev" href="{files[index-1]}">← {html.escape(sections[index-1][0])}</a>' if index else '<span></span>'
 following=f'<a rel="next" href="{files[index+1]}">{html.escape(sections[index+1][0])} →</a>' if index+1<len(files) else '<a href="scenes.html" target="_top">Other scenes →</a>'
 pagination='<div class="chapter-pagination" aria-label="Chapter navigation">'+previous+following+'</div>'
 chapter_page=current_start+before+chunk+pagination+end
 chapter_page=chapter_page.replace('</head>','<style>'+(site/'source/user-settings/design.css').read_text()+'</style></head>')

 chapter_page=chapter_page.replace('href="index.html?start=street"','href="index.html?start=street" target="_top"')
 chapter_page=chapter_page.replace('</body>','<script src="source/font-settings.js"></script></body>')
 (site/files[index]).write_text(chapter_page)
for old,dest,anchor in [('paper-06.html','paper-05.html','recognition-and-judgment-of-everyday-experience'),('paper-08.html','paper-07.html','asymmetry-in-decision-making-power')]:
 (site/old).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={dest}#{anchor}"><title>Section moved</title></head><body><a href="{dest}#{anchor}">Read this subsection in its parent chapter</a></body></html>')
print('Created',len(files),'chapter pages:',', '.join(files))
print('Paper paragraphs:',len(paragraphs),'sections:',len(sections),'article words:',len(' '.join(t for t,_ in paragraphs).split()))
print('Sections:',[t for t,_ in sections])
