# DIFF SESSIONE — 2026-06-23

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni sessione.

**Tema:** infrastruttura di osservabilità di fine sessione — CI (FETTA 1) + handoff (FETTA 2).
Task NON-motore: `gas.py`/`brains/`/`modules/`/`tests/` INVARIATI → revisore non applicabile.

## File toccati

| File | Stato | Cosa / perché |
|------|-------|---------------|
| `.github/workflows/ci.yml` | NUOVO | Workflow GitHub Actions: `on: push`, ubuntu-latest, Python 3.11, installa `requirements.txt`, lancia `tests/test_unit_kernel.py`. Verde/rosso via exit code nativo. ZERO token LLM (niente API key/secrets/provider/doctor). bwrap non installato in v1. |
| `requirements.txt` | mod | Aggiunto `onnxruntime>=1.17` esplicito (backend fastembed) → in CI i blocchi vettoriali T30/T31/T32 non si saltano (R-reidx-deps). |
| `reports/handoff.md` | NUOVO | Istituzione D: dossier di fine sessione, compilato su questa sessione come primo esempio reale. AGGREGA `ultimo_report.md` + stato CI; non lo sostituisce. |
| `CLAUDE.md` | mod | §3: aggiunta istituzione D (handoff.md), "tre"→"quattro" istituzioni di processo. |
| `reports/stato_progetto.md` | mod | Riga "D — reports/handoff.md" + entry datata 2026-06-23 in testa. |
| `reports/ultimo_report.md` | mod | Report del task (fonte di verità). |
| `reports/diff_sessione.md` | mod | Questo file. |

## Commit della sessione

```
0eb5322 ci: workflow GitHub Actions per la suite unit a ogni push (zero token LLM)
d135bc7 docs(handoff): istituzione D — reports/handoff.md + aggancio in CLAUDE.md §3
```
(+ commit finale dei report — vedi git log vivo.)

## Sonda (FASE 0), in breve
- `requirements.txt`: c'era, dichiarava numpy+fastembed, non onnxruntime esplicito → aggiunto.
- Exit code suite: `sys.exit(1 if FAIL else 0)` → exit=1 sui FAIL (verificato). CI si fida dell'exit code, nessun tocco a `tests/`.
- WSL2 NON accessibile (nessuna distro) → prima run CI = unica sonda Linux.
- Python venv: 3.11.9.

## Decisione umana aperta
Verificare la PRIMA RUN CI su GitHub Actions (verde/rosso + PASS/FAIL/SKIP). Se i FAIL
ambientali (bwrap/env) persistono su Linux, gestirli è un task separato che tocca `tests/`
(con revisore) — NON fatto qui.
