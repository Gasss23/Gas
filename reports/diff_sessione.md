# Diff sessione — 2026-08-13

## File toccati

| File | Tipo | Descrizione |
|---|---|---|
| `modules/voice/__init__.py` | NUOVO | Package marker vuoto |
| `modules/voice/server.py` | NUOVO | Endpoint HTTP voice (172 righe) |
| `tests/test_unit_voice_server.py` | NUOVO | Suite pytest 18 test |
| `.github/workflows/ci.yml` | MODIFICATO | Aggiunto step voice suite + summary |
| `reports/ultimo_report.md` | AGGIORNATO | Report fetta |
| `reports/stato_progetto.md` | AGGIORNATO | Stato motore + finding |
| `reports/diff_sessione.md` | AGGIORNATO | Questo file |
| `reports/handoff.md` | AGGIORNATO | Dossier di sessione |

## Cosa è cambiato e perché

**`modules/voice/server.py`** — implementazione dell'endpoint `POST /voice`. Avvolge `GasKernel.run_turn()` già accertato dalla sonda fetta 0 (b47e1bd). Decisioni architetturali già prese dall'operatore: stdlib `http.server`, single-thread nativo (serializzazione implicita = nessun lock), zero dipendenze. Sicurezza fail-closed: token `GAS_VOICE_TOKEN` obbligatorio all'avvio, confronto a tempo costante `hmac.compare_digest`. Log eventi AUTH FAIL con IP, mai il token. Fail-safe §9: eccezione in `run_turn` → 500 + log, server vivo. Fix post-review #74: `Content-Length` non numerico → 400 (era EOF).

**`tests/test_unit_voice_server.py`** — 18 test reali (nessun output simulato): avvio senza token, auth mancante/errata (token assente nei log), token corretto, eccezione run_turn, singleton kernel, edge case 400/405. Fix post-review #74: dead code in TV1 rimosso.

**`.github/workflows/ci.yml`** — aggiunto step `Run voice server suite` (pytest, sempre, con tee su `RUNNER_TEMP/voice_output.txt`) e relativa riga nel job summary.

## File non toccati

`gas.py`, `brains/`, `modules/memory/`, `modules/telegram/` — stop gate rispettati. `gas voice` CLI entry non aggiunta (richiede toccare gas.py → proposta per fetta successiva).
