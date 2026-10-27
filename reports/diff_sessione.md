# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 20 con secondo giro, PR #277)

- `modules/web/lexbor.py`: sonda del figlio con lock non bloccante; ogni sonda fallita si riprova dopo 600 s, spenta dopo 3; solo Linux (uscita 3 altrove); ultima riga dello stderr nel warning; nascosti select/datalist/rp, attributo `hidden`, dialog chiusi, body/html con `hidden`; del select l'opzione scelta (tutte con multiple/size) raccolta con una discesa lineare; details chiuso → solo il primo summary.
- `modules/web/leggi.py`: docstring con la sonda nella stima dei tempi (~23 s) e la condizione «su Linux».
- `tests/test_unit_web_lexbor.py`: 53 test (sonde, Linux, stderr, select/option/size, details, hidden, commenti nel select, tempo lineare con molte opzioni annidate).
- `.claude/agents/memoria_revisore.md`: righe delle review #525-#530 (commit del revisore; #530 col merge di main).
- `reports/stato_progetto.md`: intestazione e blocco «Mani — fetta 20» con il secondo giro, le riserve R-527/R-528/R-529 e quelle di bot e verifica esterna su 0c2a5c8 (R-ve277-3/4/5, R-bot277-4).
- Merge di main 932ecd6 (7e2622f): gas.py, tests/test_unit_kernel.py e reports/coda_notte.md arrivano da main e non fanno parte del diff di sessione.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
