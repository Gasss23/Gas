# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — Presentazione clienti (v3, stile HUD) + CI rossa su Ubuntu 26.04 (sandbox del browser)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #380 (https://github.com/Gasss23/Gas/pull/380) — numero e URL dalla risposta reale dello strumento GitHub (create_pull_request / update_pull_request), non da `gh` (in questo ambiente cloud `gh` è riservato alla ricerca). Contiene la correzione della CI (va mergiata presto: sblocca la CI di tutte le PR) e la presentazione in bozza: merge secondo CLAUDE.md §10, con il sì dell'operatore.
2. Prima di usare il PDF con i clienti, farlo vedere a un legale: proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Confermare: storico verificato del copy trading = 23 mesi (non 4 anni); stop sull'equity 10% al livello del copy (30% solo al livello 3 del conto dei dati).
4. Decidere se citare nel PDF il fornitore della strategia («The Source Finance» / «TSF Forex Algo»).
5. Decidere se fissare `runs-on: ubuntu-26.04` in ci.yml (suggerimento del revisore; ci.yml è nel perimetro di review).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — prima bozza del PDF (15 pagine)**: FATTA — 83511a47.
- **Fetta 2 — dati reali del copy trading Forex (catalogo TSF, servizio 01)**: FATTA — 03466aae.
- **Fetta 3 — PDF v3: stile HUD «tipo Jarvis», 8 pagine, linguaggio per chi investe la prima volta**: FATTA — b020cbfa.
- **Fetta 4 — CI rossa: sandbox del browser su Ubuntu 26.04 (attività «Fix CI web suite: bwrap sandbox tests fail» chiesta dall'operatore)**: FATTA nel codice — 605e154c, review #803 → #804 → #805 APPROVATO; DA CONFERMARE sulla CI vera del branch (§6).
- **Fetta 5 — dati dei servizi 1, 2 e 4**: DEFERITA — l'operatore deve ancora mandarli.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md                 |   5 +++
 modules/web/browser.py                             |  93 +++++++++++++++++++++++++++++++++++++++++--
 presentazione_clienti/.gitignore                   |   1 +
 presentazione_clienti/Presentazione_Ecosistema.pdf | Bin 0 -> 1408521 bytes
 presentazione_clienti/build.py                     | 745 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 presentazione_clienti/render.js                    |  15 +++++++
 presentazione_clienti/titoli_svg.json              |  10 +++++
 reports/diff_sessione.md                           |  19 ++++++---
 reports/handoff.md                                 | n/d
 reports/stato_progetto.md                          |   1 +
 reports/ultimo_report.md                           |  24 ++++++-----
 tests/test_unit_web_browser.py                     |  89 ++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
b020cbfa presentazione clienti: versione 3 in stile HUD, 8 pagine, linguaggio semplice
605e154c fix(web): sandbox del browser su Ubuntu 26.04 — programmi di /usr/bin collegati altrove
c75f77cd chore(revisore): memoria review #805 — APPROVATO
bd08c661 chore(revisore): memoria review #804 — APPROVATO CON RISERVE
2d144fed chore(revisore): memoria review #803 — APPROVATO CON RISERVE
718c6dd5 docs(fine-task): report della presentazione clienti con i dati reali del copy trading
03466aae presentazione clienti: dati reali del copy trading Forex (catalogo TSF)
adb0e188 docs(fine-task): report della bozza della presentazione clienti
83511a47 presentazione clienti: prima bozza del PDF dell'ecosistema (15 pagine)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: 605e154c (modules/web/browser.py, tests/test_unit_web_browser.py). Tre review sullo stesso diff (riserve applicate tra una e l'altra); verdetti incollati integralmente, nell'ordine.

### Verdetto review #803 (integrale)

## VERDETTO: APPROVATO CON RISERVE

Review #803 (chat practical-tesla). Ho esaminato il diff staged, sha256 c5460dbe47b954d8 (2 file, +150/−1), invariato dall'inizio alla fine della review. Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (testa) e la memoria del revisore, in particolare le lezioni sul sandbox delle review #599–#610.

### Prove eseguite da me (Ubuntu 24.04, root, bwrap 0.9.0)
- **La causa è confermata nel log CI** (run 44173255137): «Image: ubuntu-26.04», «resolute», gli stessi 7 test bwrap rossi.
- **Riproduzione**: ho collegato `/usr/bin/sleep` (relativo) e `/usr/bin/cat` (assoluto) dentro `/usr/lib/cargo/bin/coreutils/`.
  - Con il codice di HEAD: 6 failed. Sono 4 test preesistenti (morto_bwrap, ucciso_bwrap, gas_e_la_home…, permessa_collegamento) più i 2 test nuovi.
  - Con il diff staged: 46 passed.
  - Layout ripristinato e verificato.
- **Suite**: con il layout normale e `GAS_TEST_BROWSER_OBBLIGATORIO=1`, `tests/test_unit_web_browser.py` dà 46 passed e `tests/test_unit_web_*.py` dà 642 passed, 114 skipped (coincide con quanto dichiarato). `git diff --cached --check` è pulito.
- **Mutanti** (su una copia dell'indice): 7 uccisi su 8.
  - Uccisi: fix spento, controllo della cartella-collegamento tolto, controllo dei protetti tolto, radici tolte, montaggio della cartella intera invece del file, `isfile` tolto, catena registrata anche senza file finale.
  - Sopravvive solo «protetti solo lessicali»: è equivalente, perché il realpath alla riga 289 è ridondante (vedi F-5).
- **Sonda dentro il sandbox**: di `/usr/lib/jvm` si vedono solo i 30 file collegati, su 313 presenti sull'host. `/usr/local` è assente. Ogni file è un montaggio a sé (114 sotto llvm-18). `sleep` funziona. Costo di `_programmi_fuori`: circa 17 ms per lettura.

### Elementi del diff esaminati
- `modules/web/browser.py:278` — `_programmi_fuori` segue le catene dei collegamenti di /usr/bin; rifà con `--symlink` i collegamenti non visibili e monta con `--ro-bind` il solo file vero.
  - Rischio esaminato: fuga di Gas o della home, esposizione di cartelle, socket o FIFO.
  - Esito: ok. Si monta solo un file regolare (`isfile` su un percorso che non è un collegamento, riga 316), quindi niente cartelle, socket o FIFO. Una catena rotta, ciclica o oltre 16 salti non espone niente (come prima).
- `modules/web/browser.py:309` — per ogni anello non visibile richiede `realpath(genitore) == genitore` e `_ammesso`.
  - Rischio esaminato: una cartella-collegamento sotto /usr che porta in /opt o in Gas (`_ammesso` controlla le radici solo sul percorso lessicale).
  - Esito: ok. È questo controllo a garantire che il percorso vero coincida con quello lessicale. Il mutante che lo toglie è ucciso dal test unitario.
- `modules/web/browser.py:287` — `_ammesso` richiede radici /usr o /etc/alternatives e nessuna sovrapposizione con i protetti (che sono già risolti con realpath).
  - Rischio esaminato: Gas installato sotto /usr.
  - Esito: ok, con la riserva F-2 su /usr/local.
- `modules/web/browser.py:383` — la chiamata sta prima della copertura tmpfs dei protetti e prima di `--remount-ro /`.
  - Rischio esaminato: l'ordine dei montaggi (un `--symlink` dentro un `--ro-bind` darebbe EROFS) e un tmpfs scavalcato.
  - Esito: ok. Si ricreano solo anelli non visibili, quindi mai dentro le cartelle permesse; i file esposti non sono mai protetti. La sonda `_bwrap_funziona` usa lo stesso comando, quindi resta coerente.
- `tests/test_unit_web_browser.py:479` — il test unitario fissa i casi Gas/home, catena rotta, fuori dalle radici, ciclo, cartella-collegamento e duplicato con un'uguaglianza esatta (riga 506).
  - Esito: ok. Uccide 6 mutanti.
- `tests/test_unit_web_browser.py:464` — il test d'integrazione bwrap: il programma si esegue e il file «segreto» nella stessa cartella esterna resta nascosto.
  - Esito: ok. Morde anche sul layout normale (con HEAD fallisce) e uccide il mutante «cartella intera».
- `tests/test_unit_web_browser.py:395` e `tests/test_unit_web_browser.py:429` — l'insieme dei file ammessi in più è calcolato dall'host, non preso dal codice.
  - Esito: ok con riserva. È più largo di quello che il codice espone (non applica il controllo sui genitori né quello sui protetti). Le regole di rifiuto le tiene il test unitario, non questo.

### Finding
- **F-1 (BASSA, R-803-1)**: tre promesse scritte nel modulo ora sono false. Si trovano in `modules/web/browser.py:13`, `modules/web/browser.py:88` e `modules/web/browser.py:334`, e dicono che del sistema si vedono SOLO `_PERMESSE`, node, Playwright e Chromium. Ora si vedono anche file sotto /usr raggiunti da /usr/bin e collegamenti in /etc/alternatives: su questo container sono 155 file e 114 collegamenti in più (llvm-18, jvm, `/usr/sbin/killall5`, `/usr/lib/systemd/…`). Vanno aggiornate dichiarando la classe nuova e i suoi limiti.
- **F-2 (BASSA, R-803-2)**: l'esposizione è più larga del necessario. Diventa visibile ogni bersaglio dei collegamenti di /usr/bin, non solo i coreutils. Il contenuto è innocuo: file pubblici dei pacchetti, in sola lettura, `nosuid`, senza capability e senza rete, e /usr/bin era già tutta visibile. Due restringimenti a costo quasi nullo:
  - esporre solo file con il bit di esecuzione (`st_mode & 0o111`);
  - togliere /usr/local dalle radici (è l'area locale dell'amministratore).
- **F-3 (BASSA, R-803-3)**: `os.readlink` alla riga `modules/web/browser.py:313` e `os.listdir` alla riga `modules/web/browser.py:297` stanno fuori dal try. Una corsa, per esempio un aggiornamento dei pacchetti a metà, dà OSError: `_bwrap_funziona` mette False in cache e il browser resta spento fino al riavvio. È fail-closed, non una fuga; `leggi_con_browser` intercetta comunque tutto (§9 rispettato). Rimedio: un try che salti quel programma.
- **F-4 (COSMETICA, R-803-4)**: `modules/web/browser.py:382` mette /lib, /sbin, ecc. tra i percorsi «visibili». Con /usr unito, però, /lib/x si vede solo se si vede /usr/lib/x. Un collegamento assoluto `/lib/…` verso un file non visibile non verrebbe montato e il programma resterebbe rotto: direzione fail-closed. Il commento «i percorsi come li vede il sandbox» è impreciso.
- **F-5 (COSMETICA)**: la parte realpath del controllo sui protetti (`modules/web/browser.py:289`) è ridondante, quindi nessun test la tiene; va bene tenerla come difesa in più. Il test alla riga `tests/test_unit_web_browser.py:500` scambia a mano le variabili globali del modulo invece di usare `monkeypatch` (funziona, grazie al try/finally).

### Condizione (non un finding sul codice)
La correzione è provata solo su un layout simulato. Il layout vero di 26.04 non l'ho visto: per esempio, se `/usr/lib/cargo/bin` fosse a sua volta un collegamento a una cartella, il controllo della riga 309 rifiuterebbe la catena (fail-closed) e la CI resterebbe rossa. Non dichiarare chiusa la CI rossa finché lo step «Run web suite» non è verde sulla run CI del branch (ubuntu-26.04 vera).

### Alternativa `runs-on: ubuntu-24.04`
Sconsigliata come sostituto: renderebbe la CI verde nascondendo che su 26.04 (la prossima LTS, probabile sistema del VPS) mezza /usr/bin del sandbox è rotta. Come complemento ha senso pinnare esplicitamente `ubuntu-26.04` dopo questo fix, così un futuro cambio d'immagine diventa una scelta e non una sorpresa. Tocca ci.yml, che è nel perimetro di review: la decisione spetta all'operatore.

### Coerenza col progetto
- Va nella direzione «robustezza > potenza»: ogni ramo dubbio non espone niente, cioè si comporta come prima.
- Non tocca `run_turn`, il tetto di 10 iterazioni, `_get_window`, il tetto di output né la memoria.
- Wall of Shame: niente slicing della history né output di tool simulati.
- Type hints coerenti con il resto del file.

### Rischio escluso
Non ho verificato il comportamento su un vero Ubuntu 26.04 (layout reale di rust-coreutils, smistamento del binario multicall per argv[0]), su aarch64, sul VPS, né con l'utente non root della CI: sono stati provati solo root su 24.04 e il layout simulato. Non ho misurato il tempo di avvio con le centinaia di montaggi in più su un runner affollato.

### Memoria del revisore
Riga #803 e una lezione aggiunte in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (commit 2d144fed, `scripts/commit_memoria_revisore.sh`). L'indice staged è intatto. Ho usato l'etichetta «(chat practical-tesla)» perché un altro branch è già a #808 (rischio di collisione nella numerazione).

File rilevanti:
- `/home/user/Gas/modules/web/browser.py`
- `/home/user/Gas/tests/test_unit_web_browser.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Verdetto review #804 (integrale)

## VERDETTO: APPROVATO CON RISERVE

Review #804 (chat practical-tesla): seconda review del delta rispetto alla #803. Diff staged sha256 a296d7d135f5cbba, 2 file, +175/−5, invariato durante tutta la review.

**Cosa ho rifatto io**
- **Suite**: con `GAS_TEST_BROWSER_OBBLIGATORIO=1`, `tests/test_unit_web_browser.py` dà 46 passed sia sul layout normale sia su quello 26.04 simulato (`sleep` collegato in modo relativo, `cat` in modo assoluto dentro `/usr/lib/cargo/…`; layout ripristinato e verificato). `tests/test_unit_web_*.py` dà 642 passed, 114 skipped. `--check` pulito.
- **Esposizione su questo container**: 155 file e 114 collegamenti in più, come nella #803. Sono tutti eseguibili; nessun file sotto /usr/local.
- **Mutanti**, provati su una copia dell'indice:
  - uccisi: fix spento, controllo della cartella-collegamento, /usr/local escluso, bit di esecuzione, cartella intera, catena registrata senza file finale;
  - **sopravvivono «senza protetti» e «senza radici»** (3 passed), che nella #803 erano uccisi.

**Elementi del delta esaminati**
- `modules/web/browser.py:324` — filtro del bit di esecuzione (`os.stat(dopo).st_mode & 0o111`). `dopo` non è mai un collegamento, quindi `stat` equivale a `lstat`. Rischio esaminato: un file di dati o di configurazione esposto. Esito: ok, chiude R-803-2.
- `modules/web/browser.py:278` e `modules/web/browser.py:293` — `_ESCLUSE_PROGRAMMI = ("/usr/local",)`, controllata in `_ammesso` solo sugli anelli non visibili. Insieme al controllo sul genitore reale (riga 313) vale anche se /usr/local è a sua volta un collegamento. Rischio esaminato: un collegamento che porta in /usr/local. Esito: ok.
- `modules/web/browser.py:301` e `modules/web/browser.py:326` — `os.listdir` e il blocco `islink/readlink/stat` dentro `try/except OSError`. In caso di errore si salta il programma o la cartella: nessuna eccezione arriva a `_bwrap_funziona`, quindi la sonda non resta in cache a False. Esito: ok, chiude R-803-3.
- `tests/test_unit_web_browser.py:502`, `tests/test_unit_web_browser.py:508` e `tests/test_unit_web_browser.py:511` — casi nuovi «non-eseguibile» e «da-locale», più `monkeypatch` al posto dello scambio manuale. Esito: ok. Uccidono i rispettivi mutanti; R-803-5 chiusa.
- `tests/test_unit_web_browser.py:489` e `tests/test_unit_web_browser.py:490` — `.env` dentro il protetto e `altrove/x` vengono creati vuoti con `open(...).close()`, cioè **senza bit di esecuzione**. Esito: **riserva MEDIA** (vedi R-804-1).

**Finding**
- **R-804-1 (MEDIA)** — Il filtro nuovo a monte ha reso vacui due casi del test unitario.
  - I casi «dentro-gas» e «fuori-radici» ora vengono scartati dal filtro del bit di esecuzione prima di arrivare al controllo dei protetti e a quello delle radici.
  - Così la regola centrale della correzione («mai esporre file di Gas o della home») e il recinto /usr e /etc/alternatives non sono più tenuti da nessun test.
  - La docstring del test dichiara una copertura che non c'è: il test passa per il motivo sbagliato.
  - Il codice è corretto e non c'è nessuna fuga oggi: è una regressione della rete di test introdotta da questo delta.
  - **Correzione provata**: aggiungere `os.chmod(os.path.join(protetto, ".env"), 0o755)` e `os.chmod(os.path.join(altrove, "x"), 0o755)` subito dopo le righe 489-490. Con questa modifica entrambi i mutanti sono di nuovo uccisi, «senza bit di esecuzione» resta ucciso dal caso «non-eseguibile» e la suite dà 46 passed.
  - **Consiglio**: chiuderla PRIMA del commit. Sono 2 righe, ma cambiano lo SHA del diff, quindi serve una ri-review del micro-delta. Se si committa così com'è, va tracciata in `reports/stato_progetto.md` come MEDIA aperta.
- **R-804-2 (COSMETICA)** — Due testi non descrivono il codice com'è.
  - `modules/web/browser.py:18` dice che si ricreano i collegamenti intermedi «di /etc/alternatives». In realtà si ricreano anche sotto /usr: qui 114 sotto `/usr/lib/llvm-18/bin`. Un collegamento non espone contenuto, ma la frase sta dentro una promessa «SOLO».
  - Il commento a `modules/web/browser.py:390` («contano visibili solo se lo è il loro bersaglio») si legge come un controllo che il codice non fa: /bin, /lib… sono contati SEMPRE come visibili. Formulazione proposta: «contati sempre come visibili: se il bersaglio non lo è, il programma resta rotto (fail-closed)».

**Riserve della #803**: R-803-1, 3, 4 e 5 chiuse nel codice (R-803-1 con il residuo di R-804-2). R-803-2 chiusa, ma la sua chiusura ha generato R-804-1.

**Condizione invariata dalla #803**: la chiusura della CI rossa è provata solo sul layout simulato. La prova vera è lo step «Run web suite» verde sulla run CI del branch (ubuntu-26.04).

**Coerenza col progetto**: il delta stringe l'esposizione e aggiunge fail-safe (§9). Non tocca `run_turn`, il cap di 10 iterazioni, `_get_window`, il cap di 8k né la memoria. Nessun antipattern del Wall of Shame.

**Rischio escluso**: non ho verificato il layout vero di Ubuntu 26.04 né un utente non root (tutto provato da root su 24.04). Non ho cercato su un sistema reale un caso di programma di /usr/bin con bersaglio non eseguibile: il filtro è provato solo con i dati sintetici del test.

**Memoria del revisore**: riga #804 e una lezione aggiunte in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (commit bd08c661). L'indice staged è intatto.

File rilevanti:
- `/home/user/Gas/modules/web/browser.py`
- `/home/user/Gas/tests/test_unit_web_browser.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Verdetto review #805 (integrale)

## VERDETTO: APPROVATO

Review #805 (chat practical-tesla): riguarda solo il micro-delta che chiude le riserve della #804. Diff staged sha256 e7097f30ff7b5864 (2 file, +177/−5), invariato durante tutta la review.

**Cosa ho rifatto io**
- **Mutanti**: 9 su 9 uccisi, su una copia dell'indice:
  - fix spento;
  - senza il controllo della cartella-collegamento;
  - senza i protetti;
  - senza le radici;
  - senza /usr/local escluso;
  - senza il bit di esecuzione;
  - cartella intera al posto del file;
  - catena registrata senza file finale;
  - senza protetti e senza bit insieme.
- **Codice invariato rispetto alla #804**: le ancore testuali dei mutanti su `_programmi_fuori` combaciano tutte una volta sola.
- **Suite**: `tests/test_unit_web_*.py` con `GAS_TEST_BROWSER_OBBLIGATORIO=1` dà 642 passed, 114 skipped. `git diff --cached --check` è pulito.

**Elementi del micro-delta esaminati**
- `tests/test_unit_web_browser.py:489` — un ciclo crea `.env` del protetto e `altrove/x`, con `os.chmod(f, 0o755)` alla riga `tests/test_unit_web_browser.py:491`.
  - Rischio esaminato: casi di test vacui, fermati dal filtro +x invece che dalla regola che dichiarano di provare.
  - Esito: ok. R-804-1 è chiusa: «senza protetti» e «senza radici» ora fanno fallire `test_programmi_fuori_espone_solo_catene_ammesse`.
- `modules/web/browser.py:18` e `modules/web/browser.py:19` — la docstring del modulo ora dice che i collegamenti intermedi stanno «sotto /usr o /etc/alternatives» e che «un collegamento non espone contenuto».
  - Rischio esaminato: una promessa «SOLO» più stretta del comportamento reale (che vedeva 114 collegamenti sotto `/usr/lib/llvm-18`).
  - Esito: ok, la descrizione ora corrisponde al codice.
- `modules/web/browser.py:391` — il commento sui «visibili» ora dice «contati sempre come visibili: se il bersaglio non lo è, il programma resta rotto (fail-closed)».
  - Rischio esaminato: un commento che descrive un controllo inesistente.
  - Esito: ok, corrisponde a `modules/web/browser.py:395`, che li aggiunge senza condizioni.

**Finding**: nessuno nuovo. R-803-1…5 e R-804-1/2 sono tutte chiuse.

**Condizione ancora aperta dalla #803 (non è un finding sul codice)**: la CI rossa va dichiarata chiusa solo quando lo step «Run web suite» è verde sulla run CI del branch, cioè su ubuntu-26.04 vera. Finora la correzione è provata solo sul layout simulato.

**Alternativa `runs-on: ubuntu-24.04`**: il parere della #803 resta valido.
- Come sostituto della correzione è sconsigliata: nasconderebbe il guasto su 26.04, la prossima LTS.
- Pinnare `ubuntu-26.04` in modo esplicito dopo questo fix è una scelta che spetta all'operatore (ci.yml è nel perimetro di review).

**Coerenza col progetto**: modifica fail-closed e §9 rispettato. Nessun guardrail toccato (`run_turn`, tetto di 10 iterazioni, `_get_window`, tetto di 8k caratteri di output). Nessun antipattern del Wall of Shame.

**Rischio escluso**: non ho riprovato il layout 26.04 simulato su questo micro-delta, perché il codice è identico a quello già provato nella #804 (46 passed) e il test cambia solo i permessi dei file d'esempio. Restano non verificati il layout vero di 26.04, un utente non root e aarch64.

**Memoria del revisore**: riga #805 aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola (commit c75f77cd); nessuna lezione nuova. L'indice staged è intatto.

File rilevanti:
- `/home/user/Gas/modules/web/browser.py`
- `/home/user/Gas/tests/test_unit_web_browser.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Modificati modules/web/browser.py e tests/test_unit_web_browser.py. Con GAS_TEST_BROWSER_OBBLIGATORIO=1, in locale (Ubuntu 24.04 con bwrap installato):

```
layout normale, prima (HEAD 01eb9f50):  tests/test_unit_web_*.py      640 passed, 114 skipped
layout 26.04 simulato, prima:           tests/test_unit_web_browser.py 7 failed, 37 passed
layout normale, dopo:                   tests/test_unit_web_*.py      642 passed, 114 skipped
layout 26.04 simulato, dopo:            tests/test_unit_web_*.py      642 passed, 114 skipped
```

I 114 skipped sono test di selectolax (non installato in locale), fuori scope. Sulla CI vera (ubuntu-26.04): prima 7 failed / 747 passed nello step «Run web suite» (run 44155950606); dopo: vedi §6.

## §6 STATO CI

`gh run list` non usato (in questo ambiente cloud `gh` è riservato alla ricerca). Output reale dello strumento GitHub `actions_list` (list_workflow_runs, workflow ci.yml, branch claude/practical-tesla-ea9a9g) alla scrittura:

```
CI  run 44187987070  #1949  push  in_progress        sha b020cbfa  https://github.com/Gasss23/Gas/actions/runs/44187987070
CI  run 44173255137  #1945  push  completed/failure  sha 718c6dd5  https://github.com/Gasss23/Gas/actions/runs/44173255137
```

Mappatura commit→run:
- 83511a47 → run 44155605928: failure (web suite, 7 test bwrap — guasto dell'ambiente 26.04).
- adb0e188 → run 44155950606: failure (stessa causa).
- 03466aae → nessuna run su questo SHA (pushato insieme a 718c6dd5, testato solo come parte di quell'albero).
- 718c6dd5 → run 44173255137: failure (stessa causa).
- 2d144fed, bd08c661, c75f77cd, 605e154c → nessuna run su questi SHA (pushati insieme a b020cbfa: la run testa solo l'albero di testa).
- b020cbfa → run 44187987070: in corso alla scrittura dell'handoff (è la prima run col fix: la prova della condizione del revisore).
- commit di fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna riserva del revisore aperta (R-803-1..5 e R-804-1/2 chiuse, #805 APPROVATO).
- Condizione: CI rossa da dichiarare chiusa solo con lo step «Run web suite» verde sulla run del branch su ubuntu-26.04 vera (run 44187987070 o successive).
