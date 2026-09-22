# Diff sessione — 2026-09-22/23
## Autonomia #1 "Studia/Comprendi" — K0+K1+K2

File toccati (BASE = 060beae, merge-base origin/main):

| File | Cambio | Motivo |
|------|--------|--------|
| `knowledge/sources.yaml` | +21 righe (nuovo) | K0: catalogo fonti fidate YAML |
| `knowledge/test_source.txt` | +38 righe (nuovo) | K0: fonte test locale per validare pipeline |
| `tools/ingest_knowledge.py` | +268 righe (nuovo) | K1+K2: schema .gas_knowledge.db + CLI ingest idempotente |
| `.gitignore` | +4 righe | Aggiunta esclusione `.gas_knowledge.db` + WAL/SHM |
| `requirements.txt` | +1 riga | Aggiunta `pyyaml>=6.0` (era già installata nel .venv) |
| `reports/stato_progetto.md` | +3 righe | Aggiunta entry K0+K1+K2 completati |
| `reports/ultimo_report.md` | riscritto | Report task + struttura fine-task (DECISIONI, fette FATTA/DEFERITA) |
| `reports/handoff.md` | riscritto | Handoff sessione corrente con CI failure documentata |
| `reports/diff_sessione.md` | riscritto | Questo file |

Nota: `.gas_knowledge.db` creato localmente dal test ma escluso dal repo via `.gitignore`.
