# Diff sessione — 2026-06-27 (FASE 2.5 + chiusura 5 item roadmap)

> Si riscrive a ogni sessione. La storia completa sta in git.

## Commit della sessione

```
65c4c7b feat(kernel): FASE 2.5 — compressione automatica .gas_history.json (review #39)
932f17c docs(report): chiusura 5 item roadmap 2026-06-27 — review #38 APPROVATO
a8c6d53 feat(kernel): chiusura item aperti roadmap — budget cap + Telegram bridge + calibrate/eval-vectors (review #38)
```

## File motore toccati

| File | Commit | Perché |
|---|---|---|
| `gas.py` | a8c6d53 | Budget cap + Telegram dispatch + calibrate/eval-vectors |
| `modules/telegram/__init__.py` | a8c6d53 | Package Telegram (nuovo) |
| `modules/telegram/bot.py` | a8c6d53 | Bridge bot Telegram (nuovo) |
| `tests/test_unit_kernel.py` | a8c6d53 | T41-T48 (budget + Telegram) |
| `gas.py` | 65c4c7b | FASE 2.5: _compress_history_if_needed + compress_history_cmd + trigger run_turn |
| `tests/test_unit_kernel.py` | 65c4c7b | T49-T52 (compressione history) |

## Doc aggiornati

| File | Cosa è cambiato |
|---|---|
| `reports/roadmap.md` | 5 item chiusi, nuovi prossimi passi |
| `reports/stato_progetto.md` | FASE 2.5 aggiunta, review count 39, prossimi passi aggiornati |
| `reports/ultimo_report.md` | Report task corrente (FASE 2.5) |
| `.claude/agents/memoria_revisore.md` | Lezioni review #38 e #39 |

## Cosa NON è cambiato

- Logica provider/cascata fallback invariata.
- Memoria SQLite e vector store invariati.
- Sandbox bwrap invariata.
- 7 FAIL Windows pre-esistenti invariati (ambiente, non regressioni).
