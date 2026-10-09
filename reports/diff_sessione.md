# Diff della sessione — 2026-10-09 — riserve V-1/V-2/V-3 del bot su #162

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `PROVIDER_MAX_RETRIES = 1` (override `GAS_PROVIDER_MAX_RETRIES`) passato come `max_retries` ai client di `run_turn` e `rifletti`: meno attese su risposte lente prima del fallback (V-2).
- `modules/notte/notte.py` — docstring col caso peggiore reale (~36 min, Ollama a parte) (V-1, R-227-2).
- `tests/test_unit_kernel.py` — finti `OpenAI` accettano `max_retries`; T81e, T81f.
- `tests/test_unit_notte.py` — finto `OpenAI` accetta `max_retries`.
- `reports/setup_notte.md` — §2c caso peggiore ~36 min con `GAS_PROVIDER_MAX_RETRIES=1`.
- `reports/stato_progetto.md` — #162 mergiata, riserve bot #162 chiuse, R-229-1 aperta.
- `.claude/agents/memoria_revisore.md` — lezioni review #228 e #229 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
