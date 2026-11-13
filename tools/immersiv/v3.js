// Video 3: Zufall in Echtzeit (Stichprobe, feste Chance 55 %)
const DUR=23.4,P=0.55;const SEQ=CFG.seq;
const NK=[[1.4,0],[6.9,10],[9.0,10],[12.6,30],[14.0,30],[18.2,100]];
function nAt(t){if(t<=NK[0][0])return 0;for(let i=1;i<NK.length;i++){if(t<=NK[i][0]){const a=NK[i-1],b=NK[i];return lerp(a[1],b[1],(t-a[0])/(b[0]-a[0]));}}return 100;}
const CX0=120,CX1=990,CY0=900,CY1=570;const cx=n=>CX0+(CX1-CX0)*n/100,cy=r=>CY0-(CY0-CY1)*r;
const run=n=>{let h=0;for(let i=0;i<n;i++)h+=SEQ[i];return n?h/n:0;};
const band=n=>1.96*Math.sqrt(P*(1-P)/n);
window.render=function(t){
 bg(t);header();const intro=eo(seg(t,0,.7));ctx.save();ctx.translate(0,150);
 title('STICHPROBE · SIMULATION','Gleiche Chance.','Ganz anderes Bild.',intro);
 ctx.save();ctx.globalAlpha=intro;
 const nf=nAt(t),n=Math.floor(nf);
 // Gitter Chart
 [0,.25,.5,.75,1].forEach(v=>{ctx.strokeStyle='rgba(238,243,248,.10)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(CX0,cy(v));ctx.lineTo(CX1,cy(v));ctx.stroke();T(Math.round(v*100)+' %',CX0-14,cy(v)+8,'400 24px M',C.faint,'right');});
 [0,25,50,75,100].forEach(v=>T(String(v),cx(v),CY0+40,'400 24px M',C.faint,'center'));
 T('Versuche',CX1,CY0+76,'400 22px M',C.faint,'right');T('Simulation · feste Chance 55 %',CX0,CY0+76,'400 22px M',C.faint,'left');
 // echte Chance
 ctx.setLineDash([12,10]);ctx.strokeStyle='rgba(46,219,153,.8)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(CX0,cy(P));ctx.lineTo(CX1,cy(P));ctx.stroke();ctx.setLineDash([]);
 {const f='500 22px M';const s='echte Chance: 55 %';const w=TW(s,f)+26;pill(CX1-w,cy(P)-44,w,36,'rgba(10,19,29,.9)','rgba(46,219,153,.6)');T(s,CX1-w/2,cy(P)-19,f,C.accent,'center');}
 // Band (typische Schwankung)
 if(nf>=5){ctx.beginPath();let first=true;for(let i=5;i<=nf;i+=.5){const b=band(i);const X=cx(i),Y=cy(clamp(P+b));first?ctx.moveTo(X,Y):ctx.lineTo(X,Y);first=false;}
  for(let i=nf;i>=5;i-=.5){const b=band(i);ctx.lineTo(cx(i),cy(clamp(P-b)));}ctx.closePath();ctx.fillStyle='rgba(77,163,255,.16)';ctx.fill();ctx.strokeStyle='rgba(77,163,255,.5)';ctx.lineWidth=2;ctx.stroke();}
 // laufende Quote
 if(nf>=1){ctx.beginPath();for(let i=1;i<=n;i++){const X=cx(i),Y=cy(run(i));i>1?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}
  const fr=nf-n;if(n<100){const r1=run(n),r2=run(n+1);ctx.lineTo(cx(nf),cy(lerp(r1,r2,fr)));}
  ctx.strokeStyle='#eef3f8';ctx.lineWidth=5;ctx.lineJoin='round';ctx.stroke();
  const cr=n<100?lerp(run(Math.max(n,1)),run(n+1),nf-n):run(100);const mx=cx(nf),my=cy(cr);const col=Math.abs(cr-P)<.06?C.accent:(cr<P?C.warn:C.yellow);glow(mx,my,40,'rgba(238,243,248,.35)');ctx.fillStyle=col;ctx.beginPath();ctx.arc(mx,my,11,0,7);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.stroke();}
 // Karten
 const hits=SEQ.slice(0,n).reduce((a,b)=>a+b,0),rate=n?hits/n:0;
 const cards=[['VERSUCHE',String(n)],['TREFFER',String(hits)],['QUOTE',n?fmt(rate*100)+' %':'–']];
 cards.forEach((c,i)=>{const X=90+i*306;card(X,1004,288,128);T(c[0],X+144,1046,'500 22px M',C.faint,'center',1,3);T(c[1],X+144,1112,'800 56px B',i===2?(Math.abs(rate-P)<.06?C.accent:(rate<P?C.warn:C.yellow)):C.text,'center');});
 // Raster
 for(let i=0;i<100;i++){const a=clamp(nf-i);if(a<=0)continue;const col=i%10,row=Math.floor(i/10);const k=eob(a);const X=110+col*88,Y=1160+row*27;const w=74,h=19;ctx.save();ctx.translate(X+w/2,Y+h/2);ctx.scale(k,k);
  if(SEQ[i]){ctx.fillStyle=C.accent;if(a<1)ctx.shadowColor=C.accent,ctx.shadowBlur=24;}else{ctx.fillStyle='rgba(239,106,92,.62)';}
  rr(-w/2,-h/2,w,h,10);ctx.fill();ctx.restore();}
 // Callouts
 const CO=[[6.9,9.0,'Nach 10: 30 %. Schwach?','Normal wären 24–86 %.'],[12.6,14.0,'Nach 30: 50 %.','Noch immer im Rauschen.'],[18.2,21.0,'Nach 100: 55 %.','Genau die echte Chance.']];
 CO.forEach(c=>{const a=fade(t,c[0],c[0]+.35,c[1]-.2,c[1]+.1);if(a>0){const k=eob(seg(t,c[0],c[0]+.4));ctx.save();ctx.globalAlpha*=a;ctx.translate(540,478);ctx.scale(.9+.1*k,.9+.1*k);ctx.translate(-540,-478);
   rr(90,436,900,92,26);ctx.fillStyle='rgba(10,19,29,.96)';ctx.fill();ctx.strokeStyle=C.accent;ctx.lineWidth=3;ctx.stroke();T(c[2],540,488,'800 42px B',C.text,'center');T(c[3],540,516,'400 24px I',C.muted,'center');ctx.restore();}});
 ctx.restore();
 const ea=seg(t,21.0,21.8);
 if(ea>0){ctx.save();ctx.globalAlpha=ea;ctx.beginPath();ctx.rect(0,420,W,1500);ctx.clip();ctx.clearRect(0,420,W,1500);bg(t);ctx.restore();
  T('Kurze Serien täuschen.',540,830,'800 76px B',C.text,'center',eo(seg(t,21.0,21.8)));T('Erst viele Versuche',540,940,'800 56px B',C.accent,'center',eo(seg(t,21.5,22.3)));T('zeigen die Wahrheit.',540,1010,'800 56px B',C.accent,'center',eo(seg(t,21.8,22.6)));
  T('Simulation mit fester Trefferchance von 55 %',540,1300,'400 22px M',C.faint,'center',eo(seg(t,22.0,22.8)));}
 ctx.restore();window.FY=1745;footer();window.FY=0;
};
