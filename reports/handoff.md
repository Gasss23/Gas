# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Voce V7b: voce frase per frase (chat M2, coordinata da M1) — aggiornato dopo bot e verifica esterna su a73916a

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #325 (https://github.com/Gasss23/Gas/pull/325). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5125667041","url":"https://github.com/Gasss23/Gas/pull/325"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.
2. Sul Mac, dopo il merge: sentire se Gas comincia a parlare dopo la prima frase e leggere la riga «tempi».

---

## §1 SCOPE & ESITO FETTE

- **V7b — voce frase per frase**: `FATTA` (review #618–#622-M2).
- **Allineamento alla V7a mergiata (#322) e a main**: `FATTA` (review #651-M2).
- **V-3 COSMETICA del bot su #322** (tipo di `t_cervello`): `FATTA` (review #652-M2).
- **Bot su a73916a** (APPROVATO CON RISERVE): V-1 (test della sintesi fermata con margine di una sola frase), V-2 (righe non chiuse su risposta illeggibile), V-3 (502 falso del proxy a pagina chiusa prima degli header), V-4 cosmetica (errore della voce a metà solo in console): `FATTE`, review #653-M2 APPROVATO.
- **Verifica esterna su a73916a** (https://github.com/Gasss23/Gas/pull/325#issuecomment-6585732063): APPROVATO CON RISERVE, solo BASSE (§3 fermo a e111045: ora il log arriva alla testa; §6 senza CI; «fine» in ritardo e thread di guardia già dichiarati).
- **V8, V9**: `DEFERITE` — una PR alla volta, dopo il merge della precedente.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  11 +++++++++
 clients/voice/browser_client.html  | 151 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------
 clients/voice/browser_server.py    |  59 ++++++++++++++++++++++++++++++++++++++++++++++++
 modules/voice/server.py            |  87 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  12 +++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  22 ++++++++----------
 tests/test_unit_voice_server.py    | 319 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1196be7 fix(voce): righe chiuse su risposta illeggibile, proxy senza 502 falso a pagina chiusa, test della sintesi fermata più netto (V-1..V-4 bot #325 su a73916a; review #653-M2)
fc1b96c chore(revisore): memoria review #653 — APPROVATO
a73916a docs(voce-v7b): numero della PR #325 nei report
e111045 docs(voce-v7b): report di fine task (review #618–#622-M2, #651–#652-M2)
d1e9822 fix(voce): tempo del cervello senza risposta solo con t_cervello valorizzato (V-3 bot #322; review #652-M2)
1fd1f5a chore(revisore): memoria review #652 — APPROVATO
9f2046e Merge remote-tracking branch 'origin/main' into feat/voce-v7b-m2
ee8b079 Merge branch 'feat/voce-v7-m2' into feat/voce-v7b-m2
c77ad6c feat(voce): V7b — voce frase per frase: Gas comincia a parlare dopo la prima frase (chat M2)
75778a3 chore(revisore): memoria review #622 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della fetta (c77ad6c). Cinque passaggi del revisore sullo stesso diff staged; verdetti integrali.

Review #618-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #618-M2, fetta V7b «parlato a pezzi», branch feat/voce-v7b-m2. Ho rivisto solo il diff staged (4 file).

Letture fatte prima della review: CLAUDE.md (sez. 5), reports/stato_progetto.md (parti sulla voce), .claude/agents/memoria_revisore.md.

Il diff non tocca gas.py né brains, non affetta la history e non simula tool. Le eccezioni della sintesi vocale (TTS) restano intercettate e scritte nel log, come prima.

**Elementi del diff esaminati**
- `modules/voice/server.py:457` — `_do_pezzi_response`: risposta a righe JSON (NDJSON), una sintesi per frase. Rischi esaminati:
  - errore a metà o sulla prima frase: riga `errore_voce`, poi riga `fine`, nessuna sintesi in più (coperto dai test);
  - testo vuoto: il ramo `if not text.strip()` a `modules/voice/server.py:434` resta nel JSON, quindi la prima riga ha sempre `content`;
  - tempi chiusi una volta sola anche col client chiuso.
  - Esito: ok.
- `modules/voice/server.py:469` — `riga()`: un OSError in scrittura ferma la sintesi. Sonda reale (`/tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/sonda.py`, socket grezzo che chiude dopo la prima riga):
  - con 3 frasi: 3 sintesi su 3;
  - con 4 frasi: 3 su 4.
  - La prima scrittura dopo la chiusura riesce (manda solo il reset di connessione), quindi lo stop arriva con una frase di ritardo. La spesa non peggiora rispetto a V7a, che sintetizzava sempre tutta la parte parlata, ma «niente spesa per frasi che nessuno ascolta» è ottimistico. Esito: riserva.
- `modules/voice/server.py:427` — `_vuole_audio_testo` accetta anche «pezzi». Senza chiave ElevenLabs, o col formato «audio+testo» vecchio, resta il JSON di prima; il client solo audio passa ancora da `_wants_audio`. Esito: ok (compatibilità coperta dal test).
- `clients/voice/browser_server.py:175` — `_inoltra_a_pezzi`:
  - inoltra con `read1` + flush;
  - la proxy usa HTTP/1.0, quindi la fine della risposta è la chiusura della connessione;
  - un OSError o HTTPException a metà viene loggato e fa uscire;
  - il `finally` di `_proxy_voice` chiude la connessione verso il server voce.
  - Esito: ok.
- `clients/voice/browser_client.html:729` — `onended` di `suonaPezzo`: prende la prossima frase dalla coda; se è finita chiude il turno, altrimenti mette `attende`. Ogni callback ricontrolla `riproduzione !== rip` e `turno !== numTurno`. Race esaminate:
  - `pause` al cambio di src: quando si cambia src il player è già ended e in pausa, e il `pause` naturale passa da `player.ended`;
  - interruzione mentre `attende` è attivo: l'arrivo della frase dopo viene ignorato.
  - Esito: ok.
- `clients/voice/browser_client.html:710` — `lasciaRiproduzione` mette solo `fermo = true`. Il lettore si chiude in `leggiResto` (`clients/voice/browser_client.html:693`) solo DOPO la riga successiva. Dopo un'interruzione la connessione resta aperta finché il server non manda un'altra frase. Il server voce è single-thread (HTTPServer), quindi il turno nuovo resta in coda dietro le sintesi rimaste, e anche la riga `tempi` del turno vecchio può ancora scriversi a schermo. Esito: riserva.
- `clients/voice/browser_client.html:760` — `play().catch` con autoplay negato: chiude la conversazione e lascia la risposta. Però col tasto play si ascolta solo la prima frase, e il riascolto a fine risposta dà solo l'ultima, non tutta la parte parlata come prima. Esito: riserva (regressione d'uso minore).

**Riserve (tutte BASSE, da tracciare in stato_progetto.md)**
- **R-618-1-M2**: `lasciaRiproduzione` dovrebbe chiamare subito `righe.chiudi()` (il lettore va tenuto in `rip`). Oggi, dopo un'interruzione, il server continua a sintetizzare (circa 1–2 frasi in più) e tiene occupato il turno successivo.
- **R-618-2-M2**: il ramo «client chiuso → stop della sintesi» (`modules/voice/server.py:469`) non ha test. La sonda sopra si può trasformare in test, con l'asserzione sul numero di sintesi rispetto al numero di frasi.
- **R-618-3-M2**: con autoplay negato, o col riascolto dai controlli, si sente una sola frase. Va dichiarato, oppure si accumulano i blob e si fa un riascolto completo.

**Verifiche fatte**
- `tests/test_unit_voice_server.py`: 85 passed in 227 s, test nel browser compresi.
- Non ho rifatto il mutante dichiarato (tolto `lasciaRiproduzione` dall'interruzione).

**Rischi esclusi (non verificati)**
- Comportamento reale di Chrome/Safari sul Mac con ElevenLabs vero: tempi di decodifica tra una frase e l'altra e pause udibili. Non è riproducibile qui senza chiave e senza casse.
- Il mutante del browser dichiarato da M2: non rieseguito, per i tempi lunghi della suite col browser.

**Memoria del revisore**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga `#618-M2` e una lezione nuova: la prima scrittura dopo che il client ha chiuso riesce; per fermarsi subito si chiude il lettore subito.
- Il commit della memoria (`bash scripts/commit_memoria_revisore.sh`) è stato **negato dal classificatore dei permessi**. Il file è modificato ma **non committato**: va committato dall'agente principale insieme alla fetta. Nessun altro commit fatto.

Review #619-M2:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #619-M2 su feat/voce-v7b-m2 (diff staged, 4 file). Il delta rispetto alla #618 riguarda clients/voice/browser_client.html e tests/test_unit_voice_server.py. Le tre riserve della #618 sono chiuse nel codice. Ne restano due nuove, entrambe BASSE e non bloccanti.

Elementi del diff esaminati:
- `clients/voice/browser_client.html:727` — `lasciaRiproduzione()` imposta `fermo=true` e chiama subito `righe.chiudi()` (`reader.cancel()`). La `prossima()` in attesa riceve `done`, e una riga parziale finisce nel `catch` di `leggiResto`. Rischio esaminato: la connessione resta aperta dopo interruzione, pausa o errore. Esito: ok, R-618-1-M2 chiusa nel codice. Ho fatto un mutante che toglie la chiamata a :727: i 3 test «pezzi» (browser compreso) passano lo stesso. La chiusura immediata lato pagina non è coperta da nessun test (riserva R-619-1-M2).
- `tests/test_unit_voice_server.py:1326` — il test usa un socket grezzo che chiude dopo la prima riga, con 6 frasi e una sintesi lenta da 0,15 s, e verifica al massimo 3 sintesi. Rischio esaminato: un test che passa anche quando il ramo `except OSError` di `riga()` non ferma la sintesi. Esito: ok, R-618-2-M2 chiusa. Il limite di 3 è coerente con la lezione della #618 (la prima write dopo la chiusura riesce). Il mutante l'avete fatto voi: io non l'ho rifatto, ho visto solo che il test è verde.
- `modules/voice/server.py:476` (contesto, invariato rispetto alla #618) — `riga()` restituisce False su OSError e il ciclo si ferma. Esito: ok.
- `clients/voice/browser_client.html:716` — `mettiRiascolto(rip)` mette nel player l'MP3 intero, cioè le frasi raccolte in `rip.tutti` messe una dopo l'altra. Viene chiamato a fine turno e, con autoplay negato, a fine lettura (:703, :790). Rischio esaminato: il riascolto copre solo l'ultima frase. Esito: ok, R-618-3-M2 chiusa. Il test «pezzi» conta 3 sorgenti.
- `clients/voice/browser_client.html:703` — nel ramo `soloRaccogli` (autoplay negato), `mettiRiascolto` non controlla `rip.turno === numTurno`. Non controlla nemmeno se l'utente ha già premuto play sulla prima frase mentre le altre arrivano: in quel caso `player.src` cambia durante l'ascolto e la riproduzione si interrompe. Lo stesso vale se nel frattempo è partito un turno nuovo; con il server single-thread la finestra è minima. Esito: riserva BASSA (R-619-2-M2). Soluzione suggerita: in quel ramo uscire se `rip.turno !== numTurno || !player.paused`, oppure aggiornare `src` solo a player fermo.
- `clients/voice/browser_client.html:682` — `chiudi()` avvolge `reader.cancel()` in un try/catch, ma `cancel()` restituisce una Promise e un suo eventuale rifiuto non viene intercettato. Esito: cosmetica (basta un `.catch(()=>{})`).

Prove eseguite:
- `pytest tests/test_unit_voice_server.py -k "v7b or pezzi"`: 9 passed, nessun test saltato (il browser c'è, i modi pezzi e pezzi_interrotti girano).
- Mutante R-618-1, togliendo `righe.chiudi()`: 3 passed, quindi il mutante sopravvive. Il file è stato ripristinato e corrisponde allo staged (`git diff --quiet` pulito).

Rischi esclusi:
- Non ho ascoltato l'MP3 concatenato: in dev non c'è un'uscita audio reale. Eventuali tag ID3 in mezzo o una durata stimata male in Safari o Chrome non sono verificati; vanno provati sul Mac.
- Non ho rieseguito l'intera suite (12 modi del browser, 3 run consecutive): mi fido dei vostri «12 passed».
- Non ho riletto per intero i file non toccati dal delta (modules/voice/server.py, clients/voice/browser_server.py): li ha già esaminati la #618.

Riserve da tracciare in stato_progetto.md:
- R-619-1-M2 (BASSA): nessun test copre la chiusura immediata del lettore lato pagina. Un test possibile: nel modo `pezzi_interrotti`, contare quante sintesi fa il server dopo l'interruzione.
- R-619-2-M2 (BASSA): `mettiRiascolto` nel ramo `soloRaccogli` cambia `src` senza controllare il turno né se il player sta suonando.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. I guardrail (`_get_window`, limite di 10 iterazioni) non sono toccati.

Memoria: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga contatore #619-M2 e una lezione (fix lato client «chiudi subito» da provare con un mutante). Come mi hai chiesto non ho committato e non ho lanciato commit_memoria_revisore.sh: le righe #618 e #619 le committi tu con il resto.

Review #620-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #620-M2 (rifà la #619-M2) sul diff staged del branch feat/voce-v7b-m2, 4 file. Ho letto CLAUDE.md, la memoria del revisore e le parti che servivano di stato_progetto.md.

**Elementi del diff esaminati**
- `clients/voice/browser_server.py:143`: prende il socket verso il server voce prima di `getresponse()`. Rischio: che `conn.sock` diventi None o venga staccato. Esito: ok. Il riferimento si prende prima che `getresponse()` lo stacchi, e il socket si chiude davvero con `resp.close()` (righe 200-201) quando cadono i riferimenti di makefile.
- `clients/voice/browser_server.py:178`: `_guarda_pagina` (il thread di guardia). Rischi esaminati, come da tue domande:
  (a) **recv in parallelo alle scritture sullo stesso socket**: ok. send e recv su thread diversi sono sicuri a livello di sistema operativo, il socket Python non ha un buffer condiviso, e `MSG_PEEK` non consuma byte.
  (b) **shutdown dopo una fine normale**: ok. A fine risposta il socket verso la voce è già chiuso, quindi il suo fd interno è -1. `shutdown` dà errore EBADF, che viene intercettato, e non tocca nessun fd vero.
  (c) **fd riusati**: rischio trascurabile. Se la pagina viene chiusa prima che il thread entri in recv, si ottiene EBADF dal socket Python (fd -1). Se è già dentro recv, il kernel tiene il riferimento al file originale. Resta solo una finestra teorica di nanosecondi, e anche lì `MSG_PEEK` non consuma dati.
  Esito: ok, con due riserve BASSE (sotto).
- `clients/voice/browser_server.py:197`: avvia il thread daemon, uno per ogni risposta a pezzi. Rischio: thread bloccato per sempre se il browser non chiude mai il TCP dopo il FIN del proxy (HTTP/1.0). Esito: riserva BASSA (thread daemon, perdita limitata).
- `tests/test_unit_voice_server.py:1026`: il server finto guarda la chiusura con select e recv `MSG_PEEK` prima della 3ª frase; il controllo è a `tests/test_unit_voice_server.py:1116` (`chiusure == [True]`). Rischio: un test che passa anche senza il fix. Esito: ok. Ho riprodotto il mutante: tolto l'avvio del thread a `clients/voice/browser_server.py:197`, `pezzi_interrotti` dà 1 failed; poi ho rimesso il file com'era (diff del worktree pulito). Con `-k "pezzi or v7b"`: 9 passed (browser compreso).
- `clients/voice/browser_client.html:706`: riascolto messo solo se `rip.turno === numTurno && player.paused`. Rischio: cambiare l'audio mentre l'utente ascolta col tasto play. Esito: ok, R-619-2-M2 chiusa.
- `clients/voice/browser_client.html:682`: `reader.cancel().catch(() => {})`. Esito: ok, nota cosmetica chiusa.

**Riserve (BASSE)**
- R-620-1-M2: `except OSError: pass` a `clients/voice/browser_server.py:184` tratta anche un `TimeoutError`, che è un OSError, come «pagina chiusa», e quindi chiude la connessione verso la voce. Oggi non succede, perché il socket della pagina non ha timeout (`timeout` di socketserver = None). Basta però impostare in futuro `BrowserProxyHandler.timeout` per troncare tutte le risposte lunghe. Va escluso `TimeoutError` (return senza shutdown).
- R-620-2-M2: il thread di guardia resta bloccato per sempre se il peer non chiude mai il TCP (half-open). È daemon, ce n'è uno per risposta: solo una piccola perdita.
- R-620-3-M2 (COSMETICA): il commento a `clients/voice/browser_server.py:221` cita «il finally di _proxy_voice», ma ora la chiusura la fanno il finally di `_inoltra_a_pezzi` e il thread di guardia.

**Non verificato**: comportamento con un browser vero sul Mac (keep-alive, chiusura del TCP dopo la fine della risposta) e su una VPS dietro un reverse proxy, che potrebbe non inoltrare subito la chiusura. In dev non si può riprodurre. La suite voce completa da 182 non l'ho rilanciata: ho rilanciato solo il sottoinsieme pezzi/v7b più il mutante.

**Memoria**: ho aggiunto la riga contatore #620-M2 e una lezione in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md`. Il commit con `scripts/commit_memoria_revisore.sh` è stato bloccato dal classificatore dei permessi (Git Destructive), quindi il file è modificato ma NON committato. Va incluso nel commit di `/fine-task`.

Review #621-M2:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #621-M2 su feat/voce-v7b-m2: diff staged di 4 file, cambiato rispetto alla #620 solo `clients/voice/browser_server.py`. Prima della review ho letto CLAUDE.md (sez. 5 già nel contesto), `reports/stato_progetto.md` (le righe su voce/620) e la coda di `.claude/agents/memoria_revisore.md`.

**Elementi del diff esaminati**
- `clients/voice/browser_server.py:187` — `except TimeoutError: return` messo prima di `except OSError` in `_guarda_pagina`. Rischio esaminato: che un tempo scaduto venga letto come «pagina chiusa» e chiuda la connessione verso la voce. L'ordine è giusto: ho controllato che `TimeoutError` sia sottoclasse di `OSError` (risultato `True`), quindi senza questo ramo prima finirebbe nel `pass` e chiuderebbe. Il ramo `OSError` vero resta come prima: chiude la connessione verso la voce. Esito: ok, R-620-1-M2 chiusa.
- `clients/voice/browser_server.py:178` — docstring di `_guarda_pagina`: thread daemon, uno per risposta, resta fermo senza danno se la pagina non chiude mai il TCP. Rischio esaminato: thread che si accumulano. Con un thread daemon per risposta e un browser che chiude normalmente il TCP non si accumulano, e il caso limite è dichiarato. Esito: ok, **accetto R-620-2-M2 come chiusa-dichiarata**.
- `clients/voice/browser_server.py:224` — il commento ora dice «il finally di _inoltra_a_pezzi chiude anche il server voce». È coerente con `clients/voice/browser_server.py:204` (`resp.close()` nel finally). Esito: ok, R-620-3-M2 chiusa.
- `clients/voice/browser_server.py:200` — avvio del thread di guardia, invariato dalla #620. Esito: ok.

**Test**
- `pytest tests/test_unit_voice_server.py -k "v7b or proxy"`: 13 passed, 73 deselected.
- Nel diff di `browser_server.py` nessuno slicing della history (grep rc=1). Il codice non tocca né la history né i provider.

**Riserva (BASSA)**
- Nessun test copre il ramo `TimeoutError` in `clients/voice/browser_server.py:187`. Oggi è irraggiungibile, perché il socket della pagina non ha timeout. Se in futuro qualcuno mette un timeout sul socket della pagina, il ramo diventa vivo e non è protetto dai test. Va registrata in stato_progetto.md.

**Rischio escluso**
- Non ho fatto nuovi mutanti su questo giro: il delta è un solo ramo irraggiungibile più commenti, e il mutante del thread di guardia era già stato riprodotto nella #620.
- Non ho verificato il comportamento con un browser reale né su VPS: non è riproducibile in questo ambiente.

**Memoria del revisore**
- Ho aggiunto la riga contatore `#621-M2` in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- **Non ho fatto il commit** di quel file con `scripts/commit_memoria_revisore.sh`: il classificatore dei permessi ha negato il commit. Va committato dall'agente principale insieme al resto del fine-task. Nessun commit del diff sotto review, come richiesto.

Review #622-M2 (diff finale committato in c77ad6c):

## VERDETTO: APPROVATO

Ri-review #622-M2 sul branch feat/voce-v7b-m2 (diff staged, 4 file). Rispetto alla #621 cambia solo il test.

Cosa ho controllato nel diff:
- `tests/test_unit_voice_server.py:1344` — nuovo test parametrico `test_v7b_guardia_della_pagina`, copre i 4 rami di `_guarda_pagina` con una pagina finta:
  - lettura vuota → la connessione verso la voce si chiude;
  - ConnectionResetError → si chiude;
  - TimeoutError → non si chiude;
  - dati inattesi → non si chiude.
  - Rischio esaminato: un test che passa anche senza il ramo che dovrebbe proteggere. Esito: ok. Ho riprodotto il mutante (tolto `except TimeoutError`): fallisce solo `[tempo-False]` (1 failed, 3 passed). Il file l'ho poi ripristinato dalla versione staged, quindi l'area di staging è intatta.
- `clients/voice/browser_server.py:187` — `except TimeoutError` messo prima di `except OSError` (TimeoutError è una sottoclasse di OSError).
  - Rischio esaminato: ordine dei rami e copertura dei test. Esito: ok, la riserva BASSA della #621 è chiusa anche nella rete dei test.
- `clients/voice/browser_server.py:178` — `_guarda_pagina`. Il test crea l'handler con `__new__` e gli assegna solo `connection`, quindi niente socket reale.
  - Rischio esaminato: dipendenza da attributi dell'handler non preparati dal test. Esito: ok, il metodo usa solo `self.connection`.

Esecuzione:
- `-k guardia`: 4 passed.
- `-k "v7b or proxy"`: 17 passed.

Wall of Shame: nessuno slicing della history e nessuna simulazione dell'output dei tool. Il test usa oggetti finti per i socket, non output finti di tool di Gas.

Rischio escluso: non ho verificato il comportamento con un socket reale della pagina che ha un timeout impostato. Oggi quel caso non si presenta (il socket della pagina non ha timeout) e il ramo è provato solo con l'oggetto finto. Non ho ripetuto la suite completa né la prova d'ascolto nel browser, perché fuori dal delta.

Memoria: ho aggiunto la riga contatore #622-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata (75778a3, solo quel file). Il primo tentativo di commit, scritto in un comando unico con l'aggiunta della riga, è stato fermato da review_gate.sh. Ripetuto da solo, lo script è passato. L'area di staging del motore non è cambiata (4 file) e non ho fatto altri commit.

Merge della V7a aggiornata (ee8b079). Review #651-M2:

## VERDETTO: APPROVATO

Review #651-M2: merge di feat/voce-v7-m2 (5d39333) dentro feat/voce-v7b-m2 (c77ad6c), con tutto in staging.

**Cosa contiene il merge.** `git diff --cached MERGE_HEAD` tocca solo i 5 file della V7b: clients/voice/browser_client.html, clients/voice/browser_server.py, modules/voice/server.py, tests/test_unit_voice_server.py e la memoria. Tutto il resto (main da #318 a #323, ascolto.py, gas.py, brains, report) è identico a quello della V7a aggiornata. Nei file voce e nella memoria non ci sono marcatori di conflitto.

**Elementi del diff esaminati:**
- `clients/voice/browser_client.html:615` — nel catch del fetch (errore di rete) nasconde i tempi e il «Ho capito». Rischio esaminato: che la V7b li avesse lasciati fuori. Esito: ok. Il ramo `!resp.ok` (riga 618) legge `error` e `tempi` con una sola `resp.json()` e mostra la riga dei tempi. Il catch «risposta non leggibile» (riga 649) li nasconde, e copre anche il caso di NDJSON vuoto o rotto alla prima riga. Quindi i tre rami d'errore della V7a convivono con `lettoreRighe`.
- `clients/voice/browser_client.html:715` — in `leggiResto` la riga «fine» chiama ancora `mostraTempi(j.tempi)`. Rischio esaminato: che i tempi della V7b sparissero col merge. Esito: ok. Il test `pezzi` lo conferma: «… voce 0.2s · rete …» e `tempiVisibili` vale true. `#tempi` sta fuori da `#player-wrap` e c'è la regola `[hidden]` presa dalla V7a.
- `modules/voice/server.py:430` — `_vuole_audio_testo` accetta anche il formato pezzi. Rischio esaminato: che i rami della V7a (`_rispondi_senza_turno` con il controllo della chiave ElevenLabs, `_segna("cervello")` quando il risultato è None, `_t0` dopo `rfile.read`) saltassero il percorso NDJSON. Esito: ok. Le risposte d'errore restano JSON (`_send_json` con i tempi), quindi la pagina le legge nel ramo `!resp.ok`. I tempi delle risposte a pezzi si chiudono una volta sola, nella riga «fine».
- `tests/test_unit_voice_server.py:1035` — il ramo `guasto` della voce finta viene dopo il ramo pezzi, che risponde solo con `modo in ("pezzi","pezzi_interrotti")` e ha il suo `return`. Rischio esaminato: risoluzione del conflitto che rende il caso guasto irraggiungibile o che salta le asserzioni della V7b. Esito: ok. Prima viene verificato il formato «audio+testo+pezzi», poi il blocco del guasto con `return`. L'aggiunta `startsWith('errore')` nella `waitForFunction` serve per lo stato «errore: voce non disponibile».
- Contesto: `clients/voice/ascolto.py:388` chiede l'MP3 grezzo senza `X-Gas-Formato`, quindi l'ascolto continuo («voce H24» sul Mac, in main) non passa dal ramo pezzi. Esito: ok.
- Memoria: rispetto a HEAD nessuna riga tolta. Rispetto a MERGE_HEAD aggiunge solo le righe da #618-M2 a #622-M2 con le loro lezioni.

**Prove riprodotte:** `pytest tests/test_unit_voice_server.py tests/test_unit_voice_stt.py`, 183 passed in 4 min e 17 s, nessun test saltato (compresi quelli nel browser).

**Nota (non è una riserva):** risale alla V7b e non nasce dal merge. Nel ramo `!audio` (`riproduzione = null`) la lettura delle righe continua senza poter essere fermata da un turno nuovo. In teoria una riga «fine» in ritardo potrebbe riscrivere i tempi del turno dopo. In pratica il server manda la riga «fine» subito dopo la prima riga senza audio, quindi la finestra è trascurabile.

**Rischio escluso:** non ho provato il comportamento reale sul Mac (Safari/Chrome con ElevenLabs e Groq veri, concatenazione MP3 ascoltata): in questo ambiente non si riproduce. Non ho rieseguito i test fuori dalla voce (kernel, gate, avvisa_operatore, voce_ascolto), perché quei file sono identici a MERGE_HEAD, già verificata nella #650-M2.

**Memoria:** la riga #651-M2 è in coda a /home/user/Gas/.claude/agents/memoria_revisore.md ed è nello staging con il merge. `scripts/commit_memoria_revisore.sh` non ha fatto il commit perché a merge in corso git non permette un commit parziale («cannot do a partial commit during a merge»). Lo script ha scritto l'avviso in gas_debug.log ed è uscito con 0. La riga entra nel commit del merge.

Correzione del tipo (d1e9822). Review #652-M2:

## VERDETTO: APPROVATO

Review #652-M2 su feat/voce-v7b-m2, dopo i merge ee8b079 e 9f2046e. In staging c'è un solo file, modules/voice/server.py.

**Elementi del diff esaminati:**
- `modules/voice/server.py:395` — nel ramo `result_content is None`, `self._segna("cervello", t_cervello)` adesso sta sotto `if t_cervello is not None:`. Rischio esaminato: che la guardia faccia sparire il tempo del cervello in un caso reale. Esito: ok. Il comportamento non cambia: a questa riga si arriva solo se il `try` è finito senza eccezioni. Quindi `t_cervello = time.monotonic()` (riga 374) è sempre stato eseguito prima di `run_turn`, e la condizione è sempre vera. La modifica serve solo al tipo: un `Optional[float]` non arriva più a un parametro `float` (chiude la V-3 COSMETICA del bot).
- `modules/voice/server.py:388` — nel ramo eccezione c'è la stessa guardia `if t_cervello is not None`. Rischio esaminato: che i due rami del cervello siano trattati in modo diverso. Esito: ok, ora i due rami sono scritti allo stesso modo.
- Contesto: nessun antipattern della sez. 5 di CLAUDE.md. Il percorso d'errore resta fail-safe: risposta 500 dichiarata, mai un crash.

**Prova riprodotta:** `pytest tests/test_unit_voice_stt.py -k v7`, 11 passed. È compreso `test_v7_tempo_del_cervello_anche_senza_risposta`, il test che nella #649-M2 aveva bloccato il mutante su questo stesso ramo.

**Rischio escluso:** questa volta non ho rieseguito la suite completa della voce, compresi i test nel browser. Il diff è di una sola guardia sempre vera, non tocca né la pagina né il percorso NDJSON, e quella suite è passata nella #651-M2 (183 passed). Non ho verificato con un type checker (mypy) che la V-3 sia davvero chiusa: lo strumento non fa parte del flusso del repo.

**Memoria:** la riga #652-M2 è scritta in /home/user/Gas/.claude/agents/memoria_revisore.md ed è committata da sola con `scripts/commit_memoria_revisore.sh` (commit 1fd1f5a). `modules/voice/server.py` resta in staging e non è committato.

(La review #651-M2 del merge precedente era già stata consegnata con APPROVATO. La sua riga in memoria è entrata nel commit di merge ee8b079.)

Correzione delle note del bot su a73916a (1196be7). Review #653-M2:

## VERDETTO: APPROVATO

Review #653-M2. Branch feat/voce-v7b-m2 (PR #325). Ho esaminato il diff staged con `git diff --cached`: 3 file, 34 righe aggiunte e 4 tolte. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md e la memoria del revisore.

Elementi del diff esaminati:
- `tests/test_unit_voice_server.py:1342` — patch di `_PARLATO_MAX_FRASI` a 6 (V-1). Rischio esaminato: la patch potrebbe non agire, perché è una costante di modulo. `frasi_parlate` però la legge come globale al momento della chiamata (modules/voice/server.py:179), quindi la patch ha effetto. Mutante riprodotto: ho fatto restituire `True` a `riga()` anche a client chiuso (modules/voice/server.py:484). Risultato: `assert 6 <= 3`, 1 failed. Il margine ora è netto (6 contro ≤3, non più una sola sintesi). Ho ripristinato il file dall'index. Esito: ok.
- `clients/voice/browser_server.py:207` — invio degli header di `_copia_righe` dentro try/except OSError, con log.warning e return (V-3). Rischio esaminato: un'eccezione degli header che risale fino all'`except (ConnectionRefusedError, OSError)` di `_proxy_voice` (clients/voice/browser_server.py:162, contesto) e dà un 502 falso. Ora si ferma prima. Il `finally` di `_inoltra_a_pezzi` (clients/voice/browser_server.py:203, contesto) chiude comunque `resp`, quindi il server voce non resta appeso. Mutante: con browser_server.py di HEAD il test nuovo (tests/test_unit_voice_server.py:1361) dà 1 failed; ripristinato dall'index. Esito: ok.
- `clients/voice/browser_client.html:651` — `if (righe) righe.chiudi();` nel catch «risposta non leggibile» (V-2). Rischio esaminato: `righe` non definita, oppure `chiudi` che lancia un'eccezione. `righe` è dichiarata con `let ... righe = null` prima del try (clients/voice/browser_client.html:633). `chiudi()` è già protetto da try/catch (clients/voice/browser_client.html:701). Esito: ok.
- `clients/voice/browser_client.html:718` — `console.warn` per un `errore_voce` arrivato dopo la prima riga (V-4 COSMETICA). Il controllo su typeof e sul valore non vuoto evita stampe vuote. Il testo a schermo non cambia. Esito: ok.

Prove: test_unit_voice_server + test_unit_voice_stt, 184 passed riprodotti (test del browser compresi). Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. Il diff non tocca kernel, provider, `_get_window` né i tetti.

Rischio escluso: non ho verificato il comportamento reale nel browser (Safari/Chrome sul Mac) di `reader.cancel()` nel catch, né la chiusura vera del TCP verso il server voce in quel ramo. Non si può riprodurre in questo ambiente senza browser. Lo copre solo la logica del codice e la prova manuale dell'operatore.

Memoria: riga contatore #653-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (fc1b96c). L'index del diff sotto review è intatto (3 file). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py` + `tests/test_unit_voice_stt.py`: 183 passed (browser obbligatorio, `GAS_TEST_BROWSER_OBBLIGATORIO=1`) dopo l'allineamento alla V7a; -k v7 di test_unit_voice_stt 11 passed dopo la #652-M2. I test nuovi della V7b stanno in `tests/test_unit_voice_server.py` (formato a pezzi nel server, proxy che inoltra le righe e chiude a monte, pagina nel browser coi modi «pezzi» e «pezzi_interrotti»). Dopo la #653-M2: 184 passed (test nuovo `test_v7b_pagina_chiusa_prima_degli_header`, mutante → 1 failed; tetto delle frasi a 6 nel test della sintesi fermata, mutante → 6 sintesi). Kernel non toccato dalla fetta (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette dall'integrazione GitHub.
- a73916a: handoff-check e smista success; suite completate (notifica check_suite.completed); verifica-bot: primo avvio annullato, secondo APPROVATO CON RISERVE.
- 1196be7 (correzione), fc1b96c (memoria) e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- Dopo un guasto restano visibili testo e player della risposta precedente sotto i tempi nuovi; nessun test per il guasto dopo un turno riuscito né per un vero errore di rete (V-2 bot su 5d39333, BASSA).
- Nel ramo senza audio una riga «fine» in ritardo potrebbe in teoria riscrivere i tempi del turno dopo (nota della #651-M2; finestra trascurabile).
- Eccezione MP3 non prevista senza tempo «voce» (preesistente).
