# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Cervello forte: difesa contro il futuro default `--bare` di `claude -p` (chat M2, coordinata da M1) — aggiornato dopo il bot su 5e784c3

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #321 (https://github.com/Gasss23/Gas/pull/321). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5114638285","url":"https://github.com/Gasss23/Gas/pull/321"}`); `gh` nel cloud non è autenticato. Stanotte niente merge (M1): decide l'operatore.
2. Sul Mac: `python3 gas.py doctor` → la riga «Cervello forte · login» deve dire «login dell'abbonamento».

---

## §1 SCOPE & ESITO FETTE

- **1. Figlio `claude -p` senza chiavi API (fail-closed se diventa bare)**: `FATTA` — test che lo fissa.
- **2. Flag o variabile per restare non-bare**: `FATTA (nessuno documentato)` — scritto nel docstring.
- **3. Riga «login» nel doctor, con versione, zero token**: `FATTA` — `stato_abbonamento()` in brains, 3 righe in gas.py autorizzate da M1.
- **V-1 della verifica esterna su d0a0035** («abbonamento» anche con CLI non loggata): `FATTA` (review #634-M2). V-2 ve (il doctor non vede in anticipo il cambio di default): dichiarata nel docstring.
- **V-1 bot su 5e784c3** (test T99 della suite kernel che lanciavano il `claude` vero dal doctor): `FATTA` (review #635-M2); **R-635-1** (interruttore ereditato dalla shell): `FATTA` (review #636-M2). **V-2 bot** (handoff e stato_progetto non allineati): `FATTA` in questo giro di report.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 brains/claude_cli.py               |  57 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 gas.py                             |   3 +++
 reports/diff_sessione.md           |  17 ++++++++---------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  33 +++++++++++++++------------------
 tests/test_unit_claude_cli.py      |  92 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_dotenv.py          |  20 ++++++++++++++++++++
 tests/test_unit_kernel.py          |  15 +++++++++++++--
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
c83032f docs(forte-non-bare): report dopo il bot su 5e784c3 (PR #321, review #635/#636-M2)
5e2fd43 test(forte): la suite kernel non lancia mai il claude vero dal doctor (V-1 bot #321 su 5e784c3, R-635-1; review #635/#636-M2)
f6a6d9e chore(revisore): memoria review #636 — APPROVATO
e59a4f5 chore(revisore): memoria review #635 — APPROVATO CON RISERVE
735a0b2 chore(revisore): memoria review #635 — APPROVATO CON RISERVE
5e784c3 docs(forte-non-bare): report dopo la verifica esterna su d0a0035 (PR #321, review #634-M2)
612369a fix(forte): «login dell'abbonamento» solo se la CLI dice anche di essere loggata (V-1 ve #321, review #634-M2)
d0a0035 docs(forte-non-bare): report di fine task (PR #321, review #632/#633-M2)
2f5d53d fix(forte): difesa contro il futuro default --bare di claude -p; riga «login» nel doctor (chat M2)
26ecd7a chore(revisore): memoria review #632 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit 2f5d53d è stato rivisto in due passaggi sullo stesso diff staged (tra i due cambia solo `stato_abbonamento` e i suoi test). Verdetti integrali:

Review #632-M2 (primo passaggio):

## VERDETTO: BOCCIATO

Diff controllato: diff staged con sha256 009335ee, base b472fe1, branch fix/forte-non-bare-m2, 4 file e 137 righe aggiunte. Ho rilanciato i test: test_unit_claude_cli più test_unit_dotenv danno 57 passed. Non ho rilanciato la suite del kernel.

**Motivo del blocco**
- `brains/claude_cli.py:416` (la riga `versione = (ver.stdout or "").strip().splitlines()[0][:60] ...`): ricava la versione dall'output di `claude --version`. Ho cercato le eccezioni che sfuggono al blocco `except (OSError, subprocess.SubprocessError)`. Esito: **blocco**. Ci sono due casi, entrambi riprodotti.
  1. Se `--version` stampa solo spazi o un a capo, `ver.stdout` non è vuoto, ma dopo `strip()` diventa `""` e `splitlines()[0]` dà IndexError. Ho lanciato `gas.py doctor` con `GAS_CLAUDE_BIN` puntato a una CLI finta che fa solo `echo`: il doctor si ferma con un traceback (`IndexError: list index out of range`).
  2. Se la CLI stampa byte non UTF-8 (prova con `printf "\377\376"` e LANG=C.UTF-8), `subprocess.run(text=True)` alza UnicodeDecodeError. È un ValueError, non un SubprocessError, quindi sfugge allo stesso modo.
  - Il docstring promette «Mai un'eccezione» e il progetto chiede «zero crash»: il doctor è proprio lo strumento di diagnosi e non deve morire per un output strano della CLI.
  - Correzione minima:
    - `errors="replace"` nella `subprocess.run`;
    - versione presa con `next(iter(stdout.strip().splitlines()), "?")`;
    - un `except Exception` finale che ritorna `("WARN", "non verificabile …")`;
    - due casi di test in più (stdout `"\n"` e byte non UTF-8 con il runner vero).

**Elementi esaminati che vanno bene**
- `brains/claude_cli.py:406` (`stato_abbonamento`): lancia solo `--version` e `auth status`, mai `-p`. Rischio cercato: spendere token. Esito: ok. Il test parametrico fissa la sequenza esatta dei comandi e la CLI finta del test del doctor esce con 9 su qualunque altro comando. Il timeout di 15 s per comando arriva come TimeoutExpired, che è un SubprocessError, quindi viene preso.
- `brains/claude_cli.py:430`: smista i casi none, rc≠0, api_key e simili. Rischio cercato: dare OK quando il login non è l'abbonamento. Esito: ok. OK arriva solo per claude.ai e oauth_token; JSON illeggibile o metodo mancante danno WARN. Nota cosmetica: con rc≠0 e `api_key` il messaggio dice «nessun login», ma l'esito resta WARN, che è corretto.
- `gas.py:5087`: chiama `stato_abbonamento` solo se `binario` è stato trovato. Rischio cercato: modifiche fuori dal perimetro autorizzato da M1. Esito: ok. In gas.py ci sono 3 righe in tutto (import a `gas.py:35` e la chiamata nel doctor), dentro le 3-4 autorizzate. Il crash descritto sopra, però, si propaga fin qui.
- `brains/claude_cli.py:53` (contesto, `_ENV_PERMESSE`): elenco esatto delle variabili che il figlio riceve. Rischio cercato: il comportamento fail-closed, cioè che una chiave API arrivi al figlio. Esito: ok. Nessuna ANTHROPIC_*, *_API_KEY, CLAUDE_CODE_SIMPLE o BEDROCK passa; CLAUDE_CODE_OAUTH_TOKEN sì. Lo verificano `tests/test_unit_claude_cli.py:398` e, con il runner vero, `tests/test_unit_claude_cli.py:446`.
- `tests/test_unit_dotenv.py:265`: riga «login» del doctor con CLI finta, OK per claude.ai e WARN per api_key, con la versione. Esito: ok.
- Nessuno slicing della history e nessun output dei tool simulato: il diff non tocca `run_turn` né la finestra dei messaggi.

**Riserve da annotare (non bloccanti)**
- BASSA: alla scadenza del timeout, `subprocess.run` uccide solo il processo figlio diretto. Se un processo nipote tiene aperte le pipe, la seconda `communicate()` può restare bloccata, quindi il limite di 15 s non è garantito in assoluto. Caso teorico.
- BASSA: nel caso peggiore il doctor aspetta circa 30 s (due comandi da 15 s).

**Cosa non ho verificato**
Non ho provato il comportamento della CLI `claude` vera: qui non c'è login, e non so se `auth status` stampi davvero il campo `authMethod`, né se in una versione futura possa aprire una sessione. Mi baso sulla documentazione cli-reference citata da M1. Non ho rilanciato la suite del kernel (1063 PASS), che resta un'affermazione della chat.

**Memoria del revisore**
Ho scritto la riga #632-M2 con la lezione nuova in `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (commit 26ecd7a, solo quel file). Il diff staged del motore è rimasto com'era. Dopo la correzione serve una nuova review.

Review #633-M2 (diff finale committato in 2f5d53d):

## VERDETTO: APPROVATO CON RISERVE

Ri-review dopo la bocciatura #632-M2. Branch fix/forte-non-bare-m2, diff staged di 4 file. Il motivo del blocco è chiuso: con le uscite strane della CLI che ho provato il doctor non va più in traceback.

**Cosa ho esaminato nel diff**
- `brains/claude_cli.py:409` — `subprocess.run` ora ha `errors="replace"`. Rischio esaminato: `UnicodeDecodeError` con byte non UTF-8. Esito: ok. Anche senza `errors=`, quell'errore è un `ValueError` e verrebbe comunque preso da `except ValueError` (`brains/claude_cli.py:421`): la difesa è doppia.
- `brains/claude_cli.py:414` — `next(iter(righe), "?")[:60]`. Rischio esaminato: `IndexError` con stdout vuoto, di soli spazi o di soli a capo, e con returncode diverso da 0. Esito: ok, la versione diventa «?».
- `brains/claude_cli.py:415-416` — `json.loads` è dentro lo stesso try. Con un runner che restituisce bytes, quelli non UTF-8 danno un `ValueError`, che viene preso. Esito: ok.
- `brains/claude_cli.py:424` — `except Exception` finale, che risponde «non verificabile (Tipo)». Esito: ok. È coerente con «robustezza > potenza» e con la regola della sez. 9 (eccezioni intercettate, fallback, mai crash), applicata qui al doctor. Il codice dopo il try (`brains/claude_cli.py:426-437`) usa `st` solo quando `metodo` è una stringa, quindi `st` esiste sempre.
- `gas.py:5088` — chiamata dal doctor solo se `binario` è valorizzato. Non cambia rispetto a #632. Esito: ok.
- `tests/test_unit_claude_cli.py:61` e `tests/test_unit_claude_cli.py:69` — test nuovi: versione «\n», «   » e «»; CLI finta col runner vero che stampa \377\376; runner che solleva `KeyError`. Esito: ok.

**Prove che ho rifatto io**
- Test di `claude_cli` e `dotenv`: **61 passed**.
- `GAS_CLAUDE_CLI=1 GAS_CLAUDE_BIN=<CLI finta> python3 gas.py doctor`, con due CLI finte: una che stampa `\377\376` e una che stampa `"   "`. In entrambi i casi esce la riga `[WARN ] Cervello forte login … non verificabile (versione …)` e nessun traceback.
- Mutante: tolto `errors="replace"` e ristretto l'`except` finale a `ZeroDivisionError` → **1 failed** (`test_stato_abbonamento_byte_non_utf8_e_errori_inattesi`). Il file è stato ripristinato; `git diff` non staged è vuoto.
- Antipattern della sez. 5: niente slicing della history (`[:60]` taglia una stringa di versione, non i messaggi) e niente simulazione dell'output dei tool.

**Riserve**
- R-633-1 BASSA (riportata dalla #632): un processo nipote che tiene aperte le pipe e l'attesa massima di circa 30 s (2 × timeout di 15 s). Sono già annotate nei report.
- R-633-2 BASSA: nessun test fissa da solo il ruolo di `errors="replace"`. Il ramo `except ValueError` lo copre comunque, quindi un mutante che toglie solo `errors=` probabilmente sopravvive. Il comportamento resta corretto.

**Cosa non ho verificato**
Non ho provato una CLI `claude` vera con login reale, né il comportamento con `--bare` di default. Qui non c'è un binario `claude` autenticato e quel default è un rilascio futuro, non riproducibile oggi.

**Memoria del revisore**
- Ho scritto la riga contatore `#633-M2 … APPROVATO CON RISERVE … Nessuna lezione nuova` in `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- `scripts/commit_memoria_revisore.sh` **non è partito**: l'hook `review_gate.sh` ha bloccato tutto il comando, perché `.claude/.review_ok` non corrisponde ancora al diff staged. La riga, che contiene anche lo SHA del diff, è stata scritta in un secondo comando senza lo script.
- Il file è modificato ma non in staging e non committato. Va committato dopo aver eseguito `bash scripts/segna_review_ok.sh`, oppure con `/fine-task`.
- Come richiesto, non ho committato nulla.

Commit della correzione V-1 ve (dopo d0a0035). Review #634-M2:

## VERDETTO: APPROVATO

Review #634-M2 (chat M2). Diff staged su fix/forte-non-bare-m2 (PR #321), 2 file, sha256 del diff c9f58d4c. Chiude la V-1 BASSA della verifica esterna #321.

Elementi del diff esaminati:
- `brains/claude_cli.py:424`: calcola `loggato` dentro il try, come `returncode == 0` e `loggedIn` non uguale a `False`. Ho controllato due rischi. (1) Un'eccezione fuori dal try: non può succedere, perché `isinstance` e `.get` girano solo su un dict e sono comunque coperti dall'`except Exception`. (2) Un JSON senza `loggedIn` (CLI vecchia): non viene penalizzato, perché il controllo `is False` è stretto e la chiave mancante dà None. Il caso della stringa `"false"` diventa truthy, ma con `rc != 0` cade comunque in WARN. Esito: ok.
- `brains/claude_cli.py:437-440`: OK solo se il metodo è dell'abbonamento E la CLI è loggata; altrimenti, con `metodo == "none"` o non loggato, «nessun login» (WARN). Rischio esaminato: il cambio di comportamento sui metodi diversi dall'abbonamento. Un `api_key` con `loggedIn:false` ora riceve «nessun login» invece di «NON dell'abbonamento». Prima con rc diverso da 0 era già così. Resta comunque WARN, quindi non c'è nessun falso OK. È una scelta di messaggio, non un difetto. Esito: ok.
- `brains/claude_cli.py:35-37`: il docstring del modulo dichiara il limite V-2: il doctor non vede in anticipo il cambio di default a `--bare`. È coerente con la difesa che chiude in caso di errore: il figlio non riceve chiavi API. Esito: ok.
- `tests/test_unit_claude_cli.py:433-434`: due casi nuovi nel test parametrico (claude.ai con rc 1; `loggedIn` false con rc 0), entrambi WARN «nessun login». Rischio esaminato: che i test siano solo di forma. Non lo sono: con il codice precedente il caso alla riga 434 dava OK, quindi il test cattura davvero la regressione. Esito: ok.

Contesto: `tests/test_unit_claude_cli.py:428` copre ancora il caso positivo (`loggedIn` true, rc 0, OK).

Ho eseguito `pytest tests/test_unit_claude_cli.py`: 44 passed. La suite dotenv non l'ho rilanciata: fa fede il dato del chiamante, 63 passed.

Antipattern (Wall of Shame): il diff non tocca la history; niente slicing, niente simulazione di tool. La funzione resta senza eccezioni e non chiama il modello. Il cap a 10 iterazioni e `_get_window` non vengono toccati.

Rischio escluso: non ho verificato `claude auth status` con la CLI vera; l'esempio di `rc` e `loggedIn` viene dalla doc, non da un'esecuzione. Non è riproducibile qui perché la CLI loggata con l'abbonamento sta sul computer di Gas.

Memoria del revisore: ho aggiunto la riga contatore `#634-M2 (chat M2) — 2026-11-02 — APPROVATO — …; nessuna lezione nuova` in /home/user/Gas/.claude/agents/memoria_revisore.md. Il commit atomico non è partito: `bash scripts/commit_memoria_revisore.sh` è stato negato dal classificatore dei permessi, e comunque avevi chiesto «Non committare». Il file è modificato ma non committato e va incluso nel commit di fine task.

Commit della correzione V-1 bot su 5e784c3 (5e2fd43). Il diff è stato rivisto in due passaggi: #635-M2 sul finto in `_doc99`, #636-M2 sullo stesso diff più la chiusura di R-635-1. Verdetti integrali:

Review #635-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #635-M2: PR #321, branch fix/forte-non-bare-m2. Lo SHA-256 del diff staged comincia con bd3d6e00 e il diff tocca solo tests/test_unit_kernel.py. Ho letto CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (voce «R2 e futuro default --bare», intorno alla riga 602) e la mia memoria.

**Elementi del diff esaminati**
- `tests/test_unit_kernel.py:11178` — dentro `_doc99()` sostituisce `gas.claude_cli_stato_abbonamento` con un finto che risponde ("OK", "finto (test T99)") e lo rimette com'era nel `finally`. Rischio esaminato: il finto non agisce perché il doctor potrebbe leggere la funzione per altra via, oppure non viene tolto se il doctor solleva un errore. Esito: **ok**. Il doctor la legge come nome globale del modulo al momento della chiamata, quindi la sostituzione funziona. Il ripristino nel `finally` copre anche il caso di errore. Il finto accetta qualunque argomento (`*a, **k`).
- `tests/test_unit_kernel.py:11186` — `gas.doctor(...)` ora gira dentro il `try`, con l'output catturato come prima. Rischio esaminato: le righe «Cervello forte» controllate da T99p, T99s, T99w e T99x cambiano. Esito: **ok**. La riga «login» non è tra quelle che quei test cercano («comando claude», «claude-cli»).
- Contesto: `gas.py:35` importa la funzione come `claude_cli_stato_abbonamento`. `gas.py:5088` la chiama solo se `binario` è stato trovato. Il punto del finto è quello giusto. Esito: **ok**.

**Prove riprodotte**
- Ho messo in testa al PATH un `claude` spia che registra gli argomenti. Suite kernel: 1063 PASS, 0 FAIL, registro vuoto. Il fix chiude la V-1 BASSA del bot.
- Stessa prova con `GAS_CLAUDE_CLI=1` esportato nella shell: 1063 PASS, ma il registro ha 24 righe, cioè 12 coppie `--version` / `auth status`.

**Riserva**
- **R-635-1 BASSA**: se la shell ha `GAS_CLAUDE_CLI=1` esportato, la suite kernel lancia ancora 12 volte il `claude` vero della macchina. Lo fanno gli altri helper che chiamano il doctor: `_doctor_inproc` a `tests/test_unit_kernel.py:2214`, `_doctor_inproc_61` a `tests/test_unit_kernel.py:3647` e le chiamate dirette a `tests/test_unit_kernel.py:7250` e `tests/test_unit_kernel.py:10166`. Ereditano l'interruttore dalla shell e non lo ripuliscono. Il `.env` non c'entra, perché la riga 53 imposta `GAS_NO_DOTENV=1`. Prima di questa PR il doctor non eseguiva mai `claude`, quindi il problema nasce con la riga «login». Impatto basso: sono comandi a zero token e non distruttivi. Correzione proposta: mettere il finto (o togliere `GAS_CLAUDE_CLI`) una volta sola in cima al modulo, accanto a `GAS_NO_DOTENV`, invece che solo in `_doc99`.

**Coerenza col progetto**: la modifica tocca solo un test. Non tocca `_get_window`, il tetto di 10 iterazioni, il tetto di output né i fallback §9. Nessuno slicing della cronologia. Il finto sta nel test e non simula l'output di un tool del modello, quindi non rientra nel divieto della sez. 5. La riga «login» vera resta provata in tests/test_unit_dotenv.py e tests/test_unit_claude_cli.py.

**Cosa non ho verificato**
- Il mutante «finto tolto → la spia viene chiamata» non l'ho rieseguito. Basta la logica: con `GAS_CLAUDE_CLI=1` e la spia nel PATH, `shutil.which` la trova e `gas.py:5088` la chiama.
- Non ho rieseguito tests/test_unit_dotenv.py e tests/test_unit_claude_cli.py, che il diff non tocca.
- Comportamento sul Mac non verificato: non riproducibile qui.

**Memoria**: aggiunta la riga #635-M2 e una lezione nuova (riprovare i fix «non lancia il binario vero» anche con l'interruttore acceso nella shell). Committata con scripts/commit_memoria_revisore.sh, ultimo commit e59a4f5. Il diff staged del test è rimasto com'era.

File: /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/gas.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #636-M2 (diff finale committato in 5e2fd43):

## VERDETTO: APPROVATO

Review #636-M2, PR #321, branch fix/forte-non-bare-m2. Diff esaminato: `git diff --cached`, solo `tests/test_unit_kernel.py`, sha256 fd182467.

Cosa ho esaminato nel diff:
- `tests/test_unit_kernel.py:59`: toglie `GAS_CLAUDE_CLI` dall'ambiente in testa al modulo, accanto a GAS_NO_DOTENV e alla pulizia delle variabili Telegram. Rischio esaminato: qualche test potrebbe contare sul valore ereditato dalla shell. Ho controllato tutti i punti che usano la variabile: `tests/test_unit_kernel.py:11019` e `tests/test_unit_kernel.py:11076` (la mettono a «1» da soli), `tests/test_unit_kernel.py:11056` (la mettono a None o «0» da soli), `tests/test_unit_kernel.py:11194` («0» e «1» espliciti), `tests/test_unit_kernel.py:11252` (salvata e ripristinata in finally). Il salvataggio `_saved99` adesso parte da None, e il ripristino resta corretto. La suite gira come script (CI: `python tests/test_unit_kernel.py`), quindi la rimozione vale solo per quel processo e per i suoi figli. Esito: ok, la riserva R-635-1 è chiusa.
- `tests/test_unit_kernel.py:11182`: in `_doc99` sostituisce `gas.claude_cli_stato_abbonamento` con una versione finta e rimette quella vera in `finally`. Rischio esaminato: la versione finta potrebbe restare attiva se il doctor solleva un'eccezione. Il `finally` la rimette sempre. Esito: ok (già approvato nella #635).

Riprodotto da me: `GAS_CLAUDE_CLI=1` esportato e un `claude` spia in testa al PATH che registra gli argomenti → 1063 PASS, 0 FAIL, file di registro della spia mai creato.

Rischio escluso: `tests/test_unit_dotenv.py` non l'ho rieseguito con la variabile esportata. È fuori dal diff e gestisce `GAS_CLAUDE_CLI` da sé con le sue fixture. Non ho verificato nemmeno l'ambiente della CI: lì la variabile non è impostata, quindi il caso non si presenta.

Memoria: ho aggiunto la riga contatore #636-M2 (nessuna lezione nuova) e l'ho committata con lo script (commit f6a6d9e). File: /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Test di `brains/claude_cli.py` e del doctor: `tests/test_unit_claude_cli.py` 29 → 44 test raccolti (V-1 bot su c83032f: prima qui c’era «42», numero rimasto da prima della V-1 ve), `tests/test_unit_dotenv.py` 17 → 19 (in tutto 61 passed dopo la correzione di #632, 63 dopo la V-1 ve: 2 casi in più nel parametrico; conteggi con pytest --collect-only alla base b472fe1 e al commit). Kernel (`tests/test_unit_kernel.py`, che chiama il doctor): RIEPILOGO 1063 PASS, 0 FAIL (prima della correzione di #632, che tocca solo `stato_abbonamento` e i suoi test). Dopo la V-1 bot: kernel 1063 PASS, 0 FAIL, anche con `GAS_CLAUDE_CLI=1` esportato e un `claude` spia in testa al PATH (spia mai chiamata). Prova a mano: doctor con CLI finta che stampa una riga vuota → «[WARN ] Cervello forte login … non verificabile», nessun traceback.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 5e784c3 (fine-task precedente, head allora): check completati (notifica check_suite.completed); bot APPROVATO CON RISERVE (V-1 BASSA, V-2 COSMETICA), chiuse in questo giro.
- c83032f (fine-task precedente, con 5e2fd43, f6a6d9e, e59a4f5, 735a0b2 pushati insieme: la run ha testato solo questa testa): handoff-check e smista success, suite kernel verde, le altre suite in corso alla lettura della verifica esterna; bot APPROVATO CON RISERVE (V-1 COSMETICA «29 → 42», corretta qui).
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-633-1-M2** BASSA: un processo nipote che tiene aperte le pipe può far durare oltre il timeout; attesa massima normale ~30 s (2 × 15 s).
- **R-633-2-M2** BASSA: `errors="replace"` senza un test dedicato (il ramo `except ValueError` lo copre comunque).
- Non verificato con una CLI `claude` vera e loggata: il campo `authMethod` viene dalla documentazione (cli-reference). Da provare sul Mac.
