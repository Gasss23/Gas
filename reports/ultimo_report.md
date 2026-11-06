# Ultimo report — 2026-11-06 — Bot di verifica: «ad alta voce» non è una gravità (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR del parser del bot: tocca `scripts/bot_esito.py`, quindi `verifica-bot` dà neutral e decide l'operatore (fetta già approvata via M1).

## Esito delle fette

- **PR #339 (voce V15)**: `MERGIATA` in main (3cde8a5) con CI verde e bot APPROVATO CON RISERVE senza ALTA/MEDIA su dba3b2c, col sì dell'operatore via M1.
- **Falso failure «ad alta voce»** (bot #339 su 312cd86): `FATTA` — `_ALTA_VOCE` in `scripts/bot_esito.py` («alta» solo minuscolo; «a voce alta» solo a fine frase), test sul verdetto vero; review #687-M2 APPROVATO CON RISERVE, #688-M2 APPROVATO.
- **Falso failure su citazione senza parentesi** («R-682-1-M2 MEDIA …», bot #339 su d9c09e9): `NON FATTA — fuori scope` (blocca invece di lasciar passare: direzione sicura).
- **Fetta 2 voce rapida**, **documento fetta 3**: `DEFERITE — prossime fette`.
- Test: tests/test_unit_verifica_bot.py 593 passed (prima 582).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
