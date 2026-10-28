# Ultimo report — 2026-10-28 (chat Motore)

**Task:** il report della notte dice perché il cervello forte è fallito; `gas doctor` avvisa se `claude` si trova solo nel PATH del terminale (PR #287).

## DECISIONI UMANE RICHIESTE
1. Merge della PR #287 (https://github.com/Gasss23/Gas/pull/287): review #538 APPROVATO CON RISERVE, quindi serve il «sì» dell'operatore (CLAUDE.md §10).

## Esito
- **Fetta 1 — motivo vero dell'errore del forte**: FATTA. `_motivo_forte` in `gas.py` porta nella riga «Pipeline esausta» (e nel report della notte) il messaggio fisso di `brains/claude_cli.py`, al posto di «RuntimeError». Solo RuntimeError che iniziano con «claude-cli: », prima riga, al massimo 160 caratteri. `claude` non trovato ora suggerisce GAS_CLAUDE_BIN; nuovo caso «non eseguibile» (PermissionError).
- **Fetta 2 — avviso del doctor**: FATTA. `_claude_solo_nel_terminale`: WARN se GAS_CLAUDE_BIN non è un percorso assoluto e `claude` sta fuori da /usr/bin, /bin, /usr/sbin, /sbin e dal venv di Gas; il messaggio indica `GAS_CLAUDE_BIN=<percorso>` da mettere nel `.env`.
- Test: T99s–T99v nel kernel (1053 → 1057 PASS, 0 FAIL); pytest 2265 passed, 61 skipped.
- Review #538 APPROVATO CON RISERVE: R-538-1 BASSA, R-538-2 COSMETICA (tracciate in `stato_progetto.md`).

## Anomalie
- `gh` nel container non è autenticato: PR creata e CI letta con gli strumenti GitHub della sessione.
- Non provato sotto launchd sul Mac: la prova vera è il giro notturno del 29.
