# Diff sessione — 2026-08-13

## File toccati

(da `git diff --stat BASE..HEAD`, BASE = b47e1bd)

| File | Tipo | Descrizione |
|---|---|---|
| `.claude/agents/memoria_revisore.md` | MODIFICATO | Aggiunte lezioni review #74 e #75 |
| `.github/workflows/ci.yml` | MODIFICATO | Aggiunto step `Run voice server suite` + riga summary |
| `modules/voice/__init__.py` | NUOVO | Package marker vuoto |
| `modules/voice/server.py` | NUOVO | Endpoint HTTP `POST /voice` (172 righe) |
| `reports/diff_sessione.md` | MODIFICATO | Questo file |
| `reports/handoff.md` | MODIFICATO | Dossier di sessione |
| `reports/stato_progetto.md` | MODIFICATO | Stato FASE 3 Fetta 1 + riserve voice |
| `reports/ultimo_report.md` | MODIFICATO | Report fetta |
| `tests/test_unit_voice_server.py` | NUOVO | Suite pytest 18 test |

## Cosa è cambiato e perché

**`modules/voice/server.py`** — implementazione `POST /voice`. Avvolge `GasKernel.run_turn()` accertato dalla sonda fetta 0. Single-thread stdlib, zero dipendenze, auth bearer `hmac.compare_digest`, fail-closed su token assente, fail-safe §9. Fix post-review #74: `Content-Length` non numerico → 400 (era EOF).

**`tests/test_unit_voice_server.py`** — 18 test reali (mai output simulato): TV1 avvio-senza-token, TV2 no-auth, TV3 token-errato-con-log-senza-segreto, TV4 token-corretto, TV5 eccezione-run_turn, TV6 singleton-kernel, TVExtra edge case, unit _token_ok. Fix post-review #74: dead code TV1 rimosso.

**`.github/workflows/ci.yml`** — step `Run voice server suite` (pytest, `if: always()`, tee su `RUNNER_TEMP/voice_output.txt`) + riga nel job summary.

**`.claude/agents/memoria_revisore.md`** — lezioni da review #74 e #75 aggiunte dal subagent revisore.

**`reports/*`** — aggiornamenti canonici di fine sessione.

## File non toccati

`gas.py`, `brains/`, `modules/memory/`, `modules/telegram/` — stop gate rispettati. `gas voice` CLI entry non aggiunta (richiede toccare gas.py → proposta per Fetta 2).
