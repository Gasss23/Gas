# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — voce più veloce: connessione verso ElevenLabs riusata (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. («mergia tutte» dell'operatore, via M1, 11 nov mattina: la chat mergia la #372 con CI e bot verdi senza ALTA/MEDIA.) Merge della PR #372 (https://github.com/Gasss23/Gas/pull/372): la verifica esterna #372 dà APPROVATO CON RISERVE (V-1 e V-2 BASSE, V-3 COSMETICA), quindi la PR resta pronta per il «mergia» dell'operatore; con verdetto del bot APPROVATO pulito e CI verde la mergia la chat (regola notturna di M1).

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi**: `FATTA` (commit di codice nel §3).
- **R-765-1-M2 MEDIA (doppio addebito), R-765-2-M2 MEDIA (connessione ferma), R-765-3-M2 BASSA (test)**: `FATTA` — chiuse prima del commit, review #768-M2.
- **V-1 del bot #372 (nuovo tentativo dopo l'invio = possibile doppio addebito)**: `FATTA` — il nuovo tentativo parte solo durante l'invio (review #770-M2).
- **R-770-1-M2 BASSA (connessione chiusa dal server mentre era ferma) e R-770-2-M2 COSMETICA**: `FATTA` — `_conn_caduta` (select a 0 s) prima del riuso (review #771-M2).
- **V-1 della verifica esterna #372 (test della soglia agganciato alla costante)**: `FATTA` — valori fissi 19/21 s (review #772-M2).
- **Merge di origin/main (#370, #369)**: `FATTA` — review #776-M2.
- **Merge di origin/main (#371) dopo il «mergia» dell'operatore**: `FATTA` (725eaa7, review #784-M2).
- **Misura del guadagno sul Mac**: `DEFERITA` — serve la rete vera.
- **Latenza del cervello (prima frase 5-9 s)**: `DEFERITA` — fetta separata (streaming della prima frase da `claude -p`).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 ++++++++++
 modules/voice/tts.py               | 126 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           | n/d
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          | n/d
 reports/ultimo_report.md           | n/d
 tests/test_unit_voice_tts.py       | 217 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: confronto con origin/main (bb424f0, dopo il merge). Regola «n/d» — i conteggi dei report riscritti in questo commit di fine-task non sono misurabili mentre li si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
725eaa7 Merge origin/main (#371) nella #372 — review #784-M2 APPROVATO (chat M2)
2edadc7 docs(fine-task): #372 dopo V-1 bot, R-770-1, V-1 ve e merge di main — review #770-#776-M2 (chat M2)
cc70808 Merge origin/main (#370, #369) nella #372 — review #776-M2 APPROVATO (chat M2)
39eaf0a test(voce): soglia di inattività del keep-alive a valori fissi 19/21 s (V-1 ve #372)
e7dadc1 fix(voce): keep-alive TTS, connessione chiusa dal server scartata prima dell'invio (R-770-1-M2)
2479a53 fix(voce): keep-alive TTS, nuovo tentativo solo durante l'invio (V-1 bot #372)
36095b4 docs(fine-task): voce — connessione ElevenLabs riusata, PR #372 (chat M2)
4f031dc perf(voce): connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi (una per thread, buttata dopo 20 s ferma, niente doppio addebito) — review #765-M2, #768-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #784-M2 (merge di origin/main con la #371) — verdetto integrale

## VERDETTO: APPROVATO

Il merge di main (con la #371) nella PR #372 è pulito. Il codice della #372 non cambia e il codice di main entra identico. 506 test passati, rieseguiti da me.

**Cosa ho controllato nel diff**
- `modules/voice/tts.py:106` — `_conn_caduta` e la soglia `_KEEPALIVE_INATTIVA_MAX_S` (`modules/voice/tts.py:88`, usata a `:133`) sono identiche a HEAD (diff 0 sul file). Rischio esaminato: che il merge alteri il keep-alive. Esito: ok.
- `tests/test_unit_voice_tts.py:520` — `test_keepalive_riusa_la_connessione` e gli altri test del keep-alive sono identici a HEAD e passano. Rischio esaminato: test persi o modificati nel merge. Esito: ok.
- `clients/voice/ascolto.py:58` — gli import dell'ascolto sono solo della libreria standard e nel file non c'è nessun riferimento a tts o `synthesize`. Lo stesso vale per `scripts/voce/diagnosi_ascolto.py`. Rischio esaminato: un'interazione tra l'ascolto della #371 e la sintesi vocale. Esito: nessuna interazione.
- `reports/stato_progetto.md:626` — c'è la voce della #372. Rispetto a MERGE_HEAD non manca nessuna riga. Rispetto a HEAD manca una sola riga: la voce della #368, sostituita dalla versione di main che la segna «MERGIATA». Esito: ok.

**Controlli meccanici**
- Nessun file in conflitto, nessun marcatore di conflitto, `git diff --cached --check` pulito.
- Il codice preso da main è identico a MERGE_HEAD (diff 0): `clients/voice/ascolto.py`, `scripts/voce/*`, `tests/test_unit_voce_ascolto.py`, `reports/proposta_verifica_parlante.md`.
- `.claude/agents/memoria_revisore.md`: 0 righe tolte rispetto a MERGE_HEAD. I numeri doppi (#757-M1, #753-M1, #746/#747 chat M3, #614-M2) c'erano già prima, nessuno è nuovo.
- Test: tts, stt e ascolto insieme 506 passed in 58 s.

**Non verificato**
- Il comportamento reale sul Mac (latenza di ElevenLabs con la connessione riusata, taratura dell'ascolto): non si può riprodurre qui.
- La CI della PR dopo il merge: il commit non esiste ancora.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas-tts/.claude/agents/memoria_revisore.md` la riga `#784-M2 — 2026-11-11 — APPROVATO — …` (nessuna lezione nuova) e l'ho messa in staging.
- Il numero #784 l'hai dato tu: nella memoria fusa l'ultimo numero è #776-M2.
- Non ho lanciato `scripts/commit_memoria_revisore.sh`: c'è un merge in corso e hai chiesto la memoria in staging. Entra nel commit di merge.

### Review #776-M2 (merge di origin/main) — verdetto integrale

## VERDETTO: APPROVATO

Review #776-M2: merge di origin/main e3eb542 (#370 e #369) nella PR #372 (keep-alive ElevenLabs). Il merge è in staging in /home/user/Gas-tts, HEAD 39eaf0a, MERGE_HEAD e3eb542.

**Cosa ho controllato**
- **Merge pulito:** `git ls-files -u` è vuoto, non ci sono marcatori di conflitto né in memoria né in reports/, e `git diff --cached --check HEAD` è pulito.
- **Memoria e stato_progetto, nessuna riga persa:**
  - Rispetto a HEAD il diff contiene solo aggiunte: 11 righe in memoria (#753-M1, #757-M1, #761–#765) e 2 voci in stato_progetto (#366 decisioni M1, #369 allucinazioni). Nessuna riga tolta.
  - Rispetto a MERGE_HEAD (`git diff MERGE_HEAD`) non manca nessuna riga, né in memoria né in stato_progetto.
  - Non ci sono doppioni nuovi: l'unico numero ripetuto in più rispetto a HEAD è #753-M1, che è doppio già in main (1° e 2° giro).

**Citazioni**
- `modules/voice/tts.py:121` — `_post_riusando`, il keep-alive con un solo nuovo tentativo, fatto solo durante l'invio. Rischio esaminato: che il merge alteri il file o che il codice di main ci interagisca. Il file non è nel diff del merge, main non lo ha toccato dal merge-base e il codice nuovo di main non contiene nessun riferimento al TTS. Esito: ok.
- `modules/voice/tts.py:106` — `_conn_caduta`, il controllo che la connessione non sia già chiusa prima di riusarla. Non toccato dal merge. Esito: ok.
- `tests/test_unit_voice_tts.py:610` — `test_keepalive_connessione_ferma_da_troppo_si_butta`, insieme agli altri test keep-alive (righe 520–623). Restano intatti. tts+stt: 180 passed, rieseguiti da me dopo il merge. Esito: ok.
- Contesto: `modules/telegram/bot.py:1091` — importa `synthesize_speech`. La #370 cambia bot.py solo in un commento (riga «§8 … versione leggera»), quindi la chiamata al TTS resta invariata. Esito: ok.
- Contesto: `modules/voice/server.py:95` — importa il TTS. Il diff di main in server.py tocca solo il ramo della trascrizione (`TrascrizioneAllucinata`, vuota → silenzio) e non aggiunge chiamate di sintesi. Non c'è interazione con il keep-alive. Esito: ok.

**Rischi esclusi (non verificati)**
- La suite kernel (1134 PASS, 1 FAIL T31g per fastembed assente) non l'ho rieseguita: prendo per buono il numero del chiamante. Nel merge gas.py coincide con main, già approvato nelle review #764/#765-M1coord.
- Il comportamento del keep-alive verso ElevenLabs reale non è verificato: non si riproduce in dev.

**Memoria**
- Ho aggiunto la riga `#776-M2 — 2026-11-11 — APPROVATO — …` in coda a /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging (`git add`). MERGE_HEAD è ancora presente.
- `scripts/commit_memoria_revisore.sh` non l'ho eseguito: il primo tentativo è stato bloccato dall'hook review_gate perché `.review_ok` non corrisponde al diff in staging. In più, durante un merge `git commit -o` non può fare commit parziali. Il file entra quindi con il commit del merge.
- Ora il diff in staging è cambiato (memoria aggiornata): bisogna rigenerare il marcatore con `bash scripts/segna_review_ok.sh` prima di committare.

Nessuna lezione nuova.

### Review #772-M2 (V-1 verifica esterna #372) — verdetto integrale

## VERDETTO: APPROVATO

Review #772-M2 (chat M2): diff in staging di /home/user/Gas-tts, PR #372. Il diff tocca solo tests/test_unit_voice_tts.py (2 righe aggiunte, 2 tolte).

Elementi del diff che ho esaminato:
- `tests/test_unit_voice_tts.py:615`: l'avanzamento di 5 s diventa `ora[0] += 19`. Rischio esaminato: con 19 s si deve ancora riusare la connessione, perché 19 è sotto la soglia di 20 s (`modules/voice/tts.py:88`) e il controllo usa il `>` stretto. Prima, con 5 s, una soglia abbassata a 15 non veniva scoperta. Esito: ok. Il mutante «soglia 15» ora è preso (1 failed).
- `tests/test_unit_voice_tts.py:618`: `ora[0] += _KEEPALIVE_INATTIVA_MAX_S + 1` diventa `ora[0] += 21`. Rischio esaminato: il test non deve più ricavare il valore atteso dalla costante che sta controllando. «usata» viene aggiornato dopo la lettura della seconda risposta, quindi l'inattività misurata è 21 s ed è maggiore di 20: si apre una connessione nuova. Esito: ok. I mutanti «soglia 1e9» e «soglia 25» sono presi (1 failed ciascuno).
- Contesto (file non toccato): `modules/voice/tts.py:133`. Il confronto `time.monotonic() - usata > _KEEPALIVE_INATTIVA_MAX_S` è coerente con i valori fissi 19 e 21.

Verifiche eseguite: la suite del file dà 40 passed. Ho provato tre mutanti della costante (1e9, 25, 15), uno alla volta, ripristinando ogni volta il file originale: tutti presi. modules/voice/tts.py è rimasto intatto (in `git status` compaiono solo il test e la memoria).

Rischio che ho escluso:
- Il confine esatto di 20 s non è coperto: la differenza tra `>` e `>=` non viene scoperta. Lo considero accettabile e non apro una riserva, perché il contratto è «circa 20 s» e la finestra 19/21 basta a bloccare la soglia.
- Il mutante «usata non aggiornato» non l'ho riprovato. Con questi valori il test da solo non lo distingue (da 1000 a 1040 sono comunque più di 20 s). La review #768 lo dava preso, ma non ho controllato da quale test.
- Nessun guardrail toccato: il cap di 10 iterazioni, `_get_window` e l'assenza di slicing non sono interessati da questo diff, che riguarda solo un test.

Memoria: ho aggiunto la riga `#772-M2` in coda a /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging in /home/user/Gas-tts (`M  .claude/agents/memoria_revisore.md`). Nessuna lezione nuova. Non ho committato, come da tua richiesta di sola messa in staging.

File rilevanti:
- /home/user/Gas-tts/tests/test_unit_voice_tts.py
- /home/user/Gas-tts/modules/voice/tts.py
- /home/user/Gas-tts/.claude/agents/memoria_revisore.md

### Review #771-M2 (R-770-1/R-770-2) — verdetto integrale

## VERDETTO: APPROVATO

Re-review #771-M2 sul diff in staging in /home/user/Gas-tts (PR #372, keep-alive ElevenLabs). Ho letto CLAUDE.md (sez. 5, 8, 9), lo stato del progetto (parte Voce) e la mia memoria (#765, #768, #770-M2). Le due riserve di #770-M2 sono chiuse.

**Cosa ho controllato nel diff**
1. `modules/voice/tts.py:106`: nuova funzione `_conn_caduta`. Se il socket non c'è risponde False, e va bene perché la request la aprirà. Fa un select a 0 s. Rischio: un errore del select che risale e fa crashare. Esito ok: OSError, ValueError e TypeError vengono intercettati.
2. `modules/voice/tts.py:116`: un errore del controllo conta come «caduta». Rischio: un socket chiuso o con fileno -1 che fa esplodere select. Esito ok: si chiude e se ne apre una nuova, in linea con il §9.
3. `modules/voice/tts.py:136`: il controllo viene fatto prima di `riusata = conn is not None`. Rischio: che la riconnessione consumi il nuovo tentativo. Esito ok: la connessione nuova ha `riusata=False` e un nuovo tentativo resta possibile solo per una connessione davvero riusata che cade durante l'invio. Al secondo giro del ciclo conn è None, quindi il controllo non viene rifatto.
4. `modules/voice/tts.py:162`: `getresponse()` ora ha un solo ramo `except (HTTPException, OSError)`. Rischio: perdere la gestione di HTTPException. Esito ok: il ramo tolto non veniva mai eseguito, perché il precedente catturava già HTTPException. La docstring corrisponde al codice.
5. `tests/test_unit_voice_tts.py:662`: socketpair con il lato «server» chiuso. Verifica che si crei una connessione nuova, che la vecchia sia chiusa con 1 richiesta e la nuova abbia 1 richiesta (nessun nuovo tentativo consumato). Esito ok. Ho provato il mutante «`_conn_caduta` restituisce sempre False»: questo test lo cattura (1 failed, 39 passed). Ho poi ripristinato il file e `git diff` sulle modifiche non in staging è vuoto.
6. `tests/test_unit_voice_tts.py:680`: socket vivo, la connessione viene riusata. Esito ok. Il monkeypatch in `tests/test_unit_voice_tts.py:626` è giustificato: con un MagicMock, select solleverebbe TypeError, che conterebbe come caduta e falserebbe il test del timeout.

Risultato: tts **40 passed**, rilanciati da me.

**Falsi positivi da TLS (la tua domanda)**
Ho fatto una prova reale in locale: server Python TLS 1.3 con `num_tickets=4` e tre POST keep-alive. Dopo `resp.read()` il socket non risulta mai leggibile e `pending()` è 0. I ticket arrivano subito dopo l'handshake, prima della risposta HTTP, e la lettura della risposta li consuma. Resterebbe un falso positivo solo se un server mandasse un ticket o altri dati dopo la risposta. In quel caso il costo è un handshake in più e nessun errore né doppio addebito, quindi è accettabile.
Il punto cieco è l'opposto, un falso negativo: dati già nel buffer SSL (`sock.pending()>0`), che select non vede. Nel caso normale qui non succede, perché la risposta viene letta tutta, e rientra nel rischio residuo dichiarato in docstring. Se vuoi una difesa in più costa poco: `or sock.pending()` per gli SSLSocket. Non è una riserva.

**Cosa non ho verificato**
- Il comportamento con l'endpoint reale ElevenLabs e la sua CDN (quando manda i ticket, chiusure con o senza close_notify): non si riproduce in dev senza rete e senza la chiave. La prova copre solo un server OpenSSL locale.
- Il tempo che il select a 0 s aggiunge sulla latenza della voce: non l'ho misurato. È trascurabile per costruzione (una chiamata di sistema senza attesa).

**Memoria**
Ho aggiunto la riga `#771-M2` e una lezione su come provare i falsi positivi TLS in /home/user/Gas-tts/.claude/agents/memoria_revisore.md. Il file è in staging insieme a tts.py e al test. Non ho lanciato `commit_memoria_revisore.sh`, perché mi hai chiesto solo lo staging.

File: /home/user/Gas-tts/modules/voice/tts.py, /home/user/Gas-tts/tests/test_unit_voice_tts.py, /home/user/Gas-tts/.claude/agents/memoria_revisore.md

### Review #770-M2 (V-1 bot #372) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #770-M2, seguito della PR #372, sul diff STAGED in /home/user/Gas-tts. Il finding V-1 del bot è chiuso: ora un nuovo tentativo parte solo se la connessione salta mentre la richiesta viene inviata. Ho controllato solo il delta e il mutante richiesto.

**Cosa ho esaminato nel diff**
- `modules/voice/tts.py:126`: solo `conn.request()` resta nel try che può ripetere. Il nuovo tentativo scatta solo su una connessione riusata, al primo tentativo (`modules/voice/tts.py:131`). Rischio esaminato: un secondo POST dopo che ElevenLabs ha già ricevuto la richiesta. **Esito: ok.**
- `modules/voice/tts.py:141`: `conn.getresponse()` ha un try suo: chiude la connessione e alza OSError, senza nuovo tentativo. Ho provato il mutante che rimette `getresponse()` nel try che ripete: lo prende `test_keepalive_errore_dopo_l_invio_non_riprova` (`tests/test_unit_voice_tts.py:646`), che verifica 2 richieste, 1 connessione e connessione chiusa. **Esito: ok.**
- Test: `tests/test_unit_voice_tts.py` dà 38 passed.

**Riserve**
- **R-770-1-M2 (BASSA): il nuovo tentativo ormai non scatta quasi mai.** Quando ElevenLabs chiude una connessione inattiva, di solito l'invio riesce lo stesso (finisce nel buffer) e l'errore `RemoteDisconnected` arriva solo in `getresponse()`. Quindi nel caso tipico ora si ha un errore e la frase persa, e il nuovo tentativo scatta quasi solo su `BrokenPipe`. Il limite di 20 s di inattività riduce il problema, ma solo se ElevenLabs tiene aperte le connessioni più di 20 s, cosa non nota. Rimedio senza rischio di doppio addebito: prima di inviare su una connessione riusata, controllare che il socket non sia già leggibile (`select` a 0 s; se è leggibile, il server l'ha chiusa) e in quel caso aprirne una nuova. È quello che fa `is_connection_dropped` di urllib3.
- **R-770-2-M2 (COSMETICA):**
  - il ramo `except http.client.HTTPException` a `modules/voice/tts.py:145` non viene mai eseguito, perché la riga sopra cattura già `(HTTPException, OSError)`;
  - nella docstring, `modules/voice/tts.py:110` è una riga troppo lunga.

**Cosa non ho verificato**
- Il tempo reale dopo cui ElevenLabs chiude le connessioni inattive, e quindi quanto spesso capiti R-770-1-M2. Serve una prova dal vivo con chiave e rete vere, che qui non ho.
- Non ho rilanciato le suite voice_server e telegram: il delta tocca solo tts.py e il suo test.

**Memoria del revisore**
- Ho aggiunto la riga #770-M2 e una lezione nuova in /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git -C /home/user/Gas-tts add`. Nessun commit.

### Review #768-M2 (seguito di #765-M2) — verdetto integrale

VERDETTO: APPROVATO

Review #768-M2, seguito di #765-M2, sul diff STAGED in /home/user/Gas-tts: tutte e tre le riserve sono chiuse. Ho controllato solo il delta, i mutanti e la sonda di #765.

**Cosa ho esaminato nel diff**
- `modules/voice/tts.py:139`: `resp.read()` ora sta in un try separato, dopo quello che può riprovare. Un errore durante la lettura chiude la connessione e risale come OSError (`:140-142`). Rischio esaminato: un secondo POST dopo un 200, cioè il doppio addebito di R-765-1-M2. Ho rilanciato la sonda di #765 (connessione che salta a metà dell'audio su una connessione riusata): ora dà `OSError: risposta rotta (ConnectionResetError)` senza nuova richiesta, mentre prima le richieste erano 3 per 2 frasi. Il mutante «read di nuovo nel try che riprova» viene preso dai test (1 failed). **Esito: ok, R-765-1-M2 chiusa.**
- `modules/voice/tts.py:113`: una connessione inattiva da più di `_KEEPALIVE_INATTIVA_MAX_S` = 20 s (`:87`) viene chiusa e se ne apre una nuova, prima di decidere se la connessione è «riusata». Rischio esaminato: una connessione persa in silenzio che fa aspettare tutto il timeout (R-765-2-M2). Il tempo di ultimo uso (`usata`) si aggiorna solo a risposta letta e senza «Connection: close» (`:149`), e una connessione esiste solo dopo un successo, quindi il valore di partenza 0.0 non entra mai in gioco. I mutanti «soglia tolta», «soglia enorme» e «usata non aggiornato» vengono presi dai test (1, 1 e 6 failed). **Esito: ok, R-765-2-M2 chiusa.**
- `modules/voice/tts.py:121-123`: il timeout viene aggiornato sulla connessione e sul socket riusato. Ora i mutanti «settimeout tolto» e «conn.timeout tolto» vengono presi dai test (1 failed ciascuno). **Esito: ok.**
- `modules/voice/tts.py:135-137`: un'eccezione qualsiasi chiude la connessione. Il mutante che toglie il ramo `except BaseException` viene preso dai test (1 failed). **Esito: ok, R-765-3-M2 chiusa.**

**Test**
- `tests/test_unit_voice_tts.py`: 37 passed.
- Mutanti: tutti uccisi (7 sul codice nuovo più la variante «read lasciato anche fuori»).

**Cosa non ho verificato**
- Se 20 s bastano a coprire le pause fra le frasi di una risposta lunga sul server voce, e quanto tiene aperta una connessione inattiva ElevenLabs. Serve una prova dal vivo con chiave e rete vere, che qui non ho.
- Non ho rilanciato le suite voice_server, telegram e contesto: il delta tocca solo tts.py e il suo test.

**Memoria del revisore**
- Ho aggiunto la riga #768-M2, senza lezioni nuove, in /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git -C /home/user/Gas-tts add`. Nessun commit.

### Review #765-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #765-M2 sul diff STAGED in /home/user/Gas-tts, branch perf/voce-tts-keepalive-m2: la connessione HTTPS verso ElevenLabs resta aperta e si riusa, una per thread.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la memoria del revisore e le voci di stato_progetto che riguardano la voce. La modifica non tocca la storia dei messaggi né `_get_window`, non simula i tool e non indebolisce né il tetto di 10 giri né quello di 8k caratteri. Nessuna eccezione arriva a far crashare il programma: i chiamanti gestiscono già OSError ed ElevenLabsTTSError.

**Cosa ho esaminato nel diff**
- `modules/voice/tts.py:75`: `threading.local()` tiene una connessione per thread. Rischio esaminato: stato o chiave condivisi fra thread. La chiave viaggia nell'header di ogni richiesta e non viene salvata. Il server voce gira su un solo thread (`HTTPServer` senza ThreadingMixIn, `modules/voice/server.py:1517`). Il bot Telegram sintetizza da un esecutore suo (`modules/telegram/bot.py:1017`). Il mutante «connessione globale invece che per thread» viene preso dai test. **Esito: ok.**
- `modules/voice/tts.py:117`: nuovo tentativo solo se la connessione era riusata ed è il primo tentativo. Il mutante «riprova anche su una connessione nuova» viene preso dai test. **Esito: ok.**
- `modules/voice/tts.py:114`: `resp.read()` sta dentro lo stesso try che fa ripartire il tentativo, e `ConnectionResetError` è nella lista degli errori «connessione chiusa». **Esito: riserva R-765-1-M2 (MEDIA), possibile doppio addebito.** Una sonda (connessione finta, nessuna chiamata reale) lo conferma: se la connessione salta a metà dell'audio dopo che ElevenLabs ha già risposto 200, parte un secondo POST, che ElevenLabs farebbe pagare di nuovo. Due frasi hanno prodotto 3 richieste. Correzione: riprovare solo se l'errore arriva prima dello status, cioè durante `request`/`getresponse`. Un errore durante `read()` deve risalire come OSError.
- `modules/voice/tts.py:78`: l'elenco degli errori che fanno riprovare non comprende `TimeoutError`, ed è giusto, perché riprovare raddoppierebbe l'attesa. Però il bot Telegram fa una sola sintesi per risposta, a minuti di distanza, quindi riusa sempre una connessione rimasta ferma a lungo. Se il router, il cambio di Wi-Fi o la sospensione del Mac l'hanno persa senza avvisare, la richiesta aspetta tutto il timeout (`VOCE_TIMEOUT_S`) e fallisce, mentre prima funzionava. La stessa cosa vale per la conferma vocale col suo timeout di 5 s (`modules/voice/server.py:232`). **Esito: riserva R-765-2-M2 (MEDIA).** Correzione: buttare la connessione se è inutilizzata da più di circa 15-30 s. Il guadagno di velocità, che sta fra le frasi di una stessa risposta, resta intatto.
- `modules/voice/tts.py:126`: se il server manda «Connection: close» la connessione si chiude. Il mutante viene preso da `tests/test_unit_voice_tts.py:549`. **Esito: ok.**
- `modules/voice/tts.py:167`: il riuso vale solo senza `_conn_factory` e si spegne con `GAS_TTS_KEEPALIVE=0`. Il percorso vecchio è invariato e lo copre `tests/test_unit_voice_tts.py:559`. **Esito: ok.**
- `modules/voice/tts.py:110`: il timeout viene aggiornato anche sul socket riusato. Il codice è corretto, ma sopravvivono i mutanti «settimeout tolto», «conn.timeout tolto» ed «except BaseException non chiude la connessione», perché nella connessione finta dei test `sock` è sempre None. **Esito: riserva R-765-3-M2 (BASSA), mutanti non coperti.**

**Altre note**
- Socket lasciati aperti: quando un thread muore, la sua connessione viene chiusa dal garbage collector. Entrambi i chiamanti hanno thread che durano, quindi non c'è un accumulo.
- Test: `tests/test_unit_voice_tts.py` dà 33 passed. Mutanti: 3 presi, 3 sopravvissuti (elencati sopra).

**Cosa non ho verificato**
- Il comportamento reale di ElevenLabs: quanto tiene aperta una connessione inattiva e se manda «Connection: close». Serve una chiave e una rete vera, che qui non ho.
- La perdita silenziosa della connessione dopo la sospensione del Mac o un cambio di Wi-Fi. Non si riproduce in questo ambiente; R-765-2-M2 è un ragionamento sul codice, non un caso osservato.
- Non ho rilanciato le suite voice_server, stt, prova_voci, telegram_voce e contesto (428 passed secondo chi mi ha invocato), perché il diff tocca solo tts.py e il suo test.

**Memoria del revisore**
- Ho aggiunto la riga #765-M2 e una lezione nuova in /home/user/Gas-tts/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git add`. Nessun commit, come richiesto.
- La sonda è in /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda.py.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato dalla PR (dopo il merge coincide con main). Test nuovi in `tests/test_unit_voice_tts.py`: 14.
- `python -m pytest -q tests/test_unit_voice_tts.py tests/test_unit_voice_stt.py` dopo il merge: 180 passed (tts da solo 40 passed).
- `python tests/test_unit_kernel.py` dopo il merge: 1134 PASS, 1 FAIL (T31g, fastembed assente in questo ambiente: lo stesso FAIL c'è su main).
- Prima del merge: `tests/test_unit_voice_tts.py` + `tests/test_unit_voice_server.py` 250 passed.

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- Head precedente 36095b4: `unit-suite`, `handoff-check` e `verifica-bot` success (letti dalla verifica esterna #372 via API).
- Nuovi commit (2479a53…cc70808 e fine-task): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-765-1-M2 MEDIA, R-765-2-M2 MEDIA, R-765-3-M2 BASSA: CHIUSE (review #768-M2).
- V-1 bot #372: CHIUSA (review #770-M2). R-770-1-M2 BASSA, R-770-2-M2 COSMETICA: CHIUSE (review #771-M2).
- Verifica esterna #372: V-1 BASSA CHIUSA (review #772-M2); V-2 BASSA (nuovo tentativo dopo l'invio) CHIUSA dalla stessa correzione della V-1 del bot; V-3 COSMETICA (stato CI) superata da questo §6.
- Non verificato: guadagno reale e durata delle connessioni inattive di ElevenLabs (prova sul Mac).
