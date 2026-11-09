# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — chat Mani: voce via Telegram, fetta 2 (risposta anche a voce, solo dopo un vocale; R8)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 2 Telegram (numero e URL dalla risposta dello strumento GitHub `create_pull_request`): review APPROVATO CON RISERVE e PR nel perimetro, quindi decide l'operatore via M1.
2. Prova dal vivo di R-717-3: un vocale al bot, poi controllare che la risposta arrivi anche come nota vocale.

---

## §1 SCOPE & ESITO FETTE

- **PR #353 (fetta 1)**: `FATTA` — mergiata (7a9fad4).
- **Voce via Telegram, fetta 2**: `FATTA` — review #717/#718.
- **Riserve chiuse (V-1 bot #353, V-1 ve #353, R-712-2, V-1 bot #351, V-2 ve #351, R-717-1/2)**: `FATTA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/telegram/bot.py            |  88 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  13 ++++++-------
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  32 +++++++++++++++++---------------
 tests/test_unit_telegram_voce.py   | 179 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_voce_ascolto.py    |   9 +++++++--
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 7a9fad4 (dopo il merge della PR #353).

## §3 GIT LOG --ONELINE (sessione)

```
fa585ca feat(telegram): voce via Telegram, fetta 2 — dopo un vocale la risposta anche a voce (R8); riserve #351/#353 — review #717/#718
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. Il codice è stato scritto e revisionato nel worktree locale /tmp/claude-0/wt47, sulla stessa base 7a9fad4 (fast-forward, nessuna unione).

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #717, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #717 (chat Mani): R8, voce via Telegram, fetta 2. Ho revisionato il diff staged su mani/telegram2 nel worktree /tmp/claude-0/wt47 (base 7a9fad4). Il diff tocca 3 file: bot.py +88, test telegram_voce +161, test ascolto +9. Prima ho letto CLAUDE.md (sez. 5), stato_progetto.md (righe su R8 e fetta 1) e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:918` — `_turno_con_finale`: «parts» viene costruito come prima. «finali» raccoglie solo gli eventi "final". `errore` vale True con un evento "error" (`modules/telegram/bot.py:941`) o con un'eccezione (`modules/telegram/bot.py:945`). Il finale è vuoto se c'è stato un errore (`modules/telegram/bot.py:947`). Rischio esaminato: il testo dei messaggi normali cambia, oppure finiscono a voce dati degli strumenti. Esito: ok. `_risposta_del_turno` (`modules/telegram/bot.py:915`) restituisce `[0]`, cioè la stessa stringa di prima. Il test `tests/test_unit_telegram_voce.py:290` mette dati nel tool_res e controlla che alla sintesi arrivi solo «Fatto.». Il test `tests/test_unit_telegram_voce.py:307` copre un final seguito da un errore. Riserva R-717-1: il ramo dell'eccezione non ha un test (il mio mutante sopravvive), ma è quasi equivalente, perché dopo un final il kernel fa `return` (`gas.py:5226`).
- `modules/telegram/bot.py:967` — `_gestisci_parlato` manda prima il testo e poi la voce, solo se il finale non è vuoto e la voce è accesa (`modules/telegram/bot.py:970`). Rischio esaminato: voce dopo un messaggio di testo o dopo «Forte.» senza richiesta. Esito: ok. La voce parte solo dal ramo vocale (`modules/telegram/bot.py:866`). Il ramo «uso» esce prima della voce. Il kernel produce l'evento `strumento_negato` con content vuoto, quindi niente voce. `_SPENTO` (`modules/telegram/bot.py:66`) e `_voce_accesa` (`modules/telegram/bot.py:973`) usano strip e lower; il mio mutante «solo "0"» viene preso.
- `modules/telegram/bot.py:1001` — `_invia_risposta_vocale`: senza chiave manda un avviso e non chiama ElevenLabs. Import, scelta della voce, `parte_parlata` e `synthesize_speech` stanno tutti in un `except Exception`. Rischio esaminato (§9): http.client.HTTPException non è sottoclasse di OSError (lezione del 2026-11-05). Esito: ok, il try generico la intercetta. Con la sintesi fallita nessun sendVoice parte e arriva un avviso breve. Il mio mutante senza `parte_parlata` viene preso. Riserva R-717-2: il caso «HTTP 200 con ok:false» (`modules/telegram/bot.py:1018`) non ha un test, il mutante `esito is None` sopravvive. In pratica Telegram risponde ok:false con un 4xx, che urllib trasforma in HTTPError, poi None, poi l'avviso.
- `modules/telegram/bot.py:977` — `_tg_post_file`: multipart in stdlib con confine casuale. I campi sono solo chat_id e il nome file è fisso, quindi niente iniezione di intestazioni. Rischio esaminato: token nel log, eccezioni che sfuggono. Esito: ok. Il log riporta solo `type(e).__name__` e `json.load` sta dentro il try. Il corpo è verificato dal test `tests/test_unit_telegram_voce.py:349`.
- `modules/telegram/bot.py:158` — l'import di stt è in un try (V-1 bot #353): l'errore arriva all'operatore e non si chiama il kernel. Esito: ok, test `tests/test_unit_telegram_voce.py:387`. La lettura di al massimo MAX+1 byte (V-1 ve #353) è verificata da `tests/test_unit_telegram_voce.py:381`. R-712-2 è chiusa (`modules/telegram/bot.py:147`, una sola chiamata).
- `tests/test_unit_voce_ascolto.py:2441` — il test ora conta esattamente 2 righe di log (V-1 bot #351); `tests/test_unit_voce_ascolto.py:2467` aggiunge inf/nan senza avviso e -5 con avviso. Esito: ok, 295 passed.

**Risposte alle domande**
- Privacy e regola dei modelli: a ElevenLabs va solo la parte parlata della risposta finale (al massimo 3 frasi e 400 caratteri, poi il taglio di GAS_TTS_MAX_CHARS a 2000). Gli output degli strumenti no. È lo stesso flusso dei dati della voce di casa. ElevenLabs è un servizio di sintesi, non un modello che ragiona sui dati, ma resta un terzo esterno: va detto all'operatore. La scelta del cervello (forte o gratuito) non cambia, segue cervello_voce come nella fetta 1.
- Costi: al massimo un vocale in uscita per ogni vocale in entrata. Il tetto è 30 vocali all'ora in ingresso, quindi al massimo 30 sintesi all'ora, ciascuna di 400 caratteri o meno. Senza chiave, con la voce spenta o con un errore nel turno: nessuna chiamata a ElevenLabs (verificato dai test).
- sendVoice con MP3: NON VERIFICATO (R-717-3, BASSA). Non posso provarlo qui. A memoria, la documentazione della Bot API dice che sendVoice accetta OGG/OPUS, MP3 e M4A. Prima di chiuderla serve una prova reale dell'operatore. Se Telegram lo rifiuta, l'operatore riceve l'avviso «non inviata» e il testo è già arrivato.
- §9: ok. Ogni ramo nuovo (chiave mancante, sintesi, import, rete, risposta non JSON) finisce in un avviso breve e una riga di warning nel log, mai un crash.
- Testi: identici. Per i messaggi di testo la stringa è la stessa, e i test della fetta 1 restano verdi.
- Firme: il diff non tocca bottoni né approvazioni. Il ramo vocale esegue solo run_turn, come la fetta 1. Ok.
- Round-trip §7: non serve. Il kernel non è toccato e il ciclo tool_res → final è coperto con un kernel finto (`tests/test_unit_telegram_voce.py:290`).
- Wall of Shame: nessuno slicing della history nel diff (grep `[-N:]` vuoto) e nessuna simulazione dei tool (le finte stanno solo nei test).

**Riserve**
- R-717-1 BASSA: manca un test per `errore = True` nel ramo dell'eccezione (`modules/telegram/bot.py:945`).
- R-717-2 BASSA: manca un test per sendVoice con HTTP 200 e ok:false (`modules/telegram/bot.py:1018`).
- R-717-3 BASSA: sendVoice con MP3 NON VERIFICATO dal vivo.
- R-717-4 BASSA: sintesi (timeout 30 s) più invio (30 s) bloccano il polling a thread singolo fino a circa 60 s per vocale, nel caso peggiore. È da dichiarare.

**Cosa NON ho verificato**
- Il comportamento reale di Telegram e di ElevenLabs (rete e chiavi non disponibili qui), compresa la riproduzione dell'MP3 come nota vocale nei client Telegram.
- La suite completa del kernel e test_unit_voice_server: quest'ultimo era ancora in esecuzione in background quando ho chiuso. Il diff però non tocca né gas.py né modules/voice.

**Verifiche fatte**
- Copia dell'index estratta con checkout-index in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx717, niente stash.
- Risultati: 49 passed (telegram_voce), 295 passed (ascolto), 245 passed (notte + telegram_voce). `git diff --cached --check` pulito; worktree uguale all'index su bot.py.
- Miei mutanti: 2 presi su 4, i 2 sopravvissuti corrispondono a R-717-1 e R-717-2.

**Memoria**
- Ho aggiunto la riga #717 e una lezione in coda a /tmp/claude-0/wt47/.claude/agents/memoria_revisore.md. Il file è modificato e non è né in staging né committato, come richiesto.
- Ho tentato `commit_memoria_revisore.sh` per abitudine: il permesso è stato negato, quindi non è stato committato nulla. Il comando bloccato conteneva anche l'aggiunta della riga, che non era avvenuta: l'ho rifatta da sola.
- Il diff staged è invariato.

Review #718 (ri-review), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #718 (chat Mani): ri-review della #717 sullo staged di /tmp/claude-0/wt47, branch mani/telegram2, base 7a9fad4. R-717-1 e R-717-2 sono chiuse; restano aperte R-717-3 e R-717-4, da dichiarare all'operatore.

**Cosa è cambiato nello staged**
Solo i due test in coda a `tests/test_unit_telegram_voce.py`. L'ho controllato confrontando lo staged con la copia dell'index fatta per la #717:
- `modules/telegram/bot.py` è identico.
- `tests/test_unit_voce_ascolto.py` è identico.
- `tests/test_unit_telegram_voce.py` ha solo le righe 401-418 aggiunte in coda.

**Elementi del diff esaminati**
- `tests/test_unit_telegram_voce.py:403` — `test_eccezione_nel_turno_niente_voce`: il kernel finto emette un final («mezza») e poi lancia RuntimeError. Il test controlla che il testo contenga «✗ Errore interno» e che non partano né la sintesi né sendVoice. Rischio esaminato: il ramo except di `modules/telegram/bot.py:945` senza copertura (R-717-1). Esito: ok. Il mutante che toglie `errore = True` ora viene preso (1 failed). R-717-1 CHIUSA.
- `tests/test_unit_telegram_voce.py:414` — `test_invio_del_vocale_con_ok_false_avviso_breve`: l'invio restituisce `{"ok": False}` e il test vuole l'avviso «Risposta vocale non inviata». Rischio esaminato: la condizione di `modules/telegram/bot.py:1018` senza copertura (R-717-2). Esito: ok. Il mutante `esito is None` ora viene preso (1 failed). R-717-2 CHIUSA.
- `modules/telegram/bot.py:918` (contesto, non cambiato dalla #717): la logica coperta dai due test è quella già approvata nella #717. Esito: ok.

**Prove eseguite**
- Copia dell'index estratta con checkout-index in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx718: 51 passed.
- `git diff --cached --check` pulito; niente stash.

**Riserve ancora aperte (da dichiarare all'operatore)**
- R-717-3 BASSA: non ho potuto provare che Telegram accetti l'MP3 su sendVoice (NON VERIFICATO dal vivo). Serve una prova reale dell'operatore. Se Telegram lo rifiuta, l'operatore riceve un avviso breve e il testo è già arrivato.
- R-717-4 BASSA: la sintesi (fino a 30 s) più l'invio (fino a 30 s) bloccano il polling del bot, che gira in un solo thread, fino a circa 60 s per vocale nel caso peggiore.

**Cosa NON ho verificato**
- Le chiamate reali a Telegram ed ElevenLabs (né rete né chiavi disponibili qui).
- La suite del kernel: gas.py non è toccato.

**Memoria**
Ho aggiunto in coda a /tmp/claude-0/wt47/.claude/agents/memoria_revisore.md la riga #718, senza lezioni nuove; c'è anche la riga #717 di prima. Il file non è committato e non è in staging. Non ho lanciato commit_memoria_revisore.sh e lo staged non l'ho toccato.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: da 31 a 51 casi. `tests/test_unit_voce_ascolto.py`: 295 casi (assert più precisi e 3 casi in più). Riepiloghi reali:

```
51 passed in 0.08s
295 passed in 27.39s
```

Mutanti presi:
- voce anche dopo un testo;
- finale non svuotato dopo un errore;
- read() senza tetto;
- output degli strumenti detti a voce;
- niente parte_parlata;
- invio rifiutato senza avviso;
- `errore = True` tolto;
- `esito is None`;
- log a ogni errore;
- niente isfinite.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Per il commit fa585ca e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff. La PR #353 su f824f9c aveva unit-suite e handoff-check verdi ed è stata mergiata.

## §7 RISERVE APERTE

- R-717-3 BASSA: sendVoice con MP3 non verificato dal vivo (prova dell'operatore).
- R-717-4 BASSA: sintesi più invio bloccano il polling fino a circa 60 s per vocale, nel caso peggiore.
- ElevenLabs riceve la parte parlata della risposta finale, come nella voce di casa: un terzo esterno, da sapere.
- V-2 della verifica esterna #353: la regola dei modelli per i vocali va confermata dall'operatore con un commento sulla #353.
- R-712-1 e R-712-3 BASSE e le altre riserve: in `reports/stato_progetto.md`.
