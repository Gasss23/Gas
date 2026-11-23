# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — R7 fetta 4: tetto di tempo duro del compito in sottofondo (sotto-chat di M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #402 (https://github.com/Gasss23/Gas/pull/402), etichetta «verifica». Tocca il motore: merge autonomo solo con verdetto testuale del bot APPROVATO senza finding V-x, CI verde e niente conflitti; con riserve la PR resta aperta e il merge lo chiede M1 all'operatore.

Numero e URL della PR presi dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `402` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 4 R7 — tetti di tempo duri (parte sottofondo)**: FATTA. Timer demone col tempo rimasto (dalla prima creazione): alla scadenza «ko», avviso, arresto del gruppo di processi; «ko» subito se il tempo è già finito; un solo esito tra timer e fine turno; attesa del timer limitata a 30 giorni. Review #852-R7 → #853-R7.
- **Tetto duro del compito del giro di notte**: DEFERITA — prossima PR (il giro gira nel processo principale: serve un altro meccanismo).
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA.
- **Anomalia di sessione**: nel primo tentativo di scrivere questo handoff un heredoc non quotato ha fatto eseguire alla shell alcuni testi tra backtick (solo comandi di lettura o falliti: una GET sulle PR, `gh pr` rifiutato, `claude -p` uscito subito per input mancante). Nessuna scrittura; il commit 12ab9019 è partito con l'handoff vecchio, corretto dal commit successivo.

---

## §2 GIT DIFF --STAT (sessione)

```
.claude/agents/memoria_revisore.md |   4 ++++
 modules/sottofondo/__init__.py     |  76 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  10 ++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  20 +++++++-------------
 tests/test_unit_sottofondo.py      | 122 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
12ab9019 docs(fine-task): R7 fetta 4 — report, handoff con review #852-R7/#853-R7, stato_progetto
a56e9df9 feat(sottofondo): R7 fetta 4 — tetto di tempo duro: il processo in sottofondo si ferma da solo alla durata massima
ba75ec24 chore(revisore): memoria review #853 — APPROVATO CON RISERVE
36f1c779 chore(revisore): memoria review #852 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit a56e9df9 (motore): review #852-R7 sul primo staged e #853-R7 dopo le correzioni di R-852R7-2/3 (e della docstring per R-852R7-1/4). Incollati integrali.

### Review #852-R7

## VERDETTO: APPROVATO CON RISERVE

Review #852-R7: R7 fetta 4, «tetto di tempo duro» del compito in sottofondo. Branch claude/r7-tetti-di-tempo, diff staged di 2 file (+144/−0), sha256 del diff cbf6d709.

Ho letto CLAUDE.md (sez. 5, 8, 9), lo stato del progetto e la memoria del revisore (numero libero dopo #851). Ho controllato il Wall of Shame: nel diff non c'è slicing della history e non c'è simulazione di output dei tool. Il diff non tocca il cap di 10 iterazioni, `_get_window` né i provider.

**Verifiche eseguite**
- Test: 135 passed in tests/test_unit_sottofondo.py, su una copia dell'indice.
- Mutanti: 5 su 5 uccisi:
  - ramo «tempo già finito» spento;
  - `tetto.cancel()` tolto;
  - `_termina_processo` non chiamato;
  - `_nel_futuro` ignorato;
  - `annulla` tolto da `_scaduto`.
- Prova reale da capo a fondo, senza mock su timer e uscita:
  - setup: processo lanciato con start_new_session, turno appeso in `time.sleep(100)`, un figlio `sleep 100` nello stesso gruppo, 3 s rimasti al tetto;
  - risultato: processo fermato in 3,5 s con codice d'uscita −15; compito «ko» con «oltre la durata massima, fermato»; avviso inviato; riga scritta su file nel log; figlio `sleep` morto.

**Elementi del diff esaminati**
1. `modules/sottofondo/__init__.py:880` — arma il timer demone col tempo rimasto, mentre il generatore del kernel è in corso nel thread principale. Rischio: un thread che chiude il processo mentre il generatore è a metà. Esito **ok**. `os._exit` salta la pulizia, ma `_save_history` scrive su file temporaneo e poi fa `os.replace` (gas.py:1938), quindi è atomica, e SQLite è protetto dal journal. Il timer gira anche se il thread principale è bloccato in I/O, perché l'I/O bloccante rilascia il GIL.
2. `modules/sottofondo/__init__.py:824` — `killpg` del proprio gruppo, poi `os._exit`. Rischio: perdere log non scritti. Esito **ok**: il RotatingFileHandler (gas.py:67) scrive su disco a ogni riga, e la prova reale lo conferma. Rischio: colpire un gruppo che non è il nostro. Esito **ok**: l'unico chiamante è gas.py:7355, il processo separato lanciato da `avvia` (`modules/sottofondo/__init__.py:733`, start_new_session).
3. `modules/sottofondo/__init__.py:818` — la docstring promette di fermare anche i figli `claude -p`. Esito **riserva**, vedi R-852R7-1.
4. `modules/sottofondo/__init__.py:871` — `_scaduto`, cioè `annulla` + avviso + uscita in `finally`. Rischio: corsa con la scrittura dell'esito. Esito **riserva**, vedi R-852R7-2. Quando il timer scatta DOPO un «ok», `annulla` non riscrive il compito: è provato da `tests/test_unit_sottofondo.py:1470` → **ok**.
5. `modules/sottofondo/__init__.py:864` — tempo rimasto contato dalla prima creazione; se è già finito alla partenza, il compito chiude «ko» con avviso. Esito **ok**, coperto da `tests/test_unit_sottofondo.py:1453`. Con un controllo esterno in parallelo (`controlla` / `attivo`) non c'è doppio avviso, perché `annulla` restituisce True una volta sola.
6. `modules/sottofondo/__init__.py:812` — `threading.Timer(max(0.0, secondi))` senza tetto superiore. Esito **riserva**, vedi R-852R7-3.
7. `tests/test_unit_sottofondo.py:1433` — il test fa scattare il timer in modo sincrono dentro il generatore e sostituisce `_termina_processo`. Rischio: un test che non esercita il thread vero né l'uscita vera. Esito **ok**: copre lo stato, e il thread vero l'ho provato a mano (sopra), insieme a `tests/test_unit_sottofondo.py:1486`.

**Riserve (da tracciare in stato_progetto.md)**
- **R-852R7-1 BASSA** — `claude -p` e il browser restano vivi dopo lo stop.
  - Causa: `claude -p` (`brains/claude_cli.py:428`) e il browser/Chromium (`modules/web/browser.py:496`) partono con start_new_session=True, quindi in un gruppo proprio. Il `killpg` di `modules/sottofondo/__init__.py:824` non li raggiunge, e il loro timer interno muore con il processo padre. La docstring di `modules/sottofondo/__init__.py:818` dice il contrario.
  - Danno limitato: `claude -p` ha `--tools ""`, quindi nessun effetto collaterale, e muore su EPIPE quando prova a scrivere. Però finisce la richiesta in corso e consuma l'abbonamento. I comandi di `run_command` invece stanno nello stesso gruppo (gas.py:5361) e vengono fermati.
  - Correzione: sistemare la docstring e dichiarare il limite, oppure registrare i pgid dei figli e fermarli prima di uscire.
- **R-852R7-2 BASSA** — corsa tra il timer e la fine del turno.
  - Causa: non c'è mutua esclusione tra `_scaduto` (`modules/sottofondo/__init__.py:871`) e la parte finale di `_esegui` (`modules/sottofondo/__init__.py:915` fino a `modules/sottofondo/__init__.py:941`). Se il timer parte nei pochi ms in cui il turno finisce, si può avere:
    - «ok» scritto sopra «ko»;
    - due avvisi contraddittori;
    - oppure «ok» scritto e poi `os._exit` durante l'invio di «Ho finito», con l'avviso perso.
  - Correzione: un `threading.Lock` più un flag «esito scritto», presi sia da `_scaduto` sia dal thread principale prima di `cancel()`.
- **R-852R7-3 BASSA** — tetto duro spento in silenzio con valori enormi.
  - Prova: con GAS_SOTTOFONDO_MAX_MIN ≥ circa 1,5e8 (provato 1e9; threading.TIMEOUT_MAX = 9,2e9 s) il thread del Timer muore subito con OverflowError. Lo stderr va su DEVNULL e in gas_debug.log non resta nulla: §9 non rispettato.
  - Resta attivo solo il controllo vecchio, quello fatto da un altro processo.
  - Correzione: `min(secondi, threading.TIMEOUT_MAX)` oppure un limite superiore in `_durata_max_s`.
- **R-852R7-4 COSMETICA** — il SIGTERM al proprio gruppo uccide anche il processo stesso, quindi esce con codice −15 e `os._exit(1)` (`modules/sottofondo/__init__.py:827`) serve solo come riserva. Va bene, ma la docstring e il commento dovrebbero dirlo.

**Rischi esclusi (non verificati)**
- Comportamento su macOS/launchd e su VPS: provato solo su Linux nel container.
- Orfano `claude -p` reale con la CLI vera: CLI non disponibile in dev, ricavato solo dal codice.
- Durata dell'avviso Telegram dentro `_scaduto`: non ho verificato il timeout di rete di `avvisa_operatore_esito`. Se Telegram resta appeso, ritarda solo l'uscita.

**Memoria**
- Riga contatore #852-R7 e una lezione nuova aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (36f1c779).
- Il diff staged sotto review è intatto.

File rilevanti:
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/brains/claude_cli.py
- /home/user/Gas/modules/web/browser.py

### Review #853-R7

## VERDETTO: APPROVATO CON RISERVE

Review #853-R7, secondo giro di #852-R7. Branch claude/r7-tetti-di-tempo. Il diff staged tocca 2 file (+198/−0), sha256 del diff 084f4c5b.

Prima della review ho riletto CLAUDE.md sez. 5/8/9 e la memoria (fatto in #852). Il diff non contiene slicing della history né simulazione di tool. Non tocca i provider, il cap delle 10 iterazioni né `_get_window`.

**Verifiche eseguite**
- Test: 137 passed (tests/test_unit_sottofondo.py, su una copia dell'indice).
- Prova reale da capo a fondo ripetuta, con processo figlio, gruppo proprio e turno appeso: il processo si ferma in 3,5 s con rc −15, il compito va in «ko» con «oltre la durata massima, fermato», l'avviso parte.
- Mutanti: 2 uccisi su 3.
  - Il timer che ignora il flag: ucciso.
  - Il tetto del Timer tolto: ucciso.
  - Il thread principale che ignora `gia_chiuso`: **sopravvive**. Il test è sincrono e il timer ha già scritto «ko» prima che il turno finisca, quindi lo ferma la vecchia guardia R-697-2 (modules/sottofondo/__init__.py:943), non il nuovo ramo.

**Elementi del diff esaminati**
1. `modules/sottofondo/__init__.py:880`: lock più flag `chiusura` condivisi da `_scaduto` e dalla fine di `_esegui`. Rischio esaminato: due esiti o due avvisi, oppure `os._exit` durante l'avviso «Ho finito». Esito **ok**, R-852R7-2 chiusa. Il flag si prende sotto lock in `modules/sottofondo/__init__.py:885` e in `modules/sottofondo/__init__.py:931`, e il lock non resta tenuto durante l'I/O, quindi niente deadlock. Se il turno chiude per primo, il timer non ferma il processo (coperto da `tests/test_unit_sottofondo.py:1493`).
2. `modules/sottofondo/__init__.py:933`: ramo `gia_chiuso`, il thread principale cede al timer e fa `return 1`. Esito **riserva**, vedi R-853R7-2.
3. `modules/sottofondo/__init__.py:815`: attesa del Timer limitata a `TETTO_TIMER_S` (`modules/sottofondo/__init__.py:52`, 30 giorni). Rischio esaminato: OverflowError silenzioso. Esito **ok**, R-852R7-3 chiusa (`tests/test_unit_sottofondo.py:1515`). Però cambia il significato del tetto: vedi R-853R7-1.
4. `modules/sottofondo/__init__.py:821`: la docstring di `_termina_processo` ora dichiara tre cose: uscita −15, `os._exit` solo come riserva, `claude -p` e browser non fermati perché in un gruppo proprio (`brains/claude_cli.py:428`, `modules/web/browser.py:496`). Esito **ok**: R-852R7-1 e R-852R7-4 sono dichiarate. Il limite resta: un `claude -p` già partito porta a termine la richiesta in corso.

**Riserve, tutte BASSE (da tracciare in stato_progetto.md)**
- **R-853R7-1 BASSA: il tetto può scattare prima della durata configurata e dirlo in modo falso.** Con GAS_SOTTOFONDO_MAX_MIN oltre 43200 (più di 30 giorni) il timer scatta a 30 giorni e ferma il compito con «oltre la durata massima». È falso rispetto al valore configurato e diverso da `attivo()`, che usa la durata vera. Il default è 1 h (`modules/sottofondo/__init__.py:45`), quindi in pratica è irrilevante. Correzione: alla scadenza `_scaduto` ricalcola `_secondi_rimasti` e, se resta tempo, riarma il timer; in alternativa basta dichiararlo.
- **R-853R7-2 BASSA: l'avviso del timer può andare perso.** Nel ramo `gia_chiuso` (`modules/sottofondo/__init__.py:936`) il thread principale torna e gas.py:7355 fa `sys.exit`. Se in quel momento il timer, thread demone, sta ancora facendo `annulla`/`_avvisa`, Python lo congela all'uscita: l'avviso si perde e il «ko» può restare non scritto. Il compito poi si recupera dal controllo esterno o dalla ripresa, che chiude subito «ko» per tempo finito (`modules/sottofondo/__init__.py:871`). Correzione di una riga: nel ramo, `tetto.join(60)` prima del return (tanto il timer finisce con `os._exit`).
- **R-853R7-3 BASSA: la finestra della corsa non ha un test.** Manca un test del caso «flag preso dal timer, esito non ancora scritto», ed è il motivo per cui il mutante del punto 2 sopravvive. Si può aggiungere un test con un `_tetto.fn` che prende solo il flag, per esempio con un Event che sospende `annulla`.

**Rischi esclusi (non verificati)**
- Comportamento su macOS/launchd e VPS: provato solo su Linux nel container.
- Orfano `claude -p` con la CLI vera: CLI non disponibile in dev.
- Timeout di rete dell'avviso Telegram dentro `_scaduto`: non verificato.

**Memoria del revisore**
- Riga contatore #853-R7 più una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (ba75ec24).
- Il diff staged è intatto: 2 file, +198.

File rilevanti:
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/tests/test_unit_sottofondo.py

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_sottofondo.py`: 129 → 137 (8 test nuovi), tutti verdi in locale: `137 passed in 6.61s`.
- `tests/test_unit_kernel.py` non rieseguito: il diff non tocca gas.py né il kernel (solo `modules/sottofondo/` e i suoi test). Il revisore ha fatto una prova reale con processo, gruppo e figlio veri (rc −15, «ko», avviso).

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	skipped	R7 fetta 4: tetto di tempo duro del compito in sottofondo	verifica-bot	claude/r7-tetti-di-tempo	pull_request_target	45235412646	2s	2026-11-23T18:09:50Z
in_progress		feat(sottofondo): R7 fetta 4 — tetto di tempo duro: il processo in so…	CI	claude/r7-tetti-di-tempo	push	45235404850	1m16s	2026-11-23T18:09:48Z
in_progress		Merge pull request #399 from Gasss23/claude/r7-lavori-ricorrenti	CI	main	push	45234199070	7m57s	2026-11-23T18:03:07Z
```

Run di questo branch (`gh api .../actions/runs?branch=claude/r7-tetti-di-tempo`, output reale):

```
45235412646 a56e9df9 verifica-bot pull_request_target completed/skipped
45235404850 a56e9df9 CI push in_progress/null
```

Mappatura commit→run: a56e9df9 (testa del primo push): run CI e verifica-bot sopra con head a56e9df9 (verifica-bot skipped: PR ancora senza etichetta). 12ab9019: le run con quell'head, se presenti sopra; altrimenti nessuna run su questo SHA. 36f1c779 e ba75ec24 (memoria): nessuna run propria (pushati insieme a a56e9df9). Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-853R7-1 BASSA — con GAS_SOTTOFONDO_MAX_MIN oltre 30 giorni il timer scatta a 30 giorni e dice «oltre la durata massima» (default 1 h: irrilevante in pratica). Aperta.
- R-853R7-2 BASSA — nel ramo «già chiuso dal timer» il processo può uscire prima che l'avviso del timer parta (manca `tetto.join`); il compito si recupera dal controllo esterno. Aperta.
- R-853R7-3 BASSA — la finestra della corsa «flag preso dal timer, esito non ancora scritto» non ha un test. Aperta.
- R-852R7-1 BASSA (dichiarata nel codice) — `claude -p` e il browser, in un gruppo proprio, finiscono la richiesta in corso dopo l'arresto. R-852R7-4 COSMETICA dichiarata. R-852R7-2/3: CHIUSE.
- Riserve delle altre chat: in `reports/stato_progetto.md`.
