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

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
[ -n "$CMD" ] || exit 0

# Non e' un git commit -> non interferire
printf '%s' "$CMD" | grep -Eq 'git[[:space:]].*commit' || exit 0

cd /workspaces/Gas 2>/dev/null || exit 0

# Il diff staged tocca il motore?
if ! git diff --cached --name-only 2>/dev/null | grep -Eq '^(gas\.py|brains/|modules/|tests/)'; then
  exit 0   # commit di soli reports/doc/config: consentito
fi

# Marcatore di review presente -> consentito (va creato DOPO verdetto del revisore)
[ -f .claude/.review_ok ] && exit 0

echo "BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore (touch .claude/.review_ok) e ricommitta, poi rimuovilo." >&2
exit 2
