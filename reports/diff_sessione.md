# Diff sessione — 2026-07-07 (migrazione Groq gpt-oss-120b: fetta unica)

> Si riscrive a ogni sessione. La storia completa sta in git.
> BASE sessione: `3f542c1` (ultimo commit che ha toccato handoff.md)

## File con modifiche committate questa sessione (3f542c1..HEAD)

Solo l'auto-commit `5b3c4c0` della sessione precedente rientra nel range:
- `reports/roadmap.md` — auto-commit sessione precedente (non questa sessione)
- `reports/stato_progetto.md` — auto-commit sessione precedente (non questa sessione)

## File con modifiche uncommitted questa sessione (working tree vs HEAD)

- `brains/groq_brain.py` — aggiunto `"reasoning_effort": "low"` al payload Groq principale (PUNTO 1)
- `brains/claude_brain.py` — aggiunto `"reasoning_effort": "low"` al payload Groq fallback + aggiornato messaggio console (PUNTO 1; model rename era già nel diff pre-esistente)
- `brains/gemini_brain.py` — aggiunto `"reasoning_effort": "low"` al payload Groq fallback (PUNTO 1; model rename era già nel diff pre-esistente)
- `gas.py` — `GROQ_MODEL` e tabella prezzi (pre-esistente dal branch `refactor/model-ids-fonte-unica`, mergiato oggi; non toccato questa sessione)
- `tests/test_unit_kernel.py` — nome modello groq in log aggiornato (pre-esistente, non toccato questa sessione)
- `.claude/agents/memoria_revisore.md` — aggiunta lezione (pre-esistente, staged prima di questa sessione)
- `reports/roadmap.md` — rimosso "review #43" / "CHIUSA", stato reale "PENDING" (PUNTO 3)
- `reports/stato_progetto.md` — rimosso "review #43", aggiornato header, R-groq-slash PENDING, R-groq-dup aperto, nota TPM (PUNTI 3+4)

## Note

- PUNTO 2 (round-trip live) SALTATO: GROQ_API_KEY non disponibile → nessuna chiamata live eseguita
- File motore (`brains/`, `gas.py`, `tests/`) uncommitted: attesa round-trip + gate revisore
- `reports/verifica_fase25.md` — untracked, non toccato in questa sessione
