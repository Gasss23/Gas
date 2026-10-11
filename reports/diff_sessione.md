# DIFF SESSIONE — 2026-10-11, terza fetta (PR #182)

> Fotografia dell'ultima sessione; la storia completa sta in git. Base: main `bc604ae` (merge della PR #181).

| File | Cosa è cambiato e perché |
|---|---|
| `gas.py` | `_vet_letture`: dopo `--` ogni token è un operando; `_vet_opzioni`: date solo con `+formato`/`-d` |
| `modules/gate/gate.py` | `_SEGRETO_RE`/`_nome_da_segreto`: `.env` seguito da qualsiasi cosa (salvo environment/envelope/envoy) illeggibile ovunque |
| `tests/test_unit_gate.py` | casi `*.env` negati e nomi simili leggibili |
| `tests/test_unit_kernel.py` | T83m (solo controllo): `--`, date posizionale |
| `reports/design_cancello.md` | §5b aggiornato |
| `.claude/agents/memoria_revisore.md` | righe #274–#277 del revisore |
| `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | report di fine task |
