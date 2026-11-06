# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 43 parte 2: finestra di 40 s e difese contro il parlato della stanza (PR #341)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #341 (https://github.com/Gasss23/Gas/pull/341) SOLO DOPO (o insieme a) la PR #339 di M2 (V15, lato server): la #339 è in main (3cde8a5) e unita qui (ac06f01); l'operatore ha detto sì (via M1). Motivo (V-1 MEDIA della verifica esterna): senza la #339 in main la #341 allunga la finestra da 12 a 40 s e mette il tetto di 15 s, ma il filtro «parlato non per Gas» e la «pausa» non esistono ancora sul server, quindi il parlato della stanza sotto i 15 s verrebbe ancora inviato e risposto per 40 s invece che 12. Review #676 APPROVATO CON RISERVE e PR nel perimetro: decide l'operatore tramite M1. Numero e URL dalla risposta dello strumento GitHub `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **PR #340 (fetta 42)**: `FATTA` — mergiata (83f3bcd) col sì dell'operatore, CI verde; riserve nuove di bot e verifica esterna registrate.
- **Fetta 43 parte 2 — finestra di 40 s, turni di seguito con tetto 15 s, X-Gas-Seguito, comandi fine/pausa**: `FATTA` — review #676 APPROVATO CON RISERVE. Il commit di merge su main ha un diff identico a quello rivisto.
- **R-676-1/2 (test di stato e svuota dopo «fine»)**: `DEFERITA — BASSE, registrate, prossima fetta della voce`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++
 clients/voice/ascolto.py           | 144 ++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------
 reports/diff_sessione.md           |  20 ++++------
 reports/stato_progetto.md          |   6 ++-
 reports/ultimo_report.md           |  57 ++++++++++++++--------------
 scripts/voce/LEGGIMI.md            |  28 ++++++++++----
 tests/test_unit_voce_ascolto.py    | 230 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 3cde8a5 (dopo il merge della PR #339).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 220 (main dopo la #340) a 248 casi. Riepilogo reale nel venv con requirements e requirements-dev:

```
248 passed in 28.02s
```

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
- ac06f01 (merge della #339) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (si pushano insieme).
- a7ed0e8 e 43fa6ac: run dei loro push (handoff-check success; unit-suite non riletta qui).
- 51c4aa0, 4cd7b97, da24b2c: pushati insieme a 43fa6ac.

Suite voce in locale dopo il merge (ascolto, stt, prova_voci): 410 passed. Prova d'integrazione del revisore #679 con client e server veri: 21 passed.

## §7 RISERVE APERTE

- R-676-1 BASSA: due mutanti di stato sopravvivono (`self.chiudi` non azzerato; «pausa» che chiude solo nei turni di seguito).
- R-676-2 BASSA: lo svuota dopo «fine» non è coperto da test.
- R-676-3 BASSA, per M2 (girata a M1): trascrizione incerta di seguito → «Non ho capito» a voce invece di «fine».
- Dalla #340: bot V-1 BASSA (conferma non suonabile = silenzio), verifica esterna V-4 BASSA (eco dopo la conferma), R-675-1 BASSA.
- Verifica esterna su 43fa6ac (https://github.com/Gasss23/Gas/pull/341#issuecomment-6672694572): V-1 MEDIA (ordine di merge: la #341 dopo la #339) → chiusa dichiarando l'ordine in §0, nella PR e in stato_progetto; V-2 = R-676-1; V-3 BASSA («fine» su un turno non di seguito non è coperto da test); V-4 BASSA (una «pausa» interrotta dalla parola non chiude: il ramo dell'interruzione viene prima).
- Restano le riserve delle fette 40, 41 e 43 parte 1, in `reports/stato_progetto.md`.
