# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — chat Mani: voce via Telegram, fetta 4 (voce consegnata in un thread, opzione b) + tempi della voce di casa

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #359 (https://github.com/Gasss23/Gas/pull/359): CAMBIO DI SICUREZZA (guardia T78p delle firme allargata, opzione b). Serve il sì esplicito dell'operatore, anche con verdetto pulito del bot. Consigliato il secondo passaggio nella chat claude.ai col link della PR.

---

## §1 SCOPE & ESITO FETTE

- **PR #357 (fetta 3)**: `FATTA` — mergiata (524ae96) col sì dell'operatore via M1.
- **Voce consegnata in un thread (opzione b)**: `FATTA` — review #725, corretta e ri-revisionata in #727. Cambio di sicurezza: merge all'operatore.
- **Tempi della voce di casa (misura fino alla prima frase)**: `FATTA` — review #722.
- **Merge su main dopo la #357**: `FATTA` — review #728 APPROVATO.
- **R-727-1 e R-725-3 (BASSE)**: `DEFERITA — tracciate in stato_progetto.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 clients/voice/ascolto.py           |   7 +++++++
 modules/telegram/bot.py            |  44 ++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  13 ++++++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  27 ++++++++++++++------------
 tests/test_unit_kernel.py          |  52 +++++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_telegram_voce.py   |  64 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py    |  15 ++++++++++++++
```

NB: la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale (regola «n/d» dell'operatore, 2026-10-24).

## §3 GIT LOG --ONELINE (sessione)

```
62cb860 Merge mani/telegram4: voce Telegram in un thread a parte (opzione b) — review #728
aca5b88 feat(telegram): voce consegnata in un thread a parte, guardia T78p irrobustita (opzione b) — review #725/#727
3404378 feat(voce): tempo fino alla prima frase di Gas nel log dell'ascolto (misura della velocità) — review #722
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit aca5b88 (fetta 4) e 3404378 (tempi della voce di casa, unito in mani/telegram4): review #722, #725, #727. Merge 62cb860: review #728. Verdetti integrali:

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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: da 66 a 70 casi. `tests/test_unit_voce_ascolto.py`: +1 caso (296).

```
366 passed in 23.70s
```

`python tests/test_unit_kernel.py` sull'albero della fetta: 1099 PASS, 1 FAIL. Il FAIL è T31g: manca `sqlite_vec` nell'ambiente, fallisce anche sulla base. T78p è PASS. Mutanti della guardia T78p presi: A, B, C (#725), E, F, G (#727); non presi D, H (R-727-1).

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Per 3404378, aca5b88, 62cb860 e per il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (nessuna run su 3404378 e aca5b88, mai pushati da soli). La PR #357 su 55dfa82 aveva unit-suite, handoff-check e verifica-bot success ed è stata mergiata (524ae96).

## §7 RISERVE APERTE

- R-727-1 BASSA: la guardia T78p non vede lambda assegnate a nomi di modulo né metodi di classe.
- R-725-3 BASSA: avvisi e vocale possono arrivare dopo la risposta al messaggio successivo.
- R-722-1 COSMETICA, R-722-2 BASSA: il test dei tempi dipende dall'ordine delle chiamate; la misura è fino al primo pezzo pronto, non al suono.
- Bot #357: V-1 BASSA (corsivo con un solo * letto a voce), V-2 COSMETICA (link markdown).
- R-717-3 BASSA (MP3 su sendVoice da provare dal vivo), R-721-2 BASSA.
- Le altre riserve sono in `reports/stato_progetto.md`.
