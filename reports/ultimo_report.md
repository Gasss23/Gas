# Ultimo Report — Test TOCTOU positivo --match-head-commit (2026-07-30)

**Task**: test-only — copertura POSITIVA end-to-end di `--match-head-commit` (#65-R2/#63-R2)
**Branch**: test/gasmerge-match-head
**Esito**: ✅ COMPLETATO — #65-R2 CHIUSO, 11→12 test gasmerge, mordacità verificata

---

## ESITO DEL TASK

Aggiunta `TestTOCTOUPositive::test_head_unchanged_merge_uses_match_head_commit` a
`tests/test_unit_gasmerge.py`. Il test chiude il finding #65-R2/#63-R2:
copertura POSITIVA della coppia `--match-head-commit <SHA>` invocata da `gasmerge`.

**Nessuna modifica a `scripts/gasmerge.sh`** nel diff finale (verificato con `git diff`).

---

## COSA FA IL TEST

Scenario: HEAD invariata tra pre-prompt e post-prompt (TOCTOU check supera) →
`gh pr merge` viene invocato con `--match-head-commit <SHA_atteso>`.

Meccanismo di asserzione:
- Stub `_make_stub_gh_recording_merge`: intercetta `pr merge` e scrive gli argomenti
  su `merge_log` (path in `tmp_path`), poi esce 0.
- Il test:
  1. `assert result.returncode == 0` — nessun BLOCCO spurio
  2. `assert merge_log.exists()` — `pr merge` è stato effettivamente chiamato
  3. `assert f"--match-head-commit {SHA}" in recorded` — la coppia flag+SHA è presente

Un test che asserisce solo "exit 0" passerebbe anche se il flag sparisse: questa
asserzione è la misura effettiva della mordacità richiesta.

---

## PROVA DI MORDACITÀ (obbligatoria)

Rimossa temporaneamente la riga `--match-head-commit "$HEAD_SHA"` da `gasmerge.sh`,
eseguito il test → **FALLISCE** con:

```
AssertionError: '--match-head-commit abc1234def5678abc1234def5678abc1234de' NON trovato
negli argomenti di pr merge. Registrato: 'pr merge 123 --merge --delete-branch\n'
```

Ripristinato `gasmerge.sh`, `git diff scripts/gasmerge.sh` → vuoto ✅.

---

## SUITE GASMERGE (prima → dopo)

**Prima (main):** 11 test — tutti PASS
**Dopo (test/gasmerge-match-head):** 12 test — tutti PASS

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
tests/test_unit_gasmerge.py::TestTOCTOUPositive::test_head_unchanged_merge_uses_match_head_commit PASSED

12 passed in 2.14s
```

---

## VERDETTO REVISORE (integrale)

**APPROVATO CON RISERVE**

> `tests/test_unit_gasmerge.py:429-431` — arm `*"headRefOid"*` restituisce SHA identico
> a entrambe le chiamate (pre-prompt e post-prompt) → TOCTOU check passa, nessun BLOCCO
> spurio. Rischio ordine arm: nessun conflitto con `*"pr merge"*` perché le rispettive
> `$*` non si sovrappongono. **Esito: ok**.
>
> `tests/test_unit_gasmerge.py:432-434` + `533` — `echo "$@"` registra gli argomenti
> reali di `gh pr merge`; l'asserzione `f"--match-head-commit {self._SHA}" in recorded`
> è mordace (fallirebbe su flag assente o SHA errato). Doppia guardia con
> `assert merge_log.exists()` che certifica che il ramo `pr merge` sia stato raggiunto.
> **Esito: ok**.
>
> **Riserva 1 (minore):** firma di `_make_stub_gh_recording_merge` senza `-> None`
> (CLAUDE.md §4). Coerente col pattern dell'intero file; correggibile al prossimo refactor.
>
> **Riserva 2 (pre-esistente):** `/tmp/gaspr.json` hardcoded, già tracciato come #65-R3.
> Non aggravata da questo diff.
>
> **Finding #65-R2 / #63-R2: CHIUSO.**

---

## STOP GATE BLOCCANTE — verifica

- `git diff scripts/gasmerge.sh` → vuoto ✅ (nessuna modifica al script nel diff finale)
- La rimozione temporanea è stata ripristinata prima del commit ✅
- Diff staged: solo `tests/test_unit_gasmerge.py` ✅
- PR aperta, NON mergiata ✅ (istruzione rispettata)
