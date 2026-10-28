# ULTIMO REPORT — 2026-10-28 — chat Motore: interruttore del forte tra shell e .env (PR #293)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #293 (https://github.com/Gasss23/Gas/pull/293): la review #543 è APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10).

## Esito
- **PR #290**: chiusa senza merge, su «ok» dell'operatore. Era un doppione della #291 (stessa fetta fatta da un'altra sessione, già su main).
- **WARN del doctor su GAS_CLAUDE_CLI della shell e del .env non coincidenti**: FATTA, in tutti e due i versi.
  - Forte acceso nella shell ma non dal `.env` (V-3 del bot su #290).
  - Forte spento nella shell ma il `.env` ha un altro valore (V-1 della verifica esterna su #290).
  - Il nuovo `_DOTENV_SCAVALCATE` contiene solo i nomi delle variabili, mai i valori.
- **Test**: suite kernel da 1061 a 1063 PASS, 0 FAIL (main misurato in un worktree a `2f35bc6`). pytest `test_unit_dotenv`: 12 passati.

## Anomalie
- Due sessioni «chat Motore» lavorano sulla stessa RIPARTENZA: oggi ci sono stati due doppioni (#286 e #287, #290 e #291). L'ho segnalato all'operatore.
