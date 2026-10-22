# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 9)

> Si riscrive a ogni sessione; la storia completa sta in git. Finché la PR #245 non è mergiata, il diff verso main contiene anche la fetta 8.

- `modules/web/leggi.py` — `_Contesto` (pila degli elementi aperti dentro svg/math con lo spazio, punti di integrazione, uscita dal contenuto estraneo, chiusure come nello standard), `_esito_autochiuso` condiviso, `_Estrattore` con `_locale` (XHTML) e contesto, ripiego con lo stesso contesto; `parse_html_declaration` con `cdata_vero()`.
- `tests/test_unit_web_leggi.py` — nodo corrente, uscite e autochiusi in svg/math, XHTML con prefissi, chiusure attraverso elementi svg; vecchi casi portati alla semantica dei browser (264 test).
- `.claude/agents/memoria_revisore.md` — righe #467, #468, #469 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 9».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
