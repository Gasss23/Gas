# Ultimo report — 2026-11-05 — fetta 41 (chat Mani): la parola di attivazione interrompe Gas mentre parla

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 41 (numero in handoff §0): review #669 APPROVATO CON RISERVE e PR nel perimetro, quindi decide l'operatore tramite M1.

## Esito

- **PR #333 (fetta 40, soglia della voce 200)**: MERGIATA (830c5bf), col sì dell'operatore via M1, dopo il merge di main (PR #334 di M2, review #670 APPROVATO) e la CI verde.
- **Fetta 41 — interruzione**: FATTA. In `clients/voice/ascolto.py`, mentre Gas parla, si cerca solo la parola di attivazione, con soglia 0.7. Se la sente: frase fermata, frasi in fila scartate, bip e nuova richiesta, sempre sotto max_turni. afplay gira in sottofondo (`RiproduzioneAfplay`). Due variabili nuove: `GAS_ASCOLTO_INTERRUZIONE` e `GAS_ASCOLTO_SOGLIA_INTERRUZIONE`. LEGGIMI aggiornato. Suite ascolto: 173 passed; mutanti tutti presi.
  - Review #668: APPROVATO CON RISERVE, con R-668-1 MEDIA (le interruzioni azzeravano il tetto dei turni), corretta.
  - Review #669: APPROVATO CON RISERVE (R-669-1 BASSA, R-669-2/3 COSMETICHE).
  - Il diff applicato su main è identico a quello rivisto: stesso SHA-256 del diff staged.
- **Fetta 42 — «Sì, signore?»**: DEFERITA. Aspetta il merge della PR #335 di M2 (GET /voce/conferma). Il client deve ripiegare sul bip su qualsiasi errore, anche di connessione o timeout.

## Anomalie

- Il primo verdetto #670 citava file usciti dal diff di sessione dopo il merge di main e il gate B lo rifiutava. Il revisore lo ha riemesso con lo stesso esito; l'originale integrale è nell'handoff del commit dba7151.
- La fetta 41 era stata committata su un branch locale (6b74158) mentre la #333 occupava l'unico branch remoto. Dopo il merge l'ho riportata su main con lo stesso diff, e le righe #668/#669 della memoria del revisore le ho aggiunte a mano.
