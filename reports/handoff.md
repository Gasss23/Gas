# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #233) — compiti notturni che riprendono dopo un crash (R7/M3 fetta 1), spesa giornaliera incrementale (5.5), piccole riserve

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #234 (https://github.com/Gasss23/Gas/pull/234; numero e URL dall'API GitHub, `gh` non usato): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).
2. C6 (bottone «Modifica» e firme a gruppi): decisione dell'operatore.

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #233**: `FATTA` — su richiesta dell'operatore («mergia 233»), merge `7bd0875`.
- **R7/M3 fetta 1 — ripresa dei compiti dopo un crash**: `FATTA` — review #406, #407 (chat Motore) APPROVATO CON RISERVE.
- **Riserve R-407-1/2, R-405-1/2, R-404-2**: `FATTA` — review #408 APPROVATO CON RISERVE.
- **5.5 R-tel-budget-perf — spesa letta solo sulle righe nuove**: `FATTA` — review #409, #411 APPROVATO CON RISERVE.
- **V-1 bot #234, V-4 verifica esterna #234, R-409-1/2/3**: `FATTA` — review #410 APPROVATO CON RISERVE.
- **C6**: `SALTATA` — decisione dell'operatore.
- **R7 — ripresa dal punto esatto**: `DEFERITA` — da valutare.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +++
 gas.py                             |  94 +++++++++++++++++++++++++++++++++++------------
 modules/gate/gate.py               |  12 +++++-
 modules/notte/notte.py             | 124 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/da_mergiare.md             |  87 +++++++++++++-------------------------------
 reports/diff_sessione.md           |  15 +++-----
 reports/handoff.md                 | 720 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  37 +++++++------------
 tests/test_unit_gate.py            |   8 ++++
 tests/test_unit_kernel.py          |  53 +++++++++++++++++++++++++++
 tests/test_unit_notte.py           | 194 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 12 files changed, 674 insertions(+), 678 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
4227270 fix(budget): conteggi negativi o enormi nel registro dei token non abbassano né azzerano la spesa (R-410-1/2)
d9e8ed9 chore(revisore): memoria review #411 — APPROVATO CON RISERVE
7e9900c fix(notte,budget): compito tolto dal registro prima della riflessione; registro più severo; costo: in/out separati, impronta di coda (V-1 bot #234, V-4 verifica #234, R-409-1/2/3)
3ef6572 chore(revisore): memoria review #410 — APPROVATO CON RISERVE
6f6edd7 perf(budget): il costo delle ultime 24 ore legge solo le righe nuove del registro dei token (R-tel-budget-perf, roadmap 5.5)
6a16311 chore(revisore): memoria review #409 — APPROVATO CON RISERVE
5267148 docs(fine-task): report, handoff, coda da_mergiare — ripresa dei compiti dopo un crash (R7)
bb9305e fix: registro dei crash non azzerato da un catalogo rotto; read_file nega nomi vuoti; test del lock stabile (R-407-1/2, R-405-1/2, R-404-2)
5756a04 chore(revisore): memoria review #408 — APPROVATO CON RISERVE
d51de97 fix(notte): salto per crash ripetuti = ko; chiesto a mano si rilancia; voci fuori catalogo tolte (R-406-1/2/3)
38e4240 chore(revisore): memoria review #407 — APPROVATO CON RISERVE
6eaab53 feat(notte): i compiti interrotti da un crash riprendono per primi al giro dopo (R7, M3 fetta 1)
52e8693 chore(revisore): memoria review #406 — APPROVATO CON RISERVE
fc39109 chore(revisore): memoria review #406 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #406 (chat Motore) — commit 6eaab53

## VERDETTO: APPROVATO CON RISERVE

Review #406 (chat Motore). Il diff staged tocca due file: `modules/notte/notte.py` e `tests/test_unit_notte.py`. Questa è la prima fetta di R7/M3, la ripresa di un compito interrotto da un crash.

Prima della review ho letto, come richiesto: CLAUDE.md (sezioni 1, 5, 8, 9 e 10), `reports/stato_progetto.md` (cercando con grep le parti su notte/R7) e la coda di `.claude/agents/memoria_revisore.md`.

**Cosa ho rifatto io**
- Suite notte: 115 passed.
- Prova a mutazione: ho tolto `"ripresa": True` dentro `_ordina_riprese`. Falliscono 2 test r7 (tra cui il round-trip col kernel vero), quindi i test colgono il difetto. File ripristinato, `git status` pulito.
- Sonda con `solo` e con una voce «fantasma» nel registro: risultati sotto.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:509` — `_leggi_in_corso` legge il registro. Rischio: JSON rovinato, nomi con `../`, `tentativi` di tipo sbagliato. Si ottiene `{}` e un avviso nel log, nomi controllati con `_NOME_RE`, `RecursionError` preso dall'`except Exception`. Esito: ok (`True` passa come int, innocuo).
2. `modules/notte/notte.py:603` — il registro si legge dopo il `flock`, e tutte le scritture (`modules/notte/notte.py:607`, `modules/notte/notte.py:643`, `modules/notte/notte.py:649`) stanno dentro il lock. Rischio: due giri che si sovrascrivono il registro. Esito: ok.
3. `modules/notte/notte.py:643`-`modules/notte/notte.py:649` — il conto sale prima del compito e la voce si toglie dopo. Rischio: un compito finito male lasciato nel registro come se fosse un crash. `_esegui_compito` intercetta ogni `Exception` e il tempo scaduto, e risale solo una `BaseException` (kill, Ctrl-C), che è proprio il caso voluto. Compiti saltati per il tetto di tempo o per un kernel non avviato non vengono segnati; un compito già in ripresa conserva il suo conto. Esito: ok.
4. Idempotenza, `modules/notte/notte.py:252` — la NOTA_RIPRESA arriva nel prompt. Contesto: in `gas.py:2786` le azioni irreversibili passano comunque dalla firma, e una richiesta identica già in attesa viene riconosciuta come doppione, quindi nessun doppio invio. Il kernel scrive nel diario ogni tool call, perciò `ricorda` le vede. Resta un limite: la storia parziale del giro morto (`storia_<nome>.json`) non viene riletta, perché si riparte con `history=[]`. Le azioni reversibili ma non ripetibili senza danno (per esempio aggiungere in coda a un file di livello 1) dipendono solo da quanto il modello rispetta la nota. Esito: ok per una prima fetta; il limite va dichiarato.
5. Il cancello — `.gas_notte` è nell'elenco di livello 3 (`modules/gate/gate.py:300`), quindi il modello non può falsificare il registro con `write_file`. Esito: ok.
6. Con `solo` — la sonda conferma che un altro compito rimasto a metà («altro», tentativi 1) resta intatto nel registro. Esito: ok.
7. Telegram — gli avvisi di ripresa e di salto finiscono in `avvisi` e quindi nel messaggio completo. Nella versione ridotta (testo troppo lungo) resta solo il numero degli avvisi. Esito: ok.

**Finding**
- **R-406-1 (MEDIA)**, `modules/notte/notte.py:551` — un compito saltato perché supera MAX_TENTATIVI non alza l'exit code, a differenza del salto per tempo.
  - Sonda: `solo="lungo"` con tentativi=3 dà rc **0** e «compiti eseguiti: 0».
  - Il test `tests/test_unit_notte.py:1548` addirittura asserisce `== 0`.
  - Con `solo` l'operatore chiede esplicitamente quel compito e viene rifiutato con exit 0.
  - Correzione: contare il salto come esito ko (exit 1). Con `solo`, valutare se ignorare il tetto oppure almeno dare exit 1.
- **R-406-2 (BASSA)** — le voci di compiti tolti dal catalogo non si cancellano mai. La sonda «fantasma» resta dopo un giro completo; se quel nome torna nel catalogo, il compito riparte come «ripresa» con la nota e il vecchio conto. Correzione: nei giri senza `solo`, eliminare i nomi che non stanno nel catalogo.
- **R-406-3 (COSMETICA)**, `modules/notte/notte.py:646` — `esito_c["ripreso"]` non lo legge nessuno: riepilogo e Telegram usano solo gli avvisi. Va mostrato sulla riga OK/KO oppure tolto.

**Rischi esclusi**
- Suite del kernel (957) non rieseguita: il diff non tocca `gas.py`.
- Comportamento con un kill vero (SIGKILL o systemd) su VPS non verificato: il test lo simula con KeyboardInterrupt. La scrittura atomica con `os.replace` rende comunque improbabile un registro troncato.

**Memoria**: riga #406 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, con una lezione: un nuovo motivo di «salto» deve contare nell'exit code e nei conteggi come gli altri salti. Il file è committato con `scripts/commit_memoria_revisore.sh` (commit «chore(revisore): memoria review #406»); il resto dello staging è intatto.

Le riserve R-406-1/2/3 vanno tracciate in `reports/stato_progetto.md`.

---

### Review #407 (chat Motore) — commit d51de97

## VERDETTO: APPROVATO CON RISERVE

Review #407 (chat Motore): chiusura di R-406-1, R-406-2 e R-406-3. Prima di revisionare ho letto CLAUDE.md (sez. 5, 8, 9 e 10), le sezioni di reports/stato_progetto.md su R7 e notte, e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/notte/notte.py:541` — `_ordina_riprese` ora ritorna `(compiti, saltati)`.
  - Con `a_mano` il compito oltre MAX_TENTATIVI si rilancia come ripresa, con la nota «rilanciato a mano dopo N interruzioni».
  - Nel giro completo le voci che non sono nel catalogo si tolgono; con `solo` restano.
  - Rischi esaminati: conteggio del salto, voci di altri compiti toccate con `solo`, registro vuoto.
  - Esito: ok. `_leggi_in_corso` dà sempre un dict, quindi niente crash a registro vuoto o rotto. Il test r406 conferma che con `solo` la voce «altro» resta.
- `modules/notte/notte.py:677` — `if saltati_r7: return 1`, messo prima di `if not compiti`.
  - Rischio esaminato: salto che non alza l'exit code.
  - Esito: ok. Mutazione (return tolto) → falliscono 2 test (`test_r7_oltre_max_tentativi_saltato_e_azzerato` e `test_r406_unico_compito_saltato_exit_1`): i test discriminano.
- `modules/notte/notte.py:311` — il riepilogo mostra «— ripreso dopo un'interruzione». Esito: ok, chiude R-406-3.
- `tests/test_unit_notte.py:1615` — 3 test nuovi (a mano oltre il tetto, unico compito saltato → 1, voce fantasma tolta) e un'asserzione corretta a 1. Esito: ok.
- Contesto, `modules/notte/notte.py:346` (`componi_messaggio_telegram`): il messaggio Telegram mostra «ko: 0» e il salto solo tra gli avvisi, con exit 1. È lo stesso schema del salto per tetto di tempo, quindi è coerente; nessuna riserva.
- Riprodotto: notte 118 passed.

**Risposte alle domande**
- **Compito reso inattivo che perde la ripresa:** accettabile. Un compito disattivato di proposito non deve essere ripreso, e quando torna attivo riparte pulito senza la nota «ripresa». Con `solo` su un compito inattivo `compiti` resta vuoto, quindi niente potatura ed exit 1 col messaggio «non trovato».
- **Registro vuoto:** nessun crash. Provato anche con catalogo assente: rc 1.

**Finding**
- **R-407-1 (chat Motore) BASSA:** se il catalogo è assente o illeggibile, il giro completo azzera tutto il registro (lo stesso vale per la voce di un compito il cui prompt diventa invalido).
  - Sonda: registro `{"lungo": tentativi 2}` più catalogo inesistente → registro `{}`.
  - Un errore passeggero del catalogo cancella così i conteggi dei crash e la nota di ripresa.
  - Correzione: togliere le voci solo se il catalogo è stato letto senza avvisi di caricamento (o almeno non quando `catalogo_ko` è vero).
- **R-407-2 (chat Motore) COSMETICA:** la docstring di `esegui_notte` (`modules/notte/notte.py:580`) non elenca il salto per crash ripetuti tra i motivi dell'exit 1.

**Rischi esclusi**
- Suite del kernel (957) non rieseguita: gas.py non è toccato.
- Invio Telegram reale non verificato: non c'è il token in dev; ho verificato solo la composizione del messaggio leggendo il codice.
- Crash reale a metà compito (processo ucciso) non riprodotto: mi sono affidato ai test r7 con `_KCrash`.

Memoria aggiornata: riga #407 in /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione «una potatura condizionata al catalogo va fatta solo se il catalogo è stato letto bene». Committata da sola con lo script (commit 38e4240). Il diff staged è intatto: ho ripristinato il file della prova di mutazione e ho controllato che sia uguale all'originale.

---

### Review #408 (chat Motore) — commit bb9305e

## VERDETTO: APPROVATO CON RISERVE

Review #408 (chat Motore), diff staged su 4 file in /home/user/Gas. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le voci su R-404 e R-405) e la mia memoria.

**Cosa ho controllato nel diff**
- `modules/notte/notte.py:624`: `_ordina_riprese(..., pota=not avvisi)`. Rischio esaminato: un catalogo assente o rovinato cancellava il registro dei crash. Nel test r407 con `manca.yaml` i tentativi restano 2. Mutazione «pota ignorato»: 1 test fallisce, quindi il test distingue il caso. **ok**, con la riserva R-408-1.
- `modules/notte/notte.py:550`: docstring di `_ordina_riprese`. `modules/notte/notte.py:582`: docstring di `esegui_notte`, ora con il salto R7 tra i motivi dell'exit 1. **ok** (chiude R-407-2).
- `modules/gate/gate.py:740`: `read_file` negato se una qualsiasi forma di `_forme` dopo `_normalize_path(...).strip()` diventa "" o ".", e anche su ValueError (fail-closed). Prove a mano:
  - danno DENY: «./», «a/..», «./a/..», «.», «<U+0009>», «<U+200B>», «<U+3000>», «<U+00A0>», «..», «../x», "" e None;
  - restano SAFE: «README.md», «./README.md», «x/./y.md», «a b.md», «modules/»;
  - `cerca_testo` ed `elenca_cartella` su «.» o senza percorso restano SAFE.

  Mutazione «blocco tolto»: 6 test falliscono. **ok**, con la nota R-408-2.
- `modules/gate/gate.py:196`: la docstring di `_normalize_path` ora rimanda a `_invisibile`. **ok** (chiude R-405-2).
- `tests/test_unit_notte.py:761`: il test usa `LOCK_SH|LOCK_NB` al posto di `LOCK_EX`. Il rischio era che il test non distinguesse più i due casi. Mutazione: nel `finally` di `modules/notte/notte.py:695` ho messo `_notifica_telegram` PRIMA di `lock_f.close()`, e il test fallisce (lo `LOCK_SH` viene rifiutato perché il giro tiene ancora `LOCK_EX`). Quindi distingue ancora. In 25 run su 25 il test è verde. **ok** (chiude R-404-2).
- `tests/test_unit_gate.py:878`: test parametrizzato su 6 nomi vuoti o root. **ok**.

**Test che ho rilanciato:** gate+notte 936 passed, kernel 957 PASS e 0 FAIL. Dopo le mutazioni ho ripristinato i file (`git diff --stat` vuoto).

**Finding**
- **R-408-1 (chat Motore) BASSA**: `pota=not avvisi` spegne la potatura con QUALSIASI avviso, anche permanente (una voce malformata lasciata nel catalogo, o più compiti del tetto MAX_COMPITI). In quella configurazione le voci fantasma di R-406-2 non si tolgono mai, e se il nome torna ripartono come «ripresa». Per il caso del tetto non potare è anzi corretto. La correzione: potare solo se il FILE del catalogo è stato letto, distinguendolo dagli avvisi sulle singole voci.
- **R-408-2 (chat Motore) COSMETICA**: `read_file` su «.» o «./» ora dà DENY. Prima dava SAFE e poi l'errore «è una cartella», un messaggio più chiaro per il modello. Inoltre `lettura_consentita("<U+200B>")` resta True mentre `read_file` nega: le due regole sono allineate solo a metà, ma senza effetti pratici.

**Cosa NON ho verificato**
- Come il kernel mostra al modello un DENY di `read_file` su «.» dal vero: non ho fatto un round-trip agentico con un modello reale, solo `gate_classify` e la suite del kernel.
- Il comportamento di flock su filesystem diversi da quello locale del container (NFS, VPS): non riproducibile qui.

Memoria aggiornata con la riga #408 e committata (5756a04) in `/home/user/Gas/.claude/agents/memoria_revisore.md`.

---

### Review #409 (chat Motore) — commit 6f6edd7

## VERDETTO: APPROVATO CON RISERVE

Review #409 (chat Motore). Diff staged: gas.py, tests/test_unit_kernel.py. Ho letto CLAUDE.md, la parte di stato_progetto.md che riguarda il budget (R-293-1 e R-tel-budget-perf) e memoria_revisore.md. Ho rilanciato la suite del kernel: 959 PASS, 0 FAIL.

**Elementi esaminati**
- `gas.py:1183` — `_daily_cost_usd` ora legge solo le righe nuove. Rischio controllato: righe saltate per un offset sbagliato, cioè un kill-switch che sottostima. Ho fatto una sonda differenziale: 300 semi casuali × 8 aggiunte, con righe spezzate a metà, fallthrough, righe rotte, byte non UTF-8, `ts` null, righe-lista, `in`/`out` non interi. In tutti i 2400 casi la lettura a pezzi dà lo stesso costo della lettura da capo. Esito: ok.
- `gas.py:1214` — si consumano solo le righe complete (`rfind(b"\n")`, poi offset spostato di `fine + 1`). Rischio: una riga a metà scritta da un altro processo (bot + notte). `_log_tokens` (`gas.py:1178`) scrive ogni riga con un solo `write` in modalità append, quindi una riga a metà resta in attesa e si rilegge. Anche il caso in cui il file cresce tra `stat` e lettura è coperto, perché si legge fino a `st_size`. Esito: ok.
- `gas.py:869` — `_costo_riga`, equivalenza con HEAD. Rispetto a prima il nuovo codice è **più** robusto. HEAD apriva il file in UTF-8 stretto: una sola riga non UTF-8, una riga che non è un oggetto JSON o un `ts` null facevano sollevare un'eccezione, e il costo dell'intero file diventava 0.0. Era una sottostima grave già presente, che il diff chiude (la sonda lo mostra: HEAD 0.0, nuovo 3.5 e oltre). La domanda su «in» non intero ha una risposta sotto (R-409-1).
- `gas.py:1206` — condizioni che fanno rileggere da capo: inode diverso, file più corto, inizio cambiato, stessa lunghezza con mtime diverso. Rischio: file riscritto sul posto. Esito: riserva R-409-2.
- `gas.py:866` — `_COSTI_CACHE` per percorso. Più kernel nello stesso processo condividono la voce in cache, e questo va bene: lo stato dipende solo dal file. Thread: l'unico `ThreadPoolExecutor` (`modules/telegram/bot.py:256`) fa solo gli invii `sendMessage`, nessuna chiamata concorrente al costo. Memoria: si tengono solo le voci delle ultime 24 ore. Esito: ok (con R-409-3).
- `tests/test_unit_kernel.py:7090` e `tests/test_unit_kernel.py:7099` — T94a/T94b coprono riga a metà, fallthrough, riga rotta, riga più vecchia di 24 ore, file accorciato, file cancellato (cache tolta). Esito: ok, ma il caso di R-409-2 non è coperto.

Wall of Shame: nessuno slicing della history, nessun output di tool simulato. Fail-safe §9 rispettato: eccezione → `logging.warning` e 0.0. Guardrail (cap 10 iterazioni, `_get_window`) non toccati.

**Finding**
- **R-409-1 (BASSA)** — Risposta alla domanda su «in» non intero: l'effetto **non** è identico. In HEAD la somma avveniva in due passi. Una riga con `in` valido e `out` non intero contava quindi la parte `in`; adesso la riga vale 0. La sonda lo conferma (905 casi «nuovo < vecchio», tutti da `out="abc"`). Se invece è `in` a non essere intero, l'effetto è lo stesso (la riga non conta). Il caso è irraggiungibile da `_log_tokens`, che scrive sempre `int(...)`. Se si vuole l'equivalenza stretta, calcolare la parte `in` e la parte `out` separatamente.
- **R-409-2 (BASSA)** — File riscritto sul posto, più lungo del precedente, con i primi 64 byte uguali (stesso secondo e stesso provider). La lettura riparte dal vecchio offset e tiene le voci vecchie. Sonda: risultato 0.2 invece di 0.3, quindi una sottostima. Nessun codice riscrive questo log, può succedere solo a mano. Rimedio economico: salvare anche un'impronta dei byte che finiscono all'offset (es. gli ultimi 64) e rileggere da capo se non coincidono. Aggiungere un test.
- **R-409-3 (BASSA)** — Alla prima lettura (o dopo una rilettura da capo) tutto il file finisce in memoria con `f.read`, e tutte le voci vengono accodate prima del filtro delle 24 ore. È un picco transitorio: HEAD leggeva in streaming. Rimedio: scartare le voci più vecchie del limite mentre si accodano, ed eventualmente leggere a blocchi.

**Cosa NON ho verificato**
- Il comportamento con più processi davvero concorrenti sul Mac o sulla VPS (bot e notte che scrivono insieme sullo stesso file). L'ho valutato solo leggendo il codice di `_log_tokens`, perché in questo ambiente non si riproduce.
- I tempi della sonda dichiarata (482 ms la prima lettura, 12 ms la seconda) non li ho rimisurati.
- Non ho fatto prove di mutazione sui controlli di mtime e di inizio file. Da quanto si legge nei test, T94 non li esercita direttamente.

Memoria aggiornata con la riga #409 e la lezione. Commit `6a16311` fatto con `scripts/commit_memoria_revisore.sh`. File: /home/user/Gas/.claude/agents/memoria_revisore.md. Script delle sonde: /tmp/claude-0/-home-user-Gas/44c5231e-90cf-40cb-8216-3ee48596875d/scratchpad/sonda.py e /tmp/claude-0/-home-user-Gas/44c5231e-90cf-40cb-8216-3ee48596875d/scratchpad/s2.py.

---

### Review #410 (chat Motore) — commit 7e9900c

## VERDETTO: APPROVATO CON RISERVE

Review #410 (chat Motore). Il diff staged è in /home/user/Gas. Prima di cominciare ho letto CLAUDE.md, le righe utili di reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/notte/notte.py:291` — `al_termine()` viene chiamato dopo il `finally` che chiude il turno e prima della riflessione e del diario. Rischi esaminati: (1) un'eccezione dentro `al_termine`; (2) un crash del turno che non deve togliere il compito dal registro. Esito: ok.
  - Un'eccezione dentro `al_termine` viene presa e scritta come warning.
  - Se il `KeyboardInterrupt` arriva dentro `run_turn`, `al_termine` non viene chiamato e il compito resta nel registro. È il comportamento giusto: è un crash vero, quindi il compito va ripreso.
  - Anche il turno interrotto per tempo scaduto (`break`) passa da `al_termine`. È coerente con R7: ko e tempo scaduto non sono crash.
- `modules/notte/notte.py:673` — la closure `_finito(nome=c["nome"])` usa un default argument, quindi il nome viene fissato al giro giusto del ciclo e non a quello successivo. Rischio esaminato: scrittura doppia del registro. Esito: ok.
  - La rete di sicurezza in `modules/notte/notte.py:681` scatta solo se il nome è ancora nel registro, quindi nel caso normale c'è una sola scrittura.
  - `_scrivi_in_corso` (`modules/notte/notte.py:542`) non solleva mai eccezioni.
  - Caso limite, già presente prima: se la scrittura fallisce, il nome è già tolto in memoria e la rete di sicurezza non riscrive il file. Non è peggiorato rispetto a prima.
- `modules/notte/notte.py:536` — controllo `type(t) is int and 0 < t <= 1000`. Rischio esaminato: valori bool o enormi nel registro. Esito: ok. Il tetto di 1000 è molto sopra MAX_TENTATIVI, quindi non scarta voci legittime. Test parametrizzati con `true` e con 10^30.
- `gas.py:1211` — impronta della coda (gli ultimi 64 byte prima dell'offset). Rischio esaminato: che la coda calcolata a pezzi diverga da quella letta dal file. Esito: ok.
  - Con una riga a metà (`fine < 0`) né l'offset né la coda si muovono.
  - Dopo una rilettura da capo la coda riparte da `b""` e si ricompone come `(coda + nuovo[:fine+1])[-64:]`. Questo coincide con `file[max(0, off-64):off]`, che è ciò che si rilegge con `seek`/`read(min(64, off))`.
  - Con offset 0 entrambe le code sono vuote.
- `gas.py:883` — «in» e «out» vengono contati separatamente (R-409-1). Esito: riserva (R-410-1).
- `gas.py:1232` — il filtro sulle 24 ore si applica già mentre si leggono le voci (R-409-3). Esito: ok. Il risultato è equivalente al filtro finale, che resta.
- `tests/test_unit_notte.py:1667` e `tests/test_unit_kernel.py:7103` — i test nuovi. Esito: ok, discriminano davvero (mutazioni sotto).

**Prove riprodotte**
- Test: notte 122 passed, kernel 960 PASS e 0 FAIL.
- Mutazioni, fatte in un worktree già rimosso:
  - `al_termine=None` → fallisce `test_v1_bot234_registro_tolto_prima_della_riflessione`.
  - controllo `coda != c["coda"]` tolto → fallisce T94c (0.1 invece di 0.3).
- Sonda differenziale `/tmp/claude-0/-home-user-Gas/44c5231e-90cf-40cb-8216-3ee48596875d/scratchpad/sonda.py`: 300 semi × 8 aggiunte, con righe spezzate e righe rotte. La lettura a pezzi dà lo stesso totale della lettura da capo in tutti i 2400 casi. Rispetto a HEAD il nuovo non è mai più basso; è più alto in 1480 casi, cioè le righe con «out» rotto, ora contate per la parte «in».
- Sonda nuova `/tmp/claude-0/-home-user-Gas/44c5231e-90cf-40cb-8216-3ee48596875d/scratchpad/s3.py`: 18000 casi tra aggiunte spezzate, riscritture sul posto più lunghe con la stessa testa e un byte cambiato a parità di lunghezza. Nessuna differenza rispetto alla lettura da capo.

**Riserve**
- **R-410-1 (chat Motore), BASSA** — in `gas.py:883` un numero enorme (`1e400` oppure 10**400) provoca un `OverflowError`. L'`except (TypeError, ValueError)` interno non lo prende, quindi la riga intera viene scartata e anche un «in» valido va perso (sonda: `None`). È la stessa incoerenza che R-409-1 voleva chiudere. Non si raggiunge da `_log_tokens`. Rimedio: aggiungere `OverflowError` all'except interno.
- **R-410-2 (chat Motore), BASSA, già presente prima** — valori negativi di «in» o «out» abbassano la spesa calcolata (sonda: -1.9 USD) e quindi indeboliscono il blocco del budget giornaliero. Succede solo con un log scritto a mano. Rimedio: `max(0, …)` sui conteggi.
- **Limite dichiarato** — una riscrittura sul posto, più lunga, che conserva sia i primi 64 byte sia i 64 byte prima dell'offset non viene rilevata. Vale come limite noto: nessun codice riscrive il log.

**Rischio escluso** — non ho verificato il comportamento con scritture concorrenti al log (più processi di Gas che aggiungono righe mentre il file viene letto tre volte, tra stat, testa e coda): in dev non si riproduce in modo deterministico. Le aggiunte non toccano i byte prima dell'offset, quindi il rischio atteso è basso. Non ho verificato nemmeno sulla VPS.

**Memoria** — riga #410 e lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (3ef6572). Il diff staged sotto review è intatto.

---

### Review #411 (chat Motore) — commit 4227270

## VERDETTO: APPROVATO CON RISERVE

Review #411 (chat Motore): chiusura di R-410-1 e R-410-2. Ho letto CLAUDE.md, stato_progetto.md e la mia memoria (ultime righe: #406-#410).

**Elementi del diff esaminati**
- `gas.py:885`: ora ogni conteggio passa da `max(0, int(r.get(chiave, 0)))`. Ho controllato se un valore negativo può ancora abbassare la spesa del budget giornaliero. Sonde con «out» -3, "-7" e -1e400: la parte «in» (0.1) viene tenuta e quella negativa conta 0. Con la mutazione (max tolto) T94d va in FAIL, quindi il test distingue il caso. Esito: ok.
- `gas.py:886`: l'except interno ora prende anche OverflowError. Ho controllato se un numero enorme fa ancora perdere la parte «in» valida. Sonde con «out» 1e400, Infinity, NaN e 10**400 danno tutte 0.1, quindi «in» resta. Con «out» 1e300 il costo è 4e293: è una sovrastima, cioè va nel verso sicuro (il blocco di spesa del budget scatta). Esito: ok.
- `tests/test_unit_kernel.py:7118`: T94d, due casi (negativo ed enorme). Ho controllato se il test discrimina entrambe le correzioni. Il primo caso sì: con il codice vecchio dà -0.3 e quindi FAIL. Il secondo, se si toglie OverflowError, fa restituire None a `_costo_riga`, e `[1]` lancia TypeError: l'intera suite si interrompe invece di dare FAIL. Esito: riserva R-411-1.
- Contesto: `gas.py:869`. L'except esterno resta, per cui la funzione non lancia mai eccezioni: la regola «zero crash» è rispettata.

Wall of Shame: nessuno slicing della history e nessuna simulazione di output dei tool. Il cap delle 10 iterazioni, `_get_window` e il cap di output non sono toccati. Ho riprodotto la suite del kernel: 961 PASS, 0 FAIL. Dopo le mutazioni ho ripristinato gas.py: `git diff` non staged è vuoto e lo staged è invariato (2 file, +9/-2).

**Finding**
- R-411-1 (chat Motore), BASSA: T94d prende `[1]` dal risultato di `_costo_riga` senza controllare che non sia None. Se R-410-1 torna indietro, il test non dà FAIL ma interrompe tutta la suite. La CI diventa rossa comunque, però i check successivi non girano e il messaggio non nomina T94d. Rimedio: controllare `is not None` prima di indicizzare.
- R-411-2 (chat Motore), BASSA: un conteggio enorme (10**400 intero oppure inf) conta 0 invece di essere trattato come spesa massima, quindi la spesa viene sottostimata. Non può succedere tramite `_log_tokens`, che scrive interi piccoli: solo con un log scritto a mano.

**Rischio escluso**: non ho verificato il comportamento su un log reale della VPS né l'effetto sul blocco di spesa del budget a valle con costi 1e293. Il primo non è riproducibile in dev; il secondo ricade nel verso sicuro (il budget si blocca).

**Memoria**: aggiunta la riga #411 con la lezione «un test che indicizza un ritorno che può essere None deve fallire con FAIL, non con un'eccezione che ferma la suite». Committata con `scripts/commit_memoria_revisore.sh` (solo quel file, 1 inserimento).

File: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 957 → 961 PASS, 0 FAIL (T94a-d). Blocco reale: `=== RIEPILOGO: 961 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py`: 106 → `122 passed`; `tests/test_unit_gate.py`: 811 → `817 passed`.

## §6 STATO CI

- 5267148 (con 6eaab53, d51de97, bb9305e e memorie): handoff-check success, unit-suite success, verifica-bot neutral (verdetto APPROVATO CON RISERVE, decide l'operatore) — dal verdetto del bot e dalla verifica esterna #234, e dall'evento check_suite.completed sulla PR.
- 6f6edd7, 7e9900c, 4227270 e memorie: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-408-1 (BASSA): potatura del registro spenta da qualsiasi avviso del catalogo.
- R-408-2 (COSMETICA): read_file su «.» negato invece di «è una cartella».
- Limite dichiarato (#406): la ripresa riparte da capo con la nota, non rilegge la storia parziale del compito.
- R-411-1 (BASSA): T94d interrompe la suite invece di dare FAIL se torna R-410-1.
- R-411-2 (BASSA): conteggio enorme scritto a mano conta 0.
- V-3 verifica esterna #234 (BASSA, dichiarata): un Ctrl-C dell'operatore conta come crash.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
