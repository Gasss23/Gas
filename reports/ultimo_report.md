# ULTIMO REPORT — 2026-10-14 — D2: nomi di credenziali vietati (gate)

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (tocca il cancello: il bot darà riserve o neutral → decide l'operatore).
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai col link della PR.
3. Decidere se aprire la fetta D3 (deve includere anche `password` con suffisso o copia — R-ve201-1/R-bot201-1 — e il ramo del nome intero limitato all'ultimo pezzo — R-bot201-3) proposta qui sotto (nomi ancora leggibili).

## Esito

- **D2 punti 1–6 (ALTA + MEDIA)** — FATTA. `_CHIAVE_PRIVATA_RE` (modules/gate/gate.py) nega in lettura e scrittura (livello 3) tutti i nomi del prompt; i falsi positivi del prompt restano leggibili. Bordo `(?<![a-z])…(?![a-z])` come prima; `tokens?/keys?/passwd/shadow` solo come nome intero del pezzo (+ copie `-`, `~`, `.bak`, `.old`).
- **D2 BASSA facoltativa** — FATTA (.terraformrc, .tfstate, .tfvars, .boto, .s3cfg, .my.cnf, .yarnrc, .sentryclirc, .ovpn, wg0.conf): nessun falso positivo su file reali.
- **Alternativa `[a-z0-9]+_keys?\.(txt|json|ya?ml)`** — SALTATA — ridondante: il bordo `(?<![a-z])` di `keys?\.(…)` copre già prod_key.txt e my_keys.json (confermato dal revisore).
- **R-329-1 (MEDIA, revisore)** — FATTA nella fetta: separatore `[-_ ]?` (anche lo spazio: «Seed Phrase.txt», «ssh key», «private key»).
- **Misura su file reali** — nessun cambio di esito (lettura e livello di scrittura) rispetto a origin/main su `git ls-files` (98 file) e sull'albero di lavoro (298 voci mie, 340 del revisore con cartelle e .agents/.codex).
- **Test** — pytest tests/test_unit_gate.py 486 passed (era 477 prima di R-329-1); suite completa `tests/` 1291 passed, 1 skipped. Con la regex di main i test nuovi falliscono (97 fail, misurato dal revisore; 8 fail per i casi con lo spazio).
- **Costo regex** — quadratica ma limitata dal tetto dei 255 caratteri per pezzo: caso peggiore misurato dal revisore 144 µs per pezzo (la mia stima iniziale di 35 µs era sbagliata, R-329-4).
- **Review** — #329 APPROVATO CON RISERVE (R-329-1 chiusa), #330 APPROVATO CON RISERVE.
- **Verifica esterna (agente)** — APPROVATO CON RISERVE, nessuna ALTA/MEDIA ([commento](https://github.com/Gasss23/Gas/pull/201#issuecomment-6164793654)): tabella ricalcolata riga per riga senza discrepanze, 19 mutazioni tutte uccise; riserve BASSE R-ve201-1..3 e COSMETICA R-ve201-4.
- **Bot di verifica** — APPROVATO CON RISERVE, check `verifica-bot` neutral (decide l'operatore); riserve BASSE R-bot201-1/2 e COSMETICA R-bot201-3. Tutte tracciate in stato_progetto.md.

## Tabella nome → esito prima/dopo

L1 = scrittura libera, L2 = firma, L3 = mai. «prima» = origin/main (dbfafaf), «dopo» = questa fetta.

| punto | nome | prima (lettura / livello scrittura) | dopo |
|---|---|---|---|
| 1 ALTA | `api_key` | leggibile / L1 | negato / L3 |
| 1 ALTA | `apikey` | leggibile / L1 | negato / L3 |
| 1 ALTA | `api-keys.json` | leggibile / L1 | negato / L3 |
| 1 ALTA | `api_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `my_api_key.txt` | leggibile / L1 | negato / L3 |
| 1 ALTA | `access_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `refresh_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `gh_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `github_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `hf_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `openai_key` | leggibile / L1 | negato / L3 |
| 1 ALTA | `anthropic_key.txt` | leggibile / L1 | negato / L3 |
| 1 ALTA | `gemini_key` | leggibile / L1 | negato / L3 |
| 1 ALTA | `groq_token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `keys.txt` | leggibile / L1 | negato / L3 |
| 1 ALTA | `key.json` | leggibile / L1 | negato / L3 |
| 1 ALTA | `keys.yaml` | leggibile / L1 | negato / L3 |
| 1 ALTA | `dati/key.txt` | leggibile / L1 | negato / L3 |
| 1 ALTA | `prod_key.txt` | leggibile / L1 | negato / L3 |
| 1 ALTA | `my_keys.json` | leggibile / L1 | negato / L3 |
| 1 ALTA | `token` | leggibile / L1 | negato / L3 |
| 1 ALTA | `tokens` | leggibile / L1 | negato / L3 |
| 1 ALTA | `key` | leggibile / L1 | negato / L3 |
| 1 ALTA | `keys` | leggibile / L1 | negato / L3 |
| 2 MEDIA | `.azure` | leggibile / L1 | negato / L3 |
| 2 MEDIA | `.azure/accessTokens.json` | leggibile / L1 | negato / L3 |
| 2 MEDIA | `accesstokens.json` | leggibile / L1 | negato / L3 |
| 2 MEDIA | `mykubeconfig` | leggibile / L1 | negato / L3 |
| 2 MEDIA | `kubeconfigs` | leggibile / L1 | negato / L3 |
| 3 MEDIA | `password` | leggibile / L1 | negato / L3 |
| 3 MEDIA | `passwords.txt` | leggibile / L1 | negato / L3 |
| 3 MEDIA | `password.md` | leggibile / L1 | negato / L3 |
| 3 MEDIA | `passwd` | leggibile / L1 | negato / L3 |
| 3 MEDIA | `shadow` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `cookies.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `cookie.txt` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `cookies.sqlite` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `storage_state.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `auth_state.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `oauth.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `oauth2.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `.auth/user.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `sessions.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `session.json` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `gas.session` | leggibile / L1 | negato / L3 |
| 4 MEDIA | `anon.session-journal` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `wallet.json` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `wallet.txt` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `keystore.json` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `seed.txt` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `mnemonic.txt` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `seed_phrase` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `recovery_phrase` | leggibile / L1 | negato / L3 |
| 5 MEDIA | `Seed Phrase.txt` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `private_key` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `privkey` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `ssh_key` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `deploy_key` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `id-rsa` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `rsa_key` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `AuthKey_ABC.p8` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `private key` | leggibile / L1 | negato / L3 |
| 6 MEDIA | `ssh key` | leggibile / L1 | negato / L3 |
| BASSA | `.terraformrc` | leggibile / L1 | negato / L3 |
| BASSA | `terraform.tfstate` | leggibile / L1 | negato / L3 |
| BASSA | `prod.tfvars` | leggibile / L1 | negato / L3 |
| BASSA | `.boto` | leggibile / L1 | negato / L3 |
| BASSA | `.s3cfg` | leggibile / L1 | negato / L3 |
| BASSA | `.my.cnf` | leggibile / L1 | negato / L3 |
| BASSA | `.yarnrc` | leggibile / L1 | negato / L3 |
| BASSA | `.sentryclirc` | leggibile / L1 | negato / L3 |
| BASSA | `client.ovpn` | leggibile / L1 | negato / L3 |
| BASSA | `wg0.conf` | leggibile / L1 | negato / L3 |
| falsi positivi | `tokenizer.json` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `tokenizer.py` | leggibile / L2 | leggibile / L2 |
| falsi positivi | `keyboard.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `keynote.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `monkey.py` | leggibile / L2 | leggibile / L2 |
| falsi positivi | `passwordless.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `session_notes.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `seed_data.csv` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `auth_flow.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `dati/keys.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `dati/tokens.md` | leggibile / L1 | leggibile / L1 |
| falsi positivi | `.azure-pipelines/ci.yml` | leggibile / L1 | leggibile / L1 |

## Proposta fetta D3 (NON fatta: fuori dallo scope di D2)

Nomi di credenziali che passano ancora (misurati):
- MEDIA: token senza estensione con prefisso — `bot_token`, `auth_token`, `telegram_token` (Gas usa Telegram); token della CLI GitHub in `.config/gh/hosts.yml`.
- BASSA (R-329-2): `Cookies` e `Login Data` di Chrome; `storage-state.json`, `auth-state.json`; `api.token`, `gh.token`; `token.old~`; `kube_config`, `kube-config.yaml`; `seed phrases.md`, `seed_phrases`.
- BASSA: storie di shell (`.bash_history`, `.zsh_history`, `.python_history`), `.mylogin.cnf`, `login.keychain-db`, `gshadow`, `htpasswd` senza punto, `.jceks`, `.bks`, `putty.reg`, `.kdb`.
- Trucchi sul percorso: maiuscole, punti/spazi finali, NFKC e symlink sono già coperti (casefold, rstrip, risoluzione del percorso in `_vet_letture`); hard link negati in run_command. Limite strutturale: un segreto con nome qualsiasi non è coperto (divieto per nomi).

## Anomalie

- Il revisore ha committato da sé la sua memoria (28a4abb, e67ef2a) sul branch di sessione: commit separati, come da `scripts/commit_memoria_revisore.sh`.
