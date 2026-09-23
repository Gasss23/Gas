# Report — 2026-09-23 — fix(promemoria-end): grep fallback anti-loop python3 assente

## DECISIONI UMANE RICHIESTE

1. Merge della PR su branch `fix/promemoria-riserve` (numero e URL da inserire dopo push — vedi handoff §0).

---

## Scope e esito fette

### PASSO 0 — Registra esito TEST A
FATTA. Blocco arrivato: sì. Testo: "Commit di sessione non coperti da handoff: esegui /fine-task per intero prima di chiudere." Anti-loop: sì (secondo stop passato senza blocco). WARN log: nessuno.

### FETTA 1 — grep fallback in promemoria_end.sh
FATTA. Aggiunta una riga dopo `[[ "$_SHA" == "1" ]] && exit 0`:
```
[[ -z "$_SHA" ]] && printf '%s' "$INPUT" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
```
Copre il caso python3 assente o fallente: `_SHA` vuota → grep POSIX → exit 0 se `stop_hook_active=true`.

### FETTA 2 — test hook in CI
SALTATA (nessuna modifica necessaria). La CI esegue già `python -m pytest tests/test_unit_hooks.py -v` allo step "Run hook suite" di `.github/workflows/ci.yml`. Aggiunta di 1-3 righe non richiesta.

### FETTA 3 — verifica F1 (solo lettura)
FATTA. Output verbatim:
- `git ls-files -s`: `100755 b70a25bf324b69d0ac9a485508c48fa3702dae42 0	.claude/hooks/promemoria_end.sh`
- `.claude/settings.json` riga 58: `"command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/promemoria_end.sh"`

### TEST T-prom-8 e T-prom-8b
FATTI. Aggiunto helper `_make_broken_python3_path` e due test:
- T-prom-8: `stop_hook_active=true` + python3 rotto → nessun blocco (grep fallback)
- T-prom-8b: `stop_hook_active=false` + python3 rotto + commit senza handoff → blocco JSON

Suite completa: **36/36 passed**.

## Revisore

Review #102 — 2026-09-23: **APPROVATO**. Nessuna riserva aperta.

## Anomalie

Nessuna.
