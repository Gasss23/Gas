# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-05 — V-B vera, fetta B1: bot di verifica esterna su GitHub (identità separata)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #130 (https://github.com/Gasss23/Gas/pull/130).
2. Setup del bot dopo il merge: `reports/setup_verifica_bot.md` (token dell'abbonamento, GitHub App dedicata, environment `verifica-bot` ristretto a main). Senza setup il bot non parte.
3. **R-158-5**: il bot è di sola lettura e non esegue test. In variante B la verifica esterna locale §4quater resta obbligatoria accanto al bot? (consiglio: sì per le fette nel perimetro di review).
4. Dopo il test di convalida (fetta B2): ruleset `main-lock` con 1 approvazione, "dismiss stale approvals", "require approval of the most recent push" (passi forniti al momento).
5. Ancora aperte da sessioni precedenti: R-155-3 (Codex e Claude Code nella stessa cartella), V-3 / V-5 della verifica #121.

---

## §1 SCOPE & ESITO FETTE

- **Fetta B1 — bot di verifica (workflow + `scripts/bot_esito.py` + test)**: `FATTA` — commit `5010cef`, review #158/#159/#160 APPROVATO CON RISERVE; 126 test nuovi; mutation 55/56 (1 equivalente).
- **Riserve #158 e #159**: `FATTA` — tutte chiuse con test prima del commit, tranne R-158-5 (decisione umana, §0.3).
- **Riserve #160 (R-160-1, R-160-2, BASSE)**: `DEFERITA — fetta B2` (regola dell'operatore: le basse passano, si aggiustano dopo).
- **Fetta B2 — `gasmerge --auto` + V-3 #127 + test di convalida**: `DEFERITA — richiede B1 su main e setup dell'operatore.`
- **Ruleset**: `DEFERITA — dopo la convalida.`
- **Residui V-2 #127 e V-2/V-3 #129**: `DEFERITA — decisione operatore (2026-10-05): solo V-3 #127, nella fetta B2.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 ++++++
 .claude/perimetro_review.txt       |   1 +
 .github/workflows/ci.yml           |  15 +++++++++++
 .github/workflows/verifica-bot.yml | 242 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  15 ++++++-----
 reports/handoff.md                 | 227 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------
 reports/setup_verifica_bot.md      |  46 +++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   4 +--
 reports/ultimo_report.md           |  39 +++++++++++----------------
 scripts/bot_esito.py               | 240 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_verifica_bot.py    | 534 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 1222 insertions(+), 149 deletions(-)
```

NB: conteggi di `reports/handoff.md` approssimati per costruzione (il file conta se stesso).

## §3 GIT LOG --ONELINE (sessione)

```
5010cef feat(verifica-bot): bot di verifica esterna con identità separata (V-B vera, fetta B1) — review #158/#159/#160
39ea8a4 chore(revisore): memoria review #160 — APPROVATO CON RISERVE
d37d875 chore(revisore): memoria review #159 — APPROVATO CON RISERVE
05a4494 chore(revisore): memoria review #158 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `5010cef` (workflow, script, test, ci, perimetro): review #158, #159, #160 incollate per intero, nell'ordine. Il diff revisionato da #160 è quello committato (marcatore `segna_review_ok.sh` sullo stage revisionato).
Unica modifica al testo: le citazioni del sorgente della action ESTERNA `anthropics/claude-code-action` (file che non esiste in questo repo) sono riscritte da `file:riga` a `file riga N`, perché `check_verdetto.py` verifica ogni `file:riga` a HEAD.

### Review 158

## VERDETTO: APPROVATO CON RISERVE

Review #158 — fetta B1 della "V-B vera" (bot di verifica con identità separata). Worktree `/Users/gas/Gas/.claude/worktrees/gate-ip-ottetti`, branch `feat/verifica-bot` (verificato, coincide col dichiarato), diff staged 5 file / +777.

Letti: CLAUDE.md (sez. 5), reports/stato_progetto.md (V-B in priorità), la mia memoria. Eseguito `tests/test_unit_verifica_bot.py` con `/Users/gas/Gas/.venv`: **69 passed** (riprodotto). Scaricate da GitHub le tre action pinnate allo SHA esatto: `structured_output` e `client-id` esistono davvero; nel sorgente di claude-code-action (agent mode) la modalità "agent" parte anche su `labeled` e la PR non viene mai messa in checkout nella root.

**Elementi del diff esaminati**
- `.github/workflows/verifica-bot.yml:118` (checkout della PR in `./pr` a `needs.smista.outputs.head`) — rischio: "pwn request", cioè esecuzione di codice della PR con i segreti — **ok**: nessuno step `run` tocca `./pr`; gli strumenti concessi a Claude non includono esecuzione (niente python/bash/pytest/Edit/Write; verificato che l'action spezza `--allowedTools` sulle virgole e toglie gli spazi, quindi il YAML ripiegato funziona); i `.claude/settings.json` caricati sono quelli di main (hook che escono su branch `main`, nessun `permissions.allow`, `.claude/settings.json:6` nel contesto).
- `.github/workflows/verifica-bot.yml:193` (job `esito`) — rischio: token di scrittura raggiungibile dal modello — **ok**: il token dell'App si crea solo qui, su un runner separato, con `permission-pull-requests: write` e nessun permesso sul contenuto (niente merge); verdetto passato come `env` (mai `${{ }}` nei run); `GITHUB_TOKEN` del job `verifica` in sola lettura. Espressioni corrette: `needs` è disponibile nell'`env` del job; `!cancelled()` fa partire `esito` anche con `verifica` saltato (doc-only); `steps.mN.outputs.structured_output == ''` fa scattare la cascata; output con delimitatore casuale.
- `.github/workflows/verifica-bot.yml:38` (filtro `if` di `smista`) — rischio: fork / autore estraneo / etichetta — **ok**; i soli campi interpolati sono repository, numero e SHA (titolo/corpo/ref mai).
- `.github/workflows/verifica-bot.yml:32` (`concurrency` con `cancel-in-progress` a livello di workflow) — rischio: cancellazione di run buone — **riserva R-158-3**.
- `.github/workflows/verifica-bot.yml:93` (`Bash(gh api:*)`) — rischio: rete verso host esterni — **riserva R-158-4**.
- `scripts/bot_esito.py:61` (`decidi`) — controllo della head e ramo doc-only prima di tutto; JSON rotto o campi mancanti → COMMENT — **ok, con riserva R-158-2** (sonde sotto).
- `scripts/bot_esito.py:160` (`commit_id` legato allo SHA analizzato) — rischio: approvazione che resta valida dopo un push — **ok A CONDIZIONE** che il ruleset abbia "Dismiss stale approvals" (passo E di `reports/setup_verifica_bot.md`); senza, un APPROVE su H1 resta valido dopo il push di H2 senza etichetta.
- `scripts/bot_esito.py:37` (`solo_reports`: vecchi nomi dei rename, `..`, 3000 file) — **ok**; la race fra lettura della head e lettura dei file è neutralizzata da `concurrency` (un push cancella la run) e dal ricontrollo della head in `esito`.
- `scripts/bot_esito.py:134` (`cmd_smista`) — decide solo "doc-only sì/no", senza una classe di path sensibili — **riserva R-158-1**.
- `tests/test_unit_verifica_bot.py:319` (`test_checkout_senza_credenziali`) — **nota**: nella root la proprietà è annullata dall'action stessa, che riscrive `.git/config` col `GITHUB_TOKEN` (`replaceCheckoutCredentials`); il token è in sola lettura, quindi innocuo, ma il test prova meno di quanto dice il nome.
- `.github/workflows/ci.yml:125` (nuovo step della suite) — **ok**: `pyyaml` è in `requirements.txt`, `jq` è già sul runner.

**Riserve (da tracciare in stato_progetto.md)**
- **R-158-1 (MEDIA — da chiudere PRIMA del passo E / variante B)**: il bot può approvare PR che toccano la propria macchina (`.github/workflows/**`, `scripts/bot_esito.py`, `.claude/verifica_esterna.md` che "lo cambia solo l'operatore"). Una PR che aggiunge un workflow `on: push` su main con `environment: verifica-bot` riceve, dopo il merge, la chiave dell'App; un'approvazione LLM sbagliata su questi path si autoalimenta. Fix: in `smista`, se un file (anche vecchio nome di un rename) cade in questa classe → COMMENT deterministico e merge all'operatore. Oggi non sfruttabile: il ruleset non richiede approvazioni.
- **R-158-2 (BASSA)**: `decidi` approva con testo incoerente. Sonde riprodotte, tutte APPROVE: (a) preambolo "la VERIFICA ESTERNA precedente era APPROVATO" prima della riga vera "VERIFICA ESTERNA #1 — BOCCIATO", con campo APPROVATO (`_RIGA_VERDETTO` prende la prima occorrenza); (b) "V-1 — MEDIA — x" senza parentesi con JSON BASSA; (c) "F-1 (MEDIA)"; (d) "V-1 (MEDIA)" solo in RACCOMANDAZIONE; (e) "APPROVATO CON RISERVE" con `finding: []`. Fix: ancorare `^VERIFICA ESTERNA` con `re.M` e pretendere che tutte le occorrenze coincidano col campo; nella sezione FINDING qualsiasi `\b(ALTA|MEDIA)\b` → COMMENT; "CON RISERVE" con zero finding → COMMENT; ciascuno col suo test.
- **R-158-3 (BASSA, fail-closed)**: la `concurrency` a livello di workflow cancella verifiche buone: ogni evento che non deve far partire il bot (altra etichetta aggiunta subito dopo `verifica`, es. `gh pr create --label x --label verifica`, o un `opened` senza etichette in ritardo) apre una run con job saltati che cancella la verifica in corso → nessuna review, quota sprecata. Fix: `concurrency` sui job `verifica`/`esito`.
- **R-158-4 (BASSA)**: `Bash(gh api:*)` permette `--hostname <host esterno>`; l'action ripulisce l'env dei sottoprocessi solo con `allowed_non_write_users`; con `Read` senza limiti di path (`/proc/self/environ`) una prompt injection nella PR potrebbe esfiltrare `CLAUDE_CODE_OAUTH_TOKEN`. Non porta ad approvazioni (la chiave dell'App non è in quel job). Fix: togliere `gh api` (bastano `gh pr view/checks/diff`, `gh run view`).
- **R-158-5 (DECISIONE UMANA — coerenza con `.claude/verifica_esterna.md`)**: il bot è di sola lettura, quindi non può applicare "Prova, non leggere" (niente test, niente mutation), e la soglia di approvazione ignora NON VERIFICATO: un APPROVE del bot è più debole della verifica §4quater locale. L'operatore deve decidere se in variante B la §4quater resta obbligatoria accanto al bot, e dove vengono importate in stato_progetto.md le riserve BASSE che oggi vivono solo nel corpo della review.
- **Cosmetica**: `componi_corpo` non tronca le descrizioni dei finding minori; un corpo oltre 65536 caratteri fa fallire la POST (fail-closed, ma si perde un APPROVE).

Le 2 mutation dichiarate equivalenti lo sono davvero (`{}` → "verdetto strutturato incompleto"; testo di soli spazi senza riga VERIFICA ESTERNA). Le 24 mutation complessive non le ho rilanciate.

**Rischi esplicitamente esclusi (NON verificati)**
- Esecuzione reale del workflow: `pull_request_target` gira solo dalla definizione su main, quindi la prima prova reale arriva dopo il merge (convalida B2). Non verificato, perché richiede il repo configurato: che i segreti dell'environment ristretto a main siano concessi davvero a `pull_request_target` (che usa main come ref); che `checkHumanActor` dell'action accetti l'attore dei push; che `structured_output` venga popolato con `claude_code_oauth_token`.
- actionlint non eseguito (non installato). Mutation non rilanciate.
- Prompt injection riuscita (un LLM convinto ad approvare dal contenuto della PR) — rischio residuo intrinseco al design, che lo strato deterministico non può chiudere; R-158-1 ne limita il danno sui path più critici.
- Doc-only approvate senza LLM: possono alterare reports/stato_progetto.md (finding "chiusi" senza prova). Scelta dichiarata dell'operatore (dosaggio), non contestata.

**Memoria**: riga contatore #158 + 2 lezioni in `.claude/agents/memoria_revisore.md`, committate da sole (commit `05a4494`, `chore(revisore): memoria review #158`). Index del diff sotto review intatto (5 file, +777).

### Review 159

## VERDETTO: APPROVATO CON RISERVE

Review #159 — seconda review del diff STAGED (worktree `/Users/gas/Gas/.claude/worktrees/gate-ip-ottetti`, branch feat/verifica-bot). Letti prima: CLAUDE.md, reports/stato_progetto.md, memoria (riga #158).

R-158-2, R-158-3, R-158-4 sono chiuse; R-158-1 è chiusa solo IN PARTE: mancano path della macchina del bot che il bot carica davvero a runtime (R-159-1). Con l'operatore che chiede sicurezza alta e una correzione di poche righe, consiglio di chiudere R-159-1 PRIMA del commit. Non blocco perché è una riserva della stessa classe di R-158-1 (MEDIA) e oggi l'approvazione del bot non decide nessun merge (variante A).

**Elementi del diff esaminati**
- `scripts/bot_esito.py:98` (macchina del bot → COMMENT prima di ogni altro controllo, anche doc-only e head) — rischio: ordine aggirabile — **ok**; mutation `.github/`→`.githubX/` dà 2 failed.
- `scripts/bot_esito.py:192` (approva solo col valore esatto "false"; assente o strano = macchina del bot) — rischio: output di smista vuoto che lascia approvare — **ok**; mutation `!= "false"`→`== "true"` dà 4 failed.
- `scripts/bot_esito.py:38` (elenco MACCHINA_BOT) — rischio: path del bot dimenticati — **riserva R-159-1**.
- `scripts/bot_esito.py:51` (riga verdetto ancorata `^` + `re.M`, tutte le righe coincidenti) — **ok**; senza `^` 1 failed, senza `re.M` 2 failed; residuo R-159-4.
- `scripts/bot_esito.py:90` (`if g in gruppo`, confronto per sottostringa) — rischio: falsi blocchi su testo innocuo — **riserva R-159-3**.
- `.github/workflows/verifica-bot.yml:73`, `.github/workflows/verifica-bot.yml:205` (`concurrency` solo su verifica/esito; smista senza; un evento non qualificante salta tutti i job) — **ok**. Verificato il caso `opened`+`labeled` con la stessa head: la prima `esito` pubblica un COMMENT innocuo, l'APPROVE successivo prevale.
- `.github/workflows/verifica-bot.yml:141` (e :156, :171): i claude_args non passano `--setting-sources` — **riserva R-159-1**.
- `tests/test_unit_verifica_bot.py:239`: `docs/CLAUDE.md` esplicitamente fra i "non macchina del bot" — riserva R-159-1.
- Contesto: `.claude/settings.json:36` (hook PreToolUse Bash → review_gate.sh), `.claude/hooks/session_end.sh:37` (`git push`).

**Riprodotto da me**: 106 passed; mutation a campione 5/5 uccise (voce `.github/`, `!= "false"`, `re.M`, CON RISERVE senza finding, ancora `^`); `scripts/bot_esito.py` ripristinato e identico allo stage, index intatto (5 file, 956 righe).

**Riserve**
- **R-159-1 (MEDIA — R-158-1 non chiusa del tutto)**: clonata claude-code-action al commit pinnato (cab360f). In `base-action/src/parse-sdk-options.ts` riga 340 il default di `settingSources` è `["user","project","local"]` → il job verifica carica `.claude/settings.json` di main con TUTTI i suoi hook: review_gate.sh a ogni Bash, scrivi_rep.sh/promemoria_end.sh su Stop, session_end.sh (`git push`) su SessionEnd; review_gate.sh chiama `scripts/hash_diff_staged.sh`. Gli hook sono bash arbitrario, girano con `CLAUDE_CODE_OAUTH_TOKEN` nell'env, possono andare in rete e `--allowedTools` non li limita. Nessuno di questi file è in MACCHINA_BOT: una PR che modifica `.claude/hooks/review_gate.sh` non è "macchina del bot"; se l'LLM la approva, dopo il merge quel codice gira col token dell'abbonamento. Stessa classe di R-158-1. Secondo effetto: con le impostazioni di progetto attive Claude Code carica i CLAUDE.md annidati delle cartelle che legge sotto ./pr: un `modules/CLAUDE.md` aggiunto dalla PR diventa istruzioni del verificatore durante la verifica di quella stessa PR (`docs/CLAUDE.md` è proprio nel test_no). Fix: (1) `--setting-sources user` nei 3 claude_args (l'action lo supporta, righe 340-348): niente hook, settings o CLAUDE.md del repo nel bot; (2) per prudenza `.claude/hooks/` in MACCHINA_BOT; (3) test sul workflow che pretende `--setting-sources user` in ogni step dell'action; (4) togliere `docs/CLAUDE.md` dal test_no oppure match sul nome base `CLAUDE.md`/`CLAUDE.local.md` in qualsiasi cartella. Da NON fare: tutta `.claude/` in MACCHINA_BOT (`.claude/agents/memoria_revisore.md` cambia a ogni fine-task e bloccherebbe quasi tutte le PR).
- **R-159-2 (BASSA-MEDIA)**: il repo è **PUBBLICO** (gh repo view). `Read` senza ambito permette `/proc/self/environ`; un'iniezione nel contenuto della PR può far finire il token OAuth nel campo `testo`, che `componi_corpo` pubblica nella review (pubblica anche quella). Fix: in `componi_corpo`/`decidi`, se il testo contiene `sk-ant-`, `ghs_`, `ghp_`, `-----BEGIN` → COMMENT senza testo; in aggiunta `Read(./**)` in STRUMENTI.
- **R-159-3 (BASSA, fail-closed)**: sonde su `decidi` con verdetto APPROVATO e finding vuoti, finite in COMMENT: "CI-1 (test saltati su macOS)" (SALTATI contiene ALTA, anche minuscolo per via di `.upper()`); "SHA-256 (in media 3 ms)"; "PR-131 (parte multimediale)"; "UTF-8 (caratteri ad alta codifica)"; "FINDING: nessun finding ALTA/MEDIA." (la frase più naturale di un verdetto pulito); il segnaposto del protocollo ripetuto tale e quale. Stessa forma "(… mediante gh run view)", non sondata. Fix: `re.findall(r"\b(ALTA|MEDIA|BASSA|COSMETICA)\b", gruppo)` al posto di `g in gruppo`, con test su queste frasi; "nessun finding ALTA/MEDIA" resta un compromesso dichiarato (lo gestisce il prompt).
- **R-159-4 (BASSA)**: passano ancora come APPROVE: la riga "Verifica esterna: BOCCIATO" minuscola (ignorata, `_RIGA_VERDETTO` senza `re.I`); "V-1 — media — x" minuscolo senza parentesi con JSON BASSA. È il residuo della scelta "solo maiuscole"; resta valido il campo strutturato. `re.I` sulla riga del verdetto costa poco.
- R-158-5 resta una decisione umana (la porta l'agente principale).

**Rischi esplicitamente esclusi**: comportamento reale su GitHub (run vere, caricamento effettivo degli hook nel runner, secret scanning di GitHub sul corpo della review, esito della concurrency su `cancelled()` dei job a valle) non riproducibile in locale; le conclusioni su settingSources vengono dalla lettura del sorgente dell'action pinnata, non da una run. Le 43 mutation dichiarate riprodotte solo a campione (5).

Memoria aggiornata: riga #159 + 2 lezioni ("macchina del bot" da costruire dal runtime dell'agente; filtri a parola su testo italiano sempre con `\b`), committata da sola con `scripts/commit_memoria_revisore.sh` (commit d37d875). Index staged intatto.

### Review 160

## VERDETTO: APPROVATO CON RISERVE

Terza review, breve: solo le correzioni R-159-1..4 e i loro effetti collaterali, sul diff staged della worktree `/Users/gas/Gas/.claude/worktrees/gate-ip-ottetti` (branch feat/verifica-bot). Letti prima CLAUDE.md (già nel contesto), le righe di stato_progetto.md sul bot e la memoria fino a #159.

**Elementi esaminati**
- `.github/workflows/verifica-bot.yml:148`, `.github/workflows/verifica-bot.yml:164`, `.github/workflows/verifica-bot.yml:180` (`--setting-sources user` nei 3 `claude_args`) — rischio: l'action pinnata ignora il flag e torna al default — sorgente al commit cab360f: `base-action/src/parse-sdk-options.ts` riga 340 usa il flag se c'è, altrimenti `["user","project","local"]` — **ok**; il test `tests/test_unit_verifica_bot.py:503` lo pretende su tutti e 3 i passi.
- `.github/workflows/verifica-bot.yml:101` (`Read(./**)`, il punto da verificare) — rischio: sintassi non valida o lettura bloccata su ./pr e ./CLAUDE.md. Lato action (sorgente verificato): le parentesi passano intatte grazie all'escape dei metacaratteri (`parse-sdk-options.ts` righe 28-55, nato proprio per il bug in cui `Bash(gh:*)` diventava `Bash`); split su virgola con trim (riga 232), l'a capo del `>-` non dà problemi; `cwd` non sovrascritto → resta la root di main, che contiene ./pr e ./CLAUDE.md. Lato Claude Code (documentazione, non eseguito): `./path` relativo alla cartella corrente, `**` glob in stile gitignore, la lettura dentro la cartella di lavoro è permessa anche senza regola. **ok**: il bot non resta cieco (confidenza alta lato action, media lato CLI).
- `scripts/bot_esito.py:77` (`NOMI_MACCHINA_BOT` sul nome del file) — sonda: `docs/CLAUDE.md` → True, `pr/x/CLAUDE.local.md` → True, `docs/MYCLAUDE.md` → False, `.claude/agents/memoria_revisore.md` → False — **ok**.
- `scripts/bot_esito.py:54` e `scripts/bot_esito.py:127` / `scripts/bot_esito.py:164` (`_SEGRETO` → COMMENT e testo non pubblicato) — **ok**, con il limite R-160-1.
- `scripts/bot_esito.py:100` (tra parentesi conta solo la gravità che apre la parentesi) — sonda: `(Alta priorità)` → COMMENT ALTA; "(test saltati)" e "(in media 3 ms)" approvano (ci sono i test); `(riserva: media)` minuscolo approva: compromesso dichiarato, il campo `finding` strutturato resta quello che fa fede — **ok**.
- `scripts/bot_esito.py:59` / `scripts/bot_esito.py:129` (R-159-4: `re.I` + confronto in maiuscolo; una riga ambigua → COMMENT, fallisce chiuso) — **ok**, con l'eccezione R-160-2.

Test: **126 passed**, riprodotti. Mutation non rifatta (dosaggio dei costi): accetto il 55/56 dichiarato, sopravvissuto equivalente.

**Riserve (BASSA, non bloccanti, da tracciare in stato_progetto.md)**
- **R-160-1 (BASSA)**: `Read(./**)` limita solo Read, non la capacità di leggere file: `Grep` e `Glob` sono autorizzati senza restrizioni di percorso; `Bash(git -C pr diff:*)` permette `git -C pr diff --no-index /proc/self/environ /dev/null`. `_SEGRETO` riconosce solo le forme letterali: un segreto offuscato su richiesta di una prompt injection passerebbe. BASSA perché il bot parte solo su PR dello stesso repo aperte dal proprietario, con l'etichetta messa dall'agente. Fix possibile: `Grep(./**)`/`Glob(./**)` se la sintassi è supportata (non verificato) e niente `--no-index` nel prefisso git, oppure dichiararlo limite MITIGATO.
- **R-160-2 (BASSA)**: con `"VERIFICA ESTERNA: NON APPROVATO"` nel testo e campo `APPROVATO` → **APPROVE** (sonda eseguita). La regex della riga non ha `\b` né controllo sulla negazione (anche "DISAPPROVATO"); il difetto c'era già prima di `re.I`. Il campo strutturato fa fede, ma il controllo di coerenza non coglie il caso. Fix: `\b` davanti all'esito + COMMENT se la riga contiene `NON APPROVATO`.

**Cosa NON ho verificato**: il comportamento effettivo del CLI Claude Code con `Read(./**)` e le regole di percorso su Grep/Glob con autorizzazione senza restrizioni (binario chiuso, non riproducibile in dev: mi baso sulla documentazione; la prima run reale del workflow è la prova definitiva). Comportamento su GitHub (environment, ruleset, App) e mutation completa: fuori dal perimetro ridotto richiesto.

Memoria aggiornata: riga #160 + una lezione ("restringere UN tool non restringe la capacità: chiudere la classe dei tool che leggono"). Commit 39ea8a4 (`chore(revisore): memoria review #160`). Diff staged non toccato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py`, `brains/`, `modules/`: suite kernel non rilanciata. Modificati `tests/` (nuovo `tests/test_unit_verifica_bot.py`) e la macchina di controllo. Suite di controllo (pytest locale: hooks, gate, handoff_check, gasmerge, verifica_bot): **273 → 399 passed** (`399 passed in 95.58s`), 0 FAIL. Nuova suite: 126 passed. Mutation su `scripts/bot_esito.py`: 56 mutation, 55 KILLED, 1 SURVIVED equivalente.

## §6 STATO CI

```
completed	failure	feat(verifica-bot): bot di verifica esterna con identità separata (V-…	CI	feat/verifica-bot	push	37352159123	1m28s	2026-10-05T17:56:12Z

Mappatura commit→run:
- 5010cef (testa del push precedente): run 37352159123 — unit-suite success, handoff-check failure (handoff non ancora nel diff: atteso, lo porta il commit di fine-task).
- 39ea8a4, d37d875, 05a4494 (memoria revisore): nessuna run su questi SHA (pushati insieme a 5010cef, testati solo nell'albero di 5010cef).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff (copertura pre-merge: gasmerge, gh pr checks --watch).
```

## §7 RISERVE APERTE

- **R-160-1 (BASSA)**: letture fuori cartella via Grep/Glob/`git diff --no-index`; `_SEGRETO` solo su forme letterali → fetta B2.
- **R-160-2 (BASSA)**: "VERIFICA ESTERNA: NON APPROVATO" col campo APPROVATO → APPROVE → fetta B2.
- **R-158-5 (DECISIONE UMANA)**: bot di sola lettura; §4quater locale obbligatoria in variante B? (§0.3).
- Non verificato fino al primo run reale: environment ristretto a main concesso a `pull_request_target`, `structured_output` con token OAuth, attore dei push accettato dall'action, `Read(./**)` lato CLI.
- Da sessioni precedenti: R-155-3, V-3 / V-5 #121, R-160-x a parte; V-3 #127 → fetta B2.
