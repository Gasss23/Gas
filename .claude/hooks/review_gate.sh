#!/usr/bin/env bash
# PreToolUse hook (Bash) — gate di review DETERMINISTICO.
# Blocca (exit 2) un `git commit` il cui diff STAGED tocca il PERIMETRO DI REVIEW
# (.claude/perimetro_review.txt: motore + macchina di controllo — hook, gate,
# revisore, CI; V-1 verifica esterna PR #118) se manca il marcatore .claude/.review_ok
# o se il marcatore non contiene l'hash del diff staged attuale; blocca anche
# se nel working tree ci sono modifiche al motore NON staged o non tracciate
# (R-136-1: `commit -a`, pathspec o `add && commit` le farebbero entrare dopo
# il controllo, che vede solo l'index del momento).
# Costringe a far passare il diff dal subagent `revisore` prima del commit.
#
# Limiti dichiarati (best-effort, per design):
#  - Il matcher sul testo del comando NON copre tutte le forme di `git commit`
#    (alias, heredoc esotici, git -C): e' una RETE sopra la regola di workflow
#    di CLAUDE.md sez.3, non un sostituto. La barriera primaria resta l'istruzione.
#  - Legge il comando da tool_input.command (JSON su stdin), non da `cat` grezzo.
#  - L'input hook puo' essere un array JSON [{...}] o un oggetto {}: gestito.
#  - L'hook gira dal WORKING TREE: un hook modificato e non in stage esegue se
#    stesso. Il controllo del working tree blocca il COMMIT di qualunque file del
#    perimetro fuori stage, ma non può impedire che la versione manomessa giri.
#  - Il marcatore lega il DIFF, non il verdetto: scripts/segna_review_ok.sh si può
#    lanciare senza review (la barriera resta la regola di CLAUDE.md sez.3).
#  - Un indice alternativo (GIT_INDEX_FILE=...) è fuori controllo (R-137-3).

: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"
INPUT=$(cat)

# Parser JSON a cascata: jq -> python3 (se funziona) -> python -> perl
# Usiamo test di esecuzione reale (non solo command -v) perche' su Windows
# python3 puo' essere uno stub Microsoft Store che esiste ma exit != 0.
_parse_cmd() {
  if command -v jq >/dev/null 2>&1; then
    # NB: NON usare `(.[0] // .)`: su un oggetto `.[0]` e' un ERRORE (non null) e
    # jq 1.7 non lo sopprime con `//` → parse fallito → gate inerte (fail-open,
    # misurato 2026-10-03 su jq-1.7.1-apple con l'input oggetto di Claude Code).
    jq -r 'if type == "array" then .[0] else . end | .tool_input.command // empty'
  elif python3 -c "import sys" >/dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  elif python -c "import sys" >/dev/null 2>&1; then
    python -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  else
    perl -MJSON::PP -e 'my $d=JSON::PP->new->decode(do{local$/;<STDIN>}); my $o=ref($d)eq"ARRAY"?$d->[0]:$d; print $o->{tool_input}{command}//"" if $o->{tool_input}'
  fi
}

CMD=$(printf '%s' "$INPUT" | _parse_cmd 2>/dev/null)
PARSE_RC=$?
if [ "$PARSE_RC" -ne 0 ]; then
  # Parser fallito: non sappiamo se e' un commit. FAIL-CLOSED: il controllo
  # "e' un git commit?" si fa sul testo GREZZO dell'input, cosi' un commit non
  # sfugge al gate per un JSON inatteso (i comandi non-commit restano liberi).
  CMD="$INPUT"
fi
[ -n "$CMD" ] || exit 0

# Non e' un git commit -> non interferire
printf '%s' "$CMD" | grep -Eq 'git[[:space:]].*commit' || exit 0

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || {
  echo "BLOCCATO (gate review): cd in CLAUDE_PROJECT_DIR ('$CLAUDE_PROJECT_DIR') fallito — fail-closed." >&2
  exit 2
}

# Perimetro di review: fonte unica .claude/perimetro_review.txt. R-138-1: il
# perimetro NON può togliersi da solo dalla lista. Le voci sono l'UNIONE di:
#   (1) voci cablate qui sotto (il perimetro stesso e gli hook: non rimovibili);
#   (2) il file accanto all'hook (working tree; vale anche nei test su repo temporanei);
#   (3) la versione in stage (`git show :...`) e (4) quella di HEAD.
# Restringere il perimetro richiede quindi un commit revisionato: finché la riga
# è in HEAD o nell'index, conta. File del working tree assente → fail-closed.
PERIM_FILE="$(dirname "$0")/../perimetro_review.txt"
PERIM_PATHS=()
PERIM_RE_PARTS=()
_aggiungi_voci() {
  local riga esc
  while IFS= read -r riga || [ -n "$riga" ]; do
    riga="${riga%%#*}"
    riga="$(printf '%s' "$riga" | tr -d '[:space:]')"
    [ -n "$riga" ] || continue
    PERIM_PATHS+=("${riga%/}")
    esc=$(printf '%s' "$riga" | sed 's/[][\.*^$()+?{}|]/\\&/g')
    case "$riga" in
      */) PERIM_RE_PARTS+=("$esc") ;;
      *)  PERIM_RE_PARTS+=("$esc\$") ;;
    esac
  done
}
if [ ! -r "$PERIM_FILE" ]; then
  echo "BLOCCATO (gate review): perimetro di review assente ($PERIM_FILE) — fail-closed." >&2
  exit 2
fi
_aggiungi_voci < "$PERIM_FILE"
if [ "${#PERIM_PATHS[@]}" -eq 0 ]; then
  echo "BLOCCATO (gate review): perimetro di review vuoto ($PERIM_FILE) — fail-closed." >&2
  exit 2
fi
_aggiungi_voci <<'VOCI_CABLATE'
.claude/perimetro_review.txt
.claude/hooks/
VOCI_CABLATE
_aggiungi_voci < <(git show :.claude/perimetro_review.txt 2>/dev/null)
_aggiungi_voci < <(git show HEAD:.claude/perimetro_review.txt 2>/dev/null)
PERIM_RE="^($(IFS='|'; printf '%s' "${PERIM_RE_PARTS[*]}"))"

# Il diff staged tocca il perimetro? — verifica FAIL-CLOSED.
# In una pipeline bash l'exit code finale e' quello dell'ultimo comando, non di
# git: un git failure risulterebbe in exit 0 (fail-open, review #80). Il subshell
# qui sotto esce ESPLICITAMENTE con l'exit code di git (PIPESTATUS[0]), non di `tr`.
# R-138-2: --no-renames (un rename dal perimetro verso fuori mostra anche il path
# di origine) e -z (nomi non-ASCII o con virgolette arrivano grezzi, non quotati).
# R-139 (blocco): la pipeline con `tr` NON deve nascondere l'exit code di git —
# il subshell esce con quello di git (PIPESTATUS[0]), non con quello di tr.
DIFF_OUT=$(git diff --cached --name-only --no-renames -z 2>/dev/null | tr '\0' '\n'; exit "${PIPESTATUS[0]}")
GIT_RC=$?
if [ "$GIT_RC" -ne 0 ]; then
  echo "BLOCCATO (gate review): 'git diff --cached' fallito (exit $GIT_RC) — impossibile verificare il diff motore, fail-closed." >&2
  exit 2
fi

# R-136-1: modifiche al motore fuori dall'index (non staged o non tracciate)
# possono entrare nel commit DOPO questo controllo (`commit -a`, pathspec,
# `add && commit`). Fail-closed: il commit si fa solo con il motore tutto in
# stage (e revisionato) oppure tutto pulito.
WT_OUT=$(git status --porcelain --no-renames --untracked-files=all -- "${PERIM_PATHS[@]}" 2>/dev/null)
WT_RC=$?
if [ "$WT_RC" -ne 0 ]; then
  echo "BLOCCATO (gate review): 'git status' fallito (exit $WT_RC) — fail-closed." >&2
  exit 2
fi
if printf '%s\n' "$WT_OUT" | grep -qE '^(.[^ ]|\?\?) '; then
  echo "BLOCCATO (gate review): ci sono modifiche NON in stage (o file non tracciati) nel perimetro di review (.claude/perimetro_review.txt). Mettile in stage e falle revisionare, oppure mettile da parte (git stash), poi riprova." >&2
  exit 2
fi
if ! printf '%s\n' "$DIFF_OUT" | grep -qE "$PERIM_RE"; then
  exit 0   # nessun file del perimetro in stage: commit doc/report consentito
fi

# Marcatore di review: contiene lo SHA-256 del diff staged revisionato (scritto da
# scripts/segna_review_ok.sh DOPO il verdetto). Consentito SOLO se combacia col
# diff staged attuale: un marcatore residuo di una sessione precedente, vuoto
# (vecchio `touch`) o di un diff cambiato dopo la review NON apre il gate.
if [ -f .claude/.review_ok ]; then
  ATTESO=$(head -n 1 .claude/.review_ok | tr -d '[:space:]')
  # Script accanto al repo dell'hook (non della cwd): vale anche nei test su repo temporanei.
  ATTUALE=$(bash "$(dirname "$0")/../../scripts/hash_diff_staged.sh" 2>/dev/null)
  if [ -n "$ATTESO" ] && [ -n "$ATTUALE" ] && [ "$ATTESO" = "$ATTUALE" ]; then
    exit 0
  fi
  echo "BLOCCATO (gate review): .claude/.review_ok non corrisponde al diff staged (marcatore residuo, vuoto o diff cambiato dopo la review). Fai revisionare il diff attuale e rigenera il marcatore con: bash scripts/segna_review_ok.sh" >&2
  exit 2
fi

echo "BLOCCATO (gate review): il diff staged tocca il perimetro di review (.claude/perimetro_review.txt) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore con: bash scripts/segna_review_ok.sh — poi ricommitta." >&2
exit 2
