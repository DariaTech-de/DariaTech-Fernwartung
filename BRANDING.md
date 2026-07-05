# DariaTech Fernwartung – Branding

Diese Datei dokumentiert die Personalisierung von RustDesk zu **DariaTech Fernwartung**.

## Konzept

- **App-Name überall**: `DariaTech Fernwartung` — als Whitelabel über den zentralen
  `APP_NAME` in `libs/hbb_common/src/config.rs`. Daraus leiten sich automatisch ab:
  - alle UI-Texte (die Übersetzungsschicht `src/lang.rs` ersetzt „RustDesk“ durch den App-Namen),
  - Windows: Installationsordner `C:\Program Files\DariaTech Fernwartung`, installierte
    `DariaTech Fernwartung.exe`, Dienstname, Startmenü-/Uninstall-Einträge (MSI via
    `preprocess.py --app-name`),
  - macOS: `DariaTech Fernwartung.app` (`PRODUCT_NAME` in
    `flutter/macos/Runner/Configs/AppInfo.xcconfig`), LaunchDaemon-/Agent-Pfade
    (zur Laufzeit via `correct_app_name()`),
  - Konfigurations-/Log-Verzeichnisse.
- `libs/hbb_common` ist **kein Submodule mehr**, sondern fest eingecheckt (vendored),
  damit der `APP_NAME`-Patch versioniert ist. Basis: `rustdesk/hbb_common@42af0f0a`.
- **URI-Schema bleibt `rustdesk://`** (`get_uri_prefix()` in `src/common.rs` fest
  verdrahtet): URL-Schemata dürfen keine Leerzeichen enthalten, und Android/iOS/
  Linux-Desktop-Datei/MSI registrieren das Schema statisch.
- Interner Binärname der Roh-Artefakte bleibt `rustdesk` (z. B. `rustdesk-1.4.6-x86_64.exe`
  als Download); bei der Installation wird auf den Markennamen umbenannt.
- Attribution **„Powered by RustDesk"** wird unten im Startbildschirm und im About-Dialog angezeigt
  (Open-Source-Projekt fair gewürdigt); Upstream-Update-Checks sind im Whitelabel-Modus
  automatisch deaktiviert.

Der Anzeige-Name für die Flutter-UI liegt zusätzlich in `flutter/lib/consts.dart` als `kAppBrandName`.

## Bereits umgesetzt (Name)

| Plattform | Datei | Feld |
|-----------|-------|------|
| Windows | `flutter/windows/runner/Runner.rc` | `ProductName`, `FileDescription`, `CompanyName`, `LegalCopyright` |
| macOS | `flutter/macos/Runner/Info.plist` | `CFBundleDisplayName` |
| Android | `flutter/android/app/src/main/AndroidManifest.xml` | `android:label` (App + Input-Service) |
| Linux | `res/rustdesk.desktop`, `res/rustdesk-link.desktop` | `Name`, `Comment` |
| In-App | `flutter/lib/consts.dart` (`kAppBrandName`, `kPoweredBy`) | Fenstertitel, Tab-Leiste, About-Dialog, Startbildschirm |

## Logo & Icon – umgesetzt

Logo und Icon wurden aus der gelieferten Logo-Datei abgeleitet:
- **Logo** = der grüne Banner „DariaTech – IT Systemhaus" (aus dem Original ausgeschnitten).
- **Icon** = das Chevron-/Rauten-Symbol (teal `#01C4A6` auf Grün `#09250F`), als Vektor
  nachgebaut und in alle benötigten Größen gerendert.

Markenfarben: Grün `#09250F`, Teal `#01C4A6`.

### In-App (Flutter)

| Datei | Inhalt |
|-------|--------|
| `flutter/assets/logo.png` | Header-Logo (Startbildschirm, `loadLogo()`) |
| `flutter/assets/icon.png` | App-Icon, abgerundetes grünes Quadrat (`loadIcon()`) |
| `flutter/assets/icon.svg` | App-Icon als Vektor (Fallback) |

### Betriebssystem-Icons

| Plattform | Datei(en) |
|-----------|-----------|
| Windows | `flutter/windows/runner/resources/app_icon.ico` (16–256) |
| macOS | `flutter/macos/Runner/AppIcon.icns`, `res/mac-icon.png` |
| Linux | `res/icon.png` (Master 1024), `res/icon.ico`, `res/32x32.png`, `res/64x64.png`, `res/128x128.png`, `res/128x128@2x.png` |
| Android | `mipmap-*/ic_launcher.png`, `_round`, `_foreground` (alle DPI) + `values/ic_launcher_background.xml` = `#09250F` |
| iOS | `AppIcon.appiconset/Icon-App-*.png` (opak, alle Größen) |

### Tray-Icons

| Datei | Verwendung |
|-------|-----------|
| `res/tray-icon.ico` | Windows-Tray (teal Symbol) |
| `res/mac-tray-dark-x2.png`, `res/mac-tray-light-x2.png` | macOS-Tray (monochrom) |

### Neu erzeugen

Die Assets werden mit Python (Pillow) generiert. Die Skripte liegen unter
`tools/branding/` und können nach einer Logo-Aktualisierung erneut ausgeführt werden:

```bash
cd tools/branding
python3 deploy_brand.py   # schreibt alle Asset-Dateien ins Repo
```

- Liegt das Original-Logo als `tools/branding/source-logo.png` vor, wird das
  Header-Logo daraus ausgeschnitten; **fehlt es, erzeugt das Skript automatisch
  einen gleichwertigen Banner** (Mark + „DariaTech / IT SYSTEMHAUS“) aus den
  Vektordaten.
- Das Skript erzeugt zusätzlich: `res/scalable.svg` (Linux-Pakete),
  `res/mac-tray-*.png` (macOS-Menüleiste, compile-time eingebettet),
  `libs/portable/src/res/label.png` (Windows-Portable-Installer) und die
  Android-`launch_image`-Splash-Bilder.

> Hinweis: `.gitignore` ignoriert `*png/*svg/*jpg` global, enthält aber
> **explizite Ausnahmen (`!…`) für alle Branding-Assets** – sie sind damit normal
> versioniert. Ohne diese Dateien schlagen die CI-Builds fehl (Android-Icons,
> `label.png`, `mac-tray-*.png` werden zur Compile-Zeit gebraucht).

Nach Asset-Änderungen neu bauen (siehe `build.py` / `flutter/README.md`).
