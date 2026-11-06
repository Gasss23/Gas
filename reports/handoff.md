# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Fetta 3 voce: compiti lunghi in sottofondo (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 3 (numero e URL dalla risposta JSON di `create_pull_request`; `gh` nel cloud non è autenticato). Sì dell'operatore alla fetta (5 nov, confermato via M1 il 6 nov); con riserve il merge passa dal sì via M1 (CLAUDE.md §10).
2. Prova sul Mac dopo il merge: a voce un compito lungo («confronta tre offerte e fammi un riassunto»): Gas deve rispondere che ci lavora e poi avvisare su Telegram.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 3 — compiti lunghi in sottofondo**: `FATTA` — strumento `in_sottofondo` offerto solo a voce (scelto dal modello), processo separato `gas.py sottofondo <id>` col suo kernel, solo cervello forte (tetto incluso), avviso Telegram finale, un compito alla volta, coda privata `.gas_sottofondo/`. Review #695-M2 (MEDIA R-695-1 chiusa con le BASSE), #696-M2 APPROVATO CON RISERVE (R-696-1/2-M2 BASSE).
- **Correzioni dopo bot e verifica esterna sulla PR #345** (commit c19e9df): `FATTE` — bot V-1 MEDIA (avviso promesso anche quando Telegram non può avvisare → diniego con `notifica_possibile`) e V-2..V-4, verifica esterna V-1/V-2, R-696-2 (eccezione nel figlio → avviso), R-697-1 MEDIA (posto `attivo.json` vuoto/illeggibile → presa atomica tmp+`os.link`, posto vecchio ripulito), R-697-2/3, R-698-1 (killpg solo se il processo è davvero nostro, `_e_nostro`). Review #697-M2 APPROVATO CON RISERVE, #698-M2 BOCCIATO (chiusa), #699-M2 APPROVATO CON RISERVE (R-699-1/2-M2 BASSE).
- **Lettura a voce dei compiti finiti alla prossima attivazione** (fetta 3.2 della proposta): `DEFERITA — prossima fetta`.
- **Passaggio automatico oltre N giri** (fetta 3.3): `DEFERITA — opzionale`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  11 ++
 .github/workflows/ci.yml           |   7 +
 .gitignore                         |   1 +
 gas.py                             |  67 +++++++
 modules/gate/gate.py               |   3 +
 modules/sottofondo/__init__.py     | 334 ++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          | 120 +++++++++++++
 tests/test_unit_sottofondo.py      | 359 +++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 44dbe2d (merge della #344).

## §3 GIT LOG --ONELINE (sessione)

```
c19e9df fix(sottofondo): chiude bot #345 V-1..V-4, verifica esterna V-1/V-2, R-696-2, R-697-1/2/3, R-698-1
581e645 chore(revisore): memoria review #699 — APPROVATO CON RISERVE
bee724e chore(revisore): memoria review #698 — BOCCIATO
c50f530 chore(revisore): memoria review #697 — APPROVATO CON RISERVE
f3c3007 docs(voce): report di fine task — fetta 3 compiti in sottofondo (chat M2)
f9348b7 feat(kernel+voce): fetta 3 — compiti lunghi in sottofondo (strumento in_sottofondo a voce, processo separato, solo forte, avviso Telegram) (sì dell'operatore via M1) (chat M2)
a880e25 chore(revisore): memoria review #696 — APPROVATO CON RISERVE
db7a72c chore(revisore): memoria review #695 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #695-M2 sul primo stage di f9348b7 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #695-M2. Diff staged su feat/voce-v12-m2 (base 44dbe2d), 7 file, 409 righe aggiunte. Fetta 3, «compiti lunghi in sottofondo». Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), le parti utili di reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `gas.py:4885`: lo strumento `in_sottofondo` viene offerto solo nei turni a voce non effimeri. Il turno effimero azzera comunque `_offerta`. Rischio esaminato: strumento offerto a testo o nel parlato della stanza. Esito: ok (anche T105b lo copre).
- `gas.py:4568`: `_in_sottofondo` nega l'operazione se il turno non è a voce, se il cervello forte è spento o se il suo tetto è superato. Ogni eccezione diventa un diniego registrato nel log (§9). Rischio esaminato: modello che chiama lo strumento a testo, crash del kernel. Esito: ok. Il tetto vale anche nel processo separato: `run_turn(cervello="forte")` passa da `_cascata_provider("forte")` (`gas.py:946`, contesto), che usa solo claude-cli e non scende mai ai gratuiti (§2), e il ciclo ricontrolla il tetto prima di ogni chiamata (`gas.py:5009`, contesto).
- `gas.py:4841`: `_turno_voce` è uno stato del kernel che vale per il turno. Rischio esaminato: il percorso della firma. Esito: **riserva R-695-1-M2**, vedi sotto.
- `modules/sottofondo/__init__.py:100`: `avvia` lancia `[python, gas.py, "sottofondo", id]` senza shell, con `start_new_session` e input/output scartati. Il compito non compare negli argomenti visibili con `ps`. Rischio esaminato: iniezione negli argomenti e compito visibile ad altri processi. Esito: ok. L'id nasce da `strftime` più `token_hex`; nel figlio è ridotto a `Path(id).name`. Un id «attivo» fa leggere attivo.json, che non ha stato «in_coda», quindi il figlio esce con 1.
- `modules/sottofondo/__init__.py:56`: `_vivo` usa `os.kill(pid, 0)`. Rischio esaminato: processi orfani e zombie. Esito: **riserva R-695-2-M2**, vedi sotto.
- `modules/sottofondo/__init__.py:130`: il figlio esce dal ciclo con `break` al primo evento `final`. Il kernel salva la storia prima di emettere `final` (`gas.py:5177`, contesto), quindi nulla si perde. La storia condivisa fra i due processi passa dall'unione già esistente (`_save_history` con lock su file), la stessa che usano già voce e Telegram insieme. Esito: ok, con la riserva R-695-3-M2 per la chiusura esplicita.
- `modules/gate/gate.py:74`: `in_sottofondo` è classificato UNCERTAIN, quindi con finestra contaminata va alla firma. Esito: la classe è prudente, ma vedi R-695-1-M2.
- `modules/telegram/bot.py:942` (contesto): `applica_firma` è chiamata solo dal kernel del bot Telegram.

**Sonda dal vero.** Su un kernel nuovo, con `GAS_CLAUDE_CLI=1`, `execute_tool_call("in_sottofondo", '{"compito":"x"}', firmata=True)` restituisce «Operazione negata: in_sottofondo esiste solo nei turni a voce.»

**Test rilanciati nel venv.** `tests/test_unit_sottofondo.py`: 15 passed. `tests/test_unit_kernel.py`: 1092 PASS, 0 FAIL. T105a fa il giro completo previsto da §7 (strumento chiamato, risultato, risposta finale). La suite gate/voice_stt/claude_cli (989 passed) e il mutante dichiarato non li ho rilanciati.

**Wall of Shame e guardrail.** Nessuno slicing della storia: `testo[: n - 1]` in `_breve` taglia una stringa. Nessuna simulazione dei tool: il test finge il comando della CLI con il runner, come negli altri test. Il tetto di 10 iterazioni, `_get_window` e `_cap_window_chars` non sono toccati. Il diario registra solo la lunghezza del compito.

**Riserve (da tracciare in stato_progetto.md)**
- **R-695-1-M2 MEDIA: la firma di `in_sottofondo` non porta a nulla.** Con finestra contaminata il cancello chiede la firma. Però `applica_firma` gira nel kernel del bot Telegram, dove `_turno_voce` è False, e nega sempre. L'operatore firma e ottiene un diniego. È sicuro (si ferma in chiusura), ma il comportamento dichiarato non funziona. Due correzioni possibili:
  - con `firmata=True` saltare il controllo sul turno a voce, mantenendo forte e tetto;
  - negare subito senza chiedere la firma quando la finestra è contaminata.
  Serve un test con `firmata=True` su un kernel nuovo.
- **R-695-2-M2 BASSA: uno zombie blocca la coda.** Il server voce scarta l'oggetto Popen senza `wait`. Se il figlio viene ucciso (OOM, SIGKILL) prima di cancellare attivo.json, il suo pid diventa uno zombie e `os.kill(pid, 0)` lo vede vivo. La coda resta bloccata finché un altro Popen nel server non lo raccoglie. In pratica succede presto, perché i turni del forte lanciano la CLI con subprocess. Se il figlio finisce normalmente non succede.
- **R-695-3-M2 BASSA: chiusura del turno e avviso perso.**
  - `esegui` non chiama `close()` sul generatore dopo il `break`, come invece fa il server voce (R-677-1-M2). Oggi funziona perché CPython libera subito il generatore.
  - `esegui` ignora il rifiuto restituito da `avvisa_operatore_esito` (tetto di notifiche al giorno raggiunto, Telegram non configurato) senza scriverlo nel log: l'operatore non saprebbe mai che il compito è finito. Va registrato con `logging.warning`.
- **R-695-4-M2 BASSA: avvio fallito lascia residui.** Se Popen fallisce dopo `accoda`, il file del compito resta «in_coda» per sempre e attivo.json blocca la coda per 120 s. Inoltre `_scrivi_privato` e `job["compito"]` fuori dal try possono far terminare il figlio con un traceback, finito nel vuoto perché l'output è scartato. Gas non crasha, ma il figlio sì.

**Rischi esplicitamente esclusi (non verificati)**
- Comportamento reale su VPS e Mac: avvio con il vero `claude -p`, figlio che sopravvive alla chiusura del server voce, consegna su Telegram. Non riproducibile in dev.
- Corsa fra due `accoda` contemporanei: non la considero, perché il server voce è single-thread (`modules/voice/server.py:65`).
- Interleaving della storia fra voce e figlio sotto carico vero: mi affido al meccanismo di unione già esistente e ai suoi test, che non ho rilanciato.
- Iniezione di testo esterno nella risposta che va su Telegram: il destinatario è fisso (solo l'operatore) e il testo passa da `pulisci`, ma non ho fatto sonde con contenuti ostili.

**Memoria.** Riga contatore #695-M2 e 2 lezioni nuove aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate in db7a72c. L'index del diff staged (7 file) è rimasto intatto.

Review #696-M2 (bis di #695-M2) sul commit f9348b7 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #696-M2 (bis di #695-M2), diff STAGED su feat/voce-v12-m2 (base 44dbe2d), 7 file, 545 inserimenti. Ho letto CLAUDE.md, l'inizio di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md. Ho applicato le due lezioni del 2026-11-06: firma su un kernel nuovo e zombie dei Popen.

**Elementi del diff esaminati**
- `gas.py:4574`: con `firmata=True` salta solo il controllo «turno a voce»; il cervello forte (`_rung_disponibile`) e il tetto restano a 4577 e 4580. Rischio esaminato: vicolo cieco della firma (R-695-1-M2). **Sonda end-to-end**: `enqueue_approval("in_sottofondo")`, poi `resolve_approval(approved, utente 42)`, poi `applica_firma` su un GasKernel nuovo (`_turno_voce` assente, come nel bot Telegram). Risultato: `eseguita=True`, «Compito avviato in sottofondo», un solo avvio; la seconda `applica_firma` dà «già eseguita», quindi niente doppia esecuzione. Il gate continua a classificare `in_sottofondo` come UNCERTAIN. Esito: ok.
- `gas.py:4774`: il dispatch passa `firmata=firmata`. L'unico chiamante con `firmata=True` resta `applica_firma` (`gas.py:3620`, contesto), dopo il controllo dell'utente autorizzato, dell'hash e del reclamo. Rischio esaminato: aggiramento della firma. Esito: ok.
- `modules/sottofondo/__init__.py:110`: un thread daemon chiama `proc.wait()`. Rischio esaminato: uno zombie che `_vivo` vede vivo, con la coda bloccata (R-695-2-M2). **Sonda con Popen vero** (`true`): con `avvia` il figlio viene raccolto e `_vivo` dà False; con un Popen senza wait, lo zombie dà True. Quindi la correzione è efficace. Esito: ok.
- `modules/sottofondo/__init__.py:174`: nel finally viene chiamato `close()` del generatore del turno. A 198-201 un avviso negato, come stringa o come tupla di `avvisa_operatore_esito` (ho verificato i ritorni in `modules/telegram/avviso.py:150`), finisce in `logging.warning`. Rischio esaminato: R-695-3-M2. Esito: ok.
- `gas.py:4594`: se Popen fallisce dopo `accoda`, `annulla` mette il job a «ko» e libera `attivo.json`. `annulla` (`modules/sottofondo/__init__.py:115`) non lancia mai eccezioni e libera la coda solo se l'id coincide. Il wrapper `esegui` (`modules/sottofondo/__init__.py:136`) trasforma ogni eccezione in annulla + 1. Rischio esaminato: R-695-4-M2, job orfano e 120 s di blocco. Esito: ok (T105e).
- `tests/test_unit_sottofondo.py:118` e `tests/test_unit_sottofondo.py:140`: test del reaping e della chiusura del turno con riferimento vivo, più il caplog a 164 e il compito corrotto a 174. Ho rilanciato le suite: **20 passed**, kernel **1094 PASS, 0 FAIL**. Esito: ok.
- Guardrail: nessuno slicing della history e nessuna simulazione dell'output dei tool. Il cap di 10 iterazioni e `_get_window` non sono toccati. Nel diario va solo la lunghezza del compito. Esito: ok.

**Riserve (BASSE)**
- **R-696-1-M2 BASSA**: in un turno Telegram il modello può chiamare `in_sottofondo` anche se lo strumento non gli è offerto. Con la finestra contaminata, la classe UNCERTAIN parcheggia la richiesta per la firma e, se l'operatore firma, il compito parte. Con la finestra pulita invece viene negato. È un'asimmetria, non un aggiramento: serve comunque la firma esplicita e il read-back mostra il compito. Correzione possibile: negare prima del parcheggio quando il turno non è a voce.
- **R-696-2-M2 BASSA**: se il wrapper `esegui` intercetta un'eccezione, `annulla` registra il «ko» ma non manda nessun avviso Telegram. L'operatore, a cui a voce è stato detto «ti avviserò», resta in attesa senza saperlo. C'è solo il warning in gas_debug.log.

**Rischi esclusi (non verificati)**
- Comportamento reale sul Mac o sulla VPS: il processo `gas.py sottofondo` con `claude -p` vero e l'avviso Telegram vero non sono riproducibili qui senza credenziali. Le sonde usano un `avvia` finto e `true` come figlio.
- Concorrenza fra due `accoda` simultanei, server voce e bot nello stesso istante: la finestra fra `attivo()` e la scrittura non ha lock. È preesistente rispetto a #695 e non l'ho sondata.
- Il passaggio della CI `.github/workflows/ci.yml` (nuovo step pytest) non è stato eseguito su GitHub.

**Memoria**: riga `#696-M2` e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (a880e25). Il diff staged è rimasto intatto (7 file).

File della sonda: /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda696/p.py

Review #697-M2 sul primo stage di c19e9df (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #697-M2 (branch feat/voce-v12-m2, PR #345, base f3c3007). Ho esaminato il diff STAGED su gas.py, modules/sottofondo/__init__.py, tests/test_unit_kernel.py e tests/test_unit_sottofondo.py. Ho rilanciato i test: test_unit_sottofondo 26 passed, kernel 1096 PASS 0 FAIL. Le sonde le ho fatte su una root temporanea nello scratchpad.

**Elementi del diff esaminati**
- `gas.py:4585` — chiama `notifica_possibile` prima di `accoda` e nega con il motivo. Rischio esaminato: la promessa di avviso potrebbe non partire, e il controllo stesso potrebbe sollevare un'eccezione. Il controllo sta dentro il try §9 già esistente. Il residuo dichiarato (l'ultimo posto può essere consumato dal figlio o da `_ripulisci`) è accettabile. — ok
- `modules/sottofondo/__init__.py:115` — `notifica_possibile` usa `_max_giorno`, `_manca_configurazione`, `_uso_oggi` e `USO_FILENAME` di modules/telegram/avviso.py. Rischio esaminato: accoppiamento con funzioni private. Ho controllato le firme a HEAD (`modules/telegram/avviso.py:42`, `modules/telegram/avviso.py:57`, `modules/telegram/avviso.py:95`): combaciano. Se cambiano nome, l'eccezione finisce in un diniego, quindi in caso di dubbio non si promette nulla. Accoppiamento accettabile; meglio che avviso.py esponga in futuro una funzione pubblica `posso_avvisare(root)`. — ok
- `modules/sottofondo/__init__.py:87` — età calcolata da `creato`, durata massima di almeno 60 s, pid None tollerato entro 120 s. Rischio esaminato: liberare il posto di un compito vivo, o di uno appena accodato. Un compito appena accodato (pid None, meno di 120 s) non viene toccato: `_ripulisci` esce subito. Un `creato` assente vale come età enorme, quindi il posto risulta libero: corretto. — ok
- `modules/sottofondo/__init__.py:154` — il posto si prende con O_CREAT|O_EXCL. Rischio esaminato: un `attivo.json` che esiste ma è illeggibile. **SONDA**: con `attivo.json` vuoto (anche con mtime del 1970) `accoda` risponde «c'è già un compito in sottofondo» per sempre. `_ripulisci` (`modules/sottofondo/__init__.py:101`) esce su `not dati` e O_EXCL fallisce. Prima della modifica un file corrotto veniva ignorato e sovrascritto: questa è una regressione. Il caso si presenta con un crash o un ENOSPC fra `os.open` e `json.dump`; lo stesso `json.dump` che fallisce lascia il file vuoto. — riserva MEDIA (R-697-1-M2)
- `modules/sottofondo/__init__.py:96` — `_ripulisci` marca ko il compito e avvisa. Rischio esaminato: cancellare il posto di un compito vivo. **SONDA**: con un pid vivo (il mio processo) e `creato` di 2 ore fa, il compito viene marcato ko, l'avviso dice «il processo si è interrotto» e parte un secondo compito. Il primo processo non viene fermato: quando finisce riscrive lo stato ok e manda un secondo avviso, che contraddice il primo. — riserva BASSA (R-697-2-M2)
- `modules/sottofondo/__init__.py:107` — `unlink` incondizionato di `attivo.json` dopo `annulla`. Rischio esaminato: una corsa fra il processo della voce e quello del bot Telegram. A legge il posto morto X; B ripulisce e prende il posto Y con O_EXCL; A esegue l'unlink e cancella Y; poi A prende Z. Risultato: due compiti insieme, e la garanzia di O_EXCL non regge. La finestra è stretta. `annulla` fa già l'unlink filtrato per id; serve solo per i posti senza id. — riserva BASSA (R-697-3-M2)
- `modules/sottofondo/__init__.py:224` — l'eccezione nel wrapper `esegui` porta ad `annulla` più `_avvisa`, e `_avvisa` (`modules/sottofondo/__init__.py:194`) intercetta eccezioni e rifiuti e li scrive nel log. Rischio esaminato: un'eccezione che esce dal processo figlio. — ok (R-696-2-M2 chiusa)
- `tests/test_unit_sottofondo.py:180` e seguenti — nuovi test su `notifica_possibile`, processo morto, durata massima, corsa con O_EXCL, eccezione e comando vero via subprocess. — ok. Nessun test copre `attivo.json` vuoto o corrotto né il compito vivo oltre la durata: sono proprio i due casi delle riserve.

**Riserve**
- **R-697-1-M2 MEDIA** — un `attivo.json` illeggibile blocca la coda per sempre, con un messaggio falso: il modello dirà all'operatore «ne sto già facendo uno». Correzione suggerita: in `_ripulisci`, se il file esiste ma `_leggi` dà None e l'mtime è più vecchio di 120 s, cancellarlo. Conviene anche scrivere il contenuto prima di prendere il posto: tmp, poi `os.link` su `attivo.json` (atomico ed esclusivo), poi unlink del tmp. Consiglio di correggerla prima del push: costa poco.
- **R-697-2-M2 BASSA** — oltre la durata massima il processo vivo non viene fermato. Va fermato (`os.killpg`, è disponibile perché c'è `start_new_session`) oppure l'avviso deve dire «oltre la durata massima». Inoltre `_esegui` non deve sovrascrivere uno stato ko con ok.
- **R-697-3-M2 BASSA** — l'unlink incondizionato a `modules/sottofondo/__init__.py:107` va fatto solo quando il posto riletto ha ancora lo stesso id (o è senza id). Nota collegata, già presente prima di questa modifica: `_esegui` (`modules/sottofondo/__init__.py:237`) sostituisce `attivo.json` senza controllare l'id. Un figlio partito in ritardo potrebbe sovrascrivere il posto di un altro compito; la finestra è stretta.

Effetti dell'avviso dentro `accoda`: `_ripulisci` può mandare un messaggio Telegram durante il turno voce. Questo aggiunge la latenza della rete alla risposta parlata e consuma un posto del tetto giornaliero dopo che `notifica_possibile` aveva già detto sì. È accettabile come residuo dichiarato, da annotare.

Wall of Shame: nessuno slicing della storia, nessuna simulazione di output dei tool. Guardrail §8 (cap delle iterazioni) non toccato. §9 rispettato nei provider e nel figlio.

**Rischi esplicitamente esclusi**
- Comportamento su macOS (VPS/Mac) di O_EXCL e del riuso dei pid: non riproducibile qui.
- Invio reale su Telegram: nessuna configurazione in dev.
- La corsa R-697-3-M2 l'ho ricostruita leggendo il codice, non riprodotta con due processi veri.

La memoria è aggiornata in /home/user/Gas/.claude/agents/memoria_revisore.md (riga #697-M2 più una lezione sui lock con O_EXCL e i file corrotti), committata in c50f530.

Review #698-M2 sul secondo stage di c19e9df (verdetto integrale):

## VERDETTO: BOCCIATO

Review #698-M2 (bis di #697-M2). Chat M2, branch feat/voce-v12-m2, PR #345, base f3c3007. Ho esaminato il diff staged (4 file, +310/−18). Letture obbligatorie fatte: CLAUDE.md, la sezione di reports/stato_progetto.md sul sottofondo (riga 615), la coda della memoria.

**Motivo bloccante (uno solo, si corregge con poco)**
- **R-698-1-M2 MEDIA.** In modules/sottofondo/__init__.py:121 si chiama `os.killpg(int(pid), SIGTERM)` sul pid letto da attivo.json. Prima non si controlla che quel pid sia ancora il nostro figlio `gas.py sottofondo <id>`.
  - Quando succede: il figlio muore senza pulizia (riavvio del Mac o della VPS, `kill -9`). Il docstring di `_ripulisci` cita proprio questo caso («ucciso, riavvio»). Poi per più di 60 minuti nessuno accoda nulla. Al primo `accoda` successivo, se il pid è stato riusato, `_vivo(pid)` risponde True.
  - Perché è grave: `killpg` manda SIGTERM a tutto il gruppo di quel pid. Dopo un riavvio i pid ripartono bassi. Su macOS molte app dell'operatore sono leader del proprio gruppo e girano con lo stesso utente, quindi niente EPERM. Risultato: un'app o una shell dell'operatore chiusa, con perdita di lavoro non salvato.
  - Sonda (/tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda698.py): un `sleep 100` con sessione propria fa da processo estraneo. attivo.json ha il suo pid e `creato` di 2 ore fa. `accoda` restituisce un id nuovo, il processo estraneo termina con -15, e parte l'avviso «oltre la durata massima, fermato».
  - È peggio del difetto che corregge: R-697-2 era BASSA (avviso falso, due compiti insieme), questo è un danno irreversibile su processi fuori dal perimetro di Gas.
  - **Correzione suggerita.** Prima di `killpg`, verificare l'identità e, se non è certa, NON uccidere: marcare comunque ko e liberare il posto.
    - Controlli possibili: `os.getpgid(pid) == pid`, e riga di comando del processo (`ps -o command= -p <pid>`, che funziona su macOS e Linux) contenente `sottofondo <ident>`.
    - Va bene anche: salvare in attivo.json l'ora d'avvio del processo e confrontarla.
    - Test da aggiungere: pid vivo ma estraneo (comando diverso) → nessun `killpg`, compito ko, posto libero.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:181` — il posto si prende con `os.link(tmp, attivo.json)`; il tmp viene da `_scrivi_privato` (0600, scrittura atomica) e si toglie nel `finally`. Rischio: posto vuoto o corrotto dopo un crash, e `os.link` su macOS/APFS. Esito: ok, R-697-1-M2 chiusa.
  - Il file nasce già completo, e `FileExistsError` porta a «occupato».
  - APFS supporta gli hard link (anche HFS+).
  - Su un filesystem senza hard link (exFAT, SMB) `os.link` alza un OSError diverso da `FileExistsError`. Nella sonda (PermissionError) il tmp viene tolto e la cartella resta vuota. L'eccezione esce da `accoda` e viene presa da gas.py:4598, che risponde «non accodato». Quindi niente crash, ma la funzione resta sempre negata: nota BASSA, irrilevante per ~/Gas su APFS.
- `modules/sottofondo/__init__.py:96` — `_ripulisci`: un posto illeggibile con mtime oltre 120 s viene tolto; poi `annulla`, rilettura e unlink solo se l'id è lo stesso. Rischio: lock eterno, e posto altrui cancellato in una corsa. Esito: ok, R-697-3-M2 chiusa.
  - Resta una finestra TOCTOU fra rilettura e unlink: molto stretta e non sfruttabile in pratica.
  - Nota: `annulla` toglie già il posto quando l'id combacia, quindi l'unlink di `_ripulisci` serve solo se `annulla` fallisce.
- `modules/sottofondo/__init__.py:270` — `_esegui` parte solo se il posto è suo, altrimenti annulla e restituisce 1. Rischio: un figlio in ritardo (oltre 120 s) che ruba il posto a un altro compito. Esito: ok, coperto da `test_figlio_senza_posto_non_ruba`.
- `modules/sottofondo/__init__.py:303` — un esito tardivo non sovrascrive uno stato ko già scritto. Rischio: doppio esito e doppio avviso. Esito: ok. Con SIGTERM e senza handler il processo muore prima comunque; la guardia copre il caso di un `kill` non riuscito.
- `modules/sottofondo/__init__.py:121` — `killpg`. Esito: **blocco**, vedi sopra. Il figlio nasce con `start_new_session=True` (modules/sottofondo/__init__.py:200), quindi per il nostro figlio pid e gruppo coincidono e il caso legittimo funziona. Il problema è solo l'identità di un pid riusato.
- `gas.py:4585` — `notifica_possibile` viene chiamata prima di `accoda`, dentro il try §9. Rischio: promettere un avviso Telegram che non può partire. Esito: ok, coperto dal test T105f in tests/test_unit_kernel.py.

**Test rilanciati**
- tests/test_unit_sottofondo.py: 31 passed.
- tests/test_unit_kernel.py: 1096 PASS, 0 FAIL (venv del scratchpad).

**Rischi esplicitamente esclusi**
- `os.link` e `killpg` non li ho provati su macOS reale: niente Mac in questo ambiente. La semantica di APFS e dei gruppi di processi l'ho valutata dalla documentazione POSIX; la sonda sul pid riusato è su Linux.
- Avviso Telegram reale non verificato: nei test `avvisa` è sostituito da una funzione finta.

**Riserve precedenti ancora aperte (invariate)**
- R-696-1-M2 BASSA: `in_sottofondo` chiamato da Telegram con finestra contaminata parte lo stesso con la firma.

**Memoria aggiornata**
- Riga #698-M2 e una lezione nuova (mai kill/killpg su un pid letto da file senza verificarne l'identità) in /home/user/Gas/.claude/agents/memoria_revisore.md.
- Committata con scripts/commit_memoria_revisore.sh (bee724e). Il diff staged sotto review è rimasto intatto.

Review #699-M2 sullo stage finale di c19e9df (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #699-M2 (seconda revisione dopo il BOCCIATO #698-M2). Chat M2, branch feat/voce-v12-m2, PR #345, base f3c3007. Diff staged su 4 file (sha256 del diff 0cb455dd9e71…).

Ho letto prima: CLAUDE.md (sezioni 5, 8, 9), le righe di reports/stato_progetto.md sulla fetta 3 sottofondo e le ultime voci della mia memoria, compresa la lezione di #698 sui kill fatti su un pid letto da file.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:142` — `_e_nostro` controlla tre cose: il pid è un int > 1, il processo è capo del proprio gruppo, e `ps -o command=` (timeout 5 s) restituisce codice 0, con un comando che finisce con `sottofondo <id>` e contiene `gas.py`. Qualsiasi eccezione dà False.
  - Rischi esaminati: pid passato come bool o come stringa, id che è la coda di un altro id, comando troncato da `ps`, processo che non è capo del gruppo.
  - Sonde fatte da me (scratchpad, file sonda699.py):
    - `True` e `"123"` come pid → False.
    - id «1» contro un comando «sottofondo 21» → False.
    - processo senza sessione propria → False.
    - percorso di gas.py lungo più di 300 caratteri → riconosciuto (con output non su terminale `ps` non tronca).
  - Esito: ok.
- `modules/sottofondo/__init__.py:123` — `os.killpg` parte solo se il compito ha superato la durata massima, il processo è vivo e `_e_nostro` dice sì.
  - Rischio: il caso bloccante di R-698-1-M2.
  - Sonda698 rifatta: un `sleep` estraneo con sessione propria al posto del pid resta vivo (poll None), il compito diventa ko e il nuovo compito viene accodato. Con un figlio vero oltre la durata, il processo viene fermato (-15).
  - Esito: ok, **R-698-1-M2 chiusa**.
- `modules/sottofondo/__init__.py:127` — il motivo «oltre la durata massima, fermato» viene scritto nel compito e nell'avviso Telegram anche quando il pid non era nostro o `killpg` è fallito. Nel ramo «non nostro» non viene scritta nessuna riga in gas_debug.log.
  - Esito: riserva (R-699-1-M2).
- `tests/test_unit_sottofondo.py:328` — test con un processo estraneo vero: nessun `killpg`, processo ancora vivo, compito ko, nuovo compito accodato.
  - Esito: ok.
- `tests/test_unit_sottofondo.py:348` — test con un figlio vero simulato: riconosciuto per «abc123», non per «altro».
  - Esito: ok.
- Contesto: `gas.py:4593` intercetta qualsiasi eccezione di `accoda`. Un `OSError` di `os.link` su un filesystem senza hard link diventa un diniego, non un crash, e il file temporaneo viene tolto (verificato).
  - Esito: ok.

**Rilanciati**: test_unit_sottofondo 33 passed, test_unit_kernel 1096 PASS e 0 FAIL. Nessuno slicing della history, nessuna simulazione di tool, nessun guardrail indebolito.

**Riserve**
- **R-699-1-M2 BASSA** — se il pid non è nostro (o `killpg` fallisce), l'avviso all'operatore dice comunque «fermato» e non resta traccia nel log. Correzione: motivo distinto («processo non riconosciuto, non fermato») più un `logging.warning`.
- **R-699-2-M2 BASSA** — dove `ps` non c'è (container minimale), un figlio nostro oltre la durata non viene mai fermato e gira in parallelo al nuovo compito, senza avvisi. L'esito tardivo è comunque scartato grazie al controllo `stato == "ko"`. Correzione: log quando `ps` fallisce, oppure ripiegare su `/proc/<pid>/cmdline` su Linux.

**Rischi esclusi (non verificati)**
- Comportamento reale di `ps` su macOS (versione BSD) e la riga di comando del Python framework sul Mac dell'operatore: non riproducibili in questo ambiente Linux. Secondo la man page, con output non su terminale BSD `ps` non tronca.
- Gara fra il controllo di `_e_nostro` e `killpg` (il pid viene riusato in quei millisecondi): finestra trascurabile, non provata.

**Memoria**: riga #699-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, più una lezione: dopo un controllo d'identità che può dire «no», i messaggi a valle non devono promettere l'azione saltata. Committata con scripts/commit_memoria_revisore.sh (commit 581e645).

Sonde nello scratchpad: /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda698.py e /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda699.py

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T105a-e (voce: in_sottofondo offerto e avviato — round-trip §7; testo negato; forte spento; firma; avvio fallito), T105f (avviso impossibile → diniego), T105g (finestra contaminata → serve la firma). Suite kernel `=== RIEPILOGO: 1096 PASS, 0 FAIL ===` (prima della fetta 1089). `tests/test_unit_sottofondo.py` (nella CI): 33 passed (coda, permessi, presa atomica del posto, posto vuoto vecchio/recente, durata massima, killpg solo se nostro, pid estraneo non fermato, eccezione → avviso, esito tardivo, comando vero). Prova dal vero: `gas.py sottofondo inesistente` → exit 1 con warning.

## §6 STATO CI

`gh` non autenticato nel cloud. Sulla head f3c3007 la CI (`unit-suite`, `handoff-check`) era verde; il bot aveva dato BOCCIATO (V-1 MEDIA, chiusa in c19e9df). I commit nuovi sono pushati insieme a questo report: run non ancora disponibile alla scrittura.

## §7 RISERVE APERTE

- R-696-1-M2 BASSA: in un turno Telegram con finestra contaminata il modello può chiamare in_sottofondo (non offerto) e, con la firma dell'operatore, il compito parte; a finestra pulita è negato.
- R-699-1-M2 BASSA: oltre la durata massima, se il processo non è nostro o killpg fallisce, l'avviso dice comunque «fermato» e non resta traccia nel log.
- R-699-2-M2 BASSA: dove `ps` non c'è, un figlio nostro oltre la durata non viene fermato (resta in parallelo al compito nuovo).
- Residui noti: l'ultimo avviso Telegram del giorno può essere consumato dal compito finito; il controllo `notifica_possibile` dentro la chiamata aggiunge un po' di latenza.
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero.
