# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — avviso file delicati (R-390-1), giro notturno da Telegram (R1), firma in parallelo (5.2), compito della chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #233 (https://github.com/Gasss23/Gas/pull/233): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10). Numero e URL dall'API GitHub (`create_pull_request`), `gh` assente nel container.
2. Aprire la terza chat «Mani» col prompt in fondo a `reports/lavoro_parallelo.md`.
3. Prova dal vero sul Mac: bot acceso, `/compito <nome>` dal telefono.

---

## §1 SCOPE & ESITO FETTE

- **R-390-1 + note verifica esterna #232**: `FATTA` — review #391 (chat Motore) APPROVATO CON RISERVE.
- **Compito della chat Mani** (documento): `FATTA`.
- **R1 — giro o compito lanciato da Telegram**: `FATTA` — review #392 e #393 (chat Motore) APPROVATO CON RISERVE. V-2 verifica esterna #233 non serve (i `.sh`/`.py` finali vanno alla firma, livello 2).
- **Avviso se il giro muore prima di partire** (R-393-1, R-394-1, V-1/V-3 verifica esterna #233 2° giro): `FATTA` — review #394 e #395 (chat Motore) APPROVATO CON RISERVE.
- **5.2 — firma inviata in parallelo (R-c4b1-3)**: `FATTA` — review #396 (chat Motore) APPROVATO CON RISERVE.
- **5.2 — bottone Modifica e firme a gruppi (C6)**, **R7**: `DEFERITA` — prossime fette.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 gas.py                             |  13 ++++++++-----
 modules/gate/gate.py               |  18 ++++++++++++++----
 modules/notte/notte.py             |  18 ++++++++++++++++--
 modules/telegram/bot.py            | 188 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------
 reports/da_mergiare.md             |  41 +++++++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  17 ++++++++++-------
 reports/handoff.md                 | 301 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------
 reports/lavoro_parallelo.md        |  17 ++++++++++++++++-
 reports/setup_notte.md             |   5 +++++
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  29 +++++++++++++++++------------
 tests/test_unit_gate.py            |   7 +++++++
 tests/test_unit_kernel.py          |  24 ++++++++++++++++++++++++
 tests/test_unit_notte.py           | 225 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 15 files changed, 812 insertions(+), 103 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
b49f47b fix(telegram): richiesta di firma e notifiche inviate in parallelo ai destinatari (R-c4b1-3, roadmap 5.2)
f041652 chore(revisore): memoria review #396 — APPROVATO CON RISERVE
73cca2d fix(notte): marcatore di avvio del giro, niente doppio avviso; nome del compito senza «-» iniziale (R-394-1, V-1/V-3 verifica esterna #233)
bd6adb7 chore(revisore): memoria review #395 — APPROVATO CON RISERVE
1678804 fix(notte): avviso su Telegram se il giro lanciato dal bot muore prima di partire (R-393-1)
7bded4d chore(revisore): memoria review #394 — APPROVATO CON RISERVE
9793154 docs(fine-task): report, handoff, coda da_mergiare — R-390-1, giro da Telegram (R1), chat Mani
5a21053 fix(notte): giro da Telegram col gas.py del modulo e uscita nel log; plist/desktop di nuovo segnalati (R-392-1/2, V-3 verifica esterna #233)
db6c397 chore(revisore): memoria review #393 — APPROVATO CON RISERVE
aeb483d chore(revisore): memoria review #393 — APPROVATO CON RISERVE
18c4628 feat(notte): lanciare il giro o un solo compito da Telegram (/notte, /compito <nome>) (R1)
751e870 chore(revisore): memoria review #392 — APPROVATO CON RISERVE
caf5bdd docs: coda da_mergiare, compito della chat Mani, riserve #391
f12e973 fix(avvisi): chiavi e database come estensioni interne, via le ambigue e i caratteri invisibili (R-390-1, verifica esterna #232)
42864b0 chore(revisore): memoria review #391 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #391 (chat Motore) — commit f12e973

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto, nell'ordine richiesto: CLAUDE.md (sez. 5 e 8), reports/stato_progetto.md (la parte su R-390) e la coda di .claude/agents/memoria_revisore.md.

**Cosa ho riprodotto io stesso**
- Test del cancello (tests/test_unit_gate.py): 759 passati.
- Test del kernel (tests/test_unit_kernel.py): 950 PASS, 0 FAIL.
- Prove a mano su 15 nomi di file (risultati sotto).

**Punti del diff esaminati**
- modules/gate/gate.py:521 — l'elenco delle estensioni interne delicate ora contiene gli eseguibili più chiavi, archivi di password e database: pem, p12, pfx, kdbx, ovpn, gpg, jks, sql, sqlite, sqlite3, ipynb, env. Escono html, htm, js, ts, pl, cmd, service, desktop, plist.
  - Rischio esaminato: veri positivi persi, cioè la lezione della review #390.
  - Prove: `server.pem.txt`, `a.PEM.txt` (il maiuscolo è gestito da `_normalize_path`), `tabella.sql.md` e `note.gpg.md` danno True. `customer.service.md` e `manuale.html.pdf` danno False.
  - Esito: ok, con la riserva R-391-1.
- modules/gate/gate.py:549 — toglie dal nome i caratteri invisibili (Unicode categoria Cf) prima di TUTTI i controlli, anche quello sul file nascosto e sull'estensione finale.
  - Rischio esaminato: un carattere invisibile che aggira i controlli.
  - Prove: `​.bashrc`, `a.py​.txt` (così si chiude anche R-390-2), `a﻿.secret` e `a.sh
.txt` danno True. `unicodedata` era già importato (modules/gate/gate.py:34). L'`except` che restituisce True resta.
  - Esito: ok.
- tests/test_unit_gate.py:819-824 — 14 casi nuovi che coprono sia il ritorno dei tipi delicati sia i falsi allarmi tolti, più i 3 casi con caratteri invisibili. Esito: ok.
- Contesto, gas.py:3803 — chiamante invariato: la funzione serve solo all'avviso per i file nuovi di livello 1, non decide il cancello. Nessun cambio ai limiti fissi (10 iterazioni, `_get_window`) e nessun antipattern della sez. 5. Esito: ok.

**Riserve**
- R-391-1 (chat Motore) BASSA: alcuni veri positivi vanno persi per scelta. `a.html.txt`, `x.js.md`, `x.service.txt` e `a.ts.txt` ora danno False. È lo scambio accettato dalla verifica esterna #232, ma va dichiarato in stato_progetto.md.
- R-391-2 (chat Motore) COSMETICA:
  - `env` come estensione interna fa scattare l'avviso anche su documenti come `dev.env.md` o `report.env.2024.md`.
  - I segni combinanti (categoria Mn, es. `a.śh.txt` → False) non vengono tolti. Si vedono a occhio, quindi non sono un aggiramento invisibile.

**Cosa NON ho verificato:** il comportamento reale dell'avviso su Telegram o sul server (VPS), perché qui non è riproducibile. Mi sono limitato al valore restituito dalla funzione e al chiamante invariato.

**Memoria:** ho aggiunto la riga contatore «#391 (chat Motore)» con «Nessuna lezione nuova» e l'ho committata da sola (42864b0). Il diff staged del motore è rimasto intatto.

File rilevanti: /home/user/Gas/modules/gate/gate.py, /home/user/Gas/tests/test_unit_gate.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #392 (chat Motore) — commit 18c4628

## VERDETTO: APPROVATO CON RISERVE

Review #392 (chat Motore): R1, lanciare `/notte` e `/compito <nome>` da Telegram. Ho letto CLAUDE.md (sezioni 5, 8, 9), `reports/stato_progetto.md` (letto in modo mirato) e la mia memoria.

**Cosa ho esaminato nel diff**
- `modules/telegram/bot.py:522`: il comando viene intercettato dopo il controllo delle chat autorizzate e prima di `run_turn`. Rischi controllati: che una chat non autorizzata lanci un giro, che il comando arrivi al modello. Esito ok, e il test `_handle_update` lo copre.
- `modules/telegram/bot.py:478`: `lancia_giro` avvia il processo con una lista di argomenti (niente shell), stdin/stdout/stderr su DEVNULL, `start_new_session`, `close_fds`, e il nome viene ricontrollato con `[a-z0-9_-]{1,40}`. Rischi controllati: iniezione di comandi, nomi con «../» o spazi o maiuscole. Esito ok. `/compito --help` passa la validazione ma finisce solo come nome inesistente, quindi è innocuo.
- `modules/telegram/bot.py:466`: `_raccogli_giri` (chiamata anche a `modules/telegram/bot.py:409` ogni minuto) raccoglie i processi finiti, quindi niente zombie, e impedisce un secondo lancio dal bot. Esito ok. Un riavvio del bot perde la lista, ma resta il lock flock.
- `modules/notte/notte.py:526`: filtro `solo`. Un nome assente aggiunge un avviso e dà exit 1; un nome non valido non compare nel riepilogo; il lock occupato manda già la notifica `GIRO_OCCUPATO`. Esito ok.
- `gas.py:5252`: `argv[2]` arriva a `notte_cmd`, e `solo` viene passato solo se c'è (compatibile con i finti dei test). Esito ok.
- Ambiente ereditato: il processo figlio riceve l'ambiente del bot (chiavi API e token Telegram). È lo stesso che `gas.py` caricherebbe comunque dal `.env`, quindi non c'è un'esposizione nuova. Esito ok.
- Ho rifatto i test: notte 96 passed, kernel 950 PASS / 0 FAIL. Il round-trip con 2 tool call (sezione 7 di CLAUDE.md) c'è. Il diff non contiene slicing della history né output di tool simulati.

**Riserve**
- **R-392-1 (chat Motore), BASSA**: `gas.py` viene cercato in `kernel.root`, che è la cartella da cui è partito il bot (`modules/telegram/bot.py:391`), non la cartella del modulo. L'ho provato: con una cartella senza `gas.py` il bot risponde «Compito avviato», il processo figlio esce con codice 2 e non arriva nessun riepilogo. Correzione: controllare `(root / "gas.py").is_file()` prima di lanciare, oppure ricavare il percorso da `__file__`.
- **R-392-2 (chat Motore), BASSA**: l'output del processo figlio va in DEVNULL, mentre il timer lo scrive in `.gas_notte/launchd.log`. Se il figlio muore prima di `esegui_notte` (errore di import o di sintassi) non resta traccia e non arriva notifica. Correzione: scrivere l'output in un file di log, oppure far segnalare a `_raccogli_giri` i codici d'uscita diversi da 0 e 1.
- **R-392-3 (chat Motore), COSMETICA**: un compito del catalogo oltre `MAX_COMPITI` risulta «non trovato» con `/compito`. Inoltre un messaggio modificato in `/notte` rilancia il giro, come già succede per `run_turn`.

**Cosa NON ho verificato**: il comportamento reale su Telegram e sul Mac/VPS (launchd, bot acceso davvero). Non è riproducibile qui: la prova è solo con il Popen reale in una cartella temporanea e con i finti dei test. Non ho controllato nemmeno `reports/setup_notte.md` (modificato ma non in staging, fuori dal perimetro).

**Memoria**: riga #392 (chat Motore) aggiunta, con la lezione «processo lanciato in background con output in DEVNULL e risposta "avviato": sondare il caso del figlio che muore subito». È committata da sola in 751e870 tramite `scripts/commit_memoria_revisore.sh`; il diff in staging è rimasto intatto.

File:
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/modules/notte/notte.py
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_notte.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #393 (chat Motore) — commit 5a21053

## VERDETTO: APPROVATO CON RISERVE

Review #393 (chat Motore). Ho letto prima CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano) e la mia memoria.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:466`: `_GAS_PY` viene da `Path(__file__).resolve().parents[2] / "gas.py"`. Rischio: che venga avviato un gas.py diverso da quello del bot. Esito: ok. Il test `tests/test_unit_notte.py:1331` controlla che il comando usi `_GAS_PY` e che il file esista. Il cwd del figlio resta `root`.
- `modules/telegram/bot.py:499`: se gas.py manca, la risposta è «NON avviato» e non parte nessun processo. Rischio: rispondere «avviato» e poi silenzio. Esito: ok, coperto da `tests/test_unit_notte.py:1381`. Riserva cosmetica: il messaggio dice «dettagli in gas_debug.log», ma su questo ramo non viene scritto nessun `log.warning` (vedi R-393-2).
- `modules/telegram/bot.py:504`: stdout e stderr del figlio vanno in append binario su `.gas_notte/telegram_giro.log`; il `with` chiude il file nel padre dopo `Popen`. Rischio: file lasciato aperto, oppure eccezione di `Popen` non gestita. Esito: ok. Se `Popen` fallisce, il `with` chiude il file e l'`except` esterno registra l'errore nel log e risponde «NON avviato». Niente shell, comando passato come lista.
- `modules/telegram/bot.py:480`: warning per codici d'uscita diversi da 0, 1 e 2; il processo esce sempre dalla lista, anche quando `poll` solleva un'eccezione. Rischio: che restino crash precoci non segnalati. Esito: **riserva (R-393-1)**. `_raccogli_giri` è chiamata anche dal ciclo di polling (`modules/telegram/bot.py:409`), quindi il warning arriva in tempo quando scatta.
- `modules/gate/gate.py:526`: `plist` e `desktop` tornano tra le estensioni interne delicate. Esito: ok. Sonda: `dati/a.plist.txt`, `dati/a.desktop.txt` e `dati/x.plist` danno tutti True. Il caso è coperto da `tests/test_unit_gate.py:824`.

**Controllo su V-2 della verifica esterna #233 (.sh/.py finali)**
La conclusione è giusta, ma la motivazione è imprecisa. `_DENY_WRITE_SUFFIXES` (`modules/gate/gate.py:124`) per `write_file` non produce un DENY: tramite `livello_scrittura` dà il livello FIRMA, cioè 2 (`modules/gate/gate.py:451`). Sonda: `run.sh`, `run.py`, `run.sh.`, `run.SH`, `run.Py ` e `x.zsh` danno livello 2 e IRREVERSIBLE. L'avviso del kernel (`gas.py:3803`) scatta solo per i file nuovi a livello LIBERO, quindi questi file non lo raggiungono mai: V-2 non serve. Da correggere solo la frase «DENY in scrittura» in report e handoff: il livello giusto è FIRMA.

**Riproduzione**
- notte+gate: 858 passed.
- `tests/test_unit_kernel.py`: 950 PASS, 0 FAIL.
- `python -c "import nonesiste"` esce con codice 1 (dimostra R-393-1).

**Finding**
- **R-393-1 (chat Motore), BASSA**: un crash Python prima di `esegui_notte` esce con codice 1, che è proprio il codice che il warning esclude. Vale per ImportError, SyntaxError in un modulo importato e qualunque traceback non gestito. Quindi il caso che R-392-2 voleva coprire («import, sintassi») non lascia ancora nessuna riga in gas_debug.log né una notifica all'operatore. Ora il traceback finisce almeno in `telegram_giro.log`, quindi R-392-2 è chiusa a metà. Il docstring promette più di quello che il codice fa. Correzione possibile: segnalare anche il codice 1 quando il giro non ha scritto il riepilogo, oppure avvisare su Telegram.
- **R-393-2 (chat Motore), COSMETICA**:
  - il ramo «gas.py non trovato» rimanda a gas_debug.log senza scriverci niente;
  - `telegram_giro.log` cresce senza rotazione (come `launchd.log`);
  - `dati/run.sh` seguito da un carattere invisibile in fondo (U+200B) risulta a livello LIBERO e `sembra_delicato` dà False, perché l'ultima estensione, ripulita, non viene confrontata con le interne. Il nome del file però non è più `.sh` per shell e launchd.

**Cosa non ho verificato**: il comportamento reale sul Mac dell'operatore, cioè avvio del bot da un'altra cartella sotto launchd, permessi di `.gas_notte` e ricezione del riepilogo su Telegram. In questo ambiente non si può riprodurre: mi fido della sonda dichiarata dall'agente principale (giro avviato da una cartella temporanea, codice 1, log scritto). Non ho controllato nemmeno un uso concorrente del log da parte di più bot: oggi è possibile un solo giro alla volta.

Il diff staged è intatto (4 file, +57/-10).

**Memoria aggiornata**: riga #393 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, con questa lezione: un filtro sui codici d'uscita di un processo figlio Python va confrontato anche con i codici dell'interprete stesso (traceback → 1, file non apribile → 2). Ho committato la memoria due volte con `scripts/commit_memoria_revisore.sh`, la seconda per correggere un numero di riga (482→480 nella prima riga ho scritto 479, corretto in 480). Commit finale: `db6c397`.

---

### Review #394 (chat Motore) — commit 1678804

## VERDETTO: APPROVATO CON RISERVE

Review #394 (chat Motore). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), la riga R1 di reports/stato_progetto.md (R-393-1 e R-393-2 aperte) e la coda di .claude/agents/memoria_revisore.md, applicando la lezione #393 sui codici d'uscita dell'interprete.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:476` — `_giro_partito` guarda se `ultimo_giro.md` è stato scritto dopo il lancio (`mtime >= t0-1`): file assente → False, qualsiasi altro errore → True. Rischi: granularità dell'orologio e giro che finisce entro lo stesso secondo. Sonde reali: riepilogo scritto nello stesso istante o 0.5s prima → True; 1.5s prima → False; root inesistente → False; voce senza root → True. La tolleranza di 1s evita falsi avvisi su file system a granularità di 1s (HFS+). Il rovescio è che un riepilogo del timer scritto meno di 1s prima del lancio viene preso per nuovo (falso negativo, trascurabile). Il clock è lo stesso (`time.time()` e mtime locale). — ok
- `modules/telegram/bot.py:498` — avvisa se il codice d'uscita è diverso da 2 e manca un riepilogo nuovo. Si chiude il caso di R-393-1: traceback di Python con codice 1. Il testo è fisso e non contiene dati del processo. GAS_NOTTE_TELEGRAM=0 viene rispettato. Se `invia_notifica` o `poll` sollevano, l'eccezione viene intercettata e loggata e la voce viene comunque tolta (lo prova `test_raccogli_giri_non_solleva`). — ok, con le riserve sotto
- `modules/notte/notte.py:584` (contesto, file non toccato) — nel ramo `except` di `esegui_notte` il giro esce con 1 senza scrivere il riepilogo e ha già mandato da sé «INTERROTTO alle …». — riserva R-394-1
- `modules/telegram/bot.py:520` — `log.warning` nel ramo «gas.py non trovato». Chiude la parte di R-393-2 sulla riga di log mancante. — ok
- `tests/test_unit_notte.py:1392` — copre codice 1 senza riepilogo, 120 con riepilogo vecchio, 2, 1 e 0 con riepilogo nuovo, in corso, interruttore spento e poll che solleva. Riprodotto: 99 passed. — ok
- `modules/telegram/bot.py:409` (contesto) — `_raccogli_giri` è chiamata dal loop di polling al massimo una volta al minuto, e anche dentro `lancia_giro`. `invia_notifica` ha un timeout di 15s per destinatario e parte solo per un giro morto, quindi il loop può fermarsi al massimo 15s×N una volta sola. Stesso ritardo sulla risposta a `/notte` se il giro precedente è morto. Accettabile. — ok

**Riserve**
- **R-394-1 (chat Motore) BASSA**: il giro può essere interrotto da un'eccezione dentro `esegui_notte` (es. flock ENOLCK, `carica_catalogo` o `_componi_riepilogo` che sollevano). In quel caso il giro esce con 1, non scrive il riepilogo e ha già mandato da sé «Gas — giro notturno INTERROTTO alle …». Il bot aggiunge un secondo messaggio «si è fermato prima di partire (nessun riepilogo)»: è doppio e impreciso, perché il giro era partito. Possibili correzioni: far scrivere un riepilogo minimo anche nel ramo `except`, oppure usare un marcatore dedicato (es. `.gas_notte/ultimo_avvio`) scritto da `esegui_notte` appena entra.
- **R-394-2 (chat Motore) COSMETICA**:
  - Se il riepilogo non si può scrivere ma il giro è completato (notte.py logga e prosegue), arriva prima il riepilogo vero su Telegram e poi un falso «prima di partire». È raro: la cartella `.gas_notte` era scrivibile per il lock.
  - Se il giro di Telegram muore mentre un giro del timer scrive il riepilogo (il timer tiene il lock e quindi il giro di Telegram non esce con 2), l'avviso si perde.

**Rischi esclusi**
- Invio Telegram reale e comportamento su macOS/launchd non verificati: niente token né Mac in questo ambiente. Tempi di blocco stimati dai timeout del codice, non misurati.
- Non ho rieseguito la suite del kernel (950 PASS dichiarati dall'agente) né la sonda con `import modulo_che_non_esiste`: mi fido delle prove riportate, la logica è coperta dai test unitari che ho rieseguito.

**Memoria**: aggiunta la riga #394 (chat Motore) con la lezione: «un segnale indiretto di "il figlio è partito" va incrociato con tutti i rami d'uscita del figlio che già notificano da sé». Committata con `scripts/commit_memoria_revisore.sh` (commit 7bded4d). Nota: nella riga di memoria il controllo dell'avviso è citato a `modules/telegram/bot.py:497`, la riga corretta è la 498.

File: /home/user/Gas/modules/telegram/bot.py, /home/user/Gas/tests/test_unit_notte.py, /home/user/Gas/modules/notte/notte.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #395 (chat Motore) — commit 73cca2d

## VERDETTO: APPROVATO CON RISERVE

Review #395 (chat Motore), diff staged su 3 file: modules/notte/notte.py, modules/telegram/bot.py, tests/test_unit_notte.py.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (letto in parte), coda di .claude/agents/memoria_revisore.md (review #390–#394, inclusa la lezione #394: un segnale indiretto va confrontato con tutti i punti d'uscita del processo figlio).

Elementi del diff esaminati:
- `modules/notte/notte.py:515` — il marcatore `ultimo_avvio` viene scritto dopo il mkdir e prima del lock, dentro un try suo. Rischi esaminati:
  - scrittura che fallisce: finisce solo nel log, il giro prosegue;
  - un giro del timer è in corso quando il bot ne lancia un altro: il figlio scrive il marcatore, poi trova il lock occupato ed esce con codice 2. Il codice 2 è già escluso da `_raccogli_giri`, e il figlio manda da sé l'avviso «NON avviato»;
  - due processi che scrivono insieme: conta solo l'ora di modifica del file, non il contenuto.
  - Esito: ok.
- `modules/telegram/bot.py:478` — `_giro_partito` ora guarda il marcatore invece del riepilogo; l'import è dentro il try (il nome di cartella non è più scritto due volte). Rischio esaminato: avviso doppio o mancante. Ogni uscita di `esegui_notte` dopo il mkdir avvisa già da sé (riepilogo, «INTERROTTO», «NON avviato»), quindi chiude R-394-1 e anche il caso «riepilogo non scrivibile» di R-394-2. Esito: ok.
- `modules/telegram/bot.py:442` e `modules/telegram/bot.py:443` — il separatore è solo spazio o tab e il nome non può iniziare con «-». Prove fatte a mano:
  - `/compito\tconta` → compito;
  - `/compito\nconta` e `/compito conta` → None (va al modello come testo normale);
  - `/compito -`, `/compito _x`, `-h`, `--help` → errore;
  - `/notte\t` → notte.
  - Esito: ok, con la riserva R-395-1.
- `tests/test_unit_notte.py:1440` — nuovo test: marcatore scritto anche con catalogo assente e nel ramo except. I test esistenti sono passati dal riepilogo al marcatore. Esito: ok.

Domande poste:
- Il modello può toccare `.gas_notte`? No. Verificato:
  - DENY in scrittura: `modules/gate/gate.py:117`;
  - livello 3, mai nemmeno con firma: `modules/gate/gate.py:250`;
  - per `run_command` la sandbox rimonta la root in sola lettura: `gas.py:1629`.
  - Il modello quindi non può falsificare il marcatore per nascondere l'avviso.
- Compatibilità coi test esistenti: rieseguiti io, notte **103 passed** e kernel **950 PASS / 0 FAIL**.

Finding:
- **R-395-1 (chat Motore) BASSA**: il catalogo (`modules/notte/notte.py:112`, `[a-z0-9_-]{1,40}`) accetta ancora nomi che iniziano con «-» o «_».
  - Quei compiti sono validi nel catalogo ma da Telegram non si possono lanciare.
  - Il messaggio d'errore («solo a-z 0-9 _ -, max 40») non spiega perché vengono rifiutati.
  - Anche «_» iniziale ora è rifiutato, più di quanto chiedesse V-1.
  - Rimedio: allineare la regex del catalogo, oppure dire nel messaggio «deve iniziare con lettera o cifra».
- **R-395-2 (chat Motore) COSMETICA**, due casi residui:
  - Se il mkdir di `.gas_notte` fallisce, il figlio manda «INTERROTTO» senza aver scritto il marcatore e il bot aggiunge «prima di partire». Avviso doppio, caso raro.
  - Un giro del timer che parte nello stesso istante di una morte precoce del giro lanciato dal bot la nasconde ancora. Il resto di R-394-2 è ancora aperto, ma ora vale solo nel momento in cui un giro parte.

Non verificato:
- Comportamento reale su Mac con launchd e Telegram vero (non riproducibile qui).
- Il ramo Windows senza `fcntl` (lì il marcatore viene scritto comunque).
- L'ora di modifica del file su filesystem di rete o con orologio sfasato tra bot e figlio (stesso host, considerato trascurabile).

Memoria: riga #395 aggiunta, con la lezione «quando si restringe un validatore di input lato chiamante, confrontarlo col validatore dei dati che deve raggiungere». Committata da sola con `scripts/commit_memoria_revisore.sh` (commit bd6adb7). L'index staged del diff non è stato toccato.

File:
- /home/user/Gas/modules/notte/notte.py
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/tests/test_unit_notte.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #396 (chat Motore) — commit b49f47b

## VERDETTO: APPROVATO CON RISERVE

Review #396 (chat Motore). Ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci su R-c4b1 in reports/stato_progetto.md e le ultime righe di .claude/agents/memoria_revisore.md. Nel diff non c'è slicing della history né simulazione di tool. Il ciclo di run_turn e `_get_window` non sono toccati.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:240` — `_invia_a_tutti` manda il messaggio a tutti i destinatari in parallelo (ThreadPoolExecutor, al massimo 8 thread, `with` che aspetta tutti). Rischi esaminati:
  - **Stato condiviso:** ogni thread crea il suo dict (`{"chat_id": ..., **payload}`). `reply_markup` è condiviso, ma `json.dumps` lo legge soltanto.
  - **Logging:** è thread-safe.
  - **Destinatari vuoti:** `max(1, …)` e `sum([])=0` restituiscono False.
  - **Thread che non partono:** se la creazione dei thread fallisce (RuntimeError), l'errore viene preso dall'except esterno e la funzione restituisce False.
  - **Token nei log:** si registra solo il tipo dell'eccezione.
  - **Ordine dei messaggi:** c'è un solo messaggio per chat e la funzione ritorna solo dopo che tutti i thread hanno finito, quindi l'ordine rispetto ai messaggi successivi nella stessa chat resta garantito.
  - Esito: ok.
- `modules/telegram/bot.py:283` e `modules/telegram/bot.py:317` — `invia_read_back` e `invia_notifica` ora usano l'helper. Il rischio esaminato era un cambio di semantica: restituiscono ancora (True, '') se almeno un invio va a buon fine, altrimenti (False, «invio fallito verso tutti i destinatari»). Il cambio di comportamento quando il trasporto solleva è solo teorico, perché `_tg_post` non solleva mai (vedi sotto). Esito: ok.
- `tests/test_unit_kernel.py:6953` — T77o2. Il rischio era che il test non distinguesse l'invio in parallelo da quello in serie. Ho fatto una mutazione mettendo `_INVIO_MAX_THREAD=1`: T77o2 fallisce con 3.61 s, quindi il test distingue. Ho ripristinato il file dall'index; la copia di lavoro è uguale allo staged. Esito: ok.
- Contesto: `modules/telegram/bot.py:55` — `_tg_post` usa urllib senza stato condiviso; nel caso limite il `_opener` globale creato al primo uso ha una race innocua. Intercetta ogni Exception e restituisce None, quindi non solleva mai. Esito: ok.
- Contesto: `gas.py:2794` — se l'invio fallisce, la firma viene revocata come prima. Esito: ok.

**Test riprodotti:** kernel 952 PASS, 0 FAIL.

**Riserve**
- **R-396-1 (chat Motore) BASSA:** «al massimo ~15 s» non è un tetto di tempo totale.
  - Il timeout di urlopen vale per ogni singola operazione di socket: non copre la risoluzione DNS, e una risposta che arriva a goccia lo rinnova.
  - Oltre 8 destinatari il caso peggiore diventa ceil(N/8)×15 s.
  - Non è un peggioramento rispetto a prima: va solo dichiarato nel commento di `modules/telegram/bot.py:234`.
- **R-396-2 (chat Motore) COSMETICA:**
  - Un destinatario che solleva produce due warning (il tipo dell'eccezione più «invio fallito»).
  - Il ramo `except` di `_uno` si raggiunge solo col trasporto finto del test, perché `_tg_post` non solleva mai: per Telegram reale il cambio «gli altri destinatari ricevono comunque» non cambia nulla.

**Rischio escluso:** non ho verificato l'invio reale verso api.telegram.org, né il comportamento con rete lenta o DNS bloccato su Mac o VPS, perché da qui non si può riprodurre. Non ho rilanciato la suite notte (103 passed): mi fido del dato dell'agente.

Memoria aggiornata: riga #396 aggiunta e committata (commit f041652). Lezione: un «timeout=N» passato a urlopen limita ogni singola attesa di socket, non la durata della chiamata.

File: /home/user/Gas/modules/telegram/bot.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 950 → 952 PASS, 0 FAIL (T77o2). Blocco reale: `=== RIEPILOGO: 952 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py`: `103 passed in 3.01s`; `tests/test_unit_gate.py`: 760 casi (745 a inizio sessione).

## §6 STATO CI

CI NON VERIFICATA (gh assente nel container). f12e973, caf5bdd: run del primo push della PR #233 (letta dalla verifica esterna: unit-suite success, handoff-check failure per handoff mancante). 9793154: run letta dalla verifica esterna #233 (2° giro): handoff-check success, unit-suite in corso. 18c4628, 5a21053 e memorie: nessuna run su questi SHA (pushati insieme a 9793154). 1678804, 73cca2d, b49f47b e memorie: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-391-1 (chat Motore, BASSA): `a.html.txt`, `x.js.md`, `a.ts.txt` non più segnalati (scelta dichiarata).
- R-391-2 (chat Motore, COSMETICA): `env` interno su `dev.env.md`; segni combinanti non tolti.
- R-392-3 (chat Motore, COSMETICA): compito oltre MAX_COMPITI «non trovato»; messaggio modificato rilancia.
- R-393-2 (chat Motore, COSMETICA): log senza rotazione; `run.sh` + invisibile finale (la riga di log mancante è chiusa da #394).
- R-395-1 (chat Motore, BASSA): nomi del catalogo con «-»/«_» iniziale non lanciabili da Telegram.
- R-395-2 (chat Motore, COSMETICA): avviso doppio se il mkdir fallisce; avviso perso se un giro del timer parte nello stesso istante.
- R-396-1 (chat Motore, BASSA): tetto ~15 s non assoluto (DNS, >8 destinatari).
- R-396-2 (chat Motore, COSMETICA): doppio warning per destinatario che solleva.
- Verifica esterna #233: V-4/V-5 (cosmetiche, Cc non tolti, = R-391-2); 2° giro V-2 (= R-391-1).
