# DIFF SESSIONE — 2026-10-30 — Mani, fetta 30: gli invisibili citati dal bot come <U+XXXX>

File toccati rispetto a main 95be7b1 (PR #306 mergiata):
- `.github/workflows/verifica-bot.yml` — nel PROMPT del bot, nuova regola: ogni carattere invisibile o di controllo citato si scrive come <U+XXXX>, mai il carattere vero. Motivo: falso NO di #297 e compromesso V-2 della terza verifica esterna su #305.
- `scripts/bot_esito.py` — `contiene_segreti` cerca anche senza le citazioni <U+XXXX> (V-1 verifica esterna #309).
- `tests/test_unit_verifica_bot.py` — assert che fissa la regola nel PROMPT (R-580-1, V-1 bot #309) e test sulle credenziali spezzate da una citazione.
- `.claude/agents/memoria_revisore.md` — righe delle review #580, #581 e #582.
- `reports/stato_progetto.md` — blocco «Mani — fetta 30» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
