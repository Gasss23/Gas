# Ultimo report — 2026-11-07 — fetta 44 (chat Mani): riserve dell'ascolto, proposta «Hey Gas», riserve della PR #341

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 44 (review #702/#703 APPROVATO CON RISERVE, solo BASSE): decide l'operatore tramite M1.
2. «Hey Gas» (reports/proposta_parola_gas.md): si può addestrare in circa 1 ora su Colab senza cambiare codice. La licenza dei dati negativi e l'italiano sono da valutare. Decidere se procedere e se aggiungere il verificatore personale.

## Esito

- **PR #341**: MERGIATA (c1a4503) il 2026-11-07, col sì dell'operatore e il rischio R-694-1/R-695-2 accettato. Prima del merge ho dovuto unire main altre due volte, con le PR #344 e #345 di M2 (review #697 e #701 APPROVATO).
- **Fetta 44**: FATTA.
  - riprendi.sh controlla che l'ascolto resti acceso e mostra l'errore all'ultimo tentativo;
  - pausa.sh dice «non installato»;
  - eco quando Gas dice «Hey Jarvis»;
  - V-2/V-3/V-4 della #341.
- **Riserve della #341**: FATTE.
  - La finestra va da 0 a 120 s, come la pagina web.
  - Ridire la parola nella finestra fa ripartire il conto dei turni.
  - Dopo «Hey Jarvis» detto nella finestra (senza bip) si può fare una pausa fino a 5 s; rumori brevi non tengono aperta la registrazione (R-702-1).
- Test: suite ascolto da 257 a 283 passed; 6 mutanti presi.
- Review #702 e #703 APPROVATO CON RISERVE: resta R-702-2 BASSA, da provare sul Mac.
