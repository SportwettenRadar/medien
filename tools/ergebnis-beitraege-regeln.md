# Ergebnis-Beiträge Instagram (und TikTok): feste Vorgabe (Entscheidung Daniel, 02.11.2026, überarbeitet 14:36)

Die Ergebnis-Beiträge starten ab Di 03.11.2026 (vorgezogen auf Daniels Entscheidung vom 02.11. 21:36; zuvor geplant 14.11.) auf Instagram, TikTok und YouTube (Short). Die Regeln gelten ab dem ersten Post. Daniel, 02.11. 14:36: Rendite und sonstige Kennzahlen werden weggelassen, damit alles Instagram-konform ist, und das ist KEINE Ausnahmeregelung. Damit bleiben die bisherigen Instagram-Regeln (`instagram-neukonto-regeln.md`) unverändert in Kraft; die Kennzahl-Variante vom 02.11. 14:31 (Einsätze, Wetten, Treffer %, Rendite %) ist zurückgenommen.

## Regeln
1. Das Wort "zurückgerechnet" bzw. "Rückrechnung" kommt nirgends vor. Zeiträume vor dem 11.10.2026 (Testphase) werden nicht als eigene Bilanz gezeigt; sollte eine "seit Start"-Angabe je vorkommen, steht EINE Fußnote: "Sept.–10.10.: Testphase, mit den heutigen Regeln berechnet."
2. Keine Rendite, keine Trefferquote in Prozent, keine Einsätze/Gewinn-Summen, keine Euro-Beträge, keine Kurve mit Werten. Erlaubt: Auswertung der Einträge mit Spiel, Markt, Quote und gewonnen/verloren (Stufe 3, Regel 28.10.), Darstellung als Punkte je Eintrag.
3. Wording "Auswertung", nicht "Signale". Alle Einträge zeigen, nichts aussortieren, Verluste gleichberechtigt, kein Ampel-/Rot-Großformat für einzelne Tage, schwache Wochen genauso posten.
4. Pflichtangaben: "18+ · Keine Gewinngarantie", kein Link in der Caption (Link zum Telegram-Kanal in der Bio), keine Preise/Abo/Verkaufssprache.
5. Zahlen (Rendite, Trefferquote, Einsätze, Kurve) gibt es weiter nur im Telegram-Ergebniskanal und auf der Homepage.

## Layouts (Beispiele mit erfundenen Daten, 02.11.2026)
- Tagesauswertung: eine Karte je Spieltag, je Eintrag Spiel, Markt, Quote und "gewonnen"/"verloren".
- Wochenrückblick: eine Zeile je Wochentag, ein Punkt je Eintrag (grün gewonnen, grau verloren), keine Summen.
- Monatsbericht: Text-Karte ohne Zahlen: alle Auswertungen im Ergebnis-Kanal, nichts nachträglich geändert, kleine Stichprobe; Link in der Bio.
- Generator der Beispiele: `tools/ig_ergebnis_beispiele.py` (Karten 1080x1350, Schrift/Logo wie `ig_spezial.py`).
- Dieselben Regeln gelten für TikTok (bestätigt 02.11.).

## Bestehende Planung (erledigt am 02.11.)
- YouTube Short 02.11. 18:00 und YouTube Video 02.11. 16:00: Titel, Beschreibung, Tags auf "Testphase oder live: so liest du unseren Trackrecord" umgestellt (Video 26.10. bleibt, war veröffentlicht).
- X-Video 02.11. 19:00: Text auf "Testphase (bis 10.10.) und Livebetrieb" umgestellt.
- Instagram Sa 21.11. 12:30 "Was ist eine Rückrechnung?" ersetzt durch Karussell "Regression zur Mitte" (Daniel ok, 02.11. 14:36).
- Metricool 03.–10.11. geprüft, kein weiterer Treffer. Ab 11.11. nur lokale Pläne abgeglichen (Abruf zu groß).
- Erledigt 02.11. (Daniel ok): Video 15 neu gerendert (Folie "Testphase", `out_v2/15_Trackrecord_lesen_v4.mp4`, Short `shorts2_v2/Short_15_Trackrecord_lesen_v2.mp4`) und in den Beiträgen 02.11. 16:00 (YouTube), 18:00 (YouTube Short), 19:00 (X) getauscht. Homepage (`trackrecord.js`, `trackrecord-daten.js`) und Generatoren (`seiten_generator.py`, `auto_ergebnisse.py`) auf die Fußnote "Sept.–10.10.: Testphase, mit den heutigen Regeln berechnet." umgestellt, Cache-Version angehoben.
- TikTok: gleiche Regeln wie Instagram (Daniel, 02.11.).

## Kennzahl-Reihenfolge (Entscheidung Daniel, 02.11. 14:39; am 15:48 bestätigt: "gilt überall")
Wenn Kennzahlen gezeigt werden, jede in eigener Zeile, in dieser Reihenfolge (Beispielwerte Stand 31.10., "seit Start" ab 01.09.; aktuelle Werte aus `ergebnisse.json`):
```
351 Wetten
227 Treffer (64,7 %)
+8,2 Einsätze
Rendite +2,3 %
```
- Feste Vorgabe für alle künftigen Ergebnis-Beiträge und jede Stelle, an der Kennzahlen erscheinen (Telegram, Homepage, YouTube, X; Instagram/TikTok nur, falls dort später doch Kennzahlen kommen, siehe nächste Zeile). Sie ersetzt die frühere Reihenfolge (Einsätze zuerst).
- ENTSCHIEDEN (Daniel, 02.11. 14:41): Auf Instagram/TikTok keine Kennzahlen; die drei Beispielkarten (Tagesauswertung, Wochenrückblick, Monatsbericht) werden so gepostet.
- ENTSCHIEDEN (Daniel, 02.11. 14:41): Die Verlaufslinie (Gesamtverlauf) wird auf Instagram weggelassen.

## Produktion ab 03.11.2026 (Entscheidung Daniel, 02.11. 22:09, voll automatisch)
- Täglich 10:00 (gleiche Zeit auf Instagram, TikTok, YouTube): Auswertung des Vortages. Instagram: Karussell + Stories; TikTok: Reel; YouTube: Short (gleicher Clip).
- Mo zusätzlich 12:30 Wochenauswertung (Instagram Karussell + Story), am 1. des Monats 14:00 Monatsbericht (Instagram Karussell + Story).
- Layout (freigegeben 02.11.): Tabelle Nr., Spiel, Markt, Quote, Haken grün / graues Kreuz (nie rot), 12 Zeilen je Karte; Einzelspiele (max. 5) als eigene Karte im selben Karussell; Hinweiskarte "So lesen". Woche/Monat: Punkte je Eintrag (Live und Einzelspiele getrennt), keine Zahlen. Keine Kennzahlen, keine Prozente, keine Summen, keine Kurve (Daniel, 02.11.: auch "13 von 24" nur nach 4 Wochen ohne Warnung testen).
- Reel: bis 24 Live-Einträge in Tabellenfolien (8 je Folie, chronologisch), darüber Hinweis auf das Karussell; Einzelspiele eigene Folie; Endscreen "Link in der Bio".
- Hinweise auf Kanal/Warteliste: nur "Alle Auswertungen im Ergebnis-Kanal. Link in der Bio." Warteliste nie in Beiträgen, nur auf der Zielseite hinter der Bio. Bezahlte Reichweite (Anzeigen) zurückgestellt, bis die Meta-Regeln für Wett-Werbung geklärt sind.
- Technik: `tools/ig_tagesbeitraege.py` (Modi tag/woche/monat, liest `daten/signale.json`, Ausgabe `ergebnis/<datum>/<modus>/`, manifest.json mit Texten). Geplante Aufgabe "Ergebnis-Beiträge Instagram, TikTok, YouTube (täglich 10:00)" läuft 09:22, baut, pusht, plant über Metricool ein, prüft. Bei fehlenden/unvollständigen Daten wird nichts eingeplant und Daniel benachrichtigt.
- Beispiel-Generatoren: `ig_ergebnis_*.py`; Beispielgrafiken in `instagram_ergebnis_beispiele/`.
