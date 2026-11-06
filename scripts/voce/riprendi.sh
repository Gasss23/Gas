#!/bin/bash
# Fetta 43 (standby) — riaccende l'ascolto di Gas dopo pausa.sh.
# Uso:  bash scripts/voce/riprendi.sh
# Ricarica com.gas.ascolto dal plist che installa.sh ha messo in ~/Library/LaunchAgents.
# Il server voce non si tocca.
set -uo pipefail
[ "$(uname -s)" = "Darwin" ] || { echo "STOP: questo script è solo per il Mac." >&2; exit 1; }
S=com.gas.ascolto
DOMINIO="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/$S.plist"
if launchctl print "$DOMINIO/$S" >/dev/null 2>&1; then
  echo "Gas sta già ascoltando: non c'era niente da riprendere."
  exit 0
fi
if [ ! -f "$PLIST" ]; then
  echo "STOP: l'ascolto non è installato (manca $PLIST)." >&2
  echo "Installalo con: bash scripts/voce/installa.sh" >&2
  exit 1
fi
# Subito dopo pausa.sh il servizio vecchio può non essere ancora sparito: bootstrap dà
# «Bootstrap failed: 5». Tre tentativi a un secondo di distanza, come installa.sh.
for tentativo in 1 2 3; do
  if launchctl bootstrap "$DOMINIO" "$PLIST" 2>/dev/null; then
    echo "RIPRESO: Gas ascolta di nuovo. Di' «Hey Jarvis» per parlargli."
    exit 0
  fi
  [ "$tentativo" -lt 3 ] && sleep 1
done
echo "ATTENZIONE: l'ascolto non è ripartito. Aspetta qualche secondo e rilancia" >&2
echo "  bash scripts/voce/riprendi.sh   (se non basta: bash scripts/voce/installa.sh)" >&2
exit 1
