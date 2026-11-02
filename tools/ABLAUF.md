# Automatik Ergebnisse (Sportwetten Radar)

Datenquelle: `daten/ergebnisse.json` (schreibt der Bot nach jedem Post im Ergebnis-Kanal t.me/sportwettenradar).

## Ablauf je Lauf (Montag 11:00 = woche, am 1. 11:00 = monat)
1. Repos aktualisieren: `sportwettenradar/medien` und `sportwettenradar/sportwetten-radar.net`.
2. `python3 tools/auto_ergebnisse.py --medien <medien> --homepage <homepage> --modus woche|monat`
3. `status: stopp` → nichts veröffentlichen, Fehlerliste an Daniel melden.
4. `status: ok` →
   - Homepage committen und pushen (trackrecord-daten.js, Monatsbericht-Seiten, sitemap.xml).
   - Grafik in `x/` im Medien-Repo committen und pushen.
   - X-Post über Metricool einplanen (sofort bzw. nächste volle Viertelstunde), Bild-URL:
     `https://raw.githubusercontent.com/sportwettenradar/medien/main/<datei>`
   - Text: nackte Zahlen, kein Gewinnversprechen, kein Buchmacher-Link, Zeilenformat (jede Kennzahl eigene Zeile, Einsätze zuerst), Fußnote nur wo Tage vor dem 11.10.2026 enthalten sind („* Sept.–10.10.: Testphase, mit den heutigen Regeln berechnet.“; Erkennung über das Feld `rueckrechnung`, das Wort nie anzeigen), „18+ · Keine Gewinngarantie“, Link zur Homepage.
5. Kurze Meldung an Daniel, was veröffentlicht wurde.

## Prüfungen im Skript
- Treffer ≤ Wetten, Rendite plausibel, Gewinn = Rendite × Wetten / 100 (Rundungstoleranz)
- Wochen volle Mo–So, Monat nach Mehrheitsregel, Summe der Tage = Woche/Monat
- Bereits veröffentlichte Homepage-Werte werden nie überschrieben; Abweichung = Stopp

## Neues Zahlenformat (Entscheidung Daniel, 02.11.2026)
- Format überall: `+8,2 Einsätze` / `351 Wetten` / `227 Treffer (64,7 %)` / `Rendite +2,3 %`, je Kennzahl eine Zeile, Einsätze zuerst, keine Ampelfarben.
- Tagesbilanz (X, Grafik): Live-Wetten des Tages, darunter Block „Seit Start“ im selben Format, eine Fußnote, Pflichtsatz.
- Trackrecord (Homepage und Monatsseiten): vier Kennzahlen, EINE Linie (kumulierte Einsätze je Tag seit 01.09.2026, Nulllinie gestrichelt, letzter Wert als Punkt, Bereich ab Livestart hinterlegt und mit „live“ beschriftet), darunter Monatstabelle Monat | Einsätze | Wetten | Treffer | Rendite.
- Datenquelle: `tage[]` ab 01.09.2026 mit Feld `seitStart` {wetten, treffer, rendite, gewinn} (Stand am Tagesende). `auto_ergebnisse.py` schreibt daraus `TRACKRECORD_TAGE` und `TRACKRECORD_START` in trackrecord-daten.js.
- Nach jeder Umstellung: `python3 tools/abgleich_zahlen.py --medien <medien> --homepage <homepage>` (Exit 0 = alle Zahlen gleich, auch keine verbotenen Wörter).
