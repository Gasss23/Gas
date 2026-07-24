#!/usr/bin/env bash
set -euo pipefail

# Wrapper obbligatorio: questo script vive nella working dir su cui esso
# stesso fa `git checkout main && git pull --ff-only`. Bash legge lo script
# a chunk durante l'esecuzione (non lo parsa tutto in anticipo): un pull che
# modifica questo file a metà corsa può far eseguire byte misti tra la
# versione vecchia e quella nuova. Incapsulare tutto in una funzione forza
# bash a leggere l'intero corpo di main() (fino alla sua `}` di chiusura)
# prima di iniziare l'esecuzione, quindi un pull successivo non può più
# corrompere la corsa in atto.
main() {
PR="${1:?uso: gasmerge <numero-PR>}"
command -v jq >/dev/null || { echo "ERRORE: jq assente"; exit 1; }
cd ~/Gas || exit 1
git fetch --prune origin >/dev/null

gh pr view "$PR" --json headRefName,title,state > /tmp/gaspr.json
BRANCH=$(jq -r .headRefName /tmp/gaspr.json)
TITLE=$(jq -r .title /tmp/gaspr.json)
STATE=$(jq -r .state /tmp/gaspr.json)
[ "$STATE" = "OPEN" ] || { echo "BLOCCO: PR #$PR è $STATE"; exit 1; }

echo "=== PR #$PR — $TITLE"
echo "=== branch: $BRANCH"
echo
echo "--- FILE E DIFF ---"
git diff --stat "origin/main...origin/$BRANCH"
echo
echo "--- CHECK CI ---"
# `gh pr checks` da solo può uscire 0 anche con check ancora in corso: il
# --watch con --fail-fast attende l'esito reale, con un timeout duro per non
# restare appesi all'infinito. set +e/-e locale per catturare l'exit code
# senza far terminare lo script su un exit non-zero prima del case sotto.
set +e
timeout 900 gh pr checks "$PR" --watch --fail-fast --interval 10
CI_RC=$?
set -e
case "$CI_RC" in
  0) : ;;
  1) echo "BLOCCO: check CI falliti"; exit 1 ;;
  8) echo "BLOCCO: check CI ancora pending"; exit 1 ;;
  124) echo "BLOCCO: timeout (900s) in attesa dei check CI"; exit 1 ;;
  *) echo "BLOCCO: gh pr checks uscito con codice $CI_RC"; exit 1 ;;
esac
echo
echo "--- VERIFICA INDIPENDENTE CHECK (JSON) ---"
# Verifica finale indipendente dal --watch sopra: un exit 0 su "nessun check
# registrato" è indistinguibile da un exit 0 su "tutti verdi", e main-lock
# richiede che unit-suite sia effettivamente tra i check.
CHECKS_JSON=$(gh pr checks "$PR" --json name,bucket)
N_CHECKS=$(echo "$CHECKS_JSON" | jq 'length')
if [ "$N_CHECKS" -eq 0 ]; then
  echo "BLOCCO: zero check registrati su questa PR"; exit 1
fi
echo "$CHECKS_JSON" | jq -r '.[] | "\(.name): \(.bucket)"'
BAD_CHECKS=$(echo "$CHECKS_JSON" | jq -r '[.[] | select(.bucket != "pass" and .bucket != "skipping")] | length')
if [ "$BAD_CHECKS" -ne 0 ]; then
  echo "BLOCCO: esiste almeno un check con bucket diverso da pass/skipping"; exit 1
fi
echo "Tutti i check verdi (pass/skipping)."
echo
echo "--- INVARIANTE IP ---"
if git grep -qE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' "origin/$BRANCH" -- reports/; then
  echo "BLOCCO: trovato un IP in reports/"; exit 1
fi
echo "0 match OK"
echo
echo "--- FILE DI MOTORE ---"
ENGINE=$(git diff --name-only "origin/main...origin/$BRANCH" \
         | grep -E '^(gas\.py|brains/|modules/|tests/|scripts/|\.claude/)' || true)
if [ -n "$ENGINE" ]; then
  echo "$ENGINE"
  echo ">>> La PR tocca il MOTORE (o il gate di merge/hook stesso). Hai letto"
  echo ">>> il verdetto INTEGRALE del revisore in reports/handoff.md e lo"
  echo ">>> scope è quello che avevi deciso TU?"
else
  echo "nessuno (doc-only)"
fi
echo
echo "--- PROVENIENZA SCRIPT ---"
SELF_LOG=$(git log -1 --format='%h %ad' -- scripts/gasmerge.sh)
echo "scripts/gasmerge.sh @ ${SELF_LOG:-<mai committato>}"
if [ -n "$(git status --porcelain scripts/gasmerge.sh)" ]; then
  echo "*** GASMERGE MODIFICATO E NON COMMITTATO ***"
fi
echo
echo "Lo scope è quello che avevi chiesto? Se sì digita $PR, altrimenti INVIO per annullare."
read -r ANS
[ "$ANS" = "$PR" ] || { echo "ANNULLATO"; exit 1; }

gh pr merge "$PR" --merge --delete-branch
git checkout main && git pull --ff-only origin main
git branch -d "$BRANCH" 2>/dev/null || true
git fetch --prune
echo; echo "=== main ora: $(git log --oneline -1)"
echo "=== head su origin: $(git ls-remote --heads origin | wc -l)"
}

main "$@"
