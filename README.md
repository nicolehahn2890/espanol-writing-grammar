# Español Akademie

Eine Web-App zum Lernen der spanischen Grammatik von **A1 bis C2** — aufgebaut wie eine Akademie: Zu jedem Thema gibt es einen vollständigen **Lehrtext** und danach feste **Schreibübungen**, die automatisch geprüft werden.

> Reine HTML/CSS/JS-Datei, kein Build, keine Abhängigkeiten. Läuft **vollständig offline**. Der Fortschritt wird lokal im Browser gespeichert.

## Benutzung

`index.html` einfach im Browser öffnen — fertig. Nichts zu installieren.

## Aufbau

1. **Niveau wählen** (A1–C2) im Katalog auf der Startseite
2. **Modul wählen** — jede nummerierte Karte ist ein Grammatikthema mit Fortschritt und Status
3. **Lehrtext lesen** — Regeln, Konjugations-/Formtabellen, Beispiele und Stolperfallen-Tipps
4. **Übungen starten** — feste Schreibaufgaben, sofort ausgewertet
5. **Ergebnis** ansehen und bei Bedarf wiederholen

## Inhalt

- **50 Grammatikthemen** über alle sechs Niveaustufen (A1–C2)
- **Vollständige Lehrtexte** zu jedem Thema (alle Zeiten, Modi, Sonderregeln)
- **500 feste Schreibübungen** in vier Typen:
  - **Lückentext** — die richtige Form einsetzen
  - **Konjugation / Multiple Choice** — Formen erkennen und bilden
  - **Satz umstellen** — Wortstellung üben
  - **Übersetzung DE→ES** — gezielt die Zielgrammatik anwenden
- **Intelligente Wiederholung**: falsch beantwortete Aufgaben kommen bevorzugt wieder

## Technik

- `index.html` (Struktur, Styles und Logik) + `assets/` (`bg-tile.png` Konfetti-Hintergrund, `icon-180.png` App-Icon) und `apple-touch-icon.png`
- Kawaii-Pixel-Art-Design (Pixelify Sans + Press Start 2P, Pastell-Regenbogen, eckige Ecken, chunky 3px-Outlines & Hard-Offset-Schatten, gestufte Hover/Press-Animationen)
- Schriften via Google Fonts (Online); für komplett offline `@font-face` selbst hosten
- Fortschritt in `localStorage` (`espanol_trainer_v1`)
- Keine Netzwerkanfragen, kein API-Key, keine Tracking

## Entwicklung

Details zur Architektur, zum Datenmodell und zu den Konventionen stehen in [`SPANISH-TRAINER-SKILL.md`](./SPANISH-TRAINER-SKILL.md).

Nach Änderungen an `index.html`: das `<script>` extrahieren und mit `node --check` prüfen sowie die `<div>`-Balance kontrollieren, bevor committet wird.

Alle Änderungen gehen auf den `main`-Branch.
