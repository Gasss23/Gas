# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-04 — Voce V12: il testo con risposta a voce conta nel tetto orario (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #332 (https://github.com/Gasss23/Gas/pull/332). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5146911127","url":"https://github.com/Gasss23/Gas/pull/332"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.

---

## §1 SCOPE & ESITO FETTE

- **V12 — R-663-1-M2** (decisione dell'operatore via M1): `FATTA` — una richiesta a testo con risposta a voce conta nel tetto orario; 429 prima del turno.
- **Altre BASSE**: R-660-1-M2 `FATTA` (test senza chiave), R-660-2-M2 `FATTA` (parola al tetto), V-2 cosmetica bot #330 su ae3258e `FATTA`, V-1 cosmetica bot #331 `FATTA`.
- **Riserve della review #665-M2** (R-665-1/2/3-M2): `FATTE` nella stessa fetta (review #666-M2 APPROVATO).
- **File di ripartenza** `reports/ripartenza_m2.md` (chiesto da M1 prima del clear della chat): `FATTA`.
- **Tetto sul numero di frasi** (V-1 verifica esterna su 956a00a): `DEFERITA` — non chiesta in questa fetta; il parlato resta entro 1500 caratteri.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/voice/server.py            |  37 ++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |   9 ++++-----
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |  31 +++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  19 +++++++++----------
 tests/test_unit_voice_server.py    |  90 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
89a176d docs(voce): file di ripartenza della chat M2 (PR #332)
bbf45e5 docs(voce-v12): report di fine task (PR #332, review #665–#666-M2)
f970f75 fix(voce): V12 — anche il testo con risposta a voce conta nel tetto orario; taglio al tetto senza perdere parole; riserve basse V10/V11 (review #665–#666-M2)
f573267 chore(revisore): memoria review #666 — APPROVATO
287d393 chore(revisore): memoria review #665 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della V12 (f970f75). Review #665-M2 sul primo diff:

## VERDETTO: APPROVATO CON RISERVE

Review #665-M2. Ho fatto le letture obbligatorie: CLAUDE.md, stato_progetto.md (le parti che servivano) e memoria_revisore.md. Oggetto: il diff staged su feat/voce-v12-m2, cioè modules/voice/server.py e tests/test_unit_voice_server.py.

**Elementi del diff esaminati**
- `modules/voice/server.py:432` — nuovo blocco del tetto orario per le richieste a testo con sintesi. Rischi esaminati: richieste a voce contate due volte e 429 che arriva dopo il lavoro del kernel. Il blocco gira solo con `not is_audio`. Sta dopo «uso» (che risponde 400 senza contare) e prima di `run_turn`, quindi il 429 arriva prima di qualsiasi lavoro. La voce resta contata una sola volta, in `_do_stt` (modules/voice/server.py:661, contesto). Il messaggio di modules/voice/server.py:439 è coerente con quello della voce (modules/voice/server.py:404): cambia solo il suggerimento («chiedi la risposta solo a testo» invece di «scrivi»). Esito: ok nel codice, riserva sui test (R-665-1).
- `modules/voice/server.py:514` — `_sintesi_a_testo()`. Rischio: che non corrisponda ai rami finali che chiamano la sintesi (modules/voice/server.py:478-482, contesto). Per il testo `_vuole_righe_senza_schermo()` è sempre False, quindi i rami sono identici a «`_vuole_audio_testo()` oppure (`_wants_audio()` e formato diverso da `audio+pezzi`)». Esito: ok, riserva sui test (R-665-2).
- `modules/voice/server.py:199` — `frasi_voce` legge un carattere oltre il tetto. Casi limite eseguiti, tutti con ogni pezzo ≤1500:
  - 1500 caratteri senza spazi → [1500], senza avviso;
  - 1501 senza spazi → [1500, avviso];
  - spazio in posizione 1500 → [1500, avviso], la parola non si perde;
  - spazio in posizione 1499 → [1499, avviso].
  
  Esito: ok.
- `tests/test_unit_voice_server.py:1397` — test del tetto: audio+testo e Accept audio/mpeg contano, solo testo e audio+pezzi no, poi 429 senza turno (`len(turni) == 4`). Esito: ok, ma vedi R-665-2.
- `tests/test_unit_voice_server.py:1389` — `audio+pezzi` senza chiave restituisce un JSON con `errore_voce` e zero sintesi. Esito: ok (è copertura in più).
- `tests/test_unit_voice_server.py:1221` — docstring di `_voce_a_pezzi` spostata prima dell'import, con il ritorno giusto (content-type, righe, mock). Esito: ok.
- Il tetto delle prove voci (`prove_voci`, `/voci/*`) non è toccato. `git diff --cached --check` è pulito.

**Prove (mutanti in una copia in scratch; il repo vero non è stato toccato)**
- Base `-k "v10 or v11 or v12 or v7b"`: 19 passed. Suite completa voice_server + voice_stt sul repo: 199 passed.
- Mutanti uccisi (i test V12 falliscono):
  - tolta la registrazione in `turni_parlati`;
  - ripristinato il vecchio taglio `testo[:MAX].rsplit`.
- **Mutanti sopravvissuti:**
  - tolto `not is_audio` a modules/voice/server.py:432. Una richiesta a voce con audio+testo verrebbe contata due volte e potrebbe ricevere il 429 dopo aver già speso Groq. Nessun test se ne accorge.
  - tolta l'esclusione `!= _FORMATO_PEZZI_VOCE` in `_sintesi_a_testo`. Il test sopravvive perché manda `audio+pezzi` senza `Accept: audio/mpeg`, mentre clients/voice/ascolto.py:520 lo manda.

**Riserve (da tracciare in stato_progetto.md)**
- R-665-1-M2 BASSA: la guardia `not is_audio` (modules/voice/server.py:432) non ha un test. Serve un test a voce con audio+testo e tetto 2 che controlli che ogni richiesta conti una volta sola.
- R-665-2-M2 BASSA: l'esclusione di `audio+pezzi` in `_sintesi_a_testo` non ha un test. In tests/test_unit_voice_server.py:1436 va aggiunto `Accept: audio/mpeg`, come fa il client H24. Se si sbaglia si conta in eccesso (lato sicuro), quindi non blocca.
- R-665-3-M2 BASSA: il testo con sintesi conta anche quando manca `ELEVENLABS_API_KEY`. In quel caso non si spende niente su ElevenLabs, e oltre il tetto si riceve un 429 invece del 503 utile. Questo va contro il principio V5 («i rifiuti locali non contano», modules/voice/server.py:657-660). Proposta: contare solo se la chiave c'è, oppure dichiararlo.

**Rischi esclusi (non verificati)**
- Race sul contatore `turni_parlati` con più thread (leggi-modifica-scrivi senza lock): il comportamento è lo stesso di prima nel percorso voce e non l'ho provato sotto concorrenza.
- Comportamento dal vero con ElevenLabs e il client ascolto.py sul Mac: non riproducibile qui, la sintesi è finta.
- Taglio patologico «a » seguito da 1600 caratteri senza spazi → si dice solo «a»: comportamento che esisteva già prima, irrealistico, non trattato.

**Memoria**
Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #665-M2 e una lezione: quando una condizione copia dei rami, va mutata ogni congiunzione. Ho committato con `scripts/commit_memoria_revisore.sh` (commit 287d393, solo quel file). Il diff staged di server.py e del test è rimasto intatto.

Review #666-M2 sul diff finale (con le tre riserve chiuse):

## VERDETTO: APPROVATO

Review #666-M2 sul branch feat/voce-v12-m2. Ho rivisto tutto il diff staged (`git diff --cached`: modules/voice/server.py e tests/test_unit_voice_server.py), non solo la parte nuova. Ho fatto le tre letture obbligatorie: CLAUDE.md, reports/stato_progetto.md e la mia memoria, inclusa la riga #665-M2 con le tre riserve.

**Parti del diff esaminate**
- `modules/voice/server.py:432` — blocco del tetto orario per le richieste a testo che chiedono la risposta a voce. Ora scatta solo se valgono tre condizioni: la richiesta non è a voce (`not is_audio`), chiede la sintesi (`_sintesi_a_testo()`) e `ELEVENLABS_API_KEY` c'è.
  - Rischi esaminati: una richiesta a voce contata due volte (prima per Groq, poi qui); un rifiuto locale senza chiave che consuma un posto nel tetto (contro il principio V5).
  - Esito: ok. Il controllo avviene prima del turno: oltre il tetto risponde 429 e il kernel non parte. Il percorso «uso» esce con 400 prima del conteggio. Le richieste a voce vengono contate solo nel blocco esistente prima della trascrizione.
- `modules/voice/server.py:516` — `_sintesi_a_testo()` ripete le stesse condizioni della risposta finale (righe 487-490).
  - Rischio esaminato: una richiesta a testo «audio+pezzi» con `Accept: audio/mpeg` contata anche se dopo la V11 riceve solo testo.
  - Esito: ok. Formato uguale a `_FORMATO_PEZZI_VOCE` → nessun conteggio, e la risposta finale va a JSON. Le due cose restano allineate.
- `modules/voice/server.py:197` — `frasi_voce`: il taglio guarda anche il carattere subito dopo il tetto (parte già approvata nella #665).
  - Esito: ok, il mutante che ripristina il vecchio taglio viene ucciso.
- `tests/test_unit_voice_server.py:1396` — `test_v12_testo_con_sintesi_conta_nel_tetto`: server vero con kernel finto, sintesi e trascrizione finte, tetto 3.
  - Verifica tre cose: due richieste a voce più una a testo con voce riempiono il tetto, mentre testo puro e audio+pezzi+Accept non contano; poi 429 per testo e per voce; senza chiave, con tetto 1, due 200 e lista dei conteggi vuota.
  - Rischio esaminato: test che dipende dall'ordine, perché la lista dei conteggi è condivisa a livello di classe.
  - Esito: ok. Il test usa una sottoclasse `_H` e il server scrive con `type(self)`, quindi la classe base non viene toccata. La suite completa passa.
- `tests/test_unit_voice_server.py:1222` — la docstring di `_voce_a_pezzi` torna nella posizione giusta, prima dell'import. Esito: ok, cosmetico.

**Prove eseguite da me**
- `tests/test_unit_voice_server.py` + `tests/test_unit_voice_stt.py`: 199 passati.
- 6 mutanti su una copia presa dall'index nella cartella scratch, file originale ripristinato e confrontato con `cmp`:
  1. tolto `not is_audio`
  2. tolta l'esclusione `!= _FORMATO_PEZZI_VOCE`
  3. tolta la condizione sulla chiave
  4. tolta la riga che registra il conteggio
  5. ripristinato il vecchio taglio di `frasi_voce`
  6. tolto `_vuole_audio_testo()` da `_sintesi_a_testo`
  Tutti uccisi (1 test fallito ciascuno). Le riserve R-665-1, R-665-2 e R-665-3-M2 sono chiuse.

**Nota BASSA, non bloccante e non tracciata come riserva:** il conteggio del testo avviene prima del turno. Se il kernel fallisce (500), quel posto nel tetto resta consumato anche se ElevenLabs non è stato chiamato. Per le richieste a voce succede già lo stesso, ma lì Groq è stato speso davvero.

**Cosa non ho verificato**
- Il comportamento con il client H24 reale e con ElevenLabs/Groq veri: i test usano servizi finti e il client reale non è riproducibile qui.
- La finestra di un'ora che scade davvero: non ho simulato `time.monotonic` oltre i 3600 secondi.

**Memoria:** riga #666-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit f573267). Il diff staged è intatto: restano in stage solo i due file.

Copia scratch e script dei mutanti:
- /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratch/m666
- /tmp/claude-0/-home-user-Gas/363006d5-ae75-5e2f-8a8d-a34502419f69/scratch/mut.sh

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: 104 → 107 test (`test_v12_frasi_voce_parola_al_tetto`, `test_v12_audio_pezzi_senza_chiave_json`, `test_v12_testo_con_sintesi_conta_nel_tetto`). Con `modules/voice/server.py` di main falliscono i due test V12 di codice (il terzo è copertura). Mutanti del revisore: 6 su 6 uccisi. voice_server + voice_stt: 199 passed. Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette dalle notifiche.
- 287d393, f573267, f970f75, bbf45e5, 89a176d e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (f970f75 pushato prima dei report; la run sul push finale testerà solo la testa).

## §7 RISERVE APERTE

- Verifica esterna su 956a00a, V-1 BASSA: nessun tetto al numero di frasi (entro 1500 caratteri), deferita.
- Nota bassa del revisore #666-M2 (non tracciata come riserva): se il kernel fallisce, il posto nel tetto del testo resta consumato.
