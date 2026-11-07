# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — chat Mani, fetta 44: riserve dell'ascolto H24, proposta «Hey Gas» e riserve della PR #341 (PR nuova, numero dalla risposta di `create_pull_request`)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 44: le review #702 e #703 sono APPROVATO CON RISERVE (solo BASSE) e la PR è nel perimetro, quindi decide l'operatore tramite M1.
2. Parola di attivazione «Hey Gas» (reports/proposta_parola_gas.md): l'addestramento si può fare (circa 1 ora su Colab, nessun cambio di codice). Restano aperte la licenza dei dati negativi (probabilmente CC BY-NC-SA) e il supporto dell'italiano. Decidere se procedere e se aggiungere il verificatore personale (3–5 registrazioni della tua voce).

---

## §1 SCOPE & ESITO FETTE

- **PR #341 (fetta 43 parte 2)**: `MERGIATA` (c1a4503) il 2026-11-07 con CI verde, col sì dell'operatore via M1 e il rischio R-694-1/R-695-2 accettato.
- **Fetta 44 — riserve BASSE dell'ascolto**: `FATTA`.
  - riprendi.sh controlla che l'ascolto resti acceso;
  - pausa.sh dice «non installato»;
  - V-2/V-3/V-4 della #341;
  - eco quando Gas dice «Hey Jarvis».
  - Review #677/#678 sulla base vecchia; unione con main e ri-review in #702/#703.
- **Proposta «Hey Gas»**: `FATTA` (documento, nessun codice).
- **Riserve della #341 chieste da M1**: `FATTE`.
  - Finestra 0–120, come la pagina web (V-1 del bot su a269c12).
  - La parola nella finestra fa ripartire i turni (V-2 del bot su a269c12).
  - Pausa dopo la parola nella finestra tollerata fino a 5 s, con tetto (V-1 del bot su 179d05c, R-702-1).
  - LEGGIMI corretto (frase del bip, 0 = niente finestra).
- **R-702-2 (coda della parola che consuma la tolleranza)**: `DEFERITA — BASSA, dipende dalla latenza reale di openWakeWord, da provare sul Mac`.

---

## §2 GIT DIFF -- .claude/agents/memoria_revisore.md |   7 +++
 clients/voice/ascolto.py           | 121 ++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  20 +++---
 reports/proposta_parola_gas.md     | 156 +++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   5 +-
 reports/ultimo_report.md           |  80 +++++------------------
 scripts/voce/LEGGIMI.md            |  14 +++--
 scripts/voce/pausa.sh              |   7 +++
 scripts/voce/riprendi.sh           |  60 ++++++++++++++----
 tests/test_unit_voce_ascolto.py    | 226 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 reports/handoff.md                 | n/d (sessione)

```
STAT
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main c1a4503 (dopo il merge della PR #341).

## §3 GIT LOG --ONELINE (sessione)

```
8133c60 feat(voce): fetta 44 — riserve dell'ascolto, proposta «Hey Gas» e riserve della PR #341 (finestra 0–120, turni dopo la parola, pausa dopo la parola con tetto) — review #702/#703
50d6785 feat(voce): fetta 44 — riserve basse dell'ascolto e proposta della parola «Hey Gas»
48f5ffa chore(revisore): memoria review #678 — APPROVATO CON RISERVE
b97c355 chore(revisore): memoria review #677 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Fetta 44 sulla base vecchia (worktree /tmp/claude-0/wt44) — review #677, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #677 (chat Mani), fetta 44. Ho esaminato `git diff --cached` nel worktree /tmp/claude-0/wt44 (base a7ed0e8, 6 file). Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md e la memoria del revisore. La suite gira su una copia dell'index in scratch: **262 passed**.

**Elementi del diff esaminati**
- `scripts/voce/riprendi.sh:12` — `gira()` è `launchctl print | grep -q "state = running"` con `set -o pipefail`. Rischio: grep -q si chiude al primo match, il SIGPIPE che arriva a launchctl rende falsa tutta la pipeline. L'ho riprodotto in scratch: un finto che continua a scrivere dopo il match dà rc=141, cioè un falso «non gira». È la stessa trappola già chiusa in `scripts/voce/installa.sh:176` (R-615-7: lì l'output si salva prima e si usa case). Esito: **riserva R-677-1, MEDIA**. Il caso è poco probabile con un output corto, ma ricade su due punti: lo script dice «non resta acceso» ed esce 1 mentre Gas ascolta, oppure non riconosce un ascolto già acceso. Correzione di una riga: `STATO="$(launchctl print "$DOMINIO/$S" 2>/dev/null || true)"` più `case *"state = running"*`. Consiglio di farla in questa fetta.
- `scripts/voce/riprendi.sh:24` e `scripts/voce/riprendi.sh:32` — attesa dell'uscita (50×0,1 s), poi tre bootstrap; solo l'ultimo lascia visibile lo stderr; dopo `sleep 3` (`scripts/voce/riprendi.sh:46`) ricontrolla. Su bash 3.2 regge: `seq`, `sleep 0.1` e `{ …; break; }` ci sono tutti. Il caso venv rotto è coperto (`tests/test_unit_voce_ascolto.py:2172`). Esito ok, con **riserva R-677-2 BASSA**: se il servizio è già caricato ma cade di continuo PRIMA di riprendi, ora non dice più «già ascoltando» (bene). Però aspetta 5 s, fallisce 3 bootstrap e consiglia «rilancia riprendi.sh», che non serve, invece di indicare il log. Nessun test copre questo caso. Limite dichiarato: un crash che arriva dopo più di 3 s (caricamento del modello, permesso del microfono) dà comunque «RIPRESO».
- `scripts/voce/pausa.sh:16` — senza plist e senza servizio caricato risponde «non è installato» ed esce 0 senza bootout. Plist mancante ma servizio caricato: fa il bootout come prima. Esito ok.
- `clients/voice/ascolto.py:105` e `clients/voice/ascolto.py:493` — la regex con `\b` lascia fuori «Jarvisiano» e prende «ehi Gas». Il controllo sta DOPO `next(pezzi)`, cioè dopo che `_Frasi` ha letto la prima riga con «content» (`clients/voice/ascolto.py:709`). `iter(_Frasi)` restituisce l'oggetto stesso, quindi `getattr(pezzi, "testo")` e il `close()` a riga 508 funzionano. Privacy: nel log c'è solo un messaggio fisso, mai il testo. §9: un `content` che non è stringa viene ignorato. Il generatore mai avviato non chiude `r` come prima: nessuna regressione. Esito ok.
- `tests/test_unit_voce_ascolto.py:684` — test dell'eco. **R-677-3 COSMETICA**: `Risp` ha `testo` già impostato all'inizio, quindi il test non prova che il controllo stia dopo `next()`. Lo prova solo in parte `test_frasi_ndjson_tengono_il_testo` (testo vuoto prima dell'iterazione).
- Il launchctl finto (ASCOLTO_CADE, `state = exiting`) è coerente con il launchd vero. I test di installa.sh restano verdi.
- reports/proposta_parola_gas.md: coerente, fuori perimetro. Dichiara cosa non è verificato e dice che nessun codice cambia.

**Cosa non ho verificato**
- Il comportamento reale di `launchctl print` e bootstrap su macOS (dimensione dell'output, stato durante il ThrottleInterval, codice di «Bootstrap failed»): non si riproduce su Linux, ho solo il finto.
- Non ho rifatto gli 11 mutanti dichiarati, ho controllato solo che i test relativi ci siano.

**Memoria**: riga #677 e una lezione (grep -q con pipefail, da confrontare con R-615-7) aggiunte in .claude/agents/memoria_revisore.md e committate da sole (b97c355). Lo staged è intatto: 6 file, 399+/43-.

**Riserve da tracciare in stato_progetto.md**: R-677-1 MEDIA (correzione consigliata prima del commit), R-677-2 BASSA, R-677-3 COSMETICA.

Ri-review #678, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #678 (chat Mani): ri-review della fetta 44 nel worktree /tmp/claude-0/wt44, sul diff staged (6 file, +428/−44). Ho letto la memoria del revisore (riserve della #677) e la sezione 5 di CLAUDE.md. Il diff non tocca la history né i provider, quindi nessun antipattern del Wall of Shame.

Righe esaminate:
- `scripts/voce/riprendi.sh:14` — la funzione `gira()` salva l'output di `launchctl print` in una variabile `local` (con `|| true`) e lo controlla con `case *"state = running"*`. Rischio: il SIGPIPE con pipefail (R-677-1). L'ho riprovato in una copia con un finto launchctl che scrive 20000 righe dopo il match: rc=0, cioè nessun falso «non gira». `local` dentro una funzione e `case` con glob quotato valgono anche su bash 3.2. Esito: ok, **R-677-1 chiusa**.
- `scripts/voce/riprendi.sh:43` — `[ "$ANDATO" = si ] || cade`: se il servizio è ancora caricato dopo 5 s, lo script rimanda al log invece di fare tre bootstrap inutili. Rischio: il controllo è davvero coperto dai test? Il mutante che lo sostituisce con `true` viene preso da `test_riprendi_con_ascolto_che_cade_di_continuo` (1 failed). Esito: ok, **R-677-2 chiusa**.
- `scripts/voce/riprendi.sh:19` — `cade()` fa `exit 1` ed è usata anche dopo il controllo dei 3 s (riga 67). Rischio: comportamento cambiato rispetto alla #677? Il messaggio e l'uscita sono gli stessi e `test_riprendi_controlla_che_l_ascolto_resti_acceso` passa. Esito: ok.
- `tests/test_unit_voce_ascolto.py` (finto launchctl nel diff, `ASCOLTO_CADE` → «state = spawn scheduled»; `test_riprendi_non_usa_grep_in_pipe`) — il controllo statico esclude i commenti e richiede la forma con `case`. Esito: ok.

Esecuzione: copia dall'index in scratch, `tests/test_unit_voce_ascolto.py`: **264 passed**.

Riserve:
- **R-678-1 BASSA**: se il servizio ci mette più di 5 s a uscire (riprendi.sh lanciato mentre pausa.sh è ancora in corso), ora si finisce in `cade()` col messaggio «si ferma subito», che in quel caso è impreciso. Non fa danni: rimanda al log e a installa.sh. Basterebbe un messaggio che citi anche «sta ancora uscendo, riprova tra poco».
- **R-677-3 COSMETICA**: resta aperta, come dichiarato.

Non verificato:
- il comportamento reale di launchd sul Mac (lo stato «spawn scheduled» o il throttling durante i riavvii continui): non è riproducibile in Linux, l'ho provato solo coi finti.
- bash 3.2 non l'ho eseguito, non è disponibile qui: la compatibilità l'ho valutata leggendo i costrutti usati.
- `clients/voice/ascolto.py` non l'ho rianalizzato: le correzioni toccano solo riprendi.sh e i test.

Memoria: riga #678 e una lezione aggiunte in .claude/agents/memoria_revisore.md, commit 48f5ffa. Lo staged è rimasto intatto (6 file). /home/user/Gas non è stato toccato e non ho usato `git stash`.

Unione con main e riserve della #341 — review #702, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #702 (chat Mani). Il numero più alto nella memoria, contando anche i -M2, era #701. Oggetto: diff staged su claude/peaceful-lovelace-0w2b7q, confrontato con `git diff --cached origin/main` (c1a4503). È un merge in corso: MERGE_HEAD 50d6785 (fetta 44) più le riserve del bot sulla PR #341. Lo staged coincide con il working tree: `git diff --stat` non staged è vuoto. Prima della review ho letto CLAUDE.md (dato), reports/stato_progetto.md (riga 4: R-694-1 e R-695-2 accettati) e la memoria (#677, #678, #679, #680, #694, #695, #701).

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:1081` — fa: GAS_VOICE_FINESTRA ora va da 0 a 120. Rischio: resta diverso da `clients/voice/browser_server.py:353`, che vuole 0 < finestra ≤ 120. Esito: ok sul 120, con una riserva cosmetica sullo 0 (R-702-3). Il mutante «range 300» viene preso (2 failed).
- `clients/voice/ascolto.py:704` — fa: `turni = 0` quando la parola si sente nella finestra. Rischio (privacy): una falsa parola in ogni finestra tiene aperta la conversazione? Esito: ok. Sonda con una falsa parola in ogni finestra e max_turni=2: 9 turni sia nello staged sia su main. Su main la conversazione si chiude, ma la stessa parola la riapre subito da aspetta_parola. Il reset quindi non aggiunge esposizione oltre R-694-1/R-695-2, già accettati. L'unica differenza è che manca il «Sì, signore?» udibile. Per l'eco, la finestra parte dopo `_azzera()` (R-680-1), mentre il percorso «interrotto» resta senza reset (R-668-1). Il mutante «niente reset» viene preso.
- `clients/voice/ascolto.py:439` e `clients/voice/ascolto.py:463` — fa: dopo la parola sentita in registra, si tollera silenzio fino ad ATTESA_VOCE_S finché non arrivano 3 blocchi forti di fila. Il taglio a PRIMA_DELLA_PAROLA_S avviene prima dell'append, quindi è invariato. Il tetto REGISTRAZIONE_MAX_S regge (vedi sonda). Esito: riserva (R-702-1, R-702-2). Il mutante «niente tolleranza» viene preso.
- `clients/voice/ascolto.py:548` — fa: unione con la #341. Il controllo dell'eco legge `pezzi.testo` dopo `next()`, e `_ascolta_mentre_suona(interrompibile=)` è coerente. R-679-2 è chiusa dal testo in `scripts/voce/LEGGIMI.md:22`. Esito: ok. R-679-3 (log «senza voce» sulla pausa) resta cosmetica e questo diff non la tocca.
- `tests/test_unit_voce_ascolto.py:2362` — fa: test sulla pausa di 1,5 s dopo la parola, con i conteggi esatti dei campioni. Ci sono anche `tests/test_unit_voce_ascolto.py:2345` (reset dei turni) e `tests/test_unit_voce_ascolto.py:2338` (limite 120). Esito: ok. Nessun nome di test duplicato dopo la risoluzione del conflitto.
- `scripts/voce/riprendi.sh:43` — fa: fetta 44 già rivista in #678 (funzioni gira/cade, `[ "$ANDATO" = si ] || cade`). Rischio: che il merge l'abbia toccata. Esito: ok, identica alla versione rivista.
- `scripts/voce/LEGGIMI.md:135` — fa: documenta il limite 0–120. Esito: riserva cosmetica (R-702-3).

**Controlli sul merge**
- `git ls-files -u` vuoto, `--check` pulito, nessun marcatore di conflitto.
- Memoria: nel diff rispetto a main ci sono solo righe aggiunte (#677, #678 e lezioni), nessuna tolta.
- Test sulla copia dell'index (checkout-index in scratch, niente stash): tests/test_unit_voce_ascolto.py **282 passed**.

**Sonde (staged contro origin/main)**
- Falsa parola nella finestra, poi un clic (1 blocco forte) ogni 4 s: staged **30,0 s** registrati e inviati, main **1,36 s**.
- Coda della parola di 3 blocchi forti, pausa di 1,5 s, poi la richiesta: la richiesta si chiude a 1,52 s e il resto parte come turno di seguito (2,4 s). Con una coda di 2 blocchi va tutto insieme (4,56 s).

**Riserve**
- R-702-1 BASSA — `clients/voice/ascolto.py:463`: la tolleranza si azzera a ogni blocco forte isolato e non ha un tetto proprio. Dopo una falsa parola (R-694-1), rumori brevi a meno di 5 s l'uno dall'altro tengono aperta la registrazione fino a 30 s. Quell'audio va al server come richiesta normale, con gli strumenti. Va contro il principio di R-616-2 (l'attesa conta ogni blocco). Correzione suggerita: un contatore totale dei blocchi dalla parola che spegne `dopo_parola` dopo `max_attesa` blocchi, anche se ci sono stati blocchi forti in mezzo.
- R-702-2 BASSA — `clients/voice/ascolto.py:459`: se il rilevatore scatta prima della fine di «Jarvis», la coda della parola (≥3 blocchi forti) consuma la tolleranza. Una pausa dopo la parola allora chiude la richiesta, e il resto va come turno di seguito, senza strumenti e col filtro [NON_PER_ME]. Dipende dalla latenza reale di openWakeWord (R-694-2). Nessun test.
- R-702-3 COSMETICA — `scripts/voce/LEGGIMI.md:135`: dice solo che la pagina web «non accetta più di 120». In realtà `clients/voice/browser_server.py:353` rifiuta anche 0, che l'ascolto accetta come «finestra spenta»: con GAS_VOICE_FINESTRA=0 la pagina web non parte.

**Cosa NON ho verificato**
- Comportamento dal vero sul Mac (latenza di openWakeWord, livelli RMS della coda della parola, eco reale delle casse): non riproducibile in questo ambiente. Per questo R-702-2 resta una stima, fatta con blocchi finti.
- Gli script launchctl (pausa.sh, riprendi.sh) li ho provati solo con i finti dei test. La parte nuova rispetto alla #678 è soltanto il merge, senza cambi di logica.
- reports/proposta_parola_gas.md: documento fuori dal perimetro, non revisionato nel merito.
- Suite del kernel non rilanciata: gas.py e modules/ non sono nel diff.

**Memoria**
In coda a .claude/agents/memoria_revisore.md ho aggiunto la riga #702 e una lezione: una tolleranza di silenzio che si azzera sui blocchi forti isolati non ha un tetto proprio (stessa lezione di R-616-2). Come chiesto, il file resta nel working tree NON committato.

Ri-review #703 (correzione R-702-1 e R-702-3), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #703 (chat Mani). Ho riguardato le correzioni della #702 sul diff STAGED (merge in corso, MERGE_HEAD 50d6785, confronto con origin/main c1a4503). Ho letto prima CLAUDE.md (sezioni 5, 8 e 9), lo stato del progetto (le parti con R-694/R-702) e la memoria del revisore, inclusa la #702.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:426` — nuovo contatore `dal_la_parola`, messo a zero insieme agli altri quando la parola scatta (`clients/voice/ascolto.py:441`). Rischio: un contatore non azzerato o uno stato che resta da un turno all'altro. Esito: ok. Sono variabili locali di `registra`, partono a 0 a ogni chiamata e tornano a 0 a ogni parola sentita.
- `clients/voice/ascolto.py:456-459` — conta ogni blocco dopo la parola, sia forte sia debole, e spegne la tolleranza a `max_attesa`. Rischi: (a) i rumori brevi tengono ancora aperta la registrazione (R-702-1); (b) errore di un blocco al confine; (c) la pausa vera dopo la parola non funziona più. Esito: ok.
  - (a) La mia sonda dei clic dopo una falsa parola (un clic ogni 4 s) dà 5,44 s inviati, contro 30,0 s della #702 e 1,36 s di main.
  - (b) Con N=62: 60 o 61 blocchi di silenzio e poi voce → una sola richiesta (7,68 s e 7,76 s). 62 o 63 blocchi → la richiesta si chiude a 5,44 s e la voce va come seguito. Quando il tetto scatta, il silenzio accumulato (≥ max_silenzio) chiude nello stesso blocco in cui chiudeva la #702: il confine resta a circa 5 s dalla parola.
  - (c) Con una pausa vera di 1,5 s dopo la parola resta una sola richiesta di 4,4 s; main la spezza in 1,28 s più un seguito.
  - Con la voce subito dopo la parola e una pausa di 1,2 s a metà frase, il risultato è identico a main (2,08 + 1,60): la soglia di silenzio normale torna come prima.
- `clients/voice/ascolto.py:463-464` — uscita dalla tolleranza dopo 3 blocchi forti di fila. Rischio: che la correzione l'abbia resa inutile. Esito: ok. Il mutante «niente uscita per voce continua» fa fallire 3 test (tra cui `test_dopo_la_parola_la_pausa_finale_torna_normale`).
- `tests/test_unit_voce_ascolto.py:2396` — `test_dopo_una_falsa_parola_i_rumori_non_tengono_aperta_la_registrazione`. Rischio: un limite troppo largo che non prende la regressione. Esito: ok. Il limite è (5+1+62+10) blocchi, cioè 6,24 s, ben sotto i 30 s. Il mutante «niente tetto» (`if False:` al posto di `dal_la_parola >= max_attesa`) fa fallire solo questo test.
- `tests/test_unit_voce_ascolto.py:2362` — test della pausa vera dopo la parola nella finestra. Ancora verde con il tetto. Esito: ok.
- `scripts/voce/LEGGIMI.md:135` — riga di `GAS_VOICE_FINESTRA` (0–120, `0` = niente finestra, la pagina web accetta solo valori da più di 0 a 120). Rischio: un'affermazione falsa sulla pagina web. Esito: ok. L'ho verificata nel codice: `clients/voice/browser_server.py:354` controlla `0 < finestra <= 120`, e il limite dell'ascolto è a `clients/voice/ascolto.py:1087`. R-702-3 chiusa.

**Controlli meccanici**
- Copia dell'index fatta con `git checkout-index` in scratchpad, niente stash: `tests/test_unit_voce_ascolto.py` dà 283 passed.
- `git diff --cached --check` pulito; `git ls-files -u` vuoto.
- Antipattern della sezione 5 di CLAUDE.md: nessun taglio diretto della history (l'unico taglio di lista è sull'audio `presi`, già visto nella #694) e nessun output dei tool simulato. Cap di 10 iterazioni e `_get_window` non toccati.

**Riserve**
- R-702-2 BASSA, resta aperta: la coda della parola, cioè almeno 3 blocchi forti dopo che il rilevatore scatta, consuma la tolleranza. La sonda «coda di 3 blocchi + pausa di 1,5 s» chiude ancora la richiesta a 1,52 s e manda il resto come seguito, come su main. Dipende dalla latenza reale di openWakeWord (R-694-2) e non ha test. Va tracciata in stato_progetto.md.
- Nota fuori dal diff, nessuna riserva nuova: con un clic ogni 2 blocchi per 20 s si registrano 21,2 s, uguale tra staged e main. È il comportamento della soglia di silenzio normale, che c'era già prima e questo diff non tocca.

**Cosa NON ho verificato**
- La latenza reale di openWakeWord e il comportamento sul Mac con microfono e casse veri: non si riproducono qui. Le sonde usano i blocchi finti dei test, quindi i tempi sono quelli del modello a blocchi da 80 ms, non della stanza.
- La suite completa del kernel: il diff tocca solo client voce, script voce, LEGGIMI e i test dell'ascolto. Il merge con gas.py l'ho già controllato nella #701.

**Memoria**
- Riga #703 aggiunta in coda a `.claude/agents/memoria_revisore.md`, nel working tree e non committata. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 257 (main dopo la #341) a 283 casi. Riepilogo reale nel venv:

```
283 passed in 26.95s
```

Mutanti presi (nuovi di questa sessione):
- niente tolleranza dopo la parola;
- flag della tolleranza mai alzato;
- tolleranza senza uscita per voce continua;
- tolleranza senza tetto (R-702-1);
- finestra a 300;
- niente reset dei turni.

Il primo test sul reset dei turni non lo prendeva: l'ho riscritto finché il mutante non è stato preso.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). PR #341 su 179d05c: unit-suite, handoff-check, verifica success; bot APPROVATO CON RISERVE (neutral); mergiata. Per i commit di questa sessione (50d6785, 8133c60 e il commit di fine-task) la run non è ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-702-2 BASSA: se il rilevatore scatta prima della fine di «Jarvis», la coda della parola consuma la tolleranza e una pausa dopo la parola spezza la richiesta (il resto va come seguito). Da provare sul Mac insieme a R-694-2.
- R-677-3 COSMETICA: il test dell'eco non prova che il controllo stia dopo `next()`.
- R-678-1 BASSA: riprendi.sh lanciato mentre il servizio sta ancora uscendo da più di 5 s finisce in «cade» invece di riprovare.
- R-679-3 COSMETICA: il log di una pausa nel seguito dice «non riuscito».
- Dalla #341: R-676-1/2 BASSE (mutanti di stato e svuota), R-681-1 COSMETICA, R-694-2 BASSA (1,5 s da provare sul Mac), R-695-1 BASSA. R-694-1/R-695-2: rischio ACCETTATO dall'operatore il 2026-11-07.
- Bot su 179d05c: V-2 COSMETICA (descrizione della #341 non aggiornata, riga vuota PEP8 nei test).
- Restano le riserve delle fette 40–43 in `reports/stato_progetto.md`.
