# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-01 — feat/gate-c1 fix C1 (NFKC, substring run_command, ci.yml gate suite, bug commit_memoria_revisore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #107 (https://github.com/Gasss23/Gas/pull/107).

Riserve residue da considerare in C2:
- R-nw-1 (minore): controllo puramente lessicale — symlink non risolti. Da gestire in C2 con `Path.resolve()` + root confinement.
- R-nw-2 (cosmetic): substring check su comando intero può dare false deny su dir che iniziano con prefix deny (es. `brains_backup/`). Fail-closed by design; da documentare all'integrazione C2.

---

## §1 SCOPE & ESITO FETTE

- **FIX 1 — CI (R-gate-3)**: `FATTA` — step "Run gate suite" in ci.yml + gate nel job summary.
- **FIX 2 — run_command substring (R-gate-2)**: `FATTA` — `gate.py:206-212` NFKC+casefold sull'intera stringa; 6 test nuovi TestRunCommand.
- **FIX 3 — NFKC (R-gate-1)**: `FATTA` — `gate.py:91` NFC→NFKC; 3 test nuovi TestNFKC.
- **FIX 4 — commit_memoria_revisore.sh bug**: `FATTA` — `scripts/commit_memoria_revisore.sh:47` grep ancorato a `^#[0-9]+`; 1 test T-R2-f.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 .github/workflows/ci.yml           |  19 ++
 modules/gate/__init__.py           |   4 +
 modules/gate/gate.py               | 224 ++++++++++++++++++++++++
 reports/diff_sessione.md           |  51 ++++--
 reports/handoff.md                 | (questo file — conteggio approssimato)
 reports/stato_progetto.md          |   9 +-
 reports/ultimo_report.md           |  63 +++----
 scripts/commit_memoria_revisore.sh |   8 +-
 tests/test_unit_gate.py            | 343 +++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  38 ++++
 11 files changed, 759 insertions(+), 125 deletions(-)
```

(BASE = `12eccd5f22cc711474ff66515e18ae12d77ef86d`)

---

## §3 GIT LOG --ONELINE (sessione)

```
4f8fc73 fix(gate-c1): R-gate-1 NFKC, R-gate-2 substring check, R-gate-3 ci.yml, FIX-4 commit_memoria
f2d6d35 chore(revisore): memoria review #117 — APPROVATO CON RISERVE
e39e132 docs(gate-c1): fine-task — ultimo_report + handoff + diff_sessione + stato_progetto
83354d8 chore(revisore): memoria review #12 — ?
d74fed0 feat(gate-c1): scaffolding gate — GateClass, GATE_ALLOWLIST, gate_classify + test
8b15b69 docs(gate-c1): passo 0 — rettifica #115 + finding F-diario-args
```

NB: il commit di fine-task che contiene questo file non compare qui (non ancora committato).

---

## §4 VERDETTO DEL REVISORE

### Review #117 — APPROVATO CON RISERVE

**Testo integrale:**

> #117 — 2026-10-01 — APPROVATO CON RISERVE — fix C1: R-gate-1 (NFKC, gate.py:91), R-gate-2 (substring check gate.py:206-212), R-gate-3 (ci.yml:103 step gate suite), bug commit_memoria_revisore.sh:47 (grep '^#[0-9]+' invece di tail -1). R-nw-1 (minore, pre-C2): controllo puramente lessicale — symlink non risolti (da gestire in C2 con Path.resolve()). R-nw-2 (cosmetic): substring check su comando intero può dare false deny su dir che iniziano con prefix deny (es. brains_backup/).

**Riserve aperte post-review:**

- **R-nw-1** (minore, pre-C2): symlink non risolti — `read_file("safe_link → .gas_memory.db")` passa il gate. Richiede `Path.resolve()` con root confinement in C2.
- **R-nw-2** (cosmetic): false deny su dir con nome che inizia con prefix deny. Fail-closed by design.

**Analisi vettori bypass (richiesta esplicita):**

> Il controllo è puramente lessicale (NFKC+normpath+casefold + substring matching). Vettori coperti: path assoluti, traversal, FULLWIDTH Unicode, --flag=value, case variations. Vettori residui: symlink (non risolti lessicalmente — richiede Path.resolve() + root confinement in C2); variabili d'ambiente ($GAS_HISTORY_FILE) — non espanse con shell=False; alias shell — non applicabili con shell=False.

---

## §5 DELTA TEST DEL MOTORE

Suite gate: **74 PASS, 0 FAIL** (era 65; +9: TestRunCommand ×6, TestNFKC ×3).  
Suite hook: **37 PASS, 0 FAIL** (era 34 hooks; +1 T-R2-f nel contesto hooks R2).  
Suite kernel: **400 PASS, 5 FAIL** (invariata — F-mac-1 bwrap macOS, pre-esistenti).  
`.gas_memory.db` SHA256: `d1c8f0cc2961145a629bf0b57a43d1b0328fe4db1bf5c428a8037c92b756ef11` (invariato).

---

## §6 STATO CI

```
completed  failure  docs(gate-c1): fine-task — ultimo_report + handoff …  CI  feat/gate-c1  push  36781609144  1m15s  2026-09-30T21:47:01Z
completed  success  chore(revisore): memoria review #12 — ?               CI  feat/gate-c1  push  36781509635  1m34s  2026-09-30T21:46:04Z
completed  success  Merge pull request #106 from Gasss23/fix/diario-eco   CI  main          push  36779657997  1m2s   2026-09-30T21:28:33Z
```

**Mappatura commit → run CI:**

- `8b15b69` (passo 0): nessuna run su questo SHA (pushato insieme al successivo).
- `d74fed0` (scaffolding gate): nessuna run su questo SHA (pushato insieme al successivo).
- `83354d8` (revisore #12): run `36781509635` — `success`. Testa l'albero di d74fed0+83354d8.
- `e39e132` (fine-task sessione precedente): run `36781609144` — **`failure`**. Causa: handoff-check CI (§2 handoff fuori sync). Superata dalla nuova run post-push di questa sessione.
- `f2d6d35` (revisore #117): nessuna run su questo SHA (non ancora pushato).
- `4f8fc73` (fix C1 code): nessuna run su questo SHA (non ancora pushato).
- commit fine-task questa sessione: run non ancora disponibile alla scrittura dell'handoff.

---

## §7 RISERVE APERTE

Da questa sessione (review #117):
- **R-nw-1** (minore, pre-C2): symlink non risolti — `Path.resolve()` + root confinement in C2.
- **R-nw-2** (cosmetic): false deny su dir con nome che inizia con prefix deny (es. `brains_backup/`).

Commit errati (storico, non correggibili senza rewrite):
- `83354d8`: subject "memoria review #12 — ?" (causa: bug commit_memoria_revisore.sh, ora corretto)
- `a3afcfd`: subject "memoria review #? — ?" (stessa causa)
