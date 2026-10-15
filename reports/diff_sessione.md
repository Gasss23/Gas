# DIFF SESSIONE — 2026-10-15 (FASE 2.6 fetta 3)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `_recap_pin(user_prompt)`: il più recente tra i recap fidati pertinenti (almeno 2 parole in comune) e non scaduti, intestazione «RECAP PERTINENTE» (`GAS_RECAP_MAX_GIORNI`); `_parole_recap`, `RECAP_MIN_PAROLE`; import `timedelta`.
- `modules/memory/store.py` — `diario_per_tipo_dal`: recap di un tipo e fonte da una data in poi, sola lettura.
- `tests/test_unit_kernel.py` — T90a–j, T90c2, T90c3; `_BLOCCO80` con la nuova intestazione.
- `reports/setup_notte.md` — a capo della riga sulla riflessione (cosmetica bot #212).
- `reports/stato_progetto.md`, `reports/roadmap.md` — fetta 3 fatta, R-199-3 chiusa.
- `.claude/agents/memoria_revisore.md` — righe #348, #349 e #350.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
