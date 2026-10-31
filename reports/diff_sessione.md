# DIFF SESSIONE — 2026-10-30/31 — Mani, fetta 32: proxy filtrante per il browser senza schermo

File toccati rispetto a main 3a38e75 (PR #310, #311 e #313 mergiate; main portato nel branch con due merge, solo conflitti nei report e nella memoria):
- `modules/web/proxy.py` — nuovo: `ProxyFiltrante`, da cui il futuro browser senza schermo uscirà in rete con le stesse regole di leggi_pagina. Motivo: R6, piano approvato dall'operatore.
- `tests/test_unit_web_proxy.py` — nuovo: 55 test con server d'origine, eco locale, DNS e connettore finti.
- `tests/test_unit_web_leggi.py` — test https sulla porta 80 (V-1 bot #310).
- `.claude/agents/memoria_revisore.md` — righe delle review dalla #585 alla #592.
- `reports/stato_progetto.md` — blocco «Mani — fetta 32» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
