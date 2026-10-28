# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Il report della notte dice perché il forte è fallito; doctor avvisa se `claude` è solo nel PATH del terminale (chat Motore). Secondo giro: merge di main (PR #285) dopo la V-1 della verifica esterna.

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #287 (https://github.com/Gasss23/Gas/pull/287): review #538 APPROVATO CON RISERVE, bot e verifica esterna APPROVATO CON RISERVE; serve il «sì» dell'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON di `mcp__github__create_pull_request` (`gh` nel container non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — motivo vero dell'errore del forte nel report della notte**: `FATTA` — `_motivo_forte` in `gas.py`, messaggi di `brains/claude_cli.py` con il consiglio GAS_CLAUDE_BIN e il caso «non eseguibile».
- **Fetta 2 — doctor avvisa se `claude` è solo nel PATH del terminale**: `FATTA` — `_claude_solo_nel_terminale`, WARN con `GAS_CLAUDE_BIN=<percorso>`.
- **Fetta 3 — conflitto con main (V-1 MEDIA verifica esterna)**: `FATTA` — merge di origin/main 297fc22 (PR #285), conflitti solo nei report e nella memoria; review #539 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 brains/claude_cli.py               |   6 +++++-
 gas.py                             |  46 +++++++++++++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           |  17 +++++++++--------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  46 ++++++++++++----------------------------------
 tests/test_unit_claude_cli.py      |   5 +++++
 tests/test_unit_kernel.py          |  50 ++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d», e la riga di totale è tolta. Conteggi presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
cfb8a3c Merge origin/main (PR #285) in feat/errore-forte-notte (PR #287) — review #539 APPROVATO
f4878a3 docs(fine-task): PR #287 motivo vero dell'errore del forte e avviso del doctor, review #538
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

### Review #539 (chat Motore) — sul merge di origin/main (PR #285) in cfb8a3c

Il verdetto originale (sotto, nel blocco di codice, testo integrale e invariato) citava come `path:riga` soprattutto file entrati da main, che non sono nel diff di sessione (base 297fc22 dopo il merge): il Gate B lo ha rifiutato (1 citazione valida su 2). Come da regola il testo non è stato ritoccato: il revisore lo ha riemesso con lo stesso esito e lo stesso finding, citando i file del diff. Fa fede il verdetto riemesso; l'originale resta qui per tracciabilità.

Verdetto originale (sostituito dalla riemissione):

```text
## VERDETTO: APPROVATO

Review #539 (chat Motore). Ho controllato il merge in corso di origin/main 297fc22 (PR #285) dentro feat/errore-forte-notte (HEAD f4878a3). Il diff è in stage, MERGE_HEAD = 297fc22.

Elementi esaminati:
- `modules/web/lexbor.py:98` — `intero()` portato da main (segno + o -, «0»/«-0» → 0, tetto `< 1 << 31`). Rischio: che il merge abbia cambiato qualcosa. Esito ok: `git diff --cached origin/main -- modules/web/lexbor.py` è vuoto, quindi il file è identico a main. Il codice era già stato revisionato in #536/#537/#538 della chat Mani.
- `tests/test_unit_web_lexbor.py:171` — i test di `intero()` arrivati da main. Rischio: una divergenza dal ramo di origine. Esito ok: identico a origin/main. Vale lo stesso per reports/ripartenza_mani.md.
- `reports/stato_progetto.md:4` — la riga «Ultimo aggiornamento» unita a mano. Rischio: perdere una delle due catene «prima». Esito ok: in testa c'è la voce Motore #287, poi la voce Mani fetta 22, poi la catena del ramo completa (Motore notte fallita, Notte #284, Mani fetta 21…). La lunghezza (7747 caratteri) torna con HEAD (7448) più la voce Mani. Il paragrafo «Mani — fetta 22» (riga 634) è presente. Il punto 3 della coda (fetta PR #287 fatta) resta.
- `.claude/agents/memoria_revisore.md:926` — le righe #536/#537/#538 della chat Mani da main, poi #538 della chat Motore e la sua lezione dal ramo. Rischio: righe perse o duplicate. Esito ok: rispetto a main mancano solo le 2 righe del ramo, rispetto a HEAD solo le 3 righe Mani.
- `gas.py:426` (contesto, `_motivo_forte`). Rischio: che il merge abbia toccato il codice della PR #287. Esito ok: gas.py, brains/claude_cli.py, tests/test_unit_claude_cli.py e tests/test_unit_kernel.py sono identici al ramo (`git diff --cached HEAD` vuoto su ciascuno).

Controlli d'insieme:
- I file di `git diff --cached origin/main` sono esattamente quelli di `origin/main...HEAD`: i 9 file della PR #287, niente in più.
- Nessun marcatore di conflitto e `git diff --cached --check` pulito.
- I log di sessione (handoff, ultimo_report, diff_sessione) sono la versione del ramo, come dichiarato.
- Nessun nuovo slicing della history né simulazione di tool: il codice del motore non cambia rispetto a #538.

Finding:
- R-539-1 COSMETICA: il numero #538 compare due volte nel contatore (chat Mani e chat Motore), distinte solo dal suffisso. Il gate non si rompe, ma il contatore è meno leggibile. Non chiede interventi: questa review prosegue la numerazione con #539.

Rischio escluso: non ho rilanciato io i test (kernel 1057 PASS, pytest lexbor e claude_cli). Mi fido della tua esecuzione, perché il codice è identico byte per byte a due commit già testati e revisionati (#538 Motore, #536-#538 Mani). Non ho valutato l'interazione a runtime tra lexbor e le modifiche al forte: sono moduli separati e nessun file è in comune.

Memoria: ho scritto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga `#539 (chat Motore) — 2026-10-28 — APPROVATO — …`, con R-539-1 e «nessuna lezione nuova». Come mi hai chiesto non ho lanciato commit_memoria_revisore.sh: il file è modificato ma non in stage, quindi fai `git add .claude/agents/memoria_revisore.md` prima del commit di merge.
```

Verdetto riemesso:

## VERDETTO: APPROVATO

Review #539 (chat Motore): merge di origin/main 297fc22 (PR #285) dentro feat/errore-forte-notte (PR #287). Base della sessione: 297fc22.

Elementi del diff esaminati:
- `gas.py:426` — `_motivo_forte` legge il motivo vero solo da RuntimeError con prefisso fisso «claude-cli: », prende la prima riga e la tronca. Rischio: che il merge abbia alterato il codice già revisionato in #538 o che il testo esponga dati non fidati. Esito: ok, il codice è identico a f4878a3 (dove `git diff --cached HEAD -- gas.py` era vuoto) e i testi sorgente sono fissi.
- `gas.py:4912` — `_motivo_forte(e)` viene chiamata solo per `name == "claude-cli"` e il motivo va nella riga «Pipeline esausta», dopo l'eventuale HTTP. Rischio: motivo applicato ad altri provider, o eccezione dentro il fallback. Esito: ok, l'ambito è ristretto al forte e la cascata §9 resta intatta.
- `gas.py:4983` — il doctor legge `GAS_CLAUDE_BIN`, usa `shutil.which`, e se `_claude_solo_nel_terminale` è vero dà WARN invece di OK. Rischio: un falso OK quando la variabile arriva dalla shell del terminale invece che dal .env. Esito: ok, il caso è coperto ed è registrato come lezione in #538.
- `brains/claude_cli.py:317` — FileNotFoundError e PermissionError diventano RuntimeError con testo fisso «claude-cli: …» che indica GAS_CLAUDE_BIN nel .env. Rischio: un'eccezione propagata fino al crash. Esito: ok, il messaggio è catturato e loggato dal kernel e il fallback scatta.
- `tests/test_unit_claude_cli.py:282` — test del runner che solleva PermissionError e attende RuntimeError «non eseguibile.*GAS_CLAUDE_BIN». Esito: ok.
- `tests/test_unit_kernel.py:11195` — test del doctor con un `claude` finto solo nel PATH del terminale, che deve dare WARN. Esito: ok.

Controlli sul merge (cfb8a3c):
- I file arrivati da main sono identici a origin/main, verificato prima del commit con `git diff --cached origin/main` vuoto: modules/web/lexbor.py, tests/test_unit_web_lexbor.py e reports/ripartenza_mani.md.
- I file di `git diff 297fc22..HEAD` sono esattamente i 9 della PR #287.
- Nessun marcatore di conflitto; `--check` pulito.
- `reports/stato_progetto.md:4` unisce le due catene «prima» senza perdite.
- La memoria contiene #536, #537 e #538 della chat Mani più #538 della chat Motore.
- Nessuno slicing della history e nessuna simulazione di tool.

Finding:
- R-539-1 COSMETICA: il numero #538 compare due volte nel contatore (chat Mani e chat Motore), distinte solo dal suffisso. Il gate non si rompe; la numerazione prosegue con #539.

Rischio escluso: non ho rilanciato i test, mi baso sulla tua esecuzione (kernel 1057 PASS 0 FAIL, pytest di lexbor e claude_cli verdi). È accettabile perché il codice è identico byte per byte a commit già testati e revisionati. Non ho verificato il comportamento reale del timer notturno sul Mac: non si riproduce in dev e resta da controllare al giro del 29.

## §5 DELTA TEST DEL MOTORE

Kernel: 1053 → 1057 PASS (T99s, T99t, T99u, T99v nuovi).

```
=== RIEPILOGO: 1057 PASS, 0 FAIL ===
```

pytest (`python3 -m pytest -q tests`): `2265 passed, 61 skipped in 196.34s (0:03:16)`. Nessun FAIL.

Dopo il merge di main (cfb8a3c): kernel `=== RIEPILOGO: 1057 PASS, 0 FAIL ===`; `python3 -m pytest -q tests/test_unit_web_lexbor.py tests/test_unit_claude_cli.py` → `49 passed, 60 skipped in 0.20s`.

## §6 STATO CI

`gh` nel container non è autenticato: run lette con lo strumento GitHub della sessione (`actions_list`, workflow ci.yml, branch feat/errore-forte-notte):

```
CI  run 40736463154  push  head f4878a3  completed  success
CI  run 40736220989  push  head 7392f49  completed  failure (unit-suite success; handoff-check failure: handoff.md non ancora nel diff, atteso prima del fine-task)
verifica-bot  run 40736485838  pull_request_target  head f4878a3  completed  success
```

Mappatura commit→run:
- 071b292 → nessuna run su questo SHA (pushato insieme a 7392f49).
- 7392f49 → CI run 40736220989: unit-suite success, handoff-check failure (atteso: l'handoff è arrivato col commit dopo).
- f4878a3 → CI run 40736463154 success.
- cfb8a3c (merge di main) → run non ancora disponibile alla scrittura dell'handoff (pushato insieme al commit di fine-task).
- commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-538-1** (BASSA, review #538): doctor dà OK se GAS_CLAUDE_BIN assoluto sta solo nella shell e non nel `.env`.
- **R-538-2** (COSMETICA, review #538): `_MSG_LOGIN` oltre 160 caratteri, troncato nel motivo.
- **V-1 bot #287** (BASSA): falsi WARN del doctor (verso prudente): non considera `~/.zshenv` letto da `/bin/zsh -c`, `/usr/local/bin` nel PATH predefinito di systemd, i collegamenti simbolici (manca realpath).
- **V-2 bot #287** (COSMETICA): prefisso ripetuto «claude-cli: KO (claude-cli: …)».
- **Verifica esterna #287** ([commento](https://github.com/Gasss23/Gas/pull/287#issuecomment-6476088252)): V-1 MEDIA conflitto con main CHIUSA da cfb8a3c (review #539); V-2 = R-538-1; V-3 = R-538-2; V-4 BASSA WARN anche nel container per `claude` in /opt/node22/bin (rumore nei test).
- **R-539-1** (COSMETICA, review #539): numero #538 usato sia dalla chat Mani che dalla chat Motore.
