# Ergebnis-Beiträge Instagram (und TikTok): feste Vorgabe (Entscheidung Daniel, 02.11.2026, überarbeitet 14:36)

> **STAND 06.11.2026 (Daniel):**
> - **TikTok:** keine Ergebnis-, Auswertungs- oder Punkte-Videos mehr (zweiter Verstoß am 06.11.). TikTok läuft nur mit Stufe 1 und 2. Die tägliche Automatik (09:22) plant nur noch Instagram und YouTube. Wo unten "TikTok" im Zusammenhang mit Ergebnis-Beiträgen steht, ist das überholt.
> - **Anzeigeregel 06.11.** (claude/anzeigeregel-rendite-0611.md) ersetzt die Kennzahl-Reihenfolge vom 02.11. Für Instagram und YouTube-Short-Ergebnisbeiträge bleibt es bei der Darstellung OHNE Zahlen (Entscheidung Daniel 06.11.): kein "n von m", keine Trefferquote in Prozent, keine Ø-Quote. Diese Zahlen gibt es nur auf Telegram, Homepage und X (X läuft aus) und im Jahresblock.

Die Ergebnis-Beiträge starten ab Di 03.11.2026 (vorgezogen auf Daniels Entscheidung vom 02.11. 21:36; zuvor geplant 14.11.) auf Instagram, TikTok und YouTube (Short). Die Regeln gelten ab dem ersten Post. Daniel, 02.11. 14:36: Rendite und sonstige Kennzahlen werden weggelassen, damit alles Instagram-konform ist, und das ist KEINE Ausnahmeregelung. Damit bleiben die bisherigen Instagram-Regeln (`instagram-neukonto-regeln.md`) unverändert in Kraft; die Kennzahl-Variante vom 02.11. 14:31 (Einsätze, Wetten, Treffer %, Rendite %) ist zurückgenommen.

## Regeln
1. Das Wort "zurückgerechnet" bzw. "Rückrechnung" kommt nirgends vor. Zeiträume vor dem 11.10.2026 (Testphase) werden nicht als eigene Bilanz gezeigt; sollte eine Jahres-Angabe ("Jahr 2026 (ab 01.09.)") je vorkommen, steht EINE Fußnote: "01.09.–10.10.: Testphase, mit den Regeln vom 11.10.2026 berechnet."
2. Keine Rendite, keine Trefferquote in Prozent, keine Einsätze/Gewinn-Summen, keine Euro-Beträge, keine Kurve mit Werten. Erlaubt: Auswertung der Einträge mit Spiel, Markt, Quote und gewonnen/verloren (Stufe 3, Regel 28.10.), Darstellung als Punkte je Eintrag.
3. Wording "Auswertung", nicht "Signale". Alle Einträge zeigen, nichts aussortieren, Verluste gleichberechtigt, kein Ampel-/Rot-Großformat für einzelne Tage, schwache Wochen genauso posten.
4. Pflichtangaben: "18+ · Keine Gewinngarantie", kein Link in der Caption (Link zum Telegram-Kanal in der Bio), keine Preise/Abo/Verkaufssprache.
5. Zahlen (Rendite, Trefferquote, Einsätze, Kurve, auch "n von m" und Ø-Quote) gibt es weiter nur im Telegram-Ergebniskanal und auf der Homepage (Daniel 06.11.: gilt auch nach der neuen Anzeigeregel).

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
- Erledigt 02.11. (Daniel ok): Video 15 neu gerendert (Folie "Testphase", `out_v2/15_Trackrecord_lesen_v4.mp4`, Short `shorts2_v2/Short_15_Trackrecord_lesen_v2.mp4`) und in den Beiträgen 02.11. 16:00 (YouTube), 18:00 (YouTube Short), 19:00 (X) getauscht. Homepage (`trackrecord.js`, `trackrecord-daten.js`) und Generatoren (`seiten_generator.py`, `auto_ergebnisse.py`) auf die Fußnote "Sept.–10.10.: Testphase, mit den Regeln vom 11.10.2026 berechnet." umgestellt, Cache-Version angehoben.
- TikTok: gleiche Regeln wie Instagram (Daniel, 02.11.).

## Kennzahl-Format (Anzeigeregel 06.11.2026, ersetzt die Reihenfolge vom 02.11.)
Gilt dort, wo Kennzahlen gezeigt werden (Telegram, Homepage, X; NICHT Instagram/TikTok/YouTube-Short-Ergebnisbeiträge):
```
Tag, Woche, Monat:   3 von 5 Treffer (60,0 %)
                     Ø-Quote 1,58            (Zeile weglassen, wenn nicht vorhanden)
Monat zusätzlich:    Längste Verlustserie
Kalenderjahr:        Wetten, Treffer (%), Ø-Quote, Einsätze, Rendite (Einsätze/Rendite erst ab 100 Live-Wetten im Jahr)
```
- KEINE Einsätze, KEINE Rendite, kein "Größter Rückgang", kein "Bester/Schlechtester Tag" für Tag/Woche/Monat. Keine Kumulativ-Zahl "Seit Start".
- Die frühere Reihenfolge (Wetten / Treffer / Einsätze / Rendite je Zeitraum, Beispielwerte Stand 31.10.) ist ersetzt.
- ENTSCHIEDEN (Daniel, 02.11. 14:41, weiter gültig): Auf Instagram/TikTok keine Kennzahlen; Verlaufslinie auf Instagram weggelassen.

## Produktion ab 03.11.2026 (Entscheidung Daniel, 02.11. 22:09, voll automatisch)
- Täglich 10:00 (gleiche Zeit auf Instagram, TikTok, YouTube): Auswertung des Vortages. Instagram: Karussell + Stories; TikTok: Reel; YouTube: Short (gleicher Clip).
- Mo zusätzlich 12:30 Wochenauswertung (Instagram Karussell + Story), am 1. des Monats 14:00 Monatsbericht (Instagram Karussell + Story).
- Layout (freigegeben 02.11.): Tabelle Nr., Spiel, Markt, Quote, Haken grün / graues Kreuz (nie rot), 12 Zeilen je Karte; Einzelspiele (max. 5) als eigene Karte im selben Karussell; Hinweiskarte "So lesen". Woche/Monat: Punkte je Eintrag (Live und Einzelspiele getrennt), keine Zahlen. Keine Kennzahlen, keine Prozente, keine Summen, keine Kurve (Daniel, 02.11.: auch "13 von 24" nur nach 4 Wochen ohne Warnung testen).
- Reel: bis 24 Live-Einträge in Tabellenfolien (8 je Folie, chronologisch), darüber Hinweis auf das Karussell; Einzelspiele eigene Folie; Endscreen "Link in der Bio".
- Hinweise auf Kanal/Warteliste: nur "Alle Auswertungen im Ergebnis-Kanal. Link in der Bio." Warteliste nie in Beiträgen, nur auf der Zielseite hinter der Bio. Bezahlte Reichweite (Anzeigen) zurückgestellt, bis die Meta-Regeln für Wett-Werbung geklärt sind.
- Technik: `tools/ig_tagesbeitraege.py` (Modi tag/woche/monat, liest `daten/signale.json`, Ausgabe `ergebnis/<datum>/<modus>/`, manifest.json mit Texten). Geplante Aufgabe "Ergebnis-Beiträge Instagram, TikTok, YouTube (täglich 10:00)" läuft 09:22, baut, pusht, plant über Metricool ein, prüft. Bei fehlenden/unvollständigen Daten wird nichts eingeplant und Daniel benachrichtigt.
- Beispiel-Generatoren: `ig_ergebnis_*.py`; Beispielgrafiken in `instagram_ergebnis_beispiele/`.
