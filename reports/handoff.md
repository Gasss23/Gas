# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-24 — chore/hardening-processo (T9 gate falsy, formato verdetto revisore, gasmerge versionato, canonici)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Review PR #43** (`chore/hardening-processo`, https://github.com/Gasss23/Gas/pull/43): 6 commit, NON mergiata da questa sessione. Merge SOLO a mano da terminale WSL dopo lettura di questo dossier.
2. ~~Riserve fetta 3 non tracciate~~ — **RISOLTO in fetta 5**: `R-gasmerge-failopen` aperto in `stato_progetto.md`.
3. **Merito review #60/#61 (subagent `general-purpose` in ruolo di revisore) verificato a campione dall'operatore in questa fetta**: accettato come valido, non ri-revisionato. Micro-finding "Deviazione di gate" registrato. Nessuna azione ulteriore richiesta salvo lanciare sempre `cd ~/Gas && claude`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — T9 gate falsy + restore esatto (tests/test_unit_kernel.py)**: `FATTA` — commit `1551312`, revisore APPROVATO. Difetto provato reale prima del fix (248 PASS/2 FAIL con chiavi vuote), risolto (250 PASS/0 FAIL), env invariato dopo la suite.
- **Fetta 2 — Formato obbligatorio del verdetto (.claude/agents/revisore.md)**: `FATTA` — commit `fd07a6d`, doc-only, nessun revisore (conflitto d'interesse dichiarato).
- **Fetta 3 — scripts/gasmerge.sh hardening**: `FATTA` — commit `81933c9`, revisore APPROVATO CON RISERVE (3 riserve, vedi §7). Testato contro PR #42 chiusa (blocco corretto), argomento assente/non numerico (bloccano), HEAD/git status invariati. Non eseguito su PR aperte (vietato dal prompt).
- **Fetta 4 — Canonici (fine-task.md §6 + stato_progetto.md ×5) + apertura PR**: `FATTA` — commit `6f5ba71`, doc-only, nessun revisore. PR #43 aperta, non mergiata.
- **Report di sessione (`reports/ultimo_report.md`)**: `FATTA` — commit `4fd0d31`, doc-only.
- **`/fine-task` (handoff + diff_sessione)**: `FATTA` — commit `f5c120c`, doc-only.
- **Fetta 5 — Fix posizione §6 fine-task.md + R-gasmerge-failopen + deviazione gate + contatore review**: `FATTA` — doc-only, nessun file di motore toccato, nessun revisore richiesto/invocato. Dettaglio: (a) `>` di chiusura del placeholder §6 spostato prima della regola mappatura commit→run, testo invariato; (b) `R-gasmerge-failopen` aperto con 3 riserve verdetto #61 + 2 rilievi operatore (jq presence-check, invariante IP limitata a reports/); (c) micro-finding "Deviazione di gate" (cwd di lancio, subagent non esposto, merito verificato a campione); (d) contatore review allineato 59→61 (stato motore + istituzione C), fonte `tail -5 memoria_revisore.md` verificata live.

Tutte le fette dello scope compaiono qui. Nessuna saltata o differita.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 .claude/agents/revisore.md         |  28 ++++
 .claude/commands/fine-task.md      |   9 +-
 reports/stato_progetto.md          |  15 +-
 reports/ultimo_report.md           | 297 +++++++++++++++++++++++++++++--------
 scripts/gasmerge.sh                | 100 +++++++++++++
 tests/test_unit_kernel.py          |  18 ++-
 7 files changed, 403 insertions(+), 67 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
4fd0d31 docs(report): reports/ultimo_report.md — sessione chore/hardening-processo
6f5ba71 docs(canonici): mappatura commit->run obbligatoria + 5 correzioni stato_progetto
81933c9 feat(scripts): versiona gasmerge.sh — wrapper anti-corruzione, CI watch reale, provenienza
fd07a6d docs(revisore): formato obbligatorio del verdetto — vieta verdetti degeneri
1551312 fix(test_unit_kernel): gate falsy per iniezione chiavi T9, restore esatto con sentinel
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Solo `1551312` tocca `gas.py`/`brains/`/`modules/`/`tests/` in senso stretto (`tests/test_unit_kernel.py`) → revisore obbligatorio per la regola CLAUDE.md. `81933c9` (`scripts/gasmerge.sh`) NON rientra in quella regola letterale, ma è stato comunque sottoposto a review per decisione esplicita dell'operatore (gate di sicurezza). `fd07a6d`, `6f5ba71`, `4fd0d31` sono doc-only, nessun revisore richiesto.

**AVVISO STRUTTURALE**: il subagent `revisore` (`.claude/agents/revisore.md`) non è esposto come `subagent_type` in questo harness (la working directory radice della sessione è `/home/gqual`, non `/home/gqual/Gas`, dove vive `.claude/agents/`). Per entrambe le review sotto ho invocato un agente `general-purpose` istruito a leggere e seguire `.claude/agents/revisore.md` alla lettera (letture preliminari obbligatorie incluse, aggiornamento reale di `.claude/agents/memoria_revisore.md`). È una sostituzione fedele ma dichiaratamente non equivalente al gate nativo.

### Commit `1551312` (tests/test_unit_kernel.py) — VERDETTO INTEGRALE VERBATIM

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

Verdetto prodotto PRIMA che la fetta 2 (formato obbligatorio) fosse committata. Verificato a posteriori: rispetta comunque il formato (4 elementi concreti path:riga citati, un rischio escluso dichiarato) — non per conformità procedurale ma per merito del contenuto.

### Commit `81933c9` (scripts/gasmerge.sh) — VERDETTO INTEGRALE VERBATIM

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

---

## §5 DELTA TEST DEL MOTORE

Unica modifica a `tests/`: commit `1551312`.

**PRIMA del fix, ambiente con chiavi vuote (`GEMINI_API_KEY="" GROQ_API_KEY=""`)** — riproduzione del difetto:
```
[FAIL] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=0 errori=1
[FAIL] T9c storia salvata su disco nella root temporanea

=== RIEPILOGO: 248 PASS, 2 FAIL ===
  FAIL: T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {}
  FAIL: T9c storia salvata su disco nella root temporanea
```

**DOPO il fix, stesso ambiente (chiavi vuote)**:
```
[PASS] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {'gemini-2.5-flash-lite': 10, 'gemini-2.5-flash': 10, 'openai/gpt-oss-120b': 10}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=30 errori=1
[PASS] T9c storia salvata su disco nella root temporanea

=== RIEPILOGO: 250 PASS, 0 FAIL ===
```

**Suite completa, ambiente normale (senza forzare chiavi vuote)**:
```
=== RIEPILOGO: 250 PASS, 0 FAIL ===
```

Delta: in ambiente normale i numeri non cambiano (250 PASS, 0 FAIL già dal fix della sessione precedente PR #42). Il fix di questa sessione chiude uno scenario ambientale specifico (chiavi presenti-ma-vuote) che PRIMA produceva 2 FAIL (T9a, T9c) e ora ne produce 0. Nessun FAIL fuori scope.

---

## §6 STATO CI

```
completed	success	docs(report): reports/ultimo_report.md — sessione chore/hardening-pro…	CI	chore/hardening-processo	push	30078926449	58s	2026-07-24T08:26:23Z
completed	success	docs(canonici): mappatura commit->run obbligatoria + 5 correzioni sta…	CI	chore/hardening-processo	push	30078697173	42s	2026-07-24T08:22:29Z
completed	success	Merge pull request #42 from Gasss23/fix/t9a-deterministico	CI	main	push	30055699560	52s	2026-07-24T00:16:08Z
```

**Mappatura commit→run OBBLIGATORIA** (2 push separati in questa sessione):

- Push 1 (`git push -u origin chore/hardening-processo`) ha incluso `1551312`, `fd07a6d`, `81933c9`, `6f5ba71` → **UNA sola run**: `30078697173`, `headSha = 6f5ba71...` (verificato con `gh run view 30078697173 --json headSha`), conclusion `success`.
  - `1551312`: **nessuna run propria** — coperto solo indirettamente perché il suo contenuto è incluso nell'albero testato al push (`6f5ba71`). Copertura sostanziale, non letterale.
  - `fd07a6d`: **nessuna run propria**, stesso motivo.
  - `81933c9`: **nessuna run propria**, stesso motivo.
  - `6f5ba71`: run propria `30078697173` ✅ SUCCESS (headSha combacia esattamente).
- Push 2 (report) ha incluso `4fd0d31` → run propria `30078926449`, `headSha = 4fd0d31...` (verificato), conclusion `success`.

Nessuna formula collettiva "tutti i commit hanno CI verde" — mappatura per singolo SHA come da nuova regola introdotta in questa stessa sessione (`.claude/commands/fine-task.md` §6, commit `6f5ba71`).

---

## §7 RISERVE APERTE

- **🟡 R-gasmerge-failopen** (aperto in `stato_progetto.md` in fetta 5, verdetto #61 APPROVATO CON RISERVE + rilievi operatore):
  1. `scripts/gasmerge.sh:70-71` — `git diff --name-only ... | grep -E ... || true` sotto `pipefail`: un errore REALE di `git diff` (rc≥2, es. ref stantio) viene confuso con "nessun match" (rc=1), il rilevamento file-motore fallisce silenziosamente in fail-open.
  2. `scripts/gasmerge.sh:64-67` — stesso pattern sull'invariante IP (`git grep` in condizione `if` sotto `set -e`): un errore reale del comando produce lo stesso esito di "0 match", nessun blocco. Guardrail di sicurezza in fail-open: il più grave dei tre.
  3. `scripts/gasmerge.sh:16` vs `64,70-71` — `git fetch` unico prima di un'attesa CI fino a 900s: i controlli successivi possono leggere refs stantii se il branch della PR cambia durante l'attesa, mentre il merge finale prende lo stato attuale.
  4. [rilievo operatore] `scripts/gasmerge.sh:14` — `command -v jq` (presence check) invece del functional check `jq --version` già stabilito con R-hook-jq/review #56: un jq presente ma rotto passa il gate.
  5. [rilievo operatore] `scripts/gasmerge.sh:64` — invariante IP limitata a `reports/`: un IP in CLAUDE.md/scripts/.claude/codice non viene bloccato, mentre lo scrub 2026-07-20 riguardava tutto HEAD.
  Stato: NON chiuso, fix rimandato a sessione dedicata.
- **🟡 R-verdetto-evidenza** (introdotto sessione precedente, `stato_progetto.md`): l'obbligo di citare ≥2 elementi del diff nel verdetto è verificabile solo a occhio; un verdetto può citare `path:riga` plausibili senza averli letti. Fix strutturale (check meccanico) non impegnato.
- **Deviazione di gate — subagent `revisore` non registrato nell'harness** (registrata in `stato_progetto.md` in fetta 5): cwd di lancio sessione `/home/gqual` invece di `~/Gas` → `.claude/agents/` non scoperto. Review #60/#61 prodotte da `general-purpose` in ruolo. Merito verificato a campione dall'operatore in questa fetta (citazioni path:riga corrispondenti al codice reale, difetto #60 riprodotto con `git stash`): **accettate come valide, non ri-revisionate**. Regola ribadita: lanciare sempre `cd ~/Gas && claude`.
