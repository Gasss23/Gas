# Diff sessione — fix/t9a-deterministico (2026-07-24)

> Riscritto a ogni sessione. La storia completa sta in git.
> Range: 55959ef..HEAD (fork da origin/main)

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `tests/test_unit_kernel.py` | Iniettate chiavi fittizie GEMINI/GROQ nel blocco T9 con save/restore; rimosso gate `_has_live_keys`; T9a e T9c diventano `check(...)` incondizionali → da 2 SKIP a 0 SKIP in CI |
| `.github/workflows/ci.yml` | Solo commenti: dichiarata divergenza Python 3.11 CI vs 3.12.3 WSL; aggiornata descrizione T9a/T9c nel summary e nel gate sandbox |
| `.claude/agents/memoria_revisore.md` | Aggiunta riga #59 (APPROVATO, nessuna lezione nuova) |
| `reports/stato_progetto.md` | 9 punti canonici aggiornati con dati live: review counter #59, R-ci-summary chiuso, R-ci-openrouter chiuso+storia, lezione T9b, PR #40/#41 in riga CI, head origin=5, §7 venv WSL, errore 247 PASS dichiarato, azioni senza traccia git |
| `reports/ultimo_report.md` | Report task di questa sessione |

## Azioni senza traccia in git

- `pip install -r requirements.txt -r requirements-dev.txt` nel venv WSL (Python 3.12.3) — 2026-07-24
