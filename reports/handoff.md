# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — merge #174 + cartelle di editor/agenti e altre config non scrivibili da Gas (PR #175)

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

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/gate/gate.py               |   9 +++++++++
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 133 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  27 +++++++++++++--------------
 tests/test_unit_gate.py            |   8 ++++++++
 7 files changed, 110 insertions(+), 82 deletions(-)
```

Nota: i conteggi di righe dei report scritti dopo lo stat (`reports/handoff.md`) sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
4934af2 fix(gate): cartelle di editor/agenti e altre config di sviluppo non scrivibili da Gas
30ef31d chore(revisore): memoria review #250 — APPROVATO
5b6ff04 chore(revisore): memoria review #249 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

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

(Modifiche dell'agente al testo dei verdetti: path assoluti scritti relativi; elenco «File rilevanti» finale omesso in entrambi. R-249-2 e i nomi scoperti sono scritti in `reports/stato_progetto.md` in questo commit di fine-task.)

## §5 DELTA TEST DEL MOTORE

Gate 154 → 178 passed; `pytest tests/` 822 → 846 passed (+24 casi del gate); kernel 715 PASS / 0 FAIL.

```
178 passed in 0.23s
846 passed in 113.43s (0:01:53)
=== RIEPILOGO: 715 PASS, 0 FAIL ===
```

Mutation: con il `gate.py` della base e i test nuovi (prima del delta R-249-1) → `17 failed, 157 passed`.

## §6 STATO CI

`gh` non autenticato nel container; PR #175 appena aperta.

Per costruzione i commit intermedi (pushati prima del commit di fine-task) sono ROSSI su `handoff-check`: l'handoff della sessione arriva solo col commit di fine-task. Fa fede la run sul commit di fine-task.

- `5b6ff04`, `30ef31d`, `4934af2`: pushati insieme; run su `4934af2` attesa rossa su `handoff-check` per costruzione (gli altri non hanno una run propria).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-249-2 (BASSA, scelta dichiarata)**: DENY netto anche in `dati/` per `package.json`/`Dockerfile`/`.vscode/`.
- **R-223-2 (divieto per nomi)**: scoperti p.es. `Containerfile`, `compose.yaml`, `.pre-commit-hooks.yaml`.
- **Non verificato**: caricamento reale dei file da parte degli editor (VS Code, devcontainer).
- Decisioni dell'operatore aperte da prima (§0.4).
