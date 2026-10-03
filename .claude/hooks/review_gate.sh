#!/usr/bin/env bash
# PreToolUse hook (Bash) — gate di review DETERMINISTICO.
# Blocca (exit 2) un `git commit` il cui diff STAGED tocca il motore
# (gas.py, brains/, modules/, tests/) se manca il marcatore .claude/.review_ok
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

# Il diff staged tocca il motore? — verifica FAIL-CLOSED.
# L'exit code di git viene catturato in GIT_RC FUORI dalla pipeline:
# in una pipeline bash l'exit code finale e' quello dell'ultimo comando
# (grep), non di git — quindi un git failure silenzioso risulterebbe
# in exit 0 della pipeline (fail-open). Qui lo catturiamo esplicitamente.
DIFF_OUT=$(git diff --cached --name-only 2>/dev/null)
GIT_RC=$?
if [ "$GIT_RC" -ne 0 ]; then
  echo "BLOCCATO (gate review): 'git diff --cached' fallito (exit $GIT_RC) — impossibile verificare il diff motore, fail-closed." >&2
  exit 2
fi

# R-136-1: modifiche al motore fuori dall'index (non staged o non tracciate)
# possono entrare nel commit DOPO questo controllo (`commit -a`, pathspec,
# `add && commit`). Fail-closed: il commit si fa solo con il motore tutto in
# stage (e revisionato) oppure tutto pulito.
WT_OUT=$(git status --porcelain --untracked-files=all -- gas.py brains modules tests 2>/dev/null)
WT_RC=$?
if [ "$WT_RC" -ne 0 ]; then
  echo "BLOCCATO (gate review): 'git status' fallito (exit $WT_RC) — fail-closed." >&2
  exit 2
fi
if printf '%s\n' "$WT_OUT" | grep -qE '^(.[^ ]|\?\?) '; then
  echo "BLOCCATO (gate review): ci sono modifiche al motore NON in stage (o file non tracciati) in gas.py/brains/modules/tests. Mettile in stage e falle revisionare, oppure mettile da parte (git stash), poi riprova." >&2
  exit 2
fi
if ! printf '%s\n' "$DIFF_OUT" | grep -qE '^(gas\.py|brains/|modules/|tests/)'; then
  exit 0   # nessun diff motore verificato: commit doc/report consentito
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

echo "BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore con: bash scripts/segna_review_ok.sh — poi ricommitta." >&2
exit 2
