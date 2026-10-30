# DIFF SESSIONE — 2026-10-30 — Mani, fetta 31: leggi_pagina solo porte 80 e 443

File toccati rispetto a main 4ffcd80 (PR #309 mergiata):
- `modules/web/leggi.py` — `_PORTE_PERMESSE = {80, 443}` controllate in `_valida_url` (anche a ogni redirect); docstring aggiornata. Motivo: decisione dell'operatore del 2026-10-22.
- `tests/test_unit_web_leggi.py` — porte rifiutate, redirect verso un'altra porta, porte incrociate, test TLS su 443, IP interno su altra porta.
- `.claude/agents/memoria_revisore.md` — righe delle review #583 e #584.
- `reports/roadmap.md` — decisione delle porte segnata come fatta nel codice.
- `reports/stato_progetto.md` — blocco «Mani — fetta 31» (con V-1 bot #309 registrata come limite) e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
