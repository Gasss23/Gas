# REPORT TASK — 2026-08-19
## Sonda R2 — durabilità memoria su interruzione (design proposal)

Branch: `fix/r2-durabilita-memoria`

---

## DECISIONI UMANE RICHIESTE

1. Approvare / modificare / rigettare la proposta di design R2 (sezione §3) prima di qualsiasi implementazione.
2. Confermare scope: la durabilità di `.gas_history.json` a runtime VPS è inclusa in questa fetta o differita?

---

## §1 — SCOPE & ESITO FETTE

- **Sonda + proposta design R2**: FATTA — vedi §2 e §3.
- **Implementazione**: SALTATA — fuori scope esplicito di questa fetta. Lo scope lo decide il capo.
- **Commit di codice del fix**: SALTATO — zero modifiche al motore, hook, fine-task.md, session_end.sh.

---

## §2 — RISULTATI DELLA SONDA

### 2.1 — Chi scrive `memoria_revisore.md`, quando, in quale flusso

**Autore**: il subagent `revisore` (`.claude/agents/revisore.md`).

**Quando**: alla fine di **ogni** review, dopo aver prodotto il verdetto. La riga contatore
(`#N — YYYY-MM-DD — verdetto — lezione`) viene scritta in coda a
`.claude/agents/memoria_revisore.md` tramite tool `Edit` o `Write` del subagent.
Obbligatorio anche quando la lezione è "nessuna lezione nuova".

**Flusso completo**:
1. L'agente principale invoca il subagent `revisore` sul diff staged.
2. Il revisore legge CLAUDE.md, `reports/stato_progetto.md`, `memoria_revisore.md`.
3. Il revisore analizza il diff, produce il verdetto.
4. Il revisore **scrive** la riga contatore in `.claude/agents/memoria_revisore.md`
   (tool Edit/Write — modifica file locale, nessun commit).
5. Il verdetto torna all'agente principale.
6. Il file rimane modificato **non committato** fino al `/fine-task` passo 4.

**Contesto**: DEV-TIME (sessione Claude Code). Mai scritto dal loop GAS runtime.

**Dove è committato oggi**: `/fine-task` passo 4 (`fine-task.md:153`):
```bash
git add .claude/agents/memoria_revisore.md 2>/dev/null || true
```
incluso nel commit di fine-task insieme ai report.

---

### 2.2 — Chi scrive `.gas_history.json`, quando, a DEV-time o a RUNTIME

**Autore**: il kernel GAS (`gas.py`) tramite il metodo `_save_history()` (`gas.py:418`).

**Call sites** (tre punti, tutti dentro `run_turn`):
- `gas.py:511` — dopo `_compress_history_if_needed` (compressione auto-trigger)
- `gas.py:1548` — dopo ogni batch di tool results (loop agentico, ogni iterazione che esegue tool)
- `gas.py:1552` — dopo la risposta finale dell'assistant (ogni turno completo)

**Contesto**: **RUNTIME** — scritto dal processo GAS in produzione sul VPS a ogni turno
dell'utente. Non è un file DEV-time: Claude Code non lo scrive mai durante lo sviluppo
(a meno che il kernel non venga eseguito localmente per test).

**Meccanismo di scrittura**: atomico (`json.dumps` → tmp file → `os.replace` → `os.fsync`
su file e directory), garantisce che il file sia sempre in stato coerente su disco.

**Snapshot GAS** (nota separata): il metodo `_take_snapshot` (`gas.py:816-817`) include
`.gas_history.json` nello snapshot (`git add -f -- .gas_history.json`) prima di
`git write-tree`, ma questo snapshot è scritto su `refs/gas/snapshots/` (non su nessun
branch di lavoro) e serve per recovery dopo operazioni distruttive, non per durabilità
inter-sessione.

**Dove è "committato" oggi in DEV-TIME**: `/fine-task` passo 4 (`fine-task.md:154`):
```bash
git add .gas_history.json 2>/dev/null || true
```
Il `2>/dev/null || true` rende il passo non-bloccante: se il file non esiste o non ha
modifiche tracked, git non lo staggia silenziosamente. In una sessione dev senza
esecuzione locale del kernel, questo git add è un no-op.

---

### 2.3 — Dove avviene il commit di questi file oggi

| File | Chi committa | Quando | Trigger |
|------|-------------|--------|---------|
| `.claude/agents/memoria_revisore.md` | agente principale (flusso `/fine-task`) | fine sessione, passo 4 | `git add ...` in fine-task.md:153 |
| `.gas_history.json` (DEV) | agente principale (flusso `/fine-task`) | fine sessione, passo 4 | `git add ...` in fine-task.md:154 — no-op se non modificato |
| `.gas_history.json` (RUNTIME VPS) | **nessuno** | — | non viene committato automaticamente durante il runtime |
| `session_end.sh` | **mai** (dal 2026-08-19) | — | hook solo-push, contratto esplicito in session_end.sh:6-9 |

---

### 2.4 — Esiste un "chokepoint" dove il revisore finalizza il verdetto?

**Sì, esiste**: il punto in cui il subagent revisore scrive la riga contatore in
`.claude/agents/memoria_revisore.md` è il **chokepoint naturale** — è l'unico momento
in cui:
- il verdetto è già stato prodotto (non può cambiare dopo),
- il file è già stato aggiornato (la riga contatore è su disco),
- il subagent ha ancora il contesto della review (sa il numero, la data, il verdetto).

Il subagent ha accesso al tool `Bash` (dichiarato nel frontmatter di `revisore.md:4`),
quindi potrebbe eseguire un commit in questo punto.

---

## §3 — PROPOSTA DI DESIGN: commit atomico della memoria al momento del verdetto

### 3.0 — Separazione netta dei due file

**`memoria_revisore.md` e `.gas_history.json` sono file di natura completamente diversa**
e richiedono meccanismi diversi. La proposta che segue li tratta separatamente.

---

### 3.1 — `memoria_revisore.md`: commit al verdetto (il meccanismo proposto)

**Razionale**: oggi `memoria_revisore.md` viene aggiornato dal revisore ma resta
non committato fino a `/fine-task`. Se la sessione si interrompe prima di `/fine-task`,
la riga contatore e le eventuali lezioni nuove vengono perse (esiste solo in working tree).

**Trigger esatto**: alla fine del flusso del revisore, **dopo** aver scritto la riga
contatore in `memoria_revisore.md` (cioè dopo il tool Edit/Write che aggiorna il file),
il subagent revisore esegue:

```bash
git -C "$CLAUDE_PROJECT_DIR" add .claude/agents/memoria_revisore.md
git -C "$CLAUDE_PROJECT_DIR" commit -m "chore(revisore): memoria review #N — [verdetto breve]"
```

**File staged**: SOLO `.claude/agents/memoria_revisore.md`. Mai `git add -A` o `git add .`.
Il commit non tocca nessun file del motore né di report.

**Fail-safe**: il commit viene eseguito con `|| true` (o equivalente) — un fallimento
(es. niente da committare, lock git, repo in stato anomalo) **non** blocca il revisore
né restituisce un errore all'agente principale. Il verdetto è già stato prodotto e
restituito prima del tentativo di commit. Il turno prosegue invariato.

Pseudocodice da aggiungere in `revisore.md` (sezione "DOPO ogni review"):

```bash
# Dopo aver scritto la riga contatore in memoria_revisore.md:
git -C "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" \
    add .claude/agents/memoria_revisore.md 2>/dev/null \
  && git -C "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" \
    commit -m "chore(revisore): memoria review #${NUMERO} — ${VERDETTO}" 2>/dev/null \
  || true   # fail-safe: fallimento commit NON rompe il revisore
```

**Invariante**: se `/fine-task` viene poi eseguito, il `git add .claude/agents/memoria_revisore.md`
del passo 4 non staggia nulla di nuovo (il file è già committato). Il comportamento è idempotente.

---

### 3.2 — Perché questo commit non contraddice la FETTA 1 (session_end non committa)

`session_end.sh` è un hook di infrastruttura che gira **automaticamente** a fine sessione,
in modo non-contestuale (non sa cosa è stato fatto, non ha il numero della review, non ha
il verdetto). Il suo contratto è: non committare mai, solo pushare.

Il commit proposto è invece:
- **esplicito**: eseguito consapevolmente dal subagent revisore,
- **contestuale**: avviene nell'unico momento in cui il contenuto del commit è noto
  (numero, data, verdetto),
- **atomico**: un solo file, un solo commit, messaggio descrittivo con review #N,
- **non delegato all'infrastruttura**: è il revisore che committa la propria memoria,
  non un hook generico.

È lo stesso principio che ha portato a eliminare l'auto-commit da `session_end.sh`:
i commit devono essere espliciti e contestuali, non delegati a hook automatici che
non hanno il contesto per sapere cosa includere.

---

### 3.3 — `.gas_history.json`: DICHIARAZIONE ESPLICITA di esclusione dal meccanismo

**`.gas_history.json` è un file di RUNTIME**. Non è scritto dal revisore. Non viene
modificato durante una normale sessione Claude Code di sviluppo (a meno di esecuzioni
locali del kernel per test).

**Il "commit al verdetto" NON copre `.gas_history.json` per costruzione**. Sarebbe
concettualmente sbagliato: il revisore non sa nulla dello stato della history GAS
runtime, e includere un file runtime in un commit di review-memory mescolererebbe
due domini separati.

**La sua durabilità a runtime è un problema distinto** con due aspetti:

**Aspetto A — sessione dev interrotta prima di `/fine-task`**:
- In DEV: se il kernel è stato eseguito localmente per test, `.gas_history.json` ha
  modifiche in working tree. Se la sessione si interrompe prima di `/fine-task`, quelle
  modifiche vengono perse dal branch (ma il file resta su disco — non è perdita di dati,
  è solo mancanza di persistenza nel repo git).
- Valutazione: il trade-off è già dichiarato esplicitamente in CLAUDE.md sez.3
  ("Trade-off dichiarato: sessione interrotta prima di `/fine-task` non salva
  `.gas_history.json`") e nella riserva R2 del design fix session_end (review #82).
  **Non è una regressione di questa fetta**: era già accettato.

**Aspetto B — runtime VPS (il problema reale)**:
- `.gas_history.json` viene scritto da GAS ad ogni turno. Non viene committato mai
  in modo automatico durante il runtime. In caso di crash del VPS o riavvio forzato,
  l'ultimo `_save_history()` atomico garantisce che il file su disco sia coerente
  (niente corruzione), ma le modifiche non sono nel repo git.
- **Il meccanismo corretto per la durabilità runtime non è un commit al momento del
  verdetto** (che avviene in dev, non in prod) — è uno dei seguenti:
  1. **Snapshot GAS** (`_take_snapshot`, già implementato): lo snapshot include
     `.gas_history.json` via `git add -f` (gas.py:816-817) e lo preserva in
     `refs/gas/snapshots/`. Questo è già il meccanismo di recovery in prod.
  2. **Push periodico dal VPS** (non implementato): un job cron o unit systemd timer
     che esegue `git add -f .gas_history.json && git commit && git push` su base
     temporale (es. ogni ora). Richiede decisione esplicita dell'operatore.
  3. **Backup `.gas_backup/`** (già implementato, `gas backup`): copia locale del db
     SQLite ma non di `.gas_history.json`.

**Proposta per questa fetta**: `.gas_history.json` è **escluso** dal meccanismo
"commit al verdetto". La sua durabilità runtime è un problema separato, già parzialmente
mitigato dagli snapshot GAS. Se si vuole una soluzione completa per il VPS, è necessaria
una decisione operatore (opzioni A2 sopra) in una fetta separata con scope esplicito.

---

### 3.4 — Riepilogo della proposta

| Aspetto | Soluzione proposta |
|---------|-------------------|
| Trigger | Revisore, dopo `Edit/Write` su `memoria_revisore.md`, fine di ogni review |
| File staged | SOLO `.claude/agents/memoria_revisore.md` |
| Commit message | `chore(revisore): memoria review #N — [verdetto]` |
| Fail-safe | `|| true` — fallimento non rompe il revisore né il turno |
| Idempotenza con `/fine-task` | sì — `git add` del passo 4 è no-op se già committato |
| `.gas_history.json` | ESCLUSO — file runtime, meccanismo separato (snapshot GAS già attivo) |
| Contraddizione FETTA 1 | NO — commit esplicito/contestuale vs hook automatico non-contestuale |

---

## §4 — VERDETTO DEL REVISORE (vaglio di completezza, NON review di codice)

Invocato sul design proposto in §3. Nessuna riga contatore aggiunta a `memoria_revisore.md`
(non è una review pre-commit su diff di codice).

---

**VAGLIO INTEGRALE (verbatim)**:

### A) La sonda è completa?

**A1 — I tre call site di `_save_history()` coprono tutti i punti di scrittura?**

Ho verificato direttamente con `grep -n "_save_history" gas.py`. Il grep restituisce esattamente quattro righe: la definizione (`gas.py:418`) e tre call site (`gas.py:511`, `gas.py:1548`, `gas.py:1552`). La sonda è completa su questo punto.

Una piccola imprecisione descrittiva: il report dichiara "tutti dentro `run_turn`", ma `gas.py:511` è in `_compress_history_if_needed`, che è un metodo separato. Viene chiamato da `run_turn` e dalla CLI `gas compress-history`, ma non è "dentro `run_turn`" in senso stretto. Non è una lacuna critica, ma è impreciso: la CLI può invocare `_save_history` via `_compress_history_if_needed` anche fuori dal ciclo agentico. Il file viene comunque scritto in modo atomico in entrambi i casi, quindi non è un rischio di corruzione.

**A2 — La distinzione DEV-TIME vs RUNTIME è corretta?**

Sì. Il file `gas.py:314` assegna `self.db_path = root / ".gas_history.json"` e la scrittura avviene solo dal kernel GAS in esecuzione. In una sessione Claude Code pura (senza `python gas.py` locale), il file non viene modificato dal processo di sviluppo. La distinzione è corretta.

**A3 — Il commento su `session_end.sh` (solo push, mai commit) è verificato?**

Parzialmente. La sonda cita `session_end.sh:6-9` ma non legge quelle righe direttamente — si appoggia a CLAUDE.md sez.3 (aggiornata nella review #82) e al comportamento documentato. CLAUDE.md è la fonte autorevole e la review #82 ha approvato la modifica. La citazione di riga specifica non è stata verificata sul file reale, ma il fatto è corroborato da più fonti concordanti. Non è una lacuna critica.

---

### B) La proposta di design (§3) ha buchi?

**B1 — Il trigger "dopo Edit/Write della riga contatore" è tecnicamente realizzabile?**

Sì. Il revisore ha `Bash` nel frontmatter (il prompt del revisore lo dichiara esplicitamente). Il flusso Edit → Bash(git add && git commit) è compatibile con l'architettura degli agenti.

Un punto di fragilità: la proposta usa `${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}`. `CLAUDE_PROJECT_DIR` non è garantita in tutti i contesti di invocazione del subagent. Il fallback `git rev-parse --show-toplevel` funziona se la cwd è dentro il repo (regola R3), ma se non lo è, restituisce un path sbagliato o un errore. Il `2>/dev/null` nasconde l'errore e il path risultante potrebbe essere una stringa vuota, rendendo il `git -C ""` equivalente a `git -C .` — cwd corrente. Non è un fallimento catastrofico (con `|| true` il commit fallisce silenziosamente), ma è un caso edge non esplicitato.

**B2 — Il fail-safe `|| true` è sufficiente?**

Sostanzialmente sì. Il fail-safe è corretto per la filosofia del progetto (zero crash > potenza). Il caso peggiore è che la riga contatore resti non committata — esattamente lo stato attuale.

C'è però uno scenario intermedio non innocuo: se `git add` riesce ma `git commit` fallisce (es. lock su `.git/index.lock`), il file rimane in staging. Un successivo `git commit` (es. da `/fine-task`) includerà il file già staggiato nel proprio commit, con messaggio di fine-task anziché `chore(revisore): memoria review #N`. Il contenuto arriva comunque (non è una perdita), ma il commit message sarà semanticamente impreciso. Non è pericoloso ma vale dichiararlo.

**B3 — L'esclusione di `.gas_history.json` è giustificata?**

Sì, l'esclusione è giustificata e ben argomentata. Il revisore non tocca mai `.gas_history.json`; includerlo in un `chore(revisore):` sarebbe concettualmente sbagliato.

Una lacuna nel ragionamento al §3.3: lo snapshot GAS viene definito "meccanismo di recovery in prod", ma `_take_snapshot` viene chiamato da `run_command` (e forse `write_file`), non ad ogni turno. Un crash tra due turni senza tool call distruttive non è coperto dallo snapshot. Il §3.3 presenta gli snapshot come copertura più ampia di quanto non siano. È un'imprecisione che non invalida la proposta (il trade-off è già dichiarato in CLAUDE.md sez.3), ma andrebbe esplicitato per non creare aspettative false sulla copertura degli snapshot.

**B4 — La non-contraddizione con FETTA 1 è argomentata correttamente?**

Sì. La distinzione "commit esplicito+contestuale" vs "hook automatico non-contestuale" è esattamente il principio che aveva motivato la review #82. L'argomentazione è interna al progetto e coerente.

**B5 — Il riferimento agli snapshot GAS (gas.py:816-817) è accurato?**

Ho letto le righe direttamente: `gas.py:816` controlla l'esistenza di `.gas_history.json` e `gas.py:817` lo include nello snapshot con `git add -f`. Il meccanismo è reale e già implementato. Il riferimento è factualmente accurato. Vale però il caveat del punto B3: la copertura non è ad ogni turno.

---

### C) Ci sono rischi o lacune non indirizzati?

**C1 — Due review nella stessa sessione, branch in stato anomalo**

**Due review nella stessa sessione**: la proposta non presenta problemi — due commit `chore(revisore): memoria review #N` e `#N+1` sequenziali sullo stesso branch è uno scenario normale. Funziona.

**Branch in HEAD detached**: questo caso non è coperto dalla proposta. Se il revisore viene invocato mentre l'agente principale ha HEAD detached (scenario raro ma possibile, es. dopo un `git checkout <sha>`), `git commit` crea un commit orfano che viene perso al prossimo `checkout`. Con `|| true` il revisore non si blocca, ma la riga contatore resta non committata — comportamento identico a oggi. Non è una regressione, ma è un caso edge non esplicitato nella proposta.

**Conflitti di merge attivi**: se il repo è in stato `MERGE_HEAD`, `git commit` fallisce. Con `|| true` non è bloccante, ma anche qui vale il rischio "file in staging" descritto nel punto B2.

**C2 — Effetti collaterali su CI e gasmerge del commit `chore(revisore):`**

La proposta non affronta questo punto. Osservazioni:

**CI**: ogni commit su un branch di sessione può innescare una run CI via `session_end.sh` push (o push manuale). Un commit `chore(revisore):` tocca solo `.claude/agents/memoria_revisore.md` — nessun file del motore. La CI esegue `unit-suite` che passa banalmente senza modifiche al codice. È un aumento del numero di run CI per sessione (un extra per ogni review), ma non un rischio di falso rosso. Il costo è trascurabile.

**`gasmerge`**: non ha logica speciale per commit di tipo `chore`. Il commit viene mergiato normalmente su main tramite PR. Nessun effetto collaterale.

**Push timing**: la proposta non specifica quando il commit `chore(revisore):` arriva su origin. Il revisore esegue solo `git commit`, non `git push`. Il push avviene quando `session_end.sh` gira (fine sessione) o tramite `/fine-task`. Se la sessione si interrompe dopo il `git commit` ma prima del push, il commit esiste localmente ma non su origin — è comunque un miglioramento rispetto allo stato attuale (riga solo su disco, non committata). Questo dovrebbe essere dichiarato esplicitamente nella proposta come "il commit è locale fino al push di `session_end.sh` o `/fine-task`" per evitare aspettative di durabilità immediata su origin.

---

### Sintesi finale (revisore)

| Punto | Esito |
|-------|-------|
| A1 — call site completi | Solido; piccola imprecisione su "tutti in `run_turn`" (511 è in `_compress_history_if_needed`) |
| A2 — DEV vs RUNTIME | Solido e corretto |
| A3 — `session_end.sh` no-commit | Solido, ben supportato da più fonti |
| B1 — trigger tecnicamente realizzabile | Solido; fragilità minore su `CLAUDE_PROJECT_DIR` vuota → non bloccante con `|| true` |
| B2 — fail-safe `|| true` | Solido; rischio minore di "file staggiato nel commit sbagliato" — da dichiarare |
| B3 — esclusione `.gas_history.json` | Giustificata; **lacuna**: snapshot GAS non coprono tutti i turni, il §3.3 è parzialmente impreciso |
| B4 — non-contraddizione FETTA 1 | Solido, argomentazione coerente |
| B5 — riferimento gas.py:816-817 | Accurato e verificato |
| C1 — HEAD detached | Non coperto; non è regressione ma va dichiarato |
| C2 — CI/gasmerge | Non affrontato nella proposta; effetti non problematici ma il "push timing" andrebbe esplicitato |

**La proposta è strutturalmente solida.** Le lacune sono tutte non bloccanti per l'approvazione del design. Prima dell'implementazione si raccomanda di:

1. Aggiungere una nota al §3.1 che il commit è locale fino al push di `session_end.sh`.
2. Correggere il §3.3 sugli snapshot: precisare che coprono i turni con tool call distruttive, non tutti i turni.
3. Dichiarare il caso HEAD detached come edge escluso (comportamento = identico a oggi, non regressione).

Nessuna di queste correzioni richiede modifica al meccanismo proposto — solo una precisione descrittiva nel documento di design prima che l'implementazione parta.

---

## §5 — Anomalie rilevate durante la sonda

Nessuna anomalia tecnica. Una nota di chiarezza: il commento in `fine-task.md:151`
("inclusi qui per evitare che l'hook SessionEnd li raccolga in un secondo commit
separato") descrive il contratto pre-FETTA 1, ma è ancora accurato come motivazione:
il passo 4 li include per prevenire commit residui da hook, anche se ora l'hook non
committa più — il set completo in un solo commit di fine-task resta il design corretto.
