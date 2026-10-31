# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-31 — Voce V5: il tetto orario conta ogni chiamata a Groq, guida di prova sul Mac (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #314 (https://github.com/Gasss23/Gas/pull/314). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5099188668","url":"https://github.com/Gasss23/Gas/pull/314"}`); `gh` nel cloud non è autenticato. L'operatore ha detto «mergia #314» (via M1), ma la PR era in conflitto con main dopo la #312: unito main con un merge (832092d, review #587-M2); il merge automatico lo attiva M1.
2. Prova sul Mac seguendo `reports/prova_voce_mac.md`: PRIMA l'eco (se Gas si zittisce da solo, `GAS_VOICE_INTERRUZIONE=0`), poi «sì» a voce normale, poi TV accesa.

---

## §1 SCOPE & ESITO FETTE

- **V5.1 — R-581-2-M2** («uso» e trascrizioni vuote spendevano Groq senza contare): `FATTA` — registrazione dentro `_do_stt` subito prima di `transcribe_audio`.
- **R-585-1-M2** (i rifiuti locali consumavano il tetto e nascondevano il 503/400 utile): `FATTA` (review #586-M2).
- **V5.2 — guida di prova sul Mac** (`reports/prova_voce_mac.md`): `FATTA`.
- **Merge di main (01eba0d, PR #312) + V-2 COSMETICA bot/verifica esterna #314** («turni» → «richieste a voce» nel 429, nei commenti, nella docstring e nella guida): `FATTA` (832092d, review #587-M2 APPROVATO).
- **gas.py / brains/ / ci.yml**: non toccati.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 modules/voice/server.py            |  22 +-
 reports/diff_sessione.md           |  15 +-
 reports/handoff.md                 | n/d
 reports/prova_voce_mac.md          |  58 ++++++
 reports/stato_progetto.md          |   3 +-
 reports/ultimo_report.md           |  27 +--
 tests/test_unit_voice_stt.py       |  34 ++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
832092d Merge origin/main (01eba0d, PR #312) in feat/voce-v5-m2 (PR #314) + V-2: «richieste a voce»
2c50122 docs(voce-v5): report di fine task e guida di prova sul Mac (PR #314, review #585/#586-M2)
8487fd7 fix(voce): il tetto orario conta ogni chiamata a Groq, anche «uso» e trascrizioni vuote (V5, chat M2)
ae46fc3 chore(revisore): memoria review #586 — APPROVATO
e0dc6c7 chore(revisore): memoria review #585 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit 8487fd7 è stato rivisto in due passaggi sullo stesso diff staged. Verdetti integrali:

Review #585-M2 (primo passaggio; dopo, la registrazione è stata spostata dentro `_do_stt` per R-585-1-M2, quindi alcune righe citate sono cambiate):

## VERDETTO: APPROVATO CON RISERVE

Review #585-M2: fetta V5 che chiude R-581-2-M2 (branch feat/voce-v5-m2, diff staged: 2 file, +27/-3). Prima della review ho letto CLAUDE.md (§5), il punto R-581-2 di reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

**Cosa ho esaminato nel diff**
- `modules/voice/server.py:275` — Registra l'istante nel tetto orario subito dopo il controllo e prima di `_do_stt`. Rischio esaminato: una richiesta che spende Groq senza essere contata, oppure contata due volte. Esito: **ok**. L'unico chiamante di `transcribe_audio` è `_do_stt` (modules/voice/server.py:396), e `_do_stt` viene chiamato solo da modules/voice/server.py:276, che sta dopo la registrazione. Quindi ogni chiamata a Groq conta esattamente una volta. I casi «forte» senza richiesta, trascrizione vuota, Groq 400/502 ed errore di rete contano tutti. La vecchia registrazione prima di `run_turn` è stata tolta e non c'è doppio conteggio. Non c'è corsa sul contatore: il server è un `HTTPServer` a thread singolo (modules/voice/server.py:484). La scrittura `type(self).turni_parlati` agisce sulla sottoclasse `_H` del test, quindi i test restano isolati.
- `modules/voice/server.py:268` — La risposta 429 resta prima della registrazione, della trascrizione e del turno. Rischio esaminato: un 429 che avvia comunque un turno o spende Groq. Esito: **ok**. Il `return` a modules/voice/server.py:271 esce prima di tutto, e il 429 non consuma posti nel tetto.
- `modules/voice/server.py:33` — Docstring aggiornata («richieste PARLATE … ogni richiesta audio che arriva alla trascrizione»). Esito: **ok**, con la precisazione della riserva sotto. Il commento a modules/voice/server.py:205 dice ancora «turni parlati»: è solo cosmetico.
- `tests/test_unit_voice_stt.py:408` — Nuovo test con tetto 2: «Forte.» → 200, trascrizione vuota → 400, terza richiesta → 429; Groq chiamato 2 volte, nessun turno del kernel. Rischio esaminato: che il test non fallisca davvero se il codice torna indietro. Esito: **ok**. Ho rimesso la versione di HEAD di server.py: il test fallisce (1 failed). Ripristinata la versione staged: passa (il working tree corrisponde di nuovo all'index). La suite `tests/test_unit_voice_stt.py` dà 36 passed.
- `tests/test_unit_voice_stt.py:425` — L'asserzione `[200, 400, 429]` copre la richiesta «uso» e quella vuota, non i rami Groq 502 ed errore di rete. Esito: **ok**. Quei rami passano dalla stessa riga 275, quindi la copertura è equivalente.

**Riserve**
- **R-585-1-M2 BASSA**: contano anche le richieste rifiutate prima di Groq dentro `_do_stt`: 503 senza chiave (modules/voice/server.py:401), 400 corpo vuoto (modules/voice/server.py:405), 400 audio non valido (modules/voice/server.py:411). È accettabile: il conteggio va in eccesso, cioè nella direzione prudente per il budget, e l'autenticazione a modules/voice/server.py:248 viene prima, quindi un estraneo non può riempire il tetto. Effetto collaterale: con il server mal configurato (chiave Groq mancante), dopo 60 tentativi all'ora l'operatore vede il 429 invece del 503, che è l'errore utile per capire il problema. Correzione possibile in una fetta futura: registrare subito prima di `transcribe_audio`, ad esempio dentro `_do_stt` dopo i controlli locali, e allineare la docstring. Va tracciata in stato_progetto.md.
- La guida reports/prova_voce_mac.md (non staged) parla di «60 richieste all'ora» e riporta il messaggio «Troppi turni a voce nell'ultima ora»: entrambi coerenti con il codice. Ho controllato solo questi due punti.

**Rischi esclusi**
- Comportamento reale con Groq e con il browser sul Mac: non riproducibile qui, l'STT è finto (mock) nei test.
- Non ho rieseguito la suite voce completa né i test del browser (Playwright): il diff tocca solo il ramo server di `do_POST`. Mi fido delle 97 passed dichiarate per la parte non browser.
- Non ci sono antipattern del Wall of Shame: nessuno slicing della history, nessun output di tool simulato. Il diff non tocca il motore agentico né i guardrail (10 iterazioni, 8k, `_get_window`).

Memoria aggiornata: riga #585-M2 più una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (e0dc6c7). Il resto dell'index è intatto.

Review #586-M2 (diff finale committato in 8487fd7):

## VERDETTO: APPROVATO

Ri-review #586-M2 sul diff staged di feat/voce-v5-m2 (2 file: modules/voice/server.py, tests/test_unit_voice_stt.py). Letture obbligatorie fatte: CLAUDE.md (sezioni 5, 8, 9), memoria del revisore (ultime voci #585-M2 e lezione sul contatore di budget) e stato_progetto (le parti sulla voce).

**Integrità di server.py dopo lo stash accidentale.** `git diff --cached` contro HEAD e contro origin/main (3a38e75, a cui HEAD aggiunge solo commit di memoria) danno lo stesso risultato: 12 righe, 8 aggiunte e 4 tolte. Contengono esattamente:
- il docstring;
- il commento dell'attributo di classe;
- la rimozione della registrazione prima di run_turn;
- la registrazione dentro `_do_stt`.

Non c'è nient'altro: lo stash e il ripristino non hanno lasciato residui.

Elementi esaminati:
- modules/voice/server.py:414 — registra la richiesta nel tetto orario subito prima di `transcribe_audio` (:416), dopo i rifiuti locali: chiave assente 503 (:396), audio vuoto 400 (:400), audio non valido 400 (:406). Rischio esaminato: conteggio di richieste che non spendono Groq, o richieste che spendono senza essere contate. Il grep conferma che `transcribe_audio(` ha un solo chiamante (`_do_stt`) e `_do_stt` uno solo (:272). Ogni chiamata a Groq conta una volta, comprese quelle fallite (502) e le trascrizioni vuote. Esito: ok.
- modules/voice/server.py:267 — controllo del 429 (:267-271) con `return` prima di `_do_stt` (:272) e prima di ogni `run_turn`. Rischio esaminato: un turno o una chiamata STT avviati oltre il tetto. La registrazione rimossa (prima :302-303) stava dopo questo punto, quindi toglierla non cambia l'ordine. Esito: ok, il 429 precede ancora STT e turno.
- modules/voice/server.py:33 e modules/voice/server.py:205 — docstring («conta ogni chiamata alla trascrizione (Groq)») e commento dell'attributo. Ora corrispondono al comportamento reale. Esito: ok.
- tests/test_unit_voice_stt.py:429 — test `test_v5_rifiuti_locali_non_consumano_il_tetto`: con tetto 1, un audio vuoto dà 400, poi una richiesta valida dà 200, e STT viene chiamato una volta sola. Rischio esaminato: un test che non morde. Prova a mutante: ho ricostruito la variante #585 (registrazione prima di `_do_stt`) in una copia temporanea dell'index → 1 failed (proprio questo test); sul diff staged → 37 passed nel file stt. Isolamento: `_make_server` (tests/test_unit_voice_stt.py:50) crea una sottoclasse per ogni test, quindi `type(self).turni_parlati` non passa da un test all'altro. Esito: ok.
- tests/test_unit_voice_stt.py:408 — il test #585 (uso «forte» senza richiesta, trascrizione vuota, poi 429; nessun turno avviato) passa ancora. Esito: ok.

Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. gas.py, brains/ e i guardrail (cap 10 iterazioni, `_get_window`) non sono toccati. La funzione chiamata `_turni_recenti` filtra per tempo la lista del tetto, non la cronologia messaggi.

Rischi esplicitamente esclusi:
- Comportamento sul Mac e sul VPS reali, con Groq vero, non verificato: in dev la trascrizione è simulata nei test.
- Suite voce completa con i test del browser non rieseguita da me: ho girato solo tests/test_unit_voice_stt.py (37 passed). Il dato «98 passed» per la suite non-browser è un'affermazione dell'agente, non riverificata.
- Concorrenza sul contatore non riesaminata: HTTPServer è single-thread, come già valutato in #585.

R-585-1-M2: chiusa.

Memoria: aggiunta la riga #586-M2 a /home/user/Gas/.claude/agents/memoria_revisore.md (nessuna lezione nuova) e committata con commit_memoria_revisore.sh (ae46fc3). L'index del diff sotto review è rimasto intatto. Ora va eseguito `bash scripts/segna_review_ok.sh` prima del commit.

Review #587-M2 (merge di main 01eba0d + V-2 «richieste a voce», commit 832092d):

## VERDETTO: APPROVATO

Review #587-M2. Ho controllato il merge di origin/main 01eba0d (PR #312) dentro feat/voce-v5-m2 (HEAD 2c50122), con il diff staged e la correzione V-2 COSMETICA.

Elementi del diff esaminati:
- `modules/voice/server.py:152` — il commento della costante ora dice «richieste a voce (chiamate a Groq, V5)». Ho controllato che corrisponda a quello che il codice conta davvero: la registrazione nel tetto sta dentro `_do_stt` subito prima di `transcribe_audio` (`modules/voice/server.py:414`). Il commento ora è vero. Esito: ok.
- `modules/voice/server.py:269` — il messaggio 429 diventa «Troppe richieste a voce nell'ultima ora (…)». Ho cercato se qualche test o client legge il vecchio testo: `grep` su tests/, modules/ e clients/ non trova «Troppi turni» da nessuna parte. Il ramo 429 (`modules/voice/server.py:264-271`) non cambia nella logica e resta prima dello STT. Esito: ok.
- `modules/voice/server.py:335` — docstring di `_turni_recenti`. Cambia solo il testo, il filtro a 3600 s è lo stesso. Esito: ok. Nota cosmetica: questa riga e la `:154` superano i 100 caratteri, ma il file ne ha già altre 8 sopra quella soglia e non c'è un linter che la imponga.
- `reports/prova_voce_mac.md:54` — riga della guida allineata al nuovo messaggio. Esito: ok.
- `.claude/agents/memoria_revisore.md` (conflitto) — 0 righe tolte sia rispetto a HEAD sia rispetto a MERGE_HEAD. Rispetto a main aggiunge 3 righe (#585-M2, la lezione, #586-M2), messe dopo la #592 di main. Esito: ok.
- `reports/stato_progetto.md:4` — l'auto-merge toglie 1 riga rispetto a HEAD: è l'intestazione, sostituita da quella più recente di main. Il resto rispetto a main sono solo le righe V4/V5 del branch. Esito: ok.

Controlli strutturali:
- Rispetto a MERGE_HEAD differiscono solo i file V5: server.py, test stt, prova_voce_mac, i tre log di sessione, stato e memoria. `modules/web`, i test web e `reports/ripartenza_mani.md` sono identici a main (diff di 0 righe).
- Rispetto a HEAD cambiano solo i file di main più le 4 modifiche di testo. In gas.py, brains, clients, modules/voice e nei test voce ci sono solo 10 righe ± di testo, tutte in server.py.
- Nessun marcatore di conflitto, `git diff --cached --check HEAD` è pulito.
- Nessuno slicing della history e nessuna simulazione di tool: il kernel e il percorso `_get_window` non sono toccati.

Test, su un export dell'indice in /tmp/rv587:
- voce: `test_unit_voice_stt.py` + `test_unit_voice_server.py` → 114 passed
- web: leggi + lexbor + proxy → 579 passed, 114 skipped

Rischio escluso: non ho rieseguito la suite del kernel (gas.py), i test della pagina nel browser con Playwright obbligatorio e gli hook. Il merge non tocca né gas.py né clients/, e le modifiche a modules/voice sono solo testo. Non ho verificato perché i test web risultano skipped: nel #592 erano 557 passed e 1 skipped, quindi probabilmente in questo ambiente manca una dipendenza opzionale (lexbor o un browser). Non dipende da questo diff, perché i file web sono identici a main.

Memoria: ho aggiunto la riga contatore #587-M2 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, senza metterla in stage. Non ho lanciato `commit_memoria_revisore.sh`, perché con il merge in corso `git commit -o` non può fare un commit parziale. Va messa in stage e committata insieme al commit di merge (o subito dopo). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite parte non-browser (server + stt): 96 → 98 passed (+2: tetto con «uso» e vuota; rifiuto locale che non consuma il tetto). Mutanti: il primo test fallisce sul server.py di main, il secondo sulla variante #585. I test della pagina nel browser non sono toccati da questa fetta (girano obbligatori in CI). Nessun FAIL. Dopo il merge di main (832092d): voce stt+server 114 passed (mia run e review #587-M2).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- e0dc6c7, ae46fc3, 8487fd7: pushati insieme prima dell'apertura della PR #314; nessuna run della PR su questi SHA.
- 2c50122 (head prima del merge di main): unit-suite, handoff-check, verifica-bot success (bot APPROVATO CON RISERVE; verifica esterna APPROVATO CON RISERVE, https://github.com/Gasss23/Gas/pull/314#issuecomment-6545842665).
- 832092d (merge di main): pushato insieme al commit di fine-task; run non ancora disponibile alla scrittura.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-584-1-M2** BASSA (da #313) — rumore costante ≥ 0,045 RMS preso per voce: da provare con la TV (test 3 della guida).
- **R-583-1-M2** COSMETICA (da #313).
- **R-576-1-M2** BASSA e **R-576-3-M2** COSMETICA (da #311).
- Prova sul Mac (eco, «sì» a voce normale, TV): da fare con `reports/prova_voce_mac.md`.
