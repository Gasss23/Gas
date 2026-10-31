# DIFF SESSIONE — 2026-10-31 — Mani, fetta 33: browser senza schermo dietro il proxy filtrante

File toccati rispetto a main 9fdbd2b (PR #312 e #314 mergiate; main portato nel branch con un merge, conflitto solo nella memoria):
- `modules/web/browser.py` — nuovo: `leggi_con_browser`, Chromium senza schermo in un processo figlio con la rete solo dal proxy. Motivo: R6, piano approvato dall'operatore.
- `modules/web/leggi.py` — cornice NON FIDATO in `_incornicia` ed estrazione in `_estrai`; pagina vuota riprovata nel browser se acceso.
- `modules/web/proxy.py` — testa della risposta riscritta con Connection: close, intestazioni nominate in Connection tolte, «200» del tunnel nel tetto, segno X-Gas-Proxy, stati 100–599.
- `tests/test_unit_web_browser.py` — nuovo: 25 test con origine finta e Chromium vero.
- `tests/test_unit_web_proxy.py` — 16 test nuovi per le risposte, Connection e il tunnel.
- `tests/test_unit_web_leggi.py` — un patch da `_componi` a `_estrai`.
- `.github/workflows/ci.yml` — env NODE_PATH e browser obbligatorio nel passo web.
- `.claude/agents/memoria_revisore.md` — righe delle review dalla #593 alla #596.
- `reports/stato_progetto.md` — blocco «Mani — fetta 33» e riga «Ultimo aggiornamento».
- `reports/roadmap.md` — R6: proxy e browser fatti, manca bwrap.
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
