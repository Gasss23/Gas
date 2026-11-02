# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Voce V7a: misura dei tempi (chat M2, coordinata da M1) — aggiornato dopo bot e verifica esterna su 33a0346

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #322 (https://github.com/Gasss23/Gas/pull/322). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5123668093","url":"https://github.com/Gasss23/Gas/pull/322"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.
2. Sul Mac, dopo il merge: leggere la riga «tempi» della pagina e le righe `gas.voce.tempi` di `gas_debug.log`.

---

## §1 SCOPE & ESITO FETTE

- **V7a — tempi di trascrizione, cervello e voce**: `FATTA` (review #614–#616-M2).
- **Merge di main (PR #318, #321)**: `FATTA` (review #643-M2).
- **Bot su 33a0346**: V-1 (tempi a schermo anche sui guasti) e V-2 (caricamento dell'audio contato come «rete», `_t0` dopo la lettura del corpo): `FATTE`, review #644-M2 CON RISERVE (R-644-1-M2: tempi vecchi dopo un errore di rete, chiusa) → #645-M2 APPROVATO. V-3 bot (X-Gas-Tempi non letta da nessun client: serve ai client futuri) COSMETICA, nessun fix.
- **Verifica esterna su 33a0346** (https://github.com/Gasss23/Gas/pull/322#issuecomment-6582445935): V-1 MEDIA (PR in conflitto con main dopo la #320) `FATTA` col merge di main (solo documenti e memoria); V-2 (§6 senza run) aggiornata qui; V-3/V-4 basse, già dichiarate.
- **V7b, V8, V9**: `DEFERITE` — una PR alla volta, dopo il merge della precedente.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 ++++++
 clients/voice/browser_client.html  |  31 +++++++++++++++++++++++---
 modules/voice/server.py            |  51 +++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  13 ++++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  23 ++++++++------------
 tests/test_unit_voice_server.py    |  29 +++++++++++++++++++++----
 tests/test_unit_voice_stt.py       | 118 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
60499a4 Merge remote-tracking branch 'origin/main' into feat/voce-v7-m2
685c9bb fix(voce): tempi a schermo anche sui guasti, caricamento dell'audio contato come rete (V-1/V-2 bot #322 su 33a0346; review #644/#645-M2)
d58208d chore(revisore): memoria review #645 — APPROVATO
34ff97f chore(revisore): memoria review #644 — APPROVATO CON RISERVE
33a0346 docs(voce-v7a): numero della PR #322 nei report
f3a3cc4 docs(voce-v7a): report di fine task (review #614–#616-M2, merge di main #643-M2)
7ced8a2 Merge origin/main (PR #318 V6, #321) in feat/voce-v7-m2 (review #643-M2)
3156c6a chore(revisore): memoria review #616 — APPROVATO
190d3fc feat(voce): V7a — tempi di trascrizione, cervello e voce nella risposta, nel log e nella pagina (chat M2)
c7ebecb chore(revisore): memoria review #615 — APPROVATO CON RISERVE
b48c9a5 chore(revisore): memoria review #614 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della fetta (190d3fc). Tre passaggi del revisore sullo stesso diff staged; verdetti integrali.

Review #614-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #614-M2: fetta V7a, misura dei tempi della voce. Branch feat/voce-v7-m2, ho guardato solo il diff staged (4 file). Ho letto CLAUDE.md §5, §8 e §9, le parti di stato_progetto.md che riguardano la voce e la coda della memoria.

**Elementi del diff esaminati**
- `modules/voice/server.py:234` — `_chiudi_tempi`: restituisce None se `_tempi` è None o vuoto, aggiunge `server` e azzera `_tempi`. Rischio esaminato: tempi rimasti appesi o mandati due volte da una richiesta all'altra. Il server usa HTTP/1.0 (nessun `protocol_version`), quindi crea un handler nuovo per ogni richiesta, e l'attributo di classe resta None. — ok
- `modules/voice/server.py:285` — `do_POST` inizializza `_t0` e `_tempi = {}` come prima cosa. Rischio esaminato: la tua domanda sui 405/404 o su `_send_json` chiamato fuori da `do_POST`. In quei casi `_tempi` è None (attributo di classe), oppure `{}` sul 404/401 di `do_POST`, quindi `_chiudi_tempi` restituisce None: nessuna eccezione nuova e nessun campo `tempi`. — ok
- `modules/voice/server.py:241` — riga di log con `log.warning`. Rischio esaminato: privacy. Le chiavi sono fisse, i valori sono float e il parlato non c'è; il test lo verifica. Alla tua domanda: si può accettare per la fase di misura, ma WARNING nella scatola nera dovrebbe voler dire «c'è un problema». Esiste già un precedente più pulito: il logger `gas.snapshot`, alzato a INFO, scrive solo nel file, perché la console è a WARNING (gas.py:44-48). Però così la riga sparirebbe dal terminale del server. Se il terminale serve davvero, warning va bene così, purché sia dichiarato. — riserva BASSA (R-614-3-M2)
- `modules/voice/server.py:419` e `modules/voice/server.py:445` — `_segna("voce")` solo dopo che il TTS è riuscito. Stesso discorso per il cervello: viene segnato su final o error (`modules/voice/server.py:354`, `:357`), non quando run_turn solleva un'eccezione. Rischio esaminato: un TTS che va in timeout, cioè il primo sospetto della latenza, non compare nei tempi. — riserva BASSA (R-614-1-M2). Proposta: segnare anche nei rami `except` (ElevenLabsTTSError, OSError, Exception di run_turn).
- `modules/voice/server.py:261` — intestazione `X-Gas-Tempi` con l'MP3 grezzo. Rischio esaminato: header injection. Ci finiscono solo chiavi fisse e numeri. — ok
- `clients/voice/browser_client.html:701` — `descriviTempi`: accetta solo numeri finiti, la rete è calcolata con `Math.max(...,0)` e il testo va in `textContent` (`clients/voice/browser_client.html:635`). Rischio esaminato: XSS o NaN se `tempi` arriva malformato. `t0` è la const locale di `invia` (riga 600). — ok
- `tests/test_unit_voice_stt.py:595` — il test del JSON gira senza ELEVENLABS_API_KEY, quindi lo `_segna("voce")` del ramo audio+testo (`modules/voice/server.py:419`) non è coperto da nessun test. Il ramo MP3 invece sì (`tests/test_unit_voice_stt.py:619`). — riserva BASSA (R-614-2-M2)

**Wall of Shame**: niente slicing della history, niente simulazione di tool, `_get_window` e il tetto delle 10 iterazioni non sono toccati. Lo `_segna` e la `round` non possono sollevare eccezioni, quindi non ci sono nuove eccezioni non intercettate.

**Test riprodotti**: tests/test_unit_voice_stt.py, tests/test_unit_voice_server.py e tests/test_unit_voice_tts.py danno 165 passed, browser compresi (nessuno saltato). I tuoi 167 includono probabilmente un altro file voce che non ho lanciato.

**Rischio escluso**: non ho verificato i tempi reali su Groq, ElevenLabs e la VPS (non si riproducono in dev, i test usano mock). Non ho nemmeno fatto mutation test sulle singole righe `_segna`, a parte la valutazione di copertura qui sopra.

**Riserve da tracciare in stato_progetto.md**
1. R-614-1-M2 BASSA: i tempi non coprono i rami d'errore lenti (TTS in timeout, eccezione di run_turn).
2. R-614-2-M2 BASSA: manca un test per la voce nel JSON audio+testo.
3. R-614-3-M2 BASSA: una riga informativa scritta a livello WARNING.

**Memoria**: ho aggiunto la riga #614-M2 più una lezione («fermare il cronometro anche sui rami d'errore lenti») in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola dallo script (b48c9a5). Non ho committato altro.

Review #615-M2:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #615-M2 (dopo la #614-M2). Ho esaminato il branch feat/voce-v7-m2, solo il diff staged (4 file). Ho letto prima CLAUDE.md §5, la memoria del revisore e le riserve R-614. Nel diff non c'è slicing della history e non c'è simulazione di tool. I cap del kernel non sono toccati.

**Elementi del diff esaminati**
- `modules/voice/server.py:432`: il tempo della voce ora si segna in un `finally` (formato audio+testo). Rischio esaminato: tempo perso quando il TTS fallisce o va in timeout. Esito ok: si segna su tutti e tre i rami (ok, errore ElevenLabs, OSError). Nel mutante `finally`→`else` falliscono i casi [errore] e [rete].
- `modules/voice/server.py:367`: `t_cervello` parte da None prima del try e si segna nell'except. Rischio esaminato: un'eccezione sollevata prima di assegnare `t_cervello` (per esempio durante la preparazione di `kw`). Esito ok: la guardia `is not None` evita un crash dentro il gestore dell'errore. In quel caso il 500 esce solo con `server`, oppure senza tempi, ed è accettabile.
- `modules/voice/server.py:455` e `modules/voice/server.py:460`: `_segna` in testa ai due except del percorso MP3. Rischio esaminato: rami senza test. Esito: **riserva BASSA (R-615-1-M2)**. Nessun test copre il 502 del TTS con `Accept: audio/mpeg`. Il codice è corretto a lettura, ma il mutante non toccherebbe questi rami.
- `modules/voice/server.py:79`: logger `gas.voce.tempi` impostato a INFO. Rischio esaminato: la riga si perde nel file oppure sporca il terminale. Esito ok, verificato con una sonda reale (import di `modules.voice.server` e poi di `gas`, come fa `run_server`):
  - il root è a WARNING (30) e ha due handler: un `RotatingFileHandler` a livello 0 (NOTSET) e uno `StreamHandler` a 30;
  - il livello effettivo del logger è 20;
  - la riga INFO è arrivata in gas_debug.log e non è uscita in console. È lo stesso schema di `gas.snapshot` e `gas.knowledge` in `gas.py:79`.
  - Nessun `propagate=False` nel codice. Ho tolto dal log la riga di sonda.
- `modules/voice/server.py:245`: `_log_tempi.info` scrive solo numeri e il codice HTTP, mai il parlato. Esito ok. **Nota COSMETICA (R-615-2-M2)**: la docstring di `_chiudi_tempi` dice ancora «gas_debug.log e terminale del server», ma ora la riga va solo nel file. Anche l'indentazione della riga di continuazione è disallineata.
- `tests/test_unit_voice_stt.py:640`: test parametrico con TTS ok/errore/rete. Esito ok: chiude la R-614-2-M2 per il formato audio+testo.
- `tests/test_unit_voice_stt.py:657`: kernel che solleva un'eccezione, risposta 500 con `{cervello, server}`. Esito ok: il mutante lo fa fallire.
- `tests/test_unit_voice_stt.py:619`: controlla livello INFO e nome del logger. Esito ok: chiude la R-614-3-M2.

**Riproduzione**
- Mutante (`finally`→`else` e nessun `_segna` nell'except di run_turn): 3 failed su `-k v7`, riprodotto. Ho ripristinato il file: il diff non staged è vuoto.
- Suite stt+tts+server senza browser: 153 passed. Non coincide con i vostri 155, molto probabilmente perché avete selezionato file diversi: non ho incluso test_unit_voice_contesto.py.

**Riserve**
- R-615-1-M2 BASSA: aggiungere un test del 502 TTS col formato MP3 che controlli `voce` nei `tempi` della risposta JSON.
- R-615-2-M2 COSMETICA: allineare la docstring di `_chiudi_tempi` al nuovo logger, che scrive solo nel file.

**Rischi esclusi**
- Test del browser (Playwright) e `clients/voice/browser_client.html` non rieseguiti: il delta della M2 non li tocca. Restano validi i 165 passed della #614.
- Comportamento sul Mac e sulla VPS con il server avviato davvero via `python -m` non verificato. La sonda riproduce lo stesso ordine di import, ma non il processo reale.

La riga contatore #615-M2 è aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con commit_memoria_revisore.sh. Il diff staged non è stato committato. Nessuna lezione nuova.

Review #616-M2 (diff finale committato in 190d3fc):

## VERDETTO: APPROVATO

Review #616-M2: seconda review dopo la #615-M2, branch feat/voce-v7-m2, diff staged di 4 file. Ho letto CLAUDE.md (sezioni 5, 8 e 9), le voci di reports/stato_progetto.md che servivano e la coda di .claude/agents/memoria_revisore.md.

Elementi del diff esaminati:
- `tests/test_unit_voice_stt.py:658` — nuovo test con due casi (errore e rete). Manda una richiesta con `Accept: audio/mpeg`; `synthesize_speech` simulato lancia `ElevenLabsTTSError(500)` oppure `OSError("timeout")`; il test controlla che la risposta sia un 502 JSON con i tempi `{trascrizione, cervello, voce, server}`. Rischio esaminato: un test che passa anche senza la correzione. L'ho provato togliendo i due `_segna` dagli except: 2 failed. Rimesso il file com'era, `git diff` non in staging su server.py è vuoto. `-k v7`: 9 passed. Esito: ok, R-615-1-M2 chiusa.
- `modules/voice/server.py:455` e `modules/voice/server.py:460` — `_segna("voce", t)` prima di ogni 502 nei due except del percorso MP3. Rischio esaminato: tempo segnato dopo `_send_json`, cioè a richiesta già chiusa, e quindi perso. Qui viene segnato prima, quindi `_chiudi_tempi` lo include. Il percorso del successo segna dopo `synthesize_speech`, prima di `_send_audio`. Esito: ok.
- `modules/voice/server.py:238` — la docstring di `_chiudi_tempi` ora dice «una riga INFO nel solo gas_debug.log (logger gas.voce.tempi)», coerente con il logger dedicato a INFO di `modules/voice/server.py:79`. Indentazione della riga di continuazione corretta. Esito: ok, R-615-2-M2 chiusa.
- Wall of Shame: nel diff non c'è slicing della history né output dei tool simulato (i mock stanno solo nei test, e sostituiscono servizi esterni, non tool del modello). Le eccezioni del TTS vengono intercettate e loggate con `log.warning`, senza crash. Esito: ok.

Rischi esclusi:
- Suite voce completa (stt, server e tts, browser compresi) lanciata in background ma non finita entro il tempo della review: esito non verificato. Al suo posto ho usato `-k v7` più il mutante; le altre righe non sono cambiate rispetto alla #615-M2, dove i 153 test erano passati.
- Latenza reale di ElevenLabs e Groq sulla VPS non misurata: in dev non si può riprodurre senza le chiavi vere.

Riga contatore: aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md come `#616-M2 — 2026-11-02 — APPROVATO — …`, nessuna lezione nuova.

Da fare per te: `bash scripts/commit_memoria_revisore.sh` non è partito, l'ha bloccato il classificatore della modalità automatica perché era un commit non richiesto. Il file contiene la riga ma non è committato: committalo tu (lo script o `/fine-task`, passo 4). Non ho committato nient'altro, come richiesto.

Merge di origin/main (7ced8a2). Review #643-M2:

## VERDETTO: APPROVATO

Review #643-M2: merge di origin/main 3cd550f (PR #318 V6 e PR #321 forte-non-bare) nel branch feat/voce-v7-m2. Tutto è in staging e il merge è ancora in corso (esiste `.git/MERGE_HEAD`).

Letture obbligatorie fatte: CLAUDE.md (sez. 5), reports/stato_progetto.md (la parte sulla voce e su V7), .claude/agents/memoria_revisore.md (da #611 a #641).

**Elementi del diff esaminati**
- `modules/voice/server.py:293` — inizio di do_POST dopo la risoluzione del conflitto: ci sono `self._t0`, `self._tempi = {}` (V7a) e `self._capito = None` (V-3 bot #318). Rischio esaminato: stato rimasto da una richiesta precedente sulla stessa connessione (keep-alive), oppure una delle due parti persa nella risoluzione. Le tre righe sono tutte presenti e azzerate prima di ogni ramo, compresi 404/405. Esito: ok.
- `modules/voice/server.py:392` — `_rispondi_senza_turno`, versione presa da main (V-2 bot #318: senza ElevenLabs si risponde con un 200 di solo testo). Rischio esaminato: le risposte «non ho capito» e «uso» perdono i tempi o il campo capito. Il percorso è questo: TrascrizioneIncerta segna la trascrizione (`modules/voice/server.py:502`), imposta `_capito` e chiama `_rispondi_senza_turno`. Tutti e tre i suoi rami finiscono in `_send_json` (che aggiunge `tempi`), in `_do_audio_testo_response` o in `_do_tts_response`, e ognuno porta capito e tempi. Esito: ok.
- `modules/voice/server.py:253` — `_send_json` e `_chiudi_tempi`: invariati rispetto alla V7a già approvata in #616-M2. I tempi si chiudono una sola volta per richiesta e il log contiene solo numeri. Esito: ok.
- `tests/test_unit_voice_stt.py:665` — i test V7 (tempi nel JSON e nel log, intestazione X-Gas-Tempi con l'MP3, TTS fallito, kernel che si rompe, rifiuto 429 senza tempi) stanno accanto ai test V6 arrivati da main. Esito: ok.

**Controlli strutturali**
- `git diff --cached origin/main` su modules/voice, clients, tests, .github, brains e gas.py: 4 file (+176/−3), cioè solo la V7a già rivista; brains/, gas.py e .github sono identici a main.
- `git diff --cached HEAD`: entrano solo le modifiche V6/#321 di main (in server.py la variabile `GAS_VOICE_STT_ECO_NO_SPEECH` nella documentazione, il reset di `_capito` e il ramo senza TTS).
- Nessun marcatore di conflitto, né in modules/voice/server.py né nella memoria.
- Nessuno slicing della history e nessun tool simulato.
- Test riprodotti da me: voce (stt, server, contesto, tts) **193 passed** in 210 s, test nel browser compresi.

**Rischi esclusi (non verificati)**
- Le suite claude_cli, dotenv e kernel (1063 PASS dichiarati) non le ho rieseguite. Il codice di #321 arriva da main identico ed era già stato rivisto in #632–#641-M2.
- Nessun test controlla esplicitamente il campo `tempi` nella risposta «non ho capito». La convivenza l'ho verificata leggendo il codice, non con un test. Non è un blocco: il percorso passa dallo stesso `_send_json` già coperto.
- La latenza reale sul Mac non è verificabile in questo ambiente.

**Memoria**
- Ho aggiunto la riga `#643-M2 — 2026-11-02 — APPROVATO — …` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con «Nessuna lezione nuova».
- Non ho lanciato commit_memoria_revisore.sh perché il merge è in corso: la riga resta nel file, non ancora in staging, e va inclusa nel commit di merge.
- Nella memoria non esiste un #642: ho usato il numero #643 che mi hai indicato.
- Ricorda che nella memoria #614-M2 compare due volte; la numerazione parallela è già dichiarata in #617-M2.

Commit della correzione (bot su 33a0346). Review #644-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #644-M2: diff staged di 4 file su feat/voce-v7-m2 (PR #322). Chiude V-1 e V-2 del bot su 33a0346. Ho fatto le tre letture obbligatorie: CLAUDE.md è nel contesto; di stato_progetto e della memoria ho letto le parti utili.

Cosa ho esaminato nel diff:
- `clients/voice/browser_client.html:609`: con una risposta non 2xx la pagina ora legge il JSON una volta sola e ne prende sia `error` sia `tempi` (questi solo se sono un oggetto). Tutto sta dentro un try/catch: un corpo che non è JSON lascia `tempiErr=null` e la pagina non va in errore. La riga dei tempi si scrive con `textContent`, non con innerHTML, quindi niente rischio di HTML iniettato; inoltre `descriviTempi` accetta solo numeri finiti. Esito: ok.
- `modules/voice/server.py:311`: `_t0` riparte dopo `rfile.read(length)`. Il primo `_t0` alla riga 293 resta per le risposte 404/401/400 date prima della lettura del corpo, quindi `_send_json` non usa mai un `_t0` lasciato da una richiesta precedente sulla stessa connessione. Il «server» adesso misura solo il lavoro fatto dopo aver ricevuto il corpo; la pagina calcola la rete come totale meno server, e il totale parte prima del fetch, quindi il caricamento finisce nella «rete», com'è giusto. `time` era già importato (riga 70). Esito: ok.
- `tests/test_unit_voice_stt.py:755`: il test usa un socket grezzo con HTTP/1.0, manda il corpo in due pezzi con 0,6 s di pausa e controlla `server < 0.5`. Il margine è ragionevole: il prompt «ciao» con il kernel finto del fixture è veloce. Esito: ok.
- `tests/test_unit_voice_server.py:904`: il `waitForFunction` ora accetta anche uno stato che comincia con «errore». Questo non indebolisce le altre modalità del test, perché dopo restano le asserzioni sul testo, sull'audio e sui turni, che fallirebbero comunque. Il nuovo modo «guasto» (riga 992) risponde 502 con i tempi, e il test controlla lo stato finale e il prefisso della riga tempi (riga 1051). `1.25.toFixed(1)` dà "1.3", come si aspetta l'asserzione. Esito: ok.

Riserva (BASSA, da tracciare in stato_progetto.md): nel ramo «errore di rete» (il catch del fetch, `clients/voice/browser_client.html:605`) la riga tempi non viene azzerata, quindi può restare a schermo quella del turno precedente. Il problema c'era già prima di questo diff, che però lo rende più visibile, perché adesso anche i guasti mostrano i tempi. La correzione è una riga: `tempiEl.hidden = true` in quel ramo.

Wall of Shame: nessun taglio della cronologia, nessun output dei tool simulato. Cap di 10 iterazioni e `_get_window` non toccati.

Prove: ho rilanciato `tests/test_unit_voice_stt.py` e `tests/test_unit_voice_server.py` per intero: 169 passed in 220 s.

Cosa non ho verificato:
- Non ho rifatto i due test mutanti (pagina vecchia e server vecchio) e mi fido del tuo «1 failed» per ciascuno.
- Non ho controllato come si comporta su Safari/iOS reale né con un 502 vero di un proxy davanti al server, che può mandare un corpo HTML senza tempi. Il codice in quel caso degrada a riga tempi vuota, ma l'ho visto solo leggendolo, non provandolo.

Memoria: ho aggiunto la riga #644-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con 34ff97f. Nessuna lezione nuova.

Review #645-M2 (diff finale committato):

## VERDETTO: APPROVATO

Review #645-M2: stesso diff staged della #644-M2 (4 file, 46+/4-), con in più la riga che chiude la riserva R-644-1-M2 (la riga dei tempi di un turno precedente che restava a schermo dopo un errore di rete). La riserva è chiusa; il resto del diff non è cambiato.

- `clients/voice/browser_client.html:606`: nel catch del fetch c'è ora `tempiEl.hidden = true` prima di `fineTurno`. Rischio esaminato: tempi vecchi visibili dopo un errore di rete. La riga li nasconde; il testo resta nell'elemento ma non si vede, e il turno successivo lo riscrive comunque (righe 616 e 642). Esito: ok.
- `clients/voice/browser_client.html:609`: il ramo `!resp.ok` è invariato rispetto alla #644: legge error e tempi in un solo `resp.json()` e scrive con `textContent`, quindi niente HTML iniettato. Esito: ok.
- `modules/voice/server.py:311`: `_t0` riparte dopo `rfile.read` ed è invariato rispetto alla #644. Il tempo di caricamento resta nella «rete». Esito: ok.

Prove: ho rilanciato `tests/test_unit_voice_server.py -k "guasto or normale or errore"`: 4 passed. La suite voce completa (169 passed) l'ho fatta girare nella #644, prima di questa riga in più.

Cosa non ho verificato:
- Non c'è un test che provochi un vero errore di rete (fetch rifiutato) per controllare che la riga tempi si nasconda: la modifica è di una riga e l'ho verificata solo leggendola.
- Non ho controllato il comportamento su Safari/iOS reale.

Memoria: ho aggiunto la riga #645-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con d58208d. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Test della voce (tutti i `tests/test_unit_voice*.py`, browser compresi) + claude_cli + dotenv: 258 passed dopo il merge di main. Kernel (`tests/test_unit_kernel.py`): RIEPILOGO 1063 PASS, 0 FAIL. Dopo la correzione del bot: test_unit_voice_stt + test_unit_voice_server 169 passed (revisore #644-M2); test nuovi `test_v7_caricamento_lento_non_conta_come_server` e il modo «guasto» del test nel browser, ognuno col suo mutante → 1 failed. I test V7 nuovi stanno in `tests/test_unit_voice_stt.py` (tempi nel JSON/log, MP3 con X-Gas-Tempi, TTS fallito, kernel che si rompe, 429 senza tempi) e `tests/test_unit_voice_server.py` (pagina).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette dall'integrazione GitHub.
- f3a3cc4 e 33a0346 (fine-task precedenti, pushati in due momenti): suite completate (notifiche check_suite.completed); su 33a0346 handoff-check e verifica-bot success alla lettura della verifica esterna, bot APPROVATO CON RISERVE.
- Correzione, memoria (34ff97f, d58208d), merge di main 60499a4 e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- Nessun test provoca un vero errore di rete nella pagina per vedere la riga tempi nascosta (R-644-1-M2 chiusa solo a lettura).
- Nessun test controlla esplicitamente il campo `tempi` nella risposta «non ho capito» (V6): convivenza verificata leggendo il codice (review #643-M2), stesso `_send_json` già coperto.
- La latenza reale si misura solo sul Mac.
