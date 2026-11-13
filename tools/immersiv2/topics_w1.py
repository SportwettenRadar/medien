from engine import *
import math
def fmtd(v,d=1): return f"{v:.{d}f}".replace('.',',')
def mo_quote():
    qs=[1.5,2.0,4.0,10.0]; items=[dict(l=f"Quote {fmtd(q,2)}",v=round(100/q,1),dec=1,suf=' %',c='a',n=None) for q in qs]
    for it,q in zip(items,qs): it['n']=f"1 ÷ {fmtd(q,2)} = {fmtd(100/q,1)} %"
    d=9.5; b1=dict(type='bars',d=d,cap='So viel Wahrscheinlichkeit steckt in der Quote',items=items,max=100,rv=rvs(4,d,.9,1.6))
    q=3.4; p=100/q
    b2=dict(type='big',d=6.5,cap='Ein Rechenbeispiel',c='b',v=round(p,1),dec=1,suf=' %',ring=p/100,top='QUOTE 3,40',bot='= 1 ÷ 3,40',sub='Je höher die Quote, desto unwahrscheinlicher hält der Anbieter das Ereignis.',subT=2.6)
    return build('2026-11-16_quote-in-chance','MATHE-MONTAG · QUOTE','Quote in Chance','umrechnen',[b1,b2],[['Quote runter,'],['Chance rauf.'],['1 ÷ Quote.','a']],dict(l1='1 geteilt durch Quote.',l2='Der schnellste Weg, eine Quote zu verstehen.',n='Rechenbeispiel, vereinfachtes Modell, ohne Marge'),bpm=100,key=2,prog=1)
VIDEOS={'2026-11-16_quote-in-chance':mo_quote}
if __name__=='__main__':
    import sys
    mode,name=sys.argv[1],sys.argv[2]; cfg=VIDEOS[name]()
    if mode=='frames': frames(cfg,[float(x) for x in sys.argv[3].split(',')]); print(cfg['dur'])
    else: print(video(cfg,'/home/claude/medien/immersiv'))
