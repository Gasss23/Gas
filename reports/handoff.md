# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — chat Mani: voce via Telegram, fetta 4 (voce consegnata in un thread, opzione b) + tempi della voce di casa + correzioni della guardia T78p dopo bot e verifica esterna #359

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #359 (https://github.com/Gasss23/Gas/pull/359): è un CAMBIO DI SICUREZZA, perché allarga la guardia T78p delle firme (opzione b). Serve il sì esplicito dell'operatore, anche se il verdetto del bot è pulito. Consigliato il secondo passaggio nella chat claude.ai col link della PR.
2. Guardia T78p: il revisore (#733) consiglia di fermarsi qui. Le elusioni che restano (R-733-1/2, BASSE) richiedono codice scritto apposta e visibile in review. Decide l'operatore se accettare questo limite della guardia statica.

---

## §1 SCOPE & ESITO FETTE

- **PR #357 (fetta 3)**: `FATTA` — mergiata (524ae96).
- **Voce consegnata in un thread (opzione b)**: `FATTA` — review #725 e #727.
- **Tempi della voce di casa**: `FATTA` — review #722.
- **Bot e verifica esterna #359 (V-1/V-2 MEDIA sulla guardia T78p, V-3/V-4/V-5)**: `FATTA` — review #729–#733, guardia trasformata in allow-list, 27 mutanti presi su 28 (1 inconclusivo).
- **Merge di main con la PR #358 di M2**: `FATTA` — review #735 APPROVATO.
- **R-733-1/2, R-725-3 (BASSE)**: `DEFERITA — tracciate in stato_progetto.md; per R-733 decide l'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  17 ++++++++
 clients/voice/ascolto.py           |   7 ++++
 modules/telegram/bot.py            |  46 +++++++++++++++++++---
 reports/diff_sessione.md           |  17 ++++----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   5 ++-
 reports/ultimo_report.md           |  26 ++++++-------
 tests/test_unit_kernel.py          | 220 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_telegram_voce.py   |  92 +++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py    |  15 +++++++
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
4e57b58 Merge origin/main (#358 di M2, server voce più sicuro) nella PR #359 — review #735
5801c12 chore(revisore): memoria review #729–#733 e stato della fetta 4 (chat Mani)
fff8f3b fix(telegram): guardia T78p della voce come allow-list, chiude le elusioni di bot e verifica esterna #359 — review #729–#733
f352190 docs(fine-task): fetta 4 voce Telegram in un thread — PR #359 per il sì dell'operatore (sicurezza)
62cb860 Merge mani/telegram4: voce Telegram in un thread a parte (opzione b) — review #728
aca5b88 feat(telegram): voce consegnata in un thread a parte, guardia T78p irrobustita (opzione b) — review #725/#727
3404378 feat(voce): tempo fino alla prima frase di Gas nel log dell'ascolto (misura della velocità) — review #722
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti integrali per commit:
- 3404378: review #722.
- aca5b88: review #725 e #727.
- 62cb860: review #728.
- fff8f3b: review #729–#733.
- 4e57b58: review #735.

### Review #722

## VERDETTO: APPROVATO CON RISERVE

Review #722 (chat Mani). Riguarda il diff staged su mani/tempi-ascolto nel worktree /tmp/claude-0/wt49 (base b827447). I due file del diff sono `clients/voice/ascolto.py` (+7) e `tests/test_unit_voce_ascolto.py` (+15).

Letture fatte prima della review:
- CLAUDE.md, sezione 5.
- reports/stato_progetto.md, letto in modo mirato.
- La memoria del revisore, comprese le voci #720 e #721 del repo principale e di wt48 (sono le review più alte, la regola notturna è quella applicata nella #721). Il file in wt49 si ferma alla #719.

Elementi del diff esaminati:
1. `clients/voice/ascolto.py:537` — `t0 = time.monotonic()` prima di `invia`/`invia_seguito`, fuori dal `try`. Rischio controllato: un nuovo punto da cui può partire un'eccezione (§9) e un cambio di comportamento. `time.monotonic` non solleva eccezioni in pratica. Non cambia nessun ramo: fine, pausa, errore e seguito restano identici. Esito: ok.
2. `clients/voice/ascolto.py:588` — `if suonati == 1: log.info("tempo: prima frase di Gas dopo %.2f s …")`, dopo il filtro `if not audio: continue` e prima di `riproduci`. Rischi controllati:
   - Dati nel log: la riga contiene solo un float in secondi. Niente parlato, niente `testo` del pezzo, niente motivo né URL.
   - Ripetizione della riga: `suonati` sale solo una volta per pezzo con audio, quindi c'è una sola riga per turno. Se la risposta non contiene audio (o si interrompe prima del primo pezzo) la riga non compare.
   - Esito: ok.
3. `tests/test_unit_voce_ascolto.py:2490` — il test `test_tempo_fino_alla_prima_frase_nel_log`. Usa il monkeypatch di `a.time.monotonic`, che è il modulo `time` globale: il patch vale per tutto il processo ma pytest lo ripristina a fine test. Rischi controllati:
   - Altri test rotti: no.
   - Default legati alla definizione: i default `adesso=time.monotonic` in `clients/voice/ascolto.py:905` e `clients/voice/ascolto.py:974` sono già legati quando il modulo viene definito, quindi il patch non li tocca.
   - Iteratore esaurito: le chiamate oltre la lista ricevono 999.0, mai `StopIteration`.
   - `logging` usa `time.time` e non `monotonic`.
   - Esito: ok, con la riserva R-722-1.

Verifiche riprodotte sulla copia dell'index (checkout-index nello scratchpad, niente stash):
- `pytest tests/test_unit_voce_ascolto.py`: 296 passed.
- `git diff --cached --check` pulito; worktree uguale all'index.
- Mutanti miei, 4 su 4 presi (ognuno dà 1 failed):
  - riga «a ogni frase» (`>= 1`);
  - t0 preso dopo l'invio;
  - riga tolta;
  - livello `debug` al posto di `info`.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. Il diff non tocca il kernel, `_get_window`, il tetto di 10 iterazioni né il tetto di 8k.

Riserve:
- **R-722-1 COSMETICA** — il test dipende dall'ordine esatto delle chiamate a `time.monotonic`. Se in futuro si aggiunge una chiamata nel percorso di invio, il test diventa rosso: non diventa mai un falso verde.
- **R-722-2 BASSA** — misura il tempo fino al primo pezzo audio pronto, non fino al suono effettivo (la riga viene scritta prima di `riproduci`). Inoltre non separa invio, server e sintesi: per sapere dove si perde tempo servirà incrociarla con i tempi del server (V7a).

Regola notturna: la PR rientra. Ci sono solo riserve BASSE o COSMETICHE e nulla tocca sicurezza, gate, cancello o perimetro del kernel.

Rischio escluso: il comportamento sul Mac (afplay vero, rete verso il server della voce, valore reale misurato) non è stato verificato perché non si può riprodurre nel container. Non ho neanche controllato su quale file finisce il logger `gas.ascolto` sul Mac: è configurazione dell'avvio, fuori dal diff.

Memoria: ho aggiunto la riga #722 in coda a /tmp/claude-0/wt49/.claude/agents/memoria_revisore.md, non committata come richiesto. Non ho lanciato commit_memoria_revisore.sh perché la tua istruzione dice «non committata». Nessuna lezione nuova.

File rilevanti:
- /tmp/claude-0/wt49/clients/voice/ascolto.py
- /tmp/claude-0/wt49/tests/test_unit_voce_ascolto.py
- /tmp/claude-0/wt49/.claude/agents/memoria_revisore.md
### Review #725

## VERDETTO: APPROVATO CON RISERVE

**Review #725 (chat Mani).** Diff STAGED in /tmp/claude-0/wt50, branch mani/telegram4, HEAD 58f088a (la PR #357 non è ancora mergiata).

**È un cambio di sicurezza:** la guardia T78p, che garantisce che le firme si gestiscano «un click alla volta», è stata allargata. Il merge spetta all'operatore, che ha già scelto l'opzione (b) via M1.

**Prove sulla copia dell'index** (fatta con checkout-index, niente stash, cartella /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/r725):
- telegram_voce: 70 passed.
- kernel: 1099 PASS e 1 FAIL. L'unico FAIL è T31g, legato all'ambiente. T78p è verde.
- voce_ascolto: 296 passed.
- `git diff --cached --check`: c'è una riga vuota in fondo al file di test.

### Elementi del diff esaminati
- `modules/telegram/bot.py:997` — `_consegna_voce` crea il pool (un solo thread) alla prima voce e gli passa solo `_invia_risposta_vocale` (riga 1002). Il testo `finale` è già calcolato prima dell'invio al thread. Gli errori finiscono nel log (§9). **Rischio esaminato:** il thread tocca qualcosa oltre alla voce? No. Il thread chiama solo `testo_da_dire`, `synthesize_speech`, `_send_text`, `_tg_post` e `_tg_post_file`. `_tg_post` (riga 75) e `_tg_post_file` creano una richiesta nuova a ogni chiamata e non hanno stato condiviso. Il thread non usa mai kernel, memoria o firme. Usare `_send_text` in parallelo al polling è sicuro. `modules/voice/server.py` all'import non avvia niente, e il blocco degli import di Python basta. — **ok**
- `modules/telegram/bot.py:987` — `_gestisci_parlato` mette la voce in coda dopo aver mandato il testo. Rischio esaminato: l'ordine dei messaggi su Telegram. — **riserva R-725-3**
- `modules/telegram/bot.py:1007` e `modules/telegram/bot.py:559` — `_chiudi_voce` con `shutdown(wait=False, cancel_futures=True)` viene chiamato al Ctrl-C. **Provato con un ThreadPoolExecutor vero:**
  - con la chiusura, all'uscita si aspetta solo la voce in corso (2 s);
  - senza la chiusura, si eseguono tutte le voci in coda (4 s).
  
  L'attesa per la voce in corso arriva a circa 2×VOCE_TIMEOUT_S, ma 15 s è il tetto per ogni operazione sul socket, non per l'intera voce (come R-721-2). Un secondo Ctrl-C interrompe l'attesa con un traceback. — **ok con riserva R-725-2**
- `modules/telegram/bot.py:63` — VOCE_TIMEOUT_S resta 15 e cambia solo il commento. — **ok**
- `tests/test_unit_kernel.py:8393` — La guardia T78p allargata: un secondo pool solo in `_consegna_voce`, nomi vietati nelle tre funzioni della voce, e la riga 8401 controlla che si sottometta solo `_invia_risposta_vocale`. **Rischio esaminato:** si può eludere? **Sì**, vedi R-725-1. — **riserva**
- `tests/test_unit_telegram_voce.py:504` — Test con thread vero: ordine giusto, una voce alla volta, il chiamante non aspetta. Il fixture `tg` (riga 84) sostituisce `_consegna_voce` con una consegna immediata, quindi gli altri test restano sincroni. La riga 548 verifica `shutdown(False, True)` e che la coda si azzeri. — **ok**

### Riserve
**R-725-1 MEDIA — la guardia T78p si elude.** Ho provato 3 mutanti miei e con tutti T78p risulta PASS:
1. **Mutante A:** in `_gestisci_parlato`, `_voce_in_coda.submit(lambda: kernel.run_turn(trascritto))`. Mette un turno nel thread della voce, cioè proprio il rischio da evitare. La guardia controlla `submit` solo dentro `_consegna_voce`, e `_riferiti78p` non vede `run_turn` dentro una lambda.
2. **Mutante B:** `_voce_in_coda.map(...)` dentro `_consegna_voce`. La guardia guarda solo `submit`.
3. **Mutante C:** chiamata diretta a `gestisci_callback(...)` dentro `testo_da_dire`, che gira nel thread. La guardia per nomi non segue le funzioni chiamate.

Correzione proposta:
- ogni chiamata `.submit` o `.map` nel modulo è ammessa solo in `_invia_a_tutti` e in `_consegna_voce`;
- `_voce_in_coda` si nomina solo in `_consegna_voce` e `_chiudi_voce` (più l'assegnazione a livello di modulo);
- i nomi vietati si controllano anche nelle funzioni del modulo raggiungibili da `_invia_risposta_vocale` (`testo_da_dire`, `_send_text`, `_tg_post`, `_tg_post_file`).

Oggi il codice è corretto. La riserva riguarda la protezione contro regressioni future.

**R-725-2 BASSA — uscita fuori dal ramo Ctrl-C.** Un KeyboardInterrupt durante `time.sleep(5)` del ramo except (`modules/telegram/bot.py:564`, fuori dal try) salta `_chiudi_voce`. All'uscita Python esegue allora tutta la coda delle voci (comportamento provato).

**R-725-3 BASSA — ordine dei messaggi.** Il vocale e gli avvisi «✗ Risposta vocale … la risposta è nel testo sopra» ora possono arrivare dopo la risposta in testo del messaggio successivo: «sopra» può trarre in inganno.

**R-725-4 COSMETICA — riga vuota in fondo al file.** `git diff --check` segnala una riga vuota in fondo a `tests/test_unit_telegram_voce.py`, come nella #720.

### Rischio escluso
- Non ho verificato il comportamento reale su VPS e Telegram, con ElevenLabs lento o con SIGTERM di systemd (il segnale di default uccide il processo senza aspettare): non si riproduce in sviluppo, e ho provato solo con mock e con un ThreadPoolExecutor vero in locale.
- Non ho ri-revisionato `clients/voice/ascolto.py` e `tests/test_unit_voce_ascolto.py`, già coperti dalla #722: ho solo rieseguito i 296 test.

### Memoria
- Ho aggiunto la riga #725 più una lezione in coda a /tmp/claude-0/wt50/.claude/agents/memoria_revisore.md. Il numero più alto prima era #724.
- **NON** l'ho committata (come da tua istruzione), quindi non ho lanciato `commit_memoria_revisore.sh`.
- Nota: il file ora è «MM», cioè ha parti staged e parti nel working tree. Va rifatto lo staging prima di `segna_review_ok.sh`, altrimenti lo SHA del diff revisionato cambia.
### Review #727

## VERDETTO: APPROVATO CON RISERVE

Review #727 (chat Mani). È una ri-review della #725 sul diff staged in /tmp/claude-0/wt50 (branch mani/telegram4, base 58f088a). Prima ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (solo le parti che servivano) e la coda della mia memoria.

**Cosa ho controllato nel diff**
- `tests/test_unit_kernel.py:8410` — `_consegne78p` cerca in tutto il modulo le chiamate `.submit` e `.map` e le ammette solo in `_invia_a_tutti` e `_consegna_voce`. Rischio esaminato: una sottomissione con lambda da un'altra funzione, o un metodo diverso da submit. Esito: ok. Il mutante A (lambda con `kernel.run_turn` sottomessa da `_gestisci_parlato`) e il mutante B (`.map` in `_consegna_voce`) danno T78p FAIL. Fallisce anche un mio mutante nuovo, E: in `_gestisci_parlato`, `ex = globals()['_voce_in_coda']; ex.submit(...)`.
- `tests/test_unit_kernel.py:8416` — `_funzioni78p` più la visita del grafo delle chiamate partendo da `_invia_risposta_vocale`. Inoltre `tests/test_unit_kernel.py:8425` cerca i nomi vietati in tutte le funzioni raggiunte, e `tests/test_unit_kernel.py:8436` controlla che `testo_da_dire` sia davvero tra le raggiunte. Rischio esaminato: una chiamata vietata dentro una funzione chiamata dal thread. Esito: ok per le funzioni di primo livello. Il mutante C (`gestisci_callback` dentro `testo_da_dire`) dà FAIL, e così il mio mutante F (`_KERN.run_turn(finale)` dentro `testo_da_dire`). Esito: riserva per gli altri casi (vedi R-727-1).
- `modules/telegram/bot.py:564` — il `time.sleep(5)` del ramo except ora sta in un try. Su KeyboardInterrupt chiama `_chiudi_voce` (`modules/telegram/bot.py:567`) ed esce con 0. Anche lo sleep di `modules/telegram/bot.py:550` sta dentro il try esterno, coperto da `modules/telegram/bot.py:559`. Rischio esaminato: uscita su Ctrl-C che salta la chiusura della coda. Esito: ok, R-725-2 chiusa. Nota: questo ramo non ha un test, ma è una modifica meccanica e l'ho verificata leggendo il codice.
- `modules/telegram/bot.py:1002` — `_consegna_voce` non è cambiata rispetto alla #725. Il submit ha un solo bersaglio, `_invia_risposta_vocale`, ed è dentro try §9. Il mio mutante G (submit di `_handle_update` in più) dà FAIL. Esito: ok.
- `tests/test_unit_telegram_voce.py:560` — fine del file: niente più riga vuota, e `git diff --cached --check 58f088a` non trova niente. R-725-4 chiusa.

**Prove sulla copia dell'index** (checkout-index nello scratchpad, niente stash)
- pytest su telegram_voce + voce_ascolto: 366 passed.
- `python tests/test_unit_kernel.py`: 1099 PASS, 1 FAIL. L'unico FAIL è T31g (manca sqlite_vec nell'ambiente, come sulla base); T78p è PASS.
- Mutanti: 6 su 8 presi (A, B, C della #725, più i miei E, F, G). Due non presi, D e H: sono la riserva R-727-1.

**Riserve**
- **R-727-1 BASSA**: il grafo considera solo le funzioni definite al primo livello del modulo. Non entrano nel controllo:
  - una lambda assegnata a un nome di modulo (mutante D: `_aiuto = lambda *a: gestisci_callback(*a)`, chiamata da `testo_da_dire`): T78p PASS;
  - un metodo statico di una classe (mutante H: `_H.f()` che chiama `_handle_update`, chiamato da `testo_da_dire`): T78p PASS;
  - le funzioni di altri moduli, per esempio `parte_parlata` in modules/voice/server.py.

  Servono costrutti fatti apposta, non errori probabili, quindi la riserva è BASSA. Si chiude seguendo anche le assegnazioni di lambda di modulo e i ClassDef, oppure vietando lambda e classi di modulo che contengono nomi vietati.
- **R-725-3 BASSA** (ordine degli avvisi rispetto al messaggio dopo): resta aperta, come dichiarato.

**Cosa non ho verificato**
- Il comportamento dal vivo con Telegram vero (sendVoice e la coda sotto carico reale): non si può riprodurre qui.
- Le elusioni intenzionali via stringhe (`globals()["gestisci_callback"]`, `getattr(modulo, ...)`): una guardia statica per nomi non può coprirle per costruzione.
- La fetta clients/voice/ascolto.py e tests/test_unit_voce_ascolto.py: non cambiata rispetto alla #722, l'ho solo ri-eseguita (dentro i 366 passed).

**Antipattern**: nessuno slicing della history e nessuna simulazione degli strumenti.

È un cambio di sicurezza (la guardia delle firme è stata allargata): il merge lo decide l'operatore.

**Memoria**: riga #727 più una lezione aggiunte in coda a /tmp/claude-0/wt50/.claude/agents/memoria_revisore.md, solo nel working tree, NON committate come richiesto.

### Review #728

## VERDETTO: APPROVATO

Review #728 (chat Mani): merge in staging di mani/telegram4 (aca5b88) su origin/main 524ae96, che contiene la PR #357, nel branch claude/peaceful-lovelace-0w2b7q.

**Cosa ho controllato e con che esito**
- **I file di codice coincidono con aca5b88.** I 5 file nell'index hanno lo stesso blob di aca5b88:
  - modules/telegram/bot.py: 5753741
  - tests/test_unit_kernel.py: 39864e3
  - tests/test_unit_telegram_voce.py: 0f8f4bc
  - clients/voice/ascolto.py: 078de61
  - tests/test_unit_voce_ascolto.py: 1391990

  Per questi 5 file origin/main ha gli stessi blob di 58f088a, e 58f088a è antenato di main. Quindi il diff rispetto a main per il codice è esattamente quello già visto in #722, #725 e #727. I file di M2 (modules/voice/server.py e i test voice_server/sottofondo) restano quelli di main: non compaiono nel diff staged.
- **Memoria.** È l'unione dei due lati: rispetto ad aca5b88 e a main non manca nessuna riga, e non ce n'è nessuna estranea (confronto con comm sulle righe ordinate). Nessun marcatore di conflitto.
- **Stato del merge.** `git ls-files -u` è vuoto, `git diff --cached --check` è pulito e prima della mia riga il working tree era uguale all'index.
- **Test sulla copia dell'index** (checkout-index nello scratchpad, niente stash):
  - telegram_voce + ascolto: 366 passed.
  - Suite del kernel: 1099 PASS, 1 FAIL. L'unico FAIL è T31g (sqlite_vec assente, dipende dall'ambiente); T78p PASS.

**Elementi del diff esaminati**
1. modules/telegram/bot.py:1002 — `_consegna_voce` (pool di un solo thread per la voce, opzione (b)). Rischio: che dopo il merge sia diversa dalla versione revisionata in #727. Esito: ok, il blob è identico ad aca5b88.
2. tests/test_unit_kernel.py:8410 — calcolo di `_consegne78p` nella guardia T78p allargata (cambio di sicurezza). Rischio: che il merge sia andato a toccare la guardia. Esito: ok, il blob è identico e T78p passa sulla copia dell'index.
3. clients/voice/ascolto.py:537 — `t0 = time.monotonic()` prima dell'invio, con la riga di log a clients/voice/ascolto.py:588. Rischio: che il merge abbia perso la parte di #722. Esito: ok, il blob è identico.
4. .claude/agents/memoria_revisore.md — l'unico conflitto, risolto come unione. Rischio: righe perse o marcatori rimasti. Esito: ok (contesto, non conta come citazione).

**Rischi esclusi**
- Non ho verificato di nuovo la logica del thread né la solidità della guardia: è coperta da #725 e #727 e i blob sono identici.
- Non ho verificato il comportamento reale su Telegram/VPS né la CI remota: non si riproducono in dev.
- Restano aperte le riserve BASSE R-727-1 (la guardia T78p non vede lambda di modulo né metodi di classe) e R-725-3 (gli avvisi e il vocale possono arrivare dopo la risposta al messaggio successivo).

**Cambio di sicurezza**: la guardia T78p è allargata, quindi il merge della PR lo decide l'operatore.

**Memoria**
- Ho aggiunto la riga #728 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree e non in index, come richiesto.
- Non ho lanciato `scripts/commit_memoria_revisore.sh`: committerebbe la memoria mentre il merge è ancora in staging, contro la tua indicazione. La riga va committata insieme al merge o subito dopo.

### Review #729

## VERDETTO: APPROVATO CON RISERVE

Review #729 (chat Mani). Ho controllato il diff in staging su claude/peaceful-lovelace-0w2b7q (HEAD f352190, PR #359, cambio di sicurezza). Prima ho letto CLAUDE.md (sez. 5), le voci recenti di reports/stato_progetto.md e la coda della mia memoria (#725, #727, #728).

**Come ho verificato**
- Ho lavorato su una copia dell'index, estratta con checkout-index nello scratchpad. Niente stash.
- `git diff --cached --check` è pulito.
- Per i tre file del diff il working tree coincide con l'index.
- telegram_voce + ascolto: 367 passed.
- Suite kernel: 1099 PASS, 1 FAIL. L'unico FAIL è T31g (manca sqlite_vec, è l'ambiente). T78p è PASS.

**Elementi del diff esaminati**
1. `tests/test_unit_kernel.py:8403`. `_sottomessi78p` registra ogni chiamata `.submit`/`.map` dentro `_consegna_voce` come coppia (metodo, primo argomento). Se il primo argomento non è un nome, registra il suo dump; senza argomenti registra "". Rischio: map o bersagli diversi. Ho provato `submit(fn=_risposta_del_turno)` e un alias della coda (`q = _voce_in_coda; q.submit(_risposta_del_turno, …)`): FAIL entrambi, presi. Esito: **riserva**. La guardia vede solo `submit`/`map` scritti direttamente come `x.submit(...)`. Due forme passano (R-729-1).
2. `tests/test_unit_kernel.py:8444`. `_locali78p` e la allow-list (`_globali_ok78p`, `_attributi_ok78p`, `_import_ok78p`, righe 8450-8466) controllano le funzioni raggiunte da `_invia_risposta_vocale`. Rischio: nomi di modulo che sfuggono alla lista. Ho provato:
   - `import gas`, un import relativo e `__import__("gas")`: FAIL.
   - `global avvisa_firme_scadute` con assegnazione finta, un parametro di default che copre il nome globale, walrus e comprensione: FAIL. Il grafo delle chiamate segue comunque `avvisa_firme_scadute`, che è in bot.py, e la allow-list boccia le funzioni che raggiunge.
   - `_send_text` rifatto a livello di modulo con un wrapper che chiama le firme: FAIL.
   
   Il trucco del `global` copre solo nomi già importati a livello di modulo (sys, subprocess, re, ThreadPoolExecutor…). Con gli attributi ammessi non si arriva a niente di pericoloso, e ThreadPoolExecutor lo prende `_pool78p`. Esito: **ok**. Chiude V-2 e R-727-1 per i nomi dentro bot.py.
3. `modules/telegram/bot.py:1012`. Nuova docstring di `_chiudi_voce`. Ho verificato che `_send_text` usa `_tg_post`, che ha timeout predefinito di 70 s, e che con SIGTERM la Python esce senza passare dall'except. La docstring è coerente. Esito: **ok** (V-4).
4. `tests/test_unit_telegram_voce.py:563`. Nuovo test: Ctrl-C durante la pausa di 5 s dopo un errore. Ho provato due mutanti:
   - `_chiudi_voce()` sostituito con `pass` alla riga 567 di modules/telegram/bot.py: 1 failed.
   - uscita anticipata con `SystemExit`: 1 failed.
   
   Il test non lascia stato globale: `_chiudi_voce` e `gas.GasKernel` sono patchati e ripristinati da monkeypatch. Esito: **ok** (V-3).
5. Citazione di contesto: `modules/telegram/bot.py:1002`. `_consegna_voce` non è soggetta a nessuna allow-list. Da qui nasce R-729-1.

**I mutanti (applicati a modules/telegram/bot.py, poi T78p)**
- FAIL, cioè presi: 12. Sono i 10 elencati sopra (`import gas`, import relativo, `__import__`, `global`, default che copre il nome, walrus, comprensione, rebind di `_send_text`, alias della coda, `submit(fn=...)`) più i due di V-3 sul test.
- PASS, cioè elusioni: 3, riprodotti nella copia.
  - (a) `invia = _voce_in_coda.submit` seguito da `invia(_risposta_del_turno, None, chat_id, finale, None)` in `_consegna_voce`. È proprio il «callable in variabile» che la correzione V-1 dice di escludere, ma con il metodo invece del bersaglio.
  - (b) `getattr(_voce_in_coda, "map")(_risposta_del_turno, …)` in `_consegna_voce`.
  - (c) `submit(_invia_risposta_vocale, base_url, chat_id, globals())` più `finale.get("avvisa_firme_scadute")(None)` nel thread. `get` è un attributo ammesso.

**Riserve**
- **R-729-1 MEDIA**: le elusioni (a) e (b) portano un turno (`_risposta_del_turno`) nel thread della voce senza che T78p lo veda. È la stessa classe di V-1, chiusa solo per la forma `.map(...)` scritta direttamente. Correzione semplice, da fare prima di rimandare al bot o alla verifica esterna:
  - una allow-list dei nomi caricati in `_consegna_voce`: `{ThreadPoolExecutor, _voce_in_coda, _invia_risposta_vocale, base_url, chat_id, finale, Exception, log, type}`. Questa prende `getattr` e `_risposta_del_turno`;
  - ogni `Attribute` su `_voce_in_coda` o su `coda` deve essere il `func` di una Call. Questa prende `invia = _voce_in_coda.submit`.
- **R-729-2 BASSA**: gli argomenti di `submit` dopo il primo non sono vincolati, quindi passa (c). Servono due modifiche volute, ma basterebbe chiedere che gli argomenti siano esattamente i nomi `base_url, chat_id, finale`.
- R-725-3 BASSA resta aperta (avvisi e vocale possono arrivare dopo la risposta successiva).
- CAMBIO DI SICUREZZA: il merge spetta all'operatore.

**Cosa NON ho verificato**
- Il mutante del chiamante «import gas dentro testo_da_dire» l'ho rifatto io (FAIL, `('testo_da_dire', 'import', 'None.gas')`). I suoi sei mutanti invece non li ho rifatti: mi fido del suo risultato, perché i miei ne coprono le stesse classi.
- Il comportamento reale del bot con Telegram ed ElevenLabs veri: in questo ambiente non ci sono token.
- Le funzioni in altri moduli (`parte_parlata` in modules/voice/server.py, `synthesize_speech`): il grafo per scelta non le segue. Resta la parte di R-727-1 sugli altri moduli.

**Memoria**
Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #729 e una lezione: una allow-list a valle va estesa anche alla funzione che consegna al pool. Le ho messe solo nel working tree, non nell'index, come chiesto. Per lo stesso motivo NON ho lanciato `scripts/commit_memoria_revisore.sh`, che la committerebbe: il file va committato da te a fine task.

Script dei mutanti (rilanciabile): /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut.py

### Review #730

## VERDETTO: APPROVATO CON RISERVE

Review #730 (chat Mani): ri-review della #729 sul diff staged (branch claude/peaceful-lovelace-0w2b7q, HEAD f352190, PR #359). È un CAMBIO DI SICUREZZA, quindi il merge lo decide l'operatore.

**Letture fatte prima della review:** CLAUDE.md (sez. 5, 8 e 9), reports/stato_progetto.md (solo le righe su #359, Fetta 4 e T78p), la coda di .claude/agents/memoria_revisore.md (#725–#729 e le lezioni).

**Come ho verificato:** su una copia dell'index fatta con `git checkout-index` in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx730, senza stash.
- Suite kernel: 1099 PASS, 1 FAIL (solo T31g, già noto). T78p è PASS.
- tests/test_unit_telegram_voce.py: 71 passed.
- `git diff --cached --check` è pulito, e su modules/ e tests/ il working tree coincide con l'index.

**Elementi del diff esaminati:**
- `tests/test_unit_kernel.py:8464` — `_consegna_fuori78p` controlla con una allow-list nomi e attributi di `_consegna_voce`. Rischio esaminato: un turno portato nel thread con getattr o con un metodo legato in una variabile (R-729-1). Esito: ok. I mutanti a_alias_metodo, b_getattr_map e submit_var fanno fallire T78p.
- `tests/test_unit_kernel.py:8473` — `_coda_non_chiamata78p` vuole che ogni attributo di `_voce_in_coda`/`coda` sia chiamato direttamente. Rischio esaminato: `invia = _voce_in_coda.submit` usato in un'altra funzione. Esito: ok, il controllo copre tutto il modulo.
- `tests/test_unit_kernel.py:8479` — `_argomenti_submit78p` vuole per submit esattamente gli argomenti `[_invia_risposta_vocale, base_url, chat_id, finale]`, senza keyword. Rischio esaminato: R-729-2, cioè `globals()` passato al thread o `finale=` come keyword. Esito: ok, c_globals e c_kw fanno fallire T78p.
- `tests/test_unit_kernel.py:8444` — `_locali78p` considera locale ogni nome che riceve un assegnamento. Rischio esaminato: un nome dichiarato `global`. Esito: **riserva R-730-1**, sotto.
- `tests/test_unit_kernel.py:8425` (contesto) — `_funzioni78p` e il `next()` di `_f_consegna78p` guardano solo le def di primo livello e solo la prima `_consegna_voce`. Esito: **riserva R-730-2**, sotto.
- `modules/telegram/bot.py:1007` (contesto) — la sola `submit` di `_consegna_voce`. Esito: ok, invariata rispetto alla #729.

**Mutanti:**
- I tuoi 11 di mut2.py, rilanciati da me: tutti T78p FAIL. Per lanciarlo sulla mia copia ho cambiato la riga 2 di /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut2.py: la sorgente ora si passa come secondo argomento. Il file di prima, bot_orig.py, è identico al bot.py dell'index.
- Miei, presi da T78p (FAIL):
  - decoratore su `_consegna_voce`;
  - decoratore su `_invia_risposta_vocale` che restituisce `_risposta_del_turno`;
  - valore di default di un parametro (`_invia_risposta_vocale=_risposta_del_turno`);
  - lambda dentro `_consegna_voce`;
  - `global` con assegnamento morto dentro `testo_da_dire` (lo prende il controllo sulle funzioni chiamate).
- Miei, NON presi da T78p (PASS, cioè elusioni):
  1. Dentro `_consegna_voce`: `global _voce_in_coda, _invia_risposta_vocale, _risposta_del_turno`, poi `if False: _risposta_del_turno = None`, poi `_invia_risposta_vocale = _risposta_del_turno`. Così il thread esegue `_risposta_del_turno`.
  2. Fuori da ogni funzione: `_invia_risposta_vocale = _risposta_del_turno`, `_send_text = _risposta_del_turno`, `globals()['_invia_risposta_vocale'] = ...`.
  3. Una seconda `def _consegna_voce` più sotto, con `getattr(_voce_in_coda, 'submit')(_risposta_del_turno, ...)`.
- Script: /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut730.py e /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut730b.py. Dopo ogni giro ho verificato con cmp che bot.py della copia fosse ripristinato.
- Altri tre mutanti non contano: due decoratori della prima serie bloccavano l'import del modulo e una lambda era scritta male; li ho rifatti sopra (5b, 9b, 7b).

**Riserve:**
- **R-730-1 BASSA** (`tests/test_unit_kernel.py:8444`): `_locali78p` tratta come locale un nome dichiarato `global`. Con un assegnamento morto, qualunque nome globale entra nell'allow-list di `_consegna_voce` e delle funzioni chiamate dal thread. In `_consegna_voce` questo porta un turno nel thread (elusione 1). Correzione semplice: togliere da `_locali78p` i nomi delle istruzioni `ast.Global` e `ast.Nonlocal`. Serve codice scritto apposta, non capita per sbaglio, per questo BASSA.
- **R-730-2 BASSA** (`tests/test_unit_kernel.py:8425`): il codice fuori dalle funzioni non è controllato. Si possono riassegnare i nomi fidati (`_invia_risposta_vocale`, `_send_text`, `log`, …) e ridefinire `_consegna_voce`; il `next()` guarda solo la prima def. Rientra nel limite già dichiarato della guardia statica. Rimedio possibile: vietare fuori dalle funzioni gli assegnamenti ai nomi di `_funzioni78p` e delle allow-list, e accettare una sola def per nome.
- Restano aperte R-725-3 BASSA, R-722-1 COSMETICA e R-722-2 BASSA.

**Rischi esclusi (cosa non ho verificato):**
- Comportamento dal vivo del thread della voce con Telegram reale (sendVoice, tempi): non riproducibile qui.
- Elusioni dinamiche fuori dall'AST del modulo (importlib, `sys.modules`, monkeypatch da altri moduli come modules/voice/server.py): limite dichiarato della guardia statica, non provato.
- Ho girato solo la suite kernel e tests/test_unit_telegram_voce.py; la suite dell'ascolto non l'ho rilanciata, perché il diff #730 tocca solo il test kernel.

**Memoria:** ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree e non nell'index come chiesto, la riga #730 e una lezione: in un'allow-list AST basata sui «locali», togliere sempre i nomi dichiarati `global`/`nonlocal` e controllare le riassegnazioni dei nomi fidati fuori dalle funzioni. Non ho lanciato `scripts/commit_memoria_revisore.sh`, perché committerebbe la memoria contro la tua istruzione; va inclusa a fine task.

### Review #731

## VERDETTO: APPROVATO CON RISERVE

Review #731 (chat Mani). Ri-review della #730 sul diff STAGED (branch claude/peaceful-lovelace-0w2b7q, HEAD f352190, PR #359, cambio di sicurezza). Prima ho letto CLAUDE.md (sez. 5), stato_progetto.md (solo le parti che servono) e la coda della mia memoria (#729, #730).

**Elementi del diff esaminati**
- tests/test_unit_kernel.py:8449 — `_locali78p` ora toglie dai locali i nomi dichiarati global/nonlocal (R-730-1). Rischio: un assegnamento morto rende «locale» un nome globale. Esito: ok, il mutante e1 di mut3.py fallisce come atteso. Riserva R-731-1 (sotto): i «locali» si raccolgono ancora con `ast.walk(f)`, che scende negli scope annidati.
- tests/test_unit_kernel.py:8503 — `_riassegnati78p` controlla rebind e doppie def dei nomi fidati, i `global` diversi da _voce_in_coda/_BOT_USERNAME e le chiamate globals()/vars()/setattr (R-730-2). Rischio: elusioni a livello di modulo. Esito: ok su rebind di funzioni, doppie def, globals()[...] e `type X =`. Riserve R-731-2 e R-731-3 sui builtin e su forme di legame non contate.
- tests/test_unit_kernel.py:8479 — `_fidati78p` = funzioni del modulo + `_globali_ok78p` + i tre nomi della coda. Rischio: un nome fidato che non è legato a modulo (un builtin) passa con un solo legame, perché la regola «c > 1» vale solo per nomi già legati. Esito: riserva (R-731-2).
- modules/telegram/bot.py:1002 (`_consegna_voce`) e modules/telegram/bot.py:1072 (`_invia_risposta_vocale`), file nel diff. Ho controllato che la guardia descriva il codice reale: c'è un solo `submit` con i 4 argomenti esatti, e `isinstance`/`str` sono usati nel thread (modules/telegram/bot.py:1088). Esito: ok.

**Verifica sulla copia dell'index** (checkout-index, niente stash; worktree uguale all'index su modules/ e tests/)
- test_unit_kernel: 1099 PASS, 1 FAIL (solo T31g, già noto); T78p PASS.
- test_unit_telegram_voce: 71 passed.
- `git diff --cached --check`: pulito.

**Mutanti miei** (scratchpad mut4.py e mut5.py, su bot.py della copia; la copia è stata ripristinata e confrontata con cmp)
- FAIL, cioè preso dalla guardia: `type _send_text = int` a livello di modulo.
- PASS, cioè elusioni:
  1. In testo_da_dire: `[0 for exec in ()]` seguito da `exec('...')`. Il bersaglio della comprensione finisce nei «locali» della funzione esterna, ma la comprensione ha uno scope suo: `exec` resta il builtin. Questo apre exec/getattr/__import__ nel thread della voce.
  2. In _consegna_voce: `[0 for getattr in () for _risposta_del_turno in ()]` seguito da `getattr(_voce_in_coda, 'map')(_risposta_del_turno, [chat_id])`. Porta un turno nel thread: è l'effetto di R-729-1 che rientra da un'altra strada.
  3. A livello di modulo: `isinstance = (lambda _o: (lambda *a: _o(*a) if a[0] != 'x' else _risposta_del_turno(*a)))(isinstance)`. Un builtin dell'allow-list riassegnato una sola volta non viene preso.
  4. A livello di modulo: `match _risposta_del_turno:` con `case _send_text: pass`. Il legame passa da MatchAs, che ha un nome-stringa e non un Name Store, quindi non viene contato.
  5. A livello di modulo: `from modules.voice.server import *`. Viene contato come legame di «*», non dei nomi che lega.
- Inconclusivo: il wrapper su `str` rompe altri test (T77r) prima che T78p venga stampato.

**Riserve**
- **R-731-1 MEDIA** — `_locali78p` (tests/test_unit_kernel.py:8444) usa `ast.walk(f)`, che scende in comprensioni, lambda e def annidate: questi hanno uno scope proprio, quindi un nome legato lì risulta «locale» alla funzione esterna anche se non lo è. Così qualunque nome passa l'allow-list, sia nelle funzioni raggiunte dal thread sia in _consegna_voce (elusioni 1 e 2). La classe è la stessa di R-730-1. Correzione: raccogliere i locali solo nello scope della funzione, senza scendere in ListComp/SetComp/DictComp/GeneratorExp/Lambda/FunctionDef/ClassDef annidati. In alternativa, vietare nelle funzioni sotto guardia i bersagli di comprensione che coincidono con un nome globale o builtin.
- **R-731-2 BASSA** — Un builtin dell'allow-list (isinstance, str, len, int, type, bytes, dict, Exception) riassegnato una volta a livello di modulo non viene preso (elusione 3). Correzione: per i nomi fidati non legati nel sorgente atteso, il numero di legami ammesso è 0; oppure confrontare ogni nome con un conteggio di riferimento fisso.
- **R-731-3 BASSA** — I legami a livello di modulo fatti con match-capture (MatchAs/MatchStar/MatchMapping.rest) e con `import *` non vengono contati (elusioni 4 e 5). Correzione: contare anche quei nodi e vietare `import *` nel modulo.

Tutte e tre le elusioni richiedono codice volutamente avversario e visibile in review. Il gate primario resta il revisore; T78p è una rete in più. Per questo sono riserve e non un blocco.

**Cosa non ho verificato**
- getattr/importlib/sys.modules dinamici fuori da bot.py, e il comportamento interno di funzioni di altri moduli (parte_parlata, synthesize_speech): sono limiti dell'analisi statica già dichiarati, non li ho ritestati.
- Gli scope ricavati dall'AST dipendono dalla versione di Python: ho provato solo con Python 3.13.18 della sandbox, non con la versione della CI né del Mac.
- Il comportamento runtime reale del thread della voce su Telegram/VPS non è riproducibile qui.
- Non ho ri-eseguito mut3.py dell'agente: mi fido del suo 16/16 FAIL. Il caso e1 l'ho ricontrollato solo leggendo il codice a :8449.

Wall of Shame: nel diff non c'è slicing della history né simulazione di tool. Nessun guardrail (cap 10 iterazioni, cap 8k, `_get_window`) è toccato.

CAMBIO DI SICUREZZA: il merge lo decide l'operatore.

**Memoria**: ho aggiunto la riga #731 e una lezione in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree e non nell'index, come richiesto. Per questo NON ho lanciato `scripts/commit_memoria_revisore.sh`, che la committerebbe: va committata nel commit di fine task.

File utili: /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/modules/telegram/bot.py, /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut4.py, /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut5.py, /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/k731.txt

### Review #732

## VERDETTO: APPROVATO CON RISERVE

Review #732, chat Mani. È la ri-review della #731 sul diff staged del branch claude/peaceful-lovelace-0w2b7q (HEAD f352190, PR #359). È un CAMBIO DI SICUREZZA, quindi il merge lo decide l'operatore.

Prima della review ho letto CLAUDE.md (sez. 5), la parte di reports/stato_progetto.md sulla PR #359 (riga 683) e la coda della memoria (#728–#731).

**Elementi del diff esaminati**
- `tests/test_unit_kernel.py:8546`: `_ombre78p` raccoglie i legami in tutti gli scope delle funzioni sotto guardia. Contano argomenti anche di lambda, Name Store/Del, def e class annidate, import, match-capture ed except-as. Rischio esaminato: un `[0 for X in ()]` che faccia passare per locale un nome globale. Esito: **ok**, R-731-1 chiusa. Le eccezioni sono limitate a `_voce_in_coda` in `_consegna_voce` e ai nomi di `_import_ok78p`. I mutanti r1 e r2 della #731 ora danno FAIL.
- `tests/test_unit_kernel.py:8521`: nessun builtin si lega a livello di modulo. Rischio esaminato: `isinstance = <wrapper>`. Esito: **ok**, R-731-2 chiusa per i builtin.
- `tests/test_unit_kernel.py:8512`: `_riassegnati78p` conta i legami di modulo, compresi MatchAs/MatchStar/MatchMapping.rest ed ExceptHandler.name, e vieta `import *`. Esito: **ok** per R-731-3. Resta però una **riserva**, R-732-1, descritta sotto.
- `tests/test_unit_kernel.py:8452`: `_globali_ok78p` contiene `parte_parlata`, `synthesize_speech` e `DEFAULT_VOICE_ID`, che oggi sono importati solo dentro le funzioni (`modules/telegram/bot.py:1035` e `modules/telegram/bot.py:1081`). Esito: **riserva** R-732-1.
- `modules/telegram/bot.py:1012`: cambia solo la docstring di `_chiudi_voce`. Esito: **ok**, è invariata dalla #729.
- `tests/test_unit_telegram_voce.py:563`: test V-3 (Ctrl-C durante la pausa). Esito: **ok**, è invariato dalla #729.

**Prove sulla copia dell'index** (checkout-index in scratchpad/idx732, niente stash)
- Kernel: 1099 PASS, 1 FAIL. L'unico FAIL è T31g, già noto. T78p è PASS.
- Test telegram_voce + voce_ascolto: 367 passed.
- `git diff --cached --check` pulito; il working tree coincide con l'index su modules/ e tests/; la copia di bot.py è stata ripristinata e verificata con cmp.

**Mutanti miei** (scratchpad/mut732.py e mut732b.py)
- FAIL (preso): `_URL = _U()` a livello di modulo, dove `_U.sub` esegue un turno. Lo segnala `('lega', '_URL')`.
- PASS, quindi elusioni:
  1. `synthesize_speech = _risposta_del_turno` a livello di modulo, più `synthesize_speech(...)` dentro `_tg_post_file`, che è raggiunta dal thread.
  2. `parte_parlata = lambda t: _risposta_del_turno(None, 0, t)` a livello di modulo, togliendo l'import locale in `testo_da_dire`. Così un turno girerebbe nel thread della voce.
  3. `sys.modules[__name__]._send_text = _risposta_del_turno`.
  4. `_send_text.__code__ = _risposta_del_turno.__code__`.
  5. `_send_text.__globals__['_tg_post'] = _risposta_del_turno`.
  6. `import builtins as _b; _b.len = <wrapper>`.
- Inconclusivi: `from gas import GasKernel as parte_parlata` e `_b.isinstance = lambda *a: True`. Rompono il modulo o la suite prima che T78p venga eseguito.

**Riserve**
- **R-732-1 MEDIA**: i nomi dell'allow-list con 0 legami a livello di modulo (`parte_parlata`, `synthesize_speech`, `DEFAULT_VOICE_ID`) passano con un solo legame, perché `c > 1` scatta solo se il nome era già legato (`tests/test_unit_kernel.py:8512`). È la stessa falla di R-731-2, ma sui nomi importati dentro le funzioni invece che sui builtin. La sintassi è del tutto ordinaria e porta un turno nel thread della voce. Correzione: fissare per ogni nome fidato il numero esatto di legami atteso a livello di modulo (0 per questi tre), non «al massimo 1».
- **R-732-2 BASSA**: a livello di modulo non sono controllate le scritture su attributo o subscript: `sys.modules[__name__].x = …`, `f.__code__ = …`, `f.__globals__[…] = …`, `builtins.x = …`. Il limite già dichiarato riguarda sys.modules e getattr dinamici «fuori da bot.py», mentre questi stanno in bot.py. Correzione suggerita: vietare a livello di modulo ogni assegnamento con bersaglio Attribute o Subscript, oppure almeno ogni menzione di `__code__`, `__globals__`, `sys.modules` e `builtins`.

**Rischio escluso**: non ho verificato il comportamento dal vivo del thread della voce (Telegram ed ElevenLabs reali), perché non è riproducibile qui senza token. Restano anche i limiti statici già dichiarati: getattr, importlib e sys.modules dinamici negli altri moduli, e le funzioni di altri moduli (modules.voice.*) chiamate dal thread.

**Memoria**: ho aggiunto la riga #732 e una lezione in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree. Non l'ho messa in index e non ho lanciato scripts/commit_memoria_revisore.sh, perché la tua istruzione «NON in index» è in conflitto con il commit atomico previsto dal protocollo: il commit resta a te, a fine task. L'index contiene ancora solo bot.py, test_unit_kernel.py e test_unit_telegram_voce.py.

File utili:
- /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut732.py
- /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/mut732b.py
- /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx732

### Review #733

## VERDETTO: APPROVATO CON RISERVE

Review #733 (chat Mani). È la ri-review della #732 sul diff staged del branch claude/peaceful-lovelace-0w2b7q (HEAD f352190, PR #359). Si tratta di un cambio di sicurezza: il merge lo decide l'operatore.

Ho letto CLAUDE.md (sez. 5), stato_progetto.md solo nelle parti che servono e la coda della memoria (#729–#732). Non ho trovato antipattern del Wall of Shame: il diff tocca solo una guardia statica nei test, senza slicing della history e senza simulare tool.

**Come ho verificato**
- Ho lavorato su una copia dell'index (checkout-index, niente stash): /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx733
- `git diff --cached --check` è pulito. Su modules/ e tests/ il working tree coincide con l'index.
- Suite kernel: 1099 PASS e 1 FAIL, solo T31g (il FAIL già noto). T78p è PASS.
- tests/test_unit_telegram_voce.py: 71 passed.

**Elementi del diff esaminati**
- tests/test_unit_kernel.py:8483 — definisce `_legati_una_volta78p`, l'insieme dei nomi che a livello di modulo devono avere esattamente 1 legame. Rischio: un nome fidato lasciato fuori, o uno messo dentro per errore. L'ho confrontato con il modulo: ci sono `log` (modules/telegram/bot.py:41), i due timeout (bot.py:60 e :63), `_voce_in_coda` (bot.py:999), `_MARKDOWN` e `_URL` (bot.py:1026-1028). I builtin, `parte_parlata`, `synthesize_speech` e `DEFAULT_VOICE_ID` cadono nel ramo «0 legami». Esito: ok.
- tests/test_unit_kernel.py:8526 — controllo del numero ESATTO di legami (1 oppure 0) per ogni nome fidato che non è una funzione. Rischio: che lasci passare un legame singolo di un nome che oggi ne ha 0, cioè l'elusione R-732-1. I mutanti s1 e s2 della #732 ora danno FAIL, come provato dall'agente. Il conteggio dei pacchetti (`import urllib.error` + `import urllib.request` contati una volta sola) è coerente. Esito: ok. R-732-1 chiusa.
- tests/test_unit_kernel.py:8530 — vieta, fuori dalle funzioni, gli store su Attribute e Subscript (Assign, AugAssign, AnnAssign, Delete). Rischio: falsi positivi sul codice di modulo esistente, ed elusioni con chiamate invece che con store. Falsi positivi nessuno (T78p PASS). Elusioni: vedi R-733-1. Esito: riserva BASSA.
- tests/test_unit_kernel.py:8535-8545 — vieta in tutto il modulo `__code__`, `__globals__` e gli altri interni delle funzioni, `sys.modules`, l'import di builtins/importlib e i nomi `__builtins__`, `__import__`, `exec`, `eval`, `compile`. Rischio: alias. Il controllo guarda solo il nome letterale `sys`, quindi `import sys as _s` passa. Esito: riserva BASSA (R-733-1).
- modules/telegram/bot.py:1028 (contesto, file nel diff) — `_URL = re.compile(...)` è un legame unico a modulo. Rischio: la guardia conta i legami ma non controlla il valore. Esito: riserva BASSA (R-733-2).

**Mutanti miei**
Script: /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/m733/mut.py — 12 mutanti, ciascuno su una copia separata.
- 1 dà T78p FAIL: `setattr(_me, '_send_text', …)` su un auto-import dentro una funzione. Lo blocca il controllo su globals()/setattr.
- 9 danno T78p PASS (elusioni):
  - m1: `import sys as _s` + `_s.modules[__name__]._send_text = _risposta_del_turno` dentro una funzione chiamata a modulo
  - m2: `from sys import modules` + `modules[__name__]._send_text = …` dentro una funzione
  - m3: `getattr(sys, 'modules')[__name__].__setattr__('_send_text', …)` a modulo
  - m4: `locals().update(_send_text=…)` a modulo (a livello di modulo locals() è globals())
  - m5: `_g = globals` + `_g().update(…)`
  - m6: `import modules.telegram.bot as _me` + `_me._send_text = …` dentro una funzione
  - m7: auto-import + `_me.__setattr__('_send_text', …)` a modulo
  - m12: `_patch.__getattribute__('__glob' + 'als__')[...] = …`
  - m8: `_URL = _UrlFinto()`, una classe il cui `sub` fa un turno: un solo legame, ma con un valore ostile
- 2 non concludono: m9 (`_URL` costruito da una funzione) e m10 (handler di logging che fa un turno) rompono l'import del modulo prima di T78p, quindi non sono significativi.

**Come li ho classificati (rispetto alla tua nota)**
Tutte e nove le elusioni sono BASSE. Ognuna richiede di riassegnare deliberatamente una funzione del modulo stesso tramite le sue parti interne: aliasare `sys` per arrivare a `sys.modules`, auto-importare il modulo, usare `locals()`/`globals` come dizionario, chiamare `__setattr__`/`__getattribute__` con stringhe composte, oppure scrivere una classe finta il cui metodo avvia un turno. Nessuna di queste può nascere per caso in un refactor, e in review si vede. Non ho trovato elusioni con sintassi ordinaria: nessuna MEDIA.

**Riserve**
- R-733-1 BASSA: il modulo può ancora riscrivere le proprie funzioni tramite alias di `sys` o `from sys import modules`, auto-import del modulo, `locals()` a modulo, alias di `globals`, oppure `__setattr__`/`__getattribute__` con stringhe. Il divieto su `sys.modules` (tests/test_unit_kernel.py:8538-8540) guarda solo il nome letterale `sys`. Il divieto sugli store (tests/test_unit_kernel.py:8530) vale solo fuori dalle funzioni e solo per gli store, non per le chiamate. È un limite di una guardia statica che l'operatore può accettare: consiglio di non inseguirlo oltre.
- R-733-2 BASSA: il VALORE dei nomi legati una volta (`_URL`, `_MARKDOWN`, `log`, i timeout) non è vincolato. Un solo legame a un oggetto ostile passa (m8). Anche qui serve codice chiaramente voluto.

**Rischi esplicitamente esclusi**
- Il monkeypatch da ALTRI moduli (gas.py, test, plugin che fanno `bot._send_text = …`) è fuori dal perimetro: la guardia analizza solo modules/telegram/bot.py. Con un grep su gas.py, modules/ e brains/ non ho trovato assegnamenti del genere, ma non è una prova dinamica.
- Comportamento a runtime su VPS/Telegram reale non verificato: non è riproducibile in dev, e il diff tocca solo la guardia statica nei test.
- Il caso `except … as` resta inconclusivo, come già detto nella #732. Non l'ho ripreso.

**Memoria**
Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #733 e una lezione nuova, solo nel working tree e NON nell'index. Come mi hai chiesto, non ho eseguito scripts/commit_memoria_revisore.sh, che invece le istruzioni del revisore prevederebbero subito dopo la riga contatore. L'index contiene ancora solo modules/telegram/bot.py, tests/test_unit_kernel.py e tests/test_unit_telegram_voce.py.

### Review #735

## VERDETTO: APPROVATO

Review #735 (chat Mani). Ho controllato il merge staged di origin/main 567beb7 (dentro c'è la PR #358, server voce R8 di M2) nel branch claude/peaceful-lovelace-0w2b7q (HEAD 5801c12, PR #359). Ho letto CLAUDE.md sez. 5, la parte di stato_progetto toccata dal merge e la coda della memoria.

**Il merge è integro**
- File di main: nell'index hanno lo stesso blob di 567beb7. Sono modules/voice/server.py (288f456), tests/test_unit_voice_server.py (259a69d), reports/proposta_voce_sicura.md (c432268) e reports/ripartenza_m2.md (c1d9956).
- File di Mani: nell'index hanno lo stesso blob di HEAD (e diverso da main). Sono modules/telegram/bot.py, tests/test_unit_kernel.py, tests/test_unit_telegram_voce.py, clients/voice/ascolto.py e tests/test_unit_voce_ascolto.py.
- reports/handoff.md, ultimo_report.md e diff_sessione.md sono presi da HEAD. ultimo_report e diff_sessione sono già modificati nel working tree, non in index: è la tua riscrittura di fine task.
- reports/stato_progetto.md, unito in automatico: aggiunge solo la riga «Server voce più sicuro, R8 fetta 1» di M2. Nessun marcatore di conflitto.
- `.claude/agents/memoria_revisore.md` è l'unione dei due lati:
  - mancano 0 righe di HEAD e 0 righe di main;
  - l'unica riga «in più» è vuota;
  - nessun marcatore;
  - prima della mia aggiunta il working tree era uguale all'index.
- `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.

**Elementi del diff esaminati**
- modules/voice/server.py:347 — `parte_parlata`, la funzione della allow-list T78p che il thread della voce Telegram chiama. Rischio: che la #358 ne cambi il comportamento. Ho confrontato l'albero AST tra la base 524ae96 e 567beb7: è identico. Identiche anche `cervello_voce` (modules/voice/server.py:452), `istruzione_turno_voce` e `_USO_FORTE_PARLATO`, che bot.py importa (modules/telegram/bot.py:969, :984, :1035). Esito: ok.
- modules/voice/server.py:407 — `_bind_locale`, con `_env_acceso` a modules/voice/server.py:442: funzioni nuove della #358, a livello di modulo e solo per l'avvio del server. Rischio: che aggiungano un import o un nome che la guardia T78p dovrebbe autorizzare. Non entrano nel grafo delle chiamate raggiunte da `_invia_risposta_vocale`, e T78p resta PASS. Esito: ok.
- modules/voice/server.py:593 — `_autorizza`, con lo sfratto a tabella piena (R8, già revisionato in #734-M2). Rischio: che il merge abbia alterato il codice revisionato. Il blob è identico a 567beb7. Esito: ok.
- tests/test_unit_kernel.py:8454 — la allow-list T78p contiene `parte_parlata`, e a tests/test_unit_kernel.py:8459 l'import fidato `("modules.voice.server", "parte_parlata")`. Rischio: allow-list rimasta senza effetto dopo il merge. Il file è quello di HEAD e il test passa sulla copia dell'index. Esito: ok.

**Prove sulla copia dell'index** (checkout-index in una cartella temporanea, niente stash, cartella poi cancellata)
- tests/test_unit_telegram_voce.py, tests/test_unit_voce_ascolto.py e tests/test_unit_voice_server.py: **550 passed**.
- tests/test_unit_kernel.py: **1099 PASS / 1 FAIL**. L'unico FAIL è T31g (GAS_VECTORS, dipende dall'ambiente, atteso).
- T78p («update gestiti uno alla volta…»): **PASS**.

**Cosa NON ho verificato**
- Non ho rifatto la review di merito sulla sicurezza della #358 (tetti per IP, bind, controllo dell'Host): l'ha già fatta M2 in #720–#734-M2 e il blob è identico. Ho controllato solo l'integrità del merge e l'interazione con il thread della voce.
- Non ho verificato il comportamento reale sul Mac né sul VPS (server voce vivo, client): non è riproducibile qui.
- La venv del repo non esiste: le prove girano con il python3 di sistema.

**Riserve e note**
- Nessuna riserva nuova.
- Restano aperte quelle già tracciate per la #359: R-733-1 e R-733-2, entrambe BASSE.
- Restano aperte quelle di M2 per la #358, elencate nella riga dello stato.
- È un cambio di sicurezza: il merge lo decide l'operatore.

**Memoria**
- Ho aggiunto in coda la riga #735, solo nel working tree e non in index (come richiesto), in /home/user/Gas/.claude/agents/memoria_revisore.md. Nessuna lezione nuova.
- Non ho lanciato scripts/commit_memoria_revisore.sh perché il merge è in corso e la riga doveva restare fuori dall'index.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: da 66 a 71 casi. `tests/test_unit_voce_ascolto.py`: +1 caso. Sull'albero del merge:

```
550 passed in 295.24s (0:04:55)
```

(telegram_voce + voce_ascolto + voice_server). `python tests/test_unit_kernel.py`: 1099 PASS, 1 FAIL. Il FAIL è T31g: manca `sqlite_vec` nell'ambiente, ed era già presente sulla base. T78p è PASS.

Mutanti della guardia T78p: 27 presi su 28, script `mut5m.py` nello scratchpad. Presi tutti quelli di bot, verifica esterna e review #725–#732. Uno è inconclusivo: `except … as _send_text` rompe il modulo prima del test.

## §6 STATO CI

`gh` non è stato usato: GitHub passa dallo strumento MCP. Su f352190 la PR #359 aveva unit-suite success, handoff-check success e verifica-bot failure (V-1 MEDIA, ora corretta). Per fff8f3b, 5801c12, 4e57b58 e per il commit di fine-task che contiene questo file la run non era ancora disponibile alla scrittura dell'handoff; nessuna run sui primi tre, che non sono mai stati pushati da soli.

## §7 RISERVE APERTE

- R-733-1 BASSA: il modulo può ancora riscrivere le sue funzioni con codice voluto. Esempi: alias di sys o `from sys import modules`, auto-import, `locals()`, alias di globals, `__setattr__` con stringhe.
- R-733-2 BASSA: il VALORE dei nomi legati una volta (`_URL`, `log`…) non è vincolato.
- R-725-3 BASSA: avvisi e vocale possono arrivare dopo la risposta al messaggio successivo.
- R-722-1 COSMETICA, R-722-2 BASSA (tempi della voce di casa).
- Bot #357: V-1 BASSA (corsivo con un solo * letto a voce), V-2 COSMETICA.
- R-717-3 BASSA (MP3 su sendVoice da provare dal vivo), R-721-2 BASSA.
- Le altre riserve sono in `reports/stato_progetto.md`.
