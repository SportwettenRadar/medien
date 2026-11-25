# Nachtrag Rechtstexte (Entwurf, NICHT veröffentlicht) – Stand 25.11.2026

## 2. Belehrung: Hinweis auf die Widerrufsfunktion (nach Absatz „Um Ihr Widerrufsrecht auszuüben …“)
Neu: „Sie können Ihren Widerruf auch über die Widerrufsfunktion auf unserer Website erklären (Link „Vertrag widerrufen“ im Seitenfuß und unter [widerrufen.html]). Dort geben Sie Ihren Namen, die Bezeichnung des Vertrags und die E-Mail-Adresse an, an die wir die Eingangsbestätigung senden, und klicken auf „Widerruf bestätigen“. Wir senden Ihnen unverzüglich eine Eingangsbestätigung per E-Mail.“
Footer: im Block „Rechtliches“ unter „Verträge hier kündigen“: <li><a href="widerrufen.html">Vertrag widerrufen</a></li> (Footer kommt aus risikohinweis.html, Generator übernimmt).
UNSICHER: Wortlaut gegen Muster-Widerrufsbelehrung (Anlage 1 EGBGB, Gestaltungshinweis zur Widerrufsfunktion) abgleichen; ich habe den amtlichen Wortlaut nicht im Original gesehen.

## 3. Datenschutz 3.5 (ersetzt den online stehenden Absatz)
Bei jeder Buchung speichern wir zusammen mit Ihrer Telegram-Chat-ID und der Stripe-Abonnement-Kennung den Zeitpunkt der Buchung, das gebuchte Paket, den Status des Abonnements sowie Ihre Bestätigungen, dass (a) die Leistung sofort beginnen soll, (b) Ihnen bekannt ist, dass Sie bei einem Widerruf den anteiligen Wert der bis dahin erbrachten Leistung zu zahlen haben, und (c) Sie mindestens 18 Jahre alt sind. Diese Angaben dienen ausschließlich dem Nachweis, dass die gesetzlichen Voraussetzungen für den Vertragsschluss, den sofortigen Beginn der Leistung und den Wertersatz im Widerrufsfall erfüllt sind. [Rest unverändert: PythonAnywhere, Rechtsgrundlagen, Speicherdauer]
(Online steht derzeit noch „Erlöschen des Widerrufsrechts“ und ein grammatisch kaputter Satz „dass Sie der sofortigen Beginn der Leistung zugestimmt (Widerrufs-Erklärung)“ – meine Folgeänderung von heute.)

## 4a. Datenschutz neu: Vertragsbestätigung per E-Mail
Nach der Buchung senden wir Ihnen an die bei Stripe angegebene E-Mail-Adresse eine Vertragsbestätigung. Der Versand erfolgt über unser Postfach bei STRATO (Ziffer 4). Sie enthält das gebuchte Paket, den Preis, die Laufzeit, den Zeitpunkt der Buchung, Ihre Bestätigungen nach Ziffer 3.5, die Widerrufsbelehrung mit Muster-Widerrufsformular und den Link zur Widerrufsfunktion. Rechtsgrundlagen sind Art. 6 Abs. 1 lit. b und lit. c DS-GVO (Bestätigung des Vertrags auf einem dauerhaften Datenträger).
OFFEN: Speicherung einer Kopie der Mail? Dauer? (Code 3 fragen)

## 4b. Datenschutz neu: Widerruf über unsere Website (analog 3.6)
Nutzen Sie die Widerrufsfunktion auf unserer Website, verarbeiten wir Ihren Namen, die Bezeichnung des Vertrags, Ihre E-Mail-Adresse und den Zeitpunkt des Eingangs, um Ihren Widerruf zuzuordnen, auszuführen und den Eingang zu bestätigen. Die Angaben werden beim Absenden an unsere Anwendung bei PythonAnywhere (Ziffer 3.4) übermittelt und dort als Nachweis gespeichert. Die Eingangsbestätigung senden wir Ihnen per E-Mail über unser Postfach bei STRATO (Ziffer 4); eine Kopie geht an support@sportwetten-radar.net. Die Widerrufserklärung wird bis zum Ablauf der gesetzlichen Verjährungsfristen aufbewahrt. Rechtsgrundlagen: Art. 6 Abs. 1 lit. b und lit. c DS-GVO (§ 356a BGB).
OFFEN: Verarbeitet /widerrufen die IP-Adresse wie /kuendigen (Rate-Limit)? Wenn ja, den IP-Absatz aus 3.6 übernehmen. Telegram-Nachricht als zusätzliche Bestätigung? (Code 3 fragen)
Nummerierung: neue Abschnitte als 3.7 und 3.8, bisherige 3.7–3.9 rücken auf 3.9–3.11; Querverweise prüfen.
