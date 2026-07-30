# ULTIMO REPORT — fix/gasmerge-hardening (PR #56)

**Data:** 2026-07-30  
**Branch:** fix/gasmerge-hardening  
**PR:** #56 — fix(gasmerge): hardening #65-R1/#63-R1/#65-R3  
**Commit principale:** 61db9f9  

---

## ESITO: APPROVATO E PR APERTA (NON MERGATO)

Tre fix applicati su `scripts/gasmerge.sh` e `tests/test_unit_gasmerge.py`.
Revisore APPROVATO (review #69). Suite: 12/12 PASS. PR aperta per review umana.

---

## FIX 1 — #65-R1: guard su NEW_HEAD vuoto (post-conferma)

**File:** `scripts/gasmerge.sh:177`  
**Aggiunto:** `[ -n "$NEW_HEAD" ] || { echo "BLOCCO: NEW_HEAD vuoto (ri-lettura post-conferma) — head non verificabile"; exit 1; }`

Il guard per HEAD_SHA (prima cattura) era già in place a riga 158.
Il guard per NEW_HEAD (ri-lettura post-conferma) mancava: senza di esso, `gh` poteva
restituire stringa vuota con exit 0, e il TOCTOU check bloccava comunque via
`"" != "SHA_valido"` ma con il messaggio fuorviante "head cambiata".

**Prova mordacità:**
- HEAD_SHA vuoto (1ª cattura): script blocca con "BLOCCO: HEAD_SHA vuoto — head non verificabile" (exit 1) ✅
- NEW_HEAD vuoto (post-conferma) — PRIMA del fix: blocca via TOCTOU con "BLOCCO: head cambiata durante la conferma (aaa111... → )" (fuorviante)
- NEW_HEAD vuoto (post-conferma) — CON il fix: blocca con "BLOCCO: NEW_HEAD vuoto (ri-lettura post-conferma) — head non verificabile" ✅
- Nuovo test T-fix1: `TestTOCTOU::test_new_head_empty_blocks_with_explicit_message` verifica che "head cambiata" NON appaia con NEW_HEAD vuoto

---

## FIX 2 — #63-R1: git risolto dinamicamente negli stub di test

**File:** `tests/test_unit_gasmerge.py:101,116`  
**Cambio:** `shutil.which("git")` al momento della creazione dello stub (in Python,
prima che `fake_bin` venga preposta a PATH), poi il path viene incorporato come
letterale nell'`exec` del body bash dello stub.

**Strategia:** il git reale viene risolto nel processo Python (che ha PATH originale,
senza `fake_bin`). L'`exec "/abs/path/git"` nel body bash usa un path assoluto → nessun
lookup PATH → nessuna ricorsione. Fallback `/usr/bin/git` se `shutil.which` ritorna None.

**Prova no-ricorsione:** la suite termina in ~4s (12 test), nessun timeout.

---

## FIX 3 — #65-R3: /tmp/gaspr.json condiviso → mktemp per-run

**File:** `scripts/gasmerge.sh:27-29`, `tests/test_unit_gasmerge.py:68,441`

Script:
```bash
GASPR_JSON=$(mktemp /tmp/gaspr.XXXXXX.json)
export GASPR_JSON
trap 'rm -f "$GASPR_JSON"' EXIT
```
Tutte le occorrenze di `/tmp/gaspr.json` nel body script sostituite con `"$GASPR_JSON"`.

Test: gli stub bash che scrivono il JSON leggono `$GASPR_JSON` ereditato tramite
`export` dal processo padre (gasmerge.sh). Nessun path fisso /tmp residuo nella suite.

---

## Verifiche reali eseguite

a) **Suite gasmerge:** 12/12 PASS (11 esistenti invariati + 1 nuovo test mordacità)

```
tests/test_unit_gasmerge.py::TestArgValidation::test_no_arg_exits_2 PASSED
tests/test_unit_gasmerge.py::TestArgValidation::test_non_numeric_arg_exits_2 PASSED
tests/test_unit_gasmerge.py::TestJqCheck::test_broken_jq_exits_with_message PASSED
tests/test_unit_gasmerge.py::TestPRState::test_pr_not_open_blocks PASSED
tests/test_unit_gasmerge.py::TestIPGuard::test_git_grep_error_blocks PASSED
tests/test_unit_gasmerge.py::TestIPGuard::test_ip_outside_reports_blocks PASSED
tests/test_unit_gasmerge.py::TestDiffGuard::test_git_diff_name_only_error_blocks PASSED
tests/test_unit_gasmerge.py::TestIPAllowlist::test_ip_with_marker_passes PASSED
tests/test_unit_gasmerge.py::TestIPAllowlist::test_ip_without_marker_blocks PASSED
tests/test_unit_gasmerge.py::TestIPAllowlist::test_public_ip_without_marker_blocks PASSED
tests/test_unit_gasmerge.py::TestTOCTOU::test_head_changed_during_confirm_blocks PASSED
tests/test_unit_gasmerge.py::TestTOCTOU::test_new_head_empty_blocks_with_explicit_message PASSED
12 passed in 3.97s
```

b) **Suite kernel (test_unit_kernel.py):** INTERNALERROR pre-esistente (sys.exit a livello
modulo che confonde pytest). Non causato da questa sessione. Suite hooks+handoff: 19/19 PASS.

c) **Prova mordacità FIX 1:** output reale incluso sopra. ✅

d) **bash -n scripts/gasmerge.sh:** syntax OK  
   **Dry-run argomento non numerico:** `uso: gasmerge <numero-PR>  (argomento non numerico: 'abc')` → exit 2 ✅

---

## Revisore — verdetto INTEGRALE (review #69, 2026-07-30)

**APPROVATO — review #69 (2026-07-30)**

Il commit sul branch `fix/gasmerge-hardening` che tocca `scripts/gasmerge.sh` e
`tests/test_unit_gasmerge.py` è autorizzato.

Elementi verificati:
- `scripts/gasmerge.sh:27-29` — mktemp/export/trap EXIT: chiude #65-R3, fail-closed corretto
- `scripts/gasmerge.sh:177` — guard NEW_HEAD vuoto: blocco esplicito e diagnosticamente
  corretto, posizionato nel punto giusto della sequenza TOCTOU
- `tests/test_unit_gasmerge.py:101,116` — `shutil.which("git")`: chiude #63-R1, fallback
  /usr/bin/git presente
- `tests/test_unit_gasmerge.py:473-523` — nuovo test stateful con counter file: mordace
  sul FIX 1 (rimuovere il guard produce "head cambiata" che fa fallire l'asserzione dedicata)

Riserva ereditata ancora aperta: **#65-R2** (`--match-head-commit` senza copertura test
end-to-end positiva) — non toccata da questo diff, da tenere tracciata in `stato_progetto.md`.

---

## Finding chiusi da questa sessione

- ✅ **#65-R1** — guard HEAD_SHA/NEW_HEAD vuoto (missing piece = guard NEW_HEAD post-conferma)
- ✅ **#63-R1** — stub git hardcoda /usr/bin/git
- ✅ **#65-R3** — /tmp/gaspr.json condiviso non thread-safe

## Finding aperti residui (non toccati per mandate)

- 🟡 **#65-R2** — `--match-head-commit` senza copertura test positiva end-to-end
