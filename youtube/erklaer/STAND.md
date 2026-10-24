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
- [ ] Monatsbericht-Video 01.11. (Erinnerung 01.11. 11:30 gesetzt, trig_01XSXVnj97p8jixSRAhNG2mD)

## 23.10. Umbau Eröffnung (Freigabe Daniel)
- Alle Videos starten mit Hook-Folie (typ "hook", 2,6 s, großer Satz, Zoom). Gilt auch für alle künftigen Videos inkl. Monatsbericht.
- Neue Dateien: youtube/erklaer/out_v2 (16:9), youtube/shorts2_v2 (neue Shorts), youtube/alt_v2 (ältere Shorts mit vorangestelltem Hook, tools/hook_vor_short.py)
- Alle 58 eingeplanten YouTube-Posts in Metricool auf die neuen Dateien umgestellt (Termine unverändert)
- Sendeplan: tools/sendeplan.md

## 24.10. Playlists + Shorts-Vorschaubild
- Alle 21 Erklärvideos 25.10.–04.11. in Metricool mit Playlist versehen (über Metricool-Weboberfläche im Browser, Daniel eingeloggt). API zeigt youtubeData.playlistId: Sportwetten verstehen = PLGJDnNMLqxao, So arbeitet Sportwetten Radar = PLC9BzoTSUGzI, Verantwortungsvoll wetten = PLC6BZPnzm6hU, Ergebnisse und Monatsberichte = noch unbekannt. Ob die API playlistId beim Schreiben annimmt: ungetestet (Feldnamen playlist/playlists/playlistName werden verworfen).
- ACHTUNG: API-Updates an diesen 16:9-Posts nur mit playlistId im youtubeData, sonst geht die Playlist verloren.
- Alle 35 Shorts 25.10.–28.11.: videoCoverMilliseconds 1200 (Hook-Folie als Vorschaubild). Prüfung 25.10. 18:45 (trig_015Fcuu2WAifiCZPdNfKPYrR).
- Monatsbericht 01.11.: Playlist "Ergebnisse und Monatsberichte" im Browser setzen.
