# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — avviso file delicati (R-390-1), giro notturno da Telegram (R1), compito della chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #233 (https://github.com/Gasss23/Gas/pull/233): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10). Numero e URL dall'API GitHub (`create_pull_request`), `gh` assente nel container.
2. Aprire la terza chat «Mani» col prompt in fondo a `reports/lavoro_parallelo.md`.
3. Prova dal vero sul Mac: bot acceso, `/compito <nome>` dal telefono.

---

## §1 SCOPE & ESITO FETTE

- **R-390-1 + note verifica esterna #232**: `FATTA` — review #391 (chat Motore) APPROVATO CON RISERVE.
- **Compito della chat Mani** (documento): `FATTA`.
- **R1 — giro o compito lanciato da Telegram**: `FATTA` — review #392 (chat Motore) APPROVATO CON RISERVE.
- **R-392-1/2 e V-3 verifica esterna #233**: `FATTA` — review #393 (chat Motore) APPROVATO CON RISERVE. V-2 #233 non serve (i `.sh`/`.py` finali vanno alla firma, livello 2: nota della review #393).
- **Roadmap 5.2 e R7**: `DEFERITA` — prossime fette.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  13 ++++++++-----
 modules/gate/gate.py               |  18 ++++++++++++++----
 modules/notte/notte.py             |  11 +++++++++--
 modules/telegram/bot.py            |  96 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/da_mergiare.md             |  29 +++++++++++++++++++++++------
 reports/diff_sessione.md           |  17 ++++++++++-------
 reports/handoff.md                 | 165 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------
 reports/lavoro_parallelo.md        |  17 ++++++++++++++++-
 reports/setup_notte.md             |   5 +++++
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  27 +++++++++++++++------------
 tests/test_unit_gate.py            |   7 +++++++
 tests/test_unit_notte.py           | 166 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 14 files changed, 499 insertions(+), 79 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 950 → 950 PASS, 0 FAIL (nessun test kernel nuovo). Blocco reale: `=== RIEPILOGO: 950 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py tests/test_unit_gate.py`: `858 passed in 7.76s` (notte 84 → 98 casi, gate 745 → 760).

## §6 STATO CI

CI NON VERIFICATA (gh assente nel container). Commit f12e973 e caf5bdd: run del push della PR #233 (la verifica esterna #233 ha letto unit-suite success, handoff-check failure per handoff mancante). Commit 18c4628, 5a21053 e i commit di memoria: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-391-1 (chat Motore, BASSA): `a.html.txt`, `x.js.md`, `a.ts.txt` non più segnalati (scelta dichiarata).
- R-391-2 (chat Motore, COSMETICA): `env` interno su `dev.env.md`; segni combinanti non tolti.
- R-392-3 (chat Motore, COSMETICA): compito oltre MAX_COMPITI «non trovato»; messaggio modificato rilancia.
- R-393-1 (chat Motore, BASSA): crash di Python prima del giro (codice 1) senza avviso.
- R-393-2 (chat Motore, COSMETICA): ramo «gas.py non trovato» senza riga di log; log senza rotazione; `run.sh` + invisibile finale.
- Verifica esterna #233: V-4 (Cc non tolti, cosmetica), V-5 (= R-391-2).
