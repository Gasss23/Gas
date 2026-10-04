# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Rename nel §2, perimetro più largo, check CI presi da main, branch `fix/gate-rename-perimetro-ci`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #121 (https://github.com/Gasss23/Gas/pull/121), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 121`, l'operatore conferma digitando `121`.
2. Prossima fetta PRIORITARIA, già decisa: V-B "vera", cioè revisione con identità separata su GitHub (bot + segreti). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **V-3 — rename e §2 (verifica esterna PR #120)**: `FATTA`.
- **V-2 — perimetro più largo (autorizzato dall'operatore)**: `FATTA`.
- **R-141-2 — la CI eseguiva i check della PR**: `FATTA` come mitigazione (check presi da main; resta R-143-2).
- **R-143-1 — tag "origin/main" che dirotta base e check**: `FATTA`.
- **R-143-4 — .DS_Store**: `FATTA`.
- **Nota b — stat troncato o quotato nel fine-task**: `FATTA`.
- **V-1 della verifica #120 — formulazione di V-A**: `FATTA` (stato_progetto corretto).
- **R-143-2 / R-143-3**: `DEFERITA — R-143-2 alla V-B vera; R-143-3 procedura da decidere`.
- **R-144-1 — ref abbreviato in gasmerge.sh / promemoria_end.sh**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .claude/commands/fine-task.md      |   4 ++--
 .claude/perimetro_review.txt       |   8 ++++++++
 .github/workflows/ci.yml           |  23 +++++++++++++++++++----
 .gitignore                         |   2 ++
 reports/diff_sessione.md           |  18 +++++++++++-------
 reports/handoff.md                 | 326 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   8 ++++++--
 reports/ultimo_report.md           |  30 ++++++++++++++++++------------
 scripts/check_handoff.py           |  23 +++++++++++++++++++----
 scripts/check_verdetto.py          |   2 +-
 scripts/fine_task_finale.sh        |   2 +-
 tests/test_unit_handoff_check.py   |  58 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 13 files changed, 323 insertions(+), 184 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
1357b68 docs(gate-rename): fine-task — rename nel §2, perimetro piu' largo, check CI da main, handoff (review #143/#144)
c287d5f chore(revisore): memoria review #144 — APPROVATO CON RISERVE
13b7933 fix(gate): rename nel §2, perimetro piu' largo, check CI presi da main — review #143/#144 APPROVATO CON RISERVE
067c83d chore(revisore): memoria review #144 — APPROVATO CON RISERVE
f63bf47 chore(revisore): memoria review #143 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. `1357b68` è il primo commit di fine-task, superato da questa correzione del §6.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `13b7933`: la #143 sul diff e la #144 sul delta che chiude R-143-1 e R-143-4. Entrambe sono incollate per intero.

### Review 143

## VERDETTO: APPROVATO CON RISERVE

Review #143. Branch fix/gate-rename-perimetro-ci, diff staged di 4 file, base main 1db7d81. Prima della review ho letto CLAUDE.md, stato_progetto.md (sezione motore) e la memoria del revisore. Non ho trovato blocchi. C'è però un by-pass concreto del nuovo passo CI (R-143-1), che ho riprodotto e che si chiude con una riga: conviene correggerlo in questa stessa PR.

**Elementi del diff esaminati**

- `scripts/check_handoff.py:60` — `_diff_names` ora usa `--no-renames -z`, come `_session_files`.
  - Rischio esaminato: incoerenza tra l'insieme reale e l'insieme di sessione; nomi non ASCII; regressione di R-141-1 (git fallito trattato come diff vuoto).
  - Il ramo `returncode != 0 → None` è intatto.
  - Mutation "solo `_diff_names` senza `--no-renames`": la uccide `test_v3_rename_stat_pasted_honestly_passes`.
  - Esito: **ok**.
- `scripts/check_handoff.py:66-76` e `:104` — `_espandi_rename`, applicata a ogni riga di §2.
  - Rischio esaminato: forme reali di `--stat` e possibile by-pass. Ho fatto una sonda su un repo usa-e-getta con l'output vero di git:
    - `m.py => m2.py` con rename e modifica: ok;
    - `y.py => new/y.py`: ok;
    - `old/x.py => x.py`: ok;
    - `.../ccc/{a => b}` troncato: mismatch;
    - file chiamato `sp => ace.py` senza rename: diviso in `sp` e `ace.py`, mismatch;
    - `"t\303\251.py" => …` quotato: mismatch.
  - I tre mismatch sono falsi blocchi fail-closed, mai by-pass: il check resta un'uguaglianza esatta di insiemi, quindi un'espansione permissiva cambia solo il modo di scrivere l'insieme, non permette di omettere file.
  - Il troncamento `...` e il quoting non ASCII esistevano già per qualsiasi path lungo o accentato: le espansioni nuove non li peggiorano.
  - Mutation "solo `_espandi_rename → [path]`": uccisa.
  - Esito: **ok**, con nota (b) sotto.
- `.github/workflows/ci.yml:228-245` — i check vengono copiati da `origin/main` in `$RUNNER_TEMP/gate_main` ed eseguiti da lì.
  - Ho verificato:
    - `sys.path[0]` è la cartella dello script, quindi `from check_verdetto import` risolve sulla copia di main;
    - `PERIMETRO_FILE` è la copia di main, in unione con la versione alla base, che è sempre main;
    - `_get_repo` resta il checkout della PR, perché dipende dalla cwd;
    - lo shell di default `bash -e` fa fallire il passo se `git show` fallisce.
  - Rischio esaminato: risoluzione ambigua del ref.
  - Esito: **riserva** R-143-1.
- `.claude/perimetro_review.txt:30-34` — aggiunti `gas_identity.md`, `requirements*.txt`, `tools/`, `clients/`.
  - Ho verificato:
    - l'hook e il gate B usano lo stesso formato e lo stesso match per prefisso dalla radice;
    - `.html`, `.txt` e `.md` sono in `_VALID_EXTENSIONS`, quindi una sessione che tocca solo `clients/` o solo `requirements.txt` può essere citata.
  - Esito: **ok**, con riserva R-143-4.
- `tests/test_unit_handoff_check.py:649`, `:673` e `:683` — i tre test nuovi.
  - Con lo script di main al posto di quello nuovo: 2 failed (`-k v3`).
  - Esito: **ok**.

**Misure riprodotte**
- `pytest tests/` senza `test_unit_kernel.py`: 274 passed.
- `test_unit_handoff_check.py`: 39 passed.
- Dopo controprova e mutation il working tree è tornato identico (nessun diff non staged).

**Riserve**

- **R-143-1 (media, verificata — correggere prima del merge)**: `git show origin/main:…` usa un ref abbreviato.
  - Git risolve `refs/tags/origin/main` PRIMA di `refs/remotes/origin/main` e dà solo un warning "refname is ambiguous".
  - `actions/checkout` con `fetch-depth: 0` scarica anche i tag.
  - Sonda (`scratchpad/sonda143b.sh`): un tag `origin/main` che punta a un commit sabotato → `git show origin/main:f.txt` stampa "SABOTATO"; `git show refs/remotes/origin/main:f.txt` stampa "buono".
  - Quindi chi spinge un tag omonimo fa caricare alla CI check neutralizzati, senza toccare ci.yml.
  - Fix: `refs/remotes/origin/main` nelle tre righe `git show`. Più robusto ancora: fare prima `git fetch origin main` e usare `FETCH_HEAD` o lo SHA risolto da `refs/remotes/`.
  - `merge-base origin/main` dentro gli script ha la stessa ambiguità: è un problema preesistente, da tracciare.
- **R-143-2 (residuo dichiarato, strutturale)**: ci.yml viene dalla PR, quindi una PR può rimuovere il passo. Il vettore è più semplice di R-143-1, per cui R-141-2 è MITIGATA, non chiusa.
  - Candidato per chiuderla: un workflow `pull_request_target` dedicato a handoff-check. Usa la definizione di main e qui non eseguirebbe codice della PR: solo git più gli script di main, con `permissions: contents: read` e `persist-credentials: false`.
  - In alternativa, le regole "required workflow" dei ruleset, se disponibili per un account personale (non verificato).
  - Decisione umana.
- **R-143-3 (bootstrapping, risposta ad a)**: in sé accettabile, perché i test pytest esercitano la versione nuova e un falso negativo di main vale solo fino al merge del fix. Due conseguenze vanno scritte in stato_progetto:
  1. **Stallo.** Se main ha un falso BLOCCO, la PR che lo corregge viene bloccata dalla versione vecchia. Le uniche uscite sono modificare ci.yml (cioè proprio il residuo R-143-2) oppure sospendere il ruleset da admin. Serve una procedura dichiarata.
  2. **Divergenza locale/CI.** Il gate locale di fine-task gira con lo script della PR, la CI con quello di main: un handoff può passare in locale e fallire in CI per una sessione. Questa PR non ha rename, quindi non ne soffre.
- **R-143-4 (attrito, risposta a c)**: il controllo dell'hook sul working tree (R-136-1) blocca OGNI commit se nel perimetro c'è un file non tracciato e non ignorato. Il controllo viene eseguito prima del test "nulla del perimetro in stage".
  - `.DS_Store` non è in `.gitignore` e non c'è un excludesfile globale: aprire `clients/voice` dal Finder blocca anche i commit dei soli report.
  - Lo stesso vale per artefatti dei client vocali (audio, output delle sonde in `clients/voice/probe`).
  - Rimedio: aggiungere `.DS_Store` e gli artefatti dei client a `.gitignore`.
  - Oggi `clients/` e `tools/` sono puliti e non vedo altri falsi blocchi: le voci con `/` finale fanno match solo alla radice.
- **Nota (b)**: rimangono falsi blocchi fail-closed per path troncati con `.../`, per nomi che contengono " => " e per nomi non ASCII quotati da `--stat`. La mitigazione è far generare §2 a fine-task con `git -c core.quotePath=false diff --cached --stat=400 …`: è un cambio a `.claude/commands/fine-task.md`, fuori da questo diff.
- **Risposta a (d), by-pass residui**: ci.yml (R-143-2) e il tag omonimo (R-143-1). Escludo come vettori:
  - textconv: `git show` di un blob non lo applica senza `--textconv`, e servirebbe comunque una config locale;
  - l'ombreggiamento di moduli Python dalla cwd: quando si esegue uno script, la cwd non è in `sys.path`;
  - PYTHONPATH e PATH: si modificano solo da ci.yml, quindi rientrano in R-143-2.

**Rischi esplicitamente esclusi (non verificati)**
- Comportamento reale sul runner GitHub, in particolare che `actions/checkout@v4` con `fetch-depth: 0` scarichi davvero `refs/tags/*` e che nel `pull_request` il merge-base sia origin/main. Ho ragionato sulla documentazione e simulato in locale; la CI non è riproducibile in dev.
- Se il ruleset `main-lock` protegga anche i tag: non ho accesso alle impostazioni GitHub.
- Il comportamento di `review_gate.sh` con le nuove voci: l'ho letto (`.claude/hooks/review_gate.sh:72-128`) ma non ho fatto sonde dedicate. Il formato è condiviso e già coperto dalle suite precedenti.
- Non ho eseguito la suite kernel: il diff non tocca gas.py, brains/ né modules/.

**Memoria**: riga #143 e una lezione nuova (ref abbreviato ambiguo: i tag vincono sui remote) aggiunte a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, committate con `commit_memoria_revisore.sh` → `f63bf47`. Il diff staged sotto review è rimasto intatto. Le righe con "git … commit" sono passate da file, per via del matcher del gate (R-gjq-1).

File di sonda:
- `/private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/sonda143.sh` (forme di `--stat`)
- `/private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/sonda143b.sh` (tag `origin/main`)

### Review 144

## VERDETTO: APPROVATO CON RISERVE

Review #144: delta sulla #143. Branch fix/gate-rename-perimetro-ci, 8 file staged. R-143-1 e R-143-4 sono chiuse; la nota (b) è applicata. Non ci sono blocchi. Resta una riserva minore: il ref abbreviato sopravvive in due script che il diff non tocca.

**Elementi del diff esaminati**

- `.github/workflows/ci.yml:239-241` — i tre `git show` usano ora `refs/remotes/origin/main`.
  - Rischio: il tag omonimo della sonda #143, che portava a caricare check sabotati.
  - Col ref completo la sonda `sonda143b.sh` restituisce "buono".
  - Il commento alla riga 232 lo spiega.
  - Esito: **ok**, R-143-1 chiusa lato CI.
- `scripts/check_handoff.py:50` e `scripts/check_verdetto.py:83` — `_get_base` usa `merge-base refs/remotes/origin/main HEAD`.
  - Rischio: un tag `origin/main` sulla punta del branch fa risultare base = HEAD. La sessione appare vuota e il check risponde "non applicabile", cioè passa (fail-open).
  - Ho riprodotto i test e tolto il fix da un solo script alla volta:
    - ref abbreviato solo in check_handoff → `test_r143_1_tag_named_origin_main_does_not_hijack_base` FAILED;
    - ref abbreviato solo in check_verdetto → lo stesso test FAILED, sull'assert `rv`.
  - Il test asserisce rc=1 e "V-A" su entrambi gli script, quindi copre le due modifiche separatamente.
  - Esito: **ok**.
- `scripts/fine_task_finale.sh:133` — anche BASE usa il ref completo. Il comportamento resta invariato senza tag. Esito: **ok**.
- `.claude/commands/fine-task.md:214` — §2 si genera con `git -c core.quotePath=false diff --cached --stat=400`.
  - Rischio: i falsi blocchi della nota (b), cioè path troncati con `...` e nomi non ASCII tra virgolette.
  - Coerente con `_diff_names` (`-z`, nomi grezzi).
  - Esito: **ok**.
- `.gitignore:35-36` — aggiunto `.DS_Store`. L'hook usa `git status` senza `--ignored`, quindi un `.DS_Store` ignorato non conta più come file non tracciato nel perimetro. Esito: **ok**, R-143-4 chiusa.
- `tests/test_unit_handoff_check.py` — test R-143-1. Usa `_setup_session_senza_handoff` (riga 583) e un tag su HEAD. Esito: **ok**.

**Misure riprodotte**
- pytest senza la suite kernel: 275 passed.
- Dopo le mutation il working tree è tornato identico.

**Riserve**

- **R-144-1 (minore, nuova)**: il ref abbreviato resta in file fuori dal diff.
  - `scripts/gasmerge.sh:42` e `scripts/gasmerge.sh:141`, cioè `git diff "origin/main...origin/$BRANCH"`. In locale `git fetch` segue automaticamente i tag che puntano alla storia scaricata. Un tag `origin/main` sulla punta della PR farebbe quindi stampare all'operatore "nessuno (doc-only)" proprio sul promemoria di merge, che è una barriera umana.
  - `.claude/hooks/promemoria_end.sh:45`: solo un promemoria.
  - Fix: anche qui `refs/remotes/origin/main`. Va fatto in questa PR o tracciato.
  - Cosmetico: il messaggio d'errore in `.claude/commands/fine-task.md:21` dice ancora "origin/main".
- **R-143-2** (ci.yml arriva dalla PR) e **R-143-3** (procedura in caso di stallo/bootstrapping): restano aperte come dichiarato. La chiusura di R-143-2 è affidata alla prossima fetta, la verifica esterna con identità separata.
- **Nota**: `.gitignore` non è nel perimetro. Una PR potrebbe ignorare file nuovi del perimetro e così nasconderli al controllo dell'hook sul working tree. Restano comunque fuori dal commit, salvo `add -f`, che li manda in stage dove l'hook li vede. Rischio basso, solo da tenere presente.

**Rischi esplicitamente esclusi (non verificati)**
- Che `actions/checkout@v4` più `git fetch origin main` valorizzino davvero `refs/remotes/origin/main` sul runner. Lo deduco dal fatto che il ref abbreviato funzionava prima e che non esisteva nessun tag omonimo, ma la CI non è riproducibile in dev.
- Non ho eseguito la suite kernel e le suite hook: il delta non tocca gas.py, brains/, modules/ né `.claude/hooks/`.

**Memoria**
- Riga #144 aggiunta a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova, committata con `commit_memoria_revisore.sh` → `067c83d`.
- Il numero di riga di ci.yml nella riga #144 (237-239) era sbagliato: l'ho corretto in 239-241 con un secondo commit, `c287d5f`.
- Il diff staged sotto review è intatto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py, brains/ o modules/: la suite kernel non è stata rilanciata. Test in tests/ (gate): `pytest tests --ignore=tests/test_unit_kernel.py` **271 → 275 passed**, tutti verdi.

## §6 STATO CI

```
completed	success	docs(gate-rename): fine-task — rename nel §2, perimetro piu' largo, c…	CI	fix/gate-rename-perimetro-ci	push	37206161421	1m8s	2026-10-04T13:35:28Z
completed	failure	chore(revisore): memoria review #144 — APPROVATO CON RISERVE	CI	fix/gate-rename-perimetro-ci	push	37206057264	1m16s	2026-10-04T13:33:42Z
completed	success	Merge pull request #120 from Gasss23/fix/handoff-check-vincolante	CI	main	push	37205287598	1m5s	2026-10-04T13:20:43Z
```

Mappatura commit→run (corretta dopo la prima scrittura, che attribuiva per errore la run intermedia a `13b7933`):
- `f63bf47`, `13b7933`, `067c83d`, `c287d5f`: un solo push con testa `c287d5f` (l'ultimo commit di memoria del revisore), run **37206057264**. Esito `unit-suite: success`, `handoff-check: failure`. Il rosso è ATTESO (V-A: perimetro toccato, handoff non ancora presente). Gli altri tre SHA non hanno una run propria: sono inclusi nell'albero testato.
- `1357b68` (primo commit di fine-task): run **37206161421**, `unit-suite: success`, `handoff-check: success`.
- Commit di correzione del §6 (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **PRIORITÀ — V-B vera**: revisione con identità separata su GitHub. Chiude anche R-143-2. È la condizione per la variante B del merge.
- **R-143-3**: procedura di stallo (falso blocco su main).
- **R-144-1**: ref abbreviato in gasmerge.sh e promemoria_end.sh (prossima fetta).
- **R-139-1, V-C**: invariate.
