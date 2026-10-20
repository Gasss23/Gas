# DIFF SESSIONE — 2026-10-20 (dopo #225: firme scadute C5, avvisi dei lead raggruppati)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/memory/store.py` — `scadi_approvazioni`, `conta_approvazioni`; `expire_stale_approvals` ne usa la prima.
- `modules/telegram/bot.py` — `componi_avviso_scadute`, `avvisa_firme_scadute`; controllo nel loop del bot una volta al minuto.
- `modules/notte/notte.py` — `_chiudi_firme_scadute` a fine giro, numero negli avvisi del mattino.
- `gas.py` — riga «Firme» di `gas doctor`; avvisi dei lead raggruppati a fine turno (`_invia_avvisi_lead`), lead nuovi contati.
- `tests/test_unit_kernel.py`, `tests/test_unit_notte.py` — test nuovi (T73d2, T61b2, T74b6, giro e bot).
- `.claude/agents/memoria_revisore.md` — righe #381–#383.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
