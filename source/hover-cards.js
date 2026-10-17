const hoverRecords=CARD_RECORDS;
const hoverByRegion=new Map(hoverRecords.map(card=>[card.region,card]));
let hoverDelay=null,hoverClose=null,hoverLocked=false,shownPhoto=null;
const hoverStyle=document.createElement('style');hoverStyle.textContent=`
#hover-photo{position:fixed;z-index:10;width:min(340px,calc(100vw - 32px));height:290px;border-radius:9px;perspective:1100px;filter:drop-shadow(0 8px 20px #0002)}#hover-photo[hidden]{display:none}#hover-flip{padding:0;border:0;width:100%;height:100%;background:transparent;text-align:left;cursor:pointer;font-family:Arial,sans-serif;color:white;border-radius:9px;display:block}#hover-flip:focus-visible{outline:2px solid #008a52;outline-offset:4px}.photo-inner{display:block;position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform .55s cubic-bezier(.2,.7,.2,1)}#hover-photo.flipped .photo-inner{transform:rotateY(180deg)}.photo-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#000;border-radius:9px;overflow:hidden}.photo-front img{width:100%;height:100%;object-fit:cover;display:block}.photo-number{position:absolute;left:20px;top:20px;font-size:12px;letter-spacing:.12em}.photo-cue{position:absolute;bottom:20px;left:20px;font-size:11px;color:#bbb}.photo-back{transform:rotateY(180deg);padding:22px;display:flex;flex-direction:column;justify-content:center;gap:12px}.photo-back small{font-size:10px;letter-spacing:.1em;color:#aaa}.photo-back strong{font-size:18px;line-height:1.2;font-weight:500}.photo-back .story{font-size:13px;line-height:1.55}.photo-back .turn{font-size:10px;color:#aaa}#hover-close{position:absolute;right:9px;top:9px;z-index:3;color:white;background:#000;border:1px solid #555;width:27px;height:27px;cursor:pointer;font-size:17px}@media(prefers-reduced-motion:reduce){.photo-inner{transition:none}}
`;document.head.append(hoverStyle);
const hoverPhoto=document.createElement('aside');hoverPhoto.id='hover-photo';hoverPhoto.hidden=true;hoverPhoto.innerHTML='<button id="hover-close" aria-label="Close photo">×</button><button id="hover-flip" aria-label="Turn photo over" aria-pressed="false"><span class="photo-inner"><span class="photo-face photo-front"><img alt=""><span class="photo-number"></span><span class="photo-cue">Click to turn over</span></span><span class="photo-face photo-back"><small></small><strong></strong><span class="story"></span><span class="turn">Click to return to the photo</span></span></span></button>';document.body.append(hoverPhoto);
function hideHoverPhoto(){clearTimeout(hoverDelay);clearTimeout(hoverClose);hoverPhoto.hidden=true;hoverLocked=false;shownPhoto=null;}
function showHoverPhoto(record){
 if(chaos>0||window.scrollY>0)return;
 shownPhoto=record.id;hoverPhoto.classList.remove('flipped');hoverPhoto.querySelector('#hover-flip').setAttribute('aria-pressed','false');
 const img=hoverPhoto.querySelector('img');img.src=record.image;img.alt=`Photo ${record.id}: ${record.label}`;
 hoverPhoto.querySelector('.photo-number').textContent=`PHOTO ${record.id}`;
 hoverPhoto.querySelector('.photo-back small').textContent=`${record.id} / ${record.type}`;
 hoverPhoto.querySelector('.photo-back strong').textContent=record.title;hoverPhoto.querySelector('.story').textContent=record.text;
 hoverPhoto.setAttribute('aria-label',`Photo ${record.id} — ${record.label}`);hoverPhoto.hidden=false;
 const w=hoverPhoto.offsetWidth,h=hoverPhoto.offsetHeight,x=pointer?.x??innerWidth/2,y=pointer?.y??innerHeight/2;
 hoverPhoto.style.left=`${Math.max(16,Math.min(innerWidth-w-16,x+22))}px`;hoverPhoto.style.top=`${Math.max(16,Math.min(innerHeight-h-16,y-h*.45))}px`;
 document.body.dataset.photo=record.id;
}
function scheduleHoverCard(id){
 clearTimeout(hoverDelay);clearTimeout(hoverClose);
 if(hoverLocked)return;
 if(chaos>0||scrollY>0){hideHoverPhoto();return}
 const record=hoverByRegion.get(id);
 if(!record)return;
 if(record.id===shownPhoto)return;
 hoverDelay=setTimeout(()=>{if(current===id&&!hoverLocked)showHoverPhoto(record)},300);
}
hoverPhoto.addEventListener('pointerenter',()=>{hoverLocked=true;clearTimeout(hoverDelay);clearTimeout(hoverClose)});
hoverPhoto.addEventListener('pointerleave',()=>{hoverLocked=false});
hoverPhoto.querySelector('#hover-flip').addEventListener('click',()=>{const flipped=hoverPhoto.classList.toggle('flipped');hoverPhoto.querySelector('#hover-flip').setAttribute('aria-pressed',String(flipped));hoverPhoto.querySelector('#hover-flip').setAttribute('aria-label',flipped?'Return to photo':'Turn photo over')});
hoverPhoto.querySelector('#hover-close').addEventListener('click',hideHoverPhoto);
window.addEventListener('wheel',hideHoverPhoto,{passive:true});window.addEventListener('scroll',hideHoverPhoto,{passive:true});window.addEventListener('keydown',e=>{if(e.key==='Escape')hideHoverPhoto()});
