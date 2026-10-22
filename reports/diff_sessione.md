# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 8)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_Estrattore.parse_html_declaration` (CDATA in HTML come commento fasullo fuori da svg/math), `_Estrattore.set_cdata_mode` (niente testo grezzo in XHTML), ripiego allineato, commento sul limite dei parser vecchi.
- `tests/test_unit_web_leggi.py` — CDATA in HTML, XHTML con grezzi annidati e titolo con tag (199 test).
- `.claude/agents/memoria_revisore.md` — riga #463 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 8».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
