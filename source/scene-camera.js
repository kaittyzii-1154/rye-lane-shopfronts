const svg=document.querySelector('#scene-view svg'),regions=SCENE_REGIONS,view=SCENE_VIEW;
let current=null,pointer=null,chaos=0,z=1,cx=view[0]+view[2]/2,cy=view[1]+view[3]/2,drag=null;
let viewport={w:1,h:1},fit=1,pinch=null;
const touches=new Map();
function inside(p,poly){let hit=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>p.y)!=(b[1]>p.y)&&p.x<(b[0]-a[0])*(p.y-a[1])/(b[1]-a[1])+a[0])hit=!hit}return hit}
function activate(id){if(id===current)return;if(current)document.getElementById(current).classList.remove('active');current=id;if(id)document.getElementById(id).classList.add('active');scheduleHoverCard(id)}
function minimumZoom(){return Math.max(viewport.w/view[2],viewport.h/view[3])/fit}
function maximumZoom(){return SCENE_ZOOM_LIMIT?minimumZoom()*SCENE_ZOOM_LIMIT:Math.max(12,minimumZoom())}
function clampCamera(){z=Math.max(minimumZoom(),Math.min(maximumZoom(),z));const hw=viewport.w/(2*fit*z),hh=viewport.h/(2*fit*z);cx=Math.max(view[0]+hw,Math.min(view[0]+view[2]-hw,cx));cy=Math.max(view[1]+hh,Math.min(view[1]+view[3]-hh,cy))}
function draw(){clampCamera();const w=viewport.w/(fit*z),h=viewport.h/(fit*z);svg.setAttribute('viewBox',`${cx-w/2} ${cy-h/2} ${w} ${h}`)}
function resize(){const r=svg.getBoundingClientRect();viewport={w:Math.max(1,r.width),h:Math.max(1,r.height)};fit=Math.min(viewport.w/view[2],viewport.h/view[3]);draw()}
function reset(){z=minimumZoom();cx=view[0]+view[2]/2;cy=view[1]+view[3]/2;draw();activate(null)}
function detect(e){pointer={x:e.clientX,y:e.clientY};const m=svg.getScreenCTM();if(!m)return;const p=new DOMPoint(pointer.x,pointer.y).matrixTransform(m.inverse());activate(regions.find(r=>inside(p,r.polygon))?.id||null)}
function zoomAt(next,x,y){const rect=svg.getBoundingClientRect(),px=x-rect.left-viewport.w/2,py=y-rect.top-viewport.h/2,wx=cx+px/(fit*z),wy=cy+py/(fit*z);z=Math.max(minimumZoom(),Math.min(maximumZoom(),next));cx=wx-px/(fit*z);cy=wy-py/(fit*z);draw();activate(null)}
svg.addEventListener('pointermove',e=>{if(touches.has(e.pointerId))touches.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pinch&&touches.size===2){const [a,b]=[...touches.values()];zoomAt(pinch.z*Math.hypot(a.x-b.x,a.y-b.y)/pinch.distance,(a.x+b.x)/2,(a.y+b.y)/2);return}if(drag){cx-=(e.clientX-drag.x)/(fit*z);cy-=(e.clientY-drag.y)/(fit*z);drag={x:e.clientX,y:e.clientY};draw();return}detect(e)});
svg.addEventListener('pointerleave',()=>activate(null));
svg.addEventListener('pointerdown',e=>{svg.setPointerCapture(e.pointerId);touches.set(e.pointerId,{x:e.clientX,y:e.clientY});drag={x:e.clientX,y:e.clientY};activate(null);if(touches.size===2){const[a,b]=[...touches.values()];pinch={z,distance:Math.max(1,Math.hypot(a.x-b.x,a.y-b.y))};drag=null}});
function release(e){touches.delete(e.pointerId);pinch=null;drag=null;if(touches.size===1){const p=[...touches.values()][0];drag={...p}}if(!touches.size&&e.type==='pointerup')detect(e)}
svg.addEventListener('pointerup',release);svg.addEventListener('pointercancel',release);
svg.addEventListener('wheel',e=>{e.preventDefault();const delta=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?viewport.h:1);zoomAt(z*Math.exp(-Math.max(-120,Math.min(120,delta))*.002),e.clientX,e.clientY)},{passive:false});
svg.addEventListener('dblclick',reset);
window.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select'))return;if(e.key==='0'||e.key==='Home'){e.preventDefault();reset()}if(['+','=','-'].includes(e.key)){e.preventDefault();const r=svg.getBoundingClientRect();zoomAt(z*(e.key==='-'?.8:1.25),r.left+r.width/2,r.top+r.height/2)}});
window.addEventListener('resize',resize);resize();reset();
