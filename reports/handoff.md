# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 43 parte 2: finestra di 40 s e difese contro il parlato della stanza (PR #341)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #341 (https://github.com/Gasss23/Gas/pull/341): l'operatore ha detto sì (via M1), a condizione di CI verde e nessuna ALTA/MEDIA da bot e verifica esterna sul nuovo head. La #339 è in main da 3cde8a5, quindi l'ordine di merge (prima la #339, poi la #341) è rispettato. Su 7e4a7d3 il merge è stato rifiutato per conflitti con la PR #344 di M2, arrivata in main subito prima. Ho unito main (b874179, review #697 APPROVATO) e ora va ripetuto il giro CI + bot + verifica esterna su questo head.
2. Rischio di privacy da accettare esplicitamente (R-694-1, R-695-2; V-2 della verifica esterna su 7e4a7d3): nella finestra di 40 s il rilevatore della parola resta acceso a soglia 0,5. Un falso «Hey Jarvis» rende normale (senza il filtro «non per me» del server) il parlato della stanza che arriva entro circa 2 s, più circa 0,3–0,7 s di stanza prima della parola. L'alternativa è spegnere il rilevatore nella finestra; in quel caso, per fare una richiesta normale, si dice di nuovo «Hey Jarvis» dopo la fine della finestra.

---

## §1 SCOPE & ESITO FETTE

- **PR #340 (fetta 42)**: `FATTA` — mergiata (83f3bcd) col sì dell'operatore, CI verde; riserve nuove di bot e verifica esterna registrate.
- **Fetta 43 parte 2 — finestra di 40 s, turni di seguito con tetto 15 s, X-Gas-Seguito, comandi fine/pausa**: `FATTA` — review #676 APPROVATO CON RISERVE. Il commit di merge su main ha un diff identico a quello rivisto.
- **R-676-1/2 (test di stato e svuota dopo «fine»)**: `DEFERITA — BASSE, registrate, prossima fetta della voce`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  15 ++++++
 clients/voice/ascolto.py           | 195 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 reports/diff_sessione.md           |  15 +++---
 reports/stato_progetto.md          |   6 ++-
 reports/ultimo_report.md           |  65 ++++++++++++++++++++---
 scripts/voce/LEGGIMI.md            |  35 +++++++++---
 tests/test_unit_voce_ascolto.py    | 360 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 44dbe2d (dopo il merge della PR #344).

## §3 GIT LOG --ONELINE (sessione)

```
b874179 Merge origin/main (PR #344, fix claude-cli --effort di M2) nella PR #341 — review #697 APPROVATO
7e4a7d3 docs(fine-task): fetta 43 parte 2 — scadenza della parola, merge della #343, review #695–#696 (PR #341)
8c31f6e Merge origin/main (PR #343, voce rapida fetta 2) nella PR #341 — review #696 APPROVATO CON RISERVE
165a9a4 fix(voce): una parola sentita più di 2 s prima della voce non rende normale il turno (V-1 ve #341 su 562f137)
a1aa77b chore(revisore): memoria review #695 — APPROVATO CON RISERVE
562f137 docs(fine-task): fetta 43 parte 2 — V-1 del bot su 23d9c1c corretta, review #694 (PR #341)
01b1089 fix(voce): parola a metà di un turno di seguito — il parlato di prima non parte (V-1 bot #341 su 23d9c1c)
4e81502 chore(revisore): memoria review #694 — APPROVATO CON RISERVE
23d9c1c docs(fine-task): fetta 43 parte 2 — merge della #342, review #693, verdetti su bdc79ce (PR #341)
7296f39 Merge origin/main (PR #342, parser del bot) nella PR #341 — review #693 APPROVATO CON RISERVE
bdc79ce docs(fine-task): fetta 43 parte 2 — V-1 del bot corretta, review #680–#681 (PR #341)
1792ab3 fix(voce): la parola di attivazione detta nella finestra apre una richiesta normale (V-1 bot #341)
7669be5 chore(revisore): memoria review #681 — APPROVATO CON RISERVE
288c3f6 chore(revisore): memoria review #680 — APPROVATO CON RISERVE
851a0d1 docs(fine-task): fetta 43 parte 2 — merge della #339 e review #679 nella PR #341
ac06f01 Merge origin/main (PR #339, voce V15) nella PR #341 — review #679 APPROVATO CON RISERVE
a7ed0e8 docs(fine-task): fetta 43 parte 2 — ordine di merge dichiarato (la #341 dopo la #339, V-1 MEDIA della verifica esterna) e riserve registrate
43fa6ac docs(fine-task): fetta 43 parte 2 chat Mani — finestra di 40 s e difese, review #676, PR #341; PR #340 mergiata
51c4aa0 Merge branch 'mani/finestra' into claude/peaceful-lovelace-0w2b7q
4cd7b97 feat(voce): fetta 43 parte 2 — finestra di 40 s e difese contro il parlato della stanza
da24b2c chore(revisore): memoria review #676 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 4cd7b97 — review #676, verdetto integrale. Il commit 51c4aa0 (merge su main dopo la #340) ha un diff identico, verificato confrontando i diff:

## VERDETTO: APPROVATO CON RISERVE

Review #676 (chat Mani). Riguarda la fetta 43 parte 2, cioè le difese contro il parlato della stanza nel client di ascolto. Ho lavorato nel worktree /tmp/claude-0/wt43b sul diff staged (3 file: ascolto.py, LEGGIMI, test).

**Cosa ho controllato**
- Ho letto prima CLAUDE.md, stato_progetto.md e la mia memoria.
- Ho letto il server della #339 da origin/feat/voce-v12-m2:modules/voice/server.py.
- Ho fatto girare i test su una copia dell'index (non sul worktree): **248 passed**.
- Ho provato 4 mutanti miei sulla copia: 1 preso dai test, 3 no.
- Il codice del diff non contiene slicing della history né simulazione di tool.

**Citazioni**
- `clients/voice/ascolto.py:735` — se il server manda `X-Gas-Comando: fine`, l'invio restituisce `(True, None, "", "fine")` prima di guardare il Content-Type. Rischio: un JSON vuoto preso per un errore, con bip. Esito: ok. Torna col server della #339 (`_chiudi_seguito` risponde 200 con `{"content":"","fine":true}`, e `end_headers` mette l'intestazione in ogni formato). `_comando()` (riga 692) accetta solo «fine» e «pausa», e un'eccezione nella lettura diventa "".
- `clients/voice/ascolto.py:462` e `clients/voice/ascolto.py:508` — un errore o una risposta senza voce in un turno di seguito, o con «pausa», chiude senza bip. Dopo la parola il bip d'errore resta. Rischio: bip a ripetizione col forte spento (il server risponde 500 ai turni di seguito). Esito: ok. Anche i fake a 3 valori e gli esiti malformati vanno bene: l'IndexError o il TypeError finiscono nell'`except` (§9).
- `clients/voice/ascolto.py:627` — una registrazione di seguito che arriva al tetto (`registra(..., max_s=seguito_max_s)`) non si invia e chiude la conversazione. Rischio: soglia sbagliata di uno. Esito: ok, il mutante con `>` al posto di `>=` è preso dai test. Nota: il tetto conta anche gli 0,8 s di silenzio finale, quindi il parlato massimo che passa è circa 14,2 s. Va bene, nessuna azione.
- `clients/voice/ascolto.py:444` — `self.chiudi = False` all'inizio di ogni turno. Rischio: se l'azzeramento manca, la conversazione dopo un «fine» o una «pausa» si chiude dopo il primo turno, senza finestra. Esito: **riserva**. Il codice è giusto, ma il mutante «riga tolta» passa tutti i 248 test.
- `clients/voice/ascolto.py:458` — una «pausa» dopo la parola, con audio, deve chiudere. Esito: **riserva**. Il mutante `if comando == "pausa" and seguito` sopravvive: `tests/test_unit_voce_ascolto.py:520` prova solo la pausa di seguito e `tests/test_unit_voce_ascolto.py:527` solo quella senza audio. Con quel mutante «Hey Jarvis, pausa» suonerebbe «Va bene.» e lascerebbe la finestra aperta 40 s.
- Contesto, interruzione: dopo una parola che interrompe si torna a `seguito = False` e la registrazione torna a 30 s. Coperto dai due test sull'interruzione. Ok.
- `scripts/voce/LEGGIMI.md` — tabella e privacy aggiornate (40 s, 15 s, «pausa», chiusura in silenzio, audio a Groq dichiarato). Ok. «40 secondi senza che nessuno parli» è un'approssimazione: in realtà sono 40 s in cui non arrivano 0,24 s di voce continua. Non serve correggerlo.

**Riserve**
- **R-676-1 BASSA** — Due mutanti sulla gestione dello stato passano tutti i test:
  - `self.chiudi` non azzerato in `turno`;
  - «pausa» che chiude solo nei turni di seguito.

  Da aggiungere:
  - un test con due conversazioni di fila: «fine» nella prima, poi la seconda deve ancora aprire un turno di seguito;
  - un test «parola + pausa con audio»: tipi == ["parola"], niente seguito.
- **R-676-2 BASSA** — Il `self._svuota()` dopo «fine» (ascolto.py:461) non è coperto: il mutante che lo toglie passa. Asserire una chiamata a svuota in più nel test di «fine».
- **R-676-3 BASSA**, per M2, fuori da questo diff — Nel server della #339, una trascrizione incerta in un turno di seguito risponde a voce «Non ho capito» (`_rispondi_senza_turno(_NON_HO_CAPITO)` in `_do_stt`) e non chiude. Il rumore della stanza nella finestra può quindi produrre fino a 5 «Non ho capito» parlati. Il caso è da girare a M2: con `_seguito()` attivo il server dovrebbe chiudere con «fine».

**Privacy**: la finestra passa da 12 a 40 s, quindi la stanza è ascoltata più a lungo. In cambio ogni turno di seguito porta al massimo circa 15 s di audio invece di 30, il parlato lungo non parte, e il server usa solo il cervello forte e chiude se il parlato non era per Gas. Il saldo è a favore della privacy, ma ogni turno di seguito arriva comunque a Groq per la trascrizione prima che il cervello decida. È scritto nel LEGGIMI ed è una scelta dell'operatore.

**Cosa non ho verificato**
- Il comportamento vero sul Mac (microfono, openWakeWord, rumore reale della stanza): non si può riprodurre qui. I tempi sono provati solo con blocchi sintetici.
- L'integrazione end-to-end client ↔ server della #339: non l'ho fatta girare. Il contratto l'ho controllato leggendo il codice; il server finto dei test copre solo intestazioni e codici.
- flake8: non è installato nell'ambiente, quindi lo stile (E30x) non è controllato.

**Memoria**: aggiunta la riga #676 (chat Mani) e una lezione nuova (un flag di stato per turno va provato su due conversazioni di fila) in .claude/agents/memoria_revisore.md. Committata con lo script: commit da24b2c, solo quel file. Lo staged è identico a prima. Il marcatore non l'ho toccato.


Merge ac06f01 (main con la PR #339 dentro la PR #341) — review #679, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #679 (chat Mani): merge di origin/main 3cde8a5 (PR #339, V15 di M2) nel branch claude/peaceful-lovelace-0w2b7q (PR #341). Il merge è staged e non committato; il repo vero non l'ho toccato.

**Com'è stato fatto il merge (controllato blob per blob nell'index)**
- Uguali a MERGE_HEAD: gas.py, modules/voice/server.py, modules/voice/tts.py, tests/test_unit_kernel.py, tests/test_unit_voice_stt.py, tests/test_unit_voice_prova_voci.py, reports/ripartenza_m2.md.
- Uguali a HEAD: clients/voice/ascolto.py, scripts/voce/LEGGIMI.md, reports/handoff.md, reports/ultimo_report.md, reports/diff_sessione.md.
- `git ls-files -u` è vuoto e non ci sono marcatori di conflitto.
- Nessuno slicing della storia (`[-N:]`) nelle righe aggiunte; `_get_window` non è toccata.

**Elementi del diff esaminati**
- tests/test_unit_voce_ascolto.py:1098 — il finto `synthesize_speech` accetta `**kw` (il `timeout=` della conferma V15). Rischio esaminato: che il merge portasse altro dal lato main. Oltre a HEAD c'è solo questa riga e quella sotto. Esito: ok.
- tests/test_unit_voce_ascolto.py:1109 — stessa modifica sul finto dei tre casi d'errore. Vale ancora la riserva già aperta (R-675-1): i casi d'errore passano anche con un'eccezione non prevista nel finto. Esito: ok.
- reports/stato_progetto.md:4 — la riga «Ultimo aggiornamento». Rischio esaminato: voci perse nel conflitto. È il prefisso di Mani più la riga 4 di main, e la coda coincide esattamente. Ho controllato ogni voce di HEAD e sono tutte presenti; il blocco V15 arriva da main. Esito: ok.
- clients/voice/ascolto.py:714 — il client manda `X-Gas-Seguito: 1` solo con `seguito=True`. Il server (modules/voice/server.py:688) lo legge solo per il parlato. Rischio esaminato: header assente, e allora il parlato della stanza finirebbe a un turno normale. Il mutante «header tolto» è ucciso. Esito: ok.
- clients/voice/ascolto.py:735 — con `X-Gas-Comando: fine` il client esce prima di leggere il corpo, quindi vale in ogni formato. Il server manda il comando da `end_headers` (modules/voice/server.py:466) e «fine» come JSON 200 `{"content":"","fine":true}` (modules/voice/server.py:683). Rischio esaminato: confusione con la riga NDJSON `{"fine": true}`, che chiude normalmente il flusso. Non succede: il comando si legge solo dall'intestazione, mai dal corpo. Esito: ok.
- clients/voice/ascolto.py:462 — un turno di seguito che fallisce (500 o 429) chiude la conversazione senza bip. Esito: ok, confermato dalla prova qui sotto.
- scripts/voce/LEGGIMI.md:14 — dice che nella conversazione senza la parola «pausa» fa rispondere «Va bene.». Il server finale nel seguito risponde invece con JSON muto `{"content":"","pausa":true}` (modules/voice/server.py:530, correzione V-2 del bot #339 su 312cd86). La prova d'integrazione conferma che non viene suonato nulla. Esito: riserva.

**Prova d'integrazione (scratch, copia dell'index)**
- Test: client vero (`invia_al_server` e `Ascolto.turno`) contro il VoiceHandler vero. La trascrizione è finta; la sintesi è finta e solleva un errore dove non deve essere chiamata. Il kernel è finto e conta anche le chiamate a `registra_seguito`. Risultato: 21 passed.
- Risposta `[NON_PER_ME]` o vuota con `seguito=True`: esce `(True, None, "", "fine")` nei formati "", audio+testo, audio+pezzi e pezzi-voce. Il turno è effimero e va solo al forte; nessuna sintesi, nessuna registrazione in storia. `Ascolto.turno` imposta `chiudi=True`, senza bip e senza audio.
- «pausa» nel seguito: comando «pausa», nessun turno del kernel, conversazione chiusa, niente voce e niente bip.
- «pausa» con la parola: si sente «Va bene.» e arriva il comando, in tutti i formati.
- 500 nel seguito (evento error del kernel, o eccezione) e 429 (tetto orario, senza chiamare la trascrizione): `(False, None, "HTTP 500/429", "")` e chiusura senza bip.
- Risposta vera nel seguito (NDJSON, audio+testo, MP3): suona un pezzo, `chiudi` resta False e `registra_seguito` viene chiamato.
- Mutante «X-Gas-Seguito tolto» nel client: 10 failed nella prova, 1 nella suite del repo (`test_invio_di_seguito_manda_l_intestazione`).
- Suite sulla copia dell'index: voce_ascolto, voice_stt e prova_voci, 410 passed.

**Riserve**
- **R-679-1 BASSA**: nel repo manca un test d'integrazione V15 tra client vero e server vero. La suite usa solo il server finto `_ServerComando`. Consiglio di portare nel repo la prova di scratch (casi fine, pausa, 500/429), con la sintesi che fallisce se viene chiamata. Il file è nello scratchpad (prove/test_integ_679.py) e si lancia con `IDX=<radice dell'albero>`.
- **R-679-2 BASSA**: scripts/voce/LEGGIMI.md:14 è falso dopo il merge, perché nel seguito la pausa è muta (risponde «Va bene.» solo dopo la parola). Lo stesso vale anche per «basta!».
- **R-679-3 COSMETICA**: una pausa nel seguito finisce nel log come «turno di seguito non riuscito: risposta inattesa (senza voce)». La chiusura è giusta, ma il log non lo dice: andrebbe registrata come pausa.

**Cosa non ho verificato**
- La suite del kernel (test_unit_kernel.py) non l'ho rilanciata: gas.py e il suo test sono blob identici a MERGE_HEAD, già rivisti e provati da M2 (#682 – #686-M2). Il client non li tocca.
- Il comportamento sul Mac (microfono vero, afplay, ElevenLabs e Groq veri) non è riproducibile qui.
- Effetto collaterale visto ma non indagato: anche nel seguito una trascrizione «ciao gas» fa rispondere «Dimmi.», per la regola `_SOLO_ATTIVAZIONE` del server, e la finestra resta aperta. Il parlato è rivolto a Gas, quindi lo ritengo accettabile.

**Memoria**
- Ho aggiunto in coda a .claude/agents/memoria_revisore.md la riga contatore `#679 (chat Mani) — 2026-11-06 — APPROVATO CON RISERVE — …` e una lezione nuova: al primo merge che unisce client e server scritti da chat diverse, rileggere la documentazione utente contro il comportamento finale del server.
- Il file è solo nel working tree («MM»), NON committato, come chiesto: va aggiunto con `git add` al commit del merge.


Commit 1792ab3 (V-1 del bot su 851a0d1: parola nella finestra) — review #680, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #680 (chat Mani) della PR #341. Ho guardato il diff staged su 851a0d1 con `git diff --cached`. Prima ho letto le tre fonti obbligatorie: CLAUDE.md sez. 5, stato_progetto.md (solo le parti sulla voce) e la memoria del revisore.

**Elementi esaminati**
- `clients/voice/ascolto.py:382`: `_parola_nel_blocco` usa la stessa soglia di `aspetta_parola`. Un errore del rilevatore (eccezione, None, valore non numerico) vale «no» (§9). Rischio: un crash nella finestra. Esito: ok. Una riserva cosmetica, vedi R-680-3.
- `clients/voice/ascolto.py:446`: `aspetta_voce` passa ogni blocco al rilevatore. La parola arriva circa 1 s dopo «Hey», mentre la voce apre il turno già dopo 0,24 s. Quindi di solito la parola si sente dentro `registra`, ed è coperta da `clients/voice/ascolto.py:410`, dove il tetto passa a 30 s al volo. Il ciclo `while` rilegge `max_s` a ogni giro, quindi l'aumento vale davvero. Esito: ok.
- `clients/voice/ascolto.py:643`: il flag si azzera a ogni giro della finestra. `seguito = not self.parola_nella_finestra` e il filtro dei 15 s vale solo se il turno è di seguito. Esito: ok. Il mutante «azzeramento tolto» è preso dal test del turno successivo.
- `tests/test_unit_voce_ascolto.py:608`: verifica che la parola nella finestra dia un turno normale. Esito: ok. Il blocco della parola sta negli `iniziali`, quindi il test prende anche il mutante «aspetta_voce senza rilevatore».
- `tests/test_unit_voce_ascolto.py:641`: rilevatore rotto dopo la prima risposta, il turno resta di seguito. Esito: ok.
- `scripts/voce/LEGGIMI.md:10`, `scripts/voce/LEGGIMI.md:13` e `scripts/voce/LEGGIMI.md:18`: chiudono V-2 (i 15 s comprendono la pausa finale) e V-3/R-679-2 (la pausa nel seguito è muta, «Va bene.» solo con la parola). Esito: ok, coerenti col server.
- Contesto, coerenza col server V15: `modules/voice/server.py:534`. Se la trascrizione è solo «Hey Jarvis», senza X-Gas-Seguito, il server risponde «Dimmi.» senza far partire un turno. «Hey Jarvis, pausa» passa da `modules/voice/server.py:526` e risponde «Va bene.». Il ciclo «ripetimelo» (`modules/voice/server.py:143`) non può più ripartire quando la parola si sente. Esito: ok.

**Verifiche eseguite**
- Copia dell'index in scratch: `tests/test_unit_voce_ascolto.py` dà 253 passed.
- Due mutanti miei, entrambi presi (1 failed ciascuno): «flag non azzerato» e «`rileva_parola=False` in registra».

**Domande del chiamante**
- **Doppie attivazioni:** no. Dentro `registra`, dopo la parola, il rilevatore non viene più chiamato. Poi `turno` lo azzera prima della riproduzione e `conversazione` lo azzera alla fine, prima di `aspetta_parola`. Resta però R-680-1.
- **Parola sentita ma la voce non parte:** caso quasi impossibile, perché la parola stessa supera `voce_rms` per 0,24 s. Se succede, `aspetta_voce` restituisce None e la parola si perde. Il flag resta alto finché la finestra non finisce (vedi R-680-2).
- **Privacy:** il rilevatore gira in locale, quindi non esce nessun dato nuovo. Una falsa parola nella finestra manda fino a 30 s di audio come turno normale, senza i filtri V15. È la stessa fiducia nella parola che vale già fuori dalla finestra, solo resa più probabile da R-680-1.

**Riserve (da tracciare in stato_progetto.md)**
- **R-680-1 BASSA:** fra la riproduzione e la finestra il rilevatore non viene azzerato. Durante la riproduzione `_ascolta_mentre_suona` passa a openWakeWord la voce di Gas, con soglia 0,7. La finestra usa soglia 0,5, e il buffer interno di openWakeWord (circa 1–2 s di caratteristiche audio) porta quella voce nei primi punteggi. Un punteggio fra 0,5 e 0,7 sulla voce di Gas alzerebbe il flag e il parlato della stanza passerebbe come turno normale. Correzione: `self._azzera()` subito prima di `self.aspetta_voce()`, più un test con un rilevatore che conserva lo stato.
- **R-680-2 BASSA:** se la parola si sente nella finestra prima che la voce parta, il flag resta alto finché la finestra non finisce. Il parlato che arriva dopo (anche la TV) diventa un turno normale da 30 s. Inoltre una parola sentita senza voce si perde a fine finestra. Nessun test copre questi due casi.
- **R-680-3 COSMETICA:** gli errori del rilevatore nella finestra non lasciano traccia nel log. La traccia c'è comunque in `aspetta_parola`. Da segnalare: `if seguito is False:` andrebbe scritto `if not seguito:`.

**Rischi esclusi (non verificati)**
- Il comportamento reale di openWakeWord: punteggi residui dopo la riproduzione e ritardo della parola sul Mac. Il pacchetto e il microfono non ci sono in questo ambiente, quindi R-680-1 è un'analisi del codice, non una prova.
- Nessuna prova di integrazione con il server vero su questo diff: la #679 ne aveva fatta una, questa no.
- Suite del kernel non eseguita: il diff non tocca gas.py.

**Memoria:** ho aggiunto la riga #680 e una lezione sullo stato dei rilevatori fra una fase e l'altra. Commit 288c3f6 fatto con `scripts/commit_memoria_revisore.sh`; lo staged del diff non è stato toccato.

Commit 1792ab3 — review #681 (ri-review con R-680-1 corretta), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #681 (chat Mani). Ho riletto il diff staged del branch claude/peaceful-lovelace-0w2b7q (PR #341). Il diff tocca 3 file: clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py e scripts/voce/LEGGIMI.md.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (in testa), .claude/agents/memoria_revisore.md (la #680 e la sua lezione sul rilevatore con stato).

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:644` — dopo la riproduzione, prima di `aspetta_voce()`, rimette `parola_nella_finestra` a False e chiama `self._azzera()`. Rischio esaminato: il residuo di openWakeWord (la voce di Gas sentita con soglia 0,7) poteva far scattare la parola nella finestra, dove la soglia è 0,5. Altri effetti esaminati:
  - con `finestra_s=0` l'ho provato in una copia nella scratch: 1 solo turno, 3 azzeramenti, nessun turno di seguito, flag False. Il doppio azzeramento prima del `break` non fa danni, perché `_azzera` è fail-safe e si può ripetere.
  - dopo un'interruzione il ramo `continue` ha il suo `_azzera` e non arriva al codice nuovo. Il giro normale successivo invece ci arriva.
  - Esito: ok, R-680-1 chiusa.
- `tests/test_unit_voce_ascolto.py:634` — `test_rilevatore_azzerato_prima_della_finestra`: dopo la riproduzione il rilevatore resta a 0,6 finché non viene azzerato. Rischio esaminato: un test che non morde. Ho tolto la riga `self._azzera()` in una copia: falliscono 2 test (questo e quello sotto). Esito: ok.
- `tests/test_unit_voce_ascolto.py:93` — gli azzeramenti attesi passano da 2 a 3. È coerente col nuovo punto di azzeramento e uccide anche lui il mutante. Esito: ok.
- `clients/voice/ascolto.py:656` — ora c'è `if not seguito:` con il log. È solo una modifica estetica e non cambia il comportamento. Esito: ok.
- `clients/voice/ascolto.py:387` — `_parola_nel_blocco`: se il rilevatore va in errore vale «no», senza crash (§9). Esito: riserva R-681-1, sotto.

**Prove**: suite ascolto sull'albero staged (copiato con `checkout-index` nella scratch): 254 passed. Mutante «azzeramento prima della finestra tolto»: 2 failed. Niente `git stash`, lo staged non è stato toccato.

**Riserve**
- R-681-1 COSMETICA: la R-680-3 non è chiusa nel senso in cui l'avevo scritta nella #680. Diceva che gli errori del rilevatore nella finestra non lasciano traccia nel log. Il diff ha cambiato solo `if not seguito:`, e `clients/voice/ascolto.py:387` fa ancora `except Exception: return False` senza `log.warning`. Rimedio: un `log.warning` con il nome dell'errore, eventualmente limitato come `_errori_rilevatore`. Si può anche chiuderla dichiarandola accettata.
- R-680-2 BASSA: resta aperta ed è registrata.

**Rischio escluso**: non ho verificato il comportamento reale di openWakeWord sul Mac, cioè se `azzera_rilevatore` svuota davvero il buffer interno del modello e quanto vale il residuo vero dopo la voce di Gas. In dev non si può riprodurre: i test usano un rilevatore finto. Non ho guardato `scripts/voce/LEGGIMI.md` oltre al diff della documentazione.

Nessuno slicing della history e nessuna simulazione di tool: il diff non tocca il kernel.

Memoria aggiornata con la riga #681 (chat Mani) e committata con scripts/commit_memoria_revisore.sh: commit 7669be5. Lo staged è intatto (3 file, +132/−11).


Merge 7296f39 (main con la PR #342 dentro la PR #341) — review #693, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #693 (chat Mani): merge di origin/main c131452 (PR #342 di M2, parser del bot) in claude/peaceful-lovelace-0w2b7q (PR #341). Il merge è staged in /home/user/Gas. Non ho fatto stash né modifiche al repo, a parte la memoria.

**Cosa ho controllato**
- **Perdite**:
  - Questi file sono identici a MERGE_HEAD: `scripts/bot_esito.py`, `tests/test_unit_verifica_bot.py`, `tests/dati_verifica_bot/` e `reports/ripartenza_m2.md`.
  - Questi file sono identici a HEAD (lato Mani): `clients/voice/ascolto.py`, `scripts/voce/LEGGIMI.md`, `reports/handoff.md` e `reports/ultimo_report.md`.
  - La memoria è l'unione dei due lati: #676–#681 di Mani e #687–#692-M2.
  - In `reports/stato_progetto.md` ci sono sia le modifiche di M2 sia quelle di Mani. Nessuna perdita.
- **Interazione tra le due PR**: dalla base comune 3cde8a5 i file di codice toccati sono disgiunti. La #342 tocca il bot e i suoi test, la #341 tocca la voce. Nessuna interazione.
- **Marcatori di conflitto**: nell'index non ce ne sono.
- **Test** (su una copia dell'index in scratch): `test_unit_voce_ascolto` + `test_unit_verifica_bot` danno 872 passed.

**Citazioni**
- `tests/test_unit_voce_ascolto.py:692` — l'intestazione diventa «finestra dopo la risposta» (V-2 del bot). Rischio esaminato: un commento che non corrisponde più al comportamento. Esito: ok, perché il valore predefinito è 40 s (`scripts/voce/LEGGIMI.md:126`). Però il testo vecchio resta in `:443`, vedi R-693-1.
- `clients/voice/ascolto.py:446` — il rilevatore resta acceso nella finestra (V-1 bot #341). Rischio esaminato: una modifica arrivata col merge. Esito: ok, il file è identico a HEAD (`git diff --cached HEAD` vuoto) e la #342 non lo tocca.
- `reports/stato_progetto.md:615` — la riga M2 «Bot di verifica, ad alta voce». Rischio esaminato: persa nella fusione automatica. Esito: ok, c'è, insieme a `reports/stato_progetto.md:616` (V15 «MERGIATA il 6 nov»).
- `reports/stato_progetto.md:668` — la voce Mani della fetta 43 parte 2 con le riserve del bot e della verifica esterna su bdc79ce. Rischio esaminato: riserve tracciate male. Esito: ok, sono tracciate col link al commento della verifica esterna.
- `reports/diff_sessione.md:3` — la base aggiornata a c131452 (PR #340, #339, #342). Esito: ok.
- `scripts/bot_esito.py:133` — `_ALTA_VOCE` arriva da main. Esito: ok, identico a MERGE_HEAD.

**Riserve**
- **R-693-1 COSMETICA**: la docstring in `tests/test_unit_voce_ascolto.py:443` dice ancora «nella finestra dei 12 s». La V-2 del bot è stata corretta solo nell'intestazione a `:692`.
- **R-693-2 BASSA**: la V-1 del bot su bdc79ce resta aperta in `stato_progetto`. Se la parola si sente a metà di una registrazione di seguito, tutto il blocco diventa un turno normale. Servono il rimedio oppure che l'operatore dichiari il rischio accettato. Va decisa prima del merge della #341, oppure detta esplicitamente all'operatore.

**Cosa non ho verificato**
- Suite intera sulla copia: 33 failed su 3299 passed, perché nel sandbox manca `bwrap`. Ho guardato da vicino solo i fallimenti di `test_unit_web_browser`. Gli altri non li ho attribuiti uno per uno, ma il merge non tocca il web e nessuno dei due lati tocca moduli diversi da voce e bot. Fa fede la CI.
- Comportamento reale della voce sul Mac: non riproducibile qui.

**Memoria**: ho aggiunto la riga #693 e una lezione in .claude/agents/memoria_revisore.md. È nel working tree, non committata e non aggiunta all'index (stato MM): va aggiunta con `git add` prima del commit del merge.


Commit 01b1089 (V-1 del bot su 23d9c1c: taglio prima della parola) — review #694, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #694 (chat Mani). Diff staged su 23d9c1c, PR #341, branch claude/peaceful-lovelace-0w2b7q. Ho letto CLAUDE.md, la memoria e il contesto in stato_progetto.

**Cosa ho controllato nel diff**
- `clients/voice/ascolto.py:104` — nuova costante `PRIMA_DELLA_PAROLA_S = 1.5`. Rischio: che il taglio porti via la parola stessa. `blocchi_per(1.5)` = round(18,75) = 19, quindi si tengono 18 blocchi più quello della parola: circa 1,52 s. «Hey Jarvis» dura circa 0,8–1,2 s e il modello lo valuta su una finestra di circa 1,3 s, chiusa a fine parola. Ci sta, con 0,3–0,7 s di margine. Esito: ok (vedi R-694-2).
- `clients/voice/ascolto.py:420` — `tieni = max(0, …-1)` e `presi = presi[-tieni:] if tieni else []`. Rischi controllati:
  (a) Il caso `tieni=0` è gestito: evita `presi[-0:]`, che terrebbe tutta la lista.
  (b) Caso «voce non ancora partita»: con `rileva_parola=True` non si verifica. registra viene chiamata solo da `clients/voice/ascolto.py:657`, con `inizio` = 3 blocchi di aspetta_voce, quindi la voce è già partita. Anche se succedesse, `presi` avrebbe al massimo 2 blocchi e il taglio non cambierebbe niente.
  (c) Contatore del silenzio: non viene azzerato al taglio, ma i blocchi forti della parola lo riportano a 0. Si chiuderebbe in anticipo solo con una parola sotto la soglia della voce, una cosa che c'era già prima.
  (d) Il contatore di attesa non conta, perché la voce è già partita.
  (e) Il tetto dei 30 s ora parte da 1,5 s prima della parola, come previsto.
  Esito: ok.
- `tests/test_unit_voce_ascolto.py:630` — test con 8 s di stanza, poi la parola, poi voce; controlla la lunghezza esatta inviata, `(18+1+20+10)*BLOCCO`. L'ho fatto girare su una copia dell'index in scratch: 255 passed. Ho provato due versioni sbagliate del codice: senza taglio, e con `tieni=0`. Il test le scarta tutte e due. Esito: ok.
- `scripts/voce/LEGGIMI.md:14` — scritto che nella finestra non c'è bip e che il parlato prima della parola non parte. Corretto, a parte il residuo di R-694-1. Esito: ok. `tests/test_unit_voce_ascolto.py:443`: la docstring dei «12 s» è corretta e un grep sui 3 file non trova altre occorrenze. Esito: ok.

**Privacy**: il V-1 del bot è chiuso per la parte grave. Al massimo 15 s di stanza diventavano un turno normale; ora ne restano circa 0,3–0,7 s prima della parola.

**Riserve**
- R-694-1 BASSA: resta un residuo, da far accettare all'operatore in stato_progetto.
  1. Nel turno normale vanno ancora circa 0,3–0,7 s di stanza prima della parola, senza il filtro «non per me».
  2. Un falso positivo del rilevatore nella finestra (soglia 0,5) in mezzo al parlato della stanza rende normale tutto quello che si dice dopo, fino a 30 s. Questo c'era già dal #341 e la correzione non lo copre.
- R-694-2 BASSA: i 1,5 s non sono provati con il ritardo vero di openWakeWord sul Mac. Serve una prova dal vivo: dire «Hey Jarvis, che ore sono» nella finestra e controllare nel testo trascritto che la parola sia intera.

**Cosa NON ho verificato**: il comportamento reale sul Mac (microfono, ritardo vero di openWakeWord, durata vera di «hey_jarvis»), che qui non si può riprodurre. Il filtro «non per me» e la scelta del cervello lato server non li ho riletti, perché sono fuori dal diff.

**Memoria**: aggiunta la riga #694 e una lezione (provare due versioni sbagliate su un taglio «tieni gli ultimi N»). Committata con scripts/commit_memoria_revisore.sh (4e81502); lo staged non è cambiato (3 file, +28/−3).


Commit 165a9a4 (V-1 della verifica esterna su 562f137: la parola scade dopo 2 s) — review #695, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #695 (chat Mani). Diff staged su `claude/peaceful-lovelace-0w2b7q` (PR #341, HEAD 562f137). Lo sha256 del diff, b6025b22d756…, è uguale prima e dopo il commit della memoria. Prima della review ho letto CLAUDE.md, le voci R-680-2 e #341 in `reports/stato_progetto.md` e la memoria del revisore.

**Correttezza: la correzione regge.** La parola resta valida per al massimo 25 blocchi (`blocchi_per(2,0)`). Poi `parola_nella_finestra` torna False e il parlato dopo parte come turno di seguito. Nessuno slicing della history, nessuna simulazione dei tool, i guardrail non sono toccati. È un cambiamento solo del client, senza nuove eccezioni: `_parola_nel_blocco` tratta già un errore del rilevatore come «no» (§9).

**Righe del diff esaminate**
- `clients/voice/ascolto.py:453` — nuovo contatore `da_parola` (blocchi dall'ultima parola sentita, None se nessuna parola). Rischio esaminato: valore rimasto da un turno precedente. È una variabile locale di `aspetta_voce` e il flag torna False prima della chiamata (`clients/voice/ascolto.py:662`, contesto). Esito: ok.
- `clients/voice/ascolto.py:459` — la parola sentita di nuovo rimette il conteggio a 0. Caso «parola di nuovo dentro i 2 s»: con 20 blocchi + parola + altri 20 il turno è normale; con 40 blocchi senza una seconda parola è di seguito. Il conteggio riparte. Esito: ok.
- `clients/voice/ascolto.py:462` — scadenza con `>`. La parola sentita in uno dei blocchi che aprono la voce dà turno normale: il flag diventa True e la funzione esce prima di poterlo far scadere. Esito: ok.
- `clients/voice/ascolto.py:462` — riserva sul confine. Il contatore avanza anche nei 3 blocchi che servono ad aprire la voce. Il confine reale è quindi circa 1,84 s tra la parola e il primo blocco di voce, non 2 s: con 24 blocchi di silenzio il turno è già di seguito. Esito: riserva R-695-1.
- `clients/voice/ascolto.py:671` (contesto, non nel diff) — interazione con `registra`. Se il flag è scaduto, `rileva_parola=True` e la parola sentita dentro la registrazione rende comunque il turno normale. Sonda «falso positivo vecchio, voce, poi parola»: turno normale. Esito: ok.
- `tests/test_unit_voce_ascolto.py:679` — falso positivo 20 s prima del parlato: il turno resta di seguito. Prende il mutante «senza azzeramento» (1 test fallito). Esito: ok.
- `tests/test_unit_voce_ascolto.py:689` — parola 0,8 s prima della voce: turno normale. Insieme all'altro test prende il mutante «scade subito» (3 test falliti). Il controllo con `is RUMORE_PAROLA` è valido: `_blocchi` passa lo stesso oggetto, altrimenti questo test fallirebbe. Esito: ok.
- `scripts/voce/LEGGIMI.md:15` — testo ammorbidito, coerente con i 18 blocchi (1,44 s) tenuti in `registra` e con la scadenza. «Più di 2 secondi» è un'approssimazione: vedi R-695-1. Esito: ok con riserva.

**Prove (su una copia dell'index in scratch, niente stash):** suite ascolto 257 passed; i due mutanti presi come sopra. Sonde con gli strumenti dei test: 24, 25 e 26 blocchi di silenzio, rinnovo, parola nei blocchi della voce, flag scaduto con parola dentro `registra`.

**Riserve**
- R-695-1 BASSA: il confine effettivo è circa 1,84 s prima del primo blocco di voce (circa 2 s se si conta dalla parola all'apertura del turno), mentre LEGGIMI dice «più di 2 secondi». Nessun test sul confine: un mutante `>=` o uno spostamento di un blocco non verrebbe preso. Per chiuderla basta un test con 22 e 23 blocchi di silenzio, oppure sottrarre `blocchi_per(INIZIO_VOCE_S)` dal conteggio, oppure precisare il testo.
- R-695-2 BASSA: un falso positivo del rilevatore entro circa 1,8 s dall'inizio del parlato della stanza rende ancora normale quel turno. È il residuo di R-694-1, ristretto da tutta la finestra a meno di 2 s: da far accettare all'operatore.

**Cosa non ho verificato:** la latenza reale di openWakeWord e la frequenza dei falsi positivi alla soglia 0,5 sul Mac. Non sono riproducibili nel sandbox: lì il rilevatore è finto. Non ho verificato neanche se, con la pausa naturale dopo «Hey Jarvis», la voce parte entro 1,8 s. Nel caso tipico la parola è essa stessa voce, quindi `aspetta_voce` esce prima che il rilevatore scatti e la parola viene presa in `registra`, una strada che questo diff non cambia. Non ho rilanciato la suite intera: il diff tocca solo il client voce.

**Memoria:** aggiunte la riga #695 e una lezione (sondare il confine con N-1/N/N+1 blocchi quando il contatore avanza anche nei blocchi che completano la condizione di uscita). Committata con `scripts/commit_memoria_revisore.sh` (commit a1aa77b); i 3 file staged non sono stati toccati.

Merge 8c31f6e (main con la PR #343 dentro la PR #341) — review #696, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Numero di review: **#696**. Ho controllato le memorie di tutti i branch: il numero più alto è #695 (chat Mani). Per M2 il più alto è #692-M2, sia su origin/main sia su feat/voce-v12-m2. La riga #696 è scritta in coda a .claude/agents/memoria_revisore.md e NON è committata: resta nel working tree come richiesto. Nessuna lezione nuova.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (righe che riguardano la voce), memoria_revisore.md (coda).

**Integrità del merge (base c131452)**
- I file cambiati da main e dal branch sono insiemi disgiunti, a parte i 4 report.
- Uguali a MERGE_HEAD nell'index: gas.py, brains/claude_cli.py, modules/voice/server.py, ripartenza_m2 e i test claude_cli, kernel, voice_contesto e voice_stt.
- Uguali a HEAD nell'index: clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py, scripts/voce/LEGGIMI.md, handoff, ultimo_report, diff_sessione e memoria.
- stato_progetto: il risultato di `git merge-file` (HEAD, base, MERGE_HEAD) è identico byte per byte (cmp) all'index, rc=0, nessuna voce persa.
- Nessun marcatore di conflitto, `ls-files -u` vuoto, `diff --check` pulito.

**Test**
- Su una copia dell'index in scratch: voce_ascolto, voice_stt, voice_contesto, claude_cli e prova_voci danno **470 passed**. Senza prova_voci tornano i 415 dichiarati.
- Sonda in scratch: client vero (`invia_al_server`) contro il VoiceHandler vero, con kernel finto che registra i kw.
  - Turno di seguito: `cervello=forte`, `effimero=True`, `voce=True`; istruzione = seguito + C1.
  - Turno con la parola: solo `voce=True` + C1.
  - «pausa» con o senza seguito: nessun turno, il client riceve il comando `pausa`.
  - `[NON_PER_ME]`: il client riceve `(True, None, "", "fine")`.
- Il contratto HTTP fra client e server non cambia con la #343: aggiunge solo il kw `voce` e il testo C1.

**Elementi citati**
- clients/voice/ascolto.py:766 — mette `X-Gas-Seguito: 1` sui turni di seguito. Rischio: la #343 cambia il modo in cui il server tratta il seguito. Esito: ok (con la sonda, server.py fa ancora forte+effimero e aggiunge voce=True).
- clients/voice/ascolto.py:493 — `comando == "fine"` chiude la conversazione. Rischio: C1 o la finestra di 6 cambiano la risposta `[NON_PER_ME]`. Esito: ok (con la sonda resta JSON vuoto + `fine`).
- tests/test_unit_voce_ascolto.py:511 — finto server con la sequenza «risposta, poi fine». Rischio: i test del client dipendono dal server di M2. Esito: ok (usano un server finto; la suite è verde sull'index).
- scripts/voce/LEGGIMI.md:20 — la doc della pausa (muta senza la parola, «Va bene.» con la parola). Rischio: la #343 cambia la pausa. Esito: ok (la pausa esce prima di run_turn, sonda coerente).
- reports/stato_progetto.md:615 — voce «Voce rapida, fetta 2», arrivata con l'unione automatica. Rischio: perdita o doppione. Esito: riserva cosmetica (dice «PR aperta», ma la #343 è mergiata).
- Contesto:
  - modules/voice/server.py:598 — `kw["voce"] = True` per ogni turno audio, quindi anche seguito ed effimero.
  - gas.py:4857 e gas.py:4936 — routing del seguito e payload usano entrambi `_get_window(_n_finestra)`. Nessun taglio diretto della history, Wall of Shame rispettato.
  - modules/voice/server.py:205 — testo C1.

**Riserve**
- R-696-1 BASSA: nei turni di seguito C1 («rispondi solo all'ultima cosa che l'operatore ha detto», modules/voice/server.py:205) viene prima di ISTRUZIONE_SEGUITO e dà per scontato che a parlare sia l'operatore. Questo può spingere il modello a trattare il parlato della stanza come rivolto a Gas. Si verifica solo dal vero sul Mac.
- R-696-2 BASSA: a voce, il routing «solo forte dopo un seguito» guarda 6 messaggi invece di 10 (gas.py:4857). È coerente col payload, quindi il seguito non arriva ai gratuiti. Però il residuo già aperto V-1 bot d9c09e9 (risposte del forte che citano un seguito poi mandate ai gratuiti) scatta dopo 3 scambi invece di 5.
- R-696-3 COSMETICA: in reports/stato_progetto.md, alla riga 615 c'è «PR aperta» (va scritto «PR #343 MERGIATA (e68a951)»). Nella voce V15 c'è ancora «ultimi ~10 messaggi» (a voce ora sono 6).

**Cosa NON ho verificato**
- Suite kernel non rilanciata: gas.py e test_unit_kernel.py sono identici a MERGE_HEAD, già rilanciati da M2 con 1089 PASS. Nel sandbox manca bwrap.
- Effetto reale di C1 e di `--effort low` sul modello e sui tempi: richiede il Mac con `claude` loggato.
- Latenza reale del client sul Mac.

Merge b874179 (main con la PR #344 dentro la PR #341) — review #697, verdetto integrale:

## VERDETTO: APPROVATO

Review #697 (chat Mani). Il numero più alto in memoria era #696, quindi questa è la #697. Le righe #693-M2 e #694-M2 hanno una numerazione a parte, quella della chat M2.

Oggetto: merge staged di origin/main 44dbe2d (PR #344 di M2) nel branch claude/peaceful-lovelace-0w2b7q (PR #341, HEAD 7e4a7d3). La base comune è e68a951.

**Elementi del diff esaminati**
- `brains/claude_cli.py:276` — la regex `_RIFIUTO_EFFORT` riconosce solo «unknown/unrecognized option/argument» seguito da `--effort`, con il blocco `(?![\w-])` alla fine. Rischi esaminati: perdita nel merge, interazione con la #341, backtracking. Il file staged è identico a MERGE_HEAD. Il backtracking quadratico l'ha già chiuso #694-M2 (un solo `\s*` libero). Esito: ok.
- `brains/claude_cli.py:285` — `_effort_rifiutato` ora legge solo lo stderr e conta solo con un'uscita diversa da zero. L'unico chiamante è `brains/claude_cli.py:350`, dentro il blocco try che riprova senza effort, quindi un'eccezione resta intercettata come prima. Rischio esaminato: un chiamante nel client voce della #341. Il grep su clients/ e scripts/voce non trova riferimenti a claude_cli né a effort. Esito: ok, nessuna interazione.
- `tests/test_unit_claude_cli.py:507` — il blocco `finally` rimette `_effort_non_supportato`, così un test fallito non lascia l'effort spento per i test successivi. `tests/test_unit_claude_cli.py:511` è il test parametrico, con il caso `--effort-level` → False. `tests/test_unit_claude_cli.py:567` è il test di tempo lineare. Rischio esaminato: test persi nel merge. Il file è identico a MERGE_HEAD. Esito: ok.
- `reports/stato_progetto.md:615` — è la voce nuova «Fetta 3 sottofondo». La `reports/stato_progetto.md:616` dice ora «PR #343 MERGIATA (e68a951)». Rischio esaminato: perdita di righe della chat Mani o della chat M2. Ho rifatto `git merge-file` con base, HEAD e MERGE_HEAD in scratch: esce con codice 0 ed è identico byte per byte (cmp) al file staged. Rispetto a HEAD il diff tocca solo queste righe. Esito: ok.
- `.claude/agents/memoria_revisore.md` — le prime 1292 righe staged sono identiche (cmp) all'intero file di HEAD, cioè fino alla riga #696. La coda (#693-M2, la lezione, #694-M2) è identica alle ultime 3 righe di MERGE_HEAD. Esito: ok, l'unione è senza perdite.

**Integrità del merge**
- File identici a MERGE_HEAD: brains/claude_cli.py, tests/test_unit_claude_cli.py, reports/proposta_fetta3_sottofondo.md, reports/ripartenza_m2.md.
- File identici a HEAD: reports/handoff.md, reports/ultimo_report.md, reports/diff_sessione.md, clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py, gas.py, modules/voice/server.py.
- `git ls-files -u` è vuoto e `git diff --cached --check HEAD` è pulito. Nessun marcatore di conflitto in reports/, .claude/, brains/ e tests/.
- Nei file di codice i due lati non si sovrappongono: da e68a951 la PR #344 cambia solo claude_cli e il suo test.

**Test**
Ho copiato l'index in scratch con `git checkout-index`, senza stash e senza toccare il repo: test_unit_claude_cli + test_unit_voce_ascolto danno **316 passed** in 31,7 s.

**Cosa non ho verificato e perché**
- La suite intera: in questo sandbox manca bwrap, e nella review #693 i suoi test web fallivano per questo, fuori dal diff.
- `claude --help | grep effort` e il comportamento dell'effort con la CLI vera sul Mac: non si possono riprodurre nel cloud.
- Le sonde regex: non le ho rilanciate, le ha già fatte #694-M2 sullo stesso contenuto (file identico a MERGE_HEAD).

**Memoria**
La riga #697 è in coda a .claude/agents/memoria_revisore.md, nel working tree e non committata, come chiesto. Non ho lanciato `commit_memoria_revisore.sh`, e il file è già staged dal merge: serve `git add` prima del commit. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 220 (main dopo la #340) a 257 casi (248 con la fetta, 254 dopo la correzione V-1 del bot su 851a0d1, 255 dopo quella su 23d9c1c, 257 dopo quella su 562f137). Riepilogo reale nel venv con requirements e requirements-dev:

```
257 passed in 28.55s
```

Dopo il merge della #344 (b874179), review #697 su una copia dell'index: test_unit_claude_cli + test_unit_voce_ascolto 316 passed.

Mutanti presi (15):
- «fine» ignorato;
- pausa che non chiude;
- errore di seguito con bip;
- `chiudi` ignorato;
- parlato lungo inviato;
- tetto di seguito a 30 s;
- `seguito` sempre False;
- intestazione mancante;
- interruzione che resta di seguito;
- finestra a 12 s;
- comando sconosciuto accettato;
- risposta senza voce di seguito con bip;
- più 3 rinforzati dopo il primo giro.

I due mutanti di stato trovati dal revisore sono nella riserva R-676-1.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP).

Mappatura commit → run:
- 851a0d1: CI run con handoff-check success; verifica-bot BOCCIATO (V-1 MEDIA, corretta in 1792ab3).
- bdc79ce: CI run 42293018752, unit-suite e handoff-check success (voce H24: 254 passed); bot APPROVATO CON RISERVE (neutral).
- 23d9c1c: unit-suite e handoff-check success; bot failure (V-1 alzata a MEDIA, corretta in 01b1089).
- 562f137: handoff-check success, unit-suite in corso alla verifica esterna.
- 7e4a7d3 (contiene 165a9a4, a1aa77b, 8c31f6e): unit-suite, handoff-check, smista e verifica success. Bot APPROVATO CON RISERVE (check neutral): V-1 BASSA, V-2 COSMETICA, nessuna ALTA/MEDIA. Verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/341#issuecomment-6697209245). Merge rifiutato da GitHub per conflitti con la #344.
- b874179 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.
- a7ed0e8 e 43fa6ac: run dei loro push (handoff-check success; unit-suite non riletta qui).
- 51c4aa0, 4cd7b97, da24b2c: pushati insieme a 43fa6ac.

Suite voce in locale dopo il merge (ascolto, stt, prova_voci): 410 passed. Dopo la correzione V-1 (1792ab3): suite ascolto 254 passed. Prova d'integrazione del revisore #679 con client e server veri: 21 passed.

## §7 RISERVE APERTE

- R-676-1 BASSA: due mutanti di stato sopravvivono (`self.chiudi` non azzerato; «pausa» che chiude solo nei turni di seguito).
- R-676-2 BASSA: lo svuota dopo «fine» non è coperto da test.
- R-676-3 BASSA, per M2 (girata a M1): trascrizione incerta di seguito → «Non ho capito» a voce invece di «fine».
- Dalla #340: bot V-1 BASSA (conferma non suonabile = silenzio), verifica esterna V-4 BASSA (eco dopo la conferma), R-675-1 BASSA.
- Verifica esterna su 43fa6ac (https://github.com/Gasss23/Gas/pull/341#issuecomment-6672694572): V-1 MEDIA (ordine di merge: la #341 dopo la #339) → chiusa dichiarando l'ordine in §0, nella PR e in stato_progetto; V-2 = R-676-1; V-3 BASSA («fine» su un turno non di seguito non è coperto da test); V-4 BASSA (una «pausa» interrotta dalla parola non chiude: il ramo dell'interruzione viene prima).
- Bot su 851a0d1: V-1 MEDIA corretta (1792ab3); V-2 e V-3 corrette nel LEGGIMI.
- Bot su bdc79ce V-1 = R-693-2, alzata a MEDIA su 23d9c1c: corretta in 01b1089 (taglio a 1,5 s prima della parola).
- R-694-1 BASSA: residuo (0,3–0,7 s di stanza prima della parola; falso positivo nella finestra → il dopo è normale fino a 30 s), da far accettare all'operatore.
- R-694-2 BASSA: 1,5 s da provare sul Mac.
- Verifica esterna su 562f137 V-1 (= R-680-2) corretta in 165a9a4; R-695-1 BASSA (confine reale circa 1,84 s, senza test), R-695-2 BASSA (falso positivo entro circa 1,8 s: residuo da far accettare all'operatore).
- R-696-1/2 BASSE per M2 (C1 nei turni di seguito, routing su 6 messaggi), R-696-3 COSMETICA.
- Bot su 7e4a7d3: V-1 BASSA (il tetto dei turni di seguito, minimo 3 s, non tiene conto della pausa finale GAS_ASCOLTO_SILENZIO fino a 5 s: con valori estremi ogni seguito arriva al tetto e chiude), V-2 COSMETICA (LEGGIMI dice «nella conversazione senza la parola … resta il bip», ma i turni di seguito non hanno bip). Prossima fetta della voce.
- Verifica esterna su 7e4a7d3: V-1 = R-676-1, V-2 = R-694-1/R-695-2 (privacy, §0 punto 2), V-3 = V-3/V-4 della verifica su 43fa6ac, V-4 COSMETICA (§6 con run parziali).
- R-680-2 BASSA: parola sentita nella finestra prima della voce, il flag resta alto fino a fine finestra.
- R-681-1 COSMETICA: errori del rilevatore nella finestra senza riga di log.
- Restano le riserve delle fette 40, 41 e 43 parte 1, in `reports/stato_progetto.md`.
