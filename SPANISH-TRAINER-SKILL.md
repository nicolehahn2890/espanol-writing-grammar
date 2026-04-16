---
name: spanish-trainer
description: >
  Use this skill for EVERY request related to the Spanisch-Trainer App — a Spanish grammar learning app
  built in standalone HTML, deployed to GitHub Pages. Trigger on any mention of:
  "Spanisch Trainer", "Español Trainer", "Spanisch App", "Grammatik App", "espanol-trainer",
  "nicolehahn2890.github.io/espanol-trainer" (new app, not the old verb trainer), or any request
  to add/fix/extend the Spanish learning app. Also trigger when the user uploads an HTML file related to this app.
  Never skip this skill for Spanish trainer app work.
---

# Spanisch-Trainer — Skill

## Wer ist die Nutzerin?

Rexi — kein Coding-Hintergrund, kein Terminal. Ausschliesslich Claude.ai. Deutsch, Du-Anrede.
Deployment immer ueber GitHub Browser-Interface (Stift-Symbol, Strg+A, Inhalt ersetzen, Commit).
Spanisch-Level: C1

---

## Was ist die App?

- Geplante Live-URL: https://nicolehahn2890.github.io/espanol-trainer (NEUES Repo, nicht der alte Verb-Trainer!)
- Repository: github.com/nicolehahn2890/espanol-trainer (neu anzulegen)
- Technologie: Standalone HTML-Datei (kein Framework, kein Build-Schritt)
- Dateiname: index.html
- localStorage-Key: espanol_trainer_v1 — NIEMALS umbenennen!
- API: Anthropic Claude Haiku (claude-haiku-4-5-20251001) fuer Modus B (freies Schreiben)

---

## Design-System

Hintergrund: #0f0d14
Sekundaer-BG: #17141f, #1e1a2a, #252130
Primaerfarbe Pink: #F4A7C3 / #E879A0
Sekundaerfarbe Violet: #C4A8E8 / #9B6DD6
Akzent Mint: #A8E0CC / #5CC4A0
Akzent Blau: #7BAEE8 / #3A7BD5
Akzent Peach: #F9C9A8
Text: #f0eaf8 / #b8b0cc / #7a7090
Font: DM Sans + Playfair Display (Google Fonts)

Level-Farben:
  A1/A2: Mint (#5CC4A0)
  B1/B2: Blau (#7BAEE8 / #3A7BD5)
  C1: Violet (#C4A8E8)
  C2: Violet dunkel (#9B6DD6)

---

## App-Architektur

### State-Objekt S
```
S = {
  apiKey: '',         // Anthropic API Key, gespeichert in localStorage
  progress: {},       // { "B2_Subjuntivo": { done: 3, correct: 2 } }
  totalExercises: 0,
  totalCorrect: 0,
}
```

### Screens
- home: Level-Auswahl (A1-C2) + Stats
- topics: Themenliste fuer gewaehltes Level
- mode: Modus-Auswahl (A oder B) + Grammatik-Erklaerung
- exercise: Gefuehrte Uebungen (Modus A)
- free: Freies Schreiben mit KI (Modus B)
- results: Ergebnis-Anzeige nach Modus A
- settings: API-Key + Fortschritt zuruecksetzen

### Key-Format fuer Progress
```
topicId z.B. "B2_subjuntivo_imp"
S.progress[topicId] = { done: N, correct: N }
```

---

## Uebungs-Typen (Modus A)

```
mc:        Multiple Choice (4 Optionen, choices[], correct: Index)
fill:      Lueckentext (answer: String, flexible Vergleich mit Normalisierung)
translate: Uebersetzen DE→ES (answer: String)
```

Feedback immer mit: Richtig/Falsch-Anzeige + korrekte Antwort + grammatikalische Erklaerung (explain).

### Antwort-Normalisierung (fill/translate)
```javascript
const normalize = s => s.toLowerCase()
  .replace(/[áàä]/g,'a').replace(/[éèë]/g,'e')
  .replace(/[íìï]/g,'i').replace(/[óòö]/g,'o')
  .replace(/[úùü]/g,'u').replace(/ñ/g,'n')
  .replace(/[¡¿!?.,"']/g,'').trim();
```
Akzente werden also toleriert/ignoriert beim Vergleich.

---

## Grammatik-Themen (vollstaendige Liste)

### A1
- A1_presente: Presente de indicativo (ser/estar/tener/ir + regulaere Verben)
- A1_articulos: Articulos (el/la/los/las, un/una)
- A1_pronombres: Pronombres personales (yo/tu/el/ella...)
- A1_numeros: Numeros y fechas (Zahlen, Datum, Uhrzeit)
- A1_negacion: Negacion simple (no + Verb)

### A2
- A2_pasado: Preterito indefinido (abgeschlossene Vergangenheit)
- A2_imperfecto: Preterito imperfecto (Gewohnheiten/Beschreibungen)
- A2_adjetivos: Adjetivos calificativos (Stellung + Kongruenz)
- A2_gustar: Verbos como gustar (gustar/encantar/molestar)
- A2_preposiciones: Preposiciones basicas (a/de/en/con/por/para)

### B1
- B1_futuro: Futuro simple (-e/-as/-a...)
- B1_condicional: Condicional simple (wuerde...)
- B1_subjuntivo_pres: Subjuntivo presente (Wuensche/Zweifel/Emotionen)
- B1_imperativo: Imperativo afirmativo (Befehle)
- B1_ser_estar: Ser vs. Estar
- B1_perifrasis: Perifrasis verbales (estar+gerundio, ir a+inf...)

### B2
- B2_subjuntivo_imp: Subjuntivo imperfecto (-ra/-se Formen)
- B2_condicionales: Oraciones condicionales (Typ 1/2/3)
- B2_subjuntivo_perf: Subjuntivo perfecto (haya + Partizip)
- B2_imperativo_neg: Imperativo negativo (no + Subjuntivo)
- B2_relativos: Pronombres relativos (que/quien/el cual/cuyo)
- B2_adverbios: Adverbios y locuciones (-mente, sin embargo...)

### C1
- C1_subj_pluscuamp: Subjuntivo pluscuamperfecto (hubiera + Partizip)
- C1_voz_pasiva: Voz pasiva (ser+Partizip / se pasivo)
- C1_estilo_indirecto: Estilo indirecto (indirekte Rede mit Zeitverschiebung)
- C1_subjuntivo_conc: Subjuntivo en concesivas (aunque/a pesar de que)
- C1_gerundio: Gerundio avanzado (temporal/kausal/modal)
- C1_ser_estar_adv: Ser/Estar avanzado (Bedeutungsunterschiede)

### C2
- C2_perifrasis_adv: Perifrasis verbales avanzadas (llevar+gerundio...)
- C2_modalidad: Modalidad y matices (deber de vs. deber...)
- C2_discurso: Conectores del discurso (asimismo/no obstante...)
- C2_subjuntivo_fin: Subjuntivo en finales y temporales
- C2_lexicologia: Lexico avanzado y registro (Kollokationen/Idiome)

---

## Modus B — KI-Feedback

API-Aufruf:
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
    max_tokens: 800,
    system: systemPrompt,
    messages: [{ role: 'user', content: `Meine Antwort: ${text}` }],
  })
});
```

System-Prompt-Struktur fuer Feedback:
1. BEWERTUNG (1 Satz)
2. KORREKTUREN: Fehler → Korrektur (Emojis: ❌ / ✅)
3. ERKLAERUNG grammatikalisch
4. POSITIVES
5. VERBESSERTER TEXT

---

## WICHTIGE CODING-REGELN

1. localStorage-Key espanol_trainer_v1 NIE umbenennen
2. Keine Sonderzeichen in JS-Strings ausser Standard-Umlaute
3. Alle 3 Uebungstypen (mc/fill/translate) pro Thema nutzen
4. Antwort-Normalisierung immer verwenden (Akzente tolerieren)
5. Feedback immer mit explain-Text versehen
6. API-Key NIE hardcoden — immer aus S.apiKey lesen
7. anthropic-dangerous-direct-browser-access Header immer setzen (Browser-API-Call)
8. Bei Erweiterungen: Uebungen als Array im EXERCISES-Objekt, Key = topicId

---

## Ausstehende Verbesserungen (TODO)

- Mehr Uebungen pro Thema (Ziel: 8-10 pro Thema, alle 3 Typen)
- Fehlende Themen-Uebungen erganzen (aktuell haben nur manche Themen spezifische Uebungen)
- Mehr Free-Tasks pro Thema (Ziel: 4-5 pro Thema)
- Grammatik-Themen ueberpruefen und ggf. erganzen
- Evtl. Audio-Aussprache-Tipps
- Evtl. Vokabel-Modul

---

## Deployment

1. index.html herunterladen
2. github.com/nicolehahn2890/espanol-trainer > index.html > Stift-Symbol
   (oder neues Repo anlegen falls noch nicht vorhanden)
3. Strg+A > Entf > Strg+V > Commit changes
4. Repository Settings > Pages > Branch: main > Save
5. ~2 Min warten > https://nicolehahn2890.github.io/espanol-trainer/
