# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5180114384","url":"https://github.com/Gasss23/Gas/pull/339"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10. Sì dell'operatore già dato via M1: CI verde e bot + verifica esterna senza ALTA/MEDIA sul nuovo head.
2. Punto 1 FATTO col sì dell'operatore (e7a75c0) e R-682-1-M2 CHIUSA con la scelta A dell'operatore (f75719d): un seguito a voce nella finestra manda il turno al solo forte; riflessione rimandata. Nessuna nuova decisione richiesta per la #339.

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
- **V-1/V-2 bot su 312cd86** (segno in coda; «Basta!» dalla TV nel seguito detto a voce): `FATTA` — 2e367e2, review #681-M2. Il FAILURE del bot su 312cd86 è un falso positivo del parser («letto ad alta voce» preso per ALTA): fuori scope, macchina del bot.
- **V-1 (a) bot su a87d273/be60a21** (i seguiti veri non entrano nella storia): `FATTA` col sì dell'operatore — `registra_seguito` in gas.py, e7a75c0, review #682-M2. Riserva nuova R-682-1-M2 MEDIA in attesa di decisione.
- **V-1 MEDIA bot su 16dd4a5** (seguito salvato non contava come input non fidato): `FATTA` — ae61546, review #684-M2; T103l rafforzato in 933780f (#685-M2).
- **V-2 MEDIA bot su 16dd4a5** (audio dei seguiti a Groq Whisper): rischio ACCETTATO dall'operatore (scelta a, via M1, 6 nov), dichiarato nei commenti (933780f) e registrato come R-684-2-M2.
- **R-682-1-M2 MEDIA** (seguiti salvati → finestra dei gratuiti): `FATTA` con la scelta A dell'operatore — f75719d, review #683-M2 BOCCIATO poi bis APPROVATO CON RISERVE.
- **V-2/V-3 bot su be60a21** (segno in mezzo; risposta vuota effimera → 500): `FATTA` — e7a75c0.
- **C1**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  21 ++++++++++++
 gas.py                              | 129 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 modules/voice/server.py             | 169 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 modules/voice/tts.py                |   4 ++-
 reports/diff_sessione.md            |  20 +++++++-----
 reports/handoff.md                  | n/d
 reports/ripartenza_m2.md            |  11 ++++---
 reports/stato_progetto.md           |   3 +-
 reports/ultimo_report.md            |  37 ++++++++++++---------
 tests/test_unit_kernel.py           | 218 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py     |   5 +--
 tests/test_unit_voice_prova_voci.py |  34 ++++++++++++++++++--
 tests/test_unit_voice_stt.py        | 277 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: origin/main 83f3bcd.

## §3 GIT LOG --ONELINE (sessione)

```
933780f docs(kernel+voce): V15 — trascrizione Groq dei seguiti dichiarata come rischio accettato dall'operatore; T103l sul ramo della firma (V-2 bot #339 su 16dd4a5, R-684-1-M2) (chat M2)
cb4dff2 chore(revisore): memoria review #685 — APPROVATO
ae61546 fix(kernel+voce): V15 — un seguito a voce nella finestra è input non fidato (scritture alla firma); [non-per-me] col trattino (V-1 bot e V-2 ve #339 su 16dd4a5) (chat M2)
1ca1ca8 chore(revisore): memoria review #684 — APPROVATO CON RISERVE
16dd4a5 docs(voce): report di fine task V15 dopo R-682-1 chiusa con la scelta A (PR #339, chat M2)
f75719d feat(kernel): V15 R-682-1 — un seguito a voce nella finestra manda il turno al solo forte; riflessione rimandata (scelta A dell'operatore via M1) (chat M2)
41c3275 chore(revisore): memoria review #683 — APPROVATO CON RISERVE
be724e6 chore(revisore): memoria review #683 — BOCCIATO
d38f95d docs(voce): report di fine task V15 punto 1 (seguiti nella storia vera) e R-682-1-M2 da decidere (PR #339, chat M2)
e7a75c0 feat(kernel+voce): V15 punto 1 — i seguiti rivolti a Gas entrano nella storia vera; segno [NON_PER_ME] ovunque; risposta vuota effimera = silenzio (V-1/V-2/V-3 bot #339 su be60a21, sì dell'operatore via M1) (chat M2)
390785b chore(revisore): memoria review #682 — APPROVATO CON RISERVE
be60a21 docs(voce): report di fine task V15 dopo V-1/V-2 del bot su 312cd86 (PR #339, chat M2)
2e367e2 fix(voce): V15 — segno [NON_PER_ME] anche in coda; nel seguito la pausa chiude senza voce (V-1/V-2 bot #339 su 312cd86, chat M2)
93ee68d chore(revisore): memoria review #681 — APPROVATO CON RISERVE
312cd86 docs(voce): report di fine task V15 dopo V-2 ve, merge di main e frase fissa del seguito (PR #339, chat M2)
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

Review #681-M2 sul commit 2e367e2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #681-M2 sul diff STAGED (base 312cd86, branch feat/voce-v12-m2, PR #339): modules/voice/server.py e tests/test_unit_voice_stt.py. Prima della review ho letto CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (voce V15, riga 615) e la coda di .claude/agents/memoria_revisore.md. git status mostra solo «M » (niente «MM»), quindi l'albero di lavoro coincide con quello staged.

Cosa ho esaminato:
- modules/voice/server.py:150 — `_NON_PER_ME` ha una terza alternativa, `|\[non_per_me\]\W*$`. Il segno con le parentesi ora vale anche in coda. Rischi controllati:
  - Precedenza della regex: l'alternativa nuova non ha `^`, ma l'uso è con `.search` (server.py:628), quindi funziona come voluto.
  - Il segno in mezzo alla risposta non conta: «x [NON_PER_ME] y» → False.
  - Backtracking: 200k spazi in 2 ms; 30k segni ripetuti, tempo trascurabile.
  - Uso: solo dentro il ramo `is_audio and self._seguito()`, quindi fuori dal seguito non cambia niente.
  - Esito: ok.
- modules/voice/server.py:525 — nel seguito, con `_SOLO_PAUSA`, risponde `_send_json(200, {"content": "", "pausa": True})` dopo aver impostato `_comando = COMANDO_PAUSA`. L'intestazione X-Gas-Comando parte da end_headers (modules/voice/server.py:460). Rischi controllati:
  - Niente sintesi e niente «capito» nel corpo, come in `_chiudi_seguito` (modules/voice/server.py:664). Coerente con la privacy della stanza.
  - Nessun turno del kernel.
  - Fuori dal seguito resta `_rispondi_senza_turno(RISPOSTA_PAUSA, …)`, invariato.
  - `_seguito()` vale solo per il parlato (`self._parlato`, modules/voice/server.py:672), e questo ramo è già dentro `is_audio`.
  - Esito: ok.
- tests/test_unit_voice_stt.py:752 — `test_v15_seguito_pausa_senza_voce`. Prova 3 formati. La sintesi finta solleva AssertionError se viene chiamata. Controlla il codice 200, X-Gas-Comando: pausa, content vuoto, assenza di «audio» e che non parta nessun turno (kernel.kw resta "NESSUN TURNO"). Mutante «ramo seguito tolto» (`if False:`) provato da me in una copia scratch dell'albero: 1 failed. Esito: ok.
- tests/test_unit_voice_stt.py:736 (test non_per_me con le varianti in coda) e la frase col segno in mezzo nel test rivolto_a_gas: coprono la regex in entrambi i versi. Il mutante «coda tolta» non l'ho rieseguito: mi fido del dato dell'agente (1 failed), e il caso in coda è asserito esplicitamente. Esito: ok.
- Suite voice_stt + prova_voci + voce_ascolto nel venv di scratch: 381 passed, confermato.
- Wall of Shame: nessuno slicing della history, nessuna simulazione di tool (i finti sono patch nei test). gas.py, `_get_window`, il cap delle 10 iterazioni e il cap di output non sono toccati.

Riserve:
- R-681-1-M2 BASSA: se il modello risponde davvero a Gas ma chiude per errore col segno in coda («Fatto. [NON_PER_ME]»), la risposta viene taciuta e la conversazione si chiude. Il verso è sicuro per la privacy, ma va saputo: si vedrà solo nella prova dal vero.
- R-681-2-M2 COSMETICA: nel seguito la risposta di pausa è JSON semplice anche col formato «audio+pezzi», come `_chiudi_seguito`. Il client (chat Mani) deve decidere dall'intestazione X-Gas-Comando, non dal tipo del corpo. Collegata a R-679-2-M2, già aperta.
- Residuo già noto, non nuovo: R-676-1-M2. «[NON PER ME]» senza trattino basso vale solo come risposta intera, non in coda.

Cosa NON ho verificato:
- Il client reale (clients/voice/ascolto.py della chat Mani) non è nel diff e oggi non manda X-Gas-Seguito: il comportamento end-to-end sul Mac non si può riprodurre qui.
- Il comportamento del modello forte (se mette davvero il segno in testa o in coda) non è verificabile con test unitari.
- Il FAILURE del bot su 312cd86 (falso positivo di `_FINDING_GRAVE_A_PAROLE` su «letto ad alta voce») è fuori da questo diff, come da istruzioni: macchina del bot, decide l'operatore.

Memoria: riga #681-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con scripts/commit_memoria_revisore.sh (commit 93ee68d). Nessuna lezione nuova.

Review #682-M2 sul commit e7a75c0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #682-M2: branch feat/voce-v12-m2, PR #339, diff staged su base be60a21. File: gas.py, modules/voice/server.py, tests/test_unit_kernel.py, tests/test_unit_voice_stt.py.
Prima della review ho letto CLAUDE.md (sez. 1, 2, 5, 8, 9 e 10), le voci voce/V15 di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md (#675–#681-M2).

**Elementi del diff esaminati**
- `gas.py:1805` — nuovo `registra_seguito(domanda, risposta)`. Rifiuta testi vuoti o non stringa. Comprime la storia se serve, aggiunge user+assistant e salva con `_save_history(fine_turno=True)`, che restituisce True solo se la storia è davvero su disco. Un'eccezione diventa `logging.warning` e False (§9).
  - Rischio esaminato: sequenza dei ruoli rotta per `_get_window`, salvataggio rimandato che resta in sospeso, crash.
  - Con fine_turno=True l'unione con la storia di altri processi non viene rimandata. La coppia parte da user. Nessuno slicing.
  - Esito: **ok**.
- `modules/voice/server.py:636` — la registrazione scatta solo con `is_audio and self._seguito()`. Arriva dopo il `close()` del generatore (`modules/voice/server.py:612`), quindi la storia vera è già ripristinata dal finally di `gas.py:5111`. Arriva anche dopo i rami strumento_negato, NON_PER_ME e vuota, che fanno `return` prima. Il kernel è raggiunto con getattr; False o eccezione diventano warning e la risposta parte lo stesso.
  - Rischio esaminato: parlato «non per me» che entra in storia, doppio salvataggio nei turni normali, concorrenza.
  - Il server è `HTTPServer` (`modules/voice/server.py:1139`), quindi un thread solo. I turni normali non passano `effimero` e si salvano da sé, come asserito nel test di `tests/test_unit_voice_stt.py:912`. La scelta del turno da salvare sta solo lato server.
  - Esito: **ok**, con la riserva R-682-1 sotto.
- `modules/voice/server.py:152` — la nuova regex `_NON_PER_ME` riconosce il segno tra parentesi in qualunque punto, anche con spazi o in minuscolo. La forma senza parentesi conta solo come risposta intera.
  - Rischio esaminato: rallentamento patologico della regex (ReDoS) e falsi positivi.
  - Non ci sono quantificatori annidati e la seconda alternativa è ancorata all'inizio. L'unico falso positivo possibile è che si taccia una risposta vera: è il verso sicuro per la privacy, scelto dall'operatore, e allarga la riserva già aperta R-681-1-M2. Il caso del test che lo contraddiceva è stato tolto in modo coerente.
  - Esito: **ok**.
- `gas.py:5069` — nuovo ramo `elif effimero`: risposta vuota del forte senza chiamate a strumenti → evento `final` con testo vuoto invece di «Pipeline esausta». Vale solo per il turno effimero; la storia viene comunque ripristinata nel finally.
  - Rischio esaminato: un guasto vero del forte nascosto come «silenzio».
  - Esito: **riserva** R-682-2.
- `tests/test_unit_kernel.py:11582` — T103g: dopo la registrazione la storia è su disco subito. Il turno normale successivo, con uno strumento vero (write_file eseguito), vede il seguito nel payload: è il round-trip agentico di §7. Il seguito compare una volta sola e i tre casi vuoti sono rifiutati. T103f (`tests/test_unit_kernel.py:11558`) copre V-3.
  - Esito: **ok**.
- `tests/test_unit_voice_stt.py:916` — test sulla registrazione che fallisce (False ed eccezione): risposta 200 lo stesso.
  - Esito: **ok**.

**Test rilanciati da me** (venv della sessione): `tests/test_unit_kernel.py` 1079 PASS 0 FAIL, con T103f e T103g PASS. `tests/test_unit_voice_stt.py` 107 passed.

**Wall of Shame**: nessuno slicing della storia, nessuna simulazione dell'output dei tool. Il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Riserve**
- **R-682-1-M2 MEDIA (privacy)** — Il seguito salvato entra nella finestra dei turni normali successivi, e quei turni possono andare ai modelli gratuiti della cascata.
  - Effetto: un parlato della stanza che il forte scambia per rivolto a Gas (R-680-1-M2) finisce così ai gratuiti. R-675-1-M2 lo voleva confinato al forte (CLAUDE.md §2).
  - L'operatore ha scelto «salva i seguiti con risposta vera», ma questa conseguenza va dichiarata esplicitamente nel report, così può decidere.
  - Possibili rimedi: marcare quei messaggi come forte-only, oppure accettare il rischio.
- **R-682-2-M2 BASSA** — Il ramo `elif effimero` (`gas.py:5069`) non logga nulla. Se il forte torna vuoto per un guasto, la conversazione si chiude in silenzio senza traccia in gas_debug.log. Basta un `logging.info`.
- **R-682-3-M2 BASSA** — La registrazione avviene prima della sintesi vocale. Se il TTS fallisce, la risposta è in storia ma l'operatore non l'ha sentita (come succede già nei turni normali).

**Rischio esplicitamente escluso**: non ho verificato la concorrenza su più processi reali (voce + Telegram che scrivono `.gas_history.json` nello stesso momento durante il turno effimero). L'unione tra processi (`_unisci_storia_altrui`) non è toccata dal diff e qui l'ho solo letta, non provata con processi veri. Non ho verificato nemmeno il comportamento col forte vero (`claude -p`) sul Mac: non è riproducibile in dev.

**Memoria**: aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #682-M2 e una lezione nuova: un dato confinato al forte va seguito anche dopo, quando entra nella storia condivisa. Committata da sola con `scripts/commit_memoria_revisore.sh` (commit 390785b); il resto dello staged è intatto.

Review #683-M2 sul primo stage di f75719d (verdetto integrale):

## VERDETTO: BOCCIATO

Review #683-M2: diff staged di gas.py e tests/test_unit_kernel.py (PR #339, base d38f95d). Ho letto CLAUDE.md (sezioni 2, 5, 6, 8, 9), la voce V15 di reports/stato_progetto.md e la coda della memoria (lezione del 6 novembre sul dato confinato al forte).

### Motivo del blocco

1. `gas.py:4064` — rifletti() costruisce `OpenAI(base_url=url, api_key=os.environ.get(env))` per ogni rung della cascata. Con la nuova classe «forte» (`gas.py:4047`) l'unico rung è `("claude-cli", "GAS_CLAUDE_CLI", None, MODEL_CLAUDE_FORTE)`. Quindi `base_url=None` porta all'endpoint predefinito di OpenAI (api.openai.com) e la chiave diventa il valore "1".
   - L'ho riprodotto in scratch: OpenAI viene costruito con base_url None e ClaudeCliClient non viene mai usato. La riflessione fallisce sempre con «nessun provider ha prodotto una riflessione valida».
   - Effetto: proprio la trascrizione che contiene il parlato del seguito, il dato da proteggere, verrebbe mandata a un servizio esterno che Gas non usa (la richiesta parte col corpo prima del 401). È peggio della situazione che la fetta vuole correggere.
   - Esito: **blocco**.
2. `gas.py:4058` — il controllo `if not os.environ.get(env): continue` per il rung claude-cli considera acceso anche `GAS_CLAUDE_CLI=0` (run_turn invece usa `_rung_disponibile`, `gas.py:908`). Esito: **blocco** (va corretto insieme al punto 1).
3. `tests/test_unit_kernel.py:11633` — T103k controlla solo `provider_atteso == "claude-cli"`. Il campo viene impostato prima della chiamata, e in T103k il finto `_NoOpenAI103` solleva `AssertionError`, che rifletti cattura. Il test passa quindi proprio perché rifletti chiama OpenAI invece del forte e fallisce: il mutante «client sbagliato» resta vivo. Esito: **blocco** (il test deve pretendere `esito["ok"]` e l'uso di ClaudeCliClient).

**Correzione richiesta**: in rifletti, per `name == "claude-cli"`:
- usare `ClaudeCliClient(timeout=self.CLAUDE_CLI_TIMEOUT_SEC)` e `_rung_disponibile(name, env)`, come run_turn;
- valutare anche il tetto del forte;
- in T103k verificare `ok is True` e che il finto CLI sia stato chiamato.

### Elementi del diff esaminati (ok)

- `gas.py:4828` — instradamento: dopo `classifica_compito`, se la finestra contiene un seguito il turno diventa «forte».
  - Il controllo usa `self._get_window()`, cioè la stessa finestra già tagliata da `_cap_window_chars` che va nel payload: controllo e invio sono coerenti.
  - Se un seguito esce dalla finestra a metà turno, il turno resta sul forte (verso prudente).
  - Effimero: era già forte.
  - Telegram (processo separato) calcola la finestra sulla propria storia in memoria; l'unione con la storia degli altri processi avviene al salvataggio, quindi la verifica copre esattamente ciò che viene inviato.
  - Esito: ok.
- `gas.py:4908` — il payload usa `_senza_segni_interni(_window)`. Ho cercato tutte le costruzioni di `messages=`: in run_turn passano solo da `payload` (`gas.py:4938`, `gas.py:4963`); rifletti invia un testo trascritto, non i dict. Esito: ok.
- `gas.py:1588` — il riepilogo di compressione eredita la chiave se ha riassunto un seguito.
  - La compressione è deterministica (nessun LLM).
  - Il riepilogo resta di solito fuori dalla finestra da 10 messaggi (dopo la compressione la storia ha 22 messaggi), quindi la chiave non diventa permanente.
  - Esito: ok.
- `gas.py:1839` — `registra_seguito` segna la coppia user/assistant dopo `_add_to_history`.
  - `_hash_messaggi` (`gas.py:1291`) serializza tutto il dict con sort_keys e `_unisci_storia_altrui` (`gas.py:1315`) unisce dict interi: la chiave sopravvive al merge, nessun confronto si rompe.
  - Se il salvataggio fallisce, la chiave resta in memoria (prudente).
  - Esito: ok.
- `gas.py:5104` — `logging.info` nel ramo della risposta vuota effimera: chiude R-682-2-M2. Esito: ok.
- Wall of Shame:
  - Nessuno slicing nuovo della storia; `_get_window` e `_cap_window_chars` non sono toccati.
  - `_senza_segni_interni` copia i messaggi senza togliere né tagliare nulla.
  - Nessun output di tool simulato.
  - Il ciclo resta a 10 iterazioni.
  - Esito: ok.

### Riserve (da tracciare anche dopo la correzione)

- **R-683-1-M2 MEDIA (privacy, percorso derivato)**: quando la riflessione sul forte funzionerà, il recap nato da una finestra con un seguito viene scritto come recap fidato. `_recap_pin` (`gas.py:3904`) lo inietta nel messaggio system di ogni turno per `RECAP_MAX_GIORNI` giorni, compresi i turni che vanno ai gratuiti. Così un riassunto del parlato della stanza arriva ai gratuiti. Proposta: in quel caso scrivere il recap con un tipo che il pin non legge, oppure iniettarlo solo nei turni sul forte.
- **R-683-2-M2 BASSA**: col forte spento, un normale «ciao» da Telegram o dal terminale riceve «Pipeline esausta: … claude-cli: GAS_CLAUDE_CLI non impostata» (T103i). Il messaggio non dice che il turno è solo-forte per via di un seguito a voce, e l'operatore aveva chiesto «forte fermo». Inoltre Gas resta inservibile sui gratuiti finché il seguito non esce dalla finestra (circa 8 messaggi): è la scelta A dell'operatore, ma va dichiarata nel testo dell'errore.

### Altri punti controllati (nessun percorso aggiuntivo)

- Giro notturno: `modules/notte/notte.py:283` azzera `kernel.history`.
- `_memoria_pin`: legge il diario, dove i seguiti non scrivono.
- Telegram e terminale: passano da run_turn.

### Rischi non verificati

- Non ho verificato il comportamento reale di rete di `OpenAI(base_url=None)` sul Mac o sulla VPS, cioè se il corpo parte davvero prima del 401. Non è riproducibile qui senza rete; il blocco si regge comunque sul client sbagliato, provato in scratch.
- Non ho rilanciato la suite kernel completa (fanno fede i 1083 PASS dichiarati dall'agente): ho eseguito solo la prova mirata di rifletti, `/tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/prova_rifl.py`.
- Il lato server della voce (`modules/voice/server.py`) è fuori da questo diff.

### Memoria

Ho aggiunto in `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #683-M2 e una lezione nuova: quando un secondo chiamante di `_cascata_provider` riceve una classe nuova, verificare che sappia costruire il client di quel rung e che usi `_rung_disponibile`. Il file è committato da solo (be724e6); gas.py e il test restano nello staging, non committati.

Review #683-M2 bis sul commit f75719d (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #683-M2 bis (chat M2, branch feat/voce-v12-m2, PR #339, base d38f95d). Diff STAGED: gas.py e tests/test_unit_kernel.py. Prima ho letto CLAUDE.md, la parte di reports/stato_progetto.md che riguarda R-682/683 e la mia memoria (riga #683-M2).

**Elementi del diff esaminati**
- `gas.py:4004` — se la finestra della riflessione (40 messaggi, presa con `_get_window`) contiene un seguito, `rifletti` esce subito con un errore, senza chiamare nessun modello e senza scrivere un recap. Rischio esaminato: il blocco di #683 (classe «forte» → `OpenAI(base_url=None)`, controllo che accettava anche `GAS_CLAUDE_CLI=0`) e R-683-1 (un recap nato da un seguito finiva nel pin dei gratuiti). — ok: la classe «forte» non c'è più nel ramo; nessun client viene costruito; nessun recap viene scritto.
- `tests/test_unit_kernel.py:11639` — T103k ora pretende: `ok` False, «seguito a voce» nel messaggio d'errore, `provider_atteso` None, nessuna chiamata al finto (`_tools103 == []`) e nessun recap nuovo nel diario. Rischio esaminato: un test che passa anche se la chiamata fallisce (lezione #683). — ok: il mutante «skip tolto» provato in scratch fa fallire T103k (1082 PASS, 1 FAIL).
- `gas.py:5146` — se la cascata si esaurisce in un turno solo-forte per via di un seguito, l'errore spiega perché (R-683-2). Rischio esaminato: che il testo compaia anche nei turni forti normali. — ok: compare solo con `_solo_forte_seguito` (`gas.py:4833`), che vale True solo quando il classificatore NON aveva già scelto forte. T103i (`tests/test_unit_kernel.py:11610`) lo asserisce; il mutante «solo-forte tolto» fa fallire T103h e T103i.
- `gas.py:4914` — il payload passa da `_senza_segni_interni(_window)`: la finestra resta intera, senza slicing, e si toglie solo la chiave interna. — ok: il mutante «strip tolto» fa fallire T103h.
- `gas.py:1586` — la compressione segna il riepilogo quando riassume un seguito. Il segno passa anche da un riepilogo al successivo, perché il vecchio riepilogo finisce in `to_compress`. — ok: il mutante fa fallire T103j.
- Contesto: `gas.py:1816` — `_add_to_history` non salva su disco, quindi segnare `history[-2]`/`history[-1]` prima di `_save_history(fine_turno=True)` non rompe il confronto con la base in `_unisci_storia_altrui` (gas.py:1335). La compressione è locale (nessun LLM). Gli altri chiamanti: `modules/notte/notte.py:257` lavora con la storia vuota; `gas.py:6262` (`clear`) riceve l'errore e pulisce lo stesso. Tutto fail-safe §9.
- `gas.py:5110` — ora il ramo effimero vuoto lascia una traccia nel log (R-682-2-M2 chiusa).

**Prove eseguite**
- Suite kernel sull'albero staged esportato: 1083 PASS, 0 FAIL. T103h, T103i, T103j e T103k PASS.
- 4 mutanti in copia scratch, tutti uccisi: skip in rifletti, solo-forte, strip della chiave, segno nella compressione.
- Wall of Shame: nessuno slicing nuovo della storia; `_get_window` intatta; cap di 10 iterazioni e `_cap_window_chars` non toccati; nessuna simulazione di tool.

**Riserve (da tracciare in stato_progetto.md)**
- R-683b-1-M2 BASSA: con `clear` la riflessione automatica di un task che ha un seguito in finestra non viene «rimandata» ma persa, perché la storia si pulisce subito dopo. Il messaggio «rimandata» è impreciso in quel caso.
- R-683b-2-M2 BASSA: dopo un seguito, i turni normali successivi (anche quelli da Telegram, finché il seguito resta negli ultimi 10 messaggi) spendono il budget del forte. Col forte spento restano fermi, con un errore dichiarato. È un impatto pratico da spiegare all'operatore.

**Rischio escluso**
Non ho verificato il comportamento reale di `claude -p` (ClaudeCliClient) quando riceve il payload, né cosa succede sul Mac o sulla VPS con due processi (voce e Telegram) che scrivono la stessa storia nello stesso momento: non si riproduce in dev. Mi sono limitato a controllare che le chiavi sopravvivano all'unione JSON.

- Memoria aggiornata (riga «#683-M2 bis») e committata con `scripts/commit_memoria_revisore.sh` → commit 41c3275 (solo `/home/user/Gas/.claude/agents/memoria_revisore.md`). Lo staging del diff del motore è rimasto com'era.

Review #684-M2 sul commit ae61546 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #684-M2, branch feat/voce-v12-m2, PR #339, sul diff STAGED (gas.py, modules/voice/server.py, tests/test_unit_kernel.py, tests/test_unit_voice_stt.py). Ho fatto le letture obbligatorie: CLAUDE.md §5/§8/§9 (nel contesto), reports/stato_progetto.md (voce V15, riga 615) e la coda di .claude/agents/memoria_revisore.md (#682-M2, #683-M2, #683-M2 bis).

**Elementi del diff esaminati**

- `gas.py:2086` — `_finestra_e_contaminata` restituisce True quando nella finestra c'è un messaggio con `seguito_voce`.
  - Rischio esaminato: effetti collaterali sui tre chiamanti.
  - (a) `run_turn`, `gas.py:4917`: con un seguito in finestra gli strumenti UNCERTAIN vanno al cancello di firma, salvo `_libero_dopo_lettura`. `salva_contatto` e `imposta_stato_contatto` vengono segnati non fidati. Le righe di diario prendono il prefisso NON FIDATO. `avvisa_operatore` passa dal limite di avvisi al cancello. Sono le stesse conseguenze di una pagina web letta: è la direzione giusta e più prudente.
  - (b) Compressione, `gas.py:1561`: il riepilogo che contiene un seguito si dichiara INPUT ESTERNO. Era già solo-forte per la chiave (`gas.py:1586`), quindi la cosa è coerente.
  - (c) `rifletti`, `gas.py:4023`: non cambia nulla. Con un seguito in finestra la riflessione esce già prima (`gas.py:4009`), senza chiamare nessun modello.
  - La funzione resta pura. `_ha_seguito_voce` controlla che il messaggio sia un dict.
  - Turni Telegram dopo un seguito: le scritture finiscono nel normale flusso di firma (parcheggio e notifica), per 10 messaggi circa. È un costo d'uso accettabile e si somma a R-683b-2-M2, già aperta.
  - Il pin non fidato non viene toccato.
  - Esito: ok.
- `modules/voice/server.py:153` — `_NON_PER_ME` accetta anche il trattino come separatore, sia tra parentesi sia nella forma nuda come risposta intera.
  - Rischio esaminato: backtracking catastrofico e falsi positivi.
  - Ogni classe di caratteri ha un solo quantificatore ed è separata da parole fisse. La forma nuda resta ancorata a `^…$`.
  - Esito: ok.
- `tests/test_unit_voice_stt.py:753` — due casi nuovi, «[non-per-me]» e «Non-per-me.», con chiusura senza voce.
  - Esito: ok (107 passed rilanciati).
- `tests/test_unit_kernel.py:11647` e `tests/test_unit_kernel.py:11653` — T103l.
  - Rischio esaminato: il test distingue davvero il fix da un diniego qualsiasi?
  - Ho costruito il mutante «controllo tolto» in una copia di scratch. T103l FAIL, quindi il mutante muore, ma a ucciderlo è SOLO il controllo diretto `_contam103l`.
  - Nel mutante `write_file` viene ESEGUITA. Viene poi negata dal percorso («Operazione negata: il percorso 'l103.txt' esce dalla root di Gas…»), quindi `cancello="negata"` e il file non esiste. La parte round-trip del test passerebbe lo stesso.
  - Esito: riserva R-684-1-M2.

**Riserve**

- R-684-1-M2 BASSA: la parte round-trip di T103l non dimostra il cancello. Accetta qualunque `"negata"`, anche il diniego del percorso. Rimedio: pretendere il testo del ramo di firma, cioè out che inizia con «Azione in attesa di approvazione umana» oppure contiene «impossibile notificare la richiesta di firma». Oppure usare un percorso che `_safe_path` accetta, così che nel mutante il file venga davvero creato.

**Wall of Shame**: nessuno slicing della storia, `_get_window()` resta in uso, nessuna simulazione di output degli strumenti. Il tetto di 10 iterazioni e la gestione delle eccezioni dei provider non sono toccati.

**Verifiche rilanciate da me**:
- Suite kernel sull'albero staged: 1084 PASS, 0 FAIL. T103j vede [CONTIENE INPUT ESTERNO], T103l passa.
- `test_unit_voice_stt.py`: 107 passed.
- Mutante in `/tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/mut`: un solo FAIL, T103l.

**Rischi esclusi**:
- Non ho rilanciato `prova_voci` e `voce_ascolto` (i 382 dichiarati comprendono anche quelli). Il diff in `server.py` è la sola regex, già coperta dai casi in `test_unit_voice_stt`.
- Non ho verificato dal vero il flusso di firma via Telegram dopo un seguito: serve il bot Telegram reale.
- V-2 MEDIA del bot (l'audio del seguito va a Groq Whisper) è fuori dal diff e la decide l'operatore.

**Memoria**: riga #684-M2 e una lezione aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate con lo script (commit 1ca1ca8). L'index staged del diff non è stato toccato.

Review #685-M2 sul commit 933780f (verdetto integrale):

## VERDETTO: APPROVATO

Review #685-M2: chat M2, branch feat/voce-v12-m2, PR #339, base ae61546. Ho letto il diff staged (3 file, +11/-4).

Ho letto prima CLAUDE.md (sez. 2, 5, 8, 9), la memoria del revisore (fino a #684-M2, con la lezione sul cancello «negata») e reports/stato_progetto.md (letto solo in parte, con grep).

Elementi del diff esaminati:

- `gas.py:914` — il commento vicino a CHIAVE_SEGUITO_VOCE ora dice che dei seguiti si occupa solo il cervello forte, che però non è mai un gratuito. Dichiara anche l'eccezione accettata dall'operatore: Groq Whisper trascrive anche l'audio dei seguiti, come tutta la voce (V-2 del bot su #339, R-684-2-M2).
  - Rischio esaminato: un commento che nasconde l'invio a un gratuito.
  - Esito: ok. Ora è scritto esplicitamente e torna con la scelta (a) dell'operatore.
- `gas.py:5155` — nel messaggio d'errore «Pipeline esausta» del turno solo-forte, «mai ai gratuiti» diventa «mai ai cervelli gratuiti».
  - Rischio esaminato: rompere T103i se il test confronta la stringa.
  - Esito: ok. T103i passa nella suite sull'albero staged.
- `modules/voice/server.py:587` — nota nel ramo seguito: la trascrizione con Groq Whisper riceve l'audio anche qui, rischio accettato il 6 nov.
  - Rischio esaminato: una modifica di comportamento nascosta.
  - Esito: ok. Nel diff cambiano solo righe di commento, nessuna riga di codice. Il file compila (py_compile).
- `tests/test_unit_kernel.py:11656` — T103l ora pretende che l'output venga dal ramo della firma: «Azione in attesa di approvazione umana» oppure «impossibile notificare la richiesta di firma». Chiude R-684-1-M2.
  - Ho controllato che le due stringhe siano quelle vere del cancello di firma in `gas.py:3465` e `gas.py:3468`.
  - Esito: ok.
- Prova del mutante, in una copia staged in scratch (mut685): ho tolto il controllo del seguito da `_finestra_e_contaminata` (`gas.py:2088`) e ho tolto dal test anche il controllo diretto `_contam103l`.
  - Risultato: 1083 PASS, 1 FAIL, ed è T103l. L'output del mutante è «Operazione negata: il percorso 'l103.txt' esce dalla root…», che il nuovo controllo sul testo scarta.
  - Ora il mutante lo uccide anche la sola parte round-trip.
- Suite kernel sull'albero staged, non mutato (st685): 1084 PASS, 0 FAIL. T103l passa sul ramo «impossibile notificare la richiesta di firma… (TELEGRAM_BOT_TOKEN mancante)».

Wall of Shame: nessun taglio diretto della storia, nessun output di tool simulato. Guardrail (tetto di 10 iterazioni, `_get_window`) non toccati.

Nota di processo, non una riserva: R-684-2-M2 va registrata in reports/stato_progetto.md come riserva ACCETTATA dall'operatore (scelta (a) via M1), insieme alla chiusura di V-2 del bot su #339. Lo fa l'agente principale.

Rischi esclusi, cioè cose che non ho verificato:

- Suite voice_stt (107 passed secondo il chiamante): non l'ho rilanciata. Il diff di server.py è solo commenti e il file compila, quindi il rischio è nullo.
- Comportamento reale di Groq Whisper e della voce sul Mac o sul VPS: non riproducibile qui, e comunque il diff non lo cambia.
- Il ramo «Azione in attesa di approvazione umana» con Telegram configurato: in dev passa solo il ramo «impossibile notificare» perché TELEGRAM_BOT_TOKEN manca. Il test accetta entrambi; non ho esercitato il primo.

Memoria: ho aggiunto la riga «#685-M2 — 2026-11-06 — APPROVATO — …» (nessuna lezione nuova) e l'ho committata con scripts/commit_memoria_revisore.sh (commit cb4dff2, solo quel file; l'index staged resta intatto).

## §5 DELTA TEST DEL MOTORE

Su 933780f: T103l (seguito in finestra → finestra contaminata, write_file al ramo della firma, non eseguita); T103j ora vede [CONTIENE INPUT ESTERNO] — suite kernel `=== RIEPILOGO: 1084 PASS, 0 FAIL ===` (nel venv della sessione; T31g fallisce solo dove manca il modulo `vectors`, anche su main); voice_stt + prova_voci + voce_ascolto `382 passed`. Mutante «controllo seguito tolto» ucciso da T103l.

Su f75719d: T103h (finestra con seguito → solo forte, chiave non inviata), T103i (forte spento → errore che spiega, nessun gratuito), T103j (riepilogo di compressione segnato), T103k (riflessione rimandata, nessun modello, nessun recap) — suite kernel `=== RIEPILOGO: 1083 PASS, 0 FAIL ===`; mutanti uccisi: instradamento, chiave nel payload, segno di compressione, skip della riflessione. voice_stt + contesto `109 passed`.

Su e7a75c0: T103f (risposta vuota effimera → final vuoto) e T103g (registra_seguito → storia e disco subito, turno normale dopo con write_file lo vede: round-trip §7) — suite kernel `=== RIEPILOGO: 1079 PASS, 0 FAIL ===`; voice_stt + prova_voci + voce_ascolto `382 passed`; voice_server + tts + contesto `136 passed`. Mutanti uccisi: registro tolto nel server, regex vecchia, ramo `elif effimero` tolto, salvataggio finto. Nota: la verifica esterna su be60a21 aveva 1076/1 per T31g, che fallisce anche su main nel suo ambiente (modulo `vectors` mancante): ambientale.

`tests/test_unit_voice_stt.py`: test V15 (pausa, seguito, «forte» dalla stanza, prefisso del segno, incerta/vuota nel seguito, chiusura del turno, strumento negato → frase fissa), «Jarvis Gas» fra i positivi. `tests/test_unit_voice_prova_voci.py`: +1 (`test_v15_conferma_errore_recente_non_richiama_elevenlabs`). `tests/test_unit_kernel.py` T103a-e (round-trip §7 del turno effimero; T103b controlla `strumento_negato`). `tests/test_unit_voce_ascolto.py` (chat Mani): solo `**kw` sui due finti, autorizzato da M1. Mutanti su gas.py (storia non ripristinata, strumenti offerti, strumento eseguito, salvataggio, forte non forzato) uccisi da T103. Esecuzione sull'head 4ee1feb, nel venv con requirements + requirements-dev: voice_stt + voice_prova_voci + voce_ascolto `380 passed in 77.91s`; su 2e367e2 (+`test_v15_seguito_pausa_senza_voce`, varianti in coda) `381 passed in 77.90s`, mutanti «coda tolta» e «ramo seguito tolto» uccisi (1 failed ciascuno); suite kernel `=== RIEPILOGO: 1077 PASS, 0 FAIL ===` (prima della sessione 1076).

## §6 STATO CI

`gh` non autenticato nel cloud: run lette con l'integrazione GitHub.
- 04532a3, 8c9bc1b, 2d2d432: nessuna run su questi SHA da soli.
- 5cf7267: CI failure (run 42127434430; superata dai commit successivi).
- b0405dc: CI success (run 42127632662); verifica-bot FAILURE nel verdetto (MEDIA: storia del seguito, strumenti attivi).
- 061334c, bb731b2: nessuna run su questi SHA da soli (pushati con 3581f6f).
- 3581f6f: CI success (run 42128563229); verifica-bot con la stessa MEDIA.
- bad216f, aa1babe, fd64e77: nessuna run su questi SHA da soli (pushati con a87d273).
- a87d273: CI success (run 42133629442), verifica-bot success (run 42133634353) con verdetto testuale V-1 (a)/(b) MEDIA e verifica esterna con V-2.
- 2530577, 10dc900, fd1b320, 4899032, 4ee1feb: nessuna run su questi SHA da soli (pushati con 312cd86).
- 312cd86: verifica-bot FAILURE per falso positivo del parser (verdetto testuale: V-1/V-2 BASSE, V-3 COSMETICA; «ad alta voce» letto come ALTA); CI in corso alla lettura.
- 93ee68d, 2e367e2: nessuna run su questi SHA da soli (pushati con be60a21).
- be60a21: verifica-bot FAILURE per la MEDIA V-1 (punto 1, allora aperto); verifica esterna con la stessa MEDIA.
- 390785b, e7a75c0: nessuna run su questi SHA da soli (pushati con d38f95d).
- d38f95d: verifica-bot FAILURE per la MEDIA R-682-1 (allora aperta).
- be724e6, 41c3275, f75719d: nessuna run su questi SHA da soli (pushati con 16dd4a5).
- 16dd4a5: verifica-bot FAILURE (BOCCIATO: V-1 e V-2 MEDIA, chiuse sopra); verifica esterna APPROVATO CON RISERVE (solo BASSE).
- 1ca1ca8, ae61546, cb4dff2, 933780f e commit di fine-task che contiene questo file: run non ancora disponibile (pushati insieme).

## §7 RISERVE APERTE

- R-684-2-M2 ACCETTATA dall'operatore (6 nov, via M1): la trascrizione Groq Whisper (servizio gratuito) riceve anche l'audio dei seguiti, come tutta la voce.
- Verifica esterna su 16dd4a5, BASSE: V-3 il parlato «per Gas» resta in chiaro in .gas_history.json (rischio residuo, coerente col punto 1); V-1/V-2 chiuse in ae61546.
- R-682-1-M2 e R-682-2-M2: chiuse in f75719d. R-683-1-M2 (recap nel pin): chiusa (nessun recap con seguito in finestra). R-683-2-M2: chiusa (l'errore spiega).
- R-683b-1-M2 BASSA: con `clear` la riflessione di un task con un seguito in finestra si perde (non «rimandata»).
- R-683b-2-M2 BASSA: dopo un seguito, i turni normali (anche da Telegram) spendono il budget del forte finché il seguito è negli ultimi ~10 messaggi; col forte spento restano fermi con errore dichiarato.
- R-682-3-M2 BASSA: il seguito si registra prima della sintesi vocale.
- Parser del bot: «ad alta voce» in un finding BASSA è letto come gravità ALTA (`_FINDING_GRAVE_A_PAROLE`, case-insensitive) → FAILURE falso su 312cd86. Fetta separata sulla macchina del bot, decide l'operatore.
- R-681-1-M2 BASSA: «Fatto. [NON_PER_ME]» (segno in coda per errore) tace una risposta vera; verso sicuro.
- R-681-2-M2 COSMETICA: pausa nel seguito in JSON anche con audio+pezzi; il client decide da X-Gas-Comando.
- V-3 bot su 312cd86 COSMETICA: con lo strumento negato il diario scrive turno_fine esito=ok.
- R-678-1-M2 BASSA: che il modello rispetti l'istruzione «niente strumenti» si vede solo dal vero.
- R-678-2-M2 COSMETICA: «ricordare» ambiguo nell'istruzione.
- R-679-1-M2 BASSA: test d'errore di Mani verdi anche con eccezioni impreviste (chat Mani).
- R-679-2-M2 BASSA: manca il lato client della V15 (`X-Gas-Seguito`, `X-Gas-Comando`; chat Mani via M1).
- R-680-1-M2 BASSA: nel seguito una frase della stanza scambiata per richiesta d'azione fa parlare Gas con la frase fissa.
- R-680-2-M2 BASSA: testo scritto dal modello insieme a una chiamata a strumento resta scartato (comportamento preesistente).
- R-676-1-M2: chiusa per la forma con parentesi (anche con spazi); «NON_PER_ME (…)» senza parentesi con aggiunte resta una risposta.
- R-675-2-M2 BASSA: oltre il tetto orario «pausa» riceve 429; i turni ambientali consumano il tetto.
- R-675-4-M2 COSMETICA: «basta così?» come domanda chiude la conversazione; «forte, pausa» va al forte.
- R-675-5-M2 BASSA: forte spento → turni di seguito 500 (il client deve chiudere); forte acceso → ogni frase captata spende il budget del forte.
- Da verificare lato client (Mani): JSON (non NDJSON) nella risposta «fine» col formato audio+pezzi.
