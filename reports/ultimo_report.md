# FETTA 1 — Cablare hook suite in CI
**Data:** 2026-07-17  
**Branch:** fix/ci-hook-tests  
**Commit:** 1ed35247ad0a844c174138123ff21b44357c119e  

---

## Esito

COMPLETATO. Tutte le modifiche richieste applicate, commit pushato, CI avviata.

---

## Verifica sicurezza pre-commit (grep remote/push/origin/GAS_REPO_DIR/tmp_path)

Tutti i remote in `tests/test_unit_hooks.py` usano path locali dentro `tmp_path`
(`str(bare_path)`, `str(bare)`) oppure `/nonexistent/path/repo.git` (test di push
failure intenzionale). Nessun remote punta a github.com o al repo reale.
Sonda superata → commit autorizzato.

---

## Revisore

NON invocato. Il diff tocca esclusivamente `.github/workflows/ci.yml` e
`requirements-dev.txt`. Nessun file motore (gas.py, brains/, modules/, tests/).
Gate di review non si applica per CLAUDE.md §3.

---

## File modificati

```
 .github/workflows/ci.yml | 10 ++++++++++
 requirements-dev.txt     |  2 ++
 2 files changed, 12 insertions(+)
```

---

## Dettaglio modifiche

### requirements-dev.txt (nuovo file)
```
# Dipendenze di SVILUPPO/CI. NON installare sul VPS: il deploy è requirements.txt.
pytest==9.1.1
```

### .github/workflows/ci.yml — 3 variazioni

**a) Checkout — persist-credentials: false**  
Aggiunto `with: persist-credentials: false`. Il token di push viene rimosso dal
.git/config del workspace: i test hook eseguono gli hook (che fanno `git push`),
quindi la superficie di push veniva lasciata aperta inutilmente. Nessuno step di
questa CI pusha → chiusura a costo zero.

**b) Install dependencies — requirements-dev.txt**  
Aggiunta riga `pip install -r requirements-dev.txt` dopo il pip di requirements.txt.
Installa pytest nel runner CI senza aggiungerlo alle dipendenze di deploy del VPS.

**c) Nuovo step "Run hook suite (pytest, zero token LLM)"**  
Inserito tra "Run unit suite" e "Job summary":
```yaml
- name: Run hook suite (pytest, zero token LLM)
  if: always()
  run: python -m pytest tests/test_unit_hooks.py -v
```
- `if: always()`: un FAIL del kernel non nasconde l'esito degli hook.
- Nessun `|| true`, nessun `continue-on-error`, nessun `set +e`, nessun parsing.
- L'exit code nativo di pytest è il verdetto.
- Job rimane `unit-suite` (check required `main-lock` invariato, nessun job nuovo).

---

## Vincoli rispettati

- NO paths-ignore (CLAUDE.md §10)
- NO nuovo job (check required main-lock = `unit-suite`)
- NO || true / continue-on-error / set +e / parsing output
- NO touch a .claude/hooks/, T-hook-h, tests/, reports/stato_progetto.md
- NO /fine-task, NO apertura PR

---

## CI

- Run ID: 29591105016
- URL: https://github.com/Gasss23/Gas/actions/runs/29591105016
- Stato al momento del commit: queued
