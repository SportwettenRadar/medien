# Stand YouTube-Erklärvideos (Freigabe Daniel 22.10.2026, 09:19)

- Plan: tools/youtube-grundstock-plan.md · Inhalte/Termine: youtube/erklaer/videos.py → meta.json, specs/
- Generator: tools/erklaervideo.py (16:9, ohne Ton, Fortschrittsleiste, Vorschaubild 1280x720)
- Videos: youtube/erklaer/out/<nr>_<slug>.mp4 + _thumb.png (Raw-URL für Metricool)
- Einplanung Metricool: 2 pro Tag 12:00 und 19:30, 24.10.–04.11.; Monatsbericht Oktober 01.11. 19:30 (Video wird am 01.11. aus den Monatsdaten gebaut)
- Playlists: nicht über Metricool setzbar → Daniel ordnet sonntags in YouTube Studio zu

## Status
- [x] 23 Videos gebaut
- [x] ins Repo gepusht
- [x] in Metricool eingeplant 22.10. (IDs 402879793, 402880033 … 402881688; mit Vorschaubild, Kanal am 22.10. bestätigt)
- [x] Monatsbericht-Video Oktober gebaut (specs/24, out_v2/24_Monatsbericht_2026_10.mp4 + _thumb.png), 01.11. 19:30 in Metricool eingeplant (ID 412807439). Playlist "Ergebnisse und Monatsberichte" fehlt noch: Daniel setzt sie in YouTube Studio / Metricool-Weboberfläche.

## 23.10. Umbau Eröffnung (Freigabe Daniel)
- Alle Videos starten mit Hook-Folie (typ "hook", 2,6 s, großer Satz, Zoom). Gilt auch für alle künftigen Videos inkl. Monatsbericht.
- Neue Dateien: youtube/erklaer/out_v2 (16:9), youtube/shorts2_v2 (neue Shorts), youtube/alt_v2 (ältere Shorts mit vorangestelltem Hook, tools/hook_vor_short.py)
- Alle 58 eingeplanten YouTube-Posts in Metricool auf die neuen Dateien umgestellt (Termine unverändert)
- Sendeplan: tools/sendeplan.md

## 24.10. Playlists + Shorts-Vorschaubild
- Alle 21 Erklärvideos 25.10.–04.11. in Metricool mit Playlist versehen (über Metricool-Weboberfläche im Browser, Daniel eingeloggt). API zeigt youtubeData.playlistId: Sportwetten verstehen = PLGJDnNMLqxao, So arbeitet Sportwetten Radar = PLC9BzoTSUGzI, Verantwortungsvoll wetten = PLC6BZPnzm6hU, Ergebnisse und Monatsberichte = PLLLK7PIctfk0 (von Daniel 01.11.). Ob die API playlistId beim Schreiben annimmt: ungetestet (Feldnamen playlist/playlists/playlistName werden verworfen).
- ACHTUNG: API-Updates an diesen 16:9-Posts nur mit playlistId im youtubeData, sonst geht die Playlist verloren.
- Alle 35 Shorts 25.10.–28.11.: videoCoverMilliseconds 1200 (Hook-Folie als Vorschaubild). Prüfung 25.10. 18:45 (trig_015Fcuu2WAifiCZPdNfKPYrR).
- Monatsbericht 01.11.: Playlist "Ergebnisse und Monatsberichte" im Browser setzen.
- 26.10.: Test bestanden – Short 25.10. veröffentlicht, Hook-Folie erscheint als Vorschaubild (Daniel geprüft). Playlists auf YouTube korrekt befüllt.

- 01.11.: Monatsbericht Oktober veröffentlicht (Y-_C0GysC_M), Playlist von Daniel in Studio gesetzt. Künftige Monatsberichte: playlistId PLLLK7PIctfk0 in youtubeData mitgeben.
- Video 15 "Trackrecord richtig lesen" (g0mjY48saHM, 26.10. veröffentlicht) enthält "Jeder Monat. Jede Woche."; korrigierte Fassung out_v2/15_Trackrecord_lesen_v3.mp4 gebaut, Austausch wartet auf Daniels Ja (alt in Studio löschen).
