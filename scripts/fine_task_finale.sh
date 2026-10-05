#!/usr/bin/env bash
# fine_task_finale.sh — gate pre-commit + push + URL_HANDOFF (deterministico).
#
# Uso (da 4bis di /fine-task, DOPO il commit):
#   bash scripts/fine_task_finale.sh
#
# Ordine:
#   1. Gate A — check_handoff.py
#   2. Gate B — check_verdetto.py
#   3. Gate IP — nessun IP nell'albero del branch (identico a gasmerge.sh: loopback ok, token gasmerge-ip-ok ok)
#   4. Push del branch corrente (MAI main)
#   5. Guardia HEAD == @{u}
#   6. URL_HANDOFF con SHA lungo (solo se handoff.md è stato rigenerato in questa sessione)
#
# Qualunque gate rosso → exit 1 + messaggio chiaro, nessun push.

set -uo pipefail

SCRIPT_DIR=$(dirname "$(realpath "$0")")

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
if [[ -z "$PROJECT_DIR" ]]; then
    PROJECT_DIR=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null) || {
        printf 'fine_task_finale: ERRORE impossibile determinare PROJECT_DIR.\n' >&2
        exit 1
    }
fi

# R2: entra in PROJECT_DIR per coerenza tra gate Python (cwd-dipendenti) e operazioni git
cd "$PROJECT_DIR" || {
    printf 'fine_task_finale: ERRORE impossibile entrare in PROJECT_DIR=%s\n' "$PROJECT_DIR" >&2
    exit 1
}

# Guardia main (MAI push su main)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
if [[ -z "$BRANCH" ]] || [[ "$BRANCH" == "main" ]]; then
    printf 'fine_task_finale: ERRORE BRANCH="%s" — rifiuto push su main o HEAD non valido.\n' \
        "$BRANCH" >&2
    exit 1
fi

# Gate A — coerenza §2 GIT DIFF --STAT
printf '=== Gate A: check_handoff ===\n' >&2
python3 "${SCRIPT_DIR}/check_handoff.py"
GA=$?
if [[ $GA -ne 0 ]]; then
    printf 'fine_task_finale: STOP — check_handoff rosso (exit %d). Correggi §2 in handoff.md e ripeti.\n' \
        "$GA" >&2
    exit 1
fi

# Gate B — citazioni §4 VERDETTO
printf '=== Gate B: check_verdetto ===\n' >&2
python3 "${SCRIPT_DIR}/check_verdetto.py"
GB=$?
if [[ $GB -ne 0 ]]; then
    printf 'fine_task_finale: STOP — check_verdetto rosso (exit %d). Correggi §4 in handoff.md e ripeti.\n' \
        "$GB" >&2
    exit 1
fi

# Gate IP — logica identica a gasmerge.sh: tutto l'albero, stesso regex, stesso filtro loopback+allowlist.
# Step 1: loopback-only (per riga, via sed). Step 2: gasmerge-ip-ok allowlist.
printf '=== Gate IP ===\n' >&2
set +e
# R-148-2/R-148-3: come gasmerge.sh — tree risolto una volta, -a e LC_ALL=C.
if ! IP_TREE=$(git rev-parse --verify -q "HEAD^{tree}"); then
  printf 'fine_task_finale: STOP — tree di HEAD non risolvibile — verifica IP NON eseguita\n' >&2
  exit 1
fi
# R-155-1: come gasmerge.sh — IP adiacente a un punto incluso, "1.2.3.4.5" escluso.
IP_MATCHES=$(LC_ALL=C git grep -a -nE '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)' "$IP_TREE")
IP_RC=$?
set -e
case "$IP_RC" in
  1) printf 'Gate IP: 0 IP trovati — OK\n' >&2 ;;
  0)
    # Step 1: rimuovi righe con soli IP di loopback (127.x.x.x).
    # Per ogni riga, cancella tutti i 127.x.x.x con sed; se nel residuo
    # resta ancora un IPv4 quad-dotted, la riga non è loopback-only.
    # Una riga con loopback E un IP non-loopback non è esente.
    set +e
    NON_LOOPBACK=$(printf '%s\n' "$IP_MATCHES" | while IFS= read -r line; do
      stripped=$(printf '%s\n' "$line" | LC_ALL=C sed -E 's/127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}//g')
      if printf '%s\n' "$stripped" | LC_ALL=C grep -qE '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)'; then
        printf '%s\n' "$line"
      fi
    done)
    set -e
    if [[ -z "$NON_LOOPBACK" ]]; then
      printf 'Gate IP: tutti gli IP sono loopback (127.x.x.x) — OK\n' >&2
    else
      # Step 2: allowlist esplicita sul solo CONTENUTO (R-147-1, come gasmerge.sh):
      # un path che contiene "gasmerge-ip-ok" non allowlista più le sue righe.
      set +e
      UNMARKED=$(LC_ALL=C git grep -a -nE -e '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)' --and --not -e 'gasmerge-ip-ok' "$IP_TREE")
      UNMARKED_RC=$?
      set -e
      case "$UNMARKED_RC" in
        0|1) : ;;
        *) printf 'fine_task_finale: STOP — git grep (allowlist) uscito con codice %d — gate IP non verificato\n' "$UNMARKED_RC" >&2; exit 1 ;;
      esac
      set +e
      RESIDUAL=$(printf '%s\n' "$NON_LOOPBACK" | LC_ALL=C grep -Fx -f <(printf '%s\n' "$UNMARKED"))
      FILTER_RC=$?
      set -e
      case "$FILTER_RC" in
        1) printf 'Gate IP: tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK\n' >&2 ;;
        0)
          printf 'fine_task_finale: STOP — IP trovato nell'\''albero del branch — sostituisci con <IP-redatto> o aggiungi gasmerge-ip-ok e ripeti.\n' >&2
          printf '%s\n' "$RESIDUAL" >&2
          exit 1
          ;;
        *)
          printf 'fine_task_finale: STOP — errore nel filtro allowlist (rc=%d) — gate IP non verificato\n' "$FILTER_RC" >&2
          exit 1
          ;;
      esac
    fi
    ;;
  *)
    printf 'fine_task_finale: STOP — git grep uscito con codice %d — verifica IP NON eseguita\n' "$IP_RC" >&2
    exit 1
    ;;
esac

# Push
printf '=== Push ===\n' >&2
git push
PUSH_EXIT=$?
if [[ $PUSH_EXIT -ne 0 ]]; then
    printf 'fine_task_finale: ERRORE git push fallito (exit %d).\n' "$PUSH_EXIT" >&2
    exit 1
fi

# Guardia HEAD == @{u}
git fetch origin 2>/dev/null || true
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "@{u}" 2>/dev/null || true)
if [[ -z "$REMOTE" ]] || [[ "$LOCAL" != "$REMOTE" ]]; then
    printf 'fine_task_finale: ERRORE HEAD (%s) != @{u} (%s) — URL non valido.\n' \
        "$LOCAL" "$REMOTE" >&2
    exit 1
fi

# B2: stampa URL solo se handoff.md è stato rigenerato in questa sessione
BASE=$(git merge-base refs/remotes/origin/main HEAD 2>/dev/null || true)
if [[ -n "$BASE" ]] && git diff --quiet "${BASE}..HEAD" -- reports/handoff.md 2>/dev/null; then
    printf 'URL_HANDOFF: non disponibile — handoff.md non rigenerato in questa sessione\n'
    exit 0
fi

# URL_HANDOFF con SHA lungo
SHA=$(git rev-parse HEAD)
printf 'URL_HANDOFF: https://raw.githubusercontent.com/Gasss23/Gas/%s/reports/handoff.md\n' "$SHA"
