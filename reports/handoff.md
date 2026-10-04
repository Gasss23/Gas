# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Passata unica di mutation sul gate IP (66/66 uccise), branch `test/gate-ip-passata-mutation`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #126 (https://github.com/Gasss23/Gas/pull/126), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 126`, l'operatore conferma digitando `126`.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`?
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
4. Prossima fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub), condizione per il gasmerge completamente automatico (variante B). L'operatore dovrà inserire una chiave API nei segreti di GitHub.

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #125**: `FATTA` (operatore, main `eeaaf1b`).
- **Passata unica di mutation sul gate IP (richiesta dell'operatore)**: `FATTA` — 66/66 uccise in `gasmerge.sh` e `fine_task_finale.sh`.
- **V-1 verifica #125 — arresto del ramo "IP non allowlistati" in gasmerge**: `FATTA`.
- **V-2 verifica #125 — sed senza `g` (due loopback)**: `FATTA` in entrambi gli script.
- **R-153-1 — spazi ai bordi, backslash, loopback+IP**: `FATTA` (review #154).
- **R-153-2 — mktemp di gasmerge su BSD**: `DEFERITA — bassa, fail-closed`.
- **V-3 verifica #125 — latin1 su glibc**: `DEFERITA — job CI di mutation o V-B`.
- **Gasmerge automatico (variante B)**: `DEFERITA — richiede V-B chiusa + test di convalida (decisione operatore 2026-10-04)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 284 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  31 ++++++++++++++++---------------
 tests/test_unit_gasmerge.py        |  30 ++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  21 +++++++++++++++++++++
 7 files changed, 210 insertions(+), 176 deletions(-)
```

NB: i conteggi di righe sono quelli dello stage PRIMA di riempire §2/§3/§6 (handoff.md conta se stesso): il set di file è esatto, i conteggi no.

## §3 GIT LOG --ONELINE (sessione)

```
c2c2d3e test(gate-ip): passata unica di mutation sul gate IP (66/66 uccise) — verifica esterna #125 V-1/V-2, review #153/#154
a3ac340 chore(revisore): memoria review #154 — APPROVATO
1f29fc8 chore(revisore): memoria review #153 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `c2c2d3e` (solo test): la #153 sul diff iniziale e la #154 sul delta che chiude R-153-1. Entrambe incollate per intero.

### Review 153

## VERDETTO: APPROVATO CON RISERVE

Review #153. Ho fatto le letture obbligatorie: CLAUDE.md sez. 5/8/10 (in contesto), `reports/stato_progetto.md` letto in modo selettivo con grep, la memoria del revisore fino alla #152.

**Elementi del diff esaminati**
- `tests/test_unit_gasmerge.py:307` — aggiunge l'asserzione `"--- FILE DI MOTORE ---" not in stdout` in `test_ip_outside_reports_blocks`. Rischio esaminato: che il ramo RESIDUAL stampi BLOCCO ma non si fermi (V-1 #125, lezione #150). Esito: ok. Ho rifatto la mutation `resid_noexit` e la uccide proprio questo test.
- `tests/test_unit_gasmerge.py:780` — `test_due_loopback_sulla_stessa_riga_passa`. Rischio: un `sed` senza `g` lascerebbe passare la mutation (V-2). Esito: ok. `sed_noG` ora viene uccisa da questo test. La riga contiene solo loopback, quindi il gate IP del repo non scatta.
- `tests/test_unit_hooks.py:2109` — `test_finale_4m_due_loopback_sulla_stessa_riga`, lo stesso caso su fine_task_finale. Esito: ok. `sed_noG` (finale) viene uccisa da 4m.
- Contesto `scripts/gasmerge.sh:27` — `mktemp /tmp/gaspr.XXXXXX.json`. Rischio: collisioni fra esecuzioni concorrenti. Esito: riserva R-153-2, vedi sotto.

**Riproduzione**
- pytest su `tests/` senza `test_unit_kernel.py` ed `e2e`: 305 passed, come dichiarato.
- Sweep `mut_sweep.py` rilanciato in sequenza: gasmerge 25 uccise su 26, finale 25 su 25. Lo stesso esito che hai riportato.
- Correttezza dell'harness: ogni pattern viene controllato con `assert old in src` e c'è anche il controllo "IDENTICA". Nessuna riga "NON APPLICABILE" o "IDENTICA" nelle due passate. Alla fine `scripts/` risulta pulito.
- Unico superstite: `ipRC1_noop` (`0)` diventa `0|9999)`). È equivalente per costruzione, perché un exit code non supera mai 255: come mutation è inutile. Va sostituita con `1)` → `1|0)`, che ho eseguito io ed è uccisa in entrambi gli script.
- Attenzione: la mia prima esecuzione, in parallelo, ha dato falsi KILLED, tutti da `test_pr_not_open_blocks` per "mktemp: File exists". Lo sweep va lanciato solo in sequenza.

**Classi di mutation mancanti**
Ho scritto un harness supplementare: `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/mut_rev153.py`, 14 mutation per script.
- Uccise: asimmetria `-n` fra le due grep (in un senso e nell'altro), `-E` tolto, regex ristretta in ciascuna delle tre regex (`{1,3}` → `{3}`), coda `$` tolta dal `grep -qE`, `-Fx` → `-Fxv`, sorgente del `-f` vuota, marker cambiato nel `--not`, `1)` → `1|0)`, stampa di `$stripped` al posto di `$line` (solo gasmerge).

**R-153-1 (MEDIA, preesistente, fail-open verificato con sonde)**
Tre mutation sopravvivono e non sono equivalenti. Rompono la conservazione della riga che `-Fx` confronta con UNMARKED:
1. `while IFS= read -r line` → `while read -r line` (`scripts/gasmerge.sh:109`, `scripts/fine_task_finale.sh:83`). Un IP con spazio o tab finale passa.
2. `while IFS= read -r line` → `while IFS= read line` (stesse righe). Un backslash nella riga, anche finale, fa passare l'IP.
3. Solo in `scripts/fine_task_finale.sh:86`: `printf '%s\n' "$line"` → `"$stripped"`. Una riga mista loopback + IP passa. In gasmerge la uccide `test_mixed_loopback_and_public_blocks`, in finale manca il test gemello.

- Sonde (`test_sonde_rev153.py` + `sonde_rev153.py` nello scratchpad): sugli script originali 10/10 bloccano. Sotto mutation i casi corrispondenti escono con "tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK" e proseguono fino a "--- FILE DI MOTORE ---" o "=== Push ===".
- Fix: aggiungere test in entrambi gli script per riga con spazio o tab finale e per backslash, più il gemello della riga mista in finale. Non è una regressione di questo diff.

**R-153-2 (bassa, preesistente)**
- Su macOS, `scripts/gasmerge.sh:27` non randomizza il nome: con BSD mktemp le X non sono in coda e il file si chiama letteralmente `/tmp/gaspr.XXXXXX.json`.
- Con due gasmerge concorrenti il secondo muore con "File exists". È fail-closed.
- Fix: `mktemp /tmp/gaspr.XXXXXX`, oppure `mktemp -t gaspr`.

**Rischio escluso**
- Non ho verificato il comportamento su Linux/glibc: lì `read`, `sed` e `mktemp` differiscono, il test latin1 potrebbe non discriminare e la randomizzazione di mktemp è diversa. Non è riproducibile qui su darwin; resta da coprire con CI o V-B.
- Non ho mutato i rami fuori dal gate IP (gate A/B, push, PR state).

**Gate IP sul tree staged**: 0 righe con IP non loopback e senza marker nei due file di test.

**Memoria**: aggiunte la riga #153 e 2 lezioni (falsi kill da harness in parallelo; mutation sulla conservazione del dato confrontato con `-Fx`). Committata con `scripts/commit_memoria_revisore.sh`, commit `1f29fc8`. Il diff staged (2 file, +19) è intatto e `scripts/` è pulito.

File:
- /Users/gas/Gas/.claude/agents/memoria_revisore.md
- /private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/mut_rev153.py
- /private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/test_sonde_rev153.py
- /private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/sonde_rev153.py

### Review 154

## VERDETTO: APPROVATO

Review #154 sul diff staged aggiornato (2 file, +51, solo test). Tutto riprodotto in sequenza: R-153-1 è chiusa e i test nuovi uccidono le tre mutation che sopravvivevano nella #153. Letture obbligatorie: CLAUDE.md, `reports/stato_progetto.md` (selettiva) e la memoria del revisore fino alla #153.

**Elementi del diff esaminati**
- `tests/test_unit_gasmerge.py:790` — `test_riga_con_spazi_o_backslash_blocca`, parametrizzato su spazio finale, tab finale, spazio iniziale e backslash. Asserisce "BLOCCO: trovati IP non allowlistati" e che "--- FILE DI MOTORE ---" non compaia.
  - Rischio esaminato: `IFS=` o `-r` tolti da `read` (gasmerge.sh:109) farebbero passare l'IP.
  - Esito: ok. `read_noIFS` viene uccisa dal caso spazio, `read_noR` dal caso backslash.
- `tests/test_unit_hooks.py:2115` — `test_finale_4n_righe_difficili_bloccano`: gli stessi 4 casi più loopback e IP sulla stessa riga. Asserisce "IP trovato" e che "=== Push ===" non compaia.
  - Rischio esaminato: in `scripts/fine_task_finale.sh:86` stampare la riga ripulita al posto di quella originale renderebbe il controllo fail-open.
  - Esito: ok. `read_noIFS`, `read_noR` e `print_stripped` vengono uccise ciascuna da un caso del test.
- `tests/test_unit_gasmerge.py:307` / `:780` e `tests/test_unit_hooks.py:2109`: invariati rispetto alla #153, ok.

**Riproduzione**
- pytest su `tests/` senza `test_unit_kernel.py` ed `e2e`: 314 passed, come dichiarato.
- Il mio `mut_rev153.py`, rilanciato in sequenza: 28/28 KILLED su entrambi gli script. Alla fine `scripts/` è pulito.
- Lo sweep esteso (`sweep2.txt`, 66/66) l'ho letto ma non rieseguito. Controllato nel file dell'harness: `ipRC1_noop` è stata tolta e ci sono `ipRC1_swallow0`, `print_stripped` e `read_noIFS`. Le mutation che si sovrappongono alle mie le ho uccise anch'io in modo indipendente.
- Gate IP sul tree staged dei due file di test: 0 righe con IP non loopback e senza marker. Il marker `gasmerge-ip-ok` sta sulla riga del sorgente Python, non nel contenuto scritto nei repo di prova, quindi il gate sotto test vede comunque gli IP.

**Note cosmetiche, non bloccanti**
- Il caso "spazio iniziale" non discrimina nulla: la riga di git grep comincia sempre con `<sha>:path:n:`, quindi uno spazio a inizio contenuto non è mai a inizio riga. Non fa danni.
- Manca un caso con backslash a fine riga (continuazione di riga), ma `read_noR` viene già uccisa dal caso con backslash interno.

**Rischio escluso**
- Non ho verificato su Linux/glibc (comportamento di `read`/`sed`, test latin1): resta da coprire con CI o V-B.
- Non ho rieseguito lo sweep esteso a 66 mutation.
- R-153-2 (`mktemp /tmp/gaspr.XXXXXX.json` su BSD, `scripts/gasmerge.sh:27`) è fuori diff e resta aperta: bassa, fail-closed.

**Memoria**
- Riga #154 aggiunta, nessuna lezione nuova; committata con `scripts/commit_memoria_revisore.sh`, commit `a3ac340`. Il diff staged (2 file, +51) è intatto.
- Nota operativa: il marcatore `.claude/.review_ok` è legato al diff della #153. Per committare questo diff devi rigenerarlo con `bash scripts/segna_review_ok.sh`. Il gate ha bloccato anche il mio primo comando di memoria, perché nella stessa riga c'era "git": l'ho rilanciato da un file.

File: `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, `/private/tmp/claude-501/-Users-gas-Gas/91091029-3df7-47ca-a712-d6baf2fbda65/scratchpad/mut_rev153.py`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/ né agli script. Modifiche solo a tests/:
- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 303 → **314 passed** (`314 passed in 88.50s (0:01:28)`).
- Harness di mutation (scratchpad `mut_sweep.py`, in sequenza): prima passata 50/51 (unica sopravvissuta equivalente, poi sostituita); passata estesa finale **66/66 KILLED**, `ripristino: scripts/ pulito`. Il revisore ha rilanciato in modo indipendente 28/28 KILLED.
- Kernel non rilanciato: non toccato.

## §6 STATO CI

```
completed	failure	test(gate-ip): passata unica di mutation sul gate IP (66/66 uccise) —…	CI	test/gate-ip-passata-mutation	push	37231493425	1m28s	2026-10-04T20:16:55Z
completed	success	Merge pull request #125 from Gasss23/test/gate-ip-rami-errore-loopback	CI	main	push	37227345457	1m17s	2026-10-04T19:11:54Z
completed	success	docs(gate-ip-test): fine-task — rami d'errore e loopback del gate IP,…	CI	test/gate-ip-rami-errore-loopback	push	37221829534	1m12s	2026-10-04T17:47:07Z
```

Mappatura commit→run:
- `1f29fc8`, `a3ac340` (memoria #153/#154): nessuna run su questi SHA (pushati insieme a `c2c2d3e`).
- `c2c2d3e` (test): run `37231493425` — `unit-suite: success` (su ubuntu: hooks `86 passed`, voice `19`, handoff `40`, gate `74`, gasmerge `43 passed`), `handoff-check: failure` (`check_handoff: ERRORE — la sessione tocca il perimetro di review ma reports/handoff.md non è nel diff di sessione: handoff obbligatorio (V-A).`): atteso, l'handoff arriva col commit di fine-task.
- Commit di fine-task (che contiene questo file): run non ancora disponibile alla scrittura dell'handoff. La copertura pre-merge resta a `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

- **R-153-2 (bassa)**: `scripts/gasmerge.sh:27` `mktemp /tmp/gaspr.XXXXXX.json` su BSD non randomizza il nome (due gasmerge concorrenti: il secondo muore, fail-closed).
- **Latin1 su glibc**: i test passano su Linux, ma le mutation `LC_ALL=C` sono state uccise solo su macOS.
- **R-150-1 (bassa)**: ramo `PUSH_EXIT` morto in fine_task_finale.sh.
- Limite noto del gate IP: cieco a UTF-16 e a IP spezzati o codificati.
- V-3 / V-5 verifica #121: decisione operatore. R-143-2 (ci.yml dalla PR) → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #125 (handoff `efabd94`)

Unica aggiunta al testo: il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio, richiesto dal gate IP su reports/.

VERIFICA ESTERNA PR #125 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad, checkout di efabd940a6560fe6c5129331011687efa8fb93b1 (coincide con headRefOid della PR). Merge-base con main: dfb52a5. Ho letto per intero il diff dei test, di stato_progetto e di ultimo_report, più memoria_revisore e diff_sessione. Ho letto anche i blocchi del gate IP di fine_task_finale.sh e gasmerge.sh. Ho eseguito:
- pytest senza kernel e senza e2e, alla base e al commit (venv di /Users/gas/Gas).
- Un harness di mutation (mut125.py, nella scratchpad). Ha 22 mutation sul gate IP: 11 su fine_task_finale.sh e 11 su gasmerge.sh. Le ho girate una alla volta, sui test del commit.
- Le mutation che la PR dichiara chiuse, rigirate con i test della base (dfb52a5), per vedere che prima sopravvivono.
- Una sonda di merge sul mutante che sopravvive.
- gh: run e check della PR, ruleset, log CI.
Il repo reale non è stato toccato: `git status` mostra solo .agents/, .codex/, AGENTS.md, già non tracciati prima.

CLAIM VERIFICATI
- §2, set di file: VERO. I 7 file coincidono con `git diff --stat dfb52a5..HEAD`. Le righe reali sono 255/155 e handoff.md è +293; il NB del §2 le dichiara non esatte (cosmetico).
- §3, log: VERO. I tre commit (24c8640, 8ef9d32, 1c146e1) coincidono con `git log dfb52a5..HEAD`, meno efabd94 escluso per costruzione.
- Nessuno script e nessun ci.yml toccato, nessun gate indebolito: VERO. Il diff è solo tests/, reports/ e memoria_revisore.
- Test 299 → 303: VERO. Ho riprodotto 299 passed alla base e 303 passed a efabd94.
- CI: VERO.
  - La run 37221648955 su 24c8640 ha unit-suite pass e handoff-check fail ("handoff obbligatorio (V-A)"), come dichiarato nel §6.
  - La run 37221829534 su efabd94 ora ha unit-suite pass e handoff-check pass.
  - Nel log: hooks 80, voice 19, handoff 40, gate 74, gasmerge 38 passed.
  - 4j, 4k, 4l, TestIPErroreFiltro e test_git_grep_error_blocks sono PASSED su ubuntu.
- Ruleset main-lock: VERO. È active, i required sono unit-suite e handoff-check, con policy strict.
- Le 5 mutation dichiarate uccise sono VERE, e ciascuna è uccisa dal test nominato:
  - finale `*)`→`9999)` sulla prima grep, e exit 1 tolto dal suo ramo: ucciso da 4j (1 failed).
  - finale, sed loopback inefficace: ucciso da 4k.
  - finale, exit 1 tolto dal filtro: ucciso da 4l.
  - gasmerge, filtro `*)`→`9999)` o exit 1 tolto: ucciso da TestIPErroreFiltro.
  - gasmerge, exit 1 tolto dal ramo `*)` della prima grep (R-151-1): ucciso da test_git_grep_error_blocks.
- "Prima sopravvivevano, ora muoiono": VERO. Con i test della base (dfb52a5) tutte le mutation qui sopra passano 33/33, quindi sopravvivono; con i test nuovi muoiono. V-1 della #124 e R-151-1 sono chiuse.
- Altre mutation killed (nessuna sorpresa):
  - finale: loopback allargato, exit 1 tolto dopo RESIDUAL, `*)` e exit 1 della grep allowlist, tree non risolvibile, `[[ -z NON_LOOPBACK ]]` forzato.
  - gasmerge: `*)` e exit 1 della prima grep, loopback sed e allargato, `*)` del filtro, exit 1 della grep allowlist, tree non risolvibile.
- V-4 della #124 (stato_progetto): VERO. La riga R-149-1 è riscritta (7 su 11, chiusa in #124, completata in #125) e il gate test passa da 65 a 74, in accordo con la CI. V-5 (`dict[str, str]`): VERO.
- Gate IP sul tree efabd94 (stesso regex, `--and --not`, senza loopback): 0 residui.

FINDING
- V-1 (MEDIA) — Il ramo principale di deny del gate IP in `gasmerge.sh` non ha test che lo faccia fermare. Togliere `exit 1` dopo `echo "$RESIDUAL"` (il ramo `0)` del FILTER_RC, "trovati IP non allowlistati", `gasmerge.sh` ~riga 136) fa passare 37/37 test (TestIPGuard, TestIPAllowlist, TestIPErroreFiltro e tutti i `-k "TestIP or TestLoopback"`).
  - Sonda riprodotta: sul mutante, un branch con `gateway: 8.8.8.8` non marcato e stdin "123" stampa l'IP, prosegue oltre il gate, e `gh pr merge` viene chiamato (RC 0, merge_log creato). Il gate quindi stampa e poi lascia passare.  # gasmerge-ip-ok
  - Causa: i test del ramo (test_ip_without_marker_blocks, test_public_ip_without_marker_blocks e simili) asseriscono solo rc≠0, "BLOCCO" e l'IP stampato. Senza stdin lo script esce comunque al `read` successivo. È la stessa classe di lacuna della lezione #150 e di R-151-1.
  - Non è una regressione di questa PR, ma la PR e il handoff presentano i "rami d'errore" come coperti (R-149-1 "completata"). Il ramo equivalente in fine_task_finale.sh (F-resid-noexit) invece è ucciso da 7+ test. La memoria_revisore (riga 2026-10-04 dopo #152) dice proprio di ripassare i test preesistenti del gemello, ma questo non è stato fatto per questo ramo.
  - Fix proposto: in uno dei test "IP non marcato" di gasmerge aggiungere `assert "--- FILE DI MOTORE ---" not in result.stdout`. In alternativa: stdin "123\n" con `_make_stub_gh_recording_merge` e `assert not merge_log.exists()`.
- V-2 (BASSA) — `sed` loopback senza il flag `g` sopravvive in entrambi gli script (finale `{1,3}//g')`→`//')`, e il gemello in gasmerge). Una riga con due IP 127.x resterebbe "non loopback": falso BLOCCO, quindi fail-closed (più severo, non un bypass). Manca un test su una riga con due loopback. Fix: un test con `127.0.0.1 127.0.0.2` che deve passare.
- V-3 (BASSA, già dichiarata, non provata) — il test latin1 su glibc/GNU grep non è provato localmente. Il handoff lo dichiara correttamente come DEFERITA. La CI ubuntu lo vede solo passare, non discriminare.
- V-4 (COSMETICA) — il §6 del handoff dice che la run del commit di fine-task "non è ancora disponibile". Ora è disponibile ed è verde (37221829534, unit-suite e handoff-check pass), quindi il §6 è superato. Stessa classe di V-3 della #124.
- V-5 (COSMETICA, preesistente) — `gasmerge.sh:27` usa `mktemp /tmp/gaspr.XXXXXX.json`. Su macOS/BSD il suffisso fa creare un file letterale, e due esecuzioni parallele collidono ("File exists"). L'ho visto solo lanciando i test in parallelo; in serie va. Non tocca Linux/CI.

NON VERIFICATO
- Il testo integrale del verdetto della verifica #124 incollato nel handoff, e che l'unica aggiunta sia il marker `# gasmerge-ip-ok`: non ho l'originale.
- Il comportamento di GNU grep e sed su glibc (V-3): non ho Docker né GNU grep locale.
- I verdetti #151/#152 incollati nel handoff: non ho riprodotto l'output del revisore. Ho però riprodotto le sue mutation (vedi sopra) e i numeri (303).
- Merge reale con gasmerge: non lanciato.

RACCOMANDAZIONE
Il lavoro dichiarato è vero e riprodotto: 303 passed, CI verde su efabd94, nessun gate indebolito, V-1/V-4/V-5 della #124 e R-151-1 chiusi con prova prima/dopo. La PR #125 è mergiabile. Prima di dichiarare "parità e copertura completa dei rami del gate IP", in una micro-fetta:
1. Chiudere V-1 (MEDIA): asserzione di arresto, o merge_log assente, nel ramo `RESIDUAL` di gasmerge.
2. Aggiungere il test a due loopback (V-2).
3. Aggiornare il §6 del handoff con la run verde.
Lasciare aperta la V-3 (latin1 su glibc), da chiudere con la V-B vera o con un job CI di mutation. Le decisioni dell'operatore V-3/V-5 della #121 restano invariate.

Esito: PR #125 mergiata (operatore); V-1 e V-2 chiusi in questa PR #126 insieme alla passata unica di mutation (66/66); V-5 = R-153-2 aperta; V-3 aperta.
