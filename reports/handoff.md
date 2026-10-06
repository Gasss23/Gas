# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — G-3: agente non admin, fase "solo avviso" (sessione cloud)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #138 (https://github.com/Gasss23/Gas/pull/138). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4761143817","url":"https://github.com/Gasss23/Gas/pull/138"}`): `gh` non è autenticato in questo container. Merge manuale (tocca `scripts/`).
2. Creare e provare il token dell'agente (`reports/setup_agente_non_admin.md` A–B).
3. Decidere se l'avviso diventa blocco per `gasmerge --auto` (fase 2).

---

## §1 SCOPE & ESITO FETTE

- **G-3 fase 1 (solo avviso)**: `FATTA`.
- **R-186-1 / R-186-2**: `FATTA`; R-186-3, R-186-4 dichiarate.
- **Prova con GitHub reale (token senza Administration → 403/404)**: `SALTATA — gh non autenticato nel container; passo B3 dell'operatore`.
- **G-3 fase 2 (blocco)**: `DEFERITA — decisione dell'operatore`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Verifica esterna §4quater #138**: `FATTA` — APPROVATO CON RISERVE (§8). **V-1 (MEDIA, falso OK su repo non visibile/sbagliato)**: `FATTA` (review #188/#189). V-2 (è solo un avviso) = fase 1 voluta. V-3 cosmetica (stat).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 .claude/perimetro_review.txt       |   1 +
 CLAUDE.md                          |   1 +
 reports/diff_sessione.md           |  15 +++++++++++----
 reports/handoff.md                 | 262 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------
 reports/setup_agente_non_admin.md  |  60 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  17 ++++++++++-------
 scripts/avviso_token_admin.sh      |  42 ++++++++++++++++++++++++++++++++++++++++++
 scripts/fine_task_finale.sh        |   7 +++++++
 scripts/gasmerge.sh                |   5 +++++
 tests/test_unit_gasmerge.py        |  91 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  22 ++++++++++++++++++++++
 13 files changed, 479 insertions(+), 52 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
c70f5e9 fix(g3): niente falso OK su repo non visibile o non dell'operatore — review #188/#189
56a179a chore(revisore): memoria review #189 — APPROVATO CON RISERVE
2b92542 chore(revisore): memoria review #188 — APPROVATO CON RISERVE
3b35720 docs(g3): fine-task — report, handoff con verdetti #186/#187, diff sessione
9540340 feat(g3): agente non admin, fase solo avviso — scripts/avviso_token_admin.sh in gasmerge e fine-task — review #186/#187
e6784e6 chore(revisore): memoria review #187 — APPROVATO CON RISERVE
73d93d8 chore(revisore): memoria review #186 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-g3/`) resi relativi alla radice del repo, perché il gate B li risolva.

### Review #186 — diff staged iniziale (BOCCIATO)

## VERDETTO: BOCCIATO

**Motivo bloccante (R-186-1).** Il percorso reale di gasmerge non esegue mai il controllo. L'ho riprodotto.

**Elementi del diff esaminati**

- `scripts/gasmerge.sh:38` — `G3="$(dirname "${BASH_SOURCE[0]}")/avviso_token_admin.sh"`
  - Rischio esaminato: risoluzione del path quando gasmerge viene lanciato tramite il symlink `~/bin/gasmerge`. Secondo la regola R10 di stato_progetto.md (riga 381) quel symlink è obbligatorio.
  - Esito: **blocco**. Bash non risolve il symlink, quindi `BASH_SOURCE[0]` vale `~/bin/gasmerge` e lo script viene cercato in `~/bin/avviso_token_admin.sh`. Prova fatta: symlink in scratchpad + `GAS_REPO_DIR=/home/user/wt-g3`. Risultato: `AVVISO G-3: …/bin/avviso_token_admin.sh assente — controllo saltato`.
  - Con `bash scripts/gasmerge.sh` invocato per path assoluto l'avviso invece compare. Con un path relativo funziona solo per caso, perché il `cd` della riga 30 avviene prima del `dirname`.
  - Non c'è crash e l'avviso è visibile, quindi è fail-safe. Però la fetta, nel punto che conta (il merge), non fa nulla.
  - `test_gasmerge_chiama_l_avviso_senza_bloccare` lancia gasmerge per path assoluto e quindi non vede il problema.
  - Fix: `G3="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/avviso_token_admin.sh"`, come già fa `fine_task_finale.sh:19`, oppure `scripts/avviso_token_admin.sh` relativo al repo dopo il `cd`. In più serve un test che invochi gasmerge tramite symlink e ne esiga l'avviso.
- `scripts/gasmerge.sh:39` — `bash "$G3" || true` sotto `set -euo pipefail`.
  - Rischio esaminato: che l'avviso possa interrompere gasmerge.
  - Esito: **ok**. `|| true` neutralizza qualsiasi exit code, il ramo "assente" fa solo un `echo`, e il gh figlio non legge lo stdin che serve al `read -r ANS` della conferma.
- `scripts/avviso_token_admin.sh:17-18` — `ERR=$(gh api … --silent 2>&1 >/dev/null); RC=$?`
  - Rischio esaminato: che venga catturato l'exit code sbagliato o che il corpo della risposta (le deploy key) finisca a terminale.
  - Esito: **ok**. Con il solo `set -u`, `$?` è l'exit code di gh dentro l'assegnazione, e lo stdout va in `/dev/null`.
- `scripts/avviso_token_admin.sh:24` — `grep -qE 'HTTP (403|404)'`
  - Rischio esaminato: classificazione errata di un 403 che non riguarda i permessi.
  - Esito: **riserva R-186-2 (BASSA)**. Un 403 da rate limit secondario (`API rate limit exceeded … (HTTP 403)`) con un token admin stampa "OK", cioè dà via libera quando non dovrebbe. Stessa cosa per un 404 da repo sbagliato (`GH_REPO` o remote di un fork). Oggi conta poco perché è solo un avviso, ma va chiuso prima di trasformarlo in blocco: per esempio distinguendo "Resource not accessible" o controllando il messaggio.
- Scelta dell'endpoint (`repos/{owner}/{repo}/keys`): **ok**. Per i token fine-grained "List deploy keys" richiede Administration in lettura, e un PAT classic del proprietario con scope `repo` risponde 200, quindi giustamente avvisa. Il ragionamento su `permissions.admin` (che dà il ruolo dell'utente, non la capacità del token) è corretto.
  - Falso positivo nella direzione sicura: un token con Administration **Read-only** avvisa anche se non può cambiare il ruleset.
  - **R-186-3 (BASSA)**: la sonda verifica solo Administration. Le voci Workflows ed Environments su "No access", richieste da `reports/setup_agente_non_admin.md` §A.4, non vengono verificate, quindi il messaggio "non amministra il repo — OK" non le copre. Va dichiarato nel setup.
- `scripts/fine_task_finale.sh:132-136` — chiamata dopo il gate IP e prima di `=== Push ===`, con `set -e` riattivato.
  - Esito: **ok**. `SCRIPT_DIR` è risolto con `realpath "$0"`, quindi funziona anche via symlink, e `|| true` copre il `set -e`. Test `test_finale_g3_avviso_token_admin_non_blocca` eseguito: passa.
- **R-186-4 (BASSA, dichiarata)**: `gh api` non ha un timeout proprio. In caso di rete bloccata, gasmerge e fine-task restano fermi sul controllo. È lo stesso rischio che hanno già `gh pr view` e `git push` subito dopo, quindi non aggiunge un modo di fallire nuovo.
- Coerenza con CLAUDE.md: la regola "token senza Administration, nessun merge salvo `gasmerge --auto` col sì del bot o richiesta esplicita" va nella direzione di V-B e G-3. Lo script è stato aggiunto correttamente a `.claude/perimetro_review.txt`: il gate protegge anche se stesso.

**Test eseguiti:** `TestAvvisoTokenAdmin` 8 passed, `-k g3` di hooks 1 passed. La suite completa da 606 l'ho presa per buona e non l'ho rieseguita.

**Rischi esclusi:** non ho verificato che GitHub risponda davvero 403/404 a un token fine-grained senza Administration e 200 a uno admin, perché qui gh non è autenticato col token dell'operatore. Va provato al passo B3 del setup. Non ho nemmeno verificato `realpath` su macOS anteriori al 13, che servirebbe per il fix proposto: `fine_task_finale.sh` però lo usa già.

**Per sbloccare:** correggere `gasmerge.sh:38` e aggiungere un test con gasmerge invocato tramite symlink, poi rifare la review (#187). R-186-2, R-186-3 e R-186-4 vanno tracciate in stato_progetto.md e non bloccano.

Memoria aggiornata con la riga #186 e una lezione sugli script chiamati via symlink. L'ho committata da sola con lo script atomico (`73d93d8`), e il diff staged è rimasto intatto (9 file): `.claude/agents/memoria_revisore.md`.

### Review #187 — ri-review dopo R-186-1/2

## VERDETTO: APPROVATO CON RISERVE

Ri-review #187. Il motivo per cui avevo bocciato la #186 (R-186-1: il controllo non partiva mai quando gasmerge viene lanciato dal symlink `~/bin/gasmerge`) è risolto. Ho riprodotto il caso reale e ho controllato che il test nuovo fallisca col vecchio codice.

**Punti del diff esaminati**

- **`scripts/gasmerge.sh:15`**, il calcolo di `G3` all'inizio di `main()`, prima del `cd`, che segue i symlink con `realpath` (e ripiega sul path grezzo se `realpath` manca).
  - Rischio esaminato: path sbagliato via symlink, e un crash per `set -euo pipefail` se `realpath` non c'è.
  - Dentro una funzione, `BASH_SOURCE[0]` resta il file dello script, e il `|| printf` evita che uno stato diverso da zero faccia terminare la sostituzione.
  - Riprova reale col symlink in scratchpad, `GAS_REPO_DIR=/home/user/wt-g3` e un gh finto che risponde 0: stampa «AVVISO G-3: il token gh in uso AMMINISTRA il repo…». Prima stampava «assente — controllo saltato».
  - Esito: **ok**.
- **`tests/test_unit_gasmerge.py`, `test_gasmerge_via_symlink_trova_l_avviso`**.
  - Rischio esaminato: un test che passa comunque, come quello della #186 che lanciava gasmerge per path assoluto.
  - Ho rimesso via `sed` la vecchia riga `G3="$(dirname "${BASH_SOURCE[0]}")/…"`: il test **FALLISCE**. Poi ho ripristinato lo script: il file su disco è di nuovo identico allo staged (`git diff` vuoto).
  - Esito: **ok**.
- **`scripts/gasmerge.sh:41`**, `if [ -r "$G3" ]; then bash "$G3" || true; else …`.
  - Rischio esaminato: un'interruzione di gasmerge sotto `set -e`.
  - Esito: **ok**. `|| true` copre qualsiasi codice d'uscita, e il ramo "assente" fa solo un `echo`.
- **`scripts/avviso_token_admin.sh:25`**, il ramo `rate limit` messo prima del ramo `HTTP (403|404)`.
  - Rischio esaminato: un 403 da rate limit letto come "OK" (R-186-2).
  - L'ordine è corretto e il caso `API rate limit exceeded … (HTTP 403)` è nel test parametrizzato.
  - Esito: **ok**. R-186-2 è chiusa.
- **`scripts/avviso_token_admin.sh:11-12`** e il setup (§«Cosa NON copre il controllo»).
  - Rischio esaminato: le dichiarazioni di R-186-3 (si prova solo Administration) e R-186-4 (nessun timeout su `gh api`).
  - Esito: **riserva dichiarata**, coerente nello script, nel setup e in stato_progetto.md.

`TestAvvisoTokenAdmin`: 10 passed.

**Riserve (non bloccanti, già tracciate)**

- **R-186-3** (bassa): la sonda verifica solo Administration. Workflows ed Environments li controlla l'operatore quando crea il token.
- **R-186-4** (bassa): `gh api` non ha un timeout proprio.
- **R-187-1** (cosmetica): il ripiego quando manca `realpath` resta relativo se lo script è lanciato con un path relativo, e viene letto dopo il `cd`. Nel caso limite (niente `realpath` e lancio da fuori dal repo) compare un avviso «assente», non un crash. Accettabile.

**Non verificato**

- Che GitHub risponda davvero 403/404 a un token fine-grained senza Administration, e 200 a uno admin: qui gh non è autenticato col token dell'operatore. Va provato al passo B3 del setup.
- La suite completa da 608 test in C e C.UTF-8 non l'ho rieseguita, l'ho presa per buona. Ho eseguito solo la classe G-3 e la mutation.

Ho aggiunto la riga #187 alla memoria e l'ho committata col solo script atomico (commit `e6784e6`). Il diff staged è intatto (9 file, nessun commit da parte mia). File: `.claude/agents/memoria_revisore.md`.

### Review #188 — fix V-1 della verifica esterna #138

## VERDETTO: APPROVATO CON RISERVE

Review #188: il fix chiude il caso "token che non vede il repo" (SSO, repo privato o inesistente). Resta scoperto un caso più stretto: un repo sbagliato ma visibile dà ancora "OK" (R-188-1). V-1 va quindi scritta come MITIGATA, non CHIUSA (R-188-2). Nessuna delle due blocca, perché in fase 1 lo script è solo un avviso.

**Elementi del diff esaminati**

- **`scripts/avviso_token_admin.sh:31`**, il secondo controllo `gh api "repos/{owner}/{repo}"` dentro il ramo 403/404 di `/keys`.
  - Rischio esaminato: falso OK su 404/403 non legati ai permessi.
  - Ho sostituito la condizione con `if true`: falliscono 2 test (riprodotto). Ho poi ripristinato il file, che è di nuovo identico allo staged.
  - Il secondo `gh` gira sotto il solo `set -u`, con stdout e stderr scartati e dentro un `if`, quindi non può interrompere lo script. Resta `exit 0` in ogni ramo, e gasmerge/fine-task restano protetti dal `|| true` già visto nella #187.
  - Esito: **riserva R-188-1 (MEDIA-BASSA)**. Il 200 prova solo che il repo è *visibile*, non che sia *il repo giusto*. Se `GH_REPO` o il remote puntano a un repo altrui ma pubblico, `/keys` risponde 404 e `repos/{o}/{r}` risponde 200, quindi esce "OK".
  - L'ho riprodotto con un gh finto che nega solo `/keys`: stampa «G-3: il token gh in uso non amministra il repo — OK». Il caso SSO è chiuso, perché l'SSO nega anche l'endpoint del repo. Il caso "fork o repo sbagliato" citato nel commento invece no, se quel repo è pubblico.
  - Fix proposto: esigere anche `.permissions.admin == true` sul repo, per esempio `gh api repos/{owner}/{repo} --jq .permissions.admin` uguale a `true`. Quel campo rispecchia il RUOLO dell'utente: inutile per misurare il token, ma serve proprio a dire "è il repo dell'operatore". Più un test con repo visibile e `admin:false` che non deve dare OK.
- **`tests/test_unit_gasmerge.py`, `test_repo_non_visibile_non_e_ok` e il nuovo stub di `test_token_senza_administration_ok`** (negato solo `/keys`).
  - Rischio esaminato: test che passano comunque, e il vecchio test "OK" diventato falso dopo il fix.
  - Lo stub con `case "$*" in *"/keys"*` separa davvero le due chiamate, e la mutation qui sopra viene uccisa.
  - `TestAvvisoTokenAdmin`: 12 passed.
  - Esito: **ok**.
- **`reports/stato_progetto.md:114`**, che scrive V-1 come «CHIUSA».
  - Esito: **riserva R-188-2 (bassa)**. Per R-188-1 la parola giusta è «MITIGATA (resta il repo sbagliato ma visibile)», oppure CHIUSA solo dopo il fix con `permissions.admin`.

**Cosa non ho verificato**

- Le risposte reali di GitHub, cioè 404 contro 403 su `/keys` e 200 sul repo per un token fine-grained con Contents in lettura/scrittura: gh qui non è autenticato col token dell'operatore. Resta da fare al passo B3 del setup.
- La suite da 610 test in C e C.UTF-8 non l'ho rieseguita: ho girato solo la classe G-3 e la mutation.
- Non ho accertato se Gasss23/Gas sia pubblico: la mia `curl` passa dal proxy, che potrebbe aggiungere le credenziali.

Ho aggiunto alla memoria la riga #188 e la lezione «una sonda di visibilità non prova l'identità della risorsa». L'ho committata solo con lo script atomico (`2b92542`); il diff staged è intatto (3 file) e non l'ho committato. File: `.claude/agents/memoria_revisore.md`.

### Review #189 — ri-review R-188-1/2

## VERDETTO: APPROVATO CON RISERVE

Ri-review #189: R-188-1 e R-188-2 sono chiuse e la mutation che ho rilanciato viene uccisa. Resta una riserva senza blocco: non è provato che `permissions.admin` misuri il ruolo dell'utente anche con un token fine-grained (R-189-1).

**Punti del diff esaminati**

- **`scripts/avviso_token_admin.sh:33-34`**: dopo il 403/404 su `/keys`, l'"OK" esce solo se `gh api repos/{owner}/{repo} --jq '.permissions.admin'` stampa esattamente `true`.
  - Rischio esaminato: falso OK su un repo sbagliato ma visibile, e un crash se il secondo `gh` fallisce.
  - `|| RUOLO=""` gira sotto il solo `set -u`, quindi un fallimento non interrompe lo script; il confronto è stretto.
  - Riprove:
    - Mutation `[ -n "$RUOLO" ]`: **1 failed**. Poi ho ripristinato il file, che coincide con lo staged.
    - Gh finto che restituisce `null` (campo assente): «non verificabili», nessun OK.
  - Esito: **ok**. R-188-1 è chiusa.
- **`tests/test_unit_gasmerge.py`, `test_repo_visibile_ma_non_dell_operatore_non_e_ok`**, più lo stub dell'OK che ora risponde `true`.
  - Rischio esaminato: un test che non distingue i casi.
  - È proprio lo scenario che avevo riprodotto nella #188: `/keys` 404 e repo 200 con `false`. `TestAvvisoTokenAdmin`: 13 passed.
  - Esito: **ok**.
- **`reports/setup_agente_non_admin.md`** e **`reports/stato_progetto.md`**: la nota "l'OK vale solo per il TUO repo" e V-1 dichiarata CHIUSA con la condizione completa.
  - Esito: **ok**. R-188-2 è chiusa.

**Riserve**

- **R-189-1 (bassa, non verificata):** tutto poggia sul presupposto che con un token fine-grained `permissions.admin` misuri il ruolo dell'utente e non i permessi del token.
  - Se invece misurasse il token, il token ristretto avrebbe `admin:false`. L'avviso darebbe allora sempre «non verificabile» e mai OK: un errore dal lato prudente, ma l'avviso diventerebbe inutile.
  - Va provato al passo B3 del setup, che deve mostrare l'"OK" con il token `gas-agente`.
- **R-189-2 (cosmetica):** il commento di testata (`scripts/avviso_token_admin.sh:9`) dice ancora "solo se il token VEDE il repo" e non nomina il ruolo admin.

**Cosa non ho verificato:**
- Le risposte reali di GitHub: gh qui non è autenticato col token dell'operatore.
- La suite da 611 test in C e C.UTF-8: non l'ho rieseguita, ho girato solo la classe G-3 e la mutation.

Ho aggiunto alla memoria la riga #189 e l'ho committata con lo script atomico (`56a179a`). Il diff staged (4 file) è intatto e non l'ho committato. File: `.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo, con `GAS_TEST_LOCALE_UTF8_ATTESO=1`:

```
LC_ALL=C:       pytest gasmerge+hooks+gate+handoff_check+verifica_bot+voice_server → 611 passed
LC_ALL=C.UTF-8: pytest gasmerge+hooks+gate+handoff_check+verifica_bot+voice_server → 611 passed
```

(+14 test G-3: 13 in TestAvvisoTokenAdmin, 1 in hooks.)

## §6 STATO CI

Stato dal connettore GitHub e dalla verifica esterna #138 (`gh` non autenticato qui). Mappatura commit → run:
- `73d93d8`, `e6784e6`, `9540340`: pushati insieme → run sul push di `9540340` (atteso handoff-check rosso, prima del fine-task).
- `3b35720` (primo fine-task): run 37489696539: unit-suite success, handoff-check success.
- `2b92542`, `56a179a`, commit del fix V-1 e di questo fine-task: pushati insieme, run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-189-1** (BASSA, non verificata): si presume che con un token fine-grained `permissions.admin` misuri il ruolo dell'utente; se misurasse il token, l'avviso direbbe sempre "non verificabile" (lato prudente). Da provare al passo B3.
- **R-189-2** (cosmetica): il commento di testata dello script non nomina il controllo del ruolo.
- **R-186-3**, **R-186-4** (BASSE, dichiarate). **R-187-1** (cosmetica).
- V-2 #138: è solo un avviso finché l'operatore non decide la fase 2.

## §8 VERIFICA ESTERNA #138 (verdetto integrale)

Lanciata con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 3b35720> <URL_PR>` (agente nuovo, Sonnet). V-1 MEDIA chiusa (review #188/#189); V-2 = fase 1 voluta; V-3 (stat fotografato prima dell'ultimo commit) strutturale; V-4 dichiarate.

VERIFICA ESTERNA PR #138 — APPROVATO CON RISERVE

**Metodo:**
- Clone usa-e-getta nella scratchpad, checkout di 3b35720 (head della PR; coincide con lo SHA dell'URL).
- Ho letto diff e script, e rieseguito le suite alla base 0e7dc4e e al commit.
- Ho provato `avviso_token_admin.sh` con un `gh` finto su 8 esiti.
- Ho letto check-run della PR e ruleset con `gh` e connettore GitHub.
- Il repo reale `/home/user/Gas` ha `git status` vuoto.

**CLAIM VERIFICATI:**
- **VERO** — Il diff reale dal merge-base (0e7dc4e) è 13 file, 4 commit (73d93d8, e6784e6, 9540340, 3b35720). I file coincidono con il §2 dell'handoff. Il commit di fine-task è escluso dal log del §3, come l'handoff dichiara.
- **COSMETICO (V-3)** — Le cifre del §2 sono 325+/54- e `handoff.md` 142 righe. Lo stat reale con il commit pinnato è 340+/54- e 157 righe, perché l'handoff si riscrive nel commit di fine-task. Non c'è nessuna riga di nota che lo dica.
- **VERO** — Test: 608 passed in `LC_ALL=C` e 608 passed in `LC_ALL=C.UTF-8`, con `GAS_TEST_LOCALE_UTF8_ATTESO=1`. Alla base sono 597 passed. Il delta è +11, come dichiarato. Ho usato le sei suite elencate nell'handoff.
- **VERO** — CI sullo SHA pinnato: `unit-suite` success e `handoff-check` success (run 37489696539). Gli altri tre job (`smista`, `verifica`, `esito`) risultano skipped. Il ruleset `main-lock` è attivo e richiede `unit-suite` e `handoff-check`.
- **VERO** — Il §6 dell'handoff dice "CI non verificata", ma la CI reale è verde sullo SHA. L'handoff sottostima, non sovrastima.
- **VERO** — I rami dello script d'avviso si comportano come dichiarato. Con il gh finto:
  - 0 → AVVISO "AMMINISTRA";
  - 403 "Resource not accessible" → OK;
  - 404 → OK;
  - rate limit → "non verificabile";
  - rc=4 (non autenticato) e 401 → "non verificabile";
  - errore di rete → "non verificabile".
  - Lo script esce sempre con 0.
- **VERO** — Il diff di `gasmerge.sh` calcola `G3` con `realpath` prima del `cd`, quindi il symlink `~/bin/gasmerge` è coperto. La mutation che rimette il vecchio codice è riportata come uccisa dal test. Questo punto non l'ho rieseguito: è nel verdetto #187, ma le suite complete passano.
- **VERO** — R-186-1 (symlink) e R-186-2 (rate limit) sono chiuse.
  - R-186-2: il ramo `rate limit` precede `HTTP (403|404)`. Il caso "secondary rate limit" stampa "non verificabile".
  - R-186-1: il symlink è coperto dal test `test_gasmerge_via_symlink_trova_l_avviso`, eseguito nella suite da 608.
- **VERO** — `scripts/avviso_token_admin.sh` è aggiunto a `.claude/perimetro_review.txt`, quindi il gate copre anche il nuovo controllo.

**FINDING:**
- **V-1 (MEDIA) — Falso "OK" sul 404.** Ho riprodotto che un 404 con un token che non vede il repo stampa «non amministra il repo — OK».
  - Il 404 vale sia per "token senza Administration" sia per "repo sbagliato" (remote di un fork o `GH_REPO` sbagliato).
  - Altri 403 non legati ai permessi, per esempio il blocco SAML/SSO dell'organizzazione, ricadono nello stesso "OK".
  - Il revisore #186 l'aveva notato (R-186-2 copriva anche il 404), ma la riserva è stata chiusa trattando solo il rate limit. Il 404 da repo sbagliato non è tracciato in nessuna riserva aperta del §7.
  - Oggi è solo un avviso, quindi l'effetto è basso. Diventa una vera falla quando l'avviso si trasforma in blocco (fase 2). Il cambio di fase non deve avvenire senza prima chiudere questo punto.
  - Fix proposto: accettare "OK" solo per il messaggio esatto dei permessi ("Resource not accessible by personal access token" / "Must have admin rights"). Per il 404, verificare prima che `gh api repos/{owner}/{repo}` risponda 200. Altrimenti stampare "non verificabile".
- **V-2 (MEDIA, di progetto) — Il controllo è solo un avviso e non impedisce nulla.** Un token admin resta usabile dall'agente nello stesso container. L'intero G-3 si regge sull'operatore che crea e usa davvero il token senza Administration. Il fatto che l'handoff stesso lo dichiari "fase 1" mitiga. In questa sessione `gh` era autenticato e ha letto i ruleset del repo. Questo, da solo, non dimostra che sia un token admin né quale sia. Va comunque notato per il passo B3.
- **V-3 (COSMETICA)** — Vedi sopra: lo stat del §2 non combacia con quello reale e manca la nota che lo spiega.
- **V-4 (BASSA)** — Il ramo di ripiego senza `realpath` (R-187-1) e la mancanza di timeout su `gh api` (R-186-4) sono dichiarati e rimangono bassi. Non li ho riprodotti.

**NON VERIFICATO:**
- La risposta reale di GitHub a un token fine-grained senza Administration (passo B3). Non avevo un token di quel tipo. Le risposte 403/404 le ho solo simulate con un gh finto.
- Che l'endpoint `keys` richieda davvero Administration in lettura per tutti i tipi di token. Lo prendo dal ragionamento del revisore.
- Il test via symlink e la mutation, che non ho rieseguito singolarmente. Li ho considerati coperti dalla suite verde.
- `fine_task_finale.sh` end-to-end: ho visto solo il diff (chiamata prima di `=== Push ===`, con `|| true`) e i test passati.
- Il contenuto di `reports/setup_agente_non_admin.md`: non l'ho letto riga per riga.

**RACCOMANDAZIONE:**
- La PR è mergeabile per una fase "solo avviso": CI verde, test coerenti con quanto dichiarato, nessun gate indebolito.
- Prima della fase 2 (blocco per `gasmerge --auto`) chiudere V-1 e tracciarlo come riserva aperta nello stato del progetto.
- Eseguire la prova B3 con un token reale senza Administration, e aggiungere il caso 404 da repo sbagliato ai test.
