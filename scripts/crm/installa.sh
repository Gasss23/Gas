#!/bin/bash
# CRM di Gas sempre acceso sul Mac (richiesta dell'operatore del 24-11).
# Uso (dalla cartella di Gas):  bash scripts/crm/installa.sh
# Spegnere:                     bash scripts/crm/spegni.sh
#
# Cosa fa, nell'ordine (si FERMA al primo errore):
#   1. controlla che sia un Mac, che ci sia .venv e che GAS_CRM_TOKEN sia nel .env
#      (letto come lo legge il CRM, senza stamparlo);
#   2. controlla che la porta del CRM sia libera (un CRM avviato a mano va chiuso prima);
#   3. scrive il plist in ~/Library/LaunchAgents con la cartella vera di Gas e lo carica;
#   4. aspetta che la dashboard risponda su 127.0.0.1;
#   5. mette sulla Scrivania l'icona «CRM Gas» che apre la dashboard nel browser.
# La dashboard non usa l'IA (solo il pulsante «Riscrivi con Opus») e funziona senza internet.
set -euo pipefail

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAS="$(cd "$QUI/../.." && pwd)"
AGENTI="$HOME/Library/LaunchAgents"
SERVIZIO=com.gas.crm
PLIST="$AGENTI/$SERVIZIO.plist"

stop() { echo "STOP: $*" >&2; exit 1; }

[ "$(uname -s)" = "Darwin" ] || stop "questo script è per il Mac"
[ -x "$GAS/.venv/bin/python" ] || stop "manca .venv in $GAS: prima installa Gas (pip install -r requirements.txt)"

# 1. token e porta letti con lo stesso codice del CRM (.env compreso)
PORTA="$(cd "$GAS" && .venv/bin/python - <<'PY'
import sys
from modules.crm import __main__ as cli, server
cli._carica_chiavi()
if server.token_da_env() is None:
    sys.exit(2)
print(cli._env_int("GAS_CRM_PORT", 8770, 1024, 65535))
PY
)" || stop "manca GAS_CRM_TOKEN (almeno 16 caratteri) nel file .env di Gas: senza token il CRM non parte"
case "$PORTA" in ''|*[!0-9]*) stop "porta del CRM non valida: $PORTA" ;; esac
URL="http://127.0.0.1:$PORTA/"

risponde() { curl -s -o /dev/null --max-time 2 "$URL"; }

# 2. via la copia vecchia; poi la porta deve essere libera
mkdir -p "$AGENTI"
launchctl bootout "gui/$(id -u)/$SERVIZIO" 2>/dev/null || true
sleep 1
if risponde; then
  stop "sulla porta $PORTA risponde già qualcosa (un CRM avviato a mano nel Terminale?): chiudilo con Ctrl+C e rilancia"
fi

# 3. plist con la cartella vera (| come separatore: il percorso contiene /)
ESC="$(printf '%s' "$GAS" | sed -e 's/[\\|&]/\\&/g')"
sed "s|CARTELLA_GAS|$ESC|g" "$QUI/$SERVIZIO.plist" > "$PLIST"
plutil -lint "$PLIST" >/dev/null || stop "plist non valido: $PLIST"
launchctl bootstrap "gui/$(id -u)" "$PLIST" || stop "launchctl non ha caricato $SERVIZIO"

# 4. aspetta la dashboard (al massimo 30 s)
for _ in $(seq 1 30); do
  risponde && break
  sleep 1
done
risponde || stop "la dashboard non risponde su $URL: guarda $GAS/.gas_memory_crm_server.log"

# 5. icona sulla Scrivania (solo l'indirizzo: il token NON finisce in nessun file)
ICONA="$HOME/Desktop/CRM Gas.webloc"
cat > "$ICONA" <<WEBLOC
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>URL</key>
  <string>$URL</string>
</dict>
</plist>
WEBLOC

echo "OK: il CRM è acceso e partirà da solo a ogni avvio del Mac."
echo "Aprilo col doppio clic su «CRM Gas» sulla Scrivania (oppure $URL)."
echo "Al primo accesso il browser chiede il token: è GAS_CRM_TOKEN nel file .env."
