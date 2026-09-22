# Diff sessione — 2026-09-23
## FIX promemoria_end.sh — blocco JSON Stop hook

Questa sessione ha implementato la FETTA 1 del fix `/fine-task` automatico.

---

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `.claude/hooks/promemoria_end.sh` | Riscrittura da soft-warning stderr a blocco JSON stdout; aggiunta logica handoff fresco (ultimo commit non-chore), lettura `stop_hook_active` da stdin, filtro `chore(scrivi-rep):` da SESSION_COMMITS, fail-open in tutti i percorsi |
| `tests/test_unit_hooks.py` | 9 test aggiornati/aggiunti per nuova semantica: `_run_promemoria` ora passa stdin JSON, helper `_is_blocked`, test T-prom-1..7 + 3b + 3c su repo git reali |
| `.claude/agents/memoria_revisore.md` | Riga #101 aggiunta dal revisore (APPROVATO) |
| `reports/ultimo_report.md` | Report di fine task (questa sessione) |
| `reports/handoff.md` | Handoff di fine sessione (questa sessione) |
| `reports/diff_sessione.md` | Questo file |

---

## Note

- Suite 34/34 green dopo le modifiche.
- Test e2e manuale confermato su branch temporaneo (mai pushato, eliminato).
- Revisore #101: APPROVATO senza riserve.
