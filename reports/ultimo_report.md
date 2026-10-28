# ULTIMO REPORT — 2026-10-28 — chat Motore: riserve del punto 3 (cervello forte e doctor), PR #290

## DECISIONI UMANE RICHIESTE
1. Merge della PR #290 (https://github.com/Gasss23/Gas/pull/290): la review #542 è APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10).

## Esito
- **R-538-1 (GAS_CLAUDE_BIN solo nella shell)**: FATTA. Il doctor dà WARN se `GAS_CLAUDE_BIN` manca nel `.env` di Gas, se è vuota, o se ha un valore diverso da quello in uso. Questi ultimi due casi sono V-1 della verifica esterna e V-2 del bot.
- **V-3 bot #290 (GAS_CLAUDE_CLI acceso solo nella shell)**: FATTA. Il doctor dà WARN «di notte il forte è spento».
- **V-1 bot #290 (.env della cwd)**: FATTA. C'è un solo percorso, `DOTENV_PATH` (accanto a gas.py), usato sia dal caricamento sia dal doctor.
- **R-538-2 (tetto del motivo)**: FATTA. Il tetto passa da 160 a 300. Correzione della motivazione (V-3 della verifica esterna): `_MSG_LOGIN` è lungo 152 caratteri, quindi il vecchio tetto non lo troncava; il cambio dà solo margine.
- **V-2 bot #287 (prefisso ripetuto)**: FATTA.
- **V-1 bot #287 (falsi WARN)**: FATTA per `/usr/local` su Linux e per i collegamenti, risolti da entrambe le parti (R-540-1, test T99z). `DEFERITA — ~/.zshenv`: l'errore va nel verso prudente.
- **Test**: suite kernel da 1061 a 1066 PASS, 0 FAIL. Il valore di main (1061) è misurato in un worktree a `094eb57`. In CI i conteggi sono più alti di 2 (V-4 del bot, test che dipendono dall'ambiente).

## Anomalie
- Su `6771320` il bot ha dato una MEDIA: l'handoff era fermo a `cceadcc`, perché ho pushato un commit del motore prima del fine-task. Questo fine-task la chiude.
