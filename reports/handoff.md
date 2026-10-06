# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — F-mac-1: test di run_command senza sandbox OS + sandbox esigito in CI (sessione cloud notturna, arretrati)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #136 (https://github.com/Gasss23/Gas/pull/136). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756805937","url":"https://github.com/Gasss23/Gas/pull/136"}`): `gh` non è autenticato in questo container.
2. Conferma su macOS reale dopo il merge: `python tests/test_unit_kernel.py` → 0 FAIL.
3. Ordine di merge della notte: i report canonici sono riscritti da ogni PR; dopo un merge le altre vanno riallineate a main.

---

## §1 SCOPE & ESITO FETTE

- **F-mac-1**: `FATTA`.
- **R-173-1 / R-173-2**: `FATTA`.
- **Prova su macOS reale**: `SALTATA — nessun Mac nel container; assenza di bwrap simulata pre-impostando gas._OS_SANDBOX_CACHE`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Verifica esterna §4quater #136**: `FATTA` — APPROVATO CON RISERVE (§8), solo BASSE/COSMETICHE, nessuna correzione al codice.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .github/workflows/ci.yml           |   3 +++
 reports/diff_sessione.md           |  19 ++++++-----------
 reports/handoff.md                 | 417 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  29 ++++++++++---------------
 tests/test_unit_kernel.py          |  26 ++++++++++++++++++++---
 7 files changed, 173 insertions(+), 326 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
2132f4b docs(kernel-skip-senza-bwrap): fine-task — report, handoff con verdetti #173/#175, diff sessione
800bd7f test(kernel): F-mac-1 — senza sandbox OS i test di run_command girano in os_with_fallback, in CI il sandbox è esigito — review #173/#175
7cfef00 chore(revisore): memoria review #175 — APPROVATO
9ca25f2 chore(revisore): memoria review #173 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-mac1/`) resi relativi alla radice del repo, perché il gate B li risolva.

### Review #173 — diff staged del fix

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md, la voce F-mac-1 in `reports/stato_progetto.md` e la memoria del revisore. Il branch corrente è `fix/kernel-skip-senza-bwrap` e coincide con quello dichiarato, con base e91ceb4.

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:63`: l'helper `senza_sandbox_os_usa_fallback` mette `sandbox_mode = "os_with_fallback"` solo se `k.os_sandbox_available` è False.
   - Rischio: che cambi altro nel kernel o scatti anche quando il sandbox c'è. In `gas.py`, `sandbox_mode` si legge solo a :1912. Nel costruttore non c'è nulla che dipenda da questo valore, quindi impostarlo dopo `__init__` è sicuro.
   - Esito: ok.

2. `tests/test_unit_kernel.py:295/:300` (T11c2): verifica che lo snapshot fallito blocchi `run_command` (fail-closed).
   - Rischio: un falso verde.
   - Con bwrap il test resta in os_strict e il diniego arriva dallo snapshot (lo snapshot fallisce perché non c'è un repo git).
   - Senza bwrap gira in fallback e lo snapshot fallito è l'unica barriera prima di `ls -la`. Se si toglie quel controllo, `ls` viene eseguito e il test FALLISCE.
   - Il messaggio di diniego di os_strict a `gas.py:1914-1920` non contiene "snapshot". Quindi l'asserzione non può confondere i due dinieghi.
   - Esito: ok, T11c2 prova ancora il fail-closed dello snapshot in entrambi gli ambienti.

3. `tests/test_unit_kernel.py:352-356` (T12-modo): controlla che il modo sia os_strict se il sandbox c'è e os_with_fallback solo se manca.
   - Rischio: che il ripiego scatti anche in CI. La mutation "helper che passa sempre al fallback" segnalata dall'agente fa fallire T12-modo con bwrap.
   - Esito: ok.

4. `tests/test_unit_kernel.py:358-388` (T12a-e): i comandi che senza bwrap girano davvero sono `wc`, `true`, `grep`, `cat` ed `echo`, con argomenti letterali e cwd in `mkdtemp`.
   - L'env viene ripulito da `_sanitized_subprocess_env`.
   - `cat ../etc_passwd_finto` viene negato al vetting, prima di essere eseguito.
   - In T12d `>` resta un argomento di `cat`, quindi il comando non scrive nulla.
   - Esito: ok, sono innocui. Anzi, senza bwrap T12d è più discriminante: con bwrap anche una shell vera non potrebbe scrivere, perché il filesystem è read-only.

**Riproduzione**
- Con bwrap: `python tests/test_unit_kernel.py` dà **652 PASS / 0 FAIL**.
- Senza bwrap simulato (`/tmp/claude-0/senza_bwrap.py`): **648 PASS / 0 FAIL**.
- La differenza di 4 test sono gli SKIP di T13a/b/c/e.

**Sulle domande poste**
- Far girare questi test in fallback invece di saltarli (SKIP) è coerente con §7 e §9, ed è più onesto. Allowlist, divieto di shell e snapshot sono barriere applicative: su macOS vengono provate davvero invece di sparire.
- Il fail-closed di os_strict resta provato in modo deterministico da T13d (:491-496), che forza `os_sandbox_available=False`.
- Il comportamento a runtime non cambia: il diff tocca solo i test.

**Riserve**

- **R-173-1 (MEDIA-BASSA): la CI perde un allarme.**
  - Prima, se la sonda `_probe_os_sandbox` (`gas.py:220`) avesse cominciato a rispondere sempre False per una regressione, la CI dava 5 FAIL.
  - Ora la stessa regressione dà CI verde: T13a/b/c/e finiscono in SKIP e T11/T12 passano in fallback. L'ho verificato: la simulazione con la cache a False è proprio questa mutation, e dà 648/0.
  - Il controllo in `.github/workflows/ci.yml:221` guarda lo smoke-test, che usa `--unshare-all` e quindi è una sonda diversa da quella del kernel. Gli SKIP finiscono solo nel riepilogo della run (ci.yml:152), non la fanno fallire.
  - Fix suggerito: una variabile d'ambiente impostata dal workflow (es. `GAS_TEST_SANDBOX_OS_ATTESO=1`) e un check del tipo "se è impostata, `OS_SB` deve essere True".

- **R-173-2 (cosmetica):** in `stato_progetto.md` la voce F-mac-1 chiusa conserva ancora la frase "Devono essere SKIP su sistemi senza sandbox OS", che contraddice la soluzione adottata. Va riformulata.

**Rischio escluso:** non ho verificato l'esecuzione su un macOS vero, né l'output dei comandi BSD (`wc` con spazi iniziali, `grep` che non riordina le opzioni). Non è riproducibile in dev; dalla lettura delle asserzioni ("3" contenuto nell'output, output diverso da "3") non dovrebbero dipendere da queste differenze, ma la conferma sul Mac spetta all'operatore.

**Memoria del revisore:** ho aggiunto la riga #173 e una lezione nuova in `.claude/agents/memoria_revisore.md`. L'ho committata con lo script atomico (commit 9ca25f2), che committa solo quel file. Il diff staged è intatto e non è stato committato.

### Review #175 — ri-review R-173-1/2

## VERDETTO: APPROVATO

Le due riserve della #173 sono chiuse. L'allarme della CI torna a scattare se la sonda del kernel smette di vedere il sandbox. Ho riprodotto i tre scenari dichiarati e i numeri coincidono. Il branch è `fix/kernel-skip-senza-bwrap`, come dichiarato.

**Elementi del diff esaminati**

1. `.github/workflows/ci.yml:89`: aggiunge `GAS_TEST_SANDBOX_OS_ATTESO: "1"` solo nell'env dello step "Run unit suite".
   - Rischio: allargare l'effetto ad altri step o indebolire un controllo esistente. L'env vale solo per quello step. Lo step-gate a ci.yml:221 e lo smoke-test restano com'erano.
   - Un guasto del sandbox in CI ora fa diventare rossa la suite con un solo FAIL (T13-atteso), mentre prima erano 5. Lo step-gate continua a distinguere il "rosso da sandbox" dal "rosso da test".
   - Esito: ok.

2. `tests/test_unit_kernel.py:445`: il check T13-atteso pretende che `OS_SB` sia True quando la variabile vale "1".
   - Rischio: un'asserzione che si appoggia sulla stessa sonda che dovrebbe controllare, cioè la lezione della #173. Qui il valore viene dalla sonda del kernel (`_probe_os_sandbox`), mentre l'attesa viene dal workflow, garantita dallo smoke-test. Sono fonti indipendenti, quindi una regressione della sonda viene presa.
   - Riproduzione:
     - con bwrap e variabile: **653 PASS / 0 FAIL**;
     - sonda simulata a False (cache) e variabile: **648 PASS / 1 FAIL**, ed è proprio T13-atteso;
     - senza variabile e senza bwrap (caso Mac): **648 PASS / 0 FAIL**.
   - Esito: ok.

3. `reports/stato_progetto.md`: nella voce F-mac-1 non c'è più "Devono essere SKIP". Ora descrive la soluzione adottata e cita R-173-1. Esito: ok, R-173-2 chiusa.

**Note cosmetiche, non bloccanti**
- Un valore della variabile diverso da "1" (ho provato "true") disattiva il check in silenzio.
- Quando la variabile manca, l'output non mostra nessuna riga SKIP per T13-atteso.
- `ci.yml` fa parte della macchina del bot, quindi la verifica automatica sulla PR farà un COMMENT, non un APPROVE.

**Rischio escluso:** non ho eseguito il workflow su un runner GitHub reale. Che la variabile arrivi davvero al processo Python nello step lo deduco dalla sintassi standard di `env:` dello step; lo confermerà la prima run CI della PR, dove T13-atteso deve risultare PASS.

**Memoria del revisore:** ho aggiunto la riga #175 in `.claude/agents/memoria_revisore.md` e l'ho committata con lo script atomico (commit 7cfef00), che committa solo quel file. Il diff staged dei 3 file non è stato committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules: solo `tests/test_unit_kernel.py` (+2 check: T12-modo, T13-atteso solo con la variabile) e `ci.yml`.

```
con bwrap, GAS_TEST_SANDBOX_OS_ATTESO=1        →  === RIEPILOGO: 653 PASS, 0 FAIL ===
con bwrap, senza variabile                     →  === RIEPILOGO: 652 PASS, 0 FAIL ===
senza bwrap (simulato), senza variabile         →  === RIEPILOGO: 648 PASS, 0 FAIL ===   (origin/main: 642 PASS, 5 FAIL)
senza bwrap (simulato), con variabile           →  === RIEPILOGO: 648 PASS, 1 FAIL ===   (T13-atteso, voluto)
```

## §6 STATO CI

Stato da connettore GitHub e dalla verifica esterna #136 (`gh` non autenticato qui). Mappatura commit → run:
- `9ca25f2`, `7cfef00`, `800bd7f`: pushati insieme → run su `800bd7f`: unit-suite success, handoff-check failure (atteso, handoff non ancora rigenerato).
- `2132f4b` (primo fine-task): unit-suite success, handoff-check success.
- commit di questo fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- macOS reale non provato (conferma dell'operatore dopo il merge).
- V-2 #136 (BASSA): T13-atteso scatta solo con la variabile esattamente "1"; un valore diverso lo spegne in silenzio.
- V-3 #136 (BASSA, dichiarata): su macOS T11c2/T12* provano la sandbox applicativa, il fail-closed di os_strict resta su T13d.
- V-5 #136 / #175 (cosmetiche): senza variabile T13-atteso non stampa SKIP.

## §8 VERIFICA ESTERNA #136 (verdetto integrale)

Lanciata con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 2132f4b> <URL_PR>` (agente nuovo, Sonnet). Nessun finding sopra BASSA: nessuna correzione al codice; V-4 (stat fotografato prima dell'ultimo commit) è strutturale.

VERIFICA ESTERNA PR #136 — APPROVATO CON RISERVE

Metodo: ho clonato il repo in una scratchpad e fatto checkout di 2132f4b (base e91ceb4). Ho rilanciato `tests/test_unit_kernel.py` in quattro scenari più la base, usando un bwrap reale e un wrapper che forza `gas._OS_SANDBOX_CACHE=(False,..)`. Ho controllato diff, ruleset e check-run con l'API REST di gh. Il repo reale resta pulito.

CLAIM VERIFICATI
- §2 diff-stat: VERO nei 7 file e nel segno. Nei conteggi è obsoleto: l'handoff riporta 133+/338-, il reale è 142+/338- (tests +26/-3, handoff.md 398 righe toccate).
- §3 git log: VERO. I tre commit citati ci sono, più il quarto, 2132f4b (fine-task), che l'handoff dichiara di non contenere.
- Delta test, 4 scenari: tutti VERI.
  - Con bwrap e variabile: 653 PASS / 0 FAIL.
  - Con bwrap, senza variabile: 652 / 0.
  - Senza bwrap simulato, senza variabile: 648 / 0, con SKIP di T13a/b/c/e.
  - Senza bwrap simulato, con variabile: 648 / 1 FAIL, ed è T13-atteso.
- Base senza bwrap: 642 PASS / 5 FAIL, come dichiarato (T11c2, T11e, T12a, T12c, T12e). Il fix risolve davvero il problema di partenza.
- R-173-1 CHIUSA: VERO. La mutation "sonda a False" dava 648/0 (verde) senza la variabile e ora dà un FAIL con T13-atteso. L'asserzione usa la sonda del kernel mentre l'attesa viene dal workflow, quindi le due fonti sono indipendenti.
- Il diff non tocca `gas.py`, `brains` né `modules`: VERO. Il runtime è invariato.
- CI sullo SHA 2132f4b: `unit-suite` success e `handoff-check` success. `esito`, `verifica` e `smista` sono skipped. Il ruleset `main-lock` è attivo e richiede esattamente `unit-suite` e `handoff-check`.
- §6 dell'handoff, run di 800bd7f: `unit-suite` success e `handoff-check` failure, come atteso.

FINDING
- V-1 (BASSA): in CI le due garanzie sul sandbox restano due sonde diverse.
  - Lo smoke-test del workflow (`--unshare-all`, BWRAP_OK) e la sonda del kernel `_probe_os_sandbox` sono indipendenti.
  - T13-atteso intercetta solo la regressione della sonda del kernel. Il caso opposto lo prende già il Gate sandbox del workflow.
  - Non c'è un buco, ma ho verificato solo la prima direzione con la simulazione. Non è un blocco.
- V-2 (BASSA): T13-atteso scatta solo se la variabile vale esattamente "1".
  - Se un domani la variabile viene scritta "true" o "True" nel workflow, il check si disattiva in silenzio.
  - Il revisore l'aveva già segnalato come cosmetico, ma sul lato CI è un controllo che sparisce senza errore.
  - Fix proposto: accettare i valori truthy, oppure un check del workflow che fallisca se la variabile non è "1".
- V-3 (BASSA): perdita di copertura del fail-closed di `os_strict` per T11c2 e T12a/c/e.
  - Senza bwrap questi test girano ora in `os_with_fallback`, quindi su macOS non provano più `os_strict`.
  - Il fail-closed è coperto solo da T13d, che forza `os_sandbox_available=False`.
  - È una scelta dichiarata e ragionevole.
- V-4 (COSMETICA): il diff-stat di §2 non coincide con quello reale (133 contro 142 inserzioni), perché è stato generato prima dell'ultimo commit. `handoff-check` passa comunque, perché confronta i nomi dei file.
- V-5 (COSMETICA): senza variabile T13-atteso non stampa nessuna riga SKIP.

NON VERIFICATO
- I log della run CI sono illeggibili da qui (il download dei log restituisce un redirect a un blob esterno che il proxy blocca). Non ho potuto vedere con i miei occhi che T13-atteso risulti PASS su un runner reale e che la variabile arrivi al processo Python. Mi baso solo sul `success` dello step `unit-suite`, che con la variabile impostata implica T13-atteso PASS.
- Il comportamento su macOS reale non è provato. L'assenza di bwrap è solo simulata con la cache, e sul Mac restano da vedere le differenze tra i comandi BSD, cioè `wc` con spazi iniziali e `grep`.
- Non ho letto in dettaglio i contenuti di `reports/*` e della memoria del revisore (solo il diffstat).

RACCOMANDAZIONE
- Si può fare il merge. Prima o subito dopo, l'operatore deve confermare su un Mac reale che `python tests/test_unit_kernel.py` dia 0 FAIL, come già indicato in §0.
- Valutare di irrigidire V-2 con un micro-task a basso costo.
- Prima di unire altre PR della notte, riallineare i report canonici a main, come già dichiarato in §0.
