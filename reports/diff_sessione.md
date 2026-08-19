# Diff sessione — 2026-08-19
## Branch: fase4/check-verdetto-fail-closed

File toccati (da `git diff --stat BASE..HEAD`, BASE=9f67dfe):

| File | Perché |
|------|--------|
| `.claude/agents/memoria_revisore.md` | Aggiunta lezione review #80/#81 (sessione precedente) + #82 (questa sessione) |
| `.claude/commands/fine-task.md` | Passo 4 aggiornato: git add ora include memoria_revisore.md e .gas_history.json (set completo) |
| `.claude/hooks/review_gate.sh` | fix: fail-closed su git-diff failure e cd impossibile (56c2d11) |
| `.claude/hooks/session_end.sh` | FETTA 1: rimosso auto-commit, rimane solo push fail-safe condizionale |
| `CLAUDE.md` | Sez.3 aggiornata: descrizione hook SessionEnd corretta (R1 review #82) |
| `reports/diff_sessione.md` | Questo file (riscritto ogni sessione) |
| `reports/handoff.md` | Rigenerato con set reale 11 file |
| `reports/stato_progetto.md` | Aggiornato stato review/suite + riserve FETTA 1 |
| `reports/ultimo_report.md` | Report fine task di questa sessione |
| `tests/test_unit_hooks.py` | R-voice-3 (test Content-Length:abc→400) + T-hook-b/d/f aggiornati per nuovo contratto session_end |
| `tests/test_unit_voice_server.py` | R-voice-3: test esplicito Content-Length non numerico → 400 |
