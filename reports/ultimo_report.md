# R-hook-jq — fail-loud jq in scrivi_rep.sh

**Data:** 2026-07-19  
**Branch:** fix/hook-jq-failloud  
**Commit codice:** 0ced9e0  
**Scope:** SOLO `.claude/hooks/scrivi_rep.sh` + `tests/test_unit_hooks.py`  

---

## Esito per fetta

### FETTA 1 — scrivi_rep.sh — FATTA

**(a) Fail-loud jq**

Ristrutturazione minima del flusso per permettere il rilevamento del trigger senza jq:

1. `transcript_path` estratto da stdin via `sed` (anziché `jq -r`) — rimuove la dipendenza circolare nella fase di ingresso.
2. Aggiunto pre-filtro `grep -qi "scrivi rep" "$TP"` per rilevare il trigger senza jq.
3. Aggiunto check funzionale `if ! jq --version >/dev/null 2>&1; then` — fail-loud: emette warning su stderr e esce con 0.

Contratto comportamentale rispettato:
- Nessun trigger → `grep` non trova nulla → exit 0 silenzioso, stderr vuoto, nessun file, nessun commit. ✓
- Trigger + jq disponibile → comportamento attuale invariato. ✓  
- Trigger + jq assente → warning su stderr ("jq non trovato — dipendenza mancante, feature scrivi rep inerte"), exit 0, nessun file scritto, nessun commit. ✓ **NUOVO**

Nota tecnica: impossibile nascondere jq da PATH rimuovendo directory — su questo sistema `/bin` è symlink a `/usr/bin`, quindi jq, bash, grep, sed sono nella stessa directory. Usato `jq --version` (functional check) anziché `command -v jq` (presence check) per permettere il mock nel test via fake jq eseguibile (exit 1). Il revisore ha approvato il trade-off (review #56).

Stop gate conforme: nessun file oltre scrivi_rep.sh toccato in questa fetta.

**(b) Commento riga 3**

`# (incl. auto-push su main) il 2026-06-13.` → `# (pusha sul branch corrente) il 2026-06-13.`

Stantio dal main-lock (2026-07-09): l'hook pusha sul branch corrente, mai su main.

---

### FETTA 2 — T-hook-i — FATTA

**Precondizione detached-HEAD verificata prima di scrivere FETTA 3:**  
Il guard in `scrivi_rep.sh` riga 55: `if ! _cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)" || [ "$_cur_branch" = "main" ]`. In bash, l'exit status di un'assegnazione propaga dall'exit status del command substitution interno: `git symbolic-ref` esce non-zero su HEAD detached → assegnazione non-zero → `!` → condizione vera → guard attivo. Verificato empiricamente. Guard COPRE detached-HEAD → T-hook-j va scritto.

**T-hook-i:** repo temp, branch feature/i, transcript con "scrivi rep", fake jq (eseguibile, exit 1) preposto al PATH.  
Asserzioni: exit 0 ✓ · stderr non vuoto e cita "jq"/"dipendenza" ✓ · `ultima_risposta.md` NON scritto ✓ · 0 commit nuovi ✓

---

### FETTA 3 — T-hook-j — FATTA

**T-hook-j:** repo temp, checkout hash (HEAD detached), transcript con "scrivi rep", jq reale disponibile.  
Asserzioni: exit 0 ✓ · warning su stderr cita "detach"/"main-lock" ✓ · 0 commit nuovi ✓

Nota: con jq disponibile e trigger presente, `ultima_risposta.md` VIENE scritto (step prima del guard branch). Il test asserisce solo sull'assenza di commit, allineato al contratto del guard.

---

## Verifica

```
source venv/bin/activate && python -m pytest tests/test_unit_hooks.py -v
```

```
tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_a_main_no_commit        PASSED
tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_b_feature_branch_commits PASSED
tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_c_detached_head_no_commit PASSED
tests/test_unit_hooks.py::TestSessionEndPush::test_hook_d_push_to_feature_branch_not_main PASSED
tests/test_unit_hooks.py::TestSessionEndPush::test_hook_e_push_failure_warns_and_exits_zero PASSED
tests/test_unit_hooks.py::TestSessionEndAddRobust::test_hook_f_add_without_gas_history PASSED
tests/test_unit_hooks.py::TestScriviRepPush::test_hook_g_push_to_feature_branch_not_main PASSED
tests/test_unit_hooks.py::TestScriviRepPush::test_hook_h_main_no_commit           PASSED
tests/test_unit_hooks.py::TestScriviRepJq::test_hook_i_no_jq_warns_and_exits_zero PASSED
tests/test_unit_hooks.py::TestScriviRepJq::test_hook_j_detached_head_no_commit    PASSED
10 passed in 2.17s
```

**10/10 PASS — nessun rosso.**

---

## Verdetto revisore (verbatim, review #56)

```
#56 — 2026-07-18 — APPROVATO — quando il PATH non si può manipolare nei test
senza rompere dipendenze di sistema (tool nella stessa dir di bash/grep),
usare functional check (`tool --version`) + fake eseguibile (exit 1) invece
di presence check (`command -v`): permette il mock controllato senza effetti
collaterali su altri tool.
```

---

## Diff

**`.claude/hooks/scrivi_rep.sh`** — +12 righe, -1 riga (TP extraction via sed, grep pre-filter, jq functional check, commento corretto)  
**`tests/test_unit_hooks.py`** — +103 righe (classe TestScriviRepJq con T-hook-i e T-hook-j)

Files toccati: 2/2 in scope. Nessun file fuori scope.

---

## Stop gate finale

- ci.yml: NON toccato ✓  
- session_end.sh: NON toccato ✓  
- gas.py / brains/ / modules/: NON toccati ✓
