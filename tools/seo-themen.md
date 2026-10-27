# SEO-Erklärseiten: Themenstand (wöchentlich montags, Auftrag Daniel 23.10.2026)

Reihenfolge laut Auftrag. Erledigt = auf der Homepage veröffentlicht.

| Nr | Thema | Seite | Status |
|---|---|---|---|
| 1 | Was bedeutet Quote 1,70? | quote-1-70-bedeutung.html | veröffentlicht 27.10.2026, Indexierung bei Daniel offen |
| 2 | Was ist Über 1,5 Tore? | | offen |
| 3 | Lohnen sich Live-Wetten? | | offen |
| 4 | Wie viele Tore fallen in der 2. Halbzeit? | | offen |
| 5 | Einzelwette oder Kombiwette? | | offen |
| 6 | Erwartungswert bei Sportwetten | | offen |
| 7 | Budget für Sportwetten festlegen | | offen |
| 8 | Warnsignale Spielsucht | | offen |

Danach eigene Vorschläge mit Begründung.

## Ablauf je Seite
1. Eintrag in WISSEN (tools/seiten_generator.py), Generator auf Kopie des Homepage-Repos laufen lassen.
2. Footer-Link "Wissen" in ALLEN HTML-Dateien ergänzen (nach dem Link zu seriose-tippgeber-erkennen.html), Sitemap kommt aus dem Generator.
3. Video einbetten (youtube-nocookie, erst nach Klick), Datenschutz Abschnitt "Eingebettete YouTube-Videos" (id="youtube") ist seit dieser Seite vorbereitet.
4. Vorschau an Daniel, nach Freigabe Homepage + Generator committen, Daniel bittet um Indexierung (Search Console).
5. Nächste Erinnerung per send_later 7 Tage später.

## Vorsicht
Die Automatik (Tages-/Wochenlauf) regeneriert Seiten mit dem Generator aus dem Medien-Repo. Änderungen an Seiten immer zuerst im Generator machen, sonst werden sie überschrieben (27.10.: Fußnote Rückrechnung wurde so überschrieben und ist behoben).
