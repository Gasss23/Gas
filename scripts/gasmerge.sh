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
# Fetta B2: `gasmerge --auto N` = merge senza prompt, SOLO se l'App di verifica (quella che
# il ruleset di main richiede) ha pubblicato il check verifica-bot in success sulla head.
AUTO=0
if [ "${1:-}" = "--auto" ]; then AUTO=1; shift; fi
# Validazione esplicita del parametro PR: messaggio su stderr, exit 2 (uso errato).
if [ -z "${1:-}" ] || [ -n "${2:-}" ]; then
  echo "uso: gasmerge [--auto] <numero-PR>" >&2
  exit 2
fi
if ! printf '%s' "$1" | grep -qE '^[0-9]+$'; then
  echo "uso: gasmerge [--auto] <numero-PR>  (argomento non numerico: '$1')" >&2
  exit 2
fi
PR="$1"
# functional check (non solo presenza): coerente con R-hook-jq / review #56.
jq --version >/dev/null 2>&1 || { echo "ERRORE: jq assente o non funzionante"; exit 1; }
# GAS_REPO_DIR override per i test; default = prod (stesso pattern di session_end.sh).
cd "${GAS_REPO_DIR:-$HOME/Gas}" || exit 1
# R-153-2: le X in fondo al template (BSD mktemp non randomizza "XXXXXX.json": un file
# rimasto da un'esecuzione interrotta bloccava ogni gasmerge successivo con "File exists").
GASPR_JSON=$(mktemp "${TMPDIR:-/tmp}/gaspr.XXXXXX") || { echo "ERRORE: mktemp fallito"; exit 1; }
export GASPR_JSON
trap 'rm -f "$GASPR_JSON"' EXIT
git fetch --prune origin >/dev/null

gh pr view "$PR" --json headRefName,title,state > "$GASPR_JSON"
BRANCH=$(jq -r .headRefName "$GASPR_JSON")
TITLE=$(jq -r .title "$GASPR_JSON")
STATE=$(jq -r .state "$GASPR_JSON")
[ "$STATE" = "OPEN" ] || { echo "BLOCCO: PR #$PR è $STATE"; exit 1; }
# V-3 verifica esterna #127: la head si cattura QUI, prima di ogni controllo, e i controlli
# (IP, file di motore, check del bot) leggono QUEL commit, non un ref che può muoversi.
# Il merge usa --match-head-commit sullo stesso SHA: si mergia esattamente ciò che si è visto.
HEAD_SHA=$(gh pr view "$PR" --json headRefOid --jq '.headRefOid')
[ -n "$HEAD_SHA" ] || { echo "BLOCCO: HEAD_SHA vuoto — head non verificabile"; exit 1; }
REF_SHA=$(git rev-parse --verify -q "refs/remotes/origin/$BRANCH^{commit}" || true)
if [ "$REF_SHA" != "$HEAD_SHA" ]; then
  echo "BLOCCO: refs/remotes/origin/$BRANCH (${REF_SHA:-<assente>}) non coincide con la head della PR ($HEAD_SHA)"
  exit 1
fi

echo "=== PR #$PR — $TITLE"
echo "=== branch: $BRANCH"
echo
echo "--- FILE E DIFF ---"
git diff --stat "refs/remotes/origin/main...$HEAD_SHA"
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

# Secondo fetch dopo l'attesa CI (potenzialmente 900s): un push durante l'attesa
# sposta il ref → la head vista dai check non è più quella catturata → BLOCCO.
git fetch --prune origin >/dev/null
REF_SHA=$(git rev-parse --verify -q "refs/remotes/origin/$BRANCH^{commit}" || true)
if [ "$REF_SHA" != "$HEAD_SHA" ]; then
  echo "BLOCCO: head cambiata durante l'attesa CI ($HEAD_SHA → ${REF_SHA:-<assente>}) — riavvia gasmerge"
  exit 1
fi

echo
echo "--- INVARIANTE IP ---"
# Gate deny-by-default su tutto l'albero del branch: qualsiasi riga con IP
# quad-dotted viene bloccata. Eccezione esplicita: se la riga contiene il
# token letterale "gasmerge-ip-ok" è allowlistata (vouch umano per esempi
# o fixture che devono contenere indirizzi noti). Il gate resta disciplinare
# anche dopo il filtro: rc>=2 dal filtro = errore reale del filtro → BLOCCO
# (mai fail-open). Il marker va sulla riga sorgente dell'esempio, NON sui
# file temporanei scritti dal test (così il guard li becca comunque).
set +e
# R-148-2: tree risolto UNA volta (le due git grep sotto vedono lo stesso albero
# anche se un fetch concorrente sposta il ref). R-148-3: -a e LC_ALL=C, così file
# binari e righe non UTF-8 non escono dal controllo.
# V-3 #127: il tree è quello di HEAD_SHA (il commit che si mergerà).
if ! IP_TREE=$(git rev-parse --verify -q "$HEAD_SHA^{tree}"); then
  echo "BLOCCO: tree di $HEAD_SHA non risolvibile — verifica IP NON eseguita"
  exit 1
fi
# R-155-1: un IP adiacente a un punto (a fine frase, "<IP>.nip.io", "host.<IP>")
# è un IP; "1.2.3.4.5" (punto seguito o preceduto da una cifra) no.
IP_MATCHES=$(LC_ALL=C git grep -a -nE '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)' "$IP_TREE")
IP_RC=$?
set -e
case "$IP_RC" in
  1) echo "0 IP trovati — OK" ;;
  0)
    # Step 1: rimuovi le righe con soli IP di loopback (127.x.x.x).
    # Logica: per ogni riga, cancella tutti i 127.x.x.x con sed; se nel residuo
    # resta ancora un IPv4 quad-dotted, la riga originale non è loopback-only e
    # viene tenuta. Una riga con loopback E un IP non-loopback non è esente.
    set +e
    # V-2 #124/#125: anche `read` in C. In locale UTF-8 bash 5 legge un byte non UTF-8
    # seguito dal newline come un carattere multibyte: il newline sparisce, l'ultima
    # riga va persa e il suo IP passava come "loopback" (fail-open).
    NON_LOOPBACK=$(echo "$IP_MATCHES" | while IFS= LC_ALL=C read -r line; do
      stripped=$(echo "$line" | LC_ALL=C sed -E 's/127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}//g')
      if echo "$stripped" | LC_ALL=C grep -qE '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)'; then
        echo "$line"
      fi
    done)
    set -e
    if [ -z "$NON_LOOPBACK" ]; then
      echo "Tutti gli IP sono loopback (127.x.x.x) — OK"
    else
      # Step 2: allowlist esplicita. R-147-1: il marker si cerca nel solo
      # CONTENUTO della riga (`git grep --and --not`), non nell'output intero:
      # il prefisso `<ref>:<path>:` di git grep conteneva branch e path, quindi
      # un branch o un file chiamato "...gasmerge-ip-ok..." allowlistava tutto.
      set +e
      UNMARKED=$(LC_ALL=C git grep -a -nE -e '(^|[^0-9.]|(^|[^0-9])\.)[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|\.([^0-9]|$)|$)' --and --not -e 'gasmerge-ip-ok' "$IP_TREE")
      UNMARKED_RC=$?
      set -e
      case "$UNMARKED_RC" in
        0|1) : ;;
        *) echo "BLOCCO: git grep (allowlist) uscito con codice $UNMARKED_RC — gate IP non verificato"; exit 1 ;;
      esac
      set +e
      RESIDUAL=$(printf '%s\n' "$NON_LOOPBACK" | LC_ALL=C grep -Fx -f <(printf '%s\n' "$UNMARKED"))
      FILTER_RC=$?
      set -e
      case "$FILTER_RC" in
        1) echo "Tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK" ;;
        0)
          echo "BLOCCO: trovati IP non allowlistati nell'albero del branch:"
          echo "$RESIDUAL"
          exit 1
          ;;
        *)
          echo "BLOCCO: errore nel filtro allowlist (rc=$FILTER_RC) — gate IP non verificato"
          exit 1
          ;;
      esac
    fi
    ;;
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
# R-145-1: --no-renames (un rename fuori dal perimetro mostra anche il vecchio
# path) e quotePath=false (nomi non-ASCII non quotati) — stesso trattamento di
# check_handoff/review_gate.
# V-3 verifica esterna #122: -z, perché anche con quotePath=false git quota i
# nomi con apice, tab o backslash (e il confronto col perimetro falliva). I NUL
# diventano a-capo: resta escluso solo un nome che contiene un a-capo.
ENGINE_DIFF=$(git -c core.quotePath=false diff -z --no-renames --name-only "refs/remotes/origin/main...$HEAD_SHA" | tr '\0' '\n')
DIFF_RC=$?
set -e
if [ "$DIFF_RC" -ne 0 ]; then
  echo "BLOCCO: git diff uscito con codice $DIFF_RC — verifica file-motore NON eseguita"
  exit 1
fi
# R-144-1 / V-1 verifica esterna PR #121: le voci vengono dalla fonte unica
# .claude/perimetro_review.txt, UNIONE della versione di main e di quella del
# branch (un branch che restringe il perimetro non si declassa da solo), più
# le cartelle storiche scripts/ e .claude/. Perimetro illeggibile su entrambi
# i lati → ogni file conta come motore (fail-safe: il promemoria non tace).
PERIM_VOCI=$( { git show "refs/remotes/origin/main:.claude/perimetro_review.txt" 2>/dev/null || true
                git show "$HEAD_SHA:.claude/perimetro_review.txt" 2>/dev/null || true
                printf 'scripts/\n.claude/\n'; } \
  | sed -e 's/#.*//' -e 's/[[:space:]]//g' | grep -v '^$' | sort -u)
PERIM_LETTO=1
git cat-file -e "refs/remotes/origin/main:.claude/perimetro_review.txt" 2>/dev/null \
  || git cat-file -e "$HEAD_SHA:.claude/perimetro_review.txt" 2>/dev/null \
  || PERIM_LETTO=0
ENGINE=""
# R-167-1: anche qui `read` in C (stessa classe del gate IP: un path che finisce con un
# byte non UTF-8 si mangerebbe il newline e il file di motore seguente).
while IFS= LC_ALL=C read -r f; do
  [ -n "$f" ] || continue
  if [ "$PERIM_LETTO" -eq 0 ]; then ENGINE+="$f"$'\n'; continue; fi
  while IFS= LC_ALL=C read -r v; do
    case "$v" in
      */) [[ "$f" == "$v"* ]] && { ENGINE+="$f"$'\n'; break; } ;;
      *)  [[ "$f" == "$v" ]] && { ENGINE+="$f"$'\n'; break; } ;;
    esac
  done <<< "$PERIM_VOCI"
done <<< "$ENGINE_DIFF"
if [ "$PERIM_LETTO" -eq 0 ]; then
  echo "ATTENZIONE: .claude/perimetro_review.txt illeggibile su main e sul branch — ogni file conta come motore"
fi
if [ -n "$ENGINE" ]; then
  printf '%s' "$ENGINE"
  echo ">>> La PR tocca il PERIMETRO DI REVIEW (motore o macchina di controllo). Hai"
  echo ">>> letto il verdetto INTEGRALE del revisore in reports/handoff.md e lo"
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
if [ "$AUTO" -eq 1 ]; then
  echo "--- VERIFICA-BOT (merge automatico) ---"
  if [ -n "$(git status --porcelain scripts/gasmerge.sh)" ]; then
    echo "BLOCCO: gasmerge modificato e non committato — niente merge automatico"; exit 1
  fi
  # G-1 verifica chat #130: il sì del bot è il check `verifica-bot` dell'App. Quale App lo
  # dice SOLO il ruleset di main (integration_id del check richiesto): se il ruleset non lo
  # richiede, il setup non è finito e il merge automatico non esiste.
  set +e
  RULES=$(gh api "repos/{owner}/{repo}/rules/branches/main")
  RULES_RC=$?
  BOT_ID=$(printf '%s' "$RULES" | jq -r '[.[] | select(.type == "required_status_checks")
    | .parameters.required_status_checks[]? | select(.context == "verifica-bot")
    | .integration_id // empty] | first // empty' 2>/dev/null)
  set -e
  if [ "$RULES_RC" -ne 0 ]; then
    echo "BLOCCO: regole di main non leggibili (rc=$RULES_RC) — merge automatico annullato"; exit 1
  fi
  if ! printf '%s' "$BOT_ID" | grep -qE '^[0-9]+$'; then
    echo "BLOCCO: il ruleset di main non richiede il check verifica-bot di un'App — merge automatico non disponibile (setup F)"
    exit 1
  fi
  set +e
  RUNS=$(gh api "repos/{owner}/{repo}/commits/$HEAD_SHA/check-runs?check_name=verifica-bot&filter=all&per_page=100")
  RUNS_RC=$?
  # G-2: un NO dell'App su questo SHA resta NO; altrimenti conta l'ULTIMO check dell'App.
  ESITO_BOT=$(printf '%s' "$RUNS" | jq -r --argjson id "$BOT_ID" '
    if (.total_count // 0) > (.check_runs | length) then "elenco troncato" else
    [.check_runs[] | select(.app.id == $id)]
    | if length == 0 then "nessun check"
      elif any(.conclusion == "failure") then "NO"
      else (sort_by(.id) | last
            | if .status == "completed" then (.conclusion // "senza conclusione")
              else "in corso" end) end end' 2>/dev/null)
  ESITO_RC=$?
  set -e
  if [ "$RUNS_RC" -ne 0 ] || [ "$ESITO_RC" -ne 0 ]; then
    echo "BLOCCO: check verifica-bot non leggibili (gh rc=$RUNS_RC, jq rc=$ESITO_RC) — merge automatico annullato"
    exit 1
  fi
  case "$ESITO_BOT" in
    success) echo "verifica-bot dell'App $BOT_ID: success su $HEAD_SHA — OK" ;;
    NO) echo "BLOCCO: il bot ha detto NO su $HEAD_SHA (G-2): serve un commit nuovo"; exit 1 ;;
    *) echo "BLOCCO: verifica-bot su $HEAD_SHA: $ESITO_BOT — il merge automatico vuole success"; exit 1 ;;
  esac
else
  echo "Lo scope è quello che avevi chiesto? Se sì digita $PR, altrimenti INVIO per annullare."
  read -r ANS
  [ "$ANS" = "$PR" ] || { echo "ANNULLATO"; exit 1; }
fi

# Ri-verifica TOCTOU post-conferma: ri-fetch + ri-lettura head.
# Blocca se la head è cambiata mentre attendevamo al prompt (finestra umana).
git fetch --prune origin >/dev/null
set +e
NEW_HEAD=$(gh pr view "$PR" --json headRefOid --jq '.headRefOid')
TOCTOU_RC=$?
set -e
if [ "$TOCTOU_RC" -ne 0 ]; then
  echo "BLOCCO: ri-lettura head PR fallita (rc=$TOCTOU_RC) — merge annullato per sicurezza"
  exit 1
fi
[ -n "$NEW_HEAD" ] || { echo "BLOCCO: NEW_HEAD vuoto (ri-lettura post-conferma) — head non verificabile"; exit 1; }
if [ "$NEW_HEAD" != "$HEAD_SHA" ]; then
  echo "BLOCCO: head cambiata durante la conferma ($HEAD_SHA → $NEW_HEAD) — riavvia gasmerge"
  exit 1
fi
[ "$AUTO" -eq 0 ] || echo "=== MERGE AUTOMATICO di #$PR su $HEAD_SHA"
gh pr merge "$PR" --merge --delete-branch --match-head-commit "$HEAD_SHA"
git checkout main && git pull --ff-only origin main
git branch -d "$BRANCH" 2>/dev/null || true
git fetch --prune
echo; echo "=== main ora: $(git log --oneline -1)"
echo "=== head su origin: $(git ls-remote --heads origin | wc -l)"
}

main "$@"
