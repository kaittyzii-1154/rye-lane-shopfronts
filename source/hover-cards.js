const hoverRecords=CARD_RECORDS;
const hoverByRegion=new Map(hoverRecords.map(card=>[card.region,card]));
let hoverDelay=null,hoverClose=null,hoverLocked=false,shownPhoto=null,shownRecord=null;
const hoverStyle=document.createElement('style');hoverStyle.textContent=`
#hover-photo{position:fixed;z-index:10;width:min(340px,calc(100vw - 32px));height:290px;border-radius:9px;perspective:1100px;filter:drop-shadow(0 8px 20px #0002)}#hover-photo[hidden]{display:none}#hover-flip{padding:0;border:0;width:100%;height:100%;background:transparent;text-align:left;cursor:pointer;font-family:Arial,sans-serif;color:white;border-radius:9px;display:block}#hover-flip:focus-visible{outline:2px solid #008a52;outline-offset:4px}.photo-inner{display:block;position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform .55s cubic-bezier(.2,.7,.2,1)}#hover-photo.flipped .photo-inner{transform:rotateY(180deg)}.photo-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#000;border-radius:9px;overflow:hidden}.photo-front img{width:100%;height:100%;object-fit:cover;display:block}.photo-number{position:absolute;left:20px;top:20px;font-size:12px;letter-spacing:.12em}.photo-cue{position:absolute;bottom:20px;left:20px;font-size:11px;color:#bbb}.photo-back{transform:rotateY(180deg);padding:22px;display:flex;flex-direction:column;justify-content:center;gap:12px}.photo-back small{font-size:10px;letter-spacing:.1em;color:#aaa}.photo-back strong{font-size:18px;line-height:1.2;font-weight:500}.photo-back .story{font-size:13px;line-height:1.55}.photo-back .turn{font-size:10px;color:#aaa}#hover-close{position:absolute;right:9px;top:9px;z-index:3;color:white;background:#000;border:1px solid #555;width:27px;height:27px;cursor:pointer;font-size:17px}@media(prefers-reduced-motion:reduce){.photo-inner{transition:none}}
#hover-photo .photo-front::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.4),transparent 38%,transparent 65%,rgba(0,0,0,.35))}#hover-photo .photo-number,#hover-photo .photo-cue{z-index:1;color:#fff;-webkit-text-fill-color:#fff;text-shadow:0 1px 4px #000,0 0 12px #0008}#hover-photo .photo-back{color:#fff;justify-content:flex-start;padding-top:28px}#hover-photo .photo-back small{font-size:10.5px;line-height:1.45;letter-spacing:.04em;color:#ccc;padding-right:12px}#hover-photo .photo-address{margin-top:auto;padding-top:12px;border-top:1px solid #ffffff30;font-size:11px;line-height:1.5}#hover-photo .photo-address[hidden]{display:none}#hover-photo .photo-address a{color:#ddd;text-decoration:none;border-bottom:1px solid #ffffff55}#hover-photo .photo-address a:hover{color:#fff;border-bottom-color:#fff}
#hover-photo.scene-preview{filter:none}#hover-photo.scene-preview .photo-front::after{display:none}#hover-photo.scene-preview .photo-number,#hover-photo.scene-preview .photo-cue{color:#222;-webkit-text-fill-color:#222;text-shadow:none}#hover-photo.scene-preview .photo-front{background:#fff}#hover-photo.scene-preview .photo-front img{object-fit:cover;padding:0}#hover-photo.scene-preview .photo-back{display:none}
`;document.head.append(hoverStyle);
const hoverPhoto=document.createElement('aside');hoverPhoto.id='hover-photo';hoverPhoto.hidden=true;hoverPhoto.innerHTML='<button id="hover-close" aria-label="Close photo">×</button><div id="hover-flip" role="button" tabindex="0" aria-label="Turn photo over" aria-pressed="false"><span class="photo-inner"><span class="photo-face photo-front"><img alt=""><span class="photo-number"></span><span class="photo-cue">Click to turn over</span></span><span class="photo-face photo-back"><small></small><strong></strong><span class="story"></span><span class="photo-address" hidden></span></span></span></div>';document.body.append(hoverPhoto);
function hideHoverPhoto(){clearTimeout(hoverDelay);clearTimeout(hoverClose);hoverPhoto.hidden=true;hoverLocked=false;shownPhoto=null;}
function showHoverPhoto(record){
 if(chaos>0||window.scrollY>0)return;
 const caption=record.displayName||`PHOTO ${record.id}`;
 shownRecord=record;
 hoverPhoto.classList.toggle('scene-preview',Boolean(record.href));
 const action=hoverPhoto.querySelector('#hover-flip');action.setAttribute('role',record.href?'link':'button');action.setAttribute('aria-label',record.href?'Open '+record.label:'Turn photo over');
 hoverPhoto.querySelector('.photo-cue').textContent=record.href?'Open scene ↗':'Click to turn over';
 shownPhoto=record.id;hoverPhoto.classList.remove('flipped');hoverPhoto.querySelector('#hover-flip').setAttribute('aria-pressed','false');
 const img=hoverPhoto.querySelector('img');img.src=record.image;img.alt=record.displayName||`Photo ${record.id}: ${record.label}`;
 hoverPhoto.querySelector('.photo-number').textContent=caption;
 hoverPhoto.querySelector('.photo-back small').textContent=record.businessName||record.displayName||`${record.id} / ${record.type}`;
 const address=hoverPhoto.querySelector('.photo-address');address.replaceChildren();address.hidden=!record.address;
 if(record.address){const link=document.createElement('a');link.textContent=record.address+' ↗';link.href=record.mapUrl;link.target='_blank';link.rel='noopener noreferrer';link.setAttribute('aria-label','Open '+(record.businessName||record.label)+' in Google Maps');address.append(link)}
 hoverPhoto.querySelector('.photo-back strong').textContent=record.title;hoverPhoto.querySelector('.story').textContent=record.text;
 hoverPhoto.setAttribute('aria-label',record.displayName||`Photo ${record.id} — ${record.label}`);hoverPhoto.hidden=false;
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
hoverPhoto.querySelector('#hover-flip').addEventListener('click',e=>{if(e.target.closest('a'))return;if(shownRecord?.href){window.location.assign(shownRecord.href);return}const flipped=hoverPhoto.classList.toggle('flipped');hoverPhoto.querySelector('#hover-flip').setAttribute('aria-pressed',String(flipped));hoverPhoto.querySelector('#hover-flip').setAttribute('aria-label',flipped?'Return to photo':'Turn photo over')});
hoverPhoto.querySelector('#hover-close').addEventListener('click',hideHoverPhoto);
window.addEventListener('wheel',hideHoverPhoto,{passive:true});window.addEventListener('scroll',hideHoverPhoto,{passive:true});window.addEventListener('keydown',e=>{if(e.key==='Escape')hideHoverPhoto()});

hoverPhoto.querySelector('#hover-flip').addEventListener('keydown',e=>{if(e.target.closest('a'))return;if(e.key==='Enter'||e.key===' '){e.preventDefault();e.currentTarget.click()}});
