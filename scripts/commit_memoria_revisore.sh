#!/usr/bin/env bash
# commit_memoria_revisore.sh — commit atomico di SOLO memoria_revisore.md post-review.
#
# Uso (opzionale): commit_memoria_revisore.sh [num_review] [verdetto]
#   Se non forniti, li estrae dall'ultima riga di memoria_revisore.md.
#
# Garantisce: anche se altri file sono in staging (es. motore sotto review),
# solo memoria_revisore.md entra nel commit — il resto dell'index resta intatto.
# Tecnica: git commit -o <path> crea il commit col solo path specificato,
# preso dal working tree, senza alterare lo staging degli altri file.
#
# FAIL-SAFE §9: qualsiasi errore (lock, HEAD detached, niente da committare,
# repo anomalo) → warning in gas_debug.log → exit 0. Non crasha mai.

MEM_FILE=".claude/agents/memoria_revisore.md"

# ── Trova repo root ──────────────────────────────────────────────────────────
if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
    REPO_ROOT="$CLAUDE_PROJECT_DIR"
else
    if ! REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || [ -z "$REPO_ROOT" ]; then
        # Impossibile trovare il repo — log e uscita silenziosa
        printf '%s [WARN] commit_memoria_revisore: impossibile trovare repo root (CLAUDE_PROJECT_DIR non settata e git rev-parse fallito)\n' \
            "$(date '+%Y-%m-%dT%H:%M:%S' 2>/dev/null || echo 'N/A')" \
            >> "${GAS_DEBUG_LOG:-gas_debug.log}" 2>/dev/null || true
        exit 0
    fi
fi

LOG_FILE="${REPO_ROOT}/gas_debug.log"

_log_warn() {
    printf '%s [WARN] commit_memoria_revisore: %s\n' \
        "$(date '+%Y-%m-%dT%H:%M:%S' 2>/dev/null || echo 'N/A')" "$1" \
        >> "$LOG_FILE" 2>/dev/null || true
}

# ── Estrai review number e verdetto ─────────────────────────────────────────
REVIEW_NUM="${1:-}"
VERDICT="${2:-}"

if [ -z "$REVIEW_NUM" ] || [ -z "$VERDICT" ]; then
    LAST_LINE=$(tail -1 "${REPO_ROOT}/${MEM_FILE}" 2>/dev/null)
    if [ -n "$LAST_LINE" ]; then
        # Pattern riga contatore: #86 — 2026-08-19 — APPROVATO CON RISERVE — ...
        REVIEW_NUM=$(printf '%s' "$LAST_LINE" | grep -oE '#[0-9]+' | grep -oE '[0-9]+' | head -1)
        VERDICT=$(printf '%s' "$LAST_LINE" | grep -oE 'APPROVATO CON RISERVE|APPROVATO|BOCCIATO' | head -1)
    fi
fi

REVIEW_NUM="${REVIEW_NUM:-?}"
VERDICT="${VERDICT:-?}"

COMMIT_MSG="chore(revisore): memoria review #${REVIEW_NUM} — ${VERDICT}"

# ── cd nel repo ──────────────────────────────────────────────────────────────
cd "$REPO_ROOT" 2>/dev/null || {
    _log_warn "cd in REPO_ROOT ('$REPO_ROOT') fallito — commit skipped"
    exit 0
}

# ── Verifica che il file esista ──────────────────────────────────────────────
if [ ! -f "$MEM_FILE" ]; then
    _log_warn "file '$MEM_FILE' non trovato — commit skipped"
    exit 0
fi

# ── Commit atomico path-scoped ───────────────────────────────────────────────
# git commit -o <path>: prende il file dal working tree, crea un commit con
# SOLO quel path, lascia lo staging degli altri file completamente intatto.
GIT_MSG=$(git commit -o "$MEM_FILE" -m "$COMMIT_MSG" 2>&1)
COMMIT_RC=$?

if [ "$COMMIT_RC" -ne 0 ]; then
    # Exit 1 = niente da committare (file identico a HEAD) → idempotente, ok.
    # Exit ≠ 0 per altri motivi (lock, HEAD detached, repo anomalo) → warn.
    _log_warn "git commit -o $MEM_FILE fallito (rc=$COMMIT_RC): ${GIT_MSG}; index degli altri file intatto"
fi

exit 0
