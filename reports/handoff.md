# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — merge #174 + cartelle di editor/agenti e altre config non scrivibili da Gas (PR #175, secondo giro dopo la bocciatura del bot)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #175 (https://github.com/Gasss23/Gas/pull/175). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/175"}`): `gh` nel container non è autenticato. Fetta di SICUREZZA (cancello): secondo passaggio nella chat claude.ai con lo stesso URL. Merge autonomo dell'agente solo con verdetto testuale del bot `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Divieto per nomi vs scrittura consentita solo in cartelle precise (R-223-2): scelta di progetto.
3. R-249-2: DENY netto anche in `dati/` per `package.json`/`Dockerfile`/`.vscode/` (scelta dichiarata, da rivedere con FASE 4).
4. Aperte da prima: archivio verifiche esterne (a/b), roadmap, costo del bot di verifica, V-2 bot #163, V-2 verifica esterna #172, prova sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Merge di #174**: `FATTA` — su richiesta esplicita dell'operatore, merge commit `3ce844f` (= BASE di questa sessione).
- **Fetta 1 — R-247-2 + V-1 verifica esterna #174**: `FATTA`.
- **R-249-1**: `FATTA` nella stessa PR.
- **R-249-2 e nomi scoperti**: `DEFERITA` — dichiarati in `stato_progetto.md`, decisione dell'operatore.
- **Secondo giro — V-1 MEDIA del bot su #175** (la «V-1 bot #174», punti/spazi finali per pezzo del percorso, era stata attribuita per errore come chiusa): `FATTA` — `p.rstrip(". ")` su ogni pezzo; attribuzioni corrette in `stato_progetto.md`.
- **V-2 bot #175 + V-1 agente di verifica esterna #175**: `FATTA` — `.pdbrc`, `.pylintrc`, `pylintrc`, `.husky`, `.npmrc`, `.windsurf`, `.zed`.
- **R-251-1** (alias Windows): `DEFERITA` — dichiarata in `stato_progetto.md` (Windows non è piattaforma di Gas).
- **Archivio dei verdetti #173/#174 in `reports/verifiche_esterne.md`** (chiesto dal bot su #175): `SALTATA` — in attesa della scelta (a)/(b) dell'operatore sull'archivio.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/gate/gate.py               |  17 ++++++++++++++++-
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 199 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  32 ++++++++++++++++++--------------
 tests/test_unit_gate.py            |  12 ++++++++++++
 7 files changed, 192 insertions(+), 85 deletions(-)
```

Nota: i conteggi di righe dei report scritti dopo lo stat (`reports/handoff.md`) sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
2fce28a fix(gate): punti/spazi finali tolti da ogni pezzo del percorso; .pdbrc, .pylintrc, .husky, .npmrc, .windsurf, .zed
46d8cd4 chore(revisore): memoria review #251 — APPROVATO CON RISERVE
0513cfd docs(fine-task): report PR #175 (cartelle di editor/agenti e altre config non scrivibili)
4934af2 fix(gate): cartelle di editor/agenti e altre config di sviluppo non scrivibili da Gas
30ef31d chore(revisore): memoria review #250 — APPROVATO
5b6ff04 chore(revisore): memoria review #249 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. `0513cfd` è il commit di fine-task del primo giro.

## §4 VERDETTO DEL REVISORE

### Review #249 (prima versione del diff di 4934af2)

## VERDETTO: APPROVATO CON RISERVE

**Letture obbligatorie fatte.** CLAUDE.md (sez. 5, 8 e 9), la voce 6 di `reports/stato_progetto.md` con R-247-2 e R-223-2, e la coda di `.claude/agents/memoria_revisore.md` (lezione del #247: elencare tutti i nomi che lo strumento accetta).

**Elementi del diff esaminati:**

- `modules/gate/gate.py:135` — aggiunge `.vscode`, `.cursor`, `.gemini`, `.idea` e `.devcontainer` a `_DENY_WRITE_ANY_PART_NAMES`.
  - Rischio esaminato: che il confronto non copra il contenuto delle cartelle o le varianti di maiuscole.
  - Il controllo di `gate.py:199` confronta ogni pezzo del percorso, dopo NFKC e casefold. Ho provato `.VSCODE/tasks.json` e `.Vscode`: tutti e due DENY.
  - Esito: ok.
- `modules/gate/gate.py:136-137` — aggiunge 11 file di configurazione, tutti scritti in minuscolo (coerente col casefold, quindi `Dockerfile` diventa DENY).
  - Rischio esaminato: falsi positivi.
  - Le varianti `package.json.bak` e `dati/dockerfile_esempio.txt` restano UNCERTAIN, perché il confronto è esatto e non per prefisso.
  - La lettura non cambia: il divieto vale solo se `write` è vero.
  - Esito: ok.
- `tests/test_unit_gate.py:415-419` e `:430` — aggiungono casi DENY a ogni livello (`dati/.vscode/settings.json`, `tests/.mypy.ini`) e casi di nomi simili che devono restare UNCERTAIN.
  - Esito: ok. Ho rieseguito i test: 174 passed. Prendo per buono il dato «17 failed con il gate.py della base», non l'ho riprodotto.
- Contesto, `modules/gate/gate.py:76-95` (`_DENY_PREFIXES`): `.git` copre già `.github/`, e `.env` copre `.envrc`. Nessuna sovrapposizione né contraddizione con le aggiunte.

**Riserve:**

- **R-249-1 (BASSA) — formati alternativi ancora scrivibili.** `.devcontainer.json` nella cartella principale è una forma ammessa dalla specifica dei devcontainer e può contenere `postCreateCommand`. `*.code-workspace` può contenere i task di VS Code. Le due forme danno lo stesso rischio delle cartelle appena vietate, ma restano UNCERTAIN. Le ho provate con `_wf`. Attenua il fatto che UNCERTAIN non è SAFE. Va aggiunta al residuo dichiarato oppure chiusa con due nomi in più (`.devcontainer.json` va bene come nome esatto; `*.code-workspace` è un'estensione e servirebbe un suffisso).
- **R-249-2 (BASSA, da dichiarare) — falsi positivi.** Il divieto vale a ogni livello, quindi `dati/progetto/package.json`, `dati/Dockerfile` e `dati/.vscode/...` diventano DENY. Il DENY è un rifiuto netto, senza via di approvazione da parte dell'operatore, a differenza di UNCERTAIN. Se un giorno Gas dovesse preparare un progetto web o container per l'utente (per esempio una landing page nella fase 4 del funnel marketing), il cancello lo bloccherebbe. Oggi la roadmap non ha nessun caso d'uso del genere, quindi il compromesso è accettabile, coerente con «robustezza > potenza», ma va scritto in `stato_progetto.md` accanto a R-223-2.
- **Il divieto resta per nomi, e va dichiarato.** Il commento del codice lo dice già. Restano scoperti, per esempio, `Containerfile`, `compose.yaml` e `.pre-commit-hooks.yaml`: tutti UNCERTAIN, provati. In questi casi il rischio è minore, perché serve un comando lanciato apposta dall'operatore.

**Cosa NON ho verificato:**

- Che ogni strumento carichi davvero quei file in automatico (i task di VS Code con `folderOpen` e il devcontainer con `postCreateCommand`): non riproducibile qui, non ci sono gli editor installati.
- Il comportamento sul filesystem di macOS con nomi con punto o spazio finale: non riproducibile su Linux.
- Il comportamento sul VPS: non riproducibile in sviluppo.

**Wall of Shame:** non c'è slicing della history né output dei tool simulato. Il diff non tocca `_get_window`, il tetto di 10 iterazioni né il tetto di 8k di output.

Memoria aggiornata con la riga contatore #249 e una lezione (vietare una cartella di configurazione non basta: va provata anche la sua forma a file singolo). Commit `5b6ff04`, solo `.claude/agents/memoria_revisore.md`. Il diff staged è rimasto intatto.

### Review #250 (delta R-249-1, diff finale di 4934af2)

## VERDETTO: APPROVATO

Ho ri-revisionato tutto il diff staged. Il delta chiude la riserva R-249-1 e il resto è invariato rispetto alla review #249. Test del gate rieseguiti: 178 passed.

**Elementi del diff esaminati:**

- **`modules/gate/gate.py:106`** — aggiunge `.code-workspace` a `_DENY_WRITE_SUFFIXES`.
  - Rischi esaminati: aggiramento con punti finali, maiuscole, falsi positivi.
  - Provato con `_wf`: `gas.code-workspace.` → DENY, grazie al `rstrip("/. ")` già esistente; `dati/x.CODE-WORKSPACE` → DENY, grazie al casefold.
  - Falsi positivi: `note.code-workspace.txt` e un file chiamato solo `code-workspace` restano UNCERTAIN, perché il confronto è sull'estensione con il punto davanti.
  - Esito: ok.
- **`modules/gate/gate.py:137`** — aggiunge il nome esatto `.devcontainer.json` alla lista dei nomi vietati.
  - Rischio esaminato: un divieto troppo largo.
  - `.devcontainer.json.bak` resta UNCERTAIN. La lettura resta permessa: `_rf` dà SAFE sia per `.devcontainer.json` sia per `gas.code-workspace`.
  - Esito: ok.
- **`tests/test_unit_gate.py:420-421`** — 4 casi nuovi nell'elenco dei percorsi da vietare: cartella principale, `dati/`, maiuscole, e il caso col suffisso.
  - Esito: ok.
- **Resto del diff** (`gate.py:132-139` e i casi di test di R-247-2): uguale a quanto revisionato nella #249.

**Rischi esclusi:**

- Non ho verificato che VS Code esegua davvero i task di un `.code-workspace` o il `postCreateCommand` di `.devcontainer.json`: gli editor non sono installati qui.
- Non ho rifatto la prova inversa (gate.py della base + test nuovi → test che falliscono).
- R-249-2 (falsi positivi su `package.json`/Dockerfile/`.vscode` in `dati/`) e i nomi ancora scoperti (`Containerfile`, `compose.yaml`, `.pre-commit-hooks.yaml`) non sono chiusi dal codice. Il coordinatore li scrive in `stato_progetto.md`; va controllato che ci finiscano prima del merge.

Wall of Shame: nessuno slicing della history, nessun output di tool simulato. Il diff non tocca `_get_window` né i tetti.

Memoria aggiornata con la riga #250 e committata da sola (commit `30ef31d`). Il diff staged è rimasto intatto.

(Modifiche dell'agente al testo dei verdetti #249/#250/#251: path assoluti scritti relativi; elenco «File rilevanti» finale omesso. R-249-2 e i nomi scoperti sono scritti in `reports/stato_progetto.md` in questo commit di fine-task.)

### Review #251 (delta del secondo giro, diff di 2fce28a)

## VERDETTO: APPROVATO CON RISERVE

Il diff staged (`git diff --cached`, 2 file, +11/-1) chiude il problema segnalato dal bot. Le prove che ho fatto non mostrano falsi positivi e nessuna regressione.

**Letture obbligatorie fatte:** CLAUDE.md (sez. 5, 8, 9, 10), `reports/stato_progetto.md` (voce 6, letta con Grep), coda di `.claude/agents/memoria_revisore.md`.

**Elementi del diff esaminati**

1. `modules/gate/gate.py:206` — `p.rstrip(". ") in _DENY_WRITE_ANY_PART_NAMES` su ogni pezzo del percorso, solo in scrittura.
   - **Rischio esaminato:** falsi positivi, e un pezzo che diventa vuoto dopo il rstrip.
   - **Prove sul codice reale:**
     - Diventano DENY in scrittura e restano consentiti in lettura: `pytest.ini.`, `Makefile.`, `tests/pyproject.toml `, `.vscode./tasks.json`, `dati/.vscode /x`, `Dockerfile.`, `dati/makefile...`.
     - Anche `pytest.ini` seguito da uno spazio non separabile (U+00A0) o da uno spazio ideografico (U+3000) diventa DENY: la normalizzazione Unicode (NFKC) li trasforma in spazi normali prima del rstrip.
     - `...`, `dati/...`, `dati/... /x`, `. .`, `dati/. ./x` danno un pezzo vuoto: la stringa vuota non è nel frozenset, quindi restano UNCERTAIN. Nessun falso positivo e nessuna eccezione.
     - Restano UNCERTAIN, giustamente: `dati/makefile.bak`, `dati/.husky.txt`, `dati/pylintrc.d/x`, `pytest.ini` con spazio iniziale o con tab finale (Windows toglie solo punti e spazi finali).
     - Restano UNCERTAIN come prima le 4 prove dell'agente: `note.txt`, `dati/a..b/x.md`, `dati/..note.md`, `dati/progetto.ini`.
   - **Mutation:** su una copia in scratch ho tolto il rstrip → 6 test FAIL, esattamente i 6 casi nuovi.
   - **Esito:** ok.

2. `modules/gate/gate.py:201-202` e `:166-181` (contesto, non toccati) — `_DENY_WRITE_TOP_PREFIXES` e `_in_denylist` confrontano con `startswith`.
   - **Rischio esaminato:** serve lo stesso rstrip anche lì?
   - **Risposta:** no. Un suffisso di punti o spazi non può impedire un `startswith` che altrimenti passerebbe. Verificato: `scripts./x`, `claude.md. `, `CLAUDE.md .` erano già DENY, e `.gas_memory.db.` è DENY anche in lettura.
   - **Esito:** ok.

3. `modules/gate/gate.py:142` — nomi nuovi `.pdbrc`, `.pylintrc`, `pylintrc`, `.husky`, `.npmrc`, `.windsurf`, `.zed`.
   - **Rischio esaminato:** collisione con nomi legittimi di `dati/`. Il confronto è esatto per pezzo, quindi `dati/.husky.txt` passa.
   - **Esito:** ok.

4. `tests/test_unit_gate.py:422-425` — 13 casi nuovi nella lista parametrica di `test_write_config_strumenti_sviluppo_deny`.
   - **Rischio esaminato:** test che non mordono. Con la mutation falliscono i 6 casi del rstrip; per i 7 nomi nuovi vale il dato dell'agente (13 FAIL con il `gate.py` di HEAD).
   - **Esito:** ok.

**Numeri dei test che ho riprodotto:** 191 passed sul cancello, 859 passed su `tests/`, kernel 715 PASS / 0 FAIL (lanciati con `PYTHONDONTWRITEBYTECODE=1`).

**Coerenza col progetto:** nessun Wall of Shame (nessuno slicing della history, nessuna simulazione dei tool). Il cancello resta fail-closed e i guardrail non sono toccati. La modifica va nella direzione della riserva FASE 4.5.

**Riserva**

- **R-251-1 (BASSA):** il commento a `gate.py:204-205` giustifica la modifica con "su Windows sono lo stesso file". Però altri due alias Windows dello stesso file restano UNCERTAIN:
  - `pytest.ini::$DATA` (stream alternativo di NTFS);
  - `PYTEST~1.INI` (nome corto 8.3).

  Due strade: coprirli, oppure dichiarare in `stato_progetto.md` che Windows non è una piattaforma su cui gira Gas (oggi VPS Linux e Mac). Non blocca: su Linux e APFS questi nomi sono file diversi e innocui.

**Rischi esplicitamente esclusi**

- **Su Windows non ho eseguito niente:** gli alias li ho ricavati da come NTFS gestisce i nomi, non li ho riprodotti (dev Linux).
- **Kernel 717 in CI non verificato:** ho visto solo i 715 in locale. Lo scarto di 2 dichiarato (test del profilo sandbox saltati in locale) lo prendo dal testo di `stato_progetto.md`.
- **`reports/stato_progetto.md` non revisionato:** è nel working tree, non staged, e fuori dal perimetro di review. L'ho solo letto: cita già la review #251, cioè questa.

**Memoria aggiornata:** riga contatore #251 più una lezione (gli alias Windows vanno elencati tutti), committata con `scripts/commit_memoria_revisore.sh` → commit `46d8cd4`. L'index del motore staged è rimasto intatto.


## §5 DELTA TEST DEL MOTORE

Gate 154 → 191 passed; `pytest tests/` 822 → 859 passed (+37 casi del gate); kernel 715 PASS / 0 FAIL in locale (717 in CI: 2 test del profilo sandbox saltati in locale).

```
191 passed in 0.23s
859 passed in 115.35s (0:01:55)
=== RIEPILOGO: 715 PASS, 0 FAIL ===
```

Mutation: primo giro, `gate.py` della base + test nuovi → `17 failed, 157 passed`; secondo giro, `gate.py` di `0513cfd` + test nuovi → `13 failed, 178 passed` (revisore #251: tolto il rstrip → 6 FAIL, i 6 casi nuovi).

## §6 STATO CI

`gh` non autenticato nel container; stato letto con lo strumento GitHub collegato.

Per costruzione i commit intermedi sono ROSSI su `handoff-check`: fa fede la run sul commit di fine-task.

- `5b6ff04`, `30ef31d`, `4934af2`: pushati insieme; run su `4934af2` rossa su `handoff-check` per costruzione.
- `0513cfd` (fine-task del primo giro): `unit-suite` success, `handoff-check` success, `verifica-bot` **failure** (V-1 MEDIA, corretta in questo giro).
- `46d8cd4`, `2fce28a`: pushati insieme al commit di fine-task di questo giro; nessuna run propria sui due intermedi.
- Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-251-1 (BASSA, dichiarata)**: alias Windows (`::$DATA`, nomi 8.3) restano UNCERTAIN.
- **Archivio verdetti #173/#174**: in attesa della scelta (a)/(b) dell'operatore.

- **R-249-2 (BASSA, scelta dichiarata)**: DENY netto anche in `dati/` per `package.json`/`Dockerfile`/`.vscode/`.
- **R-223-2 (divieto per nomi)**: scoperti p.es. `Containerfile`, `compose.yaml`, `.pre-commit-hooks.yaml`.
- **Non verificato**: caricamento reale dei file da parte degli editor (VS Code, devcontainer).
- Decisioni dell'operatore aperte da prima (§0.4).
