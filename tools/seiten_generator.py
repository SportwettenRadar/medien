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
WISSEN_DATUM = "2026-11-09"  # bei inhaltlicher Änderung der Wissen-Seiten anpassen
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
<script src="menu.js?v=3"></script>
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


FUSSNOTE = "* 01.09.–10.10.: Testphase, mit den Regeln vom 11.10.2026 berechnet."


def tr_block(monat=None, fallback="", liste=False):
    """Gleiche Darstellung wie auf der Startseite (Kennzahlen, Linie, Monatstabelle), gerendert von trackrecord.js."""
    idx = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
    v1 = re.search(r"trackrecord-daten\.js\?v=([0-9a-z]+)", idx)
    v2 = re.search(r"trackrecord\.js\?v=([0-9a-z]+)", idx)
    attr = f' data-tr-monat="{monat}"' if monat else (" data-tr-liste" if liste else "")
    return f"""<div class="trk" data-tr{attr}>
    <div data-tr-body><noscript>{fallback}</noscript></div>
  </div>
  <script src="trackrecord-daten.js?v={v1.group(1) if v1 else '1'}"></script>
  <script src="trackrecord.js?v={v2.group(1) if v2 else '1'}"></script>"""


def month_pages(months):
    paths = []
    for i, m in enumerate(months):
        L, E = m["live"], m["einzelspiele"]
        q = L["treffer"] / L["wetten"] * 100 if L["wetten"] else 0
        eq = E["treffer"] / E["tipps"] * 100 if E["tipps"] else 0
        qu = L.get("quote")
        name = mname(m["monat"])
        path = f"monatsbericht-{m['monat']}.html"
        title = f"Monatsbericht {name}: Live-Wetten und Einzelspiele — Sportwetten Radar"
        desc = (f"Ergebnisse {name}: {L['wetten']} Live-Wetten, {L['treffer']} Treffer ({de(q)} %)"
                + (f", Ø-Quote {de(qu, 2)}" if qu else "") +
                f", längste Verlustserie {L['verlustserie']}. Einzelspiele: {E['treffer']} von {E['tipps']} getroffen.")
        nachbarn = []
        if i > 0:
            nachbarn.append(f'<a href="monatsbericht-{months[i-1]["monat"]}.html">← {mname(months[i-1]["monat"])}</a>')
        nachbarn.append('<a href="monatsberichte.html">Alle Monatsberichte</a>')
        if i < len(months) - 1:
            nachbarn.append(f'<a href="monatsbericht-{months[i+1]["monat"]}.html">{mname(months[i+1]["monat"])} →</a>')
        inner = f"""
  <p>Am 1. jedes Monats veröffentlichen wir den Monatsbericht für den Vormonat. Hier stehen alle Zahlen für
  {name} — auch die unangenehmen. Nichts wird im Nachhinein aussortiert.</p>

  {tr_block(m["monat"])}

  <h2><span class="num">01</span>Live-Wetten im Detail</h2>
  <table class="kv">
    <tr><th>Wetten</th><td>{L['wetten']}</td></tr>
    <tr><th>Treffer</th><td>{L['treffer']} ({de(q)} %)</td></tr>
{('    <tr><th>Ø-Quote</th><td>' + de(qu, 2) + '</td></tr>') if qu else ''}
    <tr><th>Längste Verlustserie</th><td>{L['verlustserie']} in Folge</td></tr>
  </table>
  <p>Ø-Quote ist der Durchschnitt der Quoten aller gesetzten Live-Wetten des Monats. Einsätze und Rendite zeigen wir auf
  dieser Webseite nicht. Wir weisen sie je Kalenderjahr in unseren Telegram-Kanälen aus, sobald 100 Live-Wetten vorliegen, nicht je Monat: Ein einzelner Monat ist zu stark vom Zufall abhängig.
  Verlustserien gehören dazu. Wie wir rechnen, erklären wir unter
  <a href="rendite-erklaert.html">Rendite erklärt</a>.</p>

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
  Den Verlauf aller Monate und die Jahreskurve der Trefferquote findest du im <a href="index.html#trackrecord">Trackrecord</a>.</p>

  <p class="wissen-pager">{' · '.join(nachbarn)}</p>
"""
        y, mo = map(int, m["monat"].split("-"))
        pub = (datetime.date(y + (mo == 12), mo % 12 + 1, 1)).isoformat()
        paths.append((page(path, title, desc, "Monatsbericht", name, inner, article_ld(title, desc, path, pub)), pub))
    # Übersicht
    rows = "\n".join(
        f'    <tr><td><a href="monatsbericht-{m["monat"]}.html">{mname(m["monat"])}{"*" if m.get("rueckrechnung") else ""}</a></td>'
        f'<td>{m["live"]["wetten"]}</td><td>{m["live"]["treffer"]}</td>'
        + (f'<td>{de(m["live"]["quote"], 2)}</td>' if m["live"].get("quote") else '<td>–</td>')
        + (f'<td>{m["live"]["verlustserie"]}</td>' if "verlustserie" in m["live"] else '<td>–</td>') + '</tr>'
        for m in reversed(months))
    fn = f"<p>{FUSSNOTE}</p>" if any(m.get("rueckrechnung") for m in months) else ""
    fallback = ('<table class="kv"><tr><th>Monat</th><th>Wetten</th><th>Treffer</th><th>Ø-Quote</th><th>Verlustserie</th></tr>' + rows + "</table>" + fn)
    inner = f"""
  <p>Jeden Monat veröffentlichen wir am 1. die Ergebnisse des Vormonats. Alle Berichte bleiben dauerhaft
  einsehbar — die starken wie die schwachen.</p>
  {tr_block(None, fallback, liste=True)}
"""
    t = "Alle Monatsberichte — Sportwetten Radar"
    d = "Alle Monatsberichte von Sportwetten Radar: Live-Wetten mit Trefferquote, Ø-Quote und Verlustserien, Einzelspiele mit Trefferquote."
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
  Verhältnis von Trefferquote und Quote. Mehr dazu unter <a href="rendite-erklaert.html">Rendite erklärt</a> und
  <a href="quote-1-70-bedeutung.html">Was bedeutet Quote 1,70?</a></p>

  <h2><span class="num">04</span>Was Sportwetten Radar macht</h2>
  <p>Sportwetten Radar wertet laufende Spiele in Echtzeit aus und meldet per Telegram eine Live-Wette,
  sobald die Spieldaten eine Gelegenheit zeigen, die der Wettmarkt noch nicht abbildet. Wir vermitteln
  keine Wetten und nennen keine Einsätze. Die Entscheidung bleibt bei dir. Wie es bisher gelaufen ist,
  steht im <a href="index.html#trackrecord">Trackrecord</a> und in den <a href="monatsberichte.html">Monatsberichten</a>.</p>
""", "2026-10-27"),
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
  Der Gewinn in Einsätzen ist umgekehrt Rendite × Anzahl der Wetten ÷ 100. Bei 200 Live-Wetten und
  +5 % Rendite sind das +10 Einsätze.</p>

  <h2><span class="num">04</span>Warum die Trefferquote nicht reicht</h2>
  <p>Ab welcher Trefferquote du im Plus bist, hängt von der Quote ab: bei 1,60 ab 62,5 %, bei 1,80
  ab 55,6 %, bei 1,40 erst ab 71,4 %. Wer eine hohe Trefferquote mit niedrigen Quoten erreicht, kann
  trotzdem verlieren (wie eine Quote in eine Wahrscheinlichkeit übersetzt wird, steht unter
  <a href="quote-1-70-bedeutung.html">Was bedeutet Quote 1,70?</a>). Deshalb zeigen wir für Live-Wetten neben der Trefferquote immer die Durchschnittsquote (Ø-Quote). Mit beiden lässt sich die Trefferquote selbst einordnen: Die Gewinnschwelle liegt bei 1 ÷ Quote. Einsätze und Rendite weisen wir je Kalenderjahr in unseren Telegram-Kanälen aus, sobald 100 Live-Wetten vorliegen. Auf dieser Webseite zeigen wir sie nicht, und für Tage, Wochen und Monate gar nicht, weil kurze Zeiträume stark vom Zufall abhängen.
  Für <a href="index.html#produkt">Einzelspiele zum Kombinieren</a> zeigen wir nur die Trefferquote, weil
  jeder seinen Wettschein selbst zusammenstellt und es keine einheitliche Quote gibt.</p>

  <h2><span class="num">05</span>Was die Rendite nicht ist</h2>
  <p>Die Rendite beschreibt die Vergangenheit, nicht die Zukunft. Sie gilt nur, wenn wirklich jede Live-Wette
  mit gleichem Einsatz mitgespielt wurde. Deine Quote beim Buchmacher kann leicht von der Quote zum
  Zeitpunkt unserer Analyse abweichen. Und auch ein starker Zeitraum schützt nicht vor schwachen Wochen,
  siehe <a href="verlustserien.html">Verlustserien</a>.</p>
""", "2026-10-27"),
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
  <p>In jedem <a href="monatsberichte.html">Monatsbericht</a> steht die längste Verlustserie, und die Jahreskurve
  der Trefferquote im <a href="index.html#trackrecord">Trackrecord</a> zeigt, wie sie zwischendurch schwankt. Wer nur Gewinne zeigt, verschweigt die Hälfte. Wer vorher weiß, wie tief es zwischendurch
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
    ("sportwetten-telegram.html",
     "Sportwetten auf Telegram: Live-Wetten-Analyse per Bot — Sportwetten Radar",
     "Wie funktionieren Sportwetten-Tipps auf Telegram? Bot, Kanal und Gruppe im Vergleich, worauf du achten solltest und wie Sportwetten Radar Live-Wetten per Telegram meldet.",
     "Telegram", "Sportwetten auf Telegram",
     """
  <p>Telegram ist für Sportwetten-Analysen besonders verbreitet. Der Grund ist einfach: Live-Wetten leben
  von Sekunden. Eine Meldung muss sofort auf dem Handy ankommen, ohne dass ein Algorithmus sie
  verzögert oder ausblendet. Telegram stellt Nachrichten aus Kanälen und von Bots direkt zu.</p>

  <h2><span class="num">01</span>Kanal, Gruppe oder Bot – der Unterschied</h2>
  <ul>
    <li><strong>Kanal:</strong> Nur der Betreiber schreibt, alle anderen lesen. Gut für Meldungen und Ergebnisse.</li>
    <li><strong>Gruppe:</strong> Alle Mitglieder können schreiben. Lebendig, aber oft unübersichtlich – und ein
    beliebter Ort für Werbung und unseriöse Angebote.</li>
    <li><strong>Bot:</strong> Ein automatisches Programm, mit dem du persönlich chattest. Er kann dich zum Beispiel
    für ein Angebot freischalten, dir dein Abo anzeigen oder deine Kündigung entgegennehmen.</li>
  </ul>

  <h2><span class="num">02</span>So funktioniert Sportwetten Radar auf Telegram</h2>
  <ul>
    <li><strong>Der Bot</strong> (<a href="https://t.me/KILivewetten_bot" target="_blank" rel="noopener">@KILivewetten_bot</a>)
    ist dein Zugang: Warteliste, Buchung, Abo-Übersicht und Kündigung laufen über ihn.</li>
    <li><strong>Der Mitgliederkanal</strong> meldet Live-Wetten in Echtzeit, sobald die Analyse eines laufenden
    Spiels eine Gelegenheit zeigt, dazu bis zu 5 Einzelspiele pro Tag.</li>
    <li><strong>Der öffentliche Ergebnis-Kanal</strong>
    (<a href="https://t.me/sportwettenradar" target="_blank" rel="noopener">t.me/sportwettenradar</a>) zeigt kostenlos
    jede Live-Wette nach ihrer Auswertung, die Einzelspiele des Tages sowie Tages-, Wochen- und Monatsbilanzen.
    So kannst du prüfen, wie es wirklich läuft, bevor du dich entscheidest.</li>
  </ul>

  <h2><span class="num">03</span>Worauf du bei Telegram-Tipps achten solltest</h2>
  <p>Auf Telegram gibt es viele Wett-Kanäle – leider auch viele, die mit „sicheren Tipps“ oder angeblich
  manipulierten Spielen werben. Seriöse Anbieter nennen einen Betreiber mit Impressum, zeigen alle Ergebnisse
  inklusive Verlusten und versprechen keine Gewinne. Eine ausführliche Checkliste findest du unter
  <a href="seriose-tippgeber-erkennen.html">Seriöse Tippgeber erkennen</a>.</p>

  <h2><span class="num">04</span>Unsere Zahlen</h2>
  <p>Alle Ergebnisse stehen im <a href="index.html#trackrecord">Trackrecord</a> und in den
  <a href="monatsberichte.html">Monatsberichten</a>, auch die schwachen Monate. Wie wir Rendite rechnen, erklären wir unter
  <a href="rendite-erklaert.html">Rendite erklärt</a>.</p>
""", "2026-10-22"),
    ("seriose-tippgeber-erkennen.html",
     "Telegram-Tippgruppen: So erkennst du seriöse Tippgeber — Sportwetten Radar",
     "Sind Wett-Tipps auf Telegram seriös? Checkliste mit 8 Merkmalen und den typischen Warnzeichen unseriöser Tippgruppen – von Gewinngarantien bis Krypto-Zahlung.",
     "Wissen", "Seriöse Tippgeber erkennen",
     """
  <p>Tippgruppen und Wett-Kanäle gibt es auf Telegram zu Tausenden. Einige arbeiten ordentlich, viele nicht.
  Verbraucherschützer und Medien berichten immer wieder über Abzocke mit „sicheren Tipps“. Mit diesen
  Merkmalen trennst du seriöse von unseriösen Angeboten.</p>

  <h2><span class="num">01</span>8 Merkmale seriöser Tippgeber</h2>
  <ul>
    <li><strong>Erkennbarer Betreiber:</strong> Impressum mit ladungsfähiger Anschrift, Datenschutzerklärung und AGB.</li>
    <li><strong>Alle Ergebnisse, dauerhaft:</strong> Gewinne und Verluste bleiben sichtbar. Nichts wird gelöscht oder im Nachhinein geschönt.</li>
    <li><strong>Trefferquote und Quote zusammen:</strong> Eine hohe Trefferquote allein sagt wenig – entscheidend ist das Verhältnis zur Quote. Seriöse Anbieter nennen deshalb auch die Durchschnittsquote und die Rendite über einen längeren Zeitraum (<a href="rendite-erklaert.html">Rendite erklärt</a>).</li>
    <li><strong>Verlustserien werden genannt:</strong> Wer offenlegt, wie tief es zwischendurch ging, ist ehrlich (<a href="verlustserien.html">Verlustserien</a>).</li>
    <li><strong>Keine Gewinngarantie:</strong> Sportwetten sind mit einem Verlustrisiko verbunden. Wer etwas anderes verspricht, lügt.</li>
    <li><strong>Prüfbar vor dem Kauf:</strong> Ergebnisse lassen sich kostenlos verfolgen, bevor Geld fließt.</li>
    <li><strong>Normale Zahlungswege:</strong> Zahlung über bekannte Anbieter mit Beleg, keine Überweisung an Privatpersonen oder in Kryptowährung.</li>
    <li><strong>Einfache Kündigung:</strong> Klare Laufzeiten und ein Kündigungsweg, der ohne Hürden funktioniert.</li>
  </ul>

  <h2><span class="num">02</span>Typische Warnzeichen</h2>
  <ul>
    <li>„100 % sicher“, „Fixed Matches“, „garantierter Gewinn“ oder „Verluste zurückholen“</li>
    <li>Screenshots von Wettscheinen mit hohen Gewinnen, aber keine vollständige Bilanz</li>
    <li>Zeitdruck: „Nur heute“, „Letzte Plätze“, „Jetzt oder nie“</li>
    <li>Zahlung per Krypto, Gutscheinkarte oder an private Konten</li>
    <li>Hauptgeschäft sind Bonuscodes von Wettanbietern statt eigener Analysen</li>
    <li>Kein Impressum, nur ein anonymer Telegram-Name</li>
  </ul>

  <h2><span class="num">03</span>Wie wir es halten</h2>
  <p>Sportwetten Radar nennt einen Betreiber im <a href="impressum.html">Impressum</a>, veröffentlicht jede Live-Wette
  nach ihrer Auswertung kostenlos im <a href="https://t.me/sportwettenradar" target="_blank" rel="noopener">Ergebnis-Kanal</a>
  und zeigt alle Monate im <a href="monatsberichte.html">Trackrecord</a>. Wir vermitteln keine Wetten, geben keine
  Gewinngarantie und arbeiten nicht mit Bonuscodes von Wettanbietern. Bezahlt wird über Stripe mit Beleg.</p>
""", "2026-10-22"),
    ("live-wetten-analyse.html",
     "Live-Wetten-Analyse im Fußball: Was Spieldaten verraten — Sportwetten Radar",
     "Wie funktioniert eine Live-Wetten-Analyse im Fußball? Welche Spieldaten zählen, warum die Quote dem Spielverlauf hinterherhinken kann und wo die Grenzen liegen.",
     "Wissen", "Live-Wetten-Analyse im Fußball",
     """
  <p>Bei Wetten vor dem Anpfiff zählt vor allem, was man über beide Mannschaften weiß. Bei Live-Wetten kommt
  etwas Entscheidendes dazu: das, was gerade auf dem Platz passiert. Eine Live-Analyse versucht, aus den
  laufenden Spieldaten zu erkennen, ob die aktuelle Quote das Spielgeschehen richtig abbildet.</p>

  <h2><span class="num">01</span>Welche Daten zählen</h2>
  <ul>
    <li><strong>Spielstand und Spielminute:</strong> Die Grundlage jeder Live-Quote.</li>
    <li><strong>Torschüsse und Schüsse aufs Tor:</strong> Zeigen, wie viel tatsächlich passiert.</li>
    <li><strong>Gefährliche Angriffe und Ecken:</strong> Geben Hinweise auf Druckphasen.</li>
    <li><strong>Quotenverlauf:</strong> Zeigt, wie der Wettmarkt das Spiel gerade einschätzt.</li>
    <li><strong>Ballbesitz:</strong> Wird oft überschätzt. Viel Ballbesitz ohne Abschlüsse sagt wenig.</li>
  </ul>

  <h2><span class="num">02</span>Warum Markt und Spielverlauf auseinanderlaufen können</h2>
  <p>Live-Quoten reagieren stark auf Spielstand und verbleibende Zeit. Ob eine Mannschaft gerade Druck macht
  und Chancen herausspielt, fließt nicht immer sofort ein. In solchen Momenten kann die Quote vom tatsächlichen
  Spielgeschehen abweichen. Eine datenbasierte Analyse sucht genau diese Momente.</p>

  <h2><span class="num">03</span>Die Grenzen</h2>
  <ul>
    <li>Statistik beschreibt Wahrscheinlichkeiten, keine Gewissheiten. Auch eine gute Analyse liegt oft daneben.</li>
    <li>Live-Daten kommen mit kurzer Verzögerung, und Buchmacher setzen Märkte nach Toren oder Karten für einige Minuten aus.</li>
    <li>Deine Quote beim Buchmacher kann leicht von der Quote zum Zeitpunkt der Analyse abweichen.</li>
    <li>Ob sich eine Methode lohnt, zeigt nur eine lange, vollständige Bilanz – nicht ein einzelner Tag.</li>
  </ul>

  <h2><span class="num">04</span>Wie Sportwetten Radar arbeitet</h2>
  <p>Sportwetten Radar wertet laufende Spiele in Echtzeit aus und meldet per <a href="sportwetten-telegram.html">Telegram</a>
  eine Live-Wette, wenn die Daten eine auffällige Abweichung zeigen. Die genaue Methodik ist unser Betriebsgeheimnis,
  die Ergebnisse sind es nicht: Sie stehen vollständig im <a href="index.html#trackrecord">Trackrecord</a> und im
  kostenlosen <a href="https://t.me/sportwettenradar" target="_blank" rel="noopener">Ergebnis-Kanal</a>.</p>
""", "2026-10-22"),
    ("quote-1-70-bedeutung.html",
     "Was bedeutet Quote 1,70? Wahrscheinlichkeit und Gewinn erklärt — Sportwetten Radar",
     "Was sagt eine Quote von 1,70 über die Wahrscheinlichkeit aus? Ab welcher Trefferquote lohnt sie sich? Mit Rechenbeispiel, Tabelle und Erklärung der Buchmacher-Marge.",
     "Wissen", "Was bedeutet Quote 1,70?",
     """
  <p>Eine Quote von 1,70 sieht harmlos aus. Dahinter steckt aber eine klare Aussage: Der Markt hält das
  Ereignis für ziemlich wahrscheinlich, zahlt aber nur einen kleinen Aufschlag. Hier erklären wir, was die
  Zahl bedeutet und wie du sie selbst nachrechnest.</p>

  <h2><span class="num">01</span>Was du bei Quote 1,70 bekommst</h2>
  <p>Die Quote ist der Faktor, mit dem dein Einsatz multipliziert wird, wenn die Wette getroffen wird.
  Bei 1 Einsatz und Quote 1,70 bekommst du 1,70 Einsätze zurück. Davon ist 1 Einsatz dein eigener, der
  Gewinn beträgt also 0,70 Einsätze. Geht die Wette verloren, ist der ganze Einsatz weg. Ein Treffer
  gleicht deshalb nur 0,70 eines Fehlschlags aus.</p>

  <h2><span class="num">02</span>Welche Wahrscheinlichkeit steckt drin?</h2>
  <p>Die in der Quote enthaltene Wahrscheinlichkeit ist 1 geteilt durch die Quote:
  1 ÷ 1,70 = 0,588, also rund 58,8 %. Das ist zugleich die Trefferquote, die du auf Dauer mindestens
  brauchst, um mit dieser Quote nicht zu verlieren.</p>
  <table class="kv">
    <tr><th>Quote 1,40</th><td>71,4 %</td></tr>
    <tr><th>Quote 1,55</th><td>64,5 %</td></tr>
    <tr><th>Quote 1,70</th><td>58,8 %</td></tr>
    <tr><th>Quote 2,00</th><td>50,0 %</td></tr>
    <tr><th>Quote 2,50</th><td>40,0 %</td></tr>
  </table>
  <p class="wissen-note">Die Tabelle zeigt die Mindest-Trefferquote ohne Gewinn und Verlust, gerechnet als 1 ÷ Quote.</p>

  <h2><span class="num">03</span>Rechenbeispiel: 10 Wetten zu Quote 1,70</h2>
  <ul>
    <li>6 Treffer bringen je 0,70 Einsätze Gewinn: zusammen +4,2 Einsätze. 4 Fehlschläge kosten −4,0 Einsätze.
    Ergebnis: +0,2 Einsätze, also eine Rendite von +2 %.</li>
    <li>Mit 5 Treffern: +3,5 Einsätze minus 5,0 Einsätze, Ergebnis −1,5 Einsätze, also −15 %.</li>
  </ul>
  <p>Schon 6 statt 5 Treffer von zehn entscheidet zwischen einem kleinen Plus und einem deutlichen Minus.
  Bei so knapper Marge zählt jede einzelne Wette. Wie wir daraus die Rendite rechnen, steht unter
  <a href="rendite-erklaert.html">Rendite erklärt</a>.</p>

  <h2><span class="num">04</span>Die Quote ist nicht die ganze Wahrheit</h2>
  <p>Buchmacher verdienen an der Marge: Die Wahrscheinlichkeiten aller möglichen Ausgänge ergeben zusammen mehr als
  100 %. Ein Beispiel mit angenommenen Quoten: Über 2,5 Tore zu 1,70 und Unter 2,5 Tore zu 2,10.
  Dann ergibt 58,8 % + 47,6 % zusammen 106,4 %. Die Marge liegt hier bei rund 6,4 %. Die „faire“ Wahrscheinlichkeit
  für Über liegt damit eher bei rund 55 %, nicht bei 58,8 %. Du brauchst also eine bessere Einschätzung als
  die des Marktes, nicht nur eine gute.</p>

  <h2><span class="num">05</span>Was das für Live-Wetten bedeutet</h2>
  <p>Live ändert sich die Quote mit Spielstand und Spielzeit. Eine Quote von 1,70 kann in Minute 60 etwas ganz anderes bedeuten
  als vor dem Anpfiff. Wie das bei Über/Unter aussieht, steht unter
  <a href="live-wetten-ueber-unter.html">Live-Wetten auf Über/Unter Tore</a>. Und auch bei einer Trefferquote von rund 59 %
  gehen vier von zehn Wetten verloren, oft mehrere hintereinander (<a href="verlustserien.html">Verlustserien</a>).
  Setze deshalb nie mehr, als du bereit bist zu verlieren.</p>

  <h2><span class="num">06</span>Das Video dazu</h2>
  <div class="yt-embed" data-yt="75tMIKqfsJc">
    <button type="button" class="yt-load" aria-label="Video von YouTube laden">▶ Video laden: Quote richtig lesen</button>
    <p class="wissen-note">Mit dem Klick lädst du das Video von YouTube (Google). Dabei werden Daten an YouTube übertragen.
    Mehr dazu in der <a href="datenschutz.html#youtube">Datenschutzerklärung</a>.</p>
  </div>
  <style>
    .yt-embed { margin-top: 16px; }
    .yt-embed .yt-load { display: block; width: 100%; aspect-ratio: 16 / 9; background: #0a1620; color: #fff; border: 1px solid var(--line); border-radius: 12px; font: inherit; font-size: 16px; cursor: pointer; }
    .yt-embed .yt-load:hover, .yt-embed .yt-load:focus-visible { border-color: var(--accent); }
    .yt-embed iframe { display: block; width: 100%; aspect-ratio: 16 / 9; border: 0; border-radius: 12px; }
  </style>
  <script>
  (function () {
    document.querySelectorAll(".yt-embed").forEach(function (box) {
      var btn = box.querySelector(".yt-load");
      if (!btn) return;
      btn.addEventListener("click", function () {
        var f = document.createElement("iframe");
        f.src = "https://www.youtube-nocookie.com/embed/" + box.getAttribute("data-yt") + "?autoplay=1&rel=0";
        f.title = "Quote richtig lesen: Was eine Quote von 1,60 wirklich bedeutet";
        f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
        f.allowFullscreen = true;
        btn.replaceWith(f);
      });
    });
  })();
  </script>
""", "2026-10-27"),
    ("ueber-1-5-tore.html",
     "Was ist Über 1,5 Tore? Wette, Quote und Live-Chancen erklärt — Sportwetten Radar",
     "Was bedeutet Über 1,5 Tore, wie wahrscheinlich ist es vor dem Anpfiff und wie ändern sich die Chancen live mit Spielstand und Minute? Mit Rechenbeispiel und Tabelle.",
     "Wissen", "Was ist Über 1,5 Tore?",
     """
  <p>„Über 1,5 Tore“ gehört zu den einfachsten Wetten im Fußball. Die Quote ist meist niedrig, und genau das
  wird oft unterschätzt. Hier erklären wir, was die Wette bedeutet, welche Chance dahintersteckt und warum
  sich der Preis live mit jeder Minute ändert.</p>

  <h2><span class="num">01</span>Was bedeutet Über 1,5 Tore?</h2>
  <p>Du gewinnst, wenn in der regulären Spielzeit mindestens zwei Tore fallen, egal bei welchem Team. Bei
  0:0 oder 1:0 verlierst du, bei 1:1, 2:0 oder 3:2 gewinnst du. „Unter 1,5 Tore“ ist das Gegenstück: höchstens
  ein Tor. Die halbe Zahl sorgt dafür, dass es kein Unentschieden gibt. Die Grundlagen zu Über/Unter stehen unter
  <a href="live-wetten-ueber-unter.html">Live-Wetten auf Über/Unter Tore</a>.</p>

  <h2><span class="num">02</span>Wie wahrscheinlich ist das vor dem Anpfiff?</h2>
  <p>Ein einfaches Rechenmodell dafür ist die Poisson-Verteilung. Angenommen, in einem Spiel fallen im Schnitt
  2,7 Tore pro 90 Minuten. Dann liegt die Chance auf mindestens zwei Tore bei rund 75,1 %. Eine Quote ohne
  Aufschlag wäre damit etwa 1,33 (1 ÷ 0,751). Wie du eine Quote in eine Wahrscheinlichkeit übersetzt, steht unter
  <a href="quote-1-70-bedeutung.html">Was bedeutet Quote 1,70?</a></p>

  <h2><span class="num">03</span>Wie ändert sich die Chance live?</h2>
  <p>Mit jeder Minute ohne Tor bleibt weniger Zeit. Dasselbe Rechenbeispiel (2,7 Tore pro 90 Minuten) für die
  Restzeit, die „faire“ Quote ist wieder 1 ÷ Chance:</p>
  <table class="kv">
    <tr><th>Stand und Minute</th><td>Chance auf Über 1,5</td><td>faire Quote</td></tr>
    <tr><th>0:0, Minute 30</th><td>53,7 %</td><td>1,86</td></tr>
    <tr><th>0:0, Minute 60</th><td>22,8 %</td><td>4,39</td></tr>
    <tr><th>0:0, Minute 80</th><td>3,7 %</td><td>27,0</td></tr>
    <tr><th>1:0, Minute 30</th><td>83,5 %</td><td>1,20</td></tr>
    <tr><th>1:0, Minute 60</th><td>59,3 %</td><td>1,69</td></tr>
    <tr><th>1:0, Minute 80</th><td>25,9 %</td><td>3,86</td></tr>
  </table>
  <p class="wissen-note">Rechenbeispiel mit konstanter Torrate. Echte Quoten enthalten zusätzlich die Marge des Anbieters.</p>
  <p>Beim Stand 1:0 reicht ein weiteres Tor, bei 0:0 braucht es zwei. Deshalb liegen die Chancen so weit auseinander.
  Eine Wette auf Über 1,5 bei 0:0 in Minute 60 ist nicht „fast dieselbe“ wie vor dem Anpfiff, sie ist etwas ganz anderes.</p>

  <h2><span class="num">04</span>Was das Modell nicht kann</h2>
  <ul>
    <li>Die Torrate ist in Wirklichkeit nicht konstant: Nach Rückständen, Karten oder Wechseln ändert sich das Spiel.</li>
    <li>Jedes Spiel hat eine eigene erwartbare Torzahl. Die 2,7 sind nur ein Beispiel.</li>
    <li>Niedrige Quoten brauchen hohe Trefferquoten: Bei Quote 1,33 musst du auf Dauer mehr als 75 % treffen, um nicht zu verlieren.
    Mehr dazu unter <a href="rendite-erklaert.html">Rendite erklärt</a>.</li>
    <li>Auch eine wahrscheinliche Wette geht manchmal verloren, oft mehrere hintereinander (<a href="verlustserien.html">Verlustserien</a>).</li>
  </ul>

  <h2><span class="num">05</span>Was Sportwetten Radar daraus macht</h2>
  <p>Wir vergleichen den Spielverlauf mit der Einschätzung des Marktes und zeigen, welche Live-Wetten dabei auffallen.
  Alle Ergebnisse stehen im <a href="index.html#trackrecord">Trackrecord</a>, die schwachen eingeschlossen.
  Das Beispiel hier ist ein Rechenbeispiel, keine Empfehlung. Wetten kann Geld kosten. Hilfe bei Spielproblemen:
  <a href="https://www.check-dein-spiel.de" target="_blank" rel="noopener">check-dein-spiel.de</a>.</p>
""", "2026-11-02"),
    ("lohnen-sich-live-wetten.html",
     "Lohnen sich Live-Wetten? Chancen und Risiken ehrlich erklärt — Sportwetten Radar",
     "Lohnen sich Live-Wetten wirklich? Was für Live-Wetten spricht, was dagegen, warum die Marge und der Zufall oft stärker sind als die Trefferquote, und worauf du achten solltest.",
     "Wissen", "Lohnen sich Live-Wetten?",
     """
  <p>Die ehrliche Antwort vorweg: Für die meisten Wettenden lohnen sich Live-Wetten nicht. Das liegt nicht an
  „Live“, sondern an der Marge des Anbieters, an der Ungewissheit und an der Disziplin, die es braucht.
  Hier erklären wir, was für Live-Wetten spricht, was dagegen, und woran du eine ehrliche Bilanz erkennst.</p>

  <h2><span class="num">01</span>Was für Live-Wetten spricht</h2>
  <ul>
    <li>Du siehst das Spiel, bevor du wettest: Tempo, Chancen, Druck. Vor dem Anpfiff gibt es nur Erwartungen.</li>
    <li>Quoten reagieren auf Stand und Spielzeit, nicht immer auf alles, was auf dem Platz passiert. Daten über den
    Spielverlauf können deshalb eine Abweichung zeigen (mehr dazu unter
    <a href="live-wetten-analyse.html">Live-Wetten und Spieldaten</a>).</li>
    <li>Wetten wie <a href="ueber-1-5-tore.html">Über 1,5 Tore</a> lassen sich in der Restzeit genauer einschätzen
    als vor dem Spiel.</li>
  </ul>

  <h2><span class="num">02</span>Was dagegen spricht</h2>
  <ul>
    <li><strong>Marge:</strong> In jeder Quote steckt ein Aufschlag. Zwei Quoten von 1,90 ergeben zusammen 105,3 %.
    Diesen Aufschlag musst du auf Dauer erst einmal ausgleichen, bevor etwas übrig bleibt.</li>
    <li><strong>Tempo:</strong> Live fällt die Entscheidung in Sekunden. Das begünstigt Bauchentscheidungen und
    Nachsetzen nach Verlusten.</li>
    <li><strong>Verzögerung und Sperren:</strong> Nach einem Tor, einer Roten Karte oder einem Videobeweis setzen
    Anbieter den Markt für einige Minuten aus. Deine Quote kann sich zwischen Entscheidung und Abgabe verändern.</li>
    <li><strong>Viele Wetten in kurzer Zeit:</strong> Je mehr du wettest, desto mehr Marge zahlst du, und desto
    größer wird der Einsatz insgesamt.</li>
  </ul>

  <h2><span class="num">03</span>Rechenbeispiel: Wie knapp es ist</h2>
  <p>Angenommen, du spielst 100 Wetten mit gleichem Einsatz zur Quote 1,80. Dann brauchst du auf Dauer eine
  Trefferquote von mehr als 55,6 % (1 ÷ 1,80), um nicht zu verlieren:</p>
  <ul>
    <li>55 Treffer: 55 × 0,80 = +44 Einsätze, 45 Fehlschläge = −45 Einsätze, Ergebnis −1 Einsatz, also −1 %.</li>
    <li>56 Treffer: 56 × 0,80 = +44,8 Einsätze, 44 Fehlschläge = −44 Einsätze, Ergebnis +0,8 Einsätze, also +0,8 %.</li>
  </ul>
  <p>Ein einziger Treffer entscheidet hier zwischen Minus und Plus. Wie das Verhältnis von Quote und Trefferquote
  funktioniert, steht unter <a href="rendite-erklaert.html">Rendite erklärt</a> und
  <a href="quote-1-70-bedeutung.html">Was bedeutet Quote 1,70?</a></p>

  <h2><span class="num">04</span>Der Zufall ist lauter als du denkst</h2>
  <p>Bei 100 Wetten zur Quote 1,80 und einer „wahren“ Trefferquote von 55,6 % schwankt die Zahl der Treffer
  typischerweise um etwa ±5. Jeder Treffer mehr oder weniger verschiebt das Ergebnis um 1,8 Einsätze. Das
  ergibt allein durch Zufall eine Schwankung von rund ±9 Prozentpunkten bei der Rendite. Ein guter oder
  schlechter Monat sagt deshalb wenig aus. Erst eine lange, vollständige Bilanz zeigt, ob eine Methode trägt
  (<a href="verlustserien.html">Verlustserien</a> gehören dazu).</p>

  <h2><span class="num">05</span>Woran du eine ehrliche Bilanz erkennst</h2>
  <ul>
    <li>Alle Wetten sind enthalten, auch die verlorenen. Nichts wird nachträglich gelöscht.</li>
    <li>Die Trefferquote wird zusammen mit der Durchschnittsquote gezeigt, die Rendite über einen langen Zeitraum und nicht für einzelne Tage.</li>
    <li>Der Zeitraum ist klar, und es wird gesagt, welche Zahlen nachträglich nach den Regeln vom 11.10.2026 berechnet wurden.</li>
    <li>Es gibt keine Gewinnversprechen. Mehr dazu unter
    <a href="seriose-tippgeber-erkennen.html">Seriöse Tippgeber erkennen</a>.</li>
  </ul>

  <h2><span class="num">06</span>Unser Ansatz</h2>
  <p>Sportwetten Radar wertet laufende Spiele aus und zeigt, welche Live-Wetten dabei auffallen. Wir vermitteln
  keine Wetten und nennen keine Einsätze. Wie es bisher lief, steht im
  <a href="index.html#trackrecord">Trackrecord</a> und in den <a href="monatsberichte.html">Monatsberichten</a>,
  mit den schwachen Phasen. Das ist kein Versprechen für die Zukunft. Wetten kann Geld kosten. Setze nie mehr, als du
  bereit bist zu verlieren. Hilfe bei Spielproblemen:
  <a href="https://www.check-dein-spiel.de" target="_blank" rel="noopener">check-dein-spiel.de</a>.</p>
""", "2026-11-03"),
]


# Wissen-Übersicht: max. 6 Kategorien (Footer + Menü zeigen nur diese). Neue Wissensseiten NUR hier einsortieren,
# nie als neuen Footer-Eintrag. Reihenfolge je Kategorie = Reihenfolge auf der Seite.
WISSEN_KAT = [
    ("quoten", "Quoten & Rendite", "Wie du eine Quote liest und wie Rendite und Trefferquote zusammenhängen.",
     ["quote-1-70-bedeutung.html", "rendite-erklaert.html"]),
    ("live", "Live-Wetten verstehen", "Wie Live-Wetten und Über/Unter funktionieren und was Spieldaten verraten.",
     ["live-wetten-ueber-unter.html", "ueber-1-5-tore.html", "lohnen-sich-live-wetten.html", "live-wetten-analyse.html"]),
    ("risiko", "Risiko & Verantwortung", "Verlustserien, Einsatz und der verantwortungsvolle Umgang mit Sportwetten.",
     ["verlustserien.html"]),
    ("serioes", "Seriosität & Telegram", "Woran du seriöse Angebote erkennst und wie Wett-Analysen auf Telegram funktionieren.",
     ["seriose-tippgeber-erkennen.html", "sportwetten-telegram.html"]),
    ("ergebnisse", "Monatsberichte", "Alle Ergebnisse, auch die schwachen, dauerhaft einsehbar.",
     ["monatsberichte.html"]),
]


def wissen_hub():
    info = {e[0]: (e[4], e[2]) for e in WISSEN}
    info["monatsberichte.html"] = ("Alle Monatsberichte", "Live-Wetten mit Trefferquote, Ø-Quote und Verlustserien, Einzelspiele mit Trefferquote.")
    teile = ["\n  <p>Alle Erklärseiten von Sportwetten Radar, nach Themen sortiert. Neue Seiten kommen in die passende Kategorie.</p>\n"]
    for i, (kid, name, kdesc, pages) in enumerate(WISSEN_KAT, 1):
        items = "\n".join(f'    <li><a href="{p}">{info[p][0]}</a><br><span class="wissen-note">{info[p][1]}</span></li>' for p in pages)
        teile.append(f'  <h2 id="{kid}"><span class="num">{i:02d}</span>{name.replace("&", "&amp;")}</h2>\n  <p>{kdesc}</p>\n  <ul>\n{items}\n  </ul>\n')
    t = "Wissen: Sportwetten verständlich erklärt — Sportwetten Radar"
    d = "Erklärseiten zu Quoten, Rendite, Live-Wetten, Verlustserien und seriösen Anbietern. Alle Themen von Sportwetten Radar auf einen Blick."
    return page("wissen.html", t, d, "Wissen", "Wissen", "".join(teile), article_ld(t, d, "wissen.html", WISSEN_DATUM_HUB)), WISSEN_DATUM_HUB


WISSEN_DATUM_HUB = "2026-11-03"


def wissen_pages(today):
    out = []
    for e in WISSEN:
        path, title, desc, eb, h1, inner = e[:6]
        datum = e[6] if len(e) > 6 else WISSEN_DATUM
        out.append((page(path, title, desc, eb, h1, inner, article_ld(title, desc, path, datum)), datum))
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
    made = month_pages(months) + wissen_pages(today) + [wissen_hub()]
    sitemap(made)
    print("\n".join(p for p, _ in made))
