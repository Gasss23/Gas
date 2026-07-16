#!/usr/bin/env bash
# SessionEnd hook — RETE DI SICUREZZA puramente ADDITIVA e CONDIZIONALE.
# Indurimento commit 2026-06-13 + chiusura bug sovrascrittura 2026-06-15.
#
# Contratto:
#  - Lavoro ricorrente LEGITTIMO: persistere .gas_history.json (memoria di Gas).
#  - Stage SOLO dell'allowlist esplicita: reports/, *.md, .gas_history.json.
#    MAI `git add -A` / `git add .`. MAI il motore (gas.py/brains/modules/tests).
#  - Se dopo lo stage NULLA e' in staging -> ESCE senza commit (niente commit
#    vuoti = niente rumore nel log).
#  - SOLO additivo: nessun git distruttivo sul working tree (no reset --hard,
#    no checkout --, no stash drop, no clean). L'unica rimozione ammessa e'
#    `git restore --staged` (toglie dallo staging, NON tocca il contenuto).
#  - Steady-state: l'agente committa ESPLICITAMENTE i propri report a fine task,
#    quindi qui reports/ non ha nulla da committare (no-op su reports/). La
#    sovrascrittura silenziosa del report canonico non e' piu' possibile perche'
#    l'agente, non l'hook, decide cosa committare in reports/.
#
# GAS_REPO_DIR sovrascrivibile SOLO per i test usa-e-getta; default = prod.

set -uo pipefail

REPO="${GAS_REPO_DIR:-${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}}"
cd "$REPO" 2>/dev/null || exit 0

# 0) GUARD MAIN-LOCK / DETACHED HEAD — BLOCCANTE.
# Su main o HEAD detached NON committare mai: main è protetto da ruleset
# GitHub e un commit su HEAD detached sarebbe irraggiungibile.
# Il warning va su stderr in modo RUMOROSO: uno skip silenzioso è la
# memoria che mente per omissione.
_cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)"
if [ $? -ne 0 ]; then
  echo "session_end: HEAD detached, commit saltato — main-lock. Committare a mano su un branch." >&2
  exit 0
fi
if [ "$_cur_branch" = "main" ]; then
  echo "session_end: HEAD su main, commit saltato — main-lock. Committare a mano su un branch." >&2
  exit 0
fi

# 1) Stage del solo allowlist esplicita.
git add reports/ '*.md' .gas_history.json 2>/dev/null || true

# 2) INVARIANTE DI SICUREZZA: se un file del motore fosse finito in staging
#    (per qualunque via), NON committarlo. Lo si toglie dallo staging in modo
#    additivo (restore --staged non tocca il working tree) e si prosegue.
ENGINE_RE='^(gas\.py|brains/|modules/|tests/)'
mapfile -t staged_engine < <(git diff --cached --name-only 2>/dev/null | grep -E "$ENGINE_RE")
if [ "${#staged_engine[@]}" -gt 0 ]; then
  git restore --staged "${staged_engine[@]}" 2>/dev/null || true
fi

# 3) Niente in staging -> ESCI senza commit (condizionale: niente commit vuoti).
if git diff --cached --quiet 2>/dev/null; then
  exit 0
fi

# 4) Commit + push, tutto fail-safe (mai bloccare la chiusura della sessione).
if ! git commit -q -m "auto-commit fine sessione $(date -u +%Y-%m-%d_%H:%M) [solo reports/doc/history, motore escluso]"; then
  echo "session_end: git commit fallito su branch '$_cur_branch'." >&2
  exit 0
fi
git push -q origin HEAD:"refs/heads/$_cur_branch"
_push_rc=$?
if [ "$_push_rc" -ne 0 ]; then
  echo "session_end: git push fallito su branch '$_cur_branch' (exit code $_push_rc)." >&2
fi
exit 0
