# ULTIMO REPORT — R7 fetta 3: stato dei lavori ricorrenti del giro di notte

**Data:** 23 novembre 2026
**Branch:** claude/r7-lavori-ricorrenti (sotto-chat di M1)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #399** (vedi handoff §0): tocca il motore; merge autonomo solo con verdetto del bot APPROVATO pulito, altrimenti decide l'operatore.
2. **PR #398 (fetta 2, ripresa al boot)**: ancora aperta, sul suo ramo; il suo stato è nel report di quel ramo.

## Esito fette

- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: FATTA. Registro `.gas_notte/stato_lavori.json` in `modules/notte/notte.py` (fatto / in sospeso / fallito / da non ritentare), aggiornato dopo ogni compito eseguito; 3 ko di fila → fermo 7 giorni nei giri completi (avviso, non è un ko del giro); `python3 gas.py notte <nome>` lo rilancia sempre; prompt cambiato o data assurda → la pausa decade; potatura solo a catalogo sano (come R-407-1); sezione «Lavori ricorrenti (stato)» nel riepilogo; doc in `reports/setup_notte.md`. 9 test nuovi (209 in `tests/test_unit_notte.py`). Review #839-F3 → correzioni R-839-1 MEDIA e R-839-2 BASSA → review #842 APPROVATO CON RISERVE.
- **Correzioni delle riserve (bot e verifica esterna) sulla PR #399**: FATTA. Guasti esterni non contati tra i ko di fila, sezione con tutti i compiti, avviso col conto reale e ritmo documentato. 6 test nuovi (215). Review #843 APPROVATO CON RISERVE (R-843-1 BASSA).
- **Merge di main (PR #397, CRM) e correzioni del terzo giro**: FATTA. Merge 73277ba0 (review #844-MERGE: R-844M-1 MEDIA, con «Sempre Opus» acceso l'errore «Rispondo solo con Claude Opus» non era un guasto esterno). Correzione 87006476: prefisso aggiunto con test col kernel vero; tetto di 14 guasti esterni di fila (verifica esterna V-1); pausa in corso non tolta né allungata (R-843-1, R-845R7-1/2). Review #846-R7 APPROVATO. 220 test.
- **V-1 MEDIA del bot su 3b188028**: FATTA (7b05ccf2). Tetto delle chiamate, risposta vuota e 10 iterazioni senza risposta contano come fallimenti del lavoro (non guasti esterni), anche con «Sempre Opus». Review #847-R7 BOCCIATO → #848-R7 APPROVATO. 230 test.
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — prossima PR.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

## Anomalie / cose da sapere

- Numerazione delle review: sul ramo di questa PR il revisore ha registrato la prima review come «#839», numero già usato dalla review della PR #398 sull'altro ramo. Nei report la chiamo «#839-F3»; la seconda è #842. Al merge delle memorie le due righe #839 vanno tenute entrambe.
- Le PR #398 e #399 toccano entrambe `.claude/agents/memoria_revisore.md` e i report: al secondo merge ci sarà un conflitto da risolvere tenendo le righe di entrambi i lati.
- Letta `reports/bacheca.md`: niente che blocchi questa fetta.
