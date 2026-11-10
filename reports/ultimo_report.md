# Ultimo report — 2026-11-10 — R7 fetta 1: ripresa dei compiti in sottofondo dopo un crash (chat M3)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #364 (https://github.com/Gasss23/Gas/pull/364): contiene una correzione di SICUREZZA al cancello (`.gas_sottofondo/` mai scrivibile, dall'audit notturno), quindi serve il sì dell'operatore via M1 anche col bot APPROVATO. Revisore APPROVATO CON RISERVE (solo BASSA/COSMETICA); bot sul giro a7eb3fc APPROVATA con riserve BASSE; la correzione di sicurezza va ancora passata da bot e verifica esterna.

## Esito
- **Proposta R7** (`reports/proposta_r7_direttore.md`): FATTA — 4 opzioni, raccomandato l'ordine ripresa automatica → ripresa al boot → piano scritto dal modello → lista dei lavori ricorrenti. Mandata a M1.
- **Fetta 1 — ripresa automatica**: FATTA — `modules/sottofondo/__init__.py`: processo morto (non oltre la durata massima) → compito di nuovo in coda e riavviato, max `GAS_SOTTOFONDO_RIPRESE` (default 2, tetto 5), presa del posto sotto `fcntl.flock`, tempo totale contato dalla prima creazione. Progressi in `<id>.passi` (0600): solo nomi di strumenti registrati, «fatto»/«in_firma»; nota nel prompt del compito ripreso; avviso finale «ripreso N volte». `gas.py`: `tool_res` porta `nome`.
- **Riserve del revisore**: R-736-1 (MEDIA, corsa fra due controlli), R-736-2, R-736-3, R-737-1 CHIUSE; aperte R-737-2 (BASSA), R-738-1 e R-745-1 (COSMETICHE), in `reports/stato_progetto.md`.
- **Merge di origin/main (#360 di M2)**: FATTO, review #739 APPROVATO.
- **Bot #364 su dc6c25a** (NON approvata): V-1 MEDIA (un kill dell'operatore faceva ripartire il compito in silenzio) CHIUSA — avviso a ogni ripresa e comando `python gas.py sottofondo-ferma` (segno `<id>.ferma` sotto il lock della coda, ferma il processo solo se è il nostro figlio, chiude «ko»); V-2 BASSA (tetto di tempo con un buco) CHIUSA — niente ripresa oltre la durata contata dalla prima creazione. Review #743 → #744 → #745 APPROVATO CON RISERVE (R-743-1/2/3 e R-744-1/2 chiuse; resta R-745-1 COSMETICA).
- **Verifica esterna #364** (su dc6c25a): APPROVATO CON RISERVE, nessuna ALTA/MEDIA; V-1 BASSA (compito mai partito ritentato) tracciata in stato_progetto.
- **Merge di origin/main (#362 di M4)**: FATTO (solo report e memoria del revisore).
- **Bot #364 2° giro (a7eb3fc)**: APPROVATA, riserve BASSE (avviso di ripresa e tetto notifiche; cartella di lancio di `sottofondo-ferma`) tracciate in stato_progetto. Verifica esterna 2° giro: APPROVATO CON RISERVE, nessuna ALTA/MEDIA.
- **Audit notturno (M1) — `.gas_sottofondo/` scrivibile senza firma**: FATTO — denylist + livello 3 in `modules/gate/gate.py`, test gate (10 failed senza fix) e kernel T6s. Review #746 APPROVATO CON RISERVE (R-746-1 BASSA preesistente, R-746-2 COSMETICA).
- **Merge di origin/main (#361)**: FATTO, review #747 APPROVATO.
- Ripresa al boot, piano scritto dal modello, lista dei lavori ricorrenti: DEFERITE — fette successive.

## Test
pytest `tests/test_unit_sottofondo.py`: 112 passed. Suite kernel: 1104 PASS, 0 FAIL. Gate: 832 passed. Voce+notte+sottofondo: 478 passed.

## Anomalie
Nessuna. Non provato con processi veri (flock fra processi, kill del figlio).
