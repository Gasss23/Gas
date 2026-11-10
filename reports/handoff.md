# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — chat Mani: ascolto H24, meno attivazioni per sbaglio (Jarvis rispondeva senza essere chiamato) + correzione della V-1 MEDIA della verifica esterna #361 + merge di main (PR #360) per togliere il conflitto

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #361 (https://github.com/Gasss23/Gas/pull/361): M1 riporta il sì dell'operatore se restano solo riserve BASSE; con un verdetto non pulito l'agente chiede comunque conferma in chat prima di mergiare. Dopo il merge va provato dal vivo sul Mac che «Hey Jarvis» scatti ancora (R-736-1); se non scatta, aggiungere `GAS_ASCOLTO_BLOCCHI_PAROLA=1` nel .env.

---

## §1 SCOPE & ESITO FETTE

- **PR #359 (voce di Telegram in un thread)**: `FATTA` — mergiata (695b759) col sì esplicito dell'operatore.
- **Ascolto H24, meno attivazioni per sbaglio**: `FATTA` — review #736 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).
- **V-1 MEDIA della verifica esterna #361 (nella finestra la parola valeva con 1 solo blocco)**: `FATTA` — bc37ae5, review #737 APPROVATO CON RISERVE poi #738 APPROVATO (R-737-1 chiusa con test e mutanti).
- **V-1 MEDIA della verifica esterna #361, 2° giro (PR in conflitto con main)**: `FATTA` — a13f442, merge di origin/main 447195f (PR #360); conflitti solo nei report (memoria unione, report del nostro lato), review #739 APPROVATO.
- **V-1 della verifica esterna #359 (log degli errori del thread della voce)**: `DEFERITA — prossima fetta voce, come deciso dall'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 clients/voice/ascolto.py           |  76 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
 reports/diff_sessione.md           |  15 +++++++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  26 +++++++++++++++-----------
 scripts/voce/LEGGIMI.md            |  15 ++++++++-------
 tests/test_unit_voce_ascolto.py    | 130 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale. Base = merge-base con origin/main dopo il merge a13f442 (447195f).

## §3 GIT LOG --ONELINE (sessione)

```
a13f442 merge: origin/main (PR #360) in claude/peaceful-lovelace-0w2b7q — conflitti solo nei report, review #739
0e5291c docs(fine-task): V-1 della verifica esterna #361 chiusa — PR #361
bc37ae5 fix(voce): anche nella finestra la parola vale solo con 2 blocchi di fila — V-1 verifica esterna #361, review #737/#738
0d36e37 chore(revisore): memoria review #738 — APPROVATO
4a78ffa chore(revisore): memoria review #737 — APPROVATO CON RISERVE
f142023 docs(fine-task): numero della PR #361 in stato_progetto
3835a14 docs(fine-task): ascolto H24 meno attivazioni per sbaglio — PR #361
1a031ae fix(voce): l'ascolto risponde meno senza essere chiamato — finestra 15 s, al massimo 2 seguiti, parola su 2 blocchi di fila, soglia 0,6, coda dell'eco ignorata — review #736
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1a031ae: verdetto integrale della review #736.

## VERDETTO: APPROVATO CON RISERVE

Review #736 (chat Mani). Ho letto il diff staged (`git diff --cached`, 3 file: clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py, scripts/voce/LEGGIMI.md) e l'ho verificato su una copia dell'index fatta con `git checkout-index -a --prefix=` nello scratchpad, senza stash. Prima ho letto CLAUDE.md sez. 5, reports/stato_progetto.md (voci voce/H24) e la coda della mia memoria.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:387` — `aspetta_parola` conta i blocchi di fila sopra soglia (`sopra`). Rischio: il conto non si azzera su un ramo e due picchi isolati sommati fanno scattare la parola. Ho guardato tutti i rami: eccezione → `sopra = 0` (:395), sotto soglia → `sopra = 0` (:412), NaN → `nan >= soglia` è False, quindi azzera. Il ramo dei «buoni di fila» dopo gli errori non tocca `sopra`. Esito: **ok**.
- `clients/voice/ascolto.py:409` — `return True` solo con `sopra >= self.blocchi_parola`. Il valore viene da `max(1, int(...))` (:349) e in main da `_numero(...,1,5)` (:1145): il valore 0 o negativo è impossibile, e inf/nan/abc tornano al default 2. Esito: **ok**.
- `clients/voice/ascolto.py:524` — `aspetta_voce` scarta prima `blocchi_per(0.5)` = 6 blocchi, poi parte la finestra. A fine flusso esce con None, senza crash. Questi blocchi NON passano a `_parola_nel_blocco`, ma il rilevatore è appena stato azzerato (`_azzera`, :756), quindi non perde stato utile. La finestra reale diventa 15,5 s. Il percorso dell'interruzione (:741-749) non passa da `aspetta_voce`, quindi lì la coda dell'eco non si applica, come dichiarato. Il microfono viene comunque svuotato a fine riproduzione (:636): la coda vale 0,5 s in tempo reale dopo la fine della voce di Gas. Esito: **ok**, con riserva R-736-2.
- `clients/voice/ascolto.py:328` e `clients/voice/ascolto.py:1154` — `MAX_TURNI_PREDEFINITO=3` è usato sia dal costruttore sia da main. Le interruzioni contano nei turni (R-668-1 resta valida) e una parola ripetuta nella finestra azzera il conto come prima. Esito: **ok**.
- `clients/voice/ascolto.py:1144` — la soglia predefinita in main passa a 0,6 e la finestra usa la stessa soglia (`_parola_nel_blocco`). L'interruzione resta a 0,7 e su un blocco solo. Esito: **ok**.
- `tests/test_unit_voce_ascolto.py:2513` e `tests/test_unit_voce_ascolto.py:2541` — test nuovi su: parola isolata contro 2 blocchi di fila, errore che azzera il conto, coda dell'eco e massimo 2 turni di seguito. Rischio: test che passano anche col codice rotto. Ho rifatto io due mutanti sulla copia dell'index: senza `sopra = 0` nel ramo sotto soglia → 1 test fallito; coda dell'eco a 0 → 1 test fallito. Suite completa: **300 passed**. Esito: **ok**.
- `scripts/voce/LEGGIMI.md:135` — tabella aggiornata (0.6, nuova riga BLOCCHI_PAROLA, 15, 3), coerente con il docstring di ascolto.py. Esito: **ok**.
- Contesto: `clients/voice/browser_server.py:73` — la pagina web tiene il suo default di 12 s e il diff non la tocca. Esito: **ok**.

**Wall of Shame**: nessuno slicing di cronologia, il diff è solo nel client voce e non tocca il kernel. Nessuna simulazione di tool. §9: le eccezioni del rilevatore restano intercettate e il loop di `gira` non cambia. I guardrail del kernel (10 iterazioni, `_get_window`) non sono toccati.

**Riserve (tutte BASSE)**
- **R-736-1**: non sappiamo se con 2 blocchi di fila la parola vera scatta ancora. Con un blocco da 1280 campioni openWakeWord dà un solo punteggio (:1104), e i rilevamenti veri di solito restano sopra soglia per più frame: la libreria stessa ha un parametro «patience» con la stessa logica. Ma qui non si può provare. Rimedio pronto: `GAS_ASCOLTO_BLOCCHI_PAROLA=1`. Va confermato dal vivo sul Mac.
- **R-736-2**: se l'operatore parla entro 0,5 s dalla fine della risposta, quel primo mezzo secondo non entra nella richiesta (può mancare la prima sillaba) e non viene ascoltato dal rilevatore. È un costo accettabile rispetto all'eco, ma non è scritto nel LEGGIMI.
- **R-736-3 (cosmetica)**: il default del costruttore resta `soglia=0.5`, quello di main è `SOGLIA_PREDEFINITA=0.6`. È voluto per i test e lo dichiari, ma chi crea `Ascolto` fuori da main riceve la soglia vecchia.

**Rischio escluso**: non ho verificato il comportamento reale col microfono e openWakeWord sul Mac (falsi positivi e negativi con TV o stanza): fuori dal Mac non si riproduce. Non ho verificato nemmeno la pagina web (browser_server.py), che non è nel diff.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree e NON in index, la riga `#736 (chat Mani) — 2026-11-10 — APPROVATO CON RISERVE — …` e una lezione: «un conto N blocchi di fila va azzerato su ogni ramo che non conferma; mutante per ramo». Come mi hai chiesto non ho lanciato `scripts/commit_memoria_revisore.sh`: il file resta da committare nel tuo fine-task. L'index è intatto (staged solo i 3 file sotto review).

Commit bc37ae5: verdetto integrale della review #737 (primo giro) e della re-review #738 (sul diff finale, che aggiunge solo il test per R-737-1).

## VERDETTO: APPROVATO CON RISERVE

Review #737. Ho letto prima CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (le voci sulla voce) e la mia memoria (lezione #736: un conto «N blocchi di fila» va azzerato su ogni ramo che non conferma, e ogni azzeramento va provato con un mutante). Ho lavorato su una copia dell'index nella cartella temporanea: con il codice staged la suite del file dà 302 passed.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:452` — il conto `_sopra_finestra` (righe 452-460) si azzera sotto soglia, sale di uno a ogni blocco sopra soglia, dà True solo quando arriva a `blocchi_parola` e allo scatto si azzera. Rischi guardati: NaN (`NaN >= soglia` è False, quindi azzera), `blocchi_parola` ≤ 0 (il costruttore a :349 lo porta a 1 con `max(1, …)`), predefinito 1 (si comporta come prima) — ok.
- `clients/voice/ascolto.py:444` — azzeramento nel ramo dell'eccezione, uguale a quello di `aspetta_parola` (clients/voice/ascolto.py:397); l'errore resta «no» e si logga come prima (§9) — ok, ma nessun test lo copre (riserva).
- `clients/voice/ascolto.py:538` — azzeramento all'inizio di `aspetta_voce`, dopo la coda dell'eco. Il conto NON si azzera tra `aspetta_voce` e `registra(rileva_parola=True)`, perché la chiamata in `conversazione` (clients/voice/ascolto.py:769-772) non fa altre letture in mezzo: una parola a cavallo dei due metodi vale, come richiesto. Se la parola è scattata nella finestra, `registra` parte con `rileva_parola=False` e il conto non si usa più — ok. Nessun test lo copre (riserva).
- `clients/voice/ascolto.py:487` — interazione con il taglio PRIMA_DELLA_PAROLA_S in `registra`. Ora la parola scatta sul 2° blocco. Il 1° blocco sopra soglia è già in `presi` (se c'era voce) e `presi[-tieni:]` lo tiene, quindi il taglio tiene ancora la parola. In `aspetta_voce` (:545-552) `da_parola` parte un blocco dopo (80 ms), trascurabile rispetto a PAROLA_VALIDA_S = 2 s — ok.
- `clients/voice/ascolto.py:767` — commento corretto da 0,5 a 0,6 (V-3) — ok.
- `tests/test_unit_voce_ascolto.py:2561` — picco isolato in attesa e in registrazione, e due picchi non di fila, con `blocchi_parola=2`. I mutanti «torna il comportamento vecchio (soglia di 1 blocco)» e «niente azzeramento sotto soglia» li prende (1 failed) — ok.
- `tests/test_unit_voce_ascolto.py:2578` — due blocchi di fila valgono come parola, nella finestra e a metà frase — ok.

**Riserve BASSE (da tracciare in stato_progetto.md)**
- R-737-1: tre mutanti NON vengono presi, la suite resta 302 passed:
  - tolto l'azzeramento all'inizio di `aspetta_voce` (:538);
  - tolto l'azzeramento sull'eccezione (:444);
  - tolto l'azzeramento quando la parola scatta (:458).

  Il codice è giusto, ma questi azzeramenti non hanno un test. Il caso reale per :538: un `registra` che finisce per tetto massimo (`max_s`) o per fine flusso con l'ultimo blocco sopra soglia lascia il conto a 1; senza l'azzeramento, nella finestra dopo basterebbe un solo picco. Servono test con un residuo lasciato dal giro prima e con un'eccezione tra due blocchi sopra soglia.

**Rischi esclusi**: non ho verificato l'efficacia reale dei 2 blocchi con openWakeWord sul microfono del Mac (non riproducibile qui, servono il modello vero e la stanza). Non ho controllato la doppia attivazione in `aspetta_voce` con 4 o più blocchi alti di fila: li ho giudicati innocui da lettura (riporta solo `da_parola` a 0), senza un test.

Nessun antipattern del Wall of Shame: il diff non tocca la history né simula l'output dei tool. Guardrail invariati (cap 10 iterazioni, `_get_window`).

Memoria aggiornata (riga #737 più una lezione) e committata da sola con `scripts/commit_memoria_revisore.sh`: commit 4a78ffa. File: /home/user/Gas/.claude/agents/memoria_revisore.md

## VERDETTO: APPROVATO

Re-review #738 del diff staged su claude/peaceful-lovelace-0w2b7q. Letture obbligatorie fatte: CLAUDE.md §5, reports/stato_progetto.md (selettiva), memoria_revisore.md (lezioni del 2026-11-10 su azzeramento per ramo e punto di ripartenza). Rispetto a #737 il diff aggiunge solo il test nuovo. ascolto.py resta come in #737.

Elementi del diff esaminati:
- `tests/test_unit_voce_ascolto.py:2588` — il test `test_conto_della_parola_nella_finestra_si_azzera` usa questa sequenza del rilevatore: alto, errore, alto, alto, alto, alto. Si aspetta i risultati [F, F, F, T, F, T]. Poi parte con un residuo `_sopra_finestra = 1` e fa un `aspetta_voce()`, dove la parola non deve risultare detta. Rischio esaminato: che il test non distingua i tre azzeramenti. Esito: ok. Ogni ramo ha la sua asserzione e i mutanti lo confermano (sotto).
- `clients/voice/ascolto.py:444` — azzera il conto quando il rilevatore va in errore. Mutante `pass`: il nuovo test fallisce (1 failed, 302 passed). Esito: ok.
- `clients/voice/ascolto.py:458` — azzera il conto quando la parola scatta. Mutante `pass`: il nuovo test fallisce. Esito: ok.
- `clients/voice/ascolto.py:538` — azzera il conto all'inizio di ogni finestra in `aspetta_voce`. Mutante `pass`: il nuovo test fallisce. Esito: ok. Questo applica la lezione di memoria «punto di ripartenza testato con un residuo».
- `clients/voice/ascolto.py:453` — azzera il conto sotto soglia. Mutante extra, non richiesto: lo prende `test_nella_finestra_un_picco_isolato_non_vale_come_parola`. Esito: ok.

Ho lavorato su una copia dell'index (`git checkout-index`, nella scratchpad). Base: 303 passed. Tutti e 4 i mutanti presi. `git diff --cached --check` pulito.

**R-737-1 è chiusa**: ognuno dei 4 azzeramenti di `_sopra_finestra` ha un test che fallisce se lo si toglie.

Cosa NON ho verificato:
- Se i 2 blocchi di fila funzionano davvero contro i falsi positivi del rilevatore reale. Si vede solo sul Mac col microfono, non qui; la riserva BASSA di #736 resta.
- La suite completa del kernel: il diff tocca solo il client voce e il suo file di test.

- Verdetto nullo: nessuno.

Memoria: riga contatore #738 aggiunta in fondo a /home/user/Gas/.claude/agents/memoria_revisore.md e committata dallo script (0d36e37). Nessuna lezione nuova.

Commit a13f442 (merge di origin/main): verdetto integrale della review #739 RIEMESSO dal revisore (stesso esito) perché il gate B rifiutava l'originale: dopo il merge la base è 447195f e le sue citazioni a modules/voice/server.py e tests/test_unit_voice_server.py non erano più file del diff. Il verdetto originale è riportato sotto, non ritoccato.

## VERDETTO: APPROVATO

Review #739 riemessa (chat Mani). Riguarda il merge di origin/main 447195f (PR #360 di M2) nel branch claude/peaceful-lovelace-0w2b7q, PR #361, ora committato come a13f442. Le verifiche e l'esito sono quelli di prima. Le citazioni ora puntano solo a file del diff della sessione (base 447195f), con le righe controllate su HEAD a13f442.

Cosa ho controllato:
- `clients/voice/ascolto.py:444` — azzeramento di `_sopra_finestra` sul ramo dell'eccezione (attributo dichiarato a `clients/voice/ascolto.py:364`). Rischio: che il merge abbia toccato la correzione V-1 già revisionata in #737/#738. Il file è identico al lato del branch prima del merge (0e5291c → HEAD: diff vuoto); durante il merge era identico a HEAD nello staging. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2589` — `test_conto_della_parola_nella_finestra_si_azzera`, il test che chiude R-737-1. Rischio: test del branch perso o mescolato. Il file è identico a 0e5291c (diff vuoto). Esito: ok.
- `scripts/voce/LEGGIMI.md:136` — riga di `GAS_ASCOLTO_BLOCCHI_PAROLA` (default 2, intervallo 1–5). Rischio: documentazione del branch sovrascritta dal lato main. Il file è identico a 0e5291c. Esito: ok.
- `.claude/agents/memoria_revisore.md:1416` — righe #736–#738 del nostro lato, conservate nell'unione accanto a #740-M2, #741-M2 e #742-M2 di main. Rischio: righe perse da uno dei due lati. Nello staging del merge: rispetto a main +6/0 e rispetto al vecchio HEAD +7/0, contando la mia riga #739 a `.claude/agents/memoria_revisore.md:1422`. Nessun marcatore di conflitto. Esito: ok.
- `reports/stato_progetto.md:686` — voce R8 «ascolto H24: meno attivazioni per sbaglio» della PR #361. Rischio: perdita della modifica di main nell'unione automatica. Durante il merge, rispetto a MERGE_HEAD restavano solo le 2 righe R8 del nostro lato, quindi la modifica di main resta. Esito: ok.

Controlli generali:
- Il codice arrivato da main (modules/voice/server.py, tests/test_unit_voice_server.py, reports/ripartenza_m2.md) era identico a MERGE_HEAD durante il merge. Dopo il commit non fa più parte del diff della sessione.
- I due lati toccano file di codice diversi (base 695b759). `git ls-files -u` era vuoto e `--check` pulito.
- Ho rilanciato `test_unit_voce_ascolto.py` e `test_unit_voice_server.py` con `-k "not browser"`: 463 passed, 25 deselected.
- Nessun antipattern del Wall of Shame: il merge non porta codice nuovo nel kernel.

Cosa NON ho verificato:
- La suite del kernel e test_unit_telegram_voce: il merge non tocca né gas.py né bot.py.
- I test con browser (25 deselected).
- Il comportamento dal vivo sul Mac: non riproducibile qui.

Come chiesto, non ho toccato né la memoria né lo staging. La riga #739 è già nel commit a13f442.

**Verdetto originale #739 (prima della riemissione), integrale in un blocco di testo (le sue citazioni di modules/ e tests/test_unit_voice_server.py non sono più nel diff della sessione):**

```text
## VERDETTO: APPROVATO

Review #739 (chat Mani). Ho controllato il merge di origin/main 447195f (PR #360 di M2) nel branch claude/peaceful-lovelace-0w2b7q (HEAD 0e5291c, PR #361). Il merge è ancora in corso e le modifiche sono in staging. Ho letto prima CLAUDE.md §5, le sezioni di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

Cosa ho controllato:
- `modules/voice/server.py:331` — cache delle frasi fisse portata dalla #360 di M2 (righe 331-345). Rischio: che il merge abbia alterato il codice di main. `git diff --cached MERGE_HEAD` su questo file è vuoto (0 righe). Esito: ok.
- `tests/test_unit_voice_server.py:2113` — test della cache alla seconda richiesta, arriva da main. Rischio: test di main persi o mescolati. Il file è identico a MERGE_HEAD (diff vuoto); lo è anche `reports/ripartenza_m2.md`. Esito: ok.
- `clients/voice/ascolto.py:452` — conto dei blocchi della parola nella finestra (`_sopra_finestra`), dal nostro branch. Rischio: che il merge abbia toccato la correzione già revisionata in #737/#738. Il file è identico a HEAD; lo sono anche `tests/test_unit_voce_ascolto.py`, `scripts/voce/LEGGIMI.md`, `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md`. Esito: ok.
- `.claude/agents/memoria_revisore.md:1416` — memoria risolta come unione dei due lati. Rischio: righe di uno dei due lati perse. Prima della mia riga: rispetto a main +5 righe e 0 tolte (le #736, #737, #738 e due lezioni); rispetto a HEAD +6 e 0 tolte (#740-M2, #741-M2, #742-M2 e le altre righe di M2). Nessun marcatore di conflitto. Esito: ok.
- `reports/stato_progetto.md:684` — unito in automatico da git. Rischio: perdita della modifica fatta su main. Rispetto a MERGE_HEAD restano solo le 2 righe R8 del nostro lato (stato della #359 aggiornato e voce della PR #361), quindi la modifica di main resta. Esito: ok.

Controlli generali:
- I due lati toccano file di codice diversi. Dalla base 695b759 main ha cambiato server.py e il suo test, il nostro lato ascolto.py, il suo test e LEGGIMI. Nessun file di codice è stato modificato da tutti e due.
- `git ls-files -u` è vuoto, `git diff --cached --check` è pulito, non ci sono modifiche fuori dallo staging.
- Ho rilanciato `test_unit_voce_ascolto.py` e `test_unit_voice_server.py` con `-k "not browser"`: 463 passed, 25 deselected. Torna col numero dichiarato.
- Nessun antipattern del Wall of Shame: il merge non porta codice nuovo nel kernel.

Cosa NON ho verificato:
- La suite del kernel (test_unit_kernel) e test_unit_telegram_voce: il merge non tocca né gas.py né bot.py, e #742-M2 ha già controllato che bot.py non usa la cache della #360.
- I test con browser (25 deselected).
- Il comportamento dal vivo sul Mac: non riproducibile qui.

Memoria: ho aggiunto la riga `#739 (chat Mani) — 2026-11-10 — APPROVATO — … Nessuna lezione nuova.` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git add`. Dopo l'aggiunta il file risulta +7/0 rispetto a HEAD e +6/0 rispetto a MERGE_HEAD; ls-files -u è ancora vuoto. Come chiesto, non ho lanciato scripts/commit_memoria_revisore.sh perché il merge è in corso.

Attenzione: lo staging è cambiato (c'è la riga di memoria in più). Il marcatore della review (`bash scripts/segna_review_ok.sh`) va creato adesso, sul diff in staging così com'è, prima del commit del merge.
```

## §5 DELTA TEST DEL MOTORE

Kernel non toccato. `tests/test_unit_voce_ascolto.py`: da 296 (base 695b759) a 303 casi (300 dopo 1a031ae, 303 dopo bc37ae5).

```
303 passed in 24.80s
```

Dopo il merge a13f442: `test_unit_voce_ascolto.py` + `test_unit_voice_server.py -k "not browser"` → `463 passed, 25 deselected`.

Mutanti presi su bc37ae5: soglia di 1 blocco nella finestra (comportamento vecchio), nessun azzeramento sotto soglia, su errore, allo scatto e all'inizio della finestra.
Suite completa del repo (su bc37ae5 meno l'ultimo test): `1 failed, 2976 passed` con `-x`; il fallito è `tests/test_unit_web_browser.py::test_testo_scritto_dal_javascript` (Chromium vero nel container cloud), fuori scope: il branch non tocca `modules/`. Fa fede la unit-suite della CI.

## §6 STATO CI

`gh` non autenticato nel container (GitHub passa dallo strumento MCP). Mappatura commit→run:
- 0e5291c (testa precedente della PR): handoff-check success, smista success; unit-suite e verifica in corso alla verifica esterna #361 (2° giro); la verifica-bot di bc37ae5 risulta cancelled (sostituita dal push successivo).
- 1a031ae, 3835a14, f142023, 4a78ffa, 0d36e37, bc37ae5: nessuna run conclusa su questo SHA (commit intermedi o sostituiti da push successivi).
- a13f442 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Verifica esterna #361 (2° giro, APPROVATO CON RISERVE): V-1 MEDIA (conflitto con main) CHIUSA in a13f442; V-2 BASSA (CI e bot non ancora verdi sull'head) da controllare prima del merge; V-3 BASSA = R-736-1; V-4 BASSA: clients/voice/browser_server.py tiene finestra 12 s e 5 turni (la modalità browser non riceve la correzione), prossima fetta voce; V-5 COSMETICA = R-736-3.
- Verifica esterna #361: V-1 MEDIA e V-3 CHIUSE in bc37ae5; V-2 BASSA (il revisore #736 non aveva visto la lacuna) superata; V-4 BASSA = R-736-1.
- R-737-1 BASSA: CHIUSA in #738.

- R-736-1 BASSA: con 2 blocchi di fila la parola vera scatta ancora? Da provare dal vivo; rimedio `GAS_ASCOLTO_BLOCCHI_PAROLA=1`.
- R-736-2 BASSA: chi parla entro 0,5 s dalla fine della risposta perde la prima sillaba.
- R-736-3 COSMETICA: il costruttore tiene soglia 0,5, main usa 0,6.
- Verifica esterna #359: V-1 BASSA, prossima fetta voce.
- R-733-1/2 e V-3 della verifica esterna #359: accettati dall'operatore come limite della guardia statica.
- Le altre riserve sono in `reports/stato_progetto.md`.
