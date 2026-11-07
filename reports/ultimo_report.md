# Ultimo report — 2026-11-07 — Sottofondo: chiusura delle riserve BASSE (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (riserve BASSE: sì via M1).
2. Prova sul Mac: a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

## Esito delle fette

- **PR #345** (fetta 3 sottofondo): `MERGIATA` (5c79886).
- **Fetta BASSE del sottofondo**: `FATTA` — pid riusato, «creato» sbagliato, avviso al crash a ogni turno, niente avvisa_operatore nel compito in sottofondo, «fermato» solo se vero, pulizia dopo 7 giorni, inf/nan; review #701-M2 e #702-M2 APPROVATO CON RISERVE (R-701-3-M2, R-702-1-M2 BASSE).
- **Verifica esterna #346**: V-1 BASSA (orologio indietro → compito vero fermato) e V-2 `CORRETTE` (fb620f5, review #703-M2 APPROVATO CON RISERVE, R-703-1/2-M2 BASSE).
- **Conflitto con main (bot #346 V-1 MEDIA)**: `RISOLTO` col merge 643da99 della #341 di Mani (solo report e memoria; review #704-M2 APPROVATO).
- Test: kernel 1100 PASS 0 FAIL; sottofondo 62 passed; sottofondo + voce_ascolto dopo il merge 319 passed.

## Anomalie

- Durante i test un mio test senza `killpg` neutralizzato ha mandato SIGTERM a pytest (nessun danno, corretto prima del commit).
