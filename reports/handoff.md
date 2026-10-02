# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-02 — Fetta C3 cancello: coda approvazioni SQLite (feat/cancello-c3)

---

## §0 DECISIONI UMANE RICHIESTE

1. Gate B `check_verdetto.py` rosso sul §4 verbatim (path abbreviati `store.py:…` e `gas.py:1948` fuori diff). Verdetto NON ritoccato per istruzione operatore → report non committati, branch non pushato. Scegliere: accettare/bypassare, far ri-emettere il verdetto con path completi, o correggere prima check_verdetto.
2. PR NON verificata/creata: branch `feat/cancello-c3` non pushato (STOP al gate §4). `gh pr list --head feat/cancello-c3 --base main` → `[]`.
3. PR #109: superata da #110 — merge/chiusura a discrezione dell'operatore.
4. Mini-fetta R-c3-1 prima di C4; poi C4 (rimozione stub C2, turno di sblocco, Telegram).

---

## §1 SCOPE & ESITO FETTE

- **Step 0 — Sonda**: `FATTA` — #109 OPEN e superata da #110; spec §C3 letta; stub C2 a gas.py:1947-1952.
- **Step 1 — Doc stato_progetto**: `FATTA`
- **Step 2 — Implementazione §C3 (solo store.py, scope spec)**: `FATTA`
- **Step 3 — Test reali T73a-g**: `FATTA` — 423→463 PASS, 5 FAIL F-mac-1 invariati.
- **Step 4 — Revisore Opus**: `FATTA` — review #125 APPROVATO CON RISERVE.
- **Commit/push report + PR**: `DEFERITA — gate check_verdetto rosso sul verdetto verbatim; STOP per istruzione operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 modules/memory/store.py            | 288 +++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  34 ++---
 reports/handoff.md                 | 248 +++++++++++++++-----------------
 reports/stato_progetto.md          |   4 +
 reports/ultimo_report.md           |  56 ++++----
 tests/test_unit_kernel.py          | 251 ++++++++++++++++++++++++++++++++
 7 files changed, 700 insertions(+), 183 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
4f16a65 feat(cancello-c3): coda approvazioni SQLite in store.py (review #125 APPROVATO CON RISERVE)
aa0b0d0 chore(revisore): memoria review #125 — APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore `4f16a65` — verdetto integrale review #125:

## Verdetto review #125 — Fetta C3, coda approvazioni SQLite (branch feat/cancello-c3, diff staged)

**ESITO: APPROVATO CON RISERVE**

Prima di iniziare ho letto quanto previsto: CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (letto in modo mirato), la mia memoria (.claude/agents/memoria_revisore.md, fino alla #124) e le sezioni di design_cancello.md che servivano: §4a–§4f, §C3–§C5 e §8c/§8d.

Ho rilanciato la suite: `tests/test_unit_kernel.py` dà **463 PASS / 5 FAIL**. I 5 FAIL sono quelli già noti di F-mac-1 (T11c2, T11e, T12a, T12c, T12e: manca bwrap su macOS). Tutti i 40 check T73 sono verdi. Le sonde sugli edge case le ho fatte con uno script nello scratchpad, senza toccare il repo.

### Elementi del diff esaminati

1. `modules/memory/store.py:182` (tabella `approvals`) e `:224` (trigger `approvals_payload_immutabile`), più gli altri 3 trigger: una richiesta nasce solo `pending`, la DELETE è vietata, lo stato non cambia più dopo la risoluzione, il payload non cambia mai.
   - Rischi esaminati: aggiramento con SQL grezzo e con `INSERT OR REPLACE`.
   - `recursive_triggers = ON` era già attivo in `_connect` (store.py:421), quindi il percorso REPLACE→DELETE resta bloccato. Questo lo coprono T73c (store.py:5131 non esiste: il test è a tests/test_unit_kernel.py:5131) e T73b.
   - Esito: **ok**.
2. `modules/memory/store.py:1500` (`BEGIN IMMEDIATE` dentro `with self._connect()`), insieme a `WHERE stato='pending'` e al controllo `rowcount != 1`. Le funzioni toccate sono resolve, expire e il ramo di revoca.
   - Rischi esaminati: doppia risoluzione e race tra due callback.
   - Il blocco di scrittura immediato più l'UPDATE condizionato rendono la risoluzione idempotente. Un `return` dentro il `with` va bene: chiude la transazione con commit o rollback.
   - Esito: **ok**.
3. `modules/memory/store.py:1469` (`hash_args(d["tool_args_json"])` in get_approval) e `:1511` (`now >= row["ts_expiry"]` in resolve_approval).
   - Rischio esaminato: coda corrotta, che secondo il contratto deve dare "mai eccezione".
   - **Riprodotto**: se una riga viene inserita con SQL grezzo con `tool_args_json` di tipo BLOB, sia get_approval sia resolve_approval sollevano `AttributeError: 'bytes' object has no attribute 'encode'`. Se `ts_expiry` è TEXT, resolve_approval solleva `TypeError`.
   - Con `ts_expiry` TEXT la riga resta inoltre per sempre in get_pending_approvals (in SQLite TEXT > REAL) e expire_stale_approvals non la fa mai scadere.
   - Gli except prendono solo `(sqlite3.Error, OSError)`.
   - L'esito resta fail-closed (nessuna approvazione concessa), ma l'eccezione arriva al chiamante, cioè al thread del bot in C4.
   - Esito: **riserva R-c3-1**.
4. `modules/memory/store.py:1446` (`now + timeout_secs`).
   - Rischio esaminato: parametro `timeout_secs` non validato.
   - Riprodotto: con `timeout_secs="10"` si ha un `TypeError` non intercettato; con `float("inf")` la richiesta non scade mai.
   - Il parametro lo passa il kernel, non il modello.
   - Esito: **riserva R-c3-2** (minore).
5. `modules/memory/store.py:1490` (whitelist di `risolto_da`).
   - Rischio esaminato: correttezza del dato di audit.
   - Riprodotto: `resolve_approval(id, "approved", 1, risolto_da="kernel_revoca")` restituisce `(True, '')`, cioè un'approvazione registrata come revoca del kernel. In più `rejected` accetta `telegram_user_id="pippo"`, che viene salvato come testo.
   - Esito: **riserve R-c3-3 e R-c3-4** (minori).
6. `tests/test_unit_kernel.py:5203-5204` (T73e: DB corrotto, tabella assente, file sparito) e `:5262` (T73g, round-trip agentico §7).
   - Rischi esaminati: test reali o mockati, e se discriminano davvero.
   - Il DB è un vero SQLite in una directory temporanea, senza alcun mock della coda. T73g esegue 2 tool call reali più la risposta finale e verifica che la richiesta resti `pending`.
   - Nessun test copre le righe con tipo sbagliato (vedi R-c3-1).
   - Esito: **ok**.
7. `tests/test_unit_kernel.py:5247` (T73f) e verifica diretta del codice.
   - Rischio esaminato: un tool di approvazione esposto al modello.
   - `grep approv gas.py` trova solo il commento dello stub C2 (gas.py:1948), che non è nel diff e resta fino a C4 come deciso dall'operatore.
   - Non c'è nessun tool di approvazione in tools_schema né in GATE_ALLOWLIST, e `execute_tool_call` risponde "Tool non trovato.".
   - Esito: **ok**.

Ho controllato il Wall of Shame: il diff non fa slicing della history e non simula output dei tool. Rispetta "zero gas.py", come da scope deciso.

### Riserve (da tracciare in stato_progetto.md)

- **R-c3-1 (media, da chiudere PRIMA di C4)**: va reso vero il contratto "coda corrotta → mai eccezione" per righe con tipi sbagliati (store.py:1469, :1511). Ci sono due strade: aggiungere allo schema `CHECK(typeof(tool_args_json)='text')` e `CHECK(typeof(ts_expiry) IN ('real','integer'))` (la tabella è nuova, quindi non serve migrazione), oppure intercettare `TypeError`/`AttributeError` sui valori letti. Serve anche un test con INSERT grezzo di tipi sbagliati.
- **R-c3-2 (minore)**: validare `timeout_secs` (intero finito; altrimenti default e WARN).
- **R-c3-3 (minore)**: `approved` deve richiedere `risolto_da == "telegram_user"`.
- **R-c3-4 (minore)**: anche `rejected` dovrebbe pretendere `telegram_user_id` intero o None.
- **R-c3-5 (cosmetica)**: get/resolve/pending/expire non controllano `self.available`. Se il file sparisce, `sqlite3.connect` ricrea un `.db` vuoto senza schema (riprodotto). Non porta a crash: l'errore viene intercettato e si ha un diniego.

### Rischi esplicitamente esclusi

- **Concorrenza reale multi-processo** (due processi che risolvono nello stesso istante): non l'ho verificata con un test. La valutazione si basa solo sulla lettura del codice (`BEGIN IMMEDIATE`, `timeout=10`, `WHERE stato='pending'`). Il bot Telegram che la eserciterebbe non esiste ancora (C4).
- **Comportamento su VPS/Linux**: non riproducibile in dev su macOS, lo copre la CI.
- **Limite di read-back Telegram (~4096 caratteri, §4c)**: fuori scope, riguarda C4 come deciso dall'operatore.

### Memoria del revisore

Ho aggiunto in `/Users/gas/Gas/.claude/agents/memoria_revisore.md` la riga contatore #125 e una lezione (except sqlite3.Error non basta con la tipizzazione dinamica di SQLite). Nessun IP letterale. Il file è committato da solo con `scripts/commit_memoria_revisore.sh` (commit `aa0b0d0`). Il diff staged (store.py, stato_progetto.md, test_unit_kernel.py) resta intatto nell'index.

### Correzione nel testo sopra

Al punto 1 ho scritto per errore "store.py:5131": il riferimento giusto è `tests/test_unit_kernel.py:5131`, come indicato lì stesso.

File rilevanti:
- /Users/gas/Gas/modules/memory/store.py
- /Users/gas/Gas/tests/test_unit_kernel.py
- /Users/gas/Gas/reports/design_cancello.md
- /Users/gas/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Prima (origin/main ce3d392): `423 PASS, 5 FAIL`. Dopo (4f16a65): `463 PASS, 5 FAIL` (+40 check T73).

```
=== RIEPILOGO: 463 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

I 5 FAIL sono F-mac-1 (bwrap assente su macOS), fuori scope. pytest gate+hooks+voice_server: 144 passed prima e dopo.

## §6 STATO CI

```
completed	success	Merge pull request #110 from Gasss23/chore/hook-fine-task-obbligatorio	CI	main	push	37056446724	53s	2026-10-02T19:47:55Z
completed	success	docs(handoff): aggiorna §0 §2 §3 §6 con dati reali post-CI (SUCCESS)	CI	chore/hook-fine-task-obbligatorio	push	37053843630	54s	2026-10-02T19:23:53Z
completed	success	docs(reports): rimuovi IP letterali da diff_sessione e ultimo_report	CI	chore/hook-fine-task-obbligatorio	push	37053631494	1m4s	2026-10-02T19:21:55Z
```

- `aa0b0d0`: nessuna run su questo SHA (non pushato).
- `4f16a65`: nessuna run su questo SHA (non pushato).

## §7 RISERVE APERTE

- R-c3-1 (media, da chiudere PRIMA di C4): righe con tipi sbagliati da SQL grezzo → eccezione fuori dagli except in get/resolve.
- R-c3-2 (minore): validare `timeout_secs`.
- R-c3-3 (minore): `approved` deve richiedere `risolto_da == "telegram_user"`.
- R-c3-4 (minore): `rejected` deve pretendere `telegram_user_id` int o None.
- R-c3-5 (cosmetica): get/resolve/pending/expire non controllano `self.available`.
- Finding nuovo: il verdetto verbatim #125 non passa `check_verdetto.py` (path abbreviati / fuori diff) — conferma F-verdetto-ritoccato.
