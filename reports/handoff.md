# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Il report della notte dice perché il forte è fallito; doctor avvisa se `claude` è solo nel PATH del terminale (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #287 (https://github.com/Gasss23/Gas/pull/287): review #538 APPROVATO CON RISERVE, serve il «sì» dell'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON di `mcp__github__create_pull_request` (`gh` nel container non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — motivo vero dell'errore del forte nel report della notte**: `FATTA` — `_motivo_forte` in `gas.py`, messaggi di `brains/claude_cli.py` con il consiglio GAS_CLAUDE_BIN e il caso «non eseguibile».
- **Fetta 2 — doctor avvisa se `claude` è solo nel PATH del terminale**: `FATTA` — `_claude_solo_nel_terminale`, WARN con `GAS_CLAUDE_BIN=<percorso>`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 brains/claude_cli.py               |  6 +++++-
 gas.py                             | 46 +++++++++++++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           | 13 ++++++++-----
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 15 ++++++++++-----
 tests/test_unit_claude_cli.py      |  5 +++++
 tests/test_unit_kernel.py          | 50 ++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d», e la riga di totale è tolta. Conteggi presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
7392f49 fix(forte): il report della notte dice perché il forte è fallito; doctor avvisa se `claude` è solo nel PATH del terminale
071b292 chore(revisore): memoria review #538 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #538 (chat Motore) — sul diff di 7392f49

## VERDETTO: APPROVATO CON RISERVE

Review #538 (chat Motore), diff staged sul branch feat/errore-forte-notte (4 file, +103/-4). Ho letto CLAUDE.md (sez. 5, 8 e 9), reports/stato_progetto.md (la parte che serve: la voce del 28 ottobre su `GAS_CLAUDE_BIN` e sul PATH di launchd) e la memoria del revisore.

**Cosa ho esaminato**
- `brains/claude_cli.py:316` — FileNotFoundError ora suggerisce GAS_CLAUDE_BIN, e c'è un nuovo ramo PermissionError che diventa RuntimeError «non eseguibile». Rischio cercato: messaggi con contenuto variabile, o eccezioni che scappano senza essere intercettate. Esito: **ok**. Il testo è fisso, la causa resta agganciata con `from e`, e il rung resta nella gestione delle eccezioni dei provider (§9).
- `gas.py:426` — `_motivo_forte`. Rischio cercato: testo di Claude o della conversazione che finisce nella riga «Pipeline esausta» e nel report della notte. Ho controllato uno per uno tutti i punti di `brains/claude_cli.py` che sollevano RuntimeError (righe 317-372).
  - Sono tutti testi fissi oppure contengono solo valori controllati: il timeout, il codice di uscita, un `tipo` ripulito con `[^a-z_]` e tagliato a 40 caratteri, il prefisso «429 » di `_prefisso_limite`.
  - Il filtro accetta solo RuntimeError, solo la prima riga e solo il prefisso esatto (`re.match` con `^`).
  - Esito: **ok**, nessuna fuga di dati. Il test T99u copre il nome nella seconda riga, il testo senza prefisso e il ValueError.
- `gas.py:4912` — `_mf` viene calcolato solo per `name == "claude-cli"`, e HTTP status_code ha ancora la precedenza. Esito: **ok**, gli altri rung non cambiano.
- `gas.py:443` — `_claude_solo_nel_terminale`, insieme al chiamante del doctor in `gas.py:4983`. Rischio cercato: un falso OK.
  - Il venv conta come cartella vista dal timer, ed è giusto: `scripts/notte/com.gas.notte.plist:15` attiva `.venv`/`venv` prima di `python3 gas.py notte`, quindi la sua cartella bin è nel PATH.
  - `/usr/local/bin` e `/opt/homebrew/bin` danno WARN, coerente col PATH predefinito di launchd.
  - Un GAS_CLAUDE_BIN assoluto arriva qui solo se `shutil.which` lo ha già trovato ed è eseguibile (altrimenti c'è prima il WARN «non trovato»).
  - Esito: **riserva** (R-538-1).
- `tests/test_unit_kernel.py:11195` — T99s–T99v. Il PATH e GAS_CLAUDE_BIN vengono ripristinati in un finally, e `gas.ClaudeCliClient` viene rimesso com'era da `_orig99` (`tests/test_unit_kernel.py:11260`). Il WARN finto compare anche nell'output di T99n (nel container `claude` sta in `/opt/node22/bin`), ma nessun test esistente controlla «presente» su quella riga. Esito: **ok**.

**Esecuzione diretta**: kernel 1057 PASS, 0 FAIL. `tests/test_unit_claude_cli.py` 29 passed. Intera cartella tests/ 2265 passed, 61 skipped, nessuna regressione. Nessuno slicing della history, nessuna simulazione dei tool, cap a 10 iterazioni e `_get_window` non toccati, il doctor resta senza chiamate LLM.

**Finding**
- **R-538-1 (BASSA)**: falso OK del doctor. Se GAS_CLAUDE_BIN assoluto è esportato solo nella shell (es. `~/.zshrc`) e non nel `.env`, il doctor lanciato dal terminale dice «presente», ma il timer di launchd non vede quella variabile e ricade su `claude` cercato nel suo PATH ridotto. Oggi sul Mac la variabile sta nel `.env`, quindi il caso non è attivo. Correzione possibile: dire nel messaggio da dove arriva il valore, o controllare che sia nel `.env`. Da tracciare in stato_progetto.
- **R-538-2 (COSMETICA)**: `_MSG_LOGIN` supera i 160 caratteri, quindi nel motivo il consiglio «/login …» arriva troncato. Il senso resta, ma conviene accorciarlo o alzare il tetto.

**Cosa NON ho verificato**: il comportamento reale sotto launchd sul Mac (PATH ridotto, `.env` caricato dal giro notturno), perché non si riproduce nel container Linux. La correttezza del motivo nel report del mattino l'ho verificata solo con T99v (run_turn con runner finto), non con un giro `gas notte` completo. Non ho fatto test mutanti formali: ho controllato solo che T99u catturerebbe la rimozione del filtro sul prefisso (il caso «Mario Rossi»).

**Memoria**: aggiunta la riga #538 più una lezione (un controllo del doctor «per il timer» eseguito dal terminale eredita le variabili della shell). È già committata da sola con `commit_memoria_revisore.sh` (commit 071b292), lo staging del diff non è stato toccato.

## §5 DELTA TEST DEL MOTORE

Kernel: 1053 → 1057 PASS (T99s, T99t, T99u, T99v nuovi).

```
=== RIEPILOGO: 1057 PASS, 0 FAIL ===
```

pytest (`python3 -m pytest -q tests`): `2265 passed, 61 skipped in 196.34s (0:03:16)`. Nessun FAIL.

## §6 STATO CI

`gh` nel container non è autenticato («Failed to log in to github.com using token (GH_TOKEN)»): run lette con lo strumento GitHub della sessione (`actions_list`, branch feat/errore-forte-notte):

```
CI            run 40736220989  push                 head 7392f49  status in_progress
verifica-bot  run 40736298019  pull_request_target  head 7392f49  conclusion skipped (etichetta `verifica` non ancora messa)
```

Mappatura commit→run:
- 7392f49 → CI run 40736220989 (in corso alla scrittura dell'handoff).
- 071b292 → nessuna run su questo SHA (pushato insieme a 7392f49: la run testa solo l'albero di testa).
- commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-538-1** (BASSA, review #538): doctor dà OK se GAS_CLAUDE_BIN assoluto sta solo nella shell e non nel `.env`.
- **R-538-2** (COSMETICA, review #538): `_MSG_LOGIN` oltre 160 caratteri, troncato nel motivo.
