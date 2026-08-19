# REPORT TASK — 2026-08-19
## R2 — Durabilità memoria revisore su interruzione (implementazione)

Branch: `fix/r2-durabilita-memoria`
Commits: `70d595f` (dogfooding memoria #85), `7906580` (implementazione R2)

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR `fix/r2-durabilita-memoria → main` (R2 implementata, suite 19 PASS, review #85 APPROVATO CON RISERVE).

---

## §1 — SCOPE & ESITO

- **`scripts/commit_memoria_revisore.sh`**: SCRITTO ✅ — script bash che usa `git commit -o .claude/agents/memoria_revisore.md` per committare SOLO la memoria anche se altri file sono in staging.
- **`.claude/agents/revisore.md`**: AGGIORNATO ✅ — aggiunta sezione "Commit atomico R2" con istruzione di chiamare lo script dopo ogni riga contatore.
- **`tests/test_unit_hooks.py`**: AGGIORNATO ✅ — nuova classe `TestCommitMemoriaRevisore` con 4 test reali.
- **Review #85**: APPROVATO CON RISERVE — riserve R1/R2/R3 tutte chiuse inline prima del commit.
- **Dogfooding**: VERIFICATO ✅ — il revisore ha eseguito lo script su se stesso; HEAD = SOLO memoria, staging intatto, exit 0.

---

## §2 — IMPLEMENTAZIONE

### `scripts/commit_memoria_revisore.sh`

Tecnica: `git commit -o <path>` crea un commit con SOLO il path specificato (preso
dal working tree), senza alterare lo staging degli altri file.

**Vincolo di correttezza dimostrato empiricamente** (test T-R2-b):
- Con `git add && git commit`: il file motore staged entra nel commit → HEAD contiene
  ENTRAMBI i file → viola l'invariante che la memoria sia committata in isolamento.
- Con `git commit -o memoria_revisore.md`: HEAD contiene SOLO la memoria; gas.py resta staged.

**FAIL-SAFE §9** implementato correttamente:
- `cd` fallisce → `_log_warn` → exit 0
- file non trovato → `_log_warn` → exit 0
- `git commit` fallisce (niente da committare, HEAD detached, lock, repo anomalo) →
  stderr di git catturato e incluso nel warning → exit 0
- Scrittura nel log fallisce → `|| true` → exit 0 (fail-safe su fail-safe)

**Estrazione automatica** del numero review e del verdetto dall'ultima riga di
`memoria_revisore.md` (pattern: `#<N> — <data> — <VERDETTO> — ...`).

**`.gas_history.json`**: NON toccato. Finding durabilità runtime resta aperto separatamente.

### Aggiornamento `revisore.md`

Nuova sezione "Commit atomico di memoria_revisore.md (R2)" inserita prima di
"Lezioni nuove": istruzione esplicita di eseguire `bash scripts/commit_memoria_revisore.sh`
dopo ogni riga contatore.

---

## §3 — SUITE TEST

**19 PASS totali** (da 15 → 19): zero regressioni.

Nuovi test (`TestCommitMemoriaRevisore`):

| Test | Descrizione | Asserzioni |
|------|-------------|------------|
| T-R2-a | commit -o committa SOLO memoria, motore resta staged | (a) HEAD=SOLO mem; (b) gas.py staged; (c) exit 0 |
| T-R2-b | dimostra bug `add && commit` | gas.py in HEAD (violazione a) |
| T-R2-c | noop idempotente (file identico a HEAD) | exit 0 |
| T-R2-d | fail-safe su dir non-git | exit 0 + gas_debug.log esiste + contiene WARN |

---

## §4 — REVIEW #85

**Verdetto**: APPROVATO CON RISERVE

Riserve emesse e chiuse:
- **R1** (pre-commit bloccante): `commit_memoria_revisore.sh` era untracked → aggiunto con `git add` → CHIUSA
- **R2** (minore): `2>/dev/null` sopprimeva stderr git nel log → ora `GIT_MSG=$(git commit ... 2>&1)` → CHIUSA
- **R3** (minore): T-R2-d non verificava la scrittura del log → aggiunta asserzione `log_file.exists()` + `"WARN" in content` → CHIUSA

**Dogfooding del meccanismo R2** (eseguito dal revisore sulla propria riga contatore):
- Script invocato: `bash scripts/commit_memoria_revisore.sh`
- Commit prodotto: `70d595f` — "chore(revisore): memoria review #85 — APPROVATO CON RISERVE"
- Verifica (a): `git diff-tree --name-only HEAD` → solo `.claude/agents/memoria_revisore.md`
- Verifica (b): staging pre-esistente intatto (vuoto in quella sessione, coerente)
- Verifica (c): exit 0

---

## §5 — FINDING APERTI

- 🟡 **#84-riserva check_verdetto non-ASCII**: test speculare `test_nonascii_filename_check_verdetto` da aggiungere (branch successivo).
- 🟡 **`.gas_history.json` durabilità runtime**: NON chiuso da R2. Finding separato (VPS/snapshot). Trade-off dichiarato in CLAUDE.md §3: sessione interrotta prima di `/fine-task` non persiste `.gas_history.json`.
- 🟡 **R-verdetto-evidenza**: check meccanico path:riga nel diff — ancora disciplinare, non strutturale.
