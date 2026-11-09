# Ultimo report — 2026-11-09 — Server voce più sicuro, R8 fetta 1 (chat M2)

## DECISIONI UMANE RICHIESTE

- **Merge della PR di sicurezza: decide l'operatore** (CLAUDE.md §10).
- Scelte per le fette 2 e 3 e soglie della fetta 1: `reports/proposta_voce_sicura.md`.
- R-720-2-M2: un client locale con token vecchio blocca per 15 minuti tutti i client su 127.0.0.1 (scelta prudente da confermare).

## Esito delle fette

- **PR #356**: `MERGIATA` (69d76b9).
- **R8 fetta 1**: `FATTA` — tetto ai tentativi con token sbagliato per IP, tetto alle richieste a testo, avvio rifiutato fuori da 127.0.0.1 senza rete privata dichiarata; proposta scritta. Review #720/#722 APPROVATO CON RISERVE (codice corretto), #723 e #724 APPROVATO.
- Bot #358 V-1 (bind su tutte le interfacce con la rete privata): chiusa — server mai su tutte le interfacce, fuori da 127.0.0.1 solo IPv4 scritto per intero. Review #727/#728 con riserve (MEDIE corrette), #729 APPROVATO. Test: 290 passed.
- Bot #358 su e63491b (BOCCIATO per una MEDIA: mancava il test del blocco senza rete privata): corretta, più «::1» non più locale. Review #730-M2 con riserve BASSE. Test: 291 passed. Decisione per l'operatore: IPv4 d'esempio costruiti da intero nei test (handoff §0).
- Gate IP: esempi IPv4 nei test sostituiti con IPv6 di documentazione; review #726-M2 APPROVATO CON RISERVE (R-726-1/2-M2 BASSE).
- Test: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 276 passed.

## Anomalie

- Nessuna nel codice. Nota di processo: la fetta è stata preparata in locale di notte (branch occupato dalla #356) e riposizionata sopra main dopo il merge; albero identico a quello revisionato.
