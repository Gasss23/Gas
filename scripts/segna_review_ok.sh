#!/usr/bin/env bash
# Crea il marcatore di review DOPO un verdetto APPROVATO / APPROVATO CON RISERVE:
# scrive in .claude/.review_ok lo SHA-256 del diff staged revisionato. Il gate
# (review_gate.sh) accetta il commit solo se il diff staged ha ancora quell'hash.
set -o pipefail
ROOT=$(git rev-parse --show-toplevel) || exit 1
H=$(cd "$ROOT" && bash scripts/hash_diff_staged.sh) || { echo "segna_review_ok: hash del diff fallito" >&2; exit 1; }
[ -n "$H" ] || { echo "segna_review_ok: hash vuoto" >&2; exit 1; }
mkdir -p "$ROOT/.claude"
printf '%s\n' "$H" > "$ROOT/.claude/.review_ok"
echo "marcatore review scritto: $H"
