---
name: spanish-trainer
description: Build and maintain the Español Akademie — a single-file Spanish grammar learning web app (A1-C2). Each topic has a full teaching text (Lehrtext) followed by fixed, auto-checked writing exercises. Pure HTML/CSS/JS, no build, localStorage persistence, fully offline.
---

# Español Akademie Skill

## What this is
A single-file Spanish grammar academy (`index.html`) covering CEFR levels A1–C2. For each grammar topic it shows a complete teaching text and then a set of fixed, automatically checked writing exercises. Pure HTML/CSS/JS, no build step, no dependencies. Runs fully offline. State persists in `localStorage`.

The UI is in German (target audience: German speakers learning Spanish); all examples are in Spanish.

## Architecture
- **Single file**: Everything lives in `index.html` (HTML structure, `<style>`, `<script>`).
- **No external deps, fully offline**: no network calls at all (the old Anthropic API, speech recognition and TTS were removed).
- **State**: Global `S` object `{progress:{}}` persisted to `localStorage` under `espanol_trainer_v1` (migrates from legacy `espanol_v2`). The schema is backwards-compatible with the previous app, so existing learner progress is preserved.

## Design / look ("Akademie" style)
- Light cream theme (`--bg:#FBF4EB`), Playfair Display serif headlines, DM Sans body.
- Section headings have a rose dot before them and a fading underline rule.
- Numbered module cards (`01`, `02`, …) in a grid, each with a colored top-border accent (rotating palette `ACCENTS`), progress bar and status label ("Noch nicht begonnen" / "In Arbeit" / "Abgeschlossen").

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
- `<h3>` section heading (auto rose dot)
- `<p>`, `<ul>/<li>`, `<table>` (conjugation/form tables)
- `<span class="es">` Spanish inline text (rose, italic)
- `<div class="ex">` example box (teal), `<div class="tip">` tip box (orange)
- `<b>` to bold key forms

If a topic has no `ARTICLES[id]`, `buildFallbackArticle()` renders `grammar` + `example`. Currently all topics are covered, so the fallback is a safety net.

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
- Branch policy for this repo: commit and push to `main` only.
