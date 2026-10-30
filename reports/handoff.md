# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-30 — Voce V3: conversazione filata (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #311 (https://github.com/Gasss23/Gas/pull/311). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5087256865","url":"https://github.com/Gasss23/Gas/pull/311"}`); `gh` nel cloud non è autenticato. La mergia M1 se il bot dà APPROVATO pulito; con riserve M1 chiede il sì all'operatore.
2. Prova col microfono vero sul Mac (soglia del volume, eco, voce italiana della frase d'attesa): non riproducibile in headless.
3. Interruzione mentre Gas parla (punto 4 della fetta): parcheggiata, serve l'ok per toglierla dal parcheggio.

---

## §1 SCOPE & ESITO FETTE

- **V3.1 — modalità conversazione nel browser**: `FATTA` — finestra `GAS_VOICE_FINESTRA` (12 s), fine frase dal silenzio, bip di chiusura.
- **V3.2 — «due secondi o ci sto ragionando»**: `FATTA` — frase d'attesa con la voce di sistema del browser.
- **V3.3 — risposte a voce brevi**: `FATTA` — `run_turn(istruzione_turno=...)` in gas.py (ok di M1), `ISTRUZIONE_VOCE` ai soli turni parlati, a voce solo la parte corta e il testo intero a schermo.
- **V-1 bot #308 (su 2507621, 504 «non ripetere»)**: `FATTA`.
- **V3.4 — interruzione mentre Gas parla**: `SALTATA — parcheggiata, serve l'ok`.
- **Secondo giro — bot #311 su 17beb97 NON approvata (V-1 MEDIA, nessun tetto ai turni automatici)**: `FATTA` — `GAS_VOICE_MAX_TURNI` (5, contando il turno del clic), voce minima 250 ms; R-576-2-M2 `FATTA` (`player.onerror`); V-2 bot (test del browser saltati in CI) `DEFERITA — riserva aperta, ci.yml fuori fetta`. Verifica esterna #311 su 17beb97 APPROVATO CON RISERVE ([copia](https://github.com/Gasss23/Gas/pull/311#issuecomment-6527391973)). Review #577-M2 e #578-M2 APPROVATO CON RISERVE.
- **Merge di origin/main (PR #310 della chat Mani) per il conflitto segnalato da M1**: `FATTA` — conflitti solo nei report e nella memoria del revisore; review #579-M2 APPROVATO; voce 129 passed, web leggi 501 passed. Merge di #311 autorizzato dall'operatore («sì a #311», via M1), lo fa M1.
- **Review #574-M2 BOCCIATO → R-574-1..5-M2**: `FATTA`. **#575-M2 → R-575-1/2-M2**: `FATTA`. **#576-M2 → R-576-2-M2** `FATTA` (secondo giro); **R-576-1/3-M2** `DEFERITA — una fetta piccola dopo la prova sul Mac`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 +++++++++
 clients/voice/browser_client.html  | 430 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------
 clients/voice/browser_server.py    |  40 +++++++++++++++++++++++++++++++++-
 gas.py                             |   8 +++++--
 modules/voice/server.py            |  86 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           |  18 +++++++--------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   4 ++--
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  34 +++++++++++++++++------------
 tests/test_unit_kernel.py          |  54 +++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_server.py    | 264 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_stt.py       |  24 +++++++++++++++++---
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. BASE = 15c4da8 (main dopo la #310).

## §3 GIT LOG --ONELINE (sessione)

```
b72809b Merge origin/main (PR #310) in feat/voce-v3-m2: conflitti solo nei report e nella memoria del revisore
a1a6a25 docs(voce-v3): report dopo il bot #311 (V-1 chiusa), review #577/#578-M2
3d7a095 fix(voce): tetto ai turni di fila, voce minima 250 ms, audio rotto gestito (bot #311)
797fb5d chore(revisore): memoria review #578 — APPROVATO CON RISERVE
3e57cfc chore(revisore): memoria review #577 — APPROVATO CON RISERVE
17beb97 docs(voce-v3): report di fine task (PR #311, review #574-#576-M2)
d7730de feat(voce): conversazione filata — finestra d'ascolto, frase d'attesa, risposte parlate corte (V3, chat M2)
82e9703 chore(revisore): memoria review #576 — APPROVATO CON RISERVE
4f3cfe2 chore(revisore): memoria review #575 — APPROVATO CON RISERVE
db70c18 chore(revisore): memoria review #574 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit d7730de è stato rivisto in tre passaggi (#574-#576-M2) e il commit 3d7a095 in due (#577-#578-M2) sullo stesso diff staged (ogni passaggio dopo le correzioni del precedente; le citazioni dei primi due si riferiscono al diff di quel momento e alcune righe a HEAD sono spostate). Verdetti integrali:

Review #574-M2 (primo passaggio):

## VERDETTO: BOCCIATO

Review #574-M2. Ho revisionato il diff staged di feat/voce-v3-m2 (4 file). Ho fatto le tre letture obbligatorie (CLAUDE.md, stato_progetto per la voce, memoria con le lezioni M2 #568–#573).

**Motivo bloccante: R-574-1-M2 (MEDIA, riprodotto)**

Se l'operatore riascolta la risposta dai controlli del player mentre la finestra del microfono è aperta, la pagina parte per un turno che lui non ha chiesto, e da quel momento continua a dare errori senza fine.

- Come l'ho riprodotto: con lo stesso schema del test e la pagina vera in Chromium headless, ho chiamato `player.play()` mentre lo stato era «ti ascolto».
- Cosa succede:
  - `ascolta()` riparte una seconda volta. Il timer del primo ascolto resta attivo e non si ferma più: 100 `TypeError: Cannot read properties of null (reading 'fftSize')` in 8 s, e continua.
  - `chunks` e `recorder` vengono sovrascritti.
  - Parte un **secondo POST /voice** dopo «conversazione chiusa (silenzio)». È un turno del kernel su audio muto, e Whisper sul silenzio inventa frasi: Gas eseguirebbe un turno non chiesto.
- Il caso è raggiungibile nell'uso normale: `<audio id="player" controls>` è visibile.
- Correzione stretta proposta:
  1. `player.onended` monouso, cioè rimetterlo a `null` dentro il gestore, e associato al turno che l'ha impostato.
  2. Una guardia di rientro all'inizio di `ascolta()`: niente nuovo ascolto se `ascolto` è attivo, se `recorder.state === "recording"` o se `occupato`.
  3. Un test nel browser col riascolto a metà finestra, che controlli 1 solo POST e 0 `pageerror`.

**Elementi del diff esaminati**

- `clients/voice/browser_client.html:517` — `player.onended = () => { occupato = false; dopoRisposta("pronto"); }` — si attiva a ogni `ended`, quindi anche dopo un riascolto, e rimette `occupato` a false anche con un invio in corso. **BLOCCO** (R-574-1-M2).
- `clients/voice/browser_client.html:405` — `ascolta()` — manca una guardia contro il rientro: alla riga 433 il nuovo `setInterval` prende il posto di `ascolto` senza fermare il timer vecchio, che resta senza riferimento. **BLOCCO** (stessa causa).
- `clients/voice/browser_client.html:457` (`chiudiConversazione`) — se c'è una registrazione in corso sostituisce `onstop` e quindi non invia nulla; i timer vengono fermati e il microfono chiuso. Nel caso «fine frase già decisa» (`recorder.stop()` alla riga 447 e clic prima che arrivi `onstop`) la frase parte lo stesso, perché lo stato è già `inactive`. Effetto accettabile, la risposta poi non riapre il microfono. **ok**
- `clients/voice/browser_client.html:497` — `await resp.json()` e `atob(j.audio)` senza try nel ramo 200: se il corpo è troncato o il base64 non è valido, `occupato` resta true per sempre, il timer della frase d'attesa non viene fermato e la pagina va ricaricata. **riserva R-574-2-M2 BASSA**
- `clients/voice/browser_client.html:519` — se `player.play()` viene rifiutato, `occupato` torna false ma il microfono (`stream`) resta aperto: in conversazione e anche in push-to-talk. **riserva R-574-3-M2 BASSA.** Stesso tipo di problema: un doppio clic o uno spazio durante la richiesta di permesso del microfono (riga 377, `apriMicrofono` senza lucchetto) può aprire due flussi e il primo non viene mai chiuso. Non l'ho riprodotto: con la UI finta il permesso è istantaneo.
- `modules/voice/server.py:233` — «uso» con audio+testo restituisce `_USO_FORTE_PARLATO` e poi `return`. L'ho provato con una sonda (`transcribe_audio` sostituito per restituire «forte»): 200, audio presente, `run_turn` chiamato 0 volte. **ok**
- `modules/voice/server.py:273` — `_do_audio_testo_response`. Sonde:
  - senza chiave: 200 con `errore_voce`;
  - con `ElevenLabsTTSError(401)`: 200 con `{"content":"ok","errore_voce":"Errore TTS ElevenLabs: chiave"}`;
  - intestazione `Audio+Testo ` (maiuscole e spazio finale): accettata.
  
  Le eccezioni gestite sono le stesse di `_do_tts_response` e vengono registrate nel log. **ok**
- `modules/voice/server.py:114` — `parte_parlata`: con `"Ciao.\nCome stai?"` restituisce `"Ciao. Come stai? Il resto è a schermo."`, cioè dice «il resto è a schermo» quando il testo è già stato detto tutto (le frasi vengono riunite con lo spazio e il confronto con l'originale fallisce). Inoltre «Dott.» spezza la frase. **riserva R-574-4-M2 BASSA**
- `clients/voice/browser_server.py:71` — `GET /config` restituisce solo `{"finestra": N}`; nessun segreto, server legato a 127.0.0.1. La validazione alla riga 211 rifiuta anche `nan` e `inf` (il confronto con `nan` è falso). **ok**
- `clients/voice/browser_server.py:130` — `X-Gas-Formato` viene inoltrato solo se presente, e il test nel browser lo verifica (`tests/test_unit_voice_server.py:955`). Il 504 alla riga 144 dice «NON ripetere la richiesta». **ok**
- `tests/test_unit_voice_server.py:888` — test di tutto il giro nella pagina vera. Gira qui (7 V3 passed in circa 14 s). Mutante VAD `sogliaMin: 0.9` riprodotto da me: 1 failed, file ripristinato con `git checkout`. Il test è solido sul giro felice ma non copre riascolto, chiusura durante l'invio e risposte rotte. **ok**, con il test chiesto sopra.
- `tests/test_unit_voice_server.py:830` — il test del 504 controlla solo che la stringa sia nel sorgente, non la risposta HTTP. **riserva R-574-5-M2 COSMETICA**

**Risultati**

- Voce server + stt: 101 passed (prima che comparissero le modifiche non staged, vedi sotto).
- V3: 7 passed.
- Sonde «uso» ed errore TTS: passate.
- Riascolto in Chromium: 2 POST e 100 pageerror (difetto confermato).
- Nel diff non ci sono slicing della history né simulazione dell'output dei tool; `gas.py`, `brains/` e `ci.yml` non sono nel diff staged.

**Cosa NON ho verificato e perché**

- Comportamento con microfono e altoparlanti reali (eco, cancellazione dell'eco, soglia VAD in una stanza vera): non si riproduce in headless.
- Voce `speechSynthesis` it-IT: dipende dal sistema operativo.
- Safari e Firefox (MediaRecorder `audio/mp4`, `getFloatTimeDomainData`): ho provato solo Chromium.
- Chiamata vera a ElevenLabs: sostituita con un finto.

**Nota per l'agente principale**

Durante la review sono comparse nel working tree modifiche NON staged a `gas.py`, `modules/voice/server.py`, `tests/test_unit_kernel.py` e `tests/test_unit_voice_stt.py`. Non sono mie: ho fatto `git checkout` solo di `clients/voice/browser_client.html`, che coincideva con l'index. Questa review copre solo il contenuto staged (le citazioni sono sulle righe di `git show :file`). Quelle modifiche richiedono una review a parte prima di andare in stage.

Memoria: aggiunta la riga `#574-M2 — 2026-10-30 — BOCCIATO`, più una lezione sui callback degli elementi con controlli visibili che si possono riattivare. È committata col commit db70c18 tramite `scripts/commit_memoria_revisore.sh`.

File:
- /home/user/Gas/clients/voice/browser_client.html
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/clients/voice/browser_server.py
- /home/user/Gas/tests/test_unit_voice_server.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- Sonda di riproduzione: /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/test_sonda_replay.py
- Sonde «uso» ed errore TTS: /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/test_sonda_v3.py

NB (agente): le modifiche non staged citate sopra erano il punto 3 della fetta (gas.py, ok di M1), messe in stage dopo e riviste in #575-M2.

Review #575-M2 (secondo passaggio, con gas.py):

## VERDETTO: APPROVATO CON RISERVE

Review #575-M2 sul diff staged di feat/voce-v3-m2: 7 file, +686/−137. Prima ho letto CLAUDE.md (§5, §6, §8), stato_progetto e la mia memoria.

**Cosa ho controllato nel diff**
- `clients/voice/browser_client.html:532` — `player.onended` ora vale una volta sola ed è legato a `numTurno`. Rischio: un riascolto riapre l'ascolto (R-574-1-M2). Esito: ok.
  - Ho rifatto la prova. Ho tolto le due guardie e la riga «una volta sola» su una copia: il test nel browser in modalità «riascolto» fallisce (1 failed, 7 passed). Ho rimesso il file com'era: 8 passed, il file è identico alla versione staged.
- `clients/voice/browser_client.html:413` — la guardia di rientro in `ascolta()`, ripetuta alla riga `clients/voice/browser_client.html:415` dopo che il microfono si è aperto. Rischio: due ascolti insieme, oppure un ascolto durante un invio o una riproduzione. Esito: ok.
- `clients/voice/browser_client.html:443` — il timer si ferma da solo se l'analyser non c'è più. Rischio: i 100 TypeError su `fftSize` visti in #574. Esito: ok.
- `clients/voice/browser_client.html:506` — lettura del JSON e decodifica `atob` dentro un try, con `fineTurno` e un errore dichiarato (R-574-2-M2). Esito: ok.
- `clients/voice/browser_client.html:381` — il lucchetto `apertura` evita due richieste del microfono durante la richiesta del permesso (R-574-3-M2). Esito: ok, ma vedi la riserva R-575-2-M2.
- `modules/voice/server.py:112` — `parte_parlata` (R-574-4-M2). Rischio: falsi «Il resto è a schermo.» e tagli dopo le abbreviazioni. Esito: ok.
  - Provato a mano: «Uno.\nDue.» resta intero, senza aggiunta. «Il Dott. Rossi…» non viene tagliato dopo «Dott.». «Vedi n. 3. Fatto.» e «3.5 euro» restano interi.
- `modules/voice/server.py:265` — `ISTRUZIONE_VOCE` viene passata solo quando la richiesta è audio (`is_audio`). Rischio: che cambi anche le risposte scritte. Esito: ok, è coperto dal test `test_v3_turno_parlato_ha_istruzione_voce_e_lo_scritto_no`.
- `gas.py:4726` — `turno_pin` viene calcolato una volta per turno. Se l'istruzione è vuota o fatta di soli spazi, il pin resta vuoto. Esito: ok.
- `gas.py:4791` — `turno_pin` va in coda al messaggio system, insieme agli altri pin. È l'unico punto in cui si costruisce quel messaggio. Rischio: violare §5/§6 (taglio della cronologia, `_get_window`) o §8 (tetto di 10 giri). Esito: ok.
  - `_get_window()` è invariato (`gas.py:4787`) e il tetto `for _ in range(10)` è intatto (`gas.py:4783`).
  - Nessun taglio diretto della cronologia, e l'istruzione non entra nella cronologia.
  - Gli altri punti che chiamano `run_turn` restano compatibili: il nuovo parametro ha valore predefinito `None`.
- `tests/test_unit_kernel.py:11394` — test T101: un turno con una chiamata a uno strumento. Controlla che l'istruzione stia nel messaggio system di entrambe le chiamate del turno, che non finisca nella cronologia e che sparisca al turno dopo. Esito: ok, T101a/b PASS.
- `tests/test_unit_voice_server.py:611` — il test del 504 ora controlla «NON ripetere la richiesta» nella risposta HTTP vera (R-574-5-M2). Esito: ok.

**Test rieseguiti da me**
- Suite del kernel: 1063 PASS, 0 FAIL.
- Test voce (server + stt): 102 passed, compresi i test V3 nel browser in modalità normale e riascolto (girano davvero, non vengono saltati).

**Riserve (da tracciare in stato_progetto.md)**
- **R-575-1-M2 (BASSA)**: se l'operatore mette in pausa la risposta dai controlli del player, l'evento di fine riproduzione non arriva mai. `occupato` resta vero e il tasto non fa niente (`clients/voice/browser_client.html:569`) finché la riproduzione non arriva in fondo; un clic durante una conversazione la chiude soltanto. Correzione: sulla pausa (`player.onpause`) liberare `occupato` e chiudere la conversazione.
- **R-575-2-M2 (BASSA)**: se si chiude la conversazione mentre il browser chiede il permesso del microfono, dopo l'apertura `ascolta()` controlla solo gli stati di rientro e non `conversazione`. Così parte una registrazione manuale: microfono acceso contro l'intenzione dell'operatore, anche se non invia niente senza un altro clic. Correzione: dopo l'apertura, se la conversazione è stata chiusa nel frattempo, uscire e chiudere il microfono.

**Cosa NON ho verificato**
- Il comportamento con un microfono vero e un audio di ElevenLabs vero, sul Mac dell'operatore: non riproducibile qui, la prova nel browser usa Chromium headless con un microfono finto da file WAV.
- Le due riserve sono emerse leggendo il codice, non le ho riprodotte nel browser.
- Non ho controllato se il ramo «forte» (`claude -p`) mette davvero nel prompt il messaggio system così com'è: ho verificato solo che il messaggio venga costruito in un punto solo.

Memoria aggiornata con la riga #575-M2 e una lezione nuova, già committata (4f3cfe2) in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Il diff staged è rimasto intatto (7 file).

NB (agente): il ramo «forte» passa il messaggio system a `claude -p`: `brains/claude_cli.py` legge i messaggi `role: system` (righe 147-148 e 301).

Review #576-M2 (diff finale committato in d7730de):

## VERDETTO: APPROVATO CON RISERVE

Review #576-M2: ricontrollo del diff staged su feat/voce-v3-m2, cioè la #575-M2 più le correzioni delle sue due riserve. Ho letto prima CLAUDE.md (sez. 5), le voci #575 di reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `clients/voice/browser_client.html:544` — il gestore `player.onpause` vale una volta sola, è legato a `numTurno` e non fa nulla se `player.ended` è vero. Libera `occupato`, chiude la conversazione e mostra «risposta in pausa · conversazione chiusa».
  - Rischi esaminati: (1) una fine normale letta come pausa: esclusa dalla guardia su `ended`; (2) un rientro dopo un riascolto: escluso, perché entrambi i gestori vengono azzerati; (3) una pausa finta quando cambia `src` per il turno nuovo mentre suona ancora la risposta vecchia: provato con una sonda Playwright/Chromium, cambiare `src` mentre suona non emette `pause` dopo il nuovo gestore, e `play()` va a buon fine.
  - Esito: ok. R-575-1-M2 chiusa.
- `clients/voice/browser_client.html:555` — nel catch di `play()`, `if (turno !== numTurno || !occupato) return;` evita che l'AbortError di una pausa subito dopo `play()` sovrascriva lo stato con «premi play».
  - Rischio: che il ritorno anticipato salti la chiusura nel caso dell'autoplay negato. Non succede: lì non arriva nessun evento `pause`, quindi `occupato` è ancora true e il ramo R-574-3 resta valido.
  - Mutante senza questa guardia: il test «pausa» fallisce. File ripristinato dall'index (cmp identico).
  - Esito: ok.
- `clients/voice/browser_client.html:414` e `clients/voice/browser_client.html:419` — `ascolta()` ricorda se è partita dentro una conversazione; se la conversazione è stata chiusa mentre si attendeva il permesso, spegne il microfono e non registra.
  - Rischio: che chiudere e riaprire durante il permesso generi due ascolti. Non succede: la seconda chiamata riceve la stessa promessa `apertura` e trova il recorder già in registrazione.
  - Esito: riserva R-576-1-M2 (sotto). Il codice è corretto ma nessun test lo prova: senza la guardia i test del browser passano tutti e 3.
- `tests/test_unit_voice_server.py:886` — nuova modalità «pausa» con audio di risposta da 2 s e `pause()` durante «Gas parla». Le asserzioni a `tests/test_unit_voice_server.py:984` controllano lo stato «risposta in pausa», nessun «ti ascolto» dopo, 1 solo POST e nessun errore di pagina. Esito: ok.
- `tests/test_unit_voice_server.py:902` — se lo script Node fallisce, stampa a stderr gli stati della pagina (try/catch interno, poi `exit(1)`). Serve solo alla diagnosi e non cambia l'esito. Esito: ok.
- Contesto: in `gas.py:4726` il diff staged di gas.py è uguale a quello approvato nella #575: `istruzione_turno` solo in coda al messaggio system (`turno_pin`), `_get_window` e il tetto di 10 giri non toccati. Esito: ok.

**Prove riprodotte**
- Suite voce (voice_server + voice_stt): 103 passed.
- Test `-k browser`: 9 passed (comprende normale, riascolto e pausa).
- Due mutanti, file ripristinato dopo ciascuno.

**Riserve**
- **R-576-1-M2 (BASSA):** la correzione di R-575-2-M2 non ha un test (il mutante sopravvive). Basta un test che sostituisca `getUserMedia` con una promessa lenta e chiuda la conversazione nel frattempo.
- **R-576-2-M2 (BASSA, c'era già):** un errore di decodifica a metà riproduzione (evento `error`, nessun `pause` né `ended`, dopo che `play()` è andato a buon fine) lascia `occupato` bloccato. Manca un `player.onerror` che chiuda il turno come fa `onpause`.
- **R-576-3-M2 (COSMETICA):** senza conversazione attiva, la pausa mostra comunque «conversazione chiusa».

**Rischio escluso:** non ho verificato il comportamento su Safari e Firefox, né col microfono vero sul Mac. La sonda sul cambio di `src` e i test girano solo su Chromium headless con microfono finto. Il comportamento degli eventi `pause` su WebKit non è riproducibile qui.

**Memoria:** ho aggiunto la riga contatore #576-M2 e una lezione (togliere con un mutante le guardie messe dopo un await) in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata come 82e9703.

Commit 3d7a095 — review #577-M2 (secondo giro, dopo il bot su 17beb97; poi corrette R-577-1/2-M2, alcune righe a HEAD sono spostate di 2), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #577-M2 del diff staged su feat/voce-v3-m2 (PR #311): fix del V-1 MEDIA del bot su 17beb97 e della riserva R-576-2-M2.

Letture fatte: CLAUDE.md (sezioni 5, 8, 10), reports/stato_progetto.md (in modo mirato), .claude/agents/memoria_revisore.md (lezioni #574–#576). Il diff tocca solo clients/voice/ e tests/. Non tocca gas.py, `_get_window`, il tetto di 10 iterazioni né il tetto di 8k sull'output. Nessuno slicing diretto della history e nessuna simulazione dei tool.

**Elementi del diff esaminati**

- `clients/voice/browser_client.html:591` — il tetto sui turni di fila sta in `dopoRisposta`. Rischio esaminato: che lo si possa aggirare passando da un'altra strada. Ho cercato tutte le chiamate ad `ascolta()`: l'ascolto si riapre da solo SOLO alla riga 596, che si raggiunge solo passando dal controllo della 591. Gli errori di rete, HTTP e di lettura passano da `fineTurno` (`clients/voice/browser_client.html:579`), che chiude la conversazione e non riapre niente. Una frase scartata per silenzio non viene inviata e chiude la conversazione. Esito: ok, nessun aggiramento.
- `clients/voice/browser_client.html:438` — `turniDiFila += 1` in `recorder.onstop`, dopo `if (scarta) return`. Rischio esaminato: cosa viene contato. Conta solo le frasi davvero inviate, che la risposta vada bene o no. Chiudere la conversazione sostituisce `onstop` (`clients/voice/browser_client.html:479`), quindi nessun incremento spurio. Mutante senza l'incremento: il test «tetto» fallisce; codice ripristinato, la copia di lavoro torna identica allo staged. Esito: ok.
- `clients/voice/browser_client.html:606` — il contatore torna a 0 solo col clic di avvio. Rischio esaminato: la semantica. Il turno avviato dal clic conta come 1, quindi con maxTurni=5 ci sono 1 turno col clic più 4 riaperture automatiche: è la scelta più prudente. Un clic che ferma la registrazione (riga 604) esce prima dell'azzeramento: anche questo è prudente. Un clic durante la conversazione la chiude (riga 603); per ripartire serve un nuovo clic, che azzera. Esito: ok.
- `clients/voice/browser_client.html:568` — nel catch di `play()`, se `player.error` è valorizzato si chiama `player.onerror()`. Rischio esaminato: un TypeError se `onerror` è già stato annullato. Tutti i punti che annullano i gestori, quando il turno è quello corrente, mettono `occupato=false`, quindi la guardia della riga 567 (`turno !== numTurno || !occupato`) esce prima. `onerror` è monouso e legato a numTurno (`clients/voice/browser_client.html:547`), e viene annullato insieme a onended e onpause. Esito: ok.
- `clients/voice/browser_server.py:220` — `GAS_VOICE_MAX_TURNI` è un intero da 1 a 50, altrimenti esce con 1. La pagina accetta solo un intero positivo (`clients/voice/browser_client.html:621`); se /config non risponde resta il default 5. Il test (`tests/test_unit_voice_server.py:834`) prova abc, 0, 51 e 2.5. Esito: ok.
- `clients/voice/browser_client.html:459` — la voce continua minima passa da 150 a 400 ms. Rischio esaminato: le risposte brevissime. Esito: riserva R-577-1-M2.
- `tests/test_unit_voice_server.py:989` — modalità «errore» (audio non valido): lo stato finale è «non riproducibile» e non c'è nessun «ti ascolto» dopo «ragionando». Il test non distingue se è scattato l'evento error o il rifiuto di `play()`, ma entrambe le strade finiscono nello stesso gestore. Esito: ok.

**Esecuzione:** test browser più /config: 11 passed. Mutante sul contatore: «tetto» FAILED, poi ripristinato.

**Riserve**
- R-577-1-M2 BASSA — con `voceMinMs` a 400 ms un «sì» o un «no» secco (circa 250–350 ms) può non contare come frase. La finestra scade e la conversazione si chiude «per silenzio», proprio dopo domande come «Procedo?». È un compromesso contro il rumore: va provato sul Mac con la voce vera ed eventualmente reso configurabile.
- R-577-2-M2 COSMETICA — docstring di `clients/voice/browser_server.py:21` e commento del CFG: «turni di fila senza un clic», ma il primo turno è quello del clic. Il messaggio a schermo «dopo N turni di fila» invece è esatto.
- V-2 bot (i test browser vengono saltati in CI perché nel job mancano Node e Playwright): resta una riserva da tracciare in stato_progetto.md, come dichiarato.

**Rischio escluso:** non ho verificato il comportamento con un microfono reale, rumore ambientale vero e la politica di autoplay di Safari/Chrome sul Mac. In questo ambiente non si riproduce: c'è solo Chromium headless con un microfono finto da file. Non ho rifatto il mutante sul ramo `player.error` del catch: mi fido della prova dichiarata, secondo cui «errore» fallisce sulla pagina di HEAD.

**Memoria:** riga #577-M2 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con 3e57cfc tramite `scripts/commit_memoria_revisore.sh`. Lo staging del diff sotto review è intatto.

Commit 3d7a095 — review #578-M2 (diff finale committato), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #578-M2. Diff staged su feat/voce-v3-m2, PR #311. I file sono 3: clients/voice/browser_client.html, clients/voice/browser_server.py, tests/test_unit_voice_server.py. Nessuna modifica a gas.py, brains/ o modules/: `git diff --cached` su quei percorsi è vuoto.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), la parte di reports/stato_progetto.md che riguarda la voce, la coda di .claude/agents/memoria_revisore.md (#576-M2, #577-M2 e le lezioni sul tetto anti-loop).

**Elementi del diff esaminati**
1. `clients/voice/browser_client.html:316` — `CFG.voceMinMs: 250`, con un commento di due righe che rimanda a V-1 bot #311 e R-577-1-M2. Il rischio esaminato: con 400 ms un «sì» secco non contava. Con 250 ms passa la maggior parte delle risposte brevi, e contro il rumore di fondo resta il tetto dei turni. Esito: ok, R-577-1-M2 chiusa nel codice.
2. `clients/voice/browser_client.html:461` — la soglia usata è `CFG.voceMinMs`, non un numero scritto nel codice. Il rischio esaminato: un valore duplicato che va fuori sync. Esito: ok, la fonte è una sola.
3. `clients/voice/browser_server.py:21` — la docstring di GAS_VOICE_MAX_TURNI ora dice «contando quello avviato dal clic». Il rischio esaminato: un testo diverso dal comportamento (il contatore viene azzerato dal clic e incrementato all'invio, quindi il turno del clic conta 1). Esito: ok, R-577-2-M2 chiusa.
4. `clients/voice/browser_client.html:317` — il commento di `maxTurni` dice «il primo è quello del clic». Il rischio esaminato: coerenza con la docstring del server. Esito: ok.
5. Ho verificato che non ci sia altro di nuovo rispetto a #577:
   - `clients/voice/browser_client.html:440`: incremento all'invio.
   - `clients/voice/browser_client.html:593`: controllo del tetto in `dopoRisposta`.
   - `clients/voice/browser_client.html:608`: azzeramento al clic.
   
   Il contenuto è identico a quanto approvato in #577. Le righe sono scese di 2 rispetto alle citazioni di #577 (:438, :591, :606), coerente con il commento più lungo di `voceMinMs`. Esito: ok.

**Test eseguiti**
- Test browser e config (normale, riascolto, pausa, tetto, errore, config): 11 passati.
- Resto di tests/test_unit_voice_server.py: 61 passati.

**Riserve**
- R-578-1-M2 (BASSA): 250 ms è comunque più dei 150 ms originali. Un «sì» brevissimo dopo «Procedo?» va provato davvero sul Mac con il microfono reale. Il test headless usa una voce finta di 1,5 s e non copre questo caso.
- La riserva V-2 del bot resta aperta: i test browser vengono saltati in CI. Va tracciata in reports/stato_progetto.md.

**Rischio escluso**: non ho verificato il comportamento con un microfono reale e il rumore di una stanza vera (TV, voci). Non si può riprodurre in un container headless: il microfono finto è un file WAV pulito.

**Memoria**: riga contatore #578-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e già committata con `scripts/commit_memoria_revisore.sh` (commit 797fb5d). Nessuna lezione nuova.

Commit b72809b (merge di origin/main, PR #310 della chat Mani) — review #579-M2, verdetto integrale:

## VERDETTO: APPROVATO

Review #579-M2: merge in stage, non ancora committato, di origin/main a1a6a25 (PR #310 della chat Mani) in feat/voce-v3-m2 (PR #311). HEAD 15c4da8, MERGE_HEAD a1a6a25, merge-base 4ffcd80.

Ho letto prima CLAUDE.md §5, reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati (path:riga — cosa fa — rischio — esito)**
- `gas.py:4726` — `turno_pin` aggiunge `istruzione_turno` solo in coda al system. Rischio: che il merge abbia alterato il nostro codice del kernel o toccato `_get_window`. Esito: ok. `git diff --cached HEAD --quiet -- gas.py clients modules/voice tests/test_unit_voice_*.py tests/test_unit_kernel.py` non trova differenze: il codice voce e kernel è identico a HEAD. Nel diff contro origin/main non c'è nessuno slicing della history e nessun riferimento nuovo a `_get_window`.
- `clients/voice/browser_client.html:316-317` — `voceMinMs: 250` e `maxTurni: 5`, il tetto anti-loop della conversazione. Rischio: perdere i fix di #577/#578-M2 nella risoluzione dei conflitti. Esito: ok, invariati rispetto a HEAD. Lo stesso vale per `clients/voice/browser_client.html:461` (soglia di voce) e `clients/voice/browser_client.html:592` (commento del tetto).
- `modules/web/leggi.py:656` (contesto, codice portato da main) — controllo delle porte 80/443 in `_valida_url`. Rischio: che il merge lo modifichi rispetto a quanto già revisionato in #583/#584. Esito: ok. Contro origin/main il diff di `modules/web/leggi.py`, `tests/test_unit_web_leggi.py` e `reports/ripartenza_mani.md` è vuoto, quindi è un'unione semplice.
- `.claude/agents/memoria_revisore.md` — file in sola aggiunta. Rischio: perdere uno dei due blocchi. Esito: ok. Non manca nessuna riga né rispetto a HEAD né rispetto a origin/main: ci sono sia #573-M2…#578-M2 sia #583/#584 della chat Mani, e non ci sono marcatori.
- `reports/stato_progetto.md` e `reports/roadmap.md` (unione automatica) — Rischio: perdere righe di uno dei due lati. Esito: ok. Contro origin/main non manca nessuna riga: stato_progetto ha solo +1 riga (Voce V3) e roadmap solo le 2 righe V3 al posto dei ⏳. Le 2 righe di stato_progetto che cambiano rispetto a HEAD sono quelle aggiornate da main (data di ultimo aggiornamento e fetta 1), riprese uguali a main.

**Controlli eseguiti**
- Nessun marcatore di conflitto nei file in stage.
- `git diff --cached --check` è pulito.
- I test web leggi (`tests/test_unit_web_leggi.py`): 501 passed, 1 skipped.
- La suite voce (`tests/test_unit_voice_*.py`): 129 passed, rieseguita da me.

**Rischio escluso:** non ho rieseguito la suite completa del kernel né la CI. Il codice di gas.py e dei test del kernel è identico a HEAD, che è già stato revisionato (#575/#576-M2). Non ho verificato neanche reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md, risolti con la nostra versione: li rigenera /fine-task.

**Memoria del revisore:** ho aggiunto la riga `#579-M2 — 2026-10-30 — APPROVATO — … Nessuna lezione nuova` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. È rimasta **fuori dallo stage**: lo stato del file è `MM`. Lo script `commit_memoria_revisore.sh` non ha creato nessun commit, coerente col caso già visto di un merge in corso. Tocca a te metterla in stage prima del commit di merge, come per #579 (chat Mani).

NB (agente): fatto — `git add` della memoria, poi `segna_review_ok.sh`, poi il commit b72809b. Il revisore ha scambiato i nomi HEAD/MERGE_HEAD (HEAD era a1a6a25, MERGE_HEAD 15c4da8 = origin/main): non cambia l'esito.

## §5 DELTA TEST DEL MOTORE

Suite kernel (tests/test_unit_kernel.py), in locale: 1061 → 1063 PASS, 0 FAIL (+T101a/b, round-trip di `istruzione_turno` con tool); in CI su 17beb97 il conteggio è 1069 PASS, 0 FAIL (ambiente diverso, sandbox bwrap). Voice suite (server+stt+tts): 120 → 129 passed in locale, compresi i 5 giri della pagina vera in Chromium headless (normale, riascolto, pausa, tetto, errore); in CI quei 5 si saltano (niente Node/Playwright: V-2 bot #311, riserva aperta). Mutanti: soglia del volume a 0,9 → il giro fallisce; pagina di #574 → «riascolto» fallisce; pagina di #575 → «pausa» fallisce; pagina di 17beb97 → «tetto» ed «errore» falliscono. Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- db70c18, 4f3cfe2, 82e9703, d7730de: pushati insieme prima dell'apertura della PR #311; nessuna run della PR su questi SHA.
- 17beb97 (fine-task del primo giro): run CI 41086377142 (`unit-suite` e `handoff-check` success); check `verifica-bot` failure — bot NON approvata (V-1 MEDIA, chiusa in 3d7a095).
- 3e57cfc, 797fb5d, 3d7a095: nessuna run su questi SHA (pushati insieme ad a1a6a25).
- a1a6a25 (fine-task del secondo giro): run CI 41088904254 (`unit-suite` e `handoff-check` success); check `verifica-bot` success — bot APPROVATA, verdetto APPROVATO CON RISERVE (V-1 BASSA istruzione voce «riassunto + dettaglio», V-2 BASSA bip/microfono: nella fetta V4). Verifica esterna su a1a6a25 APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/311#issuecomment-6527791803).
- b72809b (merge di main) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme).

## §7 RISERVE APERTE

- **V-2 bot #311** BASSA — i test della pagina nel browser in CI si saltano (il job non ha Node/Playwright): una regressione del client passa con la CI verde.
- **R-576-1-M2** BASSA — la guardia del permesso del microfono (R-575-2-M2) non ha un test.
- **R-576-3-M2** COSMETICA — la pausa senza conversazione dice «conversazione chiusa».
- **R-578-1-M2** BASSA — la voce minima di 250 ms va provata col microfono vero (un «sì» brevissimo).
- Prova col microfono vero sul Mac (soglia, eco, voce italiana della frase d'attesa) e su Safari: da fare.
- **V-1/V-2 bot #311 su a1a6a25** BASSE (istruzione voce senza «dettaglio», bip/microfono) e **V-2 ve #311 su a1a6a25** BASSA (tetto dei turni solo nella pagina): nella fetta V4, già assegnata da M1.
- Ereditate e dichiarate: R-564-1-M2 («Forte!» esclamazione va al forte), V-1 ve #304, R-384-2 (chat Voce).
