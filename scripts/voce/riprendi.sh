#!/bin/bash
# Fetta 43 (standby) — riaccende l'ascolto di Gas dopo pausa.sh.
# Uso:  bash scripts/voce/riprendi.sh
# Ricarica com.gas.ascolto dal plist che installa.sh ha messo in ~/Library/LaunchAgents e
# controlla che l'ascolto giri davvero (bot V-2 su #338). Il server voce non si tocca.
set -uo pipefail
[ "$(uname -s)" = "Darwin" ] || { echo "STOP: questo script è solo per il Mac." >&2; exit 1; }
S=com.gas.ascolto
DOMINIO="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/$S.plist"
LOG="$(cd "$(dirname "$0")/../.." && pwd)/.gas_voce/ascolto.log"
# R-677-1: l'output si salva prima e si guarda con case (come installa.sh, R-615-7): con
# pipefail, `print | grep -q` può dare un falso «non gira» per il SIGPIPE.
gira() {
  local stato
  stato="$(launchctl print "$DOMINIO/$S" 2>/dev/null || true)"
  case "$stato" in *"state = running"*) return 0 ;; *) return 1 ;; esac
}
cade() {
  echo "ATTENZIONE: l'ascolto è caricato ma non resta acceso (si ferma subito)." >&2
  echo "Guarda gli ultimi errori:  tail -20 \"$LOG\"" >&2
  echo "Spesso basta reinstallare: bash scripts/voce/installa.sh" >&2
  exit 1
}
if gira; then
  echo "Gas sta già ascoltando: non c'era niente da riprendere."
  exit 0
fi
if [ ! -f "$PLIST" ]; then
  echo "STOP: l'ascolto non è installato (manca $PLIST)." >&2
  echo "Installalo con: bash scripts/voce/installa.sh" >&2
  exit 1
fi
# R-673-3: subito dopo pausa.sh il servizio può essere ancora caricato mentre esce. Si
# aspetta che sparisca (al massimo 5 s), poi si ricarica.
ANDATO=no
for _ in $(seq 1 50); do
  if ! launchctl print "$DOMINIO/$S" >/dev/null 2>&1; then ANDATO=si; break; fi
  sleep 0.1
done
# R-677-2: ancora caricato dopo 5 s e non acceso = cade di continuo (launchd lo rilancia):
# ricaricarlo non serve, serve il log.
[ "$ANDATO" = si ] || cade
# «Bootstrap failed: 5» se il vecchio non è ancora sparito: tre tentativi a un secondo di
# distanza, come installa.sh. All'ultimo l'errore di launchctl resta visibile (R-673-2).
CARICATO=no
for tentativo in 1 2 3; do
  if [ "$tentativo" -lt 3 ]; then
    launchctl bootstrap "$DOMINIO" "$PLIST" 2>/dev/null && { CARICATO=si; break; }
    sleep 1
  else
    launchctl bootstrap "$DOMINIO" "$PLIST" && CARICATO=si
  fi
done
if [ "$CARICATO" != si ]; then
  echo "ATTENZIONE: l'ascolto non è ripartito. Aspetta qualche secondo e rilancia" >&2
  echo "  bash scripts/voce/riprendi.sh   (se non basta: bash scripts/voce/installa.sh)" >&2
  exit 1
fi
# Caricato non vuol dire acceso: con un venv rotto il processo cade e launchd lo rilancia
# di continuo. Si guarda che giri ancora dopo qualche secondo (bot V-2 su #338).
sleep 3
if gira; then
  echo "RIPRESO: Gas ascolta di nuovo. Di' «Hey Jarvis» per parlargli."
  exit 0
fi
cade
