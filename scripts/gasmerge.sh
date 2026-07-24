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
# Validazione esplicita del parametro PR: messaggio su stderr, exit 2 (uso errato).
if [ -z "${1:-}" ]; then
  echo "uso: gasmerge <numero-PR>" >&2
  exit 2
fi
if ! printf '%s' "$1" | grep -qE '^[0-9]+$'; then
  echo "uso: gasmerge <numero-PR>  (argomento non numerico: '$1')" >&2
  exit 2
fi
PR="$1"
# functional check (non solo presenza): coerente con R-hook-jq / review #56.
jq --version >/dev/null 2>&1 || { echo "ERRORE: jq assente o non funzionante"; exit 1; }
# GAS_REPO_DIR override per i test; default = prod (stesso pattern di session_end.sh).
cd "${GAS_REPO_DIR:-$HOME/Gas}" || exit 1
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

# Secondo fetch dopo l'attesa CI (potenzialmente 900s): aggiorna i refs prima
# dei controlli invariante, così IP e file-motore leggono lo stato attuale.
git fetch --prune origin >/dev/null

echo
echo "--- INVARIANTE IP ---"
# Pattern: set +e / RC / set -e per distinguere 0 (match), 1 (nessun match),
# >=2 (errore reale) — stesso schema delle righe 35-45.
# Scope: tutto l'albero del branch (non solo reports/).
set +e
IP_MATCHES=$(git grep -nE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' "origin/$BRANCH")
IP_RC=$?
set -e
case "$IP_RC" in
  0)
    echo "BLOCCO: trovato IP nell'albero del branch:"
    echo "$IP_MATCHES"
    exit 1
    ;;
  1) echo "0 match OK" ;;
  *)
    echo "BLOCCO: git grep uscito con codice $IP_RC — verifica IP NON eseguita"
    exit 1
    ;;
esac
echo
echo "--- FILE DI MOTORE ---"
# Separa le due operazioni: prima il diff (set -e ferma su errore git), poi il
# grep con distinzione rc 0/1/altro — evita che un errore git sia silenzioso.
set +e
ENGINE_DIFF=$(git diff --name-only "origin/main...origin/$BRANCH")
DIFF_RC=$?
set -e
if [ "$DIFF_RC" -ne 0 ]; then
  echo "BLOCCO: git diff uscito con codice $DIFF_RC — verifica file-motore NON eseguita"
  exit 1
fi
set +e
ENGINE=$(echo "$ENGINE_DIFF" | grep -E '^(gas\.py|brains/|modules/|tests/|scripts/|\.claude/)')
GREP_RC=$?
set -e
case "$GREP_RC" in
  0)
    echo "$ENGINE"
    echo ">>> La PR tocca il MOTORE (o il gate di merge/hook stesso). Hai letto"
    echo ">>> il verdetto INTEGRALE del revisore in reports/handoff.md e lo"
    echo ">>> scope è quello che avevi deciso TU?"
    ;;
  1) echo "nessuno (doc-only)" ;;
  *) echo "BLOCCO: grep file-motore uscito con codice $GREP_RC"; exit 1 ;;
esac
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

# Cattura SHA head PR nello stesso momento dei controlli per chiudere il TOCTOU:
# gh pr merge fallisce se la head è cambiata dopo i controlli.
HEAD_SHA=$(gh pr view "$PR" --json headRefOid --jq '.headRefOid')
gh pr merge "$PR" --merge --delete-branch --match-head-commit "$HEAD_SHA"
git checkout main && git pull --ff-only origin main
git branch -d "$BRANCH" 2>/dev/null || true
git fetch --prune
echo; echo "=== main ora: $(git log --oneline -1)"
echo "=== head su origin: $(git ls-remote --heads origin | wc -l)"
}

main "$@"
