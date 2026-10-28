# ULTIMO REPORT — 2026-10-28 — chat Motore: riserve del punto 3 (cervello forte e doctor)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #290 (https://github.com/Gasss23/Gas/pull/290): la review #540 è APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10).

## Esito
- **R-538-1 (GAS_CLAUDE_BIN solo nella shell)**: FATTA. Il doctor dà un WARN se la variabile manca nel `.env`. La nuova `_chiavi_dotenv` legge solo i nomi delle variabili, mai i valori.
- **R-538-2 (motivo troncato)**: FATTA. Il tetto passa da 160 a 300 caratteri, quindi il messaggio del login arriva intero.
- **V-2 bot #287 (prefisso ripetuto)**: FATTA. Il motivo è senza «claude-cli: »; «429 » resta.
- **V-1 bot #287 (falsi WARN)**: FATTA in parte.
  - FATTI: `/usr/local/bin` e `/usr/local/sbin` contano su Linux (systemd); il confronto vale anche coi collegamenti risolti.
  - DEFERITO: il PATH di `~/.zshenv`, perché sbaglia nel verso prudente (dà un WARN in più, mai un OK sbagliato).
- **Test**: suite kernel da 1061 a 1064 PASS, 0 FAIL (main misurato in un worktree a `094eb57`); pytest 2282 passati, 61 saltati.

## Anomalie
- Nessuna.
