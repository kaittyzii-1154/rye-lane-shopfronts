from pathlib import Path
import xml.etree.ElementTree as E
import html,json
from optimize_assets import compact
site=Path(__file__).resolve().parent.parent;assets=site/'assets';E.register_namespace('','http://www.w3.org/2000/svg')
# Masks use proportions of the source drawing, ordered from foreground details to background.
def box(x1,y1,x2,y2):return [[x1,y1],[x2,y1],[x2,y2],[x1,y2]]
scene_data={
1:('Street study 04','S04',[
('Plants',box(.74,.67,1,1)),('Plants',box(.64,.35,.83,.57)),('Fruit display',[[.13,.47],[.35,.37],[.69,.47],[.76,.62],[.67,.7],[.1,.63]]),('Display racks',[[.12,.61],[.68,.6],[.78,.72],[.7,.88],[.12,.87]]),('Street poles',box(.89,0,.96,.87)),('Buildings',[[0,0],[1,0],[1,.8],[.8,.79],[.72,.65],[.1,.74],[0,.72]])]),
2:('Street overview','O',[]),
3:('Street study 01','S01',[
('People',[[.346,.65],[.37,.65],[.393,.77],[.374,.81],[.35,.78]]),('People',box(.486,.57,.512,.67)),('Railway',[[.55,0],[1,0],[1,.34],[.77,.48],[.73,.23],[.64,.14]]),('Buildings',[[0,0],[.55,0],[.68,.16],[.75,.44],[.54,.67],[.45,.75],[.26,.89],[0,.68]])]),
4:('Street study 02','S02',[
('People',[[.258,.33],[.285,.34],[.303,.42],[.299,.57],[.275,.6],[.255,.5]]),('Plants',[[.78,0],[.94,0],[.96,.25],[.85,.36],[.8,.3]]),('Street vendors',[[.04,0],[.14,0],[.36,.35],[.29,.4],[.23,.3],[.23,.76],[.04,.76]]),('Street vendors',[[.43,.19],[.62,.15],[.77,.43],[.77,.77],[.61,.94],[.4,.65],[.4,.39],[.49,.32]]),('Buildings',[[0,0],[.78,0],[.8,.35],[1,.3],[1,.75],[.75,.79],[.52,.5],[.27,.58],[.22,.83],[0,.83]])]),
5:('Street study 03','S03',[
('Street and streetlights',[[.77,.48],[.79,.48],[.79,.84],[.77,.84]]),('Street and streetlights',box(.83,.7,.87,.95)),('Street vendors',[[.29,.4],[.41,.39],[.42,.56],[.32,.58]]),('Street vendors',[[.81,.49],[.91,.43],[1,.55],[1,.7],[.87,.69]]),('Corner building',[[.45,0],[.8,0],[.89,.29],[.82,.65],[.64,.64],[.47,.48]]),('Left building',[[0,0],[.23,0],[.35,.19],[.33,.42],[.29,.5],[0,.3]]),('Middle building',[[.23,0],[.45,0],[.47,.48],[.37,.5],[.33,.38],[.35,.19]]),('Foreground building',[[0,.61],[.26,.62],[.53,.84],[.52,1],[0,1]])])}
def inside(x,y,poly):
 hit=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
 return hit
css='''*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font-family:Arial,sans-serif}a{color:inherit;text-decoration:none}a:hover{color:#008a52}header{padding:22px 4vw;display:flex;justify-content:space-between;gap:20px;font-size:12px;border-bottom:1px solid #eee;background:white;position:fixed;top:0;left:0;right:0;z-index:5}#scene-view{height:100dvh;width:100vw;overflow:hidden;touch-action:none}#scene-view svg{width:100%;height:100%;display:block}.scene-object{pointer-events:none;transition:transform .22s ease}.scene-object.active{transform:translateY(-4px)}.scene-object.active line,.scene-object.active path{stroke:#008a52!important}footer{position:fixed;bottom:16px;left:4vw;right:4vw;font-size:11px;color:#555;pointer-events:none}@media(max-width:600px){header{font-size:10px;padding:18px}footer{font-size:10px}}'''
all_records={}
for number,(name,prefix,masks) in scene_data.items():
 root=E.parse(assets/f'scene-{number:02d}.svg').getroot();view=list(map(float,root.get('viewBox').split()));vx,vy,w,h=view
 custom_path=site/'source/user-settings'/f'regions-{number}.json';custom=json.loads(custom_path.read_text()) if custom_path.exists() else None
 custom_info={}
 if custom:
  assert all(abs(a-b)<.01 for a,b in zip(custom['viewBox'],view)), 'Scene viewBox mismatch'
  masks=[]
  for user_region in custom['regions']:
   custom_info[user_region['name']]=user_region
   for poly in user_region['polygons']:masks.append((user_region['name'],[[(x-vx)/w,(y-vy)/h] for x,y in poly]))
 masks=masks+([] if custom or number in (2,4) else [('Street and streetlights' if number==5 else 'Street',box(0,0,1.001,1.001))]);regions=[];records=[];groups=[];label_keys={};group_by_id={}
 for i,(label,poly) in enumerate(masks,1):
  key=label_keys.get(label,f'part-{len(label_keys)+1:02d}');regions.append(dict(id=key,name=label,polygon=[[vx+x*w,vy+y*h] for x,y in poly]));
  if label in label_keys:continue
  label_keys[label]=key
  g=E.Element('{http://www.w3.org/2000/svg}g',{'id':key,'class':'scene-object','data-name':label});title=E.SubElement(g,'{http://www.w3.org/2000/svg}title');title.text=label;groups.append(g);group_by_id[key]=g
  info=custom_info.get(label,{})
  photo=str(info.get('photo') or f'{prefix}-{len(label_keys):02d}');assert all(c.isalnum() or c in '-_' for c in photo), 'Invalid photo identifier'
  image=f'assets/photo-{photo}.svg'
  if not (site/image).exists():(site/image).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="800" height="600" fill="#000"/></svg>')
  records.append(dict(id=photo,region=key,label=label,image=image,title=label if custom else f'A moment around the {label.lower()}',text=(info.get('story') or 'Field notes will be added here.') if custom else f'Someone might pause here while another person makes room to pass. The {label.lower()} could become a meeting point, a workplace, or a temporary obstacle at different times of day.',type=('Field notes pending' if not info.get('story') else 'Illustrative scenario') if custom else 'Illustrative scenario'))
 for parent in list(root.iter()):
  for line in list(parent):
   if line.tag.split('}')[-1]!='line':continue
   x=(float(line.get('x1'))+float(line.get('x2')))/2;y=(float(line.get('y1'))+float(line.get('y2')))/2
   region=next((r for r in regions if inside(x,y,r['polygon'])),None)
   if region is not None:parent.remove(line);group_by_id[region['id']].append(line)
 for g in reversed(groups):root.append(g)
 compact(root)
 root.set('role','img');root.set('aria-label',name+' interactive drawing');
 for original_title in root.findall('{http://www.w3.org/2000/svg}title'):original_title.text=name
 svg=E.tostring(root,encoding='unicode')
 runtime=(site/'source/scene-camera.js').read_text().replace('SCENE_REGIONS',json.dumps(regions)).replace('SCENE_VIEW',json.dumps(view))
 hover=(site/'source/hover-cards.js').read_text().replace('CARD_RECORDS',json.dumps(records))
 page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title><style>{css}</style></head><body><header><a href="scenes.html">← Other scenes</a><span>{name}</span><a href="index.html?start=street">Back to street ↗</a></header><div id="scene-view">{svg}</div><footer>Hover for 0.3 seconds to discover a photo · Click the photo to turn it over · Scroll to zoom · Double-click to reset</footer><script>{runtime}\n{hover}</script></body></html>'''
 if number==2 and not custom:page=page.replace('Hover for 0.3 seconds to discover a photo · Click the photo to turn it over · Scroll to zoom · Double-click to reset','Scroll to zoom · Drag to explore · Double-click to reset')
 (site/f'scene-{number:02d}.html').write_text(page);all_records[f'scene-{number:02d}.html']=dict(name=name,regions=regions,photos=records)
 print(name,len(regions),'regions',sum(len(g)-1 for g in groups),'lines')
(site/'scene-regions.json').write_text(json.dumps(all_records,indent=2))
order=[2,3,4,5,1];cards=[]
for i in order:
 name=scene_data[i][0];featured=' featured' if i==2 else '';cards.append(f'<a class="scene{featured}" href="scene-{i:02d}.html"><img src="assets/thumb-scene-{i:02d}.webp" alt="{name}"'+('' if i==2 else ' loading="lazy"')+f'><span>{name} ↗</span></a>')
(site/'scenes.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Other scenes — Rye Lane</title><style>*{box-sizing:border-box}body{margin:0;background:white;color:#111;font-family:Arial,sans-serif}header{padding:24px 4vw;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #eee}a{color:inherit;text-decoration:none}a:hover{color:#008a52}main{padding:45px 4vw}h1{font-size:clamp(30px,4vw,52px);font-weight:500;margin:0 0 36px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:38px 28px}.scene img{width:100%;aspect-ratio:3/2;object-fit:contain;display:block;border-bottom:1px solid #ddd}.scene span{display:block;font-size:13px;margin-top:14px}.featured{grid-column:1/-1;width:100%}.featured img{aspect-ratio:2/1;max-height:70vh}.featured span{font-size:19px}@media(max-width:650px){.grid{grid-template-columns:1fr}.featured img{aspect-ratio:3/2}}</style></head><body><header><a href="index.html?start=street">← Back to street</a><a href="paper.html">Read the paper ↗</a></header><main><h1>Other scenes</h1><div class="grid">'''+''.join(cards)+'''</div></main></body></html>''')
