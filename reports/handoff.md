# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #234) — tre stati per un comando firmato (R7, R-c4b3-5)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #236 (https://github.com/Gasss23/Gas/pull/236; numero e URL dall'API GitHub, `gh` non usato): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #234**: `FATTA` — su richiesta dell'operatore, merge `35b55be` (prima unito main #235, review #427 APPROVATO).
- **C6**: `FATTA` (decisione) — l'operatore ha scelto (a) «lasciamo così».
- **R7 / R-c4b3-5 — tre stati per un comando firmato**: `FATTA` — review #428 APPROVATO CON RISERVE.
- **R-428-1/2/3/4**: `FATTA` — review #429 APPROVATO CON RISERVE.
- **R7 / R-c4b3-4 — due processi sulla stessa storia; test R-429-1, guardia R-429-2 (V-1/V-2 verifica esterna #236)**: `FATTA` — review #430 APPROVATO CON RISERVE (R-430-1 MEDIA).
- **R-430-1/2/4/5**: `FATTA` — review #431 APPROVATO CON RISERVE.
- **Merge di origin/main (#237, chat Mani) — V-1 verifica esterna #236 (PR non mergeabile)**: `FATTA` — review #432 APPROVATO; conflitti solo nei report e nella memoria del revisore.
- **V-1/V-2/V-3 bot #236 (prima verifica), R-431-1/2, R-430-3**: `FATTA` — review #433 APPROVATO CON RISERVE (R-433-1 MEDIA).
- **V-1 MEDIA bot #236 (esito della firma perso a metà turno), V-2/V-3 bot #236, R-433-1/2**: `FATTA` — review #434 APPROVATO CON RISERVE.
- **R-434-1 (MEDIA, = V-1 bot #236 3° giro), R-434-3**: `FATTA` — review #435 APPROVATO CON RISERVE: a metà turno l'unione con l'altro processo si rimanda alla fine del turno.
- **V-2/V-3/V-4 bot #236 3° giro, R-435-1**: `DEFERITA` — prossima fetta.
- **R7 / R-c4b3-3**: `DEFERITA` — prossime fette.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  14 +++++++++++++
 gas.py                             | 269 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 modules/telegram/bot.py            |   4 ++++
 reports/da_mergiare.md             |  50 ++++++++++++--------------------------------
 reports/diff_sessione.md           |  13 ++++++------
 reports/handoff.md                 | 411 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------
 reports/roadmap.md                 |   6 +++---
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  41 +++++++++++++++++-------------------
 tests/test_unit_kernel.py          | 295 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 913 insertions(+), 194 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
4a1ac96 docs(fine-task): report e handoff — R-434-1 chiusa (#435)
8e4584f fix(storia): a metà turno l'unione con un altro processo si rimanda alla fine del turno (R-434-1, V-1 bot #236); solo UnicodeDecodeError resta «partito» (R-434-3)
7aa3e60 chore(revisore): memoria review #435 — APPROVATO CON RISERVE
48561e5 docs(fine-task): report e handoff — riserve del bot #236 (#433/#434), R-434-1 aperta
6548903 fix(storia,firma): unione della storia per contenuto, esito della firma tenuto a metà turno, lock con tetto di tempo; output non UTF-8 resta «partito» (V-1/V-2/V-3 bot #236, R-433-1/2)
f1ad943 chore(revisore): memoria review #434 — APPROVATO CON RISERVE
5b650d3 fix(firma,storia): errori d'avvio mai «partiti», incerta dopo il reclamo, test con processo vero; copie di conflitto collegate, con microsecondi e potate (V-1/V-2/V-3 bot #236, R-431-1/2, R-430-3)
5b9bfc6 chore(revisore): memoria review #433 — APPROVATO CON RISERVE
2923705 docs(fine-task): merge di main (#237) nel ramo, review #432
21a146d Merge origin/main (#237, chat Mani) in feat/merge-automatico-z1xjx2
4fb9dcd docs(fine-task): report e handoff — storia condivisa tra processi (#430/#431)
ddc3422 fix(storia): l'impronta avanza solo se la scrittura riesce; salvataggio senza lock se il lock manca; lettura iniziale sotto lock (R-430-1/2/4/5)
63e6a2f chore(revisore): memoria review #431 — APPROVATO CON RISERVE
4ad247c fix(storia): due processi sulla stessa root non si cancellano la storia (R7, R-c4b3-4); test R-429-1, guardia R-429-2
9a32029 chore(revisore): memoria review #430 — APPROVATO CON RISERVE
33173bf docs(fine-task): report e handoff — tre stati per un comando firmato (#428/#429), C6 decisa
be72cb5 fix(firma): segno «partito» azzerato a ogni tool call, errore di avvio non incerto, il modello legge «esito INCERTO» (R-428-1/2/3/4)
40da5ce chore(revisore): memoria review #429 — APPROVATO CON RISERVE
c19defc fix(firma): comando firmato partito e interrotto → esito INCERTO, non «NON eseguito» (R7, R-c4b3-5)
b997a5c chore(revisore): memoria review #428 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #428 (chat Motore) — commit c19defc

## VERDETTO: APPROVATO CON RISERVE

Review #428 (chat Motore). Il diff staged riguarda R-c4b3-5: un run_command firmato che parte e va in timeout ora viene detto «partito, esito incerto». Ho letto prima, come richiesto: CLAUDE.md sezione 5, la voce R-c4b3-5 in reports/stato_progetto.md e la memoria (#134 e la lezione del 2026-10-03 sui tre stati).

**Prove fatte su una copia dello staged nello scratchpad (poi cancellata).**
- Suite del kernel: 973 PASS, 0 FAIL. T77u passa.
- Sonda diretta, con l'allowlist di test (in produzione `SHELL_ALLOWLIST` è vuota, quindi in produzione tutto questo resta latente).

**Elementi del diff esaminati**
- gas.py:3920 — mette il segno «partito» subito prima di `subprocess.run`, dopo vetting, dry-run, controllo os_strict e snapshot. Rischio: un diniego prima della partenza marcato come «partito». Esito: ok. Ogni `return` di diniego viene prima del segno. Nella sonda, un comando negato al vetting dopo un segno rimasto True lo riporta a False e dà «[KO]».
- gas.py:3869 — azzera il segno all'ingresso di execute_tool_call, accanto a `_esito_contenuto` (dichiarato anche in gas.py:953). Rischio: il segno sopravvive alla chiamata dopo. Esito: ok per ogni chiamata che passa da execute_tool_call (la seconda parte di T77u e la mia sonda lo confermano). Riserva per i rami che non ci passano: vedi R-428-1.
- gas.py:2069 — «[KO] esito incerto: partito ma interrotto» quando meta è None e il segno è True, controllato prima di `negativo`. Rischio: il prefisso «Errore eseguendo» nasconderebbe il caso. Esito: ok, l'ordine è quello giusto.
- gas.py:3106 e gas.py:3110 — in applica_firma: `incerta`, `res["stato"]`, la notizia «PARTITO… Esito INCERTO: verifica prima di ripetere» e la presa d'atto «partita, esito INCERTO». `eseguita` resta False. Rischio: qualcuno tratta «incerta» come successo. Esito: ok. Gli unici consumatori sono modules/telegram/bot.py:694 e modules/telegram/bot.py:751, che passano a componi_esito_firma. Il diario usa «approvata id=… | [KO] esito incerto…».
- modules/telegram/bot.py:667 — nuovo ramo «⚠️ Approvata e PARTITA, ma esito INCERTO». Rischio: ordine dei rami. Esito: ok. Viene dopo `eseguita` e prima del «NON eseguita», e non mostra l'output, che contiene l'argv bwrap.
- tests/test_unit_kernel.py:6874 — il `subprocess.run` finto scade solo per il comando, non per lo snapshot git. Esito: ok, il test esercita il percorso reale fino al punto del timeout.

**Altre uscite dopo la partenza (sonda)**
- TimeoutExpired: «incerto». Corretto.
- FileNotFoundError, in fallback senza bwrap e col binario assente: «incerto» anche se il processo non è mai partito (R-428-2).
- KeyboardInterrupt: non è una `Exception`, quindi esce sia da execute_tool_call sia da applica_firma e il segno resta True. Che si propaghi è un comportamento che c'era già. Il reclamo è già avvenuto, quindi l'azione non si riesegue.

**Conteggio della notte:** invariato. modules/notte/notte.py:262-271 conta da `ev["cancello"]`, che a sua volta dipende solo dal testo di `out`.

**Riserve**
- **R-428-1 MEDIA (provata).** Il segno resta True nei rami di run_turn che non chiamano execute_tool_call ma chiamano lo stesso `_esito_diario` (gas.py:4270): il DENY e il cancello. Sequenza della sonda: run_command in timeout, poi un run_command parcheggiato nello stesso turno o in uno successivo → il diario scrive «[KO] esito incerto: partito ma interrotto» (prima «[OK] (non eseguito)»). In più `_turno_tool_ko` sale di 1 e il turno risulta «parziale». Con un run_command negato dal DENY il diario dice «esito incerto» invece di «[KO]». Il segno resta finché un qualsiasi tool non passa da execute_tool_call.
  - Correzione suggerita: in run_turn, per ogni tool call e prima dei rami del cancello, azzerare `self._run_command_meta = None` e `self._run_command_avviato = False`. In alternativa, in `_esito_diario` considerare il segno solo se `s.startswith("Errore eseguendo")`.
  - La stessa correzione chiude un difetto gemello che c'era già: un `_run_command_meta` rimasto da un run_command riuscito fa scrivere «[OK] exit=…» per un run_command parcheggiato dopo.
  - Aggiungere un test: segno True, poi `_esito_diario` di un run_command parcheggiato o negato.
- **R-428-2 BASSA.** FileNotFoundError o PermissionError su `subprocess.run` in os_with_fallback danno «incerto» anche se il processo non è partito. È l'errore prudente (meglio di «non eseguita» su un'azione partita), ma la dicitura è falsa. Si può restringere distinguendo TimeoutExpired dalle altre eccezioni.
- **R-428-3 BASSA.** Nel loop normale, cioè senza firma, il modello legge solo «Errore eseguendo run_command: … timed out after 60 seconds». La dicitura «esito incerto, verifica prima di ripetere» va solo nel diario, non nella storia.
- **R-428-4 COSMETICA.** Il docstring di applica_firma promette `"stato"` nel risultato, ma i ritorni anticipati (rifiutata, firma non valida, hash, già reclamata, eccezione) non lo impostano. Oggi non rompe niente perché bot.py usa `.get`.

**Rischi esclusi (non verificati)**
- Comportamento su VPS reale con bwrap e un vero timeout di 60 s: ho simulato solo con TimeoutExpired finto, non ho atteso un processo reale.
- pytest tests/ completo (1711 / +85) non rieseguito: il diff tocca solo la suite del kernel e bot.py, che il kernel esercita tramite componi_esito_firma.
- Nota di contesto, non introdotta da questo diff: `str(TimeoutExpired)` mette in storia l'argv bwrap con tutte le `--setenv` (già sanificate dei segreti), quindi testo lungo con variabili d'ambiente non segrete.

**Memoria:** riga #428 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit 2acb83e). Lo staging del motore è intatto: gas.py, modules/telegram/bot.py e tests/test_unit_kernel.py restano staged.

### Review #429 (chat Motore) — commit be72cb5

## VERDETTO: APPROVATO CON RISERVE

Review #429 (chat Motore). Diff in staging: gas.py, tests/test_unit_kernel.py. Ho letto prima CLAUDE.md (sez. 5), la parte di stato_progetto.md che riguarda R-428 e la mia memoria. Tutte le prove le ho fatte su una copia del tree in staging nello scratchpad, poi cancellata. Copia: **kernel 975 PASS, 0 FAIL**, come il tuo risultato.

**Elementi del diff esaminati**
- `gas.py:4220` — azzera `_run_command_meta` e `_run_command_avviato` all'inizio di ogni tool call di run_turn, prima di gate_classify. Rischio: che l'azzeramento cancelli il meta prima che il diario della stessa chiamata lo legga. La lettura avviene dopo, a `gas.py:4284`, nella stessa iterazione, quindi non succede. Esito: ok. Mutazione (tolte le due righe): T77v FAIL. Sonda sul gemello col solo meta residuo e chiamata parcheggiata: con lo staging il diario dice «[OK] (non eseguito)», con la riga del meta tolta dice «[OK] exit=0 stdout=3 char…». Il gemello è chiuso.
- `gas.py:4033` — nuovo testo d'errore per un run_command partito e poi interrotto. Rischi: conteggi di notte e cancello, il diario, argv in storia. Il testo inizia con «Errore eseguendo» e non con «Operazione negata»: per `gas.py:2050` resta negativo, i rami di `gas.py:4260` e `gas.py:4269` non lo contano come diniego. `_esito_diario` restituisce comunque «[KO] esito incerto: partito ma interrotto» a `gas.py:2068`, perché quel controllo viene prima del controllo «negativo». Non contiene più str(e), quindi niente argv di bwrap. Esito: ok. Mutazione (`if False:`): T77w FAIL, e la storia torna a contenere l'argv di bwrap.
- `gas.py:3926` — FileNotFoundError/PermissionError: il segno torna a False e l'eccezione viene rilanciata. Rischio: un errore di avvio scambiato per «incerto». Sonda con FileNotFoundError: il modello legge «Errore eseguendo run_command: [Errno 2]…», il diario «[KO]», avviato False. Esito: ok, ma la mutazione sopravvive (vedi R-429-1).
- `gas.py:3038` — il dizionario res di applica_firma nasce con "stato": "non_partita". Rischio: un ritorno anticipato senza la chiave. Ok.
- `tests/test_unit_kernel.py:6896` (T77v) e `tests/test_unit_kernel.py:6912` (T77w) — sono test veri: uccidono le mutazioni di R-428-1 (sul segno avviato) e di R-428-3.

**Altri punti che leggono `_run_command_meta`**: fuori da gas.py nessuno (grep su tutto il repo esclusi i test). In gas.py ci sono solo `_esito_diario` e applica_firma, che ha già il suo azzeramento dopo il reclamo a `gas.py:3082`.

**Riserve**
- R-429-1 BASSA: due rami corretti ma senza test.
  - Il rilancio di R-428-2: tolto il `False`, la suite resta 975/0.
  - Il meta residuo su una chiamata parcheggiata: tolto il solo azzeramento del meta, nessun test fallisce, perché T77v passa dal DENY, che è già negativo da sé.
  - Basta un test per ciascuno (FileNotFoundError → diario «[KO]» senza «incerto»; meta residuo + parcheggio → «[OK] (non eseguito)»).
- R-429-2 COSMETICA: il ramo except di `gas.py:4033` guarda solo `_run_command_avviato` e non anche `meta is None`. Un'eccezione arrivata dopo che il meta è stato valorizzato farebbe leggere al modello «INCERTO» mentre il diario dice «[OK] exit=…». In pratica non si raggiunge: dopo il meta c'è solo la concatenazione dell'output.

**Rischio escluso**: non ho verificato il comportamento dentro bwrap reale né su VPS/macOS. Nella copia il sandbox OS mancava e i test giravano in os_with_fallback; inoltre il PermissionError di un exec negato dentro bwrap non si riproduce in dev. In produzione la allowlist è vuota, quindi tutti questi rami restano latenti.

Memoria aggiornata con la riga #429 (nessuna lezione nuova) e committata da sola: 0f458fa, sopra 52b8e00, nessuno dei due pushato. Lo staging di gas.py e tests/test_unit_kernel.py è intatto. File: /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #430 (chat Motore) — commit 4ad247c

## VERDETTO: APPROVATO CON RISERVE

Review #430 (chat Motore) del diff staged su gas.py e tests/test_unit_kernel.py. Ho letto CLAUDE.md (sezioni 5, 8 e 9), la parte di stato_progetto.md su R-c4b3-4 e R-429 e la mia memoria. Le prove le ho fatte su una copia nello scratchpad, poi cancellata. Lo staging non l'ho toccato.

**Risultati delle prove**
- Suite del kernel sulla copia: 978 PASS e 1 FAIL. Il FAIL è T79a ed è un problema della copia, non del codice: la copia ha un git appena inizializzato e senza file tracciati, quindi T79a trova «0 file».
- Mutazioni:
  - senza `_unisci_storia_altrui`: T97a e T97b falliscono;
  - senza il reset di `_run_command_avviato` per FileNotFoundError: T77x fallisce;
  - senza l'azzeramento del meta in `run_turn`: T77y fallisce (diario «[OK] exit=0…»);
  - senza `and self._run_command_meta is None`: sopravvive, perché nessun test copre quel ramo.

**Elementi del diff esaminati**
- `gas.py:1154`: `_save_history` prende un flock esclusivo su `.gas_history.json.lock`, unisce, scrive e aggiorna `_storia_sync`. Rischio deadlock: il lock si prende solo qui, nessuna chiamata ricorsiva, e l'unione e la scrittura fanno solo I/O su file. Due kernel nello stesso processo usano descrittori diversi, quindi si mettono in fila senza bloccarsi a vicenda. Esito: ok. Il lock è bloccante e senza timeout: lo accetto. Il file `.lock` e le copie di conflitto sono coperti da `.gitignore` (`.gas_history.json.*`). Lo snapshot fa `git add -f` solo di `.gas_history.json`. I prefissi di `_SAFE_PATH_DENY_PREFIXES` (`.gas_history`) impediscono al modello di leggere le copie di conflitto. Esito: ok.
- `gas.py:1162`: `_storia_sync` viene aggiornato dopo `_salva_storia_su_file()`, che però inghiotte i propri errori. Esito: **riserva R-430-1 (MEDIA)**. Sonda: A aggiunge A1/rA1 e la scrittura fallisce in silenzio; B scrive; A aggiunge A2 e salva. Risultato nel file E nella memoria di A: `['u0','a0','B1','rB1','A2','rA2']`, cioè A1 e rA1 persi del tutto. Prima della modifica A li avrebbe riscritti. Correzione: `_salva_storia_su_file` restituisce un bool e `_storia_sync` avanza solo se la scrittura è riuscita.
- `gas.py:1138` / `gas.py:1140`: `nuovi = self.history[sync[3]:]` e poi `history = altrui + nuovi` solo se `nuovi` comincia con role user. Questo slicing calcola cosa salvare, non costruisce la finestra per i provider, quindi non è l'antipattern del Wall of Shame: `_get_window` resta l'unico costruttore della finestra. Ordine dei messaggi per Gemini, sonda 2: B salva dopo un blocco di tool (le chiamate `_save_history` di `run_turn` stanno sempre a fine blocco di tool o dopo la risposta finale, mai a metà sequenza), poi A accoda un turno. Ruoli: `user, assistant, user, assistant(tc), tool, user, assistant`. Le coppie tool_call/tool restano complete, nessun assistant(tool_calls) senza risposta, nessun doppio assistant. Il passaggio tool→user c'è già oggi quando si raggiunge il tetto di iterazioni. Esito: ok. Effetto dichiarato: quando B salva di nuovo a metà turno, il turno di A resta solo nella copia di conflitto (ping-pong tra copie). Lo accetto perché i dati sono conservati.
- `gas.py:1148`: `os.replace(self.db_path, copia)` sul ramo del conflitto. La compressione (`gas.py:1266`) e `clear_history` (`gas.py:1622`) assegnano una lista nuova, quindi l'id cambia e la versione dell'altro processo va nella copia di conflitto invece di essere cancellata. Esito: ok. `applica_firma` (`gas.py:3090`) estende e salva un blocco che comincia con user, quindi si unisce, ed è proprio il caso R-c4b3-4. Esito: ok.
- `gas.py:953`: `_storia_sync` è None con carica_storia=False. Il giro notturno (`modules/notte/notte.py:254`) cambia `db_path`, quindi il controllo `sync[0] != str(self.db_path)` evita di unire storie di compiti diversi. Esito: ok.
- `gas.py:4111`: il ramo «PARTITO… INCERTO» ora richiede `_run_command_meta is None`. È semanticamente corretto: con il meta valorizzato il comando è già terminato. Esito: ok, ma il ramo è senza test (R-430-5).
- `tests/test_unit_kernel.py:7418` (T97a) e `tests/test_unit_kernel.py:6938` / `tests/test_unit_kernel.py:6952` (T77x/T77y): uccidono le mutazioni dichiarate e non simulano output di tool verso il modello. Esito: ok.

**Riserve**
- **R-430-1 (MEDIA)**: `_storia_sync` avanza anche quando la scrittura fallisce in silenzio. Con una scrittura successiva di un altro processo, i nostri messaggi non scritti si perdono sia dal file sia dalla memoria. È riprodotto.
- **R-430-2 (BASSA)**: se l'apertura del file `.lock` o il flock falliscono (permessi, file system), salta TUTTO il salvataggio, con un warning. Prima la scrittura si tentava comunque. Meglio degradare a «scrivi senza lock».
- **R-430-3 (BASSA)**: le copie `.gas_history.json.conflitto.*` si accumulano senza rotazione né avviso all'operatore. Contengono la conversazione, quindi restano fuori dagli snapshot.
- **R-430-4 (BASSA)**: in `__init__` `_load_history` legge senza lock e `_sync_storia` fa stat dopo. Se un altro processo scrive in mezzo, l'impronta è quella nuova ma il contenuto quello vecchio, e i suoi messaggi verrebbero sovrascritti. La finestra di tempo è minima.
- **R-430-5 (COSMETICA)**: la condizione `meta is None` (`gas.py:4111`) non ha test, la mutazione sopravvive.

**Cosa NON ho verificato**
- Concorrenza reale tra due processi OS (bot su VPS + CLI): T97 e le mie sonde usano due kernel nello stesso processo, in sequenza. Il comportamento del flock sotto carico reale e su file system di rete non è riprodotto.
- Un vero 400 di Gemini sulla sequenza unita: ho controllato solo l'ordine dei ruoli, senza chiamate API.
- pytest su tutto `tests/`: non l'ho rilanciato, ho girato solo la suite del kernel.

Memoria: riga #430 e una lezione nuova (l'impronta avanza solo se la scrittura riesce), committate con scripts/commit_memoria_revisore.sh («chore(revisore): memoria review #430 — APPROVATO CON RISERVE»). Il file è /home/user/Gas/.claude/agents/memoria_revisore.md.

### Review #431 (chat Motore) — commit ddc3422

## VERDETTO: APPROVATO CON RISERVE

Review #431 (chat Motore). Riguarda il diff STAGED su gas.py e tests/test_unit_kernel.py, che chiude le riserve R-430-1, R-430-2, R-430-4 e R-430-5. Le prove le ho fatte su una copia nello scratchpad, poi cancellata. Nel repo vero ho toccato solo la mia memoria: commit 63e6a2f, non pushato. Lo staging è intatto (stessi 2 file, +90 e -15 righe).

**Cosa ho esaminato**
- `gas.py:1206` — `_save_history` aggiorna `_storia_sync` solo se `_salva_storia_su_file()` restituisce True (R-430-1). Rischio esaminato: l'impronta avanza anche se la scrittura fallisce. Mutazione «sync sempre»: T97c fallisce. **ok**
- `gas.py:1149` — dopo un'unione la base diventa il file dell'altro processo: `(ora, id della nuova lista, len(altrui))`. Mutazione senza questa riga: T97c fallisce, perché al salvataggio dopo il fallimento la differenza di id manda nel ramo conflitto e B2/rB2 finiscono solo nella copia. Sonda «unione, due scritture fallite, B salva, A salva»: nel file ci sono `u0,B1,B2,A1,A2`, nessuna perdita. **ok**
- `gas.py:1163` — `_blocca_storia`: se l'apertura del .lock o il flock falliscono, scrive un warning e si salva senza lock (R-430-2). Sonda con `.gas_history.json.lock` creato come cartella: warning «salvo senza lock» e storia scritta. **ok**
- `gas.py:1192` e `gas.py:955` — `_carica_storia_bloccata` legge la storia e ne prende l'impronta sotto il lock, poi in `__init__` si rifà `_storia_sync` con l'id della lista vera (R-430-4). Il `getattr(self, "history", [])` di `gas.py:1117` durante la lettura dà l'id di una lista provvisoria, ma viene subito sostituito alla riga 955: **corretto**. Mutazione senza il resync: T97a fallisce.
  - Lock lasciato aperto: dopo `__init__` il lock è libero (prova con LOCK_NB). Resta libero anche dopo la quarantena, perché il rename tocca la storia e non il .lock; in quel caso l'impronta è None e il salvataggio successivo scrive normalmente.
  - Se `_load_history` solleva un'eccezione, il `finally` rilascia comunque il lock.
  - Deadlock: nessuna chiamata annidata, quindi nessun deadlock nemmeno con due kernel nello stesso processo. **ok**
- `tests/test_unit_kernel.py:6941` — T77z: eccezione dopo che il meta è valorizzato, il testo non contiene «INCERTO». Mutazione senza `meta is None` (`gas.py:4154`): T77z fallisce (R-430-5). **ok**
- `gas.py:1153` (contesto, ramo conflitto) — l'ordine dei passi è os.replace della versione altrui, poi la nostra scrittura. Sonda «conflitto + scrittura fallita»: il file principale resta **assente** finché non si salva di nuovo, e la versione altrui sta solo nella copia. Al giro dopo B riscrive tutto e A fa di nuovo conflitto: è il ping-pong già dichiarato, senza perdita nella sonda. **riserva** (R-431-2)

**Esecuzione sulla copia**: kernel 981 PASS, 0 FAIL. Le quattro mutazioni falliscono come atteso: T97c, T97c, T77z, T97a.

**Riserve**
- **R-431-1 BASSA**: il nome della copia di conflitto ha la risoluzione al secondo più il pid. Due conflitti nello stesso secondo dallo stesso processo producono lo stesso nome e `os.replace` sovrascrive la prima copia. L'ho riprodotto: nella sonda non si è perso nulla perché la seconda copia conteneva già la prima, ma con 3 processi si possono perdere dati. Proposta: usare `%f` (microsecondi) o un contatore. È vicina a R-430-3.
- **R-431-2 BASSA**: nel ramo conflitto la copia viene spostata prima della scrittura. Se poi la scrittura fallisce, il file principale manca: un processo che parte in quel momento riparte da una storia vuota, mentre la storia altrui resta solo nella copia. Proposta: copiare o fare un hardlink invece di spostare, così il file resta finché la scrittura atomica non lo sostituisce.
- **R-431-3 COSMETICA**: `gas.py:955` indicizza `self._storia_sync`, che è Optional. A runtime funziona perché il `finally` lo valorizza sempre, ma mypy lo segnalerebbe.
- R-430-3 (copie di conflitto senza rotazione) resta aperta e dichiarata.

**Cosa non ho verificato**
- Il comportamento del flock su file system di rete o su macOS (APFS): non riproducibile qui. Lì un lock tenuto a lungo da un altro processo blocca anche l'avvio di Gas, oltre al salvataggio come succedeva già prima.
- Non ho rieseguito `pytest tests/` (1796 passed): mi fido del dato dell'agente principale, ho rieseguito solo la suite del kernel.

**Memoria**: aggiunta la riga #431 e una lezione nuova (rami che spostano il file condiviso prima di riscriverlo, collisione del nome della copia). Committata con scripts/commit_memoria_revisore.sh in 63e6a2f.

File: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #432 (chat Motore) — merge 21a146d

## VERDETTO: APPROVATO

Review #432 (chat Motore): merge in corso, solo staged, di origin/main 9030b2f (PR #237, fetta 2 della chat Mani) dentro feat/merge-automatico-z1xjx2. La merge-base è 35b55be. Prima della review ho letto CLAUDE.md (dato nel contesto), la sezione Mani/Motore di reports/stato_progetto.md (dal diff) e la coda di .claude/agents/memoria_revisore.md.

Elementi esaminati:
- `.claude/agents/memoria_revisore.md:681` — righe Mani #409/#410/#428 (chat Mani) messe in coda dopo la #431 Motore. Rischio esaminato: righe perse, duplicate o marcatori di conflitto. Ho confrontato riga per riga l'index con HEAD (680 righe) e con MERGE_HEAD (676): l'index ha 683 righe, cioè HEAD più le 3 righe Mani. Nessuna riga di HEAD o di main manca, nessuna riga non vuota è duplicata, non ci sono righe inventate né marcatori. Esito: ok.
- `modules/web/leggi.py:26` — import del modulo web, solo stdlib (righe 26-42). Rischio esaminato: uno scontro con il ramo Motore. `git diff 35b55be HEAD -- modules/web tests/test_unit_web_leggi.py` è vuoto, quindi il ramo non tocca quei file. Lo staged contro MERGE_HEAD non li elenca: sono identici a 9030b2f. Esito: ok.
- `gas.py:1163` — `_blocca_storia`, il lock della storia condivisa tra processi (#430/#431). Rischio esaminato: il merge altera il codice del ramo, oppure gas.py importa modules.web. Il grep non trova `modules.web` né `leggi_pagina` in gas.py, modules/telegram/ e brains/: l'aggancio non esiste ancora e quindi non può scontrarsi con nulla. Esito: ok.
- `gas.py:1206` — l'impronta di sincronizzazione avanza solo se `_salva_storia_su_file()` riesce (R-430-1). Rischio esaminato: una perdita durante l'unione. Il codice è intatto e lo staged contro HEAD non tocca gas.py. Esito: ok.
- `modules/telegram/bot.py:668` — ramo «esito INCERTO» (#428). Il merge non lo tocca e il file non ha import da modules/web. Esito: ok.
- `tests/test_unit_kernel.py:7448` — T97c è presente. Con `pytest --co tests` la raccolta dà 1807 test senza errori né collisioni di nomi. La web suite dà 96 passed. Esito: ok.
- `reports/stato_progetto.md:4` — l'unione automatica è sensata: la riga 4 prende la voce Mani «fetta 2, PR #237» e tiene intera la catena precedente. Il blocco Motore «Modo di lavorare», che c'era solo in HEAD, è conservato. Il blocco «Mani — fetta 2» sta sopra «fetta 1». `git ls-files -u` è vuoto: nessun percorso resta in conflitto. Esito: ok. Nota non bloccante: il blocco fetta 1 elenca ancora come aperte R-ve235-4/5/6/7 e R-393-1/2, che il blocco fetta 2 dichiara chiuse. Il disallineamento viene da main (testo Mani), non dalla risoluzione del merge.

Rischi esplicitamente esclusi:
- Non ho rieseguito la suite kernel (981/0) né i gate e la notte (1043). Mi fido dei numeri dell'agente, perché non posso fare checkout o copie del tree durante il merge senza rischiare l'index. Ho eseguito solo la web suite e la raccolta pytest.
- Non ho verificato il comportamento su VPS né la CI remota: non sono riproducibili qui.
- Non ho controllato i report di sessione (handoff.md, ultimo_report.md, diff_sessione.md). L'agente li ha tenuti quelli del ramo per scelta dichiarata e la loro coerenza spetta al gate A.

Memoria: ho aggiunto la riga contatore #432 (chat Motore) in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. È modificata ma non staged, e non è committata: `scripts/commit_memoria_revisore.sh` non funziona durante un merge, quindi devi aggiungerla tu con `git add` e includerla nel commit di merge. Nessuna lezione nuova.

### Review #433 (chat Motore) — commit 5b650d3

## VERDETTO: APPROVATO CON RISERVE

Review #433 (chat Motore). Diff staged: gas.py e tests/test_unit_kernel.py. Le prove le ho fatte su una copia con la patch applicata in /tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/rep. Il kernel dà 986 PASS e 0 FAIL. In questo container bwrap e i namespace ci sono, quindi T77ab è girato in os_strict dentro bwrap.

Elementi del diff esaminati:
- gas.py:4078 — `except (OSError, ValueError)` riporta `_run_command_avviato` a False. Rischio esaminato: le sottoclassi che nascono DOPO l'avvio del processo. Esito: **riserva (R-433-1, MEDIA)**. `UnicodeDecodeError` è una sottoclasse di ValueError e, con `text=True`, nasce in communicate quando il comando ha già finito di girare. L'ho riprodotto con `cat bad.bin` (byte 0xff, allowlist del recinto):
  - a HEAD: «il comando è PARTITO ma si è interrotto (UnicodeDecodeError): esito INCERTO», con avviato True;
  - col diff: «Errore eseguendo run_command: 'utf-8' codec can't decode…», con avviato False.

  Quindi un comando che ha girato davvero viene dato per non partito, e in applica_firma diventa «non_partita» invece di «incerta». È una regressione proprio sulla proprietà che V-1 voleva rendere fedele. Oggi l'impatto pratico è basso: `SHELL_ALLOWLIST` di produzione è vuota e i comandi ammessi sono di sola lettura. Correzione: prima del ramo generico rilanciare `UnicodeError` lasciando il segno a True, oppure fare `except ValueError as e: if isinstance(e, UnicodeError): raise`. Serve anche un test con output non UTF-8.
- gas.py:4070 — l'ambiente del figlio si calcola prima del segno «partito», e `TimeoutExpired` viene rilanciato lasciando il segno. Rischio esaminato: un ambiente rotto che lascia il segno a True. Esito: ok. Il segno viene azzerato all'inizio di execute_tool_call (gas.py:4019) e T77aa lo prova.
- gas.py:3185 e gas.py:3226 — `reclamata` è inizializzata prima di ogni return e passa a True solo dopo che `reclama_esecuzione` è andato a buon fine. In gas.py:3282 l'except generico mette `eseguita=False, stato="incerta"`. Esito: ok.
- gas.py:1162 — `os.link`, e `shutil.copy2` come ripiego, al posto di `os.replace`. Rischio esaminato: che la copia segua il file nuovo. Esito: ok. `_salva_storia_su_file` (gas.py:1237) scrive un file temporaneo e poi fa `os.replace`: il nome principale passa a un inode nuovo e la copia di conflitto tiene il vecchio. Se la nostra scrittura fallisce, il file principale resta intatto (T97d). Su un file system senza hardlink `copy2` conserva anche l'mtime, quindi la potatura resta coerente.
- gas.py:1173 — `_pota_copie_conflitto` ordina per `st_mtime_ns`. Esito: **riserva (R-433-2, BASSA)**. Con mtime uguali decide l'ordine del glob. In una sonda con 4 copie a mtime 0 e MAX=2 la copia «zzz», creata per ultima, è stata cancellata. In pratica le copie ereditano l'mtime della scrittura dell'altro processo, quindi crescono sempre, ma non c'è uno spareggio sul nome. Inoltre se un'altra potatura cancella un file mentre gira il sort, `p.stat()` fallisce e finisce nel warning «Copia di conflitto non riuscita», che è fuorviante: la copia esiste già. Non si blocca niente.
- tests/test_unit_kernel.py:6976 — T77ab lancia un `tail -f` vero con tetto di 0,5 s. Rischio esaminato: instabilità e processi orfani in CI. Esito: ok. Con bwrap il prefisso ha `--die-with-parent` (gas.py:1933) e `subprocess.run` su POSIX dopo il kill fa solo `wait()`, senza svuotare le pipe. Dopo la suite non c'era nessun `tail -f` vivo.

Mutazioni sulla copia, tutte e quattro mordono (982 PASS, 4 FAIL):

| Mutazione | Test che fallisce |
|---|---|
| `os.link` riportato a `os.replace` | T97d |
| potatura tolta | T97e |
| ripristinato il vecchio `except (FileNotFoundError, PermissionError)` | T77aa |
| `reclamata` mai a True | T77ac |

Rischio escluso: non ho provato il ramo `shutil.copy2` su un file system vero senza hardlink (FAT o certe condivisioni di rete: non riproducibile qui), né T77ab sul runner GitHub reale (provato solo in questo container, con bwrap funzionante). Non ho rieseguito `pytest tests/` intero: mi fido del dato dichiarato di 1807 passed.

Wall of Shame: nessuno slicing della cronologia e nessuna simulazione dell'output dei tool. Il cap di 10 iterazioni e `_get_window` non sono toccati.

Riserve da tracciare in stato_progetto.md:
- **R-433-1 MEDIA**: UnicodeDecodeError marcato come «non partito». Consiglio di chiuderla in questa fetta prima del commit, con un nuovo giro di review.
- **R-433-2 BASSA**: potatura con mtime uguali e stat concorrente.

Memoria: ho aggiunto la riga #433 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (5b9bfc6). Lo staging del diff è rimasto intatto (2 file).

### Review #434 (chat Motore) — commit 6548903

## VERDETTO: APPROVATO CON RISERVE

Review #434 (chat Motore) del diff staged: `gas.py` e `tests/test_unit_kernel.py`. Prima della review ho letto le tre fonti obbligatorie: CLAUDE.md (sez. 5), reports/stato_progetto.md e la mia memoria.

Le prove le ho fatte su una copia dell'albero staged nello scratchpad. La suite del kernel dà **990 PASS, 0 FAIL**. Nel repo reale ho toccato solo la memoria (commit f1ad943). Lo staging è intatto.

**Elementi del diff esaminati**
- `gas.py:1115` — `_hash_messaggi`: sha256 del JSON ordinato. Rischio esaminato: il costo a ogni salvataggio. Ho misurato 12 ms per 2,4 MB (300 messaggi da 8 KB). La compressione tiene la storia sotto `HISTORY_MAX_MSGS = 100`, e l'hash viene calcolato una volta per salvataggio, più due solo quando il file è cambiato. Esito: ok.
- `gas.py:1159` — la base si riconosce dal contenuto (n, hash) e non più dall'id della lista. Questo chiude V-2 (riuso dell'id). Caso `n_base > len(altrui)`, sondato: tutte e due le condizioni sono False, finisce nella copia «conflitto» e non si perde nessun messaggio. Esito: ok.
- `gas.py:1170` — ramo «nostra + suoi». **Riserva MEDIA (R-434-1).** Il ramo scatta anche al salvataggio a metà turno di `gas.py:4503`, dalla seconda iterazione di tool in poi. La sonda è `p1.py`: il bot scrive mentre il secondo tool della CLI è in esecuzione. Effetto: il blocco della firma entra nella storia IN MEMORIA prima della prossima chiamata al modello. Quello che il modello riceve da `_get_window()`:
  - `user, assistant(tc), tool, assistant(tc), tool, user[NOTIFICA], assistant(tc), tool, assistant «Preso atto»`
  - la finestra finisce con un assistant;
  - poi la risposta finale si accoda dopo: due assistant di fila nel file;
  - il turno della CLI viene «dirottato»: l'ultimo user che il modello vede è la notifica, non la domanda dell'operatore.

  Non crasha (§9 fa scattare il fallback), ma con Gemini il rischio è un 400 o una risposta sul tema sbagliato. T97f copre solo il caso in cui il bot scrive DOPO l'ultimo salvataggio dei tool. Correzione proposta: a metà turno (nostra lista che non chiude il turno), se si applica solo il ramo 2, NON unire né scrivere. La base resta quella vecchia e l'unione avviene al salvataggio finale, che è il caso già provato da T97f.
- `gas.py:1176` — R-430-1, la base resta `(n_base, h_base)` dopo il ramo 2. **Riserva BASSA (R-434-2).** Se la scrittura fallisce, i messaggi dell'altro sono già nella nostra lista, ma la base non li comprende. Se poi l'altro processo riscrive, `altrui[n_base:]` li riaccoda di nuovo e restano duplicati. Servono una scrittura fallita e una scrittura concorrente: caso raro.
- `gas.py:1203` — potatura con chiave `(mtime_ns, nome)` e `OSError` → `(0, nome)`. Questo chiude R-433-2. Esito: ok.
- `gas.py:1231` — lock con `LOCK_NB` e tentativi ogni 0,05 s per 5 s, poi `TimeoutError`, che il `except Exception` già presente trasforma in warning con salvataggio senza lock. Nessuna attesa infinita. Il tempo usa `_time.monotonic`, già importato. Effetto collaterale accettabile: all'avvio, con il lock occupato, `__init__` può attendere fino a 5 s. Esito: ok.
- `gas.py:4118` — `except (TimeoutExpired, UnicodeError)` rilancia con il segno «partito» a True. Questo chiude R-433-1 (T77ad PASS nella copia). **Riserva BASSA (R-434-3).** `UnicodeError` comprende anche `UnicodeEncodeError` all'avvio: l'ho sondato con `subprocess.run(['echo','\ud800'])` e un surrogato isolato arriva da un JSON valido. Il risultato è «PARTITO, INCERTO» per un comando mai partito. Il verso è prudente, ma per precisione andrebbe ristretto a `UnicodeDecodeError`.
- `tests/test_unit_kernel.py:7535` — T97f. Rischio esaminato: è davvero la prova di «a metà turno»? Copre solo una tempistica, cioè la scrittura del bot fra il salvataggio dei tool e quello finale. Manca il caso di R-434-1. Esito: riserva, legata a R-434-1.
- `tests/test_unit_kernel.py:7494` — T97b2, la sequenza A/B. Il ramo 2 riordina il file (seguito di B, poi ancora A), quindi il prefisso di A non coincide più con la sua base. Al successivo salvataggio di A a metà turno si va nella copia «conflitto», e «seguito di B» resta solo nella copia. Nessun messaggio si perde, e il test lo verifica sull'unione di storia e copie. È lo stesso effetto residuo di V-1, ma in un caso più stretto. Esito: ok, come limite dichiarato da registrare.

**Wall of Shame**
- `history[:n_base]` e `[n_base:]` lavorano sulla storia intera, per l'unione: non sono una finestra mandata al provider, quindi non sono slicing vietato. La finestra resta `_get_window()` (`gas.py:4356`).
- Nessuna simulazione di output dei tool.
- Il cap di 10 iterazioni non è toccato.

**Rischi esclusi (non verificati)**
- Il comportamento reale di Gemini, Groq e OpenRouter con una finestra che finisce con un assistant e con due assistant di fila: senza rete non è riproducibile.
- Le mutazioni dichiarate (senza ramo 2, senza UnicodeError, base = altrui+nuovi, lock bloccante): non le ho rieseguite, mi fido del report. La suite completa è verde.
- `pytest tests/` (1807): non rieseguito.

**Memoria**
- Riga #434 e una lezione nuova (provare l'unione a ogni punto di salvataggio del loop e guardare la finestra, non solo il file) committate con `scripts/commit_memoria_revisore.sh`: commit f1ad943.
- Le riserve R-434-1 (MEDIA), R-434-2 e R-434-3 (BASSE) vanno tracciate in reports/stato_progetto.md.

File:
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- Sonda: /tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/prove/p1.py
- Log della suite: /tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/k.log

### Review #435 (chat Motore) — commit 8e4584f

## VERDETTO: APPROVATO CON RISERVE

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (voce R-c4b3-4, riga 409) e .claude/agents/memoria_revisore.md (le ultime #432–#434 con le lezioni collegate).

**Elementi del diff esaminati**
- `gas.py:1133` — `_turno_chiuso()` dice che il turno è chiuso se l'ultimo messaggio è un assistant senza tool_calls, oppure se la storia è vuota. Rischio esaminato: il turno può chiudersi anche in altri modi, per esempio col blocco di `_storia_esito_firma`, che finisce con l'assistant «Preso atto». Esito: ok, quel blocco chiude il turno e l'unione avviene.
- `gas.py:1177` — nel ramo «nostra + suoi», se il turno non è chiuso, la funzione restituisce False senza toccare `self.history` né `_storia_sync`. Rischio esaminato: che il modello veda la notifica dell'altro processo a metà turno (R-434-1). Esito: ok. Ho tolto il controllo in una copia della sorgente e T97h fallisce: la notifica finisce prima di «risposta finale h». Il primo ramo (i nostri messaggi nuovi cominciano con user, quindi i suoi vanno prima del nostro turno) non cambia e non spezza la sequenza.
- `gas.py:1284` — `_save_history` esce senza scrivere quando l'unione è rimandata. Il lock si rilascia comunque nel finally. Rischio esaminato: crash-safety, con il turno a metà che non va su disco. Esito: riserva, vedi R-435-1.
- `gas.py:4134` — l'except che lascia il segno «partito» ora è `(subprocess.TimeoutExpired, UnicodeDecodeError)`. Un UnicodeEncodeError all'avvio cade in `except (OSError, ValueError)` (riga 4137), che lo marca «mai partito». Rischio esaminato: le sottoclassi di ValueError che nascono dopo l'avvio del comando. Esito: ok, R-434-3 chiusa.
- `tests/test_unit_kernel.py:7548` — T97h: il bot scrive mentre la CLI è al secondo giro di tool. Il test controlla che la notifica sia assente dalla storia in memoria e presente nel file, e che dopo il salvataggio finale stia dopo la risposta. Esito: ok, il test dimostra il caso che R-434-1 chiedeva.
- Contesto `gas.py:1396` (compressione) e `gas.py:3217` (`_storia_esito_firma`), gli altri chiamanti di `_save_history`. Una compressione a metà turno con conflitto pendente non viene scritta, la base resta quella vecchia e al salvataggio finale si passa dal ramo 2 (storia compressa). Esito: ok.

**Prove su una copia del codice staged nello scratchpad**: kernel 991 PASS, 0 FAIL. Mutazione senza `_turno_chiuso`: 990 PASS, 1 FAIL (T97h).

**Riserve**
- **R-435-1 BASSA**: un turno può finire senza risposta finale (10 iterazioni, pipeline esausta, eccezione del provider) mentre c'è un conflitto pendente. In quel caso non c'è un salvataggio che chiude il turno. Se il processo esce, i messaggi del turno (user e tool) non arrivano mai su disco. Sonda `/tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/r435/sonda_435.py`: il tool del secondo giro manca dal file e anche da un nuovo processo. Se invece lo stesso processo fa un altro turno che si chiude, l'unione avviene e non si perde niente. Il diario registra comunque i tool. Rimedio suggerito: un salvataggio «forzato» nel finally di `run_turn`. A turno finito, unire i messaggi dell'altro dopo un tool non sporca più la finestra (tool → user è una sequenza valida). Da tracciare in stato_progetto.md.
- **R-435-2 COSMETICA**: `compress-history` forzato (contesto `gas.py:5209`), con conflitto pendente e storia che finisce con un tool, non scrive niente ma riporta ok.
- R-434-2 BASSA resta aperta, come dichiarato.

**Rischi esclusi**
- Non ho provato la concorrenza reale tra due processi vivi (CLI e bot Telegram) su VPS: ho simulato con due kernel nello stesso processo, come fa T97h.
- Non ho rieseguito pytest tests/ completo (1807): ho rieseguito solo la suite kernel.

Riga contatore #435 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committate con 7aa3e60 tramite scripts/commit_memoria_revisore.sh. Lo staging di gas.py e tests/test_unit_kernel.py è rimasto com'era.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 971 → 991 PASS, 0 FAIL in locale (T77u-z, T77aa-ad, T97a-h; in CI con bwrap 2 in più). Blocco reale: `=== RIEPILOGO: 991 PASS, 0 FAIL ===`.
pytest `tests/`: 1807 passed (compresi i test web arrivati con main).

## §6 STATO CI

- 521b018 (testa della PR #234, mergiata): unit-suite, handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE).
- be72cb5: handoff-check failure (commit intermedio pushato prima del dossier, atteso); superato da 33173bf.
- 33173bf (con b997a5c, c19defc, 40da5ce): unit-suite, handoff-check success; verifica-bot success (APPROVATO CON RISERVE, V-1/V-2/V-3 BASSE: decide l'operatore).
- 4fb9dcd (con 9a32029, 4ad247c, 63e6a2f, ddc3422): handoff-check success; unit-suite e verifica-bot non lette (superate dal merge di main).
- 2923705 (con 21a146d): unit-suite, handoff-check success; verifica-bot FAILURE (V-1 MEDIA: esito della firma a metà turno), corretta in 6548903.
- 48561e5 (con 5b9bfc6, 5b650d3, f1ad943, 6548903): unit-suite success (kernel 992 PASS in CI), handoff-check success; verifica-bot FAILURE (V-1 MEDIA = R-434-1), corretta in 8e4584f.
- 7aa3e60, 8e4584f: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-428-1/2/3/4: chiuse in #429.
- R-429-1/2: chiuse in #430 (T77x, T77y, guardia sul meta).
- R-430-1/2/4/5: chiuse in #431.
- R-430-3, R-431-1/2: chiuse in #433; R-433-1/2: chiuse in #434.
- R-431-3 (COSMETICA): indice su un Optional in `__init__`.
- V-1/V-2/V-3 bot #236 (entrambi i giri): chiuse in #433/#434.
- R-434-1, R-434-3: chiuse in #435.
- R-435-1 (BASSA): turno finito senza risposta finale con conflitto pendente → i suoi messaggi non vanno su disco se il processo esce.
- R-435-2 (COSMETICA): compress-history con conflitto pendente non scrive ma dice ok.
- V-2/V-3/V-4 bot #236 3° giro (BASSE/COSMETICA): Popen+communicate per il segno «partito», messaggio Telegram dell'errore interno, descrizione della PR.
- R-434-2 (BASSA): dopo il ramo «nostra + suoi» una scrittura fallita più una concorrente possono duplicare messaggi.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
