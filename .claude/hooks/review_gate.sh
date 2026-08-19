#!/usr/bin/env bash
# PreToolUse hook (Bash) — gate di review DETERMINISTICO.
# Blocca (exit 2) un `git commit` il cui diff STAGED tocca il motore
# (gas.py, brains/, modules/, tests/) se manca il marcatore .claude/.review_ok.
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
    jq -r '(.[0] // .) | .tool_input.command // empty'
  elif python3 -c "import sys" >/dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  elif python -c "import sys" >/dev/null 2>&1; then
    python -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  else
    perl -MJSON::PP -e 'my $d=JSON::PP->new->decode(do{local$/;<STDIN>}); my $o=ref($d)eq"ARRAY"?$d->[0]:$d; print $o->{tool_input}{command}//"" if $o->{tool_input}'
  fi
}

CMD=$(printf '%s' "$INPUT" | _parse_cmd 2>/dev/null)
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
if ! printf '%s\n' "$DIFF_OUT" | grep -qE '^(gas\.py|brains/|modules/|tests/)'; then
  exit 0   # nessun diff motore verificato: commit doc/report consentito
fi

# Marcatore di review presente -> consentito (va creato DOPO verdetto del revisore)
[ -f .claude/.review_ok ] && exit 0

echo "BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore (touch .claude/.review_ok) e ricommitta, poi rimuovilo." >&2
exit 2
