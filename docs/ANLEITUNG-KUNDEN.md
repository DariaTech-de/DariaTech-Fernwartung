# DariaTech Fernwartung – Anleitung für Kunden

Mit **DariaTech Fernwartung** kann sich ein DariaTech-Techniker – **nur mit Ihrer
Zustimmung** – auf Ihren Bildschirm aufschalten, um Probleme direkt zu lösen.
Die Einrichtung dauert etwa 2 Minuten.

## 1. Programm herunterladen

1. Öffnen Sie die Download-Seite, die Ihnen Ihr DariaTech-Ansprechpartner nennt
   (GitHub-Seite des Projekts → **Releases**).
2. Laden Sie die Datei für Ihr System herunter:

   | Ihr System | Datei |
   |------------|-------|
   | **Windows** | `rustdesk-<version>-x86_64.exe` |
   | macOS | `rustdesk-<version>-x86_64.dmg` (Intel) bzw. `…-aarch64.dmg` (Apple Silicon) |
   | Android | `rustdesk-<version>-universal-signed.apk` |

   > Die Datei heißt technisch bedingt `rustdesk-…` – nach dem Start sehen Sie
   > **DariaTech Fernwartung** mit dem DariaTech-Logo.

## 2. Programm starten (Windows)

1. Doppelklicken Sie die heruntergeladene `.exe`-Datei.
   **Eine Installation ist nicht erforderlich** – das Programm startet direkt.
2. Falls Windows eine blaue Warnung anzeigt („Der Computer wurde durch Windows
   geschützt“): Klicken Sie auf **Weitere Informationen** und dann auf
   **Trotzdem ausführen**. Die Meldung erscheint, weil das Programm nicht von
   Microsoft zertifiziert ist – es stammt direkt von DariaTech.
3. Bestätigen Sie ggf. die Windows-Firewall-Nachfrage mit **Zugriff zulassen**.

## 2b. Programm starten (macOS)

1. Öffnen Sie die heruntergeladene `.dmg`-Datei und ziehen Sie
   **DariaTech Fernwartung** in den Ordner **Programme**.
2. Beim ersten Start kann macOS melden, die App sei **„beschädigt und muss in den
   Papierkorb gelegt werden“**. Die App ist **nicht beschädigt** — die Meldung
   erscheint, weil die App nicht über den Apple App Store verteilt wird.
   So geben Sie die App einmalig frei:
   - Öffnen Sie das Programm **Terminal** (über die Spotlight-Suche, Lupe oben rechts) und
     fügen Sie diese Zeile ein, dann Eingabetaste drücken:
     ```
     xattr -cr "/Applications/DariaTech-Fernwartung.app"
     ```
   - Starten Sie die App danach normal über den Programme-Ordner.
   - Alternativ: **Systemeinstellungen → Datenschutz & Sicherheit** → unten bei der
     blockierten App auf **„Dennoch öffnen“** klicken (falls angeboten).
3. Erlauben Sie beim ersten Start die abgefragten Rechte (**Bildschirmaufnahme** und
   **Bedienungshilfen**) in den Systemeinstellungen — sonst sieht der Techniker nur
   ein schwarzes Bild.

## 3. Dem Techniker Zugriff geben

Nach dem Start sehen Sie links im Fenster:

- **Ihre ID** – eine 9-stellige Nummer
- **Einmalpasswort** – ein zufälliges Passwort

**Nennen Sie Ihrem DariaTech-Techniker am Telefon die ID und das Passwort.**
Der Techniker verbindet sich daraufhin; Sie sehen jederzeit, was auf Ihrem
Bildschirm passiert.

> 🔒 **Sicherheit**
> - Eine Verbindung ist **nur möglich, solange das Programm bei Ihnen läuft**.
> - Das Einmalpasswort ändert sich automatisch – ein alter Zugriff funktioniert nicht erneut.
> - Geben Sie ID und Passwort **niemals** an Personen weiter, die Sie unaufgefordert
>   anrufen und sich als Support ausgeben.

## 4. Sitzung beenden

- Schließen Sie einfach das Programmfenster – damit ist die Verbindung getrennt.
- Die portable Windows-Version hinterlässt keine Installation auf Ihrem PC;
  Sie können die Datei danach löschen oder für das nächste Mal aufbewahren.

## Häufige Fragen

**Kann DariaTech jederzeit auf meinen PC zugreifen?**
Nein. Ohne das laufende Programm und ohne das aktuelle Passwort ist kein Zugriff möglich.
(Ausnahme: Sie haben mit DariaTech ausdrücklich einen dauerhaften Wartungszugang vereinbart.)

**Das Programm startet nicht / die Verbindung schlägt fehl.**
Prüfen Sie Ihre Internetverbindung und starten Sie das Programm neu.
Hilft das nicht, rufen Sie Ihren DariaTech-Ansprechpartner an.

**Muss ich das Programm aktualisieren?**
Nein. Laden Sie bei Bedarf einfach die aktuelle Version von der Download-Seite –
Ihr Techniker weist Sie darauf hin, wenn eine neue Version nötig ist.

---
*DariaTech – IT Systemhaus · DariaTech Fernwartung basiert auf dem
Open-Source-Projekt [RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0).*
