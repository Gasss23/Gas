# DIFF SESSIONE — 2026-10-25 (chat Mani, fetta 17, PR #270)

- `modules/web/leggi.py`: dopo un `<frameset>` il resto della pagina si nasconde — flag `_frameset` in `_Estrattore` (acceso in `_inizio`, controllato in `handle_data`, log in `_componi`, titolo scartato) e taglio con log nel ripiego — R-ve261-4, verso sicuro; V-1 bot e ve #270.
- `tests/test_unit_web_leggi.py`: `test_dopo_il_frameset_il_resto_si_nasconde` (10 pagine col titolo prima del frameset, parser e ripiego separati, log di entrambi, XHTML nel parser e nel ripiego).
- `.claude/agents/memoria_revisore.md`: righe delle review #515 e #516 (commit del revisore).
- `reports/stato_progetto.md`: intestazione, #514 e merge di #268 nel blocco della fetta 16, blocco «Mani — fetta 17» col secondo giro e R-516-1.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
