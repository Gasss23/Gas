#!/usr/bin/env bash
# SessionEnd hook — RETE DI SICUREZZA SOLO PER IL PUSH (dal 2026-08-19).
#
# Contratto:
#  - NON committa mai. Il commit di fine sessione è responsabilità ESCLUSIVA
#    del flusso esplicito di fine-task (CLAUDE.md sez.3 + /fine-task).
#    /fine-task include nel suo git add: reports/ + .claude/agents/memoria_revisore.md
#    + .gas_history.json (set completo — nessun residuo per l'hook).
#  - Copre il solo caso edge: agente ha committato (via /fine-task) ma la
#    sessione è terminata prima del push. In quel caso pusha il branch corrente.
#  - Se HEAD == origin/<branch> (già sincronizzato), non fa nulla.
#  - Se il branch non esiste ancora su origin (ramo nuovo), pusha comunque.
#
# GAS_REPO_DIR sovrascrivibile SOLO per i test usa-e-getta; default = prod.

set -uo pipefail

REPO="${GAS_REPO_DIR:-${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}}"
cd "$REPO" 2>/dev/null || exit 0

# 0) GUARD MAIN-LOCK / DETACHED HEAD — BLOCCANTE.
# Su main o HEAD detached non pushare mai.
if ! _cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)"; then
  echo "session_end: HEAD detached, push skip — main-lock. Committare a mano su un branch." >&2
  exit 0
fi
if [ "$_cur_branch" = "main" ]; then
  echo "session_end: HEAD su main, push skip — main-lock. Committare a mano su un branch." >&2
  exit 0
fi

# 1) Push fail-safe: esegui solo se HEAD è avanti di origin (o branch non ancora su origin).
#    NON committa — il commit è responsabilità esclusiva del flusso /fine-task.
_remote_sha=$(git rev-parse "refs/remotes/origin/$_cur_branch" 2>/dev/null || true)
_local_sha=$(git rev-parse HEAD 2>/dev/null || true)
if [ -n "$_local_sha" ] && { [ -z "$_remote_sha" ] || [ "$_local_sha" != "$_remote_sha" ]; }; then
  git push -q origin HEAD:"refs/heads/$_cur_branch"
  _push_rc=$?
  if [ "$_push_rc" -ne 0 ]; then
    echo "session_end: push fail-safe fallito su branch '$_cur_branch' (exit code $_push_rc)." >&2
  fi
fi
exit 0
