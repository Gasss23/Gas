# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — Il gate protegge se stesso + verifica esterna strutturata, branch `fix/gate-autoprotezione`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #119 (https://github.com/Gasss23/Gas/pull/119), dopo aver letto la verifica esterna. Variante A: l'agente lancia `gasmerge 119`, l'operatore conferma digitando `119`.
2. R-138-5: allargare il perimetro di review a `gas_identity.md`, `knowledge/sources.yaml`, `tools/ingest_knowledge.py`, `clients/voice/`, `requirements*.txt`?

---

## §1 SCOPE & ESITO FETTE

Questa fetta viene dalla verifica esterna della PR #118: la sessione Verificatore e la chat claude.ai hanno dato finding concordi.

- **V-1 — il gate non proteggeva se stesso**: `FATTA` (perimetro di review unico).
- **R-138-1 — il perimetro poteva togliersi da solo**: `FATTA` (unione di voci cablate, working tree, index e HEAD/base).
- **V-2 — citazioni non verificate fuori perimetro**: `FATTA`.
- **R-136-5 — bastavano citazioni di .md**: `FATTA`.
- **R-138-2 — rename e nomi non-ASCII**: `FATTA`.
- **R-138-4 — test del gate non in CI**: `FATTA`.
- **R-138-6 — promemoria post-compact**: `FATTA`.
- **V-3 — gate B non bloccante**: `FATTA` (`handoff-check` required nel ruleset, autorizzato dall'operatore).
- **Blocco della review #139 — exit code di git perso nella pipeline**: `FATTA` (corretto prima del commit, con test).
- **Verifica esterna strutturata**: `FATTA` (protocollo fisso più un agente nuovo a ogni verifica).
- **R-136-2 / R-138-3 / R-139-1 — formati alternativi del verdetto**: `DEFERITA — mitigata` (regex più forma canonica; restano tabella e voce di elenco).
- **R-138-5 — perimetro più largo**: `DEFERITA — decisione operatore (§0.2)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 .claude/agents/revisore.md         |   7 +-
 .claude/commands/fine-task.md      |  18 ++
 .claude/hooks/review_gate.sh       |  77 ++++++--
 .claude/perimetro_review.txt       |  26 +++
 .claude/settings.json              |   2 +-
 .claude/verifica_esterna.md        |  50 +++++
 .github/workflows/ci.yml           |  13 +-
 CLAUDE.md                          |   5 +-
 reports/diff_sessione.md           |  26 +--
 reports/handoff.md                 | 394 +++++++++++++++++++++----------------
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           |  34 ++--
 scripts/check_verdetto.py          | 113 ++++++++---
 tests/test_unit_handoff_check.py   | 127 +++++++++++-
 tests/test_unit_hooks.py           | 112 +++++++++++
 16 files changed, 776 insertions(+), 240 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
112f8af fix(gate): il gate protegge se stesso + verifica esterna strutturata — review #138/#139/#140 APPROVATO CON RISERVE
f33be38 chore(revisore): memoria review #140 — APPROVATO CON RISERVE
59d8a75 chore(revisore): memoria review #139 — BOCCIATO
72c9364 chore(revisore): memoria review #138 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `112f8af`, tre verdetti in sequenza, tutti incollati per intero:
- #138 sul primo diff;
- #139 sul delta, BOCCIATO;
- #140 sul fix del blocco.

Le righe di avviso aggiunte dall'harness al rientro del subagente non fanno parte dei verdetti e sono state omesse.

### Review 138

## VERDETTO: APPROVATO CON RISERVE

Review #138, branch fix/gate-autoprotezione, diff staged (9 file, +315/−31). Ho letto CLAUDE.md (sez. 3, 5, 8, 10), lo stato del progetto (riserve R-136-x/R-137-x aperte) e la memoria del revisore, e ne ho applicato le lezioni #136 e #137. Dove la #137 lo richiede, le sonde sono state scritte in file.

La fetta va nella direzione giusta e chiude davvero il caso V-1 *non avversario*: un commit di soli file del gate ora richiede la review. Chiude anche V-2 e R-136-5. Non chiude però l'auto-protezione dichiarata nel titolo: il perimetro, letto dal working tree, può togliere se stesso dalla lista. In più restano due by-pass preesistenti (rename, nomi quotati) che la domanda (a) chiedeva esplicitamente. Nessuno dei due indebolisce il gate rispetto a main: le misure sotto lo dimostrano, quindi non è un blocco. R-138-1 e R-138-2 vanno però chiuse prima di dichiarare "il gate protegge se stesso".

### Misure riprodotte
- pytest senza kernel: **259 passed** (riprodotto). Le suite toccate fanno 94 passed.
- Mutation in un worktree usa-e-getta, poi rimosso; il repo reale non è stato toccato. Tutte e 5 uccise:
  - H1: controllo del working tree solo sul motore → 1 test fallito (V1c);
  - H2: controllo dello staged solo sul motore → 2 falliti (V1a/V1b);
  - C1: regex vecchia → 2 falliti (r136_2);
  - C2: R-136-5 disattivata → 1 fallito;
  - C3: V-2 annullata → 2 falliti.

### Elementi del diff esaminati
1. `.claude/hooks/review_gate.sh:67` — legge il perimetro da `$(dirname $0)/../perimetro_review.txt`, cioè dal **working tree**. Rischio esaminato: il perimetro si esclude da solo. Esito: **riserva (R-138-1)**.
   - Sonda P7: perimetro in stage che toglie sé stesso e `gas.py`, più `gas.py` modificato in stage, senza marcatore → **rc=0**.
   - Sonda P8: perimetro manomesso **fuori stage** (ridotto a `brains/`), `gas.py` in stage senza marcatore → **rc=0**. La manomissione non entra mai in un commit, quindi nessuno la vede in un diff.
   - Il caso che restringe il perimetro ma tiene la riga di sé stesso (P7b) → rc=2, corretto.
   - L'header (righe 18-20) dichiara solo l'hook manomesso, non i dati del perimetro.
2. `.claude/hooks/review_gate.sh:94` e `:115` — `git diff --cached --name-only` confrontato con la ERE del perimetro. Rischio esaminato: rename e nomi quotati. Esito: **riserva (R-138-2, preesistente)**.
   - P1 `git mv modules/x.py docs/x.py` → name-only elenca solo `docs/x.py` → **rc=0**. Stesso esito per P1b `gas.py → docs/`.
   - P2 `modules/città.py` e P2b `modules/a"b.py` arrivano come `"modules/citt\303\240.py"` → l'ancora `^` non li vede → **rc=0**.
   - L'hook di HEAD dà rc=0 negli stessi casi: nessuna regressione, ma è proprio il punto (a).
   - Fix: `git -c core.quotePath=false diff --cached --name-only --no-renames -z`. Stessa cosa in `_session_files` di check_verdetto.py:88.
3. `.claude/hooks/review_gate.sh:105` — il controllo del working tree ora usa i pathspec del perimetro. Rischio esaminato: la sonda V1c del Verificatore e la cancellazione del perimetro. Esito: **ok**.
   - P5 `git rm --cached perimetro_review.txt` → rc=2: la riga `??` blocca.
   - P5 `git rm` → rc=2: perimetro assente, fail-closed.
   - P3 `Modules/evil.py` su FS case-insensitive → l'index normalizza a `modules/` → rc=2.
   - P4: un file del perimetro trasformato in symlink → rc=2.
   - Residuo basso: una volta committato quel symlink, il suo target fuori dal perimetro (`docs/altro.sh`) si modifica senza review (P4b rc=0). Servono due passi e il primo passa dal revisore.
4. `scripts/check_verdetto.py:97` — nuova `_VERDETTO_RE`. Rischio esaminato: falsi positivi e falsi negativi sui verdetti reali, punto (b). Esito: **riserva (R-138-3)**.
   - Su **143 §4 storici distinti**, 29 cambiano numero di blocchi e **3** producono blocchi nuovi con meno di 2 citazioni: falsi positivi fail-closed. Esempi: `**APPROVATO**\n\n---`, e `> **APPROVATO CON RISERVE**` in testa a una citazione.
   - Apre un verdetto anche su `Approvato il fix precedente, ma…` e su righe dentro i code fence.
   - Resta **fail-open** su `Verdetto finale: APPROVATO`, `- **Verdetto**: APPROVATO`, `| VERDETTO | APPROVATO |`, `Esito della review: BOCCIATO`, `Review #139 — APPROVATO`. Quindi **R-136-2 resta MITIGATA, non CHIUSA**.
   - Conflitto di processo: `.claude/agents/revisore.md:62` impone di riportare il verdetto nullo nel report. Il test `tests/test_unit_handoff_check.py:526` dimostra che una riga nuda `APPROVATO — …` diventa un blocco a 0 citazioni → exit 1. Ora che handoff-check è required (vedi sotto), la PR diventa immergeabile, a meno di ritoccare il verdetto: è la classe F-verdetto-ritoccato. Serve una forma canonica per riportare un nullo, per esempio una voce di elenco `- verdetto nullo: «…»`, che la regex non apre.
5. `scripts/check_verdetto.py:131` — R-136-5: se nel diff c'è codice, contano solo le citazioni di codice. Rischio esaminato: falsi positivi da file non-doc sempre presenti nel diff (`.gas_history.json`). Esito: **ok**, perché `.gas_history.json` non è tracciato (`git ls-files`).
6. `scripts/check_verdetto.py:223` — V-2: fuori dal perimetro il minimo per verdetto non si applica, ma le citazioni si verificano sempre (il ciclo a riga 239). Esito: **ok**. Mutation C3 uccisa da `tests/test_unit_handoff_check.py:485`.
   - Riserva collegata a R-138-1: `PERIMETRO_FILE` (riga 95) è il perimetro **della PR stessa**. Una PR che si toglie dal perimetro rende gate B non applicabile anche in CI. Fix: unione con `git show <base>:.claude/perimetro_review.txt`.
7. `tests/test_unit_hooks.py:634` (V1c) e `:646` (V1d) — mordono, H1 e H2 uccise. Esito: **ok**.
   - Limite: tutti i test eseguono l'hook del repo reale contro repo temporanei. Non possono coprire P7/P8, perché lì l'hook e il perimetro letti sono quelli del repo reale. Per R-138-1 serve un test che copi hook e perimetro nel repo temporaneo, come ho fatto nelle sonde.
8. `.claude/perimetro_review.txt:6-26` — copertura. Tutti gli script richiamati da hook, comandi, CI e revisore.md sono dentro: ho fatto un grep di `scripts/…` su settings.json, hooks, commands e workflows. Esito: **riserva minore (R-138-5)**.
   - Restano fuori file che cambiano il comportamento runtime o di sicurezza: `gas_identity.md` (system prompt runtime, letto a gas.py:207), `knowledge/sources.yaml` (filtro K4), `tools/ingest_knowledge.py` (FTS e trigger K3-bis), `clients/voice/` (ha una suite CI dedicata), `requirements*.txt`.
   - Erano fuori anche prima. Decidere se allargare il perimetro spetta all'operatore.

### Riserve (da tracciare in stato_progetto.md)
- **R-138-1 (media, nuova superficie)**: il perimetro data-driven si auto-esclude (P7 in stage, P8 fuori stage → rc=0; anche gate B legge il perimetro della PR).
  - Fix nell'hook: unione delle voci di working tree, `git show :` (index) e `HEAD:`, più voci cablate (`.claude/perimetro_review.txt`, `.claude/hooks/`).
  - Fix in check_verdetto: unione con il perimetro della base.
  - Aggiungere test P7/P8 con hook e perimetro copiati nel repo temporaneo.
  - Correggere l'header di review_gate.sh (righe 18-20).
- **R-138-2 (media, preesistente, punto (a))**: rename motore → fuori perimetro e nomi non-ASCII o quotati passano (P1/P2 rc=0, anche con l'hook vecchio). Fix: `--no-renames` più `-c core.quotePath=false` / `-z`, nell'hook e in `_session_files`.
- **R-138-3 (media, operativa)**: falsi positivi e negativi della regex, punto (b), e conflitto con revisore.md:62 sul verdetto nullo. R-136-2 resta MITIGATA.
- **R-138-4 (minore, preesistente)**: `tests/test_unit_handoff_check.py` **non è eseguito in CI**. ci.yml esegue solo kernel, hooks, voice e gate. I test di V-2 e R-136-2 girano solo in locale, anche se il check che proteggono ora è required.
- **R-138-5 (minore, decisione operatore)**: buchi del perimetro elencati al punto 8.
- **R-138-6 (cosmetica)**: `.claude/settings.json:13`, il promemoria post-compact, dice ancora "gas.py/brains/modules/tests". Il file è nel perimetro ma non è stato aggiornato.

### Su (c) V-3
Risulta già chiuso a livello di ruleset. `gh api repos/Gasss23/Gas/rules/branches/main` restituisce `required_status_checks: unit-suite, handoff-check`. Nel working tree c'è anche una modifica **NON in stage** a `CLAUDE.md` (sezione Lucchetto main, "handoff-check required dal 2026-10-03, V-3") che **non fa parte del diff revisionato**: va messa in stage nel commit dei doc. È fuori dal perimetro, quindi non serve una review, ma va detta nell'handoff. Conseguenza: ogni falso positivo fail-closed di gate B (R-138-3) ora blocca il merge.

### Rischi esplicitamente esclusi
- **Esecuzione in CI reale (GitHub Actions) del nuovo check_verdetto**: non verificata, perché le sonde sono locali. Il caso checkout detached e `rev-parse` → "HEAD" è invariato rispetto a main.
- **Comportamento di Claude Code con un hook mancante o rinominato** (per esempio `git mv` dell'hook → comando inesistente → errore non bloccante?): non verificato, non riproducibile senza toccare la configurazione reale. È nel limite dichiarato "l'hook gira dal working tree".
- **`GIT_INDEX_FILE`** (R-137-3): non ri-sondato, è un limite dichiarato.
- **Suite kernel** (`tests/test_unit_kernel.py`): non eseguita, il diff non tocca gas.py, brains/ o modules/.

### Memoria
Riga #138 e 2 lezioni aggiunte a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, committate da sole con `scripts/commit_memoria_revisore.sh` → commit `72c9364`. Index intatto: i 9 file restano in stage. Il diff staged non cambia, quindi un eventuale marcatore resta valido.

### File
Sonde (scratchpad, fuori dal repo), in `/private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/`:
- `sonde_gate.sh`
- `sonde_gate2.sh`
- `sonda_p5.sh`
- `sonda_regex.py`
- `mutazioni.sh`

Codice:
- `/Users/gas/Gas/.claude/hooks/review_gate.sh`
- `/Users/gas/Gas/scripts/check_verdetto.py`
- `/Users/gas/Gas/.claude/perimetro_review.txt`

### Review 139

## VERDETTO: BOCCIATO

**Review #139** (delta dopo la #138), branch fix/gate-autoprotezione, diff staged di 11 file (+479/−39). Ho riletto CLAUDE.md §3/§5/§8, lo stato del progetto e la memoria del revisore, e ho applicato la lezione #80 (fail-closed di review_gate) e la #137 (sonde in file).

Il diff è quasi tutto corretto: R-138-1, R-138-2, R-138-4 e R-138-6 risultano chiuse, con sonde e mutation. Il blocco è **uno solo**, si corregge con una riga ed è già verificato: il fix `-z` ha reintrodotto la regressione fail-open che la review #80 aveva chiuso, proprio nel gate che questa fetta deve irrobustire.

### Motivo bloccante
- **`.claude/hooks/review_gate.sh:112`**:
  - **Cosa fa la riga:** `DIFF_OUT=$(git diff --cached --name-only --no-renames -z 2>/dev/null | tr '\0' '\n')`, poi `GIT_RC=$?` alla riga 113.
  - **Rischio esaminato:** l'hook non ha `pipefail`, quindi `GIT_RC` è l'exit code di `tr`, non di git. Il commento alle righe 106-111 dice ancora il contrario: "catturato FUORI dalla pipeline".
  - **Sonda** (`sonda_pipe.sh`): ho messo in PATH un git finto che fallisce solo su `--name-only`, mentre status e show restano reali; `gas.py` era in stage senza marcatore.
  - **Esito della sonda:**
    - hook di HEAD → **rc=2** ("git diff --cached fallito (exit 128)");
    - hook nuovo → **rc=0**: il commit passa senza review.
  - È una regressione misurata rispetto a main. T-gate-D resta verde solo perché, in "non è un repo", fallisce anche `git status`, cioè un'altra barriera.
  - **Esito: blocco.**
  - **Fix verificato** su una copia dell'hook con il suo perimetro, con la stessa sonda → rc=2 col messaggio corretto:
    ```
    DIFF_OUT=$(git diff --cached --name-only --no-renames -z 2>/dev/null | tr '\0' '\n'; exit "${PIPESTATUS[0]}")
    ```
  - Va aggiunto un test con un git finto in PATH che fallisce solo su `diff --cached --name-only`.

### Elementi del diff esaminati (ok)
1. **`.claude/hooks/review_gate.sh:100-102`** — perimetro come unione di voci cablate, working tree, index (`:`) e HEAD. Rischio esaminato: il perimetro che si auto-esclude (R-138-1). **Esito: ok.**
   - P7 (perimetro in stage che toglie sé stesso e `gas.py`) → rc=2.
   - P8 (perimetro ridotto fuori stage) → rc=2.
   - P5 (`git rm` e `git rm --cached` del perimetro) → rc=2.
   - Mutation: togliere solo le voci cablate (M4) o solo l'unione con HEAD/index (M3) → i test restano verdi. Le due difese sono ridondanti tra loro: la mutazione combinata (M5) è uccisa da `tests/test_unit_hooks.py:673` e `:683`. È difesa in profondità, non un difetto.
2. **`.claude/hooks/review_gate.sh:123`** e **`scripts/check_verdetto.py:87`** — `--no-renames` e `-z`. Rischio esaminato: rename verso fuori dal perimetro e nomi quotati (R-138-2). **Esito: ok.**
   - Sonde P1/P1b (`git mv` di `modules/` e di `gas.py` verso `docs/`) e P2/P2b (`modules/città.py`, `modules/a"b.py`) → tutte rc=2. Con la #138 erano rc=0.
   - P3/P3b (case), P4 (symlink) e P6 (`git rm`) → rc=2.
   - Mutation M1 (senza `--no-renames`), M2 (senza `-z`) e M6 (`_session_files` con i rename) → tutte uccise.
   - Resta il residuo basso P4b: il target di un symlink già committato, se sta fuori dal perimetro, si modifica senza review (rc=0). Era già noto dalla #138.
3. **`scripts/check_verdetto.py:122`** e **`:136`** — `_carica_perimetro` fa l'unione con le voci cablate e con `<base>:.claude/perimetro_review.txt`. Rischio esaminato: una PR che si toglie dal perimetro. **Esito: ok.** La voce cablata del perimetro basta già da sola, la base aggiunge profondità.
4. **`scripts/check_verdetto.py:104`** e **`:110`** — nuova `_VERDETTO_RE` più il mascheramento dei code fence. Rischio esaminato: falsi positivi e negativi sui verdetti reali (R-138-3). **Esito: riserva (R-139-1).**
   - Mutation M7 (fence non mascherato) uccisa.
   - Handoff reali riprodotti con il nuovo check: 77b5edf/49f0c52 → OK con 12 riferimenti; c868bc0/712b7c0 → OK con 25.
   - Ora aprono un verdetto: "Verdetto finale: APPROVATO", "Esito della review: BOCCIATO", "**Verdetto** — APPROVATO".
   - Non aprono più: la prosa "Approvato il…", il fence e `- verdetto nullo: «…»`. Il conflitto della #138 con revisore.md è chiuso.
   - Fail-closed: con il mascheramento dei fence, **8 §4 storici su 143** hanno più blocchi con meno di 2 citazioni. Sono tutti anteriori al formato obbligatorio (dal 2026-07-01 al 2026-09-29). Il caso tipico è un riepilogo finale "VERDETTO FINALE: APPROVATO" dopo un verdetto pieno: diventa un blocco a 0 citazioni.
   - Fail-open residui: `- **Verdetto**: APPROVATO`, `| VERDETTO | APPROVATO |`, "Review #139 — APPROVATO", "**APPROVATO CON RISERVE.** La fix", "**APPROVATO** (review #100)".
   - **R-136-2 resta MITIGATA.** Suggerimento: in revisore.md, vietare il riepilogo "Verdetto finale:" in coda.
5. **`.github/workflows/ci.yml:103-109`** — la suite `test_unit_handoff_check.py` ora gira in CI (R-138-4). **Esito: ok.**
6. **`.claude/settings.json:13`** — promemoria post-compact aggiornato al perimetro (R-138-6). **Esito: ok.**

Doc (`fine-task.md` §4quater, `CLAUDE.md` E e lucchetto, `verifica_esterna.md`): coerenti fra loro. Il ruleset con `handoff-check` required l'avevo già verificato via gh API nella #138.

### Misure riprodotte
- pytest senza kernel: **265 passed**.
- Sonde P1–P8 e mutation M1–M7: riprodotte come sopra, in worktree e repo usa-e-getta poi rimossi (`git worktree list` → solo il repo principale).

### Rischi esplicitamente esclusi
- **Run reale di GitHub Actions** con il nuovo step e con check_verdetto sul checkout della PR: non verificata, le sonde sono tutte locali.
- **Trigger realistico del blocco** (git diff fallito con git status riuscito, per esempio un lock transitorio o un index parzialmente leggibile): non riprodotto, l'ho simulato con il git finto. Il motivo del blocco è la regressione misurata della proprietà fail-closed, non uno scenario d'attacco concreto.
- **Suite kernel**: non eseguita, il diff non tocca gas.py, brains/ o modules/.
- **R-138-5** (allargare il perimetro): è una decisione dell'operatore, non valutata.

### Dopo il fix
Basta una ri-review di delta: la riga 112 e il test con il git finto. Il resto è approvabile così com'è.

### Memoria e repo
- Riga #139 e una lezione aggiunte a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, commit `59d8a75` (index intatto).
- Nel working tree c'è `reports/stato_progetto.md` modificato e **non in stage**: non viene da me, segnalo solo che c'è.

Sonde in `/private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/`: `sonda_pipe.sh`, `mutazioni139.sh`, `mutazioni139_m5.sh`, `sonda_regex2.py`, `handoff_reali.sh`.

### Review 140

## VERDETTO: APPROVATO CON RISERVE

**Review #140**, delta sul BOCCIATO della #139, branch fix/gate-autoprotezione: diff staged di 11 file (+507/−43; rispetto alla #139 il delta è circa +28/−4). Ho riletto CLAUDE.md §3/§5, lo stato del progetto e la memoria del revisore (lezioni #80 e #139). Il motivo del blocco #139 è chiuso: il fix è quello verificato, il test morde davvero e non ci sono regressioni.

### Elementi del diff esaminati
1. **`.claude/hooks/review_gate.sh:113`**
   - **Cosa fa la riga:** `DIFF_OUT=$(git diff --cached --name-only --no-renames -z 2>/dev/null | tr '\0' '\n'; exit "${PIPESTATUS[0]}")`.
   - **Rischio esaminato:** l'exit code di git perso nella pipeline con `tr`, cioè il blocco della #139.
   - **Esito: ok.**
     - Sonda indipendente (`sonda_pipe.sh`, sull'hook in stage = working tree): ho usato un git finto che fallisce **solo** su `--name-only`, più stretto di quello del test, con status e show reali → **rc=2**, messaggio "'git diff --cached' fallito (exit 128)".
     - L'hook di HEAD dà anche lui rc=2, quindi la regressione della #80 è annullata.
2. **`tests/test_unit_hooks.py:710`**
   - **Cosa fa:** `test_gate_r139_git_diff_failure_in_pipeline_blocks` mette in PATH un git finto che esce 128 su ogni `diff` e delega il resto al git reale; con gas.py in stage si aspetta rc=2 e "git diff --cached".
   - **Rischio esaminato:** test decorativo.
   - **Esito: ok, morde.** In un worktree usa-e-getta ho riportato la riga 113 alla versione della #139: il test passa da 1 passed a **1 failed**.
   - Il git finto che fallisce su ogni `diff` è accettabile: il percorso verso lo script dell'hash (che usa `diff`) non viene raggiunto, perché il gate esce prima.
3. **`.claude/agents/revisore.md`** (righe aggiunte nella sezione formato)
   - **Cosa fa:** vieta il riepilogo "Verdetto finale: …" in coda (R-139-1).
   - **Esito: ok, ma solo come mitigazione di processo.** La regex continua ad aprire un blocco su quella forma; la regola evita solo il falso positivo fail-closed.

### Misure riprodotte
- pytest senza kernel: **266 passed**.
- `tests/test_unit_hooks.py`: **70 passed**.
- Worktree di mutation rimosso: `git worktree list` mostra solo il repo principale.

### Riserve (da tracciare in stato_progetto.md)
- **R-139-1 (aperta, MITIGATA):** la regex degli esiti resta fail-open su `- **Verdetto**: APPROVATO`, tabelle `| VERDETTO | … |`, "Review #N — APPROVATO" e "**APPROVATO** (…)". Il vincolo vero resta la prima riga obbligatoria `## VERDETTO:`. **R-136-2 resta MITIGATA**, non chiusa.
- **Cosmetica:** il commento di `review_gate.sh` alle righe 106-112 ripete due volte la stessa spiegazione su PIPESTATUS (il paragrafo "In una pipeline…" e quello "R-139 (blocco)…"). Se ne può togliere uno.
- **R-138-5:** il perimetro non comprende gas_identity.md, knowledge/sources.yaml, tools/ e clients/voice/. Decide l'operatore; la riserva è invariata.

### Rischi esplicitamente esclusi
- **Run reale di GitHub Actions** con il nuovo step `test_unit_handoff_check.py` e il test r139 su ubuntu (dove `command -v git` e il PATH sono diversi): non verificata, ho eseguito tutto in locale su macOS.
- **Il resto del diff** (check_verdetto.py, perimetro, CI, doc) non l'ho ri-verificato riga per riga rispetto alla #139: il delta dichiarato e lo stat (+28/−4) toccano solo hook, test e revisore.md. Le sonde P1/P2/P7/P8 della #139 restano valide per l'hook, che è cambiato solo alla riga 113 e nei commenti.
- **Suite kernel:** non eseguita, il diff non tocca gas.py, brains/ o modules/.

### Memoria e repo
- Riga #140 aggiunta a `/Users/gas/Gas/.claude/agents/memoria_revisore.md` ("nessuna lezione nuova"), commit `f33be38`. Lo script ha committato solo quel file: index intatto.
- `reports/stato_progetto.md` resta non in stage (è tuo, come hai detto).
- Sonde in `/private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/`: `mutazioni140.sh`, `sonda_pipe.sh`.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py, brains/ o modules/: la suite kernel non è stata rilanciata. Test toccati in tests/ (hook e gate): `pytest tests --ignore=tests/test_unit_kernel.py` **247 → 266 passed**, tutti verdi.

## §6 STATO CI

```
completed	success	fix(gate): il gate protegge se stesso + verifica esterna strutturata …	CI	fix/gate-autoprotezione	push	37158948397	1m4s	2026-10-03T22:35:10Z
completed	success	Merge pull request #118 from Gasss23/fix/gate-b-verdetto	CI	main	push	37152670007	1m6s	2026-10-03T20:45:16Z
completed	success	docs(gate-b): fine-task — gate B per-verdetto + marcatore legato al d…	CI	fix/gate-b-verdetto	push	37144827743	1m3s	2026-10-03T18:36:23Z
```

Mappatura commit→run:
- `112f8af`: run **37158948397**, success. È la testa del push che conteneva anche `72c9364`, `59d8a75` e `f33be38` (memoria revisore).
- `72c9364`, `59d8a75`, `f33be38`: nessuna run su questi SHA. Sono commit intermedi dello stesso push, inclusi nell'albero testato.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-139-1 / R-136-2** (MITIGATE): restano fail-open i formati del verdetto `- **Verdetto**:`, tabella, "Review #N — APPROVATO" e "**APPROVATO** (…)".
- **R-138-5** (decisione operatore): file runtime e di sicurezza fuori dal perimetro.
- **Residuo P4b** (basso): il target di un symlink già committato fuori perimetro.
- **R-136-3, R-137-1, R-137-2, R-137-3**: invariate.
- Cosmetica: il commento sulla pipeline nell'hook è ripetuto due volte.
- Da C4b-3: R-c4b3-3, R-c4b3-4, **R-c4b3-5** (prossima fetta motore).
