# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-05 — gasmerge: mktemp casuale (R-153-2) + test IP a inizio riga nel finale (verifica #128 V-1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #129 (https://github.com/Gasss23/Gas/pull/129).
2. **R-155-3** (operativa): Codex e Claude Code nella stessa cartella `~/Gas`; nella worktree usata per questa fetta l'hook `review_gate.sh` non protegge (legge lo stage di `~/Gas`). Codex in una cartella sua, o hook consapevole delle worktree?
3. Residui V-2 / V-3 della verifica esterna #127 (secondo fetch senza `--prune`; `HEAD_SHA` catturato dopo il gate IP): fissarli prima della variante B del merge?
4. V-3 / V-5 della verifica #121: ancora aperte.
5. Poi la fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #128**: `FATTA` — main `08a9d51`. Il primo lancio di `gasmerge 128` era uscito subito per R-153-2 (residuo `/tmp/gaspr.XXXXXX.json` lasciato da un processo ucciso); file vuoto rimosso, rilancio riuscito.
- **R-153-2 — mktemp di gasmerge.sh**: `FATTA` — `mktemp "${TMPDIR:-/tmp}/gaspr.XXXXXX"` + guardia; `TestFileTemporaneo`.
- **V-1 verifica #128 — `^` della testa non coperto nel finale**: `FATTA` — IP a inizio riga, inizio riga + `.dominio`, file senza newline in `test_finale_4p_*`.
- **V-2 verifica #128 — formula "solo allargamenti"**: `FATTA` — stato_progetto corretto ("nei mutanti testati").
- **V-4 / V-5 verifica #128** (cosmetiche: §6 superato, titolo PR): `FATTA` — handoff riscritto; PR #128 aveva già titolo e corpo con scope e rischi.
- **Residui V-2 / V-3 verifica #127, latin1 su glibc, R-150-1**: `DEFERITA — decisione operatore / fuori scope.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 reports/diff_sessione.md           |  13 ++++++-------
 reports/handoff.md                 | 210 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   8 +++++---
 reports/ultimo_report.md           |  31 ++++++++++++++++---------------
 scripts/gasmerge.sh                |   4 +++-
 tests/test_unit_gasmerge.py        |  57 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |   3 +++
 8 files changed, 169 insertions(+), 158 deletions(-)
```

NB: conteggi di `reports/handoff.md` approssimati per costruzione (il file conta se stesso).

## §3 GIT LOG --ONELINE (sessione)

```
33f7f47 fix(gasmerge): mktemp con nome davvero casuale (R-153-2) + test IP a inizio riga nel finale (verifica #128 V-1) — review #157
a0afeb4 chore(revisore): memoria review #157 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `33f7f47` (script + test): review #157, incollata per intero.

### Review 157

## VERDETTO: APPROVATO

Branch verificato: `fix/gate-ip-inizio-riga-mktemp` nella worktree /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti. Prima della review ho letto CLAUDE.md (§5), stato_progetto.md (R-153-2, R-155-x) e la memoria. Nel diff non c'è slicing della history né simulazione di tool, e il motore non viene toccato.

**Cosa ho controllato nel diff**
- `scripts/gasmerge.sh:29`: ora `mktemp "${TMPDIR:-/tmp}/gaspr.XXXXXX"` ha le X in fondo al nome, quindi il nome è casuale anche su macOS (BSD). Se mktemp fallisce, lo script stampa "ERRORE: mktemp fallito" ed esce con 1 prima di `trap` e di `gh`.
  - Rischi esaminati: con `TMPDIR` vuoto si ripiega su /tmp; il `trap` di :31 resta valido; nessun consumatore dipende dal suffisso `.json` (jq legge per path, :34-37).
  - Ho cercato con grep tutti i `mktemp` in scripts/ e negli hook: questo è l'unico, quindi la classe è chiusa. Esito: ok.
- `tests/test_unit_gasmerge.py:161` (`TestFileTemporaneo`): due esecuzioni con i residui `gaspr.XXXXXX.json` e `gaspr.XXXXXX` già presenti producono nomi diversi, dentro TMPDIR, poi rimossi. Con TMPDIR inesistente compare l'errore esplicito e `gh` non viene mai chiamato.
  - Rischio esaminato: un test che passa anche sullo script vecchio. Controprova con `GASMERGE_SCRIPT` = gasmerge di HEAD: **2 failed**, cioè falliscono entrambi i test nuovi. Esito: ok.
- `tests/test_unit_hooks.py:2151` (casi di `test_finale_4p_*`: IP a inizio riga, inizio riga + `.dominio`, file senza newline) e `tests/test_unit_gasmerge.py:914` (inizio riga + `.dominio`).
  - Rischio esaminato: il `^` della testa delle regex 1 e 3 senza copertura (V-1 #128). I casi colpiscono proprio l'alternativa `^` e ogni riga porta il marker sulla sorgente. Esito: ok.
- Contesto, `scripts/fine_task_finale.sh:86`: la mutation re2 noCaret è **equivalente, confermato**. La seconda regex lavora su righe che iniziano sempre con lo SHA del tree: 40 caratteri esadecimali senza punti, seguiti da `:`. Il sed del loopback richiede `127\.`, quindi non può modificare la colonna 0. Nessuna delle due `^` della regex 2 è raggiungibile, né in gasmerge (:113) né nel finale. Un IP a inizio contenuto è preceduto da `:`, che `[^0-9.]` copre già. Esito: ok. Si possono lasciare per simmetria con le regex 1 e 3.

**Riprodotto**
- 18 pytest mirati passati (FileTemporaneo, adiacente, 4p).
- Scansione IP del tree staged con la regex nuova (allowlist + loopback): 0 residui.
- Entrambi i file di test girano in CI (ci.yml:95 e :123), quindi anche GNU mktemp e GNU grep vengono provati lì.

**Riserve**: nessuna.

**Rischio escluso**
- Non ho rilanciato lo sweep di mutation completo (142/12) né la suite intera da 344: mi fido dell'esito dichiarato, perché ho riprodotto le parti decisive (controprova sullo script di main, analisi di raggiungibilità di re2).
- Il comportamento di GNU mktemp su ubuntu con TMPDIR inesistente non l'ho verificato in locale: lo coprirà la CI.

**Memoria**: riga #157 aggiunta in coda a /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/.claude/agents/memoria_revisore.md, senza IP, nessuna lezione nuova. È committata con `a0afeb4 chore(revisore): memoria review #157 — APPROVATO`; l'index staged è intatto (3 file, +63/-1).

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py / brains / modules. Modificati `scripts/gasmerge.sh` e tests/.

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e` (worktree, venv di `~/Gas`): 338 → **344 passed in 104.42s**.
- Mutation in sequenza (harness `mut_sweep.py`): **142 KILLED, 12 SURVIVED**. Sopravvissute, tutte equivalenti: `re3_noPre`, `re3_noSuf`, `re3_preDotDig`, `re3_sufDotDig` (allargamenti della grep allowlist) e `re2_noCaret`, `re2_noCaret2` (`^` irraggiungibile nella grep -qE), in entrambi gli script. Uccise le nuove: `re1/re3_noCaret` e `noCaret2`, `re1/re2/re3_noEOL` e `noDotEOL` in entrambi gli script; `mktemp_suffisso`, `mktemp_noguard` (gasmerge).
- Nota: un primo sweep è stato fermato dal limite di tempo del runner e ha lasciato `fine_task_finale.sh` mutato; ripristinato da HEAD e sweep del finale rilanciato a parte. Il diff della fetta non tocca quel file.

## §6 STATO CI

Output di `gh run list -L 3` alla scrittura:

```
in_progress		fix(gasmerge): mktemp con nome davvero casuale (R-153-2) + test IP a …	CI	fix/gate-ip-inizio-riga-mktemp	push	37339659414	13s	2026-10-05T16:17:16Z
completed	success	docs(tradegasfx): aggiorna esito push e CI	CI	codex/tradegasfx-redesign	push	37337781975	1m21s	2026-10-05T16:03:12Z
completed	success	Merge pull request #128 from Gasss23/fix/gate-ip-ip-adiacente-punto	CI	main	push	37317436530	1m15s	2026-10-05T13:31:15Z
```

Mappatura commit → run:
- `33f7f47`: run 37339659414 (push di `a0afeb4` + `33f7f47`, testa l'albero di `33f7f47`), in corso alla scrittura. Atteso: unit-suite verde, handoff-check rosso (handoff non ancora nel diff a quel SHA).
- `a0afeb4`: nessuna run su questo SHA (pushato insieme a `33f7f47`).
- Commit di fine-task (contiene questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-155-3 (operativa)**: hook `review_gate.sh` inerte nelle worktree (legge lo stage di `CLAUDE_PROJECT_DIR`).
- **Verifica #127 V-2 / V-3 (basse)**: secondo fetch di gasmerge senza test su `--prune`; `HEAD_SHA` catturato dopo il gate IP.
- **Latin1 su glibc** non provato. **R-150-1 (bassa)**: ramo `PUSH_EXIT` morto.
- Limite noto del gate IP: cieco a UTF-16 e a IP spezzati o codificati.
- V-3 / V-5 verifica #121: decisione operatore. R-143-2 (ci.yml dalla PR) → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #128 (handoff `e97d099`)

Uniche aggiunte al testo: questa intestazione e il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio.

VERIFICA ESTERNA PR #128 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad (`.../scratchpad/v128`), checkout di e97d09915a2a89cf6346d044f02df05716da650f. Coincide con headRefOid della PR (gh). Base 7ded2a4 (main). Altri due cloni: `v128base` a 7ded2a4 per il confronto prima/dopo, `v128mut` per le mutation. Ho eseguito:
- `git diff --stat` e `git log` reali dalla base, e il diff integrale di scripts/, tests/ e memoria_revisore.
- pytest (senza kernel e senza e2e, venv di /Users/gas/Gas) alla base e al commit pinnato, in sequenza.
- Un fuzz mio (`fuzz.py`, 62706 stringhe con `grep -E` BSD, `LC_ALL=C`): regex nuova contro un oracolo indipendente scritto con lookaround Python.
- Scansione dell'albero con regex nuova + strip del loopback + allowlist, su HEAD, origin/main e tutti i branch remoti.
- Un MIO harness di mutation (`mut128.py`; NON il `mut_sweep.py` dell'agente), una mutation alla volta, solo in sequenza. Mutation sulla singola occorrenza di ognuna delle 3 regex per script, 9 tipi, 54 in tutto.
- gh: run, job e ruleset.
Nota di metodo: il primo lancio dell'harness è stato ucciso dal timeout del runner a metà del giro. Ha lasciato `v128mut/scripts/gasmerge.sh` mutato; l'ho ripristinato con `git checkout` e ho rilanciato le mutation mancanti. I risultati sotto vengono dalle run complete. Ho avuto problemi di sandbox con `git -C` relativi e `&&` concatenati, quindi ho usato comandi semplici e script in scratchpad.
Stato finale: la worktree della sessione è pulita (HEAD e97d099) e le sonde sono nella scratchpad, non nel repo. `v128mut` pulito dopo il ripristino. Non ho toccato il checkout condiviso /Users/gas/Gas.

CLAIM VERIFICATI
- §2 `git diff --stat`: VERO. Gli stessi 9 file e le stesse righe nelle parti non-handoff. Il conteggio reale è 222+/155-; il dichiarato 208/162 è "approssimato per costruzione" (handoff.md 241 righe cambiate contro 234), come dichiarato.
- §3 log: VERO. `afc36ca` e `d4806d1` coincidono; `e97d099` (fine-task) è escluso per costruzione, dichiarato.
- Perimetro: VERO. scripts/ (2 file), tests/ (2 file), memoria_revisore e report. Nessun toccato di .github/, hook, gas.py, brains, modules, settings.json. Nessun gate indebolito sul piano del codice.
- Test 320 → 338: VERO. Alla base 320 passed (96.7s), a e97d099 338 passed (102.9s). La differenza +18 coincide con i casi parametrizzati nuovi (6+3 per script).
- Regex: VERO. Il fuzz, su 62706 stringhe con 218 positivi, ha 0 differenze rispetto all'oracolo. 0 regressioni rispetto alla regex vecchia: nessun caso che la vecchia bloccava e la nuova no. Quindi `<IP>.`, `<IP>.dominio`, `dominio.<IP>`, `.<IP>`, `<IP>..` bloccano; "1.2.3.4.5" e `1.<IP>` restano non-IP.  # gasmerge-ip-ok
- Scansione del tree con regex nuova + strip loopback + allowlist: VERO. HEAD: 0 residui. origin/main: 1 residuo, la riga #155 di memoria_revisore, che questa PR redige. Quindi la redazione era necessaria, come dichiarato. Branch remoti: solo `fix/crm-idemp-diario` ha IP non marcati (runbook S1, IP in prosa). È preesistente e bloccava anche con la vecchia regex, perché l'IP è seguito da backtick o spazio.
- CI reale sullo SHA e97d099 (run 37314295329): unit-suite success, handoff-check success. mergeStateStatus CLEAN.
- CI su afc36ca (run 37314204594): unit-suite success, handoff-check failure. È l'esito atteso dal §6 (handoff non ancora nel diff a quel SHA). Il §6 ("in corso") è ora superato (cosmetico).
- Ruleset `main-lock` (id 18805824) active. Required: unit-suite e handoff-check, policy strict. Coerente col §6.
- R-156-1 (regex non provate su GNU grep): ORA CHIUSA DALLA CI. Il log della run su ubuntu mostra tutti i test nuovi PASSED: 6+3 in gasmerge (54 passed) e 4p/4q in hooks (99 passed). Quindi vale anche per GNU grep/git su glibc nei casi testati.
- R-155-1 "CHIUSA", anche nella forma allargata `<IP>.dominio` / `dominio.<IP>` (V-1 #127): VERO, con prova prima/dopo. Alla base i casi punto finale, `<IP>.dominio`, `dominio.<IP>` non erano visti: la vecchia regex nel fuzz non li copre. Al commit pinnato bloccano, in entrambi gli script. Mutation che tornano all'ancora vecchia (tail_noDotAlt, head_noDotAlt) sono uccise dai nuovi test su tutte e 3 le regex di entrambi gli script.
- Mutation di coda e testa (riprodotte): `tail_noDotEOL`, `tail_noDotAlt`, `tail_noEOL`, `head_noDotAlt`, `head_alt3_digitOK` (parte), `head_alt3_anyChar` (parte) sono tutte uccise nei punti rilevanti. Gasmerge: 18/21 uccise; finale: 20/27 (dettaglio nei finding).

FINDING
- V-1 (MEDIA-BASSA, preesistente ma in una regex riscritta da questa PR, test-gap con fail-open dimostrato). Il `^` della testa `(^|[^0-9.]|...)` non è coperto nel finale. Mutation: togliere `^` dalla prima alternativa nella prima regex di `fine_task_finale.sh` (IP_MATCHES, righe di git grep a livello contenuto) → `(...)` diventa `([^0-9.]|(^|[^0-9])\.)`. Le 338 pass, il mutante SOPRAVVIVE.
  - Sonda riprodotta con le fixture del finale (`_repo_finale_con_bytes`) sul file `8.8.8.8\n`, `8.8.8.8` senza newline, `8.8.8.8.\n` e `8.8.8.8.nip.io\n`: tutti e 4 → "Gate IP: 0 IP trovati — OK" e il push parte. È un fail-open: un IP a inizio riga passa. Senza mutazione, gli stessi 4 casi bloccano.  # gasmerge-ip-ok
  - Stessa famiglia sulle altre due regex del finale (la grep allowlist, `occ3`): il restringimento lì fa trattare la riga come allowlistata senza marker.
  - In gasmerge la stessa mutation è uccisa su tutte e 3 le regex: il finale è meno coperto del gemello. I test 4o/4p del finale hanno IP preceduti da spazio o prefisso, mai IP a inizio riga puro.
  - Il codice è corretto oggi; è un buco di test. Il `^` preesisteva. Va però detto che la matrice "120 KILLED / 8 SURVIVED fail-closed" non lo copre: la mutation "solo `^` tolto dalla testa" non è nella lista dichiarata.
  - Fix proposto: un test nel finale con IP a inizio riga, ad esempio `b"8.8.8.8\n"` e `b"8.8.8.8.nip.io\n"` (marker sulla riga sorgente); uccide `^`-removal su R1 e R3.  # gasmerge-ip-ok
- V-2 (BASSA). "8 SURVIVED sono solo allargamenti fail-closed" vale per la loro matrice, non in assoluto. Nella mia matrice sopravvivono anche mutation che NON sono allargamenti (V-1 sopra). Le altre sopravvissute sono davvero equivalenti o allargamenti: `head_alt3_noCaret` sulla regex applicata a righe con prefisso (il `^` è morto perché precede sempre `<tree>:path:n:`), `tail_dotAnyDigit` sulla grep allowlist (allarga), `head_alt3_anyChar` e `head_alt3_digitOK` sulla grep allowlist (allargano). Nessuna apre un bypass oltre a V-1.
- V-3 (BASSA, informativa, preesistente). Dopo la PR un IP non marcato + punto di fine frase blocca (falso positivo accettato). Da ora ogni branch di altre sessioni con `<IP>.` in prosa non si mergia (ho trovato solo `fix/crm-idemp-diario`, che bloccava già). La nota è già nell'handoff e nel verdetto del revisore: non è un difetto.
- V-4 (COSMETICA). §6 dell'handoff è superato: la run su e97d099 è ora verde. Il conteggio dello stat nel §2 differisce dal reale (dichiarato approssimato).
- V-5 (COSMETICA). Il caso `.8.8.8.8\n` nei test del finale non uccide la mutation `^` in alt3 sulla regex con prefisso: è comunque equivalente. Il caso è però utile e uccide la mutation sulle altre due.  # gasmerge-ip-ok

NON VERIFICATO
- Il numero "120 KILLED / 8 SURVIVED" e il file `mut_sweep.py` dell'agente: sta nella scratchpad della sessione, non nel repo. Ho riprodotto solo con un harness mio un sottoinsieme (54 mutation sulle ancore). Non confronto riga per riga.
- Il testo del verdetto del revisore #156 incollato nel §4 e il verdetto della verifica #127 nel §7: non c'è una fonte per confrontare. Le affermazioni sul diff sono coerenti col codice.
- Ho provato GNU grep/git su glibc solo tramite i log della CI ubuntu (casi dei test nuovi). Non ho provato localmente altri casi (latin1, locale non C).
- R-155-3 (hook `review_gate.sh` inerte nelle worktree), residui V-2/V-3 della #127 (fetch senza `--prune`, `HEAD_SHA` dopo il gate IP): dichiarati, non provati e fuori dal diff.
- Stato del checkout condiviso /Users/gas/Gas: non toccato e non controllato.

RACCOMANDAZIONE
La PR #128 è mergiabile: i claim principali sono veri, CI verde sullo SHA, 0 regressioni nel fuzz, R-156-1 chiusa dalla CI ubuntu. Prima di altro lavoro sul gate IP (V-B vera, variante B del merge) fare una micro-fetta: aggiungere il test del finale per l'IP a inizio riga (V-1), e correggere nello stato la formula "solo allargamenti fail-closed" in "dei mutanti testati". Il merge della #128 può procedere con la variante A come previsto dall'operatore.
