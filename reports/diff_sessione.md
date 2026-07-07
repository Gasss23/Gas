# Diff sessione — 2026-07-07 (migrazione Groq gpt-oss-120b: fetta unica)

> Si riscrive a ogni sessione. La storia completa sta in git.
> BASE sessione: `de9909c` (ultimo commit che ha toccato reports/handoff.md)

## File toccati nei commit di questa sessione (de9909c..HEAD)

Da `git diff --stat de9909c..HEAD`:

- `.claude/agents/memoria_revisore.md` — aggiunta lezione slash-namespace Groq vs OpenRouter (il formato `provider/model` con slash è convenzione OpenRouter, non Groq storica; validare sempre con chiamata live prima del deploy)
- `reports/roadmap.md` — (1) rimosso "review #43" non ancora avvenuta, stato PENDING; (2) nota deprecazione Groq aggiornata; (3) aggiunto item "Indagine latenza GAS" non urgente (segnalato dall'utente: ~5s più lento del solito)
- `reports/stato_progetto.md` — aggiornato header data, R-groq-slash APERTO PENDING, R-groq-dup aperto (deferito), nota TPM 8K burst = comportamento atteso

## File modificati in working tree (non committati, pending revisore)

- `brains/groq_brain.py` — `reasoning_effort: "low"` aggiunto al payload principale; usa `MODEL_GROQ` da `brains/model_ids.py`
- `brains/claude_brain.py` — `reasoning_effort: "low"` aggiunto al payload Groq fallback; usa `MODEL_GROQ`
- `brains/gemini_brain.py` — `reasoning_effort: "low"` aggiunto al payload Groq fallback; usa `MODEL_GROQ`
- `tests/test_unit_kernel.py` — model log string (`llama-3.3-70b` → `openai/gpt-oss-120b`) residuo da stash

## Note

- PUNTO 2 (round-trip live con GROQ_API_KEY) SALTATO: chiave non disponibile → file motore uncommitted
- Merge `refactor/model-ids-fonte-unica` (ore 14:41) ha cambiato struttura brain durante la sessione: risolti conflitti mantenendo upstream + aggiunta reasoning_effort
- `reports/verifica_fase25.md` — untracked, non toccato
