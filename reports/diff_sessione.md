# Diff sessione — 2026-08-19 — fix/r2-riserve-86

Sessione: chiusura riserve R-r2-1 e R-r2-2 da review #86 (R2 durabilità memoria revisore).

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `scripts/commit_memoria_revisore.sh` | Forma atomica `if ! REPO_ROOT=$(cmd)` a riga 21-22 (R-r2-1, lezione #51). Nessuna modifica di logica. |
| `tests/test_unit_hooks.py` | Aggiunto T-R2-e: "mem PRESENTE + dir NON-git → git commit fallisce → WARN + exit 0" (R-r2-2, copre path riga ~75 dello script). |
| `.claude/agents/memoria_revisore.md` | Riga review #87 APPROVATO aggiunta dal subagent revisore. |
| `reports/ultimo_report.md` | Report del task con sezione DECISIONI UMANE RICHIESTE. |
| `reports/handoff.md` | Dossier di fine sessione (questo file). |
| `reports/diff_sessione.md` | Riepilogo diff sessione (questo file). |
| `reports/stato_progetto.md` | Aggiornato: riserve R-r2-1/R-r2-2 chiuse, review #87 APPROVATO. |
