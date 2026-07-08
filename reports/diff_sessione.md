# DIFF SESSIONE — 2026-07-08

> Riscritto a ogni sessione. Storia completa: git log.

## File toccati (da `git diff --stat 62f4df2..HEAD`)

| File | Cosa è cambiato e perché |
|---|---|
| `brains/model_ids.py` | Default `MODEL_GROQ`: `llama-3.3-70b-versatile` → `openai/gpt-oss-120b` |
| `brains/groq_brain.py` | Aggiunto `reasoning_effort: "low"` al payload principale Groq |
| `brains/claude_brain.py` | Aggiunto `reasoning_effort: "low"` al payload Groq fallback (rung 2); aggiornata stringa log |
| `brains/gemini_brain.py` | Aggiunto `reasoning_effort: "low"` al payload Groq fallback (rung 3) |
| `gas.py` | Prezzi Groq aggiornati: `0.59/0.79` → `0.15/0.60` per MTok (nuova tabella gpt-oss-120b) |
| `tests/test_unit_kernel.py` | T36c: stringa model ID `"llama-3.3-70b"` → `"openai/gpt-oss-120b"` per allineamento |
| `.claude/agents/memoria_revisore.md` | Aggiunta lezione #44: parametri capability-vincolati hardcoded con modello env-overridabile |
| `reports/stato_progetto.md` | Finding R-groq-slash e R-groq-dup chiusi; review count → #44; data → 2026-07-08 |
| `reports/ultimo_report.md` | Report task: 4/4 punti completati, round-trip verbatim, verdetto revisore #44 |
