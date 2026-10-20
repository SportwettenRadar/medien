#!/usr/bin/env python3
"""Erzeugt die Google-Seiten für sportwetten-radar.net:
- monatsbericht-JJJJ-MM.html je Monat aus trackrecord-daten.js
- monatsberichte.html (Übersicht)
- live-wetten-ueber-unter.html, rendite-erklaert.html, verlustserien.html
- sitemap.xml
Aufruf: python3 seiten_generator.py /pfad/zum/repo
"""
import json, re, sys, os, datetime

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
V = "20261021"
BASE = "https://sportwetten-radar.net/"
WISSEN_DATUM = "2026-10-20"  # bei inhaltlicher Änderung der Wissen-Seiten anpassen
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]


def de(n, d=1):
    s = f"{abs(n):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def signed(n, d=1):
    if n > 0:
        return "+" + de(n, d)
    if n < 0:
        return "−" + de(n, d)
    return de(0, d)


def load_months():
    import subprocess
    out = subprocess.run(["node", "-e", "global.window={};require(process.argv[1]);console.log(JSON.stringify(window.TRACKRECORD))",
                          os.path.abspath(os.path.join(REPO, "trackrecord-daten.js"))], capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    return sorted([m for m in data if re.match(r"^\d{4}-\d{2}$", m.get("monat", ""))],
                  key=lambda m: m["monat"])


def mname(key):
    y, m = key.split("-")
    return f"{MONATE[int(m) - 1]} {y}"


def head(title, desc, path):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<meta name="theme-color" content="#0a1620">
<link rel="apple-touch-icon" href="assets/logo-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sportwetten Radar">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo-icon-small.png" type="image/png">
<link rel="stylesheet" href="style.css?v={V}">
<script>function loadScript(a){{var b=document.getElementsByTagName("head")[0],c=document.createElement("script");c.type="text/javascript",c.src="https://tracker.metricool.com/resources/be.js",c.onreadystatechange=a,c.onload=a,b.appendChild(c)}}loadScript(function(){{beTracker.t({{hash:"e60965c637f67cfd464d124c72f26885"}})}});</script>
</head>
<body>
"""


def nav_and_footer(repo_page="risikohinweis.html"):
    h = open(os.path.join(REPO, repo_page), encoding="utf-8").read()
    nav = h[h.index('<nav class="nav">'):h.index("</nav>") + 6]
    foot = h[h.index("<footer>"):h.index("</footer>") + 9]
    return nav, foot


def page(path, title, desc, eyebrow, h1, inner, ld=None):
    nav, foot = nav_and_footer()
    ldjs = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ""
    html = (head(title, desc, path).replace("</head>", ldjs + "</head>") + "\n" + nav + f"""

<div class="legal-header">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
  </div>
</div>

<article class="legal-doc legal-justify wissen">
  <a class="back-link" href="index.html">← Zurück zur Startseite</a>
{inner}
  <p class="wissen-foot">18+ · Sportwetten sind mit einem Verlustrisiko verbunden. Vergangene Ergebnisse sind kein Versprechen für zukünftige.
  Hilfe bei Glücksspielproblemen: <a href="tel:08001372700">0800 1 37 27 00</a> (kostenlos, anonym) · <a href="https://www.check-dein-spiel.de" target="_blank" rel="noopener">check-dein-spiel.de</a></p>
</article>

""" + foot + """

<script src="start.js"></script>
</body>
</html>
""")
    ref = open(os.path.join(REPO, "risikohinweis.html"), encoding="utf-8").read()
    v = re.search(r"style\.css\?v=([0-9a-z]+)", ref)
    if v:
        html = re.sub(r"style\.css\?v=[0-9a-z]+", "style.css?v=" + v.group(1), html)
    open(os.path.join(REPO, path), "w", encoding="utf-8").write(html)
    return path


def article_ld(title, desc, path, date):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
            "inLanguage": "de-DE", "datePublished": date, "dateModified": date,
            "mainEntityOfPage": BASE + path,
            "author": {"@type": "Organization", "name": "Sportwetten Radar", "url": BASE},
            "publisher": {"@type": "Organization", "name": "Sportwetten Radar",
                          "logo": {"@type": "ImageObject", "url": BASE + "assets/logo-icon.png"}}}


def month_pages(months):
    paths = []
    for i, m in enumerate(months):
        L, E = m["live"], m["einzelspiele"]
        q = L["treffer"] / L["wetten"] * 100 if L["wetten"] else 0
        eq = E["treffer"] / E["tipps"] * 100 if E["tipps"] else 0
        G = L.get("gewinn", round(L["rendite"] * L["wetten"]) / 100)
        name = mname(m["monat"])
        path = f"monatsbericht-{m['monat']}.html"
        rr = m.get("rueckrechnung")
        star = "*" if rr else ""
        title = f"Monatsbericht {name}: Live-Wetten und Einzelspiele — Sportwetten Radar"
        desc = (f"Ergebnisse {name}: {L['wetten']} Live-Wetten, Trefferquote {de(q)} %, Rendite {signed(L['rendite'])} %, "
                f"längste Verlustserie {L['verlustserie']}. Einzelspiele: {E['treffer']} von {E['tipps']} getroffen.")
        nachbarn = []
        if i > 0:
            nachbarn.append(f'<a href="monatsbericht-{months[i-1]["monat"]}.html">← {mname(months[i-1]["monat"])}</a>')
        nachbarn.append('<a href="monatsberichte.html">Alle Monatsberichte</a>')
        if i < len(months) - 1:
            nachbarn.append(f'<a href="monatsbericht-{months[i+1]["monat"]}.html">{mname(months[i+1]["monat"])} →</a>')
        inner = f"""
  <p>Am 1. jedes Monats veröffentlichen wir den Monatsbericht für den Vormonat. Hier stehen alle Zahlen für
  {name} — auch die unangenehmen. Nichts wird im Nachhinein aussortiert.</p>

  <h2><span class="num">01</span>Live-Wetten{star}</h2>
  <table class="kv">
    <tr><th>Live-Wetten</th><td>{L['wetten']}</td></tr>
    <tr><th>Treffer</th><td>{L['treffer']} ({de(q)} %)</td></tr>
    <tr><th>Rendite</th><td>{signed(L['rendite'])} %</td></tr>
    <tr><th>Gewinn bzw. Verlust</th><td>{signed(G)} Einsätze</td></tr>
    <tr><th>Längste Verlustserie</th><td>{L['verlustserie']} in Folge</td></tr>
    <tr><th>Größter Rückgang</th><td>{signed(L['rueckgang'])} Einsätze</td></tr>
    <tr><th>Bester Tag</th><td>{signed(L['besterTag'])} Einsätze</td></tr>
    <tr><th>Schlechtester Tag</th><td>{signed(L['schlechtesterTag'])} Einsätze</td></tr>
  </table>
  <p>Rendite und Einsätze gelten, wenn jede Live-Wette mit demselben Einsatz gespielt worden wäre
  (1 Einsatz = dein Grundeinsatz pro Wette). Wie wir rechnen, erklären wir unter
  <a href="rendite-erklaert.html">Rendite erklärt</a>.</p>
  {'<p class="wissen-note">* Rückrechnung mit den aktuellen Einstellungen.</p>' if rr else ''}

  <h2><span class="num">02</span>Einzelspiele zum Kombinieren</h2>
  <table class="kv">
    <tr><th>Tipps</th><td>{E['tipps']}</td></tr>
    <tr><th>Treffer</th><td>{E['treffer']} ({de(eq)} %)</td></tr>
  </table>
  <p>Für Einzelspiele zeigen wir nur die Trefferquote. Da jeder seinen Wettschein selbst zusammenstellt,
  gibt es keine einheitliche Quote, auf die sich eine Rendite seriös rechnen ließe.</p>

  <h2><span class="num">03</span>Einordnung</h2>
  <p>Ein einzelner Monat sagt wenig. Gute und schwache Monate wechseln sich ab, und auch bei hoher
  Trefferquote sind mehrere Fehlschläge in Folge normal (siehe <a href="verlustserien.html">Verlustserien</a>).
  Den Verlauf aller Monate und Wochen findest du im <a href="index.html#trackrecord">Trackrecord</a>.</p>

  <p class="wissen-pager">{' · '.join(nachbarn)}</p>
"""
        y, mo = map(int, m["monat"].split("-"))
        pub = (datetime.date(y + (mo == 12), mo % 12 + 1, 1)).isoformat()
        paths.append((page(path, title, desc, "Monatsbericht", name, inner, article_ld(title, desc, path, pub)), pub))
    # Übersicht
    rows = "\n".join(
        f'    <tr><th><a href="monatsbericht-{m["monat"]}.html">{mname(m["monat"])}</a></th>'
        f'<td>{m["live"]["wetten"]} Live-Wetten · {signed(m["live"]["rendite"])} %</td></tr>'
        for m in reversed(months))
    inner = f"""
  <p>Jeden Monat veröffentlichen wir am 1. die Ergebnisse des Vormonats. Alle Berichte bleiben dauerhaft
  einsehbar — die starken wie die schwachen.</p>
  <table class="kv">
{rows}
  </table>
"""
    t = "Alle Monatsberichte — Sportwetten Radar"
    d = "Alle Monatsberichte von Sportwetten Radar: Live-Wetten mit Trefferquote, Rendite und Verlustserien, Einzelspiele mit Trefferquote."
    paths.append((page("monatsberichte.html", t, d, "Trackrecord", "Alle Monatsberichte", inner), None))
    return paths


WISSEN = [
    ("live-wetten-ueber-unter.html",
     "Live-Wetten auf Über/Unter Tore einfach erklärt — Sportwetten Radar",
     "Was ist eine Über/Unter-Wette, wie funktioniert sie live während des Spiels und worauf kommt es bei der Quote an? Die Grundlagen verständlich erklärt.",
     "Wissen", "Live-Wetten auf Über/Unter Tore",
     """
  <p>Über/Unter gehört zu den bekanntesten Wettarten im Fußball. Du wettest nicht darauf, wer gewinnt,
  sondern darauf, wie viele Tore insgesamt fallen. Das macht die Wette unabhängig davon, welches Team du
  stärker findest.</p>

  <h2><span class="num">01</span>Wie funktioniert Über/Unter?</h2>
  <p>Der Buchmacher setzt eine Grenze, meist mit einer halben Zahl, damit es kein Unentschieden gibt.
  Bei „Über 2,5 Tore“ gewinnst du, wenn mindestens drei Tore fallen. Bei „Unter 2,5 Tore“ gewinnst du,
  wenn höchstens zwei Tore fallen. Gezählt werden in der Regel die Tore beider Mannschaften in der regulären
  Spielzeit inklusive Nachspielzeit, ohne Verlängerung und Elfmeterschießen.</p>

  <h2><span class="num">02</span>Was ist anders bei Live-Wetten?</h2>
  <p>Vor dem Anpfiff steht die Quote fest. Während des Spiels ändert sie sich laufend: mit dem Spielstand,
  der verbleibenden Zeit und dem Spielverlauf. Fällt lange kein Tor, wird „Über“ teurer zu treffen und
  die Quote steigt. Nach einem Tor, einer Roten Karte oder während eines Videobeweises setzen Buchmacher
  den Markt für einige Minuten aus. In dieser Zeit gibt es gar keine Quote.</p>
  <p>Die Live-Quote beruht vor allem auf Spielstand und Spielzeit. Was auf dem Platz passiert, also
  Druckphasen, Torchancen und Abschlüsse, fließt nicht immer sofort in die Quote ein. Genau dort setzt eine
  datenbasierte Analyse an: Sie vergleicht den Spielverlauf mit der aktuellen Markteinschätzung.</p>

  <h2><span class="num">03</span>Quote und Wahrscheinlichkeit</h2>
  <p>Jede Quote enthält eine Wahrscheinlichkeit: 1 geteilt durch die Quote. Eine Quote von 1,60 entspricht
  rund 62,5 %. Wer auf Dauer mit Quote 1,60 nicht verlieren will, muss also mehr als 62,5 % seiner Wetten
  treffen. Eine hohe Trefferquote allein bedeutet deshalb noch keinen Gewinn. Entscheidend ist das
  Verhältnis von Trefferquote und Quote. Mehr dazu unter <a href="rendite-erklaert.html">Rendite erklärt</a>.</p>

  <h2><span class="num">04</span>Was Sportwetten Radar macht</h2>
  <p>Sportwetten Radar wertet laufende Spiele in Echtzeit aus und meldet per Telegram eine Live-Wette,
  sobald die Spieldaten eine Gelegenheit zeigen, die der Wettmarkt noch nicht abbildet. Wir vermitteln
  keine Wetten und nennen keine Einsätze. Die Entscheidung bleibt bei dir. Wie es bisher gelaufen ist,
  steht im <a href="index.html#trackrecord">Trackrecord</a> und in den <a href="monatsberichte.html">Monatsberichten</a>.</p>
"""),
    ("rendite-erklaert.html",
     "Rendite bei Sportwetten erklärt: Trefferquote, Quote und Einsätze — Sportwetten Radar",
     "Wie berechnet man die Rendite bei Sportwetten? Warum reicht die Trefferquote allein nicht? Mit Rechenbeispiel und Erklärung, was „Einsätze“ bedeuten.",
     "Wissen", "Rendite bei Sportwetten erklärt",
     """
  <p>Viele Tippgeber werben mit Trefferquoten. Die Trefferquote allein sagt aber nicht, ob am Ende Geld
  übrig bleibt. Dafür braucht es die Rendite. Hier erklären wir, wie wir sie rechnen.</p>

  <h2><span class="num">01</span>Gleicher Einsatz pro Wette</h2>
  <p>Wir rechnen so, als wäre jede Live-Wette mit demselben Einsatz gespielt worden. Diesen Grundeinsatz
  nennen wir „1 Einsatz“. Ob das bei dir 5 € oder 50 € sind, entscheidest du selbst. Wir nennen keine
  Beträge. So bleiben die Zahlen für jeden vergleichbar.</p>

  <h2><span class="num">02</span>Rechenbeispiel</h2>
  <p>Angenommen, du spielst 10 Wetten mit je 1 Einsatz zu einer Quote von 1,60:</p>
  <ul>
    <li>7 Treffer bringen je 0,60 Einsätze Gewinn: zusammen +4,2 Einsätze.</li>
    <li>3 Fehlschläge kosten je 1 Einsatz: zusammen −3,0 Einsätze.</li>
    <li>Ergebnis: +1,2 Einsätze bei 10 eingesetzten Einsätzen, also eine Rendite von +12 %.</li>
  </ul>
  <p>Mit nur 6 Treffern sähe es anders aus: 6 × 0,60 = +3,6 Einsätze, 4 Fehlschläge = −4,0 Einsätze,
  Ergebnis −0,4 Einsätze, also −4 %. Ein Treffer weniger von zehn macht aus einem Plus ein Minus.</p>

  <h2><span class="num">03</span>Die Formel</h2>
  <p>Rendite = (Summe aller Gewinne und Verluste in Einsätzen) ÷ (Anzahl der Wetten) × 100.
  Der Gewinn in Einsätzen ist umgekehrt Rendite × Anzahl der Wetten ÷ 100. Bei 104 Live-Wetten und
  +12,2 % Rendite sind das rund +12,7 Einsätze.</p>

  <h2><span class="num">04</span>Warum die Trefferquote nicht reicht</h2>
  <p>Ab welcher Trefferquote du im Plus bist, hängt von der Quote ab: bei 1,60 ab 62,5 %, bei 1,80
  ab 55,6 %, bei 1,40 erst ab 71,4 %. Wer eine hohe Trefferquote mit niedrigen Quoten erreicht, kann
  trotzdem verlieren. Deshalb zeigen wir für Live-Wetten immer beides: Trefferquote und Rendite.
  Für <a href="index.html#produkt">Einzelspiele zum Kombinieren</a> zeigen wir nur die Trefferquote, weil
  jeder seinen Wettschein selbst zusammenstellt und es keine einheitliche Quote gibt.</p>

  <h2><span class="num">05</span>Was die Rendite nicht ist</h2>
  <p>Die Rendite beschreibt die Vergangenheit, nicht die Zukunft. Sie gilt nur, wenn wirklich jede Live-Wette
  mit gleichem Einsatz mitgespielt wurde. Deine Quote beim Buchmacher kann leicht von der Quote zum
  Zeitpunkt unserer Analyse abweichen. Und auch ein starker Zeitraum schützt nicht vor schwachen Wochen,
  siehe <a href="verlustserien.html">Verlustserien</a>.</p>
"""),
    ("verlustserien.html",
     "Verlustserien bei Sportwetten: Warum sie normal sind — Sportwetten Radar",
     "Wie wahrscheinlich sind mehrere Fehlschläge in Folge, selbst bei hoher Trefferquote? Verlustserien mit Zahlen erklärt, plus warum ein fester Einsatz wichtig ist.",
     "Wissen", "Verlustserien: warum sie dazugehören",
     """
  <p>Auch bei einer hohen Trefferquote gehen Wetten verloren, und manchmal mehrere direkt hintereinander.
  Das ist kein Zeichen, dass etwas nicht stimmt, sondern Statistik. Wer das vorher weiß, trifft bessere
  Entscheidungen.</p>

  <h2><span class="num">01</span>Wie oft kommt das vor?</h2>
  <p>Angenommen, 70 % aller Wetten werden getroffen. Dann geht jede einzelne Wette mit 30 % verloren.
  Über viele Wetten hinweg sind Serien trotzdem praktisch sicher. Gerechnet für 100 Wetten:</p>
  <table class="kv">
    <tr><th>Mindestens 3 Fehlschläge in Folge</th><td>ca. 86 %</td></tr>
    <tr><th>Mindestens 4 Fehlschläge in Folge</th><td>ca. 43 %</td></tr>
    <tr><th>Mindestens 5 Fehlschläge in Folge</th><td>ca. 15 %</td></tr>
    <tr><th>Mindestens 6 Fehlschläge in Folge</th><td>ca. 5 %</td></tr>
  </table>
  <p>Bei 400 Wetten, also etwa einem halben Jahr, liegt die Wahrscheinlichkeit für eine Serie von
  mindestens 5 Fehlschlägen schon bei rund 50 %. Die Rechnung geht davon aus, dass die Wetten
  voneinander unabhängig sind.</p>

  <h2><span class="num">02</span>Warum wir sie offen zeigen</h2>
  <p>In jedem <a href="monatsberichte.html">Monatsbericht</a> stehen die längste Verlustserie und der größte
  Rückgang. Wer nur Gewinne zeigt, verschweigt die Hälfte. Wer vorher weiß, wie tief es zwischendurch
  gehen kann, gerät nicht in Panik, wenn es passiert.</p>

  <h2><span class="num">03</span>Fester Einsatz statt Verdoppeln</h2>
  <p>Nach einer Serie ist die Versuchung groß, den Einsatz zu erhöhen, um Verluste „zurückzuholen“.
  Genau das macht aus einer normalen Serie einen großen Verlust. Unsere Zahlen gelten für einen festen
  Einsatz pro Wette. Setze nur, was du bereit bist zu verlieren, und erhöhe den Einsatz nicht nach
  Verlusten.</p>

  <h2><span class="num">04</span>Wenn es sich nicht mehr gut anfühlt</h2>
  <p>Wenn du merkst, dass du Verlusten hinterherjagst oder mehr setzt als geplant, mach eine Pause.
  Beratung gibt es kostenlos und anonym beim Beratungstelefon Glücksspielsucht unter
  <a href="tel:08001372700">0800 1 37 27 00</a> und auf <a href="https://www.check-dein-spiel.de" target="_blank" rel="noopener">check-dein-spiel.de</a>.
  Mehr im <a href="risikohinweis.html">Risikohinweis</a>.</p>
"""),
]


def wissen_pages(today):
    out = []
    for path, title, desc, eb, h1, inner in WISSEN:
        out.append((page(path, title, desc, eb, h1, inner, article_ld(title, desc, path, WISSEN_DATUM)), WISSEN_DATUM))
    return out


def sitemap(extra):
    sm = os.path.join(REPO, "sitemap.xml")
    s = open(sm, encoding="utf-8").read()
    for path, date in extra:
        loc = BASE + path
        line = f"  <url><loc>{loc}</loc><lastmod>{date or '2026-10-20'}</lastmod></url>\n"
        if loc + "<" in s:
            s = re.sub(r"  <url><loc>" + re.escape(loc) + r"</loc>.*?</url>\n", line, s)
        else:
            s = s.replace("</urlset>", line + "</urlset>")
    open(sm, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    months = load_months()
    made = month_pages(months) + wissen_pages(today)
    sitemap(made)
    print("\n".join(p for p, _ in made))
