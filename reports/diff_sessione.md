# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 21 con secondo giro, PR #280)

- `modules/web/lexbor.py`: `intero()` con tetto alle cifre e a 2**31-1, zeri in testa ignorati; nel figlio nascosti anche video, audio, meter, progress; commento in testa aggiornato.
- `modules/web/leggi.py`: docstring sulle sonde ripetute, commento «In prova» tolto.
- `tests/test_unit_web_lexbor.py`: casi per size (+2, enorme, 11 cifre, zeri in testa, confine 2**31), hidden=false/'', video/audio/meter/progress, sonda già riuscita col lock preso; test delle opzioni annidate senza soglia in secondi.
- `.claude/agents/memoria_revisore.md`: righe delle review #531-#535 (commit del revisore; #533 e #535 coi merge di main).
- Merge di main 24ed87d (7b6bc24) e 52fc615 (465ba13): gas.py, modules/memory/store.py, tests/test_unit_kernel.py, CLAUDE.md e i report della notte arrivano da main e non fanno parte del diff di sessione.
- `reports/stato_progetto.md`: intestazione e blocco «Mani — fetta 21», con le riserve di #280 DA SISTEMARE.
- `reports/ripartenza_mani.md`: istruzioni per ripartire dopo il `/clear`, da richiamare con una riga sola.
- `reports/strumenti_mani/misura_web.py`: strumento di misura delle fette 19-20 (oracolo html5lib, fuzz, corpus, tempi), prima solo nello scratchpad; fuori dal perimetro di review, riga morta tolta.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
