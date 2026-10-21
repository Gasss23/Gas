# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — avviso file delicati (R-390-1), giro da Telegram (R1), firma in parallelo (5.2), R7 (registro e vettori), cancello (caratteri invisibili), compito della chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #233 (https://github.com/Gasss23/Gas/pull/233): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10). Numero e URL dall'API GitHub (`create_pull_request`), `gh` assente nel container.
2. C6 (bottone «Modifica» e firme a gruppi): decisione dell'operatore.
3. Aprire la terza chat «Mani» col prompt in fondo a `reports/lavoro_parallelo.md`.
4. Prova dal vero sul Mac: bot acceso, `/compito <nome>` dal telefono.
5. Fetta cancello (review #398-#400): secondo passaggio nella chat claude.ai.

---

## §1 SCOPE & ESITO FETTE

- **R-390-1 + note verifica esterna #232**: `FATTA` — review #391.
- **Compito della chat Mani** (documento): `FATTA`.
- **R1 — giro o compito lanciato da Telegram**: `FATTA` — review #392, #393.
- **Avviso se il giro muore prima di partire**: `FATTA` — review #394, #395.
- **5.2 — firma inviata in parallelo (R-c4b1-3)**: `FATTA` — review #396.
- **5.2 — C6 bottone Modifica e firme a gruppi**: `SALTATA` — decisione dell'operatore (30 settembre: niente gruppi; Modifica senza disegno).
- **R7 — registro accanto a gas.py, vettori con GAS_VECTORS_DB**: `FATTA` — review #397.
- **Cancello — caratteri invisibili e NFKC** (V-1 verifica esterna #233 3° giro, R-398-1, R-399-1): `FATTA` — review #398, #399, #400.
- **R7 — compiti lunghi che riprendono dopo un crash**: `DEFERITA` — serve un disegno.

Tutte le review (chat Motore): APPROVATO CON RISERVE, nessuna ALTA/MEDIA.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 +++++++++-
 gas.py                             |  48 ++++++++++++++++++++++++---------------
 modules/gate/gate.py               |  31 +++++++++++++++++++++----
 modules/notte/notte.py             |  18 +++++++++++++--
 modules/telegram/bot.py            | 188 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------
 reports/da_mergiare.md             |  57 +++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  17 ++++++++------
 reports/handoff.md                 | 448 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------
 reports/lavoro_parallelo.md        |  17 +++++++++++++-
 reports/setup_notte.md             |   5 ++++
 reports/stato_progetto.md          |   6 +++--
 reports/ultimo_report.md           |  35 ++++++++++++++++++----------
 tests/test_unit_gate.py            |  20 ++++++++++++++++
 tests/test_unit_kernel.py          |  80 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_notte.py           | 225 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 15 files changed, 1089 insertions(+), 118 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
b32cbea fix(cancello): nome grezzo che NFKC cambia mai libero dopo una lettura (R-399-1)
46bcd6f chore(revisore): memoria review #400 — APPROVATO CON RISERVE
0614242 fix(cancello): nome grezzo con caratteri invisibili mai libero dopo una lettura (R-398-1)
5ea821a chore(revisore): memoria review #399 — APPROVATO CON RISERVE
e706955 fix(cancello): caratteri invisibili tolti anche nel confronto dei percorsi (V-1 verifica esterna #233), test del log da un'altra cartella (R-397-2/3)
ea98089 chore(revisore): memoria review #398 — APPROVATO CON RISERVE
0fafbe9 fix(r7): gas_debug.log sempre accanto a gas.py; i comandi dei vettori rispettano GAS_VECTORS_DB (roadmap R7)
d576a9b chore(revisore): memoria review #397 — APPROVATO CON RISERVE
467ddf7 docs(fine-task): report, handoff, coda da_mergiare — avviso giro, firma in parallelo (5.2)
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

Nota: nei verdetti i caratteri invisibili citati dal revisore sono scritti come `<U+XXXX>` (stesso testo, solo resi visibili: il bot di verifica rifiuta i caratteri invisibili).

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
  - Prove: `<U+200B>.bashrc`, `a.py<U+200B>.txt` (così si chiude anche R-390-2), `a<U+FEFF>.secret` e `a.sh
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

### Review #397 (chat Motore) — commit 0fafbe9

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sezioni 5, 8, 9 e 10), le parti di reports/stato_progetto.md che riguardano R7 e i finding aperti, e le lezioni pertinenti della mia memoria (quelle sulla cartella di avvio e sul log nella root, review #306 e #310). Il diff non tocca la cronologia né `_get_window`, non simula l'output dei tool, lascia intatti il cap di 10 iterazioni e il fallback dei provider.

**Elementi del diff esaminati**
- `gas.py:48` — `_LOG_PATH = Path(__file__).resolve().parent / "gas_debug.log"`. Rischio esaminato: il log finisce in un posto diverso a seconda della cartella da cui parte Gas. Esito: ok. Ho importato gas da una cartella estranea e il gestore del log scrive su /home/user/Gas/gas_debug.log. Il log resta ignorato da git (.gitignore:10 e .gitignore:49). Il timer notturno (scripts/notte/com.gas.notte.plist:15) fa già `cd "$HOME/Gas"`, quindi per lui il percorso non cambia; il bot Telegram avviato da un'altra cartella ne guadagna.
- `gas.py:53` — il gestore del log (RotatingFileHandler) ora apre `str(_LOG_PATH)`. Rischio esaminato: crash all'import. Esito: ok. Il rischio esiste già oggi con la cartella di avvio; vedi il rischio escluso.
- `gas.py:4243` — il controllo Log di doctor ora guarda `_LOG_PATH`. Rischio esaminato: doctor lanciato su un'altra root misura il file sbagliato. Esito: ok. Ora misura il file che viene scritto davvero, cioè il comportamento corretto.
- `gas.py:856` — `_percorso_vettori`, usato dal kernel (gas.py:946), dalla sonda di doctor (gas.py:4376), da `reindex` (gas.py:4557), da `calibrate_vectors_cmd` (gas.py:4698) e da `eval_vectors_cmd` (gas.py:4744). Rischio esaminato: la nuova funzione non deve cambiare il comportamento del kernel. Esito: ok. È lo stesso codice di prima, solo spostato (strip, resolve, default). T37d e T93b passano.
- `gas.py:2049` — `_e_log_kernel`, invariato a parte la docstring. Rischio esaminato: effetto su cerca_testo ed elenca quando la root non è la cartella di gas.py. Esito: riserva (R-397-1).
- `tests/test_unit_kernel.py:6977` — T93a. Rischio esaminato: il test deve fallire se torna il bug. Esito: riserva (R-397-2).
- `tests/test_unit_kernel.py:6985` — T93b. Usa un VectorStore finto, salva e ripristina la variabile d'ambiente nel finally e cancella la cartella temporanea. Esito: ok. Se uno dei tre comandi torna al percorso predefinito, il test fallisce: la condizione `all(p == _alt93.resolve())` non regge più.

**Riproduzioni**
- Suite del kernel lanciata dalla radice del repo: 954 PASS, 0 FAIL.
- Sonda con root temporanea in una cartella estranea: il gestore del log punta a /home/user/Gas/gas_debug.log. Sia il file `<root>/gas_debug.log` sia il log vero risultano «log del kernel».
- Mutazione: gestore di nuovo con percorso relativo `"gas_debug.log"`. Lanciata dalla cartella del codice: 954/0, cioè la mutazione passa. Lanciata da /tmp: T93a FAIL.

**Finding**
- **R-397-1 (chat Motore) BASSA**: in gas.py:2066 la regola «cartella == root» di `_e_log_kernel` diventa obsoleta quando la root non coincide con la cartella di gas.py, perché il log vero non sta più lì. Un file dell'utente `<root>/gas_debug.log` viene saltato nella ricerca su cartella e contato come log del kernel. L'ho provato: con la root temporanea, cerca_testo risponde «1 log del kernel (gas_debug.log) non cercati» e il log vero è altrove. Nel caso normale (root = cartella del repo, come per il timer notturno) non cambia nulla. Correzione: tenere solo la regola che legge la cartella vera del log (baseFilename), oppure confrontare con `_LOG_PATH.parent`. Così si chiude anche il residuo che avevo dichiarato nella review #310.
- **R-397-2 (chat Motore) BASSA**: T93a non scopre il bug in CI, perché la CI lancia `python tests/test_unit_kernel.py` dalla radice del repo (.github/workflows/ci.yml:97). Lì percorso relativo e assoluto coincidono, e la mutazione «gestore relativo» passa. Il test fallisce solo se lanciato da un'altra cartella. Correzione: un sottoprocesso con cwd in una cartella temporanea che esegue `import gas` e stampa il baseFilename del gestore, con l'atteso uguale alla cartella del repo.
- **R-397-3 (chat Motore) COSMETICA**: la riga Config VECTORS_DB di doctor (gas.py:4434) calcola ancora il percorso a mano. Lo mostra senza resolve, quindi un percorso relativo appare diverso da quello che il codice usa davvero. Con la variabile fatta di soli spazi mostra il predefinito ma senza l'etichetta «(default)». Basta usare `_percorso_vettori(root)` anche lì.

**Rischio escluso (non verificato)**
- Cartella di gas.py non scrivibile, per esempio un VPS con il codice installato in sola lettura e Gas che gira con un altro utente. In quel caso l'apertura del log all'import solleva l'errore e Gas si ferma, senza ripiego. Il rischio c'era già prima con la cartella di avvio, ma ora non si aggira più cambiando cartella. Non l'ho riprodotto: in sviluppo il repo è scrivibile. Va tenuto presente al deploy sul VPS.
- launchd sul Mac non l'ho eseguito: ho solo letto il plist.

Memoria aggiornata con la riga #397 e una lezione nuova (un test sul percorso indipendente dalla cartella di avvio va lanciato da una cartella diversa da quella del codice), committata in d576a9b. File: /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #398 (chat Motore) — commit e706955

## VERDETTO: APPROVATO CON RISERVE

Review #398 (chat Motore), fetta di sicurezza sul cancello. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), la sezione di reports/stato_progetto.md su R1/5.2 e la parte finale della memoria del revisore. Nel diff non ci sono slicing della history né simulazioni di tool.

**Elementi del diff esaminati**
- `modules/gate/gate.py:180` — dopo NFKC toglie i caratteri Unicode Cf (invisibili). Rischio esaminato: che renda più permissivo qualcuno degli usi. Ho messo a confronto il gate.py di HEAD con quello staged sugli stessi percorsi:
  - `run.sh`+ZWSP e `x.s`+ZWSP+`h`: livello 1 → 2.
  - `.e`+ZWSP+`nv` e `docs/ke`+ZWSP+`ys`: livello 1 (lettura SAFE) → 3 (lettura DENY).
  - `<U+200B>/etc/passwd`: ora «percorso assoluto», quindi DENY. `.<U+200B>./x`: ora «../x», cioè traversal, quindi DENY. Togliere i Cf non può eliminare un `/` né un `..`: crea solo percorsi assoluti o traversal, quindi è più stretto.
  - `_in_denylist` (match per prefisso) e `_nome_da_segreto`: più stretti. `prod.env`+ZWSP+`x` resta DENY.
  - Esito: ok per la lettura, per la denylist, per livello_scrittura e per run_command.
- `modules/gate/gate.py:600` — `libero_dopo_lettura`: è l'unico caso PIÙ permissivo, vedi R-398-1. Esito: riserva.
- `tests/test_unit_gate.py:472` e `tests/test_unit_gate.py:489` — i casi nuovi di livello 3 e 2 con caratteri invisibili. Riprodotto: 770 passed. Esito: ok.
- `tests/test_unit_kernel.py:6985` — T93a2 importa gas in un sottoprocesso con cwd temporanea. Mutazione: con `_LOG_PATH = Path("gas_debug.log")` l'handler finisce nella cartella temporanea, quindi il test fallisce e discrimina. Riprodotto: kernel 955 PASS, 0 FAIL. Esito: ok.
- `gas.py:4434` — doctor usa `_percorso_vettori(root)` (variabile d'ambiente ripulita e risolta), e «(default)» guarda la variabile ripulita dagli spazi. È coerente con `gas.py:856`. Esito: ok.

**Finding**
- **R-398-1 (chat Motore) BASSA.**
  - Cosa succede: `libero_dopo_lettura` (`modules/gate/gate.py:600`) ora dà True a `notes/a.m<U+200B>d` e `notes/a.t<U+200B>xt`; con HEAD dava False. Il nome ripulito finisce con .md/.txt, quello del file vero no.
  - Perché il kernel non lo ferma: il suo ricontrollo sul file vero (`gas.py:2533`) passa di nuovo da `_normalize_path`, quindi toglie gli stessi caratteri e lascia passare.
  - Danno: basso. È un file di livello 1, con un'estensione che nessun interprete esegue, ancora soggetto al controllo di git check-ignore. Però contraddice la regola «a finestra contaminata restano liberi solo i documenti md/txt/csv».
  - Correzione proposta: in `libero_dopo_lettura`, return False se `relative_path` grezzo contiene un carattere Cf.
- **R-398-2 (chat Motore) COSMETICA.**
  - La pulizia dei Cf in `sembra_delicato` (`modules/gate/gate.py:555`) ora è ridondante.
  - Il controllo per sottostringa sul comando intero in `gate_classify` non toglie i Cf, quindi `--file=.e`+ZWSP+`nv` passa. Non è una regressione: il file vero ha un nome diverso da `.env`.

**Rischio escluso:** non ho provato una scrittura vera da parte del modello di un file con Cf nel nome attraverso `run_turn`, dentro la sandbox e con GAS_CWD diversa dalla root. Ho verificato solo le funzioni del gate e il percorso di codice del kernel (`gas.py:2533`), senza un giro agentico completo. Non ho verificato nemmeno il comportamento su macOS/APFS con nomi che contengono Cf (normalizzazione del filesystem): non è riproducibile qui.

**Memoria:** aggiunta la riga #398 con la lezione «una normalizzazione solo per il confronto rende più stretti i controlli che negano ma più larghi quelli che concedono: ogni funzione che concede va riprovata sul nome grezzo». Committata con `scripts/commit_memoria_revisore.sh` (ea98089), in /home/user/Gas/.claude/agents/memoria_revisore.md.

Ricordati di tracciare R-398-1 e R-398-2 in /home/user/Gas/reports/stato_progetto.md prima del commit.

---

### Review #399 (chat Motore) — commit 0614242

## VERDETTO: APPROVATO CON RISERVE

Review #399 (chat Motore): chiude R-398-1. Diff staged: modules/gate/gate.py (+5), tests/test_unit_gate.py (+4).

**Cosa ho controllato nel diff**
- modules/gate/gate.py:592 — `libero_dopo_lettura` restituisce False se il `relative_path` grezzo contiene un carattere Unicode Cf. A quel punto `rel` è sempre una stringa, perché `livello_scrittura` (modules/gate/gate.py:431) dà 3 a tutto ciò che non è una stringa. Rischio esaminato: restano scoperti altri caratteri invisibili? Ho provato zero-width space, word joiner, soft hyphen, BOM, RLO, U+180E e un tag char da 4 byte: tutti danno False. «notes/a.md» dà ancora True. Esito: ok.
- tests/test_unit_gate.py:794 — 3 casi nuovi (zero-width space nell'estensione .md e .txt, BOM nella cartella). Rischio esaminato: il test distingue la versione corretta da quella vecchia? Sì: a HEAD gli stessi nomi davano True (verificato sul file a HEAD). Esito: ok.
- gas.py:2533 (contesto) — il ricontrollo del kernel usa il nome risolto da gas.py:1970 `_file_rel_root`. Rischio esaminato: il nome risolto perde i Cf? Sonda con root temporanea: il symlink «notes/link.md» punta a «notes/a.m<U+200B>d», il nome risolto è 'notes/a.m<U+200B>d' e la funzione dà False. Esito: ok, anche il kernel nega.

**Test riprodotti**: gate 773 passed, kernel 955 PASS / 0 FAIL.

**Riserve**
- R-399-1 (chat Motore) BASSA, già presente prima di questa modifica (e anche prima di #398): è lo stesso tipo di buco, ma passa dalla normalizzazione NFKC (che unifica le varianti di uno stesso carattere). I nomi «notes/a.<U+FF4D>d» e «notes/a.<U+FF54>xt» (lettere a larghezza piena nell'estensione) danno True sia sul nome sia nel ricontrollo del kernel, ma il file vero non è un .md/.txt. Verificato anche sul codice a HEAD e prima di e706955. Il danno è basso (livello 1, estensione non eseguibile), ma contraddice la regola «solo documenti md/txt/csv». Correzione: controllare l'estensione sul nome GREZZO, oppure negare se `rel != unicodedata.normalize("NFKC", rel)`. Il secondo vale per tutto il nome e copre anche i Cf.
- R-399-2 (chat Motore) COSMETICA: i test coprono solo zero-width space e BOM. Mancano un caso NFKC e un test del kernel con un symlink che punta a un nome con Cf.

**Cosa non ho verificato**: il comportamento su filesystem che normalizzano i nomi da sé (APFS/HFS+ sul Mac, NTFS), che potrebbero far coincidere il nome grezzo con un file diverso. In dev c'è solo Linux/ext4, quindi non si può riprodurre.

**Memoria**: riga #399 con la lezione aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata (5ea821a). Lezione: se una normalizzazione serve solo per il confronto, chiudere il buco togliendo una sola categoria (Cf) lascia aperte le altre trasformazioni (NFKC). Nelle funzioni che concedono va confrontato l'esito sul nome grezzo, invece di elencare categorie.

---

### Review #400 (chat Motore) — commit b32cbea

## VERDETTO: APPROVATO CON RISERVE

Review #400 (chat Motore), sul diff staged. Chiude R-399-1. Ho letto prima CLAUDE.md (sezioni 1, 5, 8, 9, 10), la memoria del revisore e i finding #398 e #399.

**Elementi del diff esaminati**
- `modules/gate/gate.py:593` — `libero_dopo_lettura` ora nega anche quando `NFKC(rel) != rel`.
  - Rischio esaminato: altri modi di aggirare il controllo sull'estensione.
  - Sonde: «a.<U+FF4D>d», «a.<U+217F>d», «a<U+3002>md», «a.<U+24DC>d», «<U+FB01>le.md» danno tutte False.
  - Ricerca su tutti i caratteri che NFKC lascia invariati ma che casefold porta ad ASCII (ß, İ, ǰ, ẖ…), messi in ogni posizione delle estensioni md/txt/csv: 0 casi True.
  - Esito: ok.
- `modules/gate/gate.py:593` — serve ancora il controllo Cf separato? Sì: NFKC NON toglie i Cf (`NFKC("a<U+200B>") == "a<U+200B>"`, verificato). Senza quel controllo «a.m<U+200B>d» tornerebbe libero. Esito: ok, va tenuto.
- `tests/test_unit_gate.py:798` — 2 casi a larghezza piena negati e «caffè» (NFC) libero. Rischio esaminato: se il test distingue il codice giusto da quello sbagliato. A HEAD i casi a larghezza piena davano True (sonda della review #399), quindi i 2 nuovi casi falliscono senza la modifica. Esito: ok.
- Contesto, `gas.py:2533` — il ricontrollo del kernel passa il nome risolto dal filesystem a `libero_dopo_lettura`. Un nome NFD (accento decomposto: file creato su HFS+, oppure symlink verso un nome NFD) va quindi alla firma. È più stretto, mai più largo. Esito: riserva R-400-1.

**Riprodotti**: gate 776 passed, kernel 955 PASS / 0 FAIL.

**Finding**
- **R-400-1 (chat Motore) BASSA**: falsi negativi accettabili, perché l'azione va solo alla firma e non viene negata.
  - Nomi NFD come «caffè.md» danno False (sondato).
  - Lo stesso vale per nomi con «…», «ª», «º» o legature.
  - Nel caso normale non succede: il modello scrive NFC, e su Linux/APFS il nome viene conservato così com'è.
  - Da dichiarare nel commento del codice.
- **R-400-2 (chat Motore) COSMETICA**: manca un caso di test NFD (False atteso) e manca il symlink nel kernel. La parte symlink resta R-399-2.

**Rischio escluso**: non ho verificato davvero il comportamento su macOS (APFS/HFS+), perché in dev c'è solo Linux. Per lo stesso motivo non ho provato il ricontrollo del kernel con un symlink reale verso un nome NFD: l'ho ragionato sul codice.

**Memoria**: la riga #400 (chat Motore) è in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da sola (46bcd6f). Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 950 → 955 PASS, 0 FAIL (T77o2, T93a, T93a2, T93b). Blocco reale: `=== RIEPILOGO: 955 PASS, 0 FAIL ===`.
pytest `tests/test_unit_gate.py`: `776 passed` (745 a inizio sessione); `tests/test_unit_notte.py`: `103 passed`. pytest intero `1627 passed in 180.55s` sul commit 0fafbe9 (prima delle fette cancello).

## §6 STATO CI

CI NON VERIFICATA da qui (gh assente nel container); dati dai verdetti della verifica esterna e del bot su #233:
- caf5bdd (con f12e973): unit-suite success, handoff-check failure (handoff mancante).
- 9793154 (con 18c4628, 5a21053 e memorie): unit-suite success, handoff-check success.
- 73cca2d (con 1678804 e memorie): handoff-check success.
- b49f47b: handoff-check failure (handoff non aggiornato in quel push).
- 467ddf7: unit-suite success, handoff-check success; verifica-bot failure per caratteri invisibili nel verdetto (APPROVATO CON RISERVE nel testo).
- 0fafbe9, e706955, 0614242, b32cbea e memorie: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-391-1 (BASSA), R-391-2 (COSMETICA): avviso file delicati, scelte dichiarate.
- R-392-3, R-393-2 (COSMETICHE): MAX_COMPITI con /compito; log senza rotazione.
- R-395-1 (BASSA), R-395-2 (COSMETICA): nomi del catalogo con «-»/«_» iniziale; avvisi doppi/persi rari.
- R-396-1 (BASSA), R-396-2 (COSMETICA): tetto ~15 s non assoluto; doppio warning.
- R-397-1 (BASSA): `<root>/gas_debug.log` trattato come log se root ≠ cartella di gas.py.
- R-398-2, R-399-2, R-400-2 (COSMETICHE): Cf ridondante, test symlink/NFD mancanti.
- R-400-1 (BASSA): nomi NFD dopo una lettura alla firma (accettato).
- Verifica esterna #233: V-5 3° giro (giro ucciso dopo il marcatore: nessun avviso), V-2 bot (marcatore condiviso col timer) — BASSE.
