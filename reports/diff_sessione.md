# DIFF SESSIONE — 2026-11-01 — Mani, fetta 35: sandbox del browser con radice vuota ed elenco di cartelle permesse

File toccati rispetto a main 87f576c (PR #316 mergiata):
- `modules/web/browser.py` — `_comando_bwrap` con radice vuota rimontata in sola lettura ed elenco `_PERMESSE`; ri-esposti solo il file di node, i due pacchetti di Playwright e Chromium; sonda = il comando vero con «true»; nessuna cache dei fallimenti; /dev in sola lettura; permesse-collegamento rifatte come collegamenti. Motivo: prima condizione della roadmap per accendere il browser.
- `tests/test_unit_web_browser.py` — test di isolamento riscritti (ogni file visibile contro un elenco, tetti dei tmpfs, Gas e home dentro una permessa, rifiuti, sonde), test di routeWebSocket, rilevatore di pytest su argv.
- `.claude/agents/memoria_revisore.md` — righe delle review dalla #607 alla #610.
- `reports/stato_progetto.md` — blocco «Mani — fetta 35» e riga «Ultimo aggiornamento».
- `reports/roadmap.md` — prima condizione fatta, resta la prova sul VPS.
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
