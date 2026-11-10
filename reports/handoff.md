# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — voce: correzioni dell'audit notturno (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #367 (https://github.com/Gasss23/Gas/pull/367): con verdetto del bot senza finding ALTA/MEDIA e CI verde, sì dell'operatore riferito da M1 («mergia tutto quello che il bot ha approvato»).

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **B1 — timeout del socket del server voce (60 s)**: `FATTA` (1c53cf9).
- **B2 — «Hey Jarvis, forte: …» al forte, anche con la parola ripetuta**: `FATTA` (1c53cf9).
- **B3 — risposte rotte di Groq ed ElevenLabs come errori di rete (sintesi, elenco voci, libreria, aggiunta voce)**: `FATTA` (1c53cf9; R-752-2 chiusa nello stesso commit, review #755-M2).
- **B4 — `.env` del proxy del browser con le regole di Gas**: `FATTA` (1c53cf9).
- **B5 — JSON di forma sbagliata → 400**: `FATTA` (1c53cf9).
- **Miglioramenti (413, porta prima del kernel, proxy su GAS_VOICE_PORT)**: `FATTA` (1c53cf9; R-752-3 chiusa, review #755-M2).
- **Merge di origin/main f4d2d4f (#364, #365)**: `FATTA` (d1b5628), review #759-M2.
- **Merge di origin/main a164b42 (#363 terminale A)**: `FATTA` (1af440e) — conflitti solo nei report e nella memoria; review #760-M2 APPROVATO; manutenzione + voice_server + stt + tts + gate 1207 passed.
- **Bot e verifica esterna #367 su ea3033b**: APPROVATO CON RISERVE, solo BASSE (porta fuori 0-65535 → traceback; test del timeout solo sulle intestazioni e con soglia stretta; GAS_VOICE_PORT filtrato a sole cifre): registrate in §7.
- **Sospetti di M1 da valutare** («forte» durante «Sì, signore?», blocco per IP condiviso su 127.0.0.1, connessione ElevenLabs riusata): `DEFERITA` — non toccati qui.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +++++
 clients/voice/browser_server.py    |  45 ++++++++++++++++++++++++++++++++++++++-------
 modules/voice/server.py            |  39 +++++++++++++++++++++++++++++++++++----
 modules/voice/stt.py               |   8 ++++++--
 modules/voice/tts.py               |  28 ++++++++++++++++++++--------
 reports/diff_sessione.md           |  17 ++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |   2 ++
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  23 ++++++++---------
 tests/test_unit_voice_server.py    | 171 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_voice_stt.py       |  18 ++++++++++++++++++
 tests/test_unit_voice_tts.py       |  30 ++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1af440e Merge origin/main (#363) nelle correzioni dell'audit voce — review #760-M2 APPROVATO (chat M2)
ea3033b docs(fine-task): voce — correzioni dell'audit notturno, PR #367 (chat M2)
d1b5628 Merge origin/main (#364, #365) nelle correzioni dell'audit voce — review #759-M2 APPROVATO (chat M2)
1c53cf9 fix(voce): correzioni dell'audit notturno — timeout del socket, «Hey Jarvis, forte» al forte, risposte rotte di Groq/ElevenLabs come errori di rete, .env del browser come Gas, 400 al JSON di forma sbagliata, tetti 413, porta prima del kernel — review #752-M2, #755-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #760-M2 (merge di main a164b42, PR #363) — verdetto integrale

VERDETTO: APPROVATO

Review #760-M2: merge di origin/main a164b42 (PR #363, terminale A) in fix/voce-audit-m2 (PR #367), in staging nel worktree /home/user/Gas-audit.

Controlli fatti:
- **Stato del merge:** MERGE_HEAD è a164b42. `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.
- **File di main identici:** gas.py, modules/gate/gate.py, modules/manutenzione/__init__.py, tests/test_unit_manutenzione.py e .github/workflows/ci.yml non compaiono in `git diff --cached origin/main`, quindi sono identici a origin/main.
- **Differenza rimasta rispetto a main:** `git diff --cached origin/main` contiene solo l'audit voce (modules/voice/server.py, stt.py, tts.py, clients/voice/browser_server.py, test voice_server/stt/tts), i report, la memoria e stato_progetto.md (+1 riga).
- **Codice dell'audit non toccato dal merge:** la differenza staged rispetto a HEAD sui file voce, browser e test voice è di 0 righe.

Elementi del diff esaminati:
1. `modules/voice/server.py:589`: `_chiudi_tempi` scrive «tempi voce (%s): k=v.vvs». Rischio: che l'audit abbia cambiato il formato letto da log_voce. Esito: ok. Nel diff dell'audit rispetto a main nessuna riga +/- tocca «tempi», e la regex di contesto in `modules/manutenzione/__init__.py:45` richiede proprio `\(\d{3}\): (?:[a-z_]+=\d+(?:\.\d+)?s ?)+`.
2. `modules/voice/server.py:751`: il nuovo 413 passa da `_send_json`, quindi da `_chiudi_tempi`. Rischio: una riga «tempi voce» che log_voce non riconosce. Esito: ok. Il codice ha 3 cifre e, se nella richiesta non si è ancora speso tempo, `_tempi` è vuoto e non viene scritta nessuna riga.
3. `modules/voice/server.py:547` (`timeout = 60`) e `clients/voice/browser_server.py:362` (porta da GAS_VOICE_PORT): sono solo del server voce e del proxy, e la manutenzione non li usa. Rischio: interazione con `riavvia_voce` o `stato_gas`. Esito: ok, nessuna dipendenza.
4. Memoria e stato_progetto: con un controllo `uniq -d` non risultano righe duplicate introdotte dal merge. Le intestazioni #736–#739 doppie esistono già su origin/main e #742-M2 è doppio già su HEAD, quindi non dipendono da questo merge.

Test: ho lanciato una selezione mirata di manutenzione e voice_server con `-k "log_voce or tempi or audit"`: 22 passed. I 1207 dichiarati dall'agente non li ho rilanciati.

Rischio escluso: non ho riprodotto log_voce su un gas_debug.log reale del Mac con richieste andate in timeout. Il timeout chiude il socket senza passare da `_send_json`, quindi in quel caso non c'è riga dei tempi: è coerente con l'esito, ma non l'ho provato dal vivo. Resta aperta R-752-1 (riserva BASSA dell'audit: il timeout di 60 s vale per tutto l'invio di una risposta lunga e non ferma chi manda pochi byte alla volta).

Memoria: ho aggiunto la riga #760-M2 in coda a /home/user/Gas-audit/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git -C /home/user/Gas-audit add`. Nessun commit, come richiesto. Nessuna lezione nuova.

### Review #759-M2 (merge di main f4d2d4f, commit d1b5628) — verdetto integrale

VERDETTO: APPROVATO

Il merge staged di origin/main f4d2d4f (che contiene la #364 di M3 e la #365 di M2) nel ramo fix/voce-audit-m2 (commit 1c53cf9) è corretto. In server.py convivono tutte le correzioni dell'audit e il filtro del seguito, e l'ordine dei controlli in do_POST è quello giusto.

**Stato del merge**
- MERGE_HEAD coincide con origin/main (f4d2d4f).
- `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.
- gas.py, modules/gate/gate.py, modules/sottofondo/__init__.py e i loro tre test sono identici a origin/main.
- Rispetto alla base 3f08352, le righe aggiunte e tolte dall'audit sono identiche a 1c53cf9. Vale per clients/voice/browser_server.py, modules/voice/stt.py, modules/voice/tts.py, tests/test_unit_voice_tts.py e per le righe +/- di modules/voice/server.py.

**Elementi del diff esaminati**
- `modules/voice/server.py:775` — controllo della pausa, seguito dal controllo della sola parola di attivazione. Ho controllato se il filtro della #365 è stato inserito prima di questi due controlli. Esito: ok. Il filtro sta dopo entrambi, quindi «Hey Jarvis, pausa» nel seguito resta una pausa.
- `modules/voice/server.py:790` — `seguito_da_scartare` sul parlato del seguito, prima di `cervello_voce`. Ho controllato se la nuova `_PAROLA_FORTE` (con jarvis) cambia cosa viene scartato. Esito: ok, provato a mano:
  - «Jarvis, forte.» ha due parole e non viene scartato. `cervello_voce` dà `('uso','')`, poi il seguito si chiude senza voce (`modules/voice/server.py:820`).
  - «Forte!» viene scartato prima del cervello.
  - «Hey Jarvis, forte: che tempo fa» va al forte.
  - «Jarvis, Gas, forte dimmi» va al forte.
  - «Fortemente sì» resta normale.
- `modules/voice/server.py:118` — `_PAROLA_FORTE` riconosce `jarvis` e la parola ripetuta. Ho controllato se il merge ha perso o duplicato la riga. Esito: ok, compare una volta sola, nella forma di 1c53cf9.
- `modules/voice/server.py:750` (tetto 413 prima di leggere il corpo) e `modules/voice/server.py:802` (400 per JSON di forma sbagliata) — Ho controllato se il ramo testo è ancora integro dopo l'unione con la #365. Esito: ok. La #365 tocca solo il ramo audio.
- `modules/voice/server.py:1514` — la porta si apre prima del kernel e il server viene chiuso con `server_close` se il kernel fallisce. Esito: ok, l'hunk è identico.
- `tests/test_unit_voice_server.py:19` — la riga di import diventa `BaseHTTPRequestHandler, HTTPServer`. Ho controllato se nel conflitto si è perso un import. Esito: ok. Conteggio dei test: 77 nella base, +2 da main, +7 dall'audit, totale 86. Nessun nome duplicato, quindi nessun test ne nasconde un altro. Ci sono sia `test_seguito_da_scartare_e_istruzione_severa` (riga 2561) sia `test_audit_*` (righe 2409–2532).
- `tests/test_unit_voice_stt.py` — unito senza conflitti. Esito: ok, coperto dalla suite.

**Test lanciati da me**
- tests/test_unit_voice_server.py, tests/test_unit_voice_stt.py e tests/test_unit_voice_tts.py senza filtro `-k`, quindi browser inclusi: 347 passed in 5 minuti.

**Cosa non ho verificato**
- Le suite voce_ascolto, telegram_voce e sottofondo, e la suite completa: non le ho rilanciate. Mi fido delle 808 passate dichiarate dall'agente, e i file di M3 sono identici a origin/main.
- Il comportamento reale sul Mac (Whisper, flusso H24): non si può riprodurre qui.
- La riserva R-752-1 (timeout di `sendall` come durata totale dell'invio) resta aperta.

**Memoria**
- Ho aggiunto la riga contatore `#759-M2` (nessuna lezione nuova) in coda a /home/user/Gas-audit/.claude/agents/memoria_revisore.md.
- Il file è in staging con `git -C /home/user/Gas-audit add`. Nessun commit, come richiesto.

### Review #755-M2 (seguito di #752-M2, R-752-2 e R-752-3) — verdetto integrale

VERDETTO: APPROVATO

Review #755-M2 (seguito della #752-M2), nel worktree /home/user/Gas-audit, solo sul delta. Le due riserve R-752-2 e R-752-3 sono chiuse: tutti e 4 i mutanti sono stati uccisi.

**Cosa ho controllato nel diff**
- **modules/voice/tts.py:161** (`list_voices`), **modules/voice/tts.py:222** (`list_shared_voices`), **modules/voice/tts.py:279** (`add_shared_voice`)
  - Cosa fa: un HTTPException su `getresponse()` o `read()` diventa OSError, con `from exc`.
  - Rischio esaminato: risposta rotta che esce dal gestore e lascia la richiesta senza risposta.
  - Esito: ok. Il server prende già OSError in tutti e tre i rami (elenco voci, libreria, aggiunta) e risponde in modo dichiarato.
  - Mutante: ho tolto la conversione una funzione alla volta (in tutte e 3, non solo in `list_voices`). Ogni volta `test_audit_b3_altre_funzioni_tts` fallisce: ucciso.
- **clients/voice/browser_server.py:362-364**
  - Cosa fa: se manca GAS_VOICE_URL, il proxy del browser usa GAS_VOICE_PORT.
  - Rischio esaminato: ripiego senza test.
  - Esito: ok. Il nuovo `test_audit_proxy_segue_gas_voice_port` copre tre casi: GAS_VOICE_PORT=9001 dà 9001, nessuna variabile dà 8765, GAS_VOICE_URL ha la precedenza.
  - Mutante: con l'URL fisso a 8765 il caso 9001 fallisce: ucciso.

**Test**: suite tts + stt + test della porta: 137 passed, sulla copia dell'index.

**Nota (BASSA, non bloccante)**: in `add_shared_voice` la risposta può rompersi DOPO che ElevenLabs ha già aggiunto la voce. Il server però risponde «Errore di rete verso ElevenLabs» invece di «esito incerto, controlla l'account» (come fa già quando lo status è 200 ma l'id manca).

**Cosa NON ho verificato**
- R-752-1 resta aperta: lo stream NDJSON con risposte lunghe e il timeout di 60 s su `sendall` vanno misurati sul Mac, qui non si può riprodurre.
- Non ho rieseguito tutte le 373 dichiarate (prova_voci e i test del server oltre a quello della porta): il delta tocca solo tts.py e i due test nuovi.

**Memoria**: riga `#755-M2` aggiunta in coda a /home/user/Gas-audit/.claude/agents/memoria_revisore.md e messa in staging con `git -C /home/user/Gas-audit add`. Nessun commit, come chiesto. Nessuna lezione nuova.

### Review #752-M2 (correzioni dell'audit) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #752-M2 del diff STAGED in /home/user/Gas-audit (branch fix/voce-audit-m2, base 3f08352). Prima della review ho letto CLAUDE.md (sez. 5), le parti utili di stato_progetto.md e la coda della memoria. Nessun antipattern del Wall of Shame: niente slicing della history, niente output dei tool simulato. Cap 10 iterazioni, `_get_window` e i guardrail non sono toccati.

**Cosa ho controllato nel codice**
- modules/voice/server.py:495 — `timeout = 60` sul VoiceHandler.
  - Rischio: tagliare le risposte lunghe del forte.
  - Esito: ok, con riserva.
    - Mentre il kernel calcola (fino a 300 s) il socket non fa operazioni, quindi il timeout non scatta.
    - Il timeout però vale anche su `sendall`, e da Python 3.5 conta la durata TOTALE dell'invio, non il singolo pezzo. L'ho provato con un socketpair: TimeoutError a 2,0 s anche se il lettore riceveva.
    - Il client (clients/voice/ascolto.py:614) legge una riga NDJSON, suona la frase e solo dopo legge la successiva. Quando i buffer si riempiono, ogni riga deve partire entro 60 s mentre il client suona la frase prima. Con frasi normali va bene, ma va misurato sul Mac con una risposta lunga.
    - Sulla lettura il timeout vale per ogni singola recv. Basta per una connessione muta, non per lo slowloris (1 byte ogni 59 s blocca ancora l'unico thread, anche prima del token).
- modules/voice/server.py:119 — `_PAROLA_FORTE` con jarvis e `(...)*`.
  - Falsi positivi: nessuno nuovo. Non scattano «Jarvis, fortemente», «Jarvis parla più forte», «Jarvisforte x», «Gas e forte x», «ciao forte x», «Gas gasolio forte».
  - «Jarvis forte-mente ok» va al forte con richiesta «mente ok». Lo faceva già «Gas forte-mente» col vecchio regex. Sbaglia verso il forte, cioè costa budget ma non manda dati ai gratuiti.
  - Il ramo «uso» è invariato: «jarvis jarvis forte» e «Hey Jarvis, forte.» danno ("uso", "").
  - Backtracking: nessun problema, 20000 caratteri patologici in circa 2 ms.
  - Il cambio vale anche per i vocali di Telegram, che usano `cervello_voce` (modules/telegram/bot.py:969). È coerente con lo scopo.
- modules/voice/server.py:698 — 413 sul corpo. Esito: ok.
  - Il controllo viene DOPO `_autorizza` (chi non ha il token riceve 401 e il corpo non viene letto) e PRIMA di `rfile.read`.
  - Il corpo non letto non sporca la richiesta successiva: il server risponde in HTTP/1.0 e chiude la connessione dopo ogni risposta.
- modules/voice/server.py:747 — JSON di forma sbagliata dà 400. Esito: ok. `{"prompt": 0}` o `false` finiscono in «mancante o vuoto», sempre 400.
- modules/voice/server.py:754 — 413 sul prompt oltre 20000 caratteri. Esito: ok.
- modules/voice/server.py:1459 — porta aperta prima del kernel. Esito: ok. Su OSError esce con return 1 e un messaggio chiaro; su `BaseException` chiude il server e rilancia l'eccezione.
- modules/voice/stt.py:256 e modules/voice/tts.py:122 — HTTPException diventa OSError. Esito: ok. Il server (`_do_stt`) e bot.py:1084 (`except Exception`) prendono già OSError.
  - Riserva: le altre funzioni di tts restano scoperte, cioè l'elenco voci (modules/voice/tts.py:158), la libreria (modules/voice/tts.py:216) e l'aggiunta di una voce (modules/voice/tts.py:270). Il server prende solo ElevenLabsTTSError e OSError, quindi un IncompleteRead esce dal gestore: il server non crasha, ma la richiesta resta senza risposta e lo stack finisce su stderr, non in gas_debug.log. Nell'aggiunta di una voce il contatore orario è già stato incrementato e l'esito resta incerto senza nessun messaggio.
- clients/voice/browser_server.py:362 — se manca GAS_VOICE_URL, il proxy usa GAS_VOICE_PORT (stesso parsing di clients/voice/ascolto.py:246). Esito: riserva, nessun test copre questo ripiego (mutante sopravvissuto).
- clients/voice/browser_server.py:70 (`_valore_dotenv`) e il nuovo `_load_dotenv` — confrontati con `_carica_dotenv` di gas.py: regole equivalenti, vince la prima riga, una riga con virgolette non chiuse lascia valere quella dopo. Esito: ok. Differenza già presente prima: il proxy non rispetta GAS_NO_DOTENV.

**Prova dei mutanti** (12, sulla copia dell'index): 11 uccisi.
- Uccisi: regex senza jarvis, regex con `?` al posto di `*`, 413 sul corpo tolto, `>` cambiato in `>=` sul prompt, isinstance del prompt tolto, `server_close` tolto, `return 1` della porta occupata tolto, B3 di stt e di tts, `return None` delle virgolette non chiuse, rimozione di `export`.
- Sopravvissuto: il ripiego GAS_VOICE_PORT del browser (nessun test lo copre).

**Test**: suite voice server, stt e tts con `-k "not browser"`: 310 passed. Test con «browser» nel nome: 28 passed. Attenzione: `-k "not browser"` esclude anche i test nuovi b4 del dotenv, che hanno «browser» nel nome. Li ho fatti girare a parte e passano.

**Riserve** (da segnare in stato_progetto.md)
- R-752-1 (BASSA): il timeout di 60 s vale anche su sendall come durata totale. Misurare sul Mac lo stream NDJSON con risposte lunghe. Lo slowloris non è coperto.
- R-752-2 (BASSA): la conversione B3 manca nell'elenco voci, nella libreria e nell'aggiunta di una voce (modules/voice/tts.py:158/216/270).
- R-752-3 (BASSA): manca un test per il ripiego GAS_VOICE_PORT del proxy, ad esempio GAS_VOICE_PORT=9001 deve dare `BrowserProxyHandler.voice_port == 9001`.
- Cosmetica: un TimeoutError durante `rfile.read` finisce come traceback su stderr invece che in gas_debug.log.

**Cosa NON ho verificato**
- Il comportamento reale sul Mac (dimensione dei buffer di loopback, durata delle frasi, telefono in rete privata): non riproducibile qui.
- Le suite di ascolto, sottofondo, telegram_voce, contesto e prova_voci non le ho rieseguite: il diff non le tocca. Il totale dichiarato di 813 non l'ho verificato.

**Memoria**: aggiunti in coda a /home/user/Gas-audit/.claude/agents/memoria_revisore.md la riga `#752-M2` e due lezioni (sendall col timeout totale; `-k "not browser"` che esclude test nuovi). File messo in staging con `git -C /home/user/Gas-audit add`. Nessun commit fatto, come richiesto.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato. Test nuovi: `test_audit_b1_timeout_del_socket`, `test_audit_b5_json_di_forma_sbagliata_400` (6 casi), `test_audit_tetti_413`, `test_audit_porta_occupata_messaggio_chiaro`, `test_audit_b4_dotenv_del_browser_come_gas` (7 casi), `test_audit_b4_dotenv_non_sovrascrive`, `test_audit_proxy_segue_gas_voice_port` (3 casi), casi «Hey Jarvis, forte» in `test_v1_parola_forte_parlata` (server); `test_audit_b3_risposta_rotta_diventa_oserror` (stt e tts), `test_audit_b3_altre_funzioni_tts` (tts). `test_r8_avvio_con_rete_privata_dichiarata_parte` adattato (porta prima del kernel).
- Dopo il merge di main (d1b5628): `python -m pytest -q tests/test_unit_voice_server.py tests/test_unit_voice_stt.py tests/test_unit_voice_tts.py tests/test_unit_voce_ascolto.py tests/test_unit_telegram_voce.py tests/test_unit_sottofondo.py -k "audit or not browser"`:

```
808 passed, 25 deselected in 80.53s (0:01:20)
```

- Revisore #759-M2: voice_server + stt + tts con i test browser: 347 passed.

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- ea3033b: handoff-check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE); unit-suite non letta a fine run prima del merge di main.
- 1c53cf9, d1b5628 e 1af440e: nessuna run propria letta.
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-752-1 BASSA: il timeout di 60 s vale su tutto il `sendall`: misurare sul Mac uno stream NDJSON lungo; lo slowloris (1 byte ogni 59 s) non è coperto.
- R-752-2 e R-752-3 BASSE: CHIUSE (1c53cf9, review #755-M2).
- Nota #755: in `add_shared_voice` una risposta rotta dopo l'aggiunta riuscita dice «errore di rete» invece di «esito incerto» (BASSA).
- Cosmetica #752: un TimeoutError durante `rfile.read` finisce su stderr invece che in gas_debug.log.
- Bot #367 su ea3033b V-1 BASSA: GAS_VOICE_PORT fuori 0-65535 (es. 99999) → OverflowError/ValueError con traceback (server e proxy), non una regressione.
- Bot #367 V-2 BASSA: il test del timeout prova solo intestazioni ferme, non un corpo dichiarato che non arriva; soglia di 4,5 s stretta per un runner lento.
- Verifica esterna #367 V-3/V-4: /voci/prova e /voci/aggiungi hanno già un tetto loro (4096 byte); GAS_VOICE_PORT filtrato a sole cifre senza avviso (COSMETICA).
- Sospetti di M1 non toccati: «forte» durante «Sì, signore?», blocco per IP condiviso su 127.0.0.1, connessione ElevenLabs riusata.
