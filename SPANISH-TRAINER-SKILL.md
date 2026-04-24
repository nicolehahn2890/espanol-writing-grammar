---
name: spanish-trainer
description: >
  Use this skill for EVERY request related to the Spanisch-Trainer App — a Spanish grammar learning app
  built in standalone HTML, deployed to GitHub Pages. Trigger on any mention of:
  "Spanisch Trainer", "Español Trainer", "Spanisch App", "Grammatik App", "espanol-writing-grammar",
  "nicolehahn2890/espanol-writing-grammar", or any request to add/fix/extend the Spanish learning app.
  Also trigger when the user uploads an HTML file related to this app.
  Never skip this skill for Spanish trainer app work.
---

# Spanisch-Trainer — Skill

## Wer ist die Nutzerin?

Nicole — kein Coding-Hintergrund, kein Terminal. Ausschliesslich Claude.ai / Claude Code. Deutsch, Du-Anrede.
Deployment über GitHub (Branch pushen → Pull Request → merge in main → GitHub Pages).
Spanisch-Level: C1

---

## Was ist die App?

- Live-URL: https://nicolehahn2890.github.io/espanol-writing-grammar
- Repository: github.com/nicolehahn2890/espanol-writing-grammar
- Technologie: Standalone HTML-Datei (kein Framework, kein Build-Schritt)
- Dateiname: index.html
- localStorage-Key: `espanol_trainer_v1` — **NIEMALS umbenennen!**
- API: Anthropic Claude Haiku (`claude-haiku-4-5-20251001`) für Modus B (freies Schreiben) und Modus C (Hablar)
- Browser-native `SpeechSynthesis` API für TTS der Grammatik-Beispielsätze (kein API-Call, kostenlos)

---

## Design-System

```
Hintergrund:       #0f0d14
Sekundaer-BG:      #17141f / #1e1a2a / #252130
Pink:              #F4A7C3 / #E879A0
Violet:            #C4A8E8 / #9B6DD6
Mint:              #A8E0CC / #5CC4A0
Blau:              #7BAEE8 / #3A7BD5
Peach:             #F9C9A8
Text:              #f0eaf8 / #b8b0cc / #7a7090
Font:              DM Sans + Playfair Display (Google Fonts)
```

Level-Farben:
- A1/A2: Mint (#5CC4A0)
- B1/B2: Blau (#7BAEE8 / #3A7BD5)
- C1: Violet (#C4A8E8)
- C2: Violet dunkel (#9B6DD6)

---

## App-Architektur

### State-Objekt S
```javascript
S = {
  apiKey: '',      // Anthropic API Key, gespeichert in localStorage
  progress: {},    // { "B2_subjuntivo_imp": { done, correct, wrongIds:[], masteredIds:[] } }
}
```

Pro Thema:
- `done` / `correct`: Attempt-Counter (alle Runden)
- `wrongIds`: Index-Liste der Aufgaben, deren **letzte** Antwort falsch war → werden in nächster Modus-A-Runde priorisiert
- `masteredIds`: Index-Liste der Aufgaben, deren **letzte** Antwort richtig war → gelten als gemeistert

Richtige Antwort verschiebt den Exercise-Index `wrongIds → masteredIds`, falsche Antwort umgekehrt. So bleibt Mastery immer aktuell und falsche Aufgaben kommen garantiert wieder.

### Screens
| Screen | Beschreibung |
|--------|-------------|
| home | Level-Auswahl (A1–C2) + Stats |
| topics | Themenliste für gewähltes Level (inkl. Mastery-Balken pro Thema) |
| mode | Modus-Auswahl + Grammatik-Erklärung (3 Modi) + TTS-Button + Mastery-Balken |
| exercise | Geführte Übungen (Modus A) |
| free | Freies Schreiben mit KI (Modus B) |
| speech | Freies Sprechen mit KI (Modus C – Web Speech API) |
| results | Ergebnis nach Modus A |
| settings | API-Key + Fortschritt zurücksetzen |

### Daten-Objekte

```javascript
const TOPICS = { A1:[...], A2:[...], B1:[...], B2:[...], C1:[...], C2:[...] }
// Jedes Topic: { id, name, de, desc, grammar, example }

const EX = { TOPIC_ID: [ {type:'mc'|'fill'|'translate'|'sort', ...} ] }
// 50 Themen mit je 10 kuratierten Übungen — ALLE vollständig, kein Fallback nötig

const FREE = { TOPIC_ID: [ {task:'...', hint:'...'} ] }
// 50 Themen mit je 4 Schreibaufgaben — ALLE vollständig
```

---

## Übungs-Typen (Modus A — EX-Objekt)

```javascript
// Multiple Choice
{ type:'mc', q:'Frage', choices:['A','B','C','D'], correct:0, explain:'...' }

// Lückentext
{ type:'fill', q:'Frage', answer:'Antwort', hint:'...', explain:'...' }

// Übersetzen DE→ES
{ type:'translate', q:'Übersetze: "..."', answer:'...', hint:'...', explain:'...' }

// Satz umstellen
{ type:'sort', q:'Stelle zusammen:', words:['word1','word2',...], answer:'word1 word2 ...', explain:'...' }
```

Feedback immer mit: Richtig/Falsch + korrekte Antwort + `explain`-Text.

### Auswahl der 10 Aufgaben pro Runde (`buildPractice`)

`startModeA` / `retryExercises` rufen **nicht** mehr direkt `getExercises` auf, sondern `buildPractice(topicId, 10)`. Die Queue wird so gebaut:

1. **Priorität 1** — bis zu `⌈size/2⌉` Aufgaben aus `wrongIds` (zufällig)
2. **Priorität 2** — ungesehene Aufgaben (weder in `wrongIds` noch `masteredIds`)
3. **Priorität 3** — gemeisterte Aufgaben (zum Auffüllen wenn alles gemeistert)
4. Fallback — zufällige Aufgaben, falls Topic < 10 Übungen hat

`getExercises(id)` taggt jede Aufgabe mit `_idx` (stabiler Index in `EX[id]`). Dieser Index ist der Primärschlüssel für `wrongIds`/`masteredIds`.

### Fortschritts-Anzeige pro Thema

`getTopicStats(topicId)` liefert `{total, mastered, wrong, pct, done, correct}`. Zwei Stellen rendern das:

- **Themenliste** (`renderTopics`): Mini-Balken + `X/Y gemeistert` + optional `🔁 N` Badge
- **Modus-Screen** (`selectTopic`): gleicher Balken zentral über den Modus-Karten, mit Hinweis `🔁 N Aufgaben kommen wieder` wenn `wrongIds.length > 0`

Farblogik: Balken mint-grün wenn keine Wiederholungen anstehen, peach→pink sobald `wrong > 0`. `topic-dot` wird nur grün bei `mastered >= total`.

### Antwort-Normalisierung (fill/translate)
```javascript
function normalizeAnswer(s) {
  return (s||'').toLowerCase()
    .replace(/[áàä]/g,'a').replace(/[éèë]/g,'e')
    .replace(/[íìï]/g,'i').replace(/[óòö]/g,'o')
    .replace(/[úùü]/g,'u').replace(/ñ/g,'n')
    .replace(/[¡¿!?.,"']/g,'').replace(/\s+/g,' ').trim();
}
```
Akzente werden beim Vergleich toleriert.

---

## Grammatik-Themen (vollständige aktuelle Liste — 50 Themen)

### A1 (10 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| A1_presente | Presente de indicativo | Präsens |
| A1_articulos | Artículos | Artikel |
| A1_ser_estar | Ser vs. Estar (básico) | Sein – Grundlagen |
| A1_pronombres | Pronombres personales | Personalpronomen |
| A1_negacion | Negación y preguntas | Verneinung & Fragen |
| A1_numeros | Números | Zahlen 0–100 |
| A1_hora | La hora | Uhrzeit |
| A1_diasmeses | Días y meses | Wochentage & Monate |
| A1_posesivos | Posesivos | Possessivpronomen |
| A1_demonstrativa | Demostrativos | Demonstrativpronomen |

### A2 (9 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| A2_indefinido | Pretérito Indefinido | Einfache Vergangenheit |
| A2_imperfecto | Pretérito Imperfecto | Unvollendete Vergangenheit |
| A2_perf_simple | Pretérito Perfecto | Perfekt |
| A2_gustar | Verbos tipo gustar | Verben wie gustar |
| A2_adjetivos | Adjetivos y comparativos | Adjektive & Komparativ |
| A2_preposiciones | Preposiciones básicas | Grundlegende Präpositionen |
| A2_reflexivos | Verbos reflexivos | Reflexivverben |
| A2_pronombres_obj | Pronombres de objeto directo | Direkte Objektpronomen lo/la/los/las |
| A2_ir_a | Ir a + infinitivo | Analytisches Futur – Pläne & nahe Zukunft |

### B1 (8 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| B1_pluscuamperfecto | Pretérito Pluscuamperfecto | Plusquamperfekt |
| B1_futuro | Futuro simple | Zukunft einfach |
| B1_condicional | Condicional simple | Konditional |
| B1_subjuntivo_pres | Subjuntivo presente | Konjunktiv Präsens |
| B1_imperativo | Imperativo afirmativo y negativo | Imperativ |
| B1_ser_estar_adv | Ser/Estar cambios semánticos | Ser/Estar Bedeutungsunterschiede |
| B1_perifrasis | Perífrasis verbales | Verbale Umschreibungen |
| B1_indef_vs_imperf | Indefinido vs. Imperfecto | Einfache vs. unvollendete Vergangenheit |

### B2 (9 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| B2_futuro_perf | Futuro perfecto | Futur II |
| B2_cond_perf | Condicional perfecto | Konditional Perfekt |
| B2_subjuntivo_imp | Subjuntivo imperfecto | Konjunktiv Imperfekt |
| B2_subjuntivo_perf | Subjuntivo perfecto | Konjunktiv Perfekt |
| B2_condicionales | Oraciones condicionales | Konditionalsätze (Typ 1–3) |
| B2_imperativo_pron | Imperativo con pronombres | Imperativ mit Pronomen |
| B2_relativos | Pronombres relativos | Relativpronomen |
| B2_concesivas | Oraciones concesivas | Konzessivsätze |
| B2_pasiva_refleja | Pasiva refleja y pasiva con ser | Passiv – se vende / fue construido |

### C1 (7 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| C1_subj_pluscuamp | Subjuntivo pluscuamperfecto | Konjunktiv Plusquamperfekt |
| C1_voz_pasiva | Voz pasiva | Passiv |
| C1_estilo_indirecto | Estilo indirecto | Indirekte Rede |
| C1_gerundio | Gerundio avanzado | Gerundium fortgeschritten |
| C1_finales_temporales | Finales y temporales | Final- & Temporalsätze |
| C1_ser_estar_full | Ser/Estar lista completa | Ser/Estar vollständige Liste |
| C1_subj_sustantivas | Subjuntivo en oraciones sustantivas | Konjunktiv in Substantivsätzen |

### C2 (7 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| C2_perifrasis_adv | Perífrasis verbales avanzadas | Fortgeschrittene Verbumschreibungen |
| C2_modalidad | Modalidad epistémica y deóntica | Modalität |
| C2_conectores | Conectores del discurso | Diskurskonnektoren |
| C2_subj_complejo | Subjuntivo en construcciones complejas | Konjunktiv komplex |
| C2_registro | Registro y léxico avanzado | Register & Wortschatz |
| C2_nominalizacion | Nominalización | Nominalisierung |
| C2_inversion_sintactica | Inversión sintáctica y topicalización | Syntaktische Inversion & Topikalisierung |

---

## Modus C — Sprechen mit KI-Feedback

Nutzt die Browser-native **Web Speech API** (`SpeechRecognition` / `webkitSpeechRecognition`) mit `lang:'es-ES'`, `continuous:true`, `interimResults:true`. Browser-Support: Chrome/Edge/Safari vollständig, Firefox eingeschränkt. Bei fehlender Unterstützung zeigt die App einen Hinweis und das Transkript-Feld lässt sich manuell befüllen.

Workflow:
1. Nutzerin klickt Mic-Button → `toggleRecording()` startet Aufnahme mit rotem Pulse
2. Browser transkribiert live in das `speech-transcript` Textarea (editierbar)
3. Nochmaliger Klick auf Mic stoppt — oder Klick auf "Feedback erhalten"
4. Transkript geht an Claude mit speziellem Prompt (Transkriptionsartefakte ignorieren, Aussprache-Tipps)
5. Feedback erscheint im selben Format wie Modus B

Wiederverwendet die `FREE`-Tasks (jedes Thema hat 4 Schreibimpulse die auch als Sprechimpulse funktionieren).

---

## TTS — Grammatik-Beispiele anhören

Auf dem Modus-Screen steht neben dem spanischen Beispielsatz (im `grammar-box`) ein runder 🔊-Button, der die Browser-native `window.speechSynthesis` API mit `lang:'es-ES'`, `rate:0.95` nutzt. Kein API-Call, keine Kosten.

Helper in `index.html`:
- `ttsSupported()` — prüft `'speechSynthesis' in window`
- `pickSpanishVoice()` — wählt erste `es-*`-Stimme aus `getVoices()`
- `speakSpanish(text, btn)` — cancelt laufende Wiedergabe, toggelt bei erneutem Klick, setzt `.speaking` CSS-Klasse (mint-Pulse)
- `stopSpeaking()` — wird in `showScreen()` bei jedem Screen-Wechsel ≠ mode aufgerufen, damit keine Stimme weiterläuft

Wenn `ttsSupported()` `false` liefert, wird der Button versteckt (Firefox ohne Spanish-Voice Fallback: Browser rendert mit Default-Stimme, was akzeptabel ist).

---

## Modus B — KI-Feedback

```javascript
fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': S.apiKey,
    'anthropic-version': '2023-06-01',
    'anthropic-dangerous-direct-browser-access': 'true',
  },
  body: JSON.stringify({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 900,
    system: systemPrompt,
    messages: [{ role: 'user', content: `Meine Antwort: ${text}` }],
  })
});
```

System-Prompt-Struktur für Feedback:
1. **Bewertung** (1 Satz)
2. **Korrekturen**: ❌ Fehler → ✅ Korrektur (Erklärung)
3. **Haupterklärung** grammatikalisch (2–3 Sätze)
4. **Positives**
5. **Verbesserter Text**

---

## Fallback-Mechanismus

Alle 50 Themen haben kuratierte EX- und FREE-Einträge. Der Fallback wird nur für neu hinzugefügte Themen benötigt, bis deren Inhalte ergänzt werden:

`createFallbackExercises()`: Generiert sort/fill/mc/translate aus `topic.example` und `topic.grammar`, max. 8 Aufgaben.

`createFallbackFreeTasks()`: 4 generische Schreibaufgaben zum Thema.

---

## Wichtige Coding-Regeln

1. `espanol_trainer_v1` als localStorage-Key NIE umbenennen
2. Alle 4 Übungstypen (mc/fill/translate/sort) pro Thema verwenden
3. Antwort-Normalisierung (`normalizeAnswer`/`normalizeSortAnswer`) immer verwenden
4. Jeden Übungstyp mit `explain`-Text versehen
5. API-Key NIE hardcoden — immer aus `S.apiKey` lesen
6. `anthropic-dangerous-direct-browser-access` Header immer setzen
7. Neue Themen: sowohl in `TOPICS` als auch in `EX` und `FREE` eintragen
8. Keine doppelten Schlüssel in `EX` oder `FREE` — JavaScript nimmt stillschweigend den letzten!
9. Strings immer als UTF-8 schreiben — keine manuellen Escape-Sequenzen für Umlaute
10. KI-Feedback immer durch `renderMarkdownFeedback()` rendern (HTML-Escape gegen XSS)
11. API-Calls immer via `callAnthropicAPI()` Helper (einheitliche Fehlerbehandlung)
12. Navigation folgt `SCREEN_PARENT`-Map — keinen eigenen Stack aufbauen
13. Neue Felder in `S.progress[id]` defensiv prüfen (`Array.isArray(p.wrongIds)`) — alte localStorage-Einträge haben sie nicht
14. `buildPractice(topicId, size)` nutzen statt direktem `getExercises()` für Modus A — sonst fehlt die Wiederholungs-Logik
15. TTS nur über `speakSpanish()` auslösen, nie direkt `speechSynthesis.speak()` aufrufen (sonst fehlt Cancel/Toggle/Visual-State)

---

## Deployment

Direkt auf `main` pushen → GitHub Pages aktualisiert sich automatisch (~2 Min).

Live-URL: https://nicolehahn2890.github.io/espanol-writing-grammar
