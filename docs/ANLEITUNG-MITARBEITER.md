# DariaTech Fernwartung – Anleitung für Mitarbeiter

Interne Anleitung für DariaTech-Mitarbeiter: Installation, Verbindungsaufbau,
wichtige Funktionen und das Bauen neuer Versionen über GitHub Actions.

## Installation

| Einsatz | Empfehlung |
|---------|------------|
| Techniker-Arbeitsplatz (dauerhaft) | `rustdesk-<version>-x86_64.msi` – klassische Installation inkl. Dienst |
| Unterwegs / USB-Stick | `rustdesk-<version>-x86_64.exe` – portable Version, keine Installation |
| macOS | `.dmg` laden, App in „Programme“ ziehen; beim ersten Start Bildschirmaufnahme-, Bedienungshilfen- und Mikrofon-Rechte in den Systemeinstellungen erteilen |
| Linux | `.deb` / `.rpm` / AppImage aus den Releases |
| Android (Techniker-Handy) | `…-universal-signed.apk` |

Alle Downloads: **GitHub → Releases** dieses Repositories.

## Verbindung zu einem Kunden

1. Kunde startet DariaTech Fernwartung (siehe [Kunden-Anleitung](ANLEITUNG-KUNDEN.md))
   und nennt **ID** und **Einmalpasswort**.
2. In der eigenen App die Kunden-ID in das Feld **ID** eingeben → **Verbinden**.
3. Passwort eingeben – die Sitzung startet.

### Wichtige Funktionen in der Sitzung

- **Dateiübertragung**: eigenes Symbol neben „Verbinden“ oder in der Sitzungs-Toolbar –
  Dateien in beide Richtungen kopieren.
- **Rechteerhöhung (UAC)**: Toolbar → „Benutzerkonten­steuerung anfordern“, wenn
  Admin-Dialoge beim Kunden schwarz bleiben.
- **Neustart mit Wiederverbindung**: Toolbar → „Remote-Gerät neu starten“ –
  nach dem Reboot verbindet die Sitzung automatisch neu (bei installierter Version).
- **Chat / TCP-Tunnel / Bildqualität**: über die Sitzungs-Toolbar.

### Unbeaufsichtigter Zugriff (Firmen-/Wartungsgeräte)

Für Geräte mit Wartungsvertrag:

1. Auf dem Zielgerät die **MSI-Version installieren** (läuft als Dienst, startet mit Windows).
2. In der App des Zielgeräts: **Einstellungen → Sicherheit → Permanentes Passwort** setzen.
3. ID + permanentes Passwort im DariaTech-Passwortmanager dokumentieren.

> ⚠️ Permanente Passwörter nur nach schriftlicher Einwilligung des Kunden einrichten
> und ausschließlich im Passwortmanager speichern.

## Eigener ID-/Relay-Server (optional, empfohlen)

Ohne Konfiguration laufen Verbindungen über die öffentlichen RustDesk-Server.
Sobald ein DariaTech-eigener [rustdesk-server](https://github.com/rustdesk/rustdesk-server)
betrieben wird:

1. **Einstellungen → Netzwerk → ID-/Relay-Server**
2. **ID-Server**: `<server.dariatech.de>` (Hostname des eigenen Servers)
3. **Key**: öffentlicher Schlüssel des Servers (Datei `id_ed25519.pub`)
4. Gleiche Einstellungen beim Kunden eintragen (oder eine vorkonfigurierte
   Version verteilen).

## Neue Version bauen (GitHub Actions)

Die Installer für **Windows, macOS, Linux, Android und iOS** werden vollständig
von GitHub Actions gebaut – keine lokale Build-Umgebung nötig.

### Build manuell starten

1. GitHub → Tab **Actions** → Workflow **„DariaTech Release Build“**.
2. Rechts **Run workflow** → optional einen Release-Tag eintragen
   (Standard: `fernwartung`) → **Run workflow**.
3. Laufzeit: ca. 1–2 Stunden (viele parallele Jobs).
4. Ergebnis:
   - **Releases → Tag `fernwartung`** (bzw. der gewählte Tag): alle Installer
     (`.exe`, `.msi`, `.dmg`, `.deb`, `.rpm`, AppImage, Flatpak, `.apk`) als
     Pre-Release.
   - Zusätzlich hängen die Rohdateien als **Artifacts** direkt am Workflow-Lauf
     (Actions → Lauf anklicken → Abschnitt „Artifacts“).

### Build über Versions-Tag

Alternativ startet ein Versions-Tag den gleichen Build automatisch:

```sh
git tag v1.4.6-1
git push origin v1.4.6-1
```

→ Release erscheint unter dem Tag-Namen (Workflow `flutter-tag.yml`).

### Hinweise

- **Code-Signierung ist optional.** Ohne die Secrets (`SIGN_BASE_URL`,
  `ANDROID_SIGNING_KEY`, `MACOS_P12_BASE64`, …) werden die Signier-Schritte
  automatisch übersprungen; die Installer funktionieren, lösen aber
  SmartScreen-/Gatekeeper-Warnungen aus (siehe Kunden-Anleitung).
- Die Versionsnummer steht in `.github/workflows/flutter-build.yml`
  (Variable `VERSION`) sowie in `Cargo.toml` / `flutter/pubspec.yaml`.
- Einzelne fehlgeschlagene Plattform-Jobs stoppen die anderen nicht
  (`fail-fast: false`) – Windows-Installer sind meist zuerst fertig.
- Der frühere **nächtliche Auto-Build ist deaktiviert** (spart Actions-Minuten);
  er kann in `.github/workflows/flutter-nightly.yml` wieder aktiviert werden.

## Branding pflegen

Name, Logo und Icons sind in [BRANDING.md](../BRANDING.md) dokumentiert.
Nach einer Logo-Änderung:

```sh
cd tools/branding
python3 deploy_brand.py   # erzeugt alle Icons/Logos neu
```

Die erzeugten Bilddateien sind per `.gitignore`-Ausnahmen versioniert und werden
mit einem normalen `git add` übernommen. Der Anzeigename steht zentral in
`flutter/lib/consts.dart` (`kAppBrandName`).

---
*Fragen zur Pipeline oder zum Branding: intern an die Technik-Leitung.
Basis: [RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0).*
