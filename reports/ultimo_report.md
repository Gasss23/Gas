# Ultimo report — 2026-11-07 — Sottofondo: chiusura delle riserve BASSE (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (riserve BASSE: sì via M1).
2. Prova sul Mac: a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

## Esito delle fette

- **PR #345** (fetta 3 sottofondo): `MERGIATA` (5c79886).
- **Fetta BASSE del sottofondo**: `FATTA` — pid riusato, «creato» sbagliato, avviso al crash a ogni turno, niente avvisa_operatore nel compito in sottofondo, «fermato» solo se vero, pulizia dopo 7 giorni, inf/nan; review #701-M2 e #702-M2 APPROVATO CON RISERVE (R-701-3-M2, R-702-1-M2 BASSE).
- Test: kernel 1100 PASS 0 FAIL; sottofondo 59 passed.

## Anomalie

- Durante i test un mio test senza `killpg` neutralizzato ha mandato SIGTERM a pytest (nessun danno, corretto prima del commit).
