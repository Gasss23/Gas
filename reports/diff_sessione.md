# DIFF SESSIONE — 2026-10-29 — Mani, fetta 29: test del bot dopo la terza verifica esterna su #305

File toccati rispetto a main 52c113b (PR #305 e #307 mergiate; main portato nel branch con un merge, solo conflitti nei report):
- `tests/test_unit_verifica_bot.py` — test positivo sul titolo con un invisibile, ogni controllo bidi provato da solo, uguaglianza degli intervalli invisibili col gate. Motivo: V-1 e V-3 della terza verifica esterna su #305 (due mutanti sopravvivevano).
- `.claude/agents/memoria_revisore.md` — righe delle review #576, #577 e #578 (il merge di main).
- `reports/stato_progetto.md` — blocco «Mani — fetta 29» (con V-2 registrata come compromesso) e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
