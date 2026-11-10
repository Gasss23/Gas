# Ultimo report — 2026-11-10 — R7 fetta 1: ripresa dei compiti in sottofondo dopo un crash (chat M3)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #364 (https://github.com/Gasss23/Gas/pull/364): revisore APPROVATO CON RISERVE (BASSA/COSMETICA); si mergia solo col verdetto del bot APPROVATO pulito, altrimenti col sì dell'operatore via M1.

## Esito
- **Proposta R7** (`reports/proposta_r7_direttore.md`): FATTA — 4 opzioni, raccomandato l'ordine ripresa automatica → ripresa al boot → piano scritto dal modello → lista dei lavori ricorrenti. Mandata a M1.
- **Fetta 1 — ripresa automatica**: FATTA — `modules/sottofondo/__init__.py`: processo morto (non oltre la durata massima) → compito di nuovo in coda e riavviato, max `GAS_SOTTOFONDO_RIPRESE` (default 2, tetto 5), presa del posto sotto `fcntl.flock`, tempo totale contato dalla prima creazione. Progressi in `<id>.passi` (0600): solo nomi di strumenti registrati, «fatto»/«in_firma»; nota nel prompt del compito ripreso; avviso finale «ripreso N volte». `gas.py`: `tool_res` porta `nome`.
- **Riserve del revisore**: R-736-1 (MEDIA, corsa fra due controlli), R-736-2, R-736-3, R-737-1 CHIUSE; aperte R-737-2 (BASSA) e R-738-1 (COSMETICA), in `reports/stato_progetto.md`.
- **Merge di origin/main (#360 di M2)**: FATTO, review #739 APPROVATO.
- Ripresa al boot, piano scritto dal modello, lista dei lavori ricorrenti: DEFERITE — fette successive.

## Test
pytest `tests/test_unit_sottofondo.py`: 103 passed. Suite kernel: 1100 PASS, 0 FAIL. Voce+notte+sottofondo: 478 passed.

## Anomalie
Nessuna. Non provato con processi veri (flock fra processi, kill del figlio).
