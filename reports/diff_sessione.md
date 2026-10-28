# DIFF SESSIONE — 2026-10-28 — Mani fetta 23 (PR #288)

File toccati rispetto a main 0a9ce70 (dopo il merge di main per V-1 del bot #288; da main entrano gas.py, brains/claude_cli.py e i loro test, identici a main e quindi fuori da questo diff):
- `modules/web/lexbor.py` — nel figlio: `HOST`, `RISERVATI`, `CON_SHADOW`, `primi_slot()`, `shadow()`; `visita()` porta sulla pila gli slot dello shadow corrente; `opzioni()` passa il giro alle opzioni. Shadow DOM dichiarativo come il browser (scelta 3 dell'operatore).
- `tests/test_unit_web_lexbor.py` — casi shadow nel test «come il browser» e test nuovo `test_shadow_dichiarativo_in_ordine`.
- `.claude/agents/memoria_revisore.md` — righe delle review #539, #540 e #541 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 23» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — PR #288, punto c) fatto.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
