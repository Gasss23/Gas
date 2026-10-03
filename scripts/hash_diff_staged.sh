#!/usr/bin/env bash
# Stampa lo SHA-256 del diff STAGED (git diff --cached --binary) del repo corrente.
# Fonte unica dell'hash per il marcatore di review .claude/.review_ok:
#   - scripts/segna_review_ok.sh lo scrive dopo un verdetto APPROVATO;
#   - .claude/hooks/review_gate.sh lo ricalcola e lo confronta prima del commit.
# Un marcatore residuo (sessione precedente, diff cambiato dopo la review) non
# combacia più → il gate resta chiuso. Exit != 0 se git o l'hash falliscono.
set -o pipefail
# R-136-4: output indipendente dalla config git (colori, diff esterni, textconv, prefissi).
DIFF=$(git -c core.quotePath=false -c diff.noprefix=false -c diff.mnemonicPrefix=false \
  diff --cached --binary --no-color --no-ext-diff --no-textconv) || exit 1
if command -v sha256sum >/dev/null 2>&1; then
  printf '%s' "$DIFF" | sha256sum | cut -d' ' -f1
elif command -v shasum >/dev/null 2>&1; then
  printf '%s' "$DIFF" | shasum -a 256 | cut -d' ' -f1
else
  printf '%s' "$DIFF" | python3 -c "import hashlib,sys;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"
fi
