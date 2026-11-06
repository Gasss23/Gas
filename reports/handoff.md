# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5180114384","url":"https://github.com/Gasss23/Gas/pull/339"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10. Sì dell'operatore già dato via M1: CI verde e bot + verifica esterna senza ALTA/MEDIA sul nuovo head.
2. Punto 1 (V-1 a del bot su a87d273, MEDIA): scrivere o no nella storia vera i turni di seguito giudicati «per Gas». Cambia la scelta A: chiesto all'operatore via M1, NON fatto in attesa della risposta.

---

## §1 SCOPE & ESITO FETTE

- **Pausa a voce** (contratto rivisto dall'operatore via M1): `FATTA`.
- **Turni di seguito** (`X-Gas-Seguito: 1`, solo cervello forte, «[NON_PER_ME]» → `X-Gas-Comando: fine`): `FATTA`.
- **V-2 bot #335** (conferma: timeout 5 s, errore in cache 60 s) e R-669-1-M2 per la conferma: `FATTA`.
- **V-1 bot #335** («Jarvis Gas» dichiarato con un test): `FATTA`.
- **V-1/V-2 verifica esterna su b0405dc**: `FATTA` (review #676-M2).
- **Storia senza turni «non per me» e nessuno strumento nel seguito** (MEDIA del bot): `FATTA` — scelta A, `run_turn(effimero=True)` in gas.py (review #677-M2 + bis).
- **R-676-3** (review di Mani): `FATTA` — trascrizione incerta o vuota nel seguito → fine.
- **V-2 verifica esterna su a87d273** (il seguito non sapeva di non avere strumenti): `FATTA` — 10dc900, review #678-M2.
- **Merge di main** (#338/#340 della chat Mani) e `**kw` nel finto del test di Mani (autorizzato da M1): `FATTA` — fd1b320, review #679-M2.
- **V-1 (b) bot su a87d273** (strumento chiesto nel seguito → silenzio): `FATTA` — frase fissa «Per farlo ripetimelo dicendo prima Hey Jarvis.», 4ee1feb, review #680-M2.
- **V-1 (a) bot su a87d273** (i seguiti veri non entrano nella storia): `IN ATTESA della decisione dell'operatore`.
- **C1**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  12 ++++++++++++
 gas.py                              |  51 ++++++++++++++++++++++++++++++++++++++++++---------
 modules/voice/server.py             | 145 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------
 modules/voice/tts.py                |   4 +++-
 reports/diff_sessione.md            |  20 ++++++++++++--------
 reports/handoff.md                  | n/d
 reports/ripartenza_m2.md            |   9 +++++----
 reports/stato_progetto.md           |   3 ++-
 reports/ultimo_report.md            |  34 +++++++++++++++++++---------------
 tests/test_unit_kernel.py           | 110 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py     |   5 +++--
 tests/test_unit_voice_prova_voci.py |  34 ++++++++++++++++++++++++++++++++--
 tests/test_unit_voice_stt.py        | 222 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: origin/main 83f3bcd.

## §3 GIT LOG --ONELINE (sessione)

```
4ee1feb feat(kernel+voce): V15 — nel seguito uno strumento chiesto fa dire «ripetimelo con Hey Jarvis» invece del silenzio (V-1 b bot #339, sì di M1) (chat M2)
4899032 chore(revisore): memoria review #680 — APPROVATO CON RISERVE
fd1b320 Merge origin/main (PR #338 e #340 della chat Mani) nella PR #339 — test di Mani col **kw autorizzato da M1, review #679-M2
10dc900 fix(voce): V15 — il seguito sa di non avere strumenti (V-2 ve #339 su a87d273, chat M2)
2530577 chore(revisore): memoria review #678 — APPROVATO CON RISERVE
a87d273 docs(voce): report di fine task V15 col turno effimero (PR #339, chat M2)
fd64e77 feat(kernel+voce): V15 — turno effimero per i turni di seguito (scelta A dell'operatore, R-675-1-M2) (chat M2)
aa1babe chore(revisore): memoria review #677 — APPROVATO
bad216f chore(revisore): memoria review #677 — APPROVATO CON RISERVE
3581f6f docs(voce): report di fine task V15 dopo V-1/V-2 della verifica esterna (PR #339, chat M2)
bb731b2 fix(voce): V15 — seguito: «forte» dalla stanza chiude senza voce, segno [NON_PER_ME] anche come prefisso (V-1/V-2 ve #339, chat M2)
061334c chore(revisore): memoria review #676 — APPROVATO CON RISERVE
b0405dc docs(voce): report di fine task V15 (PR #339, chat M2)
5cf7267 feat(voce): V15 — pausa a voce, turni di seguito decisi dal cervello forte, conferma che non blocca (chat M2)
2d2d432 chore(revisore): memoria review #675 — APPROVATO CON RISERVE
8c9bc1b chore(revisore): memoria review #675 — APPROVATO CON RISERVE
04532a3 chore(revisore): memoria review #675 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. Il merge fd1b320 porta anche i commit di main (#338, #340) che non sono di questa sessione e non sono elencati.

## §4 VERDETTO DEL REVISORE (per commit motore)

La prima emissione #675-M2 riguardava una versione dello stage poi sostituita (contratto della pausa cambiato): non è stata riportata dall'agente revisore se non come premessa della bis, che la dichiara superata.

Review #675-M2 bis sul diff staged (contratto rivisto; sostituisce la prima emissione #675-M2 sulla versione precedente dello stage), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #675-M2 (bis). Ho guardato il `git diff --cached` attuale, quello con il contratto rivisto: pausa con «basta (così)» e risposta «Va bene.», poi X-Gas-Seguito con [NON_PER_ME], poi la conferma con la cache degli errori. Lo stage è cambiato mentre la review era in corso. La prima versione (pausa/standby con «Va bene, mi metto in pausa.») l'avevo già esaminata e giudicata APPROVATO CON RISERVE, ma non vale più: la sostituisce questo verdetto. I test li ho lanciati sull'albero staged esportato (`git checkout-index` in /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/staged675b), non sulla cartella di lavoro: `tests/test_unit_voice_stt.py` + `tests/test_unit_voice_prova_voci.py` danno 155 passed. Sulla versione precedente dello stage la suite voce (`-k voice`) dava 304 passed.

Elementi esaminati (righe dello stage attuale):
- modules/voice/server.py:130 — regex `_SOLO_PAUSA` ancorata con ^…$ — falsi positivi e backtracking — ok. Vanno al cervello, cioè nella direzione sicura: «pausa caffè», «in pausa», «metti in pausa la musica», «basta il sale», «basta, grazie», «pausa per favore», «forte pausa». Una stringa da 350k caratteri si chiude in 0,02 s. Unico caso dubbio: «basta così?» detto come domanda chiude la conversazione (R-675-4-M2).
- modules/voice/server.py:509 — controllo della pausa solo nel ramo audio, prima di «Dimmi.» e prima di `cervello_voce` — forte e formati — ok. Passa da `_rispondi_senza_turno`, quindi funziona in ogni formato. A testo «pausa» resta una richiesta normale (test a tests/test_unit_voice_stt.py:768). «forte, pausa» va al cervello forte (R-675-4-M2).
- modules/voice/server.py:446 — override di `end_headers` che aggiunge X-Gas-Comando — comando rimasto da una richiesta precedente — ok. `_comando` si azzera in do_POST e do_GET. Il server è HTTP/1.0 senza keep-alive, quindi ogni connessione ha un'istanza nuova. Vale per JSON, MP3 e NDJSON.
- modules/voice/server.py:559 — `ISTRUZIONE_SEGUITO` aggiunta all'istruzione del turno se `_seguito()` (modules/voice/server.py:623) — privacy — **riserva MEDIA**, vedi R-675-1-M2.
- modules/voice/server.py:587 — `SEGNO_NON_PER_ME in result_content` → JSON {"content":"","fine":true} con X-Gas-Comando: fine — esce prima di ogni sintesi o streaming? — ok, ElevenLabs non viene chiamato. Il segno però è cercato come sottostringa (R-675-3-M2). Nel formato audio+pezzi il client riceve JSON e non NDJSON: va confermato lato Mani.
- modules/voice/server.py:870 e modules/voice/server.py:881 — cache negativa di 60 s per (voce, frase), timeout di 5 s, `http.client.HTTPException` intercettata — il server a un thread si blocca? — ok. Un successo azzera l'errore; con un'altra voce non resta bloccato (test a tests/test_unit_voice_prova_voci.py:737). modules/voice/tts.py:84 — nuovo parametro `timeout` con default invariato di 30 s — ok.

Riserve:
- **R-675-1-M2 MEDIA (privacy, decide l'operatore)**: il seguito manda al cervello il parlato di terzi (stanza, TV, telefonate). Con `GAS_VOCE_FORTE` spento lo manda ai modelli gratuiti, contro la regola dei modelli di CLAUDE.md §2 (ai gratuiti niente dati personali). Gli strumenti restano attivi: se il cervello sbaglia a giudicare, agisce su parlato ambientale. Inoltre run_turn salva il parlato nella storia condivisa. Proposta: turni di seguito solo col cervello forte, fail-closed se non è disponibile, e turni [NON_PER_ME] non salvati (fetta «profilo voce» in gas.py).
- **R-675-2-M2 BASSA**: oltre il tetto orario il 429 arriva prima della trascrizione, quindi «pausa» non si può dire proprio quando il client continua a mandare richieste. Anche i turni di seguito ambientali consumano il tetto.
- **R-675-3-M2 BASSA**: il segno è cercato come sottostringa. Le varianti senza parentesi («NON_PER_ME», «Non per me») non vengono riconosciute e quindi vengono lette ad alta voce.
- **R-675-4-M2 COSMETICA**: «basta così?» e «Pausa?» detti come domanda chiudono la conversazione; «forte, pausa» va al cervello forte.
- Nota: il controllo `self._parlato` in `_seguito()` è ridondante con `is_audio`, quindi il mutante sopravvive. È una difesa voluta: accettabile.

Cosa NON ho verificato: il comportamento reale del client H24 (riprendi.sh, gestione di «fine» e del JSON in formato pezzi), perché è lato Mani e non è nel repo di questa fetta. Non ho verificato nemmeno quanto bene un LLM reale distingue il parlato rivolto a Gas: non si riproduce senza cervello reale, i test usano un kernel finto.

Attenzione per il gate: le righe citate valgono per lo stage attuale (211 righe aggiunte). Se lo stage cambia ancora prima del commit, serve una nuova review.

Memoria: righe #675-M2 e #675-M2 bis, più due lezioni, in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit 04532a3 e 8c9bc1b).

Review #675-M2 ter sullo stage finale del commit 5cf7267 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #675-M2 ter: solo l'aggiunta che chiude R-675-1-M2 (parte server) e R-675-3-M2, sul `git diff --cached` attuale. I test li ho lanciati sull'albero staged esportato (/tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/staged675c): `tests/test_unit_voice_stt.py` + `tests/test_unit_voice_prova_voci.py` danno 155 passed.

Cosa ho controllato:
- modules/voice/server.py:567 — nel ramo `_seguito()` il turno va solo al cervello forte (`kw["cervello"] = "forte"`). Rischio controllato: che passi lo stesso ai gratuiti. Esito: ok. In gas.py:923 (contesto, file non toccato) la catena «forte» contiene solo claude-cli: se il forte non c'è, il turno non scende ai gratuiti. I test verificano il forte col seguito (tests/test_unit_voice_stt.py:747) e nessun campo `cervello` senza seguito (tests/test_unit_voice_stt.py:763). **R-675-1-M2 parte server: chiusa.**
- modules/voice/server.py:143 — nuova regex `_NON_PER_ME` (`^\W*non[_\s]+per[_\s]+me\W*$`, maiuscole e minuscole uguali), usata in modules/voice/server.py:594. Rischio controllato: risposte vere scambiate per il segno, e lentezza su testi lunghi. Esito: ok.
  - Riconosciute: «[NON_PER_ME]», «NON_PER_ME», «Non per me.», ««[NON_PER_ME]»».
  - Restano risposte normali: «Non per me è un problema, lo faccio subito.», «[NON_PER_ME] Ciao», «Non è per me.».
  - Nessun rallentamento: 200k caratteri in meno di 1 ms. **R-675-3-M2: chiusa.**

Riserve:
- **R-675-1-M2, parte storia: resta APERTA (MEDIA)**. I turni [NON_PER_ME] finiscono comunque nella storia condivisa scritta da gas.py. Va fatta nella fetta «profilo voce», che spetta all'operatore.
- **R-675-5-M2 BASSA (nuova)**. Due effetti da dire all'operatore:
  1. Con il forte dormiente (`GAS_CLAUDE_CLI` spento) ogni turno di seguito risponde 500 senza X-Gas-Comando. La finestra di conversazione non funziona finché il forte non è acceso, e il client (lato Mani) deve chiudere la conversazione anche su un errore.
  2. Con il forte acceso, ogni frase captata nella finestra (anche TV o persone che parlano fra loro) spende il budget giornaliero del forte.
- Restano come prima R-675-2-M2 (tetto orario) e R-675-4-M2 (frasi in forma di domanda).

Cosa NON ho verificato: un turno reale col forte (claude-cli) acceso. Non si riproduce in questo ambiente: i test usano un kernel finto, quindi ho verificato solo che il server chiede il forte, non come risponde davvero.

Memoria: riga #675-M2 ter in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con scripts/commit_memoria_revisore.sh (commit 2d2d432).

Review #676-M2 sul commit bb731b2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #676-M2. Ho esaminato il diff staged (2 file, +34/-4) sul branch feat/voce-v12-m2. Nel worktree non ci sono modifiche fuori dallo stage (stato «M » su entrambi i file). I test li ho comunque lanciati sull'albero staged esportato in /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/st676: voice_stt + voice_prova_voci danno **156 passed**.

**Cosa ho controllato nel diff:**
- `modules/voice/server.py:538` — nel ramo `cervello == "uso"`, se il turno è un seguito (`_seguito()`), ora chiama `_chiudi_seguito()` invece di pronunciare `_USO_FORTE_PARLATO`.
  - Rischio esaminato: che un vero «forte» detto dall'operatore nel seguito venga perso.
  - Effetto: la conversazione si chiude in silenzio. È lo stesso trattamento del parlato non rivolto a Gas e va nella direzione della privacy della stanza.
  - `_seguito()` vale solo per il parlato. Il ramo testo (400) e il parlato fuori dal seguito restano invariati.
  - Esito: **ok**.
- `modules/voice/server.py:633` — il nuovo helper `_chiudi_seguito()` imposta `_comando = COMANDO_FINE` e risponde `{"content": "", "fine": True}`.
  - Rischio esaminato: che `_comando` resti appeso alla richiesta successiva.
  - Si azzera dopo l'invio degli header (`modules/voice/server.py:459`) e in `modules/voice/server.py:834`.
  - È riusato in modo identico nel ramo [NON_PER_ME] (`modules/voice/server.py:601`), quindi il comportamento non cambia.
  - Esito: **ok**.
- `modules/voice/server.py:145` — nuova regex `_NON_PER_ME`. L'ho provata a mano:
  - «[NON_PER_ME] x», ««[non_per_me]» la TV» e «[NON_PER_ME]x» vengono riconosciuti.
  - «Non per me è un problema», «Il segno [NON_PER_ME]» (segno non in testa) e «[non_per_me_ok] ciao» no.
  - Falsi positivi: una risposta vera che comincia col segno esatto fra parentesi non è plausibile. «[non_per_me_ok]» non scatta perché la regex vuole la `]` subito dopo.
  - Esito: **riserva** (vedi R-676-1-M2).
- `tests/test_unit_voice_stt.py:743` — il test del segno ora ha anche due varianti col prefisso (`tests/test_unit_voice_stt.py:750` è il nuovo `test_v15_seguito_forte_dalla_stanza_non_parla`).
  - Con trascrizione «Forte!» e X-Gas-Seguito: 1, verifica status 200, `X-Gas-Comando: fine`, content vuoto e che il kernel non venga chiamato (`kw == "NESSUN TURNO"`).
  - Il test usa l'HTTP vero, senza simulare output di tool.
  - Esito: **ok**.

**Riserve:**
- **R-676-1-M2 (BASSA):** solo la forma esatta con parentesi e underscore vale come prefisso. Con una coda dopo il segno, «[NON PER ME] (fra persone)» e «NON_PER_ME (fra persone)» non vengono riconosciuti e quel testo verrebbe letto ad alta voce. Il caso è residuale (il prompt chiede il segno esatto). Si può chiudere estendendo il prefisso a `\[non[_\s]+per[_\s]+me\]`, oppure tracciarlo in stato_progetto.md.

**Cosa NON ho verificato:**
- Comportamento reale sul client della stanza (Mac/telefono) alla ricezione di `fine` dopo un «forte» captato: non riproducibile in dev.
- Il mutante «niente ramo seguito nell'uso» non l'ho rieseguito: mi fido del dato dell'agente, coerente col test che asserisce `comando == "fine"`.

**Wall of Shame e guardrail:** niente slicing della history, niente simulazione di tool. Cap delle iterazioni e `_get_window` non toccati.

Memoria: riga #676-M2 aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (061334c). Lo stage del diff non è stato toccato.

Review #677-M2 sul diff staged di fd64e77 prima delle correzioni R-677-1/2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #677-M2 sul diff staged attuale: 4 file. Comprende l'aggiornamento richiesto da M1, cioè la parte R-676-3 di `_do_stt`. Letture fatte prima della review: CLAUDE.md (sez. 5, 8, 9), la memoria del revisore e le voci V15/R-675 di stato_progetto (cercate con grep).

**Elementi del diff esaminati**
- gas.py:4707 — se il turno è effimero forza `cervello = "forte"` prima di classificare. Rischio: un gratuito che riceve il parlato della stanza. Esito: ok. Il router usa "forte" (catena solo claude-cli). Lo prova T103d: OpenAI finto che solleva, risultato un solo errore dichiarato.
- gas.py:4766 — salva `_storia_vera` e lavora su `list(self.history)`; `_salva()` non fa nulla e la compressione viene saltata. Rischio: modifiche fatte sul posto ai dict condivisi dalla copia superficiale. Esito: ok. `_add_to_history` fa solo append. `_get_window` e `_cap_window_chars` restituiscono liste nuove. L'unico punto che modifica sul posto (`_segna_esito_in_storia`) sta nel percorso delle firme, che un turno effimero non attraversa. Nessuno slicing nuovo: il grep di `[-N:]` sul diff è vuoto. `_get_window` e `for _ in range(10)` non sono toccati.
- gas.py:4930 — se il modello chiede comunque uno strumento, si esce con `final` vuoto e lo strumento non viene eseguito. Rischio: simulazione dell'output del tool o esecuzione nascosta. Esito: ok. Nessun tool_res, niente nella storia. Lo strumento non viene offerto nemmeno al modello: `_offerta = {}` arriva a ClaudeCliClient come `tools=None`, e la CLI gira comunque con `--tools ""` (brains/claude_cli.py:303).
- gas.py:5084 — nel finally la storia vera torna al suo posto. Il ramo `_storia_rimandata` di un turno precedente resta pendente e lo salderà il turno normale successivo, che è corretto. Rischio: ripristino che non avviene davvero. Esito: **riserva** (R-677-1-M2, sotto). Provato in scratch: dopo un `break` sul `final` senza `close()`, `k.history is vera` è False (4 messaggi, col parlato). Torna True solo dopo `del g` / gc. Anche con `g.throw(...)` il generatore resta sospeso sull'evento di errore, con la copia attiva fino alla chiusura.
- modules/voice/server.py:574 — nel ramo seguito passa `kw["effimero"] = True`. Rischio: l'effimero che finisce anche fuori dal seguito. Esito: ok. Lo coprono il test con seguito=False ("effimero" not in kw) e l'assert nel test del seguito.
- modules/voice/server.py:601 — nel seguito una risposta vuota chiude come [NON_PER_ME]. Esito: ok. Fuori dal seguito il comportamento non cambia.
- modules/voice/server.py:809 e modules/voice/server.py:830 — R-676-3: nel seguito una STT incerta o vuota fa `_chiudi_seguito()` e ritorna None. Il chiamante (modules/voice/server.py:511) ritorna senza turno. Rischio: doppia risposta HTTP oppure un turno partito lo stesso. Esito: ok. Il test copre 3 casi × con/senza seguito; senza seguito restano «non ho capito» e il 400.
- tests/test_unit_kernel.py T103 — fa il round-trip §7 (caso c, normale con write_file dopo l'effimero). Esito: ok, ma vedi R-677-2-M2.
- Diario: `_chiudi_turno` scrive solo esito, conteggi, provider, tentati e classe, mai il prompt. `_recap_pin(user_prompt)` legge e basta. Ok.

**Test sull'albero staged esportato** (git checkout-index)
- Kernel: 1076 PASS, 0 FAIL; T103a-d PASS.
- tests/test_unit_voice_stt.py: 103 passed.
- Non ho rifatto i mutanti dichiarati.

**Riserve (da tracciare in stato_progetto.md)**
- **R-677-1-M2 BASSA** — Il ripristino dipende dalla chiusura del generatore. Il server fa `break` sul final senza `turno.close()`. Finché l'handler non esce, quindi, `self.history` è la copia col parlato e la risposta. Oggi non fa danni: HTTPServer single-thread e kernel della voce non condiviso con Telegram, che ha la sua istanza. Se però un secondo `run_turn` partisse mentre un generatore effimero è ancora sospeso, salverebbe il parlato su `.gas_history.json`, e il ripristino successivo cancellerebbe dalla memoria i messaggi di quel turno. Correzione proposta: `turno.close()` in un `finally` del blocco in modules/voice/server.py:576 (vale anche per gli altri chiamanti).
- **R-677-2-M2 BASSA** — T103 consuma il generatore con `list()` e quindi non copre il percorso del server (break senza close). Aggiungere un caso con break, controllo che `history` sia la storia vera dopo `close()`, e un turno normale dopo.

**Rischi esclusi**
- Comportamento reale di `claude -p`, cioè se il modello vero, senza strumenti descritti, emette comunque il formato di tool call: non verificato, serve il forte vivo.
- Concorrenza tra processi su `.gas_history.json`: non provata. L'effimero non salva, quindi non partecipa all'unione in `_save_history`.
- Effetto sul client voce di un `fine` dovuto alla STT incerta: client non esercitato.

Memoria aggiornata: riga #677-M2 e una lezione (stato sostituito in un generatore e ripristinato nel finally = vale solo alla chiusura). Committata con scripts/commit_memoria_revisore.sh, commit bad216f; lo stage del motore è intatto.

File: /home/user/Gas/gas.py, /home/user/Gas/modules/voice/server.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/tests/test_unit_voice_stt.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #677-M2 bis sullo stage finale di fd64e77 (verdetto integrale):

## VERDETTO: APPROVATO

Review #677-M2 bis. Ho rivisto solo l'aggiunta per R-677-1-M2 e R-677-2-M2, sullo stage attuale e già con la correzione del test (il riferimento vivo `tenuti`). Il ripristino della storia ora non dipende più dal garbage collector: il server chiude il turno subito, e un test lo dimostra.

**Elementi del diff esaminati**
- **modules/voice/server.py:592-594** — Il nuovo `try/finally` attorno al ciclo sugli eventi del turno chiude sempre il generatore con `close()`, quando esiste. Vale sia dopo il `break` sul final sia dopo il `return` sull'errore. Esito: ok.
  - Rischio esaminato: `close()` che solleva o che rientra. `GeneratorExit` è una BaseException, quindi gli `except Exception` interni di run_turn non la catturano. Parte il finally di gas.py: rimette la storia vera, scrive `turno_fine` e poi `_invia_avvisi_lead`, che è già protetto. Quel finally non fa `yield`, quindi non può nascere RuntimeError.
  - Se `close()` sollevasse comunque, il server risponde 500 tramite l'`except Exception` esterno. Unico caso limite, teorico: se l'errore arriva dopo un 500 già inviato, partirebbe una seconda risposta. Non ha effetti pratici.
- **tests/test_unit_voice_stt.py:806** — `test_v15_il_turno_viene_chiuso_subito` usa un kernel finto che tiene un riferimento vivo al generatore (`tenuti`), così il finally parte solo con il `close()` del server. Rischio esaminato: un test che passa anche senza la correzione. Esito: ok.
  - Mutante provato in una copia scratch dello stage (`close()` sostituito da `pass`): 1 failed. Con lo stage vero: 104 passed.
- **tests/test_unit_kernel.py:11547** — T103e: dopo un `break` sul final, finché il generatore è sospeso la storia è ancora la copia. Dopo `close()`, `history` è (`is`) la storia vera e non contiene il parlato. Esito: ok, PASS.
- Effetto collaterale (ok): `_chiudi_turno` e gli avvisi lead ora partono prima dell'invio della risposta vocale, non più all'uscita dall'handler. Aggiungono latenza solo nei turni che creano lead e mandano un avviso Telegram (rete). Il seguito effimero non ne è toccato: non usa strumenti, quindi non crea lead.

**Esecuzione sullo stage esportato**
- Suite kernel: 1077 PASS, 0 FAIL.
- `tests/test_unit_voice_stt.py`: 104 passed.

**Rischio escluso**
- Latenza reale aggiunta dall'invio dell'avviso lead prima della risposta vocale: non misurata. Servirebbero Telegram reale e un turno con lead.
- Il caso «su errore del kernel» citato nella docstring del test non è esercitato: il test copre solo il final. Il percorso con `return` sull'errore resta comunque coperto dal `finally` per costruzione del codice.

**Memoria**
- Aggiunta la riga #677-M2 bis in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata con `scripts/commit_memoria_revisore.sh` (commit aa1babe). Lo stage del motore non è stato toccato.

File:
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/tests/test_unit_voice_stt.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #678-M2 sul commit 10dc900 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #678-M2 sul diff staged (2 file, +6/-1) del branch feat/voce-v12-m2, PR #339.

**Elementi del diff che ho esaminato**
- `modules/voice/server.py:151`: `ISTRUZIONE_SEGUITO` ora dice al modello che nel turno di seguito «NON hai strumenti» e che non deve mai dire di aver fatto un'azione. Deve invece chiedere all'operatore di ripeterla dicendo prima la parola di attivazione.
  - Rischio esaminato: Tool Simulation (CLAUDE.md §5), cioè il modello che dichiara fatta un'azione mai eseguita.
  - Esito: ok. Il testo descrive davvero quello che succede nel turno effimero: nessuno strumento offerto e tool_call ignorata (gas.py, review #677).
- `modules/voice/server.py:146-154` confrontato con `modules/voice/server.py:202` (`ISTRUZIONE_VOCE`, contesto).
  - Rischio esaminato: contraddizione con «una o due frasi» e con «Non chiudere con domande né con offerte».
  - Esito: ok. La risposta richiesta è una sola affermazione, non una domanda e non un'offerta, quindi resta nelle due frasi. L'istruzione si aggiunge dopo quella della voce (`modules/voice/server.py:570`), quindi la regola sul seguito vale in più rispetto a quella generale e non la sostituisce.
  - Il precedente «senza usare strumenti» nel ramo [NON_PER_ME] ora è ridondante ma innocuo.
- `tests/test_unit_voice_stt.py:840`: il test controlla che `ISTRUZIONE_SEGUITO` contenga «NON hai strumenti» e «non dire mai».
  - Rischio esaminato: un test che sembra coprire il comportamento ma controlla solo il testo.
  - Esito: riserva R-678-1-M2, vedi sotto.
- Esecuzione: `tests/test_unit_voice_stt.py` sull'albero staged dà 104 passed.

**Riserve**
- R-678-1-M2 (BASSA): l'asserzione prova che il testo c'è, non che il modello lo rispetti. Nessun test unitario può provarlo senza un LLM vero. Va dichiarata come limite e controllata in una prova dal vero sul Mac (chiedere un'azione a Gas nel seguito senza dire «Hey Jarvis»).
- R-678-2-M2 (COSMETICA): «ricordare» è ambiguo. Può voler dire memorizzare una cosa, oppure richiamarla dal blocco di memoria che resta iniettato nel messaggio di sistema. Una domanda come «ricordami chi è X» potrebbe avere risposta senza strumenti, ma il testo spinge a rimandarla. L'errore è nel verso prudente, quindi accettabile. In una fetta futura si può scrivere «memorizzare» al posto di «ricordare».
- Riserva del chiamante, la confermo: i turni di seguito non entrano nella storia, quindi il turno dopo non ricorda il precedente. È una conseguenza voluta della scelta A dell'operatore e va tracciata in `stato_progetto.md`.

**Cosa non ho verificato**
- Come risponde davvero il cervello forte (`claude -p`) a questo testo: non riproducibile nel container, il forte è dormiente e non c'è un LLM.
- La suite del kernel: non l'ho rieseguita perché `gas.py` non è nel diff.

**Memoria**: riga #678-M2 scritta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova. Committata da sola con `scripts/commit_memoria_revisore.sh` (commit 2530577). Lo stage del motore è intatto.

Commit consentito: sì, dopo `bash scripts/segna_review_ok.sh` come ultimo passo prima del commit.

Review #679-M2 sul merge fd1b320 di origin/main (PR #338 e #340) nella PR #339 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #679-M2: merge di origin/main 83f3bcd (PR #338 fetta 43 e PR #340 fetta 42 della chat Mani) in feat/voce-v12-m2 (PR #339, V15). Il merge è in staging e non è committato.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (riga 4 e blocchi Mani/V15) e la coda di .claude/agents/memoria_revisore.md (lezione del 2026-11-05 su «errore → None»).

**Merge: non si perde nulla**
- Base comune 2bb05b0. Questi file in staging sono identici a quelli di main (MERGE_HEAD): clients/voice/ascolto.py, scripts/voce/LEGGIMI.md, scripts/voce/pausa.sh, scripts/voce/riprendi.sh.
- Tutti i file modificati dal branch sono uguali a HEAD, tranne memoria e stato_progetto (attesi). Handoff, ultimo_report e diff_sessione sono nella versione del branch, come previsto.
- `ls-files -u` è vuoto e non ci sono marcatori di conflitto. L'unico avviso di `--check` è uno spazio in coda che c'è già in main (reports/stato_progetto.md:669), non l'ha introdotto il merge.
- Memoria del revisore: è l'unione dei due lati, con 0 righe perse da HEAD o da MERGE_HEAD e nessuna riga estranea.

**Elementi del diff esaminati**
- `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento». Rischio: perdere la cronologia di uno dei due lati. Ho verificato con uno script che la riga è esattamente il prefisso V15 + « — prima: » + la riga 4 intera di main, e che ogni voce «prima:» di HEAD è ancora presente. I blocchi fetta 43 e fetta 42 vengono da main, il punto V15 dal branch — **ok**.
- `tests/test_unit_voce_ascolto.py:957` — il finto `synthesize_speech` del test 200/401 ora accetta `**kw`. Rischio: un TypeError col `timeout=` che il server passa dalla V15. Ho rieseguito la versione di main del test contro il server V15: `test_conferma_col_server_voce_vero` fallisce, quindi la correzione serve davvero — **ok**.
- `tests/test_unit_voce_ascolto.py:968` — `def tts(frase, k, voce, **kw)` nel test dei casi d'errore. Con la firma vecchia i 3 casi d'errore passavano verdi lo stesso: il TypeError non viene intercettato, il server chiude la connessione e il client restituisce None. È la prova concreta che R-675-1 è un problema reale — **riserva** (R-679-1-M2).
- `modules/voice/server.py:911` — la conferma chiama `synthesize_speech` con `timeout=CONFERMA_TIMEOUT_S`. Su 502 registra l'errore e per `CONFERMA_PAUSA_ERRORE_S` (60 s) non richiama ElevenLabs (`modules/voice/server.py:907`). Contratto col client: un 502 diventa HTTPError, quindi None e bip (`clients/voice/ascolto.py:737`); il client riprova al massimo una volta al minuto (`clients/voice/ascolto.py:104`); 503 senza chiave e audio vuoto finiscono in None. Nessuna cache dei dati condivisa tra i test: il fixture crea ogni volta una sottoclasse `_H` e la scrittura `type(self).conferma_errore` resta su quella — **ok**.
- `modules/voice/server.py:655` — `X-Gas-Seguito` viene letto solo dalla richiesta, e `X-Gas-Comando` viene emesso in `modules/voice/server.py:458`. Il client di Mani non manda Seguito e non legge Comando: è compatibile all'indietro, ma per lui la V15 non fa ancora niente. Con «pausa» suona «Va bene.» e la conversazione resta aperta; il ramo «fine»/JSON vuoto non scatta mai senza Seguito — **riserva** (R-679-2-M2).
- `scripts/voce/pausa.sh:1` / `scripts/voce/riprendi.sh:1` — script di main, già approvati in #673/#674. Ho controllato solo la sintassi con `bash -n`: ok. Non toccano il server — **ok**.

**Esecuzione**: voce_ascolto + voice_stt + voice_prova_voci danno 379 passed, dall'albero di lavoro col venv indicato. I 4 test d'integrazione col server vero passano.

**Riserve (da tracciare in stato_progetto.md)**
- R-679-1-M2 BASSA (coincide con R-675-1 ancora aperta, ora provata): i casi d'errore del test d'integrazione restano verdi anche se il finto solleva un'eccezione imprevista. Correzione: controllare «HTTP 502/503» in caplog e mettere `pytest.fail` nel finto del caso senza_chiave. Spetta alla chat Mani.
- R-679-2-M2 BASSA: manca ancora la parte client della V15 (mandare `X-Gas-Seguito: 1` nella finestra di conversazione, gestire `X-Gas-Comando: pausa/fine` e il 200 con JSON vuoto). Finché non c'è, la pausa a voce risponde ma non mette in standby. È lavoro della chat Mani, va coordinato da M1.
- Cosmetica: il fixture `server_voce_vero` (`tests/test_unit_voce_ascolto.py:943`) azzera `conferma_cache` ma non `conferma_errore`. Oggi è innocuo (sottoclasse nuova per ogni test), ma per simmetria con `tests/test_unit_voice_prova_voci.py:155` andrebbe azzerato anche quello.

**Cosa non ho verificato**: comportamento reale sul Mac (launchctl di pausa.sh/riprendi.sh, audio, microfono), non riproducibile in questo ambiente. Neanche la suite completa del kernel: il merge non tocca gas.py né i test del kernel (blob uguali a HEAD), quindi l'ho giudicata non necessaria.

**Memoria**: riga `#679-M2 — 2026-11-06 — APPROVATO CON RISERVE — …` aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e messa in staging con `git add`, senza commit e senza lo script, come chiesto. Nessuna lezione nuova.

File rilevanti: /home/user/Gas/tests/test_unit_voce_ascolto.py, /home/user/Gas/modules/voice/server.py, /home/user/Gas/clients/voice/ascolto.py, /home/user/Gas/reports/stato_progetto.md, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #680-M2 sul commit 4ee1feb (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #680-M2. Diff staged: 4 file, +34/-1, branch feat/voce-v12-m2, PR #339. Letture obbligatorie fatte: CLAUDE.md sez. 5 e 8, reports/stato_progetto.md (voce V15), .claude/agents/memoria_revisore.md.

**Cosa ho esaminato**
- `gas.py:4938` — nel turno effimero la chiamata a strumento ignorata ora rende `{"type": "final", "content": "", "strumento_negato": True}`.
  - Rischio esaminato: effetti sugli altri chiamanti di `run_turn`.
  - Esito: **ok**. Gli altri chiamanti non passano mai `effimero`, quindi la chiave non compare per loro: `modules/telegram/bot.py:789`, `modules/notte/notte.py:286` e il CLI in `gas.py:6292`. In ogni caso leggono solo `type` e `content`. Il cap di 10 iterazioni, `_get_window` e il ripristino della storia vera non sono toccati, e non c'è slicing della history.
- `modules/voice/server.py:589` — la chiave si legge con `bool(event.get(...))`; il valore iniziale `False` è a `modules/voice/server.py:567`.
  - Rischio esaminato: chiave assente o di tipo strano.
  - Esito: **ok**. Il default è sicuro e nessuna eccezione nuova può nascere da qui.
- `modules/voice/server.py:616` — se il turno è audio, è un seguito e lo strumento è stato negato, chiama `_rispondi_senza_turno(RISPOSTA_SERVE_ATTIVAZIONE, "serve_attivazione")`. Il controllo viene prima del ramo «[NON_PER_ME] o vuoto → fine».
  - Rischio esaminato: ordine dei rami e privacy.
  - Esito: **ok**. La frase è fissa (`modules/voice/server.py:143`) e non contiene niente di quello che si dice nella stanza. Nessun `X-Gas-Comando` viene impostato, quindi la conversazione resta aperta. Il caso vuoto senza strumento continua a chiudere. Senza TTS la frase arriva come testo con la chiave `serve_attivazione` (mai un 503).
- `tests/test_unit_voice_stt.py:831` — il test nuovo controlla status 200, `X-Gas-Comando` assente, `content` uguale alla frase e `serve_attivazione` vero.
  - Esito: **ok**. Se si toglie il ramo, il turno cade nel ramo vuoto → fine con `content` vuoto, quindi il mutante viene ucciso.
- `tests/test_unit_kernel.py:11520` — T103b ora asserisce `[True]` sulla chiave.
  - Esito: **ok**.
- Verifica eseguita da me: i test v15 di voice_stt danno 11 passed. Non ho rieseguito tutta la suite del kernel: mi fido del dato dichiarato (1077 PASS).

**Riserve**
- **R-680-1-M2 (BASSA)**: prima, una frase captata nella stanza che il forte scambiava per una richiesta d'azione (ad esempio detta a un'altra persona) finiva in silenzio. Ora Gas parla nella stanza con la frase fissa. È un compromesso accettabile: il modello avrebbe dovuto rispondere «[NON_PER_ME]», e la frase non rivela nulla. Va comunque osservato nella prova dal vero.
- **R-680-2-M2 (BASSA)**: se il modello scrive del testo insieme alla chiamata a strumento, quel testo resta scartato. È un comportamento che c'era già, la modifica non lo cambia.

**Cosa NON ho verificato**
- Il comportamento reale di `claude -p` o degli altri provider quando non vengono offerti strumenti, cioè quanto spesso il forte ne chiede uno comunque: non si può riprodurre senza il modello vero.
- Il lato client (chat Mani), cioè cosa fa il client con la chiave `serve_attivazione`: non fa parte di questo diff.

Memoria aggiornata con la riga #680-M2 e committata con `scripts/commit_memoria_revisore.sh` (commit 4899032). Lo staged del motore è intatto: 4 file, +34/-1.

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/tests/test_unit_voice_stt.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_stt.py`: test V15 (pausa, seguito, «forte» dalla stanza, prefisso del segno, incerta/vuota nel seguito, chiusura del turno, strumento negato → frase fissa), «Jarvis Gas» fra i positivi. `tests/test_unit_voice_prova_voci.py`: +1 (`test_v15_conferma_errore_recente_non_richiama_elevenlabs`). `tests/test_unit_kernel.py` T103a-e (round-trip §7 del turno effimero; T103b controlla `strumento_negato`). `tests/test_unit_voce_ascolto.py` (chat Mani): solo `**kw` sui due finti, autorizzato da M1. Mutanti su gas.py (storia non ripristinata, strumenti offerti, strumento eseguito, salvataggio, forte non forzato) uccisi da T103. Esecuzione sull'head 4ee1feb, nel venv con requirements + requirements-dev: voice_stt + voice_prova_voci + voce_ascolto `380 passed in 77.91s`; suite kernel `=== RIEPILOGO: 1077 PASS, 0 FAIL ===` (prima della sessione 1076).

## §6 STATO CI

`gh` non autenticato nel cloud: run lette con l'integrazione GitHub.
- 04532a3, 8c9bc1b, 2d2d432: nessuna run su questi SHA da soli.
- 5cf7267: CI failure (run 42127434430; superata dai commit successivi).
- b0405dc: CI success (run 42127632662); verifica-bot FAILURE nel verdetto (MEDIA: storia del seguito, strumenti attivi).
- 061334c, bb731b2: nessuna run su questi SHA da soli (pushati con 3581f6f).
- 3581f6f: CI success (run 42128563229); verifica-bot con la stessa MEDIA.
- bad216f, aa1babe, fd64e77: nessuna run su questi SHA da soli (pushati con a87d273).
- a87d273: CI success (run 42133629442), verifica-bot success (run 42133634353) con verdetto testuale V-1 (a)/(b) MEDIA e verifica esterna con V-2.
- 2530577, 10dc900, fd1b320, 4899032, 4ee1feb e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme: la run testerà solo la testa).

## §7 RISERVE APERTE

- V-1 (a) bot su a87d273, MEDIA: i turni di seguito veri non entrano nella storia (decide l'operatore, §0 punto 2).
- R-678-1-M2 BASSA: che il modello rispetti l'istruzione «niente strumenti» si vede solo dal vero.
- R-678-2-M2 COSMETICA: «ricordare» ambiguo nell'istruzione.
- R-679-1-M2 BASSA: test d'errore di Mani verdi anche con eccezioni impreviste (chat Mani).
- R-679-2-M2 BASSA: manca il lato client della V15 (`X-Gas-Seguito`, `X-Gas-Comando`; chat Mani via M1).
- R-680-1-M2 BASSA: nel seguito una frase della stanza scambiata per richiesta d'azione fa parlare Gas con la frase fissa.
- R-680-2-M2 BASSA: testo scritto dal modello insieme a una chiamata a strumento resta scartato (comportamento preesistente).
- R-676-1-M2 BASSA: «[NON PER ME] (…)» e «NON_PER_ME (…)» con aggiunte non riconosciuti.
- R-675-2-M2 BASSA: oltre il tetto orario «pausa» riceve 429; i turni ambientali consumano il tetto.
- R-675-4-M2 COSMETICA: «basta così?» come domanda chiude la conversazione; «forte, pausa» va al forte.
- R-675-5-M2 BASSA: forte spento → turni di seguito 500 (il client deve chiudere); forte acceso → ogni frase captata spende il budget del forte.
- Da verificare lato client (Mani): JSON (non NDJSON) nella risposta «fine» col formato audio+pezzi.
