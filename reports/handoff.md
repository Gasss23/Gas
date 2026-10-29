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
- **R-570-1-M2 COSMETICA**: `DEFERITA — cosmetica, resta aperta (§7)`.
- **gas.py / brains/ / ci.yml**: `SALTATA — fuori dal mandato di M1`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 clients/voice/browser_server.py    |  49 +++++++++++++++++++++++++++++++++++++++++--------
 modules/voice/server.py            |  15 ++++++++++++++-
 reports/diff_sessione.md           |  15 +++++++--------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   1 +
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  36 +++++++++++++-----------------------
 tests/test_unit_voice_server.py    | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_stt.py       |  40 +++++++++++++++++++++++++++++++++++-----
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Il conteggio di `reports/ultimo_report.md` è di prima dell'ultima riga aggiunta (R-570-1-M2).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite (pytest, servizi finti): 113 → 118 test, `118 passed in 27.02s`; il file del server anche con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto (62 passed). Mutante sul tetto di connessione: il test nuovo fallisce dopo 30 s col codice vecchio, passa in ~1,6 s col fix. Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 5d95951, 8b33bf3, a6c97fb, 591730e: pushati insieme prima dell'apertura della PR #308; nessuna run della PR su questi SHA.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-570-1-M2** COSMETICA — test del proxy senza `server_close()` (ResourceWarning con `-W always`), socket di riempimento creati prima del `try`.
- Comportamento di Safari/Chrome con una richiesta aperta fino a 600 s: non verificato, da vedere nella prova sul Mac.
- Ereditate dalla V1 (dichiarate): R-564-1-M2 («Forte!» esclamazione va al forte), V-1 ve #304 (altri falsi positivi), R-384-2 (chat Voce, commento in ci.yml).
