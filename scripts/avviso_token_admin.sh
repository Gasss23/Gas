#!/usr/bin/env bash
# G-3 (agente non admin). Senza argomenti: "solo avviso", NON blocca mai (exit 0 sempre).
# Fase 2 (decisione operatore 2026-10-14, «sì blocco»): con `--blocco` esce 1 in tutti i
# casi tranne l'OK verificato (token che amministra, non verificabile, gh assente → 1).
# La usa `gasmerge --auto`: il merge automatico si ferma se il token non è quello giusto.
#
# L'agente deve lavorare con un token gh che NON può amministrare il repo (ruleset,
# workflow, environment, impostazioni). `permissions.admin` dell'API riflette il RUOLO
# dell'utente (il proprietario è sempre admin), non i permessi del token: per questo si
# prova la CAPACITÀ del token su un endpoint che richiede Administration (deploy key):
#   200      → il token amministra il repo  → AVVISO
#   403/404  → il token non amministra      → OK, solo se il token VEDE il repo (V-1 #138)
#   altro    → non verificabile             → AVVISO (anche un 403 da rate limit, R-186-2)
# R-186-3: prova SOLO Administration; Workflows/Environments "No access" del setup non sono
# verificati da qui. R-186-4: nessun timeout proprio su `gh api` (come i gh/git che seguono).
# Va eseguito dentro il repo (gh risolve {owner}/{repo} dal remote).
set -u
BLOCCO=0
OK=0   # bot #207 V-1: mai ereditata dall'ambiente (OK=1 esportato non deve aprire il blocco)
if [ "${1:-}" = "--blocco" ]; then BLOCCO=1; fi
esci() { if [ "$BLOCCO" = 1 ] && [ "$OK" != 1 ]; then exit 1; fi; exit 0; }
if ! command -v gh >/dev/null 2>&1; then
  echo "AVVISO G-3: gh assente — permessi del token non verificabili" >&2
  esci
fi
ERR=$(gh api "repos/{owner}/{repo}/keys" --silent 2>&1 >/dev/null)
RC=$?
if [ "$RC" -eq 0 ]; then
  echo "AVVISO G-3: il token gh in uso AMMINISTRA il repo (può cambiare ruleset, workflow," \
       "environment). L'agente dovrebbe usare il token senza Administration:" \
       "reports/setup_agente_non_admin.md" >&2
elif printf '%s' "$ERR" | grep -qiE 'rate limit'; then
  # R-186-2: un 403 da rate limit non dice nulla sui permessi del token.
  echo "AVVISO G-3: permessi del token non verificabili (rate limit di GitHub)" >&2
elif printf '%s' "$ERR" | grep -qE 'HTTP (403|404)'; then
  # V-1 verifica esterna #138 + R-188-1: 403/404 vale "non amministra" SOLO se è il repo
  # dell'operatore: il token lo vede E l'utente vi ha RUOLO admin (permissions.admin, che
  # misura il ruolo, non il token). Repo sbagliato (fork, GH_REPO, anche se pubblico) o
  # blocco SSO → "non verificabile", mai un falso OK.
  RUOLO=$(gh api "repos/{owner}/{repo}" --jq '.permissions.admin' 2>/dev/null) || RUOLO=""
  if [ "$RUOLO" = "true" ]; then
    echo "G-3: il token gh in uso non amministra il repo — OK" >&2
    OK=1
  else
    echo "AVVISO G-3: permessi del token non verificabili (repo non visibile o non dell'operatore)" >&2
  fi
else
  echo "AVVISO G-3: permessi del token non verificabili (gh rc=$RC)" >&2
fi
esci
