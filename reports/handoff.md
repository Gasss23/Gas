# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Voce V2: istruzione d'uso a voce, avvio parlante, attesa del forte nel browser (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #308 (https://github.com/Gasss23/Gas/pull/308). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5076568053","url":"https://github.com/Gasss23/Gas/pull/308"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve decide l'operatore (tramite M1).

---

## §1 SCOPE & ESITO FETTE

- **V2.1 — V-2 verifica esterna #304 («Gas, forte.» da solo dava un 400 confuso)**: `FATTA` — «forte» parlato senza richiesta → istruzione d'uso da ascoltare (200/sintesi), nessun turno; «/forte» scritto resta 400.
- **V2.2 — V-3 verifica esterna #304 (server muto all'avvio)**: `FATTA` — riga «avvio in corso» prima del caricamento; provata con un `.env` vero temporaneo (poi cancellato).
- **V2.3 — attesa del forte nel proxy del browser (in più, detto a M1)**: `FATTA` — 600 s (`GAS_VOICE_TIMEOUT`), connessione 10 s, 504 chiaro.
- **Riserve #568-M2 (R-568-1/2/3-M2) e #569-M2 (R-569-1-M2)**: `FATTA`.
- **Secondo giro — bot #308 su 2dff07f (APPROVATA, APPROVATO CON RISERVE)**: V-1 BASSA (proxy a thread singolo fermo fino a 600 s) `FATTA` — `ThreadingHTTPServer`; V-2 COSMETICA (riga «avvio in corso» anche quando poi l'avvio si ferma) `SALTATA — la parte lenta è l'import di gas, che deve girare prima di leggere il token (può stare nel .env); il revisore #571-M2 è d'accordo`.
- **Secondo giro — verifica esterna #308 su 2dff07f (APPROVATO CON RISERVE, [commento](https://github.com/Gasss23/Gas/pull/308#issuecomment-6510176231))**: V-2 BASSA (risposta HTTP rotta → socket chiuso) `FATTA` — 502 JSON; V-1 BASSA (§6 superato) `FATTA`; V-3/V-4 BASSE accettate (503 senza chiave ElevenLabs come sul percorso normale; attese del browser da vedere sul Mac).
- **R-570-1-M2 COSMETICA**: `FATTA` nel secondo giro. **R-571-1/2-M2**: `FATTA` (review #572-M2 APPROVATO).
- **Merge di origin/main (PR #307 della chat M1) per il conflitto segnalato da M1**: `FATTA` — conflitti solo in `reports/diff_sessione.md`, `reports/handoff.md`, `reports/ultimo_report.md` (tenuta la nostra versione, riscritta qui) e `.claude/agents/memoria_revisore.md` (tenuti entrambi i blocchi); review #573-M2 APPROVATO; voce + richieste + gate 966 passed sul codice unito.
- **gas.py / brains/ / ci.yml**: `SALTATA — fuori dal mandato di M1`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 ++++++++++
 clients/voice/browser_server.py    |  63 +++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 modules/voice/server.py            |  15 ++++++++++++++-
 reports/diff_sessione.md           |  19 ++++++++-----------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   1 +
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  39 +++++++++++++++------------------------
 tests/test_unit_voice_server.py    | 190 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_stt.py       |  40 +++++++++++++++++++++++++++++++++++-----
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. BASE = 52c113b (main dopo la #307, merge-base dopo il merge 168a848).

## §3 GIT LOG --ONELINE (sessione)

```
168a848 Merge origin/main (PR #307) in feat/voce-v2-m2: conflitti solo nei report e nella memoria del revisore
2f223ab docs(voce-v2): report dopo il secondo giro di bot e verifica esterna #308, review #571/#572-M2
691e8c0 fix(voce): proxy del browser a thread, risposta rotta → 502 JSON, 504 che cita la coda (bot e ve #308)
5bf8eaa chore(revisore): memoria review #572 — APPROVATO
d8c8041 chore(revisore): memoria review #571 — APPROVATO CON RISERVE
2dff07f docs(voce-v2): report di fine task (PR #308, review #568-#570-M2)
591730e feat(voce): istruzione d'uso a voce, avvio parlante, attesa del forte nel browser (V2, chat M2)
a6c97fb chore(revisore): memoria review #570 — APPROVATO CON RISERVE
8b33bf3 chore(revisore): memoria review #569 — APPROVATO CON RISERVE
5d95951 chore(revisore): memoria review #568 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit 591730e è stato rivisto in tre passaggi sullo stesso diff staged (ogni passaggio dopo la correzione delle riserve del precedente). Verdetti integrali:

Review #568-M2 (primo passaggio; le citazioni si riferiscono al diff prima delle correzioni di R-568-1/2/3-M2, alcune righe a HEAD sono spostate):

VERDETTO: APPROVATO CON RISERVE

Review #568-M2. Ho esaminato il diff staged su feat/voce-v2-m2 (4 file). Prima di iniziare ho letto CLAUDE.md, la parte di stato_progetto.md che riguarda la voce e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/voice/server.py:202` — gestisce `cervello == "uso"`: se l'input è testo risponde 400, se il client vuole audio sintetizza la risposta con `_do_tts_response`, altrimenti risponde 200 in JSON con `"uso": True`.
  - Rischio esaminato: che «uso» faccia partire un turno.
  - Esito: ok. Tutti e tre i rami fanno `return` prima del `try` di `run_turn`.
  - `cervello_voce` restituisce «uso» per «Gas, forte.» prima di controllare GAS_VOCE_FORTE, quindi con l'interruttore acceso non parte un turno vuoto al forte.
  - I 3 test stt controllano `visti == []`.
  - Rispondere 200 invece di un codice 4xx è accettabile. Il browser manda sempre `Accept: audio/mpeg` (clients/voice/browser_client.html:375), quindi riceve l'audio con l'istruzione e non mostra più «errore: …». Il JSON porta `"uso": true` per distinguere la risposta. Il «/forte» scritto resta 400.
  - Se manca ELEVENLABS_API_KEY la risposta è 503, come sul percorso normale: è coerente.
- `modules/voice/server.py:327` — stampa la riga di avvio con `flush=True` prima di `sys.path` e degli import.
  - Esito: ok. Il test a tests/test_unit_voice_server.py:537 controlla l'ordine delle righe.
- `clients/voice/browser_server.py:110` — `except TimeoutError` messo prima di `except (ConnectionRefusedError, OSError)`.
  - Rischio esaminato: l'ordine, dato che TimeoutError è una sottoclasse di OSError e `socket.timeout is TimeoutError` (provato, Python 3.11+).
  - Esito: ok. Il mutante con il ramo tolto fa fallire 1 test (tests/test_unit_voice_server.py:570 riceve 502 invece di 504).
- `clients/voice/browser_server.py:59` — nuovo attributo di classe `timeout: int = 600`.
  - Esito: **riserva R-568-1-M2**, vedi sotto.
- `clients/voice/browser_server.py:166` — controllo che il valore sia un intero positivo.
  - Esito: **riserva R-568-2-M2**, vedi sotto.
- `tests/test_unit_voice_server.py:561` — `_browser_server_module` carica il modulo con `spec_from_file_location`, senza registrarlo in sys.modules.
  - Rischio esaminato: l'effetto di `logging.basicConfig` all'import.
  - Esito: ok. Provato sotto pytest: il root logger ha già i suoi handler (LogCaptureHandler e simili), quindi basicConfig non fa nulla. Handler e livello sono identici prima e dopo l'import.
- `tests/test_unit_voice_stt.py:70` — `_post_raw` riconosce le risposte `audio/*` invece di fare json.loads sui byte MP3.
  - Esito: ok. Il test a tests/test_unit_voice_stt.py:345 verifica il testo passato a `synthesize_speech`.

Suite voce: 117 passed (server, stt, tts).

**Riserve (tutte BASSE)**
- **R-568-1-M2**: l'attributo a `clients/voice/browser_server.py:59` si chiama `timeout` e così sovrascrive `socketserver.StreamRequestHandler.timeout`, che `setup()` usa come timeout del socket in ingresso dal browser.
  - Effetto: GAS_VOICE_TIMEOUT vale anche per la lettura della richiesta del browser.
  - Provato: con timeout=1, un client che manda gli header e poi il corpo dopo 2 s riceve «Request timed out» e una risposta vuota, che nel browser diventa «errore di rete».
  - Con il default di 600 s il danno è nullo (prima il valore era None, cioè nessun timeout). Con un valore piccolo impostato dall'operatore si possono perdere upload lenti.
  - Correzione: rinominare l'attributo (es. `voice_timeout`).
- **R-568-2-M2**: il mutante senza `if timeout <= 0` fa restare appeso il test a tests/test_unit_voice_server.py:611 invece di farlo fallire. Con «0» `run_browser_server` si mette in ascolto e resta su `serve_forever`; provato, ucciso a 40 s. In CI sarebbe un job appeso fino al timeout del job. Il test va bene così com'è, ma una regressione si vedrebbe come un blocco e non come un fallimento.
- **R-568-3-M2**: con un GAS_VOICE_URL remoto irraggiungibile (pacchetti scartati), il timeout di connessione solleva TimeoutError. L'operatore aspetta fino a 600 s (prima 90) e poi riceve il 504 «il lavoro può essere ancora in corso», che è fuorviante. Su 127.0.0.1 la connessione rifiutata è immediata e il problema non c'è.

**Rischi esplicitamente esclusi**
- Il test reale col microfono e ElevenLabs reale non è verificato: non è riproducibile in questo ambiente, tutti i test usano STT/TTS finti.
- Il comportamento di Safari/Chrome davanti a un fetch che resta aperto fino a 600 s non è verificato: il browser potrebbe chiudere prima del proxy.
- Non ho riprodotto il caricamento del `.env` temporaneo che dichiari (avvio reale).

gas.py, brains/ e ci.yml non sono toccati: confermato dal `--stat`.

Memoria: aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #568-M2 con una lezione: gli attributi di classe di un BaseHTTPRequestHandler possono collidere con quelli di socketserver (`timeout`, `rbufsize`, `wbufsize`, `disable_nagle_algorithm`). Committata col commit 5d95951 tramite scripts/commit_memoria_revisore.sh.

Review #569-M2 (secondo passaggio):

VERDETTO: APPROVATO CON RISERVE

Review #569-M2. Rivisto il diff staged su feat/voce-v2-m2 (sha256 7b26ac0b, 4 file). Le prove le ho fatte su una copia dell'index estratta con `git checkout-index`. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (solo le parti che servono) e la memoria del revisore.

**Elementi del diff esaminati**
- `clients/voice/browser_server.py:62` — l'attributo di classe ora si chiama `voice_timeout`, quindi il `timeout` di socketserver (il socket verso il browser) resta None. Rischio esaminato: la collisione di R-568-1-M2. Ho provato a rimettere un `timeout = 600` di classe: 1 failed su `tests/test_unit_voice_server.py:615`. Esito: **ok**, R-568-1-M2 chiusa.
- `tests/test_unit_voice_server.py:623` — `HTTPServer` è sostituito da una classe che solleva un'eccezione. Rischio esaminato: un test che resta appeso invece di fallire. Ho tolto `if timeout <= 0:`: 1 failed in 0,11 s, il test non resta appeso. Esito: **ok**, R-568-2-M2 chiusa.
- `clients/voice/browser_server.py:101` — prima `conn.connect()` con `_CONNECT_TIMEOUT`, poi `conn.sock.settimeout(self.voice_timeout)`; gli errori vanno all'`except OSError`, che risponde 502. Rischio esaminato: un connect che scade (TimeoutError) finisce nel 504 «ancora in corso». Prova reale: server con `listen(0)` e coda piena, così il connect resta appeso, e `_CONNECT_TIMEOUT=1`. Risultato: 502 «Voice server non raggiungibile: timed out» in 1,03 s. TimeoutError è una sottoclasse di OSError, quindi va al 502 e non al 504. Esito: **ok**.
- `clients/voice/browser_server.py:108` — `conn.request` dopo un connect esplicito. Rischio esaminato: una seconda connessione, oppure il tetto lungo perso. Prova con la stessa sequenza di chiamate: una sola `create_connection`, `c.sock` è lo stesso oggetto, `gettimeout()` resta quello impostato (77 nella prova), risposta 200. Esito: **ok**.
- `clients/voice/browser_server.py:123` — `except TimeoutError` → 504, solo per l'attesa della risposta. Il 504 quindi resta solo per il caso in cui Gas è lento. Esito: **ok**.
- `tests/test_unit_voice_server.py:631` — test con porta chiusa → 502 entro 5 s. Rischio esaminato: se il test discrimina il fix. Ho rimesso il vecchio codice (un'unica `HTTPConnection(timeout=self.voice_timeout)`, senza connect separato): **2 passed**. Una porta chiusa dà un rifiuto immediato con qualunque timeout, quindi il test non prova R-568-3-M2. Esito: **riserva**.

**Resto del diff**: `modules/voice/server.py` (istruzione d'uso parlata → 200 o TTS, riga d'avvio) e `tests/test_unit_voice_stt.py` sono coerenti con quanto già approvato in #568-M2. Nessun cambiamento oltre ai tre fix.

**Test**: voce 94 passed (server + stt; il 118 dichiarato include anche i test TTS, che non ho eseguito). Il file server con `http_proxy` impostato: 62 passed. Guardrail: `_get_window`, cap 10 iterazioni e cap 8k non sono toccati; nessuno slicing della history, nessuna simulazione di tool.

**Riserve**
- **R-569-1-M2 BASSA**: `tests/test_unit_voice_server.py:631` non discrimina R-568-3-M2: col fix tolto il test passa lo stesso. Per provarlo serve un connect che resti appeso, cioè un socket con `listen(0)` e coda riempita (oppure un indirizzo che non risponde), più `monkeypatch.setattr(bs, "_CONNECT_TIMEOUT", 1)`, e poi controllare 502 entro circa 3 s. Il codice è corretto: l'ho provato a mano.

**Rischio escluso**: non ho verificato un `GAS_VOICE_URL` remoto reale (VPS o rete esterna), che in sviluppo non si riproduce; ho simulato il connect appeso con la coda piena in locale. Non ho nemmeno confrontato byte per byte con il diff di #568-M2, perché quella copia non è stata salvata: il resto l'ho controllato per coerenza con la descrizione di #568-M2.

**Memoria**: aggiunte la riga #569-M2 e una lezione (una porta chiusa non prova un fix sul timeout di connect) in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole con lo script (commit 8b33bf3, «chore(revisore): memoria review #569 — APPROVATO CON RISERVE»).

Review #570-M2 (terzo passaggio, diff finale committato in 591730e):

VERDETTO: APPROVATO CON RISERVE

Ri-review #570-M2 di feat/voce-v2-m2, sul diff staged (sha256 di `git diff --cached` = 09d1baf2…, 4 file, +205/−14). Ho fatto le prove su un export dell'index (`git checkout-index`), non sulla cartella di lavoro. La cartella di lavoro ha modifiche non in staging solo in reports/.

Cosa ho esaminato:

- `tests/test_unit_voice_server.py:631` — il nuovo test `test_v2_browser_proxy_connessione_appesa_502_subito` sostituisce quello sulla porta chiusa. Rischio esaminato: che non distingua il fix, o che fallisca a caso sui runner Linux della CI. Esito: **ok**. 10 esecuzioni di fila: 10 passed, tutte tra 1,59 e 1,64 s. Su Linux, con la coda di accettazione piena il kernel scarta il SYN anche con `tcp_syncookies=1` (qui vale 1, come sui runner GitHub), quindi il connect del proxy resta appeso in modo prevedibile. Margini: connect a 1 s, client `_post` a 5 s, controllo finale a meno di 10 s.
- `tests/test_unit_voice_server.py:639` — `listen(0)` più 8 connect non bloccanti. Rischio esaminato: che 8 connect non bastino a riempire la coda. Esito: **ok**. Linux accetta backlog+1 = 1 connessione, le altre restano in SYN_SENT; 8 sono più del necessario.
- `tests/test_unit_voice_server.py:647` — `monkeypatch.setattr(bs, "_CONNECT_TIMEOUT", 1)`. Rischio esaminato: che il codice legga il valore una volta sola all'import, così la patch non avrebbe effetto. Esito: **ok**. `clients/voice/browser_server.py:97` legge la variabile globale a ogni chiamata.
- `clients/voice/browser_server.py:97` — la connessione usa il tetto corto `_CONNECT_TIMEOUT`. Rischio esaminato: che il test non distingua il fix dal vecchio codice. Esito: **ok**. Mutante con `timeout=self.voice_timeout)` (il comportamento vecchio, un solo tetto): 1 failed in 30,4 s. Codice vero: 1 passed in 1,6 s. Coincide con la tua prova. **R-569-1-M2 CHIUSA.**
- `clients/voice/browser_server.py:101` — `conn.connect()` separato seguito da `conn.sock.settimeout(self.voice_timeout)`. Codice invariato rispetto a #569-M2. Rischio esaminato: regressioni sul ramo 504 e sul ramo 502. Esito: **ok**. Voce server+stt: 94 passed sull'export; il test 504 passa.
- `tests/test_unit_voice_server.py:662` — il `finally` chiama `proxy.shutdown()`, chiude i riempitivi e poi `pieno` (`tests/test_unit_voice_server.py:665`). Rischio esaminato: socket non chiusi. Esito: **riserva cosmetica**, vedi R-570-1-M2 sotto.

Riserve:

- **R-570-1-M2 COSMETICA**: il test chiama `proxy.shutdown()` ma non `proxy.server_close()`, quindi il socket in ascolto del proxy resta aperto. Con `-W always::ResourceWarning` compare «unclosed <socket … laddr=('127.0.0.1', …)>». Aggiungendo `proxy.server_close()` l'avviso sparisce (provato). In più, i socket `pieno` e i riempitivi nascono prima del `try`: se il setup solleva, non vengono chiusi. Non rende il test instabile; il test 504 vicino ha lo stesso schema (`lento`/`proxy` senza `server_close`).

Cosa NON ho verificato:

- Il comportamento del test su macOS (lì `listen(0)` e la coda piena funzionano in modo diverso). La CI gira su Linux; io non posso riprodurre macOS qui.
- Un runner GitHub vero: ho provato in questo container Linux con lo stesso sysctl, non su Actions.

Memoria del revisore: riga #570-M2 e una lezione (`shutdown()` senza `server_close()`) committate con `scripts/commit_memoria_revisore.sh` (a6c97fb) in /home/user/Gas/.claude/agents/memoria_revisore.md.

Commit 691e8c0 — review #571-M2 (primo passaggio del secondo giro; poi corrette R-571-1/2-M2, alcune righe a HEAD sono spostate di poco), verdetto integrale:

VERDETTO: APPROVATO CON RISERVE

Review #571-M2. Branch feat/voce-v2-m2 (PR #308), diff in staging: 2 file (`clients/voice/browser_server.py` e `tests/test_unit_voice_server.py`). Ho fatto le prove su una copia dei file in staging, nella scratchpad, per non toccare il repo.

Letture obbligatorie fatte: CLAUDE.md (sezione 5), reports/stato_progetto.md (voce relativa a PR #308 e R-570-1-M2), coda di memoria_revisore.md (lezioni #570-M2 su server_close e su come provare un connect appeso).

**Elementi del diff esaminati**
- `clients/voice/browser_server.py:201` — il proxy ora usa ThreadingHTTPServer. Rischio esaminato: stato condiviso fra thread. BrowserProxyHandler legge solo attributi di classe (token, voice_host, voice_port, voice_timeout), che si scrivono una volta sola prima di creare il server (`clients/voice/browser_server.py:194-197`). La HTTPConnection è locale a ogni richiesta (`clients/voice/browser_server.py:96`). Il logging è thread-safe e ThreadingHTTPServer usa thread daemon. Nessuno stato mutabile condiviso. Esito: ok.
- `clients/voice/browser_server.py:131` — nuovo ramo per http.client.HTTPException, che risponde 502 JSON. Rischio esaminato: ordine dei rami except. RemoteDisconnected è anche un OSError e finisce prima nel ramo «non raggiungibile» (`clients/voice/browser_server.py:128`): accettabile. BadStatusLine e IncompleteRead arrivano al nuovo ramo. Quando scatta, al browser non è ancora stato inviato nulla, e il `finally` chiude la connessione. Mutante con il ramo cambiato in ZeroDivisionError: `test_v2_browser_proxy_risposta_rotta_502_json` fallisce (1 failed). Esito: ok.
- `tests/test_unit_voice_server.py:641` — il test del connect appeso ora crea ogni socket dentro il try e lo chiude nel finally, e chiama `server_close()`. Rischio esaminato: socket lasciati aperti. Con `-W always::ResourceWarning` sui test v2_browser: 0 «unclosed». R-570-1-M2 chiusa. Esito: ok.
- `tests/test_unit_voice_server.py:674` — `test_v2_browser_proxy_a_thread`. Rischio esaminato: il test si accorge davvero se si torna indietro? Mutante con `ThreadingHTTPServer((` cambiato in `HTTPServer((`: il test non fallisce, si BLOCCA (avvia un serve_forever vero sulla porta 9000). Ho dovuto ucciderlo a mano. È lo stesso difetto che R-568-2-M2 aveva già chiuso sul test del timeout sbagliato. Esito: riserva (R-571-1-M2).
- `tests/test_unit_voice_server.py:625` — il test del timeout sbagliato ora sostituisce `ThreadingHTTPServer`. Esito: ok, coerente con la nuova classe.
- Contesto: `modules/voice/server.py:327` — riga «avvio in corso» (V-2 bot #308 COSMETICA, non modificata). Sono d'accordo a non toccarla: `_carica_env` (`modules/voice/server.py:311`) importa gas, che è la parte lenta, e deve girare prima di leggere `GAS_VOICE_TOKEN` perché il token può stare nel `.env`. Spostare la riga lascerebbe muti proprio i secondi lenti. Il costo è una riga in più quando poi l'avvio si ferma per token mancante: trascurabile.

**Riserve**
- **R-571-1-M2 BASSA**: `test_v2_browser_proxy_a_thread` sostituisce solo `ThreadingHTTPServer`. Se il codice tornasse a `HTTPServer`, il test si bloccherebbe invece di fallire (in CI finirebbe in timeout). Correzione: con monkeypatch sostituire anche `bs.HTTPServer` con un finto che solleva AssertionError, come `_NonDevePartire`. Serve `getattr` o `raising=False`, perché `HTTPServer` non è più importato nel modulo.
- **R-571-2-M2 BASSA (solo nota, nessuna correzione obbligatoria)**: ora il proxy lavora a thread. Due POST nello stesso momento (per esempio una seconda scheda mentre il forte lavora) si collegano subito e restano in coda dietro al server voce, che fa un turno alla volta. Il tetto di GAS_VOICE_TIMEOUT conta anche il tempo in coda. Quindi la seconda richiesta può ricevere 504 mentre il server voce eseguirà comunque quel turno più tardi. Basterebbe una riga nel docstring o nel messaggio 504.

**Prove eseguite**
- Suite voce: 120 passed.
- Test v2_browser con ResourceWarning attivo: 0 «unclosed».
- Mutante sul ramo HTTPException: il test fallisce (1 failed).
- Mutante sul ritorno a HTTPServer: il test si blocca (vedi R-571-1-M2).

**Cosa non ho verificato**
- Il comportamento reale nel browser sul Mac (ricarica della pagina mentre il forte lavora; più schede aperte): non si può riprodurre nel container, ho controllato solo la struttura del codice.
- Se `browser_client.html` disattiva il pulsante durante una richiesta: l'ho visto solo nel CSS (`#btn-record:disabled`), la logica JS non l'ho letta.

Antipattern della sezione 5 (slicing della history, output dei tool simulato): non presenti. Non sono toccati né il motore né `_get_window`, né i limiti di iterazioni e di output.

Memoria del revisore: aggiunte la riga #571-M2 e una lezione nuova (stubbare sia la classe nuova sia quella vecchia). Commit d8c8041 con `scripts/commit_memoria_revisore.sh`, file `/home/user/Gas/.claude/agents/memoria_revisore.md`.

Commit 691e8c0 — review #572-M2 (diff finale committato), verdetto integrale:

VERDETTO: APPROVATO

Ri-review #572-M2 sul branch feat/voce-v2-m2 (PR #308). Ho controllato il diff staged (sha256 di `git diff --cached` = 7abf82503a9c…), facendo girare i test su una copia dell'index (`git checkout-index`). File toccati: solo `clients/voice/browser_server.py` e `tests/test_unit_voice_server.py` (+105/−20).

Letture fatte: CLAUDE.md (sezioni 5, 8, 9), `reports/stato_progetto.md` (solo le parti che servono) e `.claude/agents/memoria_revisore.md` (riga #571-M2 e lezione collegata).

Elementi del diff esaminati:
- `tests/test_unit_voice_server.py:701` — sostituisce `bs.HTTPServer` (con raising=False) con `_Vecchio`, che solleva AssertionError. Rischio: un ritorno a `HTTPServer` farebbe partire un `serve_forever` vero e il test si bloccherebbe invece di fallire (R-571-1-M2). Prova: ho riportato il codice a `server = HTTPServer((` e reimportato `HTTPServer` → 1 failed in 0.16 s, AssertionError a `tests/test_unit_voice_server.py:698`, nessun blocco. Con raising=False il test regge anche quando il nome `HTTPServer` non esiste più nel modulo, come succede oggi. — ok, riserva chiusa.
- `clients/voice/browser_server.py:128` — il messaggio 504 ora dice «(o in coda dietro un'altra richiesta)», con il commento a `clients/voice/browser_server.py:125` che spiega che il server voce fa un turno alla volta. Rischio: rompere l'asserzione esistente. L'asserzione a `tests/test_unit_voice_server.py:610` («entro 1 s» e «ancora in corso») è ancora soddisfatta: il testo «ancora in corso» c'è ancora. Dire all'utente che il turno può essere ancora in coda risponde a R-571-2-M2, che era una nota e non chiedeva di cambiare il comportamento. — ok, riserva chiusa.
- `clients/voice/browser_server.py:204` — `ThreadingHTTPServer` e il ramo `http.client.HTTPException` → 502 JSON: identici a quanto approvato in #571-M2. `http.client` è importato a `clients/voice/browser_server.py:22`. Il ramo `except` resta prima di `finally: conn.close()`. Nessuna eccezione arriva fino al crash. — ok.
- `tests/test_unit_voice_server.py:623` — lo stub per i valori sbagliati di GAS_VOICE_TIMEOUT ora punta a `ThreadingHTTPServer`, coerente con il codice. — ok.

Delta rispetto a #571-M2: oltre a R-571-1 e R-571-2, il diff ha lo stesso contenuto descritto in #571-M2 (passaggio a thread, ramo HTTPException, test a_thread / risposta_rotta / connessione appesa con try/finally, server_close). Non ho trovato altro. Nessuno slicing della history, nessun output di tool simulato, guardrail (10 iterazioni, `_get_window`, tetto di output) non toccati: il diff è solo nel client vocale.

Esecuzione: tutti i test della voce 120 passed (24.3 s); `tests/test_unit_voice_server.py` da solo 64 passed.

Rischio escluso: non ho rifatto a mano la prova con due schede reali in contemporanea contro un server voce vero con un modello forte lento. Il nuovo testo del 504 è solo un messaggio e la coda del server voce non cambia; la prova richiede un ambiente con il brain attivo, non riproducibile qui.

Memoria: riga contatore `#572-M2 — 2026-10-29 — APPROVATO — …` aggiunta in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola (5bf8eaa). Nessuna lezione nuova. Il diff staged del motore non è stato toccato.

Commit 168a848 (merge di origin/main, PR #307 della chat M1) — review #573-M2, verdetto integrale:

VERDETTO: APPROVATO

Review #573-M2: merge in staging di origin/main (PR #307, ponte M1) dentro feat/voce-v2-m2 (PR #308). MERGE_HEAD coincide con origin/main (52c113b).

Elementi del diff che ho esaminato:
- `.claude/agents/memoria_revisore.md:1020`: le righe #557-M1, #558-M1 e #559-M1 di main, ognuna con la sua lezione, sono in coda subito dopo il blocco #568-#572-M2. Ho controllato se qualcosa era stato perso o duplicato: il diff staged rispetto a HEAD è solo +6 righe (nessuna riga rimossa, a parte l'intestazione `---`), e i conti tornano: HEAD 1017 + 6 = 1023. Esito: ok.
- `gas.py:4625`: il ramo `richiedi_sviluppo` e lo schema dello strumento in `gas.py:1232` arrivano da #307. Ho controllato se il merge altera il motore oltre l'unione: il diff staged su gas.py, modules/sviluppo, modules/gate, .github, i test gate/kernel/richieste, gas_identity.md e .gitignore è identico byte per byte a `git diff merge-base..origin/main`. La nostra parte non tocca nessuno di questi file (stat vuoto). Esito: ok.
- `modules/sviluppo/richieste.py:58`: `_http` con l'handler anti-redirect, file nuovo che arriva da main. Già revisionato in #557-#559-M1; qui ho solo controllato che sia arrivato identico. Esito: ok.
- `.github/workflows/ci.yml:105`: lo step «Run voice suite» lancia ancora test_unit_voice_server, stt e tts. `.github/workflows/ci.yml:166` aggiunge la suite richieste. Il rischio era che il merge facesse sparire la suite voce dalla CI: non è successo. Esito: ok.
- `reports/stato_progetto.md:4`: con l'auto-merge l'intestazione «Ultimo aggiornamento» ha preso la versione M1. È coerente perché la nostra parte non aveva cambiato quella riga, e /fine-task la riscriverà. La sezione «Coordinamento delle chat» (righe 586-589) è stata aggiunta senza duplicati. Esito: ok.
- `reports/roadmap.md:282`: la voce «Ponte Gas → sviluppo, strada A» sostituisce quella vecchia sul ponte con firma, un solo hunk e pulito. Esito: ok.

Altri controlli:
- Marcatori di conflitto: `git grep` sui marcatori di conflitto (`<<<<<<<`, `=======`, `>>>>>>>`) e `git diff --cached --check` non trovano nulla.
- Codice voce: `git diff origin/main` su modules/voice, clients/voice e test_unit_voice_*.py è identico al diff proprio della PR (merge-base..HEAD). Stesso stat: 4 file, +292/-16.
- handoff.md, ultimo_report.md e diff_sessione.md: risolti con la nostra versione, quindi nessuna differenza staged rispetto a HEAD.
- Test, rilanciati da me: suite voce (server, stt, tts) + richieste + gate = 966 passed in 27,97 s.

Rischi che NON ho verificato:
- Non ho rilanciato `tests/test_unit_kernel.py`. Il diff di gas.py è identico a quello di #307, già revisionato e verde sulla CI di main, ma l'unione col codice voce non l'ho provata a runtime: lo farà la CI della PR.
- Non ho controllato il comportamento reale del ponte verso `Gasss23/Gas-richieste`: serve la rete e un token, ed è fuori dallo scopo di un merge.

Riga contatore: ho scritto #573-M2 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`. `scripts/commit_memoria_revisore.sh` però non ha committato: con un merge in corso `git commit -o` fallisce, lo script se ne accorge e prosegue senza bloccare. Quindi la riga è solo nel working tree (stato `MM`). **Prima di committare il merge devi fare `git add .claude/agents/memoria_revisore.md`**, altrimenti la riga #573-M2 resta fuori dal commit. Dopo l'add il diff staged cambia, quindi `segna_review_ok.sh` va lanciato dopo l'add.

NB (agente): fatto così — `git add` della memoria, poi `segna_review_ok.sh`, poi il commit 168a848.

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite (pytest, servizi finti): 113 → 120 test, `120 passed in 25.76s`; il file del server anche con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto. Mutanti: tetto di connessione (test fallisce dopo 30 s col codice vecchio), ramo HTTPException (1 failed), ritorno a HTTPServer (1 failed in 0,15 s, nessun blocco). `-W always::ResourceWarning` sui test del proxy: 0 «unclosed». Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 5d95951, 8b33bf3, a6c97fb, 591730e: pushati insieme prima dell'apertura della PR #308; nessuna run della PR su questi SHA.
- 2dff07f (fine-task del primo giro): run CI 40967502095 (`unit-suite` e `handoff-check` success); check `verifica-bot` success — bot APPROVATA, verdetto APPROVATO CON RISERVE (V-1 BASSA chiusa in 691e8c0, V-2 COSMETICA lasciata com'è, vedi §1).
- d8c8041, 5bf8eaa, 691e8c0: nessuna run su questi SHA (pushati insieme a 2f223ab).
- 2f223ab (fine-task del secondo giro): run CI 40969002250 (`unit-suite` e `handoff-check` success); check `verifica-bot` success — bot APPROVATA, verdetto APPROVATO CON RISERVE (solo V-1 COSMETICA: «attesa massima N s» approssimata, vedi §7).
- 168a848 (merge di main) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme).

## §7 RISERVE APERTE

- **V-2 bot #308** COSMETICA — la riga «avvio in corso» esce anche quando poi l'avvio si ferma per configurazione: lasciata di proposito (motivo in §1).
- **V-1 bot #308 su 2f223ab** COSMETICA — «attesa massima N s» e il 504 «entro N s» sono approssimati: il tetto vale per ogni operazione sul socket, più fino a 10 s di connessione.
- **V-3 ve #308** BASSA — istruzione d'uso a voce senza ELEVENLABS_API_KEY → 503 (come ogni risposta audio).
- **V-4 ve #308** BASSA — attese da 600 s nel browser (Safari/Chrome) non verificate: da vedere nella prova sul Mac.
- Ereditate dalla V1 (dichiarate): R-564-1-M2 («Forte!» esclamazione va al forte), V-1 ve #304 (altri falsi positivi), R-384-2 (chat Voce, commento in ci.yml).
