# diff_sessione — 2026-10-02 — chore/hook-fine-task-obbligatorio

File toccati (da git diff --stat 9f6dfd7..HEAD):

| File | Motivo |
|---|---|
| `.claude/agents/memoria_revisore.md` | Review #122 (BOCCIATO) e #123 (APPROVATO) aggiunte in coda |
| `.claude/commands/fine-task.md` | §4bis chiama bash scripts/fine_task_finale.sh; §5 rimuove cat handoff |
| `.claude/hooks/promemoria_end.sh` | Contatore per-sessione (B1), worktree-safe path (R4), WARN su log (R5) |
| `CLAUDE.md` | Regola reporting: URL_HANDOFF sostituisce cat integrale handoff |
| `scripts/fine_task_finale.sh` | Nuovo: gate A/B/IP + push + URL_HANDOFF deterministico |
| `tests/test_unit_hooks.py` | +2 nuovi test (T-prom-counter-session, T-finale-3b), fix T-finale-3 e T-finale-4 |
