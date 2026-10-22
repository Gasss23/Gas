# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 8)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_Estrattore.parse_html_declaration` (CDATA in HTML come commento fasullo fuori da svg/math), `_Estrattore.set_cdata_mode` (niente testo grezzo in XHTML), ripiego allineato, commento sul limite dei parser vecchi; secondo giro: ogni `<![` gestito dall'override senza super() (V-1 bot #245), `_Estrattore.close()` che scarta un costrutto aperto a fine pagina (R-464-1), `_COSTRUTTO_APERTO`, `_PARSER_AGGIORNATO` (html.parser vecchio → ripiego, R-465-1).
- `tests/test_unit_web_leggi.py` — CDATA in HTML, XHTML con grezzi annidati e titolo con tag; secondo giro: sezioni marcate su ogni html.parser (anche vecchio simulato), costrutti aperti a fine pagina, parser vecchio → ripiego (239 test).
- `.claude/agents/memoria_revisore.md` — righe #463, #464, #465, #466 (chat Mani).
- `reports/stato_progetto.md` — blocchi «Mani — fetta 8» e «fetta 8, secondo giro».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
