# ULTIMO REPORT — 2026-10-14 — D3: altri nomi di credenziali vietati (gate)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #202 (tocca il cancello: il bot darà riserve o neutral → decide l'operatore).
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai col link della PR #202.

## Esito

- **Fornitori senza estensione** — FATTA: bot_token, auth_token, telegram_token, slack_token, mistral_key, cohere_key, oauth_token negati (lettura e scrittura, livello 3).
- **`.config/gh`** — FATTA: la cartella della CLI GitHub (hosts.yml col token) è negata via `_PERCORSO_SEGRETO_RE` sul percorso intero.
- **Password con suffisso** — FATTA (R-ve201-1, R-bot201-1): passwords_backup.txt, password_list.txt, password-prod.csv, «passwords copy.txt», «password (1).txt», password_2024.txt negati; password_reset.md, password_policy.md, passwordless.md restano leggibili.
- **Separatore ripetibile** — FATTA (R-ve201-2): `api  key`, `api__key`, `seed  phrase` negati. Anche mnemonic.json.
- **Nome intero solo sull'ultimo pezzo** — FATTA (R-bot201-3): keys/prod.txt, shadow/readme.md, tokens/note.md tornano leggibili; .ssh/ e secrets/ restano negati.
- **R-bot201-2** (composti incollati, myapikey.txt) — SALTATA: limite del bordo sinistro, resta riserva aperta.
- **Misura su file reali** — nessun cambio di esito rispetto a origin/main (179 voci fra `git ls-files` e albero di lavoro).
- **Test** — tests/test_unit_gate.py 514 passed (con il gate di main 22 failed); pytest tests/ 1320 passed.
- **Review** — #331 APPROVATO CON RISERVE: R-331-1 (BASSA) eccesso su password_new.md, password_dev.md, slack_tokens_docs.md, accodata a R-329-3.
- **Riserve di #200** (bot e verifica esterna) — tracciate in stato_progetto.md come promesso.
