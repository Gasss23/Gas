# Ultimo report — 2026-08-19
## Task: check_verdetto fail-closed + R-voice-3

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #64 (fix(review-gate): fail-closed + test R-voice-3) una volta che CI è verde.

---

## FETTA 1 — review_gate.sh fail-closed: `FATTA`

**Problema chiuso**: il check "nessun diff motore" in `.claude/hooks/review_gate.sh` era fail-open per due motivi:
1. `cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0` — cd fallito → exit 0 (fail-open).
2. `git diff --cached --name-only 2>/dev/null | grep -Eq ...` — pipeline bash: l'exit code era quello di `grep`, non di `git`. Un `git diff` fallito produceva output vuoto → grep restituiva 1 → `! 1` = true → exit 0 (fail-open).

**Fix applicato** (`.claude/hooks/review_gate.sh`):
- `cd` failure → exit 2 con messaggio su stderr (fail-closed).
- `git diff --cached` catturato in `DIFF_OUT=$(...)` + `GIT_RC=$?` fuori pipeline. Se `GIT_RC != 0` → exit 2 (fail-closed).
- Solo se git OK E `DIFF_OUT` non contiene file motore → exit 0.

**Test aggiunti** (`tests/test_unit_hooks.py`, classe `TestReviewGateFailClosed`):
- T-gate-A: diff motore staged + `.review_ok` assente → exit 2 ✅
- T-gate-B: diff motore staged + `.review_ok` presente → exit 0 ✅
- T-gate-C: solo file non-motore staged → exit 0 (esente) ✅
- T-gate-D: CLAUDE_PROJECT_DIR non è un git repo → git diff fallisce → exit 2 (fail-closed) ✅

**Risultato test**: 4/4 PASS (repo git reali, nessun mock).
**Revisore**: #80 — 2026-08-19 — APPROVATO.
**Commit**: `56c2d11`

**Scope rispettato**: solo `.claude/hooks/review_gate.sh` e `tests/test_unit_hooks.py`. Nessuna modifica al motore (gas.py, brains/, modules/).

---

## FETTA 2 — test R-voice-3 Content-Length abc→400: `FATTA`

**Cosa**: aggiunto test esplicito che verifica che una POST con `Content-Length: abc` (non numerico) restituisca 400.

Il codice già gestiva il caso (`modules/voice/server.py:85-89`, `except ValueError`). Mancava solo la copertura del test.

**Implementazione** (`tests/test_unit_voice_server.py`, `TestTVExtra.test_invalid_content_length_returns_400`):
- Usa `http.client.HTTPConnection` direttamente (non urllib, che normalizza `Content-Length` internamente).
- Invia `Content-Length: abc` → verifica status 400 e che il messaggio di errore citi "Content-Length".

**Risultato test**: PASS. Suite voice: 19 PASS (era 18).
**Gate**: codice già corretto — test PASSA (gate non ha bloccato, comportamento corretto).
**Revisore**: #81 — 2026-08-19 — APPROVATO.
**Commit**: `87cce8e`

**Scope rispettato**: solo `tests/test_unit_voice_server.py`. Nessuna modifica al codice di produzione.

---

## Contatori suite (post-task)

| Suite | Prima | Dopo |
|---|---|---|
| Hook (`test_unit_hooks.py`) | 10 PASS | **14 PASS** |
| Voice (`test_unit_voice_server.py`) | 18 PASS | **19 PASS** |
| Kernel (`test_unit_kernel.py`) | 276 PASS | 276 PASS (invariato) |
