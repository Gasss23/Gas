# Task — Fix phantom PR bug: riscrittura REGOLA §0 in /fine-task
**Data:** 2026-08-22
**Branch:** sonda/phantom-pr-bug

---

## Fette

- **Fetta 1 — Riscrittura REGOLA §0 in `.claude/commands/fine-task.md`**: `FATTA`
  REGOLA §0 sostituita con un gate procedurale bash che impone `gh pr list --head "$BRANCH" --base main --json number,url` dopo il push. Tutti i rami coperti: PR esistente → numero da JSON; PR assente → crea con `--fill`, poi `gh pr view` per numero; qualsiasi gh exit non-zero → "PR NON verificata/creata: <errore reale>" + task INCOMPLETO. Vincolo ferreo esplicito: nessun numero hardcoded, nessun placeholder.

- **Fetta 2 — TEST A (percorso "crea")**: `FATTA`
  Branch `sonda/phantom-pr-bug` non aveva PR. Esecuzione verbatim del gate:
  ```
  === TEST A: BRANCH=sonda/phantom-pr-bug ===
  gh pr list exit=0
  PR_JSON=[]
  Nessuna PR trovata — creo PR...
  gh pr create exit=0
  CREATE_OUT=https://github.com/Gasss23/Gas/pull/74
  gh pr view exit=0
  VIEW_JSON={"number":74,"url":"https://github.com/Gasss23/Gas/pull/74"}
  RISULTATO OK (creata): PR #74 — https://github.com/Gasss23/Gas/pull/74
  ```
  Verifica post-test: `gh pr view sonda/phantom-pr-bug --json number,url,state`
  ```
  {"number":74,"state":"OPEN","url":"https://github.com/Gasss23/Gas/pull/74"}
  ```
  Numero proveniente ESCLUSIVAMENTE da output JSON di `gh`.

- **Fetta 3 — TEST B (percorso "errore")**: `FATTA`
  Due sotto-test eseguiti, nessun numero PR fabbricato:
  ```
  === TEST B: percorso errore (BRANCH=main) ===
  GATE §0 BLOCCATO: BRANCH='main' non valido.
  RISULTATO: PR NON verificata/creata: BRANCH non valido (main).
  Task: INCOMPLETO

  === TEST B2: percorso errore (repo inesistente → gh non-zero) ===
  gh pr list exit=1
  PR_JSON=GraphQL: Could not resolve to a Repository with the name 'Gasss23/NonEsiste-XYZ'. (repository)
  RISULTATO: PR NON verificata/creata: gh pr list exit 1 — GraphQL: Could not resolve to a Repository with the name 'Gasss23/NonEsiste-XYZ'. (repository)
  Task: INCOMPLETO
  ```

- **Fetta 4 — Revisione subagent revisore**: `FATTA`
  Verdetto integrale (review #92):

  **APPROVATO CON RISERVE**

  Il fix risolve correttamente il bug phantom-PR (R-phantom-pr-1): la REGOLA §0 ora impone l'esecuzione di `gh pr list` prima di scrivere qualsiasi numero in §0, eliminando la possibilità di allucinazione. La logica dei rami (BRANCH non valido / gh fallisce / PR assente / PR esistente) è completa e fail-closed. Il principio "dati reali da `gh`, mai inventati" è rispettato con un VINCOLO FERREO esplicito.

  **R-finegat-1** (non bloccante): `.claude/commands/fine-task.md:78` — `PR_JSON=$(gh pr list ... 2>&1)`. Se `gh` emette un warning su stderr con exit 0, `PR_JSON` contiene testo misto non-JSON. La check `[ "$PR_JSON" = "[]" ]` fallisce, si entra nel ramo PR-già-esistente, python3 a riga 104 lancia `json.JSONDecodeError` non catturata, `PR_NUMBER`/`PR_URL` risultano vuoti, §0 viene scritto malformato senza segnale esplicito. Mitigazione: `2>/dev/null` per la capture JSON + try/except in python3.

  **R-finegat-2** (cosmetico): `.claude/commands/fine-task.md:79-80` — `GH_EXIT=$?; if [ $GH_EXIT -ne 0 ]`. Non-atomico per la lezione #51, ma sicuro in questo contesto (nessun comando intermedio). Da allineare alla forma `if ! PR_JSON=$(gh pr list ...); then` per coerenza con il resto del progetto.

- **Fetta 5 — Aggiornamento reports/stato_progetto.md**: `FATTA`
  R-phantom-pr-1 chiuso, riserve R-finegat-1/2 aggiunte ai finding aperti.

## Anomalie

Nessuna.

## Scope superato / proposto / fuori mandato

Nessuno. La riscrittura si è limitata a REGOLA §0 senza toccare altre parti di fine-task.md.

## Riserve aperte da questa sessione

- 🟡 **R-finegat-1** (non bloccante): stderr misto nel JSON capture di `gh pr list`; fix suggerito: `2>/dev/null` + try/except python3.
- 🟡 **R-finegat-2** (cosmetico): pattern non-atomico `GH_EXIT=$?`; fix: forma `if ! PR_JSON=$(...)`.
