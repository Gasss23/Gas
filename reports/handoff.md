# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-30 — Voce V4: interruzione, «sì» subito, riassunto + dettaglio, tetto lato server, test della pagina in CI (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #313 (https://github.com/Gasss23/Gas/pull/313). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5088931155","url":"https://github.com/Gasss23/Gas/pull/313"}`); `gh` nel cloud non è autenticato. La mergia M1 se il bot dà APPROVATO pulito; con riserve M1 chiede il sì all'operatore.
2. Prova col microfono vero sul Mac, PRIMA cosa: che la voce di Gas dalle casse NON lo interrompa da sola (eco); se succede, `GAS_VOICE_INTERRUZIONE=0` nel `.env` (interruzione accesa di default per scelta dell'operatore). Poi un «sì» a voce normale detto subito, la TV accesa (R-584-1-M2).

---

## §1 SCOPE & ESITO FETTE

- **V4.1 — interruzione mentre Gas parla** (sì dell'operatore): `FATTA`.
- **V4.2 — «sì» detto subito** (V-1 bot #311 su c3079f4): `FATTA`.
- **V4.3 — riassunto + dettaglio** (V-1 bot #311 su a1a6a25): `FATTA`.
- **V4.4 — bip e microfono** (V-2 bot #311 su a1a6a25): `FATTA`.
- **V4.5 — tetto lato server** (V-2 ve #311 su a1a6a25): `FATTA`.
- **V4.6 — test della pagina obbligatori in CI** (V-2 bot #311, ok di M1 a ci.yml): `FATTA`.
- **Secondo giro — bot #313 su 2e8a125 NON approvata, V-1 MEDIA («sì» a volume medio detto subito)**: `FATTA` (a6de670, review #584-M2). V-2 BASSA (interruzione accesa, eco non provata): `SALTATA — accesa per scelta dell'operatore (M1), istruzione GAS_VOICE_INTERRUZIONE=0 nel §0`. Verifica esterna su 2e8a125 APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/313#issuecomment-6530181510).
- **V-5 bot #311 su c3079f4** (riserve non tracciate): `FATTA` (stato_progetto).
- **Review**: #580-M2 → R-580-1/2/3-M2 `FATTA`; #581-M2 → R-581-1-M2 `FATTA`, R-581-2-M2 `DEFERITA — BASSA, dichiarata`; #582-M2 BOCCIATO → R-582-1-M2 `FATTA`; #583-M2 → R-583-1-M2 `DEFERITA — COSMETICA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 ++++++++
 .github/workflows/ci.yml           |  14 ++++++++++++
 clients/voice/browser_client.html  | 135 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------
 clients/voice/browser_server.py    |   8 ++++++-
 modules/voice/server.py            |  60 +++++++++++++++++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  15 ++++++-------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   3 ++-
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  28 +++++++++++++-----------
 tests/test_unit_voice_server.py    |  76 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 tests/test_unit_voice_stt.py       |  41 +++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
a6de670 fix(voce): soglia del «sì» detto subito anche a volume medio (V-1 bot #313)
44df1db chore(revisore): memoria review #584 — APPROVATO CON RISERVE
2e8a125 docs(voce-v4): report di fine task (PR #313, review #580-#583-M2)
b7169f6 feat(voce): interruzione mentre Gas parla, «sì» subito, riassunto + dettaglio, tetto lato server, test pagina in CI (V4, chat M2)
74bc2f9 chore(revisore): memoria review #583 — APPROVATO CON RISERVE
1f015b7 chore(revisore): memoria review #582 — BOCCIATO
270a1eb chore(revisore): memoria review #581 — APPROVATO CON RISERVE
264dbe4 chore(revisore): memoria review #580 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit b7169f6 è stato rivisto in quattro passaggi (#580-#583-M2) e il commit a6de670 in uno (#584-M2, in fondo) sullo stesso diff staged (ogni passaggio dopo le correzioni del precedente; le citazioni dei primi tre si riferiscono al diff di quel momento e alcune righe a HEAD sono spostate). Verdetti integrali:

Review #580-M2 (primo passaggio):

## VERDETTO: APPROVATO CON RISERVE

Review #580-M2, diff staged su feat/voce-v4-m2. Letture fatte: CLAUDE.md, reports/stato_progetto.md (sezione voce V3/V4), memoria_revisore.md (lezioni del 2026-10-30 su macchina a stati, tetti e guardie dopo un await). gas.py e brains/ non sono toccati. Nel diff c'è anche clients/voice/browser_server.py (`/config` interruzione), che il brief non elencava.

**Elementi del diff esaminati**
- `clients/voice/browser_client.html:507` — `vigila(turno)`: il polling si ferma da solo se manca l'analyser, se il turno è cambiato o se la conversazione è chiusa. Quando scatta toglie i tre handler prima di `pause()`, quindi onpause non chiude la conversazione, poi mette `occupato=false` e chiama `riapri`. Rischio esaminato: corse con onended/onpause/onerror e timer rimasti accesi. `fermaVigilanza` è chiamata in onended, onerror, onpause, `chiudiConversazione` e `dopoRisposta`. Il riascolto dal player non la riaccende, perché gli handler sono già null. — ok
- `clients/voice/browser_client.html:638` — la vigilanza parte solo dopo `play()` riuscito, con `turno === numTurno && occupato`. Un ended o una pausa prima della risoluzione la escludono. Mutante che toglie questa riga: il test «interruzione» fallisce. — ok
- `clients/voice/browser_client.html:530` — `riapri` tiene il tetto dei turni. Ho controllato tutte le funzioni che chiamano `ascolta` (lezione 2026-10-30): il clic azzera il contatore; `dopoRisposta` chiama `ascolta` solo sotto il tetto, altrimenti `riapri`; `riapri` controlla il tetto. Il turno interrotto conta, con +1 in onstop. — ok
- `clients/voice/browser_client.html:475-477` — rumore di fondo come mediana dei campioni, con tetto a 2×sogliaMin. La voce ora viene riconosciuta anche nei primi 300 ms. Rischio esaminato: soglie in cascata. — **riserva R-580-1-M2 (MEDIA)**, vedi sotto
- `modules/voice/server.py:294` — tetto orario: i turni parlati recenti si contano prima di `run_turn`; il ramo 429 fa `return` e nessun turno del kernel parte. Il server è a thread singolo (HTTPServer), quindi niente corse. L'assegnazione `type(self).turni_parlati = …` crea una lista nuova e non tocca la lista della classe base, così i test sono isolati, ognuno con la sua sottoclasse. Mutante che toglie il `return`: `test_v4_tetto_orario_dei_turni_parlati` fallisce. — ok. Riserva **R-580-2-M2 (BASSA)**: il controllo sta DOPO lo STT (vedi sotto).
- `modules/voice/server.py:128` — `parte_parlata` divide il testo in due solo alla prima riga vuota. La ricorsione è profonda al massimo 1, perché il primo pezzo non contiene righe vuote. «Il resto è a schermo» non si duplica. Il dettaglio fatto solo di spazi viene ignorato. La funzione si usa solo nella risposta audio+testo (`modules/voice/server.py:353`). — ok
- `modules/voice/server.py:308` — `ISTRUZIONE_VOCE_SCHERMO` si usa solo con `X-Gas-Formato: audio+testo`. `ISTRUZIONE_VOCE` non parla più di schermo. — ok
- `.github/workflows/ci.yml:105` — il nuovo step installa playwright@1.63.0 e poi `playwright install --with-deps chromium`. Se fallisce, fallisce lo step e quindi il job: blocca, non lascia passare. Non può far passare lo step voce: non ha `continue-on-error` e NODE_PATH vive solo nell'env dello step voce. — ok
- `.github/workflows/ci.yml:121-122` — NODE_PATH più `GAS_TEST_BROWSER_OBBLIGATORIO=1`. Le due vie che prima saltavano il test diventano `pytest.fail` (`tests/test_unit_voice_server.py:936` e `tests/test_unit_voice_server.py:999`). Il sottoprocesso node eredita NODE_PATH. — ok
- `clients/voice/browser_client.html:410` — se la configurazione dell'AudioContext fallisce, `chiudiMicrofono` rilascia il microfono e la funzione restituisce false; il chiamante chiude la conversazione. — ok

**Esecuzione e sonde** (fatte su un export dell'index, mai sulla cartella di lavoro)
- Suite voce con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: **133 passed** (131 s): risultato riprodotto.
- Mutanti uccisi: chiamata `vigila` tolta → test interruzione fallisce; `return` del 429 tolto → test del tetto orario fallisce.
- **Sonda R-580-1-M2**: ho aggiunto un modo con la voce che interrompe ad ampiezza 0.1 (RMS circa 0.07: sopra `sogliaInterruzione` 0.06). Stati osservati: `'Gas parla' → 'mi hai interrotto · ti ascolto…' → 'conversazione chiusa (silenzio)'`, 1 sola POST. Gas viene zittito ma la frase va persa. Causa: quando `ascolta` parte la voce è già in corso, quindi i primi 300 ms sono tutti voce. Il rumore di fondo stimato arriva al tetto 0.03 e la soglia effettiva diventa 3×0.03 = **0.09**, più alta di quella d'interruzione 0.06. Ogni voce tra 0.06 e 0.09 RMS interrompe Gas ma non viene registrata. Non c'è crash, ma la funzione principale non funziona per voci di volume medio: le stesse dell'operatore al Mac. Correzione suggerita: quando l'ascolto riparte da un'interruzione, saltare la stima del rumore (o usare quella del turno prima, o partire già con `parlando=true`), oppure allineare le due soglie. Consiglio di chiuderla in questa fetta, prima della PR. La stessa sonda con un «sì» debole detto subito (ampiezza 0.1) è passata.

**Riserve**
1. **R-580-1-M2 (MEDIA)**: soglia d'interruzione (0.06) più bassa della soglia effettiva dell'ascolto che riparte subito dopo (0.09). Gas viene zittito e la frase va persa. Riprodotta (vedi sopra).
2. **R-580-2-M2 (BASSA)**: il 429 arriva dopo lo STT, quindi un client fuori controllo spende comunque Groq. Il ramo «uso» (forte senza richiesta) non passa dal tetto e spende TTS. Nessun turno del kernel parte in entrambi i casi, quindi l'obiettivo dichiarato è rispettato. Per risparmiare anche Groq il tetto andrebbe controllato prima di `_do_stt`.
3. **R-580-3-M2 (BASSA)**: `ord[Math.floor(n/2)]` è la mediana alta. Con 3 campioni su 6 di voce, la voce che inizia a metà della finestra di 300 ms diventa già il rumore di fondo. La mediana bassa (`(n-1)/2`) è più tollerante.

**Rischi esplicitamente non verificati**
- Eco reale della voce di Gas dagli altoparlanti del Mac: un'auto-interruzione è possibile se l'eco supera 0.06 nonostante echoCancellation. Non è riproducibile in Chromium headless, dove il microfono finto non riceve l'audio del player. È limitata (ascolto, poi chiusura per silenzio) e si spegne con `GAS_VOICE_INTERRUZIONE=0`. Va provata sul Mac.
- Il nuovo step CI non l'ho eseguito sul runner GitHub. Ho controllato solo la sintassi e la logica: il risultato reale si vedrà nella run CI della PR. Non ho verificato la provenienza delle dipendenze transitive di npm (manca un lockfile; la versione è fissata solo al primo livello).

- Memoria aggiornata: riga `#580-M2` con le riserve più una lezione sulle soglie in cascata, committata (264dbe4) con `scripts/commit_memoria_revisore.sh`.

File rilevanti: /home/user/Gas/clients/voice/browser_client.html, /home/user/Gas/modules/voice/server.py, /home/user/Gas/.github/workflows/ci.yml, /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/tests/test_unit_voice_stt.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #581-M2 (secondo passaggio):

## VERDETTO: APPROVATO CON RISERVE

Review #581-M2. È la ri-review del diff staged su feat/voce-v4-m2, cioè #580-M2 più le correzioni delle sue tre riserve. Prima ho letto CLAUDE.md (sez. 5, 8 e 10), reports/stato_progetto.md (voce V4, riga 600) e la coda di .claude/agents/memoria_revisore.md, compresa la lezione #580 sulle soglie in cascata.

**Delta rispetto a #580.** Ho confrontato il file staged con le copie #580 salvate nello scratchpad (page.orig e server.orig). Le uniche differenze sono quelle dichiarate. Nella pagina: `giaInVoce`, la mediana bassa e `riapri(msg, true)`. Nel server: il tetto spostato prima dello STT e l'helper `_turni_recenti`. Il resto della pagina, browser_server.py, ci.yml e le istruzioni voce sono identici a #580. Anche l'esito di `git diff --cached --check` è pulito.

**Citazioni dal diff:**
- `modules/voice/server.py:266` — controlla il tetto orario prima di `_do_stt`, quindi oltre il tetto Groq non viene chiamato. Rischio esaminato: le richieste «uso» potevano contare per il tetto o avviare un turno. Sonda con tetto 2: 5 richieste «Forte.» danno 200 e non contano; poi le richieste normali danno 200, 200, 429, con run_turn chiamato solo 2 volte; un «uso» oltre il tetto dà 429 con STT chiamato 0 volte. Il ramo «uso» (`modules/voice/server.py:288`) esce con `return` prima della registrazione. Esito: ok.
- `modules/voice/server.py:303` — registra l'istante del turno solo quando il turno va davvero a run_turn. `_turni_recenti` (`modules/voice/server.py:335`) filtra le richieste dell'ultima ora. Rischio esaminato: crescita della lista o conteggio di richieste fallite. La lista cresce solo sotto il tetto e un 429 non aggiunge niente. Il test `tests/test_unit_voice_stt.py:406` verifica `stt.call_count == 2` su 3 richieste. Esito: ok.
- `clients/voice/browser_client.html:472` — con `giaInVoce` la frase parte già «parlando» (voceDa = ultimaVoce = t0) e salta la stima del rumore (`clients/voice/browser_client.html:477`), quindi la soglia è sogliaMin. Questo chiude R-580-1-M2 (verificato da `tests/test_unit_voice_server.py:944`, ampiezza 0.1). Rischio esaminato, su tua richiesta: che `giaInVoce` faccia inviare una frase a una finestra silenziosa. **Succede.** Sonda con un colpo di 400 ms ad ampiezza 0.4 mentre Gas parla, poi silenzio: Gas si zittisce e partono 2 POST. Il secondo è un clip di circa 1,2 s quasi tutto silenzio, perché `parlando = true` salta anche `voceMinMs`. Esito: riserva R-581-1-M2. Per ragionamento, sulla pagina #580 la finestra dopo l'interruzione chiedeva voce nuova; non l'ho riprovato perché il classificatore ha negato la sovrascrittura temporanea del file.
- `clients/voice/browser_client.html:481` — mediana bassa, `ord[Math.floor((ord.length - 1) / 2)]`. Con un numero pari di campioni prende il valore più basso dei due centrali, e il tetto `sogliaMin*2` resta. Chiude R-580-3-M2. Esito: ok.
- `clients/voice/browser_client.html:542` — `riapri` passa `giaInVoce` solo da `vigila`. `dopoRisposta` chiama ancora `ascolta()` e `riapri(msg)` senza flag, e il tetto `maxTurni` si applica prima. Esito: ok.

**Prove:** suite voce con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: 134 passed, rifatte da me. Il file di sonda temporaneo in tests/ è stato rimosso; l'albero di lavoro è come prima.

**Riserve:**
- **R-581-1-M2 (BASSA, propongo di tracciarla):** con `giaInVoce` un rumore breve (oltre 300 ms sopra 0,06: tosse, porta, eco residua) interrompe Gas e invia da solo un clip quasi muto. Whisper può trascrivere testo inventato e far partire un turno. Argini già presenti: `maxTurni` (5) e il tetto orario lato server. Correzione suggerita: se nella nuova finestra non arriva nessun campione sopra soglia entro `silenzioMs`, scartare il clip (`scarta = true`) invece di inviarlo, oppure richiedere almeno qualche campione di voce dopo t0.
- **R-581-2-M2 (BASSA):** le richieste «uso» spendono una trascrizione Groq senza contare per il tetto. È voluto e oltre il tetto vengono bloccate, ma sotto il tetto un client rotto può ripeterle senza limite.

**Rischio escluso:** non ho verificato il comportamento reale con microfono, echo cancellation e Whisper sul Mac (quindi né se Whisper allucina davvero sul clip muto, né quanto spesso la tosse supera 0,06 per 300 ms): in dev il microfono è finto da file. Non ho verificato nemmeno la CI su GitHub (installazione di Playwright 1.63.0): non è riproducibile qui.

Memoria aggiornata con la riga contatore #581-M2 e una lezione nuova, committata a parte (270a1eb) con scripts/commit_memoria_revisore.sh.

File: /home/user/Gas/clients/voice/browser_client.html, /home/user/Gas/modules/voice/server.py, /home/user/Gas/tests/test_unit_voice_stt.py, /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #582-M2 (terzo passaggio):

## VERDETTO: BOCCIATO

Review #582-M2 su feat/voce-v4-m2, diff staged: è #581-M2 più la correzione di R-581-1-M2.

Ho fatto le tre letture obbligatorie: CLAUDE.md (sezioni 5, 8 e 10), reports/stato_progetto.md (righe sulla voce V3/V4, letto a pezzi) e la coda della memoria del revisore.

**Cosa è cambiato rispetto a #581.** Ho confrontato la pagina in staging con la copia salvata durante #581 (scratchpad bc6.html). Le differenze sono solo `voceDopoMs`, il ramo `scarta` con il riavvio dell'ascolto e la guardia della UI in `onstop`. Per i file Python e per il test ho usato la copia di #580. Le differenze sono tutte già viste in #581 (tetto prima dello STT, `_turni_recenti`, `stt.call_count == 2`), più il solo modo «colpo». `clients/voice/browser_server.py` e `.github/workflows/ci.yml` sono identici a #580. Lo staging non tocca né gas.py né brains/.

### Elementi del diff esaminati
- `clients/voice/browser_client.html:494` — se la frase partita da un'interruzione ha meno di `voceMinMs` di voce vera, il clip viene scartato (`scarta = true`, `recorder.stop()`) e l'ascolto riparte in modo normale (`clients/voice/browser_client.html:499`). Il riavvio è `ascolta()` senza `giaInVoce`, quindi non può ripetersi all'infinito. Non conta un turno e chiude per silenzio alla fine della finestra. Il tetto dei turni non viene aggirato perché non parte nessun invio. Rischio esaminato: corsa tra il riavvio e il vecchio recorder. Esito: **blocco**, vedi R-582-1-M2.
- `clients/voice/browser_client.html:441` — `chunks = []` riassegna un array GLOBALE (dichiarato a `clients/voice/browser_client.html:335`). `ondataavailable` (`clients/voice/browser_client.html:452`) scrive nell'array globale, non in uno del proprio recorder. Esito: **blocco**, è la causa di R-582-1-M2.
- `clients/voice/browser_client.html:454` — `onstop` aggiorna la UI solo se il `recorder` corrente non sta registrando. È corretto in tutti e due gli ordini: se il vecchio `onstop` arriva dopo che il nuovo recorder è partito, la UI non si spegne; se arriva prima, si spegne e il nuovo `start` la riaccende. Esito: ok.
- `clients/voice/browser_client.html:485` — `voceDopoMs += 50` solo sopra la soglia e solo dentro questo ascolto. Con `giaInVoce` il `pavimento` resta 0, quindi la soglia è `sogliaMin`. Esito: ok.
- `tests/test_unit_voice_server.py:946` e `tests/test_unit_voice_server.py:1028` — il modo «colpo» verifica 1 solo POST e «mi hai interrotto». Non prova però il caso «colpo seguito da una frase vera», che è proprio quello in cui si vede il bug. Esito: riserva, il test va esteso.

### R-582-1-M2 — MEDIA, bloccante
Il nuovo recorder parte dentro i microtask: dopo `await apriMicrofono()` il microfono è già aperto, quindi l'attesa è immediata. L'ultimo `dataavailable` del recorder appena fermato arriva invece come task successivo, cioè dopo `chunks = []`. Così la coda del clip scartato finisce in testa al clip nuovo.

Sonda in Chromium headless, con il proxy e il server finto del test: microfono «colpo di 400 ms, 1,6 s di silenzio, 1,2 s di voce vera».
- Il primo POST comincia con `1a45dfa3`, l'header EBML: è un file webm valido.
- Il secondo POST, cioè la frase vera, comincia con `8c8100f080fb03ff`. L'header EBML compare solo al byte 57–71 (varia tra i giri).
- `ffprobe` e `ffmpeg` sul secondo clip rispondono «EBML header parsing failed / Invalid data found when processing input».

Effetto: dopo un colpo di tosse mentre Gas parla, la frase vera che segue è indecodificabile, quindi si perde con un errore dello STT. È proprio lo scenario che la correzione voleva proteggere, e la correzione stessa crea il problema. Non c'è crash: il server risponde con un errore e la pagina resta viva. Il bug però è deterministico e sistemarlo costa poco.

Correzione richiesta:
1. Dare a ogni recorder il proprio array: in `ascolta()` un `const pezzi = []` usato da `ondataavailable` e dal `Blob` dentro `onstop`, oppure il riavvio lanciato da `onstop`, a vecchio recorder finito.
2. Aggiungere un modo di test «colpo_voce» (microfono `[(0.8,0),(1.5,0.4),(4.5,0),(0.4,0.4),(1.6,0),(1.2,0.4),(8,0)]`) che controlli 2 POST e che il corpo del secondo cominci con `1a45dfa3`. Va salvato anche il corpo nel server finto, oggi viene registrata solo la lunghezza.
3. Fare un mutante che rimette l'array globale: il nuovo test deve fallire.

### Riserva che resta
- R-581-2-M2 BASSA: le richieste «uso» spendono Groq senza contare per il tetto. Resta dichiarata come era.

### Test eseguiti
Con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: `-k "colpo or interruzione"` dà 3 passed. La suite completa da 135 passed dichiarata dall'agente non l'ho rilanciata per intero.

### Rischio esplicitamente escluso
- Non ho verificato il comportamento reale di Groq/Whisper sul clip corrotto (se rifiuta con un 400 o trascrive solo una parte): non l'ho chiamato per non spendere quota. La prova di corruzione è ffmpeg, cioè lo stesso tipo di decoder.
- Non ho verificato l'ordine degli eventi in Safari o Firefox, solo in Chromium.
- Sul Mac col microfono vero non è riproducibile qui.

### Note operative
- La sonda sta in /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/p582/test_p582.py e si lancia con `PYTHONPATH=/home/user/Gas` e `--rootdir=/home/user/Gas`.
- Durante la sonda ho scritto per errore un file c2.webm nella radice del repo. L'ho già cancellato e `git status` è pulito, a parte i file in staging e i report.
- La riga contatore #582-M2 e una lezione nuova sono in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (1f015b7). Il diff in staging non è stato toccato.
- Non creare il marcatore `segna_review_ok`: serve una nuova review dopo la correzione.

Review #583-M2 (quarto passaggio, diff finale committato in b7169f6):

## VERDETTO: APPROVATO CON RISERVE

Review #583-M2. Ho riesaminato il diff staged su feat/voce-v4-m2: è il diff #582-M2 più la sola correzione R-582-1-M2.

Letture obbligatorie fatte: CLAUDE.md (sez. 5), reports/stato_progetto.md (Grep mirato), coda di .claude/agents/memoria_revisore.md. Ho applicato la lezione #582: provare i primi byte del clip, non solo il numero di POST.

**Elementi del diff esaminati**
- `clients/voice/browser_client.html:443` — ogni chiamata ad `ascolta()` crea il suo `const pezzi = []`. La variabile globale `chunks` non c'è più (rispetto alla copia della pagina #582 il delta è solo questo, più il commento). Rischio esaminato: l'ultimo `dataavailable` del recorder scartato arriva dopo il riavvio sincrono a `clients/voice/browser_client.html:499-500`. Ora finisce nell'array del vecchio recorder, chiuso nella sua closure, e nessuno lo legge più. — ok
- `clients/voice/browser_client.html:454` — `ondataavailable` scrive in `pezzi`. `clients/voice/browser_client.html:459` crea il `Blob` da `pezzi`, dentro l'`onstop` dello stesso recorder. Rischio esaminato: un onstop che legge il buffer di un altro recorder. Non può succedere, ogni onstop vede solo il proprio. La guardia della UI a `clients/voice/browser_client.html:456` e lo `scarta` per singolo recorder a `clients/voice/browser_client.html:457` sono invariati rispetto a #582. — ok
- `tests/test_unit_voice_server.py:951` — nuovo modo «colpo_voce» (colpo di 400 ms, 1,6 s di silenzio, 1,2 s di voce). `tests/test_unit_voice_server.py:978` — il server finto registra i primi 4 byte di ogni corpo. `tests/test_unit_voice_server.py:1035` — ogni clip webm, in tutti i modi, deve iniziare con `1a45dfa3`. `tests/test_unit_voice_server.py:1036` — per «colpo_voce» servono 2 POST. Rischio esaminato: un test che non fallisce senza la correzione. Mutante: ho rimesso la pagina staged #582 (array globale) e «colpo_voce» dà 1 failed. Ripristinata, `cmp` col file staged identico. — ok
- `tests/test_unit_voice_server.py:1035` — il controllo EBML scatta solo se il Content-Type contiene «webm». In Chromium è così (il mutante lo prova), ma con un browser che registra in ogg/opus il controllo non verificherebbe niente e il test passerebbe comunque. — riserva (R-583-1-M2, COSMETICA)

**Prove eseguite**
- Ho rifatto la mia sonda #582 (colpo seguito da voce vera, modo interruzione) sulla pagina staged.
  - Esito: 2 POST, ed entrambi iniziano con `1a45dfa39f428681`, cioè l'header EBML al byte 0. Con la pagina #582 il secondo iniziava con `8c8100…`.
  - Il secondo clip si decodifica con ffmpeg senza errori. Dura 2,76 s, con voce tra 0,25 e 1,5 s (RMS circa 0,3).
  - Stati della pagina corretti: «mi hai interrotto · ti ascolto…», poi «parli», «invio», chiusura per silenzio. Nessun errore JS.
- R-582-1-M2 è CHIUSA.
- Test: tests/test_unit_voice_server.py + tests/test_unit_voice_stt.py con GAS_TEST_BROWSER_OBBLIGATORIO=1 danno **112 passed**. Con `-k voice` su tutta tests/ (include la tts) danno **138 passed**. Non ho riprodotto il conteggio 136 che dichiari; con `-k voice` ne passano di più, nessun fallimento.
- Nient'altro è cambiato rispetto a #582:
  - Sulla pagina: diff con la copia staged #582 (r582.html nello scratchpad), solo le 4 righe descritte.
  - Su modules/voice/server.py, clients/voice/browser_server.py, tests/test_unit_voice_stt.py e .github/workflows/ci.yml: l'ora di modifica è precedente alla copia #582, quindi non toccati dopo quella review.
  - Il test ha l'ora di modifica successiva, e il suo diff contiene solo le aggiunte per «colpo_voce» e i 4 byte.
  - gas.py non è nel diff.
- Wall of Shame: nessuno slicing della history, nessun output di tool simulato, guardrail del kernel non toccati.

**Riserve**
- R-583-1-M2 COSMETICA (nuova): il controllo dell'header EBML dipende dal Content-Type «webm» e con un altro formato il test passerebbe senza verificare niente. Basta registrarla.
- Restano aperte da #581, invariate: R-581-2-M2 BASSA (le richieste «uso» spendono Groq senza contare per il tetto).

**Rischio esplicitamente escluso**
- Non ho verificato il comportamento su Firefox e Safari, né con un microfono reale. Lì l'ordine tra l'ultimo `dataavailable` e `stop` può essere diverso, e il formato può essere ogg o mp4, dove il controllo EBML non scatta. In dev c'è solo Chromium headless con microfono finto da file. In ogni caso la correzione con buffer per singolo recorder non dipende dall'ordine degli eventi.
- Non ho verificato su un file vero se lo STT Groq trascrive il clip.
- Per gli altri file del diff, «invariati rispetto a #582» si basa sull'ora di modifica, non su un confronto byte per byte: per quei file non ho copie #582.

**Memoria**
Riga contatore `#583-M2` aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata col commit 74bc2f9, solo quel file; l'index staged resta intatto (6 file). Nessuna lezione nuova oltre a quella di #582.

File rilevanti:
- /home/user/Gas/clients/voice/browser_client.html
- /home/user/Gas/tests/test_unit_voice_server.py
- sonda: /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/p582/t583.py
- secondo clip catturato: /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratchpad/p582/c2.webm

Commit a6de670 — review #584-M2 (secondo giro, dopo il bot su 2e8a125), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #584-M2, diff staged su feat/voce-v4-m2 (PR #313), correzione per V-1 MEDIA del bot su 2e8a125. Letture fatte prima della review: CLAUDE.md sez. 5, reports/stato_progetto.md, .claude/agents/memoria_revisore.md. Il diff tocca solo il client vocale e il test: non tocca gli antipattern del Wall of Shame (né history né `_get_window`, nessuna simulazione di tool) né i guardrail del motore.

**Elementi del diff esaminati**
- `clients/voice/browser_client.html:433` — nuova funzione pura `sogliaDaCampioni`: senza campioni restituisce sogliaMin, altrimenti max(sogliaMin, 3 × min(mediana bassa, sogliaMin)). Rischio esaminato: che il tetto non chiuda davvero V-1. Ho controllato in node: con 6 campioni a 0,07 dà 0,045, con 0,03 e con 0,06 dà sempre 0,045, con 0,004 dà 0,015, con un array vuoto dà 0,015. La soglia resta quindi ≤ 0,045, sotto una voce media (0,07) e sotto la soglia di interruzione (`sogliaInterruzione` 0,06, `clients/voice/browser_client.html:321`). Esito: ok.
- `clients/voice/browser_client.html:489` — `ascolta()` raccoglie i campioni solo se `ora - t0 < 300 && !giaInVoce`, e a `clients/voice/browser_client.html:490` calcola la soglia a ogni tick. Rischio esaminato: che il refactor cambi il comportamento di prima. Ho confrontato i due percorsi:
  - con `giaInVoce`: prima `pavimento` restava 0, quindi soglia = sogliaMin; ora non ci sono campioni, quindi sogliaMin. Uguale.
  - dopo 300 ms: prima `pavimento` restava fermo; ora l'array smette di crescere e la soglia resta costante. Uguale.
  - al primo tick: il campione viene inserito prima del calcolo, come prima.
  - costo: ordinare circa 6 elementi ogni 50 ms è trascurabile. La funzione è dichiarata al livello più alto di uno `<script>` classico, quindi è globale e `page.evaluate` la raggiunge.

  Esito: ok.
- `clients/voice/browser_client.html:436` — tetto del pavimento abbassato da 2×sogliaMin a sogliaMin. Rischio esaminato: rigetto del rumore. Un rumore costante fino a circa 0,044 RMS (ventola, stanza normale: tipicamente 0,001–0,03) resta sotto la soglia. Sopra 0,045 invece il rumore viene preso per voce: la frase parte e si chiude solo a `maxFraseS` (`clients/voice/browser_client.html:499`), e una clip di rumore arriva a Whisper. Prima il rumore era tollerato fino a 0,09. È lo scambio inevitabile per chiudere V-1. Esito: riserva BASSA (R-584-1).
- `tests/test_unit_voice_server.py:910` — il test calcola la soglia dentro la pagina vera (voce media, rumore, vuoto); le asserzioni sono a `tests/test_unit_voice_server.py:1029` e `tests/test_unit_voice_server.py:1030`. Rischio esaminato: che il test non discrimini. Con il tetto riportato a 2×sogliaMin la soglia per la voce media sarebbe 0,09 ≥ 0,07 e il test fallirebbe: la mutazione dichiarata è coerente. L'uguaglianza esatta con 0,015 regge perché la funzione restituisce direttamente il letterale `CFG.sogliaMin` (max(0,015; 0,012)). Esito: ok.
- `tests/test_unit_voice_server.py:964` — il commento della modalità «sisubito» rimanda al controllo diretto. Hai dichiarato che il caso end-to-end «sì a voce media» non discrimina in headless: va bene come dichiarazione. Il test prova la funzione, non il collegamento con il ciclo di ascolto, che però ho verificato leggendo il codice qui sopra. Esito: ok.

**Riserve**
- **R-584-1 (BASSA)**: in una stanza con rumore costante ≥ 0,045 RMS l'ascolto tratta il rumore come voce. Ogni ascolto produce allora una frase lunga `maxFraseS`, che viene inviata e trascritta, con rischio che Whisper inventi testo. Da tracciare in stato_progetto.md e da verificare nella prova sul Mac (se Gas «sente» frasi da sole, il colpevole è la soglia).
- **Nota COSMETICA**: il commento a `clients/voice/browser_client.html:479` parla ancora di «un tetto» senza dire quale; ora il valore sta nel commento della funzione, quindi è accettabile.
- **V-2 bot (interruzione attiva di default)**: mantenuta per scelta dell'operatore, con l'istruzione GAS_VOICE_INTERRUZIONE=0 nelle istruzioni per il Mac. Nessuna obiezione.

**Rischi esplicitamente esclusi**
- Livelli RMS reali del microfono del Mac (voce media e rumore di stanza) non verificati: non riproducibili in dev, perché il dispositivo finto di Chromium non è un microfono vero. I valori 0,07 e 0,03 sono stime.
- Non ho rilanciato la suite vocale con GAS_TEST_BROWSER_OBBLIGATORIO=1. Mi fido dei 136 passed dichiarati; ho verificato solo l'aritmetica della funzione in node.

La riga contatore #584-M2 e una lezione nuova sono state aggiunte in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committate a parte (commit 44df1db, solo quel file; l'index del diff sotto review non è stato toccato).

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite (server+stt+tts) con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: 129 → 136 passed in locale (il revisore #583-M2 ne conta 138 con `-k voice` su tutta tests/). Giri della pagina vera in Chromium headless: 5 → 10 (nuovi: interruzione, interruzione media, colpo, colpo + voce, sì subito); ogni clip webm inviato deve cominciare con l'header EBML. Mutanti: ogni giro nuovo fallisce sulla pagina precedente (main per interruzione e sì subito; #580 per interruzione media; #581 per colpo; #582 per colpo + voce). In CI questi giri diventano obbligatori (step nuovo con Playwright 1.63.0). Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 264dbe4, 270a1eb, 1f015b7, 74bc2f9, b7169f6: pushati insieme prima dell'apertura della PR #313; nessuna run della PR su questi SHA.
- 2e8a125 (fine-task del primo giro): run CI 41104451129 (`unit-suite` e `handoff-check` success; step Playwright eseguito, voice suite 136 passed con i giri della pagina); check `verifica-bot` failure — bot NON approvata (V-1 MEDIA, chiusa in a6de670).
- 44df1db, a6de670 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme).

## §7 RISERVE APERTE

- **R-584-1-M2** BASSA — rumore costante ≥ 0,045 RMS preso per voce (frase lunga inviata): da provare sul Mac.
- **R-581-2-M2** BASSA — le richieste «uso» (forte senza richiesta) spendono una trascrizione Groq senza contare per il tetto orario.
- **R-583-1-M2** COSMETICA — il controllo dell'header vale solo per i clip webm (in Chromium lo sono).
- **R-576-1-M2** BASSA (da #311) — la guardia del permesso del microfono non ha un test.
- **R-576-3-M2** COSMETICA (da #311).
- **R-578-1-M2** BASSA (da #311) — un «sì» brevissimo va provato col microfono vero.
- Prova sul Mac: eco della voce di Gas (auto-interruzione), TV, «sì» brevissimo; Safari/Firefox non provati (formato e ordine degli eventi).
- Dipendenze transitive di Playwright in CI non fissate (nessun lockfile, versione fissata solo al primo livello).
