# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-08 — FASE 4.5 fetta 1: `gas notte` + cancello rinforzato (catena di avvio fuori sandbox)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #160 (https://github.com/Gasss23/Gas/pull/160). Numero e URL vengono dalla risposta di GitHub alla creazione della PR: in questo ambiente `gh` non è autenticato e la PR è stata creata con lo strumento GitHub della sessione. L'operatore ha chiesto di fare il merge senza chiedere conferma se tutto è positivo. Condizioni da soddisfare sul nuovo head (il bot aveva BOCCIATO `d3a593d`, V-1 corretta in `c120bda`):
   - `verifica-bot` success;
   - `unit-suite` e `handoff-check` verdi.
2. Dopo il merge, sul Mac: seguire `reports/setup_notte.md` (catalogo, tetto di spesa, timer launchd).
3. R-222-4, da sapere: Gas non può più fare alcune cose. Se serve un comportamento diverso, la decisione è dell'operatore.
   - Non può scrivere:
     - file di codice o shell (`.py`, `.sh`, …);
     - `scripts/`, `CLAUDE.md`, `gas_identity.md`, `requirements*`.
   - Non può leggere `.gas_notte/`.
4. Ancora aperte da prima:
   - lezioni #4, #5, #6: parere dell'agente, approvare la 6 e la 5 e rifiutare la 4;
   - firma in attesa `fab385e4…`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 FASE 4.5 — comando `gas notte`**: `FATTA` — `2a2ed0d`, review #220.
- **Correzioni della verifica esterna #160 (V-1 MEDIA tetto di spesa, V-2 riepilogo, V-3 test del lock)**: `FATTA` — `d0cfc17`, review #221.
- **Correzione del bot di verifica #160 (V-1 MEDIA: catena di avvio scrivibile e poi eseguita fuori dalla sandbox)**: `FATTA` — `d0cfc17`, review #222 e #223. Il cancello nega `write_file` su `venv`, `.git`, `.gas_notte`, sui file di codice e di shell e sui file sensibili al primo livello.
- **Correzione bot di verifica #160 su `d3a593d` (V-1 MEDIA: CLAUDE.local.md, CLAUDE.md nelle sottocartelle, AGENTS.md scrivibili)**: `FATTA` — `c120bda`, review #224 e #225. Anche V-2 (esempio con `git` non consentito) corretta; V-3 (conteggio kernel 707 locale vs 709 in CI) dichiarata in §5.
- **Allineamento a main** (`bcf2d5c`): merge di `origin/main` (solo il commit di merge della #159, nessun file cambiato).
- **Riepilogo su Telegram al mattino**: `DEFERITA` — rimandato alla fetta 2.
- **Tetto di tempo (R-220-3)**: `DEFERITA` — rimandato alla fetta 2.
- **Prova reale con launchd sul Mac**: `DEFERITA` — non si può riprodurre su Linux; la fa l'operatore.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  11 +++++++++++
 .github/workflows/ci.yml            |   8 ++++++++
 .gitignore                          |   2 ++
 gas.py                              |   9 +++++++++
 modules/gate/gate.py                |  45 +++++++++++++++++++++++++++++++++++++++++--
 modules/notte/__init__.py           |   4 ++++
 modules/notte/notte.py              | 279 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md            |  20 +++++++++++--------
 reports/handoff.md                  | 378 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------
 reports/setup_notte.md              |  44 ++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md           |   4 ++--
 reports/ultimo_report.md            |  40 +++++++++++++++++++++++++-------------
 scripts/notte/catalogo_esempio.yaml |  16 +++++++++++++++
 scripts/notte/com.gas.notte.plist   |  27 ++++++++++++++++++++++++++
 tests/test_unit_gate.py             |  68 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_notte.py            | 379 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 16 files changed, 1293 insertions(+), 41 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
bcf2d5c Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
c120bda fix(fase-4.5): cancello — file d'istruzioni degli agenti non scrivibili a ogni livello (V-1 bot #160)
39b1ba6 chore(revisore): memoria review #225 — APPROVATO
bfe71a7 chore(revisore): memoria review #224 — APPROVATO CON RISERVE
d3a593d docs(fase-4.5): report fine-task — gas notte + cancello rinforzato (PR #160)
d0cfc17 fix(fase-4.5): chiude V-1/V-2/V-3 verifica esterna, V-1 bot e R-221/R-222 su gas notte
c1f093c chore(revisore): memoria review #223 — APPROVATO CON RISERVE
c052d7c chore(revisore): memoria review #222 — APPROVATO CON RISERVE
1ece5c4 chore(revisore): memoria review #221 — APPROVATO CON RISERVE
680dafb docs(fase-4.5): report fine-task — gas notte fetta 1 (PR #160)
2a2ed0d feat(fase-4.5): gas notte — giro autonomo dei compiti dal catalogo (fetta 1)
365e27d chore(revisore): memoria review #220 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `2a2ed0d` — review #220, verdetto integrale del revisore:

## VERDETTO: APPROVATO CON RISERVE

Il commit si può fare. Nessuna regola del "Wall of Shame" viene violata: non c'è slicing diretto della cronologia e non c'è output dei tool simulato. Il cancello e il cap di 10 iterazioni restano quelli di `run_turn`, che non è stato toccato. Ho trovato quattro riserve di gravità BASSA (sotto); vanno scritte in `reports/stato_progetto.md`.

**Elementi del diff esaminati**

1. `modules/notte/notte.py:135` — ogni compito parte con `kernel.history = []` e a :136 `kernel.db_path` punta a `.gas_notte/storia_<nome>.json`, così la cronologia dell'operatore non entra nella finestra né viene sovrascritta. Il nome non può uscire dalla cartella perché la regex di :47 ammette solo `[a-z0-9_-]{1,40}`. Ho provato a togliere il cambio di `db_path` (mutation): 2 test FAIL, quindi i test lo coprono. Esito: ok.
2. `modules/notte/notte.py:80` — `_dentro` confronta i path dopo `resolve()`, quindi un catalogo dentro la root viene rifiutato anche se ci arriva tramite symlink (testato). Hardlink e parent fuori root non li ho provati. Esito: ok.
3. `modules/notte/notte.py:152` — nel diario va una sola riga di metadati (`fonte="kernel"`). Ho provato ad aggiungere il testo della risposta alla riga (mutation): `test_diario_solo_metadati` FAIL. Le righe di diario delle singole tool call restano quelle di sempre di `run_turn` (riassunto degli argomenti), come di giorno. Esito: ok.
4. `modules/notte/notte.py:202-207` — lock non bloccante: se un altro giro è in corso esce con codice 2 dentro il try, e il `finally` chiude il file. Su Windows (`fcntl` None) gira senza lock, ed è dichiarato. Esito: ok.
5. `gas.py:3583` — `notte_cmd` più il dispatch in `main()` sono l'unica modifica al kernel. L'import è pigro, quindi non ci sono effetti al caricamento. Esito: ok.
6. `tests/test_unit_notte.py:162` — round-trip agentico §7 col kernel vero: read_file, poi calcola, poi la risposta finale. Verifica anche che la storia dell'operatore resti intatta e che "SEGRETO" non arrivi mai al provider. Esito: ok.
7. `.github/workflows/ci.yml:133` — nuovo passo `if: always()` con `pipefail`, e nessun `paths-ignore` aggiunto. Esito: ok.

Risultati riprodotti da me: `test_unit_notte.py` 20 passed; `tests/test_unit_kernel.py` 707 PASS, 0 FAIL. Dopo le mutation il file è stato ripristinato e confrontato con l'index (nessuna differenza).

**Riserve**

- **R-220-1 (BASSA)**: l'isolamento della cronologia regge fino alla firma, non oltre.
  - Un'azione notturna messa in attesa e poi firmata su Telegram viene eseguita dal kernel del bot (`modules/telegram/bot.py:225`, che usa `.gas_history.json`).
  - `_storia_esito_firma` (`gas.py:1553`) scrive la notifica e l'output del tool nella conversazione dell'operatore.
  - L'output finisce nel ruolo tool, quindi la contaminazione viene comunque calcolata. Va però corretta la frase "non sporca la conversazione dell'operatore" nel docstring di `notte.py` e in `reports/setup_notte.md`, oppure in una fetta futura va legato l'esito della firma alla storia del compito.
- **R-220-2 (BASSA)**: `GasKernel.__init__` (`gas.py:659`) legge comunque `.gas_history.json` prima che `notte` azzeri la cronologia. Se il file è corrotto lo rinomina in `.corrupt.*` anche durante il giro notturno. Questo contraddice "non viene letta". Rimedio possibile: un parametro del kernel che salta il caricamento della storia.
- **R-220-3 (BASSA)**: non c'è un tetto di tempo né per compito né per giro. Un provider bloccato, tra timeout e retry del client, può allungare il giro di ore. È limitato (10 iterazioni per 4 provider), ma non dichiarato.
- **R-220-4 (BASSA, coincide col rischio (a) che hai dichiarato)**: `.gas_notte/` non è tra i prefissi vietati di `modules/gate/gate.py:76` (`_DENY_PREFIXES`). Il problema riguarda anche `launchd.log`, che sta in quella cartella secondo il plist: di giorno Gas può scriverlo (quindi falsificarlo) e leggerlo. Rimedio: aggiungere `.gas_notte` ai prefissi vietati. È una modifica al cancello, quindi va revisionata.

**Rischi esclusi (non verificati)**

- Comportamento reale di launchd sul Mac (risveglio dallo stop, creazione del log, caricamento di `.env` con zsh): non riproducibile in questo ambiente Linux.
- Corsa tra un giro notturno e una sessione diurna o il bot attivi in contemporanea sullo stesso `.gas_memory.db`: non l'ho testata. Mi affido al WAL di SQLite già in uso.

Ho aggiunto in memoria la riga #220 e la lezione: l'isolamento di un'esecuzione autonoma va seguito anche lungo il percorso della firma, cioè chi esegue l'azione approvata e in quale cronologia scrive l'esito. Le ho committate col commit `365e27d`, che contiene solo quel file; il diff staged sotto review è rimasto com'era.

---

Commit `d0cfc17` — review #221 (prima parte del diff: V-1/V-2/V-3 della verifica esterna), verdetto integrale del revisore:

## VERDETTO: APPROVATO CON RISERVE

In breve: le tre correzioni della verifica esterna funzionano. La correzione del tetto di spesa (V-1), però, porta con sé una regressione nell'exit code che conviene chiudere in questa stessa PR, prima del merge. Ci sono poi tre riserve minori sui test e sul conteggio.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9), `reports/stato_progetto.md` (le parti su notte e R-220) e la mia memoria (dalla #195 alla #220). Il diff non contiene slicing della storia né output dei tool simulati. `run_turn`, il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Elementi del diff esaminati**

1. `modules/notte/notte.py:239` — se `_env_budget() <= 0.0` imposta `GAS_DAILY_TOKEN_BUDGET="1.0"` solo per questo processo e scrive un avviso.
   - **Rischio:** che il valore non arrivi davvero al limite di spesa del kernel, oppure che `_env_budget` interpreti l'env in modo diverso da `_env_float` (`gas.py:435`).
   - **Esito:** ok. Assente, "0", "nan", "abc", "inf" e valori negativi portano tutti a 1.0. Un valore valido messo dall'operatore viene rispettato. Il kernel lo rilegge a ogni turno (`gas.py:2491`), quindi il valore impostato dal giro conta. `test_budget_esaurito_ferma_il_compito` lo prova con il kernel vero.
   - **Riserva:** vedi R-221-1.
2. `modules/notte/notte.py:265` (contesto non toccato, ma ora raggiunto dal nuovo avviso) — `return 1 if avvisi else 0`.
   - **Rischio:** che un avviso solo informativo cambi l'exit code.
   - **Esito:** riserva, R-221-1.
3. `modules/notte/notte.py:153-155` — conta le azioni negate (output che inizia con `"Operazione negata"`) e quelle in attesa (output che contiene `"in attesa di approvazione umana"`).
   - **Rischio:** falsi positivi e rami non coperti dai test.
   - **Esito:** riserva, R-221-3 e R-221-4.
4. `modules/notte/notte.py:190` — riga di conteggio per compito e frase finale corretta.
   - **Esito:** ok. La frase non promette più la firma quando la richiesta è stata revocata, e `test_unit_notte.py:228` controlla "negate: 1".
5. `tests/test_unit_notte.py:319` — test V-3: tiene un `LOCK_SH | LOCK_NB` sul file di lock e si aspetta exit 2.
   - **Esito:** ok. Con `LOCK_SH` al posto di `LOCK_EX` il secondo lock condiviso verrebbe concesso e il test fallirebbe.
6. `tests/test_unit_notte.py:231` — `test_budget_notte_di_default`.
   - **Esito:** ok sul comportamento, riserva sulla pulizia dell'ambiente (R-221-2).

**Riproduzioni**
- `test_unit_notte.py`: 23 passed.
- `tests/test_unit_kernel.py`: 707 PASS, 0 FAIL.
- `pytest tests/` completo: 716 passed.
- `notte.py` ripristinato dopo la mutation e identico allo staged.

**Finding**

- **R-221-1 (MEDIA, regressione introdotta da questo diff).** L'avviso del budget va nella lista `avvisi`, e la riga 265 la usa per decidere l'exit code.
  - **Effetto:** con un catalogo vuoto, o con tutti i compiti disattivati, e senza budget nel `.env`, il giro esce con 1 invece che con 0. Riprodotto: RC 1 senza budget, RC 0 con budget.
  - **Perché conta:** contraddice il docstring di `esegui_notte` ("0 ... o nessuno attivo"), e il timer notturno segnerebbe l'unità come fallita ogni notte.
  - **Fix:** mettere l'avviso del budget in una lista separata, oppure calcolare l'exit code solo sugli avvisi del catalogo. Aggiungere un test: catalogo vuoto senza budget → 0.
- **R-221-2 (BASSA, test).** `monkeypatch.delenv(..., raising=False)` su una variabile assente non registra nulla. Il `GAS_DAILY_TOKEN_BUDGET=1.0` impostato da `esegui_notte` resta quindi attivo nei test successivi dello stesso processo. Una sonda lo ha mostrato ("LEAK: 1.0"). Oggi è innocuo (716 passed), ma resta una fonte di test instabili: nella fixture `_ermetico` serve `setenv` seguito da `delenv`, oppure una pulizia esplicita alla fine.
- **R-221-3 (BASSA, test).** La mutation che spegne il ramo "in attesa" (riga 155) sopravvive: 23 passed. Tutti i test girano senza Telegram, quindi ogni azione parcheggiata viene revocata e il ramo "in attesa" non viene mai provato. Il diff dichiara 4 mutation colte, ma questo ramo non è coperto.
- **R-221-4 (BASSA).** Alla riga 155 il controllo `_IN_ATTESA in out` è una ricerca di sottostringa anche sull'output di `read_file`/`run_command`, che è testo non fidato.
  - Un file che contiene la frase gonfia il conteggio "in attesa della tua firma" nel riepilogo.
  - Inoltre "Azione già in attesa ..." (`gas.py:1512`) conta due volte lo stesso ID.
  - **Fix:** usare `startswith` su `"Azione in attesa di approvazione umana"` (`gas.py:1540`) ed escludere il caso "già".

**Rischi non verificati**
- Il comportamento reale con Telegram configurato (firma vera, conteggio "in attesa" lungo il percorso del bot): non è riproducibile in dev senza token. Per questo è anche una lacuna di test (R-221-3).
- Il comportamento sotto systemd/launchd sulla VPS: ho dedotto l'impatto di R-221-1 dall'exit code, non l'ho provato su un timer reale.
- `reports/setup_notte.md` (passo 2b) l'ho solo letto: coerente col codice.

**Altro**
- Nel worktree ci sono modifiche NON staged a `modules/gate/gate.py` e `tests/test_unit_gate.py`. Sono fuori da questa review: se finiscono in staging, serve una review a parte.
- Memoria aggiornata in `/home/user/Gas/.claude/agents/memoria_revisore.md` (riga #221 più una lezione nuova), commit `1ece5c4`.

---

Commit `d0cfc17` — review #222 (gate + chiusura R-221), verdetto integrale del revisore:

## VERDETTO: APPROVATO CON RISERVE

La fix fa quello che promette: chiude la catena venv / `.py` nella root segnalata dal bot (V-1) e chiude le riserve R-221-1..4. Restano scrivibili altri file che vengono eseguiti fuori dalla sandbox (gli script `.sh`, R-222-1, gravità MEDIA). Il problema esisteva già prima e questo diff non lo peggiora, ma ricade nella stessa minaccia di V-1.

Letture fatte: CLAUDE.md sez. 5, `reports/stato_progetto.md` (solo le parti che servivano), memoria #202–#221.

**Prove rifatte da me:** gate + notte 129 passed, kernel 707 PASS / 0 FAIL, `tests/` 748 passed. Ho provato quattro mutazioni del codice e i test le colgono tutte:
- exit code calcolato di nuovo da `avvisi` → 1 test fallisce;
- conteggio "in attesa" per sottostringa invece che per prefisso → 1 fallisce;
- `rstrip("/. ")` tolto → 1 fallisce;
- `".git"` tolto dai prefissi → 3 falliscono.

Ho ripristinato i file e controllato che `git diff` sia vuoto.

### Elementi del diff esaminati
- `modules/gate/gate.py:92-95`: aggiunge `venv`, `.venv`, `.git`, `.gas_notte` ai prefissi vietati.
  - Rischio: rompere `run_command`, perché il controllo per sottostringa a :234 usa gli stessi prefissi.
  - Ho provato in os_strict: `git status`, `git log --oneline`, `git -C . diff`, `ls -la`, `grep -rn prevent .` restano UNCERTAIN. `cat .github/workflows/ci.yml` diventa DENY, ed è voluto.
  - Esito: **ok**.
- `modules/gate/gate.py:102` / `:158`: il controllo sui suffissi si applica solo a `write_file`, sul percorso già normalizzato (NFKC, normpath, minuscole) più `rstrip("/. ")`.
  - Rischio: aggirare il blocco. Ho provato `yaml.PY`, `yaml．py` (punto fullwidth), `yaml.py/.`, `yaml.py ` + NBSP / U+3000, `a/../yaml.py`, `sitecustomize.py`, `__pycache__/*.pyc`, `*.cpython-311-darwin.so`: tutti DENY.
  - `yaml.py\t`, uno spazio invisibile (ZWSP) dentro `venv` e la `у` cirillica passano, ma creano un file DIVERSO, che Python non importa: innocui.
  - Una cartella `openai/` senza `__init__` è solo un namespace package e non oscura il pacchetto installato in site-packages.
  - Gas non può creare symlink: `write_file` scrive solo contenuto e `run_command` vede la root in sola lettura (`--ro-bind`, gas.py:1344).
  - Esito: **ok**.
- `gas.py:1652` (contesto): `applica_firma` riclassifica col cancello PRIMA di `execute_tool_call`. La tua premessa ("dopo la firma si passa solo da `_safe_path`") non è corretta: il nuovo DENY vale anche per le azioni già in attesa di firma create prima della fix. Esito: **ok**.
- `modules/notte/notte.py:239` / `:266`: `catalogo_ko` dipende solo dagli avvisi del catalogo. L'avviso sul budget è aggiunto dopo e non cambia più l'exit code. Il test `tests/test_unit_notte.py:344` lo copre. R-221-1 **chiusa**.
- `tests/test_unit_notte.py:33-34`: `setenv` seguito da `delenv`. Ho seguito l'ordine in cui pytest annulla le modifiche: prima rimette "0", poi cancella la variabile. Il budget che il giro imposta viene quindi ripulito. R-221-2 **chiusa**.
- `modules/notte/notte.py:155`: conteggio per prefisso. "Azione già in attesa" non viene contato. R-221-3 e R-221-4 **chiuse**, ma con la riserva R-222-2.

### Riserve
- **R-222-1 (MEDIA, c'era già prima, stessa minaccia di V-1).** Gli script `.sh` sono scrivibili a finestra pulita (UNCERTAIN, eseguiti senza firma) e poi girano fuori dalla sandbox:
  - `scripts/hash_diff_staged.sh` lo lancia l'hook `review_gate` di Claude Code: è proprio l'hash del cancello di review;
  - `scripts/gasmerge.sh` gira tramite il symlink in `~/bin/gasmerge`, col token gh dell'operatore;
  - lo stesso vale per `scripts/fine_task_finale.sh`.

  L'ho verificato: `write_file scripts/gasmerge.sh` → UNCERTAIN. Fix: aggiungere `.sh`, `.zsh`, `.bash`, `.command` a `_DENY_WRITE_SUFFIXES`, oppure `scripts` a `_DENY_PREFIXES`. Stessi casi ma con testo invece di codice: `CLAUDE.md` e `.mcp.json` (letti dall'agente di sviluppo, che ha la shell), `gas_identity.md` (finisce nel prompt di sistema), `requirements.txt` (pip). Tutti oggi UNCERTAIN.
- **R-222-2 (BASSA).** Il commento a `modules/notte/notte.py:155` ("mai testo di file/comandi") è falso.
  - `read_file` restituisce il contenuto grezzo del file (gas.py:2401), `run_command` lo stdout grezzo (gas.py:2376).
  - Un file che INIZIA con "Azione in attesa di approvazione umana" (o con "Operazione negata") gonfia quindi i conteggi del riepilogo.
  - Il test a :352 mette la frase solo in mezzo alla riga, non all'inizio, quindi non copre il caso.
  - Effetto limitato a un numero nel riepilogo. Fix: un segnale dal kernel invece del testo, oppure correggere il commento.
- **R-222-3 (BASSA).** `_IN_ATTESA` (`modules/notte/notte.py:58`) ricopia a mano la stringa di gas.py:1540, e nessun test usa il kernel reale. Se il testo in gas.py cambia, il conteggio scende a 0 senza alcun errore. Il test con lo stub uccide la mutazione ma non lega le due stringhe.
- **R-222-4 (BASSA, autonomia: da dire all'operatore).**
  - Gas non può più scrivere nessun file `.py`, nemmeno su richiesta esplicita: il DENY non si può firmare, e il ricontrollo a gas.py:1652 lo nega anche dopo una firma.
  - Gas non può più leggere `.gas_notte/ultimo_giro.md`, quindi non sa rispondere a "cosa hai fatto stanotte?". Stesso discorso per `.github/` e `.gitignore`.

### Cosa NON ho verificato
- Il comportamento reale su macOS/APFS (plist launchd, `source venv/bin/activate` sotto zsh): non riproducibile in questo ambiente Linux. Ho ragionato su come Python cerca i moduli, senza un run su Mac.
- Che non esistano symlink nella root del Mac dell'operatore: qui non ce ne sono (`find -type l` vuoto). Un symlink già presente che punta dentro `venv/` passerebbe il controllo lessicale del cancello, e `_safe_path` (gas.py:1139) non elenca `venv`.
- Il ramo Telegram configurato con un kernel reale (R-221-3 è chiusa solo con lo stub).

La memoria è aggiornata: riga contatore #222 più una lezione, committata come c052d7c in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Il diff in stage è rimasto intatto (5 file).

---

Commit `d0cfc17` — review #223 (diff finale: chiusura R-222), verdetto integrale del revisore:

## VERDETTO: APPROVATO CON RISERVE

Le riserve R-222-1, R-222-2 e R-222-3 risultano chiuse e l'ho verificato direttamente. R-222-4 è una scelta accettata, che va comunicata all'operatore. Restano due riserve BASSE, nessuna bloccante.

Letture preliminari fatte: CLAUDE.md (sez. 5, 6, 8), le voci di `reports/stato_progetto.md` cercate con Grep, `.claude/agents/memoria_revisore.md` fino alla #222.

**Elementi del diff esaminati**

1. `modules/gate/gate.py:171` — Il controllo sul primo livello del percorso (`_DENY_WRITE_TOP_PREFIXES`) guarda solo il primo pezzo del percorso già normalizzato (NFKC, normpath, maiuscole ridotte) e scatta solo in scrittura.
   - Rischio esaminato: aggiramento con `./`, maiuscole, `../`, pezzi vuoti.
   - Sonde DENY: `./scripts/x`, `././scripts/x`, `a/../scripts/x`, `dati/./../scripts/x`, `scripts//x`, `scripts/./x`, `SCRIPTS/x`, `ｓcripts/x` (lettera a larghezza piena), `scripts\x`, `x/../CLAUDE.md`, `CLAUDE.MD`, `claude.md ` e `claude.md.`, `.MCP.JSON`, `REQUIREMENTS.txt`, `requirements.in`.
   - `dati/scripts/x` resta UNCERTAIN, come previsto.
   - Percorsi `.`, `./` e `''`: l'elenco dei pezzi è vuoto, la guardia `parts[:1]` evita l'IndexError e il risultato è UNCERTAIN (la scrittura su una cartella fallisce più avanti nel kernel).
   - **ok**
2. `modules/gate/gate.py:105` — Aggiunte le estensioni `.sh`, `.zsh`, `.bash`, `.command` ai file non scrivibili, controllate su `norm.rstrip("/. ")`.
   - Rischio esaminato: varianti del suffisso.
   - `x.SH`, `x.sh/` e `a.command ` danno DENY; `x.sh.txt` resta UNCERTAIN, ed è corretto.
   - Mutation riprodotte su una copia: senza il controllo di primo livello 7 test falliscono, senza le estensioni di shell ne falliscono 4.
   - **ok**
3. `modules/gate/gate.py:112` — Il controllo è di sola scrittura: CLAUDE.md, `scripts/` e `requirements` restano leggibili (sez. 6). Il test `tests/test_unit_gate.py:394` copre i casi annidati.
   - **ok**
4. `modules/notte/notte.py:156` — Il commento ora dichiara il limite noto (un file o un output che inizia con la stessa frase gonfia il conteggio) invece della frase falsa di prima.
   - **ok**
5. `tests/test_unit_notte.py:374` — Il test controlla che le frasi contate dal giro notturno compaiano davvero nel codice del kernel (`inspect.getsource(gas.GasKernel)`).
   - Mutation riprodotta: cambiando la frase in `gas.py` il test fallisce.
   - **ok**

**Prove riprodotte:** gate + notte 147 passed; `pytest tests/` 766 passed. La suite kernel (707/0) non l'ho rieseguita a parte: il diff non tocca `gas.py`.

**Riserve (BASSE, da tracciare in stato_progetto.md)**

- **R-223-1 (BASSA)** — `reports/` resta scrivibile da Gas a finestra pulita (`reports/stato_progetto.md` ha dato UNCERTAIN). Quei file sono letti per obbligo dal revisore (stato_progetto.md) e dal bot di verifica (handoff). È lo stesso tipo di rischio chiuso per CLAUDE.md: testo che diventa istruzioni per agenti con privilegi. Da valutare un DENY in scrittura su `reports`, oppure dichiararlo come rischio accettato.
- **R-223-2 (BASSA, difesa in profondità)** — Il nuovo divieto di scrittura è solo testuale, dentro il cancello, e non è ripetuto in `_safe_path` (gas.py:1184), che lavora sul percorso reale dopo aver seguito i link. Un collegamento simbolico nella root lo aggirerebbe. Oggi non è sfruttabile: la sandbox monta la root in sola lettura (gas.py:1344), write_file non crea collegamenti e nella root non ce ne sono.

**Rischio escluso:** non ho verificato il comportamento su macOS con launchd (filesystem che non distingue le maiuscole, normalizzazione NFD), perché non è riproducibile in questo container. Il casefold del cancello copre il caso maiuscole, ma non l'ho provato su un filesystem reale di quel tipo. Non ho controllato nemmeno i file di configurazione di pytest (`pytest.ini`, `setup.cfg`, oggi UNCERTAIN): senza un `.py` scrivibile non ho trovato un modo di eseguire codice.

**Memoria:** riga #223 più una lezione nuova, committate con `scripts/commit_memoria_revisore.sh` (commit `c1f093c`). Il diff staged è rimasto intatto (5 file).


Commit motore `c120bda` (V-1 del bot su `d3a593d`: file d'istruzioni degli agenti scrivibili sotto il primo livello). Due passaggi, verdetti integrali:

### Review #224

## VERDETTO: APPROVATO CON RISERVE

In breve: la correzione chiude V-1 (dal primo livello a qualsiasi profondità del percorso), non blocca percorsi legittimi e lascia libera la lettura di CLAUDE.md. Restano due riserve basse, nessuna bloccante.

Letture fatte: CLAUDE.md (§5, §8, §9), reports/stato_progetto.md letto a pezzi con Grep, memoria del revisore (ultime review #204–#223, comprese le lezioni #222/#223 sui file d'istruzioni per gli agenti).

**Elementi del diff esaminati**

1. `modules/gate/gate.py:119` — `_DENY_WRITE_ANY_PART_NAMES = {"claude.md","claude.local.md","agents.md"}`.
   - Rischio esaminato: nomi messi in modo da non coincidere più con l'uscita di `_normalize_path` (NFKC + normpath + casefold).
   - Esito: **ok**. I nomi sono già minuscoli e in forma normale, e il confronto è esatto, non per prefisso.

2. `modules/gate/gate.py:182` — se l'operazione è una scrittura e un qualsiasi pezzo del percorso normalizzato è uno di quei nomi, il risultato è DENY.
   - Rischi esaminati: falsi DENY, la lettura di CLAUDE.md bloccata per sbaglio, aggiramenti.
   - Sonde (write → read):

     | Percorso | Scrittura | Lettura |
     |---|---|---|
     | `tests/CLAUDE.md` | DENY | SAFE |
     | `tests/CLAUDE.md/.` | DENY | SAFE |
     | `x/../tests/CLAUDE.md` | DENY | SAFE |
     | `Claude.Local.MD` | DENY | SAFE |
     | `dati/agents.md/x.txt` (cartella con quel nome) | DENY | SAFE |
     | `dati/claude.md.txt` | UNCERTAIN | SAFE |
     | `dati/note_claude.md` | UNCERTAIN | SAFE |

   - Nessun falso DENY realistico: blocca solo un pezzo del percorso che si chiama esattamente così. La regola vale solo in scrittura, quindi la lettura resta SAFE.
   - Esito: **ok**.

3. `tests/test_unit_gate.py:398-406` — test parametrico con 9 casi.
   - Ho rifatto la mutation (regola spenta → 8 FAIL), poi ho ripristinato il file. Il 9° caso è coperto dal prefisso di primo livello, come dichiarato.
   - Esito: **ok**.

4. `scripts/notte/catalogo_esempio.yaml:13` — `git status` sostituito con `ls -la`, con una nota che spiega che git non è tra i comandi consentiti.
   - Il compito resta `attivo: false`.
   - Esito: **ok**.

**Riproduzioni**
- gate + notte: 156 passed.
- `pytest tests/`: 775 passed.
- Il primo giro completo dopo la mutation dava 8 FAIL. Era un artefatto mio, non del codice: la mutation lascia il file della stessa dimensione e l'ho ripristinato nello stesso secondo, quindi Python ha riusato il `.pyc` del mutante. Ho cancellato `__pycache__`, rieseguito, e ho ottenuto 775 passed. Lezione registrata in memoria.

**Riserve**
- **R-224-1 (BASSA):** `AGENTS.override.md` resta UNCERTAIN, cioè scrivibile quando la finestra non contiene input esterno. Codex lo carica come istruzioni con precedenza su AGENTS.md, e l'operatore usa Codex nella stessa cartella (R-155-3). Basta aggiungere `"agents.override.md"` al frozenset. GEMINI.md e `.cursorrules` li considero fuori scope: quegli agenti non sono in uso. `.github/copilot-instructions.md` è già coperto dal prefisso `.git`, e `.claude/` a qualunque profondità è già coperto da `_in_denylist`.
- **R-224-2 (COSMETICA):** `tests/CLAUDE.md ` (spazio finale) e `tests/CLAUDE.md.` restano UNCERTAIN. Il controllo sui suffissi usa `rstrip`, quello sui nomi no. Su Linux e APFS sono file diversi, che Claude Code non carica: innocuo.

**Rischio escluso:** non ho rieseguito la suite del kernel (707 PASS). Il diff non tocca `gas.py` e cambia solo come `gate_classify` classifica `write_file`, che la suite in `tests/` copre. Non ho verificato neanche il comportamento di macOS con nomi in forma NFD sul Mac dell'operatore: non è riproducibile in questo ambiente.

La riga #224 e la lezione sono in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole in bfe71a7. Il diff in stage è intatto: 3 file, +24/−2.

### Review #225

## VERDETTO: APPROVATO

In breve: R-224-1 è chiusa. `AGENTS.override.md` ora non è più scrivibile a qualsiasi livello del percorso, la lettura resta consentita e i test riprodotti passano tutti.

Letture fatte: CLAUDE.md §5, stato_progetto.md letto a pezzi con Grep, memoria del revisore (#224 compresa).

**Elementi del diff esaminati**

1. `modules/gate/gate.py:121` — `"agents.override.md"` aggiunto a `_DENY_WRITE_ANY_PART_NAMES`, con commento R-224-1.
   - Rischi esaminati: falsi DENY, la lettura bloccata per sbaglio, il nome scritto in una forma che non coincide con il percorso normalizzato.
   - Esito: **ok**. Il nome è minuscolo e già normalizzato; il confronto è esatto su ogni pezzo e vale solo in scrittura (`:182` invariato).

   | Percorso | Scrittura | Lettura |
   |---|---|---|
   | `AGENTS.override.md` | DENY | SAFE |
   | `dati/agents.override.md` | DENY | SAFE |
   | `dati/agents.override.md.txt` | UNCERTAIN | SAFE |

2. `tests/test_unit_gate.py:398-403` — due casi in più nel test parametrico (`AGENTS.override.md`, `dati/agents.override.md`).
   - Rischio esaminato: test vacuo, cioè che passa anche senza la regola.
   - Esito: **ok**. Ho tolto il nome dal frozenset e i 2 casi falliscono. Ho poi ripristinato il file (`git diff` vuoto) e cancellato `__pycache__`.

3. `scripts/notte/catalogo_esempio.yaml:13` — invariato rispetto alla #224 (`ls -la`): **ok**.

**Riproduzioni**: rieseguite con `PYTHONDONTWRITEBYTECODE=1` per non ricadere nel problema del `.pyc` vecchio della #224.
- gate + notte: 158 passed.
- `pytest tests/`: 777 passed (775 + 2 casi nuovi).

**Riserve**: nessuna nuova. R-224-2 (spazio o punto finale nel nome) resta cosmetica e lasciata di proposito.

**Rischio escluso:** non ho rieseguito la suite del kernel (707 PASS). `gas.py` non è toccato e il cambio riguarda solo come il cancello classifica `write_file`, che la suite in `tests/` copre. Non ho verificato neanche se la versione di Codex usata dall'operatore legga davvero `AGENTS.override.md`: mi baso sulla documentazione, perché qui non è riproducibile.

La riga #225 è in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da sola in 39b1ba6. Il diff in stage è intatto: 3 file, +26/−2.

---

## §5 DELTA TEST DEL MOTORE

- **Suite kernel** (`python tests/test_unit_kernel.py`): 707 PASS prima e dopo. Output reale: `=== RIEPILOGO: 707 PASS, 0 FAIL ===`.
- **Suite notte** (`tests/test_unit_notte.py`): 0 → 26 test.
- **Suite cancello** (`tests/test_unit_gate.py`): 104 → 132 test (121 + 11 casi di `c120bda`).
- **Insieme notte + cancello**: `158 passed`.
- **`python -m pytest tests/`**: 777 passed (dichiarato dal revisore #225; in questa sessione 775 prima degli ultimi 2 casi).
- **V-3 bot**: la suite kernel dà 707 PASS in locale e 709 PASS in CI (stesso file, stesso SHA): scarto fisso di 2 già noto su main, causa non indagata.
- **Mutation colte**:
  - reset della cronologia;
  - catalogo dentro la root;
  - testo nel diario;
  - lock condiviso;
  - tetto di spesa di default;
  - conteggio delle azioni negate e in attesa;
  - exit code;
  - controllo `isfinite`.

## §6 STATO CI

`gh` non è autenticato (`Failed to log in to github.com using token (GH_TOKEN)`): le run sono state lette con lo strumento GitHub Actions della sessione.

| Commit | Run CI | Stato |
|---|---|---|
| `2a2ed0d` | CI run 37800758579 (#765), push | handoff-check failure (atteso: l'handoff arriva col commit di fine-task, come riportato anche dal bot) |
| `365e27d` | nessuna run su questo SHA | pushato insieme a `2a2ed0d` |
| `680dafb` | CI run 37800887986 | success (unit-suite, handoff-check) — check `verifica-bot`: **failure (BOCCIATO, V-1 MEDIA)**, corretto in `d0cfc17` |
| `1ece5c4`, `c052d7c`, `c1f093c` | nessuna run su questi SHA | pushati insieme a `d0cfc17` |
| `d0cfc17` | CI run 37803770301 (#767), push; verifica-bot run 37803772906 | (letta nella sessione precedente; superata da `d3a593d`) |
| `d3a593d` | CI run 37803950160 | success (unit-suite, handoff-check); `verifica-bot`: primo tentativo cancelled, secondo tentativo (run 37803954238) **failure (BOCCIATO, V-1 MEDIA)**, corretto in `c120bda` |
| `bfe71a7`, `39b1ba6`, `c120bda`, `bcf2d5c` | nessuna run propria | pushati insieme al commit di fine-task |
| commit di fine-task che contiene questo file | — | run non ancora disponibile alla scrittura dell'handoff |

## §7 RISERVE APERTE

**Aperte, tutte BASSE** (tracciate in `reports/stato_progetto.md`, voce 6):
- R-220-2 — l'`__init__` del kernel legge `.gas_history.json`.
- R-220-3 — nessun tetto di tempo.
- R-223-1 — Gas può ancora scrivere in `reports/`, che il revisore e il bot leggono.
- R-223-2 — il divieto di scrittura è solo testuale e non è ripetuto in `_safe_path`. Oggi non è sfruttabile.

**Aperta, COSMETICA:** R-224-2 — `tests/CLAUDE.md ` (spazio o punto finale) resta UNCERTAIN; innocuo.

**Chiuse in questa sessione:**
- V-1 e V-2 del bot su `d3a593d`; R-224-1;
- R-220-1 e R-220-4;
- R-221-1..4;
- R-222-1..3;
- V-1, V-2, V-3 della verifica esterna;
- V-1 del bot di verifica.

**Scelta accettata:** R-222-4.
