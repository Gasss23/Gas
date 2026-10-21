# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #233) — compiti notturni che riprendono dopo un crash (R7/M3 fetta 1), spesa giornaliera incrementale (5.5), piccole riserve

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #234 (https://github.com/Gasss23/Gas/pull/234; numero e URL dall'API GitHub, `gh` non usato): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).
2. C6: decisa (a) «lasciamo così» dall'operatore il 2026-10-21 — nessuna azione.

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
- **Compiti sani per primi, sospetti in coda; registro dei costi a blocchi; date future (V-1/V-2 verifica #234 3° giro, V-1 bot #234, R-419-1, R-420-1)**: `FATTA` — review #419, #420, #421 APPROVATO CON RISERVE.
- **Righe valide lunghe contate; «sospetto» mantenuto e in coda (V-1/V-2 verifica #234 4° giro, R-421-1/2/3)**: `FATTA` — review #422 APPROVATO CON RISERVE.
- **Riserve R-422-1/2/3 (avviso righe enormi, test a cavallo di blocchi)**: `FATTA` — review #423 APPROVATO CON RISERVE.
- **Riga finale non riletta a file invariato; firme scadute nel log (V-1 bot V-B e verifica esterna #234 5° giro, R-417-1, R-423-1)**: `FATTA` — review #424 APPROVATO CON RISERVE. V-3 verifica esterna (registro senza blocco): non regge, il registro si tocca dopo il lock esclusivo del giro.
- **R7 / R-222-2 — esito «negata/in attesa» detto dal kernel, non dall'inizio del testo; T94j più stretto (R-424-2/3)**: `FATTA` — review #425 APPROVATO CON RISERVE.
- **Lock sulla cache dei costi; test del kernel per l'esito al cancello (V-1/V-2 verifica esterna #234 7° giro, R-425-1/2)**: `FATTA` — review #426 APPROVATO CON RISERVE.
- **Merge di origin/main (#235, chat Mani) per togliere il conflitto della PR**: `FATTA` — review #427 APPROVATO; conflitti solo nei report di sessione e nella memoria del revisore.
- **C6**: `SALTATA` — l'operatore ha scelto (a) «lasciamo così» (2026-10-21).
- **R7 — ripresa dal punto esatto**: `DEFERITA` — da valutare.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   24 ++++++++
 gas.py                             |  214 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 modules/gate/gate.py               |   12 +++-
 modules/memory/store.py            |   21 ++++++-
 modules/notte/notte.py             |  169 +++++++++++++++++++++++++++++++++++++++++++++++++----
 reports/da_mergiare.md             |  103 +++++++++++++-------------------
 reports/diff_sessione.md           |   16 ++---
 reports/handoff.md                 | 1143 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------
 reports/roadmap.md                 |    6 +-
 reports/stato_progetto.md          |    4 +-
 reports/ultimo_report.md           |   62 ++++++++++----------
 tests/test_unit_gate.py            |    8 +++
 tests/test_unit_kernel.py          |  286 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_notte.py           |  359 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 14 files changed, 2039 insertions(+), 388 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
239768c docs(fine-task): merge di main (#235) nel ramo, C6 decisa «lasciamo così»
d6cc1cd Merge origin/main (#235, chat Mani) in feat/merge-automatico-z1xjx2
634eba9 docs(fine-task): report e handoff — lock della cache dei costi, test dell'esito al cancello (#426)
efd2294 fix(budget): lock sulla cache dei costi; test del kernel per l'esito al cancello (V-1/V-2 verifica #234 7° giro, R-425-1/2)
cf1915e chore(revisore): memoria review #426 — APPROVATO CON RISERVE
47b3957 docs(fine-task): report, handoff e roadmap — R-222-2 chiusa (#425)
52501e2 fix(notte,kernel): esito «negata/in attesa» detto dal kernel, non dal testo (R7 R-222-2); T94j conta i byte letti (R-424-2/3)
ef8a5dd chore(revisore): memoria review #425 — APPROVATO CON RISERVE
6160555 docs(fine-task): report e handoff — riserve #422-#424, riga finale non riletta, firme scadute nel log
214a450 fix(budget,notte): riga finale non riletta a file invariato; firme scadute anche nel log (V-1 bot/verifica #234 5° giro, R-417-1, R-423-1)
06da7ac chore(revisore): memoria review #424 — APPROVATO CON RISERVE
d718b5d fix(budget): avviso anche per righe enormi scartate dal ramo lungo; test a cavallo di blocchi (R-422-1/2/3)
6609ca5 chore(revisore): memoria review #423 — APPROVATO CON RISERVE
0c02776 docs(fine-task): report e handoff — righe valide lunghe, sospetto in coda (#422)
373542f fix(budget,notte): righe valide lunghe contate; sospetto mantenuto e in coda (V-1/V-2 verifica #234 4° giro, R-421-1/2/3)
9533488 chore(revisore): memoria review #422 — APPROVATO CON RISERVE
9f470a9 chore(revisore): memoria review #422 — APPROVATO CON RISERVE
eb869d2 docs(fine-task): report, handoff, coda da_mergiare — compiti sani per primi, lettura a blocchi, date future (#419-#421)
3701278 fix(budget): data futura entro 7 giorni tenuta com'è (stabile tra processi), oltre scartata; tetto di riga ovunque (R-420-1/2/3/4)
a871d24 chore(revisore): memoria review #421 — APPROVATO CON RISERVE
7204835 fix(notte,budget): compito saltato resta «sospetto» e parte in coda; ts futuro contato adesso; lettura a blocchi senza copie quadratiche (R-419-1/2/3, V-1 bot #234, R-414-1)
1bddf93 chore(revisore): memoria review #420 — APPROVATO CON RISERVE
898a4a2 fix(notte,budget): compiti mai interrotti sempre per primi; registro dei costi letto a blocchi con uscita rapida sulle righe vecchie (V-1/V-2 verifica esterna #234)
ecec535 chore(revisore): memoria review #419 — APPROVATO CON RISERVE
8e3072b docs(fine-task): report, handoff, coda da_mergiare — ordine delle riprese (#418)
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

### Review #419 (chat Motore) — commit 898a4a2

## VERDETTO: APPROVATO CON RISERVE

Review #419 (chat Motore). Diff staged: gas.py, modules/notte/notte.py, tests/test_unit_kernel.py, tests/test_unit_notte.py. Prima della review ho letto CLAUDE.md (sez. 5), le voci aperte in reports/stato_progetto.md e la mia memoria (#415-#418). Spazio su disco: `df -h /` dava 29G liberi. Ho lavorato su una copia nello scratchpad e poi l'ho cancellata; nel repo reale ho toccato solo la memoria.

**Cosa ho riprodotto:** notte 126 passed, kernel 965 PASS / 0 FAIL. Ho rimesso il vecchio ordine `ripresi + altri + in_coda` come prova: falliscono 3 test della notte, compreso quello nuovo.

**Elementi del diff esaminati**
- modules/notte/notte.py:593 — l'ordine ora è `altri + ripresi + in_coda`. Rischio esaminato: un compito che crasha toglie ancora notti ai compiti sani? Esito: **riserva** (R-419-1).
- gas.py:1258 — lettura a blocchi: `dati = resto + blocco`, offset avanzato di `fine + 1`, `resto` ripreso dal blocco successivo. Rischi esaminati: righe a cavallo di più blocchi, blocco che finisce esattamente su «\n», file senza «\n», aggiunta incrementale. Ho confrontato 300 log casuali con blocchi da 1/2/3/7/64 byte e da 1 MiB, più un'aggiunta incrementale, con una lettura intera di riferimento: risultati identici, salvo le righe costruite a mano di R-419-3. Esito: ok sulla correttezza, **riserva** sulle prestazioni (R-419-2).
- gas.py:1266 — uscita rapida con `_TS_RAPIDO_RE` (gas.py:867), un solo `"ts"` e confronto col cutoff. Rischi esaminati: spazi, `"ts"` annidato, chiave `ts` duplicata, `"ts"` dentro una stringa, ts con frazioni di secondo, fallthrough, righe spazzatura. Tutti coincidono con json.loads, tranne le chiavi scritte con escape. Esito: **riserva** (R-419-3).
- gas.py:1284 — la riga finale senza «\n» si prende dal resto in memoria e si ignora sopra i 64 KB (R-414-2 chiusa). Esito: ok.
- tests/test_unit_kernel.py:7204 — T94g, blocchi da 7 byte confrontati con la lettura intera, poi un'aggiunta. Esito: ok.
- tests/test_unit_notte.py:1741 — test «6 notti su 6». Esito: **riserva**. Il catalogo mette «breve» per primo, quindi la notte 1 passa comunque e il test non prova il caso peggiore.

**Finding**
- **R-419-1 (MEDIA): V-1 non è chiusa davvero.** Ho simulato 8 notti con il compito che crasha messo PRIMO nel catalogo:
  - con questo diff, «breve» parte così: [0,1,1,1,0,1,1,1];
  - a HEAD partiva così: [0,0,1,1,0,0,1,1];
  - con il compito che crasha messo secondo: [1,1,1,1,1,1,1,1].

  La causa: dopo MAX_TENTATIVI il compito viene saltato e il suo conto si azzera (modules/notte/notte.py:576). Al giro dopo torna tra gli «altri» e, se nel catalogo viene prima, fa cadere di nuovo il giro. Risultato: si perde ancora 1 notte su 4. Il commento di modules/notte/notte.py:591 («non toglie notti agli altri») e la docstring sono quindi falsi in questo caso. Rimedio:
  - all'azzeramento tenere una traccia del compito (es. `{"tentativi": 0, "sospetto": True}`) e metterlo in coda anche quando riparte come «nuovo»;
  - in alternativa, dichiarare il limite;
  - in entrambi i casi aggiungere un test col compito che crasha primo nel catalogo.

  Finché non si fa, V-1 non va dichiarata chiusa nei report.
- **R-419-2 (BASSA): rallentamento quadratico su una riga senza «\n» lunghissima.** Se nel file mancano gli «\n» per molti blocchi, `resto + blocco` ricopia tutto a ogni blocco. Misura: coda senza «\n» da 128 MB = 7,0 s a ogni chiamata (HEAD 0,35 s), perché l'offset non avanza e si rilegge ogni volta. In quel caso `resto` tiene anche tutto in memoria, contro lo scopo di V-2. Rimedio: cercare «\n» solo nel blocco nuovo e, oltre i 64 KB, smettere di accumulare fino al prossimo «\n».
- **R-419-3 (BASSA): l'uscita rapida può scartare una riga che json.loads conterebbe.** Succede con una chiave scritta con escape:
  - `{"ts":"<vecchio>","ts":"<nuovo>",...}`, oppure
  - `{"ts":"<nuovo>","x":{"ts":"<vecchio>"}}`.

  Riprodotto: in questi casi la spesa risulta più bassa del vero. Succede solo con log scritti a mano (`_log_tokens` usa json.dumps, che non fa escape di lettere ASCII). Rimedio da una riga: niente uscita rapida se `b"\\" in raw`.
- **R-419-4 (COSMETICA): testi rimasti indietro.** Il nome di tests/test_unit_notte.py:1531 (`..._ripresa_per_primo`), la docstring di tests/test_unit_notte.py:1721 («per primo») e il commento V-1 bot di modules/notte/notte.py:586 non descrivono più l'ordine attuale. Va aggiornata anche la nota R-418-3 in reports/da_mergiare.md.
- **Domanda sul tetto di tempo:** se gli «altri» esauriscono il tempo del giro, un compito ripreso messo in fondo non parte. Compare comunque ogni notte nell'avviso «tetto di tempo del giro … saltati N compiti (nomi)», che va anche in gas_debug.log, quindi si vede. Però il suo conto resta fermo (1 o 2) e non arriva mai al salto né all'azzeramento. Estende R-418-2, BASSA, nessun nuovo finding.

**Antipattern del Wall of Shame:** nessuno slicing della history, nessuna simulazione di output dei tool. `_daily_cost_usd` resta tutto dentro try/except con logging.warning (FAIL-SAFE §9). Il cap di 10 iterazioni e `_get_window` non sono toccati.

**Cosa NON ho verificato:**
- Il comportamento sul VPS, con un log vero da decine di MB e un disco lento: non è riproducibile qui. Le misure 1,7 s / 1 ms dell'agente non le ho rifatte.
- Un kill vero del processo durante un giro: ho usato il KeyboardInterrupt simulato di `_KCrash`.
- Una scrittura concorrente nel log mentre lo si legge a blocchi.

**Memoria:** riga #419 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, registrate da sole (ecec535). Il diff staged è rimasto com'era.

---

### Review #420 (chat Motore) — commit 7204835

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sezioni 1, 5, 8, 9 e 10), le parti di `reports/stato_progetto.md` che servivano e le ultime righe di `.claude/agents/memoria_revisore.md`, comprese le lezioni #418 e #419. Spazio su `/`: 28% usato. Ho lavorato su una copia nello scratchpad (HEAD più il diff staged), che poi ho cancellato. Nel repo reale ho toccato solo la memoria, già registrata con lo script (commit 1bddf93).

**Elementi del diff esaminati**

- `modules/notte/notte.py:589` — dopo MAX_TENTATIVI interruzioni la voce diventa `{"tentativi": 0, "inizio": …, "sospetto": True}` invece di essere cancellata. Rischio esaminato: il compito che crasha torna «nuovo» e ruba di nuovo notti agli altri. Ho simulato 12 notti con il compito che crasha in OGNI posizione del catalogo ([lungo,a,b], [a,lungo,b], [a,b,lungo]): gli altri perdono solo la notte 1, poi girano sempre. Mutazione (rimesso `del in_corso[...]`): falliscono 2 test. **Esito: ok.**
- `modules/notte/notte.py:583` — un compito con tentativi 0 va in coda e senza marcatura `ripresa`. Rischi esaminati:
  - Potatura: un compito sospetto tolto dal catalogo si toglie anche dal registro (riga 573, con `pota`).
  - Sospetto chiesto a mano: il ramo t==0 viene prima del ramo `a_mano`, quindi il compito parte comunque.
  - `in_corso != letto`: la voce viene sostituita con un dict nuovo, quindi la differenza si vede e il registro si scrive.
  - Kernel non creato: il compito resta sospetto.

  **Esito: ok.** Riserva R-420-4 qui sotto.
- `modules/notte/notte.py:540` — `_leggi_in_corso` accetta tentativi 0 solo con `sospetto is True`. Rischio: un registro rovinato con tentativi 0 o con `sospetto` non booleano. Senza sospetto la voce si scarta ancora. **Esito: ok.**
- `gas.py:1273` — una riga oltre `_RIGA_MAX` senza «\n» diventa `lunga` e se ne tengono solo gli ultimi 64 byte. `gas.py:1292-1293` — offset e coda si aggiornano con `pendenti`. Rischio esaminato: la coda in cache deve restare uguale ai 64 byte prima dell'offset nel file. Ho fatto una sonda con blocchi da 1, 7, 64, 100, 4096 e 70000 byte, 40 log casuali per ogni dimensione, righe spazzatura da 65 a 140 KB, più l'aggiunta a metà di una riga lunga che si chiude al giro dopo. Ho confrontato offset e coda con `data.rfind(b"\n")+1` e con i 64 byte reali prima dell'offset, e il totale con quello calcolato a cache vuota: 0 errori. La coda resta corretta anche con `lunga` vera, perché `resto` contiene esattamente gli ultimi 64 byte dei byte pendenti e subito dopo viene `blocco[:fine+1]`, senza buchi. **Esito: ok.** Riserva R-420-2 qui sotto.
- `gas.py:1285` — niente uscita rapida se nella riga c'è un backslash (chiude R-419-3). **Esito: ok.**
- `gas.py:887` — un ts nel futuro (oltre 1 ora) diventa l'ora attuale. Rischio esaminato: che la voce resti nel conto per sempre. **Esito: riserva R-420-1.**
- `tests/test_unit_notte.py:1761` (test nuovo R-419-1), `tests/test_unit_notte.py:1552` (test vecchio aggiornato), `tests/test_unit_kernel.py:7178` (T94e2). Risultati sulla copia: notte 127 passed, kernel 966 PASS / 0 FAIL. **Esito: ok.**

**Riserve**

- **R-420-1 MEDIA** — Il ts futuro viene trasformato in «adesso» quando la riga si LEGGE, e `_COSTI_CACHE` vive solo dentro il processo.
  - Ogni processo nuovo rilegge il log da capo e ri-timbra la riga con l'ora del momento: `gas notte` da cron, ogni comando da terminale, ogni riavvio del bot.
  - Quindi una riga con ts «2999-01-01…» conta nel tetto per sempre. L'ho provato: col primo calcolo vale 0,1 USD; nello stesso processo, dopo la scadenza simulata, vale 0; con la cache svuotata (processo nuovo) torna a 0,1. Una riga finale senza «\n» conta sempre allo stesso modo.
  - La docstring a `gas.py:873` («mai un blocco per sempre») è vera solo dentro un processo che resta acceso.
  - Con un errore di orologio realistico (ore o giorni) la voce scade comunque a ts+24h, quindi il caso grave nasce solo da un log rovinato o scritto a mano. È proprio il caso che R-413-1 voleva coprire.
  - Correzione suggerita: contare come «adesso» solo i ts futuri entro un margine plausibile (es. 2-7 giorni) e scartare quelli oltre con un warning in gas_debug.log; in alternativa usare una data che non cambi da un processo all'altro. Va aggiunto un test a cache vuota.
- **R-420-2 BASSA** — Il vero tetto di riga non è `_RIGA_MAX` (64 KB) ma «un blocco intero senza \n». Una riga JSON valida tra 1 e 2 MiB conta oppure no a seconda di dove cade rispetto ai blocchi. Provato con una riga da 1.048.698 byte: a offset 0 il totale è 0, a offset 1.048.277 è 0,1. Capita solo con log scritti a mano. Per allineare il comportamento al commento basta scartare nel ciclo anche `len(resto + blocco[:fine]) > _RIGA_MAX`.
- **R-420-3 COSMETICA** — Il commento «V-2 verifica #234: lettura del log dei token a blocchi da 1 MiB» è finito in coda alla riga di `_RIGA_MAX` (`gas.py:869`) invece di stare su `_COSTI_BLOCCO`.
- **R-420-4 BASSA** — Con la mutazione «senza il ramo t==0» fallisce solo il test vecchio, non `test_r419`: il sospetto finirebbe tra i ripresi, comunque dopo gli altri. Il test nuovo quindi non protegge da solo la messa in coda del sospetto. Collegato: se il sospetto non parte per il tetto di tempo, resta `{0, sospetto}` senza mai arrivare a un nuovo salto (estende R-418-2; si vede solo in «saltati per tempo»).

Coerenza col progetto: nessuno slicing della history, nessuna simulazione di output dei tool, cap e `_get_window` non toccati. `_daily_cost_usd` resta a prova di crash: in caso di errore scrive in gas_debug.log e restituisce 0.0. Il diff va nella direzione «robustezza > potenza».

**Rischi esplicitamente esclusi**

- Comportamento reale su VPS con cron e un log di token grande (centinaia di MB): non riproducibile qui. Ho misurato solo la logica, non i 0,10 s dichiarati dall'agente.
- Non ho rifatto la sonda differenziale dell'agente (150 log × 5 aggiunte) contro una lettura completa di riferimento: ho fatto una sonda mia, mirata a offset e coda.
- Gate dei test (817): non eseguito.

Memoria aggiornata: riga #420 più una lezione (un valore «normalizzato all'ora attuale» dentro una cache in memoria va provato anche a cache vuota, cioè in un processo nuovo). Il file è `/home/user/Gas/.claude/agents/memoria_revisore.md`, registrato in 1bddf93.

---

### Review #421 (chat Motore) — commit 3701278

## VERDETTO: APPROVATO CON RISERVE

Review #421 (chat Motore), sul diff staged: gas.py, tests/test_unit_kernel.py, tests/test_unit_notte.py. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (in modo mirato) e .claude/agents/memoria_revisore.md. Spazio su disco con `df -h /`: 29G liberi, uso 28%.

Ho riprodotto tutto su una copia nello scratchpad, poi cancellata. Nel repo reale non ho toccato nulla oltre alla memoria (commit a871d24); lo staging è intatto. Risultati: kernel 966 PASS / 0 FAIL, notte 128 passed.

**Elementi esaminati**
- gas.py:887 — `_ts_log_valido`: un ts nel futuro fino a 7 giorni resta com'è, oltre viene scartato con un `logging.warning`. Rischio esaminato: il caso V-1 del bot #234 (orologio tornato indietro) e la tenuta a cache vuota. Prova: con l'orologio indietro di 3 giorni, due righe di «ieri» del vecchio orologio contano 0,2 USD. Contano finché l'ora attuale non arriva a ts+24h, con lo stesso valore in ogni processo; la durata massima è circa 8 giorni. Bordo dei 7 giorni: −5 minuti contato, +5 minuti scartato. La spesa resta quindi nel tetto, con una durata limitata. Esito: ok, R-420-1 chiusa.
- gas.py:1285 — una riga oltre `_RIGA_MAX` viene saltata ovunque cada. Rischio esaminato: righe lunghe a cavallo dei blocchi. Prova: una riga di 100 KB in mezzo dà 0,2 come atteso. Una riga di circa 1 MiB a offset 0, 500.000 e 1.048.277 dà sempre 0,1, mentre in #420 l'esito cambiava con l'offset. Esito: ok, R-420-2 chiusa, ma senza test (vedi R-421-2).
- gas.py:1310 — riga finale senza «\n», rivalutata a ogni chiamata (contesto). Rischio esaminato: avviso ripetuto. Esito: riserva R-421-1.
- tests/test_unit_kernel.py:7171 — T94e2 riscritto. Ho rimesso la vecchia logica dell'«adesso» (mutazione): T94e2 FALLISCE, quindi il test protegge la correzione. Nota: la parte «a cache vuota» da sola non distingue le due logiche (danno 0,1 entrambe); a discriminare è `_fut94b[0] == _due_ore94`. Esito: ok.
- tests/test_unit_notte.py:1786 — test unitario di `_ordina_riprese`. Ho tolto il ramo `tentativi == 0` (mutazione): falliscono questo test e test_r7_oltre_max_tentativi_saltato_e_azzerato. Esito: ok, R-420-4 chiusa.
- gas.py:868 — il commento è stato spostato su `_COSTI_BLOCCO`, ma ora compare due volte (una riga sopra e la stessa in linea). Esito: riserva cosmetica, R-421-3.

**Avviso ripetuto (domanda dell'operatore)**
- Riga oltre 7 giorni chiusa da «\n»: le righe scartate non entrano in cache ma l'offset le supera, quindi l'avviso esce una volta per processo. Prova: 5 chiamate nello stesso processo → 1 avviso; 3 processi nuovi → 3 avvisi. È il comportamento atteso.
- La stessa riga come ULTIMA riga senza «\n»: 5 chiamate → 5 avvisi (vedi R-421-1).

**Finding**
- R-421-1 BASSA: una riga oltre i 7 giorni, se è l'ultima del file e non ha «\n», produce un avviso in gas_debug.log a OGNI chiamata di `_daily_cost_usd`. `_budget_superato` la chiama più volte per turno (gas.py:3410, gas.py:4055, gas.py:4107, gas.py:4132), quindi la scatola nera cresce a ogni turno finché qualcuno non aggiunge una riga al log. Correzioni possibili: niente avviso per la riga finale rivalutata, oppure ricordare in cache che quella riga è già stata segnalata.
- R-421-2 BASSA: R-420-2 non ha un test. Togliendo il controllo su gas.py:1285 (mutazione) il kernel resta 966/0. Serve un test con una riga di 64 KB–1 MiB, chiusa da «\n», nello stesso blocco di righe valide e con un ts recente: oggi verrebbe contata.
- R-421-3 COSMETICA: il commento «V-2 verifica #234 … a blocchi da 1 MiB» è duplicato su gas.py:868-869.

**Rischio escluso**
- Non ho provato su VPS un salto vero dell'orologio di sistema: l'ho simulato scrivendo ts futuri nel log.
- Residuo dichiarato: se l'orologio torna indietro di più di 7 giorni (per esempio un orologio di sistema azzerato), la spesa precedente esce dal tetto, che resta aperto solo per quelle 24 ore. Accettabile, ma va scritto in stato_progetto.md.

**Antipattern (Wall of Shame)**: nessuno slicing della history e nessuna simulazione di output dei tool. Le eccezioni restano intercettate: `_costo_riga` e `_daily_cost_usd` con logging.warning e 0.0.

**Memoria**
- Aggiunta la riga #421 con la lezione: un avviso su una riga da scartare va provato anche sull'ultima riga senza «\n», che si rivaluta a ogni chiamata perché l'offset non avanza.
- Registrata con `scripts/commit_memoria_revisore.sh` (commit a871d24).
- File: /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #422 (chat Motore) — commit 373542f

## VERDETTO: APPROVATO CON RISERVE

Review #422 (chat Motore), sul diff staged: gas.py, modules/notte/notte.py, tests/test_unit_kernel.py, tests/test_unit_notte.py. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (in modo mirato) e la memoria del revisore.

Spazio su disco (`df -h /`): 29 GB liberi, uso al 29%. Ho lavorato su una copia nello scratchpad (HEAD più il diff staged), poi l'ho cancellata. Nel repo reale non ho toccato niente, a parte la memoria.

**Riproduzione**
- Kernel: 967 PASS, 0 FAIL.
- Notte: 129 passed.

**Mutazioni**
- `_RIGA_MAX = 65536`: T94h fallisce (0.2 invece di 0.3).
- Senza la conservazione del sospetto in modules/notte/notte.py:701: il test nuovo fallisce.
- Senza il ramo in modules/notte/notte.py:585: il test nuovo fallisce.

**Elementi esaminati**
- gas.py:872 — `_RIGA_MAX = 16 << 20`.
  - Rischio esaminato: lettura completa e lettura a blocchi danno risultati diversi per righe tra 64 KB e 16 MiB.
  - Sonda su 36 casi (righe da 70 KB, 1 MiB, 1 MiB+5, 5 MiB, M-1, M, M+1, M+512 KB e 20 MiB, ciascuna agli offset 0, 1, 500k e 1 MiB-3): tutti uguali al riferimento. Una riga di 16 MiB o meno si conta sempre, una più lunga si scarta sempre.
  - Riga lunga 3 MiB aggiunta al file a pezzi: contata una volta sola.
  - Esito: ok.
- gas.py:1278 — accumulo `resto += blocco` fino a 16 MiB.
  - Rischio esaminato: memoria e tempo.
  - Riga finale da 16 MiB senza «\n», riletta a ogni chiamata: 0,086 s per chiamata, picco di memoria 49 MiB (64 MiB se la riga ha il «\n»).
  - Riga finale da 64 MiB senza «\n»: 0,057 s per chiamata, perché passa dal ramo `lunga` e tiene solo la coda.
  - Succede solo con un log scritto a mano o rovinato. Su una VPS è accettabile.
  - Esito: ok.
- gas.py:1288 — warning sulle righe oltre il tetto.
  - Esito: riserva R-422-1 (sotto).
- gas.py:1315 — `_costo_riga(resto, avvisa=False)`.
  - La riga finale senza «\n» non scrive più l'avviso a ogni chiamata (chiude R-421-1).
  - Quando arriva il suo «\n» la riga passa per il ramo normale e avvisa una volta.
  - Esito: ok.
- modules/notte/notte.py:585 e modules/notte/notte.py:701 — un compito sospetto che ricade va in coda con la nota di ripresa, e il segno resta finché il compito non finisce.
  - Ho simulato 9 notti con il compito che crasha in posizione 0, 1 e 2 del catalogo.
  - Gli altri compiti perdono solo la notte 1. Poi l'andamento è [crash 2, crash 3, salto con {0, sospetto}, crash 1 con sospetto, …]: il segno non si perde mai.
  - Esito: ok.
- Casi chiesti, tutti ok:
  - `_leggi_in_corso` con sospetto e tentativi > 0: già accettato dal codice precedente, il diff aggiunge solo un commento.
  - Sospetto che arriva a MAX_TENTATIVI: scende nel ramo salto, torna a {0, sospetto} e il giro conta come ko.
  - Sospetto chiesto a mano (`solo="lungo"`): parte con la nota di ripresa, finisce, e il registro si svuota (`{}`).
- tests/test_unit_notte.py:1797 — il test nuovo copre il crash con il segno conservato e l'ordine breve, medio, lungo.
  - Esito: ok.

**Finding**
- **R-422-1 BASSA**: il warning «riga oltre 16 MiB ignorata» (gas.py:1288) parte solo per le righe tra 16 e circa 17 MiB.
  - Le righe più lunghe passano dal ramo `lunga` e vengono scartate senza nessun log. Provato: riga da 20 MiB, 0 warning; da M+1 e da M+512 KB, warning presente.
  - Quindi la frase del brief «oltre 16 MiB scartate con logging.warning» vale solo in parte.
  - Rimedio: un warning anche nel punto in cui `lunga` diventa True, oppure quando la riga lunga si chiude.
- **R-422-2 BASSA**: V-1 è provata solo a metà.
  - La mutazione che riporta l'accumulo tra blocchi a 64 KB (`if len(resto) > 65536` in gas.py:1278) sopravvive: 967 PASS, 0 FAIL.
  - Motivo: la riga di T94h è da 100 KB e sta dentro un solo blocco da 1 MiB.
  - Manca un test con una riga valida più lunga di un blocco (per esempio 2 MiB, oppure `_COSTI_BLOCCO` ridotto con un patch).
- **R-422-3 COSMETICA**: i commenti in gas.py:1260 («riga oltre 64 KB senza «\n»») e gas.py:1313 («oltre 64 KB non può essere una riga di _log_tokens») sono ormai falsi.

**Wall of Shame e guardrail**
- Niente slicing della history e niente simulazione di output dei tool: il codice nuovo tocca solo il log dei token e il registro della notte.
- Fail-safe §9: tutto resta dentro il try e il `except` con `logging.warning` di `_daily_cost_usd`. Il cap di 10 iterazioni e `_get_window` non sono toccati.

**Rischio escluso**: non ho verificato il comportamento su una VPS reale con un disco lento o poca RAM. Le misure (circa 0,09 s e 64 MiB di picco) vengono dal container di sviluppo. Non ho verificato nemmeno gli accessi concorrenti al log (scrittura di `_log_tokens` durante la lettura a blocchi): non è riproducibile in modo deterministico qui, e il diff non cambia l'aggiunta in coda al log.

**Memoria**: riga #422 aggiunta, con la lezione «quando si alza un tetto letto a blocchi, il test deve usare una riga più lunga di un blocco». Committata con scripts/commit_memoria_revisore.sh (commit 9533488, solo la memoria; l'index staged è rimasto intatto). Nello scratchpad restano file di sessioni precedenti (b, m, v, v415.md…v421.md), che non ho toccato.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/modules/notte/notte.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/tests/test_unit_notte.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #423 (chat Motore) — commit d718b5d

## VERDETTO: APPROVATO CON RISERVE

Review #423 (chat Motore). Ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (sezione R-422) e la mia memoria, poi ho esaminato il diff STAGED (gas.py, tests/test_unit_kernel.py). Il working tree coincide con lo staged.

**Elementi del diff esaminati**
- `gas.py:1284` — nel ramo `lunga`, quando la riga troppo lunga si chiude col suo «\n», ora scrive `logging.warning("log dei token: riga oltre %d byte ignorata")`. Rischio esaminato: avviso doppio o ripetuto. Esito: ok. Ho provato su una copia con blocco da 4 KB e tetto di 50 KB:
  - «\n» che chiude esattamente un blocco senza nient'altro dopo: 1 avviso, poi 0. Il caso non ne produce un secondo, perché `find == rfind` e quindi `righe` resta vuoto.
  - Stesso caso con una riga valida dopo: 1 avviso, conto 0.1.
  - Due righe lunghe di fila: 2 avvisi, poi 0.
  - Riga lunga finale senza «\n»: 0 avvisi a ogni chiamata (R-421-1 rispettata). Aggiungendo poi il «\n» si ha 1 avviso, poi 0.
  - Bordo: 50.000 byte la riga si conta; 50.001 byte si scarta con 1 avviso.
- `tests/test_unit_kernel.py:7202` (righe 7213 e 7216) — T94i con `_COSTI_BLOCCO = 4096` e `_RIGA_MAX = 50_000`, e ripristino nel finally. Rischi esaminati: la mutazione non viene presa, oppure lo stato globale patchato sporca gli altri test. Esito: ok.
  - Mutazione «accumulo a 65536» al posto di `_RIGA_MAX`: solo T94i FAIL (0.2 invece di 0.3), T94h passa. R-422-2 è chiusa.
  - Mutazione «avviso nuovo tolto»: T94i FAIL. R-422-1 è coperta.
  - Le globali sono lette dalla funzione al momento della chiamata, quindi la patch vale. Valori, handler e cache vengono ripristinati nel finally. La suite intera dà 968 PASS e 0 FAIL, riprodotti su una copia nello scratchpad (poi cancellata).
- `gas.py:1260` e `gas.py:1315` — i commenti «64 KB» ora dicono `_RIGA_MAX`. Esito: ok, R-422-3 chiusa.

**Riserva**
- R-423-1 (chat Motore), COSMETICA: T94i usa il logger root, quindi stampa i warning anche in console durante la suite. Inoltre non verifica che l'avviso sia uno solo: il controllo è `any(...)`, non un conteggio uguale a 1. Il caso di un solo avviso l'ho verificato con la sonda, non lo verifica il test.

**Rischio escluso**: non ho verificato il comportamento con i valori reali (blocco da 1 MiB, tetto di 16 MiB) né i tempi su file grandi. La logica è identica a scala ridotta, e i 36 casi da 70 KB a 20 MiB erano già stati provati nella review #422. Le altre suite (notte) non le ho rilanciate, perché il diff non le tocca.

**Memoria**: aggiunta la riga #423 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata solo quel file (commit 6609ca5). Lo staging è intatto (2 file, +30/-2). Non ho toccato HEAD oltre a quel commit.

### Review #424 (chat Motore) — commit 214a450

## VERDETTO: APPROVATO CON RISERVE

Review #424 (chat Motore) del diff STAGED (gas.py, modules/notte/notte.py, tests/test_unit_kernel.py, tests/test_unit_notte.py). Prima della review ho letto: CLAUDE.md (sez. 5), stato_progetto.md (righe sul budget e sulla notte) e la memoria del revisore.

**Prove fatte su una copia nello scratchpad (poi cancellata)**
- Ho controllato che la copia fosse uguale byte per byte al diff staged.
- Risultati: kernel 969 PASS / 0 FAIL, notte 129 passed. T79a fallisce solo se la copia non ha l'indice git; con l'indice popolato passa.
- Mutazioni:
  - con `invariato` forzato a False, T94j fallisce (1 chiamata invece di 0);
  - senza la riga di log in notte.py, `test_firme_scadute_chiuse_e_negli_avvisi` fallisce;
  - togliendo `and not invariato` dalla condizione di lettura i test **passano lo stesso** (969/0): vedi R-424-2.
- Sonda di equivalenza: 7.103 confronti tra «cache calda» e «cache vuota» su 300 sequenze casuali (righe aggiunte, righe tagliate senza «\n», «\n» aggiunti, file troncati, chiamate ripetute). Differenze: 0.

**Elementi esaminati**
- `gas.py:1265` — `invariato` vale solo se esiste `c["fin"]` con la stessa (dimensione, mtime_ns). Rischio: «fin» ereditato dopo un reset della cache. Esito ok: il reset (gas.py:1255-1257) crea un dizionario nuovo senza «fin», quindi `invariato` è False e il file si rilegge.
- `gas.py:1266` — salta la lettura dei blocchi se il file è invariato. Rischio: interazione col ramo `st_size == offset`. Esito ok: se il mtime cambia il reset c'era già; se è uguale, prima non si leggeva niente e ora `voce_fin` è None in cache. Sonda: 0,2/0,2/0,2 anche dopo `utime`, uguale alla lettura a cache vuota.
- `gas.py:1316` e `gas.py:1322` — riuso di `fin[2]`; altrimenti nuova decodifica e aggiornamento di `c["fin"]`. Rischio: stessa dimensione e stesso mtime che nascondono un cambiamento. Esito **riserva** (R-424-1): provato riscrivendo a mano l'ultima riga a parità di lunghezza e forzando lo stesso mtime_ns con `os.utime`. Risultato: 0,2 in cache contro 0,3 a cache vuota.
  - Con gli append normali non succede, perché la dimensione cambia sempre, e il valore si corregge al primo append successivo.
  - Su ext4 lo mtime ha risoluzione di pochi millisecondi. Il caso diventa realistico solo su filesystem con risoluzione di 1 secondo e con una modifica a mano della riga finale fatta nello stesso secondo.
  - È la stessa fiducia che il codice dava già alle righe complete (contro le modifiche sul posto protegge solo l'impronta di testa e di coda).
- `gas.py:1327` — il cutoff delle 24 ore si riapplica a ogni chiamata anche alla voce in cache. Rischio: una voce scaduta che resta contata. Esito ok.
  - Nota: una riga finale con data oltre 7 giorni nel futuro resta in cache come None anche quando rientra nei 7 giorni, mentre prima veniva rivalutata a ogni chiamata. Ora si comporta come le righe complete; la metto in R-424-1.
- `modules/notte/notte.py:718` — l'avviso «firme scadute» va anche in gas_debug.log, dopo l'append all'elenco degli avvisi. Rischio: messaggio doppio con il ciclo `for a in avvisi` di notte.py:664-665. Esito ok: quel ciclo viene prima delle firme scadute; il test conta esattamente una riga (`tests/test_unit_notte.py:1207`).
- `tests/test_unit_kernel.py:7225` — R-423-1: l'avviso in T94i ora è contato `== 1`. Esito ok. Il logger root che stampa in console non è stato toccato; era COSMETICA, accettabile.
- `tests/test_unit_kernel.py:7247` — T94j. Esito **riserva**:
  - R-424-2: conta le decodifiche (`_costo_riga`), non le letture. La promessa di V-1, «a file invariato non si legge niente», non è protetta: se si toglie `and not invariato` alla riga 1266 il file torna a essere riletto (fino a 16 MiB) a ogni chiamata e la suite resta verde.
  - R-424-3: dopo il «\n» il test non controlla che `_costo_riga` venga chiamata una volta sola. Il totale di 0,2 esclude solo il doppio conteggio.

**V-3 della verifica esterna (in_corso.json senza blocco): SMENTITA.**
- `modules/notte/notte.py:635` prende un `flock` LOCK_EX non bloccante. Se il lock è occupato il giro esce con 2; se il filesystem non supporta flock, l'errore viene rilanciato e il giro esce con 1 senza toccare il registro.
- Il lock resta aperto fino al `finally` (notte.py:742-745).
- Le uniche letture e scritture di in_corso.json sono alle righe 653, 658, 703 e 706, tutte dopo il lock. Nel repo nessun altro scrive quel file (grep).
- Due giri sovrapposti sulla stessa root si escludono. Con root diverse i file in_corso.json sono diversi.
- Unico buco teorico: `fcntl is None` (Windows), che non è un ambiente di destinazione.

**Riserve da tracciare in stato_progetto.md**
- R-424-1 (chat Motore) BASSA: se l'ultima riga senza «\n» viene riscritta a mano con la stessa lunghezza e lo stesso mtime_ns, il valore resta vecchio finché non arriva un append. Lo stesso per una riga finale con data oltre 7 giorni nel futuro, che resta scartata anche quando rientra nei 7 giorni (come le righe complete).
- R-424-2 (chat Motore) BASSA: T94j non protegge il «niente lettura»; la mutazione su gas.py:1266 sopravvive.
- R-424-3 (chat Motore) COSMETICA: T94j non conta le chiamate a `_costo_riga` dopo il «\n».

Nessuno slicing della history: i `[-64:]` sono byte del log. Nessuna simulazione di tool, guardrail invariati. Le eccezioni restano intercettate dal `try/except` esterno, che scrive un warning e restituisce 0.0.

**Rischio escluso**: non ho verificato il comportamento reale dello mtime su un filesystem della VPS con risoluzione di 1 secondo (o NFS), perché non è riproducibile qui. L'ho solo simulato con `os.utime`. Non ho misurato tempi o memoria della lettura evitata, ho solo contato le decodifiche.

**Memoria**: riga #424 aggiunta e committata (commit 06da7ac, solo /home/user/Gas/.claude/agents/memoria_revisore.md). Il resto dello staging è intatto. Lezione nuova: un test che promette «niente lavoro» deve contare l'operazione costosa promessa (qui la lettura del file), non solo quella a valle.

### Review #425 (chat Motore) — commit 52501e2

## VERDETTO: APPROVATO CON RISERVE

Review #425 (chat Motore). Ho letto CLAUDE.md (sezioni 5, 8 e 9), le voci R7, R-222-2 e R-424 in reports/stato_progetto.md e le ultime righe e lezioni di .claude/agents/memoria_revisore.md. Le prove le ho fatte su una copia nello scratchpad, poi cancellata. Nel repo reale ho committato solo la memoria (commit ef8a5dd). I quattro file staged sono rimasti intatti.

Elementi del diff esaminati:
- gas.py:3840 — `_esito_contenuto` viene azzerato all'ingresso di execute_tool_call. Rischio esaminato: un valore residuo da una chiamata precedente. Esito: ok. L'azzeramento avviene a ogni chiamata, prima del try.
- gas.py:3995 — `_esito_contenuto` diventa True solo all'uscita normale. Rischio esaminato: un diniego del kernel che passa da quell'uscita e quindi smette di essere contato. Esito: ok.
  - run_command: i dinieghi tornano tutti prima (vetting, os_strict, snapshot); il dry-run comincia con «[DRY-RUN]».
  - read_file: il diniego di `_risolvi_lettura` torna prima.
  - ricorda: il testo comincia sempre col blocco dati della memoria, mai con «Operazione negata».
  - Lettori nativi: `_lettura_meta` viene azzerato nel ramo prima della chiamata (gas.py:3970). Ho controllato tutti i dinieghi (gas.py:2329-2353 dispatcher, gas.py:2355 _elenca_cartella, gas.py:2398 _leggi_righe, gas.py:2431 _cerca_testo, `_conta_file` subito sotto): tornano tutti PRIMA che il meta venga impostato. Dopo il meta c'è solo la costruzione della stringa finale, che non può fallire in modo realistico; anche un'eccezione a quel punto verrebbe catturata dal try del dispatcher.
- gas.py:4194-4229 — `_cancello` in run_turn. Rischio esaminato: classificazione sbagliata nei tre rami. Esito: ok.
  - DENY → "negata".
  - Parcheggio: «Azione in attesa…» → in_attesa; «Operazione negata…» (anche `_NEGATO_STORE` e la revoca) → negata; «Azione già in attesa» → None, come prima.
- gas.py:4261 — chiave nuova nell'evento tool_res. Rischio esaminato: altri consumatori che si rompono. Esito: ok. modules/telegram/bot.py:616, la CLI (gas.py:5442) e modules/voice/server.py:158 leggono solo "output" o ignorano l'evento. Nessun test confronta il dizionario intero.
- modules/notte/notte.py:262 — usa `ev["cancello"]` se c'è, altrimenti il vecchio prefisso. Rischio esaminato: regressione con i kernel finti dei test. Esito: ok, notte 130 passed.
- tests/test_unit_kernel.py:7238-7266 — T94j: patch di `gas.open` e `del gas.open` nel finally. Rischio esaminato: (a) il `del` cancella un `open` vero del modulo; (b) la patch non intercetta le letture. Esito: ok. gas.py non ha un `open` a livello di modulo, e la lettura usa l'`open` builtin (gas.py:1269). Il tetto di 128 byte corrisponde alle due impronte da 64 byte (gas.py:1244 e gas.py:1252).
- tests/test_unit_notte.py:1195 — test nuovo R-222-2. Esito: ok. La lettura «../fuori.txt» passa davvero dal ramo DENY del cancello: la mutazione lo conferma.

Prove sulla copia:
- Suite: kernel 969 PASS 0 FAIL, notte 130 passed.
- Mutazioni:
  - senza «and not _esito_contenuto» → FAIL del test nuovo;
  - DENY senza `_cancello="negata"` → FAIL del test nuovo;
  - parcheggio senza "negata" → FAIL di test_irreversibile_parcheggiato_non_eseguito;
  - «and not invariato» tolto da gas.py:1266 → T94j FAIL (246 byte letti; R-424-2 chiusa).
- R-424-3: `_n94j3 == 1` controlla che dopo il «\n» la riga venga decodificata una volta sola. Chiusa.
- Wall of Shame: nessun taglio della storia, nessuna simulazione di output dei tool, cap e guardrail non toccati.

Riserve:
- **R-425-1 (chat Motore), BASSA**: la mutazione «parcheggio senza `_cancello = "in_attesa"`» sopravvive (kernel 969/0, notte 130). Nessun test con un kernel vero produce «in attesa ≥ 1»; l'unico che lo verifica (tests/test_unit_notte.py:388) usa un kernel finto senza la chiave.
- **R-425-2 (chat Motore), COSMETICA**: `_esito_contenuto` non è dichiarato in `__init__` (lo si legge con getattr). È stato tenuto per istanza come `_lettura_meta` e `_run_command_meta`, quindi non è sicuro se due turni girano insieme sullo stesso kernel. Il problema c'era già prima.

Rischi esclusi:
- Concorrenza reale bot/notte sullo stesso kernel: non riprodotta, è un problema già esistente.
- Suite dei gate (817): non rieseguita, perché il diff non tocca gli script dei gate.
- Comportamento su VPS: non verificato, non riproducibile in dev.

Memoria: aggiunta la riga #425 (lezione: quando un flag si decide all'uscita normale, cercare i rami che impostano il meta e dopo possono ancora negare o sollevare eccezioni). Commit ef8a5dd in /home/user/Gas/.claude/agents/memoria_revisore.md.

### Review #426 (chat Motore) — commit efd2294

## VERDETTO: APPROVATO CON RISERVE

Review #426 (chat Motore) del diff in staging (gas.py e tests/test_unit_kernel.py, +54 righe). Ho letto prima CLAUDE.md (sez. 5, 8 e 9), la parte di reports/stato_progetto.md sul budget e su R7, e la memoria del revisore. Le prove le ho fatte su una copia nello scratchpad, poi cancellata.

**Elementi del diff esaminati**
1. `gas.py:868` — `_COSTI_LOCK = threading.Lock()` a livello di modulo. Rischio esaminato: un lock non rientrante può bloccarsi se qualcuno lo riprende mentre lo tiene già, o se il processo viene sdoppiato con fork. Il corpo non rientra in `_daily_cost_usd`: chiama solo `logging.warning`, che usa gli handler standard (StreamHandler e RotatingFileHandler, nessuno personalizzato), e `_costo_riga`, una funzione pura. Il codice non usa né `os.fork` né multiprocessing. Esito: ok.
2. `gas.py:1234` — `_daily_cost_usd` prende il lock e chiama `_daily_cost_usd_bloccato`, cioè il corpo di prima senza modifiche. Rischio esaminato: chiamanti che hanno già il lock e modifiche della cache fatte fuori dal lock. L'unico chiamante è `_budget_superato` (`gas.py:1351`), che non ha il lock in mano. Tutte le modifiche a `_COSTI_CACHE` (pop, get, assegnazione) stanno dentro il corpo protetto. Il `try/except` che rende la funzione fail-safe resta dentro il corpo, quindi il lock si rilascia sempre col `with`. Esito: ok. C'è una riserva BASSA (R-426-2), sotto.
3. `tests/test_unit_kernel.py:7271` — T94k. Rischio esaminato: il test potrebbe non ripristinare blocco e switch interval, essere lento o instabile in CI. Il `finally` rimette `_COSTI_BLOCCO`, lo switch interval e la cache, e l'ho verificato con un assert a ogni giro. Ho lanciato T94k da solo 30 volte: 30 su 30 corretti, 0,04 s in media, 0,06 s al massimo. Su una sola CPU (taskset): 20 su 20. Con il lock tolto (sostituito da nullcontext) fallisce sempre: 5 su 5, e 3 su 3 su una CPU. Il test quindi blocca davvero l'errore e non è instabile. Esito: ok.
4. `tests/test_unit_kernel.py:7298` — T96 con kernel vero. Mutazioni provate: (a) `_cancello` di «in attesa» messo a None, per cui il parcheggio esce senza «in_attesa»: T96 FAIL, quindi R-425-1 è chiusa; (b) `_esito_contenuto` sempre False (`gas.py:4003`): T96 FAIL, perché il file letto viene etichettato «negata». Esito: ok.
5. `gas.py:952` — `self._esito_contenuto = False` aggiunto in `__init__`. Rischio esaminato: la riga serve davvero? Togliendola la suite resta 971 PASS e 0 FAIL, perché `gas.py:4236` la legge ancora con `getattr(..., False)`. Esito: riserva COSMETICA (R-426-1).

**Riprodotto sulla copia**: test del kernel 971 PASS, 0 FAIL. pytest su tutta `tests/`: 1711 passed in 186 s, che include notte e gate (le tue 947).

**Riserve**
- **R-426-1 (chat Motore) COSMETICA**: la dichiarazione in `__init__` serve solo come documentazione. Il getattr con default in `gas.py:4236` la rende superflua, e nessun test se ne accorge se la si toglie. Se vuoi che conti, il getattr si può sostituire con l'attributo diretto.
- **R-426-2 (chat Motore) BASSA, da dichiarare**: il lock è uno solo per tutti i log dei token, di qualsiasi kernel, e resta preso durante la lettura del file. Una prima lettura di un log grande (circa 1,7 s con 2 milioni di righe, come misurato nella #419) mette in attesa i `_budget_superato` degli altri thread, per esempio Telegram e voce. Non produce errori di conteggio né blocchi permanenti: è solo latenza.

**Rischio escluso**: non ho verificato il comportamento con Python free-threaded (3.13t) né sul VPS. Il primo non è nel piano, il secondo non si riproduce in sviluppo. Non ho misurato la contesa reale del lock sotto carico Telegram più voce: in sviluppo non ci sono turni concorrenti veri.

**Wall of Shame**: nessuno slicing della history e nessun output dei tool simulato. Nel test i tool passano dal vero `execute_tool_call` attraverso `run_turn_scriptato`. Cap e `_get_window` non sono toccati.

**Memoria**: aggiunta la riga #426 in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (cf1915e). Lo staging di gas.py e dei test è rimasto com'era. Nessuna lezione nuova.

### Review #427 (chat Motore) — merge d6cc1cd — verdetto originale

(Testo integrale, in un blocco di codice perché le sue citazioni puntano a file usciti dal diff di sessione dopo il merge; fa fede per il gate il verdetto riemesso qui sotto.)

```text
## VERDETTO: APPROVATO

Review #427 (chat Motore): merge in corso di origin/main 0616d3a (PR #235, chat Mani) dentro feat/merge-automatico-z1xjx2. Prima della review ho fatto le letture obbligatorie: CLAUDE.md e la coda di .claude/agents/memoria_revisore.md. Di reports/stato_progetto.md ho letto solo le parti toccate dal merge.

**Elementi del diff esaminati**
- `.claude/agents/memoria_revisore.md:630` — righe della chat Mani (#391/#392/#393) inserite tra le #391–#393 della chat Motore. Rischio esaminato: righe perse o duplicate nella risoluzione. Ho confrontato riga per riga HEAD (666 righe), MERGE_HEAD (649) e staged (672):
  - nessuna riga di HEAD manca nello staged;
  - nessuna riga di main manca;
  - nessun duplicato (righe vuote escluse);
  - nessuna riga estranea a entrambi.

  666 + 6 righe Mani (#391, #392, #393, #406, #407, #408) = 672. I numeri uguali sono distinti dalle etichette «(chat Mani)»/«(chat Motore)». Esito: ok.
- `.github/workflows/ci.yml:113` — passo «Run web suite» (`if: always()`, `pipefail`, `tests/test_unit_web_*.py`) dentro il job `unit-suite` (riga 24; `handoff-check` resta a riga 282). Rischio esaminato: test web non lanciati, oppure check required alterati. Il ci.yml staged è identico a quello di MERGE_HEAD (diff vuoto). Il ramo non tocca ci.yml dalla merge-base 7bd0875, quindi non c'era conflitto reale. Nomi dei job required invariati. Esito: ok.
- `modules/web/leggi.py:20` — import del modulo (riga 20 `from __future__`, poi righe 22–36): solo libreria standard (http.client, ssl, socket, ipaddress, html.parser…). Rischio esaminato: scontri col ramo. Nessun import da gas.py, notte, gate, memory o telegram, e nessuno di questi importa `modules.web` o `leggi_pagina` (grep vuoto). Raccolta pytest dell'intera cartella tests: 1796 test (1711 + 85) senza collisioni di nomi né problemi con tests/conftest.py. Rieseguiti i soli web: 85 passed. Esito: ok.
- `reports/stato_progetto.md:605` — paragrafo «Mani — fetta 1» aggiunto dopo il blocco della chat Motore. La riga 601 (R1 giro da Telegram) è la versione del ramo, più aggiornata di main. Esito: ok.
- `reports/stato_progetto.md:4` — nell'intestazione «Ultimo aggiornamento» il 2026-10-21 ora cita solo la PR #235 (chat Mani). Il lavoro della chat Motore dello stesso giorno non è nominato, ma la riga di HEAD era già ferma al 20. Esito: cosmetico, non blocca. Puoi correggerlo nell'aggiornamento di fine task.

**Rischio escluso**
- Non ho rieseguito la suite kernel (971/0) né l'intera suite pytest sul tree unito: mi fido del tuo dato «kernel 971 PASS 0 FAIL, web+notte+gate 1032 passed». Ho verificato solo la raccolta dei test e i 85 test web.
- Non ho verificato l'esito della CI su GitHub: il merge non è ancora pushato.
- Non ho riesaminato la logica di sicurezza di leggi_pagina (SSRF, timeout): è già stata revisionata dalla chat Mani (review #391–#393 e #406–#408 Mani) e il merge non la modifica.

**Memoria del revisore**
La riga contatore #427 (chat Motore) è stata aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, ma NON è committata. `scripts/commit_memoria_revisore.sh` ha fallito senza bloccare (rc 0, warning in gas_debug.log: «fatal: cannot do a partial commit during a merge»). Il merge è ancora in corso (MERGE_HEAD presente) e l'index degli altri file è intatto. Il file risulta `MM`: prima del commit di merge devi fare `git add .claude/agents/memoria_revisore.md` per includere la riga.
```

### Review #427 (chat Motore) — verdetto RIEMESSO dal revisore con le citazioni nella forma del gate (stesso esito; la base della sessione è passata a 0616d3a dopo il merge)

## VERDETTO: APPROVATO

Review #427 (chat Motore), versione riemessa con citazioni nel diff di sessione `0616d3a..HEAD`: merge in corso di origin/main 0616d3a (PR #235, chat Mani) dentro feat/merge-automatico-z1xjx2. L'esito è lo stesso; ho aggiunto i punti del codice del ramo controllati per gli scontri con modules/web. Prima della review ho fatto le letture obbligatorie: CLAUDE.md e la coda di .claude/agents/memoria_revisore.md. Di reports/stato_progetto.md ho letto solo le parti toccate dal merge.

**Elementi esaminati nel diff di sessione**
- `gas.py:21` — import del kernel (`modules.memory`, `brains.model_ids`, poi `modules.gate.gate` a :28–:30, `modules.telegram` a :31). Rischio esaminato: scontro di nomi o di import col nuovo package modules/web. gas.py non importa `modules.web` e non nomina `leggi_pagina` (grep vuoto). Il tool non è registrato nel kernel, quindi il merge non tocca il percorso di run_turn. Esito: ok.
- `modules/gate/gate.py:82` — `UNTRUSTED_INPUT_TOOLS`. Rischio esaminato: incoerenza tra il gate del ramo e il nuovo lettore web. Oggi `leggi_pagina` non è un tool del loop, quindi la sua assenza dalla lista è coerente. Le uniche occorrenze di «web» in gate.py (`modules/gate/gate.py:553`, `modules/gate/gate.py:571`) sono commenti ed estensioni di file, nessun legame col modulo. Esito: ok, con una nota per il futuro: quando `leggi_pagina` diventerà un tool del loop, dovrà entrare in `UNTRUSTED_INPUT_TOOLS`.
- `modules/notte/notte.py:80` — import della notte (riga 80 `from __future__`, poi righe 82–91, solo libreria standard). Rischio esaminato: dipendenze incrociate con modules/web. Non ce ne sono, e nessun riferimento a web in notte.py né in `modules/memory/store.py` (grep vuoto). Esito: ok.
- `tests/test_unit_kernel.py:1` — la suite kernel del ramo convive con tests/test_unit_web_leggi.py. Rischio esaminato: collisioni di nomi di test o di conftest. Raccolta pytest dell'intera cartella tests: 1796 test (1711 + 85) senza errori. Rieseguiti i soli test web: 85 passed. Esito: ok.
- `.claude/agents/memoria_revisore.md:630` — righe Mani inserite tra le #391–#393 della chat Motore. Rischio esaminato: righe perse o duplicate nella risoluzione. Ho confrontato riga per riga HEAD (666 righe), MERGE_HEAD (649) e staged (672):
  - nessuna riga di HEAD manca nello staged;
  - nessuna riga di main manca;
  - nessun duplicato;
  - nessuna riga estranea a entrambi.

  666 + 6 righe Mani (#391, #392, #393, #406, #407, #408) = 672. Esito: ok.
- `reports/stato_progetto.md:605` — paragrafo «Mani — fetta 1» aggiunto. La riga 601 (R1 giro da Telegram) è la versione del ramo, più aggiornata di main. Esito: ok.
- `reports/stato_progetto.md:4` — nell'intestazione il 2026-10-21 cita solo la PR #235. Esito: cosmetico, da sistemare nell'aggiornamento di fine task.

**Controlli di contesto (file non nel diff di sessione)**
- `.github/workflows/ci.yml:113` — passo «Run web suite» (`if: always()`, `pipefail`, `tests/test_unit_web_*.py`) nel job `unit-suite` (riga 24); `handoff-check` resta a riga 282. Il ci.yml staged è identico a quello di main e il ramo non lo tocca dalla merge-base 7bd0875. Check required invariati. Esito: ok.
- `modules/web/leggi.py:20` — solo libreria standard, nessun import del kernel, della notte, del gate o dello store. Esito: ok.

**Rischio escluso**
- Non ho rieseguito la suite kernel (971/0) né l'intera suite pytest sul tree unito: mi fido del dato del chiamante. Ho verificato solo la raccolta dei test e i 85 test web.
- Non ho verificato l'esito della CI su GitHub: il merge non è ancora pushato.
- Non ho riesaminato la logica di sicurezza di leggi_pagina (SSRF, timeout): è già revisionata dalla chat Mani e il merge non la modifica.

**Memoria del revisore**
La riga #427 è già in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` dal primo passaggio; come chiesto, non ho toccato né il repo né la memoria. La riga NON è committata: `scripts/commit_memoria_revisore.sh` non può fare un commit parziale durante un merge. Prima del commit di merge devi fare `git add .claude/agents/memoria_revisore.md` per includerla.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 957 → 971 PASS, 0 FAIL (T94a-k, T94e2, T95, T96). Blocco reale: `=== RIEPILOGO: 971 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py`: 106 → `130 passed`; `tests/test_unit_gate.py`: 811 → `817 passed`.

## §6 STATO CI

- 5267148: handoff-check, unit-suite success; verifica-bot neutral (APPROVATO CON RISERVE).
- 9d793f3: unit-suite success, handoff-check success (verifica esterna #234 2° giro); verifica-bot neutral (APPROVATO CON RISERVE).
- ab60f35: handoff-check failure (pushato senza il dossier, per l'HEAD staccato da un agente di verifica); superato dal commit successivo.
- 2d07cd3: unit-suite success (kernel 964 PASS in CI), handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE) — dal verdetto del bot.
- 0a11a8b (con a86f493, 5142d8f e memorie): run non letta (nessun evento ricevuto prima della scrittura).
- 0a11a8b: verifica-bot failure (il bot ha letto come riserva la frase «nessuna ALTA/MEDIA aperta» della descrizione; testo del verdetto APPROVATO CON RISERVE con V-1 BASSA, ora chiusa da d9f58bb).
- 01bf064 (con 3a43d93, 5999fdb, f2c3e29 e memorie): run non letta prima della scrittura.
- 8e3072b (con d9f58bb): verifica-bot neutral (APPROVATO CON RISERVE, V-1/V-2 basse poi chiuse); check suite completata.
- eb869d2 (con 898a4a2, 7204835, 3701278 e memorie): check suite completata senza check falliti (evento GitHub).
- 0c02776 (con 9f470a9, 9533488, 373542f): check suite completata senza check falliti (evento GitHub); verifica-bot neutral (APPROVATO CON RISERVE, V-1 BASSA chiusa da 214a450).
- 6160555 (con d718b5d, 6609ca5, 214a450, 06da7ac): unit-suite, handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, nessuna riserva ALTA/MEDIA).
- 47b3957 (con ef8a5dd, 52501e2): unit-suite success (kernel 971 PASS), handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, nessuna ALTA/MEDIA).
- 634eba9 (con cf1915e, efd2294): unit-suite, handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE).
- d6cc1cd (merge di main): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-408-1 (BASSA): potatura del registro spenta da qualsiasi avviso del catalogo.
- R-408-2 (COSMETICA): read_file su «.» negato invece di «è una cartella».
- Limite dichiarato (#406): la ripresa riparte da capo con la nota, non rilegge la storia parziale del compito.
- R-411-2 (BASSA): conteggio enorme scritto a mano conta 0.
- V-3 verifica esterna #234 (BASSA, dichiarata): un Ctrl-C dell'operatore conta come crash.
- R-412-1 (BASSA): si tengono le prime 12 parole della ricerca.
- R-412-2 (COSMETICA): T95 parziale.
- R-414-1/2 (BASSE), R-414-3 (COSMETICA): orologio indietro, coda senza a capo riletta, messaggio di T94a.
- R-415-3, R-416-2, R-417-2, R-418-1 (COSMETICHE).
- R-418-2 (BASSA): compito in coda fermato dal tetto di tempo resta a tentativi 2.
- R-423-1: chiusa in #424.
- R-424-1 (BASSA): riga finale riscritta a mano con stessa lunghezza e stesso mtime resta col valore vecchio fino al prossimo append.
- R-424-2/3: chiuse in #425.
- R-425-1/2: chiuse in #426.
- R-426-1 (COSMETICA): la dichiarazione in `__init__` è solo documentazione (getattr con default).
- R-426-2 (BASSA, dichiarata): un solo lock per tutti i log dei token: una prima lettura lunga fa aspettare gli altri thread (solo latenza).
- Residuo dichiarato: orologio indietro di oltre 7 giorni → quella spesa esce dal tetto per 24 ore.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
