# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — chat Mani, fetta 45: riserve BASSE della #341 e della #347 (voce H24)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 45 (il numero e l'URL vengono dalla risposta dello strumento GitHub `create_pull_request`): review APPROVATO CON RISERVE e PR nel perimetro, quindi decide l'operatore via M1.

---

## §1 SCOPE & ESITO FETTE

- **PR #348**: `FATTA` — mergiata (53ae39b) col sì dell'operatore.
- **Fetta 45 — riserve della #341 e della #347**: `FATTA`. R-676-1, R-681-1, R-679-3, R-707-3, R-708-1, V-3 e V-1/V-2 del bot #347, V-1 del bot su b48a0a8.
- **V-1 della verifica esterna #347 (tolleranza dopo una parola sentita prima della voce)**: `SALTATA — scelta, R-708-2: aiuta quasi solo i falsi positivi e allarga la privacy (sonda del revisore #707)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 clients/voice/ascolto.py           |  36 +++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  15 +++++++--------
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  24 ++++++++++++------------
 scripts/voce/LEGGIMI.md            |  16 +++++++++++-----
 tests/test_unit_voce_ascolto.py    |  75 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 53ae39b (dopo il merge della PR #348).

## §3 GIT LOG --ONELINE (sessione)

```
06088cb Merge fetta 45 (riserve della #341 e della #347, voce) — review #707–#709, unione #713 APPROVATO
d711cc6 fix(voce): fetta 45 — riserve della #341 e della #347 (log del rilevatore e della pausa, avviso sulla finestra, LEGGIMI «Hey Gas» NO, test R-676-1) — review #707–#709
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. La fetta è stata scritta e revisionata nel worktree locale /tmp/claude-0/wt45 (base c523a04), poi unita a main (fra c523a04 e 53ae39b main non ha toccato i tre file di codice: verificato nella review #713).

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #707 (prima versione, con la tolleranza poi tolta), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #707 (chat Mani). Worktree /tmp/claude-0/wt45, branch mani/fetta45, base main c523a04, diff staged non committato. Ho letto CLAUDE.md, reports/stato_progetto.md (voci fetta 43 parte 2 e fetta 44) e la memoria del revisore.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:732` — conversazione() passa `dopo_parola=self.parola_nella_finestra` a registra(). Rischio: più audio inviato o tempi di registrazione più lunghi rispetto a main, nel caso del falso positivo. Esito: **riserva** (R-707-1 e R-707-2, sotto). La sonda è più avanti.
- `clients/voice/ascolto.py:482` — il tetto R-702-1 (`dal_la_parola >= max_attesa`) vale anche per il percorso nuovo. Rischio: una tolleranza senza fine. Esito: **ok**. Il tetto tiene: con i clic la registrazione arriva al massimo a 5,2 s. Il tetto però conta dall'inizio di registra e non dalla parola: fino a circa 2 s in più (PAROLA_VALIDA_S).
- `clients/voice/ascolto.py:420` — R-681-1: scrive un log.warning al 1°, 101°, 201°… errore; il contatore `_errori_parola` non si azzera mai. Rischio: log pieno, o nessun log. Esito: **ok**. Al massimo una riga ogni circa 8 s con un rilevatore sempre rotto (12,5 blocchi al secondo), e l'errore resta «no» (§9).
- `clients/voice/ascolto.py:555` e `clients/voice/ascolto.py:607` — R-679-3: con `comando == "pausa"` scrive un info invece del warning. Rischio: un errore vero che sparisce. Esito: **riserva** (R-707-3). `modules/voice/server.py:466` aggiunge X-Gas-Comando in ogni risposta (`end_headers`). Se il server risponde 500 con «pausa» (per esempio il TTS di «Va bene.» fallisce dopo la parola), `invia_al_server` restituisce `(False, None, "HTTP 500", "pausa")` e ora il log dice solo «pausa a voce: chiudo la conversazione in silenzio», senza il motivo. In più `clients/voice/ascolto.py:549` scrive già una riga info quasi uguale, quindi nel log ci sono due righe di pausa.
- `clients/voice/ascolto.py:214` — `_finestra_dall_ambiente()`: valore corretto con `_numero`, avviso se il valore letto è diverso. Rischio: falsi avvisi, oppure crash con un valore non numerico. Esito: **ok**. "abc" e "" non danno avviso, "300" e "-5" sì. Nota COSMETICA: "inf" e "nan" tornano a 40 senza avviso, per via di `isfinite`. Chiamata a `clients/voice/ascolto.py:1118`.
- `scripts/voce/LEGGIMI.md:42` — il controllo dell'eco vale solo col formato a frasi. Verificato sul codice: con un MP3 intero `pezzi` è un list_iterator senza `testo`, quindi l'interruzione resta accesa. Esito: **ok**.
- `scripts/voce/LEGGIMI.md:47` — «Hey Gas» non si fa, decisione dell'operatore del 7/11, con rimando a `reports/proposta_parola_gas.md`. Esito: **riserva COSMETICA** (R-707-4). Il documento citato e reports/stato_progetto.md non contengono questa decisione: la proposta dice ancora «Se si va avanti con Hey Gas…». Per CLAUDE.md §3 le decisioni vanno scritte nel repo.
- `scripts/voce/LEGGIMI.md:100` — limiti del controllo di riprendi.sh (primi 3 s). Esito: **ok**, testo onesto.
- `tests/test_unit_voce_ascolto.py:2410` (R-676-1), `tests/test_unit_voce_ascolto.py:2420`, `tests/test_unit_voce_ascolto.py:2432`, `tests/test_unit_voce_ascolto.py:2455`, `tests/test_unit_voce_ascolto.py:2467` — i test nuovi. Esito: **ok**. Sulla copia dell'index: 291 passed. Ho rifatto due mutanti e sono presi entrambi:
  - `dopo_parola=False`: 1 fail, quello di :2420.
  - `self.chiudi` non azzerato in turno(): 2 fail.

**Sonda contro main** (copie in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/main e …/staged; script in …/scratchpad/sonda/sonda.py e sonda2.py). Secondi inviati nel turno dopo la finestra:

| Caso | main | staged |
|---|---|---|
| A: falso positivo, 3 blocchi di stanza, pausa 2 s, 1,6 s di stanza | 1,04 s normale + 2,4 s di seguito (passa dal filtro [NON_PER_ME]) | 4,64 s, tutto in un turno normale senza filtro |
| B/C: falso positivo + clic ogni 1 s o 4 s | 1,04 s | 5,2 s (si ferma al tetto) |
| D: parlato continuo di 10 s | 10,8 s | 10,8 s (uguale) |
| F: stanza a raffiche con pause di 1,2 s | 1,12 + 4×1,12 di seguito | 2,64 + 3×1,12 |
| G: parola vera forte che scatta al 4° blocco + pausa 1,5 s | 4,24 s | 4,24 s (identico: passa da registra, già in main) |
| G2: parola che scatta al 1° blocco | spezzata | richiesta unica |
| G4: pausa di 6 s dopo la parola | 1,12 s | 5,2 s di silenzio, poi la voce va come seguito |

Risposta alla domanda «più audio o tempi di registrazione rispetto a main?»: sì, solo quando la parola, vera o falsa, si sente PRIMA che la voce si apra, ed entro il tetto di circa 5 s. Il parlato continuo non cambia.

**Riserve**
- **R-707-1 BASSA**: il percorso nuovo scatta soprattutto sui falsi positivi. Il rilevatore vero (openWakeWord) scatta a fine parola, quindi con «Hey Jarvis» detto forte la voce si apre prima e si passa da registra, come in main (caso G). Il caso «falso positivo prima del parlato della stanza» aggiunge fino a circa 5 s di stanza al turno normale, che salta il filtro. Nel caso A, 3,6 s che in main passavano dal filtro come turno di seguito. È lo stesso meccanismo già in main per il percorso da registra (#702/#703) e rientra nella natura di R-694-1/R-695-2, accettati dall'operatore. Però il riassunto accettato parla di «circa 2 s di parlato della stanza senza filtro»: va dichiarato all'operatore come estensione. Aggiunta: il tetto parte da registra e non dalla parola, quindi fino a circa 7 s dalla parola.
- **R-707-2 BASSA** (= R-702-2): anche qui la coda della parola, almeno 3 blocchi forti dopo l'apertura della voce, consuma la tolleranza (caso G3: richiesta spezzata in staged come in main). Il guadagno reale di V-1 ve #347 va provato sul Mac insieme a R-694-2.
- **R-707-3 BASSA**: «pausa» insieme a un errore HTTP perde il motivo nel log (`clients/voice/ascolto.py:555`). Rimedio: tenere `motivo` nella riga info quando c'è, oppure ridurre a info solo il caso muto (`ok` vero e risposta vuota). In più c'è la riga doppia con `clients/voice/ascolto.py:549`.
- **R-707-4 COSMETICA**: la decisione «Hey Gas no» del 7/11 va scritta in reports/proposta_parola_gas.md e/o in reports/stato_progetto.md. Inoltre "inf" e "nan" in GAS_VOICE_FINESTRA non danno avviso.

**Cosa non ho verificato**
- Comportamento sul Mac con openWakeWord vero (latenza dello scatto, R-694-2): non riproducibile in dev, la sonda usa un rilevatore finto. Quindi non so quanto spesso la parola vera arrivi prima dei 3 blocchi di voce.
- Il server vero che risponde 500 con l'intestazione «pausa»: dedotto dal codice di `end_headers`, non provato end-to-end.
- Gli altri 3 mutanti dichiarati dall'agente (log del rilevatore, log della pausa, avviso della finestra): non rifatti.

**Memoria**: riga #707 e due lezioni aggiunte in coda a /tmp/claude-0/wt45/.claude/agents/memoria_revisore.md. Il file non è committato, come da istruzioni, e l'index non è stato toccato (copia con checkout-index, niente stash). In memoria non c'era già una #706 né una #707.

Review #708 (ri-review), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #708 (chat Mani). Ri-review della #707 sul diff staged del worktree /tmp/claude-0/wt45 (base main c523a04). Ho letto prima CLAUDE.md, la coda di stato_progetto e la memoria del revisore.

**Cosa ho esaminato nel diff**
- clients/voice/ascolto.py:447 — `dopo_parola` ora è solo la variabile locale che c'era già in main dentro registra(). Il diff non tocca più registra(), aspetta_voce() né conversazione(). Rischio: che restasse un pezzo della tolleranza tolta. Esito: ok. Il grep trova `dopo_parola` solo a :447-491 (codice di main) e in nessun test. R-707-1 e R-707-2 sono chiuse, perché il percorso non c'è più.
- clients/voice/ascolto.py:555 — `if not (comando == "pausa" and ok)`. Rischio: perdere il motivo quando «pausa» arriva insieme a un errore HTTP. Esito: ok.
  - Pausa muta (ok=True, risposta None): c'è solo la riga info di :549, nessun warning.
  - Pausa con 500 (ok=False): il warning resta, col motivo.
  - Eccezione in invio: `comando` resta "" e il warning si scrive.
  - Il mutante `if comando != "pausa":` a :555 viene preso: 1 test fallito, test_pausa_con_errore_tiene_il_motivo_nel_log a tests/test_unit_voce_ascolto.py:2453.
  - R-707-3 è chiusa.
- clients/voice/ascolto.py:605 — `if comando != "pausa"` nel ramo «suonati == 0»: niente più riga doppia per la pausa. Rischio: il ramo non è coperto dai test. Esito: riserva (R-708-1). Ho provato il mutante `if True:`: il warning «senza voce» torna anche per la pausa e la suite resta a 291 passed, quindi nessun test lo prende. test_pausa_nel_seguito_non_e_un_errore_nel_log (tests/test_unit_voce_ascolto.py:2443) usa risposta None e quindi si ferma nel ramo di :555.
- tests/test_unit_voce_ascolto.py:2443 — il test controlla che «pausa a voce: chiudo la conversazione» compaia una sola volta e che non ci siano «non riuscito» né «senza voce». Esito: ok per il ramo di :555.
- clients/voice/ascolto.py:214 — `_finestra_dall_ambiente`: avvisa solo se il valore è un numero finito fuori da 0–120. Esito: ok (comportamento invariato dalla #707). Restano inf/nan senza avviso, che è la parte COSMETICA già nota di R-707-4.
- scripts/voce/LEGGIMI.md:47 — cita la decisione «Hey Gas no» e reports/proposta_parola_gas.md. Rischio: il riferimento non è ancora in main. Esito: riserva cosmetica, aperta finché la PR #348 non entra.
- scripts/voce/LEGGIMI.md:101 — il limite dei 3 secondi di riprendi.sh. Esito: ok, solo documentazione.

**Verifiche eseguite**
- Copia dell'index fatta con checkout-index in scratch, senza stash: tests/test_unit_voce_ascolto.py dà 291 passed.
- Mutante su :555: preso. Mutante su :605: NON preso.

**Riserve**
- R-708-1 BASSA: manca un test per il ramo «suonati == 0» con «pausa» (clients/voice/ascolto.py:605). Serve un finto che risponda ok=True con pezzi tutti vuoti (es. `[b""]`) e comando «pausa». Il test deve controllare che la riga «pausa a voce» compaia una volta e che «senza voce» non ci sia.
- R-708-2 BASSA: la V-1 della verifica esterna #347 resta NON corretta, per scelta. Va dichiarata in reports/stato_progetto.md a fine task, col motivo: il guadagno vale quasi solo per i falsi positivi e allarga l'esposizione della privacy.
- R-707-4 COSMETICA (resta aperta): la decisione «Hey Gas no» sarà in main solo quando entra la PR #348. Restano anche inf/nan in GAS_VOICE_FINESTRA, che tornano a 40 senza avviso.

**Cosa NON ho verificato**
- La suite completa: ho lanciato `pytest tests` in background ma non ho atteso l'esito. Ho verificato solo tests/test_unit_voce_ascolto.py. Il tuo dato «291 passed» coincide con quel file da solo.
- Il comportamento reale sul Mac (microfono, openWakeWord, server voce): non si riproduce in questo ambiente.

**Memoria**
- Riga #708 aggiunta in coda a /tmp/claude-0/wt45/.claude/agents/memoria_revisore.md, non committata come richiesto, con una lezione nuova: quando la correzione tocca due rami gemelli, va provato un mutante su ciascun ramo.
- Non ho lanciato commit_memoria_revisore.sh, perché il file deve restare non committato nel worktree.

**File rilevanti**
- /tmp/claude-0/wt45/clients/voice/ascolto.py
- /tmp/claude-0/wt45/tests/test_unit_voce_ascolto.py
- /tmp/claude-0/wt45/scripts/voce/LEGGIMI.md
- /tmp/claude-0/wt45/.claude/agents/memoria_revisore.md
- Copia dell'index usata per test e mutanti: /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/r708

Review #709 (test di R-708-1), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #709 (chat Mani). Breve ri-review della #708 sul diff staged in /tmp/claude-0/wt45, base main c523a04. R-708-1 è chiusa. Restano solo le due riserve già note dalla #708 (sotto).

**Cosa ho esaminato**
- tests/test_unit_voce_ascolto.py:2472: il nuovo test test_pausa_senza_audio_suonabile_non_e_un_errore_nel_log. Ho controllato che passi davvero dal ramo «niente suonato»: sì.
  - La lista `[b""]` non è vuota, quindi non entra nel ramo d'errore di clients/voice/ascolto.py:553.
  - Il pezzo vuoto viene saltato da `if not audio: continue` a clients/voice/ascolto.py:577, quindi `suonati` resta 0 e il turno arriva al ramo di clients/voice/ascolto.py:605.
  - Il test controlla tre cose: la riga «pausa a voce» compare una volta sola, non c'è nessun «senza voce», `f.tipi == ["parola", "seguito"]` e `f.bip == ["ok"]`.
  - Esito: ok.
- clients/voice/ascolto.py:605: il mutante `if True:` su questa riga ora viene preso (1 fallito, proprio il nuovo test). Esito: ok.
- Nient'altro è cambiato. Ho estratto l'index in una copia nuova e l'ho confrontata con `diff -r` con la copia della #708: l'unica differenza è il test aggiunto, a parte la cache. clients/voice/ascolto.py e scripts/voce/LEGGIMI.md sono identici. Esito: ok.

**Verifiche eseguite**
- tests/test_unit_voce_ascolto.py sulla copia dell'index: 292 passed.

**Riserve ancora aperte**
- R-708-2 BASSA: la V-1 della verifica esterna #347 resta non corretta, per scelta. Va scritta in reports/stato_progetto.md a fine task, con il motivo: il guadagno riguarda quasi solo i falsi positivi e aumenta l'esposizione della privacy.
- R-707-4 COSMETICA: la decisione «Hey Gas no», citata in scripts/voce/LEGGIMI.md:47, entra in main solo con la PR #348. Restano anche inf/nan in GAS_VOICE_FINESTRA, che tornano a 40 senza avviso.

**Cosa NON ho verificato**
- La suite completa: ho lanciato solo tests/test_unit_voce_ascolto.py. Sul tuo «292 passed» per la suite completa mi fido del tuo dato.
- Il comportamento reale sul Mac (microfono, openWakeWord): non si può riprodurre in questo ambiente.

**Memoria**
- Ho aggiunto la riga #709 in coda a /tmp/claude-0/wt45/.claude/agents/memoria_revisore.md, senza committarla. Nessuna lezione nuova.
- La copia dell'index usata è in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/r709.

**File rilevanti**
- /tmp/claude-0/wt45/tests/test_unit_voce_ascolto.py
- /tmp/claude-0/wt45/clients/voice/ascolto.py
- /tmp/claude-0/wt45/scripts/voce/LEGGIMI.md
- /tmp/claude-0/wt45/.claude/agents/memoria_revisore.md

Review #713 (unione con main dopo la #348), verdetto integrale:

## VERDETTO: APPROVATO

Review #713 (chat Mani). Oggetto: il merge staged di mani/fetta45 (d711cc6, fetta 45 voce, già revisionata nelle review #707, #708 e #709 su base c523a04) dentro claude/peaceful-lovelace-0w2b7q. HEAD è 53ae39b, cioè origin/main dopo la PR #348. MERGE_HEAD è d711cc6 e la merge-base è c523a04.

Elementi del diff esaminati:
- `clients/voice/ascolto.py:214` — `_finestra_dall_ambiente()` riporta GAS_VOICE_FINESTRA nei limiti 0–120 e scrive un avviso nel log se il valore è fuori. Rischio esaminato: crash con NaN o testo non numerico. `math.isfinite` protegge il NaN e un ValueError fa tornare il valore corretto; `math` è importato (`clients/voice/ascolto.py:63`) e la funzione viene chiamata da `main()` (`clients/voice/ascolto.py:1113`). Esito: ok.
- `clients/voice/ascolto.py:419` — il contatore `_errori_parola` scrive nel log il primo errore del rilevatore e poi uno ogni 100. Il ritorno resta `False`, quindi un errore vale «no» come prevede la regola §9. Rischio esaminato: log che si riempie e crash. Esito: ok.
- `clients/voice/ascolto.py:555` — per la pausa muta (`comando == "pausa" and ok`) il warning sparisce. Un errore vero continua a scrivere il suo motivo (R-707-3) e `chiudi = True` resta senza condizioni. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2420` — test che verifica la traccia nel log quando il rilevatore è rotto nella finestra. `tests/test_unit_voce_ascolto.py:2453` copre la pausa con errore, che deve tenere il motivo nel log. `tests/test_unit_voce_ascolto.py:2464` è il test parametrizzato sulla finestra fuori dai limiti. Esito: ok.

Controlli richiesti:
1. **I tre file nell'index sono identici a mani/fetta45.** Ho confrontato i blob:
   - ascolto.py: c5c7147
   - LEGGIMI.md: 1d4a563
   - test_unit_voce_ascolto.py: 1e1fd52

   A HEAD gli stessi tre file hanno i blob di c523a04 (1419a29, 4d6b4c8, e03624d). `git diff --stat c523a04 53ae39b` su questi tre file è vuoto. Quindi il diff contro HEAD è esattamente quello già revisionato nelle review #707–#709.
2. **Memoria senza perdite.** Nessuna riga persa né del lato HEAD (#706, #710) né del lato fetta (#707, #708, #709 con le loro lezioni). L'unica riga in più dell'index rispetto ai due lati è una riga vuota, effetto del confronto con sort/uniq, non un contenuto nuovo.
3. **Nessun marcatore.** `git diff --cached --check` è pulito, `git ls-files -u` è vuoto (nessun conflitto rimasto aperto) e la ricerca di `<<<<<<<` nell'index non trova niente.
4. **Test.** Su una copia dell'index (`git checkout-index` nello scratchpad), `tests/test_unit_voce_ascolto.py` dà **292 passed**. Non ho usato stash: `git stash list` è vuoto.

Guardrail: il diff non tocca gas.py, la finestra della storia (`_get_window`) né il tetto di 10 iterazioni. Nessuna simulazione di output dei tool, nessuno slicing della history. Coerente con «zero crash».

Rischio escluso: non ho rieseguito la parte semantica della fetta 45, cioè le sonde temporali e i mutanti delle review #707–#709. Il contenuto è identico per blob a quello già revisionato, quindi qui ho verificato solo l'integrità del merge. Non ho verificato nemmeno il comportamento reale sul Mac, con microfono e openWakeWord: non è riproducibile in questo ambiente. Le riserve aperte delle review #707–#709 restano come erano.

Memoria: ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga `#713 (chat Mani) — 2026-11-07 — APPROVATO — … Nessuna lezione nuova.`. È solo nel working tree e non è committata, come mi hai chiesto: non ho lanciato `scripts/commit_memoria_revisore.sh`, che comunque durante un merge in corso non può fare un commit parziale. Lo stato del file ora è `MM`: devi metterlo in staging (`git add`) prima di chiudere il merge, altrimenti la riga #713 resta fuori dal commit.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 283 (main) a 292 casi. Riepilogo reale:

```
292 passed in 29.05s
```

Mutanti presi:
- `chiudi` non azzerato;
- niente log del rilevatore;
- log della pausa (ramo d'errore e ramo «niente suonato»);
- niente avviso sulla finestra.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Per 06088cb e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff. PR #348 su 4f70927: unit-suite, handoff-check, verifica success; mergiata.

## §7 RISERVE APERTE

- R-708-2 BASSA: la V-1 della verifica esterna #347 resta non corretta, per scelta (motivo in §1).
- R-707-4 COSMETICA: con «inf» o «nan» in GAS_VOICE_FINESTRA il valore torna a 40 senza avviso.
- Bot #348 su 4f70927, tutte sulla proposta Telegram e da sistemare nella PR della fetta 1 Telegram:
  - V-1 BASSA: «sendAudio funziona già»;
  - V-2 BASSA: decisione dell'operatore non scritta in cima alla proposta;
  - V-3 BASSA: il ramo del vocale va dopo il controllo delle chat autorizzate (il codice della fetta 1 lo fa già);
  - V-4 COSMETICA: §6.
- Restano R-702-2, R-694-2, R-678-1, R-677-3 e le riserve precedenti in `reports/stato_progetto.md`.
