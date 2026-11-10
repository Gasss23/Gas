# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — voce: seguito più severo e risposte più brevi (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #365 (https://github.com/Gasss23/Gas/pull/365): da solo solo con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore (via M1).
2. PR #363 (terminale A, altra sessione di lavoro di questa chat): merge all'operatore (sicurezza).

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — seguito più severo (filtro lato server + istruzione)**: `FATTA` (1340aa0).
- **Fetta 2 — risposte a voce più brevi (una frase, tetto 800)**: `FATTA` (1340aa0).
- **R-744-1-M2, gravità media (risposte di una parola scartate)**: `FATTA` — chiusa prima del commit, review #746-M2.
- **Note BASSE di bot e verifica esterna #365 (V-2 copertura del ramo «forte», V-3 elenco stretto e accenti) e R-746-1/2-M2**: `FATTA` (d07fbdf, review #747-M2). NB: il check del bot su e0f8f31 era «failure» ma il verdetto testuale era APPROVATO CON RISERVE con sole BASSE: il parser ha letto come finding la citazione di una riserva già chiusa (falso failure noto, direzione sicura).
- **Merge di origin/main 2dd0e8c (#362) nel ramo**: `FATTA` — conflitti solo nei report e nella memoria; da main arrivano solo `reports/prova_r1_notte.md` e una riga di memoria (fuori dal perimetro di review). Chiude V-1 (gravità media, PR non mergeabile) della seconda verifica esterna #365.
- **Prova sul Mac col modello vero**: `DEFERITA` — non riproducibile qui.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 modules/voice/server.py            |  73 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  12 +++++++-----
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |   2 ++
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  28 ++++++++++++----------------
 tests/test_unit_voice_server.py    |  37 ++++++++++++++++++++++++++++++++++++-
 tests/test_unit_voice_stt.py       |  67 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
4ec82c5 Merge origin/main (#362) nella #365 — conflitti solo nei report e nella memoria, chiude V-1 verifica esterna #365 bis (chat M2)
588c450 docs(fine-task): voce #365 — note BASSE di bot e verifica esterna chiuse (review #747-M2), riserve aggiornate (chat M2)
d07fbdf fix(voce): seguito — elenco delle risposte brevi più largo con accenti normalizzati, copertura del ramo «forte» nel seguito, assert «Resto.»; chiude V-2/V-3 bot e verifica esterna #365, R-746-1/2-M2 — review #747-M2 (chat M2)
e0f8f31 docs(fine-task): voce — seguito più severo e risposte più brevi, PR #365; riserve del bot sulla #363 registrate (chat M2)
1340aa0 feat(voce): seguito più severo (frammenti di una parola chiusi senza cervello, istruzione «nel dubbio non è per te») e risposte a voce più brevi (una frase, tetto 800) — review #744-M2, #746-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #747-M2 (correzioni BASSE di bot, verifica esterna e #746, commit d07fbdf) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #747-M2 sul diff staged di /home/user/Gas-voce (branch feat/voce-filtro-m2, PR #365). Prima ho letto le parti obbligatorie: CLAUDE.md §5, le parti voce/M2 di stato_progetto.md e la memoria del revisore. Non ho trovato antipattern del Wall of Shame: nessuno slicing della history, nessun output di tool simulato, guardrail non toccati.

**Elementi del diff esaminati**
- `modules/voice/server.py:203` — `_senza_accenti`: NFKD seguito dalla rimozione dei caratteri combinanti. Viene applicata a tutto l'elenco, che diventa `_RISPOSTE_BREVI_NORM`. Rischi esaminati:
  - collisioni dopo la normalizzazione, per esempio «perché» e «perche»: sono innocue, finiscono tutte e due nel frozenset;
  - forme NFD: coperte da un test;
  - eccezioni: nessuna, perché `unicodedata` fa parte della libreria standard.
  - Esito: ok.
- `modules/voice/server.py:215` — la normalizzazione si applica anche alla trascrizione, prima di `\w+`. Rischio esaminato: che un solo lato normalizzato lasci passare «Lunedi» o «Perchè». Mutanti:
  - normalizzazione tolta dalla trascrizione: rosso;
  - controllo fatto sull'elenco non normalizzato: rosso.
  - Esito: ok.
- `modules/voice/server.py:85` — l'import di `unicodedata` sta fra `re` e `subprocess`, fuori dall'ordine alfabetico. Esito: riserva cosmetica.
- `modules/voice/server.py:190` — elenco allargato (sicuro, forse, stasera, numeri da 11 a 20, decine, cento, mille, ora/dopo/mai/sempre/niente/nulla/subito/adesso). Ho valutato se il filtro serve ancora. Sì: scarta ancora nomi, interiezioni («Ehm», «Mamma.», «Forte!») e tutte le parole fuori elenco. Però «Ora!», «Mai!», «Niente!», «Dopo» sono anche frammenti tipici della TV o della stanza, e adesso arrivano al cervello con la spesa di un turno. Esito: riserva **R-747-2-M2 (BASSA)**, un compromesso da scrivere nel commento o in stato_progetto. Non lo considero un blocco: nel seguito un falso «passa» costa un turno, un falso «scarta» perde la risposta dell'operatore.
- `tests/test_unit_voice_server.py:2410` — casi a parola singola (davvero di UNA sola parola, come chiedeva la lezione del #746), forma NFD, «Resto.» da solo (R-746-2 chiusa) e i contro-esempi «Mamma.»/«Ehm». Esito: ok.
- `tests/test_unit_voice_stt.py:844` — test V-2 «Gas, forte.» nel seguito: si aspetta il comando `fine`, il contenuto vuoto, nessun turno. Mutanti:
  - tolto il ramo `elif self._seguito()` di «uso»: rosso, ok;
  - filtro esteso a ≤2 parole, così «Gas, forte.» viene scartato dal filtro prima del ramo «uso»: **il test V-2 da solo resta VERDE**. I due rami danno la stessa risposta (`_chiudi_seguito`, `modules/voice/server.py:996`), quindi il test non prova di aver superato il filtro. Quel mutante lo prendono comunque altri test della suite (rosso). Esito: riserva **R-747-1-M2 (BASSA)**: aggiungere un'osservazione del percorso, per esempio caplog che verifica l'assenza di «seguito scartato senza cervello» oppure una spia su `cervello_voce`.

**Esecuzione**
- pytest su voice_server + voice_stt con `-k "not browser"`: 276 passed, l'ho riprodotto io.
- 4 mutanti, tutti rossi sulla suite.
- Ho ripristinato `server.py` dopo ogni mutante: alla fine ci sono solo le modifiche staged e nessuna modifica non staged.

**Rischio escluso**
- Non ho verificato il comportamento con trascrizioni reali di Whisper (accenti sul Mac o sulla VPS, come scrive «perchè»): non è riproducibile in dev, i test usano stringhe fisse.
- Non ho controllato ligature o caratteri compatibili che NFKD trasforma in più lettere: è un caso marginale, al massimo un frammento passa al cervello.

**Riserve da tracciare in stato_progetto.md**
1. R-747-1-M2 (BASSA): il test V-2 non distingue il ramo «uso» dallo scarto del filtro.
2. R-747-2-M2 (BASSA): «ora/dopo/mai/sempre/niente/nulla/subito/adesso» in elenco fanno passare al cervello anche i frammenti della TV. Dichiarare il compromesso o toglierle.
3. Cosmetica: l'ordine dell'import di `unicodedata`.

**Memoria**
- Riga contatore #747-M2 e una lezione aggiunte in /home/user/Gas-voce/.claude/agents/memoria_revisore.md e messe in stage con `git -C /home/user/Gas-voce add`.
- Nessun commit, come chiesto: lo script `commit_memoria_revisore.sh` non l'ho eseguito.
- Un ciclo di attesa che avevo lanciato in background (b3fgnx8h1) è rimasto appeso: è innocuo e si chiude da solo al timeout.

### Review #744-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #744-M2. Ho esaminato il diff in staging nel worktree /home/user/Gas-voce (branch feat/voce-filtro-m2). Letture fatte: CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (letto in modo mirato), memoria del revisore.

**Elementi del diff esaminati**
- `modules/voice/server.py:188` — `seguito_da_scartare`: cerca le parole con `\w+` sul testo minuscolo, unicode, quindi «sì» con l'accento viene riconosciuto. Scarta se non ci sono parole oppure se c'è una sola parola fuori dall'elenco. Rischi esaminati: input vuoto, solo punteggiatura, apostrofi («D'accordo» conta 2 parole e passa), «Sì sì» passa. Nessuna eccezione possibile: tipi a posto, nessun crash. Esito: ok.
- `modules/voice/server.py:753` — punto della chiamata. Ordine dei filtri: pausa (`_SOLO_PAUSA`, che copre anche «basta»), poi attivazione, poi frammento, poi `cervello_voce` (forte). Vale solo per il parlato nel seguito, perché `_seguito()` richiede `_parlato`; il percorso JSON/testo non è toccato. «Forte!» nel seguito ora lo chiude il filtro invece del ramo «uso», ma l'esito è lo stesso (`_chiudi_seguito`, comando fine, nessun turno). Nessuna spesa del cervello per i frammenti. Esito: ok.
- `modules/voice/server.py:182` — `_RISPOSTE_BREVI_SEGUITO`. Rischio esaminato: risposte legittime perse. «Sì.», «No!», «Grazie.», «Perché?», «Ok» passano. Però «Continua», «Avanti», «Tre», «3», «Domani», «Marco», «Bene» vengono scartati: verificato eseguendo la funzione. Esito: riserva R-744-1-M2.
- `modules/voice/server.py:219` — tetto del parlato 1500→800; docstring di `frasi_voce` aggiornata a «800 + 1 + 37». Nessun altro uso della costante fuori dal modulo. Esito: ok.
- `modules/voice/server.py:246` — `ISTRUZIONE_VOCE` e `ISTRUZIONE_VOCE_SCHERMO` chiedono «UNA frase breve»; la frase «mai più di due» resta. `modules/telegram/bot.py:985` (contesto, file non toccato) usa `istruzione_turno_voce(True)`: lì cambia solo il testo dell'istruzione, coerente. Esito: ok.
- `tests/test_unit_voice_stt.py:828` e `tests/test_unit_voice_stt.py:844` — test end-to-end via HTTP: i frammenti chiudono senza turno, le risposte brevi e le frasi arrivano al cervello in modo effimero, con la parola di attivazione «Mamma.» va al cervello. `tests/test_unit_voice_server.py:2392` è il test della funzione e dell'istruzione. Esito: ok.

**Mutanti** (tutti ripristinati, nessuna modifica fuori dallo staging rimasta)
1. Chiamata disattivata (`if False and …`): 1 failed (test_seguito_frammento_chiude_senza_cervello).
2. Tolto `self._seguito() and`, cioè filtro sempre attivo: 1 failed (test_seguito_frammento_con_attivazione_va_al_cervello).
3. Elenco ignorato (`return len(parole) == 1`): 2 failed.

Suite test_unit_voice_server, voice_stt, voice_tts, voice_contesto, telegram_voce, voce_ascolto e sottofondo con -k "not browser": **743 passed**, come dichiarato. Il file si chiama tests/test_unit_sottofondo.py.

**Riserve**
- **R-744-1-M2 (MEDIA)**: le risposte di una parola fuori elenco vengono scartate in silenzio e la conversazione si chiude. Il caso più forte: quando taglia, Gas stesso dice `_PARLATO_VOCE_RESTO` («C'è altro, chiedimi se vuoi il resto.», `modules/voice/server.py:221`). Col tetto a 800 succederà più spesso, e «Continua.» o «Avanti.» vengono buttati. Stesso problema per numeri, nomi e giorni dati in risposta a una domanda che Gas fa solo quando gli serve. Non c'è crash né un'azione sbagliata, la direzione è sicura, ma l'utente deve ripetere con la parola di attivazione. Correzione minima suggerita: aggiungere almeno «continua», «avanti», «altro», «resto», «procedi», «bene»; valutare anche le cifre e i numeri brevi.
- **R-744-2-M2 (BASSA, preesistente)**: «Grazie.», l'allucinazione tipica di Whisper sul silenzio, è in elenco e continua ad andare al cervello. Non è una regressione.

**Rischi esplicitamente esclusi**
- Non ho verificato se il modello rispetta davvero l'istruzione più severa (`[NON_PER_ME]` nel dubbio, una frase da circa venti parole): dipende dal comportamento del modello e non si può riprodurre nei test unitari senza chiamate reali.
- Non ho verificato l'effetto sul client H24 (Mani) di una chiusura del seguito più frequente: client fuori da questo diff.

**Memoria**: riga `#744-M2 — 2026-11-10 — APPROVATO CON RISERVE — …` più una lezione (una lista bianca va provata contro le frasi che Gas stesso invita a dire) aggiunte in coda a /home/user/Gas-voce/.claude/agents/memoria_revisore.md, messe in staging con `git add`. Nessun commit, come richiesto, quindi niente commit_memoria_revisore.sh.

### Review #746-M2 (seguito di #744-M2, correzione di R-744-1) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #746-M2: riguarda il diff in staging del worktree /home/user/Gas-voce, branch feat/voce-filtro-m2, con base 447195f. È il seguito della #744-M2.

**R-744-1-M2 (MEDIA) è CHIUSA.** «Continua.», «Avanti!», «Altro?», «Tre.», «3», «Domani.» e «Venerdì» ora arrivano al cervello. L'unico limite che resta, i nomi propri da soli, è scritto nel commento del codice.

Cosa ho controllato nel diff:
- `modules/voice/server.py:182`: `_RISPOSTE_BREVI_SEGUITO` ora contiene continua/prosegui/avanti/altro/resto/ancora/dimmi/bene, i giorni, i numeri da uno a dieci in parole e gli ordinali. Rischio esaminato: con una lista più larga il filtro potrebbe diventare inutile. Esito ok: ho provato a runtime e «Mamma.», «Allora…», «Comunque», «Forte!», «Ehm» e «Mh» vengono ancora scartati senza chiamare il cervello.
- `modules/voice/server.py:202-203`: con `and not parole[0].isdigit()` le cifre non si scartano più. Rischio esaminato: falsi positivi. Esito ok: «²» passa al cervello, ma è un caso innocuo.
- `modules/voice/server.py:762`: il filtro scatta solo nel seguito, cioè quando l'operatore parla senza dire prima la parola di attivazione (chiamata invariata rispetto alla #744). Rischio esaminato: un frammento detto dopo la parola di attivazione verrebbe scartato. Esito ok: il test `tests/test_unit_voice_stt.py:828` e quello successivo con attivazione verificano che quel frammento va comunque al cervello.
- `tests/test_unit_voice_server.py:2401`: casi nuovi che sotto R-744-1 venivano scartati e ora devono passare. Esito ok.
- `tests/test_unit_voice_server.py:2407`: assert su «Il resto.». Esito **riserva**: sono due parole, quindi la frase passa comunque e il test non prova che «resto» sia in elenco.

Mutanti (tutti uccisi, poi ripristinati con `git checkout` dall'index; lo staging è intatto):
1. Tolto il controllo `isdigit`: 1 test fallito.
2. Tolti continua/avanti/altro/resto dall'elenco: 1 test fallito.
3. Tolto venerdì: 1 test fallito.

Test: `pytest voice_server + voice_stt -k "not browser"` dà 275 passed, come dichiarato.

Riserve (vanno scritte in stato_progetto.md):
- **R-746-1-M2 (BASSA)**: i numeri in parole oltre «dieci» («Undici.», «Venti») vengono ancora scartati nel seguito.
- **R-746-2-M2 (BASSA)**: l'assert «Il resto.» a `tests/test_unit_voice_server.py:2407` non prova nulla, perché sono due parole. Va sostituito con «Resto.» da solo.

Nota: «Basta.», «Fine.», «Zitto» ed «Esci» vengono scartati, ma lo scarto chiude la conversazione, quindi l'esito è quello voluto.

Cosa NON ho verificato:
- Comportamento con il microfono vero e Whisper: non si riproduce in dev, perché la trascrizione è simulata con un patch.
- Prove col cervello reale: non riproducibili in dev, perché il kernel nei test è finto.
- Altre suite (telegram_voce, voce_ascolto, kernel): non le ho rilanciate, perché il diff tocca solo `server.py` e i due file di test.

Memoria: ho aggiunto la riga `#746-M2` e una lezione nuova in /home/user/Gas-voce/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git -C /home/user/Gas-voce add`. Lezione: nei test di una lista bianca «una parola sola», ogni caso deve essere davvero di una parola. Nessun commit fatto.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato. Test nuovi: `test_seguito_frammento_chiude_senza_cervello`, `test_seguito_frammento_con_attivazione_va_al_cervello`, `test_seguito_forte_che_supera_il_filtro_non_parla` (stt), `test_seguito_da_scartare_e_istruzione_severa`, `test_parlato_voce_tetto_piu_corto` (server).
- `python -m pytest -q tests/test_unit_voice_server.py tests/test_unit_voice_stt.py tests/test_unit_voice_tts.py tests/test_unit_voice_contesto.py tests/test_unit_telegram_voce.py tests/test_unit_voce_ascolto.py tests/test_unit_sottofondo.py -k "not browser"` sul commit d07fbdf:

```
744 passed, 25 deselected in 89.18s (0:01:29)
```

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud); esiti letti con lo strumento GitHub MCP:
- e0f8f31 (head precedente): handoff-check success; verifica-bot failure (falso failure del parser, vedi §1); unit-suite non letta a fine run.
- 1340aa0: nessuna run propria letta.
- d07fbdf: nessuna run su questo SHA (pushato insieme al commit di fine task).
- 588c450: handoff-check success; unit-suite e verifica-bot in corso alla seconda verifica esterna, poi superati dal nuovo push.
- Merge di main: nessuna run su questo SHA (pushato insieme al commit di fine task).
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-744-1-M2 (gravità media): CHIUSA (1340aa0, review #746-M2).
- R-746-1-M2 e R-746-2-M2 BASSE: CHIUSE (d07fbdf, review #747-M2).
- Bot e verifica esterna #365 V-2 e V-3 BASSE: CHIUSE (d07fbdf).
- R-744-2-M2 BASSA (preesistente): «Grazie.», allucinazione tipica di Whisper, va al cervello nel seguito.
- R-747-1-M2 BASSA: il test di «Gas, forte.» nel seguito non distingue il ramo «uso» dallo scarto del filtro (stessa risposta).
- R-747-2-M2 BASSA: «ora/dopo/mai/sempre/niente/nulla/subito/adesso» in elenco fanno passare al cervello anche frammenti della TV (compromesso: un falso «passa» costa un turno, un falso «scarta» perde la risposta dell'operatore).
- Cosmetica #747 (e V-5 della seconda verifica esterna #365): ordine dell'import di `unicodedata`.
- Seconda verifica esterna #365 (commento sulla PR, su 588c450): V-1 (gravità media, conflitto con main) CHIUSA col merge di main; V-2 BASSA (CI non conclusa) da rileggere sulla head nuova; V-3 BASSA (falso failure del parser, non riprodotto); V-4 BASSA («Ⅻ», «ﬁne» scartati dopo NFKD: marginale, dentro il limite dichiarato).
- Limite dichiarato: un nome proprio da solo nel seguito si scarta.
- Non verificato: il modello rispetta davvero «nel dubbio [NON_PER_ME]» e «una frase» (prova sul Mac).
