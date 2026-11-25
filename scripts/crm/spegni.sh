#!/bin/bash
# Spegne il CRM sempre acceso (installato con scripts/crm/installa.sh). I dati restano.
# Uso (dalla cartella di Gas):  bash scripts/crm/spegni.sh
set -uo pipefail
SERVIZIO=com.gas.crm
launchctl bootout "gui/$(id -u)/$SERVIZIO" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/$SERVIZIO.plist"
rm -f "$HOME/Desktop/CRM Gas.webloc"
# R-860-3: anche l'accesso dal telefono (decisione 21), se c'era: niente collegamento Tailscale
# lasciato verso una porta dove poi potrebbe ascoltare un altro programma
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if grep -qs "GAS_CRM_NOME_TAILSCALE" "$QUI/../../.env" || command -v tailscale >/dev/null 2>&1 \
   || [ -x /Applications/Tailscale.app/Contents/MacOS/Tailscale ]; then
  bash "$QUI/telefono.sh" spegni || echo "ATTENZIONE: accesso dal telefono non spento: bash scripts/crm/telefono.sh spegni" >&2
fi
echo "OK: CRM spento e tolto dall'avvio. I dati dei clienti non sono stati toccati."
echo "Per riaccenderlo: bash scripts/crm/installa.sh"
