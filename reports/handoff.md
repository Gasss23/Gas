# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V14: «Sì, signore?» (GET /voce/conferma) e filtro «Dimmi.» rivisto (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #335 (https://github.com/Gasss23/Gas/pull/335). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5176502466","url":"https://github.com/Gasss23/Gas/pull/335"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.

---

## §1 SCOPE & ESITO FETTE

- **V14.1 — `GET /voce/conferma`** (decisione dell'operatore, contratto con la chat Mani via M1): `FATTA` — «Sì, signore?» con la voce attuale, cache per id voce, 503/502 puliti senza cache.
- **V14.2 — V-1 bot #334** (ok/okay fuori dal filtro «Dimmi.»): `FATTA`.
- **V14.3 — R-668-2-M2** (parola di attivazione ripetuta): `FATTA`.
- **Proposta sulla velocità della voce** (solo documento): `DEFERITA — dopo questa fetta`, come da ordine di M1.
- **Client H24** (`clients/voice/ascolto.py`): `SALTATA — fuori perimetro` (chat Mani).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  2 ++
 modules/voice/server.py             | 58 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 reports/diff_sessione.md            | 10 +++++-----
 reports/handoff.md                  | n/d
 reports/ripartenza_m2.md            |  8 ++++----
 reports/stato_progetto.md           |  5 +++--
 reports/ultimo_report.md            | 22 +++++++++-------------
 tests/test_unit_voice_prova_voci.py | 44 ++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_stt.py        |  6 ++++--
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
882346f feat(voce): V14 — GET /voce/conferma «Sì, signore?» in cache per voce; filtro «Dimmi.» senza ok e con ripetizione (chat M2)
47d7a5b chore(revisore): memoria review #669 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #669-M2 sul commit 882346f (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #669-M2. Ho rivisto tutto il `git diff --cached` attuale, compreso l'aggiornamento del coordinatore: 3 file, +104/-4, branch feat/voce-v12-m2.

Ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md (in modo mirato) e .claude/agents/memoria_revisore.md. Nel diff non c'è slicing della history e non c'è simulazione di tool. Non tocca i guardrail del motore (`_get_window`, cap 10 iterazioni, cap 8k).

**Elementi del diff esaminati**
- `modules/voice/server.py:765` — è il ramo `/voce/conferma` in `do_GET`, con `_check_auth()` chiamato prima di qualunque spesa. Rischio esaminato: endpoint a pagamento esposto senza token. Il 401 è provato dal test. Esito: ok.
- `modules/voice/server.py:799` — è `_conferma`. Senza chiave dà 503. Ricava la voce come il percorso `/voice` (`modules/voice/server.py:599`), quindi la conferma ha la stessa voce della risposta. La chiave della cache è (voce, frase). Rischio esaminato: spesa ripetuta e cache "avvelenata". Il salvataggio avviene solo dopo un audio non vuoto (`modules/voice/server.py:826`). Esito: ok.
  - Mutante rieseguito da me: «cache senza confronto della chiave» viene ucciso da `test_v14_conferma_una_sintesi_per_voce` (`tests/test_unit_voice_prova_voci.py:691`). Il file è stato ripristinato e lo stage è intatto.
- `modules/voice/server.py:799` — gestione degli errori. Rischio esaminato: eccezioni che non vengono intercettate. Esito: riserva R-669-1-M2 (sotto).
- `modules/voice/server.py:120` — è `_ATTIVAZIONE_UNA` con la ripetizione in `_SOLO_ATTIVAZIONE`. Rischi esaminati: falsi positivi e backtracking catastrofico.
  - «Ok Gas.», «Gas, ciao», «Hey Jarvis, Hey Jarvis, accendi» e «gasolio» non vengono presi come sola attivazione. «Hey Jarvis, Hey Jarvis!», «Jarvis Gas» e «Gas, gas.» sì.
  - Con 5000 ripetizioni o separatori la regex risponde in circa 2 ms, quindi è lineare.
  - Esito: ok.
- `tests/test_unit_voice_stt.py:651` / `tests/test_unit_voice_stt.py:661` — sono i casi positivi con ripetizione e i negativi con ok/okay. Coprono V-1 bot #334 e chiudono R-668-2-M2. Esito: ok.
- `tests/test_unit_voice_prova_voci.py:712` — test degli errori 401/503/502. Dopo un errore la cache resta vuota e la richiesta successiva riprova. Esito: ok.

Ho rieseguito `tests/test_unit_voice_prova_voci.py` e `tests/test_unit_voice_stt.py`: 148 passed.

**Le due scelte da valutare**
- La conferma fuori dal tetto `GAS_VOICE_MAX_TURNI_ORA` è accettabile. La voce si legge dall'env del processo, quindi in pratica c'è un solo giro su ElevenLabs per processo, e senza token non si spende nulla.
- Niente lock sulla cache: è corretto, perché il server è un `HTTPServer` single-thread (`modules/voice/server.py:1004`). Se un giorno diventasse `ThreadingHTTPServer`, il caso peggiore sono due sintesi, non una corruzione.

**Riserve (vanno tracciate in stato_progetto.md)**
- **R-669-1-M2 (BASSA)** — `_conferma` intercetta solo `ElevenLabsTTSError` e `OSError`. Però `http.client.HTTPException` (es. `IncompleteRead` durante `resp.read()`) non è un `OSError`, e `synthesize_speech` in modules/voice/tts.py non la avvolge.
  - Effetto: il server non va in crash (ci pensa socketserver), ma la traccia finisce su stderr e non in gas_debug.log, e il client riceve una connessione chiusa invece di un 502.
  - È lo stesso limite dei percorsi TTS già esistenti. Soluzione consigliata: aggiungere `http.client.HTTPException` all'`except` di rete, oppure avvolgerla dentro tts.py.
- **R-669-2-M2 (COSMETICA)** — un saluto ripetuto senza nome in mezzo («Ehi ehi Jarvis») non conta come sola attivazione e va al cervello. È innocuo.

**Rischio escluso:** non ho verificato il comportamento reale con ElevenLabs né la riproduzione sul client H24 del Mac (clients/voice/ascolto.py, che è fuori dal diff e della chat Mani). In questo ambiente non ci sono chiave né audio, quindi l'unica prova è con i mock.

**Memoria:** ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #669-M2 e una lezione: `HTTPException` non è sottoclasse di `OSError`. È committata da sola con lo script, commit 47d7a5b. Lo stage del motore è intatto (3 file).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_prova_voci.py`: +2 test (`test_v14_conferma_una_sintesi_per_voce`, `test_v14_conferma_errori_puliti_senza_cache`); la fixture `server` azzera `conferma_cache`. `tests/test_unit_voice_stt.py`: casi del filtro aggiornati (positivi con ripetizione, negativi «Ok Gas.», «Okay, Jarvis», «Hey Jarvis, Hey Jarvis, accendi»). Mutanti uccisi: niente cache, chiave senza voce, audio vuoto in cache. Suite voce della CI in un venv con requirements + requirements-dev: `284 passed in 321.95s` prima del filtro rivisto; dopo, `-k "v13 or v6"` di voice_stt 46 passed e revisore 148 passed su voice_prova_voci + voice_stt. Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub.
- 47d7a5b, 882346f: nessuna run su 47d7a5b da solo (pushato insieme a 882346f); 882346f: run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (la run sul push finale testerà solo la testa).

## §7 RISERVE APERTE

- R-669-1-M2 BASSA: `http.client.HTTPException` non intercettata in `_conferma` (e negli altri percorsi TTS): connessione chiusa invece di 502, traccia fuori da gas_debug.log.
- R-669-2-M2 COSMETICA: «Ehi ehi Jarvis» (saluto ripetuto) va al cervello.
- R-668-1-M2 BASSA: «Dimmi.» spende ElevenLabs e un posto nel tetto orario. R-668-3-M2 BASSA: segno «attivazione» non testato nei formati audio+testo e NDJSON.
- R-667-2-M2 BASSA: fuso della macchina del server; sul VPS servirà un fuso configurabile (lì l'istruzione vieta anche data_ora). R-667-3-M2 COSMETICA: datetime naive → «fuso UTC».
- Verifica esterna #334: V-3 BASSA nessun tetto in codice al numero di frasi; V-4 COSMETICA ora presa a inizio turno.
- Bot su #332: V-1 BASSA (posto nel tetto del testo consumato se il turno fallisce), V-2 COSMETICA (commenti V12, 429 «o scrivi»).
