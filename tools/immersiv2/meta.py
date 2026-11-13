import json,sys,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import topics_all as T
from engine import *
HOOK={'2026-11-14_restzeit':'Was ist ein zweites Tor in Minute 80 noch wert?','2026-11-15_budget':'Wie viel darfst du verlieren?','2026-11-16_quote-in-chance':'Was sagt eine Quote wirklich?','2026-11-17_torchance':'Wie wahrscheinlich ist dieses Tor?','2026-11-18_marge':'Warum ergeben Quoten mehr als 100 %?','2026-11-19_verzoegerung':'Wie live ist „live“ wirklich?','2026-11-20_zehn-tipps':'Wie viele von 10 Tipps treffen wirklich?','2026-11-21_nachspielzeit':'Was bringen 5 Minuten Nachspielzeit?','2026-11-22_verluste':'Was kostet es, Verluste zurückzuholen?','2026-11-23_breakeven':'Ab wann lohnt sich Quote 1,60?','2026-11-24_elfmeter':'Wie schnell ist ein Elfmeter?','2026-11-25_clv':'Wie erkennst du, ob du den Markt schlägst?','2026-11-26_uhrzeiten':'Warum zählt die Uhrzeit?','2026-11-27_pechserien':'Wie lang kann eine Pechserie sein?','2026-11-28_nach-dem-1-0':'Reicht eine Führung nach 30 Minuten?','2026-11-29_limits':'Was helfen Limits wirklich?','2026-11-30_kombi':'Wie wahrscheinlich ist eine 5er-Kombi?','2026-12-01_abseits':'Wann ist es wirklich Abseits?','2026-12-02_spielstand':'Warum ändert ein 1:0 das ganze Spiel?','2026-12-03_oeffentlich':'Warum zeigen wir jedes Ergebnis?','2026-12-04_nullnull':'Wie oft gibt es an einem Spieltag ein 0:0?','2026-12-05_nullnull-modell':'Wie oft endet ein Spiel 0:0?','2026-12-06_warnsignale':'Erkennst du diese Warnsignale?','2026-12-07_erwartungswert':'Was kostet ein kleiner Quotenunterschied?','2026-12-08_torwart-winkel':'Warum kommen Torhüter heraus?','2026-12-09_stichprobe':'Was beweisen 10 Würfe?','2026-12-10_nie':'Was werden wir nie tun?','2026-12-11_fuenf-tore':'Wie oft fallen 5 Tore in einem Spiel?','2026-12-12_fahrstuhl':'Wie schnell fallen die Chancen?','2026-12-13_treppe':'Treppe oder Spirale?','2026-12-14_torverteilung':'Was heißt 2,7 Tore im Schnitt?','2026-12-15_mauer':'Wie weit steht die Mauer?','2026-12-16_oasis':'Wie funktioniert die Selbstsperre?','2026-12-17_testphase':'Testphase oder live?','2026-12-18_ueber25':'Wie oft Über 2,5 an einem Spieltag?','2026-12-19_modellgrenzen':'Wo irrt ein einfaches Modell?','2026-12-20_vorsaetze':'Dein Budget für 2027?','2026-12-21_ueber25-rechnung':'Wie hoch ist die Chance auf Über 2,5?','2026-12-22_konter':'Warum sind Konter so gefährlich?','2026-12-23_schwache-tage':'Wie viele Pleiten in Folge sind normal?','2026-12-24_auswertung':'Wie entsteht eine Auswertung?','2026-12-25_zufall-tippen':'Wie gut ist blindes Tippen?','2026-12-26_hz2':'Ist bei 0:0 zur Pause noch etwas drin?','2026-12-27_selbsttest':'Fünf ehrliche Fragen an dich','2026-12-28_beide-treffen':'Wie oft treffen beide Teams?','2026-12-29_eckball':'Wer steht beim Eckball wo?','2026-12-30_spielerfehlschluss':'Muss nach 5× Kopf Zahl kommen?','2026-12-31_rueckblick':'Wie sah 2026 bei uns aus?','2027-01-01_fehlerspanne':'Wie viele Wetten braucht ein Beleg?','2027-01-02_zwei-tore-in-zehn':'Zwei Tore in zehn Minuten?','2027-01-03_hilfe':'Wann solltest du Hilfe holen?','2027-01-04_doppelte-chance':'Wie rechnest du Doppelte Chance?','2027-01-05_strafraum':'Wie groß ist ein Strafraum?','2027-01-06_ueberanpassung':'Warum ist mehr Anpassung schlechter?','2027-01-07_start':'Was erwartet dich ab dem 8. Januar?','2027-01-08_drei-zahlen':'Drei Zahlen zum Start'}
MANUAL={'2026-11-14_restzeit':dict(eb='LIVE-RECHNUNG · ÜBER 1,5 TORE',t1='Die Restzeit bestimmt',t2='den Preis',punch=['Die Zeit läuft.','Die Chance sinkt.','Die Quote steigt.'],note=T.NOTE_M,src=''),
 '2026-11-17_torchance':dict(eb='TORCHANCE · NACHGESTELLT',t1='Wie wahrscheinlich',t2='ist dieses Tor?',punch=['Nähe und Winkel','entscheiden.'],note='Rechenbeispiel · vereinfachtes Modell · keine Empfehlung',src=''),
 '2026-12-09_stichprobe':dict(eb='MYTHOS & METHODE · STICHPROBE',t1='Kurze Serien',t2='täuschen',punch=['Je mehr Versuche,','desto näher an 55 %.'],note=T.NOTE_M,src='')}
def meta():
    out={}
    for n,f in T.V.items():
        c=f()
        if c is None: continue
        out[n]=dict(eb=c['eb'],t1=c['t1'],t2=c['t2'],punch=[l[0] for l in c['punch']['lines']],note=c['note'] or '',src=c['end'].get('n') or '')
    out.update(MANUAL); 
    return dict(sorted(out.items()))
H18='18+ · Keine Gewinngarantie. Wetten kann Geld kosten. Hilfe bei Spielproblemen: check-dein-spiel.de'
def texts(n,m):
    title=(m['t1']+' '+m['t2']).replace('  ',' ').strip(); body=' '.join(m['punch'])
    ex=''
    SRC={'2026-12-01_abseits':'Quelle: IFAB-Regelwerk, Regel 11','2026-12-15_mauer':'Quelle: IFAB-Regelwerk, Regel 13','2027-01-05_strafraum':'Quelle: IFAB-Regelwerk, Regel 1','2026-12-16_oasis':'Quelle: Europäisches Verbraucherzentrum (evz.de), Glücksspielbehörde der Länder'}
    if n in SRC: ex='\n'+SRC[n]
    elif ('Simulation' in m['src'] or 'Rechenbeispiel' in m['src']) and m['src']!=m['note']: ex='\n'+m['src']+'.'
    note=m['note'] if m['note'] and ('Rechenbeispiel' in m['note'] or 'Simulation' in m['note']) else ''
    if note.startswith('Rechenbeispiel ·') or note.startswith('Illustration'): note=note.replace(' · ',', ')+'.' if note.startswith('Rechen') else ''
    base=f"{title}\n\n{HOOK[n]} {body}\n{note}{ex}".replace('\n\n\n','\n\n').rstrip()
    return dict(title=title,ig=f"{base}\n\n{H18}\n\n#Fußball #Statistik #Analyse",tt=f"{base}\n\n18+ · Keine Gewinngarantie\n#fussball #statistik #analyse",yt=f"{base}\n\n{H18}\n\n#Shorts #Fußball #Statistik")
if __name__=='__main__':
    M=meta(); 
    for n,m in M.items(): m['hook']=HOOK[n]; m.update(texts(n,m))
    json.dump(M,open(f'{OUT}/meta.json','w'),ensure_ascii=False,indent=1)
    from playwright.sync_api import sync_playwright
    os.makedirs('/home/claude/medien/immersiv/hook',exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
        for n,m in M.items():
            cfg=dict(eb=m['eb'],t1=m['t1'],t2=m['t2'],hook=m['hook'],scenes=[],punch=dict(t0=0,lines=[]),end=dict(t0=0),name=n,dur=1)
            open(f'{OUT}/cfg_hook.js','w').write('window.CFG='+json.dumps(cfg,ensure_ascii=False)+';')
            for f in ('lib.js','gen.js'): open(f'{OUT}/{f}','w').write(open(f'{HERE}/{f}').read())
            open(f'{OUT}/page_hook.html','w').write(open(f'{HERE}/page.html.tpl').read().replace('CFGFILE','cfg_hook.js'))
            pg.goto('file://'+f'{OUT}/page_hook.html'); pg.wait_for_function('window.ready===true',timeout=20000)
            pg.evaluate('renderHook()'); pg.screenshot(path=f'/home/claude/medien/immersiv/hook/{n}.png')
        b.close()
    print(len(M))
