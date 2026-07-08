# REPORT — 2026-07-08 — Migrazione Groq gpt-oss-120b: COMPLETATA (4/4 punti)

## DECISIONI UMANE RICHIESTE

Nessuna. Task completato al 100%.

---

## Esito per punto

### PUNTO 1 — `reasoning_effort: "low"` nei 3 brain
`FATTA` (sessione precedente 2026-07-07) — aggiunto a tutti e tre i payload Groq:
- `brains/groq_brain.py`: payload principale `chat()`
- `brains/claude_brain.py`: payload Groq fallback (rung 2)
- `brains/gemini_brain.py`: payload Groq fallback (rung 3)

### PUNTO 2 — Round-trip reale con tool call
`FATTA` — Eseguita chiamata live all'endpoint Groq con payload identico a `groq_brain.py`:

**(a) MODELLO ACCETTATO:** `openai/gpt-oss-120b`

**(b) TOOL_CALLS parsate:**
```json
[
  {
    "id": "fc_f43247c6-7062-41ed-ad13-31399c0c7cb7",
    "type": "function",
    "function": {
      "name": "calcola",
      "arguments": "{\"espressione\":\"17 * 43\"}"
    }
  }
]
```

**(c) CONTENT (no reasoning):** `''` (vuoto — corretto: il modello ha usato la tool call)
**[reasoning presente nel response ma escluso: len=25, reasoning_tokens=7]**

**(d) LATENZA:** 1138 ms

Usage: `prompt_tokens=151, completion_tokens=39, reasoning_tokens=7`

**Conclusione:** il formato slash-namespace `openai/gpt-oss-120b` è accettato dall'endpoint Groq `/v1/chat/completions`, il parametro `reasoning_effort: "low"` funziona (7 reasoning_tokens, non 0), le tool calls sono parsate correttamente.

### PUNTO 3 — Gate revisore (review #44)

**VERDETTO: APPROVATO CON RISERVE**

Riserve (non bloccanti):
- **A** — `reasoning_effort` hardcoded: se `GAS_MODEL_GROQ` sovrascrive con un modello non-reasoning, il rung torna un 4xx silente (fail-safe regge, diagnostica opaca). Suggerito commento inline.
- **B** — Prezzi $0.15/$0.60 non verificabili staticamente: confrontare con pricing page Groq al deploy VPS.
- **C** — T36c usa stringa letterale invece della costante importata: aggiornamento manuale necessario alla prossima migrazione. Cosmetica.

Memoria revisore aggiornata (`.claude/agents/memoria_revisore.md`): parametri capability-vincolati hardcoded con modello env-overridabile → pattern riserva ricorrente.

### PUNTO 4 — Commit motore + report
`FATTA` — Commit `f028e51` su `main`:
```
feat(groq): migra a openai/gpt-oss-120b con reasoning_effort: low
```
7 file modificati: `brains/model_ids.py`, `brains/groq_brain.py`, `brains/claude_brain.py`, `brains/gemini_brain.py`, `gas.py`, `tests/test_unit_kernel.py`, `.claude/agents/memoria_revisore.md`.

---

## Finding chiusi da questa sessione

- ✅ **R-groq-slash** — formato slash-namespace `openai/gpt-oss-120b` accettato: STATUS 200, tool_calls OK, latenza 1138ms
- ✅ **R-groq-dup** — fonte unica già rispettata via `brains/model_ids.py` (confermato da revisore #44, nessuna modifica necessaria)

## Note

- Riserve review #44 tracciate in `stato_progetto.md` (non bloccanti, da valutare al deploy VPS).
- `reports/verifica_fase25.md` rimasto untracked — non parte di questo task.
