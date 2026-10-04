#!/usr/bin/env bash
# Stop hook — blocca se ci sono commit di sessione non coperti da handoff fresco.
# exit 0 in TUTTI i percorsi (fail-open: mai intrappolare la sessione).
# Blocco: {"decision":"block","reason":"..."} su stdout.
# Contatore: blocca al massimo 3 volte PER SESSIONE (session_id da payload stdin).
#   Formato file: "<session_id>:<count>" — reset automatico se session_id cambia.
#   File: $GIT_DIR/promemoria_block_count (R4: path worktree-safe via git rev-parse --git-dir).
#   Al 4° tentativo → fail-open con WARNING su stderr E su gas_debug.log.
# Anti-loop: se stop_hook_active==true nel payload stdin → exit 0 silenzioso.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
if [[ -z "$PROJECT_DIR" ]]; then
    PROJECT_DIR=$(git -C "$(cd "$(dirname "$0")" && pwd)" rev-parse --show-toplevel 2>/dev/null) || exit 0
fi

LOG="${PROJECT_DIR}/gas_debug.log"

# Legge payload hook da stdin; fail-open se non parsabile
INPUT=$(cat)

# Estrai stop_hook_active e session_id in un unico parse Python
_PARSED=$(printf '%s' "$INPUT" | python3 -c \
    "import json,sys
d=json.load(sys.stdin)
active = '1' if d.get('stop_hook_active') else '0'
sid = d.get('session_id', '')
print(active)
print(sid)" \
    2>/dev/null)

_SHA=$(printf '%s' "$_PARSED" | head -1)
SESSION_ID=$(printf '%s' "$_PARSED" | tail -1)

# Fallback regex se python3 non riesce
if [[ -z "$_SHA" ]]; then
    printf '%s' "$INPUT" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
fi
[[ "$_SHA" == "1" ]] && exit 0

# HEAD su main → exit silenzioso (main-lock: no operazioni di push/block)
BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
[[ "$BRANCH" == "main" ]] && exit 0

# Calcola BASE senza rete (nessun git fetch)
if ! BASE=$(git -C "$PROJECT_DIR" merge-base refs/remotes/origin/main HEAD 2>/dev/null) || [[ -z "$BASE" ]]; then
    printf '%s WARN promemoria_end: git merge-base fallito (origin/main non raggiungibile)\n' \
        "$(date -u +%FT%TZ)" >> "$LOG" 2>/dev/null || true
    exit 0
fi

# SESSION_COMMITS = commit in BASE..HEAD esclusi quelli con subject "chore(scrivi-rep):*"
SESSION_COMMITS=$(git -C "$PROJECT_DIR" log --format="%s" "${BASE}..HEAD" 2>/dev/null \
    | grep -cv '^chore(scrivi-rep):') || SESSION_COMMITS=0
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

# R4: percorso counter worktree-safe
GIT_DIR_PATH=$(git -C "$PROJECT_DIR" rev-parse --git-dir 2>/dev/null || echo "${PROJECT_DIR}/.git")
[[ "$GIT_DIR_PATH" != /* ]] && GIT_DIR_PATH="${PROJECT_DIR}/${GIT_DIR_PATH}"
COUNTER_FILE="${GIT_DIR_PATH}/promemoria_block_count"

if [[ "${HANDOFF_IN_LAST}" -ge 1 ]]; then
    # Handoff fresco → azzera il contatore
    rm -f "$COUNTER_FILE" 2>/dev/null || true
    exit 0
fi

# Handoff NON fresco → contatore per sessione (B1)
COUNT=0
if [[ -f "$COUNTER_FILE" ]]; then
    STORED=$(cat "$COUNTER_FILE" 2>/dev/null || echo ":")
    STORED_SID=$(printf '%s' "$STORED" | cut -d':' -f1)
    STORED_COUNT=$(printf '%s' "$STORED" | cut -d':' -f2-)
    if [[ "$STORED_SID" == "$SESSION_ID" ]] && [[ "${STORED_COUNT}" =~ ^[0-9]+$ ]]; then
        COUNT=$STORED_COUNT
    fi
    # session_id diverso → COUNT resta 0 (reset implicito)
fi
COUNT=$((COUNT + 1))
printf '%s:%s' "$SESSION_ID" "$COUNT" > "$COUNTER_FILE" 2>/dev/null || true

if [[ $COUNT -le 3 ]]; then
    printf '{"decision":"block","reason":"Esegui /fine-task ORA: è obbligatorio, non è un suggerimento."}\n'
else
    # R5: WARN sia su stderr che su gas_debug.log
    WARN_MSG=$(printf '%s WARN promemoria_end: blocco #%d, fail-open (limite 3/sessione raggiunto). Esegui /fine-task ORA.\n' \
        "$(date -u +%FT%TZ)" "$COUNT")
    printf '%s\n' "$WARN_MSG" >&2
    printf '%s\n' "$WARN_MSG" >> "$LOG" 2>/dev/null || true
fi

exit 0
