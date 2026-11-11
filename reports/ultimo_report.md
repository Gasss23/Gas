# Ultimo report — 2026-11-11 notte — Voce: log «parola quasi sentita» (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (riserve solo BASSE).
2. Dopo una prova sul Mac: soglia della parola a 0,6 se le chiamate vere finiscono tra le «quasi sentite». sì/no dopo i dati.

## Esito
- **Log «parola quasi sentita»** (clients/voice/ascolto.py): FATTA — ogni salita del rilevatore da 0,30 in su che non attiva scrive punteggio massimo, blocchi e soglia (solo numeri, max una riga ogni 5 s). L'attivazione non cambia.
- **Diagnosi** (scripts/voce/diagnosi_ascolto.py): FATTA — sezione «Quasi sentite» per giorno e ultime.
- Review #791-M1coord APPROVATO CON RISERVE (R-791-1/2 BASSE).

## Test
tests/test_unit_voce_ascolto.py: 326 → 332 passed (6 nuovi). Kernel non toccato.

## Anomalie
Dati del Mac (sera 11/11): dopo il riavvio delle 23:34 una sola attivazione (23:38, punteggio 0,90), poi nessuna; tempi claude-cli: primo testo 3,15 s, tutto 5,49 s, avvio fuori CLI 1,73 s; la prima frase arriva al client solo a fine turno (6,16 s): lo streaming della #374 prepara la voce in anticipo ma la risposta HTTP parte a turno finito.
