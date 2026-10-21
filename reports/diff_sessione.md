# Diff della sessione (chat Motore, 2026-10-21, PR #241)

- `gas.py`: `recupera_esito_firma` (esito di un'azione firmata riscritto in storia dopo un'interruzione, mai una nuova esecuzione); testo della notizia «interruzione o errore interno» (V-1 bot #241).
- `modules/telegram/bot.py`: `_riprova_orfana` chiama il recupero se l'azione è già reclamata; log se il kernel non sa recuperare (V-1 verifica esterna #241).
- `modules/notte/notte.py`: `stato_mattino` e `righe_stato_mattino`, resoconto di spesa e stato nel riepilogo e nel messaggio Telegram del mattino (R1).
- `tests/test_unit_kernel.py`: T78l-T78p (recupero, log, guardia «un click alla volta»).
- `tests/test_unit_notte.py`: 3 test del resoconto; limite finto di Telegram portato a 330 nel test dei soli conteggi.
- `.claude/agents/memoria_revisore.md`: righe delle review #445-#454 (unione con le righe della chat Mani nel merge).
- `reports/`: stato_progetto, roadmap, da_mergiare, ultimo_report, handoff, diff_sessione aggiornati.

La storia completa sta in git.
