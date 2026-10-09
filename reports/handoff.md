# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-09 — merge #163 + test R-226-4 / R-227-1 (PR #164)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #164 (https://github.com/Gasss23/Gas/pull/164). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/164"}`): `gh` nel container non è autenticato. Merge autonomo dell'agente solo con verdetto testuale del bot `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. V-2 bot #163: il gate B (`scripts/check_verdetto.py`) rifiuta i riferimenti `path:riga` a file fuori dal repo (es. l'SDK `openai`), e l'agente finisce per riscrivere i verdetti del revisore. Va deciso se cambiare il gate (ignorare i riferimenti esterni marcati) o il formato del revisore: è macchina di controllo, decide l'operatore.
3. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi `reports/setup_notte.md`.

---

## §1 SCOPE & ESITO FETTE

- **Merge di #163**: `FATTA` — su richiesta esplicita dell'operatore, merge commit `17a2e9d` (= BASE di questa sessione).
- **Fetta 1 — R-226-4, tetto col kernel vero** (`tests/test_unit_notte.py`): `FATTA`.
- **Fetta 2 — R-227-1, rung Ollama in run_turn** (`tests/test_unit_kernel.py` T81h): `FATTA`.
- **Fetta 3 — `.gitignore` `gas_debug.log.*`**: `FATTA`.
- **Fetta 4 — V-1 bot #164** (ordine `turno_fine` < riga `notte`, chiusura esplicita): `FATTA` in `ef7b28e`. **V-2 bot #164** (numeri locali/CI): `FATTA` in questo handoff (§5).
- **T81b/T81d non ermetici** (osservazione review #232): `DEFERITA` — preesistente, fuori scope.
- **V-4 verifica esterna #163**: `DEFERITA` — cosmetica. **V-2 bot #163**: `DEFERITA` — decisione operatore (§0 punto 2).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 .gitignore                         |   1 +
 reports/diff_sessione.md           |  14 ++++++--------
 reports/handoff.md                 | 248 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  35 +++++++++++++++++------------------
 tests/test_unit_kernel.py          |  23 +++++++++++++++++++++++
 tests/test_unit_notte.py           |  39 +++++++++++++++++++++++++++++++++++++++
 8 files changed, 151 insertions(+), 213 deletions(-)
```

Nota: i conteggi di righe dei report scritti dopo lo stat (`reports/handoff.md`, ed eventualmente `reports/ultimo_report.md`) sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
ef7b28e test(notte): turno_fine scritto prima della riga notte (chiusura esplicita, V-1 bot #164)
0602881 chore(revisore): memoria review #233 — APPROVATO
7743b07 docs(fine-task): report PR #164 (test R-226-4, R-227-1)
308114e test(notte,kernel): run_turn reale chiuso dal tetto + rung Ollama in run_turn (R-226-4, R-227-1)
09b45bb chore(revisore): memoria review #232 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #232 (diff staged di 308114e)

VERDETTO: APPROVATO

Ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la voce 6 di `reports/stato_progetto.md` e la coda della mia memoria (#228–#231). Il diff tocca solo test, `.gitignore` e il report di stato. Non trovo antipattern: nessuno slicing della history, e i finti client `OpenAI` sono doppi del provider HTTP, non output di tool inventati (il tool `calcola` gira davvero nel kernel). Il cap di 10 iterazioni e `_get_window` restano intatti.

**Elementi del diff esaminati**

1. `tests/test_unit_notte.py:429` — Nuovo test `test_tetto_chiude_il_run_turn_reale_con_turno_fine_ko`: kernel vero, orologio finto che avanza di 25s a ogni chiamata, tetto a 60s.
   - **Fragilità del conteggio:** l'ambiente del test (`_ermetico`, riga 25) configura solo `GEMINI_API_KEY`, e il finto client risponde al primo rung. Quindi il numero di chiamate è il numero di iterazioni, non dipende da quanti modelli Gemini sono in cascata. Il conto è deterministico: 1025 → 1050 → 1075, il tetto scatta alla terza chiamata. La forbice `2 <= n < 10` resta robusta anche se cambia la granularità degli eventi.
   - **Effetti collaterali del finto `time.monotonic`:** in `gas.py` lo usa solo `doctor` (riga 2692), che qui non viene eseguito. `threading` lega la sua copia di `monotonic` al momento dell'import, e `monkeypatch` ripristina tutto a fine test. Nessuna interferenza con rate limit, budget o durate del kernel.
   - **Esito: ok.** Rilanciato: 5 passed sul filtro `-k "reale or tetto"`.
2. `tests/test_unit_kernel.py:7276` — Nuovo T81h: lascia configurato solo Ollama e verifica che run_turn costruisca il client con url Ollama, timeout 600, max_retries 1.
   - **Ripristino dell'ambiente:** l'ho provato con un ambiente ostile (`GAS_OLLAMA_TIMEOUT_SEC=5`, `GROQ_API_KEY=x`, `GAS_OLLAMA_URL=http://altro/v1` preimpostati). T81h passa comunque, perché le chiavi vengono tolte prima di creare il kernel. Dopo la suite i valori sono tornati quelli di partenza, e `GAS_PROVIDER_MAX_RETRIES`, che era assente, resta assente (finally corretto). Anche `gas.OpenAI` torna al client vero salvato in `_vero_openai` (riga 166).
   - **Esito: ok.** Suite pulita: 715 PASS, 0 FAIL.
3. `.gitignore:48` — `gas_debug.log.*` copre solo i log ruotati; `gas_debug.log` era già ignorato alla riga 9. Esito: ok.
4. `reports/stato_progetto.md:356` — Barrate R-226-4 e R-227-1, e aggiunto il merge di #163 (`17a2e9d`). Coerente col diff. Esito: ok.

**Osservazione fuori dal diff, non bloccante:** con l'ambiente ostile falliscono T81b e T81d, test già esistenti: leggono `GAS_OLLAMA_TIMEOUT_SEC` dall'ambiente senza isolarlo. Non sono ermetici, ma il problema c'era già prima di questa modifica. È un candidato per una riserva futura.

**Rischi esplicitamente esclusi**
- Non ho ripetuto le due prove di mutazione dichiarate (tetto disattivato in `notte.py`; `_timeout_provider` fisso). Mi baso sulla tua dichiarazione e sul fatto che la logica dei test le renderebbe rosse. Niente checkout o stash, come richiesto.
- Non ho rilanciato l'intera suite pytest (787): ho eseguito solo il sottoinsieme notte toccato e la suite kernel completa.

**Memoria:** riga #232 aggiunta in `.claude/agents/memoria_revisore.md` e committata da sola (`09b45bb`). Il diff staged sotto review non è stato toccato (4 file, +59/-1).

(Unica modifica dell'agente al testo: il path assoluto della memoria è stato scritto relativo; `&lt;` reso come `<`.)

### Review #233 (diff staged di ef7b28e, V-1 bot #164)

VERDETTO: APPROVATO

Il test ora riesce a distinguere la chiusura esplicita del generatore da quella fatta dal garbage collector. L'ordine degli id è garantito, quindi l'asserzione non è fragile.

**Elementi del diff esaminati**

1. `tests/test_unit_notte.py:459-461`: legge una sola volta il diario e lo filtra in due liste, `turno_fine` e `notte`. Ho controllato che la colonna `id` sia davvero presente nelle righe restituite. Lo è: `diario_recente` esegue `SELECT * FROM diario ORDER BY id DESC` (`modules/memory/store.py:928`). Esito ok.
2. `tests/test_unit_notte.py:465`: controlla che ci sia esattamente una riga `notte` e che `fine[0]["id"] < riga_notte[0]["id"]`. Ho verificato se l'ordine degli id è garantito. Lo è: `modules/memory/store.py:101` dichiara `id INTEGER PRIMARY KEY AUTOINCREMENT`. Con AUTOINCREMENT SQLite assegna id sempre crescenti e non riusa mai quelli già usati, nemmeno dopo una cancellazione. Il diario poi non cancella mai righe (si aggiunge solo in coda). Con un semplice rowid basterebbe comunque, perché nessuno cancella. Esito ok.
3. Contesto, `modules/notte/notte.py:207-220`: dopo il `finally` la riga `notte` viene scritta in modo sincrono. Ho verificato che la tua mutation (`gen.close()` sostituito con `pass`) venga scoperta ogni volta e non solo per caso. Viene scoperta sempre: la variabile locale `gen` tiene vivo il generatore fino al `return` di `_esegui_compito`. Il garbage collector quindi può chiuderlo, e scrivere `turno_fine`, solo dopo `_diario_log("notte", …)`. Il risultato non dipende dai tempi né dal momento in cui gira il GC. Esito ok.

Ho rilanciato la suite: `tests/test_unit_notte.py` dà 36 passed.

**Rischio escluso:** non ho ripetuto la tua mutation (`gen.close()` → `pass`). Il tuo risultato (FAIL con `5 < 4`) è coerente con l'analisi del ciclo di vita del generatore fatta sopra. Non ho verificato su VPS, ma il test è deterministico e non dipende dall'ambiente.

**Memoria:** ho aggiunto la riga #233 in `.claude/agents/memoria_revisore.md`, committata con `scripts/commit_memoria_revisore.sh` (commit `0602881`). Il diff staged è rimasto intatto (solo `tests/test_unit_notte.py`, +6/-1). Ora va creato il marcatore della review con `bash scripts/segna_review_ok.sh` prima del commit.

## §5 DELTA TEST DEL MOTORE

Kernel 714 → 715 PASS in locale (T81h nuovo), 0 FAIL; in CI 716 → 717 (V-2 bot #164: in CI girano 2 test del profilo sandbox che in locale sono [SKIP]). Notte 35 → 36 test. `pytest tests/` 786 → 787 passed. Dopo `ef7b28e`: notte 36 passed. Righe reali:

```
[PASS] T81h R-227-1: run_turn sul rung Ollama usa il timeout di Ollama (600s) — client visti: [('http://ollama.test/v1', 600, 1)]
=== RIEPILOGO: 715 PASS, 0 FAIL ===
787 passed in 116.66s (0:01:56)
```

Mutation dell'agente:
- tetto disattivato in `modules/notte/notte.py` → `assert 2 <= len(chiamate) < 10` FAIL (`assert 20 < 10`);
- `_timeout_provider` fisso a `PROVIDER_TIMEOUT_SEC` → `[FAIL] T81h … client visti: [('http://ollama.test/v1', 120, 1)]`.
- `gen.close()` → `pass` in `modules/notte/notte.py` (dopo `ef7b28e`) → `AssertionError: assert (1 == 1 and 5 < 4)`.
Tutte ripristinate con copia, `git diff --quiet` pulito.

## §6 STATO CI

`gh` non autenticato nel container: stato dai check della PR #164 e dai verdetti delle verifiche.

- `308114e`: handoff-check failure (handoff della sessione precedente, per costruzione del fine-task), dato della verifica del bot.
- `7743b07` (primo fine-task): run 37922529818 — `unit-suite` success, `handoff-check` success; `verifica-bot` success (verdetto testuale APPROVATO CON RISERVE: V-1, V-2 chiuse qui).
- `09b45bb`, `0602881`: nessuna run su questo SHA (pushati con altri, testati solo come parte dell'albero della testa).
- `ef7b28e` e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **T81b/T81d non ermetici (BASSA, test, preesistente)**: leggono `GAS_OLLAMA_TIMEOUT_SEC` dall'ambiente senza isolarlo.
- **V-2 bot #163 (processo, decisione operatore)**: gate B e verdetti del revisore con riferimenti esterni (§0 punto 2).
- **V-4 verifica esterna #163 (COSMETICA)**: voce 6 di `stato_progetto.md` troppo lunga.
