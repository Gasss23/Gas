#!/usr/bin/env bash
# Stop hook — blocca se ci sono commit di sessione non coperti da handoff fresco.
# exit 0 in TUTTI i percorsi (fail-open: mai intrappolare la sessione).
# Blocco: {"decision":"block","reason":"..."} su stdout.
# Anti-loop: se stop_hook_active==true nel payload stdin → exit 0 silenzioso.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
if [[ -z "$PROJECT_DIR" ]]; then
    PROJECT_DIR=$(git -C "$(cd "$(dirname "$0")" && pwd)" rev-parse --show-toplevel 2>/dev/null) || exit 0
fi

LOG="${PROJECT_DIR}/gas_debug.log"

# Legge payload hook da stdin; fail-open se non parsabile
INPUT=$(cat)
_SHA=$(printf '%s' "$INPUT" | python3 -c \
    "import json,sys; d=json.load(sys.stdin); print('1' if d.get('stop_hook_active') else '0')" \
    2>/dev/null)
[[ "$_SHA" == "1" ]] && exit 0

# HEAD su main → exit silenzioso (main-lock: no operazioni di push/block)
BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
[[ "$BRANCH" == "main" ]] && exit 0

# Calcola BASE senza rete (nessun git fetch)
if ! BASE=$(git -C "$PROJECT_DIR" merge-base origin/main HEAD 2>/dev/null) || [[ -z "$BASE" ]]; then
    printf '%s WARN promemoria_end: git merge-base fallito (origin/main non raggiungibile)\n' \
        "$(date -u +%FT%TZ)" >> "$LOG" 2>/dev/null || true
    exit 0
fi

# SESSION_COMMITS = commit in BASE..HEAD esclusi quelli con subject "chore(scrivi-rep):*"
SESSION_COMMITS=$(git -C "$PROJECT_DIR" log --format="%s" "${BASE}..HEAD" 2>/dev/null \
    | grep -cv '^chore(scrivi-rep):') || SESSION_COMMITS=0
# grep -c ritorna 1 se zero righe trovate ma non errore: gestisci edge case
[[ "${SESSION_COMMITS}" =~ ^[0-9]+$ ]] || SESSION_COMMITS=0

[[ "${SESSION_COMMITS}" -le 0 ]] && exit 0

# "Handoff fresco" = l'ultimo commit non-chore(scrivi-rep) in BASE..HEAD tocca reports/handoff.md
LAST_NON_CHORE=$(git -C "$PROJECT_DIR" log --format="%H %s" "${BASE}..HEAD" 2>/dev/null \
    | grep -v ' chore(scrivi-rep):' | head -1 | awk '{print $1}')

HANDOFF_IN_LAST=0
if [[ -n "$LAST_NON_CHORE" ]]; then
    HANDOFF_IN_LAST=$(git -C "$PROJECT_DIR" diff-tree --no-commit-id -r --name-only \
        "$LAST_NON_CHORE" 2>/dev/null | grep -c '^reports/handoff\.md$') || HANDOFF_IN_LAST=0
fi

if [[ "${HANDOFF_IN_LAST}" -eq 0 ]]; then
    printf '{"decision":"block","reason":"Commit di sessione non coperti da handoff: esegui /fine-task per intero prima di chiudere."}\n'
fi

exit 0
