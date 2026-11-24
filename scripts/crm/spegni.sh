#!/bin/bash
# Spegne il CRM sempre acceso (installato con scripts/crm/installa.sh). I dati restano.
# Uso (dalla cartella di Gas):  bash scripts/crm/spegni.sh
set -uo pipefail
SERVIZIO=com.gas.crm
launchctl bootout "gui/$(id -u)/$SERVIZIO" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/$SERVIZIO.plist"
echo "OK: CRM spento e tolto dall'avvio. I dati dei clienti non sono stati toccati."
echo "Per riaccenderlo: bash scripts/crm/installa.sh"
