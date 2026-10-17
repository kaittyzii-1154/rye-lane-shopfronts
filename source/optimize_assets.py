import xml.etree.ElementTree as E
import json,math
NS='{http://www.w3.org/2000/svg}'
E.register_namespace('','http://www.w3.org/2000/svg')
def f(x):return str(round(float(x),4))
def segment(e):
 a=e.attrib;x1,y1,x2,y2=[float(a[k]) for k in ('x1','y1','x2','y2')]
 return 'M'+f(x1)+' '+f(y1)+('h'+f(x2-x1) if y1==y2 else 'v'+f(y2-y1) if x1==x2 else 'L'+f(x2)+' '+f(y2))
def compact(root):
 count=0
 for parent in list(root.iter()):
  batches={}
  for e in list(parent):
   if e.tag!=NS+'line':continue
   attrs=tuple(sorted((k,v) for k,v in e.attrib.items() if k not in ('x1','y1','x2','y2','id','data-line')))
   batches.setdefault(attrs,[]).append(segment(e));parent.remove(e);count+=1
  for attrs,commands in batches.items():E.SubElement(parent,NS+'path',dict(attrs,d=''.join(commands)))
 return count

def main_page(page):
 start=page.index('<svg');end=page.index('</svg>',start)+6;root=E.fromstring(page[start:end]);marks=[]
 for group in root.findall(NS+'g'):
  dots=[]
  for e in list(group):
   if e.tag not in (NS+'line',NS+'circle'):continue
   a=e.attrib
   if e.tag==NS+'circle':
    x,y,r=[float(a[k]) for k in ('cx','cy','r')];length=angle=0
    dots.append(f'M{f(x-r)} {f(y)}a{f(r)} {f(r)} 0 1 0 {f(r*2)} 0a{f(r)} {f(r)} 0 1 0 {f(-r*2)} 0');group.remove(e)
   else:
    x1,y1,x2,y2=[float(a[k]) for k in ('x1','y1','x2','y2')];x=(x1+x2)/2;y=(y1+y2)/2;r=0;length=math.hypot(x2-x1,y2-y1);angle=math.atan2(y2-y1,x2-x1)
   marks.append([round(v,4) for v in (x,y,length,angle,r)]+[group.get('id')])
  if dots:E.SubElement(group,NS+'path',{'d':''.join(dots),'class':'dot-marks'})
 compact(root)
 page=page[:start]+E.tostring(root,encoding='unicode')+page[end:]
 page=page.replace('MARK_DATA',json.dumps(marks,separators=(',',':')))
 css='<style>.object path:not(.dot-marks){fill:none;stroke:#1a1a1a;stroke-width:1.55;stroke-linecap:round}.object.active path:not(.dot-marks){stroke:#008a52;stroke-width:1.9}.object .dot-marks{fill:#1a1a1a;stroke:none}.object.active .dot-marks{fill:#008a52}</style>'
 return page.replace('</head>',css+'</head>')
