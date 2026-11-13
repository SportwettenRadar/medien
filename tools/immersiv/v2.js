// Video 2: Restzeit-Uhr + Wahrscheinlichkeitskurve (Über 1,5 Tore, Poisson)
const DUR=23.2;
const LAM=2.7;
const prob=m=>{const l=LAM*(90-m)/90;return 1-Math.exp(-l)*(1+l);};
const MK=[[1.6,0],[7.6,45],[8.8,45],[13.0,70],[14.2,70],[15.4,80],[16.8,80]];
function minute(t){if(t<=MK[0][0])return 0;for(let i=1;i<MK.length;i++){if(t<=MK[i][0]){const a=MK[i-1],b=MK[i];return lerp(a[1],b[1],eio((t-a[0])/(b[0]-a[0])));}}return MK[MK.length-1][1];}
const CX0=110,CX1=990,CY0=1030,CY1=520,PMAX=.8;
const cx=m=>CX0+(CX1-CX0)*m/90,cy=p=>CY0-(CY0-CY1)*p/PMAX;
const COLS=[[0,[46,219,153]],[.5,[242,193,78]],[1,[239,106,92]]];
function colAt(u){u=clamp(u);let a=COLS[0],b=COLS[1];if(u>.5){a=COLS[1];b=COLS[2];}const k=(u-a[0])/(b[0]-a[0]);const c=a[1].map((v,i)=>Math.round(lerp(v,b[1][i],k)));return `rgb(${c[0]},${c[1]},${c[2]})`;}
const CALL=[{s:7.6,e:8.8,m:45,l1:'Halbzeit',},{s:13.0,e:14.2,m:70,l1:'Minute 70'},{s:15.4,e:16.8,m:80,l1:'Minute 80'}];
window.render=function(t){window.CT=t;
 bg(t);header();const intro=eo(seg(t,0,.7));ctx.save();ctx.translate(0,150);
 title('LIVE · ÜBER 1,5 TORE','Die Restzeit bestimmt','den Preis',intro);
 ctx.save();ctx.globalAlpha=intro;
 const m=minute(t),p=prob(m),q=1/p;
 // Gitter
 ctx.strokeStyle='rgba(238,243,248,.10)';ctx.lineWidth=2;ctx.font='400 22px M';
 [0,.2,.4,.6,.8].forEach(v=>{ctx.beginPath();ctx.moveTo(CX0,cy(v));ctx.lineTo(CX1,cy(v));ctx.stroke();T(Math.round(v*100)+' %',CX0-14,cy(v)+8,'400 24px M',C.faint,'right');});
 [0,15,30,45,60,75,90].forEach(v=>{T(v+"'",cx(v),CY0+44,'400 24px M',C.faint,'center');});
 ctx.strokeStyle='rgba(238,243,248,.3)';ctx.beginPath();ctx.moveTo(CX0,CY0);ctx.lineTo(CX1,CY0);ctx.stroke();
 // Stand-Chip
 {const f='500 24px M';const s='Stand 0:0 · kein Tor bisher';const w=TW(s,f)+36;pill(CX1-w,CY1-62,w,46,'rgba(15,31,48,.9)','#1e3448');T(s,CX1-w/2,CY1-30,f,C.muted,'center');}
 // Kurve (blass komplett)
 ctx.setLineDash([6,10]);ctx.strokeStyle='rgba(238,243,248,.16)';ctx.lineWidth=3;ctx.beginPath();for(let i=0;i<=90;i++){const X=cx(i),Y=cy(prob(i));i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}ctx.stroke();ctx.setLineDash([]);
 // Kurve (bis jetzt)
 const gr=ctx.createLinearGradient(CX0,0,CX1,0);gr.addColorStop(0,'#2edb99');gr.addColorStop(.5,'#f2c14e');gr.addColorStop(.85,'#ef6a5c');
 ctx.beginPath();for(let i=0;i<=m;i+=.5){const X=cx(i),Y=cy(prob(i));i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}ctx.lineTo(cx(m),cy(prob(m)));
 const path=new Path2D();ctx.strokeStyle=gr;ctx.lineWidth=7;ctx.lineJoin='round';ctx.stroke();
 ctx.lineTo(cx(m),CY0);ctx.lineTo(CX0,CY0);ctx.closePath();const fg=ctx.createLinearGradient(0,CY1,0,CY0);fg.addColorStop(0,'rgba(46,219,153,.20)');fg.addColorStop(1,'rgba(46,219,153,0)');ctx.fillStyle=fg;ctx.fill();
 // Marker
 const mx=cx(m),my=cy(p),mc=colAt(1-p/prob(0));
 ctx.setLineDash([6,8]);ctx.strokeStyle='rgba(238,243,248,.35)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(mx,CY0);ctx.stroke();ctx.setLineDash([]);
 glow(mx,my,52,mc.replace('rgb','rgba').replace(')',',.55)'));ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(mx,my,12,0,7);ctx.fill();ctx.strokeStyle=mc;ctx.lineWidth=5;ctx.stroke();
 // Callouts
 CALL.forEach(c=>{const a=fade(t,c.s,c.s+.35,c.e-.15,c.e+.2);if(a>0){const pp=prob(c.m);const X=clamp(cx(c.m),300,790),Y=cy(pp)-132;const k=eob(seg(t,c.s,c.s+.4));ctx.save();ctx.globalAlpha*=a;ctx.translate(X,Y+60);ctx.scale(.85+.15*k,.85+.15*k);ctx.translate(-X,-Y-60);
  rr(X-190,Y,380,112,22);ctx.fillStyle='rgba(10,19,29,.96)';ctx.fill();ctx.strokeStyle=colAt(1-pp/prob(0));ctx.lineWidth=3;ctx.stroke();
  T(c.l1.toUpperCase(),X,Y+34,'500 22px M',C.muted,'center',1,3);T(fmt(pp*100)+' % · Quote '+fmt(1/pp,2),X,Y+84,'800 38px B',C.text,'center');ctx.restore();}});
 // Karten
 const cards=[['MINUTE',Math.round(m)+"'",C.text],['CHANCE',(p*100<10?fmt(p*100,1):fmt(p*100))+' %',mc],['FAIRE QUOTE',fmt(q,2),mc]];
 cards.forEach((c,i)=>{const X=90+i*306;card(X,1090,288,170);T(c[0],X+144,1138,'500 22px M',C.faint,'center',1,3);T(c[1],X+144,1224,'800 66px B',c[2],'center');});
 T('Rechenbeispiel · konstante Torrate (2,7 Tore je 90 Min.) · keine Empfehlung',540,1310,'400 21px M',C.faint,'center');
 ctx.restore();
 // Fazit
 const L=[['Die Zeit läuft.',17.3,C.text],['Die Chance sinkt.',18.3,C.text],['Die Quote steigt.',19.3,C.accent]];
 const fa=seg(t,17.1,17.5)*(1-seg(t,20.6,21.0));
 if(fa>0){ctx.save();ctx.globalAlpha=fa;ctx.fillStyle='rgba(10,19,29,.88)';rr(70,640,940,420,34);ctx.fill();ctx.restore();
  L.forEach((l,i)=>{const k=eob(seg(t,l[1],l[1]+.45));ctx.save();ctx.globalAlpha=fa*clamp(k);ctx.translate(540,740+i*110);ctx.scale(.9+.1*k,.9+.1*k);T(l[0],0,0,'800 70px B',l[2],'center');ctx.restore();});}
 const ea=seg(t,21.0,21.8);
 if(ea>0){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=ea;ctx.beginPath();ctx.rect(0,570,W,1350);ctx.clip();ctx.clearRect(0,570,W,1350);bg(t);ctx.restore();
  T('Jede Minute zählt.',540,850,'800 80px B',C.text,'center',eo(seg(t,21.0,21.8)));T('Restzeit gehört in jede Rechnung.',540,950,'400 38px I',C.muted,'center',eo(seg(t,21.6,22.4)));
  T('Rechenbeispiel, vereinfachtes Modell',540,1300,'400 22px M',C.faint,'center',eo(seg(t,21.6,22.4)));}
 ctx.restore();window.FY=1745;footer();window.FY=0;
};
