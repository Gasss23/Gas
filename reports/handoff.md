# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Promemoria di gasmerge dal perimetro, ref completi (anche gate IP), .gitignore audio, branch `fix/gasmerge-perimetro-gitignore`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #122 (https://github.com/Gasss23/Gas/pull/122), dopo la verifica esterna di questo handoff. Variante A: l'agente lancia `gasmerge 122`, l'operatore conferma digitando `122`.
2. R-147-1 (MEDIA, preesistente): un branch o un path che contiene `gasmerge-ip-ok` aggira il gate IP. Correggerlo in una micro-fetta PRIMA della V-B vera? (consigliato: sì)
3. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? Oggi la difesa sono i ref completi negli script.
4. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
5. Prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **V-1 verifica #121 — gasmerge legge il perimetro di review**: `FATTA`.
- **R-144-1 — ref abbreviati**: `FATTA` in due tempi. Dichiarata chiusa in `03e01f8`, ma la verifica esterna #122 (V-1/V-2) ha trovato il ref abbreviato nel gate IP (`gasmerge.sh:91`) e in `check_landing.sh:33`; chiusa davvero in `27f04b7` (review #147).
- **V-2 verifica #121 — .gitignore audio e output dei client**: `FATTA`.
- **R-145-1 / R-145-2**: `FATTA` (stessa fetta, review #146).
- **Correzioni stato_progetto (R-143-4 PARZIALE, R-143-1 chiusa dopo il merge di #121)**: `FATTA`.
- **Tracciamento V-3 / V-5 (verifica #121) e R-147-1/2/3**: `FATTA` (aperte).
- **R-147-1 — allowlist IP sul prefisso di git grep**: `DEFERITA — preesistente, tocca anche fine_task_finale.sh; decisione operatore (§0.2)`.
- **V-B vera**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 .claude/commands/fine-task.md      |   2 +-
 .claude/hooks/promemoria_end.sh    |   2 +-
 .gitignore                         |   9 +++++++++
 reports/diff_sessione.md           |  21 ++++++++++-----------
 reports/handoff.md                 | 354 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  43 +++++++++++++++++++++++++------------------
 scripts/check_landing.sh           |   2 +-
 scripts/gasmerge.sh                |  58 +++++++++++++++++++++++++++++++++++++++++-----------------
 tests/test_unit_gasmerge.py        | 127 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_hooks.py           |  22 ++++++++++++++++++++++
 12 files changed, 439 insertions(+), 213 deletions(-)
```

NB: i conteggi di righe sono quelli dello stage PRIMA di riempire §2/§3/§6 (handoff.md conta se stesso): il set di file è esatto, i conteggi no (verifica esterna #122, V-3 cosmetica).

## §3 GIT LOG --ONELINE (sessione)

```
27f04b7 fix(gasmerge): ref completo nel gate IP e in check_landing — verifica esterna #122 V-1/V-2, review #147 APPROVATO CON RISERVE
6cbfe39 chore(revisore): memoria review #147 — APPROVATO CON RISERVE
4e598e2 docs(gasmerge-perimetro): fine-task — promemoria dal perimetro, ref completi, .gitignore audio, handoff (review #145/#146)
03e01f8 fix(gasmerge): promemoria dal perimetro di review, ref completi, .gitignore audio — review #145/#146 APPROVATO CON RISERVE
2ffa88c chore(revisore): memoria review #146 — APPROVATO CON RISERVE
30ba09f chore(revisore): memoria review #145 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `03e01f8`: la #145 sul diff iniziale e la #146 sul delta che chiude R-145-1 e R-145-2. Commit `27f04b7`: la #147. Tutte incollate per intero.

### Review 145

## VERDETTO: APPROVATO CON RISERVE

**Letture preliminari fatte:** CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (solo le voci R-144-1, R-143-4, V-1 e V-2) e .claude/agents/memoria_revisore.md (contatori #137–#144 e lezioni del 2026-10). Il Wall of Shame non c'entra con questo diff: non tocca codice Python del motore, né history né tool. Guardrail del motore (cap a 10 iterazioni, `_get_window`, cap sull'output) non toccati.

**Riproduzioni**
- test_unit_hooks + test_unit_gasmerge + test_unit_gate: **168 passed**, numero confermato.
- Controprova sul gasmerge.sh di `refs/remotes/origin/main`: `-k TestPerimetroPromemoria` dà **3 failed, 1 passed**. Il test doc-only passa per costruzione, come dichiarato.

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:153` — costruisce PERIM_VOCI come unione del perimetro di main, del perimetro del branch e delle voci `scripts/` e `.claude/`; poi toglie commenti e spazi, scarta le righe vuote e ordina con `sort -u`. Rischio esaminato: con `set -euo pipefail` (riga 2) un `grep -v` senza output darebbe rc 1 e farebbe uscire lo script. Non succede: il `printf` garantisce sempre almeno 2 righe, e i `git show … || true` dentro il gruppo neutralizzano il ref mancante — **ok**.
- `scripts/gasmerge.sh:162` — doppio ciclo: una voce che finisce con `/` vale come prefisso, le altre come path esatto, e `"$v"` è quotato quindi niente glob. Se il perimetro è illeggibile su tutti e due i lati (PERIM_LETTO=0, righe 157-160), ogni file conta come motore. Rischio esaminato: falsi "doc-only". Sonde: tag `origin/main` puntato sul branch → promemoria corretto (P3); cancellazione di `gas_identity.md` → promemoria corretto (P4) — **ok**.
- `scripts/gasmerge.sh:141` — `git diff --name-only` senza `--no-renames` e senza `core.quotePath=false`. Rischio: un file del perimetro rinominato o con nome non-ASCII sparisce dal confronto (lezione del 2026-10-04 in memoria). Le sonde lo confermano. **P1**: `git mv gas_identity.md docs/x.md` → "nessuno (doc-only)". **P2**: `clients/caffè.py` → "nessuno (doc-only)". Il problema c'era già con la vecchia regex, quindi non è una regressione; e lo script è un promemoria, non un gate (hook e check_handoff usano già `--no-renames -z`) — **riserva R-145-1**.
- `.claude/hooks/promemoria_end.sh:45` — merge-base con il ref completo `refs/remotes/origin/main`. Rischio: rottura del ramo di fallback. È invariato: WARN nel log ed exit 0 — **ok**.
- `.claude/commands/fine-task.md:21` — solo il testo del messaggio d'errore, allineato al ref completo. È la riserva estetica della #144, chiusa — **ok**.
- `.gitignore:41` — `clients/**/*_output.*`. Rischio: il pattern prende anche i sorgenti. `git check-ignore -v --no-index` conferma che `clients/voice/tts_output.py` verrebbe ignorato. L'hook (`--untracked-files=all`) non vede i file ignorati, quindi un sorgente con quel nome sparirebbe senza avviso: non arriverebbe mai alla review né al repo. Nessun file tracciato è colpito oggi: l'unico `*_output.*` tracciato è `reports/e2e_k3bis_output.txt`, fuori da `clients/` — **riserva R-145-2**.
- `tests/test_unit_gasmerge.py:337` — la fixture `_repo` costruisce un bare repo reale con perimetro opzionale su main e sul branch. I 4 test coprono: voce esatta, prefisso con quasi-omonimo `clientsX.md`, branch che restringe il perimetro, perimetro assente. Le asserzioni sono specifiche ("PERIMETRO DI REVIEW", "illeggibile", assenza di "doc-only") — **ok**.

**Riserve**
- **R-145-1** (media, c'era già prima di questa fetta). Fix verificato su una copia: `ENGINE_DIFF=$(git -c core.quotePath=false diff --no-renames --name-only "refs/remotes/origin/main...refs/remotes/origin/$BRANCH")`. Con questa modifica P1 e P2 elencano correttamente `gas_identity.md` e `clients/caffè.py`. Fa però fallire `test_git_diff_name_only_error_blocks`, perché lo stub `_make_stub_git_diff_name_only_fail` (tests/test_unit_gasmerge.py:119) controlla `$1 = diff`, e con `-c` davanti `$1` cambia. Va adeguato anche lo stub. Consiglio di chiuderla in questa stessa fetta: costa due flag e un test.
- **R-145-2** (minore). Restringere `.gitignore:41` alle estensioni degli artefatti (es. `clients/**/*_output.wav`, `.mp3`, `.txt`, `.json`), oppure chiarire nel commento che i sorgenti `*_output.py` vanno aggiunti con `-f`. Nota a margine: `*.wav` globale ignorerebbe anche futuri fixture audio in `tests/`.

**Rischi esplicitamente esclusi**
- Esecuzione reale di `gasmerge` contro GitHub (gh vero, PR reale): non riprodotta. Uso solo gli stub gh dei test e i bare repo locali, perché lanciare lo script vero farebbe un fetch e un merge sul repo di produzione.
- Nomi di file contenenti un a-capo: non provati. Il ciclo `read -r` riga per riga non li gestirebbe; è un caso marginale per un promemoria.
- Comportamento con il perimetro presente ma vuoto (solo commenti) su main: non sondato. Restano attive solo `scripts/` e `.claude/`, scelta coerente con la "fonte unica".

**Memoria:** riga #145 e una lezione nuova aggiunte e salvate nel repo con lo script dedicato: commit `30ba09f` su `/Users/gas/Gas/.claude/agents/memoria_revisore.md`.

**File rilevanti**
- `/Users/gas/Gas/scripts/gasmerge.sh`
- `/Users/gas/Gas/.gitignore`
- `/Users/gas/Gas/tests/test_unit_gasmerge.py`
- `/Users/gas/Gas/.claude/hooks/promemoria_end.sh`
- `/Users/gas/Gas/.claude/commands/fine-task.md`
- Sonda: `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/sonda.py`

### Review 146

## VERDETTO: APPROVATO CON RISERVE

Review #146 sul diff staged aggiornato del branch `fix/gasmerge-perimetro-gitignore`. R-145-1 e R-145-2 sono chiuse. Restano solo due riserve di poco conto, che non bloccano il commit.

**Esiti rifatti da me**
- `test_unit_gasmerge` + `test_unit_hooks` + `test_unit_gate`: **170 passed**, coincide con il vostro 26 + 144.
- Stessi test contro il `gasmerge.sh` di `refs/remotes/origin/main`, con `-k "Perimetro or DiffGuard"`: **5 failed, 2 passed**, come dichiarato. Passano il test doc-only e DiffGuard, ed è atteso.
- Ho tolto un solo flag alla volta:
  - senza `--no-renames` fallisce solo `test_rename_fuori_perimetro_resta_motore`;
  - senza `core.quotePath=false` fallisce solo `test_nome_non_ascii_nel_perimetro`.
  Ogni flag ha quindi un test suo che fallisce se lo si toglie.
- Ho rilanciato le sonde della #145 sul diff nuovo:
  - P1 (rename `gas_identity.md` → `docs/x.md`): ora mostra `gas_identity.md`;
  - P2 (`clients/caffè.py`): ora mostra il nome in chiaro, non quotato;
  - P3 (tag `origin/main` che punta al branch) e P4 (cancellazione): promemoria corretto.

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:144` — `git -c core.quotePath=false diff --no-renames --name-only "refs/remotes/origin/main...refs/remotes/origin/$BRANCH"`. Rischio esaminato: un file del perimetro rinominato verso fuori, o con nome non-ASCII, che sparisce dal promemoria. Ora compare anche il vecchio path e i nomi non sono più tra virgolette. Il ramo d'errore `DIFF_RC` è invariato — **ok**.
- `tests/test_unit_gasmerge.py:119` — lo stub riconosce `diff` in qualunque posizione (`grep -qx 'diff'`) insieme a `--name-only`. Rischio esaminato: uno stub che non intercetta più la chiamata e lascia passare il test del ramo d'errore senza verificarlo davvero. `test_git_diff_name_only_error_blocks` resta verde, quindi lo stub intercetta il `git -c … diff`. `git diff --stat` (riga 42) e `git show` non lo attivano — **ok**.
- `tests/test_unit_gasmerge.py:395` — rename test: `gas_identity.md` (20 righe identiche) viene committato su main, il branch lo integra e poi fa `git mv` puro. Rischio: che git non riconosca il rename e il test passi anche senza il fix. La copia è identica al 100%, quindi il rename scatta, e la mutation qui sopra lo conferma — **ok**.
- `tests/test_unit_gasmerge.py:412` — `clients/caffè.py` con perimetro `clients/`. Rischio: differenze NFC/NFD tra macOS e Linux. In locale passa; il comportamento in CI Linux è indicato tra i rischi non verificati — **ok**.
- `.gitignore:41` — ora `clients/**/*_output.{wav,mp3,txt,json}`, su righe separate. Rischio: sorgenti ignorati senza che l'hook se ne accorga. `git check-ignore -v --no-index`: `clients/voice/tts_output.py` **non** è più ignorato; `a_output.wav`, `a_output.json` e `c_output.txt` (anche annidato) sì — **ok**.

**Riserve (di poco conto)**
- Cosmetica: le righe `clients/**/*_output.wav` e `*_output.mp3` non servono, perché `*.wav` e `*.mp3` sono già ignorati ovunque.
- Dichiarata: `*.wav` ignorato in tutto il repo è una scelta dell'operatore (V-2). Eventuali file audio di prova futuri in `tests/` andranno aggiunti con `git add -f`.

**Rischi esplicitamente esclusi**
- Non ho eseguito il test non-ASCII su Linux, dove gira la CI. Sono in dev su macOS con `precomposeunicode`. Python scrive NFC e git su Linux restituisce i byte tali e quali, quindi mi aspetto che passi, ma lo confermerà la run `unit-suite`.
- Non ho eseguito `gasmerge` reale contro GitHub, per lo stesso motivo della #145: farebbe fetch e merge sul repo di produzione.
- Non ho provato nomi di file che contengono un a-capo: il ciclo che li legge va riga per riga e non li gestirebbe. È un caso marginale per un promemoria.

**Memoria:** ho aggiunto la riga #146, senza lezioni nuove, in `/Users/gas/Gas/.claude/agents/memoria_revisore.md` e l'ho committata (`2ffa88c`). La riga #145 era già in `30ba09f`.

**File rilevanti**
- `/Users/gas/Gas/scripts/gasmerge.sh`
- `/Users/gas/Gas/tests/test_unit_gasmerge.py`
- `/Users/gas/Gas/.gitignore`
- `/Users/gas/Gas/.claude/hooks/promemoria_end.sh`
- `/Users/gas/Gas/.claude/commands/fine-task.md`

### Review 147 (commit `27f04b7`, dopo la verifica esterna #122)

## VERDETTO: APPROVATO CON RISERVE

Review #147: diff staged di fix/gasmerge-perimetro-gitignore (PR #122), 4 file, +54/−2. Letture obbligatorie fatte: CLAUDE.md §5/§8/§10, stato_progetto.md (lettura selettiva) e memoria_revisore.md (#141–#146).

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:91`: il gate IP ora esegue `git grep` su `refs/remotes/origin/$BRANCH`. Ho verificato il rischio di un tag omonimo `origin/<branch>` che dirotta la scansione su un albero pulito. Esito **ok**. Controprova: con il gasmerge.sh di HEAD, `TestIPRefCompleto` fallisce; con il fix passa.
- `scripts/check_landing.sh:33`: ora fa `rev-parse "refs/remotes/origin/${BRANCH}"`. Ho verificato il rischio di un tag `origin/main` su un HEAD non pushato che maschera il Check B. Esito **ok**. Controprova: con il check_landing.sh di HEAD, `test_land_tag_omonimo_non_maschera_head_non_pushato` fallisce.
- `tests/test_unit_gasmerge.py:418` (`test_tag_origin_main_non_dirotta_il_promemoria`): l'obiettivo è uccidere la mutation sulla riga 144. Ho riportato a mano la riga 144 a `"origin/main...origin/$BRANCH"` e il test fallisce. Esito **ok**.
- `tests/test_unit_gasmerge.py:433` (`TestIPRefCompleto`): ho verificato il rischio di autoblocco del gate IP sul sorgente del test. Il marker `# gasmerge-ip-ok` sta sulla riga Python, mentre il file scritto nel repo temporaneo resta senza marker, quindi il test resta discriminante. Esito **ok**.
- `tests/test_unit_hooks.py:1476`: il test asserisce solo `returncode == 1`, senza il messaggio `[B]`. Ho verificato se fosse comunque discriminante: lo è, perché con lo script di HEAD fallisce. Esito **ok**.
- Contesto, `scripts/gasmerge.sh:114`: il filtro `grep -v 'gasmerge-ip-ok'` lavora sulla riga intera di `git grep`, prefisso `<ref>:<path>:` compreso. Esito **riserva** (R-147-1).

**Sonda sui ref abbreviati nel perimetro (richiesta esplicita)**
Ho cercato con grep `origin/`, `rev-parse`, `merge-base`, `git diff|log|show|grep|cat-file`, `@{u}` e i ref costruiti da variabili in scripts/, .claude/hooks/, .github/workflows/ e .claude/commands/fine-task.md. Nessun `origin/...` abbreviato viene ancora usato per risolvere un ref: restano solo commenti e messaggi (fine-task.md:12-27, promemoria_end.sh:46, session_end.sh:11, ci.yml:223-233, check_landing.sh:31/36/39). Tutte le risoluzioni usano `refs/remotes/origin/...`, `HEAD`, `@{u}` o `${BASE}`. Esito **ok**.

**Test**
- pytest senza kernel e senza e2e: **284 passed**, riprodotto.
- Script ripristinati dopo le mutation, verificato con `cmp`.

**Riserve**
- **R-147-1 (MEDIA, preesistente, non è una regressione).** Il filtro allowlist `scripts/gasmerge.sh:114` agisce anche sul prefisso `<ref>:<path>:` stampato da `git grep <tree>`. Il prefisso l'ho verificato a HEAD (`refs/remotes/origin/fix/gasmerge-perimetro-gitignore:clients/voice/...`). Ne segue che basta un branch come `fix/gasmerge-ip-ok`, o un file il cui path contiene `gasmerge-ip-ok`, perché ogni IP risulti allowlistato e il gate IP sia aggirato. Il caso del branch è dimostrato sul formato dell'output, non con un repo di prova (vedi sotto). Fix proposto: filtrare dentro `git grep` sul solo contenuto, cioè `-e <IP> --and --not -e gasmerge-ip-ok`, più un test con un branch dal nome "avvelenato".
- **R-147-2 (minore).** Due mutation sopravvivono. Il ref abbreviato riportato a `gasmerge.sh:42` (diff --stat, solo visualizzazione) lascia verdi 28 test su 28. Lo stesso vale per `gasmerge.sh:156/:161` (il perimetro letto da main): un tag `origin/main` lì oggi non avrebbe un test che lo rileva.
- **R-147-3 (minore).** `tests/test_unit_gasmerge.py` non gira in `.github/workflows/ci.yml`, come test_unit_gate.py (R-gate-3). I nuovi test proteggono quindi solo in locale.
- **Cosmetica.** In `check_landing.sh:33` manca `--verify -q`. Con un ref assente, `rev-parse` stampa il nome stesso: verificato, `REMOTE_HEAD` diventa `[refs/remotes/origin/inesistente-xyz]`. Si finisce nel ramo "!=" invece che in "non esiste". Resta fail-closed (exit 1), ma il messaggio è sbagliato. Preesistente.

**Rischi esplicitamente esclusi**
- La sonda end-to-end su un repo temporaneo con branch `fix/gasmerge-ip-ok` non l'ho eseguita. Il hook `review_gate.sh` blocca qualunque comando Bash che contiene un commit, anche fuori dal progetto, e non l'ho aggirato. R-147-1 è dimostrata solo sul formato reale dell'output di `git grep` più il filtro `grep -v`.
- Non ho verificato il comportamento sulla CI GitHub reale né su una VPS Linux: ho eseguito solo su macOS in locale.
- Suite kernel non eseguita: il diff non tocca il motore. Per questo il round-trip agentico di §7 non si applica.

**Memoria**
- Aggiunta la riga #147 in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, con 2 lezioni:
  - chiudere una classe di finding richiede un grep su tutte le risoluzioni di ref, più una mutation per ogni riga (le review #144-#146 avevano mancato `gasmerge.sh:91`);
  - un marker di allowlist cercato sull'output di `git grep <tree>` matcha anche il prefisso `<ref>:<path>`.
- Commit atomico `6cbfe39` (`chore(revisore): memoria review #147`). L'index del diff sotto review è intatto: 4 file staged.

Tu ora: le riserve R-147-1/2/3 vanno tracciate in `/Users/gas/Gas/reports/stato_progetto.md`. Il marcatore `.review_ok` va rigenerato con `bash scripts/segna_review_ok.sh` prima del commit.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/. Modifiche a tests/ (`tests/test_unit_gasmerge.py`, `tests/test_unit_hooks.py`):
- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 275 → **284 passed** (+7 `TestPerimetroPromemoria`, +1 `TestIPRefCompleto`, +1 check_landing con tag).
- Riepilogo reale: `284 passed in 66.85s (0:01:06)`.
- Controprove: col gasmerge.sh di main, `-k "Perimetro or DiffGuard"` → `5 failed, 2 passed`; col gasmerge.sh di `4e598e2`, `-k tag` → `1 failed, 1 passed` (gate IP); col check_landing.sh di `4e598e2` → `1 failed`; riga 144 riportata a `origin/main...origin/$BRANCH` → `1 failed, 1 passed`.
- Kernel non rilanciato: non toccato.

## §6 STATO CI

```
completed	success	docs(gasmerge-perimetro): fine-task — promemoria dal perimetro, ref c…	CI	fix/gasmerge-perimetro-gitignore	push	37210222546	1m13s	2026-10-04T14:41:56Z
completed	failure	fix(gasmerge): promemoria dal perimetro di review, ref completi, .git…	CI	fix/gasmerge-perimetro-gitignore	push	37210021530	1m3s	2026-10-04T14:38:46Z
completed	success	Merge pull request #121 from Gasss23/fix/gate-rename-perimetro-ci	CI	main	push	37206707321	1m4s	2026-10-04T13:44:41Z
completed	success	docs(gate-rename): fine-task — correzione §6 (mappatura commit→run re…	CI	fix/gate-rename-perimetro-ci	push	37206249513	1m13s	2026-10-04T13:37:00Z
```

Mappatura commit→run:
- `30ba09f`, `2ffa88c` (memoria #145/#146): nessuna run su questi SHA (pushati insieme a `03e01f8`).
- `03e01f8` (fix): run `37210021530` — `unit-suite: success`, `handoff-check: failure` (`check_handoff: ERRORE — la sessione tocca il perimetro di review ma reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).`): atteso, l'handoff arrivava col commit successivo.
- `4e598e2` (primo fine-task): run `37210222546` — success (unit-suite e handoff-check pass, confermato dalla verifica esterna).
- `6cbfe39` (memoria #147): nessuna run su questo SHA (sarà pushato insieme a `27f04b7` e al fine-task).
- `27f04b7` (fix gate IP / check_landing): nessuna run su questo SHA (stesso push del fine-task, la run testa solo il commit di testa).
- Commit di fine-task (che contiene questo file): run non ancora disponibile alla scrittura dell'handoff. La copertura pre-merge resta a `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

- **R-147-1 (MEDIA, preesistente)**: allowlist `gasmerge-ip-ok` applicata anche al prefisso `<ref>:<path>:` di `git grep` (gasmerge.sh e gate IP di fine_task_finale.sh) → decisione §0.2.
- **R-147-2 (minore)**: mutation sopravvissute su `gasmerge.sh:42` e sul perimetro letto da main.
- **R-147-3 (minore)**: `tests/test_unit_gasmerge.py` non gira in ci.yml.
- Cosmetica #147: `check_landing.sh:33` senza `--verify -q` (messaggio sbagliato, resta fail-closed).
- Minori #146: righe `clients/**/*_output.{wav,mp3}` ridondanti; fixture audio in tests/ con `git add -f`.
- V-3 / V-5 verifica #121: aperte, decisione operatore (§0.3, §0.4).
- R-143-2 (ci.yml dalla PR) e R-143-3 (stallo con falso blocco su main): invariate, R-143-2 → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #122 (handoff `4e598e2`)

Unica aggiunta al testo: il marker `# gasmerge-ip-ok` sulla riga con l'IP di esempio, richiesto dal gate IP su reports/.

VERIFICA ESTERNA PR #122 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad a 4e598e2f7291d8bf307603620e14aaf8e5ec7954, più un secondo clone al merge-base b7421fd. Ho riletto il diff completo da base a HEAD, con il venv esistente del repo come interprete (Python 3.14). Ho rilanciato le suite, fatto controprove contro il gasmerge.sh di main e mutation singole, interrogato l'API GitHub e scritto una sonda su un repo git reale con bare remote e stub gh (probe_ip.py, nella scratchpad). Il repo reale non è stato toccato: `git status` mostra solo .agents/, .codex/ e AGENTS.md, già non tracciati prima dell'inizio.

CLAIM VERIFICATI
- §2/§3 contro git reale: VERO, con scarto cosmetico. I 10 file e i 4 commit corrispondono al merge-base b7421fd. Lo --stat dell'handoff dà 274+/219- contro i 292+/215- reali, perché non conta il commit di fine-task 4e598e2 che contiene l'handoff stesso. Il §3 lo dichiara; il §2 no.
- Test 275 -> 281: VERO. Base b7421fd: 275 passed. HEAD: 281 passed in 66.36s. Le tre suite hooks, gasmerge e gate: 170 passed, come dichiarato dalla review #146.
- Controprova "5 failed, 2 passed": VERO. Con il gasmerge.sh di b7421fd sotto i test nuovi, `-k "Perimetro or DiffGuard"` dà 5 failed, 2 passed. Il test doc-only e DiffGuard passano per costruzione.
- R-145-1 chiusa: VERO. Togliendo un flag alla volta, senza --no-renames fallisce solo test_rename_fuori_perimetro_resta_motore; senza core.quotePath=false fallisce solo test_nome_non_ascii_nel_perimetro.
- V-1 (verifica #121) chiusa, promemoria dal perimetro: VERO. gas_identity.md, clients/ e le altre voci non coperte dalla vecchia regex ora compaiono. Un branch che restringe il perimetro non si declassa da solo: contano le voci di main più quelle del branch.
- R-145-2 chiusa: VERO. Con file creati in clients/voice/sub/, tts_output.py e x_output.md risultano visibili come "??". *_output.{wav,mp3,txt,json} e x.wav sono ignorati. Nessun file tracciato è colpito da `git ls-files -ci --exclude-standard`.
- CI sullo SHA 4e598e2: VERO. Run 37210222546: unit-suite pass (1m4s) e handoff-check pass. Il test non-ASCII, che il revisore non aveva potuto provare su Linux, passa in CI.
- Run 37210021530 su 03e01f8 rossa per handoff-check: VERO. handoff-check fallita su quel run, come scritto nel §6. Non ho riletto il testo dell'errore dal log.
- Check required nel ruleset main-lock: VERO. Sono unit-suite e handoff-check, con 0 approvazioni richieste, nessun bypass actor e policy strict. Il ruleset non ha regole sui tag: è il V-3 già dichiarato nell'handoff, confermato.
- "R-144-1 CHIUSA, ref completi in gasmerge.sh": FALSO. Vedi V-1.

FINDING
- V-1 (MEDIA) — il ref abbreviato resta in scripts/gasmerge.sh:91, nel gate IP.
  - Lì c'è ancora `git grep -nE '<regex IP>' "origin/$BRANCH"`. Se esiste un tag `origin/<branch>`, git lo risolve prima del remote-tracking ref (refs/tags/ vince su refs/remotes/), e il gate scansiona l'albero sbagliato.
  - Sonda probe_ip.py: il branch feat contiene HOST="8.8.8.8".  # gasmerge-ip-ok
    - Senza tag, l'invariante dà "BLOCCO: trovati IP non allowlistati... origin/feat:x.py:1".
    - Con un tag origin/feat che punta a main, pushato sul bare e riscaricato da `git fetch --prune origin`, dà "0 IP trovati — OK", con il warning "refname 'origin/feat' is ambiguous". Bypass dell'invariante IP.
  - È la stessa classe di R-143-1 e R-144-1, che stato_progetto e handoff dichiarano chiuse. Il PR tocca le righe 42 e 141 ma non la 91.
  - Perché nessuno se ne è accorto: una mutation che riporta a `origin/main...origin/$BRANCH` il diff della riga 144 lascia verdi tutti i 26 test di gasmerge. Nessun test copre la tesi "ref completi".
  - Fix: "refs/remotes/origin/$BRANCH" alla riga 91, più un test con un tag omonimo che deve ancora produrre "BLOCCO". Va corretto anche stato_progetto ("R-144-1 CHIUSA").
- V-2 (BASSA) — scripts/check_landing.sh:33 usa `git rev-parse "origin/${BRANCH}"`, ancora abbreviato. Un tag omonimo può falsare il confronto HEAD locale contro origin. Il file è nel perimetro e lo stesso fix da una riga vale qui.
- V-3 (COSMETICA) — handoff §2 e §6. Lo --stat è disallineato di pochi punti rispetto al reale, come detto sopra. Il §6 dice "run non ancora disponibile" per il commit finale, ma ora è verde. Nulla di bloccante.
- V-4 (BASSA, già dichiarata e confermata) — .gitignore resta fuori dal perimetro (V-5 della #121). clients/**/*_output.txt e *_output.json possono nascondere dati legittimi con quel nome, e *.wav globale ignora anche fixture audio future in tests/.

NON VERIFICATO
- Esecuzione di gasmerge.sh contro il GitHub di produzione (PR e merge reali): non ho lanciato il merge. L'unica esecuzione dello script è quella su repo locali con stub gh della sonda. Non ho riletto l'errore di handoff-check nel log del run 37210021530.
- Nomi di file con a-capo e NFD/NFC su macOS: non provati. La CI Linux passa il test non-ASCII.
- I verdetti #145/#146 incollati nel §4: non ho modo di confrontarli con l'output originale del revisore. Sono coerenti con le righe in memoria_revisore.md, e ho riprodotto i numeri 168 e 170 dichiarati lì.

RACCOMANDAZIONE
Non fare altro lavoro prima di correggere la riga 91 di scripts/gasmerge.sh con il ref completo refs/remotes/origin/$BRANCH e di aggiungere un test con un tag omonimo. Allineare la riga 33 di scripts/check_landing.sh e stato_progetto, che ora dichiara chiusa una riserva ancora aperta. Il merge della PR #122 è accettabile solo se l'operatore accetta la riserva V-1 (nessuna perdita immediata, ma il bypass del gate IP è reale). Altrimenti correggere nello stesso branch, farlo rivedere e rilanciare la CI. Il resto del cambiamento (promemoria dal perimetro, flag --no-renames e quotePath, .gitignore) è provato e tiene.

Esito: V-1 e V-2 corretti in `27f04b7` (review #147); V-3 cosmetica superata da questo handoff; V-4 = V-5 della #121, aperta.
