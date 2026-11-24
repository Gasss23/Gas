# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Revisione in più sugli script del CRM

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: tocca `.claude/perimetro_review.txt` e `scripts/`, quindi il bot darà `neutral` e il merge lo decide l'operatore.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; controllare che l'ultima riga dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

---

## §1 SCOPE & ESITO FETTE

- **`scripts/crm/` nel perimetro di review** (richiesta dell'operatore: «ci sta comunque una revisione in più, dato che comunque sono dati personali dei clienti e non dobbiamo fare assolutamente neanche un errore»; decisione 20): FATTA (d54a09ad, review #853 APPROVATO CON RISERVE). R-852M-2 chiusa.
- **Note del bot sulla #403 rimaste aperte** (V-1 plist lasciato se la dashboard non parte; V-2 errore di import scambiato per token mancante): FATTE (d54a09ad).
- **R-853-1 e R-853-2 (parte delle copie)**: FATTE (75dbd9d9, review #854 APPROVATO CON RISERVE). `togli_servizio` a ogni STOP dell'installer; copie locali per giorno (30 giorni più le ultime 10).
- **R-853-2, parte KeepAlive senza tetto** (ora R-854-2): NON FATTA, resta aperta.
- **Merge di main (PR #401 del funnel, altra chat)** (1b61ec43): FATTO. Conflitti solo sui report e sulla memoria del revisore: report del ramo tenuti, righe della memoria unite, riserve dell'ultimo verdetto del bot sulla #401 (V-1 BASSA, V-2 COSMETICA) riportate in `reports/stato_progetto.md` (regola 3). Nessun file del perimetro nel merge: niente review.
- **Prova su un Mac vero**: SALTATA — il Mac non è raggiungibile da qui; provata dal revisore su Linux con comandi finti.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  6 ++++++
 .claude/perimetro_review.txt       |  3 +++
 modules/crm/store.py               | 22 ++++++++++++++++------
 reports/bacheca.md | 4 ++--
 reports/crm/decisioni.md           |  4 ++++
 reports/crm/guida.md               |  4 ++--
 reports/diff_sessione.md           | 17 +++++++++--------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 30 ++++++++++++++++--------------
 scripts/crm/installa.sh            | 18 +++++++++++++++---
 tests/test_unit_crm.py             | 29 ++++++++++++++++++++++++++---
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale. Base: main 96d5ae99.

## §3 GIT LOG --ONELINE (sessione)

```
75dbd9d9 fix(crm): copie locali per giorno (30 giorni più le ultime 10) e servizio tolto a ogni STOP dell'installer (R-853-1/2, review #854)
d54a09ad chore(perimetro): scripts/crm/ passa dal revisore (decisione 20); installer: plist tolto se la dashboard non parte, errore di import distinto (review #853)
ca2fc64b docs(fine-task): scripts/crm/ nel perimetro di review e copie locali per giorno — report, handoff (review #853, #854) e stato
1b61ec43 Merge origin/main (PR #401 funnel) nel ramo della PR #404 — report del ramo tenuti, riserve dell'ultimo verdetto del bot sulla #401 in stato_progetto (regola 3)
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

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_crm.py`: 150 → 151 passed (nuovo `test_backup_tiene_i_giorni_anche_con_tanti_riavvii`; `test_identita_clienti_e_backup` ora con `keep=2, ultime=2`).
- `tests/test_unit_hooks.py -k "perimetro or gate"`: 128 passed (rieseguito dal revisore #853).
- Suite del kernel non toccata (gas.py e test del kernel invariati).

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `d54a09ad`, `75dbd9d9`: nessuna run propria (pushati insieme al commit di fine-task).
  - Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.
- Ultima run nota su main 96d5ae99 (merge della #403): CI verde al merge.

## §7 RISERVE APERTE

- R-854-1 BASSA: Ctrl+C durante l'attesa della dashboard lascia il servizio installato (serve `trap togli_servizio INT TERM`).
- R-854-2 BASSA: KeepAlive senza tetto, registro senza rotazione, nessun avviso (parte restante di R-853-2).
- R-853-3 BASSA: nessun test degli script del CRM con comandi finti.
- COSMETICHE #853/#854: in `reports/stato_progetto.md`.
- R-852M-1 BASSA (voce, `.env` sul Mac): in `reports/stato_progetto.md`.
- Dalla PR #397: R-848-2 BASSA, R-848-3 BASSA, V-3 BASSA della verifica esterna, cosmetiche #848; R-836-1 COSMETICA.
- Script non provati su un Mac vero.
