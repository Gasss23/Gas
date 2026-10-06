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

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .claude/perimetro_review.txt       |   1 +
 CLAUDE.md                          |   1 +
 reports/diff_sessione.md           |  15 +++++++++++----
 reports/handoff.md                 | 142 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------
 reports/setup_agente_non_admin.md  |  58 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  17 ++++++++++-------
 scripts/avviso_token_admin.sh      |  33 +++++++++++++++++++++++++++++++++
 scripts/fine_task_finale.sh        |   7 +++++++
 scripts/gasmerge.sh                |   5 +++++
 tests/test_unit_gasmerge.py        |  73 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  22 ++++++++++++++++++++++
 13 files changed, 325 insertions(+), 54 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo, con `GAS_TEST_LOCALE_UTF8_ATTESO=1`:

```
LC_ALL=C:       pytest gasmerge+hooks+gate+handoff_check+verifica_bot+voice_server → 608 passed
LC_ALL=C.UTF-8: pytest gasmerge+hooks+gate+handoff_check+verifica_bot+voice_server → 608 passed
```

(+11 test G-3: 10 in TestAvvisoTokenAdmin, 1 in hooks.)

## §6 STATO CI

`gh` non autenticato (CI NON VERIFICATA con la CLI). Mappatura commit → run:
- `73d93d8`, `e6784e6`, `9540340`: pushati insieme, run CI sul push di `9540340` — esito non letto alla scrittura dell'handoff (atteso handoff-check rosso, prima del fine-task).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-186-3** (BASSA, dichiarata): si prova solo Administration; Workflows/Environments li controlla l'operatore alla creazione del token.
- **R-186-4** (BASSA, dichiarata): nessun timeout proprio su `gh api`.
- **R-187-1** (cosmetica): senza `realpath` e lancio da fuori del repo con path relativo → avviso "assente", non crash.
- Prova reale con GitHub non fatta (passo B3).
