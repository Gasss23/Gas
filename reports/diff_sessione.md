# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 21, PR #280)

- `modules/web/lexbor.py`: `intero()` con tetto alle cifre e a 2**31-1, zeri in testa ignorati; nel figlio nascosti anche video, audio, meter, progress; commento in testa aggiornato.
- `modules/web/leggi.py`: docstring sulle sonde ripetute, commento «In prova» tolto.
- `tests/test_unit_web_lexbor.py`: casi per size (+2, enorme, 11 cifre, zeri in testa), hidden=false/'', video/audio/meter/progress, sonda già riuscita col lock preso; test delle opzioni annidate senza soglia in secondi.
- `.claude/agents/memoria_revisore.md`: righe delle review #531 e #532 (commit del revisore).
- `reports/stato_progetto.md`: intestazione e blocco «Mani — fetta 21».
- `reports/ripartenza_mani.md`: prompt per ripartire dopo il `/clear`.
- `reports/strumenti_mani/misura_web.py`: strumento di misura delle fette 19-20 (oracolo html5lib, fuzz, corpus, tempi), prima solo nello scratchpad.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
