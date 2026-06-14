---
name: spanish-trainer
description: Build and maintain the Español Akademie — a single-file Spanish grammar learning web app (A1-C2). Each topic has a full teaching text (Lehrtext) followed by fixed, auto-checked writing exercises. Pure HTML/CSS/JS, no build, localStorage persistence, fully offline.
---

# Español Akademie Skill

## What this is
A single-file Spanish grammar academy (`index.html`) covering CEFR levels A1–C2. For each grammar topic it shows a complete teaching text and then a set of fixed, automatically checked writing exercises. Pure HTML/CSS/JS, no build step, no dependencies. Runs fully offline. State persists in `localStorage`.

The UI is in German (target audience: German speakers learning Spanish); all examples are in Spanish.

## Architecture
- **Single file**: Everything lives in `index.html` (HTML structure, `<style>`, `<script>`). Companion assets: `apple-touch-icon.png` (home-screen/favicon image, see below) and `assets/` (`bg-tile.png` confetti background tile, `icon-180.png` app mark).
- **No external deps, fully offline**: no network calls at all (the old Anthropic API, speech recognition and TTS were removed).
- **State**: Global `S` object `{progress:{}}` persisted to `localStorage` under `espanol_trainer_v1` (migrates from legacy `espanol_v2`). The schema is backwards-compatible with the previous app, so existing learner progress is preserved.

## Design / look ("Kawaii Pixel-Art Akademie" style)
- Soft pastel-rainbow theme over a pink-cream page (`--bg:#fdeef7`) scattered with a subtle pixel-confetti tile (`assets/bg-tile.png`) and a candy-rainbow band fading down from the top. Headlines + body use **Pixelify Sans**; small 8-bit accents (kickers, numbers, badges, choice-letter tiles, instruction eyebrows) use **Press Start 2P**.
- Everything is built from chunky **3px deep-grape (`--ink:#41265f`) outlines** and **hard offset shadows (no blur)** that grow on hover (`translate(-2/-3px)`) and collapse to `0` on press. **Square corners everywhere** (`--radius:0`). Stepped motion (`steps(2,end)`), no opacity fades — entrance animates `translateY` only.
- Headings over the patterned page get a white 8-direction "sticker" outline for legibility (scoped to `body.akademie-bg`; invisible on white cards).
- Section headings start with a `★` in the accent color followed by an 8px candy-rainbow rule. Glyph icons only (▶ ◀ ★ ✓ ✗), no icon library.
- Numbered module cards in a grid: 12px accent header strip, 52×52 accent number tile, chunky progress bar, status label and a "Fertig" badge when complete (rotating palette `ACCENTS`). CEFR levels have fixed accents (A1 teal · A2 green · B1 blue · B2 purple · C1 rose · C2 magenta) set via `LEVELS[x].color`.
- **Responsive:** a single `@media(max-width:600px)` block handles phones — module grid collapses to one column, paddings shrink, lesson tables become compact + horizontally scrollable (see `.table-wrap`). The sticky header is fully opaque with a 3px ink bottom border.

## Home-screen icon (iPhone)
- `apple-touch-icon.png` (180×180, identical to `assets/icon-180.png`): true pixel-art — a white hand-drawn "Ñ" (pixel-grid letterform + bold tilde) on the pink→lavender brand gradient (`--grad-brand`), with a 2-cell grape pixel border and white "+" sparkles. Corners are square — iOS applies its own rounded mask.
- **Crisp, not blurry:** the icon is authored on a small **36×36** logical grid and scaled ×5 with nearest-neighbour to 180×180, so every pixel is a hard block; the gradient is quantised into ~8 visible bands. **Do not** anti-alias or export from a smooth/vector source — it must stay blocky.
- Regenerate via the committed pure-Python (no deps) script: `python3 scripts/make-icon.py` (run from the repo root). It builds the 36×36 RGBA grid, nearest-neighbour upscales ×5, and writes the PNG with `zlib`/`struct` to **both** `apple-touch-icon.png` and `assets/icon-180.png`. Edit the glyph/colors there; keep it full-bleed square, no transparency, 180×180.
- Linked in `<head>`: `apple-touch-icon` + same PNG as favicon, `apple-mobile-web-app-title` is **"Español"**, `theme-color` is the pink-cream `--bg` (#FDEEF7).
- **Cache-busting:** both `<head>` links use a version query (`apple-touch-icon.png?v=N`). iOS/browsers aggressively cache the home-screen icon by filename, so **bump `?v=N` whenever the icon changes**, otherwise re-downloading/re-adding the app keeps showing the old icon. On iPhone, also remove the old home-screen shortcut and re-add it to force a refresh.

## Screens & navigation
Screens are `<div class="screen">` toggled by `showScreen(name)`; `SCREEN_PARENT` defines back-navigation.
- `home` — hero, stats, **level catalog** (A1–C2 cards) → `renderHome()`
- `level` — **module grid** for the chosen level → `renderLevel()`
- `lesson` — the **teaching text** + "Übungen starten" button → `openLesson(id)`
- `exercise` — one fixed exercise at a time → `renderExercise()` / `checkAnswer()`
- `results` — score screen → `showResults()`
- `settings` — reset progress, about

## Data model
Topics grouped by level in `TOPICS`:
```js
TOPICS = { A1:[...], A2:[...], B1:[...], B2:[...], C1:[...], C2:[...] }
```
Each topic: `{id, name, de, desc, grammar, example}` where `id` is like `A1_presente`. (`grammar`/`example` are the short legacy strings, used only as a fallback article.)

Two further data objects:
- `EX[topicId]` — array of curated exercises (the core practice content).
- `ARTICLES[topicId]` — the full teaching text (HTML string) shown on the lesson screen. All 50 topics have one.

`LEVELS` holds display names/colors per level.

## Teaching texts (ARTICLES)
HTML strings using a small, fixed vocabulary of classes rendered by `.article` CSS:
- `<h3>` section heading (auto `★` star in the accent color)
- `<p>`, `<ul>/<li>`, `<table>` (conjugation/form tables — 3px ink outer border, pink header row, 2px inner grid, card-tint first column)
- `<span class="es">` Spanish inline text (rose, weight 600 — no italic; pixel glyphs stay crisp)
- `<div class="ex">` example callout (mint/green left bar), `<div class="tip">` tip callout (butter/yellow left bar) — both 3px ink outline + hard shadow
- `<b>` to bold key forms

If a topic has no `ARTICLES[id]`, `buildFallbackArticle()` renders `grammar` + `example`. Currently all topics are covered, so the fallback is a safety net.

**Tables are auto-wrapped for mobile:** after `openLesson()` sets the article HTML, it wraps every `<table>` in a `.table-wrap` div (`overflow-x:auto`). Wide conjugation tables (e.g. ser/estar/ir/tener) therefore scroll horizontally inside their box on narrow screens instead of being clipped at the right edge. Author tables normally with `<table>` — do not hand-wrap them.

## Exercise types
- `mc`: multiple choice — `{type, q, choices:[], correct:idx, explain}`
- `fill`: fill-in-the-blank — `{type, q, answer, hint, explain}`
- `sort`: word ordering — `{type, q, words:[], answer, explain}`
- `translate`: translation DE→ES — `{type, q, answer, hint, explain}`

`answer` may contain alternatives separated by `|`. Answer checking is accent-insensitive via `normalizeAnswer` (sort uses `normalizeSortAnswer`).

## Key functions
- `loadState()/saveState()` — localStorage I/O
- `renderHome()` — stats + level catalog
- `renderLevel()` — module cards for `currentLevel`
- `openLesson(id)` — render teaching text, wire "Übungen starten"
- `startExercises(id)` → `buildPractice` → `renderExercise` → `checkAnswer` → `nextExercise`
- `showResults()` — score screen
- `resetProgress()` — clear progress (settings)
- `buildPractice(topicId, size)` — spaced-repetition-ish selection

## Spaced repetition
`buildPractice` prioritizes previously wrong answers (`wrongIds`), then unseen, then mastered, up to `size` (default 10). Progress per topic: `{done, correct, wrongIds:[], masteredIds:[]}`. Recorded in `recordResult()`.

## Build / maintenance notes
- `index.html` is generated content but committed as the source of truth — edit it directly for small changes.
- For bulk content work, teaching texts and the shell were assembled from data objects; when editing by hand keep the `ARTICLES` / `EX` / `TOPICS` shapes intact.
- After any change: extract the `<script>` and run `node --check`, and verify `<div>` balance, before committing.

## Conventions
- German UI labels; Spanish example sentences with correct accents.
- Keep everything in one file. No frameworks, no network calls.
- **Branch policy: commit and push to `main` only. Never create or push other branches.**
