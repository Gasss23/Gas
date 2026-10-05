# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-05 — V-B vera, fetta B1: bot di verifica esterna su GitHub (identità separata) + chiusura delle due verifiche esterne #130

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #130 (https://github.com/Gasss23/Gas/pull/130).
2. Setup del bot dopo il merge: `reports/setup_verifica_bot.md` (token dell'abbonamento, GitHub App dedicata, environment `verifica-bot` ristretto a main). Senza setup il bot non parte.
3. **R-158-5**: il bot è di sola lettura e non esegue test. In variante B la verifica esterna locale §4quater resta obbligatoria accanto al bot? (consiglio: sì per le fette nel perimetro di review).
4. Dopo il test di convalida (fetta B2): ruleset `main-lock` con 1 approvazione, "dismiss stale approvals", "require approval of the most recent push" (passi forniti al momento).
5. **R-161-2**: con `scripts/` nella macchina del bot, la PR della fetta B2 (`gasmerge --auto`) non sarà mai approvata dal bot: il test di convalida dell'APPROVE automatico richiede una PR successiva fuori dalla macchina (es. una piccola fetta del motore).
6. **Terza verifica esterna NON lanciata (scelta di dosaggio, da confermare)**: la seconda verifica (§9) ha trovato una sola MEDIA (V-1, Grep/Glob fuori cartella) e ha proposto e provato lei stessa la correzione (`Grep(./**)`/`Glob(./**)`), applicata in `c215635` con review #162 e mutation mirata 10/10. Le correzioni saranno ricontrollate dalla verifica della fetta B2. Se l'operatore vuole la terza verifica prima del merge, va lanciata ora.
7. Ancora aperte da sessioni precedenti: R-155-3 (Codex e Claude Code nella stessa cartella), V-3 / V-5 della verifica #121.

---

## §1 SCOPE & ESITO FETTE

- **Fetta B1 — bot di verifica (workflow + `scripts/bot_esito.py` + test)**: `FATTA` — commit `5010cef`, review #158/#159/#160 APPROVATO CON RISERVE; 126 test nuovi; mutation 55/56 (1 equivalente).
- **Riserve #158 e #159**: `FATTA` — tutte chiuse con test prima del commit, tranne R-158-5 (decisione umana, §0.3).
- **Verifica esterna #130 (APPROVATO CON RISERVE, V-1/V-2 MEDIA)**: `FATTA` — V-1 (niente git fra gli strumenti), V-2 (credenziali su tutto il verdetto), V-3 (test permessi App e needs), V-4 (negazioni e gravità a parole, chiude anche R-160-2), V-5 (macchina del bot allargata, doc-only solo .md), V-6 (ordine del setup) chiuse prima del merge; commit `43f84fb`, review #161. Verdetto integrale in §8.
- **Seconda verifica esterna #130 (APPROVATO CON RISERVE, V-1 MEDIA)**: `FATTA` — V-1 (Grep/Glob limitati a `./**` + scrub dell'ambiente: chiude anche R-160-1), V-3 (test sugli `if`, su `HEAD_ANALIZZATA` e sul ref del checkout), V-4 (nessun TypeError con `finding` non lista), V-5 (etichetta `verifica`: passo D del setup), V-6 (doc-only esclude `reports/setup_*` e `reports/design_*`) chiuse; commit `c215635`, review #162. Verdetto integrale in §9.
- **Riserve BASSE aperte (V-2 della seconda verifica, R-161-1, R-162-1, R-162-2)**: `DEFERITA — fetta B2` (regola dell'operatore: le basse passano, si aggiustano dopo).
- **Fetta B2 — `gasmerge --auto` + V-3 #127 + test di convalida**: `DEFERITA — richiede B1 su main e setup dell'operatore.`
- **Ruleset**: `DEFERITA — dopo la convalida.`
- **Residui V-2 #127 e V-2/V-3 #129**: `DEFERITA — decisione operatore (2026-10-05): solo V-3 #127, nella fetta B2.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 +++++++
 .claude/perimetro_review.txt       |   1 +
 .github/workflows/ci.yml           |  15 +++++++++
 .github/workflows/verifica-bot.yml | 248 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  15 +++++----
 reports/handoff.md                 | 374 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------
 reports/setup_verifica_bot.md      |  57 ++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   4 +--
 reports/ultimo_report.md           |  44 +++++++++++--------------
 scripts/bot_esito.py               | 278 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_verifica_bot.py    | 651 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 1562 insertions(+), 137 deletions(-)
```

NB: conteggi di `reports/handoff.md` approssimati per costruzione (il file conta se stesso).

## §3 GIT LOG --ONELINE (sessione)

```
c215635 fix(verifica-bot): chiude V-1, V-3, V-4, V-6 della seconda verifica esterna #130 — review #162
17e49de chore(revisore): memoria review #162 — APPROVATO CON RISERVE
8e11aa5 docs(verifica-bot): fine-task — correzioni verifica esterna #130 (V-1..V-6), handoff con review #161 e verdetto integrale
43f84fb fix(verifica-bot): chiude V-1..V-5 della verifica esterna #130 — review #161
cf68a2e chore(revisore): memoria review #161 — APPROVATO CON RISERVE
7d6289c docs(verifica-bot): fine-task — V-B fetta B1, handoff (review #158/#159/#160), guida setup operatore
5010cef feat(verifica-bot): bot di verifica esterna con identità separata (V-B vera, fetta B1) — review #158/#159/#160
39ea8a4 chore(revisore): memoria review #160 — APPROVATO CON RISERVE
d37d875 chore(revisore): memoria review #159 — APPROVATO CON RISERVE
05a4494 chore(revisore): memoria review #158 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `5010cef` (workflow, script, test, ci, perimetro): review #158, #159, #160; commit `43f84fb` (correzioni della verifica esterna #130): review #161; commit `c215635` (correzioni della seconda verifica): review #162. Incollate per intero, nell'ordine. Il diff revisionato da #160 è quello committato (marcatore `segna_review_ok.sh` sullo stage revisionato).
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

### Review 161

## VERDETTO: APPROVATO CON RISERVE

Review #161: delta V-1..V-6 della verifica esterna sulla PR #130. Il diff staged è relativo a HEAD 7d6289c, branch `feat/verifica-bot` (il branch corrisponde a quello dichiarato). Il diff staged tocca 3 file, +141/-17. Prima della review ho letto CLAUDE.md, la sezione B1 di `reports/stato_progetto.md` e la coda della memoria. Per dosare la quota le letture sono state mirate.

**Elementi del diff esaminati**
- `.github/workflows/verifica-bot.yml:103`: STRUMENTI resta `Read(./**),Grep,Glob` più i soli `gh pr view/diff/checks` e `gh run view/list`, senza nessun git. Rischio esaminato: scrittura di file tramite `--output`. `gh` non ha flag che scrivono file fra quelli consentiti, e il prompt è coerente (diff e commit arrivano da gh). Esito: ok.
- `scripts/bot_esito.py:128` `contiene_segreti`: applica `_SEGRETO` su `json.dumps(verdetto)` intero, e un verdetto non serializzabile conta come segreto. Rischio esaminato: id o descrizione con un token che finisce nella review pubblica. Con la sonda, `{"finding":[{"id":"ghs_abc"}]}` dà True e un set dà True. Le forme di `_SEGRETO` non contengono caratteri che json.dumps fa escape. Esito: ok.
- `scripts/bot_esito.py:190` `componi_corpo`: se scatta il controllo sui segreti non pubblica niente del verdetto, né le riserve minori né il testo. Con la sonda, una descrizione BASSA con `sk-ant-` produce solo il segnaposto. Esito: ok.
- `scripts/bot_esito.py:74` `_NEGAZIONE` su ogni riga che inizia con VERIFICA ESTERNA. Rischio esaminato: varianti di negazione. "non approvato" dà COMMENT, ma **"VERIFICA ESTERNA: NON-APPROVATO" e "VERIFICA ESTERNA: NON È APPROVATO" con il campo APPROVATO danno APPROVE**. Il motivo è che `\s+` richiede uno spazio subito prima di APPROVATO. Esito: riserva R-161-1.
- `scripts/bot_esito.py:79` `_FINDING_GRAVE_A_PAROLE`: "- V-1 — Media: x" dà COMMENT, "V-1 (BASSA) — riga lunga" dà APPROVE, e la frase "nessun finding di gravità media o alta" fuori da una riga V-n non blocca. Esito: ok. Il falso blocco su "in media" dentro una riga V-n è dichiarato ed è fail-closed.
- `scripts/bot_esito.py:48` MACCHINA_BOT con `scripts/`, perimetro, revisore, fine-task e i 5 test (corrispondono ai file reali in `tests/`). `solo_reports` accetta solo `.md`: "reports/x.MD" resta fuori, quindi fail-closed. Esito: ok.
- `tests/test_unit_verifica_bot.py`: test sul set esatto `permission-*` = `{pull-requests: write}`, sui `needs` (esito dipende da smista e verifica, verifica da smista), sull'assenza di git e sull'insieme esatto dei Bash(gh). Ho riprodotto 164 passed. Esito: ok.

**Riserve**
- **R-161-1 (BASSA)**: con il campo APPROVATO, "NON-APPROVATO" e "NON È APPROVATO" sulla riga del verdetto portano ad APPROVE. Proposta fail-closed: `\bNON\b[^\n]*?(APPROVATO|BOCCIATO)` oppure `DIS(APPROVATO|BOCCIATO)`, con un test per ciascuna forma. Va chiusa insieme a R-160-2 nella fetta B2, oppure subito se l'operatore applica la regola "MEDIA prima del merge" anche alle BASSA del bot.
- **R-161-2 (DECISIONE UMANA / ROADMAP)**: la conseguenza che hai indicato è corretta e voluta: con `scripts/` in MACCHINA_BOT, la PR di B2 (`gasmerge --auto`, che tocca `scripts/gasmerge.sh`) non sarà mai approvata dal bot (sonda: `tocca_macchina_bot(["scripts/gasmerge.sh"])` dà True). Però `reports/stato_progetto.md:9` dice "la PR di B2 è il test di convalida", e questo non regge più. Per vedere un APPROVE reale serve una PR fuori dalla macchina, per esempio una piccola fetta del motore. Va aggiornata la roadmap o lo stato prima di B2.

**Rischio escluso**: non ho verificato se il permission parser di Claude Code in modalità headless nega le redirezioni della shell dentro un comando consentito con prefisso (`gh pr view 1 > "$GITHUB_ENV"` sotto `Bash(gh pr view:*)`). Togliere git chiude la via `--output`, non la classe "scrittura via shell". Non è riproducibile senza eseguire l'action. Da provare nella fetta B2 o con una sonda nel runner. Restano aperte R-160-1 (Grep/Glob nudi, per cui la lettura fuori cartella resta mitigata solo da `_SEGRETO`) e R-158-5. Non ho rieseguito la mutation dichiarata (73 mutanti, 72 KILLED, 1 equivalente). Giudico plausibile l'equivalente "findall su sezione contro sezione.upper()" perché la regex usa re.I, ma non l'ho rieseguito.

**Memoria**: riga #161 e una lezione nuova sulle redirezioni con Bash(prefisso:*). Sono committate con `scripts/commit_memoria_revisore.sh` nel commit cf68a2e, che contiene solo la memoria; il diff staged è intatto (3 file, +141/-17).

### Review 162

## VERDETTO: APPROVATO CON RISERVE

Review #162. Diff staged nella worktree `/Users/gas/Gas/.claude/worktrees/gate-ip-ottetti`, branch `feat/verifica-bot` (controllato con `git branch --show-current`), rispetto a HEAD 8e11aa5. Tocca 3 file, con 41 righe aggiunte e 4 tolte. Prima della review ho letto CLAUDE.md, stato_progetto.md (solo le righe mirate) e la coda della mia memoria.

**Il tuo dubbio sullo scrub: il "1" funziona, non viene annullato.** L'ho controllato sul sorgente dell'action pinnata (`action.yml@cab360f`, riga 301):
`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: ${{ env.CLAUDE_CODE_SUBPROCESS_ENV_SCRUB || (inputs.allowed_non_write_users != '' && '1') || '' }}`
L'espressione legge prima l'env che lo step eredita, quindi l'env del job. Lo conferma anche `docs/security.md` dello stesso commit: la disattivazione si fa "in your workflow or job `env:` block", cioè proprio dove hai messo la variabile. Il valore vuoto si usa solo se il job non la imposta. C'è di più: nel binario del CLI 2.1.289 (locale) la funzione di decisione è `Pe ??= en(e) || en(GITHUB_ACTIONS) && !Do(e)`. Vuol dire che dentro GitHub Actions lo scrub è già attivo di default, a meno di disattivarlo con 0/false/no/off. Il tuo "1" è quindi una difesa in più, utile se un CLI futuro cambiasse il default. Non è un'impostazione persa. Nella lista delle variabili ripulite ci sono `CLAUDE_CODE_OAUTH_TOKEN`, `ACTIONS_ID_TOKEN_*`, `ACTIONS_RUNTIME_*` e `OVERRIDE_GITHUB_TOKEN`. Non ci sono `GH_TOKEN` né `GITHUB_TOKEN`, quindi i 5 comandi gh continuano a funzionare. Con lo scrub attivo il CLI forza la modalità permessi "default" e chiede un allowedTools esplicito, che c'è già.

**Elementi del diff esaminati**
- `.github/workflows/verifica-bot.yml:107` — STRUMENTI ora è `Read(./**),Grep(./**),Glob(./**)` più 5 comandi `Bash(gh …:*)`. Rischio esaminato: restava qualche tool che legge file fuori dalla cartella (la lezione #160 sui tool come classe). Il test `test_lettura_limitata_alla_cartella` vieta i tool nudi e qualsiasi prefisso che non sia Read/Grep/Glob/Bash. La classe "tool che leggono file" è chiusa: git non c'è più dalla #161. Esito: ok.
- `.github/workflows/verifica-bot.yml:94` — `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: "1"` nell'env del job. Rischio esaminato: valore sovrascritto dallo step dell'action. Escluso, vedi sopra. Esito: ok, con la riserva R-162-1.
- `scripts/bot_esito.py:196` — `elenco` usato solo se è una lista. Rischio esaminato: TypeError, quindi nessuna review pubblicata. Ho fatto una mutation (`elenco or []`): 2 test falliscono (finding=5 e finding=True), quindi viene presa. I casi `"x"` e `{"a":1}` non andavano in crash nemmeno prima, ma restano utili come casi da tenere fissi. Esito: ok.
- `scripts/bot_esito.py:62` / `:91` — `DOC_DA_VERIFICARE` escluso dal percorso doc-only. Rischio esaminato: un setup o un design passa senza LLM. Ho tolto la clausola come mutation: 2 test falliscono, quindi viene presa. È fail-closed: un .md in più passa dall'LLM e non c'è falso APPROVE. Esito: ok.
- `tests/test_unit_verifica_bot.py:619` — test con uguaglianza esatta sugli `if` di verifica (`:73`) ed esito (`:215`), sul `ref` del checkout di `./pr` e su `HEAD_ANALIZZATA`. Ho confrontato il testo dei test con il YAML (`grep if:`): corrispondono. Esito: ok.

**Riproduzione**: `tests/test_unit_verifica_bot.py` dà 174 passed. Ho fatto 2 mutation mie e sono state prese entrambe. Il file è stato ripristinato dall'index (`cmp` uguale alla copia di backup) e lo stage è intatto.

**Riserve**
- R-162-1 (BASSA): bubblewrap e l'isolamento dei processi non sono attivi. Gli step che li installano partono solo se `allowed_non_write_users` non è vuoto. Resta solo lo scrub delle variabili d'ambiente. La barriera principale contro `/proc/self/environ` resta `Read/Grep/Glob(./**)`. Va scritto così nei report: niente sandbox PID.
- R-162-2 (BASSA): `test_ambiente_dei_sottoprocessi_ripulito` controlla solo l'env del job, non l'espressione dell'action. Va bene finché il pin `cab360f` non cambia. Al prossimo aggiornamento del pin bisogna ricontrollare la riga 301 e il default del CLI.
- Restano rimandate a B2, come hai dichiarato tu: V-2 e R-161-1.

**Cosa non ho verificato**: che l'action installi davvero il CLI 2.1.289. Non ho trovato il pin della versione in `action.yml`: ho analizzato il binario locale 2.1.289 fidandomi della sonda del verificatore. Non ho verificato nemmeno il comportamento reale su runner GitHub (la variabile che passa dall'env del job all'env della composite action), perché in locale non si può riprodurre. Va confermato alla prima run vera del bot.

Memoria aggiornata: riga #162 più una lezione, commit `17e49de` fatto con `scripts/commit_memoria_revisore.sh`. Il diff staged non è stato toccato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py`, `brains/`, `modules/`: suite kernel non rilanciata. Modificati `tests/` (nuovo `tests/test_unit_verifica_bot.py`) e la macchina di controllo. Suite di controllo (pytest locale: hooks, gate, handoff_check, gasmerge, verifica_bot): **273 → 447 passed** (`447 passed in 89.33s`), 0 FAIL. Nuova suite: 174 passed. Mutation su `scripts/bot_esito.py`: 73 mutation, 72 KILLED, 1 SURVIVED equivalente (`findall` su `sezione` contro `sezione.upper()`, identico con `re.I`); mutation mirata sulle correzioni della seconda verifica (script + workflow): 10/10 KILLED.

## §6 STATO CI

```
queued		fix(verifica-bot): chiude V-1, V-3, V-4, V-6 della seconda verifica e…	CI	feat/verifica-bot	push	37368299432	1m14s	2026-10-05T20:12:33Z
completed	failure	docs(verifica-bot): fine-task — correzioni verifica esterna #130 (V-1…	CI	feat/verifica-bot	push	37366037273	15m3s	2026-10-05T19:51:00Z
completed	failure	fix(verifica-bot): chiude V-1..V-5 della verifica esterna #130 — revi…	CI	feat/verifica-bot	push	37364747687	15m3s	2026-10-05T19:38:49Z
completed	success	docs(verifica-bot): fine-task — V-B fetta B1, handoff (review #158/#1…	CI	feat/verifica-bot	push	37352488135	1m16s	2026-10-05T17:58:49Z
completed	failure	feat(verifica-bot): bot di verifica esterna con identità separata (V-…	CI	feat/verifica-bot	push	37352159123	1m28s	2026-10-05T17:56:12Z

Mappatura commit→run:
- c215635 (testa dell'ultimo push, con 17e49de): run 37368299432 — QUEUED alla scrittura dell'handoff.
- 17e49de (memoria revisore #162): nessuna run su questo SHA (pushato con c215635).
- 8e11aa5 (fine-task precedente): run 37366037273 — unit-suite success; handoff-check CANCELLED dopo 15 min in coda (runner GitHub), nessun test fallito.
- 43f84fb (con cf68a2e): run 37364747687 — handoff-check success; unit-suite CANCELLED dopo 15 min in coda, mai eseguito su questo SHA (stesso albero di codice di 8e11aa5, dove è verde).
- cf68a2e: nessuna run su questo SHA (pushato con 43f84fb).
- 7d6289c: run 37352488135 — success (unit-suite + handoff-check).
- 5010cef: run 37352159123 — unit-suite success, handoff-check failure (handoff non ancora nel diff: atteso).
- 39ea8a4, d37d875, 05a4494 (memoria revisore): nessuna run su questi SHA (testati nell'albero di 5010cef).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff (copertura pre-merge: gasmerge, gh pr checks --watch).
```

## §7 RISERVE APERTE

- **R-160-1**: CHIUSA in `c215635` (V-1 della seconda verifica: `Grep(./**)`/`Glob(./**)` + scrub). `contiene_segreti` resta solo sulle forme letterali (secondario).
- **V-2 seconda verifica (BASSA)**: negazioni e gravità fuori vocabolario ("NON risulta APPROVATO", "CRITICAL", "blocker", spazi a larghezza zero) → fetta B2: decidere solo sul campo strutturato `gravita`.
- **R-162-1 (BASSA)**: niente sandbox PID/bubblewrap nel job (solo con `allowed_non_write_users`): barriera principale `Read/Grep/Glob(./**)` + scrub dell'ambiente.
- **R-162-2 (BASSA)**: lo scrub dipende dall'espressione dell'action al pin `cab360f`: ricontrollare ad ogni aggiornamento del pin.
- **R-160-2**: CHIUSA in `43f84fb` (V-4 #130), salvo le forme di R-161-1.
- **R-161-1 (BASSA)**: "NON-APPROVATO" / "NON È APPROVATO" sulla riga del verdetto col campo APPROVATO → APPROVE → fetta B2.
- **R-161-2 (ROADMAP)**: la PR di B2 non sarà approvata dal bot (tocca `scripts/`); convalida dell'APPROVE con una PR fuori dalla macchina (§0.5).
- **Redirezioni di shell** sotto `Bash(gh ...:*)`: CHIUSA — provate dalla seconda verifica sul CLI 2.1.289 headless, tutte DENIED (§9).
- **R-158-5 (DECISIONE UMANA)**: bot di sola lettura; §4quater locale obbligatoria in variante B? (§0.3).
- Non verificato fino al primo run reale: environment ristretto a main concesso a `pull_request_target`, `structured_output` con token OAuth, attore dei push accettato dall'action, `Read(./**)` lato CLI.
- Da sessioni precedenti: R-155-3, V-3 / V-5 #121, R-160-x a parte; V-3 #127 → fetta B2.

## §8 VERIFICA ESTERNA #130 (prima, verdetto integrale)

Agente nuovo (`general-purpose`, Sonnet) con il solo prompt `Applica .claude/verifica_esterna.md a: <URL_HANDOFF 7d6289c> <URL_PR #130>`. Esito riportato così com'è; le correzioni sono nel commit `43f84fb` (review #161).

```
VERIFICA ESTERNA PR #130 — APPROVATO CON RISERVE
(Il merge è innocuo ora: il bot non ha segreti né environment e il ruleset non richiede approvazioni. V-1 e V-2 vanno chiusi PRIMA del setup dell'operatore, cioè prima di mettere i segreti.)

Metodo: clone usa-e-getta nella scratchpad, checkout di 7d6289c (pinnato dall'URL), base f5fb9c1 (merge-base con origin/main). Ho letto `scripts/bot_esito.py` e `.github/workflows/verifica-bot.yml` per intero. Ho rilanciato la suite del bot e le suite di controllo. Ho eseguito sonde dirette su `decidi`/`componi_corpo`, mutation di campionamento su script e workflow, e prove di comportamento di git. Ho controllato GitHub (gh: PR, run CI, ruleset, impostazioni Actions, environments, SHA delle action). Ho clonato `anthropics/claude-code-action` a cab360f e letto il sorgente. Il repo reale non è stato toccato (lavoro solo in scratchpad; le mutation sono state ripristinate dopo ogni prova).

CLAIM VERIFICATI
- §2/§3 handoff vs git reali: VERO nella sostanza. Gli 11 file coincidono e i 4 commit del log coincidono. Il commit di fine-task 7d6289c è assente dal log, come dichiarato. I conteggi reali sono +1241/-149, contro +1222/-149 dichiarati, e `handoff.md` è 246 righe contro 227. L'handoff ammette l'approssimazione (COSMETICA).
- Delta test "273 → 399, nuova suite 126": VERO. Ho rilanciato `tests/test_unit_verifica_bot.py` (126 passed in 5.6s) e hooks+gate+handoff+gasmerge+bot (399 passed in 90s). Alla base mancano solo i 126 test del bot. La CI reale somma 102+40+74+57+126 = 399 (+19 voice).
- CI su 7d6289c: VERO. Run 37352488135 completed/success; `unit-suite` e `handoff-check` sono SUCCESS sulla PR. La run su 5010cef è fallita solo per `handoff-check` ("Run check_handoff (versione main)"), come dichiarato. `unit-suite` era verde.
- Check REQUIRED nel ruleset `main-lock` (id 18805824): `unit-suite` e `handoff-check`, entrambi `integration_id` 15368. `required_approving_review_count` è 0, `dismiss_stale_reviews_on_push` è false e `require_last_push_approval` è false. Coerente con "ruleset DEFERITA".
- `can_approve_pull_request_reviews=false`: VERO (API `actions/permissions/workflow`). Il repo è PUBBLICO. La PR è del proprietario, non da fork, non draft.
- Pin delle action: VERO. `actions/checkout@11d5960…` = tag v4/v4.4.0. `actions/create-github-app-token@bcd2ba4…` = v3/v3.2.0, con `client-id` e `permission-pull-requests` esistenti. `claude-code-action@cab360f` = v1/v1.0.241, e `structured_output` esiste.
- `--setting-sources user` rispettato dall'action: VERO (`parse-sdk-options.ts` riga 340). `pull_request_target` è accettato dall'action (`context.ts` riga 192) e la modalità agent non imposta `permissionMode` (default: i tool non elencati restano negati in headless). Il schema JSON e il parsing di `claude_args` sono corretti: la simulazione con `shlex` dà 10 token e la cascata ripulisce gli spazi dopo le virgole.
- Riserve dichiarate CHIUSE (R-158-1, R-158-2, R-158-3, R-159-1, R-159-3, R-159-4): provate con sonde e mutation. Eccezioni in V-2 (R-159-2 NON chiusa del tutto) e V-3/V-4.
- Riserve R-160-2 e R-160-1 "BASSE aperte": R-160-2 riprodotta, vedi V-4. Per R-160-1 la lettura fuori cartella è plausibile; ho trovato anche una capacità di SCRITTURA che nessuno ha segnalato (V-1).
- Mutation di campionamento su `bot_esito.py`: 5/5 uccise (head check, soglia bloccanti, `_SEGRETO`, `commit_id`, `MACCHINA_BOT`). Sul workflow: uccise `persist-credentials`, `environment`, `Bash(python:*)` aggiunto, `Write` aggiunto, `pull-requests: read`→`write`. Il "55/56" dichiarato non è esaustivo, vedi V-3.

FINDING
- V-1 (MEDIA) — Gli strumenti concessi non sono "sola lettura". `Bash(git -C pr log:*)` e `Bash(git -C pr show:*)` (e `diff`) accettano `--output=<file>`, che scrive un file arbitrario. Sonda riprodotta: `git log -1 --format=%B --output=../written.txt` su un commit con messaggio `BASH_ENV=/tmp/evil.sh` ha scritto esattamente quella riga. Il contenuto del messaggio di commit lo controlla la PR. Catena teorica: una prompt injection nella PR fa scrivere in `$GITHUB_ENV` (percorso scoprendo con Glob/Grep, che non hanno limiti di path) una riga `BASH_ENV=<file della PR>` oppure `S1=<verdetto>`. Lo step `raccogli` (bash) la esegue o la legge e falsifica il verdetto. Se la macchina del bot non è toccata, il gate deterministico approva. Questo contraddice "il codice della PR viene solo LETTO, mai eseguito" (testo del workflow e review #158). Il danno aggiuntivo rispetto a "il modello approva sotto injection" è modesto (nello step `raccogli` non ci sono segreti), ma la proprietà di sicurezza dichiarata è falsa. Non verificato a livello Claude Code: che il motore dei permessi lasci passare il flag. Fix: togliere `git -C pr log/diff/show` e usare `gh pr diff`/Read/Grep, oppure `--disallowedTools` con `Bash(*--output*)` e `Bash(*--no-index*)`. In più un test che rifiuti qualunque prefisso git nell'allowlist.
- V-2 (MEDIA) — R-159-2 ("credenziali nel testo pubblico: chiusa") è chiusa solo sul campo `testo`. `_SEGRETO` non viene applicato a `finding[].descrizione` né a `finding[].id`, e `componi_corpo` li pubblica per intero in APPROVE ("Riserve minori da aggiustare dopo il merge"). Sonda riprodotta: verdetto APPROVATO CON RISERVE con testo pulito e un finding BASSA con `descrizione = "sk-ant-oat01-…"` → `decidi` = APPROVE e il corpo della review pubblica contiene il token. Idem per `id = "ghp_abcdef"`. La review è pubblica (repo pubblico). Fix: applicare `_SEGRETO` a tutti i campi che vengono pubblicati (id, descrizione, motivo) e, se scatta, COMMENT senza pubblicare. Test per ciascun campo.
- V-3 (BASSA) — Buchi di test su invarianti di sicurezza dichiarati. Sostituire `permission-pull-requests: write` con `permission-contents: write`, o aggiungerlo, lascia 126/126 verdi. Quindi "il token dell'App ha solo PR write e nessun permesso sul contenuto" non è protetto da nessun test. Anche `needs: [smista, verifica]`→`[smista]` nel job `esito` sopravvive. Il "55/56 mutation" riguarda solo l'insieme scelto di mutazioni. Fix: test che pretendano esattamente il set di `permission-*` dello step `app` e `verifica` fra i `needs` di `esito`.
- V-4 (BASSA, ma da chiudere prima di `gasmerge --auto`) — R-160-2 confermata e più ampia di come dichiarata. Con campo APPROVATO, `VERIFICA ESTERNA #1 — NON APPROVATO` e `… — DISAPPROVATO` → APPROVE (sonda). Anche `FINDING: V-1 — grave: un bypass totale del gate` (gravità non in forma ALTA/MEDIA maiuscola e senza parentesi) → APPROVE, residuo di R-159-4. Solo "NON BOCCIATO" dà COMMENT. Con la fetta B2 (merge autonomo) il testo incoerente non può restare un compromesso: la decisione si regge solo sul campo strutturato scelto dal modello. Fix: `\b` e controllo della negazione (NON/DIS) sulla riga, più COMMENT se il testo cita parole di gravità in minuscolo dentro la sezione FINDING.
- V-5 (BASSA) — Perimetro di `MACCHINA_BOT` più stretto della macchina che decide i merge. Verificato con `tocca_macchina_bot` → False per `scripts/gasmerge.sh`, `scripts/check_verdetto.py`, `.claude/perimetro_review.txt`, `.claude/agents/revisore.md`, `tests/test_unit_verifica_bot.py`. Per queste PR decide solo l'LLM. Con B2 `scripts/gasmerge.sh` diventa l'attore del merge. Inoltre l'auto-approvazione doc-only senza LLM copre ogni path sotto `reports/`, compresi non-md (`reports/sonda_locale_suite.txt`, `reports/e2e_k3bis_output.txt`) e i report letti come istruzioni dalle sessioni successive. Il revisore #158 ha già registrato il secondo punto come scelta dell'operatore. Valuta se aggiungere `scripts/gasmerge.sh`, `scripts/check_*`, `.claude/perimetro_review.txt` a `MACCHINA_BOT` prima di B2.
- V-6 (BASSA, documentazione) — `reports/setup_verifica_bot.md` C1/C2: oggi `environments` è vuoto. Se dopo il merge una PR con etichetta `verifica` fa partire i job con `environment: verifica-bot`, GitHub crea l'environment SENZA regola di branch. Il passo C1 troverebbe l'environment già esistente. Va aggiunta una nota: dopo C1, verificare che C2 (solo `main`) sia attivo PRIMA di C3 (segreti), e non etichettare PR prima del setup.
- COSMETICA — Conteggi §2 dell'handoff approssimati (+1222 contro +1241 reali), già dichiarati come tali.

NON VERIFICATO
- Esecuzione reale del workflow: `pull_request_target` gira solo dalla definizione su main. Quindi: che l'environment ristretto a main fornisca i segreti a un `pull_request_target`, che `structured_output` si popoli col token OAuth, che la review dell'App conti per "required approvals", i nomi dei modelli `claude-fable-5-1`, `claude-opus-5-5` e `claude-opus-4-8` e il loro accesso con il token dell'abbonamento. La cascata copre i modelli non validi, ma COMMENT e quota sprecata restano.
- Se il motore dei permessi di Claude Code blocchi `--output` o altre scritture via `git` prefissato (V-1 è provato a livello git, non a livello Claude Code). Il comportamento del CLI con `Read(./**)` e delle regole Grep/Glob senza ambito (vedi R-160-1), e la sintassi dei prefissi sui comandi composti.
- `actionlint` e `bun`/`shell-quote` non eseguiti (per il parsing di `claude_args` ho usato `shlex` come proxy). Le 56 mutation complessive non sono state rifatte: solo il campione descritto sopra.
- Il fatto che il bot approvi solo senza finding ALTA/MEDIA vale soltanto per ciò che il modello scrive nel campo `finding`: una prompt injection riuscita nel contenuto della PR è rischio intrinseco (R-158-5 resta decisione umana: il bot non esegue test né mutation).

RACCOMANDAZIONE
1. Il merge di #130 è sicuro oggi (nessun segreto, nessuna approvazione richiesta). Prima di fare il setup dell'operatore (segreti) e prima della fetta B2, chiudere V-1 e V-2 con test che falliscano sul codice attuale: allowlist git senza `--output` (o niente git), `_SEGRETO` su tutti i campi pubblicati.
2. Nella fetta B2 aggiungere V-3 (test sulle permission dell'App e sui `needs`), V-4 (negazioni e gravità minuscole) e valutare V-5 (`MACCHINA_BOT` e doc-only non-md).
3. Aggiornare `reports/setup_verifica_bot.md` per V-6.
4. R-158-5: per le fette nel perimetro di review tenere obbligatoria la verifica locale §4quater accanto al bot (il bot è di sola lettura e non applica "Prova, non leggere").
```

## §9 VERIFICA ESTERNA #130 (seconda, verdetto integrale)

Agente nuovo (`general-purpose`, Sonnet) con il solo prompt `Applica .claude/verifica_esterna.md a: <URL_HANDOFF 8e11aa5> <URL_PR #130>`. Esito riportato così com'è; le correzioni sono nel commit `c215635` (review #162).

```
VERIFICA ESTERNA PR #130 — APPROVATO CON RISERVE
(Il merge di #130 è innocuo adesso: il bot non ha segreti né environment (`environments` = 0), il ruleset non richiede approvazioni e la PR non ha l'etichetta. V-1 va chiuso PRIMA del setup che inserisce i segreti. Al momento della verifica `handoff-check` su 8e11aa5 era ancora queued, e il merge lo aspetta perché è required.)

Metodo: clone usa-e-getta nella scratchpad, checkout di 8e11aa5 (pinnato dall'URL), merge-base con origin/main = f5fb9c1, clone separato alla base per il confronto dei test. Ho letto per intero `scripts/bot_esito.py`, `.github/workflows/verifica-bot.yml`, `reports/setup_verifica_bot.md` e l'handoff. Ho rilanciato `tests/test_unit_verifica_bot.py` e le 5 suite di controllo, sia alla base che al commit. Ho eseguito circa 80 sonde dirette su `decidi`/`componi_corpo` e 33 mutation mie su script e workflow. Ho controllato GitHub con `gh` (PR, run, job, ruleset, environments, permessi Actions, label, SHA delle action). Ho clonato `anthropics/claude-code-action` a cab360f. Ho provato i permessi del CLI headless `claude -p` versione 2.1.289, cioè quella pinnata dall'action (`base-action/action.yml` riga 150), con probe in una cartella della scratchpad (nessun segreto, nessun repo reale). Il repo reale non è stato toccato: `git status` della worktree è vuoto. In `/Users/gas/Gas` restano solo tre untracked preesistenti (`.agents/skills/source-command-fine-task/`, `.codex/`, `AGENTS.md`), che non sono miei.

CLAIM VERIFICATI
- §2 e §3 dell'handoff contro git reale: VERO nella sostanza.
  - Gli 11 file coincidono e `check_handoff.py` locale dà "OK — 11 file dichiarati correttamente".
  - `check_verdetto.py` dà "OK — 42 riferimento/i verificato/i".
  - Il log reale ha 8 commit; l'ottavo è 8e11aa5, assente per costruzione e dichiarato.
  - Le righe inserite sono +1443/-137 contro +1416/-137 dichiarate, e `handoff.md` è 302 righe contro 275. L'handoff dichiara l'approssimazione (COSMETICA).
- §5 Delta test "273 → 437, nuova suite 164": VERO.
  - Alla base (f5fb9c1), hooks+gate+handoff+gasmerge: 273 passed.
  - A 8e11aa5, le stesse suite più verifica_bot: 437 passed in 97s.
  - `tests/test_unit_verifica_bot.py` da sola: 164 passed.
- CI su 8e11aa5 (run 37366037273): `unit-suite` SUCCESS. Gli step includono "Run verifica-bot suite" in success. `handoff-check` era QUEUED, quindi il check required non è ancora verde.
- Run 37364747687 (43f84fb): l'handoff §6 la descrive con unit-suite "in coda". Ora quel job è CANCELLED (handoff-check success). Il commit del codice 43f84fb non ha mai avuto un `unit-suite` completato sul proprio SHA; è coperto dal verde su 8e11aa5, che ha lo stesso albero di codice più i soli report. Run 37352488135 (7d6289c) success e 37352159123 (5010cef) con handoff-check failure: coerenti con §6.
- Ruleset `main-lock` (id 18805824): required `unit-suite` e `handoff-check` (integration_id 15368). `required_approving_review_count` 0, `dismiss_stale_reviews_on_push` false, `require_last_push_approval` false: coerente con "ruleset DEFERITA". `can_approve_pull_request_reviews=false`: VERO. Il repo è PUBBLICO. La PR è del proprietario, non da fork, non draft, senza label, senza review.
- Pin delle action: VERO. `checkout@11d5960…` = v4 / v4.4.0. `create-github-app-token@bcd2ba4…` = v3 / v3.2.0. `claude-code-action@cab360f…`: il tag v1 (annotato) punta ancora a cab360f.
- V-1 #130 (git tolto dagli strumenti): VERO. Il set Bash è esattamente 5 comandi `gh` di sola lettura (test sul set esatto). Mutation: aggiungere `git log`, `curl`, `WebFetch` o `Edit` a STRUMENTI → test rosso.
- Redirezioni di shell sotto `Bash(prefisso:*)`, il punto "non verificato" di #130 e #161: PROVATO, NON è un buco. Con CLI 2.1.289 headless e `--allowedTools Bash(echo:*)` sono DENIED, e non si crea nessun file: `>`, `>>`, `&>`, `>|`, `1>`, `cmd; cmd > f`, `> /dev/stderr`, `$(… > f)` e backtick. Passa solo `2>&1`, che non scrive. Il parser è lo stesso per qualsiasi prefisso, quindi vale per `gh`.
- Symlink dentro `./pr` verso l'esterno: Read e Grep sono bloccati ("symlink resolves outside allowed directories").
- V-2 #130 (credenziali su tutto il verdetto): VERO per le forme letterali `sk-ant-`, `gh[pousr]_X`, `github_pat_`, `-----BEGIN`, in id e descrizione dei finding (sonda: COMMENT). Il limite è in V-1 sotto.
- V-3 #130 (test su permessi dell'App e `needs`): VERO. Mutation `permission-pull-requests: write` → `permission-contents: write` (e l'aggiunta di contents), `needs: [smista, verifica]` → `[smista]` e PR write nel job verifica: uccise, 1 failed ciascuna.
- V-4 #130 (negazioni, gravità a parole): VERO per "NON APPROVATO", "DISAPPROVATO", "V-1 — grave:", "[MEDIA]", "| MEDIA |", "- Alta -" → COMMENT. Residui in V-2 sotto.
- V-5 #130: PARZIALE. `scripts/`, `.claude/hooks/`, perimetro, revisore, fine-task e i 5 test sono davvero in MACCHINA_BOT (mutation: `scripts/`, `hooks/`, perimetro, `CLAUDE.md` per nome → uccise). Il doc-only ora richiede `.md` (mutation uccisa), ma resta aperto il punto di V-6 sotto.
- V-6 #130 (ordine del setup): VERO. `setup_verifica_bot.md` ha la nota con C1–C2 prima dei segreti.
- Mutation mie che il test uccide: head check, BOCCIATO, APPROVATO CON RISERVE senza finding, doc-only, commit_id, `!= "false"` fail-open, file troncati dall'API, no `persist-credentials`, no owner/fork check, ref del checkout da branch, titolo in env, MACCHINA_BOT hard-coded, evento `pull_request_target` → `pull_request`.

FINDING
- V-1 (MEDIA) — R-160-1 non è BASSA: la lettura di file fuori cartella via Grep/Glob è reale e il filtro `_SEGRETO` è aggirabile.
  - Sonda sul CLI 2.1.289 con `--allowedTools "Read(./**),Grep,Glob"` (la configurazione del workflow). Read di `/etc/hosts` è DENIED, ma `Grep pattern=GAS path=/Users/gas/Gas/CLAUDE.md output_mode=content` è PERMESSO e restituisce il contenuto della riga, `Grep` su `/etc/hosts` è PERMESSO e `Glob /etc/host*` e `Glob` su `/Users/gas/Gas` sono PERMESSI.
  - Su un runner Linux lo stesso canale arriva a `/proc/self/environ`, cioè all'ambiente del processo che contiene `CLAUDE_CODE_OAUTH_TOKEN`. Questo NON l'ho provato su Linux. In più `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` (`action.yml` riga 301) è attivo solo con `allowed_non_write_users`, che il workflow non imposta.
  - Il repo è pubblico e la review è pubblica. L'avversario di V-B è chi scrive la PR e quindi il contenuto che il bot legge. Il token dura a lungo e consuma la quota dell'operatore.
  - `_SEGRETO` riconosce solo le forme letterali. Sonde con APPROVE (verdetto APPROVATO CON RISERVE, finding BASSA): `sk‑ant-…` con trattino Unicode U+2011, `s k-ant-`, `AKIA…`, `xoxb-…`, `eyJ….eyJ` (JWT), `sk-proj-…`, `glpat-…`, `Bearer …`. Anche un token in base64 o spezzato passa.
  - Fix già provato localmente: `Grep(./**),Glob(./**)` al posto di `Grep,Glob` nudi. Con quella regola Grep e Glob su `/etc/hosts` e `/etc` sono DENIED mentre `./inside.txt` e le ricerche senza path restano permessi, e i symlink sono bloccati. In aggiunta, `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: '1'` nell'env del job. Poi un test che pretenda `Grep(./**)` e `Glob(./**)` e vieti `Grep` e `Glob` nudi. Il handoff §7 e lo stato lo rimandano a B2 come BASSA: va chiuso prima del setup (prima di mettere il token).
- V-2 (BASSA, dichiarata aperta) — R-161-1 confermata, con forme in più. Con il campo APPROVATO, la riga del verdetto produce APPROVE per "NON-APPROVATO", "NON È APPROVATO", "NON risulta APPROVATO", "NO APPROVATO", "NEGATO / APPROVATO", "non approvo: APPROVATO" e "APPROVATO (ma io lo boccerei)". `FINDING: V-1 (CRITICAL)`, `F-1 HIGH`, `V-1 — blocker` e `V-1 — importante:` passano come APPROVE, perché la gravità non è nelle parole riconosciute. Anche `V-1 (ME​DIA)` con spazio a larghezza zero passa. La decisione regge solo sul campo strutturato; il confronto col testo è una rete debole. Fix: lista di negazioni più ampia, oppure, più robusto, ignorare il testo e decidere solo sul campo `gravita` strutturato, con un controllo semplice di coerenza.
- V-3 (BASSA, buchi di test) — tre mutation sopravvivono con 164/164 verdi. Le prime due decidono se il token dell'App, la chiave e il Claude con i segreti partono su PR che il filtro `smista` ha escluso (fork, autore estraneo, senza etichetta, draft).
  - `esito`: `if: !cancelled() && needs.smista.result == 'success'` → `if: always()`.
  - `verifica`: `if: needs.smista.outputs.solo_reports == 'false'` → `if: always()`.
  - `HEAD_ANALIZZATA: ${{ needs.smista.outputs.head }}` → `${{ github.event.pull_request.head.sha }}`. Resta fail-closed salvo il caso limite A→B→A. Lo SHA verificato non è più quello a cui lega la review.
  Il "mutation 72/73" dichiarato è un campione scelto dall'autore: non copre le condizioni `if`. Fix: test sul testo di `if` di `verifica` e `esito`, e su `HEAD_ANALIZZATA` (sola `needs.smista.outputs.head`).
- V-4 (BASSA) — `componi_corpo` va in `TypeError` quando `finding` è un intero o un booleano. `decidi` risponde bene (COMMENT "verdetto strutturato incompleto"), poi `for f in verdetto.get("finding") or []` solleva eccezione: sonda con `finding: 5` e `finding: True`. Lo step `esito` fallisce e non pubblica nulla. Fail-closed, ma l'operatore non riceve feedback. Lo schema `--json-schema` lo rende improbabile. Fix: `finding if isinstance(finding, list) else []`.
- V-5 (BASSA, operativa) — l'etichetta `verifica` non esiste nel repo (`gh label list`: bug, documentation, duplicate, enhancement, help wanted, good first issue, invalid, question, wontfix) e nessuno la crea né la applica: `setup_verifica_bot.md`, `fine-task.md`, `CLAUDE.md` e gli script `scripts/` non la menzionano come passo. Il workflow dice "l'agente la mette a fine fetta", ma non è cablato. Senza etichetta il bot non parte mai e la convalida di B2 non è raggiungibile. Fix: passo di setup per creare l'etichetta più un'istruzione in fine-task, oppure il bot parte anche su altro trigger.
- V-6 (BASSA, chiusura sovrastimata) — il handoff dà V-5 #130 per "CHIUSA", ma il doc-only senza LLM ora esclude solo i non-`.md`. Ogni `reports/*.md` si approva senza verifica. Sono file che altri letti come istruzioni: `reports/setup_verifica_bot.md` (passi dell'operatore sui segreti e l'environment), `reports/design_cancello.md` (criteri del protocollo), roadmap, stato. Il revisore #158 l'ha registrato come scelta dell'operatore, ma il handoff dovrebbe dire "parziale". Fix proposto: escludere almeno `setup_verifica_bot.md` e `design_*.md`, oppure dichiarare esplicitamente che sono accettati.
- COSMETICA — §2 dell'handoff approssimato (+1416 contro +1443 reali, `handoff.md` 275 contro 302, dichiarato). §6 descrive come "ancora in coda" una run che ora risulta cancellata. Il messaggio di pubblicazione del bot include `@menzioni` non filtrate (menzione libera nel `modello`).

NON VERIFICATO
- Esecuzione reale del workflow. `pull_request_target` gira solo dalla definizione su main, quindi la prima prova arriva dopo il merge e il setup: segreti dell'environment ristretto a main concessi a `pull_request_target`, `structured_output` col token OAuth, `checkHumanActor` sull'attore dell'etichetta, review dell'App valida come approvazione per il ruleset.
- Comportamento reale su runner Linux di Grep su `/proc/self/environ` e se l'ambiente è davvero leggibile (V-1 è provato per percorsi fuori cartella su macOS, non per quel file).
- I nomi dei modelli `claude-fable-5-1`, `claude-opus-5-5`, `claude-opus-4-8` e il loro accesso con il token dell'abbonamento. La cascata copre i modelli non validi, ma COMMENT e quota sprecata restano.
- `actionlint` non eseguito. Le 73 mutation dichiarate dall'autore non rifatte per intero: ne ho fatte 33 mie (V-3 sopra ne è l'esito). La semantica di `concurrency` con job saltati e `!cancelled()` non riproducibile in locale.
- Se `--setting-sources user` e il parsing di `claude_args` con le virgole + spazio di `STRUMENTI` (YAML `>-`) si comportano alla lettera sul runner: ho letto il sorgente dell'action, non eseguito l'action.

RACCOMANDAZIONE
1. Il merge di #130 è sicuro oggi: nessun segreto, nessuna approvazione richiesta, nessun environment. Aspetta che `handoff-check` diventi verde.
2. Prima di fare il setup (cioè prima di inserire `CLAUDE_CODE_OAUTH_TOKEN`) chiudi V-1: `Grep(./**),Glob(./**)` più `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: '1'` e un test che li pretenda. È una modifica di due righe, già provata sul CLI 2.1.289.
3. Nella fetta B2 aggiungi: V-2 (negazioni, gravità in lingua diversa o vocabolario ampliato; meglio decidere sul campo strutturato), V-3 (test sulle condizioni `if` e su `HEAD_ANALIZZATA`), V-4, V-5 (creare l'etichetta e cablarla in fine-task) e decidere su V-6.
4. Tieni la verifica locale §4quater accanto al bot per le fette del perimetro (R-158-5): il bot non esegue nulla e questa verifica lo conferma, perché V-1 e V-3 si trovano solo eseguendo.
```
