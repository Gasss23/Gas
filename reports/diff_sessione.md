# DIFF SESSIONE — 2026-10-25 (chat Mani, fetta 17, PR #270)

- `modules/web/leggi.py`: dopo un `<frameset>` il resto della pagina si nasconde — flag `_frameset` in `_Estrattore` (acceso in `_inizio`, controllato in `handle_data`, log in `_componi`) e taglio con log nel ripiego — R-ve261-4, verso sicuro.
- `tests/test_unit_web_leggi.py`: `test_dopo_il_frameset_il_resto_si_nasconde` (9 pagine, parser e ripiego separati, log di entrambi, pagina XHTML).
- `.claude/agents/memoria_revisore.md`: riga della review #515 (commit del revisore).
- `reports/stato_progetto.md`: intestazione, #514 e merge di #268 nel blocco della fetta 16, blocco «Mani — fetta 17».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
