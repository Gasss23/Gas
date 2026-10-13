#!/usr/bin/env bash
# Stop hook — blocca se ci sono commit di sessione non coperti da handoff fresco.
# exit 0 in TUTTI i percorsi (fail-open: mai intrappolare la sessione).
# Blocco: {"decision":"block","reason":"..."} su stdout.
# Contatore: blocca al massimo 3 volte PER SESSIONE (session_id da payload stdin).
#   Formato file: una riga "<session_id>:<count>" PER SESSIONE (A1: due sessioni
#   che si alternano non si azzerano più a vicenda il contatore).
#   File: $GIT_DIR/promemoria_block_count, nel git-dir DEL WORKTREE del turno
#   (A1: `git rev-parse --git-dir` in un worktree dà .git/worktrees/<nome>).
# Repo controllato (A1): quello del `cwd` del payload (il turno in corso, segue i
#   worktree, come review_gate.sh); fallback su CLAUDE_PROJECT_DIR, poi sulla dir dello script.
#   Al 4° tentativo → fail-open con WARNING su stderr E su gas_debug.log.
# Anti-loop: se stop_hook_active==true nel payload stdin → exit 0 silenzioso.

# Legge payload hook da stdin; fail-open se non parsabile
INPUT=$(cat)

# Estrai stop_hook_active, session_id e cwd in un unico parse Python
_PARSED=$(printf '%s' "$INPUT" | python3 -c \
    "import json,sys
d=json.load(sys.stdin)
active = '1' if d.get('stop_hook_active') else '0'
print(active)
print(str(d.get('session_id', '')).replace(chr(10), ' '))
print(str(d.get('cwd', '')).replace(chr(10), ' '))" \
    2>/dev/null)

_SHA=$(printf '%s\n' "$_PARSED" | sed -n 1p)
SESSION_ID=$(printf '%s\n' "$_PARSED" | sed -n 2p)
PAYLOAD_CWD=$(printf '%s\n' "$_PARSED" | sed -n 3p)

# Radice git di una directory ("" se non e' un repo o la dir non esiste).
_radice() {
    [[ -n "$1" && -d "$1" ]] || return 1
    git -C "$1" rev-parse --show-toplevel 2>/dev/null
}

# A1: il repo del turno in corso (cwd del payload) prima di CLAUDE_PROJECT_DIR,
# che punta sempre al checkout principale anche quando si lavora in un worktree.
PROJECT_DIR=$(_radice "$PAYLOAD_CWD") || PROJECT_DIR=""
# Come prima di A1: CLAUDE_PROJECT_DIR impostato ma non repo → exit 0; la dir dello
# script si usa SOLO se CLAUDE_PROJECT_DIR manca.
if [[ -z "$PROJECT_DIR" && -n "${CLAUDE_PROJECT_DIR:-}" ]]; then
    PROJECT_DIR=$(_radice "$CLAUDE_PROJECT_DIR") || exit 0
fi
[[ -z "$PROJECT_DIR" ]] && { PROJECT_DIR=$(_radice "$(cd "$(dirname "$0")" && pwd)") || exit 0; }

LOG="${PROJECT_DIR}/gas_debug.log"

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

# Righe del contatore delle ALTRE sessioni (A1: si conservano, non si sovrascrivono).
# Il session_id passa per ENVIRON, non `awk -v`: -v interpreta i backslash e la riga
# della sessione non si ritroverebbe più (R-314-1).
_altre_sessioni() {
    [[ -f "$COUNTER_FILE" ]] || return 0
    SID="$SESSION_ID" awk 'BEGIN { sid = ENVIRON["SID"] } length($0) > 0 && substr($0, 1, length(sid) + 1) != sid ":"' \
        "$COUNTER_FILE" 2>/dev/null
}

if [[ "${HANDOFF_IN_LAST}" -ge 1 ]]; then
    # Handoff fresco → azzera il contatore DI QUESTA sessione
    ALTRE=$(_altre_sessioni)
    if [[ -n "$ALTRE" ]]; then
        printf '%s\n' "$ALTRE" > "$COUNTER_FILE" 2>/dev/null || true
    else
        rm -f "$COUNTER_FILE" 2>/dev/null || true
    fi
    exit 0
fi

# Handoff NON fresco → contatore per sessione (B1, A1: una riga per session_id)
COUNT=0
if [[ -f "$COUNTER_FILE" ]]; then
    STORED_COUNT=$(SID="$SESSION_ID" awk 'BEGIN { sid = ENVIRON["SID"] } substr($0, 1, length(sid) + 1) == sid ":" { print substr($0, length(sid) + 2); exit }' \
        "$COUNTER_FILE" 2>/dev/null)
    [[ "${STORED_COUNT}" =~ ^[0-9]+$ ]] && COUNT=$STORED_COUNT
fi
COUNT=$((COUNT + 1))
ALTRE=$(_altre_sessioni)
{ [[ -n "$ALTRE" ]] && printf '%s\n' "$ALTRE"; printf '%s:%s\n' "$SESSION_ID" "$COUNT"; } \
    > "$COUNTER_FILE" 2>/dev/null || true

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
