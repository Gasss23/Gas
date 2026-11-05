# Ultimo report — 2026-11-05 — fetta 43 parte 2 (chat Mani): finestra di 40 s e difese contro il parlato della stanza

## DECISIONI UMANE RICHIESTE

1. Merge della PR #341 (https://github.com/Gasss23/Gas/pull/341): review #676 APPROVATO CON RISERVE e PR nel perimetro, quindi decide l'operatore tramite M1.

## Esito

- **PR #340 (fetta 42, «Sì, signore?»)**: MERGIATA (83f3bcd) col sì dell'operatore, a CI verde. Bot e verifica esterna: APPROVATO CON RISERVE, nessuna ALTA o MEDIA; le riserve nuove sono registrate in stato_progetto.
- **Fetta 43 parte 2**: FATTA (PR #341).
  - Finestra di conversazione di 40 s.
  - Turni senza parola con tetto di 15 s: al tetto non si invia e si chiude.
  - Header `X-Gas-Seguito`; comandi «fine» e «pausa» del server (V15 di M2); un errore in un turno di seguito chiude in silenzio.
  - Suite ascolto 248 passed; 15 mutanti presi.
  - Review #676 APPROVATO CON RISERVE (R-676-1/2/3 BASSE; la R-676-3 è sul server di M2 ed è girata a M1).
  - Il commit di merge su main ha un diff identico a quello rivisto.

## Anomalie

- Funziona del tutto solo quando anche la PR #339 di M2 sarà in main.
