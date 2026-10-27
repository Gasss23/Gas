# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 20, PR #277)

- `modules/web/lexbor.py`: sonda del figlio con lock non bloccante e riprova dopo un timeout (R-521-1/2), motivo del fallimento da `_esegui`, solo Linux (uscita 3 altrove), ultima riga dello stderr nel warning, nascosti anche select/datalist/rp, attributo `hidden` e dialog chiusi, `nodo.attrs` (R-525-1).
- `modules/web/leggi.py`: docstring con la sonda nella stima dei tempi (~23 s) e la condizione «su Linux».
- `tests/test_unit_web_lexbor.py`: 28 test (nuovi: una sonda alla volta, sonda che si riprova, fuori da Linux, pulizia dello stderr, pagina con hidden/dialog/select/datalist/rp; test della sonda e docstring del tetto sistemati).
- `.claude/agents/memoria_revisore.md`: righe delle review #525 e #526 (commit del revisore).
- `reports/stato_progetto.md`: intestazione, numeri e merge della fetta 19, blocco «Mani — fetta 20».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
