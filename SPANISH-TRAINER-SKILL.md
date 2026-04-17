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
- API: Anthropic Claude Haiku (`claude-haiku-4-5-20251001`) für Modus B (freies Schreiben)

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
  progress: {},    // { "B2_subjuntivo_imp": { done: 3, correct: 2 } }
}
```

### Screens
| Screen | Beschreibung |
|--------|-------------|
| home | Level-Auswahl (A1–C2) + Stats |
| topics | Themenliste für gewähltes Level |
| mode | Modus-Auswahl + Grammatik-Erklärung |
| exercise | Geführte Übungen (Modus A) |
| free | Freies Schreiben mit KI (Modus B) |
| results | Ergebnis nach Modus A |
| settings | API-Key + Fortschritt zurücksetzen |

### Daten-Objekte

```javascript
const TOPICS = { A1:[...], A2:[...], B1:[...], B2:[...], C1:[...], C2:[...] }
// Jedes Topic: { id, name, de, desc, grammar, example }

const EX = { TOPIC_ID: [ {type:'mc'|'fill'|'translate'|'sort', ...} ] }
// 43 Themen mit je 10 kuratierten Übungen — ALLE vollständig, kein Fallback nötig

const FREE = { TOPIC_ID: [ {task:'...', hint:'...'} ] }
// 43 Themen mit je 4 Schreibaufgaben — ALLE vollständig
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

## Grammatik-Themen (vollständige aktuelle Liste — 43 Themen)

### A1 (5 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| A1_presente | Presente de indicativo | Präsens |
| A1_articulos | Artículos | Artikel |
| A1_ser_estar | Ser vs. Estar (básico) | Sein – Grundlagen |
| A1_pronombres | Pronombres personales | Personalpronomen |
| A1_negacion | Negación y preguntas | Verneinung & Fragen |

### A2 (7 Themen)
| ID | Spanisch | Deutsch |
|----|----------|---------|
| A2_indefinido | Pretérito Indefinido | Einfache Vergangenheit |
| A2_imperfecto | Pretérito Imperfecto | Unvollendete Vergangenheit |
| A2_perf_simple | Pretérito Perfecto | Perfekt |
| A2_gustar | Verbos tipo gustar | Verben wie gustar |
| A2_adjetivos | Adjetivos y comparativos | Adjektive & Komparativ |
| A2_preposiciones | Preposiciones básicas | Grundlegende Präpositionen |
| A2_reflexivos | Verbos reflexivos | Reflexivverben |

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

Alle 43 Themen haben kuratierte EX- und FREE-Einträge. Der Fallback wird nur für neu hinzugefügte Themen benötigt, bis deren Inhalte ergänzt werden:

`createFallbackExercises()`: Generiert sort/fill/mc/translate aus `topic.example` und `topic.grammar`, max. 8 Aufgaben.

`createFallbackFreeTasks()`: 4 generische Schreibaufgaben zum Thema.

---

## Wichtige Coding-Regeln

1. `espanol_trainer_v1` als localStorage-Key NIE umbenennen
2. Alle 4 Übungstypen (mc/fill/translate/sort) pro Thema verwenden
3. Antwort-Normalisierung (`normalizeAnswer`) immer verwenden
4. Jeden Übungstyp mit `explain`-Text versehen
5. API-Key NIE hardcoden — immer aus `S.apiKey` lesen
6. `anthropic-dangerous-direct-browser-access` Header immer setzen
7. Neue Themen: sowohl in `TOPICS` als auch in `EX` und `FREE` eintragen
8. Keine doppelten Schlüssel in `EX` oder `FREE` — JavaScript nimmt stillschweigend den letzten!
9. Strings immer als UTF-8 schreiben — keine manuellen Escape-Sequenzen für Umlaute

---

## Deployment

Direkt auf `main` pushen → GitHub Pages aktualisiert sich automatisch (~2 Min).

Live-URL: https://nicolehahn2890.github.io/espanol-writing-grammar
