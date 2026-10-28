# Report del turno di notte — 2026-10-28

Ramo `notte/2026-10-28`, PR #281 (https://github.com/Gasss23/Gas/pull/281). Nessun merge (regola del turno).
La voce 0 (contatti illeggibili in `ricorda contatto` e `gas fida-contatto`) era già su main: l'ha fatta la chat Motore con la PR #279 (review #528). Al massimo una voce del motore a notte: presa la voce 6.

## Voce 6 — Segno nel DB per l'esito delle firme — FATTA (fetta di sicurezza)
- **Cosa**: per sapere se l'esito di una firma è già stato scritto nella cronologia, Gas guardava solo la cronologia stessa. Ora c'è anche un segno nel database (tabella nuova, solo inserimenti). L'esito si registra nel database PRIMA della cronologia, e il segno si mette solo quando la cronologia è davvero salvata su disco.
- **Perché / cosa migliora**:
  - un crash nel momento sbagliato non lascia più l'esito vuoto per sempre (R-445-3), e al riavvio il recupero lo scrive com'era;
  - dopo `/clear` un nuovo click su Approva non riscrive un esito già notificato.
- **Controlli**: 7 test nuovi (T78q–T78u: crash simulato, riavvio, `/clear`, migrazione di un DB vecchio, salvataggio fallito), che falliscono sul codice di prima (5 su 7). Kernel 1043 → 1053 PASS 0 FAIL; pytest 2265 passed.
  - Review #531: BOCCIATO. Il recupero metteva il segno anche con l'esito solo in memoria: dopo un crash l'esito non sarebbe più stato scritto. Corretto.
  - Review #532: APPROVATO CON RISERVE.
- **Rischi**: tocca la firma umana, quindi conviene un secondo passaggio su claude.ai. Restano due note BASSE:
  - con due processi Gas in conflitto sulla cronologia, un esito può restare solo nella copia di conflitto (R-531-3, da lettura del codice, non provato);
  - con il salvataggio rimandato, il segno si mette solo al click successivo (R-532-1, verso sicuro).
  - Non provato con Telegram vero.

## Cosa deve decidere l'operatore
1. Merge della PR #281 (il turno di notte non mergia), dopo il secondo passaggio su claude.ai col link della PR.
2. Il testo dell'attività programmata è ancora quello vecchio: se lo vuoi cambiare, chiedilo in questa sessione.
