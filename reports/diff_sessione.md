# DIFF SESSIONE — 2026-10-29 — Mani, fetta 28: `bot_esito.py` e i caratteri invisibili

File toccati rispetto a main 8424698 (PR #303 mergiata da M1):
- `scripts/bot_esito.py` — i caratteri invisibili si tolgono prima di decidere (la gravità nascosta blocca), i controlli bidi restano un NO, nella review pubblica ogni invisibile si vede come «<U+XXXX>», credenziali spezzate da un invisibile non pubblicate. Motivo: falso NO definitivo su #297.
- `tests/test_unit_verifica_bot.py` — test per gli invisibili Cf e non Cf, i controlli bidi, il caso #297, le riserve pubblicate e le credenziali spezzate.
- `.claude/agents/memoria_revisore.md` — righe delle review #569 e #570.
- `reports/stato_progetto.md` — blocco «Mani — fetta 28» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto g): fatta la (c).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
