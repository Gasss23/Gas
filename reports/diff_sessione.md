# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 20 con secondo giro, PR #277)

- `modules/web/lexbor.py`: sonda del figlio con lock non bloccante; ogni sonda fallita si riprova dopo 600 s, spenta dopo 3; solo Linux (uscita 3 altrove); ultima riga dello stderr nel warning; nascosti select/datalist/rp, attributo `hidden`, dialog chiusi, body/html con `hidden`; del select l'opzione scelta (tutte con multiple/size) raccolta con una discesa lineare; details chiuso → solo il primo summary.
- `modules/web/leggi.py`: docstring con la sonda nella stima dei tempi (~23 s) e la condizione «su Linux».
- `tests/test_unit_web_lexbor.py`: 53 test (sonde, Linux, stderr, select/option/size, details, hidden, commenti nel select, tempo lineare con molte opzioni annidate).
- `.claude/agents/memoria_revisore.md`: righe delle review #525-#529 (commit del revisore).
- `reports/stato_progetto.md`: intestazione e blocco «Mani — fetta 20» con il secondo giro e le riserve R-527/R-528/R-529.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
