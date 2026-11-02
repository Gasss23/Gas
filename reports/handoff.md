# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Voce V9: rumore (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #327 (https://github.com/Gasss23/Gas/pull/327). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5128485283","url":"https://github.com/Gasss23/Gas/pull/327"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.
2. Sul Mac, dopo il merge: prova con ventola o TV; se Gas si zittisce da solo, `GAS_VOICE_AGC=0`.

---

## §1 SCOPE & ESITO FETTE

- **V9 — rumore**: `FATTA` (review #630–#631-M2).
- **Merge di main (V6, V7a, V7b, V8, #319–#323)**: `FATTA` (review #657-M2).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 clients/voice/browser_client.html  |  44 +++++++++++++++++++++++++++++++++++++++++---
 clients/voice/browser_server.py    |   5 ++++-
 reports/diff_sessione.md           |  16 ++++++----------
 reports/handoff.md                 | n/d
 reports/prova_voce_mac.md          |   1 +
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  17 +++++++----------
 tests/test_unit_voice_server.py    |  79 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
8819f4d docs(voce-v9): report di fine task (review #630–#631-M2, #657-M2)
69a03d2 Merge remote-tracking branch 'origin/main' into feat/voce-v9-m2
8484950 docs(voce): stato delle fette V7–V9 della chat M2 (rami a pila, riserve aperte)
31f1ee4 docs(voce-v9): guida Mac, rimedio GAS_VOICE_AGC=0 con ventola o TV
5a3011a feat(voce): V9 — rumore: microfono filtrato, soglia che segue il rumore di fondo, Gas non si zittisce da solo (chat M2)
196f345 chore(revisore): memoria review #631 — APPROVATO
704c0e3 chore(revisore): memoria review #630 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della V9 (5a3011a): due passaggi del revisore.

Review #630-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #630-M2: fetta V9 «rumore», branch feat/voce-v9-m2, diff staged di 3 file. Ho letto CLAUDE.md (sez. 5), le parti di reports/stato_progetto.md su R-584-1-M2 e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `clients/voice/browser_client.html:536` — calcola la soglia della voce come il massimo fra quella di prima e `sogliaFondo()`. Rischio esaminato: si perde il «sì» detto subito (V-1 bot #313)? No, la soglia può solo salire rispetto a prima, e i modi `sisubito` e `interruzione_media` passano. — ok
- `clients/voice/browser_client.html:466` — `sogliaFondo()`: 10° percentile × 2, vale dopo 30 campioni, tetto 0,2. Rischio esaminato: soglia infinita o sordità. Con meno di 30 campioni restituisce 0, e il tetto 0,2 fa sì che una voce sopra 0,2 RMS passi sempre. Il buffer è limitato a 60 campioni e ha sempre almeno 30 elementi quando viene indicizzato. — ok. Riserva sulle frasi lunghe (sotto).
- `clients/voice/browser_client.html:581` — grazia di 500 ms all'inizio della vigilanza, con `sopraDa` azzerato. Rischio esaminato: un'interruzione vera arriva in ritardo (al massimo circa 800 ms). È un compromesso dichiarato e accettabile. — ok
- `clients/voice/browser_client.html:584` — la vigilanza usa `sogliaInterruzione()`. **Mutante**: ho rimesso la soglia fissa `CFG.sogliaInterruzione` e `rumore_costante` PASSA lo stesso (1 passed). Ho poi ripristinato il file dall'index: lo staged è invariato, 3 file. — riserva
- `clients/voice/browser_client.html:424` — `getUserMedia` con `autoGainControl: CFG.agc` e `channelCount: 1`. `CFG.agc` viene da /config (`clients/voice/browser_client.html:890`) e vale dalla prossima apertura del microfono. Rischio esaminato: un clic prima che arrivi /config. In quel caso resta il default acceso, cioè il comportamento di prima. — ok
- `clients/voice/browser_server.py:88` — /config espone `agc`; `clients/voice/browser_server.py:367` lo legge da GAS_VOICE_AGC con la stessa grammatica di GAS_VOICE_INTERRUZIONE. Rischio esaminato: nessun segreto esposto, nessun crash. Ma la lettura di "0" come spento non ha test. — ok, nota bassa
- `tests/test_unit_voice_server.py:996` — scenario con ronzio 0,3 a 150 Hz più una frase, con AGC spento (`tests/test_unit_voice_server.py:1082`). Il controllo «una sola richiesta» è coperto dall'asserzione generale `len(ricevute) == 1`. I controlli sulla chiusura per silenzio e sui valori di `sogliaFondo`/`sogliaInterruzione` stanno in `tests/test_unit_voice_server.py:1137`. Nessuna simulazione dell'output di tool del motore: il microfono finto è un fixture del client. — ok

Test eseguiti col browser obbligatorio: `rumore_costante`, `sisubito`, `interruzione_media` e `config_e_finestra` → 4 passed. Ho rifatto solo il mutante della soglia d'interruzione; i mutanti dichiarati da te (fondo spento, grazia tolta) non li ho rifatti.

**Riserve (da tracciare in reports/stato_progetto.md)**
- **R-630-1-M2 BASSA** — `sogliaInterruzione()` è provata solo come funzione isolata, con `page.evaluate`. Nello scenario regge la sola grazia. Il commento del test a `tests/test_unit_voice_server.py:1137` le attribuisce entrambe le difese. Servono un modo di prova in cui il rumore superi 0,06 dopo la grazia, oppure un commento corretto.
- **R-630-2-M2 BASSA** — R-584-1-M2 è solo MITIGATA, non chiusa. Con l'AGC acceso, che è il default, il ronzio zittisce Gas: l'hai misurato tu. Il rimedio è manuale (GAS_VOICE_AGC=0 nella guida) e lo scenario con AGC acceso non è testato. Non è una regressione: anche prima il browser lasciava l'AGC acceso di default.
- **R-630-3-M2 BASSA** — frasi lunghe e continue. Che il 10° percentile cada sulle pause fra le parole è provato solo su una serie sintetica con il 25% di pause, non su voce reale. Va provato sul Mac insieme al rumore di TV o ventola. Manca anche un test sulla lettura di GAS_VOICE_AGC=0 in `clients/voice/browser_server.py:367`.

**Rischio escluso**
- Non ho verificato il comportamento reale di noiseSuppression, AGC ed eco sul Mac con un microfono vero e una TV: non si può riprodurre in un Chromium headless con microfono finto da file. Valgono le misure che hai dichiarato tu.
- Non ho rieseguito la suite voce completa: ho fatto solo i 4 test mirati più il mutante. I «234 passed» sono una tua affermazione.

Guardrail: nessun tocco a `_get_window`, al tetto di 10 iterazioni, al tetto di 8k sull'output né ai provider. Nessuno slicing della history.

Memoria: aggiunte la riga #630-M2 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole con lo script (704c0e3). Il diff sotto review non l'ho committato.

Review #631-M2 (diff finale committato in 5a3011a):

## VERDETTO: APPROVATO

Ri-review #631-M2 dopo la #630-M2. Branch feat/voce-v9-m2, diff staged di 3 file; rispetto alla #630-M2 cambia solo il file dei test. Ho fatto le letture obbligatorie: CLAUDE.md (sezione 5), stato_progetto.md e la memoria del revisore. La #630-M2 suggeriva di provare le difese una alla volta, e l'ho fatto col mutante descritto sotto.

Elementi del diff esaminati:
- `tests/test_unit_voice_server.py:1139` — il commento dello scenario «rumore_costante» ora dice che lo scenario lo regge la grazia di 500 ms, mentre la soglia d'interruzione che sale col fondo è provata solo come funzione. Rischio esaminato: un commento che promette una copertura che non c'è (era il mutante sopravvissuto della #630-M2). Esito: ok. **R-630-1-M2 la accetto come chiusa-dichiarata.** La spiegazione regge: con il finto microfono e la noiseSuppression, dopo la grazia il ronzio scende a circa 0,02-0,03 RMS, quindi un rumore stabile sopra 0,06 non si costruisce. Il limite resta: nessuno scenario completo prova che la soglia d'interruzione salga col fondo. Va scritto così in stato_progetto.
- `tests/test_unit_voice_server.py:1414` — nuovo test parametrico su `run_browser_server`: valore assente, «1» e «sì» tengono acceso il guadagno automatico del microfono (AGC); «0», «off» e «no» lo spengono. Il server finto lancia un'eccezione al momento della creazione, cioè dopo che il valore è stato impostato. Rischi esaminati:
  - contaminazione della classe fra un test e l'altro: esclusa, perché `_browser_server_module` ricarica il modulo da file ogni volta;
  - un'uscita anticipata prima della lettura del valore: esclusa, perché le variabili d'ambiente che potrebbero far uscire prima sono tolte col monkeypatch.

  Mutante sul codice provato (`clients/voice/browser_server.py:367` cambiato in `agc = True or …`): 3 failed su 6. Codice ripristinato dall'index, `git diff` del file vuoto. Esito: ok.
- `clients/voice/browser_server.py:367` — lettura di GAS_VOICE_AGC con gli stessi valori di spegnimento di GAS_VOICE_INTERRUZIONE. Rischio: valori inattesi, che lasciano acceso (default prudente). Esito: ok.
- `tests/test_unit_voice_server.py:1082` — scenario con AGC spento solo per «rumore_costante». Esito: ok, coerente con la riserva R-630-2-M2.

Esecuzione: 6 passed sul nuovo test; suite completa `tests/test_unit_voice_server.py` 97 passed (242 s).

Riserve aperte e rischi esclusi:
- **R-630-2-M2 (BASSA)**: resta MITIGATA, non chiusa. Con l'AGC acceso, che è il default, lo scenario col ronzio non è testato; il rimedio è manuale (GAS_VOICE_AGC=0). Va scritta in stato_progetto come dici tu.
- Non verificato: il comportamento con voce vera e frasi lunghe sul Mac (resto di R-630-3-M2), non riproducibile qui senza microfono reale; va nei report come prova da fare all'operatore.
- Non verificato: il valore «false» di GAS_VOICE_AGC non è nel parametrico (nota COSMETICA, è coperto dalla stessa tupla di «0», «off» e «no»).

Memoria: riga #631-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, nessuna lezione nuova. `commit_memoria_revisore.sh` eseguito: ha committato solo quel file, l'index staged dei 3 file è intatto. Non ho committato altro.

Merge di origin/main (69a03d2). Review #657-M2:

## VERDETTO: APPROVATO

Review #657-M2: merge di origin/main (29c7cee) in feat/voce-v9-m2. Tutto è staged e il merge è ancora in corso.

**Cosa ho controllato nel diff**
- Rispetto a origin/main restano solo i 6 file della V9 (125 righe aggiunte, 9 tolte): browser_client.html, browser_server.py, test, memoria, prova_voce_mac.md, stato. Gli altri file staged (gas.py, brains/, modules/, ecc.) arrivano da main e coincidono con origin/main.
- Nei file staged non ci sono marcatori di conflitto e `git diff --cached --check origin/main` non segnala nulla.

**Citazioni**
- `clients/voice/browser_client.html:579`: in `vigila()` c'è la grazia di 500 ms e la soglia d'interruzione che sale col rumore di fondo. Rischio esaminato: conflitto con la V7b, dove ogni frase arriva come pezzo separato e la grazia potrebbe ripartire a ogni pezzo. Esito ok: `vigila` è chiamata una sola volta per turno, al primo pezzo (`clients/voice/browser_client.html:848`). L'interruzione chiama ancora `lasciaRiproduzione()` (V7b), quindi le frasi che arrivano dopo non suonano.
- `clients/voice/browser_client.html:536`: in `ascolta()` la soglia è il massimo tra quella dei primi 300 ms e quella del rumore di fondo. Rischio esaminato: che la V9 rompa i rami V7a (tempi ed errori) o il riascolto V7b. Esito ok: la V9 aggiunge solo le righe del rumore di fondo; il resto del ciclo e lo scarto del rumore breve (R-581-1-M2) sono quelli di main.
- `clients/voice/browser_server.py:88`: `/config` ora porta anche `agc`. Rischio esaminato: perdere le guardie della V8 nell'unione automatica. Esito ok: il controllo su `/voci/elenco` e `/voci/libreria` con X-Gas-Pagina (`clients/voice/browser_server.py:100`) e il ramo POST `/voci/prova` e `/voci/aggiungi` (`clients/voice/browser_server.py:148`) sono intatti, e non è stato aggiunto nessun `do_OPTIONS`.
- `tests/test_unit_voice_server.py:947`: il conflitto è risolto bene. La guida JS restituisce sia `fondo` (V9) sia `tempiVisibili` (V7a), il parametrize contiene sia «guasto» sia «rumore_costante», e `esito["fondo"]` e `esito["tempi"]` vengono dallo stesso JSON. Esito ok.
- `tests/test_unit_voice_server.py:1471`: `test_v9_gas_voice_agc` modifica `BrowserProxyHandler.agc` a livello di classe senza ripristinarlo. Con il parametrize l'ultimo caso («sì») lo riporta a True e i test del browser usano sottoclassi `_Proxy` che fissano `agc` da sé. Lo stesso schema esisteva già per `interruzione`. Esito ok, è una fragilità nota e non nuova.
- `reports/stato_progetto.md:607`: tenute le righe di main (V6, V7a, V7b, V8, R2, R-bot320-1), più la riga V9 con R-584-1-M2 MITIGATA, R-630-2-M2 e la parte aperta di R-630-3-M2, e le riserve BASSE di #318. Esito ok.

**Prove**: ho rieseguito voice_server, voice_stt e voice_prova_voci: 243 passed in 301 s, nessun test saltato, quindi i test col browser sono girati davvero.

**Rischio escluso**: il comportamento con rumore e voce veri sul Mac non l'ho verificato, perché in sviluppo non si riproduce (il microfono è finto, da file). Restano quindi aperte, come prima del merge, R-630-2-M2 (scenario con AGC acceso non testato) e la parte di R-630-3-M2 sulle frasi lunghe con voce vera.

**Memoria**: ho aggiunto la riga `#657-M2 — 2026-11-02 — APPROVATO — …` in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, senza lezioni nuove. Come richiesto l'ho lasciata nel file e non ho lanciato lo script di commit, perché il merge è in corso.

## §5 DELTA TEST DEL MOTORE

Dopo il merge di main: `tests/test_unit_voice_server.py` + `test_unit_voice_stt.py` + `test_unit_voice_prova_voci.py`: 243 passed (`GAS_TEST_BROWSER_OBBLIGATORIO=1`). I test nuovi stanno in `tests/test_unit_voice_server.py` (modo «rumore_costante» nel browser, `test_v9_gas_voice_agc`). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud. Commit della sessione (fino a 8819f4d, pushati insieme: run sulla sola testa, non letta alla scrittura) e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- R-630-2-M2: lo scenario con AGC acceso e rumore non è testato (microfono finto).
- R-630-3-M2 (resto): frasi lunghe con voce vera e rumore: da provare sul Mac.
- `test_v9_gas_voice_agc` cambia `BrowserProxyHandler.agc` a livello di classe senza ripristinarlo (fragilità nota, stesso schema di `interruzione`).
