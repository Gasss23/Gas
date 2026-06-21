# R-TASK1 — Fix hook: CLAUDE_PROJECT_DIR + guardia fail-closed + parser JSON portabile

**Data:** 2026-06-21  
**Task:** Eliminare path `/workspaces/Gas` hardcoded da hook e settings.json. Funzionante in locale ORA e su VPS DOPO senza modifiche.

---

## PATH RESIDUI TROVATI (punto 2 sonda)

| File | Contenuto hardcoded |
|------|---------------------|
| `.claude/settings.json` | `bash /workspaces/Gas/.claude/hooks/session_end.sh` |
| `.claude/settings.json` | `bash /workspaces/Gas/.claude/hooks/review_gate.sh` |
| `.claude/settings.json` | `bash /workspaces/Gas/.claude/hooks/scrivi_rep.sh` |
| `.claude/hooks/review_gate.sh` | `cd /workspaces/Gas` (mio fix precedente: `dirname $0`) |
| `.claude/hooks/session_end.sh` | `$(cd "$(dirname "$0")/../.." && pwd)` |
| `.claude/hooks/scrivi_rep.sh` | `$(cd "$(dirname "$0")/../.." && pwd)` |

**Finding critico aggiuntivo emerso dalla sonda:** gli hook NON giravano su questa macchina perché `settings.json` conteneva path `/workspaces/Gas/` che non esiste in locale. Confermato: nessun output debug prima del fix di settings.json.

---

## SONDA $CLAUDE_PROJECT_DIR (punto 1)

**Metodo:** riga di debug `>> /tmp/gas_hook_sonda.txt` aggiunta temporaneamente a `review_gate.sh`, poi fix temporaneo di settings.json per far girare il hook, poi Bash tool call trigger.

**Output reale del file sonda:**
```
DEBUG_SONDA PROJECT_DIR=[C:/Users/gqual/gas] PWD=[/c/Users/gqual/gas]
```

**Conclusioni:**
- `CLAUDE_PROJECT_DIR` esportata agli hook da Claude Code: **SÌ** → `C:/Users/gqual/gas`
- Espansione di `$CLAUDE_PROJECT_DIR` nel command string di settings.json: **SÌ**
- Path `C:/` (Windows forward slash) funziona con bash: **SÌ**
- VPS Linux: path Unix standard, stesso meccanismo
- Fallback `git rev-parse --show-toplevel`: NON necessario

---

## BUG AGGIUNTIVO SCOPERTO DURANTE IL COLLAUDO

**Symptom:** dopo R-TASK1 (commit `fe2cc05`), il gate non bloccava i commit del motore.

**Root cause:** `python3` su Windows è uno stub Microsoft Store (`exit 49`, "Python non trovato"), ma `command -v python3` lo trova e lo riporta come disponibile. Il hook originale usava `jq` (non installato su questa macchina). Risultato: `CMD` era sempre vuoto → il gate usciva con exit 0 su ogni comando senza mai controllare il diff staged.

**Debug:** aggiunta logging su file `/tmp/gate_debug.txt`; confermato che dopo `CMD check incoming...` non appariva mai `CMD=[...]` → il parser falliva silenziosamente.

**Fix applicato a `review_gate.sh`:**
1. Sostituita riga `CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')` con un parser a cascata
2. La cascata usa test di esecuzione reale (`python3 -c "import sys"`) invece di `command -v` per rilevare stub non funzionanti
3. Ordine: jq → python3 (testato, non solo trovato) → python → perl

**Cascata completa:**
```bash
_parse_cmd() {
  if command -v jq >/dev/null 2>&1; then
    jq -r '(.[0] // .) | .tool_input.command // empty'
  elif python3 -c "import sys" >/dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  elif python -c "import sys" >/dev/null 2>&1; then
    python -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  else
    perl -MJSON::PP -e '...'
  fi
}
```

**Su questa macchina:** usa il ramo `python` (confermato da test isolato).  
**Su VPS Linux:** userà `jq` (se installato) o `python3` (certamente presente).

**Nota su formato JSON:** input hook è ora un array `[{...}]` non un oggetto `{...}`. Il fix gestisce entrambi con `(.[0] // .)` in jq e `d[0] if isinstance(d,list)` in Python.

---

## MODIFICHE APPLICATE (stato finale)

### `.claude/settings.json`
Tutti e tre i comandi: `/workspaces/Gas/.claude/hooks/` → `$CLAUDE_PROJECT_DIR/.claude/hooks/`

### `.claude/hooks/review_gate.sh`
- Guardia fail-closed: `: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"`
- cd via `$CLAUDE_PROJECT_DIR`
- Parser JSON a cascata jq→python3→python→perl (fix bug parser)

### `.claude/hooks/session_end.sh`
- `REPO="${GAS_REPO_DIR:-${CLAUDE_PROJECT_DIR:?...}}"`

### `.claude/hooks/scrivi_rep.sh`
- Guardia fail-closed in cima
- `REPO_DIR="${GAS_REPO_DIR:-$CLAUDE_PROJECT_DIR}"`

---

## VERIFICA REALE

### Test 1 — Sintassi bash
```
$ bash -n .claude/hooks/review_gate.sh && bash -n .claude/hooks/session_end.sh && bash -n .claude/hooks/scrivi_rep.sh && echo "SINTASSI OK"
SINTASSI OK
```

### Test 2 — Zero occorrenze /workspaces/Gas
```
$ grep -rn "/workspaces/Gas" .claude/
(output vuoto — zero righe)
```

### Test 3 — Gate blocca commit del motore
```
$ git add gas.py         # staging separato
$ git commit -m "probe"  # chiamata Bash separata
PreToolUse:Bash hook error: [bash $CLAUDE_PROJECT_DIR/.claude/hooks/review_gate.sh]:
BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests)
ma manca .claude/.review_ok. [...]
```
Confermato: gas.py ancora staged dopo il tentativo, HEAD invariato a fe2cc05 → il commit NON è passato.

### Test 4 — session_end.sh
**DA VERIFICARE alla prossima chiusura sessione.** Non verificabile in-task.

---

## STATO FINALE
- **R-TASK1: CHIUSO** — hook funzionanti su locale Windows.
- **VPS-ready:** `$CLAUDE_PROJECT_DIR` si adatta automaticamente al path del VPS Linux.
- **Unica verifica pendente:** `session_end.sh` alla prossima chiusura sessione.
