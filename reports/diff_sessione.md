# Diff Sessione — 2026-08-19

> Fotografia dell'ultima sessione. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `.github/workflows/ci.yml` | Aggiunto job `handoff-check` (check_handoff.py) e `verdetto-check` (check_verdetto.py); aggiunto `unit-suite` per voice (`pytest tests/test_unit_voice_server.py`) |
| `.claude/agents/memoria_revisore.md` | Aggiunte review #76, #77, #78 (voice endpoint + merge resolution) |
| `modules/voice/__init__.py` | File vuoto per rendere `modules/voice/` un package Python |
| `modules/voice/server.py` | Nuovo: endpoint HTTP `POST /voice`, bearer auth, kernel singleton, fail-safe §9, try/except ValueError su Content-Length |
| `tests/test_unit_voice_server.py` | Nuovo: 18 test per il server voice (TV1–TV7), incluso fix R1+R2 da review #76 |
| `reports/handoff.md` | §4 ripristinato con verdetti #76/#77 verbatim e citazioni verificate a HEAD; rimosso "nessun diff motore" (falso); #78 senza path:riga a file fuori dal diff |
| `reports/stato_progetto.md` | Aggiornato ultimo aggiornamento con task corrente |
| `reports/ultimo_report.md` | Report di fine task (task §4 onesto) |
| `reports/diff_sessione.md` | Questo file |

## Note

- Il ramo voice (`bf04d18`) porta tutto il codice motore (18 test, 172 righe server).
- Il merge commit `02ebb9a` ha introdotto §4 con citazione `gasmerge.sh:102-109` (path
  non nel diff di sessione) che faceva fallire `check_verdetto.py`. Corretta in `f7dedeb`.
- In questo commit, §4 è stato ulteriormente corretto: rimossa la scorciatoia "nessun diff motore"
  e rimessi i verdetti #76/#77 verbatim con citazioni verificabili (4 riferimenti, tutti OK a HEAD).
