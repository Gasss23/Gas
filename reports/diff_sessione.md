# DIFF SESSIONE — 2026-10-05 — feat/verifica-bot (V-B vera, fetta B1)

| File | Cosa è cambiato e perché |
|---|---|
| `.github/workflows/verifica-bot.yml` | Nuovo: bot di verifica esterna con identità separata (pull_request_target, sola lettura, GitHub App, dosaggio quota). |
| `scripts/bot_esito.py` | Nuovo: decisione deterministica di approvazione (soglia "niente ALTA/MEDIA", macchina del bot, doc-only, credenziali). |
| `tests/test_unit_verifica_bot.py` | Nuovo: 126 test (logica, comandi con gh finto + jq reale, proprietà di sicurezza del workflow). |
| `.github/workflows/ci.yml` | Step della nuova suite + riga nel job summary. |
| `.claude/perimetro_review.txt` | `scripts/bot_esito.py` nel perimetro di review. |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #158, #159, #160. |
| `reports/setup_verifica_bot.md` | Nuovo: passi numerati dell'operatore (token, App, environment). |
| `reports/*` | Report di fine task; stato_progetto (V-B fetta B1, riserve aperte). |

La storia completa sta in git.
