# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Fetta 3 voce: compiti lunghi in sottofondo (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 3 (numero e URL dalla risposta JSON di `create_pull_request`; `gh` nel cloud non è autenticato). Sì dell'operatore alla fetta (5 nov, confermato via M1 il 6 nov); con riserve il merge passa dal sì via M1 (CLAUDE.md §10).
2. Prova sul Mac dopo il merge: a voce un compito lungo («confronta tre offerte e fammi un riassunto»): Gas deve rispondere che ci lavora e poi avvisare su Telegram.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 3 — compiti lunghi in sottofondo**: `FATTA` — strumento `in_sottofondo` offerto solo a voce (scelto dal modello), processo separato `gas.py sottofondo <id>` col suo kernel, solo cervello forte (tetto incluso), avviso Telegram finale, un compito alla volta, coda privata `.gas_sottofondo/`. Review #695-M2 (MEDIA R-695-1 chiusa con le BASSE), #696-M2 APPROVATO CON RISERVE (R-696-1/2-M2 BASSE).
- **Lettura a voce dei compiti finiti alla prossima attivazione** (fetta 3.2 della proposta): `DEFERITA — prossima fetta`.
- **Passaggio automatico oltre N giri** (fetta 3.3): `DEFERITA — opzionale`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .github/workflows/ci.yml           |   7 +++++++
 .gitignore                         |   1 +
 gas.py                             |  61 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/gate/gate.py               |   3 +++
 modules/sottofondo/__init__.py     | 204 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          |  90 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_sottofondo.py      | 179 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 44dbe2d (merge della #344).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T105a (voce: in_sottofondo offerto, compito in coda, processo avviato finto, risposta finale — round-trip §7), T105b (testo: non offerto e negato), T105c (forte spento: negato), T105d (firmata dal bot: avviato; senza firma negato), T105e (avvio fallito: diniego e coda libera). Suite kernel `=== RIEPILOGO: 1094 PASS, 0 FAIL ===` (prima 1089). `tests/test_unit_sottofondo.py` (nuovo, nella CI): 20 passed. gate + voice_stt + claude_cli 989 passed. Mutante «controllo turno voce tolto» → T105b/c FAIL. Prova dal vero: `gas.py sottofondo inesistente` → exit 1 con warning.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit della sessione e quello di fine-task sono pushati insieme: run non ancora disponibile alla scrittura dell'handoff. Nuovo passo CI: «Run sottofondo suite».

## §7 RISERVE APERTE

- R-696-1-M2 BASSA: in un turno Telegram con finestra contaminata il modello può chiamare in_sottofondo (non offerto) e, con la firma dell'operatore, il compito parte; a finestra pulita è negato.
- R-696-2-M2 BASSA: un'eccezione nel processo separato registra il «ko» ma non manda l'avviso Telegram (solo gas_debug.log).
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero, due `accoda` contemporanei da voce e bot (senza lock).
