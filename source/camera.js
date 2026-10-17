// Full-window camera. Zoom 1 fits the complete source drawing.
const canvas=document.querySelector('#macro'),ctx=canvas.getContext('2d');
let viewport={w:innerWidth,h:innerHeight},fit=1;
const camera={x:730,y:625,z:2.25},target={...camera};
let cameraFrame=0,drag=null,pinch=null,chaos=0,reverseScroll=false;
const touches=new Map();
function hash(n){const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v)}
const marks=MARK_DATA.map((m,i)=>{const [x,y,length,angle,r,group]=m;return{x,y,length,angle,r,group,dx:(hash(i+1)-.5)*64,dy:(hash(i+15001)-.5)*64,da:(hash(i+30001)-.5)*Math.PI*3,stretch:hash(i+45001)}});
// Keep the drawing covering the viewport at its widest zoom.
function minimumZoom(){return Math.max(viewport.w/1536,viewport.h/1024)/fit}
function clampCamera(c){c.z=Math.max(minimumZoom(),Math.min(16,c.z));const hw=viewport.w/(2*fit*c.z),hh=viewport.h/(2*fit*c.z);c.x=hw>=768?768:Math.max(hw,Math.min(1536-hw,c.x));c.y=hh>=512?512:Math.max(hh,Math.min(1024-hh,c.y))}
const titleOverlay=document.querySelector('#title-overlay'),titleLink=document.querySelector('#paper-link');
let textTargets=[],macroSources=[],macroMode=false;
function smooth(a,b,value){const t=Math.max(0,Math.min(1,(value-a)/(b-a)));return t*t*(3-2*t)}
function makeTextTargets(){
 const buffer=document.createElement('canvas');buffer.width=viewport.w;buffer.height=viewport.h;
 const ink=buffer.getContext('2d',{willReadFrequently:true});ink.fillStyle='#000';ink.textAlign='center';ink.textBaseline='middle';
 for(const row of document.querySelectorAll('.morph-text')){const rect=row.getBoundingClientRect(),style=getComputedStyle(row);ink.font=`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;ink.fillText(row.textContent,rect.x+rect.width/2,rect.y+rect.height/2+window.scrollY)}
 const data=ink.getImageData(0,0,buffer.width,buffer.height).data;
 const spacing=Math.max(3,Math.min(viewport.w,viewport.h)/190);textTargets=[];
 for(let y=1;y<viewport.h;){const step=(y<viewport.h*.2||y>viewport.h*.78)?Math.min(2.1,spacing):spacing;for(let x=step/2;x<viewport.w;x+=step){if(data[(Math.floor(y)*buffer.width+Math.floor(x))*4+3]>150)textTargets.push({x,y,size:step})}y+=step}
 // Stable order makes the transition reversible instead of re-randomising on every wheel event.
 textTargets.sort((a,b)=>hash(a.x*13+a.y*17)-hash(b.x*13+b.y*17));
}
function captureMacroSources(){
 const scale=fit*3.3;macroSources=[];
 for(const m of marks){const x=(m.x-camera.x)*scale+viewport.w/2,y=(m.y-camera.y)*scale+viewport.h/2;if(x< -50||x>viewport.w+50||y< -50||y>viewport.h+50)continue;macroSources.push({...m,sx:x,sy:y,screenLength:m.length*scale,screenRadius:m.r*scale})}
 if(!macroSources.length)macroSources=marks.slice(0,100).map(m=>({...m,sx:viewport.w/2,sy:viewport.h/2,screenLength:4,screenRadius:2}));
}
function paintMacro(){
 const dpr=Math.min(devicePixelRatio||1,2);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,viewport.w,viewport.h);
 const scatter=smooth(3.3,5.4,camera.z),reading=smooth(5.1,10,camera.z);
 document.body.dataset.text=reading.toFixed(3);
 const solid=reading>=1?1:0;titleOverlay.style.opacity=solid;canvas.style.opacity=1-solid;const enabled=reading>=1;titleLink.style.pointerEvents=enabled?'auto':'none';titleLink.tabIndex=enabled?0:-1;titleOverlay.setAttribute('aria-hidden',enabled?'false':'true');setReadingReady(enabled);
 if(reading>=1)return;
 ctx.lineCap='round';ctx.strokeStyle='#000';
 // Macro space stops following individual objects. Its scale stays constant while marks reorganise.
 ctx.lineWidth=(1.55*fit*3.3)*(1-reading)+Math.max(3,Math.min(viewport.w,viewport.h)/190)*1.08*reading;
 const count=Math.max(macroSources.length,textTargets.length);
 ctx.beginPath();
 for(let i=0;i<count;i++){
  const m=macroSources[i%macroSources.length],targetPoint=textTargets[i%textTargets.length];
  const sx=m.sx+m.dx*scatter*.8,sy=m.sy+m.dy*scatter*.8;
  const x=sx+(targetPoint.x-sx)*reading,y=sy+(targetPoint.y-sy)*reading;
  const sourceAngle=m.angle+m.da*scatter,targetAngle=0;
  const angle=sourceAngle+(targetAngle-sourceAngle)*reading;
  const sourceLength=m.r?scatter*5:m.screenLength*(1+scatter*.5);
  const length=sourceLength+(targetPoint.size*1.05-sourceLength)*reading;
  const sourceWidth=m.r?m.screenRadius*2:1.55*fit*3.3;
  // Repeated seeds overlap initially, then unfold into separate characters.
  ctx.moveTo(x-Math.cos(angle)*length/2,y-Math.sin(angle)*length/2);ctx.lineTo(x+Math.cos(angle)*length/2+.001,y+Math.sin(angle)*length/2);
 }
 ctx.stroke();
}

function renderCamera(){
 const w=viewport.w/(fit*camera.z),h=viewport.h/(fit*camera.z);
 svg.setAttribute('viewBox',`${camera.x-w/2} ${camera.y-h/2} ${w} ${h}`);
 const t=Math.max(0,Math.min(1,(camera.z-3.3)/5));chaos=t*t*(3-2*t);
 if(chaos>0&&!macroMode){macroMode=true;activate(null);makeTextTargets();captureMacroSources()}
 if(chaos===0){macroMode=false;document.body.dataset.text='0.000';titleOverlay.style.opacity=0;titleLink.style.pointerEvents='none';titleLink.tabIndex=-1;titleOverlay.setAttribute('aria-hidden','true');canvas.style.opacity=1;setReadingReady(false)}
 svg.setAttribute('aria-label',chaos>0?'Rye Lane. The Everyday Visibility and Publicness of Shopfronts. Scroll down to read the paper, or zoom out to return to the street.':'Market scene. Scroll or pinch to zoom, drag to pan, press 0 for the full scene, or Escape to return to the fruit stall.')
 document.body.dataset.zoom=camera.z.toFixed(2);document.body.dataset.chaos=chaos.toFixed(3);
 canvas.style.display=chaos>0?'block':'none';svg.classList.toggle('macro',chaos>0);
 if(chaos>0)paintMacro();
}
function stepCamera(){
 cameraFrame=0;let moving=false;
 for(const k of ['x','y','z']){const delta=target[k]-camera[k];if(Math.abs(delta)>(k==='z'?.0005:.03)){camera[k]+=delta*(reduced?1:.15);moving=true}else camera[k]=target[k]}
 clampCamera(camera);renderCamera();if(pointer&&!drag)detect();if(moving)cameraFrame=requestAnimationFrame(stepCamera);
}
function scheduleCamera(){if(!cameraFrame)cameraFrame=requestAnimationFrame(stepCamera)}
function resizeCamera(){viewport={w:innerWidth,h:innerHeight};fit=Math.min(viewport.w/1536,viewport.h/1024);const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(viewport.w*dpr);canvas.height=Math.round(viewport.h*dpr);clampCamera(camera);clampCamera(target);if(macroMode){makeTextTargets();captureMacroSources()}renderCamera()}
function zoomAt(z,x=viewport.w/2,y=viewport.h/2){
 z=Math.max(minimumZoom(),Math.min(16,z));const worldX=target.x+(x-viewport.w/2)/(fit*target.z),worldY=target.y+(y-viewport.h/2)/(fit*target.z);
 target.x=worldX-(x-viewport.w/2)/(fit*z);target.y=worldY-(y-viewport.h/2)/(fit*z);target.z=z;clampCamera(target);scheduleCamera();
}
window.addEventListener('wheel',e=>{const delta=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?viewport.h:1);if(window.scrollY>0||(readingReady&&delta>0&&!e.ctrlKey))return;e.preventDefault();if(readingReady&&delta<0&&!e.ctrlKey)reverseScroll=true;const direction=reverseScroll&&!e.ctrlKey?delta:-delta;zoomAt(target.z*Math.exp(Math.max(-120,Math.min(120,direction))*.0025),e.clientX,e.clientY)},{passive:false});
svg.addEventListener('pointerdown',e=>{
 svg.setPointerCapture(e.pointerId);touches.set(e.pointerId,{x:e.clientX,y:e.clientY});
 drag={x:e.clientX,y:e.clientY,moved:false};
 if(touches.size===2){const pts=[...touches.values()];pinch={distance:Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y),z:target.z};drag=null}
});
svg.addEventListener('pointermove',e=>{
 if(!touches.has(e.pointerId))return;touches.set(e.pointerId,{x:e.clientX,y:e.clientY});
 if(touches.size===2&&pinch){const pts=[...touches.values()],distance=Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y);zoomAt(pinch.z*distance/Math.max(1,pinch.distance),(pts[0].x+pts[1].x)/2,(pts[0].y+pts[1].y)/2);return}
 if(drag){const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>1)drag.moved=true;target.x-=dx/(fit*camera.z);target.y-=dy/(fit*camera.z);drag.x=e.clientX;drag.y=e.clientY;clampCamera(target);scheduleCamera()}
});
function releasePointer(e){touches.delete(e.pointerId);drag=null;pinch=null;if(svg.hasPointerCapture(e.pointerId))svg.releasePointerCapture(e.pointerId)}
svg.addEventListener('pointerup',releasePointer);svg.addEventListener('pointercancel',releasePointer);
window.addEventListener('resize',resizeCamera);
window.addEventListener('keydown',e=>{
 if(window.scrollY>1)return;
 if(readingReady&&['ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();enterReading();return}
 if(['+','=','-','0','Home','Escape','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))e.preventDefault();
 if(e.key==='+'||e.key==='=')zoomAt(target.z*1.25);if(e.key==='-')zoomAt(target.z/1.25);
 if(e.key==='0'||e.key==='Home'){Object.assign(target,{x:768,y:512,z:minimumZoom()});clampCamera(target);scheduleCamera()}
 if(e.key==='Escape'){Object.assign(target,{x:730,y:625,z:2.25});clampCamera(target);scheduleCamera()}
 const moves={ArrowUp:[0,-60],ArrowDown:[0,60],ArrowLeft:[-60,0],ArrowRight:[60,0]};if(moves[e.key]){target.x+=moves[e.key][0]/(fit*camera.z);target.y+=moves[e.key][1]/(fit*camera.z);clampCamera(target);scheduleCamera()}
});
if('scrollRestoration' in history)history.scrollRestoration='manual';
let readingReady=false,paperHeight=innerHeight;
const readingSection=document.querySelector('#paper'),paperFrame=readingSection.querySelector('iframe');
function setReadingReady(value){if(value===readingReady)return;readingReady=value;document.documentElement.classList.toggle('reading-ready',value);document.body.classList.toggle('reading-ready',value);readingSection.setAttribute('aria-hidden',value?'false':'true');document.body.style.height=value?(innerHeight+paperHeight)+'px':'';if(!value&&window.scrollY)window.scrollTo(0,0)}
// This navigation belongs to the outer page so it stays clickable while the iframe scrolls.
const readingNav=document.createElement('nav');
readingNav.id='reading-navigation';readingNav.setAttribute('aria-label','Research paper navigation');
readingNav.innerHTML='<a href="index.html?start=street">← Back to street</a><span>RYE LANE / RESEARCH PAPER</span><a href="scenes.html">Other scenes ↗</a>';
readingNav.hidden=true;document.body.append(readingNav);
function syncReadingScroll(){document.body.style.setProperty('--page-scroll',`${window.scrollY}px`);const inPaper=readingReady&&window.scrollY>=innerHeight-2;document.body.classList.toggle('in-paper',inPaper);readingNav.hidden=!inPaper}
function enterReading(){if(readingReady)window.scrollTo({top:innerHeight,behavior:reduced?'instant':'smooth'})}
titleLink.addEventListener('click',e=>{e.preventDefault();enterReading()});
window.addEventListener('scroll',syncReadingScroll,{passive:true});
window.addEventListener('resize',syncReadingScroll);
// Expand each chapter to its content height; the outer page owns scrolling.
function measurePaper(){try{const doc=paperFrame.contentDocument;if(!doc?.body)return;const height=Math.max(innerHeight,Math.ceil(doc.body.getBoundingClientRect().height+140));if(Math.abs(height-paperHeight)>2){paperHeight=height;paperFrame.style.height=height+'px'}if(readingReady)document.body.style.height=(innerHeight+paperHeight)+'px'}catch{}}
let paperObserver=null;
paperFrame.addEventListener('load',()=>{const frame=paperFrame.contentWindow;paperObserver?.disconnect();paperFrame.style.height=innerHeight+'px';measurePaper();paperObserver=new ResizeObserver(measurePaper);paperObserver.observe(frame.document.body);if(window.scrollY>innerHeight)window.scrollTo({top:innerHeight,behavior:'instant'});frame.addEventListener('wheel',e=>{if(!e.ctrlKey){e.preventDefault();window.scrollBy({top:e.deltaY*(e.deltaMode===1?16:1),behavior:'instant'})}},{passive:false});frame.addEventListener('keydown',e=>{const delta={PageDown:innerHeight*.8,PageUp:-innerHeight*.8,' ':innerHeight*.8,ArrowDown:60,ArrowUp:-60}[e.key];if(delta!==undefined){e.preventDefault();window.scrollBy({top:e.shiftKey&&e.key===' '?-delta:delta,behavior:'instant'})}});});
window.addEventListener('resize',measurePaper);
let swipeStart=null;
svg.addEventListener('pointerdown',e=>{if(readingReady&&e.pointerType==='touch')swipeStart=e.clientY});
svg.addEventListener('pointerup',e=>{if(swipeStart!==null&&swipeStart-e.clientY>50)enterReading();swipeStart=null});
if(location.hash==='#title'||location.hash==='#paper'){Object.assign(camera,{x:730,y:625,z:10});Object.assign(target,camera)}
if(location.hash==='#street')window.scrollTo(0,0);
resizeCamera();
if(location.hash==='#paper')requestAnimationFrame(enterReading);
syncReadingScroll();

function resetStreet(){reverseScroll=false;window.scrollTo({top:0,behavior:'instant'});Object.assign(camera,{x:730,y:625,z:2.25});clampCamera(camera);Object.assign(target,camera);activate(null);renderCamera();syncReadingScroll();history.replaceState(null,'',location.pathname+'?start=street');}
window.addEventListener('hashchange',()=>{if(location.hash==='#street'||!location.hash)resetStreet()});
if(new URLSearchParams(location.search).get('start')==='street')resetStreet();
window.addEventListener('rye-fonts-change',()=>{if(macroMode){makeTextTargets();paintMacro()}});
