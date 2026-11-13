// Video 1: Torchance nachgestellt (Spielfeld, Draufsicht)
const SC=20,X0=540,Y0=500;const sx=x=>X0+x*SC,sy=y=>Y0+y*SC;
const DUR=23.8;
const kf=(arr,t)=>{if(t<=arr[0][0])return[arr[0][1],arr[0][2]];for(let i=1;i<arr.length;i++){if(t<=arr[i][0]){const a=arr[i-1],b=arr[i],u=eio((t-a[0])/(b[0]-a[0]));return[lerp(a[1],b[1],u),lerp(a[2],b[2],u)];}}const l=arr[arr.length-1];return[l[1],l[2]];};
const HEIM={p1:[[0,-14,34],[30,-14,34]],p2:[[0,10,31],[1.6,7,28],[30,7,28]],p3:[[0,-9,23],[2.3,-6,19.5],[30,-6,19.5]],p4:[[0,9,16],[2.8,6,13],[3.9,3,10.5],[30,3,10.5]],p5:[[0,-3,29],[4,-1,23],[30,-1,23]]};
const GAST={d1:[[0,-5,15],[4,-2,13],[5.2,-0.6,12.4],[30,-0.6,12.4]],d2:[[0,8,20],[4,6,16.5],[30,6,16.5]],d3:[[0,-12,28],[4,-9,24.5],[30,-9,24.5]],d4:[[0,1,25],[4,1,20.5],[30,1,20.5]]};
const SH=[3,10.5],TG=[-2,0.3],POSTL=[-3.66,0],POSTR=[3.66,0];
const pos=(a,b,u)=>[lerp(a[0],b[0],u),lerp(a[1],b[1],u)];
const PASS=[[0.8,1.6,[-14,34],[7,28]],[1.9,2.7,[7,28],[-6,19.5]],[3.0,3.9,[-6,19.5],[3,10.5]]];
function ball(t){
 if(t<4.2){let p=PASS[0][2];for(const q of PASS){if(t>=q[1])p=q[3];else if(t>=q[0]){return pos(q[2],q[3],eio((t-q[0])/(q[1]-q[0])));}else break;}return p;}
 let u;if(t<5.4)u=.55*eo2((t-4.2)/1.2);else if(t<17.4)u=.55;else if(t<18.1)u=.55+.45*ei2((t-17.4)/.7);else u=1;
 let b=pos(SH,TG,u);
 if(t>=18.1){b=pos(TG,[-7.5,5],eo((t-18.1)/.8));}
 return b;}
function ballMoving(t){return (t>0.8&&t<1.6)||(t>1.9&&t<2.7)||(t>3.0&&t<3.9)||(t>4.2&&t<5.0)||(t>17.4&&t<18.9);}
const xg=(x,y)=>{const d=Math.hypot(x,y);const a1=Math.atan2(x+3.66,y),a2=Math.atan2(x-3.66,y);const ang=Math.abs(a1-a2)*180/Math.PI;const z=-0.4-0.20*d+0.025*ang;return{d,ang,p:1/(1+Math.exp(-z))};};
const SHX=xg(SH[0],SH[1]);
function pitch(a){ctx.save();ctx.globalAlpha=a;
 ctx.fillStyle='rgba(13,28,42,.92)';rr(120,Y0-52,840,52+41*SC+4,18);ctx.fill();
 ctx.save();rr(120,Y0-52,840,52+41*SC+4,18);ctx.clip();
 for(let i=0;i<8;i++){ctx.fillStyle=i%2?'rgba(46,219,153,.035)':'rgba(46,219,153,.0)';ctx.fillRect(120,Y0+i*5.5*SC,840,5.5*SC);}
 ctx.restore();
 ctx.strokeStyle='rgba(238,243,248,.48)';ctx.lineWidth=3;
 ctx.beginPath();ctx.moveTo(120,sy(0));ctx.lineTo(960,sy(0));ctx.stroke();
 ctx.strokeRect(sx(-20.15),sy(0),40.3*SC,16.5*SC);ctx.strokeRect(sx(-9.16),sy(0),18.32*SC,5.5*SC);
 ctx.beginPath();ctx.arc(sx(0),sy(11),9.15*SC,Math.PI/2-Math.acos(5.5/9.15),Math.PI/2+Math.acos(5.5/9.15));ctx.stroke();
 ctx.fillStyle='rgba(238,243,248,.6)';ctx.beginPath();ctx.arc(sx(0),sy(11),4,0,7);ctx.fill();
 // Tor
 ctx.fillStyle='rgba(238,243,248,.10)';ctx.fillRect(sx(-3.66),sy(-2.4),7.32*SC,2.4*SC);
 ctx.strokeStyle='rgba(238,243,248,.9)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(sx(-3.66),sy(0));ctx.lineTo(sx(-3.66),sy(-2.4));ctx.lineTo(sx(3.66),sy(-2.4));ctx.lineTo(sx(3.66),sy(0));ctx.stroke();
 ctx.strokeStyle='rgba(238,243,248,.16)';ctx.lineWidth=1;for(let i=1;i<7;i++){ctx.beginPath();ctx.moveTo(sx(-3.66+i*1.046),sy(-2.4));ctx.lineTo(sx(-3.66+i*1.046),sy(0));ctx.stroke();}
 ctx.restore();}
function player(x,y,fill,ring,r=14,rot=0,sq=1){ctx.save();ctx.translate(sx(x),sy(y));ctx.rotate(rot);ctx.scale(1,sq);ctx.fillStyle=fill;ctx.strokeStyle=ring;ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,r,0,7);ctx.fill();ctx.stroke();ctx.restore();}
function bubble(x,y,txt,al,col=C.accent,left=false){ctx.save();ctx.globalAlpha*=al;const f='800 36px B';const w=TW(txt,f)+36;const px=left?sx(x)-22-w:sx(x)+22,py=left?sy(y)-26:sy(y)-58;pill(px,py,w,52,'rgba(10,19,29,.95)',col);T(txt,px+w/2,py+39,f,col,'center');ctx.restore();}
function cone(from,al,g,fillA){const L=pos(from,POSTL,g),R=pos(from,POSTR,g);ctx.save();ctx.globalAlpha*=al;ctx.fillStyle=`rgba(46,219,153,${fillA})`;ctx.beginPath();ctx.moveTo(sx(from[0]),sy(from[1]));ctx.lineTo(sx(L[0]),sy(L[1]));ctx.lineTo(sx(R[0]),sy(R[1]));ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(46,219,153,.8)';ctx.lineWidth=2.5;ctx.stroke();ctx.restore();}
window.render=function(t){
 bg(t);header();
 const intro=eo(seg(t,0,.7));
 title('TORCHANCE · NACHGESTELLT','Wie wahrscheinlich','ist dieses Tor?',intro);
 pitch(intro);ctx.save();ctx.globalAlpha=intro;
 const endA=seg(t,19.8,20.6);
 // Kegel
 const coneA=fade(t,5.4,5.9,17.1,17.8);
 if(coneA>0)cone(SH,coneA,eo(seg(t,5.4,6.4)),.17);
 // Vergleichspositionen
 const CMP=[{x:-13,y:20,s:11.0},{x:0,y:6,s:12.6,left:true}];
 CMP.forEach(c=>{const a=seg(t,c.s,c.s+.4)*(1-seg(t,17.1,17.8));if(a>0){const r=xg(c.x,c.y);cone([c.x,c.y],a*.55,eo(seg(t,c.s,c.s+.8)),.09);const sc=eob(seg(t,c.s,c.s+.5));ctx.save();ctx.globalAlpha*=a;glow(sx(c.x),sy(c.y),44,'rgba(77,163,255,.5)');ctx.restore();ctx.save();ctx.globalAlpha*=a;player(c.x,c.y,C.blue,'#eef3f8',14*sc);ctx.restore();
  bubble(c.x,c.y,fmt(r.p*100,r.p<.02?0:0)+' %',seg(t,c.s+.25,c.s+.6)*(1-seg(t,17.1,17.8)),C.accent,c.left);}});
 bubble(SH[0],SH[1],fmt(SHX.p*100)+' %',seg(t,14.2,14.6)*(1-seg(t,17.1,17.8)),C.accent);
 // Entfernung + Winkel
 const dl=seg(t,6.2,7.0);if(dl>0&&t<17.8){ctx.save();ctx.globalAlpha*=1-seg(t,17.1,17.8);ctx.setLineDash([10,10]);ctx.strokeStyle='rgba(238,243,248,.85)';ctx.lineWidth=3;const e=pos(SH,[0,0],eo(dl));ctx.beginPath();ctx.moveTo(sx(SH[0]),sy(SH[1]));ctx.lineTo(sx(e[0]),sy(e[1]));ctx.stroke();ctx.setLineDash([]);
  if(dl>.9){const m=pos(SH,[0,0],.5);const f='600 30px I';const w=TW('11 m',f)+30;pill(sx(m[0])+18,sy(m[1])-18,w,44,'rgba(10,19,29,.95)','rgba(238,243,248,.5)');T('11 m',sx(m[0])+18+w/2,sy(m[1])+13,f,C.text,'center');}
  const ar=seg(t,6.4,7.2);if(ar>0){const a1=Math.atan2(sy(0)-sy(SH[1]),sx(POSTL[0])-sx(SH[0])),a2=Math.atan2(sy(0)-sy(SH[1]),sx(POSTR[0])-sx(SH[0]));ctx.strokeStyle='#2edb99';ctx.lineWidth=4;ctx.beginPath();ctx.arc(sx(SH[0]),sy(SH[1]),70,a1,lerp(a1,a2,eo(ar)),false);ctx.stroke();
   if(ar>.8){const am=(a1+a2)/2;T(fmt(SHX.ang)+'°',sx(SH[0])+Math.cos(am)*108-26,sy(SH[1])+Math.sin(am)*108+4,'800 34px B',C.accent,'center');}}
  ctx.restore();}
 // Spieler
 Object.values(GAST).forEach(a=>{const p=kf(a,t);player(p[0],p[1],'#6f8399','rgba(238,243,248,.5)',13);});
 {let g=[0.5*Math.sin(t*1.3),1.3];if(t>=17.4){const u=eo2(seg(t,17.4,18.0));g=[lerp(g[0],-1.9,u),lerp(g[1],0.9,u)];}
  player(g[0],g[1],C.yellow,'#fff',15,t>=17.4?-0.9*eo2(seg(t,17.4,18.0)):0,t>=17.4?1+.5*eo2(seg(t,17.4,18)):1);}
 Object.entries(HEIM).forEach(([k,a])=>{const p=kf(a,t);if(k==='p4'&&t>=5.2){glow(sx(p[0]),sy(p[1]),46,'rgba(46,219,153,.45)',fade(t,5.2,5.7,17.2,17.8));}player(p[0],p[1],C.blue,'#eef3f8',14);});
 // Ball + Spur
 if(ballMoving(t)){for(let k=1;k<=9;k++){const b=ball(t-k*.035);ctx.save();ctx.globalAlpha=.34*(1-k/10);ctx.fillStyle='#eef3f8';ctx.beginPath();ctx.arc(sx(b[0]),sy(b[1]),8*(1-k/16),0,7);ctx.fill();ctx.restore();}}
 const b=ball(t);const frz=(t>5.2&&t<17.4);glow(sx(b[0]),sy(b[1]),frz?44+8*Math.sin(t*5):26,frz?'rgba(46,219,153,.55)':'rgba(238,243,248,.35)');
 ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(sx(b[0]),sy(b[1]),9,0,7);ctx.fill();
 // Aufschlag-Flash Parade
 if(t>18.1&&t<18.6){glow(sx(TG[0]),sy(TG[1]),120*(1-seg(t,18.1,18.6)),'rgba(255,255,255,.6)');}
 // Karte
 const pa=fade(t,8.0,8.5,14.4,15.0);
 if(pa>0){const k=eob(seg(t,8.0,8.6));ctx.save();ctx.globalAlpha*=pa;ctx.translate(540,1205);ctx.scale(.9+.1*k,.9+.1*k);ctx.translate(-540,-1205);card(120,1090,840,230);
  const u=eo(seg(t,8.3,9.6));
  T('ENTFERNUNG',130+95,1146,'500 22px M',C.faint,'center',1,3);T(fmt(SHX.d*u)+' m',130+95,1218,'800 54px B',C.text,'center');
  T('WINKEL',130+305,1146,'500 22px M',C.faint,'center',1,3);T(fmt(SHX.ang*u)+'°',130+305,1218,'800 54px B',C.text,'center');
  ctx.strokeStyle='#1e3448';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(130+410,1115);ctx.lineTo(130+410,1295);ctx.stroke();
  T('TORCHANCE',130+620,1146,'500 22px M',C.accent,'center',1,3);T(fmt(SHX.p*100*u)+' %',130+620,1230,'800 84px B',C.accent,'center');
  T('Beispielwert, vereinfachtes Modell',540,1292,'400 22px M',C.faint,'center');
  ctx.restore();}
 const ca=fade(t,15.0,15.6,17.0,17.5);
 if(ca>0){ctx.save();ctx.globalAlpha*=ca;card(120,1110,840,170);T('Näher + größerer Winkel',540,1180,'800 48px B',C.text,'center');T('= höhere Torchance',540,1244,'800 48px B',C.accent,'center');ctx.restore();}
 const sa=fade(t,18.4,18.8,19.4,19.8);
 if(sa>0){ctx.save();ctx.globalAlpha*=sa;card(120,1110,840,170);T('Gehalten.',540,1186,'800 64px B',C.text,'center');T('Bei 16 % der Normalfall.',540,1246,'600 34px I',C.muted,'center');ctx.restore();}
 ctx.restore();
 if(endA>0){ctx.save();ctx.globalAlpha=endA;ctx.beginPath();ctx.rect(0,420,W,1500);ctx.clip();ctx.clearRect(0,420,W,1500);bg(t);ctx.restore();
  const e2=eo(seg(t,20.0,20.9)),e3=eo(seg(t,20.9,21.8));
  T('Aus einer Szene',540,830,'800 84px B',C.text,'center',e2);T('wird eine Zahl.',540,930,'800 84px B',C.accent,'center',e2);
  T('Wahrscheinlichkeit statt Bauchgefühl.',540,1030,'400 38px I',C.muted,'center',e3);
  T('Nachgestellte Szene · Beispielwerte, vereinfachtes Modell',540,1300,'400 22px M',C.faint,'center',e3);}
 ctx.restore();window.FY=1745;footer();window.FY=0;
};
