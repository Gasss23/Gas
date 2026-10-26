# DIFF SESSIONE — 2026-10-26 (chat Mani, fetta 18, PR #272)

- `modules/web/leggi.py`: noscript testo grezzo nel parser (`_modo_grezzo` in `handle_starttag`) e nel ripiego (`_GREZZI_RIPIEGO`); commenti del flag `con_noscript` e della guardia `_nascosti_html` aggiornati — R-ve261-2, R-517-1.
- `tests/test_unit_web_leggi.py`: `test_noscript_e_testo_grezzo` (9 pagine + XHTML), `test_titolo_resta_se_frameset_non_e_un_tag` (V-1 bot #270), tre casi del vecchio verso sicuro spostati o tolti.
- `.claude/agents/memoria_revisore.md`: righe delle review #517 e #518 (commit del revisore).
- `reports/stato_progetto.md`: intestazione, fetta 17 chiusa col merge, blocco «Mani — fetta 18» con R-518-1.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
