# Diff della sessione — 2026-10-08 — R-220-3 tetti di tempo di `gas notte`

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `PROVIDER_TIMEOUT_SEC` (120s) / `OLLAMA_TIMEOUT_SEC` (600s), override env, helper `_timeout_provider`, passati ai client di `run_turn` e `rifletti`: un provider appeso non blocca più per ore.
- `modules/notte/notte.py` — tetti di tempo per compito e per giro (cooperativi), chiusura del generatore, compiti saltati con avviso ed exit 1.
- `tests/test_unit_kernel.py` — finti `OpenAI` accettano `timeout`; T81a–T81d.
- `tests/test_unit_notte.py` — finto `OpenAI` accetta `timeout`; 5 test sui tetti di tempo.
- `reports/setup_notte.md` — §2c variabili dei tetti e caso peggiore reale.
- `reports/stato_progetto.md` — R-220-3 chiusa, riserve R-226-4/R-227-1/R-227-2.
- `.claude/agents/memoria_revisore.md` — lezioni review #226 e #227 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
