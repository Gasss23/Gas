# Diff sessione — 2026-06-27 (chiusura 5 item roadmap)

> Si riscrive a ogni sessione. La storia completa sta in git.

## Commit della sessione

```
a8c6d53 feat(kernel): chiusura item aperti roadmap — budget cap + Telegram bridge + calibrate/eval-vectors (review #38)
```

## File motore toccati

| File | Tipo | Perché |
|---|---|---|
| `gas.py` | Modificato (+155 righe) | `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` + `calibrate_vectors_cmd` + `eval_vectors_cmd` + dispatch main() |
| `modules/telegram/__init__.py` | Nuovo (vuoto) | Package del bridge Telegram |
| `modules/telegram/bot.py` | Nuovo (+198 righe) | Bridge bot Telegram (long polling, whitelist, GasKernel condiviso) |
| `tests/test_unit_kernel.py` | Modificato (+93 righe) | T41-T48: budget cap e modulo Telegram |

## Doc aggiornati (commit report)

| File | Cosa è cambiato |
|---|---|
| `reports/roadmap.md` | Item 1-5 spostati da "aperti" a "chiusi"; nuova sezione prossimi passi ridotta |
| `reports/stato_progetto.md` | Componenti aggiornati, review count 37→38, prossimi passi aggiornati |
| `reports/ultimo_report.md` | Report canonico task corrente |
| `reports/diff_sessione.md` | Questo file |
| `reports/handoff.md` | Dossier fine sessione |

## Cosa NON è cambiato

- Logica provider/cascata fallback invariata.
- Memoria SQLite e vector store invariati (solo nuove CLI).
- Sandbox bwrap invariata.
- 7 FAIL Windows pre-esistenti invariati (bwrap, WinError32 — ambiente, non regressioni).
