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
   - Text: nackte Zahlen, kein Gewinnversprechen, kein Buchmacher-Link, Rückrechnung kennzeichnen, „18+ · Keine Gewinngarantie“, Link zur Homepage.
5. Kurze Meldung an Daniel, was veröffentlicht wurde.

## Prüfungen im Skript
- Treffer ≤ Wetten, Rendite plausibel, Gewinn = Rendite × Wetten / 100 (Rundungstoleranz)
- Wochen volle Mo–So, Monat nach Mehrheitsregel, Summe der Tage = Woche/Monat
- Bereits veröffentlichte Homepage-Werte werden nie überschrieben; Abweichung = Stopp
