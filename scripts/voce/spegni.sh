#!/bin/bash
# R8 voce H24 — spegne l'ascolto sempre attivo e il server voce di Gas sul Mac.
# Uso:  bash scripts/voce/spegni.sh
# Toglie i due servizi da launchd e i loro plist da ~/Library/LaunchAgents: non partono
# più nemmeno al prossimo accesso. Per riaccendere: bash scripts/voce/installa.sh
set -uo pipefail
[ "$(uname -s)" = "Darwin" ] || { echo "STOP: questo script è solo per il Mac." >&2; exit 1; }
DOMINIO="gui/$(id -u)"
for s in com.gas.ascolto com.gas.voce.server; do
  launchctl bootout "$DOMINIO/$s" 2>/dev/null && echo "$s: spento" || echo "$s: già spento"
  rm -f "$HOME/Library/LaunchAgents/$s.plist"
done
echo "Fatto: Gas non ascolta più. I log restano in .gas_voce/ (cancellali se vuoi)."
