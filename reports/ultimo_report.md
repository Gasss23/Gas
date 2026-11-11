# Ultimo report — 2026-11-11 — ascolto più severo di default: zero risposte non richieste (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #371 (https://github.com/Gasss23/Gas/pull/371): review APPROVATO (riserve BASSE); merge secondo CLAUDE.md §10 (verdetto del bot sull'head), dopo il via di M1.
2. Al mattino: provare «Hey Jarvis» dal vivo; se non scatta più, `GAS_ASCOLTO_SOGLIA=0.6` o `GAS_ASCOLTO_BLOCCHI_PAROLA=2` nel .env. Lanciare i 3 comandi di lettura del log mandati a M1.

## Esito

- **PR #368 (richiesta d'un fiato)**: MERGIATA da M1 (904d9d6).
- **Default più severi (priorità ALTA dell'operatore)**: FATTA. Soglia 0,7, 3 blocchi di fila, turni di seguito spenti, finestra 10 s, interruzione 0,8; un'interruzione apre ancora la nuova domanda. Test dell'ascolto 317 passed. Review #757-M1 APPROVATO CON RISERVE (MEDIA chiusa) e #758-M1 APPROVATO.
- **Bot #371 (2 MEDIA)**: FATTA. L'interruzione mentre Gas parla vuole ora la parola su 3 blocchi di fila come fuori (b36c944, review #759-M1 APPROVATO CON RISERVE BASSE); merge di main dopo la #369 (881c4bb, review #760-M1 APPROVATO). Test 319 passed.
- **Lettura dei log del Mac**: DEFERITA — l'operatore dorme, l'ascolto è in pausa.

## Anomalie

Nessuna.
