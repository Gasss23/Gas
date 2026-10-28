# DIFF SESSIONE — 2026-10-28 — Mani fetta 22 (PR #285)

File toccati rispetto a main 0cf1d67 (dopo il merge di main per V-1 ve #285):
- `modules/web/lexbor.py` — `intero()` del figlio: «0», «000», «-0» valgono 0, un negativo non zero None (R-bot280-1, R-536-1); commento col segno (V-2 ve #285).
- `tests/test_unit_web_lexbor.py` — test parametrizzato su `intero()`, presa dal sorgente del figlio con `ast` (gira senza selectolax).
- `.claude/agents/memoria_revisore.md` — righe delle review #536, #537, #538 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 22» e riga «Ultimo aggiornamento» (completata con #538 e i giri dopo bot e verifica esterna: V-1 bot/ve su 116aac3).
- `reports/ripartenza_mani.md` — punto a) fatto, PR #285.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
