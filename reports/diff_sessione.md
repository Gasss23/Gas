# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 12)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_parser_aggiornato` (funzione pura) e warning una volta se il parser è vecchio; `_fine_script` (stati script data escaped / double escaped) e `_FineScriptTrovata` al posto della regex di html.parser; `parse_comment` per `<!-->`/`<!--->`; in XHTML `_commenti_e_cdata_xml` toglie anche PI e DOCTYPE, con `_fine_doctype` che legge il DOCTYPE come l'XML.
- `tests/test_unit_web_leggi.py` — marcatore `solo_parser_aggiornato`, test del rilevatore e dell'avviso, doppio escape, PI e DOCTYPE, commenti vuoti, posizione dalla fine (351 test).
- `.claude/agents/memoria_revisore.md` — righe #482, #483, #484 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 12».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
