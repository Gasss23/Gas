# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-05 — Gate IP: ottetti a 2-3 cifre, tree remoto, secondo fetch (riserve verifica esterna #126)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #127 (https://github.com/Gasss23/Gas/pull/127).
2. **R-155-1** (MEDIA-BASSA, preesistente): un IP seguito dal punto di fine frase passa il gate IP in entrambi gli script. Micro-fetta di fix prima della V-B? (consigliato: sì)
3. **R-155-3** (operativa): Codex e Claude Code nella stessa cartella `~/Gas`; nella worktree usata per chiudere questa fetta l'hook `review_gate.sh` non protegge (legge lo stage di `~/Gas`). Codex in una cartella sua, o hook consapevole delle worktree?
4. V-3 / V-5 della verifica #121: ancora aperte.
5. Poi la fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

---

## §1 SCOPE & ESITO FETTE

- **V-1 verifica #126 — ottetti a 2-3 cifre in fine_task_finale.sh**: `FATTA` — test `test_finale_4o_ottetti_a_piu_cifre_bloccano` (4 casi); uccide `{1,3}`→`{1,2}` sul 3° e 4° ottetto delle 3 regex.
- **V-2 verifica #126 — tree da origin in gasmerge.sh**: `FATTA` — `test_branch_locale_pulito_non_maschera_origin_con_ip`.
- **V-3 verifica #126 — secondo fetch dopo l'attesa CI**: `FATTA` — `test_push_durante_attesa_ci_visto_dal_gate` (stub gh con `on_watch`).
- **V-4 verifica #126 — ancore delle regex**: `SALTATA — chiusa come fail-closed (review #155): rimuovere un'ancora allarga il match; un test che la uccidesse congelerebbe la lacuna R-155-1.`
- **Harness mut_sweep.py esteso** (matrice ottetti, ref locale, fetch, ancore): `FATTA` — 92 KILLED, 12 SURVIVED (solo ancore).
- **V-5 / V-6 verifica #126** (cosmetiche sul vecchio handoff): `FATTA` — handoff riscritto; il verdetto #126 qui sotto ha come uniche aggiunte l'intestazione e i marker `gasmerge-ip-ok` (nessuna riga "Esito:" aggiunta).
- **R-153-2, latin1 su glibc, R-150-1**: `DEFERITA — fuori scope.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 292 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   7 +++++--
 reports/ultimo_report.md           |  39 ++++++++++++++++++---------------------
 tests/test_unit_gasmerge.py        |  46 +++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_hooks.py           |  14 ++++++++++++++
 7 files changed, 210 insertions(+), 201 deletions(-)
```

NB: conteggi di `reports/handoff.md` approssimati per costruzione (il file conta se stesso).

## §3 GIT LOG --ONELINE (sessione)

```
4babba9 test(gate-ip): ottetti a 2-3 cifre nel finale, tree remoto e secondo fetch in gasmerge — verifica esterna #126 V-1/V-2/V-3, review #155
dd15215 chore(revisore): memoria review #155 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `4babba9` (solo test): review #155, incollata per intero. Unica aggiunta: il marker `# gasmerge-ip-ok` sulla riga con l'IP di esempio, richiesto dal gate IP su reports/.

### Review 155

## VERDETTO: APPROVATO CON RISERVE

Review #155. Ho letto CLAUDE.md (sez. 1/5/8/10), le righe 15-19 e 65 di reports/stato_progetto.md e la memoria fino alla #154. Il diff staged contiene solo test: tests/test_unit_gasmerge.py (+45/-1) e tests/test_unit_hooks.py (+14). Nessuno script è modificato.

**Elementi del diff esaminati**

- `tests/test_unit_gasmerge.py:63`: aggiunge il parametro `on_watch` allo stub gh, interpolato nel ramo `*"--watch"*` prima dell'`exit`.
  - Rischio: rompere gli altri test, o un'interpolazione shell fragile.
  - Con il default `""` resta una riga vuota nel case, che bash accetta. L'unico uso quota il path.
  - Se il push di on_watch fallisse, il test fallirebbe. Non può quindi dare un falso verde.
  - Esito: ok.
- `tests/test_unit_gasmerge.py:483` `test_branch_locale_pulito_non_maschera_origin_con_ip`: il branch locale viene resettato pulito mentre origin contiene l'IP.
  - Rischio: test che non discrimina.
  - Ho ricostruito la mutation `refs/remotes/origin/$BRANCH^{tree}`→`refs/heads/$BRANCH^{tree}` (`scripts/gasmerge.sh:94`): dà 2 failed, tra cui questo test.
  - L'asserzione testuale `"--- FILE DI MOTORE ---" not in stdout` dimostra che lo script si ferma al gate. Non si basa solo su rc≠0, come chiede la lezione #150.
  - Esito: ok.
- `tests/test_unit_gasmerge.py:503` `test_push_durante_attesa_ci_visto_dal_gate`: un clone terzo pusha un IP durante il `--watch`.
  - Ho ricostruito la mutation che sostituisce con `:` il secondo `git fetch --prune` (`scripts/gasmerge.sh:79`): 1 failed, ed è proprio questo test.
  - Esito: ok.
- `tests/test_unit_hooks.py:2136` `test_finale_4o_ottetti_a_piu_cifre_bloccano`.
  - Ho ricostruito in sequenza, con uno script Python a sostituzione esatta, la mutation `{1,3}`→`{1,2}` sul 4° ottetto di ciascuna regex di `scripts/fine_task_finale.sh` (:72, :85, :96): 3 failed per ogni regex (i casi .200, .127, .255).
  - Sul 3° ottetto della :96: 1 failed (il caso 10.0.100.200).  # gasmerge-ip-ok
  - Il caso `10.20.30.40` non uccide nessuna mutation `{1,2}`: è un controllo positivo innocuo.  # gasmerge-ip-ok
  - I marker `gasmerge-ip-ok` stanno solo sulle righe sorgente, non nei byte scritti. Il gate IP sul tree staged trova 0 residui.
  - Esito: ok.
- Suite riprodotte: test_unit_gasmerge.py 45 passed; test_unit_hooks.py -k finale 26 passed. scripts/ ripristinati con `git checkout` e verificati puliti dopo ogni mutation.

**Ancore (la domanda dell'operatore)**

Le 12 rimozioni di ancora vanno dichiarate fail-closed. Non vanno fissate con un test. Il motivo è che ogni rimozione allarga una regex, e l'esito del gate è `RESIDUAL = NON_LOOPBACK ∩ UNMARKED`, che cresce o resta uguale qualunque delle 3 regex si allarghi. Quindi nessuna di queste mutation può far passare un IP che oggi viene bloccato. Un test che le uccidesse dovrebbe asserire che "1.2.3.4.5" NON viene segnalato, cioè congelerebbe nei test la lacuna R-155-1 qui sotto. Sconsiglio di scriverlo.

**Riserve**

- **R-155-1 (MEDIA-BASSA, preesistente, fuori dal diff, verificata con una sonda).** L'ancora di coda `([^0-9.]|$)`, in entrambi gli script, fa passare un IP seguito dal punto di fine frase: `connect to 8.8.8.8.` dà 0 match. Nella prosa dei report/md è un caso realistico. Oggi nel tree di HEAD ci sono 0 occorrenze non-loopback.  # gasmerge-ip-ok
  - Fix proposto, da fare in una micro-fetta: coda `([^0-9.]|\.([^0-9]|$)|$)` (e simmetrica in testa), più un test "IP a fine frase blocca" in entrambi gli script. Va da tracciare in stato_progetto.md.
- **R-155-2 (operativa, da fare PRIMA del commit).** Il branch corrente è `codex/tradegasfx-redesign`, non `test/gate-ip-ottetti-ref-tree`. Entrambi puntano a `0221462`, quindi `git switch test/gate-ip-ottetti-ref-tree` si porta dietro lo staged e le modifiche non staged. Committando adesso, il commit finirebbe sul branch della sessione Codex.
- **R-153-2** (mktemp BSD) resta aperta, fuori dal diff.

**Rischi esclusi**

- Comportamento su Linux/glibc in CI: non verificato, ho eseguito solo su macOS.
- Non ho rilanciato l'harness completo (92/12) dell'operatore. Ne ho riprodotto il sottoinsieme che corrisponde alle 3 riserve: 6 mutation, tutte uccise dal test nominato.
- Ho ignorato le modifiche non staged a reports/*.md della sessione Codex.

**Memoria**

Ho aggiunto in coda a /Users/gas/Gas/.claude/agents/memoria_revisore.md la riga #155 e due lezioni: sondare cosa esclude un'ancora prima di dichiararla equivalente, e verificare il branch corrente contro quello dichiarato.

**NON ho eseguito** `bash scripts/commit_memoria_revisore.sh`. Lo script committa sul branch corrente, e adesso è quello di Codex (R-155-2). L'agente principale deve:
1. eseguire `git switch test/gate-ip-ottetti-ref-tree`;
2. lanciare `bash scripts/commit_memoria_revisore.sh` da solo (nota #154: dopo un cambio dello staged il gate blocca i comandi che contengono "git");
3. eseguire `bash scripts/segna_review_ok.sh` e poi committare il diff dei test.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py / brains / modules. Solo tests/.

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e` (nella worktree, venv di `~/Gas`): 314 → **320 passed in 110.02s**.
- Mutation in sequenza (harness `mut_sweep.py` esteso): **92 KILLED, 12 SURVIVED**. Sopravvissute: `re{1,2,3}_noPre` e `re{1,2,3}_noSuf` in entrambi gli script (rimozione delle ancore, fail-closed secondo la review #155). Uccise le nuove: `tree_ref_locale`, `fetch2_off` (gasmerge), `re{1,2,3}_ott{3,4}_12` (finale). Ripristino: "scripts/ pulito".

## §6 STATO CI

Output di `gh run list -L 3` alla scrittura:

```
in_progress		test(gate-ip): ottetti a 2-3 cifre nel finale, tree remoto e secondo …	CI	test/gate-ip-ottetti-ref-tree	push	37298048052	17s	2026-10-05T10:40:14Z
completed	success	Merge pull request #126 from Gasss23/test/gate-ip-passata-mutation	CI	main	push	37237913740	1m14s	2026-10-04T21:53:53Z
completed	success	docs(gate-ip-mutation): fine-task — passata unica di mutation sul gat…	CI	test/gate-ip-passata-mutation	push	37231659606	1m9s	2026-10-04T20:19:36Z
```

Mappatura commit → run:
- `4babba9`: run 37298048052 (push di `dd15215` + `4babba9`, testa l'albero di `4babba9`), in corso alla scrittura. Atteso: unit-suite verde, handoff-check rosso (handoff non ancora nel diff a quel SHA).
- `dd15215`: nessuna run su questo SHA (pushato insieme a `4babba9`; il suo contenuto è incluso nell'albero testato da 37298048052).
- Commit di fine-task (contiene questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-155-1 (MEDIA-BASSA)**: IP seguito dal punto di fine frase non visto dal gate IP (entrambi gli script).
- **R-155-2**: risolta senza toccare il branch di Codex: la fetta è stata spostata nella worktree `.claude/worktrees/gate-ip-ottetti` sul branch `test/gate-ip-ottetti-ref-tree`; i commit `dd15215` e `4babba9` stanno lì.
- **R-155-3 (operativa, nuova)**: nella worktree l'hook `review_gate.sh` non ha bloccato un `commit --dry-run` senza marcatore (legge lo stage di `CLAUDE_PROJECT_DIR` = `~/Gas`). Review #155 presente comunque sullo stesso diff.
- **R-153-2 (bassa)**: mktemp BSD in gasmerge.sh. **Latin1 su glibc** non provato. **R-150-1 (bassa)**: ramo `PUSH_EXIT` morto.
- Limite noto del gate IP: cieco a UTF-16 e a IP spezzati o codificati.
- V-3 / V-5 verifica #121: decisione operatore. R-143-2 (ci.yml dalla PR) → V-B vera.

### Verdetto INTEGRALE della verifica esterna PR #126 (handoff `7689c90`)

Uniche aggiunte al testo: questa intestazione e il marker `# gasmerge-ip-ok` in fondo alle righe che contengono un IP di esempio.

VERIFICA ESTERNA PR #126 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad (`.../scratchpad/vclone`, da /Users/gas/Gas), checkout di 7689c907f7bd590a4121b19adbc9b10c7101992f. Coincide con headRefOid della PR (gh). Merge-base con main: eeaaf1b.
Ho eseguito:
- Diff, `git log` e `git diff --stat` reali dalla base. Ho letto per intero il diff dei test, di stato_progetto, ultimo_report e memoria_revisore, e i blocchi del gate IP di gasmerge.sh e fine_task_finale.sh.
- pytest (senza kernel e senza e2e, venv di /Users/gas/Gas) alla base e al commit.
- Un MIO harness di mutation indipendente (`scratchpad/v126/mut.py` e `mut2.py`; NON ho usato il `mut_sweep.py` dell'agente). Ha 56 definizioni di mutation (A–J) più una matrice di restringimenti `{1,3}`→`{1,2}` per ogni ottetto di ogni regex, 24 mutation. Sono girate una alla volta sui test del commit: tutto `tests/test_unit_gasmerge.py` per gasmerge, `-k Finale` per fine_task_finale.
- Sonde di merge/finale sui mutanti che sopravvivono.
- gh: run, check, ruleset.
Il repo reale non è stato toccato: `git status` mostra solo `.agents/`, `.codex/`, `AGENTS.md`, già non tracciati prima. Il clone è pulito a fine verifica. Nessuna sonda è nel repo.

CLAIM VERIFICATI
- §2, set di file: VERO. I 7 file coincidono con `git diff --stat eeaaf1b..7689c90`. I conteggi reali sono 221+/169-, e handoff.md è 288 righe toccate; il NB dell'handoff li dichiara non esatti (cosmetico).
- §3, log: VERO. I tre commit 1f29fc8, a3ac340, c2c2d3e coincidono con `git log`, più 7689c90 escluso per costruzione. Anche i commit della PR via gh sono questi quattro.
- Nessuno script e nessun ci.yml toccato, nessun gate indebolito: VERO. Il diff è solo tests/, reports/ e memoria_revisore.
- Test 303 → 314: VERO. Ho riprodotto 303 passed alla base e 314 passed a 7689c90 (88.8s).
- CI:
  - VERO la run 37231493425 su c2c2d3e: unit-suite success, handoff-check failure (atteso, handoff assente dal diff).
  - La run 37231659606 su 7689c90 ora ha unit-suite e handoff-check pass. Il §6 dice che non è disponibile: superato (cosmetico).
- Ruleset main-lock (via gh): VERO. È active, i required sono unit-suite e handoff-check, policy strict, 0 approvazioni.
- Il verdetto #125 incollato nel §7: VERO. L'ho confrontato riga per riga con `scratchpad/ve125.md` (output del verificatore #125). L'unica differenza nel testo è il marker `# gasmerge-ip-ok` su una riga, come dichiarato. Va aggiunta una cosa che il testo non dice: sono aggiunte anche la riga finale "Esito: …" e l'intestazione (cosmetico).
- Il 6° claim del handoff (kill) non è riprodotto per intero, vedi "NON VERIFICATO". Le mutation che la PR dichiara chiuse sono VERE sui miei casi:
  - V-1 #125: `exit 1` tolto dal ramo RESIDUAL di gasmerge, ucciso (`test_ip_outside_reports_blocks`, ex 37/37 verdi).
  - V-2 #125: sed senza `g`, ucciso in entrambi gli script (gasmerge: `test_due_loopback_sulla_stessa_riga_passa`; finale: 4m).
  - R-153-1: `IFS=`/`-r` del `read` e riga ripulita al posto dell'originale, tutti uccisi.
  - Le mutation su `-a`, `LC_ALL=C`, `-Fx`/`-F`/`-x`, `--and --not`, marker, `1)`→`1|2)`, `exit 1` dei rami UNMARKED e filtro: uccise in entrambi gli script. Totale 61 KILLED nel mio sweep principale e 18 su 24 nella matrice degli ottetti.
- Chi controlla il controllore: nessun gate indebolito, nessuno script cambiato; il marker `gasmerge-ip-ok` sta sulla riga sorgente del test, non nel contenuto scritto nei repo di prova (gate IP sul tree: 0 residui).

FINDING
- V-1 (MEDIA) — `fine_task_finale.sh`: le regex del gate IP possono perdere gli IP con terzo o quarto ottetto a 3 cifre, e nessun test lo nota. La PR presenta il gate come coperto "66/66".
  - Mutation `{1,3}`→`{1,2}` sul terzo ottetto e sul quarto, in ciascuna delle tre regex (righe 72, 85, 96 di `scripts/fine_task_finale.sh`): 6 SURVIVED (22 passed nei test Finale). Il primo e il secondo ottetto sono uccisi; gasmerge uccide tutte e 12.
  - Sonda riprodotta: sul mutante "quarto ottetto della prima git grep → `{1,2}`", sul repo `host 10.0.0.127`, `192.168.1.127`, `8.8.8.100`, `10.20.30.255`, ciascuno in un file del branch → il finale PASSA e arriva a "=== Push ===" (4/4). Sull'originale: 4/4 STOP.  # gasmerge-ip-ok
  - Causa: i test del finale (4/4b…4n) usano solo IP con ottetti a 1 cifra o prefissi 10.x/192.168.x/x. Il test gemello di gasmerge ha `192.168.1.100`, e per questo gasmerge uccide la stessa mutation.  # gasmerge-ip-ok
  - Fix: un test parametrizzato in finale con `10.0.100.200` o simile (terzo e quarto ottetto a 3 cifre), idealmente anche con ottetto a 2 cifre.  # gasmerge-ip-ok
  - Preesistente, non una regressione della PR. Ma contraddice il claim di copertura sistematica ("66/66").
- V-2 (BASSA/MEDIA) — gasmerge: il tree dell'IP è risolto da `refs/remotes/origin/$BRANCH^{tree}` senza test che lo distingua da un ref locale. La mutation → `refs/heads/$BRANCH^{tree}` SOPRAVVIVE (43 passed).
  - Sonda: con branch locale `feat` ripulito (reset `HEAD~1`) e `origin/feat` che contiene `gw 8.8.8.8` non marcato: sull'originale BLOCCO; sul mutante gasmerge supera il gate IP e resta in attesa di input (la sonda è andata in timeout a 100s, quindi non ho catturato l'output di "--- FILE DI MOTORE ---" né di merge). In pratica gate fail-open verso un ref locale diverso da quello che viene mergiato.  # gasmerge-ip-ok
  - Fix: un test con ref locale e remoto diversi (locale pulito, remoto con IP) → BLOCCO.
- V-3 (BASSA) — gasmerge: sopravvive la rimozione del secondo `git fetch --prune origin >/dev/null` dopo l'attesa CI (43 passed). Il commento nello script lo giustifica: dopo ~900s i ref sono stale e IP/file-motore leggerebbero lo stato vecchio. Manca un test che lo provi (un push al branch durante l'attesa CI).
- V-4 (BASSA) — non c'è nessun test che distingua le ancore dei quattro punti: prefisso/suffisso `(^|[^0-9.])…([^0-9.]|$)` tolto dalle 3 regex, sed senza ancora, sed limitato a `127\.`. Sono tutte allargamenti o mutation quasi equivalenti: fail-closed o neutre (falsi positivi su stringhe tipo "1.2.3.4.5"), quindi non sono un bypass. Il handoff elenca "regex ristrette" come uccise, ma il caso "allargate/ancore" non è coperto. Non rischioso.  # gasmerge-ip-ok
- V-5 (COSMETICA) — handoff §6: la run del commit di fine-task (37231659606) è ora verde e il testo dice "non disponibile".
- V-6 (COSMETICA) — handoff §4 dice "Unica aggiunta al testo: il marker" per il verdetto #125, ma c'è anche la riga "Esito:".
- Nota di metodo: alcune mutation del mio harness sono equivalenti o malformate e non le conto: `C3` (regex sed mal costruita), `I4`/`I6` (identità e `0|1` dietro `1)` del case), `J1` (`printf '%s'` vs `'%s\n'` con file vuoto), `H7`/`J3` (test di `-z` sulla sola prima riga). L'unica R-153-2 (mktemp BSD, preesistente) l'ho solo letta: è confermata dalla loro stessa nota.

NON VERIFICATO
- Il numero 66/66 e il loro harness `mut_sweep.py`: non rilanciato. Ho usato un harness mio, con 80 mutation in tutto, per giudicare la copertura, e ne ha trovate 8 sopravvissute non equivalenti. Non so quante delle loro 66 coincidano con le mie.
- Il verdetto del revisore (#153/#154) e che "28/28 KILLED": i numeri e le mutation li ho riprodotti a campione (stessa classe: read_noIFS, read_noR, print_stripped, `1|0)`), ma non il testo.
- Comportamento di GNU grep/sed/read su glibc (latin1, `LC_ALL=C`): non provato (no Docker/GNU locale). La CI ubuntu lo vede solo passare.
- Il merge reale con gasmerge non lanciato. L'esito della sonda V-2 (post-gate) è dedotto dal timeout, non da output.

RACCOMANDAZIONE
La PR #126 è mergiabile: il lavoro dichiarato è vero e riprodotto (314 passed, CI verde su 7689c90, solo test, nessun gate indebolito, V-1/V-2/R-153-1 della #125 chiusi con prova). Ma non vada presentata come "gate IP coperto sistematicamente (66/66)". Prima di dichiarare chiusa la passata di mutation, in una micro-fetta:
1. Chiudere la V-1 (MEDIA): test del finale con IP a 3 cifre sul terzo e quarto ottetto.
2. Test di tree-remoto-vs-ref-locale in gasmerge (V-2) e, se si vuole, il secondo fetch (V-3).
3. Aggiornare §6 (V-5).
Restano aperte: R-153-2 (mktemp BSD), latin1 su glibc, R-150-1; le decisioni V-3/V-5 della #121 sono dell'operatore. Prima del lavoro su V-B / gasmerge variante B conviene che la passata di mutation includa anche gli ottetti e il ref del tree, visto che il passaggio a merge autonomo rende questi gate l'unico controllo.
