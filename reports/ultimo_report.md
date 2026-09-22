# Ultimo Report — 2026-09-23
## FIX /fine-task automatico — promemoria_end.sh (FETTA 1)

**Data:** 2026-09-23  
**Branch:** sonda/fine-task-recon-2026-09-23  
**Commit motore:** 176c25d

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR** (URL da rilevare al passo 4bis con `gh`).
2. **F3 (partenza su main) — fuori scope dichiarato**: il passo 0 ha rilevato che il branch corrente era già attivo (sonda/fine-task-recon-2026-09-23); la questione "partenza da main" non è stata affrontata in questa sessione. Se si vuole risolvere F3, richiede una sessione dedicata.

---

## ESITO FETTE

### PASSO 0 — Pre-check bloccante
**FATTO** — `settings.local.json` letto: nessuna chiave `hooks` o `disableAllHooks`. Contenuto verbatim:
```json
{
  "permissions": {
    "allow": [
      "Bash(bwrap --version)",
      "Bash(claude --version)",
      "Bash(git fetch *)",
      "Bash(git checkout *)",
      "Bash(git reset *)",
      "Bash(git grep *)"
    ]
  }
}
```
Nessun blocco: procede con FETTA 1.

### Verifica formato hook Stop (prerequisito)
**FATTO** — Formato confermato dal binario Claude Code 2.1.280:
- Campo stdin: `stop_hook_active` (bool)
- Blocco: `{"decision":"block","reason":"..."}` su stdout, exit 0
- Anti-loop: `stop_hook_active == true` → exit 0 silenzioso

### FETTA 1a — Riscrittura `.claude/hooks/promemoria_end.sh`
**FATTO** — Comportamento implementato:
- Legge stdin JSON; se `stop_hook_active == true` → exit 0 (anti-loop)
- branch main, BASE non calcolabile, qualsiasi errore git → exit 0 + WARN in gas_debug.log (fail-open, no rete)
- `SESSION_COMMITS` = commit in BASE..HEAD esclusi soggetti `^chore(scrivi-rep):`
- "Handoff fresco" = ultimo commit non-chore tocca `reports/handoff.md` (via `git diff-tree`)
- `SESSION_COMMITS > 0` e handoff NON fresco → `{"decision":"block","reason":"..."}` su stdout
- Altrimenti exit 0 silenzioso
- `chmod +x` applicato

### FETTA 1b — Test in `tests/test_unit_hooks.py`
**FATTO** — 9 test aggiornati/aggiunti (classe `TestPromemoriaEnd`):
- T-prom-1: 0 commit → no blocco
- T-prom-2: commit senza handoff → blocco JSON su stdout
- T-prom-3: handoff come ultimo commit → no blocco
- T-prom-3b: commit dopo handoff → blocco
- T-prom-3c: solo chore(scrivi-rep) dopo handoff → no blocco
- T-prom-4: no origin → WARN log, exit 0, no blocco
- T-prom-5: HEAD su main → silenzioso
- T-prom-6: `stop_hook_active=true` → exit 0 anti-loop
- T-prom-7: dir non-git → exit 0
- Tutti su repo git reali temporanei, nessun mock
- Suite completa: **34/34 green**

### Test e2e manuale
**FATTO** — Branch temporaneo `test/promemoria-e2e` creato, commit dummy senza handoff.
Output hook verificato:
```
{"decision":"block","reason":"Commit di sessione non coperti da handoff: esegui /fine-task per intero prima di chiudere."}
EXIT: 0
```
Branch mai pushato, eliminato dopo il test.

### Revisore (gate obbligatorio — diff tocca tests/)
**FATTO** — Review #101: **APPROVATO** (nessuna riserva).

### Fette F2, F3 (fuori scope dichiarato)
**SALTATE — fuori scope**: il task copre SOLO FETTA 1 (promemoria_end.sh + test). F2/F3 non esistono in questo scope.

---

## ANOMALIE

- Nessuna anomalia riscontrata.
- `grep -cv` su input vuoto: verificato che rc=1 viene catturato dall'`||` e la guard `^[0-9]+$` copre edge case; comportamento confermato dal test T-prom-1.
