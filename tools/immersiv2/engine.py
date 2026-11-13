import numpy as np, wave, json, sys, os, subprocess
from scipy import signal
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'work'); os.makedirs(OUT,exist_ok=True)
SR=44100
rng=np.random.default_rng(7)
def tt(d): return np.arange(int(d*SR))/SR
def env(n,a=.005,r=.1,curve=3):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,min(n,int(r*SR)))
    e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr)**curve
    return e
def put(m,sig,t0,g=1.0):
    i=int(t0*SR)
    if i>=len(m) or i<0: return
    j=min(len(m),i+len(sig)); m[i:j]+=sig[:j-i]*g
def sine(f,d,g=1,a=.005,r=.2,curve=2):
    x=tt(d); return np.sin(2*np.pi*f*x)*env(len(x),a,r,curve)*g
def sweep(f0,f1,d,g=1,a=.01,r=.1):
    x=tt(d); f=f0*(f1/f0)**(x/d); ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*env(len(x),a,r,2)*g
def noise(d): return rng.standard_normal(int(d*SR))
def bp(x,lo,hi): return signal.sosfilt(signal.butter(2,[lo,min(hi,SR/2-100)],btype='band',fs=SR,output='sos'),x)
def hp(x,f): return signal.sosfilt(signal.butter(2,f,btype='high',fs=SR,output='sos'),x)
def lp(x,f): return signal.sosfilt(signal.butter(2,f,btype='low',fs=SR,output='sos'),x)
def whoosh(d=.5,g=.5,up=True,lo=300,hi=4000):
    n=noise(d); out=np.zeros_like(n); blocks=24; bl=len(n)//blocks
    for b in range(blocks):
        u=b/(blocks-1); u=u if up else 1-u
        c=lo*(hi/lo)**u; seg=n[b*bl:(b+1)*bl+bl//2] if b<blocks-1 else n[b*bl:]
        f=bp(seg,c*.7,c*1.4); k=min(len(f),len(out)-b*bl); out[b*bl:b*bl+k]+=f[:k]*0.5
    e=np.sin(np.pi*np.linspace(0,1,len(out)))**1.5
    return out/np.max(np.abs(out)+1e-9)*e*g
def tick(g=.4,f=2600):
    x=tt(.03); return (np.sin(2*np.pi*f*x)*np.exp(-x*160)+bp(noise(.03),2000,7000)*np.exp(-x*220)*.7)*g
def pop(f=660,g=.5,d=.16):
    x=tt(d); fr=f*(1+.8*np.exp(-x*40)); ph=2*np.pi*np.cumsum(fr)/SR; return np.sin(ph)*np.exp(-x*22)*g
def thud(g=.9,f=95,d=.5):
    x=tt(d); fr=f*np.exp(-x*7)+38; ph=2*np.pi*np.cumsum(fr)/SR; return (np.sin(ph)*np.exp(-x*7)+lp(noise(d),500)*np.exp(-x*30)*.4)*g
def ding(f=880,g=.35,d=1.2):
    x=tt(d); s=0
    for k,(m,a) in enumerate([(1,1),(2.01,.45),(3.02,.2),(5.4,.1)]): s=s+a*np.sin(2*np.pi*f*m*x)*np.exp(-x*(3.5+2.5*k))
    return s*g*(1-np.exp(-x*300))
def riser(d=1.0,g=.35,lo=300,hi=6000):
    n=whoosh(d,1,True,lo,hi); e=np.linspace(0,1,len(n))**2; s=sweep(lo,hi*.5,d,.3,.01,.05); return (n*e+s*e)*g
def tapestop(d=.7,g=.35): return sweep(900,60,d,g,.005,.08)
def whistle(d=.5,g=.25):
    x=tt(d); f=2900+60*np.sin(2*np.pi*28*x); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(x),.01,.05,1)*g
def kick(g=.8): return thud(g,130,.25)+hp(noise(.1),1500)*np.exp(-tt(.1)*40)*.2*g
def chord(freqs,d=2.2,g=.18,a=.3,r=1.0):
    x=tt(d); s=0
    for f in freqs:
        for det in (-.003,0,.003): s=s+np.sin(2*np.pi*f*(1+det)*x)+0.3*np.sin(2*np.pi*2*f*(1+det)*x)
    return s/(len(freqs)*3)*env(len(x),a,r,1.5)*g
PROGS=[[(55.0,[220.0,261.63,329.63]),(43.65,[174.61,220.0,261.63]),(65.41,[261.63,329.63,392.0]),(49.0,[196.0,246.94,293.66])],
       [(55.0,[220.0,261.63,329.63]),(49.0,[196.0,246.94,293.66]),(43.65,[174.61,220.0,261.63]),(65.41,[261.63,329.63,392.0])],
       [(65.41,[261.63,329.63,392.0]),(55.0,[220.0,261.63,329.63]),(43.65,[174.61,220.0,261.63]),(49.0,[196.0,246.94,293.66])]]
def music(dur,bpm=96,start_kick=1.0,gain=.9,fade_out=1.8,key=0,prog=0,sparse=False):
    m=np.zeros(int(dur*SR)); beat=60/bpm; bar=4*beat; fk=2**(key/12); P=PROGS[prog%3]
    for b in range(int(dur/bar)+2):
        root,ch=P[b%4]; root*=fk; ch=[c*fk for c in ch]; t0=b*bar
        put(m,chord(ch,bar+.4,.16,.25,.9),t0)
        for k in (0,2): put(m,sine(root,beat*1.6,.34,.01,.5),t0+k*beat)
        if not sparse:
            for k in range(8):
                f=ch[k%3]*(2 if k%4>=2 else 1)
                put(m,(np.sin(2*np.pi*f*tt(.3))+.3*np.sin(2*np.pi*3*f*tt(.3)))*np.exp(-tt(.3)*14)*.05,t0+k*beat/2)
    t=start_kick
    while t<dur-.5:
        put(m,thud(.38 if not sparse else .25,120,.3),t); put(m,hp(noise(.04),6000)*np.exp(-tt(.04)*90)*.07,t+beat/2); t+=beat
    m*=gain; m[:int(.8*SR)]*=np.linspace(0,1,int(.8*SR)); m[-int(fade_out*SR):]*=np.linspace(1,0,int(fade_out*SR))
    return m
def finish(m,path):
    m=np.tanh(m*1.1); m/=max(1e-9,np.max(np.abs(m)))/.89
    st=np.stack([m,m],1); w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
def eio(t): t=min(1,max(0,t)); return 4*t*t*t if t<.5 else 1-(-2*t+2)**3/2

# ---------- Zeitleiste ----------
def rvs(n,d,start=.9,tail=1.4):
    if n==1: return [start]
    return [round(start+i*(d-tail-start)/(n-1),2) for i in range(n)]
def build(name,eb,t1,t2,scenes,punch,end,note='Rechenbeispiel · vereinfachtes Modell · keine Empfehlung',bpm=None,key=None,prog=None,sparse=False):
    import datetime
    n=datetime.date.fromisoformat(name[:10]).toordinal()
    bpm=bpm or [92,96,100,104,98][n%5]; key=[0,2,-2,3,-3,5,1][n%7] if key is None else key; prog=n%3 if prog is None else prog
    t=1.6
    for S in scenes:
        S['t0']=round(t,2); S['t1']=round(t+S['d'],2); t=S['t1']
    pt=t+.1; pstep=.9
    t=pt+.3+len(punch)*pstep+1.2
    E=dict(end); E['t0']=round(t,2); dur=round(t+3.0,2)
    cfg=dict(name=name,eb=eb,t1=t1,t2=t2,scenes=scenes,punch=dict(t0=round(pt,2),step=pstep,lines=punch),end=E,note=note,dur=dur,bpm=bpm,key=key,prog=prog,sparse=sparse)
    return cfg
def audio(cfg):
    D=cfg['dur']; m=music(D,cfg.get('bpm',96),1.0,.9,key=cfg.get('key',0),prog=cfg.get('prog',0),sparse=cfg.get('sparse',False))
    for S in cfg['scenes']:
        t0=S['t0']; ty=S['type']
        put(m,whoosh(.45,.3,True,300,3000),t0-.05); put(m,pop(520,.28),t0+.05)
        if ty in('bars','vbars','steps'):
            for i,r in enumerate(S['rv']): put(m,pop(480+i*55,.36),t0+r); put(m,tick(.3,2200+i*60),t0+r+.03)
            if ty=='bars':
                for i,r in enumerate(S['rv']):
                    for k in range(8): put(m,tick(.12,1600+k*180),t0+r+.1+k*.1)
        elif ty=='big':
            put(m,riser(1.9,.32,300,5000),t0+.5); put(m,ding(880,.4,1.5),t0+2.4); put(m,ding(1318.5,.15,1.3),t0+2.45)
        elif ty=='curve':
            for a,b in zip(S['path'][:-1],S['path'][1:]):
                if b[1]!=a[1]:
                    n=int(max(3,(b[0]-a[0])*9))
                    for k in range(n): put(m,tick(.22,2200+int(1200*(b[1]-a[1]>0))+k*40),t0+a[0]+k*(b[0]-a[0])/n)
            for c in S.get('calls',[]): put(m,ding(660+(hash(c['l1'])%5)*55,.38,1.2),t0+c['s']); put(m,pop(400,.3),t0+c['s'])
        elif ty=='dots':
            n=len(S['seq']); a,b=S['a'],S['b']; last=0
            for i in np.arange(0,1,.001):
                sh=int(n*eio(float(i))+1e-6)
                if sh>last:
                    tt_=a+i*(b-a)
                    for j in range(last,sh):
                        if S['seq'][j]: put(m,pop(620+(j%5)*70,.24,.14),t0+tt_); 
                        else: put(m,sine(210,.12,.24,.003,.1),t0+tt_)
                    last=sh
            put(m,ding(587,.4,1.4),t0+b)
        elif ty=='pitch':
            for u,k in S.get('snd',[]):
                f={'pass':lambda:tick(.4,2000),'kick':lambda:kick(.9),'whistle':lambda:whistle(.5,.22),'pop':lambda:pop(660,.4),'ding':lambda:ding(784,.35,1.2),'thud':lambda:thud(.8,100,.5),'whoosh':lambda:whoosh(.5,.35,True,400,3500)}[k]
                put(m,f(),t0+u)
    P=cfg['punch']
    for i in range(len(P['lines'])):
        t=P['t0']+.3+i*P['step']; put(m,thud(.9,100,.5),t); put(m,pop([330,392,523,660][i%4],.4),t)
    E=cfg['end']['t0']; put(m,thud(1.0,70,1.0),E); put(m,chord([220*2**(cfg.get('key',0)/12),261.63*2**(cfg.get('key',0)/12),329.63*2**(cfg.get('key',0)/12),440*2**(cfg.get('key',0)/12)],2.8,.45,.35,1.4),E)
    return m
def render_video(cfg,fps=30):
    from playwright.sync_api import sync_playwright
    name=cfg['name']; os.makedirs(f'{OUT}',exist_ok=True)
    open(f'{OUT}/cfg_{name}.js','w').write('window.CFG='+json.dumps(cfg,ensure_ascii=False)+';')
    for f in ('lib.js','gen.js'):
        if not os.path.exists(f'{OUT}/{f}') or os.path.getmtime(f'{HERE}/{f}')>os.path.getmtime(f'{OUT}/{f}'): open(f'{OUT}/{f}','w').write(open(f'{HERE}/{f}').read())
    open(f'{OUT}/page_{name}.html','w').write(open(f'{HERE}/page.html.tpl').read().replace('CFGFILE',f'cfg_{name}.js'))
    return f'{OUT}/page_{name}.html'
def frames(cfg,times):
    from playwright.sync_api import sync_playwright
    page=render_video(cfg); os.makedirs(f'{OUT}/prev',exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
        pg.on('console',lambda m:print('console:',m.text)); pg.on('pageerror',lambda e:print('ERR',e))
        pg.goto('file://'+page); pg.wait_for_function('window.ready===true',timeout=20000)
        for t in times: pg.evaluate(f'render({t})'); pg.screenshot(path=f'{OUT}/prev/{cfg["name"]}_{t:05.2f}.png')
        b.close()
def video(cfg,outdir,fps=30):
    from playwright.sync_api import sync_playwright
    name=cfg['name']; page=render_video(cfg); wav=f'{OUT}/{name}.wav'; finish(audio(cfg),wav)
    out=f'{outdir}/{name}.mp4'; os.makedirs(outdir,exist_ok=True); n=int(cfg['dur']*fps)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('ERR',e))
        pg.goto('file://'+page); pg.wait_for_function('window.ready===true',timeout=20000)
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(fps),'-c:v','mjpeg','-i','-','-i',wav,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-af','loudnorm=I=-15:TP=-1.5:LRA=11','-ar','44100','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate(f'render({i/fps})'); ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close(); ff.wait(); b.close()
    return out
