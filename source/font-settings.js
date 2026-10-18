(()=>{
'use strict';
const KEY='rye-lane-fonts-v1';
const families={Arial:'Arial, sans-serif',Helvetica:'Helvetica, Arial, sans-serif',Georgia:'Georgia, serif',Times:'"Times New Roman", serif',Verdana:'Verdana, sans-serif',Trebuchet:'"Trebuchet MS", sans-serif',Courier:'"Courier New", monospace'};
const selectors={title:'#title-overlay h1',headings:'article h1,article h2,article h3',body:'article p,article li'};
let settings={};
function clean(input){const result={};for(const key of Object.keys(selectors)){const value=input?.[key];if(!value||typeof value!=='object')continue;const row={};if(families[value.family])row.family=value.family;if(Number.isFinite(value.size)&&value.size>=10&&value.size<=160)row.size=value.size;if([400,500,600,700].includes(value.weight))row.weight=value.weight;if(Object.keys(row).length)result[key]=row}return result}
function css(data){return Object.entries(clean(data)).map(([key,row])=>{const props=[];if(row.family)props.push(`font-family:${families[row.family]} !important`);if(row.size)props.push(`font-size:${key==='title'?`min(${row.size}px,8.5vw,13.5vh)`:`${row.size}px`} !important`);if(row.weight)props.push(`font-weight:${row.weight} !important`);return `${selectors[key]}{${props.join(';')}}`}).join('\n')}
const style=document.createElement('style');style.id='font-settings';document.head.append(style);
function apply(value,save=true){settings=clean(value);style.textContent=css(settings)+'\n#title-overlay h1,article h1{font-family:Arial,sans-serif!important}article h2,article h3{font-family:"Times New Roman",Times,serif!important;font-weight:700!important}article p,article li{font-family:"Times New Roman",Times,serif!important}';if(save)try{localStorage.setItem(KEY,JSON.stringify(settings))}catch{}window.dispatchEvent(new Event('rye-fonts-change'));for(const frame of document.querySelectorAll('iframe'))frame.contentWindow?.postMessage({type:'rye-fonts-apply',settings},'*')}
try{settings=clean(JSON.parse(localStorage.getItem(KEY)||'{}'))}catch{}
apply(settings,false);
window.addEventListener('message',event=>{if(event.source!==window.parent||window.parent===window)return;if(event.data?.type==='rye-fonts-apply')apply(event.data.settings)});
window.addEventListener('storage',event=>{if(event.key===KEY)try{apply(JSON.parse(event.newValue||'{}'),false)}catch{}});
for(const frame of document.querySelectorAll('iframe'))frame.addEventListener('load',()=>frame.contentWindow?.postMessage({type:'rye-fonts-apply',settings},'*'));
window.RyeFonts={css,clean,read:()=>settings};
})();
