# Ultimo report — 2026-11-09 — Voce, velocità: frasi fisse divise in cache (chat M2)

## DECISIONI UMANE RICHIESTE

- Nessuna per questa PR. Dalla #358: marcatore `gasmerge-ip-ok` per gli IPv4 d'esempio sì/no; controllo dell'interfaccia del tunnel prima del VPS.

## Esito delle fette

- **PR #358 (sicurezza del server voce)**: `MERGIATA` (567beb7).
- **Frasi fisse divise in cache**: `FATTA` — anche nelle risposte a pezzi le frasi fisse vengono dalla memoria. Review #725-M2 e #735-M2 APPROVATO.
- Test: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 314 passed.

## Anomalie

- Nessuna. Fetta preparata in locale di notte e riposizionata sopra main (patch identica a quella revisionata).
