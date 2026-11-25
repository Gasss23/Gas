#!/bin/bash
# Dashboard del CRM anche dal telefono, SOLO nella rete privata Tailscale (decisione 21).
# Uso (dalla cartella di Gas):
#   bash scripts/crm/telefono.sh          accende l'accesso dal telefono
#   bash scripts/crm/telefono.sh spegni   lo spegne (la dashboard resta sul Mac)
#   bash scripts/crm/telefono.sh stato    dice se è acceso
#
# Come funziona: il CRM resta su 127.0.0.1 e non si apre a internet. `tailscale serve`
# lo raggiunge dal nome privato del Mac (es. https://mac.tail1234.ts.net/), con HTTPS, e
# lo fa vedere SOLO ai dispositivi entrati nel tuo account Tailscale. Il token del CRM
# serve comunque. Mai `tailscale funnel` (quello pubblica su internet): lo script lo
# controlla, e il CRM rifiuta comunque ogni richiesta arrivata dal funnel (R-860-1).
set -euo pipefail

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAS="$(cd "$QUI/../.." && pwd)"
SERVIZIO=com.gas.crm
DOMINIO="gui/$(id -u)"
ENV_FILE="$GAS/.env"
PY="$GAS/.venv/bin/python"

stop() { echo "STOP: $*" >&2; exit 1; }

AZIONE="${1:-accendi}"
case "$AZIONE" in accendi|spegni|stato) ;; *) stop "uso: bash scripts/crm/telefono.sh [spegni|stato]" ;; esac

[ "$(uname -s)" = "Darwin" ] || stop "questo script è per il Mac"
[ -x "$PY" ] || stop "manca .venv in $GAS: prima installa Gas"

# il comando di Tailscale: nel PATH o dentro l'app
TS=""
if command -v tailscale >/dev/null 2>&1; then
  TS="$(command -v tailscale)"
elif [ -x /Applications/Tailscale.app/Contents/MacOS/Tailscale ]; then
  TS=/Applications/Tailscale.app/Contents/MacOS/Tailscale
fi

# GAS_CRM_NOME_TAILSCALE nel .env: messa, cambiata o tolta senza toccare il resto del file.
# Toglie anche le forme «export CHIAVE=» e «CHIAVE = v»; un .env collegato resta collegato.
scrivi_env() {
  "$PY" -I - "$ENV_FILE" "$1" <<'PY'
import os, sys, tempfile
percorso, nome = os.path.realpath(sys.argv[1]), sys.argv[2]
chiave = "GAS_CRM_NOME_TAILSCALE"
try:
    with open(percorso, encoding="utf-8") as f:
        righe = f.read().splitlines()
    modo = os.stat(percorso).st_mode & 0o777
except FileNotFoundError:
    if not nome:
        sys.exit(0)  # niente .env e niente da scrivere: non se ne crea uno vuoto
    righe, modo = [], 0o600

def nostra(riga):
    r = riga.strip()
    if r.startswith("export "):
        r = r[len("export "):].lstrip()
    return r.split("=", 1)[0].strip() == chiave and "=" in r

nuove = [r for r in righe if not nostra(r)]
if nome:
    nuove.append(f"{chiave}={nome}")
cartella = os.path.dirname(percorso)
fd, tmp = tempfile.mkstemp(dir=cartella, prefix=".env.", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("\n".join(nuove) + ("\n" if nuove else ""))
        f.flush()
        os.fsync(f.fileno())
    os.chmod(tmp, modo)
    os.replace(tmp, percorso)
except BaseException:
    os.unlink(tmp)
    raise
PY
}

# nome privato del Mac (dallo stato di Tailscale, senza il punto finale). Esce: 0 ok,
# 3 Tailscale spento o senza accesso, 5 nome non *.ts.net, altro: stato illeggibile
leggi_nome() {
  local j
  j="$("$TS" status --json 2>/dev/null)" || return 2
  NOME="$(printf '%s' "$j" | "$PY" -I -c '
import json, sys
try:
    s = json.load(sys.stdin)
except ValueError:
    sys.exit(2)
if not isinstance(s, dict) or s.get("BackendState") != "Running":
    sys.exit(3)
print(((s.get("Self") or {}).get("DNSName") or "").rstrip(".").lower())
')" || return $?
  [[ "$NOME" =~ ^([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+ts\.net$ ]] || return 5
}

# porta del CRM, letta come la legge il CRM (solo dal .env, come la vede launchd)
leggi_porta() {
  PORTA="$(cd "$GAS" && env -i HOME="$HOME" PATH=/usr/bin:/bin "$PY" - <<'PY'
import sys
try:
    import gas  # noqa: F401
except Exception:
    sys.exit(4)
from modules.crm import __main__ as cli
cli._carica_chiavi()
print(cli._env_int("GAS_CRM_PORT", 8770, 1024, 65535))
PY
)" || return 1
  case "$PORTA" in ''|*[!0-9]*) return 1 ;; esac
}

# chi usa la porta 443 del nome del Mac («nostro», «altro», «libero», «errore»), più
# «pubblico» se un funnel (internet) è acceso sul nome del Mac su QUALSIASI porta, anche
# lanciato in primo piano (R-860-1, R-860-5)
stato_serve() {
  local j
  j="$("$TS" serve status --json 2>/dev/null)" || { echo errore; return 0; }
  printf '%s' "$j" | "$PY" -I -c '
import json, sys
nome, dest = sys.argv[1], sys.argv[2]
try:
    c = json.load(sys.stdin)
except ValueError:
    print("errore"); sys.exit(0)
if c is None:
    c = {}
if not isinstance(c, dict):
    print("errore"); sys.exit(0)
configurazioni = [c] + [v for v in (c.get("Foreground") or {}).values() if isinstance(v, dict)]
pubblico = any(v and str(k).startswith(nome + ":")
               for conf in configurazioni for k, v in (conf.get("AllowFunnel") or {}).items())
gestori = ((c.get("Web") or {}).get(nome + ":443") or {}).get("Handlers") or {}
proxy = [str((h or {}).get("Proxy") or "") for h in gestori.values()]
nostro = bool(dest) and set(gestori) == {"/"} and proxy[0].rstrip("/") == dest
print(("nostro" if nostro else ("altro" if gestori else "libero")) + (" pubblico" if pubblico else ""))
' "$NOME" "${DESTINAZIONE:-}"
}

risponde_locale() { curl -s -o /dev/null --max-time 2 "$DESTINAZIONE/"; }

riavvia_crm() {
  launchctl kickstart -k "$DOMINIO/$SERVIZIO" >/dev/null
  for _ in $(seq 1 30); do
    risponde_locale && return 0
    sleep 1
  done
  return 1
}

crm_installato() { launchctl print "$DOMINIO/$SERVIZIO" >/dev/null 2>&1; }

NOME=""
PORTA=""
DESTINAZIONE=""

# --- spegni: prima di tutto il CRM smette di accettare il nome Tailscale (R-860-2), poi,
#     se Tailscale risponde, si toglie il collegamento
if [ "$AZIONE" = spegni ]; then
  scrivi_env "" || stop "non riesco a togliere GAS_CRM_NOME_TAILSCALE dal file .env: toglila a mano"
  if leggi_porta; then
    DESTINAZIONE="http://127.0.0.1:$PORTA"
    if crm_installato; then
      riavvia_crm || echo "ATTENZIONE: il CRM non risponde dopo il riavvio: rilancia bash scripts/crm/installa.sh" >&2
    fi
  else
    echo "ATTENZIONE: non riesco a leggere la porta del CRM: se il CRM è acceso, riavvialo (bash scripts/crm/installa.sh)" >&2
  fi
  if [ -z "$TS" ]; then
    echo "OK: accesso dal telefono spento (Tailscale non è installato)."
    exit 0
  fi
  if ! leggi_nome; then
    echo "ATTENZIONE: Tailscale è spento o senza accesso: il CRM rifiuta già il telefono, ma il collegamento" >&2
    echo "resta salvato in Tailscale. Quando riaccendi Tailscale, rilancia: bash scripts/crm/telefono.sh spegni" >&2
    exit 0
  fi
  STATO="$(stato_serve)"
  case "$STATO" in
    nostro*)
      "$TS" serve --yes --https=443 off >/dev/null \
        || echo "ATTENZIONE: non riesco a togliere il collegamento: $TS serve --https=443 off" >&2 ;;
    errore) echo "ATTENZIONE: non riesco a leggere la configurazione di Tailscale: controlla con $TS serve status" >&2 ;;
  esac
  case "$STATO" in *pubblico*) echo "ATTENZIONE: sul nome del Mac c'è un funnel PUBBLICO (internet): spegnilo con '$TS funnel reset'" >&2 ;; esac
  echo "OK: accesso dal telefono spento. La dashboard si apre solo dal Mac (icona «CRM Gas»)."
  exit 0
fi

# --- stato e accendi: servono Tailscale acceso e la porta
[ -n "$TS" ] || stop "Tailscale non c'è: installalo dal Mac App Store (app «Tailscale»), accedi, e rilancia"
leggi_nome || case $? in
  3) stop "Tailscale è spento o non hai fatto l'accesso: apri l'app Tailscale, accedi e rilancia" ;;
  5) stop "il nome Tailscale del Mac ($NOME) non è un nome *.ts.net: attiva MagicDNS nel pannello di Tailscale" ;;
  *) stop "non riesco a leggere lo stato di Tailscale ($TS status)" ;;
esac
leggi_porta || stop "non riesco a leggere la porta del CRM (Gas non si avvia con le sue dipendenze?)"
DESTINAZIONE="http://127.0.0.1:$PORTA"
URL="https://$NOME/"

if [ "$AZIONE" = stato ]; then
  STATO="$(stato_serve)"
  case "$STATO" in
    *pubblico*) echo "ATTENZIONE: sul nome del Mac c'è un funnel PUBBLICO (internet). Spegnilo: $TS funnel reset" ;;
    nostro) echo "Acceso: dal telefono apri $URL (con l'app Tailscale accesa)." ;;
    altro) echo "Spento per il CRM: la porta 443 del Mac la usa un altro servizio di Tailscale." ;;
    errore) echo "Non riesco a leggere la configurazione di Tailscale: è acceso?" ;;
    *) echo "Spento: la dashboard si apre solo dal Mac." ;;
  esac
  exit 0
fi

# --- accendi
crm_installato || stop "il CRM non è installato tra i servizi del Mac: prima lancia bash scripts/crm/installa.sh"
STATO="$(stato_serve)"
case "$STATO" in
  *pubblico*) stop "sul nome del Mac c'è un funnel PUBBLICO (internet): spegnilo con '$TS funnel reset' e rilancia" ;;
  altro) stop "la porta 443 del nome Tailscale del Mac la usa già un altro servizio ($TS serve status): liberala e rilancia" ;;
  errore) stop "non riesco a leggere la configurazione di Tailscale ($TS serve status): è acceso?" ;;
esac

togli_tutto() {
  scrivi_env "" || echo "ATTENZIONE: togli a mano la riga GAS_CRM_NOME_TAILSCALE dal file .env" >&2
  riavvia_crm || true
}

# 1. il CRM accetta il nome privato del Mac (e solo quello, solo sulla 443)
scrivi_env "$NOME" || stop "non riesco a scrivere nel file .env"
riavvia_crm || { togli_tutto; stop "il CRM non riparte col nome Tailscale: tolto; guarda $GAS/.gas_memory_crm_server.log"; }

# 2. tailscale serve: HTTPS nella rete privata verso il CRM locale
if [ "$STATO" != nostro ]; then
  echo "   Collego il CRM alla rete privata Tailscale…"
  if ! "$TS" serve --bg --yes --https=443 "$DESTINAZIONE"; then
    togli_tutto
    stop "tailscale serve non riuscito: guarda il messaggio sopra e rilancia"
  fi
fi
DOPO="$(stato_serve)"
if [ "$DOPO" != nostro ]; then
  case "$DOPO" in nostro*) "$TS" serve --yes --https=443 off >/dev/null 2>&1 || true ;; esac
  togli_tutto
  # R-860-4: la prima volta Tailscale stampa un link per attivare HTTPS ed esce senza collegare
  stop "il collegamento non è attivo ($DOPO). Se sopra Tailscale ha stampato un link per attivare HTTPS, aprilo, premi «Enable» e rilancia questo comando"
fi

# 3. prova dal Mac stesso attraverso Tailscale (il primo certificato può metterci qualche secondo)
PROVA=no
for _ in $(seq 1 20); do
  RISPOSTA="$(curl -s --max-time 5 "${URL}api/sessione" 2>/dev/null || true)"
  if [[ "$RISPOSTA" == *'"autenticato"'* ]]; then PROVA=si; break; fi
  sleep 2
done

echo "OK: la dashboard del CRM si apre anche dal telefono, solo dentro la tua rete privata Tailscale."
echo "Indirizzo: $URL"
[ "$PROVA" = si ] || echo "ATTENZIONE: dal Mac non ho ancora una risposta su $URL; riprova tra un minuto dal telefono."
echo "Sul telefono: installa l'app Tailscale, accedi con lo STESSO account del Mac, apri l'indirizzo"
echo "in Safari, inserisci il token (GAS_CRM_TOKEN del .env) e salvala con Condividi → «Aggiungi alla schermata Home»."
echo "Per spegnerlo: bash scripts/crm/telefono.sh spegni"
exit 0
