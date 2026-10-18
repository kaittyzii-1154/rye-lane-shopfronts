from pathlib import Path
import xml.etree.ElementTree as ET
import json,html,math,random
source=Path('/Users/jiangcai/Desktop/MA ISD UNIT3/SVG/10.10-市场摊位正视-横线矢量_复制.svg')
# Ordered front-to-back masks, in original 1536 × 1024 image coordinates.
regions=[]
def add(key,name,points,kind='object'):
 regions.append(dict(id=key,name=name,polygon=points,kind=kind))
# The two left-wall panels share the Alleyway hover target.
add('contact-panels-upper','上墙框',[(0,280),(165,280),(165,455),(0,455)])
add('contact-panels-lower','下墙框',[(0,505),(165,505),(165,675),(0,675)])
add('bollard','街道防撞柱',[(1285,655),(1300,647),(1330,651),(1340,668),(1340,883),(1351,896),(1351,938),(1280,938),(1280,895),(1290,885),(1291,718),(1285,705)])
add('awning','遮阳篷篷布',[(451,316),(527,295),(596,256),(622,266),(693,301),(779,323),(878,340),(967,348),(1037,339),(1056,352),(1064,417),(1036,418),(1029,454),(996,466),(910,451),(812,434),(704,408),(605,381),(521,351),(460,334)])
add('pole-left','遮阳篷左支撑杆',[(442,327),(460,329),(451,607),(439,646),(431,677),(428,843),(412,844),(429,578)])
add('pole-right','遮阳篷右支撑杆',[(1027,342),(1044,341),(1047,858),(1025,858)])
add('pole-back','遮阳篷后支撑杆',[(979,427),(994,427),(991,616),(981,616)])
add('bananas-left','左侧悬挂香蕉',[(488,375),(511,372),(524,392),(552,448),(553,481),(530,493),(503,478),(472,460),(465,436),(474,413)])
add('bananas-middle','中间悬挂香蕉',[(529,394),(548,399),(555,425),(574,454),(576,489),(552,501),(531,480),(516,459)])
add('bananas-right','右侧悬挂香蕉',[(571,418),(589,429),(600,457),(616,484),(611,505),(587,505),(568,490),(562,464)])
add('fruit-front-left','前排左侧水果',[(431,650),(469,636),(490,629),(527,632),(554,651),(538,685),(420,685)])
add('fruit-front-center','前排中间水果',[(553,650),(575,632),(605,620),(636,614),(671,629),(682,654),(673,686),(539,686)])
add('fruit-front-right','前排右侧水果',[(687,646),(722,622),(758,629),(793,639),(813,664),(803,687),(677,687)])
add('rack-front-left','前排左展示箱架',[(419,681),(539,681),(537,850),(419,850)])
add('rack-front-center','前排中展示箱架',[(540,682),(677,682),(678,849),(538,849)])
add('rack-front-right','前排右展示箱架',[(679,683),(812,680),(824,704),(815,850),(679,853)])
add('fruit-mid-left','中排左侧水果',[(472,597),(497,587),(540,584),(580,593),(616,610),(603,625),(473,625)])
add('rack-mid-left','中排左展示箱架',[(464,621),(613,622),(620,635),(558,653),(535,642),(491,636),(463,649)])
add('fruit-back','后排水果',[(611,563),(627,552),(668,549),(696,558),(712,577),(701,592),(608,592)])
add('rack-back','后排展示箱架',[(603,591),(707,590),(706,618),(677,626),(644,615),(604,623)])
add('fruit-back-right','后排右水果',[(713,586),(734,579),(764,585),(768,613),(709,613)])
add('rack-back-right','后排右展示箱架',[(709,610),(768,607),(770,629),(741,623),(714,630)])
add('fruit-right-small','右侧小果箱水果',[(829,622),(844,618),(874,625),(886,638),(883,649),(831,649)])
add('rack-right-small','右侧小展示箱架',[(829,645),(889,644),(892,718),(831,718)])
add('fruit-right-back','右侧后排水果',[(891,592),(916,581),(947,583),(974,595),(972,612),(896,624)])
add('rack-right-back','右侧后排展示箱架',[(889,619),(976,607),(975,629),(926,645),(923,744),(898,738)])
add('fruit-right-middle','右侧中排水果',[(929,624),(955,612),(979,616),(990,638),(983,650),(929,650)])
add('rack-right-middle','右侧中排展示箱架',[(925,645),(988,644),(990,793),(925,791)])
add('rack-right-rear','右侧最远展示箱架',[(995,616),(1081,614),(1084,680),(1045,683),(1045,635),(995,641)])
add('rack-right-front','右侧前排展示箱架',[(992,680),(1116,680),(1120,831),(1046,831),(1046,855),(1022,853),(1022,802),(994,800)])
add('plant-alley','巷内盆栽',[(814,613),(797,573),(801,533),(821,504),(813,475),(839,474),(858,485),(872,462),(897,477),(915,506),(904,540),(887,570),(877,616),(863,626),(833,625)])
add('plant-window-top','橱窗上层盆栽',[(1261,447),(1257,416),(1271,399),(1266,379),(1280,376),(1291,393),(1306,365),(1326,372),(1331,394),(1352,372),(1366,390),(1353,414),(1341,448),(1337,489),(1263,490)])
add('plant-window-bottom','橱窗下层盆栽',[(1255,619),(1228,581),(1239,548),(1254,528),(1273,517),(1292,542),(1307,527),(1328,530),(1320,558),(1337,575),(1310,601),(1300,623),(1290,658),(1254,661)])
add('plant-window-right','橱窗右侧盆栽',[(1479,661),(1464,630),(1450,606),(1459,578),(1477,590),(1483,548),(1496,521),(1509,538),(1503,568),(1523,580),(1513,603),(1521,624),(1505,663),(1507,716),(1481,718)])
add('ivy-upper-left','左上攀援植物',[(45,241),(56,173),(102,144),(124,104),(100,85),(110,30),(175,5),(253,0),(332,0),(358,49),(325,77),(305,102),(278,84),(283,42),(224,28),(208,81),(185,142),(139,169),(121,202),(77,209),(66,244)])
add('ivy-left-wall','左墙攀援植物',[(411,0),(477,0),(524,25),(526,74),(495,124),(479,159),(500,195),(508,227),(537,250),(547,276),(526,291),(487,305),(474,319),(464,350),(468,381),(449,413),(439,452),(429,494),(461,522),(488,548),(493,579),(474,606),(448,610),(437,583),(408,610),(372,602),(374,554),(391,523),(412,500),(411,448),(400,413),(412,374),(401,345),(415,307),(438,288),(445,263),(429,229),(439,194),(422,163),(410,129),(427,104),(416,75),(437,48),(410,30)])
add('ivy-center','中墙攀援植物',[(565,67),(602,72),(618,100),(634,140),(660,144),(682,182),(721,207),(727,230),(705,270),(689,294),(671,285),(653,262),(625,250),(596,268),(567,282),(562,253),(577,226),(554,199),(565,171),(581,151),(559,126)])
add('ivy-high-back','高处后墙攀援植物',[(696,0),(734,0),(737,36),(723,60),(733,93),(727,139),(707,144),(704,102),(687,74),(693,44)])
add('ivy-back-right','后墙右侧攀援植物',[(782,139),(809,147),(819,176),(806,213),(810,244),(791,260),(786,211)])
add('ivy-under-canopy','篷下后墙攀援植物',[(600,385),(631,397),(646,429),(669,433),(684,453),(722,448),(734,478),(746,525),(739,564),(711,578),(705,550),(694,531),(714,511),(694,484),(673,490),(656,465),(643,466),(630,496),(619,522),(603,517),(612,484),(596,455),(607,428)])
add('ivy-left-under','左侧篷下攀援植物',[(488,490),(519,490),(540,507),(530,537),(548,551),(539,583),(511,584),(499,554),(481,542)])
add('ivy-window-back','后方窗下植物',[(822,329),(825,301),(846,280),(846,259),(867,261),(874,278),(894,263),(914,277),(918,301),(905,318),(890,338),(852,335)])
add('building-right','右侧建筑与橱窗',[(1136,0),(1536,0),(1536,852),(1346,850),(1346,652),(1283,651),(1283,850),(1127,834),(1131,284),(1080,327),(1050,348),(977,342),(977,316)])
add('building-left','左侧建筑墙面与排水管',[(0,0),(686,0),(687,299),(600,260),(464,317),(432,478),(423,613),(411,849),(0,849)])
add('building-back','巷内建筑',[(686,0),(1136,0),(977,316),(1033,345),(1045,462),(1129,377),(1128,835),(1087,834),(1080,612),(1020,598),(982,587),(948,576),(902,577),(892,612),(817,617),(792,579),(769,579),(765,460),(709,441),(682,412),(690,297)])
add('pavement','街道路面与排水口',[(0,847),(419,849),(819,854),(829,720),(896,721),(923,794),(1021,850),(1125,836),(1283,852),(1283,943),(1349,943),(1347,850),(1536,851),(1536,1024),(0,1024)],'ground')
# Fallback closes tiny gaps; all original lines are assigned exactly once.
add('architecture-detail','建筑边缘细节',[(0,0),(1536,0),(1536,1024),(0,1024)])
def inside(x,y,poly):
 hit=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
 return hit
root=ET.parse(source).getroot();groups={r['id']:[] for r in regions}
for i,line in enumerate(root.findall('.//{http://www.w3.org/2000/svg}line')):
 attrs=dict(line.attrib);x=(float(attrs['x1'])+float(attrs['x2']))/2;y=(float(attrs['y1'])+float(attrs['y2']))/2
 region=next(r for r in regions if inside(x,y,r['polygon']))
 attrs['id']=f'line-{i+1}';attrs['data-line']=str(i+1)
 groups[region['id']].append('<line '+' '.join(f'{k}="{html.escape(v)}"' for k,v in attrs.items())+'/>')
# Keep the original boundary priority while sharing one target for each larger object.
merge_specs=[
 ('canopy','遮阳篷与全部支撑杆',['awning','pole-left','pole-right','pole-back']),
 ('left-scene','左墙与中景细节',['building-left','architecture-detail']),
 ('contact-panels','墙框',['contact-panels-upper','contact-panels-lower']),
 ('right-architecture','右侧与中景建筑',['building-right','building-back']),
 ('left-plants','左侧与中景攀援植物',[r['id'] for r in regions if r['id'].startswith('ivy-')]),
 ('hanging-fruit','悬挂水果',[r['id'] for r in regions if r['id'].startswith('bananas-')]),
 ('stall-fruit','水果摊全部水果',[r['id'] for r in regions if r['id'].startswith('fruit-')]),
 ('stall-racks','水果摊展示架',[r['id'] for r in regions if r['id'].startswith('rack-')]),
]
lookup={old:(key,name) for key,name,members in merge_specs for old in members}
hit_regions=[];merged={};merged_groups={}
for r in regions:
 key,name=lookup.get(r['id'],(r['id'],r['name']))
 hit_regions.append(dict(id=key,polygon=r['polygon']))
 if key not in merged:
  merged[key]=dict(id=key,name=name,polygon=[],kind=r['kind'],sourceParts=[])
  merged_groups[key]=[]
 merged[key]['polygon']+=r['polygon']
 merged[key]['sourceParts'].append(r['name'])
 merged_groups[key]+=groups[r['id']]
regions=list(merged.values());groups=merged_groups
def texture(key,items):
 pattern='dots' if key=='left-plants' or key.startswith('plant-') else 'vertical' if key in ('left-scene','right-architecture','bollard','contact-panels') else 'scattered' if key in ('hanging-fruit','stall-fruit','stall-racks') else 'horizontal'
 if pattern=='horizontal':return ''.join(items),pattern
 shapes=[];dot_carry=0.0
 for text in items:
  a=ET.fromstring(text).attrib
  x1,y1,x2,y2=(float(a[k]) for k in ('x1','y1','x2','y2'))
  length=math.hypot(x2-x1,y2-y1);count=max(1,round(length/({'dots':3.2,'vertical':4.0,'scattered':4.0}[pattern])))
  # Match each original stroke's ink area, including its round end caps.
  body_length=max(.1,(length*1.55+math.pi*.775**2)/count/1.55-math.pi*.775**2/1.55)
  if pattern=='dots':
   desired=(length*1.55+math.pi*.775**2)/(math.pi*1.25**2)+dot_carry
   count=max(1,min(max(1,int((length+1.55)/2.5)),round(desired)))
   dot_carry=desired-count
  rng=random.Random(int(a['data-line']))
  for j in range(count):
   t=(j+.5)/count;x=x1+(x2-x1)*t;y=y1+(y2-y1)*t
   attrs=f'id="{a["id"]}-{j}" data-line="{a["data-line"]}"'
   if pattern=='dots':
    radius=1.25
    inset=max(0,radius-.775)
    t=.5 if count==1 else (inset+(length-2*inset)*j/(count-1))/max(.001,length)
    x=x1+(x2-x1)*t;y=y1+(y2-y1)*t
    shapes.append(f'<circle {attrs} cx="{x:.3f}" cy="{y:.3f}" r="{radius:.3f}"/>')
   elif pattern=='vertical':
    half=body_length/2
    shapes.append(f'<line {attrs} x1="{x:.3f}" y1="{max(0,y-half):.3f}" x2="{x:.3f}" y2="{min(1024,y+half):.3f}"/>')
   else:
    angle=rng.uniform(-math.pi,math.pi);segment=body_length;dx=math.cos(angle)*segment/2;dy=math.sin(angle)*segment/2
    # Keep marks within the original segment's narrow strip; avoid filling blank object interiors.
    y+=rng.uniform(-.15,.15)
    lo,hi=min(x1,x2),max(x1,x2)
    shapes.append(f'<line {attrs} x1="{max(lo,min(hi,x-dx)):.3f}" y1="{max(0,min(1024,y-dy)):.3f}" x2="{max(lo,min(hi,x+dx)):.3f}" y2="{max(0,min(1024,y+dy)):.3f}"/>')
 return ''.join(shapes),pattern
english_names={'contact-panels':'Wall panels','bollard':'Street bollard','canopy':'Canopy and supports','hanging-fruit':'Hanging fruit','stall-fruit':'Fruit display','stall-racks':'Fruit display racks','plant-alley':'Alley plant','plant-window-top':'Upper window plant','plant-window-bottom':'Lower window plant','plant-window-right':'Right window plant','left-plants':'Climbing plants','right-architecture':'Right and middle buildings','left-scene':'Left wall and middle details','pavement':'Pavement and drain'}
for r in regions:
 r['name']=english_names[r['id']]
 r.pop('sourceParts',None)
# Merge interaction targets after creating each part's original texture.
home_specs=[
 ('architecture','Left shopfront',['left-scene'],'object'),
 ('right-shopfront','Right shopfront',['right-architecture'],'object'),
 ('street','Street and bollard',['pavement','bollard'],'ground'),
 ('plants','Plants',['plant-alley','plant-window-top','plant-window-bottom','plant-window-right','left-plants','contact-panels'],'object'),
 ('fruit-stall','Fruit stall',['canopy','hanging-fruit','stall-fruit','stall-racks'],'object'),
]
home_lookup={member:key for key,name,members,kind in home_specs for member in members}
assert set(home_lookup)=={r['id'] for r in regions}
textured={r['id']:texture(r['id'],groups[r['id']])[0] for r in regions}
old_regions=regions
regions=[];parts=[]
for key,name,members,kind in home_specs:
 selected=[r for r in old_regions if r['id'] in members]
 points=[point for r in selected for point in r['polygon']]
 cx=sum(point[0] for point in points)/len(points);cy=sum(point[1] for point in points)/len(points)
 record=dict(id=key,name=name,polygon=points,kind=kind,lineCount=sum(len(groups[r['id']]) for r in selected),pattern='mixed')
 regions.append(record)
 marks=''.join(textured[r['id']] for r in reversed(old_regions) if r['id'] in members)
 parts.append(f'<g id="{key}" class="object" data-name="{name}" style="transform-origin:{cx}px {cy}px"><title>{name}</title>'+marks+'</g>')
for region in hit_regions:region['id']=home_lookup[region['id']]
contact_markup='<g class="contact-details" aria-label="Rye Lane research project" style="font-family:Arial,sans-serif;fill:#111;stroke:none"><text x="32" y="340" font-size="32" font-weight="800" letter-spacing="-.7">RYE</text><text x="32" y="376" font-size="32" font-weight="800" letter-spacing="-.7">LANE</text><text x="32" y="404" font-size="11">Shopfronts &amp;</text><text x="32" y="420" font-size="11">everyday life</text><text x="32" y="565" font-size="8" fill="#666">A project by</text><text x="32" y="586" font-size="10">Caiyi Jiang</text><a href="#project-contact" aria-label="Contact Caiyi Jiang"><text x="32" y="620" font-size="10">Contact ↗</text></a></g>'
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" role="img" tabindex="0" aria-label="Market scene. Scroll or pinch to zoom, drag to pan, press 0 for the full scene, or Escape to return to the contact view."><rect width="1536" height="1024" fill="white"/>'+''.join(parts)+contact_markup+'</svg>'
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Everyday Visibility and Publicness of Shopfronts</title><style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#fff;overscroll-behavior:none}svg{display:block;position:fixed;inset:0;width:100vw;height:100dvh;overflow:hidden;touch-action:none;outline:none}#macro{position:fixed;inset:0;width:100vw;height:100dvh;pointer-events:none;display:none}svg.macro .object{visibility:hidden}.object{pointer-events:none;will-change:auto}.object line{fill:none;stroke:#1a1a1a;stroke-width:1.55;stroke-linecap:round}.object.active line{stroke:#008a52;stroke-width:1.9}.object circle{fill:#1a1a1a;stroke:none}.object.active circle{fill:#008a52}.object.active{will-change:transform}.object{transition:color .15s} 
#title-overlay{position:fixed;inset:0;z-index:2;pointer-events:none;opacity:0;color:#000;font-family:Arial,sans-serif}#title-overlay .location{position:absolute;top:12%;left:0;width:100%;text-align:center;font-size:clamp(12px,1.4vw,18px);font-weight:500;letter-spacing:.18em}#title-overlay h1{position:absolute;left:5%;top:50%;transform:translateY(-50%);width:90%;margin:0;text-align:center;font-size:clamp(32px,min(8.5vw,13.5vh),128px);line-height:1.18;font-weight:600;letter-spacing:-.025em}#paper-link{display:block;text-decoration:none;color:inherit;pointer-events:none;cursor:pointer}#paper-link:focus-visible{outline:2px solid #008a52;outline-offset:14px}#paper-link:hover{--title-ink:#008a52}.title-line{display:block;color:#000;background:none;-webkit-text-fill-color:#000} @media(max-width:540px){#title-overlay h1{font-size:clamp(26px,7.7vw,44px)}}
html.reading-ready{overflow-y:auto;scrollbar-width:none}html.reading-ready::-webkit-scrollbar{display:none}body.reading-ready{height:200dvh;overflow:visible}body>svg,#macro,#title-overlay{transform:translateY(calc(-1 * var(--page-scroll,0px)))}#paper{position:absolute;top:100dvh;left:0;width:100%;height:auto;min-height:100dvh;visibility:hidden}body.reading-ready #paper{visibility:visible}#paper iframe{width:100%;height:100%;border:0;display:block;background:#fff;pointer-events:auto}body.in-paper #paper iframe{pointer-events:auto}#reading-cue{position:absolute;bottom:5%;left:0;width:100%;text-align:center;font:11px Arial,sans-serif;letter-spacing:.12em;color:#555}
</style><style>#reading-navigation{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:20px 5vw;border-bottom:1px solid #eee;background:rgba(255,255,255,.98);color:#161616;font:12px Arial,sans-serif}#reading-navigation[hidden]{display:none}#reading-navigation a{color:inherit;text-decoration:none;pointer-events:auto}#reading-navigation a:hover{color:#008a52}@media(max-width:600px){#reading-navigation{padding:17px 22px}#reading-navigation span{display:none}}</style><style>.contact-details{pointer-events:auto}.contact-details a{cursor:pointer}.contact-details a:hover text,.contact-details a:focus text{fill:#008a52;text-decoration:underline}svg.macro .contact-details{visibility:hidden}</style><style>#project-contact{position:fixed;width:min(330px,calc(100vw - 40px));padding:32px;border:1px solid #ddd;border-radius:18px;background:#fff;color:#222;font:14px/1.6 Arial,sans-serif}#project-contact::backdrop{background:#0003}#project-contact h2{margin:0 0 22px;font:500 22px/1.2 Arial,sans-serif}#project-contact a{display:block;margin:10px 0;color:inherit;text-decoration:none}#project-contact a:hover{text-decoration:underline}#project-contact p{margin:10px 0}#project-contact .contact-close{position:absolute;right:10px;top:8px;width:30px;height:30px;padding:0;border:0;background:none;font:24px Arial,sans-serif;color:#333;cursor:pointer}</style></head><body>'''+svg+'''<canvas id="macro" aria-hidden="true"></canvas><div id="title-overlay" aria-hidden="true"><div class="location morph-text">RYE LANE</div><h1><a id="paper-link" href="#paper" tabindex="-1" aria-label="Read The Everyday Visibility and Publicness of Shopfronts"><span class="title-line morph-text">THE EVERYDAY</span><span class="title-line morph-text">VISIBILITY AND</span><span class="title-line morph-text">PUBLICNESS OF</span><span class="title-line morph-text">SHOPFRONTS</span></a></h1><div id="reading-cue">Scroll down to read</div></div><dialog id="project-contact" aria-labelledby="project-contact-title"><button type="button" class="contact-close" aria-label="Close contact details">×</button><h2 id="project-contact-title">Caiyi Jiang</h2><a href="mailto:kaittyzii@gmail.com">kaittyzii@gmail.com</a><a href="https://www.instagram.com/kaittyi/" target="_blank" rel="noopener noreferrer">Instagram · @kaittyi ↗</a><p>WeChat · Turmeriv</p></dialog><section id="paper" aria-label="Research paper"><iframe src="paper.html" title="The Everyday Visibility and Publicness of Shopfronts research paper" loading="lazy"></iframe></section><script>
const hitRegions=HITREGIONS;
const regions=REGIONS,svg=document.querySelector('svg'),objects=new Map(regions.map(r=>[r.id,document.getElementById(r.id)])),reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function inside(p,poly){let hit=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>p.y)!=(b[1]>p.y)&&p.x<(b[0]-a[0])*(p.y-a[1])/(b[1]-a[1])+a[0])hit=!hit}return hit}
let current=null,animation=null,frame=0,pointer=null;
function activate(id){if(id===current)return;if(animation){animation.cancel();animation=null}if(current)objects.get(current).classList.remove('active');current=id;if(typeof scheduleHoverCard==='function')scheduleHoverCard(id);if(typeof chaos!=='undefined'&&chaos>.00001)paintMacro();if(!id){svg.style.cursor='default';return}const el=objects.get(id);el.classList.add('active');svg.style.cursor='pointer';const ground=regions.find(r=>r.id===id).kind==='ground';animation=el.animate(reduced?[{opacity:.7},{opacity:1}]:[{transform:'translate(0px,0px) scale(1)'},{transform:`translate(0px,${ground?-2:-9}px) scale(${ground?1:1.012})`,offset:.48},{transform:`translate(0px,${ground?-1:-6}px) scale(${ground?1:1.008})`}],{duration:420,fill:'forwards',easing:'cubic-bezier(.2,.8,.3,1)'});}
function detect(){frame=0;if(typeof drag!=='undefined'&&drag){activate(null);return}if(typeof chaos!=='undefined'&&chaos>0){activate(null);return}const m=svg.getScreenCTM();if(!m||!pointer)return;const p=new DOMPoint(pointer.x,pointer.y).matrixTransform(m.inverse());if(p.x<0||p.y<0||p.x>1536||p.y>1024){activate(null);return}const r=hitRegions.find(r=>inside(p,r.polygon));activate(r?.id||null)}
svg.addEventListener('pointermove',e=>{pointer={x:e.clientX,y:e.clientY};if(!frame)frame=requestAnimationFrame(detect)});svg.addEventListener('pointerleave',()=>{pointer=null;activate(null)});svg.addEventListener('pointerdown',e=>{pointer={x:e.clientX,y:e.clientY};detect()});svg.addEventListener('pointercancel',()=>activate(null));svg.addEventListener('pointerup',e=>{if(e.pointerType!=='mouse')activate(null)});window.addEventListener('blur',()=>activate(null));
const contactDialog=document.querySelector('#project-contact');
svg.querySelector('a[href="#project-contact"]').addEventListener('click',e=>{e.preventDefault();activate(null);hideHoverPhoto();contactDialog.showModal()});
contactDialog.querySelector('.contact-close').addEventListener('click',()=>contactDialog.close());
contactDialog.addEventListener('click',e=>{if(e.target===contactDialog){const r=contactDialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)contactDialog.close()}});

// Contact links do not initiate scene dragging or photo-card hovers.
for(const eventType of ['pointermove','pointerdown','pointerup'])svg.addEventListener(eventType,e=>{if(e.target.closest('.contact-details a')){e.stopPropagation();pointer=null;activate(null);if(typeof hideHoverPhoto==='function')hideHoverPhoto()}},{capture:true});
CAMERA
</script></body></html>'''.replace('CAMERA',Path(__file__).with_name('camera.js').read_text()+'\n'+Path(__file__).with_name('hover-cards.js').read_text().replace('CARD_RECORDS',json.dumps(json.loads((Path(__file__).resolve().parent.parent/'hover-cards.json').read_text()),ensure_ascii=False))).replace('HITREGIONS',json.dumps(hit_regions,ensure_ascii=False)).replace('REGIONS',json.dumps(regions,ensure_ascii=False))
from optimize_assets import main_page
page=main_page(page)
design_css=Path(__file__).with_name('user-settings').joinpath('design.css').read_text()
page=page.replace('</head>','<style>'+design_css+'</style></head>')
page=page.replace('</body>','<script src="source/font-settings.js"></script></body>')
out=Path(__file__).resolve().parent.parent;(out/'index.html').write_text(page);(out/'object-regions.json').write_text(json.dumps(dict(objects=regions,hitRegions=hit_regions),ensure_ascii=False,indent=2))
print('Objects:',len(regions),'Lines:',sum(r['lineCount'] for r in regions));print('\n'.join(r['name']+': '+str(r['lineCount']) for r in regions))
