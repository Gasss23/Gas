# DIFF SESSIONE — 2026-10-28 — Mani fetta 22 (PR #285)

File toccati (base b95c3f3, merge della PR #280):
- `modules/web/lexbor.py` — `intero()` del figlio: «0», «000», «-0» valgono 0, un negativo non zero None (R-bot280-1, R-536-1).
- `tests/test_unit_web_lexbor.py` — test parametrizzato su `intero()`, presa dal sorgente del figlio con `ast` (gira senza selectolax).
- `.claude/agents/memoria_revisore.md` — righe delle review #536 e #537.
- `reports/stato_progetto.md` — blocco «Mani — fetta 22» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto a) fatto, PR #285.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
