# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Revisione in più sugli script del CRM e note dei verificatori (PR #404)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #404 (https://github.com/Gasss23/Gas/pull/404): tocca `.claude/perimetro_review.txt` e `scripts/`, quindi il bot dà `neutral` e il merge lo decide l'operatore.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; controllare che l'ultima riga dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

---

## §1 SCOPE & ESITO FETTE

- **`scripts/crm/` nel perimetro di review** (richiesta dell'operatore: «ci sta comunque una revisione in più, dato che comunque sono dati personali dei clienti e non dobbiamo fare assolutamente neanche un errore»; decisione 20): FATTA (d54a09ad, review #853 APPROVATO CON RISERVE). R-852M-2 chiusa. Note V-1/V-2 del bot sulla #403 chiuse nello stesso commit.
- **R-853-1 e R-853-2 (parte delle copie)**: FATTE (75dbd9d9, review #854 APPROVATO CON RISERVE). `togli_servizio` a ogni STOP dell'installer; copie locali per giorno (30 giorni più le ultime 10).
- **Merge di main (PR #401 del funnel, altra chat)** (1b61ec43): FATTO. Conflitti solo sui report e sulla memoria del revisore: report del ramo tenuti, righe della memoria unite, riserve dell'ultimo verdetto del bot sulla #401 (V-1 BASSA, V-2 COSMETICA) riportate in `reports/stato_progetto.md` (regola 3). Nessun file del perimetro nel merge: niente review.
- **Bacheca** (dfe8fbee): notizia per le altre chat (`scripts/crm/` nel perimetro); chiusa la notizia del 23-11 sul collegamento di Gas al CRM.
- **Note dei verificatori sulla #404**: FATTE.
  - Verifica esterna su ca2fc64b (APPROVATO CON RISERVE, commento https://github.com/Gasss23/Gas/pull/404#issuecomment-7139788043): V-1 BASSA (orologio indietro: la copia appena fatta veniva cancellata) chiusa in 5b75c850; V-2 BASSA (ramo indietro rispetto a main) chiusa dal merge 1b61ec43; V-3 BASSA (= R-854-1/R-853-3) chiusa in 5b75c850/8fbd65a3; V-4 COSMETICA (§6 senza verde finale) superata, vedi §6.
  - Bot su dfe8fbee (APPROVATO CON RISERVE, neutral): V-1 BASSA (copie a mano fuori formato) chiusa in 5b75c850; V-2 BASSA (unit-suite non ancora finita) superata: unit-suite success su dfe8fbee.
  - R-854-1 (Ctrl+C durante l'attesa) e R-853-3 (test degli script) chiuse in 5b75c850 (review #855, #856) e 8fbd65a3 (review #857).
- **R-854-2** (KeepAlive senza tetto, registro senza rotazione): NON FATTA, resta aperta.
- **Prova su un Mac vero**: SALTATA — il Mac non è raggiungibile da qui; script provati con comandi finti (test del repo e simulazioni del revisore), bash 5.2.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  13 ++
 .claude/perimetro_review.txt       |   3 +
 modules/crm/store.py               |  30 +++-
 reports/bacheca.md                 |   4 +-
 reports/crm/decisioni.md           |   4 +
 reports/crm/guida.md               |   4 +-
 reports/diff_sessione.md           |  27 ++--
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           |  55 ++++---
 scripts/crm/installa.sh            |  30 +++-
 tests/test_unit_crm.py             | 309 ++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale. Base: merge-base con main 7231d92d (main 96d5ae99 a inizio sessione, poi il merge della #401).

## §3 GIT LOG --ONELINE (sessione)

```
d54a09ad chore(perimetro): scripts/crm/ passa dal revisore (decisione 20); installer: plist tolto se la dashboard non parte, errore di import distinto (review #853)
75dbd9d9 fix(crm): copie locali per giorno (30 giorni più le ultime 10) e servizio tolto a ogni STOP dell'installer (R-853-1/2, review #854)
ca2fc64b docs(fine-task): scripts/crm/ nel perimetro di review e copie locali per giorno — report, handoff (review #853, #854) e stato
1b61ec43 Merge origin/main (PR #401 funnel) nel ramo della PR #404 — report del ramo tenuti, riserve dell'ultimo verdetto del bot sulla #401 in stato_progetto (regola 3)
a83ca616 docs(fine-task): handoff e diff_sessione col merge di main (PR #401) — PR #404
dfe8fbee docs(bacheca): scripts/crm/ nel perimetro di review (decisione 20); chiusa la notizia sul collegamento di Gas al CRM — PR #404
5b75c850 fix(crm): copia appena fatta mai cancellata, copie a mano ignorate, Ctrl+C durante l'installazione toglie il servizio, test degli script con comandi finti (V-1 verifica esterna #404, V-1 bot #404, R-854-1, R-853-3, R-855; review #855, #856)
8fbd65a3 fix(crm): pulizia dell'installer che regge un rm fallito, test del secondo Ctrl+C e dell'ordine plist/bootout (R-856-1, R-856-2; review #857)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Commit d54a09ad — review #853 (verdetto integrale)

## VERDETTO: APPROVATO CON RISERVE

Review #853. Diff staged sul ramo claude/nifty-galileo-3k7kbm, sopra main 96d5ae99: 3 file, +14 righe, hash_diff_staged 7ea45b74. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le parti sul CRM) e la mia memoria (la #852-MERGE con R-852M-2). Ho letto per intero tutti i file di scripts/crm/.

**Elementi del diff esaminati**
- `.claude/perimetro_review.txt:36`: aggiunge `scripts/crm/` come cartella (la riga finisce con /).
  - Rischio: che il gate non riconosca la riga, o che il perimetro si restringa.
  - Esito: ok. Ho controllato con `_nel_perimetro` di scripts/check_verdetto.py: installa.sh e il plist ora sono nel perimetro; `scripts/crmx.sh` e reports/crm/ no. Ho rieseguito `pytest tests/test_unit_hooks.py -k "perimetro or gate"`: 128 passed. R-852M-2 è chiusa.
  - Nota: la PR tocca il file del perimetro e scripts/, che stanno nell'elenco della macchina del bot (`scripts/bot_esito.py:69`). Il bot darà quindi `neutral` e il merge lo decide l'operatore: niente merge automatico.
- `scripts/crm/installa.sh:36`: tenta `import gas` dentro un try ed esce con 4 se fallisce (V-2 del bot).
  - Rischio: un `import gas` che scrive su stdout sporcherebbe PORTA. Oppure il codice 4 potrebbe non arrivare al `case`.
  - Esito: ok. Il logging di gas.py va su stderr e nel file. L'ho provato con finti uname/launchctl/plutil/curl/sleep e una copia del repo. Con gas.py rotto (modulo inesistente) esce 1 con «Gas non si avvia con le sue dipendenze». Lo stesso caso con installa.sh di HEAD diceva «manca GAS_CRM_TOKEN»: la correzione serve davvero. Anche i casi token mancante, token solo esportato (exit 2) e GAS_CRM_BIND diverso (exit 3) restano giusti.
- `scripts/crm/installa.sh:54`: nuovo ramo `4)` del `case`. Esito: ok, il messaggio arriva (vedi sopra).
- `scripts/crm/installa.sh:108`: `rm -f "$PLIST"` dopo il bootout, quando la dashboard non risponde (V-1 del bot).
  - Rischio: il percorso cancellato e il plist che launchd ricarica al login.
  - Esito: ok. PLIST è fisso e tra virgolette. In simulazione, con curl sempre muto, ~/Library/LaunchAgents resta vuota ed esce 1. Il percorso riuscito arriva in fondo con exit 0, icona creata e riga della copia cifrata mostrata.
- `reports/crm/decisioni.md:50`: punto 20, coerente con la decisione riportata dal chiamante.
- Contesto, file non toccati:
  - `modules/crm/server.py:906`: il server rifiuta da sé un indirizzo non locale. Un GAS_CRM_BIND messo in ~/.zshenv (che `zsh -c` legge e l'installer no) non apre il CRM in rete: lo fa solo fallire.
  - `modules/crm/server.py:921`: `pronto` (prova della copia cifrata, tetto di 5 s) gira prima di `serve_forever`. I 30 s di attesa dell'installer bastano.

**Riserve (nessuna bloccante)**
- **R-853-1 BASSA** (`scripts/crm/installa.sh:97`): dopo 3 bootstrap falliti il plist resta in ~/Library/LaunchAgents. L'ho provato con un launchctl finto che risponde «Input/output error».
  - Effetto: al login launchd lo carica (RunAtLoad + KeepAlive) senza il controllo della dashboard. È la stessa classe di problema di V-1, ma la correzione copre un solo ramo.
  - Stesso caso, innocuo, dopo `plutil` a `scripts/crm/installa.sh:88`: il plist non valido resta lì ma non si carica.
  - Proposta: una funzione unica «togli servizio» (bootout + rm del plist) per ogni stop dopo `scripts/crm/installa.sh:87`.
- **R-853-2 BASSA** (c'era già prima, ora è nel perimetro; `scripts/crm/com.gas.crm.plist:27`): KeepAlive true con ThrottleInterval 10 e nessun tetto.
  - Se dopo l'installazione il CRM non parte (token tolto dal .env, porta presa da un altro programma, DB non apribile), launchd lo rilancia ogni 10 s per sempre.
  - Ogni rilancio costa un `import gas`, misurato ~1 s di CPU in ambiente pulito, e scrive una riga in `.gas_memory_crm_server.log`, che non ruota. Nessuno avvisa l'operatore.
  - Caso raro (non ho trovato un crollo realistico dopo l'avvio), ma con dati dei clienti: ogni partenza riuscita fa una copia locale (`modules/crm/server.py:352`, nome al secondo a `modules/crm/store.py:1372`) e ne tiene 30. Con un ciclo di crolli dopo l'avvio, in ~5 minuti spariscono le copie dei giorni prima.
  - Proposte: un'attesa lunga prima di uscire sugli STOP quando il CRM gira sotto launchd, e la copia all'avvio solo se l'ultima è vecchia.
- **R-853-3 BASSA**: scripts/crm/ non ha nessun test. La voce invece prova il suo installer con comandi finti (`tests/test_unit_voce_ascolto.py:1938`). V-1 e V-2 sono provate solo dalla mia simulazione manuale.
- **COSMETICHE**: l'uscita 4 non dice quale modulo manca (nel messaggio di un ImportError non ci sono segreti); se il servizio viene tolto, l'icona «CRM Gas» di un'installazione precedente resta sulla Scrivania; CARTELLA_GAS viene sostituita anche nel commento di `scripts/crm/com.gas.crm.plist:5` (un percorso con «--», ammesso da CONSENTITI, renderebbe l'XML non valido e farebbe fermare lo script a plutil); spegni.sh non aspetta che il bootout finisca.

**Wall of Shame e guardrail**: in scripts/crm/ non c'è history, non ci sono tool simulati e non si toccano `_get_window`, il tetto di 10 iterazioni o quello degli 8k token. I finti comandi esistono solo nella mia simulazione, che non è nel diff.

**Rischi esclusi (non verificati)**:
- Comportamento su un Mac vero: launchd reale, permessi di macOS per Scrivania e iCloud (scrivere l'icona può essere negato al Terminale, e con `set -e` lo script finirebbe con un errore di bash dopo aver già acceso il servizio), `plutil` e `wc` di BSD. Ho provato solo su Linux con comandi finti.
- La citazione dell'operatore nel punto 20: non è verificabile dal repo.
- modules/crm/ non l'ho ri-revisionato oltre ai punti citati: è già nel perimetro.

**Note per il chiamante**:
- Ho aggiunto la riga #853 e due lezioni in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, senza indirizzi IP. Il file è modificato ma NON in stage e NON committato. Il primo tentativo con `scripts/commit_memoria_revisore.sh` è stato negato dal permesso automatico, coerente col tuo «non committare»: va committato a fine task.
- L'indice staged è intatto (3 file, +14). Non ho creato .claude/.review_ok.
- R-852M-1 (il .env della voce sul Mac) e le nuove R-853-1..4 vanno scritte in reports/stato_progetto.md: oggi non ci sono.

### Commit 75dbd9d9 — review #854 (verdetto integrale)

## VERDETTO: APPROVATO CON RISERVE

Review #854. Diff staged sul ramo claude/nifty-galileo-3k7kbm, sopra d54a09ad: 4 file, +53/−15, sha256 del diff c17b3830. Prima ho letto CLAUDE.md, la testa di reports/stato_progetto.md (riserve R-852M/R-853) e la memoria del revisore, compresa la riga #853 e le sue due lezioni.

**Elementi del diff esaminati**
- `modules/crm/store.py:1388` — per ogni giorno tiene la copia più recente, usando il nome `crm-AAAAMMGG-HHMMSS`, cioè `name[4:12]`. Rischio esaminato: nomi non in ordine di tempo, chiave del giorno sbagliata, eccezioni nuove fuori dal `try`. Esito: ok. Ho fatto 8 modifiche apposta al codice per vedere se i test se ne accorgono: vecchia regola, niente `ultime`, copia più vecchia del giorno, giorni più vecchi, niente giorni, giorno troncato al mese, `keep+1`, `ultime+1`. Su una copia dell'indice i test le hanno fatte fallire tutte e 8.
- `modules/crm/store.py:1389` — `tenere` = le ultime `ultime` copie più gli ultimi `keep` giorni; `max(1, …)` protegge da 0 e dai negativi. Rischio esaminato: un altro chiamante che usa ancora il vecchio significato di `keep`. Esito: ok. Gli unici chiamanti di `CRMStore.backup` sono `modules/crm/server.py:311` e `modules/crm/__main__.py:186`, entrambi coi valori predefiniti. `modules/crm/copia_cifrata.py:285` non è toccato e tiene già una copia cifrata al giorno. Le altre `backup(..., keep=)` del repo sono di `modules/memory/store.py`, un'altra classe. Nessuna lezione dell'elenco degli errori vietati violata: lo slicing è sull'elenco dei file, non sulla cronologia dei messaggi.
- `tests/test_unit_crm.py:2596` — test nuovo: 40 giorni più 60 riavvii nello stesso giorno. Ho rifatto il conto: restano i giorni dal 12-10 al 10-11, 10 copie di oggi, totale 29+10. Esito: ok. Con il codice vecchio il test fallisce.
- `tests/test_unit_crm.py:2133` — il test esistente passa `keep=2, ultime=2`. Tre copie nello stesso giorno, ne restano 2. Esito: ok.
- `scripts/crm/installa.sh:25` — `togli_servizio` fa lo stesso bootout e la stessa rimozione di `scripts/crm/spegni.sh`. Esito: ok.
- `scripts/crm/installa.sh:94`, `scripts/crm/installa.sh:103`, `scripts/crm/installa.sh:113` — i tre punti di STOP dopo la scrittura del plist (controllo con plutil fallito, 3 caricamenti falliti, dashboard che non risponde). Li ho simulati con comandi finti (uname, launchctl, plutil, curl, sleep): in tutti e tre il plist viene tolto e il bootout parte dopo l'ultimo tentativo di caricamento. Nel caso riuscito restano plist e icona, uscita 0. Esito: ok, R-853-1 chiusa.
- `reports/crm/guida.md:29` e `reports/crm/guida.md:89` — la guida ora descrive la regola nuova. Nel codice e nella guida non resta nessun «ultime 30» riferito alle copie locali. Esito: ok.

Ho rieseguito: `pytest tests/test_unit_crm.py` 151 passed, mypy pulito su store.py, `bash -n` ok.

**Riserve**
- **R-854-1 BASSA**: dopo il caricamento l'installer aspetta la dashboard fino a 30 secondi senza scrivere nulla (`scripts/crm/installa.sh:107`). Se l'operatore preme Ctrl+C in quel momento, plist e servizio restano installati, senza nessun controllo. L'ho provato in simulazione: uscita 130, plist presente, servizio caricato. Nello script non c'è nessun `trap`. Correzione proposta: un `trap togli_servizio INT TERM` tra la scrittura del plist e l'«OK», più una riga «aspetto la dashboard (fino a 30 s)…».
- **R-854-2 BASSA (va scritta giusta in stato_progetto)**: R-853-2 è chiusa **solo per la parte delle copie**. Resta aperta la parte sul KeepAlive senza tetto (`scripts/crm/com.gas.crm.plist:27`): un CRM che non parte si riavvia ogni 10 secondi per sempre, il registro cresce senza rotazione e nessuno viene avvisato. Non segnarla chiusa per intero.
- **R-853-3 BASSA** resta aperta, come hai detto: nessun test degli script del CRM con comandi finti.
- **COSMETICA (c'era già prima)**: un file `crm-*.db` con un nome che non è una data, per esempio una copia fatta a mano, prende il posto di un giorno e di una delle «ultime» e non viene mai cancellato.

**Rischi esclusi (non verificati)**
- Comportamento su un Mac vero (launchd vero, bootout asincrono, permessi della Scrivania): qui non si può riprodurre, la prova è solo simulata.
- Orologio del Mac che torna indietro: la copia appena fatta può essere cancellata subito e `backup()` restituisce un percorso che non esiste più. Succedeva già con la regola vecchia; non l'ho analizzato oltre.
- Il cambio d'ora non l'ho provato: tocca al massimo l'ordine dentro un'ora, non i giorni.

**Memoria**
In `/home/user/Gas/.claude/agents/memoria_revisore.md` ho aggiunto la riga #854 e 2 lezioni (Ctrl+C e `trap` negli installer; riserve composte chiuse solo in parte). **Non l'ho committata**, come in #853: hai chiesto di non committare, e l'hook del gate blocca i comandi di commit finché manca `.claude/.review_ok` (ha bloccato anche un mio comando di sola lettura che nominava lo script di commit). Anche la riga #853 è ancora solo nel working tree. Il file va committato col fine-task. Non ho creato `.claude/.review_ok` e il diff staged non è cambiato.

File della simulazione: `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sim/run.sh` (comandi finti in `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sim/bin`). Script delle prove con le modifiche: `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/mut.py`.

### Commit 5b75c850 — review #855 (verdetto integrale, primo giro)

## VERDETTO: APPROVATO CON RISERVE

Review #855. Ramo claude/nifty-galileo-3k7kbm sopra dfe8fbee. Diff staged: 4 file, +247/−2, sha256 del diff che inizia con e9b23a29. Letture fatte: CLAUDE.md (sez. 1, 5, 8, 9, 10), stato_progetto (Grep mirato), memoria del revisore (lezioni #853 e #854 applicate).

**Elementi del diff esaminati**
- `modules/crm/store.py:1398` — `tenere.add(dest)`: la copia appena fatta non si cancella mai. Rischi esaminati: che il Path non coincida con quello del glob (coincide, stessa `cartella`) e cosa succede con l'orologio indietro (al massimo 11 copie). **ok**
  - Il test nuovo è rosso col codice di HEAD (provato su un export dell'indice).
  - Il mutante «senza add» è ucciso.
- `modules/crm/store.py:44` e `modules/crm/store.py:1389` — filtro `_NOME_COPIA.fullmatch`. Rischio esaminato: un cambio di comportamento sui nomi standard. Non c'è: `[0-9]` accetta solo cifre ASCII, e il formato coincide con lo strftime di `modules/crm/store.py:1375`. **ok**
  - I test di backup già esistenti passano.
  - Il mutante «senza filtro» è ucciso. Quello «match al posto di fullmatch» sopravvive, ma è equivalente: il glob pretende già `.db` in fondo.
  - Chiamanti di contesto invariati: `modules/crm/server.py:311` e `modules/crm/__main__.py:186`.
- `scripts/crm/installa.sh:96` — trap EXIT `[ "$DA_PULIRE" = si ] && togli_servizio`. Rischi esaminati con `set -euo pipefail`: **ok**
  - Il test falso dentro una lista `&&` non fa scattare errexit.
  - Lo stato d'uscita si conserva: 0 in fondo, 1 sugli STOP. La doppia pulizia (togli_servizio esplicito, poi il trap) è idempotente.
  - Provato a mano su bash 5.2 con un sleep finto che manda il segnale al gruppo, durante l'attesa: INT e TERM danno rc 130, plist e servizio tolti; HUP (finestra del Terminale chiusa) toglie anche lui; QUIT è ignorato da bash e si chiude sullo STOP della dashboard.
- `scripts/crm/installa.sh:124` — `DA_PULIRE=no` più `trap - INT TERM` dopo la dashboard. Provato: INT, TERM e HUP dopo la dashboard lasciano il servizio. **ok, con riserva R-855-2**
- `scripts/crm/installa.sh:97` — trap INT/TERM con `exit 130`. **riserva R-855-1**
- `tests/test_unit_crm.py:2713` — `_esegui_crm`. Rischi esaminati, tutti senza problemi: **ok, con riserva R-855-3**
  - Rete: nessuna (curl finto).
  - File toccati: solo sotto tmp_path (HOME finta, cartella di Gas copiata, registro).
  - Ambiente: env ricostruito da zero, niente BASH_ENV.
  - Nessuno sleep vero; `start_new_session` fa di installa.sh il capogruppo, quindi `kill -INT -- "-$PPID"` (`tests/test_unit_crm.py:2684`) colpisce solo il suo gruppo.
- Robustezza dei test: 15 giri da 16 test, tutti verdi (circa 1 s a giro); 18 giri paralleli dei test Ctrl+C, tutti verdi.
- Prova del chiamante confermata: sui test di installa e spegni il codice di HEAD dà 2 failed (percorso completo e Ctrl+C durante l'attesa).
- Mutanti su installa.sh: 5 uccisi su 6.
  - Uccisi: «senza DA_PULIRE=no» (fa fallire anche il percorso completo), «senza trap EXIT», «senza trap INT/TERM», «senza DA_PULIRE=si», «senza la riga Aspetto».
  - Sopravvive «senza `trap - INT TERM`» (vedi R-855-2).
- Rieseguiti: `pytest tests/test_unit_crm.py` (168 passed), mypy su store.py (pulito), `bash -n` (ok), `git diff --staged --check` (pulito).

**Riserve**
- **R-855-1 BASSA** — un secondo Ctrl+C durante la pulizia lascia il servizio installato.
  - Cosa succede: il secondo SIGINT arriva mentre il trap EXIT esegue `launchctl bootout`. Il trap INT fa `exit 130`, bash esce dentro il trap EXIT e salta `rm -f "$PLIST"`.
  - Effetto: plist e servizio restano, e «STOP: interrotto, servizio tolto» compare due volte, quindi è falso.
  - Provato 3 volte su 3 con un launchctl finto che manda SIGINT al gruppo durante il bootout.
  - È lo stesso caso di R-854-1, ristretto a un operatore impaziente.
  - Correzione provata (scenario chiuso e 16/16 test di installa e spegni verdi): `trap 'trap "" INT TERM; [ "$DA_PULIRE" = si ] && togli_servizio' EXIT`. In alternativa, `rm -f "$PLIST"` prima del bootout.
- **R-855-2 BASSA** — sopravvive il mutante «senza `trap - INT TERM`».
  - Con quel mutante, un Ctrl+C dopo la dashboard stampa «servizio tolto» ma il servizio resta.
  - `tests/test_unit_crm.py:2812` non guarda lo stderr. Basta aggiungere `assert "servizio tolto" not in r.stderr`.
- **R-855-3 BASSA** — rosso falso dei test Ctrl+C se pytest parte con SIGINT ignorato.
  - Succede con `nohup` o con `&` in uno script senza job control: bash non può intercettare un segnale ignorato all'ingresso.
  - Provato: 2 failed.
  - La CI di GitHub lancia pytest in primo piano dentro una pipeline, quindi lì va bene.
  - Correzione: in `_esegui_crm`, `preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_DFL)`, oppure uno skip esplicito.
- **COSMETICHE**
  - Gli import a metà del modulo di test (plistlib, shutil, signal, subprocess) violano la regola E402 di PEP 8; in CI non c'è linter.
  - Ci sono due micro-finestre in cui un Ctrl+C dà il messaggio sbagliato: tra `scripts/crm/installa.sh:97` e la riga 98, e tra la riga 124 e la 125.
  - In `reports/crm/guida.md:89`, «con un altro nome»: una copia messa a mano col nome nel formato standard viene gestita (e quindi ruotata) come quelle automatiche.

**Rischi esplicitamente esclusi**
- Comportamento con il `/bin/bash` 3.2 del Mac: non verificato, qui c'è solo bash 5.2. In particolare non so se il trap EXIT parte anche su HUP. INT e TERM invece passano dal trap esplicito con `exit` e valgono in ogni versione.
- Tempi reali di `launchctl bootout` e `bootstrap` su macOS: non riproducibili in dev.
- R-854-2 (KeepAlive senza tetto, registro senza rotazione): fuori scope, resta aperta.
- Orologio spostato in avanti e poi riportato indietro (copie col nome «nel futuro» che occupano le ultime 10): non è un effetto di questo diff, non approfondito.

Nessun antipattern del Wall of Shame: niente slicing della history, niente simulazione di output dei tool (i comandi finti stanno solo nei test, come per la voce). Guardrail del motore non toccati.

Memoria: in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` ho aggiunto la riga #855 e 2 lezioni (pulizia interrotta da un secondo Ctrl+C; test SIGINT con SIGINT ignorato). Il file è fuori dallo stage e NON è committato, come chiesto: niente `commit_memoria_revisore.sh`, niente `.claude/.review_ok`. L'indice è intatto: restano in stage solo i 4 file del diff.

### Commit 5b75c850 — review #856 (verdetto integrale, secondo giro sullo stesso commit)

## VERDETTO: APPROVATO CON RISERVE

Review #856 (secondo giro della #855) sul diff staged del ramo claude/nifty-galileo-3k7kbm, sopra dfe8fbee: 4 file, +256/−3, sha256 del diff 25d93d3f, invariato dopo la review.

Letture fatte: CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (voce CRM e riserve R-853/854/855) e la memoria del revisore (le lezioni su trap, installer e launchd).

Ho rieseguito tutto su una copia dell'indice nello scratchpad: `pytest tests/test_unit_crm.py` dà 168 passed, `git diff --cached --check` è pulito. Ho provato 7 mutanti su installa.sh e scritto 3 sonde mie, che non sono nel repo.

**Elementi del diff esaminati**
- `scripts/crm/installa.sh:97` — il trap EXIT ora parte con `trap "" INT TERM`. Rischio esaminato: un secondo Ctrl+C mentre la pulizia fa il bootout. Ho provato con un launchctl finto che, durante il bootout della pulizia, manda un secondo SIGINT a tutto il gruppo. Col codice staged: rc 130, plist tolto, servizio scaricato, «servizio tolto» stampato una volta sola. Col mutante senza `trap ""` il servizio resta caricato e il messaggio esce due volte, cioè il difetto R-855-1. Percorso riuscito: rc 0, plist e servizio al loro posto, nel registro c'è solo il bootout del passo 2, quindi il trap EXIT non pulisce e `trap ""` non cambia nulla. Esito: ok.
- `scripts/crm/installa.sh:26` — `togli_servizio` toglie prima il plist e poi fa il bootout. Rischio esaminato: un passo che fallisce sotto `set -e`. L'ho provato con uno script giocattolo in cui `rm -f` fallisce: la funzione si chiude subito, il bootout non parte e si perde anche il messaggio STOP, sia nel ramo STOP sia nel trap EXIT. Con l'ordine vecchio il bootout partiva comunque. Esito: riserva (R-856-2).
- `scripts/crm/installa.sh:124` — `trap - INT TERM` viene prima di `DA_PULIRE=no`. Rischio esaminato: la micro-finestra fra le due righe. Ho messo un `kill -INT $$` fra le due righe. Ordine staged: il servizio viene tolto senza messaggio (scelta sicura, rc -2). Ordine della #855: stampava «servizio tolto» e lasciava il servizio. Esito: ok.
- `tests/test_unit_crm.py:2826` — il test controlla che nello stderr non compaia «servizio tolto». Rischio esaminato: il mutante R-855-2. Il mutante «senza `trap - INT TERM`» ora fa fallire 1 test. Ctrl+C dopo la dashboard: rc -2 sia con sia senza `trap ""`, quindi nessun effetto sullo stato d'uscita. Esito: ok.
- `tests/test_unit_crm.py:2726` — `preexec_fn=_segnali_normali` (definita a `tests/test_unit_crm.py:2712`). Rischio esaminato: i rossi falsi se pytest parte con i segnali ignorati. Con pytest lanciato con SIGINT e SIGTERM ignorati: 2 passed; togliendo `preexec_fn`: 2 failed. Esito: ok.
- Stati d'uscita e pulizia ripetuta, riverificati con le nuove posizioni dei trap: 0 / 1 / 130, la pulizia doppia sugli STOP funziona. I mutanti «senza trap EXIT», «senza trap INT» e «senza DA_PULIRE=no» vengono tutti presi dai test. `reports/crm/guida.md:89` è coerente con il controllo del nome di `modules/crm/store.py:44`. Esito: ok.
- Contesto: `scripts/crm/spegni.sh:7` non è toccato e non ha `set -e`, quindi lì un `rm` che fallisce non blocca nulla. Esito: ok.

**Riserve**
- **R-856-1 BASSA**: nessun test del repo fissa la correzione di R-855-1. Due mutanti passano i 16 test di installa/spegni: «senza `trap ""` nel trap EXIT» e «bootout prima di rm». Per il primo basta un test col launchctl finto che, al bootout della pulizia (quando esiste già `registro.txt.ctrlc`), manda `kill -INT` al gruppo; poi si controlla rc 130, «servizio tolto» una sola volta, servizio non caricato. La mia sonda fa esattamente questo e boccia il mutante. Per il secondo mutante basta che il launchctl finto scriva nel registro se il plist esiste ancora al momento del bootout.
- **R-856-2 BASSA**: in `scripts/crm/installa.sh:26` il riordino rende il primo comando quello che può far saltare il resto. Se `rm -f "$PLIST"` fallisce (caso raro: ~/Library/LaunchAgents non scrivibile con un plist già esistente e scrivibile), sotto `set -e` la funzione si chiude prima del bootout: il servizio resta caricato e l'operatore non vede il messaggio STOP. Correzione proposta: `rm -f "$PLIST" || echo "ATTENZIONE: non riesco a togliere $PLIST, toglilo a mano" >&2`.
- **COSMETICA**: con INT e TERM ignorati, un bootout lento (launchd aspetta che il CRM esca, fino a 20 s di default) non si ferma con Ctrl+C; è voluto, va solo saputo. Un HUP durante la pulizia (Terminale chiuso) non è ignorato, ma col plist già tolto al massimo il servizio resta caricato fino al logout.

**Cosa non ho verificato**
- Il comportamento con /bin/bash 3.2 di macOS: ho provato tutto con bash 5.2 su Linux, e su questo dipende da come bash esegue il trap EXIT quando muore per un segnale. Non è riproducibile qui.
- Il launchctl vero (bootout per etichetta senza il file plist, attesa di ExitTimeOut): solo comandi finti.

**Memoria**: aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #856, più una lezione nuova («riordinare una pulizia sotto `set -e` cambia cosa si salta»). Il file non è in stage e non l'ho committato, come avevi chiesto; non ho creato `.claude/.review_ok`.

### Commit 8fbd65a3 — review #857 (verdetto integrale)

## VERDETTO: APPROVATO

Review #857: è il terzo giro sulle riserve della #855. Ho esaminato il diff staged su claude/nifty-galileo-3k7kbm, sopra 5b75c850. Sono 2 file, +50/−3, e lo sha256 del diff staged è a157fd19… (ricalcolato prima e dopo la review: è lo stesso).

Letture obbligatorie fatte: CLAUDE.md (sezione 5 e guardrail), reports/stato_progetto.md (letto per le parti che servono) e la coda di .claude/agents/memoria_revisore.md. Ho applicato le lezioni #853-#856: ogni passo della pulizia deve reggersi da solo sotto set -e, il secondo Ctrl+C durante la pulizia, SIGINT ignorato all'ingresso.

**Elementi del diff esaminati**
- `scripts/crm/installa.sh:28`: `rm -f "$PLIST" || echo "ATTENZIONE…" >&2` prima del bootout.
  - Rischio esaminato: con set -e un rm che fallisce chiudeva togli_servizio prima del bootout (R-856-2). Sia da STOP sia dal trap EXIT il rm sta ora dentro una lista `||` e quindi non fa scattare set -e.
  - Prova: con RM_KO=si escono rc 1, l'ATTENZIONE e lo STOP «la dashboard non risponde»; il servizio non è caricato e il plist resta (il rm finto ha davvero rifiutato). I tre bootout registrati sono uno «no» (quello prima dell'installazione) e due «si».
  - Esito: ok. R-856-2 chiusa.
- `scripts/crm/installa.sh:99`: `trap "" INT TERM` in testa al trap EXIT.
  - Rischio esaminato: che il nuovo test lo fissi davvero (R-856-1).
  - Mutanti: «senza `trap ""`» → 1 rosso (test del secondo Ctrl+C); «solo `trap "" TERM`» → 1 rosso; «bootout prima del rm» → 4 rossi (i 3 STOP e il Ctrl+C durante l'attesa).
  - Esito: ok. R-856-1 chiusa.
- `tests/test_unit_crm.py:2686`: `rm` finto nel PATH; passa a `/bin/rm` salvo RM_KO.
  - Rischio esaminato: che alteri gli altri test (launchctl finto, `spegni.sh`).
  - Prova: senza RM_KO nessun argomento cade nel ramo che fallisce. Il launchctl finto toglie `registro.txt.caricato`, che non corrisponde a `*com.gas.crm.plist`. `exec` conserva il codice d'uscita. Mutante «senza l'rm finto»: fallisce solo il test RM_KO, gli altri 16 test degli script restano identici.
  - Esito: ok.
- `tests/test_unit_crm.py:2674`: il launchctl finto manda il secondo SIGINT al gruppo durante il bootout della pulizia.
  - Rischio esaminato: test fragile sulla CI Ubuntu.
  - Non c'è nessun sleep né corsa di tempi: il finto nasce dopo il `trap ""`, eredita SIG_IGN e sopravvive al proprio kill. Col mutante muore prima di togliere `.caricato`, come farebbe il launchctl vero. `start_new_session` tiene pytest fuori dal gruppo e `preexec_fn` rimette SIG_DFL.
  - Prova: test dei segnali 25/25 in serie, 6/6 in 6 esecuzioni parallele, verdi anche lanciati con nohup. Bash 5.2 e la CI è ubuntu-latest con Python 3.11 (`tests/test_unit_crm.py` gira in CI).
  - Esito: ok.
- `tests/test_unit_crm.py:2751`: `_bootout_col_plist_gia_tolto` richiede almeno un bootout dopo plutil, tutti «bootout-plist no». Il bootout di prima dell'installazione resta escluso.
  - Esito: ok. Un `next()` senza riga plutil darebbe StopIteration, ma è comunque un test rosso.
- `tests/test_unit_crm.py:2853`: test del secondo Ctrl+C. Controlla che il file `.ctrlc2` esista (il secondo SIGINT è partito davvero), rc 130, «servizio tolto» una sola volta, plist tolto e servizio scaricato.
  - Prova: eseguito a mano ho ottenuto stderr `STOP: interrotto, servizio tolto` una sola volta e due bootout entrambi «no».
  - Esito: ok.
- `tests/test_unit_crm.py:2843`: test RM_KO.
  - Mutanti: «rm nudo» → rosso; «rm `|| true` senza messaggio» → rosso.
  - Esito: ok.

**Rieseguito su una copia dell'indice (contenuto staged)**: `python3 -m pytest -q tests/test_unit_crm.py` 170 passed (17 sui soli script del CRM), `bash -n` ok, `git diff --staged --check` ok. Nessun IP letterale nel diff.

**Coerenza col progetto**: la modifica rende la pulizia dell'installer più solida e va nella direzione «zero crash, niente servizio lasciato acceso senza controlli». Non tocca kernel, provider, `_get_window` né i tetti. Wall of Shame: niente slicing della storia; i comandi finti sono controfigure di comandi di sistema nei test, non output inventato dei tool LLM. Non applicabile.

**Note COSMETICHE (non bloccanti, nessuna da tracciare per forza)**
1. Con RM_KO l'ATTENZIONE esce due volte (togli_servizio esplicito + trap EXIT) e in mezzo lo STOP dice «servizio tolto» col plist ancora al suo posto. L'ultima riga a schermo resta comunque l'ATTENZIONE. «toglilo a mano» non dice come farlo. Lo scenario richiede LaunchAgents diventata non scrivibile subito dopo averci scritto il plist.
2. Sopravvive il mutante «solo `trap "" INT`»: TERM durante la pulizia non è provato.
3. Nel finto il percorso `/bin/rm` è scritto a mano: va bene su Ubuntu e sul Mac.
4. Fuori dal diff, c'era già prima: `scripts/crm/spegni.sh:6` fa il bootout PRIMA del rm, cioè l'ordine opposto a R-855-1. Senza set -e, se il rm fallisce scrive comunque «OK: CRM spento e tolto dall'avvio».

**Cosa NON ho verificato**: il comportamento sul Mac vero. Non è riproducibile qui: launchctl/launchd sono finti. In particolare non ho provato quanto dura un bootout reale con INT/TERM ignorati né se `rm` sul plist possa fallire davvero in ~/Library/LaunchAgents (permessi, SIP, iCloud). Non ho provato nemmeno bash 3.2 di macOS: i test girano con /bin/bash di Linux 5.2.

**Memoria**: aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #857 con una lezione nuova (provare il finto passthrough col mutante «senza il finto»; il finto eredita il SIG_IGN del `trap ''` del padre). Il file è fuori stage e NON committato, come da tua richiesta: `scripts/commit_memoria_revisore.sh` non l'ho lanciato. Non ho creato `.claude/.review_ok` e non ho committato nulla. Lo staged è invariato (sha256 a157fd19…).

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_crm.py`: 150 → 170 passed. Nuovi: 3 test delle copie locali (riavvii nello stesso giorno, orologio indietro, copie a mano) e 17 test di `installa.sh`/`spegni.sh` con comandi finti; `test_identita_clienti_e_backup` ora con `keep=2, ultime=2`.
- `tests/test_unit_hooks.py -k "perimetro or gate"`: 128 passed (rieseguito dal revisore #853).
- Suite del kernel non toccata (gas.py e test del kernel invariati).

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST (`commits/SHA/check-runs`).
- Mappatura commit→run:
  - `d54a09ad`, `75dbd9d9`: nessuna run propria (pushati insieme a ca2fc64b).
  - `ca2fc64b`: handoff-check success; verifica-bot annullato (head cambiata durante la verifica).
  - `1b61ec43`: nessuna run propria (pushato con a83ca616). `a83ca616`: verifica-bot annullato (head cambiata).
  - `dfe8fbee`: unit-suite success, handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE, solo BASSE; PR sulla macchina del bot).
  - `5b75c850`, `8fbd65a3` e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-854-2 BASSA: KeepAlive senza tetto, registro senza rotazione, nessun avviso (parte restante di R-853-2).
- COSMETICHE #853/#854/#856/#857: in `reports/stato_progetto.md` (tra cui `spegni.sh` fa il bootout prima del rm, ordine opposto a R-855-1).
- R-852M-1 BASSA (voce, `.env` sul Mac) e riserve della #401 (funnel): in `reports/stato_progetto.md`.
- Dalla PR #397: R-848-2 BASSA, R-848-3 BASSA, V-3 BASSA della verifica esterna, cosmetiche #848; R-836-1 COSMETICA.
- Script non provati su un Mac vero né con bash 3.2.
