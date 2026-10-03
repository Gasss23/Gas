# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — Gate B per-verdetto + marcatore di review legato al diff, branch `fix/gate-b-verdetto`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #118 (https://github.com/Gasss23/Gas/pull/118). Variante A: l'agente lancia `gasmerge 118`, l'operatore conferma digitando `118`.

---

## §1 SCOPE & ESITO FETTE

Questa fetta è stata chiesta dalla verifica esterna di C4b-3: niente altro codice motore finché il gate B accetta verdetti vuoti.

- **R-135-4 — esenzione "nessun diff motore" su qualsiasi menzione della frase**: `FATTA`. L'esenzione ora dipende dal diff reale.
- **R-135-1 / R-135-2 — verdetto solo-contesto o vuoto accettato**: `FATTA`. Servono ≥2 citazioni del diff per ogni blocco `VERDETTO:`.
- **R-135-3 — regola delle citazioni in revisore.md**: `FATTA`, approvata dall'operatore.
- **Marcatore `.review_ok` residuo tra sessioni**: `FATTA`. Il marcatore contiene l'hash del diff staged; primo uso reale sul commit `a52f92b`.
- **R-136-1 — `commit -a` / pathspec**: `FATTA`.
- **R-136-4 — hash dipendente dalla config git**: `FATTA`.
- **R-136-2 — verdetto senza riga VERDETTO**: `FATTA` solo per la parte di formato (regola obbligatoria). Il controllo incrociato nel gate è `DEFERITA — riserva mitigata`.
- **R-c4b3-5 — timeout = esito incerto**: `DEFERITA — prossima fetta motore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +
 .claude/agents/revisore.md         |  19 +-
 .claude/hooks/review_gate.sh       |  39 +++-
 CLAUDE.md                          |   2 +-
 reports/diff_sessione.md           |  18 +-
 reports/handoff.md                 | 430 ++++++++++++++++---------------------
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           |  39 ++--
 scripts/check_verdetto.py          |  65 +++++-
 scripts/hash_diff_staged.sh        |  18 ++
 scripts/segna_review_ok.sh         |  11 +
 tests/test_unit_handoff_check.py   |  91 +++++---
 tests/test_unit_hooks.py           |  55 ++++-
 13 files changed, 477 insertions(+), 321 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
a52f92b fix(gate): gate B per-verdetto + marcatore di review legato al diff — review #136/#137 APPROVATO CON RISERVE
a7e8396 chore(revisore): memoria review #137 — APPROVATO CON RISERVE
8ac50d3 chore(revisore): memoria review #136 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `a52f92b` (tocca tests/): la #136 sul primo diff e la #137 sul delta che chiude R-136-1 e R-136-4. Entrambe sono incollate per intero.

### Review 136

# Review #136, branch fix/gate-b-verdetto: fix del gate B e marcatore legato al diff

## VERDETTO: APPROVATO CON RISERVE

**Il commit si può fare.** R-135-1, R-135-2, R-135-3 e R-135-4 sono chiuse, e un marcatore rimasto aperto o vuoto non apre più il gate. Restano due buchi fail-open che ho verificato: R-136-1 sul gate e R-136-2 sulla regex. Non bloccano: il diff è comunque strettamente meglio di prima e il gate è dichiarato best-effort. Vanno però tracciati in stato_progetto.md.

Letture fatte: CLAUDE.md (§5 e §3, gate), stato_progetto.md (F-controlli-auto, R-135-*, R-gjq-1) e memoria_revisore.md (fino a #135). Nessun antipattern del Wall of Shame: il diff non tocca la history né i tool del kernel.

### Elementi del diff esaminati
1. **scripts/check_verdetto.py:178**: l'esenzione ora dipende da `_tocca_motore(session)` e non più dalla frase "nessun diff motore".
   - Rischio: nuovo by-pass testuale.
   - Esito: **ok**. Con il nuovo script ho rifatto il check sull'handoff reale (worktree c868bc0, base 712b7c0). Quel §4 contiene la frase, ma il risultato è OK con 25 riferimenti e rc=0: la frase non esenta più. La mutation M1 (ripristino dell'esenzione per frase) viene uccisa da tests/test_unit_handoff_check.py:443.
2. **scripts/check_verdetto.py:88 e :102-107** (`_VERDETTO_RE`, `_blocchi_verdetto`) e **:186-198** (almeno 2 citazioni nel diff per ogni blocco).
   - Rischio: segmentazione sbagliata.
   - Esito: **riserva R-136-2**, dettagli sotto.
   - Mutation: M2 (tutto il §4 come un solo blocco) uccisa da :428; M3 (reports/ conta) uccisa da :436; M4 (minimo 1) uccisa da :414 e :436.
3. **.claude/hooks/review_gate.sh:72-80** con **scripts/hash_diff_staged.sh:9**: confronta lo SHA-256 di `git diff --cached --binary`.
   - Rischio: marcatore rimasto aperto, marcatore vuoto, commit diverso da quello revisionato.
   - Esito: **ok sui primi due, riserva R-136-1 sul terzo**.
   - Sonda: marcatore giusto → rc=0; marcatore con CRLF → rc=0 (il `tr` lo pulisce); diff cambiato dopo l'`add` → rc=2; binario → hash stabile.
   - Mutation: M5 (accetta qualsiasi marcatore) uccisa da tests/test_unit_hooks.py:570 e :580. M6 (tolgo `-n "$ATTESO"`) sopravvive, ma la condizione è ridondante: un hash vuoto non può coincidere con uno non vuoto.
4. **scripts/segna_review_ok.sh:6-10**: fa `cd` sulla root e rifiuta un hash vuoto.
   - Rischio: marcatore scritto nel repo sbagliato.
   - Esito: **ok**.
   - L'hook chiama lo script con un path assoluto (settings.json:36 usa `$CLAUDE_PROJECT_DIR`), quindi `dirname $0` è affidabile. Se lo script manca, ATTUALE resta vuoto e il commit viene bloccato (fail-closed).

### Le tre domande
**(a) Regex dei blocchi VERDETTO**
- **Falsi negativi, fail-open (R-136-2, verificata con sonda su `_blocchi_verdetto`):** queste righe non aprono un blocco, quindi un verdetto vuoto viene assorbito dal precedente e ne eredita le citazioni:
  - `**Verdetto**: APPROVATO — nessuna lezione nuova` → blocchi=[2];
  - `Verdetto — APPROVATO` → [2];
  - `Esito: APPROVATO` ripetuto → [2].

  Inoltre .claude/agents/revisore.md non impone di scrivere la riga "VERDETTO:". Il paragrafo "Controllo meccanico" la dà per scontata, ma il FORMATO non la chiede.
  Correzione: rendere obbligatoria nel FORMATO la riga `## VERDETTO: <esito>`, e/o aggiungere un controllo incrociato (numero di esiti APPROVATO/BOCCIATO a inizio riga ≤ numero di blocchi).
- **Falsi positivi, fail-closed (R-136-3):**
  - analisi prima della riga VERDETTO, ripetuta due volte → blocchi=[2, 0];
  - una riga "Verdetto: nullo d'ufficio…" dentro l'analisi spezza il blocco → [1, 1].

  Bloccano handoff legittimi e spingono a ritoccare i verdetti (F-verdetto-ritoccato).

**(b) Stabilità dell'hash**
- CRLF nel marcatore, binari e file non tracciati: ok. I file non tracciati non entrano finché non vengono aggiunti con `add`.
- **`git commit -a`: fail-open (R-136-1, verificata).** Con un marcatore valido e una modifica a gas.py non staged nel working tree, queste tre forme danno rc=0:
  - `git commit -a -m x`;
  - `git commit gas.py -m x`;
  - `git add gas.py && git commit -m x`.

  L'hook fa l'hash dell'index nel momento in cui gira, prima che il comando lo modifichi. Questo smentisce la frase aggiunta in CLAUDE.md, secondo cui un diff cambiato dopo la review non apre il gate.
  Correzione possibile: se il comando contiene `-a`/`--all`, un pathspec o `add`, bloccare quando `git diff --name-only` (non staged) tocca il motore.
- **Dipendenza dalla config git (R-136-4):** cambiando la config l'hash cambia (misurato con color.ui=always e con diff.noprefix). Finché la config resta uguale tra marcatore e commit va bene. Con `diff.external` configurato, però, l'output sarebbe quello di un tool esterno. Suggerisco `--no-color --no-ext-diff --no-textconv`, oppure `git write-tree`, che è indipendente dalla config.

**(c) Punti fail-open che restano**
- R-136-1 e R-136-2, descritti sopra.
- Nel gate, il caso grep assente (R-gjq-3).
- In check_verdetto, pre-esistenti: si esce con 0 se il titolo del §4 non viene trovato, se il merge-base fallisce, o se `_session_files` fallisce. In quest'ultimo caso l'insieme resta vuoto e l'esito è "handoff non nel diff".
- Inerente: `segna_review_ok.sh` può essere lanciato senza review. Il marcatore lega il diff, non il verdetto.

**Riserve minori**
- R-136-5 (cosmetica): le citazioni di file di documentazione del diff (es. CLAUDE.md:1) contano come evidenza.
- Il docstring "Exit 1" non cita il nuovo motivo.
- La riga 4 dell'header dell'hook parla ancora solo di "manca".

### Misure riprodotte
- pytest senza kernel: 244 passed. Hooks: 58 passed.
- test_unit_handoff_check + hooks: 79 passed.
- Mutation fatte su una copia con ripristino tramite trap; working tree verificato pulito.
- Nessun riferimento rimasto al vecchio `touch .review_ok` in commands, agents, hooks e scripts.

### Rischio escluso esplicitamente
- **Flusso reale non verificato:** non ho provato il marcatore con l'harness di Claude Code né `fine_task_finale.sh` end-to-end. Il primo uso reale di `segna_review_ok.sh` avviene dopo questo verdetto, quindi non era riproducibile prima.
- **Suite kernel non rilanciata:** test_unit_kernel.py non l'ho eseguito, perché il diff non tocca gas.py, brains/ o modules/.

### Nota di processo
- Due mie sonde e il primo tentativo di aggiornare la memoria sono stati bloccati dal matcher `git[[:space:]].*commit` (R-gjq-1, già nota): il testo della lezione conteneva "git commit". Non è stato eseguito nulla; ho rifatto i passi separati.
- **Ordine dei passi per il marcatore:** crea il marcatore DOPO aver ricevuto questo verdetto e senza toccare l'index nel frattempo. Il commit della memoria non ha cambiato il diff staged.

### Memoria
- Riga #136 e 2 lezioni aggiunte in coda a /Users/gas/Gas/.claude/agents/memoria_revisore.md.
- Committata con `scripts/commit_memoria_revisore.sh` in `8ac50d3`. Lo staging degli 8 file sotto review è intatto.

File rilevanti:
- /Users/gas/Gas/scripts/check_verdetto.py
- /Users/gas/Gas/.claude/hooks/review_gate.sh
- /Users/gas/Gas/scripts/hash_diff_staged.sh
- /Users/gas/Gas/scripts/segna_review_ok.sh
- /Users/gas/Gas/.claude/agents/revisore.md
- /Users/gas/Gas/tests/test_unit_handoff_check.py
- /Users/gas/Gas/tests/test_unit_hooks.py

### Review 137

## VERDETTO: APPROVATO CON RISERVE

# Review #137, seguito della #136 (branch fix/gate-b-verdetto, diff staged)

**Il commit si può fare.** Il delta chiude R-136-1 e R-136-4 e mitiga R-136-2 col formato obbligatorio. Restano aperte R-136-3, R-136-5 e tre riserve nuove minori o operative (R-137-1/2/3, sotto), da tracciare in stato_progetto.md.

Letture: CLAUDE.md §5 e §3, stato_progetto.md (R-gjq-1), memoria (con la #136). Il diff non tocca la history né i tool del kernel, quindi nessun antipattern del Wall of Shame.

### Elementi del diff esaminati
1. **.claude/hooks/review_gate.sh:73-81**: `git status --porcelain --untracked-files=all -- gas.py brains modules tests`, con blocco se c'è `^(.[^ ]|\?\?) `.
   - Rischio: `commit -a`, pathspec o `add && commit` che fanno entrare nel commit codice non revisionato.
   - Esito: **ok, R-136-1 chiusa**. Ho sondato con la versione staged dell'hook su un repo temporaneo:

     | Caso | Esito |
     |---|---|
     | `git commit -a` con gas.py modificato non staged | rc=2 |
     | `git add gas.py && git commit` | rc=2 |
     | cancellazione non staged | rc=2 |
     | solo chmod non staged | rc=2 |
     | commit doc-only con il motore sporco | rc=2 (attrito voluto) |
     | rename staged | rc=0, corretto |
     | solo file ignorati in tests/__pycache__ | rc=0, corretto |
     | working tree ripristinato | rc=0 |

   - Mutation: N1 (controllo disattivato) fa fallire B4, B5 e B6; N2 (solo `??`) fa fallire B4 e B6. I test sono mordaci.
   - Sul repo reale, `git status` del motore dà solo `M ` (staged), quindi il gate non blocca il commit di questo diff.
2. **scripts/hash_diff_staged.sh:10-11**: aggiunti `-c core.quotePath=false -c diff.noprefix=false -c diff.mnemonicPrefix=false` e `--no-color --no-ext-diff --no-textconv`.
   - Rischio: hash che cambia con la config.
   - Esito: **ok, R-136-4 chiusa**. Con `diff.external=/usr/bin/false`, `color.ui=always` e `diff.noprefix=true` impostati nel repo l'hash resta uguale (misurato).
3. **.claude/agents/revisore.md:44**: la prima riga del verdetto deve essere `## VERDETTO: <esito>`, una per verdetto.
   - Rischio: varianti markdown che sfuggono alla segmentazione.
   - Esito: **riserva, R-136-2 MITIGATA e non chiusa**, come dichiarato. Le varianti `**Verdetto**:`, `Verdetto —` ed `Esito:` restano falsi negativi se il produttore non rispetta il formato. Il controllo incrociato resta residuo.
4. **scripts/check_verdetto.py**: il docstring "Exit 1" è aggiornato. **ok**.

### Riserve nuove
- **R-137-1 (minore):** il ramo `WT_RC -ne 0` (git status fallito, fail-closed) non è coperto da test. La mutation N3 non può essere uccisa, perché T-gate-D fallisce prima, su `git diff --cached`.
- **R-137-2 (operativa, estende R-gjq-1):** con il motore modificato e non staged nel working tree, il gate blocca QUALSIASI comando Bash il cui testo contiene "git … commit", anche con niente in stage (es. `git log --grep commit`, commit di soli report). Durante lo sviluppo è più attrito di prima. Il fix resta quello di R-gjq-1: ancorare il matcher.
- **R-137-3 (dichiarata):** un indice alternativo (`GIT_INDEX_FILE=… git commit`) è fuori dal controllo, che legge solo l'index di default. Rientra nei limiti best-effort dell'header.
- Restano aperte **R-136-3** (falsi positivi fail-closed della segmentazione) e **R-136-5** (le citazioni di file doc del diff contano come evidenza).

### Misure riprodotte
- pytest senza kernel: 247 passed. test_unit_hooks: 61 passed.
- Mutation fatte con backup e trap: working tree ripristinato e verificato con `git diff --stat` vuoto.

### Rischio escluso esplicitamente
- **Flusso reale non provato:** la catena `segna_review_ok.sh` → hook invocato dall'harness di Claude Code → commit reale non l'ho eseguita, perché il primo uso reale avviene dopo questo verdetto. Non ho rilanciato `fine_task_finale.sh` end-to-end.
- **Suite kernel non rilanciata:** test_unit_kernel.py, perché il diff non tocca gas.py, brains/ o modules/.

### Memoria
- Riga #137 e una lezione nuova aggiunte a /Users/gas/Gas/.claude/agents/memoria_revisore.md. La lezione: le sonde che contengono il testo "git … commit" vanno passate da un file, altrimenti R-gjq-1 blocca l'intero comando.
- Committata con `scripts/commit_memoria_revisore.sh` in `a7e8396`. L'index sotto review non è cambiato. `reports/stato_progetto.md` risulta modificato e non staged: è fuori dal motore e il gate non lo vede. Puoi creare il marcatore con `bash scripts/segna_review_ok.sh`.

File rilevanti:
- /Users/gas/Gas/.claude/hooks/review_gate.sh
- /Users/gas/Gas/scripts/hash_diff_staged.sh
- /Users/gas/Gas/.claude/agents/revisore.md
- /Users/gas/Gas/scripts/check_verdetto.py
- /Users/gas/Gas/tests/test_unit_hooks.py

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py, brains/ o modules/: la suite kernel non è stata rilanciata. I test toccati sono in tests/ (hook e gate). `pytest tests --ignore=tests/test_unit_kernel.py`: **237 → 247 passed**. Tutti verdi, nessun FAIL fuori scope.

## §6 STATO CI

```
completed	success	fix(gate): gate B per-verdetto + marcatore di review legato al diff —…	CI	fix/gate-b-verdetto	push	37144634767	59s	2026-10-03T18:33:20Z
completed	success	Merge pull request #117 from Gasss23/feat/cancello-c4b3	CI	main	push	37143427141	1m10s	2026-10-03T18:14:11Z
completed	success	docs(c4b3): fine-task — R-135-4 (by-pass testuale del gate B) + CI 82…	CI	feat/cancello-c4b3	push	37142760199	1m3s	2026-10-03T18:03:03Z
```

Mappatura commit→run:
- `a52f92b`: run **37144634767**, success. È la testa del push che conteneva anche `8ac50d3` e `a7e8396`.
- `8ac50d3` e `a7e8396` (memoria revisore): nessuna run su questi SHA. Sono commit intermedi dello stesso push, inclusi nell'albero testato da 37144634767.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-136-2** (MITIGATA): un verdetto senza riga `VERDETTO:` si fonde col precedente. Il formato obbligatorio c'è, il controllo incrociato nel gate no.
- **R-136-3** (fail-closed): falsi positivi della segmentazione dei verdetti.
- **R-136-5** (cosmetica): le citazioni di file doc del diff contano come evidenza.
- **R-137-1** (minore): il ramo "git status fallito" del gate non è coperto da test.
- **R-137-2** (operativa): con il motore sporco, il matcher blocca qualunque comando che contenga "git … commit" (R-gjq-1).
- **R-137-3** (dichiarata): indice alternativo fuori dal controllo.
- Residuo noto: `segna_review_ok.sh` lega il diff, non il verdetto.
- Da C4b-3: R-c4b3-3, R-c4b3-4, **R-c4b3-5** (prossima fetta motore).
