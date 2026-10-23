# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 12)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_parser_aggiornato` (funzione pura) e warning una volta se il parser è vecchio; `_fine_script` (stati script data escaped / double escaped) e `_FineScriptTrovata` al posto della regex di html.parser; `parse_comment` per `<!-->`/`<!--->`; in XHTML `_commenti_e_cdata_xml` toglie anche PI e DOCTYPE, con `_fine_doctype` che legge il DOCTYPE come l'XML, e dopo il DOCTYPE ammette solo un prologo valido; PI solo con nome XML valido; lucchetto dell'avviso.
- `tests/test_unit_web_leggi.py` — marcatore `solo_parser_aggiornato`, test del rilevatore e dell'avviso, doppio escape, PI e DOCTYPE, commenti vuoti, posizione dalla fine, prologo, PI senza nome e mutanti delle verifiche esterne #252 (375 test).
- `.claude/agents/memoria_revisore.md` — righe #482…#489 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 12» con il secondo giro.
- Merge di main 2abc23b (PR #251): entrano `reports/coda_notte.md` e `reports/roadmap.md` della chat Motore.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
