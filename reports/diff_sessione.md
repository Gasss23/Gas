# DIFF SESSIONE — 2026-10-27 (chat Mani, fetta 19, PR #275)

- `modules/web/lexbor.py` (nuovo): lettura del testo visibile con lexbor in un processo figlio (tempo e memoria limitati), spenta per default (`GAS_WEB_LEXBOR=1`), sonda del figlio, fail-safe sulla lettura di sempre — R-ve246-5 in prova.
- `modules/web/leggi.py`: lettura con html.parser estratta in `_testo_e_titolo` senza cambiarla; `_componi` prova lexbor se acceso e non XHTML; docstring con l'eccezione «in prova» e il caso peggiore da accesa (R-520-2).
- `tests/test_unit_web_lexbor.py` (nuovo): 22 test (spenta per default, casi R-ve246-5, titolo, pulizia e tetti, tempo massimo, figlio rotto, sonda, XHTML, isolamento del figlio con `-I`, ambiente vuoto e tetto di memoria); saltati senza selectolax.
- `.claude/agents/memoria_revisore.md`: righe delle review #520-#524 della chat Mani (commit del revisore).
- `reports/stato_progetto.md`: intestazione (unita a mano col merge di main), merge di #272, blocco «Mani — fetta 19» con le misure, il secondo giro e le riserve.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
