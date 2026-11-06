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
   - Text: nackte Zahlen, kein Gewinnversprechen, kein Buchmacher-Link, Zeilenformat siehe Abschnitt „Anzeigeregel ab 06.11.2026“ (Tag/Woche/Monat: n von m Treffer, Trefferquote, Ø-Quote; Einsätze/Rendite nur im Block Jahr), Fußnote nur wo Tage vor dem 11.10.2026 enthalten sind („* Sept.–10.10.: Testphase, mit den Regeln vom 11.10.2026 berechnet.“; Erkennung über das Feld `rueckrechnung`, das Wort nie anzeigen), „18+ · Keine Gewinngarantie“, Link zur Homepage.
5. Kurze Meldung an Daniel, was veröffentlicht wurde.

## Prüfungen im Skript
- Treffer ≤ Wetten, Rendite plausibel, Gewinn = Rendite × Wetten / 100 (Rundungstoleranz)
- Wochen volle Mo–So, Monat nach Mehrheitsregel, Summe der Tage = Woche/Monat
- Bereits veröffentlichte Homepage-Werte werden nie überschrieben; Abweichung = Stopp

## Anzeigeregel ab 06.11.2026 (Entscheidung Daniel, ersetzt das Format vom 02.11.2026)
- **Tag, Woche, Monat:** `3 von 5 Treffer (60,0 %)` und `Ø-Quote 1,58`. KEINE Einsätze, KEINE Rendite. Monat zusätzlich „Längste Verlustserie“. Ø-Quote = Durchschnitt der Quoten ALLER gesetzten Live-Wetten des Zeitraums (nicht nur der gewonnenen), zwei Nachkommastellen. Fehlt sie (Zeitraum vor dem 11.10., Bot liefert sie noch nicht), wird die Zeile weggelassen, nie geschätzt.
- **Kalenderjahr (Jahresübersicht):** Wetten, Treffer (%), Ø-Quote, Einsätze und Rendite, aber Einsätze/Rendite erst ab 100 gewerteten Live-Wetten im Jahr (`JAHR_MIN_WETTEN`). Darunter steht kein Wert, Kurve und Zahlen erscheinen erst bei Erreichen (Januar-Lücke gewollt). 2026 läuft verkürzt ab 01.09.
- Hinweissatz auf Homepage, Monatsseiten und AGB § 2 (3): Einsätze/Rendite je Kalenderjahr ab 100 Live-Wetten, für Tage/Wochen/Monate nicht (Zufall).
- Veröffentlichte Daten: `trackrecord-daten.js` enthält für Monate/Wochen nur wetten, treffer, quote, verlustserie (keine rendite/gewinn/rueckgang/besterTag/schlechtesterTag). `TRACKRECORD_JAHRE` trägt das Jahr (gewinn/rendite null unter 100 Wetten), `TRACKRECORD_TAGE` die Jahreskurve (je Jahr bei 0 beginnend, nur für freigegebene Jahre).
- Ø-Quote-Quelle: `live.quote` aus ergebnisse.json (sobald der Bot sie liefert), sonst Einzelquoten aus `daten/signale.json`, aber nur wenn die Anzahl vollständig zu `live.wetten` passt.
- Tagesbilanz/Monatsbericht-Grafik: Karte „Live-Wetten“ (Tag/Monat) plus Karte „Jahr“ mit Einsätze/Rendite; Wochenbilanz nur die Wochenkarte. Skript-Ausgabe `grafiken[].live` enthält absichtlich nur wetten/treffer/quote, das Jahr steht in `grafiken[].jahr`.
- Datenquelle Jahr: `tage[]` mit Feld `seitStart` {wetten, treffer, rendite, gewinn} (Stand am Tagesende).
- Nach jeder Umstellung: `python3 tools/abgleich_zahlen.py --medien <medien> --homepage <homepage>` (Exit 0 = alle Zahlen gleich, keine verbotenen Felder/Wörter, Jahr-Schwelle eingehalten).
