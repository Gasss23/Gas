# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V13: ora locale nel turno parlato e risposte a voce più corte (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #334 (https://github.com/Gasss23/Gas/pull/334). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5175852245","url":"https://github.com/Gasss23/Gas/pull/334"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.

---

## §1 SCOPE & ESITO FETTE

- **V13.1 — ora locale nel turno parlato** (decisione dell'operatore via M1, prova sul Mac del 5 novembre): `FATTA` — `ora_per_voce` / `istruzione_turno_voce`; «che ore sono» senza il giro di `data_ora`.
- **V13.2 — risposte a voce più corte**: `FATTA` — «una o due frasi, mai più di due», senza premesse, con e senza schermo.
- **V13.3 — indagine «Stefano»**: `DEFERITA — non diagnosticabile dal cloud` (il parlato non è nei log per privacy V6; la storia è sul Mac). Riportata a M1 col controllo da fare.
- **Soglia `GAS_ASCOLTO_VOCE_RMS`**: `SALTATA — fuori perimetro` (`clients/voice/ascolto.py` è della chat Mani); segnalata a M1.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 modules/voice/server.py            | 37 ++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           | 11 ++++++-----
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |  7 +++++--
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 17 ++++++++---------
 tests/test_unit_voice_server.py    | 45 ++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_voice_stt.py       | 10 +++++++---
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: +3 test (`test_v13_ora_per_voce_data_ora_e_fuso_locali`, `test_v13_ora_per_voce_senza_argomento_usa_l_orologio_locale`, `test_v13_istruzione_turno_voce_con_e_senza_schermo`); 4 asserzioni esistenti (V3, V4, V10, uso «forte») da uguaglianza a `startswith(ISTRUZIONE + " Adesso sono le ")`. Suite voce della CI (voice_server, voice_stt, voice_tts, voice_contesto, voice_prova_voci) in un venv con requirements + requirements-dev: `280 passed in 316.38s`. Nel container del revisore (senza `openai`) 199 passed e 3 failed preesistenti. Mutante «vecchia costante» ucciso; mutante «ora senza fuso» sopravvive con TZ=UTC (R-667-1-M2). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub.
- faaf406, cf6233a e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (faaf406 e cf6233a pushati insieme: una run sola che testa la testa cf6233a; la run sul push finale testerà solo la testa).

## §7 RISERVE APERTE

- R-667-1-M2 BASSA: test dell'ora senza argomento cieco con TZ=UTC (forzare TZ nel test).
- R-667-2-M2 BASSA: l'ora è quella della macchina del server; sul VPS servirà un fuso configurabile.
- R-667-3-M2 COSMETICA: un datetime naive passato a `ora_per_voce` direbbe «fuso UTC».
- Bot su #332 (10fe496): V-1 BASSA (posto nel tetto del testo consumato se il turno fallisce), V-2 COSMETICA (commenti V12, 429 «o scrivi»).
- Verifica esterna su 956a00a, V-1 BASSA: nessun tetto al numero di frasi (entro 1500 caratteri), deferita.
