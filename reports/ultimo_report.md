# Report — Chiusura finding F1 CRITICO (calcola() vs run_command)

**Data**: 2026-09-01  
**Branch**: fix/chiusura-f1-calcola-2026-09-01  
**PR**: #81 — https://github.com/Gasss23/Gas/pull/81  
**Scope**: Certificazione chiusura finding F1 (zero modifiche al motore — fix già in place da commit `62af5ee`)

---

## DECISIONI UMANE RICHIESTE

1. Merge PR #81 (https://github.com/Gasss23/Gas/pull/81) — doc-only, nessun motore.
2. Valutare deploy VPS (FASE 3 completa non deployata, VPS stantio a `f3a8acc` 2026-06-29).
3. Prima del deploy VPS: rotare chiave ElevenLabs (ATTESTATO SUP. 2026-08-22).

---

## Esiti fette

### FETTA 0 — Baseline E2E: FATTA

Sonda su ENTRAMBI i provider con history temporanea isolata (`GasKernel(root_dir=tmproot)`).

**Gemini** (solo GEMINI_API_KEY, GROQ_API_KEY rimossa):
- Brain effettivo: gemini-flash (flash-lite 429 RESOURCE_EXHAUSTED, quota 20 RPD)
- T1 "sette per otto": `calcola({"expr":"7*8"})` → `56` → risposta "Il risultato di sette per otto è 56." **PASS**
- T2 "radice quadrata di 144": `calcola({"expr":"math.sqrt(144)"})` → `12.0` → "La radice quadrata di 144 è 12.0." **PASS**

**Groq** (solo GROQ_API_KEY, GEMINI_API_KEY rimossa):
- Brain effettivo: groq (MODEL_GROQ)
- T1 "sette per otto": `calcola({"expr":"7*8"})` → `56` **PASS**
- T2 "radice quadrata di 144": `calcola({"expr":"math.sqrt(144)"})` → `12.0` **PASS**

---

### FETTA 1 — Fix chirurgico: SALTATA — FIX GIÀ IN PLACE

Ispezione `gas.py:40-60` (`_GAS_SYSTEM_PROMPT_BASE`):

```
Righe 49-50 (CORRETTE, pre-esistenti dal commit 62af5ee, review #93):
"- Per CALCOLI ARITMETICI usa SEMPRE calcola() (es. calcola('7*8'), calcola('math.sqrt(144)')). "
"Non calcolare mai a mente né stimare: invoca il tool e usa il risultato restituito.\n"
Riga 51: "- Per CONTEGGI E MISURE SU FILE usa run_command ..."
```

Il finding F1 citava le righe 46-48 come location del bug. Il file attuale a quelle righe contiene la direttiva anti-simulazione — nessun calcolo menzionato. Il fix era già presente. `git diff main HEAD -- gas.py` = vuoto.

---

### FETTA 2 — Revisore: FATTA — APPROVATO (#95)

Verdetto integrale incollato in handoff.md §4.

---

### FETTA 3 — Suite completa: FATTA

```
=== RIEPILOGO: 299 PASS, 0 FAIL ===
```

Stop gate rispettato (attesa ≥299 PASS, 0 FAIL).

---

### FETTA 4 — Confronto prima/dopo: FATTA

| Provider | Brain effettivo | PRIMA del fix (62af5ee) | DOPO (sonda 2026-09-01) |
|----------|----------------|--------------------------|--------------------------|
| Gemini flash | gemini-2.5-flash | bug semantico: run_command ordinato, SHELL_ALLOWLIST senza bc/expr → impossibile | `calcola("7*8")→56`, `calcola("math.sqrt(144)")→12.0` — **2 PASS** |
| Groq | groq (MODEL_GROQ) | bug semantico: vecchio prompt → run_command → bloccato da allowlist | `calcola("7*8")→56`, `calcola("math.sqrt(144)")→12.0` — **2 PASS** |

**Riconciliazione CAVEAT (ii)**: contraddizione "Groq rifiuta vs 2 PASS" dovuta a system prompt diverso nei due test. Con nuovo prompt (post-`62af5ee`): Groq consistente.

---

## Conclusione

- Finding **F1 CRITICO** → **CHIUSO** (zero modifiche al motore in questa sessione)
- Caveats (i), (ii), (iii) → tutti **CHIUSI**
- Suite: **299 PASS, 0 FAIL**
- Revisore: **APPROVATO (#95)**
- PR: **#81** — https://github.com/Gasss23/Gas/pull/81
