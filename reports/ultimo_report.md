# Report: Chiusura finding F1 CRITICO — calcola() vs run_command

**Data**: 2026-09-01  
**Branch**: fix/chiusura-f1-calcola-2026-09-01  
**Scope**: Certificazione chiusura finding F1 (no modifica a gas.py — fix già in place)

---

## Risultato

Finding F1 CRITICO **CHIUSO**. Il fix era già presente dal commit `62af5ee` (review #93, 2026-08-29). Questa sessione ha certificato la chiusura con sonda E2E su entrambi i provider e suite completa.

---

## FETTA 0 — Baseline (sonda E2E prima della verifica)

### Verifica system prompt REALE (gas.py:40-60)

```
Linee 49-50 (CORRETTE, pre-esistenti):
"- Per CALCOLI ARITMETICI usa SEMPRE calcola() (es. calcola('7*8'), calcola('math.sqrt(144)')). "
"Non calcolare mai a mente né stimare: invoca il tool e usa il risultato restituito.\n"

Linee 51-57 (run_command delimitato solo ai file):
"- Per CONTEGGI E MISURE SU FILE usa run_command (es. wc -l file, grep -c pattern file). "
```

Il finding storico citava le righe 46-48 come luogo del bug. Quelle righe, nel file corrente, contengono invece la direttiva anti-simulazione (nessun calcolo menzionato). Il fix era già stato applicato da commit `62af5ee`.

### Sonda E2E Gemini (solo GEMINI_API_KEY, GROQ_API_KEY rimossa)

- **Brain effettivo**: gemini-flash (flash-lite 429 quota gratuita giornaliera)
- **T1 "sette per otto"**: tool=`calcola` args=`{"expr":"7*8"}` → result=`56` → risposta "Il risultato di sette per otto è 56." **PASS**
- **T2 "radice quadrata di 144"**: tool=`calcola` args=`{"expr":"math.sqrt(144)"}` → result=`12.0` → risposta "La radice quadrata di 144 è 12.0." **PASS**

### Sonda E2E Groq (solo GROQ_API_KEY, GEMINI_API_KEY rimossa)

- **Brain effettivo**: groq (MODEL_GROQ)
- **T1 "sette per otto"**: tool=`calcola` args=`{"expr":"7*8"}` → result=`56` → risposta "56" **PASS**
- **T2 "radice quadrata di 144"**: tool=`calcola` args=`{"expr":"math.sqrt(144)"}` → result=`12.0` → risposta "12.0" **PASS**

---

## FETTA 1 — Fix chirurgico

**Esito: NESSUN CAMBIO NECESSARIO**

Ispezione righe reali di `gas.py`:

| Riga | Contenuto |
|------|-----------|
| 49-50 | `"- Per CALCOLI ARITMETICI usa SEMPRE calcola() ..."` ← CORRETTO |
| 51-57 | `"- Per CONTEGGI E MISURE SU FILE usa run_command ..."` ← CORRETTO |

Il finding F1 riportava linee 46-48 come problematiche — quelle righe nel codice attuale contengono la direttiva anti-simulazione, non la direttiva calcoli. Il commit `62af5ee` aveva già risolto il bug semantico in review #93. Diff gas.py vs main: vuoto (zero byte).

---

## FETTA 2 — Revisore

**Review #95 — APPROVATO**

Revisore ha verificato:

**(a) Direttiva calcoli** `gas.py:49-50` — ordina `calcola()` per aritmetica; `run_command` limitato a misure su file (riga 51). Nessuna altra riga del prompt anomala.

**(b) SHELL_ALLOWLIST** `gas.py:992-996` — `frozenset({"ls","cat","head","tail","wc","grep","echo","pwd","date","stat","file","uniq","cut","tr","nl","diff","comm","true","false","basename","dirname","printf","seq","rev"})`. Nessun calcolatore. Nessuna violazione di sicurezza.

**(c) Guardrail §9** — `SHELL_ENV_SENSITIVE_MARKERS`, sandbox bwrap, costanti anti-DoS calcola() (`_CALCOLA_MAX_EXP=1000`, `_CALCOLA_MAX_DIGITS=500`, `_CALCOLA_MAX_FACTORIAL=1000`) intatte.

Rischio dichiarato dal revisore: comportamento provider alternativi (OpenRouter, Ollama) non verificato in questa sessione per assenza chiavi.

---

## FETTA 3 — Suite completa

```
=== RIEPILOGO: 299 PASS, 0 FAIL ===
```

**Stop gate rispettato** (attesa ≥299 PASS, 0 FAIL — confermato).

---

## FETTA 4 — Confronto prima/dopo

| Provider | Brain effettivo | Stato PRIMA del fix (`62af5ee`) | Stato DOPO (sonda 2026-09-01) |
|----------|----------------|----------------------------------|-------------------------------|
| Gemini (flash-lite) | gemini-2.5-flash-lite | System prompt ordinava run_command — SHELL_ALLOWLIST senza bc/expr → ordine IMPOSSIBILE (bug semantico) | flash-lite a 429 quota; fallback su flash |
| Gemini (flash) | gemini-2.5-flash | idem (bug semantico) | `calcola("7*8")→56`, `calcola("math.sqrt(144)")→12.0` — **2 PASS** |
| Groq | groq/openai/gpt-oss-120b | Vecchio prompt → run_command tentato → blocked by allowlist. Audit 2026-08-29: "Groq rifiuta 7×8" | `calcola("7*8")→56`, `calcola("math.sqrt(144)")→12.0` — **2 PASS** |

**Riconciliazione CAVEAT (ii)**: la contraddizione "Groq rifiuta vs Groq 2 PASS" era dovuta all'uso di due versioni del system prompt in test diversi. PR #78 (sonda/e2e-calcola-groq-2026-08-29, dopo `62af5ee`) e questa sonda usano il prompt corretto → Groq consistente.

---

## Conclusione

- Finding **F1 CRITICO** → **CHIUSO**
- Caveats (i), (ii), (iii) → tutti **CHIUSI**
- Nessuna modifica a `gas.py` in questa sessione (fix già presente da `62af5ee`)
- Suite: **299 PASS, 0 FAIL**
- Revisore: **APPROVATO (#95)**
