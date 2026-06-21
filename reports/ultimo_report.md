# R-TASK1 — Fix path hook: CLAUDE_PROJECT_DIR + guardia fail-closed

**Data:** 2026-06-21  
**Task:** Eliminare path `/workspaces/Gas` hardcoded da hook e settings.json. Funziona in locale ORA e su VPS DOPO senza ulteriori modifiche.

---

## PATH RESIDUI TROVATI (punto 2 sonda)

| File | Riga | Path hardcoded |
|------|------|----------------|
| `.claude/settings.json` | 8 | `bash /workspaces/Gas/.claude/hooks/session_end.sh` |
| `.claude/settings.json` | 21 | `bash /workspaces/Gas/.claude/hooks/review_gate.sh` |
| `.claude/settings.json` | 34 | `bash /workspaces/Gas/.claude/hooks/scrivi_rep.sh` |
| `.claude/hooks/review_gate.sh` | 20 | `cd /workspaces/Gas 2>/dev/null || exit 0` (mio fix precedente già su `dirname $0`) |
| `.claude/hooks/session_end.sh` | 23 | `REPO="${GAS_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"` (mio fix precedente già su `dirname $0`) |
| `.claude/hooks/scrivi_rep.sh` | 35 | `REPO_DIR="${GAS_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"` (fix 110c9d8 su `dirname $0`) |

**Meccanismo usato prima:** tutti e tre gli script usavano `dirname $0` (meccanismo diverso da quello che useremo ora). Nessuno aveva la guardia fail-closed.

**Finding critico aggiuntivo:** `settings.json` aveva path `/workspaces/Gas/` hardcoded nei comandi degli hook → gli hook NON giravano su questa macchina (file non trovato). Confermato: nessun output debug su Bash tool calls iniziali.

---

## SONDA $CLAUDE_PROJECT_DIR (punto 1)

**Test eseguito:** aggiunta riga di debug `echo "DEBUG_SONDA PROJECT_DIR=[$CLAUDE_PROJECT_DIR] PWD=[$PWD]" >> /tmp/gas_hook_sonda.txt` in cima a `review_gate.sh`, poi fix temporaneo di `settings.json` per far girare l'hook, poi Bash tool call per triggerare il PreToolUse.

**Output reale del file sonda:**
```
DEBUG_SONDA PROJECT_DIR=[C:/Users/gqual/gas] PWD=[/c/Users/gqual/gas]
DEBUG_SONDA PROJECT_DIR=[C:/Users/gqual/gas] PWD=[/c/Users/gqual/gas]
```

**Conclusioni:**
- `CLAUDE_PROJECT_DIR` è esportata da Claude Code agli hook: **SÌ**, valore `C:/Users/gqual/gas`
- `$CLAUDE_PROJECT_DIR` viene espanso nel command string di `settings.json`: **SÌ** (testato con `bash $CLAUDE_PROJECT_DIR/.claude/hooks/review_gate.sh`)
- Il path `C:/` (Windows forward slash) funziona correttamente con bash: **SÌ**
- Su VPS Linux sarà un path Unix standard (es. `/home/user/gas`): **compatibile**, stesso meccanismo
- Fallback `git rev-parse --show-toplevel`: **NON necessario**, `CLAUDE_PROJECT_DIR` è disponibile e stabile

---

## MODIFICHE APPLICATE

### `.claude/hooks/review_gate.sh`
- **Rimossa:** riga debug sonda (temporanea, solo per test)
- **Aggiunta guardia fail-closed** in cima: `: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"`
- **Sostituita** riga `cd "$(dirname "$0")/../.." 2>/dev/null || exit 0` con `cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0`

### `.claude/hooks/session_end.sh`
- **Sostituita** riga `REPO="${GAS_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"` con `REPO="${GAS_REPO_DIR:-${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}}"`
- La guardia fail-closed è integrata nell'assegnazione: se `GAS_REPO_DIR` non è settata (caso normale prod) e `CLAUDE_PROJECT_DIR` manca, lo script termina con errore chiaro.

### `.claude/hooks/scrivi_rep.sh`
- **Aggiunta guardia fail-closed** in cima (prima di `INPUT=$(cat)`): `: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"`
- **Sostituita** riga `REPO_DIR="${GAS_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"` con `REPO_DIR="${GAS_REPO_DIR:-$CLAUDE_PROJECT_DIR}"`

### `.claude/settings.json`
- Tutti e tre i comandi hook aggiornati da `/workspaces/Gas/.claude/hooks/` a `$CLAUDE_PROJECT_DIR/.claude/hooks/`:
  - `bash $CLAUDE_PROJECT_DIR/.claude/hooks/session_end.sh`
  - `bash $CLAUDE_PROJECT_DIR/.claude/hooks/review_gate.sh`
  - `bash $CLAUDE_PROJECT_DIR/.claude/hooks/scrivi_rep.sh`

**Invariante:** un solo meccanismo uniforme su tutti e tre gli script e in settings.json.

---

## VERIFICA REALE

### Punto 1 — Sintassi bash
```
$ bash -n .claude/hooks/review_gate.sh && bash -n .claude/hooks/session_end.sh && bash -n .claude/hooks/scrivi_rep.sh && echo "SINTASSI OK"
SINTASSI OK
```

### Punto 2 — Zero occorrenze /workspaces/Gas
```
$ grep -rn "/workspaces/Gas" .claude/
(output vuoto — zero righe)
```

### Punto 3 — git log senza errori PreToolUse
```
$ git log --oneline -1
110c9d8 fix(hooks): scrivi_rep.sh — repo root da dirname $0 invece di /workspaces/Gas hardcoded
```
Nessuna riga `PreToolUse:Bash hook error ... No such file or directory`. Hook girato correttamente (exit 0, non era un git commit quindi non interferisce).

### Punto 4 — session_end.sh
**DA VERIFICARE alla prossima chiusura sessione.** L'hook scatta su SessionEnd, non su un comando qualsiasi; non è verificabile in-task. Il test in-task dimostra solo che la sintassi è corretta e che `$CLAUDE_PROJECT_DIR` è disponibile nell'ambiente hook.

---

## STATO FINALE
- **R-TASK1: CHIUSO** su macchina locale Windows.
- **VPS-ready:** `$CLAUDE_PROJECT_DIR` sarà il path assoluto del repo sul VPS Linux — stesso meccanismo, zero modifiche necessarie al deploy.
- **Unica verifica pendente:** `session_end.sh` alla prossima chiusura sessione.
