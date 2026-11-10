# Ultimo report — 2026-11-10 — ascolto H24: meno attivazioni per sbaglio (chat Mani)

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

## Anomalie

Nessuna.
