const W=1080,H=1920;const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const C={bg:'#0a131d',accent:'#2edb99',blue:'#4da3ff',text:'#eef3f8',muted:'#a9b8c8',faint:'#6f8399',warn:'#ef6a5c',yellow:'#f2c14e',surface:'#0f1f30',line:'#1e3448'};
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));const lerp=(a,b,t)=>a+(b-a)*t;
const eo=t=>1-Math.pow(1-clamp(t),3);const eo2=t=>1-Math.pow(1-clamp(t),2);const ei2=t=>Math.pow(clamp(t),2);
const eio=t=>{t=clamp(t);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
const eob=t=>{t=clamp(t);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const fade=(t,a,b,c,d)=>Math.min(seg(t,a,b),1-seg(t,c,d)); // in a..b, out c..d
const logo=new Image();logo.src='file:///home/claude/sportwetten-radar.net/assets/logo-icon-small.png';
function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}
function T(s,x,y,font,color,align='left',alpha=1,ls=0){ctx.save();ctx.globalAlpha*=alpha;ctx.font=font;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='alphabetic';if(ls){ctx.letterSpacing=ls+'px'}ctx.fillText(s,x,y);ctx.restore();}
function TW(s,font,ls=0){ctx.save();ctx.font=font;if(ls)ctx.letterSpacing=ls+'px';const w=ctx.measureText(s).width;ctx.restore();return w;}
function bg(t){ctx.globalAlpha=1;ctx.fillStyle=C.bg;ctx.fillRect(0,0,W,H);
 let g=ctx.createRadialGradient(920,190,0,920,190,760);g.addColorStop(0,'rgba(46,219,153,.11)');g.addColorStop(1,'rgba(46,219,153,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 g=ctx.createRadialGradient(0,1920,0,0,1920,900);g.addColorStop(0,'rgba(77,163,255,.09)');g.addColorStop(1,'rgba(77,163,255,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 ctx.save();ctx.beginPath();ctx.rect(0,130,W,1300);ctx.clip();
 [140,260,380,500,620].forEach((r,i)=>{ctx.strokeStyle=`rgba(46,219,153,${.20-i*.032})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(900,380,r,0,7);ctx.stroke();});
 const a=t*0.9;ctx.strokeStyle='rgba(46,219,153,.30)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(900,380);ctx.lineTo(900+Math.cos(a)*620,380+Math.sin(a)*620);ctx.stroke();
 ctx.restore();}
function header(){if(logo.complete){ctx.save();rr(72,150,64,64,14);ctx.clip();ctx.drawImage(logo,72,150,64,64);ctx.restore();}
 T('Sportwetten Radar',156,196,'700 38px B',C.text);}
function footer(extra){const fy=window.FY||1450;T('18+ · Keine Gewinngarantie',72,fy,'400 25px M',C.faint);T('@sportwetten.radar',1008,fy,'400 25px M',C.faint,'right');}
function title(eb,l1,l2,a=1){T(eb,72,290,'500 27px M',C.accent,'left',a,4);T(l1,72,352,'800 62px B',C.text,'left',a);if(l2)T(l2,72,416,'800 62px B',C.text,'left',a);}
function glow(x,y,r,col,al=1){const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,col);g.addColorStop(1,'rgba(0,0,0,0)');ctx.save();ctx.globalAlpha*=al;ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill();ctx.restore();}
function pill(x,y,w,h,fill,stroke){rr(x,y,w,h,h/2);ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke();}}
function card(x,y,w,h,al=1){ctx.save();ctx.globalAlpha*=al;rr(x,y,w,h,26);ctx.fillStyle='rgba(15,31,48,.94)';ctx.fill();ctx.strokeStyle='#1e3448';ctx.lineWidth=2;ctx.stroke();ctx.restore();}
const fmt=(v,d=0)=>v.toFixed(d).replace('.',',');
window.ready=false;
Promise.all([document.fonts.load('800 60px B'),document.fonts.load('700 38px B'),document.fonts.load('400 25px I'),document.fonts.load('600 30px I'),document.fonts.load('400 25px M'),document.fonts.load('500 27px M'),new Promise(r=>{if(logo.complete)r();else logo.onload=r;})]).then(()=>{window.ready=true;});
