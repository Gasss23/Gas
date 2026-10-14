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
- **Bot #202 V-1/V-2/V-3** (fornitori usati da Gas; tutto negato in keys/ e tokens/ tranne .md/.rst/.py; `.config/gh` sui pezzi puliti): `FATTA` — review #333 e #334 (R-333-1 chiusa).
- **Bot #202 sullo SHA 9f5446b V-1** (copie della cartella keys.bak/) e `daily_token`: `FATTA` — review #335. V-2 (report non allineati) corretta nei report.
- **Bot #202 sullo SHA aec8d83 V-1** (keys/telegram.py leggibile): `FATTA` — tolto .py dalla deroga, review #336. V-2 (stato_progetto non allineato) corretta.
- **Bot #202 sullo SHA c2a62d2 V-1** (copie di .config/gh): `FATTA` — review #337.
- **Nome intero solo sull'ultimo pezzo** (R-bot201-3): `FATTA`.
- **R-bot201-2** (composti incollati senza separatore): `SALTATA` — limite del bordo sinistro, resta riserva.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 modules/gate/gate.py               |  53 +++++++++++++++++++++++++++++++++++++++++----------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 372 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           | 136 ++++++++++++++++++-----------------------------------------------------------------------------------------------------------------
 tests/test_unit_gate.py            |  29 ++++++++++++++++++++++++++--
 7 files changed, 352 insertions(+), 261 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
1ab03fe fix(gate): copie della cartella .config/gh (gh.bak/, gh~/)
0f1ce87 chore(revisore): memoria review #337 — APPROVATO CON RISERVE
c2a62d2 docs(fine-task): report e handoff — note del bot su #202 (aec8d83)
03195ad fix(gate): in keys/ e tokens/ leggibile solo la documentazione (.md/.rst)
bdea9cb chore(revisore): memoria review #336 — APPROVATO CON RISERVE
aec8d83 docs(fine-task): report e handoff — note del bot su #202 (9f5446b)
6473f5b fix(gate): copie della cartella keys/tokens (keys.bak/) e daily_token
5ff74fa chore(revisore): memoria review #335 — APPROVATO
9f5446b docs(fine-task): report e handoff — note del bot su #202
b99d826 fix(gate): note del bot su #202 — fornitori usati da Gas, cartelle keys/ e tokens/, .config/gh sui pezzi puliti
659392e chore(revisore): memoria review #334 — APPROVATO
c855da4 chore(revisore): memoria review #333 — APPROVATO CON RISERVE
2da725a docs(fine-task): report e handoff — D3 + V-1 #202
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

### Review #333 (diff poi committato come b99d826, prima di R-333-1) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, la memoria del revisore e il diff staged (gate.py + test_unit_gate.py). Non ho riletto per intero stato_progetto.md: ho fatto solo un grep delle sezioni. Ho riprodotto la suite e scritto una sonda (`/tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/sonda.py`) con 40 nomi e 4 misure di costo. Memoria aggiornata con la riga #333 (massimo precedente #332) e committata con `commit_memoria_revisore.sh`.

Elementi del diff esaminati:
- `modules/gate/gate.py:297` — aggiunge openrouter, elevenlabs, voice, claude, discord, gitlab, npm, pypi, huggingface al ramo dei fornitori. Rischio: falsi positivi.
  - Esito: ok.
  - Il ramo richiede `(token|key)s?` subito dopo il fornitore.
  - Restano leggibili: `modules/voice/tts.py`, `modules/voice/__init__.py`, `voice_keyboard.md`, `npm_tokenizer.py`, `npm-debug.log`, `package-lock.json`.
  - Negati: `voice_key_notes.md`, `claude_key.md`, `discord_key_docs.md`, `pypi_token.txt`, `voicekey.txt`, `.npmrc`.
  - `voice_key_notes.md` e `claude_key.md` sono eccessi. Vedi R-333-2.
- `modules/gate/gate.py:333-334` e `:348-350` — regola «cartella keys/tokens + ultimo pezzo senza estensione o .txt/.json/.yml». Rischio: riapertura di keys/openai, tokens/github, keys/prod.txt.
  - Esito: ok per i casi segnalati dal bot.
  - Negati: `keys/openai`, `Keys/OpenAI`, `keys./openai`, `keys /openai`, `keys/sub/x`, `keys/x.yaml`, `key/x.json`, `tokens/a.TXT`.
  - Leggibili, come voluto: `keys/readme.md`, `keys/setup.py`, `keys/__init__.py`, `keys/sub/x.md`.
  - Costo: `^[^.]+$` è lineare. Un pezzo da 1 MB costa 5–10 ms. Su 255 caratteri costa 0,03 ms. Il tetto 255 resta prima di `_SEGRETO_RE` e `_CHIAVE_PRIVATA_RE`.
- `modules/gate/gate.py:348,357` — `.config/gh` ora confrontato sui pezzi puliti con `rstrip(". ")`, e `_PERCORSO_SEGRETO_RE` eliminata. Rischio: bypass con punti o spazi.
  - Esito: ok.
  - Negati: `.config./gh/hosts.yml`, `.config/gh /hosts.yml`, `a/.config/gh`, `/.config//gh/x`.
  - Leggibili: `.config/ghostty/c`, `.config/gh_notes.md`.
  - `.config/. /gh` resta leggibile, ma è una directory diversa da `.config/gh`, quindi non è un bypass.
- `tests/test_unit_gate.py:625-635` e `:654-660` — nuovi casi negati e leggibili. Rischio: test che non mordono.
  - Esito: ok.
  - 538 passed riprodotti.
  - Il passaggio `keys/prod.txt` da leggibile a negato è coerente col V-2.
  - I nuovi leggibili `voiceover.md`, `claudette.md` e `keys/setup.py` coprono i falsi positivi dei nuovi fornitori.
  - Non ho rifatto la mutazione dei test.

Riserve, entrambe BASSE e tracciabili:
- R-333-1: la regola di keys/ e tokens/ usa una lista chiusa di estensioni, quindi restano leggibili `keys/prod.toml`, `keys/prod.ini`, `keys/a.cfg`, `keys/a.csv`, `keys/a.json5` e `tokens/a.conf` (verificati). Proposta: invertire la logica, cioè negare tutto in keys/ e tokens/ tranne una lista bianca di estensioni di documentazione (.md, .py, .rst).
- R-333-2: eccessi che non toccano segreti, sulla stessa linea di R-329-3. Sono `keys/Makefile`, `tokens/LICENSE`, `keys/readme` (senza estensione), `voice_key_notes.md`, `claude_key.md`. Accettabile per fail-closed.

Rischio escluso:
- Non ho confrontato i 180 percorsi di `git ls-files` più albero di lavoro con origin/main. Mi fido della misura dichiarata. Ho guardato solo i file voice/claude/npm tracciati (`clients/voice/*`, `.claudeignore`, `.claude/*`) e nessuno corrisponde al ramo con `(token|key)`.
- I backslash di Windows non sono trattati. L'autore lo dichiara e il server gira su Linux.
- Non ho eseguito la suite completa del repo, solo `tests/test_unit_gate.py`.
- Il comportamento su VPS non è verificato.

File rilevanti:
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #334 (commit b99d826, dopo R-333-1) — verdetto integrale

## VERDETTO: APPROVATO

Secondo giro sul diff staged aggiornato (R-333-1). Ho riletto il diff e rilanciato la suite e una sonda. Riga #334 aggiunta in `.claude/agents/memoria_revisore.md` e committata con `commit_memoria_revisore.sh`. Il diff del motore non è stato committato.

Elementi del diff esaminati:
- `modules/gate/gate.py:337` — `_DOC_IN_CARTELLA_CHIAVI_RE = \.(md|rst|py)$` sostituisce la lista chiusa delle estensioni vietate con una lista bianca. Rischio: un'estensione non prevista restava leggibile dentro keys/ e tokens/.
  - Esito: ok.
  - Ora sono negati `keys/prod.toml`, `tokens/a.conf`, `keys/a.json5`, `keys/Makefile`, `keys/x.md.bak` e `keys/x.py~`.
  - Il backup `.bak` non passa la lista bianca perché il pattern è ancorato a fine nome.
- `modules/gate/gate.py:351` — `not _DOC_IN_CARTELLA_CHIAVI_RE.search(puliti[-1])` e almeno un pezzo intermedio uguale a `keys?` o `tokens?`. Rischio: falsi positivi su cartelle di codice.
  - Esito: ok.
  - Restano leggibili `keys/readme.md`, `keys/setup.py`, `modules/keys/__init__.py`, `src/keys/utils.py` e `tokens.py` (il file `tokens.py` non è in una cartella).
  - Il caso `keys` da solo è negato dalla regola del nome intero.
  - Con `len(puliti) > 1` la regola riguarda solo i file dentro la cartella, non il nome del percorso stesso.
  - Il costo non cambia: la nuova regex è ancorata e gira sul pezzo già pulito.
- `tests/test_unit_gate.py` (casi aggiunti nelle liste dei negati e dei leggibili) — la suite dà 540 passed riprodotti. Non ho rifatto la mutazione dei test.

Riserve residue (accettate, BASSE):
- `keys/x.py`, `keys/x.md` e `keys/.md` sono leggibili per scelta, perché sono documenti o codice. Un file con un segreto salvato con quelle estensioni (es. `keys/segreto.md`) passerebbe. Il rischio è basso perché le altre regole per nome continuano ad applicarsi.
- `keys/x.PY` è leggibile (corrisponde al pattern ignorando le maiuscole). Il rischio è lo stesso.
- Eccessi: `keys/Makefile`, `tokens/LICENSE`, `keys/readme` senza estensione. È la linea già tracciata come R-333-2.

Rischio escluso:
- Non ho rieseguito il confronto dei 180 percorsi contro origin/main; mi fido della misura dichiarata (nessun cambio di esito).
- Non ho eseguito la suite completa del repo, solo `tests/test_unit_gate.py`.
- Il comportamento su VPS non è verificato.

File: /home/user/Gas/modules/gate/gate.py, /home/user/Gas/tests/test_unit_gate.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #335 (commit 6473f5b, bot #202 V-1 sullo SHA 9f5446b + daily_token) — verdetto integrale

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, la memoria del revisore (ultima riga #334) e le sezioni di stato_progetto.md. Il diff staged tocca solo modules/gate/gate.py e tests/test_unit_gate.py, senza slicing della history, tool simulati o guardrail indeboliti.

Elementi esaminati:
- `modules/gate/gate.py:337` — `_NOME_CARTELLA_CHIAVI_RE` diventa `^(tokens?|keys?)(-|~|\.bak|\.old)?$`. Rischio esaminato: le copie della cartella (V-1 del bot) tornano negate e nessun nome legittimo viene bloccato. Esito: ok. Il suffisso è identico a `_NOME_INTERO_RE` (`modules/gate/gate.py:331`), quindi file e cartella sono coerenti. Il confronto avviene sui pezzi già puliti da punti e spazi finali (`modules/gate/gate.py:349`).
- `modules/gate/gate.py:297` — `daily` aggiunto ai fornitori, seguito da `[-_. ]*(token|key)s?` e dal bordo `(?![a-z])` (`modules/gate/gate.py:311`), con `(?<![a-z])` davanti. Rischio esaminato: falsi positivi sui nomi che contengono "daily". Esito: ok. `daily/notes.md` e `modules/daily_report.py` restano leggibili. `dailytokenizer.md` resta leggibile grazie al bordo `(?![a-z])` (test aggiunto, 547 passed). `daily_key.md`, `dailytoken.md` e `daily-tokens.json` sono negati, in linea con voice, bot e gli altri fornitori.
- `tests/test_unit_gate.py:632-636` — negati nuovi: keys.bak/openai, keys.old/prod.txt, keys~/github, tokens-/a.conf, daily_token. Esito: ok.
- `tests/test_unit_gate.py:658-662` — leggibili nuovi: dailytokenizer.md, keys.bak/readme.md. Esito: ok. Il secondo conferma che la deroga per documentazione e codice vale anche nelle copie della cartella.

Misure che ho riprodotto:
- La suite del gate dà 547 passed.
- Ho provato 13 percorsi a mano. Sono leggibili: keys.bak/a.py, keys~/readme.md, daily/notes.md, modules/daily_report.py, keys.bak.d/x. Sono negati: keys.old/, key-/x.txt, tokens.old/x, keys.bak/sub/y e KEYS.BAK/x (maiuscolo, per il casefold).

Non riapre nulla: la regex della cartella è un sovrainsieme stretto della precedente, quindi i nomi negati prima lo restano, e `daily` aggiunge solo nomi negati.

Rischio escluso: non ho rieseguito il confronto sulle 180 voci reali contro origin/main, mi fido della misura che mi hai riportato. Il comportamento su VPS non è verificato.

Nota di non-regressione, non è una riserva: copie con altri suffissi (`keys.orig/`, `keys_old/`, `keys.backup/`) non sono coperte, ma sono leggibili anche su main. Si possono valutare in una fetta successiva.

Memoria aggiornata con la riga #335 (massimo esistente 334, più 1). Ho lanciato `scripts/commit_memoria_revisore.sh` e non ha stampato nulla. Non ho controllato l'esito del commit: non ho eseguito `git log` o `git status` dopo.

### Review #336 (commit 03195ad, bot #202 V-1 sullo SHA aec8d83) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, la memoria del revisore (ultima riga #335) e `reports/stato_progetto.md`, quest'ultimo solo con una ricerca mirata.

Elementi del diff esaminati:
- `modules/gate/gate.py:338` — `_DOC_IN_CARTELLA_CHIAVI_RE` passa da `\.(md|rst|py)$` a `\.(md|rst)$`. Rischio esaminato: file di codice con segreti dentro `keys/` o `tokens/`, per esempio `keys/telegram.py` con `TOKEN = "..."`. Esito ok: `keys/setup.py`, `keys/telegram.py`, `tokens/a.py` e `keys.bak/x.py` ora sono negati.
- `modules/gate/gate.py:352` — la negazione resta ancorata ai pezzi puliti del percorso (`puliti[-1]` per la deroga, `puliti[:-1]` per la cartella). Rischio esaminato: la deroga sul nome file potrebbe aggirare la cartella con estensioni doppie. Esito ok: `keys/a.md.bak` è negato, mentre `keys/a.py.md` resta leggibile. `a.py.md` è un documento, quindi lo accetto.
- `tests/test_unit_gate.py:633` — aggiunti `keys/setup.py` e `keys/telegram.py` tra i percorsi negati. Esito ok, il test morde sul fix.
- `tests/test_unit_gate.py:662` — `keys/setup.py` sostituito da `keys/notes.rst` tra i leggibili. Esito ok.

**Sonda** (14 voci, script nello scratchpad, scritto con Write):
- Negati: `keys/setup.py`, `keys/telegram.py`, `tokens/a.py`, `keys.bak/x.py`, `modules/keys/__init__.py`, `src/keys/utils.py`.
- Leggibili: `keys/notes.rst`, `keys/readme.md`, `keys/README.MD`, `keys/segreto.md`, `modules/voice/keys.py`, `keys.py`.

**Test**: 549 passed, riprodotti.

**Cartelle di codice chiamate `keys/` o `tokens/`**: la conseguenza che segnali (`modules/keys/__init__.py` e `src/keys/utils.py` ora negati) è accettabile. È la scelta più sicura del bot e coincide con il comportamento di main. Il costo è un falso positivo, cioè un eccesso di blocco, non una fuga. Va nel verso della filosofia "robustezza > potenza". Nessun guardrail è indebolito. Non ci sono eccezioni da propagare: è solo una regex.

**Riserve**
- R-336-1 BASSA: eccesso di blocco sul codice in cartelle `keys/` o `tokens/`, accettato (stessa linea di R-329-3 e R-333-2).
- Residuo noto: `keys/segreto.md` resta leggibile per scelta, perché i `.md` e `.rst` sono documentazione.

**Rischio escluso, non verificato**: non ho rieseguito il confronto sulle 180 voci reali contro `origin/main`. Mi fido della tua misura, perché il diff è di una sola regex più i test. Non ho verificato la suite completa fuori da `tests/test_unit_gate.py`. Non ho verificato il comportamento su VPS.

**Memoria**: riga #336 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Lo script `bash scripts/commit_memoria_revisore.sh` è uscito senza errori. Non ho committato altro.

### Review #337 (commit 1ab03fe, bot #202 V-1 sullo SHA c2a62d2) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, stato_progetto.md (solo con Grep, a norma della sez. 11) e la memoria del revisore. Il diff staged è piccolo e coerente con la linea del gate D3 (fail-closed sulle credenziali).

Elementi del diff esaminati:
- `modules/gate/gate.py:337` — introduce `_COPIA_GH_RE = ^gh(-|~|\.bak|\.old)?$`, con gli stessi suffissi di `_NOME_INTERO_RE` e `_NOME_CARTELLA_CHIAVI_RE`. Rischio: eccesso di negazione o regex fragile. La regex è ancorata, quindi `ghostty` e `gh_notes.md` non la attivano. Esito: ok.
- `modules/gate/gate.py:359` — il confronto `b == "gh"` diventa `_COPIA_GH_RE.search(b)` sul pezzo subito dopo `.config`. I pezzi sono già puliti con `rstrip(". ")` (righe 349-350), quindi i casi `.config./gh` e `gh /` restano coperti. Rischio: regressione sui casi già chiusi e costo della regex. Esito: ok. Con un pezzo da 255 caratteri il costo misurato è 0,03 ms.
- `tests/test_unit_gate.py:637-638` — tre nuovi negati: `.config/gh.bak/hosts.yml`, `.config/gh~/hosts.yml`, `.config/gh.old/hosts.yml`. Rischio: test che non pinna il comportamento. I tre percorsi sono quelli della riserva V-1 del bot. I leggibili `ghostty` e `gh_notes.md` restano nei test esistenti. Esito: ok.

Sonda eseguita (non committata, nello scratchpad) su `lettura_consentita`:
- Negati: `.config/gh.bak/`, `gh~/`, `gh-/`, `gh.old/`, `GH.bak/` (maiuscole), `gh/` e il file `.config/gh.bak`.
- Leggibili: `.config/ghostty/config`, `.config/gh_notes.md`, `.config/gh.md`.
- Suite del gate: 552 passed, riprodotti da me.

Riserve:
- R-337-1 (BASSA): restano leggibili `.config/gh.orig/hosts.yml`, `.config/gh_old/hosts.yml` e `.config/gh.bak.bak/hosts.yml`. È la stessa lista chiusa di suffissi già accettata per `keys.orig/` e `keys_old/` (memoria #335), quindi non è una regressione.
- Cosmetico: il commento a riga 336 ("Bot #202 sullo SHA 9f5446b … copie della cartella keys.bak/") ora precede `_COPIA_GH_RE`, che riguarda `gh`. È un commento fuori posto, non un bug.

Non verificato:
- Le "180 voci reali" citate nel contesto: non le ho rieseguite, mi fido della dichiarazione.
- Il comportamento su VPS e con symlink: la sonda lavora solo sul percorso testuale, non sul filesystem.

Memoria aggiornata con la riga #337 (il massimo precedente era #336) e `commit_memoria_revisore.sh` eseguito. Non ho committato altro.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_gate.py: 486 → 514 passed (D3) → 520 passed (V-1 #202) → 540 passed (bot #202 V-1/V-2/V-3, R-333-1) → 547 passed (copie keys.bak/, daily_token) → 549 passed (tolto .py dalla deroga in keys/) → 552 passed (copie di .config/gh). Mutazione: con `modules/gate/gate.py` di origin/main i test della fetta danno `22 failed, 492 passed`.

pytest `tests/`: `1346 passed in 176.83s (0:02:56)` (dopo le note del bot su #202).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `f6b3ed9`: run della PR #202 partite prima del fix V-1; esito non riportato qui (superato dalla testa nuova).
- `c2a62d2`: unit-suite e handoff-check success, gate 549 passed (dal verdetto del bot); bot APPROVATO CON RISERVE (neutral).
- `aec8d83`: unit-suite e handoff-check success (dal verdetto del bot); bot APPROVATO CON RISERVE (neutral).
- `9f5446b`: run della PR #202 con verdetto del bot APPROVATO CON RISERVE (neutral); unit-suite non riportata qui.
- `2da725a`: run della PR #202 partite prima delle note del bot; il bot ha annullato la verifica (testa cambiata).
- `40ef097`, `e72350f`, `d1dbd89`, `36f7542`, `c855da4`, `659392e`, `b99d826`, `5ff74fa`, `6473f5b`, `bdea9cb`, `03195ad`, `0f1ce87`, `1ab03fe`: nessuna run su questi SHA (pushati prima dell'apertura della PR; la run della PR testa la testa).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-331-1 (BASSA), accodata a R-329-3 in `reports/stato_progetto.md`.
- R-bot201-2 (BASSA) resta aperta.
- R-337-1 (BASSA, copie gh.orig/, gh_old/) e commento fuori posto (COSMETICA).
- R-336-1 (BASSA, codice in cartelle keys/ negato).
- R-333-2 (BASSA, eccessi: keys/Makefile, voice_key_notes.md) e la scelta di lasciare leggibili .md/.rst/.py in keys/ (review #334).
- R-332-1 (BASSA), R-ve202-2 (BASSA), R-ve202-3 (BASSA, solo macOS/Windows) in `reports/stato_progetto.md`.
