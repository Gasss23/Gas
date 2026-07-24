# Report: chore/hardening-processo — 2026-07-24

## DECISIONI UMANE RICHIESTE

1. **Review PR #43** (`chore/hardening-processo`, https://github.com/Gasss23/Gas/pull/43): 6 commit, NON mergiata da questa sessione. Merge SOLO a mano da terminale WSL dopo lettura di questo report.
2. ~~Riserve fetta 3 non tracciate in `stato_progetto.md`~~ — **RISOLTO in questa fetta**: `R-gasmerge-failopen` aperto in `reports/stato_progetto.md` con le 3 riserve del revisore + 2 rilievi aggiuntivi dell'operatore (functional check jq, invariante IP limitata a `reports/`).
3. **Merito review #60/#61 (subagent general-purpose in ruolo di revisore) verificato a campione dall'operatore**: accettato come valido, non ri-revisionato. Micro-finding registrato in `stato_progetto.md`. Regola ribadita: lanciare sempre `cd ~/Gas && claude`.

## Esito per fetta

| Fetta | Esito | Commit | Revisore |
|---|---|---|---|
| 1 — T9 gate falsy + restore esatto (tests/) | FATTA | `1551312` | APPROVATO |
| 2 — Formato obbligatorio verdetto (.claude/agents/revisore.md) | FATTA | `fd07a6d` | non richiesto (conflitto d'interesse) |
| 3 — scripts/gasmerge.sh hardening | FATTA | `81933c9` | APPROVATO CON RISERVE |
| 4 — Canonici (fine-task.md §6 + stato_progetto.md ×5) + PR | FATTA | `6f5ba71` | non richiesto (doc-only) |
| 5 — Fix posizione §6 fine-task.md + R-gasmerge-failopen + deviazione gate + contatore review | FATTA | *(vedi sotto)* | non richiesto (doc-only, nessun file di motore) |

Prerequisito eseguito: `git fetch origin && git checkout -b chore/hardening-processo origin/main` da `1ebea40` (PR #42 mergiata). Nessun merge eseguito, nessun push su main, nessun `gh pr merge`.

---

## FETTA 5 — Fix posizione §6 + R-gasmerge-failopen + deviazione gate + contatore review (doc-only)

1. **Fix di posizione `.claude/commands/fine-task.md` §6**: il `>` di chiusura del placeholder angolare era finito DOPO la regola "Mappatura commit→run OBBLIGATORIA" invece che dopo "VIETATO scrivere «prevista verde» senza output reale.", lasciando la regola imprigionata dentro il placeholder invece che fuori come testo normativo. Spostato, testo della regola invariato.
2. **`reports/stato_progetto.md`**: aggiunto il finding aperto 🟡 `R-gasmerge-failopen` con le 3 riserve del verdetto #61 (fail-open `git diff`/`git grep`, gap TOCTOU) più 2 rilievi dell'operatore (presence-check jq invece di functional-check, invariante IP limitata a `reports/`).
3. **`reports/stato_progetto.md`**: aggiunto il micro-finding "Deviazione di gate — subagent revisore non invocato nativamente", con causa (cwd di lancio `/home/gqual` invece di `~/Gas`), verifica a campione dell'operatore, e richiamo alla regola già registrata (nota VPS §6) di lanciare sempre da `~/Gas`.
4. **`reports/stato_progetto.md`**: contatore review allineato da "59 review / ultima #59" a "61 review / ultima #61 (scripts/gasmerge.sh, APPROVATO CON RISERVE); #60 = T9 gate falsy, APPROVATO" — sia nella riga di stato motore sia nell'istituzione C. Fonte verificata live:
   ```
   $ tail -5 .claude/agents/memoria_revisore.md
   #58 — 2026-07-23 — APPROVATO — nessuna lezione nuova
   #59 — 2026-07-24 — APPROVATO — nessuna lezione nuova
   #60 — 2026-07-24 — APPROVATO — Quando un gate di iniezione env passa da `is None` a falsy [...]
   #61 — 2026-07-24 — APPROVATO CON RISERVE — Grep/diff usati come CONDIZIONE di un `if` [...]
   - 2026-07-24 — Un `git fetch` unico eseguito PRIMA di un'attesa lunga [...]
   ```

Nessun file di motore toccato (gas.py/brains/modules/tests/scripts non modificati). Nessun revisore richiesto e nessuno invocato.

---

## AVVISO STRUTTURALE — subagent `revisore` non registrato in questo harness

Il file `.claude/agents/revisore.md` esiste nel repo (`/home/gqual/Gas/.claude/agents/`) ma il tool Agent di questa sessione **non lo espone come `subagent_type`** — l'elenco disponibile era `claude, claude-code-guide, Explore, general-purpose, Plan, statusline-setup`. Causa probabile: la working directory radice della sessione harness è `/home/gqual` (vedi contesto ambiente), non `/home/gqual/Gas`, quindi la scoperta di agent di progetto non trova `.claude/agents/` del repo Gas.

**Mitigazione applicata (dichiarata, non nascosta)**: per fetta 1 e fetta 3 ho invocato un agente `general-purpose` con istruzioni esplicite di leggere e seguire `.claude/agents/revisore.md` alla lettera (incluse le tre letture obbligatorie preliminari e l'aggiornamento di `.claude/agents/memoria_revisore.md`), agendo nel ruolo del revisore. Le righe contatore #60 e #61 sono state aggiunte realmente al file di memoria da quell'agente. Questo NON è il subagent dedicato dichiarato nel gate CLAUDE.md — è una sostituzione fedele ma non equivalente al 100%: **da verificare con l'operatore se accettabile come gate valido per queste due fette**, o se le PR vanno ri-revisionate quando il subagent `revisore` sarà disponibile nell'ambiente corretto.

---

## FETTA 1 — T9 gate falsy + restore esatto (tests/test_unit_kernel.py)

### Problema

Nel blocco T9, l'iniezione delle chiavi fittizie GEMINI_API_KEY/GROQ_API_KEY gatava su `_gem_key is None` (variabile assente), mentre `run_turn` in gas.py gata su falsy (`if not os.environ.get(env): continue`, gas.py:1493/1607). Con `GEMINI_API_KEY=""` nell'ambiente (presente ma vuota), il gate `is None` non scattava, il rung non veniva costruito, T9a/T9c diventavano rossi per ragione ambientale.

### Fix applicato

1. Gate di iniezione cambiato da `is None` a falsy, con sentinel `_MISSING = object()` per distinguere "assente" da "presente e vuota".
2. Il `finally` ora ripristina il valore ORIGINALE ESATTO: `pop` se assente (`_gem_key is _MISSING`), riassegnazione esplicita del valore catturato altrimenti (anche se `""`).
3. `OPENROUTER_API_KEY` e `GAS_OLLAMA_URL` in questo stesso blocco **NON toccati**: usano già `os.environ.pop(key, None)` (pop incondizionato + restore `if val is not None`), pattern diverso dal gate `is None` sull'iniezione — non hanno lo stesso difetto perché un valore d'ambiente reale non è mai il sentinel Python `None`.

### Prove obbligatorie (comandi reali, output incollato verbatim)

**(a) Suite completa (ambiente normale, senza forzare chiavi vuote):**
```
[PASS] T59c os.replace fallisce → nessun crash — exc=None
[PASS] T59c file originale intatto byte-a-byte — original_len=58 after_len=58
[PASS] T59c nessun file tmp residuo dopo fallimento — tmp_after=[]

=== RIEPILOGO: 250 PASS, 0 FAIL ===
```
Exit code: 0.

**(b) Prova che il difetto esisteva — PRIMA del fix, `GEMINI_API_KEY="" GROQ_API_KEY=""`:**
```
[FAIL] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=0 errori=1
[FAIL] T9c storia salvata su disco nella root temporanea

=== RIEPILOGO: 248 PASS, 2 FAIL ===
  FAIL: T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {}
  FAIL: T9c storia salvata su disco nella root temporanea
```
Exit code: 1. Il nit era un difetto REALE, confermato in rosso prima del fix.

**DOPO il fix, stesso ambiente (`GEMINI_API_KEY="" GROQ_API_KEY=""`):**
```
[PASS] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {'gemini-2.5-flash-lite': 10, 'gemini-2.5-flash': 10, 'openai/gpt-oss-120b': 10}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=30 errori=1
[PASS] T9c storia salvata su disco nella root temporanea

=== RIEPILOGO: 250 PASS, 0 FAIL ===
```
Exit code: 0.

**(c) Ambiente invariato dopo la suite** (con GEMINI_API_KEY="" GROQ_API_KEY="" impostate intorno alla suite, verifica che restino esattamente presenti-e-vuote, non assenti né col valore fittizio):
```
GEMINI_API_KEY after suite = [] (len=0)
GROQ_API_KEY after suite = [] (len=0)
```
Verificato anche il caso "originariamente assenti" (ambiente shell normale, GEMINI_API_KEY/GROQ_API_KEY non settate): `env | grep -c GEMINI_API_KEY` → 0 sia prima sia dopo la suite completa.

### Revisore — VERDETTO INTEGRALE VERBATIM

> **VERDETTO: APPROVATO**
>
> Il diff staged tocca esclusivamente `tests/test_unit_kernel.py`, blocco T9 (righe 138-158), esattamente come dichiarato. Nessun tocco a `gas.py`, `brains/`, `modules/`: il fix è puramente di test, non tocca la logica di produzione né i guardrail di CLAUDE.md §8 (cap 10 iterazioni) — anzi li rafforza dando loro copertura reale anche quando l'ambiente presenta chiavi vuote invece che assenti.
>
> Analisi tecnica concreta:
>
> - `tests/test_unit_kernel.py:141-142` — `_gem_key = os.environ.get("GEMINI_API_KEY", _MISSING)` con `_MISSING = object()` — distingue "variabile assente" da "presente e vuota". Rischio esaminato: che il sentinel non catturi correttamente il caso "presente e vuota" lasciando comunque un buco nel gate. Esito: verificato empiricamente — con `GEMINI_API_KEY=""` iniettata nell'ambiente, il ramo di iniezione (riga 146, `not (_gem_key if _gem_key is not _MISSING else "")`) scatta correttamente (perché `""` è falsy) e costruisce il rung; senza il fix lo stesso scenario produceva `chiamate per modello: {}` (riprodotto io stesso via `git stash`). Nessun difetto.
>
> - `tests/test_unit_kernel.py:155-158` — il `finally` ora fa `if _gem_key is _MISSING: pop(...) else: os.environ[key] = _gem_key`, cioè ripristina il valore ORIGINALE esatto invece di limitarsi a cancellare la chiave. Rischio esaminato: se si fosse corretta SOLO la condizione di iniezione (riga 146) lasciando il vecchio restore (`if _gem_key is None: pop`, senza `else`), il caso "presente e vuota" sarebbe stato iniettato correttamente ma MAI ripristinato — la chiave fittizia sarebbe rimasta nell'ambiente del processo dopo la suite, un side-effect silenzioso su un processo di lunga vita (es. CI job con più step). Esito: il fix corregge SIMMETRICAMENTE iniezione e restore; verificato dal vivo che post-suite `GEMINI_API_KEY`/`GROQ_API_KEY` tornano esattamente a `''` (non assenti, non col valore fittizio) quando l'ambiente di partenza le aveva vuote, e vengono correttamente rimosse (`pop`) quando l'ambiente di partenza non le aveva affatto. Nessun difetto.
>
> - `tests/test_unit_kernel.py:138-139` vs `141-158` — coesistenza di due pattern diversi nello stesso blocco: `OPENROUTER_API_KEY`/`GAS_OLLAMA_URL` usano `os.environ.pop(key, None)` incondizionato (semplice, perché vengono SEMPRE disattivate per il test, indipendentemente dal valore originale), mentre `GEMINI_API_KEY`/`GROQ_API_KEY` usano il sentinel perché vanno toccate SOLO se falsy. Non è un'incoerenza di stile: è la scelta corretta, perché applicare il pattern `pop(key, None)` anche a GEM/GROQ avrebbe richiesto comunque un `else: os.environ[key] = valore` esplicito per il caso "presente e truthy → non toccare" (lo stesso identico problema che il sentinel risolve, solo scritto in una forma più fragile). Nessun rischio residuo su questo punto.
>
> - Coerenza con CLAUDE.md §8 e la roadmap: il fix non allarga né indebolisce il cap a 10 iterazioni né la cascata paracadute — rende solo l'iniezione delle chiavi fittizie realmente equivalente al gate di produzione (`os.environ.get(env)` falsy in `gas.py:1493`), colmando esattamente il tipo di falso-verde ambientale già registrato in stato_progetto.md come "Lezione T9b (2026-07-24)" e "R-ci-openrouter". Va nella direzione della roadmap (copertura reale del guardrail anti-loop), non la contraddice.
>
> - Nessuna caccia positiva ad antipattern del Wall of Shame: zero slicing diretto della history, zero simulazione di output tool (il fake client resta com'era, solo il gate delle chiavi cambia).
>
> Osservazione minore non bloccante (stile, non riserva): la riga 146/147 `if not (_gem_key if _gem_key is not _MISSING else ""): ...` è corretta ma leggermente contorta; una forma equivalente più leggibile sarebbe stata `if _gem_key is _MISSING or not _gem_key:`. Non impatta la correttezza (verificato empiricamente identica in tutti e tre i rami: assente, presente-vuota, presente-truthy) — la segnalo solo per eventuale pulizia futura, non è motivo di riserva.
>
> **Rischio esplicitamente escluso dalla verifica**: non ho eseguito il fix in un vero job CI GitHub Actions (nessuna esecuzione remota triggerata da questa review) — mi sono limitato all'esecuzione locale nel venv del repo, che riproduce fedelmente lo scenario CI descritto (chiavi assenti/vuote per design nel workflow), ma non è un artefatto CI reale. Non ho inoltre verificato il comportamento con valori "quasi vuoti" ma non-stringa-vuota (es. whitespace-only `" "`), perché sia il gate di produzione (`gas.py:1493`) sia il gate di test trattano `" "` come truthy in modo identico e coerente — non è una divergenza introdotta da questo diff, quindi l'ho considerato fuori scope per questa review mirata.
>
> Memoria aggiornata: aggiunta riga contatore `#60 — 2026-07-24 — APPROVATO` in coda a `.claude/agents/memoria_revisore.md`, con una lezione nuova sulla necessità di rendere simmetrico il fix di un gate is-None→falsy anche sul lato restore (verificata empiricamente in questa sessione).

**Dichiarazione (a) richiesta dal prompt**: questo verdetto è stato prodotto PRIMA che la fetta 2 (formato obbligatorio del verdetto) fosse committata — a quel punto `.claude/agents/revisore.md` non conteneva ancora la nuova regola. **Verificato a posteriori**: il verdetto rispetta comunque il formato introdotto dopo (≥2 elementi concreti nel formato path:riga—cosa fa—rischio—esito: qui ce ne sono 4; un rischio esplicitamente escluso: presente). Non è un verdetto degenere, per puro merito del contenuto, non per conformità procedurale (la regola non esisteva ancora quando è stato scritto).

---

## FETTA 2 — Formato obbligatorio del verdetto (.claude/agents/revisore.md)

Sezione "## FORMATO OBBLIGATORIO DEL VERDETTO (dal 2026-07-24)" inserita testualmente, subito dopo "## Come revisioni" e prima di "## DOPO ogni review", senza riscrivere il resto del file. Contenuto verbatim come da istruzione dell'operatore (incluse le date/numeri di review #56/#59/PR#14/PR#18 citati come motivazione — riportati come testo prescritto, non ri-verificati riga per riga contro `memoria_revisore.md`, dove #56 in realtà porta anche una lezione tecnica oltre alla riga contatore; la formulazione dell'operatore era comunque quella da inserire testualmente).

Commit doc-only `fd07a6d`. **Nessun revisore invocato** — conflitto d'interesse dichiarato (il file modificato è la definizione del revisore stesso).

---

## FETTA 3 — scripts/gasmerge.sh

### Provenienza

Copiato da `/home/gqual/bin/gasmerge` (leggibile, 1747 byte, script personale collaudato non versionato). Modifiche mirate, nessuna riscrittura da zero.

### Modifiche applicate

- **(a) Wrapper `main()`**: intero corpo incapsulato in `main() { ... }` con `main "$@"` come ultima riga, con commento che spiega il motivo (lo script fa `git checkout main && git pull --ff-only` sulla working dir che lo contiene stesso; bash legge lo script a chunk, un pull a metà corsa rischierebbe byte misti; il wrapper forza il parsing completo del corpo prima dell'esecuzione).
- **(b) Fix CI**: `timeout 900 gh pr checks "$PR" --watch --fail-fast --interval 10`, cattura exit code con `set +e`/`set -e` locale, blocco su 1/8/124/altro ≠0; poi verifica JSON indipendente (`gh pr checks "$PR" --json name,bucket`) che blocca su zero check o bucket ≠ pass/skipping, stampando nome+bucket di ogni check.
- **(c) File sensibili**: regex estesa da `^(gas\.py|brains/|modules/|tests/)` a `^(gas\.py|brains/|modules/|tests/|scripts/|\.claude/)`.
- **(d) Provenienza**: stampa SHA+data dell'ultimo commit su `scripts/gasmerge.sh` e warning `*** GASMERGE MODIFICATO E NON COMMITTATO ***` se `git status --porcelain` non è vuoto, PRIMA della conferma digitata.
- **(e) NON toccati**: `--admin` mai aggiunto; logica di conferma digitata, invariante IP, delete branch invariati.

### Test reali (nessuno simulato)

```
$ bash -n scripts/gasmerge.sh
(nessun output = sintassi valida)
bash -n: PASS
```

```
$ command -v shellcheck
(vuoto — non installato)
shellcheck NON installato — skip (regola: NON installarlo)
```

```
$ git rev-parse HEAD   # prima
fd07a6db922615fcebe538bf9354015f59bb98a3
$ ./scripts/gasmerge.sh 42
BLOCCO: PR #42 è MERGED
EXIT CODE: 1
$ git rev-parse HEAD   # dopo
fd07a6db922615fcebe538bf9354015f59bb98a3   (invariato)
```

```
$ ./scripts/gasmerge.sh
./scripts/gasmerge.sh: line 13: 1: uso: gasmerge <numero-PR>
EXIT CODE: 1

$ ./scripts/gasmerge.sh abc
no pull requests found for branch "abc"
EXIT CODE: 1
```
(Il caso argomento-non-numerico blocca via `set -e` su `gh pr view abc` fallito, non con un messaggio "BLOCCO" dedicato — comunque exit ≠0, requisito "deve bloccare" soddisfatto.)

```
$ git status --porcelain   # dopo tutti i test
(vuoto)
```

⛔ **Non eseguito su nessuna PR aperta** — per il divieto esplicito e bloccante del prompt (mergerebbe davvero). PR #42 (chiusa/MERGED) è stata sufficiente a coprire il ramo di blocco iniziale; i rami successivi (CI watch, verifica JSON, invariante IP, provenienza, merge finale) **non sono stati esercitati da un'esecuzione reale** in questa sessione — solo verificati per lettura statica dal revisore (vedi verdetto sotto, "rischio esplicitamente escluso").

### Revisore — VERDETTO INTEGRALE VERBATIM

> ## VERDETTO — Review #61 (2026-07-24) — `scripts/gasmerge.sh` (nuovo file, diff staged)
>
> ### APPROVATO CON RISERVE
>
> Ho letto per intero `.claude/agents/revisore.md` (inclusa la sezione "FORMATO OBBLIGATORIO DEL VERDETTO" del 2026-07-24), CLAUDE.md sez. 5/8, `reports/stato_progetto.md` e `.claude/agents/memoria_revisore.md` prima di questa review. Ho esaminato `git diff --staged` reale (100 righe, `scripts/gasmerge.sh` nuovo file) — non mi sono fidato del solo riassunto fornito.
>
> ### Elementi concreti del diff esaminati
>
> 1. **`scripts/gasmerge.sh:70-71`** — `ENGINE=$(git diff --name-only "origin/main...origin/$BRANCH" | grep -E '^(gas\.py|brains/|modules/|tests/|scripts/|\.claude/)' || true)`.
>    Cosa fa: costruisce la lista dei file "di motore" toccati dalla PR, per decidere se stampare l'avviso di scrutinio extra.
>    Rischio esaminato: sotto `pipefail`, se `git diff --name-only` fallisce con un errore REALE (rc≥2 — es. `origin/$BRANCH` stantio o non risolvibile, non "nessun match"), il `|| true` sulla pipeline inghiotte anche QUEL fallimento, non solo il caso "grep non trova nulla" (rc=1 legittimo). `ENGINE` resta vuoto e lo script stampa "nessuno (doc-only)" come se il controllo avesse VERIFICATO l'assenza di file motore, quando in realtà il controllo è FALLITO silenziosamente.
>    Esito: **riserva** — fail-open su errore anziché fail-closed, su un controllo che dovrebbe innescare scrutinio umano extra.
>
> 2. **`scripts/gasmerge.sh:64-67`** — `if git grep -qE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' "origin/$BRANCH" -- reports/; then echo "BLOCCO..."; exit 1; fi` seguito da `echo "0 match OK"`.
>    Cosa fa: invariante anti-leak IP, blocca il merge se trova un IP in `reports/` sul branch della PR.
>    Rischio esaminato: sotto `set -e`, i comandi nella condizione di un `if` sono ESENTI dal trigger di uscita dello script. `git grep` restituisce rc=0 (match trovato → BLOCCO, corretto) o rc=1 (nessun match). Ma se `git grep` fallisce con un errore REALE (rc≥2 — ref inesistente, corruzione, ecc.), l'`if` valuta comunque "falso" (solo rc=0 attiva il blocco) e lo script prosegue stampando "0 match OK" **senza aver realmente verificato l'assenza di IP**. È lo stesso pattern del punto 1, ma qui colpisce un controllo di sicurezza esplicitamente citato nei canonici (scrub IP/SSH, roadmap item 0) invece di un controllo diagnostico.
>    Esito: **riserva** — stesso pattern fail-open, su un guardrail più sensibile.
>
> 3. **`scripts/gasmerge.sh:16` vs `:28,64,70-71`** — `git fetch --prune origin` avviene UNA sola volta in testa allo script (riga 16), PRIMA della sezione CI (riga 30+) che può attendere fino a **900 secondi** (`timeout 900 gh pr checks "$PR" --watch --fail-fast --interval 10`, riga 36). Le sezioni successive (diff `--stat` a riga 28 è anteriore al wait quindi coerente; ma invariante IP riga 64 e file-motore riga 70-71 sono POSTERIORI al wait) leggono `origin/$BRANCH` così come risultava al fetch iniziale, senza ri-fetch.
>    Rischio esaminato: se durante l'attesa CI (fino a 15 minuti) vengono pushati nuovi commit sul branch della PR, i controlli invariante-IP e file-motore restano sullo stato VECCHIO del branch, mentre `gh pr merge "$PR" --merge --delete-branch` (riga 92) mergia lo stato ATTUALE della PR su GitHub al momento del merge — potenzialmente diverso da quanto controllato e mostrato all'operatore per la conferma digitata.
>    Esito: **riserva** — gap TOCTOU introdotto/aggravato proprio dalla modifica (b) di questa sessione (il watch lungo è nuovo rispetto all'originale `~/bin/gasmerge`).
>
> 4. **`scripts/gasmerge.sh:71`** — regex file sensibili `^(gas\.py|brains/|modules/|tests/|scripts/|\.claude/)`.
>    Cosa fa: estesa (rispetto all'originale) per includere `scripts/` e `.claude/`.
>    Rischio esaminato: copertura di `.github/workflows/ci.yml` — una PR che indebolisse il workflow CI (es. rimuovendo `unit-suite` dai check required) non farebbe scattare l'avviso "tocca il MOTORE", passerebbe come "doc-only" nonostante sia potenzialmente più critica di un cambio a `tests/`.
>    Esito: **riserva minore** — buco residuo nella regex, non bloccante ma degno di essere chiuso alla prossima iterazione.
>
> ### Rischio esplicitamente escluso (non verificato)
>
> La descrizione dei test reali fornita conferma che l'esecuzione dal vivo ha colpito SOLO: `bash -n` (sintassi), il ramo "PR già MERGED" (uscita immediata alla riga 22, **prima** di qualunque altra sezione), l'assenza di argomento (`${1:?...}`), e l'argomento non numerico (fallisce su `gh pr view abc`, uscita per `set -e`). **Nessuno di questi esercita realmente**: il case statement sull'exit code CI (righe 39-45), la verifica JSON indipendente sui bucket (righe 51-60), il grep IP (riga 64), la regex file-motore (righe 70-71), il blocco PROVENIENZA (righe 82-86), o il flusso di merge finale (righe 92-97). Questo NON è verificabile in questo ambiente senza una PR aperta reale — cosa esplicitamente vietata dal protocollo (eseguirebbe il merge per davvero). Dichiaro quindi il comportamento runtime di tutta la logica successiva alla riga 22 come **non verificato da esecuzione reale, solo da lettura statica del codice** — coerente con la lezione già in memoria (review #47, 2026-07-14): "un claim di N PASS confermati va sempre verificato eseguendo, non fidarsi del claim". Qui non c'è nemmeno un claim di esecuzione su quei rami, quindi la review resta sulla sola correttezza statica per quella porzione.
>
> ### Valutazioni aggiuntive (non bloccanti)
>
> - Il wrapper `main() { ... }; main "$@"` (punto a) è una mitigazione REALE e corretta: bash deve completare il parsing dell'intero blocco `{ ... }` (comando composto) prima di poter definire/eseguire la funzione, quindi il corpo è già interamente in memoria come AST quando `git pull --ff-only` (dentro la funzione stessa) potrebbe modificare il file su disco — il pull successivo non può più far leggere byte misti alla funzione già parsata. Non toglie però la finestra residua sulla RIGA `main "$@"` letta separatamente, che però esegue solo una chiamata già risolta a un simbolo di funzione in memoria: nessun problema pratico.
> - Il pattern `set +e` / cattura `$?` / `set -e` attorno a `timeout 900 gh pr checks --watch` (righe 35-38) è corretto e atomico: cattura l'exit code prima di ripristinare `-e`, coerente con la lezione #51 in memoria (guard bash atomico).
> - Il case statement (righe 40-44) blocca su TUTTI gli esiti diversi da 0 (1/8/124/`*`), quindi fail-closed di default anche su codici di uscita non previsti di `gh`.
> - La doppia verifica CI (watch + JSON bucket indipendente, righe 51-60) è una buona difesa in profondità: intercetta il caso "0 check registrati" e qualunque bucket diverso da `pass`/`skipping`, fail-closed su bucket sconosciuto.
> - Quoting delle variabili (`"$PR"`, `"$BRANCH"`, `"origin/$BRANCH"`, `"$ANS"`) corretto ovunque; `read -r` usato correttamente.
> - `--admin` non è mai stato aggiunto, la logica di conferma digitata (`read -r ANS` confrontato esattamente con `$PR`) e l'invariante IP restano quelle collaudate: confermato dalla lettura diretta del diff.
> - Nessuna variabile è dichiarata `local` dentro `main()` — pollution dello scope globale della shell, ma innocuo dato che lo script esegue `main "$@"` come ultima istruzione e poi termina: non è un bug funzionale, solo un'osservazione di stile.
>
> ### Motivo dell'esito
>
> Nessuna delle riserve trovate rompe l'invariante "zero crash" né consente un bypass DIRETTO e riproducibile della conferma umana in condizioni normali — sono tutte finestre di errore rare (ref stanti, comandi git che falliscono con un errore reale anziché "nessun match", finestra di 15 minuti senza ri-fetch). Ma sono reali, concrete, e riguardano proprio i punti che la sessione dichiara di aver rinforzato (invariante IP, rilevamento file motore, verifica CI robusta): il pattern "errore del comando confuso con esito negativo legittimo" va corretto prima che questo script diventi l'unica barriera prima del merge su main, come i canonici stessi dichiarano (`gasmerge` = barriera reale ma solo disciplinare).
>
> Aggiornamento memoria: aggiunta la riga contatore `#61 — 2026-07-24 — APPROVATO CON RISERVE` in `/home/gqual/Gas/.claude/agents/memoria_revisore.md`, con due lezioni nuove: (1) il pattern "grep/diff in condizione `if` o dietro `|| true` in pipeline con `pipefail` confonde rc=1 (nessun match) con rc≥2 (errore reale)"; (2) "un fetch unico prima di un'attesa lunga lascia i controlli successivi su refs potenzialmente stantii".

**Riserve NON tracciate in `reports/stato_progetto.md`** in questa sessione (fuori dallo scope prescritto per fetta 3, che non includeva un aggiornamento canonici per gasmerge oltre alla riga di registrazione già inserita in fetta 4). Proposta per l'operatore: aprire un finding `R-gasmerge-failopen` al prossimo giro canonici, con le 3 riserve del verdetto #61 (fail-open su `git diff`/`git grep` con errore reale, TOCTOU sul fetch pre-watch-CI).

---

## FETTA 4 — Canonici + PR

### `.claude/commands/fine-task.md` §6

Inserita la clausola "Mappatura commit→run OBBLIGATORIA" testualmente come da istruzione.

### `reports/stato_progetto.md` — 5 correzioni

1. Nuovo micro-finding (2026-07-24) sulla CI di PR #42 attribuita a 3 commit su 2 run — inserito.
2. Declassata l'attribuzione dei 247 PASS (riga 9) da "provenivano dalla CI/Codespace" a "origine NON VERIFICATA (ipotesi CI/Codespace, mai confermata da un artefatto)". **Nota di precisione**: la frase letterale "provenivano dalla CI/Codespace" compariva SOLO alla riga 9 del file; la nota "§7" (item numerato "7." sotto "Note operative VPS", riferita da "vedi §7" alla riga 9) non ripeteva quella frase — si limitava a un rimando incrociato ("le '247 PASS WSL 2026-07-19' erano false... vedi errore dichiarato in riga 9") già coerente col nuovo testo. Non ho quindi trovato un secondo punto letterale da correggere in §7; se l'operatore intendeva un punto diverso, va indicato.
3. Registrata la recidiva Flag #3 (review #59) accanto al Flag #2 esistente, dentro R-hook-jq.
4. Aggiunto il finding aperto 🟡 `R-verdetto-evidenza`.
5. Registrato il porting di gasmerge in `scripts/gasmerge.sh` e il cambio di superficie.

Diff completo verificato con `git diff` prima del commit (vedi commit `6f5ba71`).

### PR aperta

`gh pr create` → **https://github.com/Gasss23/Gas/pull/43**. NON mergiata, come da regola ferrea. Nessun `gh pr merge` eseguito in questa sessione.

---

## CI di questa sessione

```
$ gh run list -L 3
completed	success	docs(report): reports/ultimo_report.md — sessione chore/hardening-pro…	CI	chore/hardening-processo	push	30078926449	58s	2026-07-24T08:26:23Z
completed	success	docs(canonici): mappatura commit->run obbligatoria + 5 correzioni sta…	CI	chore/hardening-processo	push	30078697173	42s	2026-07-24T08:22:29Z
completed	success	Merge pull request #42 from Gasss23/fix/t9a-deterministico	CI	main	push	30055699560	52s	2026-07-24T00:16:08Z
```

**Mappatura commit→run** (applicando SUBITO la regola introdotta in fetta 4 — caso di studio reale, 2 push separati in questa sessione):
- Push 1 (`1551312`, `fd07a6d`, `81933c9`, `6f5ba71`) → **UNA sola run**: `30078697173`, `headSha = 6f5ba71...` (verificato con `gh run view 30078697173 --json headSha`), conclusion `success`.
  - `1551312`, `fd07a6d`, `81933c9` **NON hanno mai avuto una run propria** — coperti solo indirettamente perché il loro contenuto è incluso nell'albero testato al momento del push (`6f5ba71`). Copertura sostanziale sì, run individuale no.
  - `6f5ba71` → run propria: `30078697173` ✅ SUCCESS.
- Push 2 (`4fd0d31`, commit del report) → run propria: `30078926449`, `headSha = 4fd0d31...` (verificato), conclusion `success`.

Nessuna formula collettiva del tipo "tutti i commit hanno CI verde" — mappatura esplicita per singolo SHA come richiesto dalla nuova regola §6.

---

## (b) Azioni senza traccia in git di questa sessione

Nessuna. Tutte le modifiche sostanziali sono passate da commit tracciati (`1551312`, `fd07a6d`, `81933c9`, `6f5ba71`). Le uniche attività non tracciate sono state:
- esecuzioni di test locali (venv WSL, `python tests/test_unit_kernel.py` con varie combinazioni di env vars) — per costruzione non producono artefatti da tracciare, solo output di terminale incollato sopra;
- lettura di file (repo, memoria revisore, canonici) da parte degli agenti di revisione.

Non ho installato nulla (shellcheck esplicitamente NON installato, come richiesto), non ho modificato `~/bin/gasmerge` né alcunché fuori dal repo `/home/gqual/Gas`.

---

## Riepilogo commit sul branch (`chore/hardening-processo`, base `1ebea40`)

```
4fd0d31 docs(report): reports/ultimo_report.md — sessione chore/hardening-processo
6f5ba71 docs(canonici): mappatura commit->run obbligatoria + 5 correzioni stato_progetto
81933c9 feat(scripts): versiona gasmerge.sh — wrapper anti-corruzione, CI watch reale, provenienza
fd07a6d docs(revisore): formato obbligatorio del verdetto — vieta verdetti degeneri
1551312 fix(test_unit_kernel): gate falsy per iniezione chiavi T9, restore esatto con sentinel
```

PR: https://github.com/Gasss23/Gas/pull/43 (APERTA, non mergiata).

Nota: `git diff --stat`/`git log --oneline` di `${BASE}..HEAD` (BASE = `git merge-base origin/main HEAD` = `1ebea40`) includono anche questo stesso commit di aggiornamento report, essendo /fine-task eseguito DOPO di esso in questa stessa sessione.
