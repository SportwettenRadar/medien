// Generische Szenen-Engine. CFG kommt aus cfg_<name>.js (window.CFG), Zeiten absolut in Sekunden.
const AT=470; // Oberkante Inhaltsbereich
const vis=(t,s,e)=>Math.min(seg(t,s,s+.35),e==null?1:1-seg(t,e-.35,e));
function fitT(s,x,y,size,weight,color,align,maxW,alpha=1){let z=size;while(z>28&&TW(s,`${weight} ${z}px B`)>maxW)z-=2;T(s,x,y,`${weight} ${z}px B`,color,align,alpha);}
function wrap(s,font,maxW){const ws=s.split(' '),out=[];let cur='';for(const w of ws){const n=cur?cur+' '+w:w;if(TW(n,font)>maxW&&cur){out.push(cur);cur=w;}else cur=n;}if(cur)out.push(cur);return out;}
function cap(s,u,y=530){let z=34;while(z>22&&TW(s,`600 ${z}px I`)>936)z-=1;T(s,72,y,`600 ${z}px I`,C.muted,'left',eo(seg(u,.1,.6)));}
const colv=c=>c==='t'?C.text:c==='a'?C.accent:c==='b'?C.blue:c==='w'?C.warn:c==='y'?C.yellow:c==='m'?C.faint:(c||C.accent);
function tickmark(x,y,r,col,k){ctx.save();ctx.strokeStyle=col;ctx.lineWidth=7;ctx.lineCap='round';ctx.lineJoin='round';ctx.beginPath();ctx.moveTo(x-r*.5,y+r*.02);ctx.lineTo(x-r*.12,y+r*.38);ctx.lineTo(x+r*.52,y-r*.34);ctx.stroke();ctx.restore();}
function ringArc(x,y,r,p,col,w){ctx.save();ctx.lineCap='round';ctx.lineWidth=w;ctx.strokeStyle='rgba(238,243,248,.09)';ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.stroke();ctx.strokeStyle=col;ctx.beginPath();ctx.arc(x,y,r,-Math.PI/2,-Math.PI/2+Math.PI*2*p);ctx.stroke();ctx.restore();}

// ---------- Szene: horizontale Balken ----------
function sBars(S,t){const u=t-S.t0;cap(S.cap,u);const n=S.items.length,Y0=600,rh=Math.min(250,(1400-Y0)/n);
 S.items.forEach((it,i)=>{const r=S.rv[i],y=Y0+i*rh,a=eo(seg(u,r,r+.4));if(a<=0)return;const k=eo(seg(u,r+.1,r+1.1));const col=colv(it.c);
  ctx.save();ctx.globalAlpha*=a;T(it.l,72,y+4,'600 31px I',C.text);
  const val=it.v*k;T((it.pre||'')+fmt(val,it.dec||0)+(it.suf||''),1008,y+8,'800 46px B',col,'right');
  rr(72,y+24,936,42,21);ctx.fillStyle='rgba(15,31,48,.95)';ctx.fill();ctx.strokeStyle='#1e3448';ctx.lineWidth=2;ctx.stroke();
  const w=Math.max(0,936*it.v/S.max*k);if(w>8){rr(72,y+24,w,42,21);const g=ctx.createLinearGradient(72,0,72+w,0);g.addColorStop(0,col+'88');g.addColorStop(1,col);ctx.fillStyle=g;ctx.fill();}
  if(it.n)T(it.n,72,y+100,'400 25px I',C.muted);
  ctx.restore();});
 if(S.ref!=null){const ra=eo(seg(u,S.refT||1.5,(S.refT||1.5)+.5));ctx.save();ctx.globalAlpha*=ra;const X=72+936*S.ref/S.max;ctx.setLineDash([8,8]);ctx.strokeStyle='rgba(238,243,248,.55)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(X,Y0-6);ctx.lineTo(X,Y0+n*rh-40);ctx.stroke();ctx.setLineDash([]);T(S.refL,X,Y0-16,'500 24px M',C.text,'center',1,1);ctx.restore();}}
// ---------- Szene: senkrechte Balken (Histogramm/Treppe) ----------
function sVbars(S,t){const u=t-S.t0;cap(S.cap,u);const n=S.items.length,X0=84,Wd=912,slot=Wd/n,bw=slot*.66,B=1290,MH=640;
 ctx.save();ctx.strokeStyle='rgba(238,243,248,.35)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(X0,B);ctx.lineTo(X0+Wd,B);ctx.stroke();ctx.restore();
 S.items.forEach((it,i)=>{const r=S.rv[i],a=eo(seg(u,r,r+.35));if(a<=0)return;const k=eob(seg(u,r,r+.8));const col=colv(it.c);const h=MH*it.v/S.max*k,x=X0+i*slot+(slot-bw)/2;
  ctx.save();ctx.globalAlpha*=a;rr(x,B-h,bw,Math.max(h,4),Math.min(14,bw/3));const g=ctx.createLinearGradient(0,B-h,0,B);g.addColorStop(0,col);g.addColorStop(1,col+'66');ctx.fillStyle=g;ctx.fill();
  const vs=(it.pre||'')+fmt(it.v*eo(seg(u,r,r+.8)),it.dec||0)+(it.suf||'');T(vs,x+bw/2,B-h-14,n>8?'500 22px M':'800 32px B',C.text,'center');
  T(it.l,x+bw/2,B+40,n>8?'400 24px M':'500 24px M',C.muted,'center');
  ctx.restore();});
 if(S.xl)T(S.xl,540,B+84,'400 24px M',C.faint,'center',eo(seg(u,.6,1.2)));}
// ---------- Szene: Karten / Schritte / Zeitleiste ----------
function sSteps(S,t){const u=t-S.t0;cap(S.cap,u);const n=S.items.length,Y0=580,gap=18,h=Math.min(265,(1400-Y0-(n-1)*gap)/n);
 if(S.tl){const last=S.rv[n-1];const ly=Y0+h/2+(n-1)*(h+gap)*eo(seg(u,S.rv[0],last+.4));ctx.save();ctx.strokeStyle='rgba(46,219,153,.5)';ctx.lineWidth=5;ctx.setLineDash([2,12]);ctx.lineCap='round';ctx.beginPath();ctx.moveTo(132,Y0+h/2);ctx.lineTo(132,ly);ctx.stroke();ctx.restore();}
 S.items.forEach((it,i)=>{const r=S.rv[i],a=eo(seg(u,r,r+.4));if(a<=0)return;const k=eob(seg(u,r,r+.5)),y=Y0+i*(h+gap);ctx.save();ctx.globalAlpha*=a;ctx.translate(0,(1-k)*30);
  card(72,y,936,h);const cy=y+h/2,col=colv(it.c);ctx.fillStyle='rgba(46,219,153,.14)';ctx.strokeStyle=col;ctx.lineWidth=3;ctx.beginPath();ctx.arc(132,cy,38,0,7);ctx.fill();ctx.stroke();
  if(it.b==='ok')tickmark(132,cy,38,col);else if(it.b==='x'){ctx.save();ctx.strokeStyle=C.warn;ctx.lineWidth=7;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(118,cy-14);ctx.lineTo(146,cy+14);ctx.moveTo(146,cy-14);ctx.lineTo(118,cy+14);ctx.stroke();ctx.restore();}else T(it.b||String(i+1),132,cy+14,'800 40px B',col,'center');
  const ls=it.s?wrap(it.s,'400 27px I',780):[];const hh=it.s?44:0;const th=hh+ls.length*34;let ty=cy-th/2+34;
  fitT(it.h,196,ty,38,800,C.text,'left',790);ls.forEach((l,j)=>T(l,196,ty+46+j*34,'400 27px I',C.muted));
  ctx.restore();});}
// ---------- Szene: grosse Zahl mit Ring ----------
function sBig(S,t){const u=t-S.t0;cap(S.cap,u);const cxx=540,cyy=880,R=270;const k=eo(seg(u,.5,2.4));const col=colv(S.c);
 const a=eo(seg(u,.2,.7));ctx.save();ctx.globalAlpha*=a;if(S.ring!=null)ringArc(cxx,cyy,R,S.ring*k,col,26);glow(cxx,cyy,300,col+'22',.8);
 if(S.top)T(S.top,cxx,cyy-100,'500 27px M',C.muted,'center',1,3);
 fitT((S.pre||'')+fmt(S.v*k,S.dec||0)+(S.suf||''),cxx,cyy+50,150,800,C.text,'center',440);
 if(S.bot)T(S.bot,cxx,cyy+110,'500 26px M',col,'center',1,2);
 ctx.restore();
 if(S.sub){const ls=wrap(S.sub,'600 36px I',860);ls.forEach((l,j)=>T(l,540,1250+j*50,'600 36px I',C.text,'center',eo(seg(u,S.subT||2.2,(S.subT||2.2)+.6))));}}
// ---------- Szene: Kurven ----------
function sCurve(S,t){const u=t-S.t0;cap(S.cap,u);const X0=130,X1=990,Y0=1060,Y1=640,fx=x=>X0+(X1-X0)*(x-(S.xmin||0))/(S.xmax-(S.xmin||0)),fy=y=>Y0-(Y0-Y1)*(y-(S.ymin||0))/(S.ymax-(S.ymin||0));
 const pct=S.yfmt!=='raw';const a=eo(seg(u,.1,.6));ctx.save();ctx.globalAlpha*=a;
 ctx.strokeStyle='rgba(238,243,248,.10)';ctx.lineWidth=2;(S.yticks||[]).forEach(v=>{ctx.beginPath();ctx.moveTo(X0,fy(v));ctx.lineTo(X1,fy(v));ctx.stroke();T(pct?Math.round(v*100)+' %':String(v),X0-14,fy(v)+8,'400 24px M',C.faint,'right');});
 (S.xticks||[]).forEach(v=>T(v+(S.xu||''),fx(v),Y0+44,'400 24px M',C.faint,'center'));
 ctx.strokeStyle='rgba(238,243,248,.3)';ctx.beginPath();ctx.moveTo(X0,Y0);ctx.lineTo(X1,Y0);ctx.stroke();
 if(S.xl)T(S.xl,X1,Y0+84,'400 22px M',C.faint,'right');
 // Marker-X
 const P=S.path;let mx=P[0][1];if(u>=P[P.length-1][0])mx=P[P.length-1][1];else for(let i=1;i<P.length;i++){if(u<=P[i][0]){const q=P[i-1],w=P[i];mx=u<=q[0]?q[1]:lerp(q[1],w[1],eio((u-q[0])/(w[0]-q[0])));break;}}
 const yAt=(s,x)=>{const xs=s.xs,ys=s.ys;if(x<=xs[0])return ys[0];for(let i=1;i<xs.length;i++){if(x<=xs[i]){const f=(x-xs[i-1])/(xs[i]-xs[i-1]);return lerp(ys[i-1],ys[i],f);}}return ys[ys.length-1];};
 S.series.forEach(s=>{const col=colv(s.c);ctx.setLineDash([6,10]);ctx.strokeStyle='rgba(238,243,248,.16)';ctx.lineWidth=3;ctx.beginPath();s.xs.forEach((x,i)=>{i?ctx.lineTo(fx(x),fy(s.ys[i])):ctx.moveTo(fx(x),fy(s.ys[i]));});ctx.stroke();ctx.setLineDash([]);
  ctx.strokeStyle=col;ctx.lineWidth=7;ctx.lineJoin='round';ctx.beginPath();let st=false;for(let i=0;i<s.xs.length;i++){if(s.xs[i]>mx)break;const X=fx(s.xs[i]),Y=fy(s.ys[i]);st?ctx.lineTo(X,Y):ctx.moveTo(X,Y);st=true;}ctx.lineTo(fx(mx),fy(yAt(s,mx)));ctx.stroke();
  const my=fy(yAt(s,mx));glow(fx(mx),my,50,col+'88');ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(fx(mx),my,12,0,7);ctx.fill();ctx.strokeStyle=col;ctx.lineWidth=5;ctx.stroke();
  if(S.series.length>1)T(s.n,fx(S.xmax)-6,fy(s.ys[s.ys.length-1])-18,'500 24px M',col,'right');});
 ctx.setLineDash([6,8]);ctx.strokeStyle='rgba(238,243,248,.35)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(fx(mx),Y1-10);ctx.lineTo(fx(mx),Y0);ctx.stroke();ctx.setLineDash([]);
 // Callouts
 (S.calls||[]).forEach(c=>{const al=fade(u,c.s,c.s+.35,c.e-.15,c.e+.2);if(al<=0)return;const s0=S.series[0],yy=yAt(s0,c.x);const X=clamp(fx(c.x),300,830),Y=Math.max(Y1-30,fy(yy)-150);const k=eob(seg(u,c.s,c.s+.4));
  ctx.save();ctx.globalAlpha*=al;ctx.translate(X,Y+60);ctx.scale(.85+.15*k,.85+.15*k);ctx.translate(-X,-Y-60);rr(X-200,Y,400,112,22);ctx.fillStyle='rgba(10,19,29,.96)';ctx.fill();ctx.strokeStyle=colv(s0.c);ctx.lineWidth=3;ctx.stroke();
  T(c.l1.toUpperCase(),X,Y+34,'500 22px M',C.muted,'center',1,3);T(c.l2||(pct?fmt(yy*100,yy<.1?1:0)+' %':fmt(yy,2)),X,Y+84,'800 38px B',C.text,'center');ctx.restore();});
 // Karten
 if(S.cm){const y0=yAt(S.series[0],mx);let cs=[];if(S.cm==='one')cs=[[S.xlab,(S.xr?S.xr(mx):Math.round(mx))+(S.xu||''),'t'],['CHANCE',fmt(y0*100,y0<.1?1:0)+' %',S.series[0].c],['FAIRE QUOTE',fmt(1/y0,2),S.series[0].c]];else if(S.cm==='multi')cs=S.series.map(s=>[s.n.toUpperCase(),S.yfmt==='raw'?fmt(yAt(s,mx),1)+' Pkt.':fmt(yAt(s,mx)*100,1)+' %',s.c]);const n=cs.length,w=(936-(n-1)*18)/n;cs.forEach((c,i)=>{const X=72+i*(w+18);card(X,1130,w,176);T(c[0],X+w/2,1178,'500 21px M',C.faint,'center',1,2);fitT(c[1],X+w/2,1262,64,800,colv(c[2]),'center',w-24);});}
 ctx.restore();}
// ---------- Szene: Raster ----------
function sDots(S,t){const u=t-S.t0;cap(S.cap,u);const n=S.seq.length,cols=S.cols,rows=Math.ceil(n/cols),p=Math.min(84,Math.floor(900/cols)),sz=p-10,gx=540-cols*p/2,gy=700;
 const pr=eio(seg(u,S.a,S.b));const shown=Math.floor(n*pr+1e-6);const pre=S.pre||0;
 for(let i=0;i<n;i++){const x=gx+(i%cols)*p,y=gy+Math.floor(i/cols)*p;const vis_=i<shown;ctx.save();rr(x,y,sz,sz,sz*.28);ctx.fillStyle=vis_?(S.seq[i]?'rgba(46,219,153,.9)':'rgba(111,131,153,.45)'):'rgba(15,31,48,.9)';ctx.fill();ctx.strokeStyle=i<pre&&vis_?C.yellow:'#1e3448';ctx.lineWidth=i<pre?4:2;ctx.stroke();
  if(vis_&&S.sym){T(S.seq[i]?S.sym[0]:S.sym[1],x+sz/2,y+sz/2+10,'800 '+Math.round(sz*.5)+'px B',S.seq[i]?C.bg:C.text,'center');}ctx.restore();}
 let h=0,m=0;for(let i=pre;i<shown;i++){m++;h+=S.seq[i];}
 const y0=gy+rows*p+60;const al=eo(seg(u,S.a+.3,S.a+.8));
 ctx.save();ctx.globalAlpha*=al;T(S.l1,72,y0,'500 24px M',C.muted,'left',1,2);T(h+' von '+m,72,y0+66,'800 64px B',C.accent,'left');T(m?fmt(h/m*100)+' %':'–',1008,y0+66,'800 64px B',C.text,'right');T(S.l2,1008,y0,'500 24px M',C.muted,'right',1,2);ctx.restore();
 if(S.note)T(S.note,540,y0+130,'400 26px I',C.muted,'center',eo(seg(u,S.noteT||S.b,(S.noteT||S.b)+.6)));}
// ---------- Szene: Spielfeld ----------
const PSC=19,PX=540,PY=575;const psx=x=>PX+x*PSC,psy=y=>PY+y*PSC;
const kfp=(arr,u)=>{if(u<=arr[0][0])return[arr[0][1],arr[0][2]];for(let i=1;i<arr.length;i++){if(u<=arr[i][0]){const a=arr[i-1],b=arr[i],f=eio((u-a[0])/(b[0]-a[0]));return[lerp(a[1],b[1],f),lerp(a[2],b[2],f)];}}const l=arr[arr.length-1];return[l[1],l[2]];};
function pitchBase(a){ctx.save();ctx.globalAlpha*=a;ctx.fillStyle='rgba(13,28,42,.92)';rr(psx(-21),PY-52,42*PSC,52+41*PSC+4,18);ctx.fill();ctx.save();rr(psx(-21),PY-52,42*PSC,52+41*PSC+4,18);ctx.clip();for(let i=0;i<8;i++){ctx.fillStyle=i%2?'rgba(46,219,153,.035)':'rgba(46,219,153,0)';ctx.fillRect(psx(-21),PY+i*5.5*PSC,42*PSC,5.5*PSC);}ctx.restore();
 ctx.strokeStyle='rgba(238,243,248,.48)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(psx(-21),psy(0));ctx.lineTo(psx(21),psy(0));ctx.stroke();ctx.strokeRect(psx(-20.15),psy(0),40.3*PSC,16.5*PSC);ctx.strokeRect(psx(-9.16),psy(0),18.32*PSC,5.5*PSC);
 ctx.beginPath();ctx.arc(psx(0),psy(11),9.15*PSC,Math.PI/2-Math.acos(5.5/9.15),Math.PI/2+Math.acos(5.5/9.15));ctx.stroke();ctx.fillStyle='rgba(238,243,248,.6)';ctx.beginPath();ctx.arc(psx(0),psy(11),4,0,7);ctx.fill();
 ctx.fillStyle='rgba(238,243,248,.10)';ctx.fillRect(psx(-3.66),psy(-2.4),7.32*PSC,2.4*PSC);ctx.strokeStyle='rgba(238,243,248,.9)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(psx(-3.66),psy(0));ctx.lineTo(psx(-3.66),psy(-2.4));ctx.lineTo(psx(3.66),psy(-2.4));ctx.lineTo(psx(3.66),psy(0));ctx.stroke();
 ctx.strokeStyle='rgba(238,243,248,.16)';ctx.lineWidth=1;for(let i=1;i<7;i++){ctx.beginPath();ctx.moveTo(psx(-3.66+i*1.046),psy(-2.4));ctx.lineTo(psx(-3.66+i*1.046),psy(0));ctx.stroke();}ctx.restore();}
const PK={h:[C.accent,'#fff'],g:['#6f8399','rgba(238,243,248,.5)'],k:[C.yellow,'#fff'],b:[C.blue,'#fff'],w:[C.warn,'#fff']};
function pplayer(x,y,kind,r=14,al=1){const c=PK[kind]||PK.g;ctx.save();ctx.globalAlpha*=al;ctx.fillStyle=c[0];ctx.strokeStyle=c[1];ctx.lineWidth=3;ctx.beginPath();ctx.arc(psx(x),psy(y),r,0,7);ctx.fill();ctx.stroke();ctx.restore();}
function sPitch(S,t){const u=t-S.t0;cap(S.cap,u,PY-82);pitchBase(eo(seg(u,0,.5)));
 (S.zones||[]).forEach(z=>{const al=fade(u,z.s,z.s+.4,z.e==null?999:z.e-.3,z.e==null?1000:z.e);if(al<=0)return;ctx.save();ctx.globalAlpha*=al*(z.a==null?1:z.a);ctx.beginPath();z.poly.forEach((p,i)=>i?ctx.lineTo(psx(p[0]),psy(p[1])):ctx.moveTo(psx(p[0]),psy(p[1])));ctx.closePath();ctx.fillStyle=colv(z.c)+'33';ctx.fill();ctx.strokeStyle=colv(z.c);ctx.lineWidth=3;ctx.stroke();ctx.restore();
  if(z.l){const cx=z.poly.reduce((s,p)=>s+p[0],0)/z.poly.length,cy=z.poly.reduce((s,p)=>s+p[1],0)/z.poly.length;T(z.l,psx(cx),psy(cy)+10,'800 34px B',C.text,'center',al);}});
 (S.lines||[]).forEach(l=>{const al=fade(u,l.s,l.s+.35,l.e==null?999:l.e-.3,l.e==null?1000:l.e);if(al<=0)return;const g=eo(seg(u,l.s,l.s+(l.d||.7)));ctx.save();ctx.globalAlpha*=al;ctx.setLineDash(l.dash?[12,10]:[]);ctx.strokeStyle=colv(l.c||'w2');if(l.c==null)ctx.strokeStyle='rgba(238,243,248,.9)';ctx.lineWidth=l.w||4;const ex=lerp(l.x1,l.x2,g),ey=lerp(l.y1,l.y2,g);ctx.beginPath();ctx.moveTo(psx(l.x1),psy(l.y1));ctx.lineTo(psx(ex),psy(ey));ctx.stroke();ctx.setLineDash([]);
  if(l.arrow&&g>.95){const an=Math.atan2(psy(l.y2)-psy(l.y1),psx(l.x2)-psx(l.x1));ctx.fillStyle=ctx.strokeStyle;ctx.beginPath();ctx.moveTo(psx(l.x2),psy(l.y2));ctx.lineTo(psx(l.x2)-Math.cos(an-.45)*22,psy(l.y2)-Math.sin(an-.45)*22);ctx.lineTo(psx(l.x2)-Math.cos(an+.45)*22,psy(l.y2)-Math.sin(an+.45)*22);ctx.closePath();ctx.fill();}
  if(l.l&&g>.8){const f='600 28px I';const w=TW(l.l,f)+28,mx=psx((l.x1+l.x2)/2)+(l.lx||0),my=psy((l.y1+l.y2)/2)+(l.ly||0);pill(mx-w/2,my-24,w,46,'rgba(10,19,29,.95)','rgba(238,243,248,.5)');T(l.l,mx,my+8,f,C.text,'center');}ctx.restore();});
 (S.circles||[]).forEach(c=>{const al=fade(u,c.s,c.s+.35,c.e==null?999:c.e-.3,c.e==null?1000:c.e);if(al<=0)return;ctx.save();ctx.globalAlpha*=al;ctx.strokeStyle=colv(c.c);ctx.lineWidth=4;ctx.setLineDash(c.dash?[10,10]:[]);ctx.beginPath();ctx.arc(psx(c.x),psy(c.y),c.r*PSC*eo(seg(u,c.s,c.s+.6)),0,7);ctx.stroke();ctx.restore();});
 (S.players||[]).forEach(p=>{const a=p.s==null?1:eo(seg(u,p.s,p.s+.3));if(a<=0)return;const q=kfp(p.kf,u);pplayer(q[0],q[1],p.k,p.r||14,a);if(p.l)T(p.l,psx(q[0]),psy(q[1])+(p.ly||-24),'600 24px I',C.text,'center',a);});
 if(S.ball){const q=kfp(S.ball,u);ctx.save();glow(psx(q[0]),psy(q[1]),26,'rgba(255,255,255,.35)');ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(psx(q[0]),psy(q[1]),9,0,7);ctx.fill();ctx.strokeStyle='#0a131d';ctx.lineWidth=2;ctx.stroke();ctx.restore();}
 (S.bubbles||[]).forEach(b=>{const al=fade(u,b.s,b.s+.35,b.e==null?999:b.e-.3,b.e==null?1000:b.e);if(al<=0)return;ctx.save();ctx.globalAlpha*=al;const f='800 36px B';const w=TW(b.txt,f)+36;const px=b.left?psx(b.x)-22-w:psx(b.x)+22,py=psy(b.y)-(b.dy==null?40:b.dy);pill(px,py,w,52,'rgba(10,19,29,.95)',colv(b.c));T(b.txt,px+w/2,py+39,f,colv(b.c),'center');ctx.restore();});
 (S.labels||[]).forEach(b=>{const al=fade(u,b.s,b.s+.35,b.e==null?999:b.e-.3,b.e==null?1000:b.e);if(al>0)T(b.txt,psx(b.x),psy(b.y),'600 28px I',colv(b.c||'t'),'center',al);});}
const SC_={bars:sBars,vbars:sVbars,steps:sSteps,big:sBig,curve:sCurve,dots:sDots,pitch:sPitch};
window.render=function(t){const Q=window.CFG;bg(t);header();const intro=eo(seg(t,0,.7));
 const tw=Math.max(TW(Q.eb,'500 27px M',4),TW(Q.t1,'800 62px B'),Q.t2?TW(Q.t2,'800 62px B'):0);const kmax=clamp(960/tw,1,1.5),kt=lerp(kmax,1,eio(seg(t,.9,1.7)));
 ctx.save();ctx.translate(0,70);ctx.translate(72,290);ctx.scale(kt,kt);ctx.translate(-72,-290);T(Q.eb,72,290,'500 27px M',C.accent,'left',1,4);fitT(Q.t1,72,352,62,800,C.text,'left',936,1);if(Q.t2)fitT(Q.t2,72,416,62,800,C.text,'left',936,1);ctx.restore();ctx.save();ctx.translate(0,170);
 Q.scenes.forEach(S=>{const al=vis(t,S.t0,S.t1);if(al<=0)return;ctx.save();ctx.globalAlpha=al*intro;SC_[S.type](S,t);ctx.restore();});
 if(Q.note){T(Q.note,540,1415,'400 21px M',C.faint,'center',intro*(1-seg(t,Q.end.t0-.1,Q.end.t0+.3)));}
 const P=Q.punch;const fa=seg(t,P.t0,P.t0+.4)*(1-seg(t,Q.end.t0-.4,Q.end.t0));
 if(fa>0){ctx.save();ctx.globalAlpha=fa;ctx.fillStyle='rgba(10,19,29,.90)';const hh=P.lines.length*110+50;rr(70,760-hh/2+40,940,hh,34);ctx.fill();ctx.restore();
  P.lines.forEach((l,i)=>{const s=P.t0+.3+i*P.step,k=eob(seg(t,s,s+.45));ctx.save();ctx.globalAlpha=fa*clamp(k);ctx.translate(540,760-hh/2+40+95+i*110);ctx.scale(.9+.1*k,.9+.1*k);fitT(l[0],0,0,70,800,colv(l[1]||'t'),'center',880);ctx.restore();});}
 const E=Q.end,ea=seg(t,E.t0,E.t0+.8);
 if(ea>0){
  fitT(E.l1,540,850,80,800,C.text,'center',900,eo(seg(t,E.t0,E.t0+.8)));
  if(E.l2){wrap(E.l2,'400 38px I',880).forEach((l,j)=>T(l,540,950+j*52,'400 38px I',C.muted,'center',eo(seg(t,E.t0+.6,E.t0+1.4))));}
  if(E.n)T(E.n,540,1300,'400 22px M',C.faint,'center',eo(seg(t,E.t0+.6,E.t0+1.4)));}
 ctx.restore();window.FY=1745;footer();window.FY=0;};
function balWrap(s,font,maxW){const ws=s.split(' '),n=ws.length;const w=(i,j)=>TW(ws.slice(i,j).join(' '),font);
 const g=wrap(s,font,maxW).length;const memo={};
 function f(i,k){const key=i+','+k;if(memo[key])return memo[key];if(k===1){const ww=w(i,n);return memo[key]=ww<=maxW?{c:ww*ww,b:[n]}:{c:1e18,b:[n]};}
  let bc=1e18,bb=null;for(let j=i+1;j<=n-(k-1);j++){const ww=w(i,j);if(ww>maxW)break;const r=f(j,k-1);const c=ww*ww+r.c;if(c<bc){bc=c;bb=[j].concat(r.b);}}return memo[key]={c:bc,b:bb};}
 const r=f(0,g);if(!r.b||r.c>=1e18)return wrap(s,font,maxW);const out=[];let p=0;for(const j of r.b){out.push(ws.slice(p,j).join(' '));p=j;}return out;}
function hookFit(h){let pick=null;for(const fs of [104,90,80]){const L=balWrap(h,`800 ${fs}px B`,860);const mw=Math.max(...L.map(l=>TW(l,`800 ${fs}px B`)));const orph=L.length>1&&(L[0].length<=4||L[L.length-1].length<=4);
  pick={fs,L,lh:Math.round(fs*1.2)};if(L.length<=3&&mw<=860&&!orph)return pick;}return pick;}
// Teaser-Layout D2 (13.11.2026 von Daniel freigegeben): Block im oberen Drittel, Frage mit Leiste, Button direkt darunter
window.renderHook=function(){const Q=window.CFG;bg(1.5);header();
 const ty=470;T(Q.eb,72,ty,'500 28px M',C.accent,'left',1,4);T(Q.t1+(Q.t2?' '+Q.t2:''),72,ty+66,'700 40px B',C.muted,'left');
 const {fs,L,lh}=hookFit(Q.hook),y0=ty+66+80+fs;
 ctx.save();rr(72,y0-fs*0.8,10,(L.length-1)*lh+fs,5);ctx.fillStyle=C.accent;ctx.fill();ctx.restore();
 L.forEach((l,i)=>T(l,122,y0+i*lh,`800 ${fs}px B`,C.text,'left'));
 const by=y0+(L.length-1)*lh+90;pill(122,by,500,84,'rgba(46,219,153,.16)',C.accent);T('Heute Abend als Video',372,by+84/2+11,'600 32px I',C.accent,'center');
 window.FY=1660;footer();window.FY=0;};
