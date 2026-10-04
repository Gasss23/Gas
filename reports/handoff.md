# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Gate IP: allowlist sul solo contenuto, tree unico, binari/non-UTF-8; gasmerge in CI, branch `fix/gate-ip-allowlist-ci-gasmerge`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #123 (https://github.com/Gasss23/Gas/pull/123), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 123`, l'operatore conferma digitando `123`.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? Oggi la difesa sono i ref completi negli script.
3. V-5 (verifica #121, confermata dalla #122 bis): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
4. Prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #122**: `FATTA` (operatore, main `ee95197`).
- **V-1 verifica #122 bis = R-147-1 — allowlist IP sul solo contenuto**: `FATTA` (gasmerge.sh e fine_task_finale.sh).
- **V-2 verifica #122 bis = R-147-3 — test_unit_gasmerge.py in CI**: `FATTA`; corretta l'affermazione falsa dei report di #122 ("test non-ASCII verde in CI").
- **V-3 verifica #122 bis — promemoria con `git diff -z`**: `FATTA`.
- **V-4 verifica #122 bis — stato_progetto "116 review"**: `FATTA`.
- **R-147-2 — mutation sopravvissute**: `FATTA` sul perimetro di main; `gasmerge.sh:42` (solo visualizzazione) senza test, dichiarato.
- **R-148-1 / R-148-2 / R-148-3**: `FATTA` (stessa fetta, review #149).
- **R-149-1 — 2 test gemelli per fine_task_finale.sh**: `DEFERITA — bassa, il codice è corretto; prossima occasione sul file`.
- **V-B vera**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .github/workflows/ci.yml           |  15 +++++++++++++++
 reports/diff_sessione.md           |  18 ++++++++----------
 reports/handoff.md                 | 357 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   8 +++++---
 reports/ultimo_report.md           |  45 ++++++++++++++++++++-------------------------
 scripts/fine_task_finale.sh        |  24 +++++++++++++++++++-----
 scripts/gasmerge.sh                |  33 +++++++++++++++++++++++++++------
 tests/test_unit_gasmerge.py        | 104 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_hooks.py           |  45 +++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 417 insertions(+), 237 deletions(-)
```

NB: i conteggi di righe sono quelli dello stage PRIMA di riempire §2/§3/§6 (handoff.md conta se stesso): il set di file è esatto, i conteggi no.

## §3 GIT LOG --ONELINE (sessione)

```
09d4005 fix(gate-ip): allowlist sul solo contenuto, tree unico, binari/non-UTF-8, gasmerge in CI — review #148/#149 APPROVATO CON RISERVE
5a83017 chore(revisore): memoria review #149 — APPROVATO CON RISERVE
fe005ee chore(revisore): memoria review #148 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `09d4005`: la #148 sul diff iniziale e la #149 sul delta che chiude R-148-1/2/3. Entrambe incollate per intero.

### Review 148

## VERDETTO: APPROVATO CON RISERVE

Review #148: diff staged di fix/gate-ip-allowlist-ci-gasmerge (base main ee95197, 5 file, +114/-6). Prima di cominciare ho letto CLAUDE.md (sez. 5), le righe su R-147 in reports/stato_progetto.md e la coda della memoria del revisore (lezioni #143-#147 su ref abbreviati, `| tr` che cambia l'exit code, marker cercato anche nel prefisso).

Wall of Shame: il diff non tocca la history né simula l'output dei tool. Cap delle iterazioni, `_get_window` e provider non sono toccati.

**Elementi del diff esaminati**

- `scripts/gasmerge.sh:117` — calcola UNMARKED con `git grep -nE -e <RE> --and --not -e gasmerge-ip-ok` sul ref completo; se esce con codice 0 o 1 prosegue, altrimenti BLOCCO.
  - Rischio esaminato: l'ordine di `--and --not` con -E, e se il marker venga cercato solo nel contenuto.
  - Verifica: su git 2.55 reale `--not` lega più forte di `--and` e il controllo è per riga. Branch `fix/gasmerge-ip-ok` e path `docs/gasmerge-ip-ok.py` ora danno BLOCCO. Il marker scritto in maiuscolo non allowlista (BLOCCO).
  - Esito: **ok**.
- `scripts/gasmerge.sh:125` — RESIDUAL = righe di NON_LOOPBACK uguali a una riga di UNMARKED (`grep -Fx -f <(printf ...)`).
  - Rischio esaminato: se il confronto esatto si può aggirare.
  - Sonde fatte su gasmerge.sh reale con /usr/bin/grep (BSD), tutte BLOCCO: contenuto con backslash e `\c`, tab finali, CR finale, riga marcata e riga non marcata identiche nello stesso file, stesso contenuto in due file, collisione di prefisso (file `a` riga 1 `x:5:...` contro file `a:1:x` riga 5), file chiamato `-e`, caratteri `.*[]^$`.
  - Quando UNMARKED è vuoto il pattern vuoto con -x non matcha nulla: il test che fa passare un IP marcato è verde.
  - Una riga lunga più di 64k fa uscire BSD grep con "out of memory" e codice 2: il gate blocca lo stesso (falso blocco, ma sicuro).
  - Le righe non possono sfuggire perché ognuna porta `path:numero di riga`, quindi è unica, e UNMARKED esce dallo stesso git grep con lo stesso formato. Una collisione aumenta i blocchi, non li riduce.
  - Esito: **ok**, con riserva R-148-2.
- `scripts/fine_task_finale.sh:91` e `:99` — stessa logica di gasmerge su HEAD, con STOP se il codice è 2 o più.
  - Controprova: con la versione di main il test `finale_4` dà 1 failed (riprodotto). Ho rimesso il file com'era copiando il backup: diff contro l'index vuoto, bit di esecuzione conservato.
  - Esito: **ok**, con riserva R-148-1.
- `scripts/gasmerge.sh:158` — `git diff -z ... | tr '\0' '\n'`.
  - Rischio esaminato (lezione #139): che `$?` restituisca l'exit code di `tr`.
  - Verifica: `set -euo pipefail` è attivo dalla riga 2. La mutation `set +o pipefail` fa fallire 1 test, la mutation senza `-z` fa fallire `test_nome_con_apice_nel_perimetro`.
  - Esito: **ok**.
- `.github/workflows/ci.yml:117` — nuovo step `if: always()` con `pipefail` e `tee`, più la riga nel job summary (`:172`).
  - Rischio esaminato: dipendenze su ubuntu e configurazione git dei test.
  - Verifica: jq e GNU `timeout` sono di serie su ubuntu-latest. I test impostano user.email e user.name per ogni repo e fissano il branch iniziale con `symbolic-ref`, senza dipendere dal git globale. gh è uno stub, quindi nessuna rete. Su GNU grep `-x ''` matcha solo righe vuote. Il fallimento dello step fa diventare rosso il job.
  - Esito: **ok**. Non l'ho visto girare, vedi i rischi esclusi.
- `tests/test_unit_gasmerge.py:473` (TestIPAllowlistSoloContenuto), `:427`, `:434`; `tests/test_unit_hooks.py:1985`.
  - Controprove riprodotte: col gasmerge.sh di main, 3 failed (due avvelenati e apice).
  - Mutation su gasmerge.sh:170 (`origin/main:` abbreviato): 1 failed (test sul tag).
  - Mutation "torna a `grep -v`": 2 failed. Mutation `-Fx` → `-F`: 2 failed.
  - La stessa mutation su `:175` (cat-file) non fa fallire nulla, ma è equivalente in pratica: decide solo PERIM_LETTO, e nel caso peggiore conta più file come motore.
  - Esito: **ok**.
- pytest senza kernel ed e2e: **289 passed** (riprodotto). Suite gasmerge 32/32, test `finale` in hooks 8/8.

**Riserve (da tracciare in stato_progetto.md)**

- **R-148-1 (bassa)**: il ramo "codice 2 o più" del secondo git grep non ha test in nessuno dei due script. La mutation che toglie `exit 1` sopravvive (32/32 e 8/8 verdi). Se quel ramo regredisce, il gate si apre: UNMARKED vuoto porta a "Tutti gli IP sono allowlistati — OK". Serve un test con uno stub git che fallisce solo sulla chiamata con `--and`.
- **R-148-2 (bassa)**: i due git grep girano separati sullo stesso ref simbolico (`refs/remotes/origin/$BRANCH`, oppure HEAD). Un fetch concorrente tra le due chiamate (per esempio l'auto-fetch di un IDE) sposta i numeri di riga. Le righe non combaciano più con -Fx e il gate passa in silenzio, ma solo per quella esecuzione. Due correzioni possibili:
  - risolvere il tree una volta sola (`git rev-parse <ref>^{tree}`) e usarlo in entrambe le chiamate;
  - più semplice: applicare il filtro loopback direttamente a UNMARKED ed eliminare il confronto.
- **R-148-3 (media, PREESISTENTE: c'è già su main, non è una regressione di questo diff)**: il gate IP non vede due casi.
  - File binari: git grep stampa "Binary file … matches", una riga senza IP che lo Step 1 scarta. La sonda `a.bin` con NUL e 8.8.8.8 dà "Tutti gli IP sono loopback — OK", sia col branch sia con main.  # gasmerge-ip-ok
  - Righe con byte non UTF-8: la sonda latin1 dà "0 IP trovati — OK", sia col branch sia con main. Con `LC_ALL=C git grep` la riga viene trovata.
  - Correzione suggerita: `git grep -a` più `LC_ALL=C` in tutte le chiamate del gate IP (gasmerge.sh e fine_task_finale.sh), con un test per caso.
- Nota: il limite dichiarato "un prefisso con IP dà un falso blocco" resta sicuro, come previsto. Le righe sopra 64k ora bloccano con "errore nel filtro" invece che con l'elenco degli IP: blocca comunque, cambia solo il messaggio.

**Rischi esplicitamente esclusi**

- **Run CI reale su ubuntu non verificata**: non posso pushare né avviare il workflow. La parte GNU grep e coreutils è solo ragionata, non eseguita (qui grep è BSD 2.6.0 e `timeout` è uno shim in ~/bin). L'agente principale deve controllare nell'handoff che lo step "Run gasmerge suite" sia verde e che la riga del summary sia popolata.
- Comportamento di GNU grep con byte non UTF-8 nel pattern file non verificato: nessun GNU grep disponibile in locale.
- `git diff --stat` a gasmerge.sh:42 (solo visualizzazione) resta senza test, come dichiarato dall'agente.
- Il nome di file con a-capo nel promemoria resta escluso (limite dichiarato).

**Memoria**: riga #148 e due lezioni nuove (gate grep provati con input binari e non UTF-8; confronto esatto tra due esecuzioni separate = TOCTOU) aggiunte in coda a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`. Committate da sole con `scripts/commit_memoria_revisore.sh` (commit `fe005ee`); il diff staged sotto review è rimasto intatto nell'index.

Sonde e mutation stanno in `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/`: `probe.py`, `sonda_main.sh`, `mutation.sh`, `controprova_finale.sh`, `longline.sh`.

### Review 149

## VERDETTO: APPROVATO CON RISERVE

Review #149 sul diff staged aggiornato (5 file, +208/-13). R-148-2 e R-148-3 sono chiuse in entrambi gli script; R-148-1 è chiusa solo in gasmerge.sh. Resta una riserva bassa su fine_task_finale.sh: due delle correzioni non hanno un test che le protegga. Protocollo seguito come per la #148 (CLAUDE.md sez. 5, stato_progetto letto in modo mirato, memoria del revisore). Il diff non introduce slicing della history né output simulati dei tool. Cap delle iterazioni, `_get_window` e provider non sono toccati.

**Elementi del diff esaminati**

- `scripts/gasmerge.sh:94` e `scripts/fine_task_finale.sh:68` — risolvono il tree una volta sola (`git rev-parse --verify -q "<ref>^{tree}"`, BLOCCO/STOP se fallisce). Le due git grep usano poi `"$IP_TREE"`.
  - Rischio: TOCTOU tra le due git grep (R-148-2), ed errore di rev-parse.
  - Il tree è fissato prima di entrambe le git grep, quindi un fetch concorrente non sposta più i numeri di riga.
  - Ho tolto `exit 1` dal ramo di errore di rev-parse (mutation G9): la mutation sopravvive, ma il gate resta chiuso. Con IP_TREE vuoto la git grep esce con codice 128, si entra nel ramo `*)` e scatta BLOCCO.
  - Il prefisso dell'output ora è lo SHA del tree. Nel messaggio cambia solo l'estetica, e branch o ref non compaiono più nel testo filtrato.
  - Esito: **ok**.
- `scripts/gasmerge.sh:124` e `:132`, `scripts/fine_task_finale.sh:96` e `:104` — `LC_ALL=C git grep -a` in tutte e quattro le git grep, `LC_ALL=C` anche su sed, `grep -qE` e `grep -Fx`.
  - Rischio: un fail-open residuo su file binari o righe non UTF-8, e falsi blocchi sul repo reale.
  - Ho fatto girare la logica nuova sul tree dell'index staged (`git write-tree`) e su origin/main: 55 e 50 match, 0 residui, rc 1. Nessun falso blocco, e nel repo non ci sono file binari.
  - I byte NUL tolti da `$(...)` spariscono allo stesso modo in NON_LOOPBACK e in UNMARKED, quindi il confronto -Fx resta coerente.
  - Esito: **ok**.
- `tests/test_unit_gasmerge.py:505` (`test_errore_della_grep_allowlist_blocca`, stub git che fallisce solo con `--and`), `:525` (TestIPFileBinariENonUtf8) e `:140` (`errors="replace"` solo in `_run`).
  - Mutation su gasmerge.sh, ognuna con 1 failed su 35:
    - G1/G2: tolgo `-a` dalla prima o dalla seconda git grep;
    - G3/G4: tolgo `LC_ALL=C` dalla prima o dalla seconda git grep;
    - G5/G6/G7: tolgo `LC_ALL=C` da sed, da `grep -qE` o da `grep -Fx`;
    - G8: tolgo `exit 1` dal ramo d'errore della allowlist.
  - Esito: **ok**.
- `tests/test_unit_hooks.py:2005` (`test_finale_4e_file_binario_con_ip`).
  - Uccide F1 e F2 (tolgo `-a` dall'una o dall'altra git grep di fine_task_finale.sh).
  - Esito: **riserva**, vedi R-149-1.
- pytest senza kernel ed e2e: **293 passed** (riprodotto). fine_task_finale.sh rimesso com'era dopo le mutation in place: diff contro l'index vuoto.

**Riserva**

- **R-149-1 (bassa)**: in `scripts/fine_task_finale.sh` sopravvivono due mutation:
  - F3: tolgo `LC_ALL=C` dalla prima git grep. Manca un test con una riga latin1 per fine_task_finale. Proprio sul Mac dell'operatore la #148 aveva visto la riga latin1 sfuggire al gate.
  - F4: tolgo `exit 1` dal ramo d'errore della allowlist. Manca il test con lo stub git che fallisce su `--and`. Se il ramo regredisce, il gate si apre.

  Quindi R-148-1 e R-148-3 sono chiuse sul codice di entrambi gli script, ma il test che le protegge esiste solo su gasmerge.sh. Bastano due test gemelli in TestFinaleScript.

**Rischi esplicitamente esclusi**

- Run CI su ubuntu non verificata, perché non posso pushare. Il comportamento di GNU grep e glibc su latin1 e NUL l'ho solo ragionato. Su Linux il test latin1 potrebbe passare anche senza `LC_ALL=C` (meno discriminante), ma resta verde. Bash 5 stampa "ignored null byte" su stderr, senza effetti.
- Non ho misurato le prestazioni di `-a` su binari grandi: oggi il repo non ne ha.

**Memoria**: riga #149 e una lezione nuova (un fix replicato su uno script gemello va coperto da mutation in entrambi i file) aggiunte in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, commit `5a83017`. L'index sotto review è rimasto intatto.

Le sonde stanno in `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/`: `mutation2.sh`, `realrepo.sh`, `realrepo_idx.sh`.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/. Modifiche a tests/ (`tests/test_unit_gasmerge.py`, `tests/test_unit_hooks.py`):
- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 284 → **293 passed**.
- Riepilogo reale: `293 passed in 73.97s (0:01:13)`.
- Controprove: col gasmerge.sh di main `-k "avvelenato or apice"` → `3 failed`; `-k Binari` → `2 failed`; col fine_task_finale.sh dello stage precedente test_finale_4d / 4e → `1 failed` ciascuno; mutation "perimetro di main abbreviato" → `1 failed`; mutation "senza exit 1 nel ramo d'errore allowlist" → `1 failed`.
- Kernel non rilanciato: non toccato.

## §6 STATO CI

```
completed	failure	fix(gate-ip): allowlist sul solo contenuto, tree unico, binari/non-UT…	CI	fix/gate-ip-allowlist-ci-gasmerge	push	37213618231	1m14s	2026-10-04T15:36:09Z
completed	success	Merge pull request #122 from Gasss23/fix/gasmerge-perimetro-gitignore	CI	main	push	37212266646	1m5s	2026-10-04T15:14:43Z
completed	success	docs(gasmerge-perimetro): fine-task bis — ref completo nel gate IP, v…	CI	fix/gasmerge-perimetro-gitignore	push	37211230456	1m13s	2026-10-04T14:58:16Z
```

Mappatura commit→run:
- `fe005ee`, `5a83017` (memoria #148/#149): nessuna run su questi SHA (pushati insieme a `09d4005`).
- `09d4005` (fix): run `37213618231` — `unit-suite: success` (step "Run gasmerge suite": `35 passed in 4.52s` su ubuntu, quindi binario, latin1 e non-ASCII verificati anche su Linux), `handoff-check: failure` (`check_handoff: ERRORE — la sessione tocca il perimetro di review ma reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).`): atteso, l'handoff arriva col commit di fine-task.
- Commit di fine-task (che contiene questo file): run non ancora disponibile alla scrittura dell'handoff. La copertura pre-merge resta a `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

- **R-149-1 (bassa)**: in `fine_task_finale.sh` sopravvivono 2 mutation (senza `LC_ALL=C` sulla prima git grep; senza `exit 1` nel ramo d'errore della allowlist): mancano 2 test gemelli di quelli di gasmerge.
- `gasmerge.sh:42` (diff --stat, solo visualizzazione) senza test sul ref completo.
- Nome di file con a-capo nel promemoria: limite dichiarato.
- V-3 / V-5 verifica #121: decisione operatore (§0.2, §0.3).
- R-143-2 (ci.yml dalla PR) e R-143-3: invariate, R-143-2 → V-B vera.

### Verdetto INTEGRALE della verifica esterna bis PR #122 (handoff `7c4a0aa`)

Unica aggiunta al testo: il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio, richiesto dal gate IP su reports/ (vale anche per i verdetti nel §4).

VERIFICA ESTERNA PR #122 (handoff pinnato 7c4a0aa) — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad, checkout di 7c4a0aac26d8d378d5390281cacab41cb3e2911e, merge-base con main b7421fd. Ho letto l'intero diff di scripts/, .claude/hooks, fine-task.md e .gitignore, più il diff di stato_progetto.md. Interprete: /Users/gas/Gas/.venv (Python 3.14.7).
Cosa ho eseguito:
- pytest (senza kernel e senza e2e) alla base e al commit.
- Controprove con gasmerge.sh preso a b7421fd e a 4e598e2, tramite GASMERGE_SCRIPT.
- Mutation singole su gasmerge.sh:144, :156/:161 e su check_landing.sh:33.
- Sonde end-to-end su repo git reali con bare remote e stub gh (probe.py nella scratchpad), sul gasmerge.sh del commit.
- API GitHub per ruleset, run e check della PR.
- Il repo reale non è stato toccato: `git status` mostra solo .agents/, .codex/ e AGENTS.md, già non tracciati prima.

CLAIM VERIFICATI
- §2 (file toccati) contro git reale: VERO sul set. Sono 12 file, tutti quelli dichiarati. I conteggi di handoff.md non tornano: lo stat dichiara 354 righe, il reale è 366 (+204/-162 secondo la PR). Il disallineamento è dichiarato nel NB del §2, quindi V-4 cosmetica.
- §3 (git log): VERO. I 6 commit elencati coincidono con quelli reali. Manca 7c4a0aa, che contiene l'handoff stesso: è dichiarato "per costruzione".
- Test 275 → 284: VERO. Alla base (b7421fd) sono 275 passed in 59.8s. Al commit sono 284 passed in 67.8s.
- Controprove "fallisce prima e passa dopo":
  - Con il gasmerge.sh di b7421fd, `-k "Perimetro or DiffGuard or IPRef or tag"` dà 7 failed, 2 passed. Passano i due che passano per costruzione (doc-only e DiffGuard).
  - Con il gasmerge.sh di 4e598e2 fallisce solo `TestIPRefCompleto` (1 failed, 27 passed). Il ref abbreviato alla riga 91 era quindi reale, e ora è chiuso.
  - Con check_landing.sh:33 riportato a `origin/${BRANCH}` fallisce solo `test_land_tag_omonimo_non_maschera_head_non_pushato`.
  - Con gasmerge.sh:144 riportato a `origin/main...origin/$BRANCH` fallisce solo `test_tag_origin_main_non_dirotta_il_promemoria`.
- R-147-2: VERO, e la mutation sul perimetro letto da main è una mutation reale. Con `origin/main` abbreviato alle righe 156 e 161 restano 28 passed su 28. Anche la riga 42 è dichiarata sopravvissuta.
- Sonda sul tag ambiguo: un tag `refs/remotes/origin/feat` creato sul main pulito dà solo un warning "ambiguous". Il gate IP scansiona comunque l'albero giusto e dà BLOCCO. Il ref completo regge.
- Nessun ref abbreviato usato per risolvere: ho cercato con grep in scripts/, .claude/hooks, ci.yml e fine-task.md. Restano solo `@{u}` (fine_task_finale.sh:125, upstream configurato), testi di messaggi e commenti. VERO.
- .gitignore (R-145-2): VERO. `clients/voice/sub/{a_output.json,b_output.txt,x.wav}` e `tests/f.wav` sono ignorati. `tts_output.py` e `c_output.md` restano visibili come `??`. `git ls-files -ci` è vuoto, quindi nessun file tracciato è colpito.
- CI sullo SHA 7c4a0aa: VERO, run 37211230456 success. unit-suite pass in 1m10s, handoff-check pass in 6s. Il §6 dice "non ancora disponibile" per il commit finale, ma ora è verde (V-4).
- Ruleset main-lock: VERO. Check required: unit-suite e handoff-check. Policy strict, 0 approvazioni, nessun bypass actor. Non c'è nessuna regola sui tag, come dichiarato in V-3 della #121.
- R-147-3 (test_unit_gasmerge.py non gira in CI): VERO, e peggio di come è presentata (vedi V-2). Il ci.yml esegue solo hooks (71 passed), voice (19), handoff_check (40), gate (74) e il runner del kernel. Nel log della run ci sono 0 occorrenze di "test_unit_gasmerge".

FINDING
- V-1 (MEDIA, già dichiarata come R-147-1: confermata, riprodotta, nessuna sopravvalutazione). Il filtro `grep -v 'gasmerge-ip-ok'` (gasmerge.sh:114) lavora anche sul prefisso `<ref>:<path>:` di `git grep`.
  - Sonda con repo reale e `gasmerge.sh` del commit, file `x.py` con `HOST="8.8.8.8"` e nessun marker nel contenuto:  # gasmerge-ip-ok
    - branch `fix/gasmerge-ip-ok` → "Tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK";
    - controllo con branch `feat` → "BLOCCO: trovati IP non allowlistati";
    - file `docs/gasmerge-ip-ok.py` con lo stesso IP, su branch `feat` → "OK".
  - Il bypass richiede solo di scegliere il nome del branch o del file, e il nome del branch lo sceglie chi apre la PR.
  - Il fix proposto funziona: `git grep -nE -e <IP> --and --not -e gasmerge-ip-ok` ha escluso la riga marcata e tenuto quella con l'IP nudo, anche con un file dal nome avvelenato. Va aggiunto un test con nome avvelenato.
  - Il gate IP duplicato in fine_task_finale.sh:90 ha la stessa debolezza sul path. Lì il ref è `HEAD`, quindi il branch non conta, ma il path sì.
  - La PR non lo aggrava e non è una regressione. Ma il merge della PR lo lascia aperto, ed è un bypass del gate disciplinare dell'IP.
- V-2 (MEDIA, nuovo) — il copertura-CI è sovrastimata e una prova ereditata è falsa.
  - Il verdetto della verifica precedente (#122 su 4e598e2), incollato integrale nel §4 dell'handoff, afferma: "il test non-ASCII, che il revisore non aveva potuto provare su Linux, passa in CI". È FALSO. Quel test sta in tests/test_unit_gasmerge.py, che la CI non esegue (nessuna occorrenza nel log, e ci.yml non lo include).
  - Di conseguenza il comportamento di gasmerge su Linux (NFC/NFD, quotePath) e tutti i 28 test di gasmerge non hanno alcuna copertura automatica. Gli 8 test nuovi di questa PR su gasmerge.sh proteggono solo la macchina locale. L'handoff non lo dice nel §6, e il §7 lo riduce a "R-147-3 minore".
  - Fix: aggiungere uno step `pytest tests/test_unit_gasmerge.py` a ci.yml. Il file è nel perimetro, quindi serve review. Rimuovere o correggere la frase falsa sul test non-ASCII in CI.
- V-3 (BASSA, nuovo) — la chiusura di R-145-1 è parziale: ci sono ancora nomi di file che sfuggono al promemoria.
  - `git diff --name-only` senza `-z`, anche con `core.quotePath=false`, quota comunque i nomi che contengono doppio apice, tab, backslash o a-capo.
  - Sonda: un file `clients/a"b.py`, o `clients/a<TAB>b.py`, o `clients/a\b.py` (un solo file nel diff, dentro `clients/`, che è nel perimetro) dà "FILE DI MOTORE: nessuno (doc-only)". Il confronto a prefisso fallisce perché il nome comincia con un doppio apice.
  - Il difetto c'era già con la vecchia regex, ma la PR dichiara la classe chiusa. È solo un promemoria: review_gate.sh e check_handoff.py usano `-z` e catturano il caso.
  - Fix: `git diff -z --name-only` con loop su NUL (`read -r -d ''`), come negli altri gate.
- V-4 (COSMETICA) — conteggi del §2 per handoff.md (354 contro 366 reali), §6 "run non ancora disponibile" ormai superato (la run 37211230456 è verde). Anche stato_progetto riga 53 dice ancora "116 review completate", ma siamo alla #147 (preesistente).
- V-5 (BASSA, già dichiarata come V-5 della #121 e confermata). .gitignore, knowledge/ e CLAUDE.md restano fuori dal perimetro. `*.wav`/`*.mp3` globali ignorano in silenzio anche fixture audio future in tests/ o clients/. `tests/f.wav` risulta ignorato dalla regola `.gitignore:39`. I file ignorati non sono visibili nemmeno all'hook.

NON VERIFICATO
- Esecuzione reale di gasmerge contro GitHub (fetch e merge veri): non lanciata, per non toccare produzione. Provato solo su repo locali con stub gh.
- Comportamento su Linux (NFC/NFD, quotePath) del test non-ASCII: nessuna esecuzione su Linux, e la CI non lo copre (V-2).
- Review #145/#146/#147 incollate nel §4: non ho l'output originale del revisore, quindi non posso confrontarle. Ho riprodotto i numeri 284 e 275, e ho controllato a mutation i test che i revisori dicono discriminanti. Non ho riesaminato i singoli passaggi.
- Esito del run 37210021530 (handoff-check rosso su 03e01f8): non ho riletto il log. Il motivo dichiarato nel §6 è plausibile.
- Nomi di file con a-capo: la sonda V-3 copre apice, tab e backslash. L'a-capo l'ho coperto solo per inferenza (stessa quotatura).

RACCOMANDAZIONE
Il merge della PR #122 è accettabile: il perimetro letto da `.claude/perimetro_review.txt`, i ref completi (anche nel gate IP e in check_landing) e il .gitignore sono provati, 284 passed riprodotti, CI verde sullo SHA e ruleset come dichiarato. Prima della V-B vera, in una micro-fetta separata:
1. chiudere V-1 (filtro dentro `git grep`, anche in fine_task_finale.sh, con test a nome avvelenato);
2. chiudere V-2 (aggiungere test_unit_gasmerge.py a ci.yml, e togliere dalla storia dell'handoff la frase che dice che il test non-ASCII passa in CI);
3. V-3 con `-z` nel promemoria.
Gli altri punti (V-4, V-5) sono cosmetici o già in decisione dell'operatore.

Esito: PR #122 mergiata (operatore); V-1, V-2, V-3 e la riga 53 di stato_progetto (V-4) chiusi in questa PR #123; V-5 resta decisione operatore.
