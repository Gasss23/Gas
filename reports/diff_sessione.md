# Diff della sessione — 2026-11-20 — CRM fetta 7 (note della PR #386 e del bot sulla PR #387)

Si riscrive a ogni sessione; la storia completa sta in git. Le PR #381 e #386 sono mergiate; questa fotografia copre il ramo ripartito da main 0aa26672 (PR #387).

- `modules/crm/copia_cifrata.py`:
  - `_genitore_assente`: nessuna cartella creata se il disco esterno non c'è; punto di mount vuoto in `/Volumes` riconosciuto (#822); permesso negato e percorso risolto senza maiuscole/minuscole (#823);
  - `copia_fuori`: copia locale controllata prima di sostituire quella del giorno; controlli dentro il try (#823);
  - temporaneo del ripristino unico ed esclusivo; file di lavoro come collegamento pendente rifiutati; pulizia delle prove interrotte;
  - `esito_all_avvio` con un tempo massimo, ATTIVA solo a prova finita (#823);
  - `_integro` in sola lettura (#823).
- `modules/crm/server.py`: `_segna_copia` e `_copia_giornaliera`; l'indicatore segna il fallimento della copia locale anche a copia esterna spenta (#822).
- `modules/crm/__main__.py`: all'avvio usa `esito_all_avvio`.
- `tests/test_unit_crm.py`: cinque test nuovi (#821, #822, #823).
- `reports/crm/guida.md`, `CLAUDE.md` §10 (non fermarsi ad aspettare il merge), `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
