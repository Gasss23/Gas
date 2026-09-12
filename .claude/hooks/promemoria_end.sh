#!/usr/bin/env bash
# soft hook: avvisa (non blocca, non committa, non pusha) se ci sono commit di
# sessione senza reports/handoff.md aggiornato.  exit 0 in TUTTI i percorsi.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
if [[ -z "$PROJECT_DIR" ]]; then
    PROJECT_DIR=$(git -C "$(cd "$(dirname "$0")" && pwd)" rev-parse --show-toplevel 2>/dev/null) || exit 0
fi

LOG="${PROJECT_DIR}/gas_debug.log"

# HEAD su main → exit silenzioso
BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
[[ "$BRANCH" == "main" ]] && exit 0

# Calcola BASE
if ! BASE=$(git -C "$PROJECT_DIR" merge-base origin/main HEAD 2>/dev/null) || [[ -z "$BASE" ]]; then
    printf '%s WARN promemoria_end: git merge-base fallito\n' "$(date -u +%FT%TZ)" >> "$LOG" 2>/dev/null || true
    exit 0
fi

# Conta commit di sessione
SESSION_COMMITS=$(git -C "$PROJECT_DIR" log --oneline "${BASE}..HEAD" 2>/dev/null | wc -l | tr -d '[:space:]')
SESSION_COMMITS="${SESSION_COMMITS:-0}"

# Verifica se reports/handoff.md è nel diff di sessione
HANDOFF_UPDATED=$(git -C "$PROJECT_DIR" diff --name-only "${BASE}..HEAD" 2>/dev/null \
    | grep -c '^reports/handoff\.md$') || HANDOFF_UPDATED=0

if [[ "${SESSION_COMMITS}" -gt 0 && "${HANDOFF_UPDATED}" -eq 0 ]]; then
    printf 'promemoria: %s commit di sessione senza handoff aggiornato — ricorda /fine-task\n' \
        "${SESSION_COMMITS}" >&2
fi

exit 0
