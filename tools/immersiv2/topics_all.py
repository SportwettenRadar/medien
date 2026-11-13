from engine import *
import math, random, datetime
def fm(v,d=1): return f"{v:.{d}f}".replace('.',',')
def Pk(k,l): return math.exp(-l)*l**k/math.factorial(k)
def Pge(k,l): return 1-sum(Pk(i,l) for i in range(k))
def binom(n,k,p): return math.comb(n,k)*p**k*(1-p)**(n-k)
L=2.7
NOTE_M='Rechenbeispiel · vereinfachtes Modell · keine Empfehlung'
NOTE_V='Hilfe: check-dein-spiel.de · 0800 1 37 27 00 (kostenfrei)'
NOTE_P='Illustration · keine echte Spielszene'
def pun(*l): return [list(x) if isinstance(x,(list,tuple)) else [x] for x in l]
def bars(cap,items,mx,d=11,ref=None,refL=None,start=.9,tail=1.6,refT=1.5):
    s=dict(type='bars',d=d,cap=cap,items=items,max=mx,rv=rvs(len(items),d,start,tail))
    if ref is not None: s['ref']=ref;s['refL']=refL;s['refT']=refT
    return s
def vbars(cap,items,mx,d=11,xl=None,start=.8,tail=1.8):
    return dict(type='vbars',d=d,cap=cap,items=items,max=mx,rv=rvs(len(items),d,start,tail),xl=xl)
def steps(cap,items,d=None,tl=False,start=.9,tail=1.6):
    d=d or (2.2+len(items)*2.4); return dict(type='steps',d=d,cap=cap,items=items,tl=tl,rv=rvs(len(items),d,start,tail))
def big(cap,v,dec=1,suf=' %',pre='',ring=None,top=None,bot=None,sub=None,c='a',d=7,subT=2.6):
    return dict(type='big',d=d,cap=cap,v=v,dec=dec,suf=suf,pre=pre,ring=ring,top=top,bot=bot,sub=sub,c=c,subT=subT)
def live_curve(cap,xs,ys,xmax,ytk,xtk,stops,xlab,xu,cm='one',series=None,xmin=0,ymax=None,ymin=0,yfmt=None,hold=1.9,travel=2.4,labels=None):
    path=[[1.0,stops[0]]];t=1.0;calls=[]
    for i,x in enumerate(stops):
        if i>0: t+=travel; path.append([round(t,2),x])
        e=t+hold; path.append([round(e,2),x]) if i<len(stops)-1 else None
        calls.append(dict(s=round(t+.2,2),e=round(e,2),x=x,l1=(labels[i] if labels else f"{xlab} {x}{xu}")))
        t=e
    d=round(t+1.0,2)
    ser=series or [dict(xs=xs,ys=ys,c='a',n='')]
    S=dict(type='curve',d=d,cap=cap,xmax=xmax,xmin=xmin,ymax=ymax or max(max(s['ys']) for s in ser)*1.05,ymin=ymin,yticks=ytk,xticks=xtk,xu=xu,xl=xlab,xlab=xlab.upper(),cm=cm,path=path,calls=calls,series=ser)
    if yfmt: S['yfmt']=yfmt
    return S
def dots(cap,seq,cols,a,b,l1,l2,d,sym=None,pre=0,note=None,noteT=None):
    return dict(type='dots',d=d,cap=cap,seq=seq,cols=cols,a=a,b=b,l1=l1,l2=l2,sym=sym,pre=pre,note=note,noteT=noteT)
def END(l1,l2=None,n=None): return dict(l1=l1,l2=l2,n=n)
V={}
def reg(name):
    def d(f): V[name]=f; return f
    return d
def B(name,*a,**k): return build(name,*a,**k)

# ================= WOCHE 1 =================
@reg('2026-11-15_budget')
def _():
    it=[dict(h='Nur Geld, das du entbehren kannst',s='Miete, Rechnungen und Rücklagen sind tabu.',b='1'),
        dict(h='Limit festlegen, bevor du startest',s='Ein Betrag pro Monat, schriftlich, vorher.',b='2'),
        dict(h='Limit nie erhöhen, um Verluste auszugleichen',s='Das ist der Moment, in dem es gefährlich wird.',b='3')]
    return B('2026-11-15_budget','VERANTWORTUNG · BUDGET','Budget festlegen,','bevor du wettest',[steps('Drei Regeln',it,d=15)],pun('Erst das Limit.',['Dann die Wette.','a']),END('Das Limit gilt immer.','Auch nach einem schlechten Tag.',NOTE_V),note=NOTE_V)
@reg('2026-11-16_quote-in-chance')
def _():
    from topics_w1 import mo_quote; return mo_quote()
@reg('2026-11-18_marge')
def _():
    q=[2.10,3.40,3.60]; p=[100/x for x in q]; s=sum(p)
    it=[dict(l=f"Quote {fm(x,2)}",v=round(100/x,1),dec=1,suf=' %',c=c,n=f"1 ÷ {fm(x,2)}") for x,c in zip(q,'abw')]
    sc1=bars('Heim · Remis · Gast – so viel Chance steckt in den Quoten',it,60,d=10.5,start=.9,tail=1.8)
    sc2=big('Alles zusammengezählt',round(s,1),1,' %',ring=min(s/100/1.2,1)*0+s/120,top='SUMME DER CHANCEN',bot='MEHR ALS 100 %',sub=f"{fm(s-100,1)} Prozentpunkte zu viel: Das ist die Marge des Anbieters.",c='w',d=8)
    assert abs(s-104.8)<.06
    return B('2026-11-18_marge','MYTHOS & METHODE · MARGE','Die Marge','in der Quote',[sc1,sc2],pun('Fair wären 100 %.',['Hier sind es '+fm(s,1)+' %.','w']),END('Die Marge ist der Preis.','Du zahlst sie bei jeder Wette mit.',NOTE_M))
@reg('2026-11-19_verzoegerung')
def _():
    it=[dict(h='Das Tor fällt',s='Im Stadion, auf dem Platz.',b='1'),dict(h='Der Datenanbieter erfasst es',s='Menschen und Systeme melden das Ereignis.',b='2'),
        dict(h='Die Daten kommen bei uns an',s='Sie werden geprüft und eingeordnet.',b='3'),dict(h='Die Nachricht erreicht dich',s='Dazu kommt oft die Verzögerung des TV-Bildes.',b='4')]
    return B('2026-11-19_verzoegerung','HINTER DEN KULISSEN · LIVE-DATEN','Live-Daten haben','eine Verzögerung',[steps('Der Weg von Tor bis Nachricht',it,d=17,tl=True)],pun('Zwischen Tor und Nachricht',['liegt immer Zeit.','a']),END('Live heißt nie „gleichzeitig“.','Darum rechnen wir mit Verzögerung.'),note=None)
@reg('2026-11-20_zehn-tipps')
def _():
    n,p=10,.6; its=[dict(l=str(k),v=round(binom(n,k,p)*100,1),dec=1,suf='',c='a' if 5<=k<=7 else 'm') for k in range(0,11)]
    mid=sum(binom(n,k,p) for k in range(5,8))*100; low=sum(binom(n,k,p) for k in range(0,5))*100; hi=sum(binom(n,k,p) for k in range(8,11))*100
    sc1=vbars('Wie viele von 10 Tipps treffen? (Trefferquote 60 %, Angaben in %)',its,28,d=12,xl='Treffer von 10')
    sc2=bars('Auch mit echter 60 %-Quote',[dict(l='4 oder weniger Treffer',v=round(low,1),dec=1,suf=' %',c='w'),dict(l='5 bis 7 Treffer',v=round(mid,1),dec=1,suf=' %',c='a'),dict(l='8 oder mehr Treffer',v=round(hi,1),dec=1,suf=' %',c='b')],70,d=9)
    return B('2026-11-20_zehn-tipps','ZAHL DER WOCHE · STREUUNG','10 Tipps, 60 Prozent:','Wie viele treffen?',[sc1,sc2],pun('Zehn Tipps sagen',['fast nichts.','a']),END('Streuung ist normal.','Auch bei echtem Vorteil.',NOTE_M))
# ================= Sa/So/Mo Woche 2 =================
@reg('2026-11-21_nachspielzeit')
def _():
    xs=list(range(0,11)); ys=[1-math.exp(-L*x/90) for x in xs]; assert abs(ys[5]-.1393)<.0005
    sc=live_curve('Mindestens ein Tor in den nächsten Minuten',xs,ys,10,[0,.1,.2,.3],[0,2,4,6,8,10],[1,5,10],'Minute','',cm='one',labels=['1 Minute','5 Minuten Nachspielzeit','10 Minuten'])
    sc['xu']=" Min."; sc['xlab']='NACHSPIELZEIT'
    return B('2026-11-21_nachspielzeit','LIVE-RECHNUNG · NACHSPIELZEIT','Was sind 5 Minuten','Nachspielzeit wert?',[sc],pun('5 Minuten.',[fm(ys[5]*100,1)+' Prozent.','a']),END('Kurz, aber nicht wertlos.','Auch Nachspielzeit hat ihren Preis.',NOTE_M))
@reg('2026-11-22_verluste')
def _():
    st=[2**i for i in range(7)]; it=[dict(l=f"Wette {i+1}",v=x,dec=0,suf='',c='a' if i<3 else ('y' if i<5 else 'w')) for i,x in enumerate(st)]
    tot=sum(st); assert tot==127
    sc1=vbars('Verdoppeln nach jedem Verlust (Einsatz in Einheiten)',it,64,d=11,xl='Siebenmal in Folge verloren')
    sc2=big('Das Ergebnis',tot,0,' Einheiten',pre='−',c='w',top='GESAMTVERLUST',sub='So viel steht nach sieben Verlusten in Folge im Minus. Der nächste Einsatz: 128.',d=8)
    return B('2026-11-22_verluste','VERANTWORTUNG · VERLUSTE','Verluste nicht','zurückholen',[sc1,sc2],pun('Jede Verdopplung',['macht es schlimmer.','w']),END('Gleicher Einsatz. Immer.','Nie nachlegen, um aufzuholen.',NOTE_V),note=NOTE_V)
@reg('2026-11-23_breakeven')
def _():
    q=1.6; need=100/q
    seq=[1]*10+[0]*6; random.Random(5).shuffle(seq)
    sc1=big('Quote 1,60',round(need,1),1,' %',ring=need/100,top='NÖTIGE TREFFERQUOTE',bot='= 1 ÷ 1,60',sub='Darunter ist jede Wette auf Dauer ein Minusgeschäft.',c='b',d=8.5)
    sc2=dots('Quote 1,60: 16 Wetten, je 1 Einheit Einsatz',seq,8,1.2,6.5,'TREFFER','TREFFERQUOTE',d=12,note='10 Treffer zahlen 16 Einheiten zurück: ±0.',noteT=7.2)
    return B('2026-11-23_breakeven','MATHE-MONTAG · BREAK-EVEN','Ab wann lohnt sich','Quote 1,60?',[sc1,sc2],pun('Unter 62,5 Prozent:',['Verlust.','w']),END('Break-even ist der Maßstab.','Alles darüber ist erst der Anfang.',NOTE_M))
@reg('2026-11-24_elfmeter')
def _():
    t=11/(100/3.6); assert abs(t-.396)<.001
    pit=dict(type='pitch',d=13,cap='Elfmeter: 11 Meter bis zum Tor',
      players=[dict(k='h',kf=[[0,0,16],[2.4,0,13.5],[4.2,0,13.5],[4.7,.2,11.6],[40,.6,11.4]],s=0),dict(k='k',kf=[[0,0,.5],[4.9,0,.5],[5.4,-1.8,.4],[40,-1.8,.4]],s=.3)],
      ball=[[0,0,11],[4.65,0,11],[5.05,3.1,.2],[5.2,3.3,-1.2],[40,3.3,-1.2]],
      lines=[dict(s=2.2,x1=0,y1=11,x2=0,y2=.4,dash=True,l='11 m',lx=40,d=1.0),dict(s=7.0,x1=-3.66,y1=-1.3,x2=3.66,y2=-1.3,l='7,32 m',d=.8)],
      bubbles=[dict(s=5.1,e=11,x=1.2,y=5.5,txt='ca. 0,4 s',c='a')],
      snd=[[2.2,'whoosh'],[3.6,'whistle'],[4.7,'kick'],[5.3,'ding']])
    sc2=big('Die Rechnung',round(t,1),1,' s',top='11 m BEI 100 KM/H',ring=.4,sub='Für den Torwart bleibt kaum Zeit zum Reagieren. Darum entscheidet oft die Platzierung.',c='b',d=8)
    return B('2026-11-24_elfmeter','SPIELFELD · ELFMETER','Elfmeter in','0,4 Sekunden',[pit,sc2],pun('11 Meter.',['100 km/h.','a'],['0,4 Sekunden.','b']),END('Physik, nicht Glück.','Es bleibt kaum Reaktionszeit.','11 m ÷ 27,8 m/s ≈ 0,4 s'),note=NOTE_P)
@reg('2026-11-25_clv')
def _():
    q0,q1=2.10,1.90; p0,p1=100/q0,100/q1; clv=p1-p0; assert abs(clv-5.01)<.02
    xs=[0,2,4,6,8,10,12]; ys=[2.10,2.08,2.03,1.99,1.96,1.93,1.90]
    sc1=dict(live_curve('Beispiel: Quote auf dasselbe Ereignis, Stunden bis Anpfiff',xs,ys,12,[1.8,1.9,2.0,2.1,2.2],[0,3,6,9,12],[0,6,12],'Std.','',cm=None,xmin=0,ymax=2.2,ymin=1.8,yfmt='raw',series=[dict(xs=xs,ys=ys,c='b',n='')],labels=['Du tippst','Der Markt bewegt sich','Schlussquote']))
    sc1['yfmt']='raw';
    for c,t in zip(sc1['calls'],['2,10','2,00','1,90']): c['l2']='Quote '+t
    sc1['xl']='Stunden bis Anpfiff'
    sc2=big('Closing Line Value',round(clv,1),1,' Prozentpunkte',pre='+',c='a',top='2,10 STATT 1,90',sub=f"Du hast {fm(p0,1)} % bezahlt, am Ende galten {fm(p1,1)} %. Der Markt gab dir recht.",d=8.5)
    return B('2026-11-25_clv','MYTHOS & METHODE · CLV','Closing Line Value:','Wer schlägt den Markt?',[sc1,sc2],pun('Besser als die',['Schlussquote.','a']),END('CLV misst Qualität.','Nicht Glück.','Rechenbeispiel, keine eigene Auswertung'),note=NOTE_M)
@reg('2026-11-26_uhrzeiten')
def _():
    it=[dict(h='Eine Quote gilt nur für einen Moment',s='Wenige Sekunden später kann sie anders aussehen.',b='1'),dict(h='Ein Tor ändert alles',s='Vor und nach dem Tor sind es zwei verschiedene Spiele.',b='2'),
        dict(h='Ohne Uhrzeit ist nichts prüfbar',s='Nur mit Zeitstempel lässt sich nachvollziehen, was wann galt.',b='3')]
    return B('2026-11-26_uhrzeiten','HINTER DEN KULISSEN · ZEIT','Warum Uhrzeiten','so wichtig sind',[steps('Drei Gründe',it,d=15.5,tl=True)],pun('Wann ist',['die halbe Wahrheit.','a']),END('Ohne Zeitstempel','keine saubere Prüfung.'),note=None)
@reg('2026-11-27_pechserien')
def _():
    n,p=100,.55; q=1-p
    def plong(k):  # P(Laenge der laengsten Verlustserie >= k) in n Wetten
        # DP ueber aktuelle Serie < k
        st=[0.0]*k; st[0]=1.0; hit=0.0
        for _ in range(n):
            nx=[0.0]*k; 
            for j in range(k):
                nx[0]+=st[j]*p
                if j+1<k: nx[j+1]+=st[j]*q
                else: hit+=st[j]*q
            st=nx
        return hit
    ks=[3,4,5,6,7,8]; vals=[plong(k)*100 for k in ks]
    # Plausibilitaet per Simulation
    rr=random.Random(1);c=0
    for _ in range(20000):
        m=r=0
        for i in range(n):
            if rr.random()<p: r=0
            else: r+=1; m=max(m,r)
        c+= m>=5
    assert abs(c/20000*100-vals[2])<1.2,(c/20000*100,vals[2])
    it=[dict(l=f"{k} Verluste in Folge",v=round(v,1),dec=1,suf=' %',c='w' if k>=6 else 'y') for k,v in zip(ks,vals)]
    sc=bars('100 Wetten, Trefferquote 55 %: Wie wahrscheinlich ist so eine Serie?',it,100,d=15,start=.9,tail=1.8)
    return B('2026-11-27_pechserien','ZAHL DER WOCHE · PECHSERIEN','Wie lang darf','eine Pechserie sein?',[sc],pun('Auch bei 55 Prozent',['kommen Serien.','w']),END('Pech hat keinen Fehler.','Es gehört zur Rechnung.',NOTE_M))
@reg('2026-11-28_nach-dem-1-0')
def _():
    lam=lambda m: L*(90-m)/90; f=lambda m: Pge(2,lam(m))
    assert abs(f(30)-.537)<.001
    xs=list(range(30,91,2)); ys=[f(m) for m in xs]
    sc=live_curve('Stand 1:0 – mindestens zwei weitere Tore bis Spielende',xs,ys,90,[0,.2,.4,.6],[30,45,60,75,90],[30,45,60,75],'Minute',"'",xmin=30,ymax=.62,cm='one')
    return B('2026-11-28_nach-dem-1-0','LIVE-RECHNUNG · NACH DEM 1:0','Nach dem 1:0 in Minute 30:','Noch zwei Tore?',[sc],pun('Eine Führung',['ist keine Garantie.','a']),END('Restzeit zählt.','Auch mit Führung.',NOTE_M))
@reg('2026-11-29_limits')
def _():
    it=[dict(h='Limit setzen, bevor du startest',s='Gilt für Zeit und Geld.',b='ok'),dict(h='Nach Verlusten Pause machen',s='Nicht nachlegen, nicht „nur noch eine“.',b='ok'),
        dict(h='Auszeit nehmen, wenn der Spaß fehlt',s='Wetten soll Unterhaltung bleiben.',b='ok'),dict(h='Sperre ist jederzeit möglich',s='Auch Selbstsperre, bei lizenzierten Anbietern.',b='ok')]
    return B('2026-11-29_limits','VERANTWORTUNG · LIMITS','Limits und Pausen','helfen wirklich',[steps('Vier Gewohnheiten',it,d=17)],pun('Pause ist',['kein Rückschritt.','a']),END('Du entscheidest.','Nicht der Spielstand.',NOTE_V),note=NOTE_V)
@reg('2026-11-30_kombi')
def _():
    ps=[.7**k*100 for k in range(1,6)]; assert abs(ps[4]-16.807)<.01
    it=[dict(l=f"{k} Tipp{'s' if k>1 else ''} kombiniert",v=round(p,1),dec=1,suf=' %',c='a' if k==1 else ('y' if k<4 else 'w'),n=f"0,7 hoch {k}") for k,p in enumerate(ps,1)]
    sc1=bars('Jeder Tipp trifft zu 70 %',it,100,d=12.5,start=.9,tail=1.8)
    sc2=big('Fünf Tipps',round(ps[4],1),1,' %',ring=ps[4]/100,c='w',top='ALLE FÜNF TREFFEN',sub='Ein Fehler reicht, und die ganze Kombi ist verloren.',d=7.5)
    return B('2026-11-30_kombi','MATHE-MONTAG · KOMBI','Fünf Tipps zu 70 %:','Kombi-Chance?',[sc1,sc2],pun('Fünfmal 70 Prozent',['sind nur 16,8.','w']),END('Chancen multiplizieren sich.','Fehler auch.',NOTE_M))
# ================= Woche 3 =================
@reg('2026-12-01_abseits')
def _():
    pit=dict(type='pitch',d=15,cap='Abseits: Die Linie zählt im Moment des Passes',
      players=[dict(k='k',kf=[[0,0,1]],s=0),dict(k='g',kf=[[0,3,14]],s=.4),dict(k='g',kf=[[0,-7,16.5]],s=.5),dict(k='g',kf=[[0,-13,17]],s=.6),
               dict(k='h',kf=[[0,-12,35]],s=.8,l='Pass'),dict(k='h',kf=[[0,-4,12],[40,-4,12]],s=1.0,l='A',ly=-24),dict(k='h',kf=[[0,8,17]],s=1.2,l='B')],
      ball=[[0,-12,35],[6.3,-12,35],[7.4,-4,12.4]],
      lines=[dict(s=3.0,x1=-21,y1=14,x2=21,y2=14,dash=True,c='b',l='vorletzter Gegner',lx=250,d=1.0,w=4)],
      zones=[dict(s=4.2,poly=[[-21,0],[21,0],[21,14],[-21,14]],c='w',a=.5)],
      bubbles=[dict(s=6.6,x=-4,y=12,txt='Abseits',c='w'),dict(s=6.6,x=8,y=17,txt='im Spiel',c='a')],
      snd=[[3.0,'whoosh'],[4.2,'pop'],[6.3,'pass'],[7.5,'whistle']])
    it=[dict(h='Nur der Moment des Passes zählt',s='Danach darf der Angreifer laufen.',b='1'),dict(h='Kopf, Körper und Füße zählen',s='Arme und Hände nicht.',b='2'),dict(h='Kein Abseits bei Abstoß, Einwurf, Eckstoß',s='Dort gibt es die Regel nicht.',b='3')]
    return B('2026-12-01_abseits','SPIELFELD · ABSEITS','Abseits:','die unsichtbare Linie',[pit,steps('Regel 11 in drei Sätzen',it,d=13)],pun('Eine Linie.',['Ein Moment.','a']),END('Abseits ist Geometrie.','Quelle: IFAB-Regel 11'),note=NOTE_P+' · Quelle: IFAB')
@reg('2026-12-02_spielstand')
def _():
    it=[dict(h='Wer führt, spielt oft vorsichtiger',s='Weniger Risiko, tiefere Abwehr.',b='1'),dict(h='Wer zurückliegt, geht mehr Risiko',s='Mehr Spieler vorn, mehr Raum hinten.',b='2'),
        dict(h='Das ändert die Torchancen',s='Beide Teams spielen anders als bei 0:0.',b='3'),dict(h='Darum zählt der Spielstand',s='Eine Quote ohne Spielstand ist unvollständig.',b='4')]
    return B('2026-12-02_spielstand','MYTHOS & METHODE · SPIELSTAND','Der Spielstand-Effekt:','Warum 1:0 alles ändert',[steps('Vier Schritte',it,d=17.5,tl=True)],pun('Der Stand verändert',['das Spiel.','a']),END('Gleiche Teams.','Anderes Spiel.'),note=None)
@reg('2026-12-03_oeffentlich')
def _():
    it=[dict(h='Jedes Ergebnis steht im Ergebnis-Kanal',s='Öffentlich auf Telegram, für alle lesbar.',b='1'),dict(h='Gewonnen, verloren, storniert',s='Alles steht drin, auch die schwachen Tage.',b='2'),
        dict(h='Du musst uns nicht glauben',s='Du kannst jedes Ergebnis selbst nachlesen.',b='3')]
    return B('2026-12-03_oeffentlich','HINTER DEN KULISSEN · ERGEBNISSE','Jedes Ergebnis','ist öffentlich',[steps('Warum wir das so machen',it,d=15.5,tl=True)],pun('Nichts versteckt.',['Nichts geschönt.','a']),END('Transparenz ist kein Extra.','Sie ist die Grundlage.'),note=None)
@reg('2026-12-04_nullnull')
def _():
    p=Pk(0,L); ns=[1,3,5,9]; vals=[(1-(1-p)**n)*100 for n in ns]; assert abs(vals[3]-46.3)<.3,vals
    it=[dict(l=f"{n} Spiel{'e' if n>1 else ''}",v=round(v,1),dec=1,suf=' %',c='a' if n<9 else 'y',n='mindestens ein 0:0') for n,v in zip(ns,vals)]
    sc=bars('Chance auf mindestens ein 0:0 (Modell: 6,7 % je Spiel)',it,60,d=13,start=.9,tail=1.8)
    return B('2026-12-04_nullnull','ZAHL DER WOCHE · 0:0','Neun Spiele:','ein 0:0 ist normal',[sc],pun('Selten pro Spiel,',['häufig pro Spieltag.','a']),END('Kleine Chance,','viele Versuche.',NOTE_M))
@reg('2026-12-05_ueber35')
def _():
    l=2.7; c=lambda k:1-sum(math.exp(-l)*l**i/math.factorial(i) for i in range(k))
    P=[c(k)*100 for k in range(1,6)]; assert abs(P[3]-28.6)<.06 and abs(P[2]-50.6)<.06
    labs=['Über 0,5','Über 1,5','Über 2,5','Über 3,5','Über 4,5']; cols=['a','a','a','y','a']
    items=[dict(l=lb,v=round(p,1),dec=1,suf=' %',c=cc,n='Faire Quote '+fm(100/p,2)) for lb,p,cc in zip(labs,P,cols)]
    sc1=bars('Torlinien im Modell: 2,7 Tore je Spiel',items,100,d=12)
    sc2=big('Über 3,5 Tore',round(P[3],1),1,' %',c='y',top='VIER ODER MEHR TORE',sub='Etwa jedes dritte bis vierte Spiel. Faire Quote 3,50, ohne Marge.',d=8)
    return B('2026-12-05_ueber35','LIVE-RECHNUNG · TORLINIEN','Je höher die Linie,','desto teurer die Quote',[sc1,sc2],pun('Hohe Linie,',['seltenes Ereignis.','y']),END('Die Linie bestimmt','den Preis.',NOTE_M),note=NOTE_M)
@reg('2026-12-06_warnsignale')
def _():
    it=[dict(h='Du wettest mit Geld für Rechnungen',s='Miete und Alltag sind keine Wetteinsätze.',b='x',c='w'),dict(h='Du jagst Verlusten hinterher',s='Mehr Einsatz, um aufzuholen.',b='x',c='w'),dict(h='Du verheimlichst dein Wetten',s='Vor Familie, Freunden, Partner.',b='x',c='w'),
        dict(h='Du wettest länger oder höher als geplant',s='Das Limit gilt nur, wenn es hält.',b='x',c='w'),dict(h='Ohne Wetten bist du gereizt',s='Unruhe oder schlechte Laune ohne Wette.',b='x',c='w')]
    return B('2026-12-06_warnsignale','VERANTWORTUNG · WARNSIGNALE','Fünf Warnsignale','bei dir selbst',[steps('Ehrlich hinschauen',it,d=17.5)],pun('Ein Signal reicht',['zum Innehalten.','a']),END('Früh handeln hilft.','Hilfe gibt es kostenfrei.',NOTE_V),note=NOTE_V)
@reg('2026-12-07_erwartungswert')
def _():
    r1,r2=2.0*.5*100,1.9*.5*100; assert r1==100 and abs(r2-95)<1e-9
    sc1=bars('Faire Münze, 50 % – Rückzahlung je 100 Einheiten Einsatz',[dict(l='Quote 2,00',v=100,dec=1,suf='',c='a',n='0,5 × 2,00 × 100'),dict(l='Quote 1,90',v=95,dec=1,suf='',c='w',n='0,5 × 1,90 × 100')],110,d=10,ref=100,refL='100 = Gleichstand',refT=1.5,start=1.2,tail=3)
    sc2=big('Der Unterschied',5,1,' %',pre='−',c='w',top='ERWARTUNG JE EINSATZ',sub='Bei 1.000 Wetten zu je 1 Einheit sind das im Schnitt 50 Einheiten Minus.',d=8)
    return B('2026-12-07_erwartungswert','MATHE-MONTAG · ERWARTUNGSWERT','Erwartungswert:','2,00 gegen 1,90',[sc1,sc2],pun('Kleiner Unterschied.',['Große Wirkung.','w']),END('Auf Dauer zählt','jede Kommastelle.',NOTE_M))
@reg('2026-12-08_torwart-winkel')
def _():
    S=(-9.0,14.0)
    def shadow(K,half=.9):
        dx,dy=K[0]-S[0],K[1]-S[1]; n=math.hypot(dx,dy); nx,ny=-dy/n,dx/n
        E=[(K[0]+nx*half,K[1]+ny*half),(K[0]-nx*half,K[1]-ny*half)]
        X=[S[0]+(e[0]-S[0])*S[1]/(S[1]-e[1]) for e in E]
        return E,X
    def free(X):
        a,b=sorted(X); ov=max(0,min(b,3.66)-max(a,-3.66)); return 7.32-ov
    K1=(0.0,.6); d=math.hypot(*S); K2=(S[0]/d*4.5,S[1]/d*4.5)
    E1,X1=shadow(K1); E2,X2=shadow(K2); f1,f2=free(X1),free(X2); assert f2<f1,(f1,f2)
    pit=dict(type='pitch',d=17,cap='Schütze 16 m vom Tor: Wie viel Tor bleibt frei?',
      players=[dict(k='h',kf=[[0,S[0],S[1]]],s=0),dict(k='k',kf=[[0,K1[0],K1[1]],[7.4,K1[0],K1[1]],[9.2,K2[0],K2[1]],[40,K2[0],K2[1]]],s=.3)],
      zones=[dict(s=1.2,e=3.4,poly=[[S[0],S[1]],[-3.66,0],[3.66,0]],c='a',a=.6),
             dict(s=3.6,e=8.6,poly=[[E1[0][0],E1[0][1]],[E1[1][0],E1[1][1]],[X1[1],0],[X1[0],0]],c='w',a=.9),
             dict(s=9.6,poly=[[E2[0][0],E2[0][1]],[E2[1][0],E2[1][1]],[X2[1],0],[X2[0],0]],c='w',a=.9)],
      bubbles=[dict(s=4.4,e=8.6,x=5,y=5,txt=f"frei: {fm(f1,1)} m",c='a'),dict(s=10.2,x=5,y=5,txt=f"frei: {fm(f2,1)} m",c='a')],
      snd=[[1.2,'whoosh'],[3.6,'pop'],[7.4,'whoosh'],[9.6,'pop'],[10.4,'ding']])
    sc2=big('Geometrie',round(f1-f2,1),1,' m',pre='−',c='b',top='WENIGER FREIES TOR',sub='Ein Torwart, der herauskommt, verdeckt mehr vom Tor. Rechenbeispiel: Torwart 1,8 m breit.',d=8)
    return B('2026-12-08_torwart-winkel','SPIELFELD · WINKEL','Der Torwart','verkürzt den Winkel',[pit,sc2],pun('Näher am Schützen.',['Weniger freies Tor.','a']),END('Mut wird belohnt.','Zumindest geometrisch.'),note=NOTE_P+' · Rechenbeispiel')
@reg('2026-12-09_stichprobe')
def _():
    return None  # fertig (v3)
@reg('2026-12-10_nie')
def _():
    it=[dict(h='Keine Gewinngarantie',s='Wetten kann Geld kosten, immer.',b='x',c='w'),dict(h='Keine Verluste verstecken',s='Schwache Tage stehen genauso im Kanal.',b='x',c='w'),
        dict(h='Kein Druck zum Wetten',s='Kein „jetzt oder nie“, keine Panikmache.',b='x',c='w'),dict(h='Nichts für unter 18',s='Alles hier ist nur für Erwachsene.',b='x',c='w')]
    return B('2026-12-10_nie','HINTER DEN KULISSEN · VERSPRECHEN','Was wir','nie tun',[steps('Vier Grenzen',it,d=17)],pun('Klare Grenzen.',['Klare Haltung.','a']),END('Das ist unser Maßstab.','Daran kannst du uns messen.'),note='18+ · Keine Gewinngarantie')
@reg('2026-12-11_fuenf-tore')
def _():
    p5=Pge(5,L); ns=[1,3,9]; vals=[(1-(1-p5)**n)*100 for n in ns]
    it=[dict(l=f"{n} Spiel{'e' if n>1 else ''}",v=round(v,1),dec=1,suf=' %',c='a' if n<9 else 'y',n='mindestens ein Spiel mit 5 oder mehr Toren') for n,v in zip(ns,vals)]
    sc=bars(f"Ein Spiel mit 5+ Toren: je Spiel {fm(p5*100,1)} % (Modell)",it,100,d=12,start=.9,tail=1.8)
    return B('2026-12-11_fuenf-tore','ZAHL DER WOCHE · TORFEST','Neun Spiele:','Kommt ein Torfest?',[sc],pun('Selten pro Spiel,',['üblich pro Spieltag.','a']),END('Viele Spiele,','viele Chancen.',NOTE_M))
@reg('2026-12-12_fahrstuhl')
def _():
    xs=list(range(0,91,3)); mk=lambda k:[Pge(k,L*(90-m)/90) for m in xs]
    ser=[dict(xs=xs,ys=mk(1),c='a',n='Über 0,5'),dict(xs=xs,ys=mk(2),c='b',n='Über 1,5'),dict(xs=xs,ys=mk(3),c='y',n='Über 2,5')]
    sc=live_curve('Stand 0:0 – Chance, dass die Linie noch fällt',None,None,90,[0,.25,.5,.75,1],[0,15,30,45,60,75,90],[0,45,75],'Minute',"'",cm='multi',series=ser,ymax=1.0,labels=['Anpfiff','Halbzeit','Minute 75'])
    return B('2026-12-12_fahrstuhl','LIVE-RECHNUNG · FAHRSTUHL','Der Quoten-Fahrstuhl:','0,5 · 1,5 · 2,5',[sc],pun('Die Zeit läuft.',['Alle Linien fallen.','w']),END('Je höher die Linie,','desto steiler der Fall.',NOTE_M))
@reg('2026-12-13_treppe')
def _():
    sc1=bars('Sieben Verluste in Folge – wie viel steht im Minus? (Einheiten)',[dict(l='Gleicher Einsatz (1 Einheit)',v=7,dec=0,suf='',c='a',n='7 × 1'),dict(l='Verdoppeln',v=127,dec=0,suf='',c='w',n='1 + 2 + 4 + 8 + 16 + 32 + 64')],130,d=11,start=1.2,tail=3)
    sc2=vbars('Gleicher Einsatz: eine Treppe, keine Spirale',[dict(l=str(i+1),v=1,dec=0,suf='',c='a') for i in range(7)],2,d=9,xl='Wette 1 bis 7')
    return B('2026-12-13_treppe','VERANTWORTUNG · EINSATZ','Gleicher Einsatz:','Treppe statt Spirale',[sc1,sc2],pun('7 statt 127.',['Das ist der Unterschied.','a']),END('Konstanter Einsatz.','Immer.',NOTE_V),note=NOTE_V)
@reg('2026-12-14_torverteilung')
def _():
    its=[dict(l=str(k),v=round(Pk(k,L)*100,1),dec=1,suf='',c='a' if k==2 else 'b') for k in range(7)]
    sc1=vbars('Wie viele Tore fallen? (Modell: 2,7 im Schnitt, Angaben in %)',its,28,d=12.5,xl='Tore im Spiel')
    sc2=big('Am häufigsten',round(Pk(2,L)*100,1),1,' %',ring=Pk(2,L),c='a',top='GENAU 2 TORE',sub='Ein Schnitt von 2,7 heißt nicht, dass 2,7 Tore fallen. Die meisten Spiele enden mit 2 oder 3.',d=8.5)
    return B('2026-12-14_torverteilung','MATHE-MONTAG · TORE','2,7 Tore im Schnitt:','Was heißt das?',[sc1,sc2],pun('Der Schnitt täuscht.',['Die Verteilung zählt.','a']),END('Zahlen haben Form.','Nicht nur einen Mittelwert.',NOTE_M))
@reg('2026-12-15_mauer')
def _():
    B0=(-7.0,23.0); g=math.hypot(*B0); dr=(-B0[0]/g,-B0[1]/g); W=(B0[0]+9.15*dr[0],B0[1]+9.15*dr[1]); pp=(-dr[1],dr[0])
    wall=[(W[0]+k*.75*pp[0],W[1]+k*.75*pp[1]) for k in (-1.5,-.5,.5,1.5)]
    pit=dict(type='pitch',d=16,cap='Freistoß: Die Mauer steht mindestens 9,15 m entfernt',
      players=[dict(k='h',kf=[[0,-10,27],[3,-8.4,24.5],[8.5,-8.4,24.5],[9.1,-7.4,23.6],[40,-6.8,22.6]],s=0),dict(k='k',kf=[[0,-.5,.6],[9.6,-.5,.6],[10.6,1.8,.5],[40,1.8,.5]],s=.2)]+
              [dict(k='g',kf=[[0,w[0],w[1]]],s=4.2+i*.3) for i,w in enumerate(wall)],
      ball=[[0,B0[0],B0[1]],[9.1,B0[0],B0[1]],[9.5,-5.5,17],[10.1,-3.4,9],[10.8,-.5,3],[11.4,2.8,-.9],[40,2.8,-.9]],
      circles=[dict(s=1.5,x=B0[0],y=B0[1],r=9.15,c='b',dash=True)],
      lines=[dict(s=2.8,x1=B0[0],y1=B0[1],x2=W[0],y2=W[1],l='9,15 m',lx=-60,c='b')],
      bubbles=[dict(s=11.2,x=1.2,y=6,txt='über die Mauer',c='a')],
      snd=[[1.5,'whoosh'],[3.0,'pop'],[3.6,'whistle'],[9.1,'kick'],[11.3,'ding']])
    sc2=big('IFAB-Regel 13',9.15,2,' m',c='b',ring=1,top='MINDESTABSTAND',sub='Das entspricht 10 Yards. Gegner müssen so weit weg stehen, bis der Ball im Spiel ist.',d=8)
    return B('2026-12-15_mauer','SPIELFELD · FREISTOSS','Die Mauer:','9,15 Meter Abstand',[pit,sc2],pun('Zehn Yards.',['Keinen Schritt näher.','a']),END('Abstand ist Regel.','Quelle: IFAB-Regel 13'),note=NOTE_P+' · Quelle: IFAB')
@reg('2026-12-16_oasis')
def _():
    it=[dict(h='Antrag beim Regierungspräsidium Darmstadt',s='Alternativ formlos bei einem lizenzierten Anbieter.',b='1'),dict(h='Mindestens drei Monate',s='Ohne Angabe sind es automatisch zwölf Monate.',b='2'),
        dict(h='Gilt bei allen angeschlossenen Anbietern',s='Casinos, Sportwetten, Lotterien, Wettbüros.',b='3'),dict(h='Aufheben nur mit Antrag',s='Nach Ablauf bleibt die Sperre, bis du sie aufhebst.',b='4')]
    return B('2026-12-16_oasis','MYTHOS & METHODE · OASIS','Selbstsperre:','So funktioniert OASIS',[steps('Die wichtigsten Fakten',it,d=19,tl=True)],pun('Eine Sperre.',['Alle Anbieter.','a']),END('Hilfe ist möglich.','Quelle: evz.de · Glücksspielbehörde',NOTE_V),note=NOTE_V)
@reg('2026-12-17_testphase')
def _():
    it=[dict(h='Bis 10.10.2026: Testphase',s='Mit den späteren Regeln berechnet, nicht verschickt.',b='1'),dict(h='Ab 11.10.2026: tatsächlich verschickt',s='Echte Meldungen mit echtem Zeitpunkt.',b='2'),dict(h='Wir kennzeichnen den Unterschied immer',s='Zahlen aus der Testphase tragen eine Fußnote.',b='3')]
    return B('2026-12-17_testphase','HINTER DEN KULISSEN · TRACKRECORD','Testphase oder live?','So liest du es',[steps('Zwei Zeiträume, klar getrennt',it,d=16,tl=True)],pun('Zwei Zeiträume.',['Nie vermischt.','a']),END('Ehrlich getrennt.','Das macht Zahlen lesbar.'),note=None)
@reg('2026-12-18_ueber25')
def _():
    p=Pge(3,L); its=[dict(l=str(k),v=round(binom(9,k,p)*100,1),dec=1,suf='',c='a' if k>=5 else 'm') for k in range(10)]
    e=sum(binom(9,k,p) for k in range(4,6))*100
    sc1=vbars(f"9 Spiele, je {fm(p*100,1)} % Über 2,5: Wie viele treffen? (Angaben in %)",its,30,d=12.5,xl='Spiele mit Über 2,5')
    sc2=big('Die Mitte',round(e,1),1,' %',ring=e/100,top='4 ODER 5 VON 9',c='b',sub='Mehr als jede zweite Spielrunde landet bei 4 oder 5, aber alles von 1 bis 8 kommt vor.',d=8) if e>50 else big('Die Mitte',round(e,1),1,' %',ring=e/100,top='4 ODER 5 VON 9',c='b',sub='Die Mitte ist wahrscheinlich, aber breite Streuung ist normal.',d=8)
    return B('2026-12-18_ueber25','ZAHL DER WOCHE · ÜBER 2,5','Neun Spiele:','Wie oft Über 2,5?',[sc1,sc2],pun('Die Mitte ist häufig.',['Die Ränder auch.','a']),END('Streuung gehört dazu.','Auch an einem Spieltag.',NOTE_M))
@reg('2026-12-19_modellgrenzen')
def _():
    a=1-math.exp(-L*.5); b=1-math.exp(-L*.55)
    sc1=bars('Eine Annahme ändert das Ergebnis: Mindestens ein Tor in Halbzeit 2',[dict(l='Gleichmäßig verteilt (50 %)',v=round(a*100,1),dec=1,suf=' %',c='b'),dict(l='Beispielannahme: 55 % der Tore in HZ 2',v=round(b*100,1),dec=1,suf=' %',c='a')],100,d=10,start=1.2,tail=3)
    it=[dict(h='Rote Karte',s='Eine Überzahl verändert die Torrate sofort.',b='1'),dict(h='Spielstand',s='Führung oder Rückstand verändern das Spiel.',b='2'),dict(h='Müdigkeit und Wechsel',s='Gegen Ende sieht ein Spiel anders aus.',b='3'),dict(h='Zufall',s='Auch ein gutes Modell sagt nur Wahrscheinlichkeiten.',b='4')]
    return B('2026-12-19_modellgrenzen','LIVE-RECHNUNG · GRENZEN','Die Grenzen','des Modells',[sc1,steps('Was ein einfaches Modell nicht sieht',it,d=16)],pun('Ein Modell ist',['kein Orakel.','a']),END('Annahmen zählen.','Darum nennen wir sie.',NOTE_M))
@reg('2026-12-20_vorsaetze')
def _():
    it=[dict(h='Monatslimit schriftlich festlegen',s='Vor dem ersten Einsatz des Jahres.',b='1'),dict(h='Nur Freizeitgeld einsetzen',s='Nie Geld, das du brauchst.',b='2'),dict(h='Pausentage fest einplanen',s='Mindestens ein wettfreier Tag pro Woche.',b='3'),dict(h='Monatlich ehrlich Bilanz ziehen',s='Zeit, Geld und Stimmung.',b='4')]
    return B('2026-12-20_vorsaetze','VERANTWORTUNG · 2027','Gute Vorsätze:','Budget für 2027',[steps('Vier Vorsätze',it,d=17.5)],pun('Plan vorher.',['Nicht danach.','a']),END('Starte mit Regeln.','Nicht mit Hoffnung.',NOTE_V),note=NOTE_V)
@reg('2026-12-21_ueber25-rechnung')
def _():
    its=[dict(l=str(k),v=round(Pk(k,L)*100,1),dec=1,suf='',c='a' if k>=3 else 'm') for k in range(8)]
    u=sum(Pk(k,L) for k in range(3))*100; o=100-u; assert abs(o-50.6)<.1
    sc1=vbars('Torverteilung (2,7 im Schnitt): ab 3 Toren heißt Über 2,5',its,28,d=12,xl='Tore im Spiel')
    sc2=bars('Zusammengezählt',[dict(l='Unter 2,5 (0, 1 oder 2 Tore)',v=round(u,1),dec=1,suf=' %',c='m'),dict(l='Über 2,5 (3 oder mehr Tore)',v=round(o,1),dec=1,suf=' %',c='a')],70,d=9,start=1.2,tail=2)
    return B('2026-12-21_ueber25-rechnung','MATHE-MONTAG · ÜBER 2,5','Über 2,5:','Wie das Modell rechnet',[sc1,sc2],pun('50,6 zu 49,4.',['Fast ein Münzwurf.','a']),END('Die Linie liegt','nah an der Mitte.',NOTE_M))
@reg('2026-12-22_konter')
def _():
    pit=dict(type='pitch',d=16,cap='Konter: 3 Angreifer gegen 2 Verteidiger',
      players=[dict(k='h',kf=[[0,2,41],[3.5,2,27],[5,2,23],[6.2,2,22],[40,2,22]],s=0),dict(k='h',kf=[[0,-10,42],[3.5,-9,28],[6,-8,22],[40,-8,22]],s=.2),dict(k='h',kf=[[0,14,42],[3.5,13,28],[6,12,21],[7.6,9.5,13],[40,9.5,13]],s=.4),
               dict(k='g',kf=[[0,-3,26],[3.5,-1.5,20],[5.2,.4,18],[40,.4,18]],s=.6),dict(k='g',kf=[[0,8,27],[3.5,8,21],[6,9,17],[40,9,17]],s=.8),dict(k='k',kf=[[0,0,1],[7.6,.4,2.2],[40,.4,2.2]],s=.4)],
      ball=[[0,2,40.5],[3.5,2,26.5],[5.2,2,22.5],[6.2,12,21],[7.7,9.5,13.4],[8.5,-2.6,.4],[40,-2.6,.4]],
      bubbles=[dict(s=1.0,e=4.6,x=2,y=34,txt='3 gegen 2',c='a',left=True)],
      lines=[dict(s=5.1,e=7.4,x1=2,y1=22.5,x2=12,y2=21,arrow=True,c='a',d=.9)],
      snd=[[1.0,'whoosh'],[3.6,'pop'],[5.3,'pass'],[7.65,'kick'],[8.5,'ding']])
    it=[dict(h='Die Abwehr ist noch nicht sortiert',s='Wenig Zeit, sich zu ordnen.',b='1'),dict(h='Viel Raum hinter den Verteidigern',s='Tempo schlägt Aufstellung.',b='2'),dict(h='Überzahl am Ball',s='Ein freier Mitspieler ist fast immer da.',b='3')]
    return B('2026-12-22_konter','SPIELFELD · KONTER','Konter:','Drei gegen zwei',[pit,steps('Warum Konter so gefährlich sind',it,d=13)],pun('Tempo.',['Raum.','a'],['Überzahl.','b']),END('Konter sind Mathematik.','Mehr Angreifer als Verteidiger.'),note=NOTE_P)
@reg('2026-12-23_schwache-tage')
def _():
    n=40; pwin=.55
    for sd in range(1,500):
        r=random.Random(sd); seq=[1 if r.random()<pwin else 0 for _ in range(n)]
        run=m=0
        for x in seq:
            run=0 if x else run+1; m=max(m,run)
        if m==4 and 20<=sum(seq)<=24: break
    # P(laengste Verlustserie >=4 in 40 Wetten)
    q=1-pwin;k=4;st=[0.0]*k;st[0]=1.0;hit=0.0
    for _ in range(n):
        nx=[0.0]*k
        for j in range(k):
            nx[0]+=st[j]*pwin
            if j+1<k: nx[j+1]+=st[j]*q
            else: hit+=st[j]*q
        st=nx
    sc1=dots('Simulation: 40 Wetten, Trefferquote 55 % (grün = Treffer)',seq,10,1.0,9.0,'TREFFER','TREFFERQUOTE',d=13.5,note='Auch ein guter Durchschnitt hat schwache Phasen.',noteT=10)
    sc2=big('Die Chance',round(hit*100,0),0,' %',ring=hit,c='w',top='4 PLEITEN IN FOLGE',sub='So wahrscheinlich ist eine Serie von mindestens 4 Verlusten in 40 Wetten bei 55 % Trefferquote.',d=8.5)
    return B('2026-12-23_schwache-tage','MYTHOS & METHODE · SCHWACHE TAGE','Auch gute Systeme','haben schwache Tage',[sc1,sc2],pun('Schwache Phasen',['sind normal.','a']),END('Zufall schwankt.','Das ist kein Fehler.','Simulation, vereinfachtes Modell'),note=NOTE_M)
@reg('2026-12-24_auswertung')
def _():
    it=[dict(h='Spiele werden live beobachtet',s='Daten gehen ein, Signale entstehen.',b='1'),dict(h='Endstände abwarten',s='Erst wenn ein Spiel wirklich vorbei ist.',b='2'),dict(h='Ergebnisse veröffentlichen',s='Am nächsten Morgen, öffentlich im Kanal.',b='3'),dict(h='Summen gegenprüfen',s='Jede Tageszahl wird nachgerechnet.',b='4')]
    return B('2026-12-24_auswertung','HINTER DEN KULISSEN · AUSWERTUNG','Wie entsteht','eine Auswertung?',[steps('Das Prinzip in vier Schritten',it,d=17.5,tl=True)],pun('Erst prüfen.',['Dann veröffentlichen.','a']),END('Sorgfalt ist','der ganze Trick.'),note=None)
@reg('2026-12-25_zufall-tippen')
def _():
    n=9; its=[dict(l=str(k),v=round(binom(n,k,1/3)*100,1),dec=1,suf='',c='a' if k>=5 else 'm') for k in range(10)]
    hi=sum(binom(n,k,1/3) for k in range(5,10))*100
    sc1=vbars('Rein zufällig tippen (1, X, 2): Wie viele von 9 passen? (Angaben in %)',its,28,d=12.5,xl='Richtige Tipps von 9')
    sc2=big('Reiner Zufall',round(hi,1),1,' %',ring=hi/100,c='b',top='5 ODER MEHR VON 9',sub='So oft sieht blindes Raten nach einem guten Spieltag aus.',d=8)
    return B('2026-12-25_zufall-tippen','ZAHL DER WOCHE · ZUFALL','Blind tippen:','Wie gut sieht das aus?',[sc1,sc2],pun('Zufall kann',['gut aussehen.','b']),END('Ein Spieltag beweist nichts.','Eine Serie schon eher.',NOTE_M))
@reg('2026-12-26_hz2')
def _():
    f=lambda m: Pge(2,L*(90-m)/90); assert abs(f(45)-.391)<.001
    xs=list(range(45,91,2)); ys=[f(m) for m in xs]
    sc=live_curve('Halbzeit 0:0 – mindestens zwei Tore in Halbzeit 2',xs,ys,90,[0,.1,.2,.3,.4],[45,55,65,75,85],[45,60,75],'Minute',"'",xmin=45,ymax=.45,cm='one')
    return B('2026-12-26_hz2','LIVE-RECHNUNG · HALBZEIT','Halbzeit 0:0:','Über 1,5 noch drin?',[sc],pun('39 Prozent',['zur Halbzeit.','a']),END('Die zweite Halbzeit','hat ihren Preis.',NOTE_M))
@reg('2026-12-27_selbsttest')
def _():
    it=[dict(h='Wette ich länger als geplant?',b='1'),dict(h='Setze ich mehr als mein Limit?',b='2'),dict(h='Versuche ich, Verluste zurückzuholen?',b='3'),dict(h='Denke ich im Alltag ständig ans Wetten?',b='4'),dict(h='Verheimliche ich es vor anderen?',b='5')]
    return B('2026-12-27_selbsttest','VERANTWORTUNG · SELBSTTEST','Fünf Fragen','an dich selbst',[steps('Ehrlich antworten',it,d=17.5)],pun('Ein „Ja“ reicht',['zum Nachdenken.','a']),END('Das ist kein Diagnosetest.','Hilfe: check-dein-spiel.de',NOTE_V),note=NOTE_V)
@reg('2026-12-28_beide-treffen')
def _():
    lh,la=1.5,1.2; ph,pa=1-math.exp(-lh),1-math.exp(-la); both=ph*pa; assert abs(both-.5429)<.001
    sc1=bars('Heim erwartet 1,5 Tore, Gast 1,2 Tore',[dict(l='Heim trifft mindestens einmal',v=round(ph*100,1),dec=1,suf=' %',c='b'),dict(l='Gast trifft mindestens einmal',v=round(pa*100,1),dec=1,suf=' %',c='b'),dict(l='Beide treffen',v=round(both*100,1),dec=1,suf=' %',c='a',n='77,7 % × 69,9 %')],100,d=12,start=.9,tail=1.8)
    sc2=big('Faire Quote',round(1/both,2),2,'',c='a',ring=both,top='BEIDE TREFFEN',sub=f"= 1 ÷ {fm(both,3)}. Alles darunter ist die Marge des Anbieters.",d=7.5)
    return B('2026-12-28_beide-treffen','MATHE-MONTAG · BEIDE TREFFEN','Beide Teams treffen:','Die Rechnung',[sc1,sc2],pun('Zwei Chancen.',['Multipliziert.','a']),END('Aus zwei Zahlen','wird eine.',NOTE_M))
@reg('2026-12-29_eckball')
def _():
    pit=dict(type='pitch',d=18,cap='Eckball: Drei Bereiche, die zählen',
      players=[dict(k='k',kf=[[0,0,1.6]],s=0),dict(k='h',kf=[[0,-20,.8]],s=.3,l='Ecke'),
               dict(k='h',kf=[[0,-1,7],[40,-1,7]],s=.8),dict(k='h',kf=[[0,2,5.5]],s=.9),dict(k='h',kf=[[0,-4,9.5]],s=1.0),dict(k='h',kf=[[0,5,10]],s=1.1),dict(k='h',kf=[[0,0,13.5]],s=1.2),
               dict(k='g',kf=[[0,-2,6]],s=1.3),dict(k='g',kf=[[0,3,4.5]],s=1.4),dict(k='g',kf=[[0,-5,8.5]],s=1.5),dict(k='g',kf=[[0,6,9]],s=1.6),dict(k='g',kf=[[0,1,12]],s=1.7)],
      zones=[dict(s=3.0,e=6.5,poly=[[-8,.5],[-2.5,.5],[-2.5,6],[-8,6]],c='a',a=.9,l='Nahpfosten'),dict(s=6.8,e=10.3,poly=[[2.5,.5],[8.5,.5],[8.5,6],[2.5,6]],c='b',a=.9,l='Fernpfosten'),dict(s=10.6,e=14.1,poly=[[-6,12],[7,12],[7,18],[-6,18]],c='y',a=.9,l='Rückraum')],
      ball=[[0,-20,.8],[14.4,-20,.8],[15.6,4,3.5]],
      circles=[dict(s=15.6,x=4,y=3.5,r=2.2,c='a')],
      snd=[[3.0,'pop'],[6.8,'pop'],[10.6,'pop'],[14.4,'kick'],[15.7,'ding']])
    return B('2026-12-29_eckball','SPIELFELD · ECKBALL','Eckball:','Wo steht wer?',[pit],pun('Nahpfosten.',['Fernpfosten.','b'],['Rückraum.','y']),END('Standards sind Plan.','Jeder hat seinen Bereich.'),note=NOTE_P)
@reg('2026-12-30_spielerfehlschluss')
def _():
    for sd in range(1,500):
        r=random.Random(sd); tail=[1 if r.random()<.5 else 0 for _ in range(20)]
        if sum(tail)==10: break
    seq=[1]*5+tail
    sc1=dots('Münze: 5× Kopf – und danach?',seq,5,1.2,10,'KOPF NACH DER SERIE','ANTEIL',d=14,sym=['K','Z'],pre=5,note='Die Münze hat kein Gedächtnis.',noteT=10.5)
    sc2=big('Nach 5× Kopf',50,0,' %',ring=.5,c='a',top='NÄCHSTER WURF',sub='Auch nach einer langen Serie bleibt die Chance bei 50 %.',d=7.5)
    return B('2026-12-30_spielerfehlschluss','MYTHOS & METHODE · FEHLSCHLUSS','Spielerfehlschluss:','Jetzt muss es klappen?',[sc1,sc2],pun('Der Zufall',['rechnet nicht auf.','a']),END('Keine Serie schuldet dir etwas.','Weder Glück noch Pech.','Simulation, 20 Würfe'),note=NOTE_M)
@reg('2026-12-31_rueckblick')
def _():
    it=[dict(h='1. September: Die Testphase beginnt',s='Daten sammeln, Regeln prüfen.',b='1'),dict(h='11. Oktober: Erste Meldungen verschickt',s='Ab jetzt zählt der echte Zeitpunkt.',b='2'),dict(h='Herbst: Jedes Ergebnis wird öffentlich',s='Im Ergebnis-Kanal auf Telegram.',b='3'),dict(h='8. Januar 2027: Der Start',s='Live-Wetten-Analyse für Fußball per Telegram.',b='4')]
    return B('2026-12-31_rueckblick','HINTER DEN KULISSEN · RÜCKBLICK','2026 in Bildern:','Der Weg zum Start',[steps('Vier Stationen',it,d=18,tl=True)],pun('Ein Jahr.',['Ein Plan.','a']),END('Danke für 2026.','Auf ein ehrliches 2027.'),note=None)
@reg('2027-01-01_fehlerspanne')
def _():
    ns=[100,400,1000,2500]; hw=[1.96*math.sqrt(.55*.45/n)*100 for n in ns]
    it=[dict(l=f"{n:,} Wetten".replace(',','.'),v=round(h,1),dec=1,suf=' Punkte',pre='±',c='w' if n<500 else ('y' if n<2000 else 'a'),n='Unsicherheit bei 55 % Trefferquote') for n,h in zip(ns,hw)]
    sc=bars('Wie genau kennst du deine Trefferquote? (95 %-Bereich)',it,11,d=15,start=.9,tail=1.8)
    return B('2027-01-01_fehlerspanne','ZAHL DER WOCHE · STICHPROBE','Wie viele Wetten','braucht ein Beleg?',[sc],pun('Mehr Wetten.',['Weniger Unsicherheit.','a']),END('Geduld ist Statistik.','Gute Zahlen brauchen Zeit.',NOTE_M))
@reg('2027-01-02_zwei-tore-in-zehn')
def _():
    f=lambda w: Pge(2,L*w/90); assert abs(f(10)-.0369)<.0005
    xs=list(range(2,31,2)); ys=[f(w) for w in xs]
    sc=live_curve('Mindestens zwei Tore innerhalb eines Zeitfensters',xs,ys,30,[0,.1,.2,.3],[0,5,10,15,20,25,30],[10,20,30],'Fenster',' Min.',xmin=0,ymax=.32,cm='one',labels=['10 Minuten','20 Minuten','30 Minuten'])
    return B('2027-01-02_zwei-tore-in-zehn','LIVE-RECHNUNG · TORFLUT','Zwei Tore','in zehn Minuten?',[sc],pun('Selten.',['Aber möglich.','a']),END('Kurze Fenster','sind teuer.',NOTE_M))
@reg('2027-01-03_hilfe')
def _():
    it=[dict(h='check-dein-spiel.de',s='Selbsttest und Beratung, anonym online.',b='1'),dict(h='Telefon: 0800 1 37 27 00',s='Beratung zu Glücksspielproblemen, kostenfrei.',b='2'),dict(h='Selbstsperre über OASIS',s='Bei lizenzierten Anbietern, bundesweit.',b='3')]
    return B('2027-01-03_hilfe','VERANTWORTUNG · HILFE','Wann Hilfe holen?','Früh. Nicht später.',[steps('Drei Anlaufstellen',it,d=15.5)],pun('Hilfe holen',['ist stark.','a']),END('Du bist nicht allein.','check-dein-spiel.de · 0800 1 37 27 00',NOTE_V),note=NOTE_V)
@reg('2027-01-04_doppelte-chance')
def _():
    ps=[45,27,28]; dc=ps[0]+ps[1]; q=100/dc; assert abs(q-1.389)<.001
    sc1=bars('Beispielwerte: Heimsieg · Remis · Auswärtssieg',[dict(l='Heimsieg (1)',v=45,dec=0,suf=' %',c='a'),dict(l='Remis (X)',v=27,dec=0,suf=' %',c='b'),dict(l='Auswärtssieg (2)',v=28,dec=0,suf=' %',c='m')],60,d=10,start=.9,tail=1.8)
    sc2=big('Doppelte Chance 1X',dc,0,' %',ring=dc/100,c='a',top='45 % + 27 %',bot='FAIRE QUOTE '+fm(q,2),sub='Wahrscheinlichkeiten werden addiert, Quoten nicht.',d=8.5)
    return B('2027-01-04_doppelte-chance','MATHE-MONTAG · DOPPELTE CHANCE','Doppelte Chance:','Chancen addieren',[sc1,sc2],pun('Chancen addieren.',['Quoten nicht.','a']),END('Erst Prozent,','dann Quote.',NOTE_M))
@reg('2027-01-05_strafraum')
def _():
    pit=dict(type='pitch',d=19,cap='Die Maße im Strafraum',
      players=[],
      zones=[dict(s=1.0,poly=[[-9.16,0],[9.16,0],[9.16,5.5],[-9.16,5.5]],c='a',a=.8),dict(s=4.6,poly=[[-20.15,0],[20.15,0],[20.15,16.5],[-20.15,16.5]],c='b',a=.35)],
      lines=[dict(s=1.6,x1=-12,y1=0,x2=-12,y2=5.5,l='5,5 m',lx=-60,c='a',d=.8),dict(s=5.2,x1=-18,y1=0,x2=-18,y2=16.5,l='16,5 m',lx=-70,c='b',d=1.0),dict(s=8.4,x1=0,y1=0,x2=0,y2=11,l='11 m',lx=50,d=1.0),dict(s=12.0,x1=-3.66,y1=-1.3,x2=3.66,y2=-1.3,l='7,32 m',d=.9)],
      labels=[dict(s=2.0,e=4.5,x=0,y=3.4,txt='Torraum',c='t'),dict(s=5.6,x=-8,y=14,txt='Strafraum',c='t'),dict(s=9.0,x=2.6,y=11.4,txt='Elfmeterpunkt',c='t')],
      snd=[[1.0,'pop'],[1.6,'pass'],[4.6,'pop'],[5.2,'pass'],[8.4,'whoosh'],[9.6,'ding'],[12.0,'pass']])
    return B('2027-01-05_strafraum','SPIELFELD · MASSE','Die Maße','im Strafraum',[pit],pun('5,5 Meter.',['16,5 Meter.','b'],['11 Meter.','a']),END('Feste Regeln.','Quelle: IFAB, Regel 1'),note=NOTE_P+' · Quelle: IFAB')
@reg('2027-01-06_ueberanpassung')
def _():
    import numpy as np
    deg=list(range(1,11))
    for sd in range(1,300):
        r=np.random.default_rng(sd); x=np.sort(r.uniform(0,1,20)); y=np.sin(2*np.pi*x)+r.normal(0,.3,20); xt=np.linspace(0,1,400); yt=np.sin(2*np.pi*xt)+r.normal(0,.3,400)
        tr=[];te=[]
        for d in deg:
            c=np.polyfit(x,y,d); tr.append(float(np.mean((np.polyval(c,x)-y)**2))); te.append(float(np.mean((np.polyval(c,xt)-yt)**2)))
        best=int(np.argmin(te))+1
        if 3<=best<=5 and te[-1]>te[best-1]*2.5 and all(tr[i]>=tr[i+1]-1e-9 for i in range(9)): break
    assert te[-1]>te[best-1]*2.5
    te_c=[min(v,1.0) for v in te]
    ser=[dict(xs=deg,ys=[round(v,3) for v in tr],c='b',n='Training'),dict(xs=deg,ys=[round(v,3) for v in te_c],c='w',n='Neue Daten')]
    sc=live_curve('Je komplexer das Modell, desto besser passt es zu alten Daten',None,None,10,[0,.25,.5,.75,1.0],[1,2,3,4,5,6,7,8,9,10],[1,best,10],'Komplexität','',cm=None,series=ser,xmin=1,ymax=1.0,yfmt='raw',labels=['Zu einfach',f'Grad {best}: am besten','Zu komplex'])
    for c,xv in zip(sc['calls'],[1,best,10]): c['l2']='Neue Daten: '+fm(te[xv-1],2)
    sc['xl']='Modellkomplexität (Polynomgrad)'
    return B('2027-01-06_ueberanpassung','MYTHOS & METHODE · ÜBERANPASSUNG','Mehr Daten sind','nicht immer besser',[sc],pun('Zu viel Anpassung',['täuscht.','w']),END('Gut auf alten Daten','heißt nicht gut auf neuen.','Simulation mit Zufallsdaten (Fehler = mittlerer quadratischer Fehler)'),note='Simulation · Fehler = mittlerer quadratischer Fehler, über 1,0 abgeschnitten')
@reg('2027-01-07_start')
def _():
    it=[dict(h='Live-Wetten-Analyse für Fußball',s='Per Telegram, mit klaren Regeln.',b='1'),dict(h='Alle Ergebnisse öffentlich',s='Auch die schwachen. Im Ergebnis-Kanal.',b='2'),dict(h='18+ · Keine Gewinngarantie',s='Wetten kann Geld kosten. Hilfe: check-dein-spiel.de',b='3')]
    return B('2027-01-07_start','HINTER DEN KULISSEN · START','Der Start:','8. Januar 2027',[steps('Was dich erwartet',it,d=15.5,tl=True)],pun('Klare Regeln.',['Offene Zahlen.','a']),END('Start am 8. Januar 2027.','Sportwetten Radar'),note='18+ · Keine Gewinngarantie')
@reg('2027-01-08_drei-zahlen')
def _():
    a=Pge(2,L)*100; b=Pge(3,L)*100; c=Pk(0,L)*100
    it=[dict(h=f"{fm(c,1)} %",s='Chance auf ein 0:0 (Modell, 2,7 Tore je Spiel)',b='1'),dict(h=f"{fm(a,1)} %",s='Chance auf Über 1,5 Tore',b='2'),dict(h=f"{fm(b,1)} %",s='Chance auf Über 2,5 Tore',b='3')]
    return B('2027-01-08_drei-zahlen','ZAHL DER WOCHE · START','Drei Zahlen','zum Start',[steps('Das Modell in drei Zeilen',it,d=15)],pun('Drei Zahlen.',['Ein Modell.','a']),END('Grundlagen zuerst.','Dann die Details.',NOTE_M))
@reg('2026-11-13_quote-lesen')
def _():
    q=[1.25,2.00,3.00]; it=[dict(l=f"Quote {fm(x,2)}",v=round(100/x,1),dec=1,suf=' %',c=c,n=f"1 ÷ {fm(x,2)}") for x,c in zip(q,'abw')]
    sc1=bars('Quote in Chance umgerechnet: 1 ÷ Quote',it,100,d=10.5,start=.9,tail=1.8)
    sc2=big('Quote 2,00',50,0,' %',ring=.5,c='a',top='SO SCHÄTZT DER ANBIETER',bot='= 1 ÷ 2,00',sub='Je niedriger die Quote, desto wahrscheinlicher hält der Anbieter das Ereignis.',d=8)
    return B('2026-11-13_quote-lesen','MATHE · QUOTE','So liest man','eine Quote',[sc1,sc2],pun('Eine Quote ist',['eine Schätzung.','a'],['Keine Vorhersage.','w']),END('Erst umrechnen,','dann einschätzen.',NOTE_M))
@reg('2026-11-13_verlustaversion')
def _():
    for sd in range(1,2000):
        r=random.Random(sd); seq=[1 if r.random()<.5 else 0 for _ in range(40)]
        if sum(seq)!=20: continue
        real=[0];fel=[0]
        for x in seq: real.append(real[-1]+(1 if x else -1)); fel.append(fel[-1]+(1 if x else -2.25))
        if min(real)>=-4 and max(real)<=4 and abs(real[10])<=2 and abs(real[20])<=2: break
    xs=list(range(41))
    ser=[dict(xs=xs,ys=real,c='b',n='Tatsächliche Bilanz'),dict(xs=xs,ys=[round(v,2) for v in fel],c='w',n='Gefühlte Bilanz')]
    sc1=live_curve('Faire Münze, 40 Wetten. Gefühlt zählt ein Verlust 2,25-mal',None,None,40,[-30,-20,-10,0,10],[0,10,20,30,40],[0,10,20,40],'Wette','',cm='multi',series=ser,xmin=0,ymin=-32,ymax=12,yfmt='raw',labels=['Start','Nach 10 Wetten','Nach 20 Wetten','Nach 40 Wetten'])
    it=[dict(h='Grenze vorher festlegen',s='Einsatz und Limit stehen vor der ersten Wette.',b='1'),dict(h='Gleicher Einsatz. Immer.',s='Nach einem Verlust nicht erhöhen.',b='2'),dict(h='Pause statt Aufholjagd',s='Nach einer Serie bewusst aufhören.',b='3')]
    sc2=steps('Drei Regeln gegen den Reflex',it,d=10.5)
    return B('2026-11-13_verlustaversion','VERANTWORTUNG · VERLUSTAVERSION','Warum Verluste','schwerer wiegen',[sc1,sc2],pun('Rechnerisch ±0.',['Gefühlt im Minus.','w']),END('Vorher entscheiden.','Hilfe: check-dein-spiel.de',NOTE_V),note='Faktor 2,25: Tversky & Kahneman (1992) · check-dein-spiel.de')
if __name__=='__main__':
    import sys
    mode,name=sys.argv[1],sys.argv[2]; cfg=V[name]()
    if mode=='frames':
        ts=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else None
        if ts is None:
            ts=[]
            for S in cfg['scenes']: ts+= [S['t0']+S['d']*.35,S['t0']+S['d']-.9]
            ts+=[cfg['punch']['t0']+2.4,cfg['end']['t0']+1.5]
        frames(cfg,ts); print(name,cfg['dur'])
    else: print(video(cfg,'/home/claude/medien/immersiv'))
