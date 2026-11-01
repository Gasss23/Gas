# DIFF SESSIONE — 2026-11-01 — Mani, fetta 34: browser senza schermo dentro bwrap

File toccati rispetto a main 0f02868 (PR #315 mergiata):
- `modules/web/browser.py` — node e Chromium in bwrap (namespace nuovi, nessuna capability, cartelle sensibili nascoste, percorsi da ri-esporre controllati), ponte verso il proxy su socket Unix, casa in sola lettura e profilo in un tmpfs con tetto, Worker spenti, routeWebSocket obbligatorio, una sola uccisione. Motivo: punto 4 del piano R6.
- `modules/web/proxy.py` — modalità con socket Unix 0600 (`percorso=`).
- `tests/test_unit_web_browser.py` — test del sandbox (rete, file, socket, capability, tetti, collegamenti, PID namespace, sonda), Worker e iframe, pulizia indipendente.
- `tests/test_unit_web_proxy.py` — test del socket Unix.
- `.claude/agents/memoria_revisore.md` — righe delle review dalla #599 alla #605.
- `reports/stato_progetto.md` — blocco «Mani — fetta 34» e riga «Ultimo aggiornamento».
- `reports/roadmap.md` — R6: bwrap fatto.
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
