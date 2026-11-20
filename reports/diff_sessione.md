# Diff della sessione — 2026-11-20 — CRM fetta 7 (note basse della PR #386)

Si riscrive a ogni sessione; la storia completa sta in git. Le PR #381 e #386 sono mergiate; questa fotografia copre il ramo ripartito da main 0aa26672.

- `modules/crm/copia_cifrata.py`:
  - `_genitore_assente`: nessuna cartella creata se il disco esterno non c'è;
  - copia locale controllata prima di sostituire quella del giorno;
  - temporaneo del ripristino unico ed esclusivo;
  - file di lavoro come collegamento pendente rifiutati;
  - pulizia delle prove interrotte;
  - `esito_all_avvio` con un tempo massimo.
- `modules/crm/server.py`: `_segna_copia` e `_copia_giornaliera`; l'indicatore segna anche il fallimento della copia locale.
- `modules/crm/__main__.py`: all'avvio usa `esito_all_avvio`.
- `tests/test_unit_crm.py`: due test nuovi.
- `reports/crm/guida.md`, `CLAUDE.md` §10 (non fermarsi ad aspettare il merge), report di fine task, `.claude/agents/memoria_revisore.md`.
