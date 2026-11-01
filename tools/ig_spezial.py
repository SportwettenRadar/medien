#!/usr/bin/env python3
"""Instagram-Spezialwissen (Inhaltsniveau, 01.11.2026): Karussell-Karten 1080x1350 und Reels 1080x1920.

Karten:  python3 ig_spezial.py karten <ziel-ordner>
Reels:   python3 ig_spezial.py reels  <ziel-ordner>
Schriften/Logo aus dem Homepage-Repo (HOME). Alle Rechenbeispiele sind in Python nachgerechnet (siehe Prüfskript in der Sitzung).
Instagram-Regeln: keine Links/Homepage im Bild, keine Trefferquoten-Prozente zu eigenen Ergebnissen, 18+ Hinweis.
"""
import json, os, sys, tempfile, html, glob

HOME = "/home/claude/sportwettenradar/sportwetten-radar.net"
HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, "..", "youtube", "erklaer", "specs")

CSS = """
@font-face{font-family:B;font-weight:700;src:url('FONTS/baloo-2-latin-700-normal.woff2')}
@font-face{font-family:B;font-weight:800;src:url('FONTS/baloo-2-latin-800-normal.woff2')}
@font-face{font-family:I;font-weight:400;src:url('FONTS/inter-latin-400-normal.woff2')}
@font-face{font-family:I;font-weight:600;src:url('FONTS/inter-latin-600-normal.woff2')}
@font-face{font-family:M;font-weight:400;src:url('FONTS/ibm-plex-mono-latin-400-normal.woff2')}
@font-face{font-family:M;font-weight:500;src:url('FONTS/ibm-plex-mono-latin-500-normal.woff2')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;background:#0a1620;color:#eef3f8;overflow:hidden}
body{position:relative;font-family:I;background:#0a1620}
svg.r{position:absolute;right:-120px;top:-120px;width:820px;height:820px}
.top{position:absolute;left:88px;top:96px;display:flex;align-items:center;gap:26px}
.top img{width:110px;height:110px;border-radius:26px}
.top span{font-family:B;font-weight:800;font-size:50px}
.eb{position:absolute;left:88px;top:300px;font-family:M;font-weight:500;font-size:31px;letter-spacing:.16em;color:#2edb99;text-transform:uppercase}
.main{position:absolute;left:88px;right:88px;top:362px}
h1{font-family:B;font-weight:800;font-size:78px;line-height:1.04;letter-spacing:-.01em;color:#f0f4f9}
h1.c{font-size:92px}
h1 em{font-style:normal;color:#2edb99}
.hint{font-family:I;font-size:36px;color:#7f93a8;margin-top:60px}
.p{background:#0f1d2c;border:2px solid #1b2c40;border-radius:30px;padding:34px 40px;margin-top:30px;font-size:38px;line-height:1.38;color:#e8eef5}
.p b{color:#fff;font-weight:600}
.p.n{display:flex;gap:30px;align-items:flex-start}
.p.n i{flex:none;font-style:normal;font-family:M;font-weight:500;font-size:30px;color:#0a1620;background:#2edb99;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-top:2px}
.main.s .p{font-size:33px;padding:24px 34px;margin-top:22px;line-height:1.34}
.main.s .p.n i{width:48px;height:48px;font-size:26px}
.sub{font-size:34px;line-height:1.4;color:#a9b8c8;margin-top:26px}
.foot{position:absolute;left:88px;right:88px;bottom:84px;display:flex;justify-content:space-between;font-family:M;font-size:27px;color:#6f8399}
"""

RINGS = ('<svg class="r" viewBox="0 0 820 820"><g fill="none" stroke="#2edb99" stroke-opacity=".28" stroke-width="2">'
         '<circle cx="410" cy="410" r="200"/><circle cx="410" cy="410" r="320"/><circle cx="410" cy="410" r="440"/>'
         '<circle cx="410" cy="410" r="560"/><circle cx="410" cy="410" r="680"/></g>'
         '<line x1="410" y1="410" x2="640" y2="250" stroke="#2edb99" stroke-opacity=".5" stroke-width="3"/></svg>')

ABS = "Rechenbeispiel, keine Empfehlung."


def e(s):
    return (html.escape(s).replace("[[", "<em>").replace("]]", "</em>").replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>").replace("\n", "<br>"))


def card(kind, eb, title, items=None, sub=None, hint=None):
    small = kind == "list" and sum(len(x) for x in items) > 190
    body = f'<div class="eb">{e(eb)}</div><div class="main{" s" if small else ""}"><h1 class="{"c" if kind=="cover" else ""}">{e(title)}</h1>'
    if kind == "list":
        body += "".join(f'<div class="p n"><i>{i+1}</i><div>{e(x)}</div></div>' for i, x in enumerate(items))
    elif kind == "panel":
        body += f'<div class="p">{e(items)}</div>'
    if sub:
        body += f'<div class="sub">{e(sub)}</div>'
    if hint:
        body += f'<div class="hint">{e(hint)}</div>'
    body += "</div>"
    top = '<div class="top"><img src="LOGO"><span>Sportwetten Radar</span></div>'
    foot = '<div class="foot"><span>18+ · Keine Gewinngarantie</span><span>@sportwetten_radar</span></div>'
    return RINGS + top + body + foot


def deck(thema, eb, titel, slides):
    out = [card("cover", eb, titel, hint=("Wischen für die Fakten →" if thema == "oasis" else "Wischen für den Rechenweg →"))]
    n = len(slides)
    for i, s in enumerate(slides):
        out.append(card(s[0], f"Teil {i+1} von {n}", s[1], s[2], s[3] if len(s) > 3 else None))
    return out


DECKS = {
    "poisson": deck("poisson", "Live-Wetten, genauer", "Über 1,5 live: Die Restzeit bestimmt den Preis", [
        ("panel", "Das Modell: Tore als Zufall",
         "Rechenbeispiel: 2,7 Tore pro 90 Minuten, also 0,03 pro Minute. Wir nehmen an, dass Tore mit gleichbleibender Rate fallen (Poisson-Verteilung)."),
        ("list", "Bei 0:0: mindestens 2 weitere Tore", [
            "Minute 30 (60 min Rest): <b>53,7 %</b>, faire Quote 1,86",
            "Minute 60 (30 min Rest): <b>22,8 %</b>, faire Quote 4,40",
            "Minute 80 (10 min Rest): <b>3,7 %</b>, faire Quote 27,1"]),
        ("list", "Minute 60: 0:0 gegen 1:0", [
            "Bei 0:0 braucht Über 1,5 noch <b>zwei</b> Tore: 22,8 %.",
            "Bei 1:0 reicht <b>ein</b> Tor: 59,3 %, faire Quote 1,69.",
            "Der Spielstand ändert den Preis stärker als die Uhr."]),
        ("panel", "Wo das Modell hinkt",
         "Die Rate ist nicht konstant: Zum Spielende steigt sie leicht, nach Führung, Rückstand oder Platzverweis ändert sie sich. Das Beispiel zeigt die Logik, nicht den echten Preis.", ABS),
    ]),
    "marge": deck("marge", "Quoten, genauer · Teil 2", "Die Marge in der Quote selbst herausrechnen", [
        ("list", "Schritt 1: Quote in Wahrscheinlichkeit", [
            "Implizite Wahrscheinlichkeit = 1 geteilt durch Quote.",
            "Über 1,90 und Unter 1,90: je <b>52,63 %</b>.",
            "Zusammen <b>105,26 %</b>. Alles über 100 % ist die Marge."]),
        ("list", "Schritt 2: Marge herausrechnen", [
            "Beispiel: Über 1,80 und Unter 2,00 ergibt 55,56 % + 50 % = <b>105,56 %</b>.",
            "Jede Seite durch die Summe teilen: Über <b>52,63 %</b>, Unter <b>47,37 %</b>.",
            "Faire Quoten ohne Marge: Über <b>1,90</b>, Unter <b>2,11</b>."]),
        ("panel", "Bei Kombis wird es mehr",
         "Zwei Quoten à 1,90 ergeben 3,61. Fair wären 4,00. Die Marge wächst auf rund <b>10,8 %</b>. Die Schwelle zum Ausgleich liegt bei 27,7 % statt fairer 25 %.", ABS),
        ("panel", "Merke",
         "Die Marge ist die Hürde, bevor irgendeine Analyse zählt. Dieser Beitrag vertieft unseren Beitrag „Was ist die Marge?“ vom 29.10."),
    ]),
    "clv": deck("clv", "Wetten prüfen", "Closing Line Value: Warum die Schlussquote ehrlicher ist als ein Ergebnis", [
        ("panel", "Das Problem",
         "Ein Ergebnis misst viel Glück. Eine gute Wette kann verlieren, eine schlechte gewinnen. Bei wenigen Wetten sagt das Ergebnis fast nichts über die Qualität."),
        ("list", "Gegen die Schlussquote messen", [
            "Die Schlussquote kurz vor Anpfiff gilt als beste Schätzung des Marktes.",
            "Wer vorher zu <b>2,00</b> bekam und der Markt schloss bei <b>1,80</b>, hatte den besseren Preis.",
            "Der Vorsprung: 2,00 geteilt durch 1,80 minus 1 = <b>+11,1 %</b>."]),
        ("panel", "Warum das hilft",
         "Qualität sieht man früher als Gewinn. Wer die Schlussquote regelmäßig schlägt, kauft im Schnitt zu besseren Preisen, auch wenn kurzfristig Verluste stehen.", ABS),
        ("panel", "Die Grenze, vor allem live",
         "Live gibt es keine echte Schlussquote. Preise ändern sich laufend, der Vergleichswert ist unklar. Das Prinzip ist ein Hinweis, kein Beweis."),
    ]),
    "spielstand": deck("spielstand", "Live-Modelle", "Spielstand-Effekt: Warum Teams in Führung anders spielen", [
        ("list", "Führung und Rückstand", [
            "Führende Teams verteidigen tendenziell tiefer und suchen Konter.",
            "Zurückliegende Teams gehen Risiko, die Räume hinten werden größer.",
            "Auswechslungen und Platzverweise verschieben das nochmals."]),
        ("panel", "Folge für Modelle",
         "Tore pro Minute sind nicht konstant. Wer nur die durchschnittliche Torrate nimmt, ignoriert, wer führt. Deshalb ist die Restzeit-Rechnung eine Vereinfachung."),
        ("list", "Gleiche Statistik, anderer Wert", [
            "Viele Schüsse beim Rückstand bedeuten oft Druck, den man nicht überbewerten sollte.",
            "Wenige Schüsse bei Führung können Absicht sein, nicht Schwäche.",
            "Zahlen brauchen den Kontext des Spielstands."]),
        ("panel", "Merke", "Erst der Kontext macht aus Daten ein Signal. Eine Zahl ohne Spielstand, Zeit und Spielverlauf kann in die Irre führen."),
    ]),
    "stichprobe": deck("stichprobe", "Zahlen ehrlich lesen", "Stichprobe: Wie viele Versuche braucht eine Aussage?", [
        ("panel", "Eine Verwandlungsquote streut",
         "Rechenbeispiel: Ein Schütze verwandelt 60 von 100 Elfmetern. Statistisch liegt seine wahre Verwandlungsquote grob zwischen <b>50,4 %</b> und <b>69,6 %</b> (95-%-Intervall).", ABS),
        ("panel", "Die Rechnung dahinter",
         "Standardfehler = Wurzel aus (p × (1 − p) geteilt durch n). Hier etwa 4,9 Punkte, mal 1,96 ergibt rund ±9,6 Punkte."),
        ("list", "Wie viel ist genug?", [
            "Bei 100 Versuchen: etwa <b>±9,6</b> Punkte.",
            "Bei 250 Versuchen: etwa <b>±6,1</b> Punkte.",
            "Bei 1.000 Versuchen: etwa <b>±3,0</b> Punkte."],
         "Genauigkeit des 95-%-Intervalls bei etwa 60 % Verwandlungsquote. Für ±3 Punkte braucht man rund 1.000 Versuche."),
        ("panel", "Für Ergebnisse jeder Art",
         "Ein Monat ist kein Beweis. Bei Quoten mit unterschiedlichen Preisen streut der Ertrag sogar stärker und braucht noch mehr Versuche.", ABS),
    ]),
    "oasis": deck("oasis", "Verantwortungsvoll wetten", "Selbstsperre: Was die Sperrdatei OASIS ist und wie sie wirkt", [
        ("list", "Das bundesweite Sperrsystem", [
            "Spielersperrsystem nach dem Glücksspielstaatsvertrag 2021, Anträge beim <b>Regierungspräsidium Darmstadt</b>.",
            "Anbieter müssen gesperrte Personen ausschließen, unter anderem bei <b>Sportwetten</b>, Online-Casino und Spielhallen.",
            "Die Sperre gilt für alle teilnehmenden Anbieter, nicht nur für einen."]),
        ("list", "Dauer und Aufhebung", [
            "Selbstsperre: ohne Angabe <b>ein Jahr</b>. Kürzer ist möglich, aber <b>nicht unter drei Monaten</b>.",
            "Fremdsperre durch Dritte: mindestens <b>ein Jahr</b>.",
            "Aufheben geht nur auf <b>schriftlichen Antrag</b>, sonst bleibt die Sperre bestehen."]),
        ("panel", "Eigene Limits",
         "Zusätzlich kannst du bei jedem Anbieter eigene Limits setzen. Besser vor dem Moment, in dem es eng wird: wenn du Verluste zurückholen willst oder mehr einsetzt als geplant."),
        ("panel", "Hilfe",
         "Kostenlos und anonym: check-dein-spiel.de und 0800 1 37 27 00 (BZgA). Quellen: Verbraucherzentrale (EVZ), Regierungspräsidium Darmstadt."),
    ]),
}


def render_cards(outdir):
    from playwright.sync_api import sync_playwright
    os.makedirs(outdir, exist_ok=True)
    fonts = "file://" + os.path.join(HOME, "assets/fonts")
    logo = "file://" + os.path.join(HOME, "logo-icon.png")
    css = CSS.replace("FONTS", fonts)
    tmp = tempfile.mkdtemp()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for name, slides in DECKS.items():
            for i, h in enumerate(slides, 1):
                hp = os.path.join(tmp, f"{name}{i}.html")
                open(hp, "w", encoding="utf-8").write(
                    f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{h.replace("LOGO", logo)}</body></html>')
                pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                bottom = pg.evaluate("(()=>{const m=document.querySelector('.main');return Math.round(m.getBoundingClientRect().bottom)})()")
                if bottom > 1215:
                    print(f"WARNUNG {name} Folie {i}: Unterkante {bottom}")
                pg.screenshot(path=os.path.join(outdir, f"{name}_{i}.png"))
        b.close()
    print("Karten fertig:", outdir)


# ---------- Reels ----------
IG_EDITS = {
    30: lambda sp: _oasis(sp),
    26: lambda sp: _marge(sp),
    27: lambda sp: _clv(sp),
}


def _marge(sp):
    for f in sp["folien"]:
        if f.get("eyebrow") == "Folge für die Trefferquote":
            f["eyebrow"] = "Folge für die Quote"
            f["text"] = "Bei 1,90 liegt die\nHürde bei 52,6 %."
            f["sub"] = "Diese Schwelle ergibt sich allein aus der Quote, bevor irgendeine Analyse zählt. Rechenbeispiel."
        if f.get("eyebrow") == "Bei Kombis wird es mehr":
            f["sub"] = "Break-even: 27,7 % statt fairer 25 %. Die Marge wächst grob auf 10,8 %. Rechenbeispiel."


def _clv(sp):
    for f in sp["folien"]:
        if f.get("eyebrow") == "Warum das hilft":
            f["sub"] = "Wer die Schlussquote regelmäßig schlägt, kauft im Schnitt zu besseren Preisen, auch wenn kurzfristig Verluste stehen. Rechenbeispiel."


def _oasis(sp):
    """Instagram-Fassung: nur geprüfte Fakten (Verbraucherzentrale/Regierungspräsidium), kein Betrag zum Einzahlungslimit."""
    for f in sp["folien"]:
        if f.get("text") == "Dauer und Aufhebung":
            f["punkte"] = ["Selbstsperre: ohne Angabe <b>ein Jahr</b>. Kürzer ist möglich, aber <b>nicht unter drei Monaten</b>.",
                           "Fremdsperre durch Dritte: mindestens <b>ein Jahr</b>.",
                           "Aufheben geht nur auf <b>schriftlichen Antrag</b>, sonst bleibt die Sperre bestehen."]
        if f.get("eyebrow") == "Das Einzahlungslimit":
            f["eyebrow"] = "Eigene Limits"
            f["text"] = "Du kannst bei jedem\nAnbieter eigene Limits setzen."
            f["sub"] = "Zusätzlich zur Sperre. Am besten vorher, bevor es eng wird."


def render_reels(outdir, nums=(25, 26, 27, 28)):
    sys.path.insert(0, HERE)
    import erklaervideo as E
    E.HOCH = True
    E.W, E.H = 1080, 1920
    orig = E.folie_html

    def fh(f, logo):
        if f["typ"] == "ende":
            top = f'<div class="top"><img src="{logo}"><span>Sportwetten <b>Radar</b></span></div>'
            body = ('<div class="main end"><div class="eb">Sportwetten Radar</div>'
                    '<h1 class="k">Zahlen statt <em>Bauchgefühl</em>.</h1>'
                    '<div class="hint">Rechenbeispiel, keine Empfehlung · 18+ · Keine Gewinngarantie · Glücksspiel kann süchtig machen · check-dein-spiel.de</div></div>')
            return top + body
        return orig(f, logo).replace("<span>sportwetten-radar.net</span>", "<span>@sportwetten_radar</span>")

    E.folie_html = fh
    os.makedirs(outdir, exist_ok=True)
    for nr in nums:
        src = glob.glob(os.path.join(SPECS, f"{nr}_*.json"))[0]
        sp = json.load(open(src, encoding="utf-8"))
        if nr in IG_EDITS:
            IG_EDITS[nr](sp)
        tmp = tempfile.mkdtemp()
        pngs = E.render(sp, HOME, tmp)
        out = os.path.join(outdir, f"reel_{os.path.basename(src).rsplit('.',1)[0]}.mp4")
        d = E.baue(sp, pngs, out)
        print(f"ok {out} {d:.1f}s")


if __name__ == "__main__":
    mode, outdir = sys.argv[1], sys.argv[2]
    if mode == "karten":
        render_cards(outdir)
    elif mode == "reels":
        render_reels(outdir, tuple(int(x) for x in sys.argv[3:]) or (25, 26, 27, 28))
