# Report — fix/r2-riserve-86: chiusura riserve R-r2-1 e R-r2-2 (review #86)

Data: 2026-08-19
Branch: fix/r2-riserve-86
Review: #87 — APPROVATO

## Obiettivo

Chiusura delle due riserve residue aperte dal review #86 su R2 (durabilità memoria revisore):
- **R-r2-1**: forma `var=$(cmd); if [ $? -ne 0 ]` fragile → sostituire con forma atomica (lezione #51)
- **R-r2-2**: path "file memoria PRESENTE + repo NON-git" non coperto da T-R2-d → aggiungere test T-R2-e

## Fette eseguite

### FETTA 1 — R-r2-1 (scripts/commit_memoria_revisore.sh, riga 21-22)

Sostituita la forma non-atomica:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$REPO_ROOT" ]; then
```
con la forma atomica:
```bash
if ! REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || [ -z "$REPO_ROOT" ]; then
```
Nessuna altra modifica di logica. Semanticamente identica; strutturalmente allineata alla lezione #51.

### FETTA 2 — R-r2-2 (tests/test_unit_hooks.py)

Aggiunto `test_r2_fail_safe_mem_present_not_git` (T-R2-e) alla classe `TestCommitMemoriaRevisore`.

**Scenario**: `CLAUDE_PROJECT_DIR` punta a dir non-git + `memoria_revisore.md` PRESENTE.
- Il file supera il check riga 64 (file esiste → non esce)
- `git commit -o $MEM_FILE` fallisce (no repo) → `rc != 0`
- `_log_warn` scrive WARN in `gas_debug.log` (riga ~75)
- Script termina con `exit 0`

**Differenza da T-R2-d**: T-R2-d testa file ASSENTE → exit precoce riga 64-66 (path diverso).
T-R2-e copre il ramo riga ~75, finora scoperto.

**Asserzioni**: exit 0 + gas_debug.log esiste + "WARN" nel log.

## Esito test

```
19/19 PASS (test_unit_hooks.py — intera suite, nessuna regressione)
TestCommitMemoriaRevisore: 5/5 PASS (T-R2-a/b/c/d + T-R2-e nuovo)
```

## Verdetto revisore

Review #87 — **APPROVATO** (nessuna riserva).
> R-r2-1: ok — forma atomica corretta, semanticamente identica al codice rimosso.
> R-r2-2: ok — tre asserzioni discriminanti, scenario distinto da T-R2-d.
> Rischio esplicitamente escluso: `git` non nel PATH (exit 127) — irriproducibile nell'ambiente WSL target, non bloccante.

## STOP gate

- File toccati: `scripts/commit_memoria_revisore.sh`, `tests/test_unit_hooks.py`
- gas.py / brains/ / modules/ / file quotePath: NON toccati ✅
- Revisore invocato sul diff staged PRIMA del commit ✅

## Commit

- `4019aa2` — chore(revisore): memoria review #87 — APPROVATO (commit dal revisore)
- `f796f2f` — fix(r2-riserve-86): chiusura riserve R-r2-1 e R-r2-2 da review #86
