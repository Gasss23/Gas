# Ultimo report — 2026-11-07 — fetta 45 (chat Mani): riserve della #341 e della #347 (voce)

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 45: review #707–#709 APPROVATO CON RISERVE (solo BASSE/COSMETICHE) e PR nel perimetro, quindi decide l'operatore via M1.

## Esito

- **PR #348**: MERGIATA (53ae39b) col sì dell'operatore. Contiene «Hey Gas» NO e la proposta voce via Telegram, opzione B scelta.
- **Fetta 45**: FATTA.
  - Log degli errori del rilevatore nella finestra (R-681-1).
  - La pausa muta non è più scritta come errore; una pausa con un errore vero tiene il motivo (R-679-3, R-707-3).
  - Avviso nel log se GAS_VOICE_FINESTRA è fuori da 0–120 (V-3 bot #347).
  - LEGGIMI: «Hey Gas» NO (V-1 bot su b48a0a8), controllo dell'eco solo col formato a frasi (V-1 bot #347), limiti di riprendi.sh (V-2 bot #347).
  - Test per R-676-1 (chiudi azzerato dopo «fine») e per il ramo «niente suonato» (R-708-1).
  - Suite ascolto 292 passed; mutanti presi.
- **V-1 della verifica esterna #347**: SALTATA per scelta (R-708-2). Era la tolleranza dopo una parola sentita prima della voce: secondo la sonda del revisore aiuta quasi solo i falsi positivi e fa passare fino a circa 5 s di stanza senza filtro.
- **Fetta 1 Telegram**: pronta in locale (review #711/#712), si pubblica dopo questa PR.
