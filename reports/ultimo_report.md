# Ultimo report — 2026-11-10 — ascolto H24: meno attivazioni per sbaglio + V-1 della verifica esterna #361 (chat Mani)

## DECISIONI UMANE RICHIESTE

Nessuna nuova. L'operatore, via M1, ha detto sì alla fetta correttiva se le riserve sono solo BASSE. Dopo il merge va provato dal vivo sul Mac se «Hey Jarvis» scatta ancora con 2 blocchi di fila (R-736-1). Se non scatta: `GAS_ASCOLTO_BLOCCHI_PAROLA=1` nel .env.

## Esito

- **PR #359 (voce di Telegram in un thread)**: MERGIATA (695b759) col sì esplicito dell'operatore.
- **Ascolto H24, meno attivazioni per sbaglio**: FATTA. Il log del 9/11 mostra falsi «Hey Jarvis» e turni di seguito risposti. Nuovi default in `clients/voice/ascolto.py`:
  - finestra di 15 s (era 40);
  - al massimo 2 turni di seguito dopo la richiesta (erano 4);
  - soglia della parola 0,6 (era 0,5);
  - parola valida solo con 2 blocchi di fila sopra soglia (`GAS_ASCOLTO_BLOCCHI_PAROLA`);
  - primo mezzo secondo della finestra ignorato (coda dell'eco).
- LEGGIMI aggiornato. Test dell'ascolto: 300 passed, 4 test nuovi, 4 mutanti presi. Review #736 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).

- **V-1 MEDIA della verifica esterna #361**: FATTA (bc37ae5). Nella finestra dopo la risposta la parola valeva con UN solo blocco: un picco isolato rendeva il turno normale e azzerava il conto dei turni di seguito. Ora anche lì servono 2 blocchi di fila (conto azzerato sotto soglia, su errore, allo scatto e a ogni nuova finestra); commento della soglia corretto (V-3). Test dell'ascolto: 303 passed, 3 test nuovi, tutti gli azzeramenti presi da mutanti. Review #737 APPROVATO CON RISERVE (R-737-1: azzeramenti senza test), chiusa dalla re-review #738 APPROVATO.
- **Verifica esterna #361, 2° giro**: APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/361#issuecomment-6755215312)). V-1 MEDIA (PR in conflitto con main, solo nei report) CHIUSA col merge di origin/main 447195f (a13f442), review #739 APPROVATO. Aperte: V-2 (CI/bot da attendere), V-4 BASSA (pagina web voce non allineata: 12 s, 5 turni).

## Anomalie

Suite completa nel container: 1 test del browser vero fallito (`test_testo_scritto_dal_javascript`), fuori scope (il branch non tocca modules/); fa fede la CI.
