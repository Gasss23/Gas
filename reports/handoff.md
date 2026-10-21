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
- **R7 R-fts-1 — tetto alle parole delle ricerche**: `FATTA` — review #412 APPROVATO CON RISERVE (solo statica, disco temporaneo pieno).
- **Budget: ts non validi/futuri, riga senza a capo, gas tokens (V-2 bot #234, V-1 verifica #234, R-411-1, R-413-1/2)**: `FATTA` — review #413, #414 APPROVATO CON RISERVE.
- **Test che riempivano /tmp, cache modello, avviso «ripreso» (R-415-1/2, R-416-1, V-2 bot #234)**: `FATTA` — review #415, #416, #417 APPROVATO CON RISERVE.
- **Ordine delle riprese (V-1 bot #234)**: `FATTA` — review #418 APPROVATO CON RISERVE (limite dichiarato R-418-3).
- **C6**: `SALTATA` — decisione dell'operatore.
- **R7 — ripresa dal punto esatto**: `DEFERITA` — da valutare.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  14 ++++++
 gas.py                             | 130 ++++++++++++++++++++++++++++++++++++++++++++-----------
 modules/gate/gate.py               |  12 +++++-
 modules/memory/store.py            |  21 ++++++++-
 modules/notte/notte.py             | 134 ++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/da_mergiare.md             |  99 ++++++++++++++++--------------------------
 reports/diff_sessione.md           |  17 ++++----
 reports/handoff.md                 | 842 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  43 +++++++++----------
 tests/test_unit_gate.py            |   8 ++++
 tests/test_unit_kernel.py          | 118 +++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_notte.py           | 243 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 13 files changed, 1076 insertions(+), 607 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
d9f58bb fix(notte): compito ripreso già fallito 2+ volte va in coda, dopo gli altri (V-1 bot #234)
632ca76 chore(revisore): memoria review #418 — APPROVATO CON RISERVE
01bf064 docs(fine-task): report, handoff, coda da_mergiare — test che non riempiono /tmp (#415-#417)
f2c3e29 fix(notte): avviso «ripreso» anche nella scatola nera (R-416-1)
0187872 chore(revisore): memoria review #417 — APPROVATO CON RISERVE
5999fdb fix: cache del modello dei test stabile tra le esecuzioni, pulizia delle cartelle di esecuzioni uccise; avviso «ripreso» solo quando il compito parte (R-415-1/2, V-2 bot #234)
59374ed chore(revisore): memoria review #416 — APPROVATO CON RISERVE
3a43d93 test(kernel): cartelle temporanee della suite in una sola cartella per esecuzione, cancellata alla fine (riempivano /tmp: ~430 per run)
3892c08 chore(revisore): memoria review #415 — APPROVATO CON RISERVE
0a11a8b docs(fine-task): report, handoff, coda da_mergiare — budget robusto (#413, #414), pulizia disco
5142d8f fix(budget): ultima riga senza a capo contata; date finte o future ignorate; gas tokens regge un ts null (V-1 verifica #234, R-413-1/2)
c10726e chore(revisore): memoria review #414 — APPROVATO CON RISERVE
a86f493 fix(budget): riga del registro dei token senza data valida ignorata, mai «per sempre nelle 24 ore» (V-2 bot #234, R-411-1)
9400261 chore(revisore): memoria review #413 — APPROVATO CON RISERVE
2d07cd3 docs(fine-task): report, handoff, coda da_mergiare — tetto parole ricerche (R-fts-1)
ab60f35 fix(memoria): tetto di 12 parole distinte (max 40 caratteri) alle ricerche nel diario e nella conoscenza (R-fts-1, roadmap R7)
f682cc0 chore(revisore): memoria review #412 — APPROVATO CON RISERVE
9d793f3 docs(fine-task): report, handoff, coda da_mergiare — spesa incrementale, correzioni #234
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

### Review #412 (chat Motore) — commit ab60f35

## VERDETTO: APPROVATO CON RISERVE

Review #412 (chat Motore). La review è solo statica. Bash non funziona: ogni comando fallisce con ENOSPC, perché il tmp della sessione è pieno. Anche la scrittura di `.claude/agents/memoria_revisore.md` è fallita (ENOSPC). Quindi non ho rieseguito né sonde né suite: i numeri «Kernel 962 PASS» e «pytest 27 passed» vengono dal brief, non li ho rifatti io.

Ho letto CLAUDE.md (testo integrale nel contesto), le voci R7/R-fts in reports/stato_progetto.md e le ultime voci della memoria (#407-#411).

Elementi del diff esaminati:
- `modules/memory/store.py:525` — `_token_fts`: tronca a 40 caratteri, poi toglie le parole doppie e si ferma a 12 parole distinte.
  - Rischi esaminati: lista vuota (dà [], poi «nessuna ricerca» come prima), parole doppie che nascono dal troncamento (deduplicate dopo il taglio, corretto), taglio a metà carattere (lo slicing di str lavora su codepoint, nessun problema).
  - Esito: ok.
- `modules/memory/store.py:1090` — `_fts_match` del diario, in AND implicito.
  - Rischio esaminato: qualità della ricerca. Con meno parole in AND i risultati sono un sovrinsieme di quelli di prima (più larghi), mai un errore. Il prefisso da 40 caratteri con «*» è più largo della parola intera.
  - Le parole contengono solo caratteri \w, quindi le virgolette non si possono rompere e la sintassi FTS5 resta valida. Il tokenizer è unicode61 di default (`modules/memory/store.py:603`).
  - Se la ricerca FTS non trova nulla, `ricorda` ricade sulla ricerca per sottostringa (`modules/memory/store.py:1100`), che non è cambiata.
  - Esito: ok.
- `gas.py:3578` — import pigro di `_token_fts`, un nome privato del modulo memoria.
  - Rischio esaminato: ImportError che fa crashare la ricerca nella conoscenza. È escluso: `modules.memory` è già importato a livello di modulo in `gas.py:20`, quindi se mancasse fallirebbe prima l'avvio del kernel. L'import pigro non aggiunge nuovi punti di crash.
  - Nome privato usato fuori dal modulo: accettabile, accoppiamento dichiarato nel commento.
  - Esito: ok.
- `gas.py:3597` — il chiamante (`_knowledge_search`) gestisce già il ritorno '' come «saltata», solo nel log.
  - Esito: ok.
- `tests/test_unit_kernel.py:7123` — T95.
  - Esito: riserva (R-412-2).

Guardrail: `_get_window`, il tetto di 10 iterazioni e il pin della memoria non sono toccati. Nessuno slicing della storia, nessuna simulazione dell'output dei tool.

Finding:
- **R-412-1 (chat Motore) BASSA**: si tengono le PRIME 12 parole. Nella conoscenza (OR, parole di almeno 3 caratteri) una domanda lunga perde le parole chiave in coda, che spesso sono il tema. Inoltre le parole vuote («che», «della», «per») occupano posti. Nel diario la regex è `\w+`, quindi contano anche «a» ed «e». Prima di questo diff nessuna parola andava persa. Rimedio da valutare: filtrare le stopword oppure preferire le parole più lunghe.
- **R-412-2 (chat Motore) COSMETICA**: nella metà diario di T95 il tetto delle 12 parole scatta prima di «parola0» doppia e della parola da 100 caratteri. Quindi parole doppie e troncamento sono provati solo sulla metà conoscenza. Manca anche una prova con un MATCH reale su SQLite e un prefisso da 40 caratteri.

Rischi esplicitamente esclusi:
- Mutazioni, esecuzione di T95 e suite kernel/pytest: non riprodotte, perché Bash è inutilizzabile (ENOSPC).
- Comportamento su VPS: non verificato.
- Qualità del ranking BM25 su dati reali: non misurata.

(Nota dell'agente principale: la riga di memoria #412 dettata dal revisore è stata aggiunta dall'agente principale dopo aver liberato il disco, commit f682cc0; suite kernel rieseguita dall'agente principale: 962 PASS, 0 FAIL.)

---

### Review #413 (chat Motore) — commit a86f493

## VERDETTO: APPROVATO CON RISERVE

Review #413 (chat Motore). Ho letto: CLAUDE.md (sez. 5, 8, 9, 10), le parti utili di reports/stato_progetto.md e la memoria del revisore (comprese le righe da #408 a #412).

**Elementi del diff esaminati**
1. `gas.py:867`: è la regex `_TS_LOG_RE`, con lo stesso formato di `_log_tokens` (`gas.py:1181`, strftime `%Y-%m-%dT%H:%M:%S`) e del cutoff (`gas.py:1213`). Ho controllato che i formati coincidano: il confronto tra stringhe resta corretto. Esito: ok.
2. `gas.py:892`: il ts viene accettato solo se è una str e la regex combacia per intero (fullmatch). Le ho provate così:
   - vengono ignorati: None, «None», «domani», 5, ts assente, «2026-10-21», «…Z», «….5», «…\n» finale;
   - viene tenuto: il ts reale di `_log_tokens`.
   Il `try/except Exception → None` resta, quindi nessun nuovo punto di crash (§9). Esito: ok. C'è una riserva, vedi R-413-1.
3. `tests/test_unit_kernel.py:7118`: T94d ora controlla `is not None` prima di indicizzare. Con una regressione dà FAIL invece di fermare la suite: R-411-1 è chiusa. Esito: ok.
4. `tests/test_unit_kernel.py:7127`: T94e prova sei ts non validi e uno valido. Mutazioni, fatte su una copia nello scratchpad poi cancellata:
   - controllo tolto del tutto: T94e FAIL (962/1);
   - controllo ridotto al solo `isinstance`: T94e FAIL (962/1).
   Il test distingue davvero il fix. Esito: ok.

Ho rifatto girare la suite del kernel sulla versione staged: 963 PASS, 0 FAIL. Non ci sono slicing della history né simulazioni di tool; `_get_window`, il tetto di 10 iterazioni e quello degli 8k non sono toccati.

**Riserve**
- **R-413-1 (BASSA)**: `\d` accetta anche le cifre Unicode, e la regex non controlla che la data esista.
  - Sonda: «<U+FF12><U+FF10><U+FF12><U+FF16>-<U+FF11><U+FF10>-<U+FF12><U+FF11>T<U+FF11><U+FF10>:<U+FF10><U+FF10>:<U+FF10><U+FF10>» e «9999-99-99T99:99:99» vengono accettati, e vale lo stesso per qualunque ts futuro. Come stringa restano sempre ≥ cutoff, quindi il budget può restare bloccato per sempre, lo stesso effetto di V-2.
  - Succede solo con un log scritto a mano: `_log_tokens` non può produrli.
  - Rimedio: `re.ASCII` oppure `[0-9]`, poi `strptime`, e scartare i ts oltre l'ora attuale più un margine.
- **R-413-2 (BASSA, preesistente, fuori dal diff)**: in `gas.py:4687` `tokens_cmd` fa `r.get("ts", "") >= cutoff`. Con `"ts": null` nel log il comando `gas tokens` si ferma con TypeError (None >= str); l'ho riprodotto con un log di una riga. Non tocca il loop del kernel.

**Cosa non ho verificato**
- Il comportamento su VPS o sul Mac con un `.gas_tokens.jsonl` reale e grande, e i tempi: non riproducibili qui.
- Il percorso di `_daily_cost_usd` con la cache già piena di voci vecchie del formato precedente: ho controllato solo per lettura che il filtro `gas.py:1244` lavori sulle stesse tuple.

**Note operative**
- Il repo reale non è stato toccato oltre alla memoria: niente checkout, l'index staged è intatto.
- La memoria è aggiornata (riga #413 con la lezione) e committata da sola con `scripts/commit_memoria_revisore.sh`: commit 9400261 sul branch feat/merge-automatico-z1xjx2.

File: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

### Review #414 (chat Motore) — commit 5142d8f

## VERDETTO: APPROVATO CON RISERVE

Review #414 (chat Motore), sul diff staged in /home/user/Gas (gas.py, tests/test_unit_kernel.py). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9), reports/stato_progetto.md (in modo selettivo) e .claude/agents/memoria_revisore.md (le lezioni e le righe da #409 a #413).

**Elementi del diff esaminati**
- gas.py:1262 — la riga finale senza «\n» viene contata solo nel totale e non entra in cache, e l'offset non si sposta. Rischi esaminati: doppio conteggio quando arriva il «\n»; una coda che contiene «\n»; un JSON a metà scritto da un processo concorrente. Sonda: 0.3 prima del «\n» e 0.3 dopo, quindi la riga è contata una volta sola. Il caso «coda con \n» non può capitare: dopo il blocco principale l'offset sta subito dopo l'ultimo «\n», e la guardia `b"\n" not in resto` lo esclude comunque. Un prefisso di riga non è JSON valido, perché la «}» finale c'è solo a riga completa. Le eccezioni restano dentro il try/except con warning (§9). — ok
- gas.py:870 — `_ts_log_valido`: cifre ASCII, data vera con `strptime` (anche il secondo 60 dà ValueError, che viene preso), niente ts oltre ora+1h. Rischio esaminato: un ts appena scritto da `_log_tokens` (gas.py:1194, UTC, stesso formato) deve passare. Sonda: adesso e +59 minuti accettati, +61 minuti scartato. `timedelta` è importato a livello di modulo (gas.py:15), quindi niente NameError silenzioso che azzererebbe il budget. — ok
- gas.py:4711 — `tokens_cmd` con un ts non stringa: `is_recent` diventa False e il comando non si ferma più. — ok
- tests/test_unit_kernel.py:7087 — T94a con la coda senza «\n», poi il «\n» che arriva; T94e con cifre a larghezza piena, 9999-99-99 e 2999; T94f con «"ts": null». — ok, salvo R-414-3
- Contesto: gas.py:1209 `_daily_cost_usd`: la cache filtra solo con `cutoff`, il filtro sul «futuro» si applica solo in lettura (vedi R-414-1).

**Riproduzioni**: suite kernel **964 PASS, 0 FAIL**, rifatta su una copia nello scratchpad. Sonde (script /tmp/claude-0/-home-user-Gas/44c5231e-90cf-40cb-8216-3ee48596875d/scratchpad/sonda.py) con i risultati riportati sopra. In più, una coda da 5 MB senza «\n»: 20 chiamate in 0,13 s.

**Finding**
- **R-414-1 (chat Motore) BASSA**: se l'orologio torna indietro di più di 1 ora (correzione NTP sulla VPS), le voci già in cache restano contate. Rilette da capo, per esempio dopo un riavvio, vengono scartate come «future». Risultato: spesa sottostimata e kill-switch del budget più debole. Sonda: 0.15 con la cache, 0 dopo la rilettura. È il prezzo dichiarato per evitare un blocco permanente. Va almeno scritto nel commento di `_ts_log_valido`, oppure va riapplicato il filtro anche alle voci in cache, così il comportamento è lo stesso nei due casi.
- **R-414-2 (chat Motore) BASSA**: una coda senza «\n» viene riletta intera a ogni chiamata, e due volte: nel blocco principale e nel blocco nuovo. Non c'è un tetto, quindi una coda spazzatura enorme costa I/O a ogni turno (misurato: trascurabile a 5 MB). Rimedio: riusare `nuovo[fine+1:]` quando è già stato letto, e saltare le code oltre una soglia, per esempio 64 KB, che non possono essere una riga di `_log_tokens`.
- **R-414-3 (chat Motore) COSMETICA**: il messaggio di T94a non stampa `_c94c2`, quindi un fallimento del caso nuovo non mostra il valore. C'è anche un difetto preesistente: con la lista vuota `_daily_cost_usd` restituisce l'intero 0 invece di 0.0.

**Escluso / non verificato**
- **Mutazioni NON verificate.** Le ho lanciate su una copia: coda tolta, futuro tolto, `strptime` ignorato, `isinstance` tolto in `tokens_cmd`. Però il filtro grep era sbagliato: prendeva anche le righe PASS che contengono «Error» e con `head -5` le righe FAIL sono rimaste tagliate fuori. Poi il disco è finito pieno (ENOSPC). Quindi non so se T94a, T94e e T94f mordono davvero.
- **Disco pieno.** /tmp occupa circa 30 GB, in gran parte cartelle `gas_test_*` lasciate dalle suite, comprese le mie 5 esecuzioni. Ho tentato di cancellare quelle dei miei run, ma il classificatore dei permessi ha negato l'operazione. **Va liberato lo spazio prima del prossimo run di test o commit**: va fatto dall'operatore o dall'agente principale, con il permesso.
- Il comportamento con un vero salto dell'orologio di sistema è stato provato solo simulando `datetime.now`.

Copia nello scratchpad cancellata. Nel repo reale ho toccato solo la memoria. Riga contatore #414 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (c10726e). Lezione nuova: nei run di mutazione filtrare solo `^\[FAIL\]|RIEPILOGO` e controllare prima lo spazio su /tmp, perché la suite lascia cartelle `gas_test_*`.

---

### Review #415 (chat Motore) — commit 3a43d93

## VERDETTO: APPROVATO CON RISERVE

Review #415 (chat Motore), sul diff staged: solo tests/test_unit_kernel.py, +11 righe in testa al file.

Prima della review ho letto CLAUDE.md (già nel contesto), reports/stato_progetto.md (solo le parti che servivano: la voce «Da fare» sulla pulizia di /tmp e R-414) e la coda di .claude/agents/memoria_revisore.md.

**Cosa ho esaminato**
- `tests/test_unit_kernel.py:21` — crea una cartella `gas_kernel_run_*` per esecuzione e ci punta `tempfile.tempdir`. Rischio esaminato: uno dei `mkdtemp` successivi esce lo stesso in /tmp. Esito: ok. L'override viene prima di `import gas` e di tutti i `mkdtemp`, e copre anche `gas.py:1590` (snapshot).
- `tests/test_unit_kernel.py:23` — imposta `TMPDIR` per i sottoprocessi. Rischio esaminato: rompe il sandbox bwrap o le cartelle di lavoro temporanee di T93a2/T93a3. Esito: ok. bwrap fa ro-bind di `/` e maschera solo `/home`, `/root` e `/run` (`gas.py:1721`), quindi /tmp non è mascherato e una root sotto la cartella di esecuzione si comporta come prima. Su copia: 964 PASS e 0 FAIL.
- `tests/test_unit_kernel.py:24` — registra con `atexit` lo `shutil.rmtree` con errori ignorati. Rischio esaminato: la pulizia non parte. Esito: ok. Il `sys.exit` finale (`tests/test_unit_kernel.py:9978`) e le eccezioni non gestite fanno partire `atexit`, e nel file non c'è nessun `os._exit`. In CI (`.github/workflows/ci.yml:97`) il codice di uscita resta quello del `sys.exit`. Il file è escluso dalla raccolta di pytest (`tests/conftest.py:6`, `collect_ignore`), quindi l'override non tocca le altre suite.
- `tests/test_unit_kernel.py:1829` — T30e mette la cache del modello sotto `gettempdir()`. Rischio esaminato: una cache che deve restare tra un'esecuzione e l'altra ora vive nella cartella per esecuzione. Esito: riserva (R-415-1).
- `tests/test_unit_kernel.py:5501` — T73e toglie la scrittura a una cartella (`chmod 0o500`). Rischio esaminato: `rmtree` non riesce a cancellarla e la cartella resta. Esito: ok, il permesso viene ripristinato nel `finally`.

**Riproduzione** (copia nello scratchpad, poi cancellata): `df -h /` prima e dopo con 28 GB liberi. Suite kernel: 964 PASS, 0 FAIL in 35 s, rc 0. /tmp prima e dopo identico: 0 voci nuove. T30e risulta SKIP in questo ambiente perché manca la rete per i pesi del modello.

**Finding**
- **R-415-1 (chat Motore) MEDIA**: T30e (`tests/test_unit_kernel.py:1829`) tiene la cache del modello in `gettempdir()/gas_vec_model_cache`, e il commento la dichiara «STABILE: scarica una volta sola». Ora quel percorso è dentro la cartella per esecuzione, quindi su una macchina con rete (il Mac dell'operatore) il modello, che pesa centinaia di MB, viene riscaricato e cancellato a ogni esecuzione. La CI non cambia, perché ogni run parte comunque senza cache. Correzione: salvare `tempfile.gettempdir()` PRIMA dell'override (es. `_TMP_SISTEMA`) e usarlo per `cache_real`.
- **R-415-2 (chat Motore) BASSA**: se il processo viene ucciso (SIGKILL), terminato con SIGTERM o fermato dal timeout della CI, `atexit` non parte e resta una cartella `gas_kernel_run_*` intera. Una sola per esecuzione: accettabile rispetto alle ~430 di prima, ma nessuno ripulisce le vecchie. Rimedio facoltativo: all'avvio togliere le `gas_kernel_run_*` più vecchie di qualche ora.
- **R-415-3 (chat Motore) COSMETICA**: la misura «0 cartelle» l'ho fatta da root, e a root i permessi non impediscono `rmtree`. Da utente normale una cartella lasciata non scrivibile verrebbe saltata in silenzio (`ignore_errors=True`). Oggi l'unico caso, T73e, ripristina il permesso.

**Cosa NON ho verificato**
- Il download reale del modello in T30e: qui manca la rete, quindi R-415-1 viene dalla lettura del codice e non da una misura.
- Il comportamento su macOS, dove `TMPDIR` è in `/var/folders` e c'è il sandbox applicativo senza bwrap: non riproducibile in questo ambiente.
- Il pytest intero da 1703: non l'ho rieseguito, il diff non lo tocca grazie a `collect_ignore`.
- Interruzioni vere con SIGKILL/SIGTERM: le ho valutate dalla semantica di Python, senza provarle.

**Memoria**: riga #415 e lezione aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate con `scripts/commit_memoria_revisore.sh` (commit 3892c08). Lezione: quando si sposta la cartella temporanea di sistema, cercare gli usi di `gettempdir()` come cache che deve restare tra le esecuzioni, perché diventano per-esecuzione.

Nota: un mio comando contenente «git commit» (nella copia dello scratchpad) è stato bloccato dall'hook del gate di review. Il repo reale non è stato toccato, a parte la memoria.

---

### Review #416 (chat Motore) — commit 5999fdb

## VERDETTO: APPROVATO CON RISERVE

Review #416 (chat Motore). Ho letto CLAUDE.md (sezioni 5, 8 e 10), le voci R7 e R-415 di reports/stato_progetto.md e la memoria del revisore.

Ho riprodotto tutto su una copia dell'index nello scratchpad, poi cancellata. Disco prima di partire: 29 GB liberi (28% usato).
- **Suite:** notte 123 passed, kernel 964 PASS / 0 FAIL. Dopo l'esecuzione in /tmp resta solo `gas_vec_model_cache`.

**Elementi del diff esaminati**
- `modules/notte/notte.py:582` — `_ordina_riprese` non scrive più l'avviso e passa `rilancio_a_mano` e `interruzioni` nel compito. Rischio: si perde il testo «rilanciato a mano dopo N interruzioni». test_r406_solo_a_mano_rilancia_oltre_il_tetto passa ancora. Esito: ok.
- `modules/notte/notte.py:670` — l'avviso «ripreso» nasce solo dopo che il kernel è partito, e quindi anche dopo il controllo del tempo rimasto. Ho controllato tre casi:
  - **Kernel che non parte:** nessun avviso e voce del registro invariata (tentativi 1).
  - **Tempo del giro finito prima del compito ripreso** (sonda con `time.monotonic` forzato): rc 1, solo l'avviso «tetto di tempo… saltati 1 compiti (lungo)», nessun «ripreso», registro invariato.
  - **Mutazione** (avviso rimesso prima della creazione del kernel): test_v2_bot234_ripreso_solo_se_parte FAIL, quindi il test discrimina.
  - Esito: ok, con la riserva R-416-1.
- `tests/test_unit_kernel.py:21` — `_TMP_SISTEMA` viene salvato prima dell'override e si tolgono le `gas_kernel_run_*` più vecchie di 6 ore. Sonda:
  - una cartella vecchia (7 ore) viene tolta, una recente resta;
  - un symlink vecchio verso una cartella esterna NON viene seguito (`rmtree` lo rifiuta, errore ignorato) e il bersaglio resta intatto.
  - Un'altra esecuzione della suite in corso da più di 6 ore potrebbe perdere la sua cartella. È accettabile: la suite dura circa 35 s, e il mtime della cartella si aggiorna a ogni `mkdtemp` dentro di essa. Esito: ok.
- `tests/test_unit_kernel.py:1839` — T30e usa `_TMP_SISTEMA` per la cache del modello: la cache resta tra le esecuzioni, quindi R-415-1 è chiusa. Esito: ok.
- `tests/test_unit_notte.py:1691` — test nuovo: kernel rotto con una voce di registro a 1 → niente «'lungo' ripreso» nel riepilogo e registro a 1. Esito: ok.

Ordine degli avvisi nel riepilogo: i test esistenti (`tests/test_unit_notte.py:1548`, `tests/test_unit_notte.py:1633`) controllano solo che il testo ci sia, non la posizione. L'avviso «ripreso» ora viene dopo quello sul budget: cambia l'ordine, nessun test rotto.

**Finding**
- **R-416-1 (chat Motore) BASSA:** l'avviso «ripreso» ora viene creato DOPO il ciclo `for a in avvisi: logging.warning("notte: %s", a)`. Quindi non arriva più in gas_debug.log: compare solo nel riepilogo e su Telegram. Prima ci arrivava. Rimedio: un `logging.warning` accanto all'`avvisi.append` nuovo.
- **R-416-2 (chat Motore) COSMETICA:**
  - l'ordine degli avvisi nel riepilogo è cambiato;
  - `import time as _time_pulizia` sta a metà del file;
  - i symlink `gas_kernel_run_*` vecchi restano in /tmp: non vengono seguiti né tolti.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. Guardrail (tetto di 10 iterazioni, `_get_window`, fail-safe dei provider) non toccati.

**Rischio escluso:** il download reale del modello in T30e con rete non è verificato (qui è un SKIP o una cache già presente). Ho verificato solo che il percorso della cache stia fuori dalla cartella dell'esecuzione. Non ho verificato nemmeno la pulizia da utente non root con cartelle senza permesso di scrittura.

**Memoria:** riga #416 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione: «spostare la generazione di un avviso dopo il punto in cui la lista viene loggata lo toglie dalla scatola nera». Committata con `scripts/commit_memoria_revisore.sh` (commit 59374ed, solo quel file). Il diff staged è rimasto intatto: 3 file, 37 righe aggiunte e 6 tolte.

---

### Review #417 (chat Motore) — commit f2c3e29

## VERDETTO: APPROVATO CON RISERVE

Review #417 (chat Motore) del diff staged: chiude R-416-1. Ho letto CLAUDE.md, stato_progetto e la mia memoria.

**Cosa ho controllato nel diff**
- `modules/notte/notte.py:675`: aggiunge `logging.warning("notte: %s", avvisi[-1])` subito dopo che l'avviso «compito 'X' ripreso…» viene aggiunto alla lista.
  - Rischio: righe doppie nel log, oppure avviso che ancora non ci arriva.
  - Esito: ok. Il ciclo che scrive nel log gli altri avvisi (`modules/notte/notte.py:641`) gira prima del loop dei compiti, quindi questo avviso finisce nel log una sola volta. Il formato è lo stesso di `modules/notte/notte.py:659` (avviso del tetto del giro). Viene ancora creato solo dopo l'avvio del kernel, come voluto in V-2 bot #234. Nessun nuovo punto di crash: `logging` è già importato e la riga è dentro il try del giro.
- `tests/test_unit_notte.py:1707`, `test_r416_avviso_ripresa_nel_log`: con caplog controlla che il testo «'lungo' ripreso» arrivi nel log quando nel registro c'è un compito in corso e il kernel parte.
  - Rischio: test che passa anche senza il fix.
  - Esito: ok. Ho tolto la riga di log in una copia: fallisce solo questo test, gli altri 123 passano.
- Riprodotto su una copia nello scratchpad, poi cancellata: suite notte **124 passed**.

**Finding**
- R-417-1 (chat Motore) BASSA, già presente e fuori dal diff: l'avviso «N richiesta/e di firma scaduta/e … chiuse, NON eseguite» (`modules/notte/notte.py:692`) viene aggiunto anch'esso dopo il ciclo di log. Va nel riepilogo e su Telegram ma non in gas_debug.log. È lo stesso difetto di R-416-1; si sistema con un `logging.warning("notte: %s", avvisi[-1])` dopo l'append.
- R-417-2 (chat Motore) COSMETICA: il test verifica che la riga ci sia, non che sia una sola. Oggi il codice non scrive doppioni, ma il test non lo protegge.

**Cosa NON ho verificato**
- Non ho controllato che l'avviso arrivi davvero nel file gas_debug.log con l'handler reale del kernel e su VPS. caplog intercetta il logger principale, e lì scrivono anche gli altri avvisi del giro, ma non ho provato il file vero in esecuzione notturna.
- Non ho rieseguito la suite del kernel: il diff tocca solo la notte.

**Memoria**
- Riga #417 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md con la lezione: quando si chiude un «avviso che non arriva nel log», cercare tutti gli avvisi aggiunti dopo il ciclo di log, non solo quello segnalato.
- Committata con lo script apposito (commit 0187872). Il diff staged sotto review è intatto.
- Nel repo non ho fatto altre modifiche e nessun checkout.

---

### Review #418 (chat Motore) — commit d9f58bb

## VERDETTO: APPROVATO CON RISERVE

Review #418 (chat Motore): chiude V-1 del bot su PR #234. Ho fatto le tre letture obbligatorie: CLAUDE.md, la parte di reports/stato_progetto.md che riguarda #234 e la notte, e la memoria del revisore.

Elementi del diff esaminati:
- `modules/notte/notte.py:583-589`: la voce di ripresa ora va in `ripresi` se tentativi == 1, in `in_coda` se tentativi >= 2. Rischio esaminato: ordine instabile e chiavi perse. Esito: ok. Le tre liste mantengono l'ordine del catalogo. Prova su una copia: con catalogo a,b,c,d,e e tentativi {a:2, b:2, d:1, e:3} l'ordine è [d, c, a, b], con e saltato (saltati=1). `ripresa`, `rilancio_a_mano` e `interruzioni` restano invariati.
- `modules/notte/notte.py:575`: il salto oltre MAX_TENTATIVI (3) non cambia. Rischio esaminato: interazione con `solo` e con il rilancio a mano. Esito: ok. Con `solo`/a_mano c'è un solo compito, quindi l'ordine non conta. Prova: e (tentativi 3) rilanciato a mano non viene saltato e ha `rilancio_a_mano=True`; b (tentativi 2) rilanciato a mano ha ripresa=True ed è eseguito.
- `tests/test_unit_notte.py:1719`: il test `test_v1_bot234_ripreso_due_volte_va_in_coda` verifica l'ordine [medio, breve, lungo] passando da `esegui_notte` intero. Rischio esaminato: un test che passa anche senza la correzione. Esito: ok. Con la versione di HEAD di notte.py il test FALLISCE; con la correzione la suite notte dà 125 passed.
- Contesto, `modules/notte/notte.py:681`: il contatore cresce solo quando il compito parte davvero. Serve a valutare il caso del tetto di tempo (vedi R-418-2).

Il nuovo codice non tocca il Wall of Shame (né la storia né `_get_window`) né i guardrail (cap 10 iterazioni, cap 8k output, anti-memoria). Non ci sono nuove eccezioni da gestire.

Finding:
- **R-418-1 (BASSA, cosmetica)**: le docstring a `modules/notte/notte.py:554` («i compiti rimasti a metà vanno per primi») e `modules/notte/notte.py:597` («ripartono per primi») non descrivono più il comportamento. Vanno aggiornate: tentativi 1 per primi, 2 o più in coda.
- **R-418-2 (BASSA, accettabile)**: un compito in coda che non parte perché è finito il tempo del giro non incrementa il contatore. Resta a tentativi 2 da una notte all'altra e non arriva mai al salto con azzeramento. Il blocco non è silenzioso: compare ogni notte in «tetto di tempo ... saltati ...» ed esce con exit 1. Lo considero accettabile perché è preferibile a un compito che fa cadere Gas e consuma tutto il giro. Riserva da tracciare: l'avviso di salto per tempo non dice che quel compito era una ripresa in coda. Si può aggiungere se si vuole che l'operatore lo riconosca.
- **R-418-3 (BASSA, da dichiarare)**: resta un costo. Con un compito che fa cadere Gas subito, nella seconda notte del ciclo (tentativi 1, per primo) il giro si perde ancora tutto. Ciclo: notte 1 si perdono i compiti che vengono dopo nel catalogo; notte 2 si perde tutto; notte 3 gli altri girano e poi cade; notte 4 il compito è saltato e il contatore azzerato. Prima della correzione si perdevano 2 notti intere su 4, ora 1. Scelta difendibile: un singolo crash può essere casuale, quindi riprovarlo per primo ha senso. Va però detto così nel report e non come «risolto del tutto».

Cosa NON ho verificato: il comportamento reale sul Mac/VPS con un processo che cade davvero (kill durante il compito) e il tetto di tempo reale del giro. Non sono riproducibili qui; ho provato solo `_ordina_riprese` in isolamento e la suite notte con un kernel finto. Non ho rieseguito la suite completa del kernel, perché il diff tocca solo modules/notte e il suo test.

Nel repo reale non ho fatto checkout né modifiche. Le prove le ho fatte su una copia nello scratchpad, già cancellata. In /home/user/Gas/.claude/agents/memoria_revisore.md ho aggiunto la riga #418 e una lezione (con contatori di crash, simulare il ciclo notte per notte e il caso in cui il compito non parte), poi l'ho registrata con scripts/commit_memoria_revisore.sh, che non ha stampato errori.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 957 → 964 PASS, 0 FAIL (T94a-f, T95). Blocco reale: `=== RIEPILOGO: 964 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py`: 106 → `125 passed`; `tests/test_unit_gate.py`: 811 → `817 passed`.

## §6 STATO CI

- 5267148: handoff-check, unit-suite success; verifica-bot neutral (APPROVATO CON RISERVE).
- 9d793f3: unit-suite success, handoff-check success (verifica esterna #234 2° giro); verifica-bot neutral (APPROVATO CON RISERVE).
- ab60f35: handoff-check failure (pushato senza il dossier, per l'HEAD staccato da un agente di verifica); superato dal commit successivo.
- 2d07cd3: unit-suite success (kernel 964 PASS in CI), handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE) — dal verdetto del bot.
- 0a11a8b (con a86f493, 5142d8f e memorie): run non letta (nessun evento ricevuto prima della scrittura).
- 0a11a8b: verifica-bot failure (il bot ha letto come riserva la frase «nessuna ALTA/MEDIA aperta» della descrizione; testo del verdetto APPROVATO CON RISERVE con V-1 BASSA, ora chiusa da d9f58bb).
- 01bf064 (con 3a43d93, 5999fdb, f2c3e29 e memorie): run non letta prima della scrittura.
- d9f58bb e memoria: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-408-1 (BASSA): potatura del registro spenta da qualsiasi avviso del catalogo.
- R-408-2 (COSMETICA): read_file su «.» negato invece di «è una cartella».
- Limite dichiarato (#406): la ripresa riparte da capo con la nota, non rilegge la storia parziale del compito.
- R-411-2 (BASSA): conteggio enorme scritto a mano conta 0.
- V-3 verifica esterna #234 (BASSA, dichiarata): un Ctrl-C dell'operatore conta come crash.
- R-412-1 (BASSA): si tengono le prime 12 parole della ricerca.
- R-412-2 (COSMETICA): T95 parziale.
- R-414-1/2 (BASSE), R-414-3 (COSMETICA): orologio indietro, coda senza a capo riletta, messaggio di T94a.
- R-417-1 (BASSA): avviso «firme scadute» del giro non va in gas_debug.log.
- R-415-3, R-416-2, R-417-2, R-418-1 (COSMETICHE).
- R-418-2 (BASSA): compito in coda fermato dal tetto di tempo resta a tentativi 2.
- R-418-3 (BASSA, dichiarata): un compito che fa cadere Gas a ogni avvio fa perdere ancora un giro su quattro.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
