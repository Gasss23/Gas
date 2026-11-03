# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-03 — Voce V11: «audio+pezzi» a testo solo testo (chat M2, coordinata da M1) — aggiornato dopo il merge di main (#329) e i verdetti su d8f4572

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #331 (https://github.com/Gasss23/Gas/pull/331). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5140968063","url":"https://github.com/Gasss23/Gas/pull/331"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.

2. R-663-1-M2 BASSA: decidere se mettere un tetto anche alla sintesi chiesta da richieste a testo (`Accept: audio/mpeg`, `audio+testo`, `audio+testo+pezzi`) o dichiarare fidati i client a testo.

---

## §1 SCOPE & ESITO FETTE

- **V11 — V-1 BASSA del bot #330 su ae3258e**: `FATTA` — `audio+pezzi` a testo → solo JSON, niente ElevenLabs (review #663-M2 APPROVATO CON RISERVE).
- **V-2 COSMETICA del bot su ae3258e**: `REGISTRATA` in stato_progetto (col taglio il parlato è 1500+38 caratteri).
- **Docstring impreciso del test V10** (V-1 bot su ef88184): `FATTA`.
- **ThreadingHTTPServer per il server voce** (riserva bot #329): `VALUTATA`, sconsigliato ora (parere nella review #663-M2); nessun codice.
- **Bot su d8f4572** (APPROVATO CON RISERVE, verifica-bot success): V-1 COSMETICA (commento dell'helper `_voce_a_pezzi` con il ritorno sbagliato) `REGISTRATA`, senza giro.
- **Verifica esterna su d8f4572** (commento https://github.com/Gasss23/Gas/pull/331#issuecomment-6609937549, APPROVATO CON RISERVE): V-1 BASSA = R-663-1-M2; V-2 BASSA (un client col token può dichiarare `Content-Type: audio/*`: passa comunque dal tetto, nessuna azione); V-3 COSMETICA (ramo «uso» a testo, nessun effetto); V-4 COSMETICA (testi «entro 1500»): `REGISTRATE`, senza giro.
- **Merge di origin/main (#329, fetta 39 della chat Mani) nel branch**: `FATTA` (review #664-M2 APPROVATO).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 modules/voice/server.py            |  11 ++++++++---
 reports/diff_sessione.md           |  18 +++++++-----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  34 +++++++++++++++++-----------------
 tests/test_unit_voice_server.py    |  30 ++++++++++++++++++++++++------
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
049d927 Merge remote-tracking branch 'origin/main' into feat/voce-v11-m2
d8f4572 docs(voce-v11): handoff, blocco §2 corretto (PR #331)
1bd0d32 docs(voce-v11): report di fine task (PR #331, review #663-M2)
c91ccb8 fix(voce): V11 — «audio+pezzi» a testo riceve solo il testo, niente sintesi fuori dal tetto orario (V-1 bot #330 su ae3258e; review #663-M2)
7c17275 chore(revisore): memoria review #663 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della V11 (c91ccb8). Review #663-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #663-M2. Branch feat/voce-v11-m2, diff staged su 2 file (modules/voice/server.py, tests/test_unit_voice_server.py). Prima ho letto CLAUDE.md, reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/voice/server.py:280`: `_parlato: bool = False` a livello di classe. Rischio: lo stato passa da una richiesta all'altra sulla stessa connessione (keep-alive). Esito: ok. Il valore della classe è un bool immutabile e la riga 354 lo crea per istanza a ogni do_POST.
- `modules/voice/server.py:354`: azzeramento a inizio do_POST. Rischio: i percorsi /voci/prova e /voci/aggiungi. Esito: ok. Prendono False e non lo leggono mai. I rami di errore prima della riga 391 (401, Content-Length, 404) usano solo `_send_json` e non leggono `_parlato`.
- `modules/voice/server.py:391`: `self._parlato = is_audio`, assegnato prima del tetto orario e di `_do_stt`. Rischio: che «non ho capito» (da `_do_stt`) e «uso» (`_rispondi_senza_turno`, `modules/voice/server.py:472`) arrivino con `_parlato` ancora False. Esito: ok. Entrambi passano dopo questa riga e per «uso» a testo la risposta resta un 400 JSON.
- `modules/voice/server.py:499`: `_vuole_righe_senza_schermo` ora richiede anche `_parlato`. Rischio: cambiare i percorsi a voce. Esito: ok. audio+testo e audio+testo+pezzi passano da `_vuole_audio_testo`, che non è toccato. Con audio+pezzi a voce `_parlato` è True, quindi il comportamento è identico a V10.
- `modules/voice/server.py:463`: ramo MP3 escluso per audio+pezzi. Rischio: che il testo con Accept: audio/mpeg ricada sul MP3 dell'intero testo, senza tetto. Esito: ok. Arriva un JSON `{"content"}`. È un cambio di comportamento voluto, e audio+pezzi lo usa solo il client H24.
- `tests/test_unit_voice_server.py:1364`: test V11 nuovo e helper con `prompt_testo` (`tests/test_unit_voice_server.py:1244`). Esito: ok, il test morde. Ho provato tre mutanti in una copia nella cartella scratch:
  - tolta la condizione sul formato alla riga 463: il test V11 fallisce;
  - tolto `and self._parlato` alla riga 499: il test V11 fallisce;
  - tolta l'assegnazione alla riga 391: falliscono `test_v10_formato_audio_pezzi_senza_schermo` e `test_v10_non_ho_capito_a_righe`.

  Suite intera `tests/test_unit_voice_server.py`: 104 passed (4:49).
- `tests/test_unit_voice_server.py:1351`: docstring di `test_v10_non_ho_capito_a_righe` corretto. Esito: ok, è coerente con R-660-1-M2 (senza chiave arriva un JSON unico).
- Contesto (file non toccato): `modules/voice/server.py:883` usa `HTTPServer` a thread singolo.

Wall of Shame (gli antipattern vietati da CLAUDE.md §5): nessuno slicing della storia, nessuna simulazione dei tool, il cap delle iterazioni non è toccato.

**Riserva**
- **R-663-1-M2 (BASSA)**: il bypass del tetto orario per le richieste a TESTO resta sui percorsi che c'erano già prima.
  - Con Accept: audio/mpeg e senza X-Gas-Formato: `_do_tts_response` sintetizza l'intero testo, senza tetto.
  - Con audio+testo e audio+testo+pezzi: si sintetizza la sola parte parlata, fino a 400 caratteri.

  Il diff chiude bene il caso segnalato (audio+pezzi, fino a 1500 caratteri), ma la classe di problema non è chiusa. Va tracciata in stato_progetto.md e decisa in una fetta a parte: o un tetto anche per la sintesi a testo, o la scelta dichiarata che i client a testo sono fidati.

**Rischio escluso**: non ho verificato il comportamento del client H24 reale (Mac/ascolto.py) davanti a una risposta JSON quando chiede audio+pezzi a testo. Il client manda solo audio, quindi il caso non dovrebbe presentarsi, ma non l'ho riprodotto con il client vero. Non ho verificato nemmeno ElevenLabs e Groq reali, che nei test sono finti.

**Parere su ThreadingHTTPServer (senza codice)**: sconsigliato adesso.
1. Il GasKernel è unico, con una sola storia e un solo `.gas_history.json`. Due `run_turn` in parallelo mescolerebbero la storia, e la finestra `_get_window` partirebbe da sequenze di tool call incrociate. È proprio il tipo di crash (400 di Gemini) che CLAUDE.md §5 vuole evitare.
2. I tetti orari (`turni_parlati`, `prove_voci`) fanno «controllo e poi append» senza lock: due richieste insieme superano entrambe il tetto. Anche `voci_ammesse`, `libreria_ammesse` e `aggiunte_voci` vengono riassegnate o lette senza lock.
3. Il beneficio è basso per un solo utente: si eviterebbe solo che una richiesta lenta blocchi /voci o le pagine statiche.

Se mai servirà, va fatto in una fetta dedicata con:
- un lock unico sul kernel (turni in serie),
- un lock su ogni tetto (controllo e append insieme),
- un test di concorrenza che fallisce senza i lock.

**Memoria**: riga #663-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit 7c17275, solo quel file). Il diff staged è rimasto intatto (stessi 2 file, 32+/9−). Lezione registrata: le mutazioni vanno fatte in una copia nella cartella scratch. Un mio primo comando con rsync è fallito; la catena && si è fermata prima di sed, quindi il repo non è stato toccato (git diff vuoto).

Merge di origin/main (049d927). Review #664-M2:

## VERDETTO: APPROVATO

Il merge è corretto: rispetto a origin/main, quello che è in staging è solo la V11. Niente della fetta 39 è andato perso o è stato duplicato.

Controlli con citazioni:
- `clients/voice/ascolto.py:545` — lato client del contratto della fetta 39. Rischio esaminato: che la risoluzione dei conflitti abbia tenuto la versione vecchia del nostro branch. Esito: ok. Il blob in index (e454e1ef) è uguale a quello di origin/main; lo stesso vale per `scripts/voce/installa.sh`, `scripts/voce/LEGGIMI.md`, `tests/test_unit_voce_ascolto.py` e `reports/roadmap.md`.
- `modules/voice/server.py:391` — `_parlato = is_audio` della V11, che guida `modules/voice/server.py:499`. Rischio esaminato: che il merge abbia riportato il server di main (V10 senza la V11). Esito: ok. Il blob in index (4a7d4e5e) è uguale a HEAD; lo stesso vale per `tests/test_unit_voice_server.py` (7466dc5b), `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md`.
- `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento» unita a mano. Rischio esaminato: perdere o ritoccare la riga di main. Esito: ok. Ho verificato in modo esatto che la riga è la voce V11 seguita da « — prima: » e poi dalla riga 4 di origin/main, identica. L'altra differenza dal main è la sola riga nuova della voce V11 nella lista delle voci voce (V9 e V10 sono intatte).
- `.claude/agents/memoria_revisore.md:1215` — memoria unita a mano. Rischio esaminato: righe doppie o righe di uno dei due lati perse. Esito: ok. Rispetto a origin/main c'è solo +1 riga (#663-M2). Le righe di main (#634 e la lezione del 2026-11-03) sono presenti e non ci sono righe duplicate.
- Diff di tutto lo staged contro origin/main (`git diff --cached origin/main --stat`): 7 file, 111 righe aggiunte e 185 tolte, come atteso.
- `git diff --cached --check`: pulito, nessun marcatore di conflitto.
- Nel diff del motore non c'è nessun taglio diretto della cronologia e nessun output dei tool simulato.

Test rieseguiti da me:
- `tests/test_unit_voce_ascolto.py`: 149 passed.
- `tests/test_unit_voice_server.py -k "v10 or v11 or v7b"`: 16 passed.

Cosa NON ho verificato:
- La suite completa di `tests/test_unit_voice_server.py` insieme a quella dell'ascolto: ha superato il tempo limite della shell e l'ho interrotta. Il resto di quel file non è toccato da questo merge, perché è uguale a HEAD, che era già stato revisionato in #663-M2.
- Niente prove sul Mac o con l'audio vero: non si possono riprodurre in questo ambiente.
- Resta aperta, invariata, la riserva BASSA R-663-1-M2 della review precedente.

Memoria: ho aggiunto la riga `#664-M2 — 2026-11-03 — APPROVATO — …` in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel file di lavoro e non in staging. Non ho lanciato `commit_memoria_revisore.sh`, come mi avevi chiesto: va aggiunta all'index prima del commit di merge. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: 103 → 104 test (nuovo `test_v11_audio_pezzi_a_testo_solo_testo`); -k "v10 or v11 or v7b" 16 passed; con `modules/voice/server.py` di main il test V11 fallisce (1 failed); suite intera del file 104 passed (rieseguita dal revisore). Dopo il merge di main: voice_server + voce_ascolto -k "v10 or v11 or v7b or ascolto" 166 passed. Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette dalle notifiche.
- d8f4572 (testa che conteneva 7c17275, c91ccb8, 1bd0d32): check suite completate senza fallimenti (notifica check_suite.completed); verifica-bot success (bot APPROVATO CON RISERVE).
- 049d927 (merge di main) e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- R-663-1-M2 BASSA: richieste a testo con sintesi (`Accept: audio/mpeg` testo intero; `audio+testo`/`audio+testo+pezzi` ≤400 caratteri) fuori dal tetto orario.
- Bot #330 su ae3258e, V-2 COSMETICA: col taglio il parlato è 1500+38 caratteri (docstring e report dicono «entro 1500»).
- R-660-1-M2 BASSA e R-660-2-M2 COSMETICA (dalla V10): restano aperte.
- Bot su d8f4572, V-1 COSMETICA: il commento di `_voce_a_pezzi` dice «ritorna (status, content-type, righe)» ma ritorna (content-type, righe, mock della sintesi), ed è dopo un import (non è una vera docstring).
- Verifica esterna su d8f4572, V-2 BASSA: un client col token può dichiarare `Content-Type: audio/*` e scegliere il percorso a voce (passa dal tetto orario: nessuna azione). V-3 COSMETICA: ramo `_wants_audio()` di `_rispondi_senza_turno` per «uso» a testo senza effetto (è un 400).
