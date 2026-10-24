# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-24 — Chat Motore: R2 via B fetta 3 (note BASSE del cervello forte chiuse, ancora spento)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #262 (https://github.com/Gasss23/Gas/pull/262): tocca motore e template fine-task; ultima review #503 APPROVATO.
2. Prima di accendere il forte: prova sul Mac di `claude -p` col login Max di Gas (R-496-3).
3. Testo nuovo dell'attività di notte da chiedere nella sessione fissa; 3 lezioni da approvare sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Costo su ogni errore (R-497-1)**: `FATTA`.
- **Prezzo per famiglia e pavimento (V-1 bot/ve #258)**: `FATTA`.
- **Conto sotto lucchetto, attesa limitata, forte fermo se il consumo non si registra (R-496-2, R-502-1/2)**: `FATTA`.
- **Costi non finiti (V-4 ve #258)**: `FATTA`.
- **Doctor «Cervello forte» (R-497-2)**: `FATTA`.
- **Messaggio dei file protetti (R-498-1), deroga n/d nel template (R-501-1)**: `FATTA`.
- **Campo `cervello: forte` nel catalogo notturno, setup del Mac**: `DEFERITA — dopo la prova del login`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 .claude/commands/fine-task.md      |   4 ++--
 .gitignore                         |   1 +
 brains/claude_cli.py               | 130 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------
 gas.py                             | 133 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------
 reports/diff_sessione.md           |  15 +++++++++------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  25 +++++++++++++------------
 tests/test_unit_claude_cli.py      |  90 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 tests/test_unit_kernel.py          |  55 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — la riga di `reports/handoff.md` è n/d e la riga di totale è tolta; le altre righe sono prese con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
e3e4eea fix(r2): numeri enormi in usage o total_cost_usd non fanno perdere il costo (V-1 ve #262)
74acd99 chore(revisore): memoria review #506 — APPROVATO
25028b0 chore(revisore): memoria review #505 — BOCCIATO
f906586 fix(doctor): «comando claude» presente solo se eseguibile davvero (V-1 bot #262)
2a94e8d chore(revisore): memoria review #504 — APPROVATO
af82b7b docs(fine-task): report R2 via B fetta 3 (review #503)
9161425 feat(r2): fetta 3 del cervello forte — costo su ogni errore, conto sotto lucchetto, doctor
a779e43 chore(revisore): memoria review #503 — APPROVATO
c1409f7 chore(revisore): memoria review #502 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare nel log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: 9161425 `feat(r2): fetta 3 del cervello forte` (review #502 → #503) il fix del doctor dopo il bot #262 (review #504) e il fix dei numeri enormi dopo la verifica esterna #262 (review #505 → #506).

### Review #502 (APPROVATO CON RISERVE, riserve corrette prima del commit)

## VERDETTO: APPROVATO CON RISERVE

Review #502 (chat Motore). Diff staged in /home/user/Gas: R2 via B fetta 3, con il cervello forte ancora spento. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci R2 di reports/stato_progetto.md (R-496-2, R-497-1/2, R-498-1) e la memoria. Ho applicato la lezione #496/#498: ogni nuovo file di stato va nella denylist e va provato col kernel reale.

**Elementi del diff esaminati**
- `brains/claude_cli.py:308`: ramo `except RuntimeError` / `except Exception` attorno a `_risposta`. Rischio: che cambi la classificazione QUOTA o il fallback. I RuntimeError escono con il messaggio originale e il «429 » resta in testa. Il costo si aggiunge solo se manca. Solo le eccezioni impreviste vengono avvolte in «risposta non valida», che non è un limite. In `run_turn` il ramo `except` resta uguale: registra il costo e poi `raise`, quindi il fallback non cambia. **ok**
- `brains/claude_cli.py:299`: un JSON che non è un oggetto e un'uscita non JSON portano `stima_minima`, calcolata una sola volta prima del runner. Il prefisso `_prefisso_limite` resta. **ok**
- `brains/claude_cli.py:189`: `_costo_equivalente` usa il prezzo della famiglia del modello. Una famiglia sconosciuta prende 15/75, cioè fail-closed; il pavimento vale anche su `total_cost_usd`. Prove dirette: `_prezzo("x")=(15,75)`; 1e-9 su sonnet dà 0.0015; nessun valore negativo passa. **ok**
- `brains/claude_cli.py:206`: `_token` con `usage` non numerico. Prova diretta: `"abc"` e `inf` danno (0,0) senza eccezioni, perché OverflowError è intercettato. **ok**
- `gas.py:1650`: flock sul file `.lock` attorno a lettura, somma e scrittura. Prova con 4 processi × 50 registrazioni da 0.01: il risultato è 2.0 esatto, nessun aggiornamento perso. Il fail-closed resta: con conto illeggibile la funzione esce sotto lucchetto senza scrivere. **riserva R-502-1**: il `LOCK_EX` è bloccante e senza timeout. La sezione critica è breve e un crash libera il lucchetto, ma un detentore fermo (SIGSTOP, disco lento) blocca il turno all'infinito. Nel repo c'è già la convenzione `LOCK_NB` a `gas.py:1319`.
- `gas.py:1646`: costi infiniti o negativi ignorati con warning; T99m PASS. **ok**
- `.gitignore:55`: lockfile aggiunto. Prova col kernel reale (`execute_tool_call`): `write_file` e `read_file` sono negati su `.gas_claude_cli_uso.json.lock`, `.GAS-claude-cli-uso.json.lock` e `sub/.gas_claude_cli_uso.json.lock`. Lo nega il prefisso esistente a `gas.py:1903`, e lo stesso prefisso c'è nel cancello `modules/gate/gate.py:104`. **ok**
- `gas.py:4887`: sezione «Cervello forte» del doctor. Usa solo `_env_flag`, `shutil.which` e `_leggi_uso_claude_cli`: nessuna chiamata a `claude`, nessun token consumato. Il tetto ha lo stesso default e gli stessi limiti di `_tetto_claude_cli_superato`. T99n PASS e l'ambiente viene ripristinato da `_saved99`. **ok**
- `gas.py:2507`: messaggio di diniego (R-498-1). **ok**
- `.claude/commands/fine-task.md:131`: il segnaposto del §2 e il commento di 4bis citano la regola «n/d»; chiude R-501-1. **ok**

**Controlli generali**
- §5 (Wall of Shame): nessuno slicing della history, nessun output di tool simulato. I test usano runner finti iniettati per la CLI, non risultati di tool inventati.
- §9: le eccezioni restano intercettate. `_registra_uso_claude_cli` non solleva mai e scrive un warning nel log.
- Cap 10 iterazioni: non toccato.

**Test rieseguiti da me**
- `tests/test_unit_claude_cli.py`: 20 passed.
- `tests/test_unit_kernel.py`: 1037 PASS, 0 FAIL.

**Riserve, da tracciare in reports/stato_progetto.md prima di accendere `GAS_CLAUDE_CLI`**
- **R-502-1 BASSA**: `fcntl.flock(..., LOCK_EX)` a `gas.py:1653` è senza timeout dentro il turno. Usare `LOCK_NB` con tentativi limitati: se il lucchetto non arriva, il turno va fermato o il consumo scritto lo stesso, mai un'attesa infinita.
- **R-502-2 BASSA**: se il lockfile non si apre, il lucchetto non si prende o la scrittura fallisce, c'è solo un warning e il consumo non entra nel conto. È fail-open sul tetto (il problema c'era già per `os.replace`; ora si aggiunge il caso del lockfile). Da valutare un fermo del forte quando la registrazione fallisce.
- **R-502-3 COSMETICA**: il ramo `except Exception` generico (`brains/claude_cli.py:308`) non ha un test, e il lockfile manca dalla lista `_TARGETS_68s` (`tests/test_unit_kernel.py:4399`). La protezione l'ho verificata solo a mano.

**Rischi esclusi**
- La CLI `claude` vera non è stata chiamata: il forte è spento e consumerebbe l'abbonamento. Il formato reale di `total_cost_usd` e `usage` resta quello dei test.
- Il lucchetto su macOS e su file system di rete (NFS) non è stato verificato: qui c'è solo Linux locale.
- La suite pytest completa (2141 passed) non l'ho rieseguita io: ho eseguito le due suite toccate.

Riga #502 e una lezione nuova (lucchetti nel turno solo con `LOCK_NB` o timeout) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate con `scripts/commit_memoria_revisore.sh` (commit c1409f7).

### Review #503 (verdetto finale sul diff committato)

## VERDETTO: APPROVATO

Ho letto prima CLAUDE.md (sez. 5, 8, 9 e 10), poi le righe R2 di reports/stato_progetto.md e infine la memoria del revisore. Questa è la review #503: l'ultima in memoria era la #502.

**Cosa ho controllato nel diff**
- `gas.py:1659` — il lucchetto sul conto ora si prende con `LOCK_EX | LOCK_NB`, riprovando ogni 0,05 s fino a `LOCK_STORIA_SEC` (5 s, `gas.py:1284`, la stessa regola del lucchetto della storia). Scaduto il tempo parte un `TimeoutError` dentro il `with`: il file si chiude e l'errore lo prende l'`except Exception`. Il rischio era che il turno restasse bloccato: non succede. Esito: ok, R-502-1 chiusa.
- `gas.py:1679` — il blocco `finally` accende `_forte_senza_conto` solo se il consumo non è stato registrato e il conto non era già fermo. Rischio esaminato: il flag acceso per sbaglio nei casi normali. Nel percorso normale si arriva sempre a `registrato=True`, anche quando il costo è 0, non numerico, infinito o negativo (diventa 0.0 e si scrive comunque). Nel ramo «conto già illeggibile» il `return` dentro il `with` passa dal `finally` con `fermo_gia=True`, quindi il flag resta spento ed è corretto, perché il forte lo ferma già `_uso_claude_cli`. Se arriva un `KeyboardInterrupt` il flag si accende e l'interruzione prosegue: va bene. Esito: ok.
- `gas.py:1688` — `_tetto_claude_cli_superato` legge il flag con `getattr` (non serve inizializzarlo nel costruttore) e restituisce `(None, tetto)`: il forte si ferma fino al riavvio, cioè fail-closed. La chiamata sta dentro `if name == "claude-cli"` (`gas.py:4668`), quindi gli altri provider non cambiano. Il messaggio di `_errore_tetto_forte` ora parla anche dell'aggiornamento non riuscito e del riavvio. Esito: ok, R-502-2 chiusa.
- Windows (`fcntl` None, contesto `gas.py:12`): si fa solo l'`open(..., "a")` del lockfile, senza attesa e senza lucchetto; lettura, somma e scrittura avvengono come prima. Niente si rompe. Esito: ok.
- §9 (eccezioni intercettate e loggate): `_registra_uso_claude_cli` intercetta tutto e logga come warning («scrittura fallita … — forte fermo»). Il flag non solleva mai e i due punti di chiamata (`gas.py:4686`, `gas.py:4718`) non cambiano. Nel ramo `except` della create, il `raise` nudo arriva dopo la registrazione: il fallback degli altri provider e il retry di Gemini restano come prima. Esito: ok.
- `tests/test_unit_kernel.py:4408` — il lockfile è nella lista T68s (scrittura negata al modello). `tests/test_unit_kernel.py:10952` — in T99o un altro fd tiene il lucchetto: misurati 0,20 s di attesa, conto fermo a 0.25, tetto `(None, 4.60)`; poi il flag e `LOCK_STORIA_SEC` vengono ripristinati. Esito: ok.
- `brains/claude_cli.py:308` — il ramo `except Exception` generico ora ha un test: l'eccezione diventa «claude-cli: risposta non valida» col costo. Esito: ok, R-502-3 chiusa.
- `.claude/commands/fine-task.md:131` — il segnaposto «output GREZZO» e il commento di 4bis ora citano la regola «n/d». Esito: ok, chiude anche R-501-1 (cosmetica).
- `.gitignore`: aggiunto `.gas_claude_cli_uso.json.lock`. Esito: ok.

**Prove rieseguite da me**
- claude_cli: 21 passed.
- kernel: 1038 PASS, 0 FAIL (T99o e T68s PASS).

**Nota di design (non è una riserva)**: in un processo che resta acceso a lungo (il bot) basta un solo errore passeggero di disco o di lucchetto per fermare il forte fino al riavvio, senza che si rimetta in moto da solo. È voluto (meglio fermo che consumare senza conto) e il messaggio dice di riavviare. Il doctor non vede questo flag, perché vive solo dentro il processo.

**Cosa NON ho verificato**
- Il comportamento vero su Windows: niente ambiente Windows qui, l'ho valutato leggendo il codice.
- Il flock su filesystem di rete (NFS, dove può dare `ENOLCK`): non riproducibile qui. Leggendo il codice, finirebbe in `except` e fermerebbe il forte (fail-closed).
- Non ho rieseguito il pytest completo (dichiarato 2142 passed, 1 skipped) né fatto una prova con un mutante sul flag.

**Memoria**
- Riga #503 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova.
- Committata da sola con `scripts/commit_memoria_revisore.sh` (commit a779e43). Il resto dello stage non è stato toccato.

### Review #504 (commit fix doctor, V-1 bot #262)

## VERDETTO: APPROVATO

Review #504 (chat Motore), diff staged della PR #262, correzione del finding V-1 del bot.

Elementi del diff esaminati:
- `gas.py:4912` — il doctor ora calcola il binario con `shutil.which(os.environ.get("GAS_CLAUDE_BIN") or "claude")`. Rischio esaminato: un percorso falso dato come «presente», e casi limite. Ho provato dal vero: un percorso assoluto inesistente dà None, una cartella dà None, `/bin/ls` restituisce il percorso, una stringa vuota ricade su "claude" grazie a `or`. Il risultato è coerente con l'adattatore in `brains/claude_cli.py:253`: un nome relativo viene risolto nel PATH sia da `which` sia da subprocess. Esito: ok.
- `gas.py:4913` — la riga del check mostra WARN con «non trovato o non eseguibile». Rischio esaminato: il doctor chiama claude e consuma l'abbonamento. Nella funzione doctor gli unici subprocess sono `git` (`gas.py:5010`, `gas.py:5022`), il forte non viene mai invocato. Esito: ok.
- `tests/test_unit_kernel.py:10970` — T99p imposta `GAS_CLAUDE_BIN=/non/esiste/claude` e si aspetta WARN; la variabile viene ripristinata in un `finally`, anche se prima non c'era (pop). Rischio esaminato: la variabile resta sporca per i test successivi. Esito: ok. Output reale: `[WARN ] Cervello forte comando claude non trovato o non eseguibile`.
- `tests/test_unit_kernel.py:10982` (contesto, T99n) — l'asserzione controlla solo «spento», «conto di oggi $0.25» e «WARN forte fermo», mai la riga «comando claude». Rischio esaminato: il test dipende dalla presenza di `claude` nel PATH della CI. Non ne dipende. Esito: ok. Qui claude è nel PATH, ma con `PATH=/usr/bin:/bin` `which` dà None, e T99n non lo guarda.

Esecuzione: kernel 1039 PASS 0 FAIL, `tests/test_unit_claude_cli.py` 21 passed.

Rischio escluso: non ho verificato come si comporta `which` su un file che esiste ma non è eseguibile sul Mac/VPS reale, né con permessi ACL particolari. Il caso «non eseguibile» non ha un test dedicato (T99p copre solo «non esiste»). L'ho accettato perché è la semantica documentata di `shutil.which` (controlla `os.access(X_OK)`). Nessuna riserva aperta.

Memoria: aggiunta la riga #504 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con `scripts/commit_memoria_revisore.sh` (commit 2a94e8d). Nessuna lezione nuova.

### Review #505 (BOCCIATO, corretto prima del commit)

## VERDETTO: BOCCIATO

Review #505 (chat Motore), diff staged della PR #262: chiusura della V-1 della verifica esterna #262 (overflow nel calcolo del costo).

**Elementi del diff esaminati**
- `brains/claude_cli.py:215`: `_n` ora limita ogni conteggio a `_TOKEN_MASSIMI`. Ho controllato se restano overflow dai token e se il tetto falsa conteggi veri. Prove dirette: `inf` va a 0 (OverflowError intercettato), `1e300` va al tetto, una stringa di 500 cifre va al tetto, il costo resta finito (90000.0). **ok**
- `brains/claude_cli.py:180`: `_TOKEN_MASSIMI = 10**9`. Ho controllato se il tetto falsa conteggi realistici. Il contesto massimo è circa 1M token e con `--tools ""` c'è un solo giro, quindi il tetto sta circa 1000 volte sopra qualsiasi chiamata vera. Al tetto il costo vale circa 120000 $, quindi il tetto giornaliero scatta comunque. **ok**
- `tests/test_unit_claude_cli.py:301`: il nuovo test copre `usage` enorme sul ramo riuscito e su quello d'errore. Però non prova lo stesso valore ostile in `total_cost_usd`. **riserva** (diventa parte del blocco)

**Motivo bloccante (stessa V-1, campo diverso)**
- `brains/claude_cli.py:202`: `float(v)` su `total_cost_usd` intero enorme (`10**400`, che `json.loads` restituisce come int) solleva OverflowError fuori da ogni try. Ho fatto la prova col runner dei test (`_runner` e `_ok`):
  - risposta riuscita con `total_cost_usd = 10**400`: si ottiene `OverflowError`, SENZA `costo_equivalente_usd`. Il percorso: `brains/claude_cli.py:345` passa al ramo generico `except Exception`, che ricalcola `_costo_dati` a `brains/claude_cli.py:313` e risolleva lo stesso OverflowError nudo;
  - risposta d'errore con `total_cost_usd = 10**400`: stesso risultato, `OverflowError` SENZA costo. Qui l'eccezione parte dentro l'`except RuntimeError`, alla riga `brains/claude_cli.py:309`.
- Contesto: `gas.py:4687` intercetta `Exception`, quindi niente crash e il fallback parte, ma registra `getattr(e, "costo_equivalente_usd", 0.0)`, cioè 0. Il tetto perde il consumo: è esattamente il sintomo della V-1.
- Correzione suggerita: in `_costo_equivalente` intercettare `OverflowError` attorno a `float(v)` (oppure scartare gli int fuori dall'intervallo prima di convertire) e far ricadere sulla stima dai token. Poi aggiungere al test il caso `total_cost_usd = 10**400` su entrambi i rami.

**Altri percorsi verificati**
- `brains/claude_cli.py:284`, `(len(sistema) + len(stdin)) // 4`: `len` è limitato dalla memoria, quindi anche 10^12 caratteri danno un prodotto float finito. **ok**
- `total_cost_usd` float `1e400` (inf) o nan: scartato dal controllo `v == v and 0 < v < 1000`. **ok**

**Rischio escluso**: non ho verificato `_registra_uso_claude_cli` in `gas.py` con costi al tetto (circa 1,2e5 $). Mi sono basato sulla review #503 («0/inf/negativo → 0») e sul fatto che un valore finito grande fa solo scattare il tetto. Non ho rilanciato le suite complete (22 passed e 1039/0 sono dichiarati dall'agente): ho fatto solo prove mirate.

**Memoria**: riga #505 e una lezione nuova (provare il valore ostile su tutti i campi numerici dello stesso calcolo, non solo su quello del finding). Ho lanciato `scripts/commit_memoria_revisore.sh`: commit `25028b0` con solo `/home/user/Gas/.claude/agents/memoria_revisore.md`.

File rilevanti:
- /home/user/Gas/brains/claude_cli.py
- /home/user/Gas/tests/test_unit_claude_cli.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- /tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/t.py (script di riproduzione)

### Review #506 (commit fix numeri enormi, V-1 ve #262)

## VERDETTO: APPROVATO

Re-review #506 (chat Motore) della PR #262, dopo il BOCCIATO #505. Prima della review ho letto CLAUDE.md (§5 sugli antipattern, §8 sui limiti API, §9 sulla gestione degli errori), `reports/stato_progetto.md` (la parte sul cervello forte via `claude -p`) e la memoria del revisore, inclusa la lezione #505: un valore ostile va provato su tutti i campi numerici.

Elementi del diff esaminati:
- `brains/claude_cli.py:202` — `float(v)` di `total_cost_usd` ora è dentro un try: un OverflowError diventa nan, e il confronto `v == v` fa usare la stima dai token. Rischio esaminato: un intero enorme fa uscire un'eccezione senza costo attaccato. Provato con 10**400, -10**400, inf, -inf, nan, '5', None, True, 0, 1e-300 e [1]: danno tutti il pavimento 0.0015 (sonnet). Il BOCCIATO #505 è chiuso. Esito: ok.
- `brains/claude_cli.py:218` — tetto `_TOKEN_MASSIMI` (10**9) su ogni campo di `usage`. Rischio esaminato: overflow o costo infinito dai token. Provato con inf, nan, una stringa di 5000 cifre (int() dà ValueError, intercettato), una lista e un `usage` che non è un dict: tutti diventano 0. Con tutti e 4 i campi a 10**400 il costo è 120000 $, un numero finito che fa scattare il tetto giornaliero (va nella direzione sicura, cioè il forte si ferma). Esito: ok.
- `tests/test_unit_claude_cli.py:301` — `test_token_enormi_non_rompono_il_costo` copre 10**400 sia in `usage` sia in `total_cost_usd`, sul ramo riuscito e su quello d'errore, con costo finito e positivo. Esito: ok. È una nota cosmetica, non una riserva: il test controlla solo `0 < costo < inf` e non il valore esatto del pavimento.
- Contesto: `brains/claude_cli.py:296` — un intero JSON con più di 4300 cifre fa fallire `json.loads` con ValueError, che il codice già intercetta: il costo diventa `stima_minima`. Un float JSON 1e400 diventa inf, che è già gestito. Esito: ok.
- Contesto: `gas.py:4715` — il kernel passa `prompt_tokens`/`completion_tokens` (massimo 3·10**9, interi) a `_log_tokens`, e `gas.py:4719` il costo, ormai sempre finito, a `_registra_uso_claude_cli`. Esito: ok.

Altri percorsi di overflow: non ne restano nel calcolo del costo né nei campi numerici della risposta. `returncode` finisce solo dentro una f-string, `subtype` e `result` sono stringhe ripulite.

Nessuna violazione del Wall of Shame: niente slicing della storia, niente output dei tool simulato. Nessun limite indebolito.

Rischio escluso: non ho verificato il comportamento con la CLI `claude` vera, perché nel container non c'è il login. La sonda ha usato solo il runner dei test e chiamate dirette alle funzioni. Resta valido quanto già dichiarato prima: un `total_cost_usd` tra 0 e 1000 riportato dalla CLI viene preso per buono (999.9 → 999.9). È una scelta di progetto che c'era già, non nasce da questo diff.

Test: claude_cli 22 passed (ho rilanciato io la suite). Suite del kernel non rilanciata: questo diff non tocca `gas.py`.

Memoria: aggiunta la riga #506 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da `scripts/commit_memoria_revisore.sh` (commit 74acd99, solo quel file). Il diff staged del motore è rimasto intatto. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1035 → 1039 PASS (T99m, T99n, T99o, T99p nuovi; lockfile in T68s), 0 FAIL.
  `=== RIEPILOGO: 1039 PASS, 0 FAIL ===`
- `pytest tests/test_unit_claude_cli.py`: 19 → 22 passed.
- `pytest tests/` completo: `2142 passed, 1 skipped in 194.63s (0:03:14)`.

## §6 STATO CI

`gh run list -L 3` alle 21:39 UTC:

```
completed	success	R2 via B fetta 3: costo su ogni errore, conto sotto lucchetto, doctor del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	40134316028	3m6s	2026-10-24T21:27:48Z
completed	skipped	R2 via B fetta 3: costo su ogni errore, conto sotto lucchetto, doctor del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	40134312898	1s	2026-10-24T21:27:46Z
completed	success	docs(fine-task): report R2 via B fetta 3 (review #503)	CI	feat/merge-automatico-z1xjx2	push	40134311011	2m58s	2026-10-24T21:27:44Z
```

Mappatura: af82b7b (testa precedente): CI verde (unit-suite, handoff-check), verifica-bot neutral (APPROVATO CON RISERVE). Commit successivi (memoria #504, fix doctor, memoria #505/#506, fix numeri enormi) e il commit di fine-task: una sola run sul push, sulla testa; run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-496-3** (BASSA): login vero col portachiavi del Mac (e `CLAUDE_CODE_OAUTH_TOKEN` sulla VPS) da provare con l'ambiente ridotto.
- Prezzi di riferimento per famiglia da ritarare con l'uso vero (dichiarato nel codice).
- Comportamento dichiarato (nota di design #503): un errore di registrazione del consumo ferma il forte fino al riavvio; il doctor non vede questo fermo.
- **V-2 bot #262** (BASSA): se la registrazione del consumo fallisce si ferma solo il processo che ha fallito; gli altri processi contano una chiamata in meno e dopo il riavvio quel consumo è perso (al massimo una chiamata per evento).
- **R-498-2** (BASSA, preesistente): alcuni log scrivibili dal modello a finestra pulita.
