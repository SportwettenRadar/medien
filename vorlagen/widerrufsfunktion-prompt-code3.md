# Prompt für Code 3: Widerrufsfunktion (§ 356a BGB) – Backend und Bot-Text

Stand 25.11.2026. Entwurf der Seite: vorlagen/widerrufen.html (nicht veröffentlicht). Vorlage für das Backend: der vorhandene Endpunkt /kuendigen.

## 1. Backend /widerrufen (PythonAnywhere, analog /kuendigen)
- POST mit JSON {name, vertrag, email}. Kein Login, keine weiteren Pflichtfelder.
- Eingang protokollieren (Zeitstempel, Angaben). Widerruf gilt mit Absendung der Erklärung.
- Sofort Eingangsbestätigung per E-Mail an die angegebene Adresse (dauerhafter Datenträger): Inhalt der Erklärung, Datum und Uhrzeit des Eingangs.
- Kopie des Eingangs an support@sportwetten-radar.net. Erstattung und Wertersatz bleiben manuell (Stripe).
- Nicht anfassen: abos.csv, kuendigungen.csv, warteliste.csv, herkunft.csv, bot_state.json, bot.log*.

## 2. Bot/Stripe-Bestelltext (Dienstleistungs-Konstruktion, EuGH C-234/25)
Checkbox statt „Verzicht auf Widerrufsrecht“: Ich verlange ausdrücklich, dass die Leistung sofort beginnt. Mir ist bekannt: Widerrufe ich innerhalb von 14 Tagen, muss ich den anteiligen Wert der bis dahin erbrachten Leistung zahlen. Abgleich mit AGB § 3 Abs. 2, § 6 und der Widerrufsbelehrung.
Nachweis (Datenschutz 3.5): Zeitpunkt, Paket, Zustimmung zum sofortigen Beginn, Volljährigkeit.

## 3. Erst danach (zusammen veröffentlichen, vor dem 08.01.2027)
- vorlagen/widerrufen.html in die Homepage legen, Footer-Link „Vertrag widerrufen“ auf allen Seiten (Footer kommt aus risikohinweis.html).
- Widerrufsbelehrung: Hinweis auf die Widerrufsfunktion (Muster-Belehrung Gestaltungshinweis 3, 1. Alternative) ergänzen.
- Datenschutz: Verarbeitung der Widerrufsangaben ergänzen.
