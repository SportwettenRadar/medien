import numpy as np, wave, json, sys
from scipy import signal
SR=44100
rng=np.random.default_rng(7)
def tt(d): return np.arange(int(d*SR))/SR
def env(n,a=.005,r=.1,curve=3):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR))
    e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr)**curve if nr<=n else 1
    return e
def put(m,sig,t0,g=1.0):
    i=int(t0*SR); 
    if i>=len(m): return
    j=min(len(m),i+len(sig)); m[i:j]+=sig[:j-i]*g
def sine(f,d,g=1,a=.005,r=.2,curve=2):
    x=tt(d); return np.sin(2*np.pi*f*x)*env(len(x),a,r,curve)*g
def sweep(f0,f1,d,g=1,a=.01,r=.1,exp=True):
    x=tt(d); f=f0*(f1/f0)**(x/d) if exp else np.linspace(f0,f1,len(x)); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*env(len(x),a,r,2)*g
def noise(d): return rng.standard_normal(int(d*SR))
def bp(x,lo,hi): 
    sos=signal.butter(2,[lo,hi],btype='band',fs=SR,output='sos'); return signal.sosfilt(sos,x)
def hp(x,f): return signal.sosfilt(signal.butter(2,f,btype='high',fs=SR,output='sos'),x)
def lp(x,f): return signal.sosfilt(signal.butter(2,f,btype='low',fs=SR,output='sos'),x)
def whoosh(d=.5,g=.5,up=True,lo=300,hi=4000):
    n=noise(d); out=np.zeros_like(n); blocks=24; bl=len(n)//blocks
    for b in range(blocks):
        u=b/(blocks-1); u=u if up else 1-u
        c=lo*(hi/lo)**u; seg=n[b*bl:(b+1)*bl+bl//2] if b<blocks-1 else n[b*bl:]
        f=bp(seg,c*.7,min(c*1.4,SR/2-100)); out[b*bl:b*bl+len(f)][:len(out[b*bl:])]+=f[:len(out)-b*bl]*0.5
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
    n=whoosh(d,1,True,lo,hi); e=np.linspace(0,1,len(n))**2; x=tt(d); s=sweep(lo,hi*.5,d,.3,.01,.05)
    return (n*e+s*e)*g
def tapestop(d=.7,g=.35):
    return sweep(900,60,d,g,.005,.08)
def chord(freqs,d=2.2,g=.18,a=.3,r=1.0):
    x=tt(d); s=0
    for f in freqs: 
        for det in (-.003,0,.003): s=s+np.sin(2*np.pi*f*(1+det)*x)+0.3*np.sin(2*np.pi*2*f*(1+det)*x)
    return s/ (len(freqs)*3) *env(len(x),a,r,1.5)*g
def music(dur,bpm=96,start_kick=1.0,gain=1.0,fade_out=1.8):
    m=np.zeros(int(dur*SR)); beat=60/bpm; bar=4*beat
    prog=[(55.0,[220.0,261.63,329.63]),(43.65,[174.61,220.0,261.63]),(65.41,[261.63,329.63,392.0]),(49.0,[196.0,246.94,293.66])]
    nb=int(dur/bar)+2
    for b in range(nb):
        root,ch=prog[b%4]; t0=b*bar
        put(m,chord(ch,bar+.4,.16,.25,.9),t0)
        for k in (0,2):  # Bass
            put(m,sine(root,beat*1.6,.34,.01,.5),t0+k*beat)
        for k in range(8):  # Arpeggio
            f=ch[k%3]*(2 if k%4>=2 else 1)
            put(m,(np.sin(2*np.pi*f*tt(.3))+.3*np.sin(2*np.pi*3*f*tt(.3)))*np.exp(-tt(.3)*14)*.05,t0+k*beat/2)
    k=0;t=start_kick
    while t<dur-.5:
        put(m,thud(.38,120,.3),t); 
        put(m,hp(noise(.04),6000)*np.exp(-tt(.04)*90)*.07,t+beat/2)
        t+=beat
    m*=gain
    # fade
    n=len(m); m[:int(.8*SR)]*=np.linspace(0,1,int(.8*SR)); m[-int(fade_out*SR):]*=np.linspace(1,0,int(fade_out*SR))
    return m
def finish(m,path):
    m=np.tanh(m*1.1); m/= max(1e-9,np.max(np.abs(m)))/.89
    st=np.stack([m,m],1); w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
def eio(t): t=min(1,max(0,t)); return 4*t*t*t if t<.5 else 1-(-2*t+2)**3/2
lerp=lambda a,b,t:a+(b-a)*t

def v1():
    D=23.8; m=music(D,96,1.2,.9)
    for t in (0.8,1.9,3.0): put(m,whoosh(.45,.35,True,400,3500),t-.05); put(m,tick(.35,2200),t+.02); put(m,pop(520,.25),t+.7)
    put(m,whoosh(.7,.7,True,500,6000),4.1); put(m,thud(1.0,100,.6),4.2)
    put(m,tapestop(.8,.4),4.9)
    put(m,sweep(300,1400,.8,.22,.02,.2),5.4)
    put(m,tick(.4,3000),6.25); put(m,pop(990,.3),6.5)
    put(m,pop(440,.45),8.0)
    for i in range(14): put(m,tick(.35,1800+i*160),8.3+i*.09)
    put(m,ding(880,.4,1.6),9.6); put(m,ding(1318.5,.18,1.4),9.65)
    put(m,pop(660,.4),11.0); put(m,pop(880,.45),12.6); put(m,ding(784,.35,1.2),14.2); put(m,pop(990,.3),14.25)
    put(m,ding(660,.22,1.0),15.0)
    put(m,riser(1.0,.4,300,7000),16.4)
    put(m,whoosh(.4,.55,True,500,5000),17.35); put(m,thud(1.1,110,.7),18.1); put(m,hp(noise(.25),1500)*np.exp(-tt(.25)*18)*.5,18.1)
    put(m,sine(110,.8,.3,.02,.6),18.4)
    put(m,thud(1.0,70,1.0),19.8); put(m,chord([220,261.63,329.63,440],3.6,.45,.4,1.6),19.8); put(m,pop(880,.3),20.9)
    return m
def minute_fn(MK):
    def f(t):
        if t<=MK[0][0]: return 0
        for i in range(1,len(MK)):
            if t<=MK[i][0]:
                a,b=MK[i-1],MK[i]; return lerp(a[1],b[1],eio((t-a[0])/(b[0]-a[0])))
        return MK[-1][1]
    return f
def v2():
    D=23.2; m=music(D,96,1.6,.9)
    MK=[[1.6,0],[7.6,45],[8.8,45],[13.0,70],[14.2,70],[15.4,80],[16.8,80]]
    f=minute_fn(MK); last=0
    for t in np.arange(1.6,16.85,.002):
        mi=int(f(t))
        if mi>last:
            for _ in range(mi-last): put(m,tick(.30+.15*(mi/80),2400+mi*8),t)
            last=mi
    for a,b in ((1.6,7.6),(8.8,13.0),(14.2,15.4)): put(m,whoosh(b-a,.18,True,300,2500),a)
    put(m,pop(500,.4),1.2)
    for t,fq in ((7.6,880),(13.0,660),(15.4,494)): put(m,ding(fq,.4,1.3),t); put(m,pop(fq/2,.3),t)
    for t,fq in ((17.3,330),(18.3,392),(19.3,523)): put(m,thud(.9,100,.5),t); put(m,pop(fq,.4),t)
    put(m,thud(1.0,70,1.0),21.0); put(m,chord([220,261.63,329.63,440],2.4,.45,.35,1.4),21.0)
    return m
def v3():
    D=23.4; m=music(D,96,1.0,.9)
    cfg=json.load(open('cfg_v3.json')); SEQ=cfg['seq']
    NK=[[1.4,0],[6.9,10],[9.0,10],[12.6,30],[14.0,30],[18.2,100]]
    def tn(n):  # time when nf reaches n
        for i in range(1,len(NK)):
            a,b=NK[i-1],NK[i]
            if b[1]>a[1] and a[1]<n<=b[1]: return lerp(a[0],b[0],(n-a[1])/(b[1]-a[1]))
        return 99
    for i in range(100):
        t=tn(i)  # appears when nf>i
        if SEQ[i]: put(m,pop(620+ (i%5)*70,.30,.14),t); put(m,tick(.2,3200),t)
        else: put(m,sine(210,.12,.30,.003,.1),t); put(m,tick(.15,1400),t)
    put(m,pop(440,.4),1.2)
    for t,fq in ((6.9,494),(12.6,587),(18.2,880)): put(m,ding(fq,.4,1.4),t)
    put(m,chord([220,261.63,329.63,440],2.4,.35,.3,1.3),18.2)
    put(m,thud(1.0,70,1.0),21.0); put(m,chord([220,261.63,329.63,440],2.4,.45,.35,1.4),21.0)
    return m
if __name__=='__main__':
    name=sys.argv[1]
    finish({'v1':v1,'v2':v2,'v3':v3}[name](),f'{name}.wav')
