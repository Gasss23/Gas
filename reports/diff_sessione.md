# DIFF SESSIONE — 2026-10-30 — Mani, fetta 32: proxy filtrante per il browser senza schermo

File toccati rispetto a main 1e8aff8 (PR #310 e #311 mergiate; main portato nel branch con un merge, solo conflitti nei report):
- `modules/web/proxy.py` — nuovo: `ProxyFiltrante`, da cui il futuro browser senza schermo uscirà in rete con le stesse regole di leggi_pagina. Motivo: R6, piano approvato dall'operatore.
- `tests/test_unit_web_proxy.py` — nuovo: 55 test con server d'origine, eco locale, DNS e connettore finti.
- `tests/test_unit_web_leggi.py` — test https sulla porta 80 (V-1 bot #310).
- `.claude/agents/memoria_revisore.md` — righe delle review dalla #585 alla #591.
- `reports/stato_progetto.md` — blocco «Mani — fetta 32» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
