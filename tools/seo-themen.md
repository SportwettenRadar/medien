# SEO-Erklärseiten: Themenstand (wöchentlich montags, Auftrag Daniel 23.10.2026)

Reihenfolge laut Auftrag. Erledigt = auf der Homepage veröffentlicht.

| Nr | Thema | Seite | Status |
|---|---|---|---|
| 1 | Was bedeutet Quote 1,70? | quote-1-70-bedeutung.html | veröffentlicht 27.10.2026, Indexierung beantragt |
| 2 | Was ist Über 1,5 Tore? | ueber-1-5-tore.html | veröffentlicht 02.11.2026, Indexierung beantragt 02.11., Video 11.11. nach Veröffentlichung einbetten |
| 3 | Lohnen sich Live-Wetten? | lohnen-sich-live-wetten.html | veröffentlicht 03.11.2026, Indexierung beantragt 03.11., Video 18.11. nach Veröffentlichung einbetten |
| 4 | Wie viele Tore fallen in der 2. Halbzeit? | tore-zweite-halbzeit.html | Vorschau 10.11.2026 (Branch vorschau-halbzeit2), wartet auf Freigabe Daniel; kein Video vorhanden; Kategorie Live-Wetten verstehen |
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
5. Seite in WISSEN_KAT einsortieren (siehe Regel oben), Generator laufen lassen.
6. Nächste Erinnerung per send_later 7 Tage später.

## Regel Wissen-Navigation (Daniel, 27.10.2026)
Footer und Menü zeigen unter "Wissen" nur 5–6 Kategorien (Quoten & Rendite, Live-Wetten verstehen, Risiko & Verantwortung, Seriosität & Telegram, Monatsberichte), verlinkt auf wissen.html#<id>. Neue Erklärseiten werden NUR in WISSEN_KAT (tools/seiten_generator.py) in eine Kategorie einsortiert, nie als neuer Footer-Eintrag. Zuordnung der geplanten Themen: Über 1,5 Tore, Lohnen sich Live-Wetten, 2. Halbzeit → Live-Wetten verstehen; Einzelwette/Kombi, Erwartungswert → Quoten & Rendite; Budget, Warnsignale Spielsucht → Risiko & Verantwortung.

## Vorsicht
Die Automatik (Tages-/Wochenlauf) regeneriert Seiten mit dem Generator aus dem Medien-Repo. Änderungen an Seiten immer zuerst im Generator machen, sonst werden sie überschrieben (27.10.: Fußnote Rückrechnung wurde so überschrieben und ist behoben).
