# DIFF SESSIONE — 2026-10-03 — C3: chiusura R-c3-1 + review #126

Range: `ce3d392..HEAD` (merge-base con origin/main). Il branch include anche i commit C3 del 2026-10-02.

| File | Cosa è cambiato e perché |
|---|---|
| `modules/memory/store.py` | C3 (2026-10-02): tabella `approvals` + trigger + metodi coda. Oggi: `_num`/`_approval_row_valida` e diniego fail-closed su righe con tipi errati in get/resolve/pending (R-c3-1). |
| `tests/test_unit_kernel.py` | T73a-g (C3) + T73h: righe corrotte via SQL grezzo → lettura nega, nessun crash (R-c3-1). |
| `.claude/agents/memoria_revisore.md` | Righe #125 e #126 del revisore + lezioni. |
| `reports/stato_progetto.md` | Voce C3 onesta (pronta, non collegata, deferiti a C4), stub C2 ancora attivo, R-c3-1 chiusa, R-c3-1b nuova, PR #109 da chiudere. |
| `reports/ultimo_report.md` | Report del task di oggi. |
| `reports/handoff.md` | Dossier: §4 verdetto #126 verbatim, §4-bis verdetto #125 verbatim (superato). |
| `reports/diff_sessione.md` | Questo file. |

Nota: si riscrive a ogni sessione; la storia completa sta in git.
