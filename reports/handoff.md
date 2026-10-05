# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-05 — Gate IP: IP adiacente a un punto (R-155-1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #128 (https://github.com/Gasss23/Gas/pull/128).
2. **R-155-3** (operativa): Codex e Claude Code nella stessa cartella `~/Gas`; nella worktree usata per questa fetta l'hook `review_gate.sh` non protegge (legge lo stage di `~/Gas`). Codex in una cartella sua, o hook consapevole delle worktree?
3. Residui V-2 / V-3 della verifica esterna #127 (secondo fetch senza `--prune`; `HEAD_SHA` catturato dopo il gate IP): fissarli prima della variante B del merge?
4. V-3 / V-5 della verifica #121: ancora aperte.
5. Poi la fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #127**: `FATTA` — `gasmerge 127` confermato dall'operatore; main `7ded2a4`.
- **R-155-1 — IP adiacente a un punto (fine frase, `<IP>.dominio`, `dominio.<IP>`)**: `FATTA` — testa `(^|[^0-9.]|(^|[^0-9])\.)` e coda `([^0-9.]|\.([^0-9]|$)|$)` nelle 6 regex del gate IP; test speculari nei due script.
- **Redazione riga #155 di memoria_revisore.md**: `FATTA` — conteneva un IP a fine frase non marcato, ora visibile al gate.
- **Residui V-2 / V-3 verifica #127**: `DEFERITA — annotati in stato_progetto, decisione operatore.`
- **R-153-2, latin1 su glibc, R-150-1**: `DEFERITA — fuori scope.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +++-
 reports/diff_sessione.md           |  12 +++++++-----
 reports/handoff.md                 | 234 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  38 ++++++++++++++++++--------------------
 scripts/fine_task_finale.sh        |   7 ++++---
 scripts/gasmerge.sh                |   8 +++++---
 tests/test_unit_gasmerge.py        |  34 ++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  27 +++++++++++++++++++++++++++
 9 files changed, 208 insertions(+), 162 deletions(-)
```

NB: conteggi di `reports/handoff.md` approssimati per costruzione (il file conta se stesso).

## §3 GIT LOG --ONELINE (sessione)

```
afc36ca fix(gate-ip): IP adiacente a un punto visibile al gate IP (R-155-1) — review #156
d4806d1 chore(revisore): memoria review #156 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `afc36ca` (scripts + tests): review #156, incollata per intero.

### Review 156

## VERDETTO: APPROVATO CON RISERVE

Review #156: diff STAGED in `/Users/gas/Gas/.claude/worktrees/gate-ip-ottetti`, branch `fix/gate-ip-ip-adiacente-punto` (l'ho controllato con `git branch --show-current` sia prima sia dopo).

Prima della review ho letto CLAUDE.md sez. 5, `reports/stato_progetto.md` in modo selettivo (R-155-1, R-155-3) e `.claude/agents/memoria_revisore.md` (#144–#155 e le lezioni). Nessun antipattern del Wall of Shame: il diff è tutto shell e test, non tocca la history, non simula tool e non tocca il motore.

**Elementi del diff esaminati**
- `scripts/gasmerge.sh:100` — prima git grep con le ancore nuove. Rischio: un IP vicino a un punto resta invisibile, oppure "1.2.3.4.5" diventa un IP. Sonde con BSD grep e git grep: danno lo stesso risultato su 18 casi. Bloccano fine frase, `<IP>.dominio`, `dominio.<IP>`, `.<IP>`, `<IP>..`, `<IP>...`, `(<IP>).`, `a.<IP>.b` e ottetti a 3 cifre. Non bloccano cinque componenti (anche con un punto prima o dopo), `10.127...` né ottetti a 4 cifre. — **ok**
- `scripts/gasmerge.sh:113` — grep -qE sulla riga dopo che il sed ha tolto il loopback. Rischio: togliere il loopback crea un'adiacenza nuova, oppure un IP pubblico sfugge su una riga mista. Le righe miste "loopback + IP." e "loopback + .IP" bloccano; "loopback + cinque componenti" e "loopback seguito da punto" passano come loopback. — **ok**
- `scripts/gasmerge.sh:126` e `scripts/fine_task_finale.sh:97` — git grep della allowlist `--and --not`. Rischio: un fail-open se questa regex resta più stretta delle altre due. Con la regex vecchia qui la mutation viene uccisa. Le mutation preDotDig/sufDotDig sopravvivono, ma allargano soltanto: il residuo è NON_LOOPBACK ∩ UNMARKED, quindi bloccano di più (fail-closed). — **ok**
- `scripts/fine_task_finale.sh:73` / `:86` — speculari a gasmerge, regex identiche byte per byte. Un git grep su tutto il repo conferma che queste 6 sono le uniche copie della regex IP: nessun gemello dimenticato. — **ok**
- `tests/test_unit_gasmerge.py:859` / `:875` e `tests/test_unit_hooks.py:2152` / `:2164` — 6 casi che bloccano e 3 che non bloccano per script. Le asserzioni sono testuali: "FILE DI MOTORE" / "=== Push ===" assenti, e il messaggio OK atteso è esatto. Ogni riga sorgente ha il marker `gasmerge-ip-ok`. — **ok**
- `.claude/agents/memoria_revisore.md:245` — la riga #155 è redatta. Senza la redazione ogni merge si sarebbe bloccato: con la regex nuova, scansionando `refs/remotes/origin/main` ho trovato 1 riga residua ed è proprio quella. Il significato della lezione resta. — **ok**

**Riproduzioni**
- **Test:** `test_unit_gasmerge.py` + `test_unit_hooks.py` → 153 passed; selezione dei test nuovi → 18 passed.
- **Mutation** (mio harness, in sequenza: 5 mutazioni × 3 regex × 2 script = 30): 26 KILLED, 4 SURVIVED. Le sopravvissute sono solo re3 preDotDig/sufDotDig nei due script, cioè allargamenti fail-closed. Coincide con quanto dichiarato. Dopo la run gli scripts/ sono ripristinati e l'index è intatto.
- **Scansione del tree staged** (`git write-tree`) con la regex nuova + filtro loopback + allowlist: 0 residui.

**Riserve**
- **R-156-1 (bassa):** il comportamento di GNU grep e di git su glibc (CI ubuntu) non l'ho provato in locale: non ci sono ggrep né docker. Lo prova la CI, perché `ci.yml:95` e `:123` eseguono entrambi i file di test. Se lì una regex non si comportasse come qui, i test 4p/4q/adiacente diventerebbero rossi, quindi un errore sarebbe visibile e non silenzioso. Da confermare con la CI verde sulla PR.
- **Nota (falso positivo accettato):** da ora una versione a 4 componenti seguita dal punto di fine frase blocca. È fail-closed. I report e l'handoff di questa fetta non devono citare IP d'esempio non marcati, nemmeno a fine frase. Se succede, li ferma lo stesso `fine_task_finale.sh`.

**Rischio escluso:** non ho verificato il comportamento con GNU grep/glibc (vedi R-156-1). Non ho scansionato con la regex nuova i branch aperti di altre sessioni (es. quello Codex). Se contengono un IP non marcato seguito da un punto, il loro merge si bloccherà (fail-closed, nessun crash). Non ho scansionato le PR future, che non sono in questo diff.

**Memoria**
- Ho aggiunto la riga `#156 — 2026-10-05 — APPROVATO CON RISERVE — …` e una lezione: rafforzare la regex di un gate va verificato scansionando con la regex nuova sia il tree staged sia `origin/main`. Ho controllato con la regex nuova che le due righe non contengano IP (0 match).
- `commit_memoria_revisore.sh` ha creato il commit `d4806d1` (chore(revisore): memoria review #156).
- **Attenzione per l'agente principale:** `git commit -o` ha committato tutto `.claude/agents/memoria_revisore.md`, compresa la redazione della riga 245 che era staged. Quel file quindi non è più nel diff staged. Ora lo stage contiene solo `scripts/fine_task_finale.sh`, `scripts/gasmerge.sh`, `tests/test_unit_gasmerge.py`, `tests/test_unit_hooks.py`. Il diff staged è cambiato, quindi il marcatore va creato su questo stage con `bash scripts/segna_review_ok.sh`: il contenuto revisionato dei 4 file è identico.

File rilevanti:
- /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/scripts/gasmerge.sh
- /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/scripts/fine_task_finale.sh
- /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/tests/test_unit_gasmerge.py
- /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/tests/test_unit_hooks.py
- /Users/gas/Gas/.claude/worktrees/gate-ip-ottetti/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py / brains / modules. Modificati scripts/ (gate IP) e tests/.

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e` (worktree, venv di `~/Gas`): 320 → **338 passed in 103.00s**.
- Mutation in sequenza (harness `mut_sweep.py`): **120 KILLED, 8 SURVIVED**. Sopravvissute: `re3_noPre`, `re3_noSuf`, `re3_preDotDig`, `re3_sufDotDig` in gasmerge.sh e in fine_task_finale.sh (terza regex = grep allowlist; allargamenti fail-closed). Uccise in entrambi gli script: `re1/re2` × `noPre`, `noSuf`, `preOld`, `sufOld`, `preDotDig`, `sufDotDig`; `re3_preOld`, `re3_sufOld`; tutta la matrice ottetti e le mutation precedenti.

## §6 STATO CI

Output di `gh run list -L 3` alla scrittura:

```
in_progress		fix(gate-ip): IP adiacente a un punto visibile al gate IP (R-155-1) —…	CI	fix/gate-ip-ip-adiacente-punto	push	37314204594	21s	2026-10-05T13:05:56Z
completed	success	Merge pull request #127 from Gasss23/test/gate-ip-ottetti-ref-tree	CI	main	push	37309324643	1m20s	2026-10-05T12:24:35Z
completed	success	docs(gate-ip-ottetti): fine-task — V-1/V-2/V-3 verifica #126 chiuse, …	CI	test/gate-ip-ottetti-ref-tree	push	37298130009	1m37s	2026-10-05T10:41:00Z
```

Mappatura commit → run:
- `afc36ca`: run 37314204594 (push di `d4806d1` + `afc36ca`, testa l'albero di `afc36ca`), in corso alla scrittura. Atteso: unit-suite verde (prova R-156-1 su ubuntu), handoff-check rosso (handoff non ancora nel diff a quel SHA).
- `d4806d1`: nessuna run su questo SHA (pushato insieme a `afc36ca`; il suo contenuto è incluso nell'albero testato da 37314204594).
- Commit di fine-task (contiene questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-156-1 (bassa)**: regex nuove non provate su GNU grep in locale; la CI ubuntu esegue i test nuovi.
- **R-155-3 (operativa)**: hook `review_gate.sh` inerte nelle worktree (legge lo stage di `CLAUDE_PROJECT_DIR`).
- **Verifica #127 V-2 / V-3 (basse)**: secondo fetch di gasmerge senza test su `--prune`; `HEAD_SHA` catturato dopo il gate IP.
- **R-153-2 (bassa)**: mktemp BSD in gasmerge.sh. **Latin1 su glibc** non provato. **R-150-1 (bassa)**: ramo `PUSH_EXIT` morto.
- Limite noto del gate IP: cieco a UTF-16 e a IP spezzati o codificati.
- V-3 / V-5 verifica #121: decisione operatore. R-143-2 (ci.yml dalla PR) → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #127 (handoff `5c8a6a0`)

Uniche aggiunte al testo: questa intestazione e il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio.

VERIFICA ESTERNA PR #127 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad (`.../scratchpad/vclone`, da /Users/gas/Gas), checkout di 5c8a6a006af530f52cf7df4e481ee2ed70cf23fa. Coincide con headRefOid della PR (gh). Merge-base con main: 0221462 (merge della #126). Un secondo clone (`vbase`) a 0221462 per i confronti prima/dopo.
Ho eseguito:
- `git diff --stat` e `git log` reali dalla base; diff integrale di tests/ e memoria_revisore; lettura di `scripts/gasmerge.sh` e `scripts/fine_task_finale.sh`.
- pytest (senza kernel e senza e2e, venv di /Users/gas/Gas) alla base e al commit pinnato.
- Un MIO harness di mutation (`scratchpad/v127/mut.py`, `mut2.py`, `mut3.py`; NON il `mut_sweep.py` dell'agente), una mutation alla volta e mai in parallelo:
  - Matrice `{1,3}`→`{1,2}` e `{1,3}`→`{1,1}` su ognuno dei 4 ottetti delle 3 regex di ciascuno script: 48 mutation sul commit pinnato. Le stesse sul finale alla base: 24.
  - Mutation su tree e fetch di gasmerge (7).
  - Rimozione delle ancore (12).
- Sonde regex dirette per il caso "IP a fine frase".
- gh: run, check, ruleset.
Nota di metodo: un mio primo lancio ha girato due volte in parallelo sullo stesso clone. L'ho interrotto, ho ripristinato `scripts/` e scartato quei risultati. Tutti i numeri sotto vengono da run singole e in sequenza.
Clone pulito a fine verifica (0 file modificati); la worktree della sessione è pulita. Non ho potuto lanciare `git status` sul checkout condiviso /Users/gas/Gas: il comando è stato rifiutato dal sandbox della worktree. Quel repo l'ho solo clonato in lettura e non ci ho scritto nulla. Nessuna sonda è nel repo.

CLAIM VERIFICATI
- §2 file toccati: VERO. I 7 file coincidono con `git diff --stat 0221462..5c8a6a0`. I conteggi reali sono 225+/197-, il handoff dichiara 210/201 e "approssimati per costruzione" (handoff.md 303 righe reali contro 292). Cosmetico e dichiarato.
- §3 log: VERO. `dd15215` e `4babba9` coincidono. Il commit di fine-task `5c8a6a0` è escluso per costruzione, come dichiarato.
- "Nessuno script modificato, solo tests/": VERO. Il diff su scripts/, .github/, .claude/hooks, gas.py, brains, modules e settings.json è vuoto. Nessun gate è indebolito.
- Test 314 → 320: VERO. Alla base 314 passed (89s), a 5c8a6a0 320 passed (95s).
- CI e ruleset (via gh):
  - VERO la run 37298130009 su `5c8a6a0`: unit-suite success, handoff-check success.
  - VERO la run 37298048052 su `4babba9`: unit-suite success, handoff-check failure. È l'esito atteso dal §6 (handoff assente dal diff a quel SHA).
  - Il §6 dice "in corso / run non ancora disponibile", ora superato (cosmetico).
  - Ruleset `main-lock` active; i required sono unit-suite e handoff-check, policy strict.
- V-1 #126 CHIUSA: VERO, con prova prima/dopo.
  - Alla base, sul finale, sopravvivono 12 mutation su 24 dei miei test (`{1,2}` e `{1,1}` sul 3° e 4° ottetto, in ciascuna delle 3 regex: righe 72, 85, 96).
  - Al commit pinnato le 24 sono tutte uccise. Il test che le uccide è `test_finale_4o_ottetti_a_piu_cifre_bloccano`.
  - Gasmerge: 24/24 uccise (righe 98, 111, 124).
- V-2 #126 CHIUSA: VERO. `refs/remotes/origin/$BRANCH^{tree}` → `refs/heads/$BRANCH^{tree}`: 2 failed (`test_branch_locale_pulito_non_maschera_origin_con_ip` e `test_push_durante_attesa_ci_visto_dal_gate`).
  - Anche `HEAD^{tree}` è ucciso (25 failed, tra cui il test nominato).
- V-3 #126 CHIUSA: VERO. Il test `test_push_durante_attesa_ci_visto_dal_gate` uccide queste mutation del secondo fetch (l'unico test che fallisce in ciascuna):
  - rimozione del secondo `git fetch --prune`;
  - spostamento del fetch prima del `--watch`;
  - fetch verso un remote inesistente.
  - Anche lo spostamento del fetch dopo il calcolo di IP_MATCHES è ucciso (3 failed, incluso il test nominato).
  - Se il push dello stub `on_watch` non avvenisse, il test fallirebbe e non passerebbe in verde per errore.
- V-4 #126 "ancore chiuse come fail-closed": VERO. Il conteggio dei sopravvissuti coincide: 12 su 12 sopravvivono (6 per script, prefisso e suffisso su ciascuna delle 3 regex). Ho verificato che sono allargamenti monotoni: `RESIDUAL = NON_LOOPBACK ∩ UNMARKED` può solo crescere. Nessuna apre un bypass.
- R-155-1 (IP seguito da punto): VERO, riprodotto con `grep -E` con la regex dello script.
  - `8.8.8.8.` → 0 match. `(8.8.8.8).` e `8.8.8.8` isolato → match.  # gasmerge-ip-ok
  - Il handoff però lo descrive in modo troppo stretto, vedi V-1 sotto.
- Gate IP sul tree di `5c8a6a0`: VERO, 0 occorrenze non-loopback senza marker (marker solo sulla riga sorgente).

FINDING
- V-1 (MEDIA-BASSA, preesistente, già aperta come R-155-1, ma sottostimata nella descrizione). La lacuna dell'ancora è più larga del "punto di fine frase".
  - Sonda riprodotta con la regex dei 3 punti: `8.8.8.8.nip.io` e `host.8.8.8.8` → 0 match, cioè passano. Sono la stessa classe: IP adiacente a un punto, in testa o in coda.  # gasmerge-ip-ok
  - Il fix proposto (`([^0-9.]|\.([^0-9]|$)|$)` e simmetrico in testa) copre anche questi casi. Il test richiesto dovrebbe includerli: oltre a "IP a fine frase", anche `<IP>.dominio` e `dominio.<IP>`, in entrambi gli script.
- V-2 (BASSA). Sopravvive la mutation `git fetch --prune origin` → `git fetch origin` sul secondo fetch di gasmerge (45 passed).
  - Un branch cancellato su origin lascerebbe un ref stale con tree letto dal gate. Praticamente innocua, perché `gh pr view` fallirebbe prima. Va solo annotata come non coperta.
- V-3 (BASSA, preesistente, dichiarata nello script). `HEAD_SHA` è catturato da `gh pr view` DOPO i controlli IP e file-motore, e `gh pr merge --match-head-commit` usa quello SHA. Il gate IP non è quindi legato allo SHA effettivamente mergiato.
  - Un push nel micro-intervallo tra i controlli e la cattura viene mergiato senza essere stato visto dal gate IP.
  - Il commento nello script lo dichiara come "residuo di millisecondi". Fix possibile: confrontare `HEAD_SHA` con `git rev-parse origin/$BRANCH` risolto dal tree controllato, prima della conferma. Non è una regressione della PR.
- V-4 (COSMETICA). Il §6 del handoff è già superato: la run su `5c8a6a0` è ora verde. Nel §2 il conteggio dello stat differisce dal reale, già dichiarato approssimato.
- V-5 (COSMETICA). Il titolo della PR #127 è `test/gate ip ottetti ref tree` e il corpo è solo l'elenco dei commit. Nessuno scope o rischio dichiarato nel corpo. Non blocca.
- Nota: il caso `10.20.30.40` del test parametrizzato uccide solo le mutation `{1,1}`, nessuna `{1,2}`. È un controllo positivo innocuo, ma la sua utilità è marginale.  # gasmerge-ip-ok

NON VERIFICATO
- Il numero "92 KILLED / 12 SURVIVED" e l'harness `mut_sweep.py` dell'agente: non rilanciati, perché sono nella scratchpad della sessione e non nel repo.
  - Ho riprodotto con un harness mio solo i sottoinsiemi pertinenti (48 mutation sugli ottetti, 7 su tree e fetch, 12 sulle ancore). I 12 sopravvissuti coincidono esattamente; la parte "92 killed" non ho potuto confrontarla riga per riga.
- Il testo del verdetto #126 incollato nel §7 e l'affermazione "uniche aggiunte: intestazione e marker": il verdetto originale non è nel repo, quindi non ho una fonte da confrontare.
- Il testo del verdetto del revisore #155: ho riprodotto le sue mutation (tree, secondo fetch, 4° ottetto) ma non ho riletto le sue sonde sul branch Codex.
- R-155-3 (l'hook `review_gate.sh` non protegge nelle worktree): non provato. Ho solo letto la dichiarazione.
- Comportamento su glibc/GNU grep (latin1, `LC_ALL=C`): non provato, ho eseguito solo su macOS. La CI ubuntu lo vede solo passare.
- Stato del checkout condiviso /Users/gas/Gas: comando `git status` rifiutato dal sandbox, quindi non ho potuto confermarlo vuoto (il worktree `gate-ip-ottetti` è pulito).

RACCOMANDAZIONE
La PR #127 è mergiabile. Solo test e report, nessuno script toccato, 320 passed, CI verde su `5c8a6a0`, e V-1/V-2/V-3 della #126 sono chiuse con prova prima/dopo.
1. Merge della PR #127.
2. Subito dopo, la micro-fetta R-155-1. Va estesa nella descrizione e nei test a `<IP>.dominio` e `dominio.<IP>`, non solo al punto di fine frase. Va fatta prima della V-B e della variante B del merge, perché lì il gate IP diventa l'unico controllo.
3. Annotare in stato_progetto V-2 (fetch senza `--prune`) e V-3 (`HEAD_SHA` non legato al tree controllato) come residui noti.
4. Restano a carico dell'operatore R-155-3 e le decisioni V-3/V-5 della #121.
