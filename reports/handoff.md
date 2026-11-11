# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — voce più veloce: prima frase in anticipo dal cervello forte e tempi del forte nel log (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR dello streaming (URL nel commento della PR e nella descrizione, dalla risposta di `create_pull_request`): con verdetto del bot APPROVATO pulito e CI verde la mergia la chat; con riserve resta pronta per il «mergia» del mattino (riserva aperta R-773-2-M2 BASSA).
2. Prova sul Mac: dopo il merge e il riavvio del server voce, `grep "tempi claude-cli" gas_debug.log | tail -5` dice dove vanno i 6–7 s del cervello sul Mac (fuori_cli = avvio di Claude Code e login; ttft = attesa del primo token). Da incollare a M1/M2.

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Streaming della prima frase (ordine 1 di M1)**: `FATTA` (6e711ce). `claude -p` nei turni a voce scrive a flusso (stream-json); il testo della risposta finale arriva a pezzi solo se comincia con `"chiamate": []`; il server voce sintetizza la prima frase intera in un filo a parte e la usa SOLO se è identica alla prima frase della risposta finale. Dal vivo (cloud, sonnet low): prima frase pronta a ~2,1 s, risposta finale del client a ~3,4 s.
- **Tempi interni del forte nel log (richiesta di M1)**: `FATTA` (a9419ea). Riga `tempi claude-cli:` in gas_debug.log a ogni chiamata: tutto, prima_riga, primo_testo, richiesta, ttft, api, cli, fuori_cli, token.
- **R-773-1-M2 BASSA, R-773-3-M2 COSMETICA**: `FATTA` (a9419ea, review #778-M2).
- **Merge di origin/main (#370)**: `FATTA` (71b04fa, review #779-M2).
- **B3 BASSA audit notturno 2 (M1): uscita della CLI letta in UTF-8 con sostituzione** + cosmetiche del bot #374 (SIGKILL, risposta arrivata non è un timeout, log dei tempi che fallisce lascia traccia): `FATTA` (e9b05e5, review #781/#782-M2).
- **Niente schema strumenti nei turni a voce semplici (ordine 2)**: `DEFERITA` — misurato qui: lo schema da 9k caratteri pesa ~0,3 s; prima servono i tempi del Mac.
- **Processo CLI caldo (ordine 3)**: `DEFERITA` — non sicuro così com'è (il prompt di sistema e il codice dei ruoli cambiano a ogni chiamata); i tempi `fuori_cli` del Mac diranno se vale.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 brains/claude_cli.py               | 286 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 gas.py                             |  14 +++++++++++---
 modules/voice/server.py            |  74 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           | n/d
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           | n/d
 reports/stato_progetto.md          | n/d
 reports/ultimo_report.md           | n/d
 tests/test_unit_claude_cli.py      | 223 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          |  47 +++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_server.py    |  69 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: confronto con origin/main (e3eb542). Regola «n/d» — i conteggi dei report scritti in questo commit di fine-task non sono misurabili mentre li si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
e9b05e5 fix(cervello): uscita della CLI letta in UTF-8 con sostituzione (B3 audit notturno 2), SIGKILL, risposta arrivata non è un timeout, log dei tempi che fallisce lascia traccia — review #781/#782-M2 (chat M2)
567b1bb docs(fine-task): #374 — riserve della verifica esterna registrate (V-1 uscita di testo, cosmetiche) (chat M2)
ba9220c docs(fine-task): voce — prima frase in anticipo e tempi del forte (chat M2)
71b04fa Merge origin/main (#370) nello streaming della prima frase — review #779-M2 APPROVATO (chat M2)
a9419ea perf(voce): tempi interni del forte nel log, nipoti uccisi al timeout, pipe chiuse — review #778-M2 (chat M2)
6e711ce perf(voce): prima frase in anticipo — claude -p a flusso (stream-json), voce della prima frase preparata mentre il forte finisce — review #773-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #782-M2 (R-781-1) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #782-M2, PR #374. Ho rivisto tutto il diff in staging su /home/user/Gas-stream: brains/claude_cli.py, tests/test_unit_claude_cli.py e la memoria. Il nuovo test chiude R-781-1-M2; resta solo R-781-2-M2, BASSA.

**Elementi del diff esaminati**
- `tests/test_unit_claude_cli.py:790` — nuovo test `test_esegui_a_flusso_result_poi_appeso_restituisce_la_risposta`: il processo scrive la riga result, poi resta appeso (`sleep 30`), con timeout di 1 s. Il test controlla `returncode != 0` e che lo stdout sia proprio la riga result. Rischio esaminato: un test che non prende il mutante. Esito: ok. Ho rieseguito io il mutante (tolto `and risultato is None`): il test fallisce (1 failed). Poi ho rimesso il codice com'era e la copia di lavoro di `brains/claude_cli.py` è di nuovo identica allo staging (riga 482 presente).
- `brains/claude_cli.py:482` — TimeoutExpired solo se manca la riga result. Rischio esaminato: un processo appeso DOPO la riga result. Esito: ok. Il processo viene ucciso allo scadere del timeout e il chiamante (`brains/claude_cli.py:609`) usa la risposta già pagata, col costo vero.
- `brains/claude_cli.py:298` e `brains/claude_cli.py:427` — encoding UTF-8 con sostituzione dei byte non validi in `_esegui` e `_esegui_a_flusso`. Esito: ok, invariati rispetto alla review #781-M2.
- `brains/claude_cli.py:528` — `logging.warning` col solo tipo dell'eccezione in `_log_tempi_cli`. Esito: ok, nessun contenuto nel log.

Test: claude_cli 77 passed (rieseguito).

**Riserva aperta**
- R-781-2-M2 (BASSA): se la CLI resta appesa dopo la riga result, la risposta arriva solo allo scadere dell'intero timeout. Uscire subito alla riga result interromperebbe Claude Code mentre chiude: va valutato a parte, come proponi. Va tracciata in stato_progetto.md.

**Rischio escluso**: non ho verificato il comportamento sotto launchd sul Mac né con il locale reale della CLI, perché non si può riprodurre nel cloud.

Nessuno slicing della history, nessuna simulazione di tool, guardrail invariati.

**Memoria**: ho aggiunto la riga `#782-M2` in /home/user/Gas-stream/.claude/agents/memoria_revisore.md e il file è in staging (diff totale: 3 file, +34/−6). Il marcatore della review (`segna_review_ok.sh`) va creato dopo questo `git add`.

### Review #781-M2 (B3 e cosmetiche del bot) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #781-M2, PR #374. Ho rivisto il diff in staging su /home/user/Gas-stream (brains/claude_cli.py e tests/test_unit_claude_cli.py). Prima ho letto CLAUDE.md, reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `brains/claude_cli.py:298` — `_esegui` ora usa `encoding="utf-8", errors="replace"`. Rischio esaminato: un UnicodeDecodeError che sfugge al riconoscimento di limite e login e al costo. Esito: ok. Un byte non valido diventa «�» e i controlli testuali di limite e login continuano a funzionare.
- `brains/claude_cli.py:427` — `Popen` di `_esegui_a_flusso` con lo stesso encoding. `os.killpg` ora usa `signal.SIGKILL` (import a riga 47). Rischio esaminato: un decode che fallisce dentro il ciclo di lettura. Esito: ok.
- `brains/claude_cli.py:482` — TimeoutExpired solo se `scaduto` è impostato e `risultato is None`. Rischio esaminato: il caso che hai chiesto, cioè un processo che resta appeso DOPO aver scritto la riga `result`. L'ho provato con una sonda vera: lo script stampa la riga result, poi `sleep 30`, timeout 1,5 s. Risultato: il processo viene ucciso a 1,5 s e la funzione ritorna `CompletedProcess(returncode=-9, stdout=<riga result>)`, senza eccezione. Il chiamante (`brains/claude_cli.py:609`) fa il parse della riga e usa la risposta già pagata, col costo vero. Prima invece c'era TimeoutExpired con la sola stima minima del costo. `_effort_rifiutato` (`brains/claude_cli.py:290`) con codice -9 scatta solo se lo stderr contiene il rifiuto di `--effort`, cosa incompatibile con una riga result valida. Esito: comportamento corretto e migliore di prima.
- `brains/claude_cli.py:528` — `_log_tempi_cli` ora registra un `logging.warning` col solo nome del tipo d'eccezione. Rischio esaminato: dati della conversazione nel log. Esito: ok, nessun contenuto finisce nel log e il turno non si rompe (§9).
- `tests/test_unit_claude_cli.py:778` — il test usa un processo vero che scrive \xff su stdout e \xfe su stderr e passa da entrambi i runner. Esito: ok. Ho rieseguito con `LC_ALL=C`: 76 passed.

**Riserve (entrambe BASSE)**
- R-781-1-M2: nessun test copre il caso «riga result, poi processo appeso». Se si toglie `and risultato is None`, la suite resta verde. Va aggiunto un test come la mia sonda: result, poi sleep, timeout breve, controllo `returncode == -9` e stdout uguale alla riga result.
- R-781-2-M2: in quel caso la risposta arriva solo allo scadere dell'intero timeout, quindi a voce la latenza è piena. Il ciclo di lettura potrebbe uscire appena legge la riga result e chiudere il processo. È un miglioramento possibile, non un difetto introdotto dal diff.

**Rischio escluso**: non ho verificato il comportamento reale sotto launchd sul Mac, con il locale vero della CLI, perché non si può riprodurre nel cloud. La copertura viene solo dal test con `LC_ALL=C` e dal processo sintetico.

Nessuno slicing della history, nessuna simulazione di tool, guardrail invariati.

**Memoria**: ho aggiunto in coda la riga `#781-M2` in /home/user/Gas-stream/.claude/agents/memoria_revisore.md, nessuna lezione nuova. Il file è in staging (`git add`) come mi hai chiesto, quindi non ho eseguito `scripts/commit_memoria_revisore.sh`. Attenzione: ora la memoria fa parte del diff in staging, quindi il marcatore della review (`segna_review_ok.sh`) va creato dopo questo `git add`.

### Review #779-M2 (merge di origin/main) — verdetto integrale

## VERDETTO: APPROVATO

Review #779-M2: merge di origin/main e3eb542 (la #370 di M1) in perf/voce-streaming-m2, preparato in /home/user/Gas-stream, con HEAD a9419ea.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le parti di reports/stato_progetto.md che riguardano questa fetta e .claude/agents/memoria_revisore.md.

**Cosa ho guardato nel diff**
- `gas.py:5025` — aggiunge `su_testo_voce` alla firma di `run_turn`, accanto a `voce: bool`. Rischio: che il merge abbia perso o duplicato un parametro della #370. Rispetto a MERGE_HEAD, gas.py cambia solo in 14 righe: l'import di `Callable`, la firma con il suo commento e il costruttore. Esito: ok.
- `gas.py:5233` — `ClaudeCliClient(timeout=…, effort…, su_testo…)`. `su_testo` passa solo se è un turno a voce, c'è la funzione ed è il ramo `claude-cli`. Rischio: che i cervelli gratuiti ricevano il flusso, cosa che andrebbe contro la regola dei modelli. Il ramo `OpenAI(...)` è rimasto com'era. Esito: ok.
- `gas.py:5280` — il controllo del tetto di 10 chiamate per turno della #370 sta dentro il ciclo, prima di ogni chiamata. Il conteggio sale a `gas.py:5288` e anche sul retry di Gemini 400 a `gas.py:5315`. Rischio: che il flusso aggiri il tetto. Non lo aggira: il flusso e l'anticipo vivono dentro una sola chiamata, che viene contata come le altre. L'anticipo parla solo quando la risposta inizia con `"chiamate": []`, quindi non aggiunge giri. Esito: ok.
- `gas.py:5249` — `_pin_rung`: il pin completo della memoria va solo a `claude-cli`, gli altri cervelli ricevono la versione senza dati dei lead. Rischio: che il testo anticipato porti dati del pin ai cervelli non forti. Non succede: il flusso esiste solo per il cervello forte, che il pin completo lo riceve già. Esito: ok.
- `modules/voice/server.py:949` — `kw["su_testo_voce"] = self._anticipo.testo`, invariato rispetto ad a9419ea (#773/#778). Esito: ok.
- `brains/claude_cli.py:634` — senza `su_testo` il forte usa l'uscita json di prima. T104e conferma che con un turno a testo resta `--output-format json`. Esito: ok.
- `.claude/agents/memoria_revisore.md` (unione delle due versioni) — nessuna riga tolta rispetto a HEAD né rispetto a MERGE_HEAD. Le righe #773, #778, #764-M1coord e #765-M1coord ci sono tutte e senza doppioni. Nessun file in conflitto, nessun marcatore di conflitto, `git diff --cached --check` pulito. Esito: ok.

**Test rieseguiti da me**
- claude_cli + voice_server: 290 passed.
- Kernel: 1136 PASS, 1 FAIL. Il FAIL è T31g, che c'era già (manca fastembed). T104d e T104e PASS.

**Rischi esclusi (non verificati)**
- Il tetto conta le chiamate a `create`, non i processi `claude -p`. Un eventuale nuovo tentativo interno di `ClaudeCliClient` non passa dal tetto. Questo c'era già prima del merge e non l'ho riesaminato qui.
- Non ho provato dal vero sul Mac (ElevenLabs con la CLI reale): non si può riprodurre in questo ambiente.
- Non ho riletto le parti della #370 che non toccano questa fetta (`modules/telegram/bot.py`, test della notte). Le ha già approvate la #764/#765-M1coord.

Nessuna riserva nuova. R-773-2-M2 resta accettata come prima.

**Memoria**
- Ho aggiunto la riga `#779-M2 — 2026-11-11 — APPROVATO — …` in coda a /home/user/Gas-stream/.claude/agents/memoria_revisore.md e l'ho messa in staging (`M ` nell'index).
- Lo script `commit_memoria_revisore.sh` non ha committato il file: git non permette un commit parziale durante un merge. Lo script ha scritto un WARN in gas_debug.log e ha lasciato intatto l'index. La riga entrerà nel commit del merge.
- Nessuna lezione nuova.

### Review #778-M2 (R-773-1/R-773-3, tempi del forte) — verdetto integrale

## VERDETTO: APPROVATO

Review #778-M2: il delta in staging su 6e711ce chiude le riserve R-773-1 e R-773-3 e aggiunge i tempi del forte nel log, senza riserve nuove.

**Elementi del diff esaminati**
- `brains/claude_cli.py:427` — `uccidi_tutti`: `os.killpg(proc.pid, 9)`, e se fallisce `proc.kill()`; il processo parte con `start_new_session=True`. Si usa al timeout (`brains/claude_cli.py:435`) e nel finally (`brains/claude_cli.py:468`). Rischi esaminati:
  - nipote che tiene aperto lo stdout: ho rifatto la sonda `bash -c "sleep 8 & sleep 8"` con timeout 1 s. TimeoutExpired arriva dopo 1,0 s (prima erano 8 s) e `pgrep` non trova nessun `sleep` rimasto;
  - `su_riga` che solleva: il figlio muore subito;
  - 5 MB di stdin a un figlio che non li legge: nessun blocco.
  - Il finally chiama killpg solo se `poll()` è None, quindi mai su un pid già raccolto. Con la sessione nuova il Ctrl-C del terminale non arriva più al figlio, ma lo uccide comunque il finally.
  - Esito: ok, R-773-1-M2 chiusa.
- `brains/claude_cli.py:468` (finally) — chiusura esplicita di stdout e stderr, dopo i join dei fili; un `OSError` viene ignorato. Esito: ok, R-773-3-M2 chiusa.
- `brains/claude_cli.py:498` — `_log_tempi_cli`. Rischi esaminati:
  - privacy: scrive solo numeri, mai testo. I tempi della CLI passano un filtro di tipo (bool escluso) e di intervallo 0–3.600.000 ms; i token vengono da `_token`, già limitato;
  - §9: tutto è dentro `try/except Exception`;
  - visibilità: il logger `gas.claude_cli.tempi` è a livello INFO. Il file handler di gas.py non ha livello, quindi la riga arriva in gas_debug.log; la console resta a WARNING (`gas.py:50`).
  - Esito: ok.
- `brains/claude_cli.py:653` — in `_esegui_cmd`, `su_riga` e `su_testo` sono avvolti per prendere i tempi della prima riga e del primo testo. `lettore.riga` intercetta ancora gli errori di `su_testo`. Il ramo json registra i tempi a `brains/claude_cli.py:636`. Esito: ok.

**Riproduzioni**
- claude_cli: 75 passed.

**Note cosmetiche (non bloccanti)**
- C'è `9` dove servirebbe `signal.SIGKILL`.
- Se manca la riga `result` (errore), la riga dei tempi riporta solo i tempi misurati da Gas.

**Rischi esclusi (non verificati)**
- Il mutante `start_new_session=False` e la prova dal vivo con i tempi dichiarati dalla CLI: li prendo dal tuo messaggio, qui non ho la CLI autenticata.
- Lo scarto di `time_to_request_from_spawn_ms`: non l'ho verificato sulla CLI vera.

**Riserve**
- R-773-2-M2 (anticipo buttato ma già pagato a ElevenLabs) resta aperta come riserva accettata: va tracciata in reports/stato_progetto.md.

**Memoria**
Ho aggiunto la riga contatore #778-M2 in /home/user/Gas-stream/.claude/agents/memoria_revisore.md, nessuna lezione nuova. Il file è in staging e non l'ho committato.

### Review #773-M2 (streaming della prima frase) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #773-M2 sul diff staged in /home/user/Gas-stream (branch perf/voce-streaming-m2, base 51b7d20). Prima della review ho letto CLAUDE.md (§5, §8, §9), reports/stato_progetto.md (le parti sulla voce rapida) e la memoria del revisore.

**Elementi del diff esaminati**
- `brains/claude_cli.py:414` — `_esegui_a_flusso`: Popen, un filo scrive lo stdin, un filo legge lo stderr, lo stdout si legge nel filo principale, un Timer uccide il processo. Rischi esaminati: deadlock, fili orfani, processo vivo se `su_riga` solleva. Sonde reali, tutte passate:
  - 5 MB di stdin a un figlio che non li legge: ritorna in 0,02 s, nessun blocco;
  - `su_riga` che solleva: figlio ucciso subito, eccezione propagata, nessun filo rimasto;
  - timeout di 1 s: TimeoutExpired dopo 1,0 s.
  - Esito: ok, con la riserva R-773-1-M2 qui sotto.
- `brains/claude_cli.py:450` — `for linea in proc.stdout`. Rischio esaminato: un timeout che non tiene. Esito: **riserva R-773-1-M2 (BASSA)**. Se un nipote del processo tiene aperto lo stdout dopo il kill, la lettura aspetta che il nipote muoia. Sonda `bash -c "sleep 8 & sleep 8"` con timeout 1 s: l'eccezione arriva dopo 8 s. `subprocess.run` (il vecchio `_esegui`) uccide e non aspetta la fine dell'uscita, quindi questo blocco non lo aveva. Con `--tools ""` è improbabile che la CLI lasci figli vivi. Rimedio: `start_new_session=True` + `os.killpg` in `uccidi`.
- `brains/claude_cli.py:304` e `brains/claude_cli.py:387` — `_INIZIO_TESTO` / `_aggiorna`: l'anticipo parte solo con `{"chiamate": [], "testo": "`. Le altre forme lo spengono: chiamate non vuote, «testo» per primo, più di 80 caratteri senza corrispondenza, escape non valido. Una seconda risposta strutturata dopo un anticipo lo spegne (`brains/claude_cli.py:377`). Ogni errore, anche di `su_testo`, è preso in `riga()` e scritto in gas_debug.log (§9). Esito: ok.
- `brains/claude_cli.py:85` — ordine dello schema cambiato, «chiamate» prima di «testo». Rischio esaminato: effetto sul non-voce. `_risposta` legge un dict, quindi l'ordine non conta per il parsing. SCHEMA_RISPOSTA si usa solo in `comando()`. T104e conferma che fuori dalla voce l'uscita resta `json`. Esito: ok. L'effetto del cambio d'ordine sulla qualità delle risposte non è misurato (vedi rischi esclusi).
- `modules/voice/server.py:434` — `AnticipoVoce.prendi`. Rischio esaminato: un anticipo sbagliato che finisce a voce. L'audio si restituisce solo se `frase` è identica alla frase anticipata, con la stessa voce (`_voce_tts`). In ogni altro caso torna None e parte la sintesi normale. Gli errori della sintesi risalgono come quelli di `sintesi` e finiscono negli `except` di prima. Esito: ok, un anticipo sbagliato non può arrivare a voce.
- `modules/voice/server.py:945` — l'anticipo si crea solo con la chiave, `not self._seguito()` e formato pezzi o pezzi_voce. `_parlato` è già impostato prima, a `modules/voice/server.py:821`. Rischio esaminato: privacy dei seguiti. Esito: ok, nessun parlato della stanza arriva a ElevenLabs prima del filtro.
- `modules/voice/server.py:416` — `testo()` normalizza il testo grezzo. Il finale passa invece da `parte_parlata` / `frasi_voce`. Rischio esaminato: costo e quota quando l'anticipo si butta. Esito: **riserva R-773-2-M2 (BASSA)**. Una prima frase con markdown, più lunga di `_PARLATO_MAX_CHAR`, un turno rifatto dal kernel o una risposta del cervello di riserva fanno buttare l'anticipo. La sintesi però è già stata pagata a ElevenLabs: una frase per turno, testo di Gas e non della stanza. Il filo non si annulla. Il costo della CLI non cambia: resta una sola chiamata.
- `gas.py:5139` — `su_testo` si passa solo se `name == "claude-cli"` e `voce`. Rischi esaminati: regola dei modelli e tocco minimo su run_turn. I gratuiti non ricevono nulla. Cap delle 10 iterazioni, `_get_window` e payload non toccati, nessuno slicing della cronologia. Esito: ok, conflitto con la #370 di M1 limitato alla firma e al costruttore del client.
- `tests/test_unit_kernel.py:12023` — T104d, round-trip §7 con uno strumento: il giro con la chiamata non dà anticipo, la risposta finale sì. Il runner è finto, ma lo strumento gira davvero (`tool_res` 42). Non è simulazione dell'output degli strumenti. Esito: ok.

**Riproduzioni**
- claude_cli + voice_server (suite intera): 287 passed.
- Kernel: 1120 PASS, 1 FAIL (T31g, fastembed assente, già presente su main); T104d e T104e PASS.

**Riserve**
- R-773-1-M2 BASSA — un nipote che tiene aperto lo stdout allunga il timeout (vedi sopra).
- R-773-2-M2 BASSA — anticipo buttato ma già pagato quando il testo grezzo e la parte parlata non coincidono.
- R-773-3-M2 COSMETICA — Popen senza `with`: le pipe si chiudono solo quando il GC raccoglie l'oggetto.

**Rischi esclusi (non verificati)**
- Il comportamento reale della CLI `claude -p` in stream-json, cioè l'ordine dei campi nell'input_json_delta di StructuredOutput e la riga `result` con gli stessi campi dell'uscita json: qui non c'è la CLI autenticata. Mi fido delle misure dal vivo del chiamante (2,1 s / 3,4 s).
- Il comportamento sul Mac con ElevenLabs vero.
- L'effetto del nuovo ordine dello schema sulla qualità delle risposte del modello non-voce.

**Memoria**
In /home/user/Gas-stream/.claude/agents/memoria_revisore.md ho aggiunto la riga contatore #773-M2 e una lezione: sostituire `subprocess.run(timeout)` con Popen e lettura a righe cambia cosa vuol dire il timeout; va sondato con un nipote in background. Ho usato il numero #773 indicato da te: in questo file l'ultima riga era #763-M2. Il file è in staging. Non ho lanciato `scripts/commit_memoria_revisore.sh`, perché hai chiesto solo lo staging; il file viaggerà nel tuo commit.

## §5 DELTA TEST DEL MOTORE

- Dopo e9b05e5: `python -m pytest -q tests/test_unit_claude_cli.py` 77 passed (anche con `LC_ALL=C`).
- `python tests/test_unit_kernel.py` dopo il merge: 1136 PASS, 1 FAIL (T31g, fastembed assente in questo ambiente: lo stesso FAIL c'è su main). Nuovi T104d (round-trip §7 con strumento + flusso: anticipo solo della risposta finale) e T104e (a testo niente flusso), PASS.
- `python -m pytest -q tests/test_unit_claude_cli.py`: 75 passed (16 test nuovi: parser a pezzi, escape e surrogati, processo vero con timeout e nipoti, tempi nel log).
- `python -m pytest -q tests/test_unit_voice_server.py tests/test_unit_claude_cli.py`: 287 passed prima di #778; 290 passed dopo il merge (rieseguiti dal revisore #779).
- Prova dal vivo nel cloud con la CLI vera: risposta corretta, riga dei tempi «tutto=4.38s prima_riga=0.62s primo_testo=3.93s richiesta=0.18s ttft=3.46s api=3.31s cli=3.49s fuori_cli=0.90s token_in=1697 token_out=94».

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- Head 567b1bb: suite di check completata senza fallimenti (notifica GitHub); `verifica-bot` success (APPROVATO CON RISERVE, solo BASSE/COSMETICHE).
- Nuovi commit (e9b05e5 e fine-task): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-773-1-M2 BASSA, R-773-3-M2 COSMETICA: CHIUSE (review #778-M2).
- R-773-2-M2 BASSA: un anticipo buttato (prima frase diversa dalla risposta finale: markdown, frase troppo lunga, cervello di riserva) è già stato pagato a ElevenLabs (una frase per turno, testo di Gas).
  V-1 verifica esterna #374 (BASSA): è anche un'uscita di testo verso ElevenLabs prima del finale. Limite dichiarato: il kernel NON modifica il testo finale del forte (`gas.py`, `yield {"type": "final", "content": msg.content}`), quindi la frase anticipata è testo che il forte ha scritto per la risposta a voce e che nel caso normale va comunque a ElevenLabs; esce in più solo quando poi non viene detta (taglio della parte parlata, risposta poi scartata e rifatta da un altro cervello).
- V-2/V-3/V-4 verifica esterna #374 (COSMETICHE): guadagno 1,2–1,3 s (misure diverse, stessa prova); riga di stato spostata fuori dal paragrafo del gate; `9` invece di `signal.SIGKILL` e finestra di microsecondi del Timer dopo la fine regolare.
- Cosmetiche #778: `9` invece di `signal.SIGKILL` (CHIUSA in e9b05e5); senza riga `result` i tempi riportano solo quelli misurati da Gas.
- Bot #374 su 567b1bb: V-1 BASSA = R-773-2-M2 (sopra); V-2 e V-3 COSMETICHE CHIUSE (e9b05e5).
- R-781-1-M2 BASSA: CHIUSA (review #782-M2). R-781-2-M2 BASSA: se la CLI resta appesa dopo la riga `result`, la risposta arriva solo allo scadere del timeout; uscire subito alla riga `result` toglierebbe anche ~0,6 s di chiusura della CLI a ogni turno, ma interrompe Claude Code mentre chiude: da valutare a parte.
- Non verificato: guadagno reale sul Mac; effetto dell'ordine «chiamate» prima di «testo» dello schema sulla qualità delle risposte non a voce.
