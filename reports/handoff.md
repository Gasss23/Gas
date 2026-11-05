# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V13: ora locale nel turno parlato e risposte a voce più corte (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #334 (https://github.com/Gasss23/Gas/pull/334). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5175852245","url":"https://github.com/Gasss23/Gas/pull/334"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.

---

## §1 SCOPE & ESITO FETTE

- **V13.1 — ora locale nel turno parlato** (decisione dell'operatore via M1, prova sul Mac del 5 novembre): `FATTA` — `ora_per_voce` / `istruzione_turno_voce`; «che ore sono» senza il giro di `data_ora`.
- **V13.2 — risposte a voce più corte**: `FATTA` — «una o due frasi, mai più di due», senza premesse, con e senza schermo.
- **V13.4 — niente «… sì o no?» in coda** (cronologia della prova sul Mac, da M1): `FATTA`.
- **V13.5 — «Hey Jarvis» da solo → «Dimmi.» senza turno** (cronologia della prova, da M1): `FATTA`.
- **Note del bot su 8416674** (V-1 BASSA istruzioni in conflitto con «usa data_ora», V-2 COSMETICA «01:30»): `FATTE`.
- **R-667-1-M2** (test dell'ora cieco con TZ=UTC; = V-1 verifica esterna su 8416674): `FATTA` — TZ forzato, mutante ucciso.
- **V13.3 — indagine «Stefano»**: `DEFERITA — non diagnosticabile dal cloud` (il parlato non è nei log per privacy V6; la storia è sul Mac). Dalla cronologia mandata da M1: quasi sicuramente dalla storia condivisa (riepilogo di sessioni precedenti); l'operatore vuole una sola storia, quindi va curato nella proposta sulla velocità.
- **Soglia `GAS_ASCOLTO_VOCE_RMS`**: `SALTATA — fuori perimetro` (`clients/voice/ascolto.py` è della chat Mani); segnalata a M1.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/voice/server.py            |  64 ++++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 reports/diff_sessione.md           |  11 ++++++-----
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |   8 ++++++--
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  22 +++++++++++++---------
 tests/test_unit_voice_server.py    |  58 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_voice_stt.py       |  43 ++++++++++++++++++++++++++++++++++++++++---
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
87ebf99 feat(voce): V13 — niente «sì o no?» in coda, «Hey Jarvis» da solo senza turno, note bot #334 (chat M2)
6a058ce chore(revisore): memoria review #668 — APPROVATO
db509c2 chore(revisore): memoria review #668 — APPROVATO CON RISERVE
8416674 docs(voce): report di fine task V13 (chat M2)
cf6233a feat(voce): V13 — ora locale nel turno parlato e risposte a voce più corte (chat M2)
faaf406 chore(revisore): memoria review #667 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #667-M2 sul commit cf6233a (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #667-M2: V13, diff STAGED su feat/voce-v12-m2. Ho fatto le tre letture obbligatorie: CLAUDE.md, reports/stato_progetto.md e la memoria del revisore.

**Cosa ho esaminato nel diff**
- `modules/voice/server.py:174`: `ora_per_voce` calcola l'ora con `datetime.now().astimezone()`, come fa data_ora in gas.py. I nomi di giorni e mesi vengono da tuple italiane, quindi non dipende dal locale. Se `tzname()` manca, scrive `UTC%z`. Ho controllato il fuso, il cambio d'anno e la dipendenza dal locale: **ok**.
- `modules/voice/server.py:481`: il ramo `is_audio` ora usa `istruzione_turno_voce(self._vuole_audio_testo())`, che viene calcolata una sola volta prima di `run_turn`. Ho provato un mutante in una copia scratch dall'index, rimettendo la vecchia costante: falliscono `tests/test_unit_voice_server.py:1343` (V10) e i test V1/V3/V4 di `tests/test_unit_voice_stt.py:454`. Il ramo è protetto dai test: **ok**.
- `modules/voice/server.py:146`: ISTRUZIONE_VOCE e ISTRUZIONE_VOCE_SCHERMO ora dicono «una o due frasi, mai più di due», senza premesse. Sono testi di prompt e non hanno rischi tecnici; `tests/test_unit_voice_server.py:1677` verifica «mai più di due» e l'assenza di «1-3»: **ok**.
- `tests/test_unit_voice_server.py:1666`: questo test non distingue l'ora locale dall'ora senza fuso quando la macchina è in UTC. Il mutante `datetime.now()` senza fuso **sopravvive** con TZ=UTC (container cloud e CI) ed è ucciso solo con TZ=Europe/Rome: **riserva** (R-667-1-M2).
- Contesto, non toccato dal diff: `gas.py:4836` costruisce il messaggio system come `system_prompt + mem_pin + lezioni_pin + recap_pin + turno_pin`. L'ora finisce quindi in coda al messaggio system, dopo `recap_pin`, che cambia già a ogni domanda.

**Effetti sulla cache dei prompt (domanda dell'operatore):** trascurabili.
- La parte fissa iniziale (`system_prompt`, poi la memoria) resta uguale tra un turno e l'altro.
- La cache della storia, che viene dopo il messaggio system, era già persa a ogni turno per via di `recap_pin`, che cambia a ogni domanda.
- Dentro un turno, fino a 10 giri, l'ora resta fissa, quindi i giri successivi possono riusare la cache.
- I provider gratuiti non hanno costi di cache. Quando arriverà il cervello forte Claude (roadmap R2), l'ora nel messaggio system peserà quanto `recap_pin` e non di più.
- Effetto pratico minimo: l'ora può essere indietro fino a un turno lungo (circa 17 s), cosa accettabile per una risposta a voce.

**Finding**
- **R-667-1-M2 (BASSA)**: `tests/test_unit_voice_server.py:1666` non vede la differenza tra ora con fuso e ora senza fuso in un ambiente UTC (CI e cloud). Correzione: nel test forzare `TZ=Europe/Rome` con `monkeypatch.setenv` e `time.tzset()`, oppure simulare `datetime`.
- **R-667-2-M2 (BASSA)**: l'ora è quella della macchina che fa girare il server. Oggi è il Mac, quindi va bene. Quando Gas passerà alla VPS (spesso in UTC) l'ora detta all'operatore sarà sbagliata, a meno di un fuso configurabile, per esempio una variabile d'ambiente. Va annotato in roadmap e stato_progetto.
- **R-667-3-M2 (COSMETICA)**: se a `ora_per_voce` arriva un'ora senza fuso, la frase dice «fuso UTC» anche quando non è vero. La docstring lo avverte e solo i test passano `adesso`.
- **Dichiarazione incompleta**: il diff tocca anche `tests/test_unit_voice_stt.py` (3 asserzioni rese più larghe allo stesso modo), che la richiesta non elencava. Il contenuto va bene.

**Test**
- 199 passed e 3 failed.
- I 3 falliti sono: `test_v1_run_server_carica_il_dotenv`, `test_v1_run_server_dotenv_rotto_non_crasha` e `test_collection_dell_intero_repo_non_esplode`. Nel container manca il modulo `openai`.
- I due test dotenv falliscono uguali a HEAD (provato in una copia di HEAD). Il terzo non l'ho ripetuto a HEAD: lo considero preesistente perché anche lui carica tutto il repo.
- Il numero dichiarato «280 passed» non l'ho riprodotto: l'ambiente dell'agente è diverso.

**Cosa NON ho verificato**
- Il caso «non trovo il contatto Stefano» in risposta a «che ore sono»: dal cloud non si può riprodurre (il parlato non viene registrato per privacy e la storia sta sul Mac).
- Se il modello rispetta davvero «mai più di due frasi» e usa l'ora senza chiamare data_ora: è un comportamento del cervello, si verifica solo con una prova vocale reale sul Mac.

Memoria aggiornata con la riga #667-M2 e una lezione (i test sul fuso non vedono nulla in CI con TZ=UTC: rifare il mutante con un fuso diverso). Committata con `scripts/commit_memoria_revisore.sh` (faaf406). Il diff staged è rimasto intatto (3 file).

Review #668-M2 sul commit 87ebf99 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #668-M2: è il diff STAGED attuale di feat/voce-v12-m2 (PR #334), quindi comprende anche le correzioni V-1 e V-2 del bot #334 che il coordinamento ha aggiunto mentre la review era in corso. 3 file, +73/-20. Ho letto CLAUDE.md (sez. 5), stato_progetto (riga V13) e la memoria.

Elementi del diff esaminati:
- modules/voice/server.py:112 — `_SOLO_ATTIVAZIONE`, regex ancorata con `^…$`: saluto opzionale, poi jarvis/gas/gus, poi solo punteggiatura. Rischio: falsi positivi su richieste vere. L'ho provata su 18 frasi.
  - Riconosciute: «Hey Jarvis!», «Gas.», «Ciao Gas», «Okay, Gas!», «Gus», «... Jarvis ...», «Ehi Jarvis.\n».
  - Non riconosciute, come deve essere: «gas forte», «Hey Gas, ci sei?», «Gasp», «Grazie Jarvis», «Ciao Jarvis, grazie».
  - Esito: ok.
- modules/voice/server.py:449 — il filtro sta dopo `_do_stt` e prima di `cervello_voce`, solo nel ramo `is_audio`. Rischi esaminati:
  - Parola «forte»: «Gas forte» non viene riconosciuto e cade sulla risposta d'uso come prima. Con `GAS_VOCE_FORTE=1`, «Hey Jarvis» riceve «Dimmi.» senza turno: nessuna spesa sul cervello forte, direzione sicura.
  - Tetto orario: la richiesta resta contata (`turni_parlati` in modules/voice/server.py:703, prima di chiamare Groq).
  - Formato: passa da `_rispondi_senza_turno`, quindi audio+testo, pezzi/NDJSON e il ripiego a testo funzionano come per «uso» e «non_capito».
  - Esito: ok.
- modules/voice/server.py:158 (e :169) — la frase «Non chiudere con domande né con offerte…» sostituisce «chiudi con una domanda secca sì/no» in entrambe le istruzioni. Rischio: un residuo della vecchia frase. Il test verifica l'assenza di «chiudi con una domanda» in tutte e due. Esito: ok.
- modules/voice/server.py:191 — `ora_per_voce`: «Adesso è giovedì 5 novembre 2026, ore 18:07…», ora senza zero iniziale (V-2), e «In questo turno… NON usare data_ora: vale al posto dell'indicazione generale». Rischio: istruzioni in contrasto. Ho controllato il contesto in gas.py:135 («per data e ora usa data_ora»): la precedenza adesso è scritta per esteso e vale solo per il turno parlato. Esito: ok.
- tests/test_unit_voice_stt.py:644 — test con 6 casi riconosciuti e 4 no (con la sentinella `kernel.kw` che dimostra se il turno c'è stato o no), più il test che a testo «Hey Jarvis» resta una richiesta normale. Esito: ok, con la riserva 3.
- tests/test_unit_voice_server.py:1658 — le asserzioni seguono il nuovo testo dell'ora; il caso EET «ore 1:30» copre il cambio di giorno. Esito: ok.

Caccia agli antipattern: nessuno slicing della cronologia, nessuna simulazione di output dei tool, nessun guardrail toccato (tetto 10 iterazioni, `_get_window`, tetto orario).

Test: 201 passed su tests/test_unit_voice_stt.py e tests/test_unit_voice_server.py. Altri 3 falliscono per una causa che sta solo in questo ambiente: l'interprete di pytest non ha i moduli `openai` e `yaml` (`test_collection_dell_intero_repo_non_esplode` e i due `test_v1_run_server_*dotenv*`, `ModuleNotFoundError`). Non dipendono dal diff.

Riserve (BASSE):
- R-668-1-M2: «Dimmi.» spende ElevenLabs e occupa un posto del tetto orario, come «non ho capito». Accettabile, ma l'operatore deve saperlo.
- R-668-2-M2: la ripetizione «Hey Jarvis, Hey Jarvis» (Whisper raddoppia spesso la parola) non viene riconosciuta e arriva al cervello. Rimedio facile: ripetizione `(?:…\W*)+`.
- R-668-3-M2: nessun test che verifichi il segno `attivazione` nei formati audio+testo e pezzi/NDJSON. Lo garantisce solo il percorso condiviso con «uso» e «non_capito».

«Ciao Gas» da solo che riceve «Dimmi.»: per me va bene, è un saluto senza richiesta.

Rischio escluso: non ho verificato il comportamento reale con Whisper ed ElevenLabs e il ciclo di clients/voice/ascolto.py sul Mac (dopo «Dimmi.» la finestra di conversazione conta un turno), perché in questo ambiente non si può riprodurre. Non ho verificato nemmeno se i modelli rispettano davvero «non chiudere con domande»: è un'istruzione al modello e la si vede solo con prove dal vivo.

Memoria: riga #668-M2 più la lezione sulla ripetizione della parola di attivazione, in /home/user/Gas/.claude/agents/memoria_revisore.md, già committata (db509c2, solo quel file; lo stage del diff è rimasto intatto).

Review #668-M2 bis sullo stage finale di 87ebf99 (+89/-26, verdetto integrale):

## VERDETTO: APPROVATO

Revisione #668-M2 bis: copre solo la parte aggiunta allo stage dopo il verdetto #668-M2, cioè la chiusura di R-667-1-M2 in tests/test_unit_voice_server.py. Lo stage attuale è di 3 file, +89/-26. Il resto del diff è già coperto dal verdetto #668-M2, che resta APPROVATO CON RISERVE con R-668-1/2/3-M2.

Elementi esaminati:
- tests/test_unit_voice_server.py:1673 — il test forza `TZ=Asia/Kolkata` (UTC+5:30, senza ora legale) con `monkeypatch.setenv` e `time.tzset()`, e controlla che lo scarto sia di 5,5 ore. Rischio: un test cieco quando CI e cloud girano in UTC (la lezione del 2026-11-05). L'ho verificato con un mutante in una copia dall'index: `datetime.now()` senza `.astimezone()` in modules/voice/server.py:187, eseguito con `TZ=UTC` → il test fallisce, quindi il mutante è ucciso. Senza il mutante passa. Esito: ok.
- tests/test_unit_voice_server.py:1682 — nel `finally` ci sono `monkeypatch.undo()` e poi `time.tzset()`. Rischio: il fuso forzato che passa ai test successivi. L'ordine è giusto, perché prima si ripristina TZ e poi si ricarica il fuso. Sulla stessa copia la suite voce completa (tests/test_unit_voice_server.py + tests/test_unit_voice_stt.py) dà 201 passed. I 2 KO sono quelli già noti `test_v1_run_server_*dotenv*`: manca `openai` nell'interprete di pytest locale, quindi dipendono dall'ambiente e non dal diff. Esito: ok.
- Contesto: modules/voice/server.py:188 ripiega su `ora.strftime("UTC%z")` quando il fuso manca. È per questo che l'asserzione `"fuso UTC" not in frase` riconosce l'ora senza fuso. Esito: ok.

Rischio escluso: non ho verificato il comportamento su Windows, dove `time.tzset` non esiste e il test andrebbe in errore. Il progetto gira su Mac e Linux e la CI è Linux, quindi oggi non serve. Va annotato solo se un giorno la suite girasse su Windows.

Memoria: ho aggiunto la riga «#668-M2 bis» in /home/user/Gas/.claude/agents/memoria_revisore.md, così il contatore copre anche lo stage +89/-26. È committata da sola (6a058ce) e lo stage del diff è rimasto intatto.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: +3 test V13 (`test_v13_ora_per_voce_data_ora_e_fuso_locali`, `test_v13_ora_per_voce_senza_argomento_usa_l_orologio_locale` con TZ forzato ad Asia/Kolkata, `test_v13_istruzione_turno_voce_con_e_senza_schermo`); `tests/test_unit_voice_stt.py`: +2 test (`test_v13_solo_parola_di_attivazione_nessun_turno`, `test_v13_attivazione_solo_dal_parlato`); 4 asserzioni esistenti (V3, V4, V10, uso «forte») a `startswith(ISTRUZIONE + " Adesso è ")`. Suite voce della CI in un venv con requirements + requirements-dev: `280 passed in 316.38s` su cf6233a; `282 passed in 311.31s` sullo stage di 87ebf99 prima della modifica al test del fuso; dopo quella modifica `-k v13` 3 passed e mutante «ora senza fuso» ucciso in TZ=UTC (revisore #668-M2 bis: voice_server + voice_stt 201 passed, 2 KO d'ambiente per `openai` mancante). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub (`get_check_runs` della PR #334).
- faaf406, cf6233a: nessuna run su questi SHA da soli (pushati insieme a 8416674).
- 8416674 (testa del push precedente): unit-suite success, handoff-check success, verifica-bot success (bot: APPROVATO CON RISERVE, V-1 BASSA e V-2 COSMETICA, chiuse in 87ebf99).
- db509c2, 6a058ce, 87ebf99 e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme: la run testerà solo la testa).

## §7 RISERVE APERTE

- R-667-2-M2 BASSA: l'ora è quella della macchina del server; sul VPS servirà un fuso configurabile (verifica esterna #334 V-2: lì l'istruzione vieta anche data_ora).
- R-667-3-M2 COSMETICA: un datetime naive passato a `ora_per_voce` direbbe «fuso UTC».
- R-668-1-M2 BASSA: «Dimmi.» spende ElevenLabs e un posto nel tetto orario.
- R-668-2-M2 BASSA: «Hey Jarvis, Hey Jarvis» (ripetizione di Whisper) non riconosciuto.
- R-668-3-M2 BASSA: segno «attivazione» non testato nei formati audio+testo e NDJSON.
- Verifica esterna #334 su 8416674: V-3 BASSA nessun tetto in codice al numero di frasi; V-4 COSMETICA ora presa a inizio turno.
- Bot su #332 (10fe496): V-1 BASSA (posto nel tetto del testo consumato se il turno fallisce), V-2 COSMETICA (commenti V12, 429 «o scrivi»).
