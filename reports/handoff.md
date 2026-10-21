# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #233) — compiti notturni che riprendono dopo un crash (R7/M3 fetta 1), piccole riserve

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della nuova PR del ramo `feat/merge-automatico-z1xjx2` (numero e URL dall'API GitHub alla creazione; `gh` non usato): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).
2. C6 (bottone «Modifica» e firme a gruppi): decisione dell'operatore.

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #233**: `FATTA` — su richiesta dell'operatore («mergia 233»), merge `7bd0875`.
- **R7/M3 fetta 1 — ripresa dei compiti dopo un crash**: `FATTA` — review #406, #407 (chat Motore) APPROVATO CON RISERVE.
- **Riserve R-407-1/2, R-405-1/2, R-404-2**: `FATTA` — review #408 APPROVATO CON RISERVE.
- **C6**: `SALTATA` — decisione dell'operatore.
- **R7 — ripresa dal punto esatto**: `DEFERITA` — da valutare.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 ++
 modules/gate/gate.py               |  12 ++++++-
 modules/notte/notte.py             | 106 +++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/da_mergiare.md             |  75 +++++++---------------------------------
 reports/diff_sessione.md           |  14 +++-----
 reports/handoff.md                 | 680 +++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  34 ++++++------------
 tests/test_unit_gate.py            |   8 +++++
 tests/test_unit_notte.py           | 168 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed, 414 insertions(+), 688 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 957 → 957 PASS, 0 FAIL (nessun test kernel nuovo). Blocco reale: `=== RIEPILOGO: 957 PASS, 0 FAIL ===`.
pytest `tests/test_unit_notte.py`: 106 → `119 passed`; `tests/test_unit_gate.py`: 811 → `817 passed`. `test_riepilogo_telegram_inviato_a_lock_rilasciato`: 25 run su 25 verdi dopo il fix.

## §6 STATO CI

Run sui commit di questa sessione (6eaab53, d51de97, bb9305e e memorie): non ancora disponibile alla scrittura dell'handoff (il ramo non era ancora stato pushato). L'esito si legge sulla PR.

## §7 RISERVE APERTE

- R-408-1 (BASSA): potatura del registro spenta da qualsiasi avviso del catalogo.
- R-408-2 (COSMETICA): read_file su «.» negato invece di «è una cartella».
- Limite dichiarato (#406): la ripresa riparte da capo con la nota, non rilegge la storia parziale del compito.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
