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
# V-2 bot #403 (come R-615-3 della voce): la cartella finisce in `zsh -c 'cd "…"'` e nell'XML
# del plist, quindi solo caratteri sicuri
CONSENTITI='^[A-Za-z0-9/._ -]+$'
[[ "$GAS" =~ $CONSENTITI ]] \
  || stop "la cartella di Gas ($GAS) ha caratteri non ammessi: usa solo lettere, cifre, / . _ - e spazi"
[ -x "$GAS/.venv/bin/python" ] || stop "manca .venv in $GAS: prima installa Gas (pip install -r requirements.txt)"

# 1. token e porta letti con lo stesso codice del CRM (.env compreso)
PORTA="$(cd "$GAS" && .venv/bin/python - <<'PY'
import sys
from modules.crm import __main__ as cli, server
cli._carica_chiavi()
import os
if server.token_da_env() is None:
    sys.exit(2)
# V-3 bot #403: il CRM sempre acceso resta SOLO su questo Mac
if (os.environ.get("GAS_CRM_BIND", "127.0.0.1").strip() or "127.0.0.1") != "127.0.0.1":
    sys.exit(3)
print(cli._env_int("GAS_CRM_PORT", 8770, 1024, 65535))
PY
)" || {
  case $? in
    3) stop "nel .env c'è GAS_CRM_BIND diverso da 127.0.0.1: il CRM sempre acceso deve restare solo su questo Mac (togli quella riga)" ;;
    *) stop "manca GAS_CRM_TOKEN (almeno 16 caratteri) nel file .env di Gas: senza token il CRM non parte" ;;
  esac
}
case "$PORTA" in ''|*[!0-9]*) stop "porta del CRM non valida: $PORTA" ;; esac
URL="http://127.0.0.1:$PORTA/"

risponde() { curl -s -o /dev/null --max-time 2 "$URL"; }

# 2. via la copia vecchia; poi la porta deve essere libera
mkdir -p "$AGENTI"
DOMINIO="gui/$(id -u)"
launchctl bootout "$DOMINIO/$SERVIZIO" 2>/dev/null || true
# V-1 bot #403 (prova dal vero di M1 sulla voce, 2026-11-02): bootout è asincrono; si aspetta
# che il servizio vecchio sparisca (al massimo 5 s) e che la sua porta si liberi
ANDATO=no
for _ in $(seq 1 50); do
  if ! launchctl print "$DOMINIO/$SERVIZIO" >/dev/null 2>&1; then ANDATO=si; break; fi
  sleep 0.1
done
[ "$ANDATO" = si ] || stop "il CRM vecchio non si spegne (launchctl bootout): aspetta qualche secondo e rilancia"
for _ in $(seq 1 10); do
  risponde || break
  sleep 0.5
done
if risponde; then
  stop "sulla porta $PORTA risponde già qualcosa (un CRM avviato a mano nel Terminale?): chiudilo con Ctrl+C e rilancia"
fi

# 3. plist con la cartella vera (| come separatore: il percorso contiene /)
ESC="$(printf '%s' "$GAS" | sed -e 's/[\\|&]/\\&/g')"
sed "s|CARTELLA_GAS|$ESC|g" "$QUI/$SERVIZIO.plist" > "$PLIST"
plutil -lint "$PLIST" >/dev/null || stop "plist non valido: $PLIST"
CARICATO=no
for tentativo in 1 2 3; do
  if launchctl bootstrap "$DOMINIO" "$PLIST"; then CARICATO=si; break; fi
  if [ "$tentativo" -lt 3 ]; then
    echo "   CRM non ancora caricato: riprovo tra 1 s (tentativo $((tentativo + 1)) di 3)."
    sleep 1
  fi
done
[ "$CARICATO" = si ] || stop "launchctl non carica $SERVIZIO (3 tentativi)"

# 4. aspetta la dashboard (al massimo 30 s); se non risponde, il servizio si toglie
#    (V-3 bot #403: niente riavvii ogni 10 s di un CRM che non parte)
for _ in $(seq 1 30); do
  risponde && break
  sleep 1
done
if ! risponde; then
  launchctl bootout "$DOMINIO/$SERVIZIO" 2>/dev/null || true
  stop "la dashboard non risponde su $URL: servizio tolto; guarda $GAS/.gas_memory_crm_server.log"
fi

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
# la copia cifrata su iCloud sotto launchd potrebbe non avere il permesso di macOS: si mostra
COPIA="$(grep -a "Copia cifrata giornaliera" "$GAS/.gas_memory_crm_server.log" 2>/dev/null | tail -1 || true)"
[ -n "$COPIA" ] && echo "$COPIA"
