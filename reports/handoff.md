# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-14 — D3: altri nomi di credenziali vietati nel cancello

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #202 (https://github.com/Gasss23/Gas/pull/202).
2. Fetta di sicurezza (cancello): secondo passaggio nella chat claude.ai col link della PR #202.

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Fornitori senza estensione** (bot/auth/telegram/slack/mistral/cohere/oauth): `FATTA`.
- **`.config/gh`**: `FATTA`.
- **Password con suffisso di copia/lista** (R-ve201-1, R-bot201-1): `FATTA`.
- **Separatore ripetibile** (R-ve201-2) e mnemonic.json: `FATTA`.
- **Verifica esterna #202 V-1** (fornitori col punto: bot.token): `FATTA` — review #332.
- **Nome intero solo sull'ultimo pezzo** (R-bot201-3): `FATTA`.
- **R-bot201-2** (composti incollati senza separatore): `SALTATA` — limite del bordo sinistro, resta riserva.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 modules/gate/gate.py               |  38 +++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 207 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           | 132 ++++++++++++++----------------------------------------------------------------------------------------------------------------------
 tests/test_unit_gate.py            |  17 +++++++++++++++--
 7 files changed, 152 insertions(+), 260 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
36f7542 fix(gate): fornitori di token anche col punto (bot.token, telegram.token)
d1dbd89 chore(revisore): memoria review #332 — APPROVATO CON RISERVE
f6b3ed9 docs(fine-task): report e handoff — D3 (PR #202)
e72350f feat(gate): D3 — altri nomi di credenziali, copie di password, .config/gh
40ef097 chore(revisore): memoria review #331 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #331 (commit e72350f, D3) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #331 del diff staged D3 (modules/gate/gate.py + tests/test_unit_gate.py). Ho letto CLAUDE.md, la memoria del revisore e i finding di stato_progetto.md (R-329-2, R-ve201-1/2, R-bot201-1/3).

**Elementi del diff esaminati**

- `modules/gate/gate.py:293` — fornitori estesi (mistral, cohere, slack, telegram, bot, o?auth) e separatore `[-_ ]*`. Rischio: costo quadratico e falsi positivi. Esito: ok. Provati bot_token, Bot_Token, AUTH TOKEN, oauth-token, bot  key e api_____key: tutti negati. author_key.md, auth.md, authors.md, oauth.md e robot_key_notes.md restano leggibili.
- `modules/gate/gate.py:305` — password con suffissi di copia/lista, in lista chiusa e ancorati a fine nome. Rischio: backtracking catastrofico e riapertura di password_reset/policy/passwordless. Esito: ok con riserva R-331-1.
  - Negati: «password (1) (2).txt», passwords_backup_2024.txt, «password 1.txt», passwords.old, password.txt~, password_backup_list.txt.
  - Leggibili: password_reset.md, password_policy.md, passwordless.md, password_2024_notes.md.
  - Il gruppo ripetuto richiede sempre un separatore, quindi non è ambiguo. Misurato su 1 MB: da 13 a 17 ms.
- `modules/gate/gate.py:328` e `modules/gate/gate.py:343` — `_NOME_INTERO_RE` applicata solo all'ultimo pezzo, prima del tetto 255. Rischio: riaprire cartelle sensibili e costo prima del tetto. Esito: ok.
  - La regex è ancorata `^…$` con alternative corte, quindi lineare (keys + 1 MB di «-»: 19 ms).
  - keys/prod.txt, shadow/readme.md e tokens/note.md ora sono leggibili, come voluto.
  - Restano negati: x/keys/key.txt e x/keys/id_rsa (nome del file); `.ssh/config` e `secrets/a.md` (ramo per pezzo, `modules/gate/gate.py:313` e `:284`); keys, keys/, x/passwd, shadow-, tokens.bak.
- `modules/gate/gate.py:332` e `modules/gate/gate.py:345` — `_PERCORSO_SEGRETO_RE` su `.config/gh`. Rischio: aggiramento del percorso e costo sul percorso intero. Esito: ok.
  - Il percorso è normalizzato (NFKC, normpath, casefold), quindi sono negati `./.config/gh/hosts.yml`, `a/../.config/gh/hosts.yml`, `.config//gh/hosts.yml`, `x/.CONFIG/GH/hosts.yml` e `home/.config/gh`.
  - Restano leggibili `.config/ghostty/config` e `.config/gh_notes.md`.
  - Costo lineare: 1,6 MB di «.config/» ripetuto in 300 ms. È il costo del ciclo sui pezzi, che già esisteva.
- `modules/gate/gate.py:393` — il chiamante di `livello_scrittura` usa `_nome_da_segreto`, quindi i nuovi nomi sono MAI anche in scrittura. Esito: ok (contesto).
- `tests/test_unit_gate.py:618` — 28 nuovi casi negati e 7 leggibili. Esito: ok.
  - 514 passed riprodotti.
  - Il tuo dato "gate.py di main: 22 failed" non l'ho riprodotto, ma le regole nuove sono tutte esercitate dai test.
- `tests/test_unit_gate.py:644` — casi leggibili per il punto 5 (keys/prod.txt, shadow/readme.md, ecc.). Esito: ok.

**Misure**

- `git ls-files` (98 file): nessun cambio di esito in lettura né in scrittura rispetto a origin/main, confrontando gate.py di main caricato come modulo separato.
- Timing su 1 MB: api+«_», password_ ripetuto, password (1) ripetuto, bot_ ripetuto, oauth ripetuto. Tutti tra 9 e 25 ms, lineari.
- Pezzo da 255 caratteri: 0,08 ms per chiamata.

**Riserve**

- **R-331-1 (BASSA)**: blocco in eccesso, stessa linea di R-329-3. Sono negati `password_new.md` e `password_dev.md`, perché new/dev sono nella lista chiusa e sono anche parole di documenti. Lo stesso per `slack_tokens_docs.md` e `bottoken_docs`. Il tuo `auth_token_docs.md` è già dichiarato nel diff. Va accodata a R-329-3 in stato_progetto.md, senza correzione.

**Escluso, non verificato**

- Il confronto sull'albero di lavoro completo (179 voci): ho verificato solo i 98 file tracciati.
- La suite `pytest tests/` (1320 passed): non rieseguita, ho eseguito solo tests/test_unit_gate.py.
- Il comportamento su macOS/Windows, dove la corrispondenza dei nomi è case-insensitive e il percorso `.config/gh` ha forme diverse.
- R-bot201-2 (composti incollati senza separatore, tipo myapikey.txt): resta aperta per il limite del bordo sinistro, non toccata da questa fetta.

La riga #331 è in memoria_revisore.md. Ho eseguito scripts/commit_memoria_revisore.sh, che non ha stampato nulla. Non ho verificato che il commit della memoria sia avvenuto.

### Review #332 (commit 36f7542, verifica esterna #202 V-1) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, la memoria del revisore (ultimo contatore #331) e il diff staged. Ho misurato con una sonda scritta con Write, perché il hook blocca i comandi Bash con le parole del commit. Questa review è la #332.

Elementi del diff esaminati:
- `modules/gate/gate.py:294` — il separatore dei fornitori diventa `[-_. ]*`, solo nel ramo gh|github|hf|openai|anthropic|gemini|groq|mistral|cohere|slack|telegram|bot|o?auth. Rischio esaminato: i nomi con il punto restano leggibili. Esito: ok.
  - Sulla sonda `telegram.token`, `bot.token`, `slack.token`, `gh.token`, `hf.key`, `oauth.key` e `o.auth.key` sono negati.
  - `robot.token.md`, `gh.keyboard.md` e `bot.keyring` restano leggibili: il bordo prima del nome e la coda `(token|key)s?` reggono.
  - Il punto è confinato al ramo dei fornitori. Il ramo `api[-_ ]*` e gli altri non cambiano, quindi `api.token` resta leggibile (già tracciato come R-329-2).
- `modules/gate/gate.py:294`, costo: nel caso peggiore (255 caratteri, tetto prima della regex) ho misurato 125-142 µs per chiamata, con `"bot"+"."*250` e `"gh"+". "*120`. Il costo è lineare per il separatore ripetuto e limitato dal tetto. Esito: ok.
- `tests/test_unit_gate.py:627` — quattro negati nuovi, nella parametrizzazione di `test_chiavi_private_e_credenziali_illeggibili_e_mai_scritte`. Rischio esaminato: i test non mordono la regressione. Esito: ok. Esercitano esattamente i casi della V-1, e i quattro nomi con punto prima passavano.
- `tests/test_unit_gate.py:652` — `robot.token.md` e `gh.keyboard.md` come leggibili in `test_nomi_simili_a_chiavi_restano_leggibili`. Esito: ok. Coprono i due falsi positivi più ovvi del nuovo separatore.

Riserva (BASSA):
- R-332-1: il punto ora separa nome ed estensione, quindi nuovi falsi positivi plausibili. La sonda li dà tutti negati: `auth.keys.md`, `auth.token.md`, `bot.key.md`, `bot.token.py`, `bot.tokens.md`, `slack.token.example`, `abot.key`, `cobot.key`.
  - È la stessa linea di R-329-3 e R-331-1 (eccesso su documentazione): la lista nera è volutamente prudente. La traccio come accettata, in stato_progetto.
  - Non è un blocco: la direzione è sicura e non tocca i guardrail.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. Non ci sono provider né eccezioni nel diff.

Rischio escluso: non ho rieseguito `tests/test_unit_gate.py` (520 passed dichiarati). Non ho rifatto il confronto sulle 180 voci di `git ls-files` e albero di lavoro contro origin/main (dichiarato senza cambi di esito). Su macOS e Windows non ho verificato nulla, come già tracciato in V-3. La V-2 (lista chiusa dei suffissi password) non è nel diff.

Memoria aggiornata: riga #332 aggiunta e committata con `bash scripts/commit_memoria_revisore.sh` (nessun errore).

## §5 DELTA TEST DEL MOTORE

tests/test_unit_gate.py: 486 → 514 passed (D3) → 520 passed (V-1 #202). Mutazione: con `modules/gate/gate.py` di origin/main i test della fetta danno `22 failed, 492 passed`.

pytest `tests/`: `1320 passed in 227.96s (0:03:47)`.

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `f6b3ed9`: run della PR #202 partite prima del fix V-1; esito non riportato qui (superato dalla testa nuova).
- `40ef097`, `e72350f`, `d1dbd89`, `36f7542`: nessuna run su questi SHA (pushati prima dell'apertura della PR; la run della PR testa la testa).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-331-1 (BASSA), accodata a R-329-3 in `reports/stato_progetto.md`.
- R-bot201-2 (BASSA) resta aperta.
- R-332-1 (BASSA), R-ve202-2 (BASSA), R-ve202-3 (BASSA, solo macOS/Windows) in `reports/stato_progetto.md`.
