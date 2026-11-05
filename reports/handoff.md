# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 42: «Sì, signore?» lato client (PR #340)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #340 (https://github.com/Gasss23/Gas/pull/340). Review #671 e #675 APPROVATO CON RISERVE e PR nel perimetro: decide l'operatore tramite M1. Numero e URL dalla risposta dello strumento GitHub `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **PR #338 (fetta 43, parte 1)**: `FATTA` — mergiata (6a4cb2e) col sì dell'operatore, CI verde.
- **Fetta 42 — «Sì, signore?» lato client**: `FATTA` — pubblicata nella PR #340. Review #671 (2 MEDIE corrette), #672 APPROVATO, #675 APPROVATO CON RISERVE. Nel commit di merge su main, righe aggiunte e tolte identiche al diff rivisto.
- **Fetta 43, parte 2 (finestra di 40 s, difese dei turni di seguito, X-Gas-Seguito, X-Gas-Comando fine/pausa)**: `DEFERITA — è la prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 clients/voice/ascolto.py           | 140 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  15 +++++++--------
 reports/stato_progetto.md          |   6 +++---
 reports/ultimo_report.md           |  39 ++++++++++++++-------------------------
 scripts/voce/LEGGIMI.md            |   8 ++++++++
 tests/test_unit_voce_ascolto.py    | 321 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 6a4cb2e.

## §3 GIT LOG --ONELINE (sessione)

```
482870d Merge della fetta 42 («Sì, signore?» lato client) su main dopo la #338
98074fc Merge origin/main (PR #335, GET /voce/conferma) nella fetta 42, con test d'integrazione col server vero — review #675
9efc4bd feat(voce): fetta 42 — «Sì, signore?» dopo la parola di attivazione (lato client)
938ed9c chore(revisore): memoria review #672 — APPROVATO
7bae1a7 chore(revisore): memoria review #671 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 9efc4bd — review #671 (primo giro), verdetto integrale. Le righe citate sono quelle del diff di allora:

## VERDETTO: APPROVATO CON RISERVE

Review #671 (chat Mani). Fetta 42: «Sì, signore?» nell'ascolto H24. Diff staged su mani/si-signore, base 942e665, 3 file (+332/-6).

Prima della review ho letto CLAUDE.md (§5, §8, §9), lo stato del progetto (voci voce/Mani) e la mia memoria (ultima voce #670, quindi questa è la #671).

**Cosa ho esaminato nel diff**
- `clients/voice/ascolto.py:719` — `scarica_conferma`: fa la richiesta con `_OPENER`, quindi niente proxy e niente redirect. Restituisce None su HTTPError, su qualsiasi eccezione (comprese connessione chiusa e IncompleteRead, perché anche `read` sta dentro il try), su codice diverso da 200, su tipo diverso da audio/*, su audio vuoto o oltre 1 MB. Il token non finisce mai nei log. La richiesta non porta audio dell'operatore: arriva solo l'MP3 della voce di Gas. Rischi controllati: §9, redirect che porta via il Bearer, privacy. **ok**
- `clients/voice/ascolto.py:747` — `Conferma`: lock attorno a `_audio`, `_in_corso` e `_ultimo`. `_in_corso` torna False in ogni caso, perché `_prendi` intercetta tutte le eccezioni. Il thread è demone. Il conto del minuto parte dall'inizio del tentativo. Rischi controllati: gara tra thread, doppio download, tentativo bloccato per sempre. **ok**
- `clients/voice/ascolto.py:504` (e la chiamata a `clients/voice/ascolto.py:545`) — `_conferma_o_bip`: il bip scatta se la conferma è None, vuota, rotta o non riproducibile. La conferma intanto continua a leggere il microfono (così il buffer non si riempie), senza rilevatore. Il `_svuota` resta subito dopo. All'interruzione e nella finestra dei 12 s resta il bip. **ok**
- `clients/voice/ascolto.py:876` — interruttore `GAS_ASCOLTO_CONFERMA` dentro `main`. **riserva (R-671-1)**
- `tests/test_unit_voce_ascolto.py:171` — il finto di main legge `k["conferma"]` con le parentesi quadre. **riserva (R-671-2)**
- `clients/voice/ascolto.py:102` — tetto di 1 MB. **riserva (R-671-3)**

**Esecuzione** (copia scratch fatta dall'index, il repo non è stato toccato): 198 test raccolti, 177 passati. I 21 falliti sono solo ambientali (`openai` non installato, `gas.py:26`) e sono identici nel repo vero.

**Mutanti miei**
- `if conferma_attiva():` sostituito con `if True:` → **SOPRAVVIVE** (32 test passati).
- M7 (conferma non passata ad `Ascolto`) → il test di main **resta appeso** e l'ho fermato col timeout. Ho verificato che `.github/workflows/ci.yml` non ha `timeout-minutes`.

**Finding**
- **R-671-1 (MEDIA)**: l'interruttore `GAS_ASCOLTO_CONFERMA=0` è testato solo nella funzione `conferma_attiva` presa da sola. Se `main` lo ignora, nessun test se ne accorge. Correzione: parametrizzare `test_main_passa_la_soglia_della_voce` anche con `GAS_ASCOLTO_CONFERMA=0` e attendersi `conferme == [None]`.
- **R-671-2 (MEDIA)**: sì, M7 merita un test più netto. Il `KeyError` del finto viene inghiottito dall'`except Exception` (§9) di `main` (`clients/voice/ascolto.py:893`), che poi chiama il vero `time.sleep(RIPROVA_MICROFONO_S)` e riprova all'infinito. Quindi il test non fallisce: si blocca. In CI, senza timeout, il job resterebbe fermo fino al limite di GitHub (6 ore). Correzione: nel finto usare `k.get("conferma")` e asserire dopo. In più, conviene un monkeypatch di `a.time.sleep` che sollevi un'eccezione (per esempio `pytest.fail`), così ogni giro nel ciclo di riprova fa fallire subito il test. La fragilità c'era già per `voce_rms` e `soglia_interruzione`: si sistemano tutti e tre insieme.
- **R-671-3 (BASSA)**: 1 MB di MP3 sono circa 60 s di conferma non interrompibile. Il server è locale e autenticato, ma un tetto di circa 200 KB basterebbe ampiamente per «Sì, signore?».
- **R-671-4 (BASSA)**: l'audio resta in memoria fino al riavvio. Se M2 cambia la voce sul server, il client continua a dire la frase con la voce vecchia. Va scritto nel LEGGIMI.
- **R-671-5 (BASSA)**: `Conferma(...)` in `main` sta fuori dal try. Se `Thread.start` fallisce all'avvio (caso rarissimo), `main` esce. Se fallisce dopo, `_in_corso` resta True e da lì in poi c'è sempre e solo il bip, che resta un ripiego sicuro.
- **COSMETICA**: la docstring di `conversazione` (`clients/voice/ascolto.py:543`) dice ancora «bip».
- Il mutante «except HTTPError tolto» sopravvive, ma è equivalente come dichiarato: lo prende l'except generico. Il ramo serve solo per un messaggio di log più preciso. Lo accetto.

**Cosa NON ho verificato**
- La coerenza con il contratto reale di M2: la PR #335 non è nei riferimenti locali, quindi non ho potuto leggere il server. Mi sono basato sul contratto descritto nel brief (200 audio/mpeg, 503, 502, connessione chiusa).
- Il comportamento sul Mac (`afplay` vero, latenza reale della conferma, microfono): non riproducibile in questo ambiente.

**Memoria**: riga #671 e una lezione nuova (un finto dentro un `main` con ciclo «except → riprova» deve usare `k.get`, altrimenti il test resta appeso invece di fallire). Committata con `scripts/commit_memoria_revisore.sh` (commit 7bae1a7). Lo staged non è stato toccato: restano in stage gli stessi 3 file.

Commit 9efc4bd — review #672 (ri-review con le correzioni), verdetto integrale:

## VERDETTO: APPROVATO

Ri-review #672 (chat Mani) della fetta 42 «Sì, signore?» sul branch mani/si-signore: diff staged di 3 file (+406/-21), HEAD 7bae1a7. Prima di revisionare ho letto CLAUDE.md, la riga 4 di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md, dove c'è la lezione #671 su `k.get`, che ho applicato. Il repo vero non l'ho toccato: test e mutanti girano su una copia dell'indice in scratch, presa con `git checkout-index`.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:777`: se `Thread.start` fallisce, il blocco except rimette `_in_corso` a False sotto lock. Rischio esaminato: conferma bloccata «in corso» per sempre. Esito ok: `_ultimo` è già impostato, quindi si riprova dopo 60 s. Il mutante «reset tolto» fallisce subito (`test_conferma_thread_che_non_parte`). **R-671-5 chiusa.**
- `clients/voice/ascolto.py:886`: try attorno a `Conferma(...)` in main, con log warning e bip come ripiego. Rischio esaminato: crash all'avvio di main. Esito ok: il mutante «try tolto» è preso da `test_main_con_conferma_che_non_parte`.
- `clients/voice/ascolto.py:102`: `CONFERMA_MAX_BYTE` passa a 200 KB. Esito ok. **R-671-3 chiusa.** Il mutante «1 MB» è preso, ma solo da un test tautologico sulla costante (vedi note cosmetiche).
- `clients/voice/ascolto.py:901`: main passa `conferma=conferma` ad Ascolto. Esito ok: i mutanti «non passata» e «sempre attiva» falliscono in meno di 0,5 s.
- `tests/test_unit_voce_ascolto.py:145`: l'helper `_main_finto` usa `k.get` e sostituisce `time.sleep` con `pytest.fail`. Rischio esaminato: test appeso nel ciclo di riprova di main. Esito ok: il `Failed` di pytest è una BaseException, quindi scavalca l'except di main. L'unico `time.sleep` di main è nel ciclo di riprova (`clients/voice/ascolto.py:910`). Il `dorme=time.sleep` di Ascolto è legato quando la classe viene definita e non viene toccato. **R-671-2 chiusa.**
- `tests/test_unit_voce_ascolto.py:195`: `test_main_passa_la_conferma` con None, «1», «0» (con «0» dà None). Esito ok. **R-671-1 chiusa.**
- `scripts/voce/LEGGIMI.md:12`: la voce vecchia resta fino al riavvio con `installa.sh`. Esito ok: lo script fa davvero bootout e bootstrap con launchctl (contesto: `scripts/voce/installa.sh:146`). **R-671-4 chiusa.**

**Mutanti e test.** Ho provato 8 mutanti in copie scratch e li ho presi tutti, ognuno in 15 s o meno, nessun test appeso:
- conferma sempre attiva
- conferma non passata ad Ascolto
- reset di `_in_corso` tolto
- try in main tolto
- tetto rimesso a 1 MB
- conferma interrompibile
- svuota dopo la conferma tolto
- `_ultimo` non impostato

Sull'export dell'indice: 183 passed e 21 failed. I 21 sono tutti ambientali (20 `test_installa_legge_il_env_come_gas`, 1 `test_dotenv_usa_il_caricatore_di_gas`), lo stesso insieme visto nelle review #669 e #671. 183 + 21 = 204, coerente con il conteggio dell'agente nel venv completo. `git diff --cached --check` è pulito.

**Note cosmetiche (non bloccanti, senza codice R)**
- `tests/test_unit_voce_ascolto.py:993`: `test_conferma_tetto_piccolo` controlla solo il valore della costante. Il taglio vero di `r.read` è già provato da `test_conferma_troppo_grande`.
- Spaziatura PEP8: manca una riga vuota prima di `tests/test_unit_voce_ascolto.py:997` (E302). Ci sono tre righe vuote prima di `class _ServerConferma` e di `test_conferma_thread_che_non_parte` (E303), e una sola prima di `test_json_con_un_solo_audio`.

**Non verificato**
- Ascolto su Mac reale (afplay, LaunchAgent, voce ElevenLabs): non riproducibile nel container Linux.
- Patch globali di `time.sleep` e `threading.Thread` nei test: non ho provato l'esecuzione con xdist o in parallelo. Le patch riguardano tutto il processo per la durata del test; nella suite seriale di oggi è un rischio basso.

Memoria aggiornata con la riga #672 e committata da sola con `scripts/commit_memoria_revisore.sh` (commit 938ed9c). Lo staged è intatto: 3 file, 406+/21-.

Commit 98074fc (merge di main più test d'integrazione) — review #675, verdetto integrale. Il commit 482870d (merge su main dopo la #338) ha righe aggiunte e tolte identiche nei file del perimetro, verificate con il confronto dei diff:

## VERDETTO: APPROVATO CON RISERVE

Review #675 (chat Mani). Oggetto: il merge di origin/main 2bb05b0 in mani/si-signore, staged e non committato, nel worktree /tmp/claude-0/wt42, più il test d'integrazione client contro il server vero.

Letture obbligatorie fatte: CLAUDE.md sez. 5, la memoria del revisore (ultime righe da #668 a #674-M2) e il contesto della fetta 42 (#671/#672). Nel diff non ci sono slicing della history né output di tool simulati. Il diff tocca solo il client voce e i test, non il motore.

**Il merge non perde nulla**
- Dalla base 942e665, HEAD (9efc4bd) toccava solo 4 file: memoria, clients/voice/ascolto.py, scripts/voce/LEGGIMI.md, tests/test_unit_voce_ascolto.py. Main non ha toccato né il client né il LEGGIMI.
- `git diff --cached MERGE_HEAD` contiene solo quei 4 file. Quindi tutto il resto (server, bot, report, test voice*) è identico a main, e ascolto.py e LEGGIMI sono identici a HEAD. Il test di ascolto è quello di HEAD più le righe nuove.
- Memoria: è l'unione dei due lati. Con `comm` risultano 0 righe di HEAD perse, 0 righe di MERGE_HEAD perse e 0 doppioni.
- `git diff --cached --check` è pulito e `ls-files -u` è vuoto.

**Elementi del diff esaminati**
- clients/voice/ascolto.py:101 — `CONFERMA_PERCORSO = "/voce/conferma"`. Rischio: un percorso diverso da quello del server. Il server usa lo stesso percorso (modules/voice/server.py:129). Esito: ok, e il mutante `/voce/conferme` viene ucciso dal test nuovo.
- clients/voice/ascolto.py:730 — il client accetta solo HTTP 200 con tipo che inizia per `audio/`. Rischio: il client rifiuta `audio/mpeg` del server. Il server risponde `audio/mpeg` (modules/voice/server.py:388). I codici 401 (modules/voice/server.py:767), 503 senza chiave e 502 per errore TTS, errore di rete o audio vuoto passano tutti per HTTPError e danno None, quindi il bip. Esito: ok, e il mutante con Content-Type `application/octet-stream` viene ucciso.
- tests/test_unit_voce_ascolto.py:934 — fixture con una sottoclasse di VoiceHandler, `conferma_cache` isolata sulla classe, porta 0, shutdown e server_close. Rischio: stato che passa da un test all'altro o server lasciato appeso. Esito: ok.
- tests/test_unit_voce_ascolto.py:952 — caso 200 con l'audio esatto e caso 401. Esito: ok, e il mutante "auth tolta" viene ucciso.
- tests/test_unit_voce_ascolto.py:962 — casi d'errore (senza chiave, errore TTS, audio vuoto). Esito: riserva R-675-1, vedi sotto.

**Test e mutanti** (copia dall'index in scratch)
- Le suite voce_ascolto più voice* danno **492 passed** (5 min 29 s). test_unit_voce_ascolto.py da solo dà 208 passed e i 4 test nuovi danno 4 passed.
- 6 mutanti sul server:
  - uccisi: percorso del client, Content-Type, auth tolta;
  - sopravvivono al test d'integrazione: controllo della chiave tolto, audio vuoto servito con 200, ElevenLabsTTSError non intercettata.
- Questi 3 restano coperti dai test del server (tests/test_unit_voice_prova_voci.py:712, che verifica 503 senza sintesi chiamata, 502 e cache vuota). Per questo la riserva è BASSA e non blocca.

**Riserve**
- **R-675-1 BASSA**: i casi d'errore del test d'integrazione (tests/test_unit_voce_ascolto.py:972) controllano solo che il risultato sia None, non i codici 503/502 che dichiarano di coprire. Il client riduce ogni errore a None, quindi un ramo d'errore cancellato sul server passa verde. Correzione:
  - usare caplog e verificare «HTTP 503» per senza_chiave e «HTTP 502» per gli altri due casi;
  - nel caso senza_chiave, far chiamare `pytest.fail` alla sintesi finta, così si prova che non viene chiamata.
- **R-675-2 COSMETICA**: 3 righe vuote prima di tests/test_unit_voce_ascolto.py:933 (E303) e una sola prima di tests/test_unit_voce_ascolto.py:974 (E302).

**Rischi esclusi**
- Comportamento reale su Mac (afplay, launchd) e con ElevenLabs vero: non verificato, non riproducibile qui.
- Report e handoff presi da main: non riletti nel merito. Ho verificato solo che sono identici a MERGE_HEAD, quindi per questi report la fetta 42 dovrà riscriverli al fine-task.
- Le suite fuori dalla voce (motore, verifica_bot) non le ho rieseguite: i loro file sono identici a main.

**Memoria**: aggiunte la riga contatore #675 e una lezione in .claude/agents/memoria_revisore.md. Sono nel working tree e NON committate, come richiesto: il file ora è `MM`, quindi va aggiunto allo stage prima del commit del merge.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 185 (main dopo la #338) a 220 casi. Riepilogo reale nel venv con requirements e requirements-dev, sul branch dopo il merge:

```
220 passed in 24.84s
```

Mutanti presi:
- fetta 42 prima della #671: sempre bip, conferma interrompibile, tipo non controllato, nessun limite ai tentativi, download non in sottofondo, svuota tolto, vuoto accettato;
- dopo la #671: conferma sempre attiva, conferma non passata da main (ora fallisce subito, niente test appeso), try in main tolto, reset di `_in_corso` tolto, tetto rimesso a 1 MB;
- dal revisore #675: percorso, Content-Type, auth tolta.

Sopravvive l'equivalente «except HTTPError tolto». Suite voce (ascolto, server, prova_voci, stt) dopo il merge della #335: 462 passed (mio), 492 passed (revisore #675, col test d'integrazione).

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP).

Mappatura commit → run:
- 482870d, 98074fc, 9efc4bd, 938ed9c, 7bae1a7: pushati insieme prima di aprire la PR #340; run del push non letta alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-675-1 BASSA: i casi d'errore del test d'integrazione controllano solo None, non i codici 503/502.
- R-675-2 COSMETICA: righe vuote PEP8 nel file di test.
- Note cosmetiche della #672: un test che controlla solo la costante del tetto; spaziature PEP8.
- Restano le riserve delle fette 40, 41 e 43 (R-673-1/2/3 e quelle di bot e verifica esterna), in `reports/stato_progetto.md`.
