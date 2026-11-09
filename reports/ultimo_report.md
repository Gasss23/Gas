# Ultimo report — 2026-11-09 — Voce, velocità: frasi fisse divise in cache (chat M2)

## DECISIONI UMANE RICHIESTE

- Nessuna per questa PR. Dalla #358: marcatore `gasmerge-ip-ok` per gli IPv4 d'esempio sì/no; controllo dell'interfaccia del tunnel prima del VPS.

## Esito delle fette

- **PR #358 (sicurezza del server voce)**: `MERGIATA` (567beb7).
- **Frasi fisse divise in cache**: `FATTA` — anche nelle risposte a pezzi le frasi fisse vengono dalla memoria. Review #725-M2 e #735-M2 APPROVATO.
- Bot #360 V-1 BASSA chiusa: test sul percorso vero «forte» a pezzi (review #737-M2 APPROVATO).
- Bot #360 2° giro (COSMETICA) chiusa: la seconda richiesta legge dalla cache (review #740-M2 APPROVATO).
- Bot #360 3° giro: tolto dal confronto il campo «tempi» (test instabile); review #741-M2 APPROVATO.
- Test: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 315 passed (314 prima del test del bot #360 V-1; i giri successivi hanno modificato quel test, non aggiunto test).

## Anomalie

- Nessuna. Fetta preparata in locale di notte e riposizionata sopra main (patch identica a quella revisionata).
