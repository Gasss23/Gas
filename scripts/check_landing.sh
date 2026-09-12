#!/usr/bin/env bash
# check_landing.sh — verifica pre-merge: file obbligatori presenti, HEAD pushato, PR aperta.
# Check A (file) e Check B (HEAD pushato) sono BLOCCANTI (exit 1).
# Check C (PR GitHub) è BLOCCANTE solo se gh è disponibile e autenticato;
# se gh è assente o non autenticato → WARN + skip (non bloccante).

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"
if [[ -z "$PROJECT_DIR" ]]; then
    echo "check_landing: WARN — impossibile determinare PROJECT_DIR" >&2
    exit 0
fi

BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
EXIT_CODE=0

# ── CHECK A: file obbligatori presenti e non vuoti ───────────────────────────
REQUIRED_FILES=(
    "reports/ultimo_report.md"
    "reports/handoff.md"
    "reports/diff_sessione.md"
)

for f in "${REQUIRED_FILES[@]}"; do
    full="${PROJECT_DIR}/${f}"
    if [[ ! -f "$full" || ! -s "$full" ]]; then
        echo "check_landing [A] FAIL: ${f} assente o vuoto" >&2
        EXIT_CODE=1
    fi
done

# ── CHECK B: HEAD pushato su origin/$BRANCH ──────────────────────────────────
LOCAL_HEAD=$(git -C "$PROJECT_DIR" rev-parse HEAD 2>/dev/null || echo "")
REMOTE_HEAD=$(git -C "$PROJECT_DIR" rev-parse "origin/${BRANCH}" 2>/dev/null || echo "")

if [[ -z "$REMOTE_HEAD" ]]; then
    echo "check_landing [B] FAIL: origin/${BRANCH} non esiste — effettua git push prima" >&2
    EXIT_CODE=1
elif [[ "$LOCAL_HEAD" != "$REMOTE_HEAD" ]]; then
    echo "check_landing [B] FAIL: HEAD locale (${LOCAL_HEAD:0:8}) != origin/${BRANCH} (${REMOTE_HEAD:0:8})" >&2
    EXIT_CODE=1
fi

if [[ $EXIT_CODE -ne 0 ]]; then
    exit 1
fi

# ── CHECK C: PR aperta su GitHub ─────────────────────────────────────────────
if ! command -v gh &>/dev/null; then
    echo "check_landing [C] WARN: gh non installato — skip verifica PR" >&2
    exit 0
fi

if ! gh auth status &>/dev/null; then
    echo "check_landing [C] WARN: gh non autenticato — skip verifica PR" >&2
    exit 0
fi

PR_JSON=$(gh pr list --head "$BRANCH" --base main --json number,url 2>/dev/null) || {
    echo "check_landing [C] WARN: gh pr list fallito — skip verifica PR" >&2
    exit 0
}

if [[ "$PR_JSON" == "[]" || -z "$PR_JSON" ]]; then
    echo "check_landing [C] FAIL: nessuna PR aperta per ${BRANCH} → main" >&2
    exit 1
fi

echo "check_landing: OK — A (file), B (pushed), C (PR aperta)"
exit 0
