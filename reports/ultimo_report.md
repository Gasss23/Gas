# Ultimo report — 2026-11-09 — voce via Telegram, fetta 4: voce in un thread (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: è un CAMBIO DI SICUREZZA (guardia T78p delle firme allargata, opzione b scelta dall'operatore). Resta aperta fino al sì esplicito dell'operatore, anche con verdetto pulito del bot. Secondo passaggio consigliato nella chat claude.ai col link della PR.

## Esito

- **PR #357 (fetta 3)**: MERGIATA (524ae96) col sì dell'operatore via M1; bot APPROVATO CON RISERVE, solo BASSE/COSMETICHE.
- **Voce in un thread (opzione b)**: FATTA.
  - `_consegna_voce`: sintesi e invio del vocale vanno in una coda di un solo thread; il polling di Telegram non resta fermo.
  - Guardia T78p: il secondo pool è ammesso solo lì e solo per `_invia_risposta_vocale`; `.submit`/`.map` solo in `_invia_a_tutti` e `_consegna_voce`; i nomi vietati si controllano in tutte le funzioni raggiunte dal thread. I mutanti del revisore A, B, C, E, F, G sono presi.
  - Ctrl-C scarta la coda della voce, anche durante la pausa di 5 s dopo un errore (R-725-2).
  - Review #725 APPROVATO CON RISERVE (R-725-1 MEDIA), corretta e ri-revisionata in #727 APPROVATO CON RISERVE (solo BASSE).
- **Tempi della voce di casa**: FATTA. Il log dice dopo quanti secondi arriva la prima frase di Gas (review #722).
- **Merge su main dopo la #357**: FATTO, review #728 APPROVATO (blob identici a quelli revisionati).
- Test: telegram_voce 70 + ascolto 296 = 366 passed; kernel 1099 PASS, 1 FAIL (T31g, ambiente), T78p PASS.

## Anomalie

Nessuna.
