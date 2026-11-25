# DIFF DI SESSIONE — 25 novembre 2026, R7 fetta 4 bis (tetto duro del giro di notte)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/notte.py`: `_arma_tetto_giro` (timer demone, attesa massima 30 giorni), `_termina_giro` (os._exit, limiti dichiarati), `_nuova_guardia` e `_giro_scaduto` (lock e flag condivisi con la fine del giro, avviso «INTERROTTO», nome del compito nel log); in `esegui_notte` timer armato a max_giro + 300 s e tolto nel finally, senza riepilogo doppio.
- `tests/test_unit_notte.py`: 8 test del tetto duro (armato e tolto, giro che si rompe, scadenza con avviso e arresto, testo su Telegram, timer vero, un solo avviso, nome nel log, attesa enorme).
- `.claude/agents/memoria_revisore.md`: righe delle review #866-R7, #867-R7 e #868-MERGE-R7, #869-MERGE-R7 (più quelle della #402 e della #410 arrivate coi merge di main fa2fc877 e 6d5adc51).
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
