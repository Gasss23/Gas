# DIFF SESSIONE — 2026-10-28 — Mani fetta 23 (PR #288)

File toccati rispetto a main 2f35bc6 (dopo i merge di main per i conflitti della #288; da main entrano gas.py, brains/claude_cli.py, tests/test_unit_dotenv.py e i test del kernel, identici a main e quindi fuori da questo diff):
- `modules/web/lexbor.py` — nel figlio: `HOST`, `RISERVATI`, `CON_SHADOW`, `primi_slot()`, `shadow()`; `visita()` porta sulla pila gli slot dello shadow corrente; `opzioni()` legge il testo delle opzioni senza shadow né assegnati. Shadow DOM dichiarativo come il browser (scelta 3 dell'operatore); commento su HOST con la fonte dello standard (V-2 ve #288); testo delle opzioni senza shadow e senza assegnati, `shadowrootslotassignment=manual` (giri #544/#545).
- `tests/test_unit_web_lexbor.py` — casi shadow nel test «come il browser» e test nuovo `test_shadow_dichiarativo_in_ordine` (con `x-a!`, `x.y-é` e template con `slot`, V-2/V-3 ve #288).
- `.claude/agents/memoria_revisore.md` — righe delle review #539–#546 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 23» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — PR #288, punto c) fatto.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
