# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 9)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_Contesto` (pila degli elementi aperti dentro svg/math con lo spazio, punti di integrazione, uscita dal contenuto estraneo anche con `</p>`/`</br>` e `<font>` con attributi, chiusure come nello standard con strutture O(1), pila «incerta» che nasconde il resto della pagina con un warning nel log), `_esito_autochiuso` condiviso, `_Estrattore` con `_locale` (XHTML) e `_font_esce`, ripiego con lo stesso contesto; `parse_html_declaration` con `cdata()`.
- `tests/test_unit_web_leggi.py` — nodo corrente, uscite e autochiusi in svg/math, XHTML con prefissi, pila incerta, font, tempo lineare, log; vecchi casi portati alla semantica dei browser (291 test).
- `.claude/agents/memoria_revisore.md` — righe #467–#472 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 9» con il secondo giro.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
