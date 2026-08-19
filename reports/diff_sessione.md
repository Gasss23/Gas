# DIFF SESSIONE — 2026-08-19 (R2 durabilità memoria revisore)

Branch: `fix/r2-durabilita-memoria`
Base: `c6cf632` (merge PR #64, origin/main)

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `scripts/commit_memoria_revisore.sh` | NUOVO — script bash per commit atomico path-scoped (`git commit -o`) di `memoria_revisore.md`; FAIL-SAFE §9; estrae review# e verdetto dall'ultima riga del file |
| `.claude/agents/revisore.md` | Aggiunta sezione "Commit atomico R2": istruzione al revisore di chiamare `commit_memoria_revisore.sh` dopo ogni riga contatore |
| `.claude/agents/memoria_revisore.md` | Aggiunta riga contatore #85 (dogfooding R2 dal revisore: APPROVATO CON RISERVE) |
| `tests/test_unit_hooks.py` | Aggiunta classe `TestCommitMemoriaRevisore` con 4 test reali (T-R2-a/b/c/d) su repo temporanei; suite 15→19 PASS |
| `reports/stato_progetto.md` | Aggiornato: R2 CHIUSA, review count 82→85, finding R2 marcato ✅ |
| `reports/ultimo_report.md` | Riscritto: report task R2 con §1–§5 |
| `reports/handoff.md` | Riscritto: dossier fine sessione con §2 a 11 file (fix check_handoff CI failure) |
| `reports/diff_sessione.md` | Riscritto: questa sessione |
| `scripts/check_handoff.py` | Fix `core.quotePath=false` non-ASCII (sessione precedente, Fetta B) |
| `scripts/check_verdetto.py` | Fix `core.quotePath=false` non-ASCII (sessione precedente, Fetta B) |
| `tests/test_unit_handoff_check.py` | Test non-ASCII `check_handoff` (sessione precedente, Fetta B) |
