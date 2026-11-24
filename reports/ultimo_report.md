# Ultimo report — 2026-11-24 — Revisione in più sugli script del CRM

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta: tocca il file del perimetro e `scripts/`, quindi il bot darà `neutral` e il merge lo decide l'operatore.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; controllare che l'ultima riga dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

## Esito
- **Richiesta dell'operatore** («ci sta comunque una revisione in più, dato che comunque sono dati personali dei clienti e non dobbiamo fare assolutamente neanche un errore»): FATTA. `scripts/crm/` è nel perimetro di review (`.claude/perimetro_review.txt`), decisione 20 in `reports/crm/decisioni.md`. R-852M-2 chiusa. Commit d54a09ad, review #853 APPROVATO CON RISERVE.
- **Note del bot sulla #403 rimaste aperte** (V-1 plist lasciato se la dashboard non parte, V-2 errore di import confuso con il token mancante): FATTE in d54a09ad.
- **Riserve della review #853**: R-853-1 (plist lasciato dopo 3 caricamenti falliti o plutil fallito) chiusa con una funzione unica `togli_servizio` usata a ogni STOP; R-853-2 chiusa SOLO per la parte delle copie: le copie locali del CRM ora tengono la più recente di ognuno degli ultimi 30 giorni più le ultime 10, così tanti riavvii nello stesso giorno non cancellano più i giorni prima. Commit 75dbd9d9, review #854 APPROVATO CON RISERVE.
- Guida aggiornata (`reports/crm/guida.md`) con la regola nuova delle copie.

## Test
- `pytest tests/test_unit_crm.py`: 151 passed (nuovo `test_backup_tiene_i_giorni_anche_con_tanti_riavvii`: 40 giorni più 60 riavvii → 30 giorni e 10 copie di oggi). Il revisore ha fatto 8 modifiche apposta al codice delle copie: i test le hanno fatte fallire tutte.
- `tests/test_unit_hooks.py -k "perimetro or gate"`: 128 passed. mypy pulito su `modules/crm/store.py`, `bash -n` sugli script.
- Installer provato dal revisore su Linux con comandi finti (uname, launchctl, plutil, curl, sleep): servizio tolto in tutti e tre i punti di STOP, caso riuscito con uscita 0. Non provato su un Mac vero.

## Riserve aperte
- R-854-1 BASSA: Ctrl+C durante l'attesa della dashboard (fino a 30 s) lascia il servizio installato; serve un `trap`.
- R-854-2 BASSA: parte restante di R-853-2, KeepAlive senza tetto (un CRM che non parte si riavvia ogni 10 s per sempre, registro senza rotazione, nessun avviso).
- R-853-3 BASSA: nessun test degli script del CRM con comandi finti.
- COSMETICHE #853/#854 (in `reports/stato_progetto.md`).
- Dalla PR #397: R-848-2 BASSA, R-848-3 BASSA, V-3 BASSA della verifica esterna, cosmetiche #848; R-836-1 COSMETICA. R-852M-1 (voce) in `reports/stato_progetto.md`.
