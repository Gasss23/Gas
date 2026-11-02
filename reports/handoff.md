# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Voce V8: pagina «prova voci» e libreria condivisa (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. PR della V8: da aprire (numero dopo la creazione).
2. Sul Mac, dopo il merge: scegliere la voce dalla pagina «prova voci»; verificare percorsi e costi della libreria condivisa.

---

## §1 SCOPE & ESITO FETTE

- **V8 — pagina «prova voci»**: `FATTA` (review #624–#626-M2).
- **V8b — libreria condivisa di ElevenLabs**: `FATTA` (review #627–#629-M2).
- **Merge di main (V6, V7a, V7b, #319–#323)**: `FATTA` (review #655-M2).
- **V9**: `DEFERITA` — PR dopo il merge di questa.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  11 +++++++
 .github/workflows/ci.yml            |   2 +-
 clients/voice/browser_server.py     |  71 ++++++++++++++++++++++++++++++++++++++--
 clients/voice/prova_voci.html       | 291 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/voice/prova_voci.py         | 126 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/voice/server.py             | 193 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 modules/voice/tts.py                | 152 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md            |  16 +++++----
 reports/handoff.md                  | n/d
 reports/prova_voce_mac.md           |   6 ++++
 reports/stato_progetto.md           |   3 +-
 reports/ultimo_report.md            |  20 ++++++------
 tests/test_unit_voice_prova_voci.py | 637 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
8e88e78 Merge remote-tracking branch 'origin/main' into feat/voce-v8-m2
87007ff docs(voce-v8): guida Mac per la libreria delle voci
bb1fd62 feat(voce): V8b — «prova voci» cerca anche nella libreria condivisa di ElevenLabs (chat M2)
d5edc3d chore(revisore): memoria review #629 — APPROVATO
5f52963 chore(revisore): memoria review #628 — APPROVATO CON RISERVE
4fdf4dd chore(revisore): memoria review #627 — APPROVATO CON RISERVE
f6ef710 docs(voce-v8): guida Mac per la pagina «prova voci», memoria review #626
2116699 feat(voce): V8 — pagina «prova voci»: scegliere la voce di Gas all'ascolto (chat M2)
83d1c3b chore(revisore): memoria review #625 — APPROVATO CON RISERVE
ba7432c chore(revisore): memoria review #624 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della V8 (2116699): tre passaggi del revisore.

Review #624-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #624-M2. Branch feat/voce-v8-m2, solo il diff staged (7 file). Prima ho letto CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (letto in parte) e la mia memoria.

**Cosa ho controllato nel diff:**
- `modules/voice/prova_voci.py:30`: `voce_valida` accetta solo id di 8-40 caratteri tra lettere e cifre, con `^…$`. Rischio: un id costruito per cambiare il percorso dell'API ElevenLabs (path injection). Esito: ok. `../../v1/user` viene rifiutato sia nel server sia in `ordina_voci`, e un test lo prova.
- `modules/voice/prova_voci.py:84`: Piper viene lanciato come lista di argomenti, senza shell. Il testo passa su stdin, il file temporaneo sta in una TemporaryDirectory, c'è timeout 60 e check=True. Rischio: comandi iniettati o processi appesi. Esito: ok. Il testo è sempre una delle frasi fisse e il modello viene da env (fidato). TimeoutExpired e un file di uscita mancante vengono intercettati in `modules/voice/server.py:678` (OSError e SubprocessError).
- `modules/voice/server.py:309`: su POST /voci/prova l'autenticazione viene controllata prima di leggere il corpo, e Content-Length deve stare tra 0 e 4096. Un valore non numerico vale -1 e porta a 400. Esito: ok. Il server è HTTP/1.0, quindi un corpo non letto dopo un 401 non contamina la richiesta successiva.
- `modules/voice/server.py:684`: la prova viene contata nel tetto prima della sintesi, solo per ElevenLabs e solo se la chiave c'è. Esito: ok, ed è prudente (anche le prove fallite contano). Il test riproduce [200, 200, 429] e il fixture azzera `prove_voci`. Il controllo di `frase` (int, non bool, nell'intervallo) è corretto.
- `modules/voice/server.py:612`: il nuovo `do_GET` risponde 405 su tutti i percorsi tranne /voci/elenco, che richiede autenticazione. Il vecchio comportamento è conservato, e il test verifica 405 su `/altro`. I GET su /voice restano 405.
- `clients/voice/browser_server.py:114`: il proxy taglia il corpo a 4096 byte e lo inoltra col token. Un corpo più lungo arriva troncato e il server risponde 400. Gli errori di rete diventano 502 in `clients/voice/browser_server.py:237`. Esito: ok.
- `clients/voice/prova_voci.html`: tutti i dati arrivano nella pagina con textContent, nessun innerHTML. URL.revokeObjectURL viene chiamato prima di ogni nuovo audio. Esito: ok, e c'è il test con `<b>` nel nome.
- `.github/workflows/ci.yml:126`: il nuovo file di test è aggiunto alla voice suite. Esito: ok. Non tocca paths-ignore né i check obbligatori.

Test: `tests/test_unit_voice_prova_voci.py` dà 27 passed. Ho riprodotto a mano il caso della riserva 2.

**Riserve (da tracciare in stato_progetto.md):**
- **R-624-1-M2 (MEDIA-BASSA), regola «niente cloni».** `modules/voice/prova_voci.py:62` esclude solo la categoria `cloned`, cioè un elenco di categorie vietate. L'API di ElevenLabs ha anche la categoria `famous`, che oggi passerebbe in silenzio. Proposta:
  - usare un elenco di categorie ammesse (es. premade, generated, professional) invece di un elenco di vietate;
  - dichiarare che il filtro vale solo nell'elenco mostrato: il POST di `modules/voice/server.py:638` accetta qualunque id valido, compresa una voce clonata indicata a mano.
- **R-624-2-M2 (BASSA).** In `modules/voice/tts.py:159`, se ElevenLabs risponde con `{"voices": 5}` il ciclo a `modules/voice/tts.py:165` solleva TypeError. Riprodotto. `do_GET` non lo intercetta: il server resta vivo grazie a socketserver, ma la pagina non riceve nessun JSON con «errore». Correzione: `if not isinstance(voci, list): raise ElevenLabsTTSError(...)`.
- **R-624-3-M2 (COSMETICA).** A `modules/voice/server.py:244`, `turni_parlati` ha perso il suo commento. A `modules/voice/server.py:245` `prove_voci` ha due commenti, e il secondo («V4/V5 … Groq») è quello vecchio finito lì per sbaglio.
- **R-624-4-M2 (BASSA, preesistente).** Il proxy del browser non controlla Origin né Host. Una qualunque pagina aperta nel browser dell'operatore può mandare un POST a 127.0.0.1:9000/voci/prova e spendere caratteri ElevenLabs. La spesa è limitata dal tetto di 40 prove all'ora. Lo stesso problema esiste già, ed è più grave, su /voice.
- **Nota (BASSA, nessuna azione obbligatoria).** Le prove con Piper non contano nel tetto (corretto: è gratis). Però il server voce gestisce una richiesta alla volta e una prova Piper può tenerlo occupato fino a 60 secondi.

**Cosa non ho verificato:**
- Comportamento reale di Piper e della vera API /v1/voices di ElevenLabs (nomi effettivi delle categorie ed etichette): qui non ci sono rete né il comando piper, e nei test sono finti.
- Esito della suite voce completa con browser (i 213 passed dichiarati): l'ho lanciata, ma non era finita entro il tempo della review, quindi non lo confermo.
- La qualità delle candidate «stile maggiordomo» all'ascolto: è un giudizio umano.

**Contatore e memoria:**
- Ho aggiunto la riga #624-M2 e una lezione nuova (i filtri etici sulle categorie di un'API esterna vanno fatti con un elenco di ammesse; dichiarare se valgono anche lato server).
- La memoria è committata da sola in ba7432c; il diff staged (7 file) è rimasto com'era.
- Non ho committato nient'altro.

File: /home/user/Gas/.claude/agents/memoria_revisore.md

Review #625-M2:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #625-M2 del branch feat/voce-v8-m2: diff staged, 7 file, nessun commit fatto da me sul codice. Prima della review ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

**Cosa ho esaminato nel diff**
- `modules/voice/prova_voci.py:34` — `CATEGORIE_AMMESSE` è ora un elenco di categorie ammesse (premade, generated, professional). Rischio esaminato: che una voce famous, clonata o di una categoria nuova arrivi nell'elenco. Il filtro in `ordina_voci` scarta tutto ciò che non è nell'elenco e il test copre famous, categoria nuova e professional. Esito: ok, R-624-1-M2 (prima parte) chiusa.
- `modules/voice/server.py:659` — POST /voci/prova accetta solo id presenti in `voci_ammesse`, oppure «piper»; altrimenti risponde 409 prima di toccare il tetto orario e prima di qualunque chiamata a ElevenLabs. Rischio esaminato: che un id valido scritto a mano (per esempio un clone) venga sintetizzato. Il test `test_prova_voce_non_elencata_rifiutata` verifica 409 e zero chiamate al TTS. Esito: ok, R-624-1-M2 chiusa.
- `modules/voice/server.py:633` — `voci_ammesse` viene riempito solo quando l'elenco riesce. Rischio esaminato: un elenco vecchio che resta valido. Se l'elenco fallisce, o se la chiave ElevenLabs manca, resta in vigore quello precedente. Era comunque già filtrato, quindi non lascia passare cloni. Esito: riserva BASSA (R-625-2-M2).
- `modules/voice/tts.py:162` — se `voices` non è una lista, ora viene sollevato `ElevenLabsTTSError`. Un JSON che è una lista al primo livello finisce in AttributeError, che viene intercettato e diventa lo stesso errore. Rischio esaminato: un TypeError che non viene intercettato in do_GET. Testato con `{"voices": 5}` e `[1, 2]`. Esito: ok, R-624-2-M2 chiusa.
- `modules/voice/server.py:244` — i commenti di `turni_parlati` (V4/V5) e `prove_voci` (V8) sono ora corretti e separati. Esito: ok, R-624-3-M2 chiusa.
- `clients/voice/browser_server.py:108` — `_stessa_origine()` gira in testa a tutte le POST (riga 119), quindi anche su /voice. Rischio esaminato: un sito esterno che fa parlare Gas o spende prove di voce. Con Origin diverso risponde 403 e il server voce non riceve niente (lo verifica il test, `viste == []`). Origin «null» viene rifiutato perché il suo netloc è vuoto. Esito: ok per il caso cross-site, R-624-4-M2 chiusa. Resta però un limite, vedi R-625-1-M2.
- `clients/voice/browser_server.py:352` (contesto, file nel diff) — il proxy ascolta solo su 127.0.0.1. È il presupposto della riserva qui sotto.

**Riserve (BASSE, da tracciare in stato_progetto.md)**
- R-625-1-M2: il confronto Origin==Host non regge un DNS rebinding. Esempio: una pagina su evil.example:9000 viene fatta risolvere a 127.0.0.1; Origin e Host valgono entrambi «evil.example:9000», quindi la richiesta passa. Lo stesso vale per GET /config. Correzione: aggiungere una lista di Host ammessi (127.0.0.1:porta, localhost:porta). Il problema esisteva già prima di questa fetta, che anzi lo riduce.
- R-625-2-M2: `voci_ammesse` non si azzera quando l'elenco fallisce (vedi sopra). Impatto trascurabile.

**Cose verificate eseguendo**
- `tests/test_unit_voice_prova_voci.py`: 33 passed.
- Suite voce completa, quella di CI, con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: 219 passed in 262 s. Il numero coincide con quello dichiarato.
- `.github/workflows/ci.yml:126`: il nuovo file di test è aggiunto al passo della suite voce, senza `paths-ignore`. Ok.

**Rischio escluso**
- Non ho verificato il comportamento reale di Piper né la risposta vera di ElevenLabs su /v1/voices (categorie effettive dell'account): servirebbero un binario, un modello e una rete veri, non disponibili in dev; i test usano sostituti finti.
- Non ho riprodotto un vero DNS rebinding con il browser: R-625-1-M2 è ricavata leggendo il codice.
- La nota su Piper, che occupa il server single-thread fino a 60 s, è accettata come dichiarata (prova manuale e rara).

Non ho trovato antipattern del Wall of Shame: niente slicing della history, niente simulazione di tool, `_get_window` e i tetti non sono toccati. Le eccezioni dei provider (ElevenLabsTTSError, OSError, SubprocessError) vengono intercettate, loggate con warning e trasformate in 502/503, senza crash.

**Memoria**
Ho aggiunto la riga contatore #625-M2 e una lezione (Origin==Host non basta contro il DNS rebinding) a /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con lo script (83d1c3b).

Review #626-M2 (diff finale committato in 2116699):

## VERDETTO: APPROVATO

Ri-review #626-M2 di #625-M2. Branch feat/voce-v8-m2, diff staged di 7 file. Prima della review ho letto CLAUDE.md (in contesto), la sezione voce di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `clients/voice/browser_server.py:111` — `_host_locale()` accetta solo `127.0.0.1:<porta>`, `localhost:<porta>` e `[::1]:<porta>`, con la porta presa da `server_address[1]` (quella vera anche quando il proxy parte con la porta 0). Rischio esaminato: DNS rebinding, cioè un sito esterno che si fa risolvere a 127.0.0.1. In quel caso il browser manda il nome del sito in Host e la richiesta viene rifiutata. Il confronto non distingue maiuscole e minuscole. Una richiesta senza Host passa, ma un browser lo manda sempre, quindi il caso riguarda solo client locali. — **ok**
- `clients/voice/browser_server.py:81` — la guardia sta in testa a do_GET, quindi copre la pagina, /config e /voci/elenco. Prova: ho tolto la guardia e `test_proxy_solo_host_locale[evil.example-403]` è fallito; poi ho ripristinato dall'index. — **ok**
- `clients/voice/browser_server.py:133` — in do_POST la guardia viene prima di `_stessa_origine`. Il test usa apposta Origin uguale a Host (`evil.example`), cioè il caso che il solo controllo Origin==Host lasciava passare, e verifica che il server voce non riceva niente (`viste == []`). — **ok**
- `modules/voice/server.py:628` — `voci_ammesse` viene azzerato a ogni GET /voci/elenco e riempito solo se l'elenco riesce. Rischio esaminato: resta valido un elenco vecchio. Prova: ho tolto l'azzeramento e `test_elenco_fallito_azzera_le_voci_ammesse` è fallito; poi ho ripristinato dall'index. Il server voce è un `HTTPServer` a thread singolo (`modules/voice/server.py:753`), quindi non c'è corsa tra l'azzeramento e il nuovo riempimento. — **ok**
- Contesto: `clients/voice/browser_server.py:369` — il proxy ascolta solo su `("127.0.0.1", browser_port)`.

**La tua domanda (Host non locale e uso legittimo):** non rompe niente. Il proxy ascolta solo su 127.0.0.1, quindi da un altro computer della rete non era raggiungibile nemmeno prima. Un uso dalla rete locale richiederebbe di cambiare l'indirizzo su cui ascolta, e sarebbe una scelta di sicurezza da riesaminare a parte. Nota minore e innocua: `[::1]` non arriva mai, perché il proxy non ascolta su IPv6.

**Test:** `tests/test_unit_voice_prova_voci.py` 37 passed. Dopo le due prove, il motore nel working tree coincide di nuovo con l'index.

**Rischio escluso:** non ho verificato il comportamento con un browser vero e un DNS rebinding reale. Il test simula l'header Host con http.client. Non ho rilanciato la suite voce completa con browser (223 passed): mi fido del tuo dato.

**Memoria:** la riga contatore #626-M2 è in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Ma `bash scripts/commit_memoria_revisore.sh` è stato **bloccato dal sistema dei permessi** (motivo dato: commit non richiesto, coerente col tuo «Non committare»). Quindi la riga **non è committata**: va inclusa nel commit di fine task.

Commit della V8b (bb1fd62): tre passaggi del revisore.

Review #627-M2:

## VERDETTO: APPROVATO CON RISERVE

Review #627-M2: fetta V8b, branch feat/voce-v8-m2, diff staged di 6 file sopra 2116699. Ho letto, come richiesto, CLAUDE.md (sez. 5), stato_progetto e memoria_revisore (lezioni #624-626-M2 applicate).

**Elementi del diff esaminati**
- `modules/voice/prova_voci.py:103`: regex alfanumerica 8-80 per il proprietario; insieme a `voce_valida` filtra in `ordina_libreria` prima che owner e id entrino in `libreria_ammesse`. Rischio esaminato: iniezione nel percorso (`/`, `?`, `..`). **ok**
- `modules/voice/server.py:689`: l'aggiunta accetta solo un id presente nella mappa dell'ultima ricerca; owner e nome vengono dal server, non dal client; un id assente dà 409. Un JSON non-dict o non UTF-8 finisce nel ramo 400, catturato. Rischio esaminato: id o owner arbitrari e path injection in `modules/voice/tts.py:262`. **ok**
- `modules/voice/server.py:699`: tetto di 5 aggiunte all'ora, contato prima della chiamata (anche un tentativo fallito consuma lo slot, scelta prudente). Server single-thread, quindi niente gara. Mutante riprodotto (`if False:`): test_server_aggiunta_tetto_ed_errore fallisce; file ripristinato dall'index. Rischio esaminato: spesa e slot illimitati. **ok**
- `modules/voice/tts.py:239`: l'anteprima passa solo se è una stringa che inizia con `https://`, altrimenti resta vuota. In `clients/voice/prova_voci.html:226` va in `player.src`, cioè un media element che non esegue script; tutto il resto è inserito via textContent. Ho verificato che nessuna CSP blocchi l'anteprima. Rischio esaminato: schema `javascript:`/`data:` e XSS. **ok**
- `modules/voice/server.py:652`: `_libreria` azzera `libreria_ammesse` in testa (lezione R-625-2), e gli errori ElevenLabs e di rete tornano nel JSON con 200, mai un crash. Il caso «voices non è una lista» è coperto. **ok**
- `clients/voice/browser_server.py:94` e `clients/voice/browser_server.py:139`: inoltro dei due nuovi percorsi dopo le guardie Host/Origin già approvate, con il corpo cappato a 4096 byte. **ok**

**Riserve**
- **R-627-1-M2 (MEDIA)**: `modules/voice/prova_voci.py:101` ammette la categoria `high_quality` della libreria, che a mia memoria sono cloni istantanei, DA VERIFICARE. Se una voce così, una volta aggiunta, compare nell'account come `cloned`, la lista bianca dell'account la scarta (`modules/voice/prova_voci.py:34`). La pagina però dice «ora è nell'elenco qui sopra» (`clients/voice/prova_voci.html:198`): l'operatore spende uno slot e la voce non appare. Soluzioni: o si toglie `high_quality`, o la si verifica sul Mac e si scrive l'esito nella pagina.
- **R-627-2-M2 (BASSA)**: ci sono affermazioni su limiti e costi non verificate, contro la richiesta di M1:
  - «occupano uno spazio voce» (`modules/voice/prova_voci.py:107` e la docstring di `_aggiungi_voce`);
  - «gratis» sull'anteprima (`clients/voice/prova_voci.html:224` e `:178`).
  Vanno marcate «da verificare» oppure tolte.
- **R-627-3-M2 (COSMETICA)**: dopo l'aggiunta `fraseEl.textContent = ""` ricostruisce il select delle frasi e perde la frase scelta.

«Niente cloni di attori»: rispettato. La lista bianca esclude `famous` e le categorie nuove, e vale anche lato server tramite `libreria_ammesse`. Si prova solo con le frasi fisse.

Test: tests/test_unit_voice_prova_voci.py dà 45 passed.

**Rischio escluso**: forma reale dell'API (percorsi, nomi dei filtri, campi, categoria che una voce aggiunta prende nell'account, costi e limiti del piano). Non è verificabile: la rete del cloud blocca elevenlabs.io e il codice è dichiarato «DA VERIFICARE». Non ho rilanciato la suite voce completa (231 dichiarati dall'agente), ma solo il file di test della fetta. Non ho revisionato reports/prova_voce_mac.md, che non è staged.

Memoria: riga #627-M2 più una lezione (le liste bianche di categorie libreria → account vanno verificate in coppia) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate con scripts/commit_memoria_revisore.sh. L'index della fetta è intatto; non ho committato altro.

Review #628-M2:

## VERDETTO: APPROVATO CON RISERVE

Ri-review #628-M2 dopo la #627-M2 (branch feat/voce-v8-m2, diff staged di 6 file). Le tre riserve della #627 sono chiuse. Restano due riserve minori.

Cose del diff che ho esaminato:
- `modules/voice/prova_voci.py:104` — Ora le categorie ammesse dalla libreria sono solo `professional` e `generated`. Rischio controllato: un clone istantaneo che nell'account diventa «cloned» e non si vede. Il test `test_ordina_libreria` lo esclude. Esito: ok, R-627-1-M2 chiusa lato server.
- `clients/voice/prova_voci.html:204` — La pagina dice «ora è nell'elenco» solo se `j.id`, l'id nuovo che il server riceve da ElevenLabs (`modules/voice/server.py:714`), compare nell'elenco ricaricato. Rischio controllato: un messaggio di successo falso. Ho fatto un mutante che rende la condizione sempre vera: il test nel browser `[True]` fallisce. Esito: ok.
- `clients/voice/prova_voci.html:198` — La pagina salva la frase scelta prima di ricaricare e la rimette dopo (riga 202). Ho tolto il ripristino con un mutante: il test nel browser `[False]` fallisce. Ho rimesso il file come nell'index con `git checkout`: il working tree coincide di nuovo con lo staged. Esito: ok, R-627-3-M2 chiusa.
- `modules/voice/prova_voci.py:110` — Avviso: «probabilmente occupano uno spazio voce: DA VERIFICARE», e la gratuità dell'anteprima viene dichiarata non verificata. La docstring di `modules/voice/server.py:683` è allineata. Ho cercato «gratis» in tutto il codice: resta solo per Piper, che è locale (`clients/voice/prova_voci.html:276`), e in un commento di `browser_client.html` sulla voce di sistema. Esito: ok, R-627-2-M2 chiusa.
- `clients/voice/prova_voci.html:260` — Contesto: `caricaElenco` restituisce `[]` anche quando la lettura fallisce. Esito: riserva, vedi R-628-1-M2.

Test: `tests/test_unit_voice_prova_voci.py` dà 46 passed, compresi i 2 casi nel browser.

Riserve:
- **R-628-1-M2 BASSA**: se `/voci/elenco` fallisce subito dopo un'aggiunta riuscita, `caricaElenco` restituisce `[]`. La pagina allora dice «ElevenLabs l'ha messa in una categoria che Gas non mostra: toglila dall'account», ma la causa vera è l'errore di rete. Bisogna distinguere «elenco non letto» da «letto, ma la voce non c'è», ad esempio restituendo `null` in caso di errore.
- **R-628-2-M2 COSMETICA**: `statoLib(..., true)` alla riga 204 colora come errore anche il messaggio di successo, perché il `true` vale per tutti e due i rami del ternario.

Cosa NON ho verificato: il comportamento reale di ElevenLabs. Non so se una voce `professional` o `generated` aggiunta all'account mantenga la sua categoria, né se l'id restituito coincida con quello che compare poi nell'elenco dell'account. La rete verso ElevenLabs non è disponibile in dev e i test usano dati finti. La pagina però ora lo gestisce in modo onesto, con il ramo «non compare».

Memoria: ho aggiunto la riga #628-M2 e una lezione in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole nel commit 5f52963. Il diff staged dei 6 file è intatto e non l'ho committato.

Review #629-M2 (diff finale committato in bb1fd62):

## VERDETTO: APPROVATO

Ho riguardato le modifiche dopo la review #628-M2. Questa è la review #629-M2, sul branch feat/voce-v8-m2, con 6 file in staging. Prima ho fatto le letture obbligatorie: CLAUDE.md (sezioni 5 e 8, che ho nel contesto), le righe sulla voce in reports/stato_progetto.md e la fine di .claude/agents/memoria_revisore.md (lezione di #628-M2: distinguere «elenco non letto» da «elenco letto, voce assente»).

**Cosa ho controllato nel diff**
1. `clients/voice/prova_voci.html:264` — `caricaElenco` ora restituisce `null` quando la lettura fallisce per un errore di rete, una risposta non ok o un JSON rotto (il ritorno è alla riga 269). Prima restituiva `[]`. Rischio: un errore di rete scambiato per «voce assente», cioè la diagnosi falsa di R-628-1-M2. — ok. L'ho provato con un mutante: rimesso `return []` alla riga 269, il test nel browser `[rompi]` fallisce (1 failed, 2 passed). Poi ho ripristinato il file dall'index: nessuna modifica rimasta fuori dallo staging, il diff in staging è invariato (6 file, +484/-15).
2. `clients/voice/prova_voci.html:204` — dopo l'aggiunta ci sono tre casi distinti: `null` dà «non si è ricaricato: ricarica la pagina» (errore), voce presente dà «ora è nell'elenco», voce assente dà «non compare» (errore). Rischio: la promessa falsa di R-627-1-M2 e la causa sbagliata di R-628-1-M2. — ok. Il controllo `elenco === null` viene prima di `.some` (riga 206), quindi non può esserci un TypeError su `null`. Il messaggio contiene «aggiunta», quindi l'attesa del test (`includes('aggiunta')`) si risolve anche nel caso rotto.
3. `clients/voice/prova_voci.html:207` — il messaggio di successo chiama `statoLib` senza `true`, quindi non è più colorato come errore. Era R-628-2-M2. — ok. Nota a margine: nessun test controlla la classe CSS. È solo estetica, non la apro come riserva.
4. `tests/test_unit_voice_prova_voci.py:309` — il server finto risponde 502 sul GET dell'elenco quando l'aggiunta è già avvenuta e `rompi` è attivo. La libreria non è toccata, perché ha un ramo suo prima (riga 299). Rischio: che il test non riproduca davvero il fallimento dopo l'aggiunta. — ok. Il conteggio dei GET dell'elenco resta 2 (riga 522) anche nel caso rotto.
5. `tests/test_unit_voice_prova_voci.py:523` — nel caso `rompi` il test controlla «non si è ricaricato» e poi esce con `return`, quindi salta il controllo `fraseDopo`. È corretto: con l'elenco non riletto il menu delle frasi resta vuoto e la pagina chiede di ricaricare. — ok.
6. `tests/test_unit_voice_prova_voci.py:486` — il test ora ha tre casi: `False`, `True` e `"rompi"`. Le opzioni vengono azzerate in ogni fixture (righe 286-287), quindi un caso non contamina il successivo. — ok.

**Prove eseguite**: con `GAS_TEST_BROWSER_OBBLIGATORIO=1` passano 47 test su 47. Il mutante descritto al punto 1 fa fallire il caso `[rompi]`.

**Cosa NON ho verificato**
- Il comportamento sul Mac con l'API ElevenLabs vera: non si può riprodurre in sviluppo, ci sono solo server finti.
- Nessun test copre la colorazione CSS del messaggio di successo.
- Non ho riletto per intero `modules/voice/server.py`, `modules/voice/tts.py` e `modules/voice/prova_voci.py`: sono già stati coperti da #627-M2 e #628-M2 e questo giro non li tocca.

Antipattern della sezione 5: nessuno slicing della cronologia e nessuna simulazione di output dei tool. Cervelli e `_get_window` non sono toccati.

**Memoria**: aggiunta la riga #629-M2 («nessuna lezione nuova») in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit d5edc3d, solo quel file). Il diff in staging non l'ho toccato e non l'ho committato.

Merge di origin/main (8e88e78). Review #655-M2:

## VERDETTO: APPROVATO

Review #655-M2: merge di origin/main (70e2f05) in feat/voce-v8-m2, con tutto in staging.

**Cosa ho guardato nel diff**
- `git diff --cached origin/main --stat`: tocca solo i 9 file attesi (prova_voci.html, prova_voci.py, server.py, tts.py, browser_server.py, ci.yml, test prova_voci, memoria, prova_voce_mac.md). Nel conflitto della memoria la parte di main viene prima e quella del branch dopo (#624–#629-M2), senza marcatori residui.
- modules/voice/server.py:320 — l'azzeramento `self._capito = None` (V-3 bot #318) sta dopo `_t0` e `_tempi`, prima dei rami `/voci/*`. Rischio esaminato: con la connessione tenuta aperta resta il «capito» di un'altra richiesta. Ho tolto la riga a mano e il test `test_v6_capito_azzerato_a_ogni_richiesta` è fallito; ho ripristinato il file dall'index. — ok
- modules/voice/server.py:332 — il ramo voci mette `_tempi = None` solo dopo i controlli di token e di dimensione, e ritorna prima del flusso `/voice`. Rischio esaminato: rompere i tempi V7a o il formato a pezzi V7b. Le risposte 401/400 hanno i tempi vuoti, quindi `_chiudi_tempi` non scrive nulla. `_t0` e i tempi del ramo `/voice` restano quelli di main. — ok
- modules/voice/server.py:629 — il `do_GET` della V8 prende il posto dell'alias 405 che main usava per tutti i GET. Rischio esaminato: perdere il 405 sugli altri percorsi. `_method_not_allowed` è conservato e PUT/DELETE/PATCH restano su main. — ok
- clients/voice/browser_server.py:133 — nel proxy della pagina, il `do_POST` controlla prima l'host locale e poi la stessa origine. `/voci/prova` e `/voci/aggiungi` passano da `_inoltra_semplice` (corpo massimo 4096 byte), mentre `/voice` resta su `_inoltra_a_pezzi` di V7b (NDJSON). Il `do_GET` mette la guardia sull'host in testa e inoltra `/voci/elenco` e `/voci/libreria`. — ok
- .github/workflows/ci.yml:126 — prova_voci è aggiunta nello stesso passo della CI che rende il browser obbligatorio. — ok

**Prove:** prova_voci, voice_server, voice_stt, voice_tts, voice_contesto e voce_ascolto: 330 passed con `GAS_TEST_BROWSER_OBBLIGATORIO=1`. Ho riprodotto il numero comunicato dal chiamante.

**Rischio escluso:** non ho verificato la pagina reale sul Mac con ElevenLabs e i limiti dell'API vera, perché qui non si possono riprodurre. Non ho riletto da capo la logica V8/V8b già vista nelle review #624–#629-M2: ho controllato solo che il merge non la alteri.

**Memoria:** ho aggiunto la riga #655-M2 in fondo a /home/user/Gas/.claude/agents/memoria_revisore.md. `scripts/commit_memoria_revisore.sh` non ha creato nessun commit: con il merge in corso esce senza errore, come previsto. La riga è nel file ma non ancora in staging: aggiungila allo staging e falla entrare nel commit di merge. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Dopo il merge di main: `tests/test_unit_voice_prova_voci.py` + `test_unit_voice_server.py` + `test_unit_voice_stt.py` + `test_unit_voice_tts.py` + `test_unit_voice_contesto.py` + `test_unit_voce_ascolto.py`: 330 passed (`GAS_TEST_BROWSER_OBBLIGATORIO=1`). I test nuovi stanno in `tests/test_unit_voice_prova_voci.py` (aggiunto anche al passo della suite voce in `.github/workflows/ci.yml`). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud. Commit della sessione e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- Percorsi, campi e costi della libreria condivisa di ElevenLabs DA VERIFICARE sul Mac (documentazione non leggibile dal cloud).
- Pagina e proxy provati solo in locale col browser dei test; la resa vera delle voci si sente solo sul Mac.
