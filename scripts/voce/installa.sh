#!/bin/bash
# R8 voce H24 — installa in un colpo solo l'ascolto sempre attivo di Gas sul Mac.
# Uso (dalla cartella di Gas):  bash scripts/voce/installa.sh
# Spegnere tutto:               bash scripts/voce/spegni.sh   (vedi scripts/voce/LEGGIMI.md)
#
# Cosa fa, nell'ordine (si FERMA al primo errore, senza toccare niente dopo):
#   1. controlla che sia un Mac e che GAS_VOICE_TOKEN sia nel .env (senza stamparlo);
#      se manca GAS_CLAUDE_BIN e `claude` c'è, lo AGGIUNGE in coda al .env;
#   2. usa .venv (lo crea se manca) e installa requirements.txt + requirements-ascolto.txt;
#   3. scarica il modello pronto della parola di attivazione (hey_jarvis) di openWakeWord;
#   4. scrive i due plist in ~/Library/LaunchAgents con la cartella vera di Gas;
#   5. li carica con launchctl (prima toglie le copie vecchie);
#   6. controllo finale: i due servizi girano e il server voce risponde su 127.0.0.1.
set -euo pipefail

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAS="$(cd "$QUI/../.." && pwd)"
AGENTI="$HOME/Library/LaunchAgents"
SERVIZI=(com.gas.voce.server com.gas.ascolto)

stop() { echo "STOP: $*" >&2; exit 1; }

# 1. controlli
[ "$(uname -s)" = "Darwin" ] || stop "questo script è solo per il Mac."
# R-615-3: lista BIANCA. La cartella finisce nel sed e nella shell del plist (cd "..."):
# fuori da lettere, cifre, / . _ - e spazio ci sarebbero $( ), backtick, \, & e simili.
CONSENTITI='^[A-Za-z0-9/._ -]+$'
[[ "$GAS" =~ $CONSENTITI ]] \
  || stop "la cartella di Gas ($GAS) ha caratteri non ammessi: usa solo lettere, cifre, / . _ - e spazi."
[ -f "$GAS/gas.py" ] || stop "non trovo gas.py in $GAS."
[ -f "$GAS/.env" ] || stop "manca $GAS/.env."
# V-4 bot #323 su 3672964: un token vuoto o col solo commento non vale.
grep -Eq '^[[:space:]]*(export[[:space:]]+)?GAS_VOICE_TOKEN=["'"'"']?[^[:space:]#"'"'"']' "$GAS/.env" \
  || stop "GAS_VOICE_TOKEN non è nel .env: aggiungilo (il server voce non parte senza)."
# V-1 bot #323: sotto launchd il PATH è minimo e il server voce non troverebbe `claude`
# (cervello forte dalla voce: mai i gratuiti, ma il forte non partirebbe). Se nel .env
# manca GAS_CLAUDE_BIN e `claude` c'è, si aggiunge col suo percorso assoluto.
# R-624-3: «valido» = primo carattere non spazio, # o virgoletta, come per il token; una
# riga vuota non si raddoppia (gas._carica_dotenv terrebbe la prima, vuota): si avvisa.
if grep -Eq '^[[:space:]]*(export[[:space:]]+)?GAS_CLAUDE_BIN=["'"'"']?[^[:space:]#"'"'"']' "$GAS/.env"; then
  :
elif grep -Eq '^[[:space:]]*(export[[:space:]]+)?GAS_CLAUDE_BIN=' "$GAS/.env"; then
  echo "AVVISO: nel .env GAS_CLAUDE_BIN è vuoto: dalla voce il cervello forte non partirà (mai i gratuiti). Scrivi il percorso di \`claude\` (\`which claude\`)."
else
  CLAUDE_BIN="$(command -v claude 2>/dev/null || true)"
  if [[ "$CLAUDE_BIN" == /* && "$CLAUDE_BIN" =~ $CONSENTITI ]]; then
    printf '\n# Aggiunto da scripts/voce/installa.sh: sotto launchd il PATH non trova claude.\nGAS_CLAUDE_BIN=%s\n' \
      "$CLAUDE_BIN" >> "$GAS/.env"
    echo "     GAS_CLAUDE_BIN=$CLAUDE_BIN aggiunto al .env (cervello forte dalla voce)."
  elif [ -n "$CLAUDE_BIN" ]; then
    echo "AVVISO: \`claude\` è in un percorso con caratteri non ammessi ($CLAUDE_BIN): scrivi tu GAS_CLAUDE_BIN nel .env, se no dalla voce il cervello forte non partirà."
  else
    echo "AVVISO: \`claude\` non trovato: dalla voce il cervello forte non partirà (mai i gratuiti). Scrivi GAS_CLAUDE_BIN=<percorso> nel .env."
  fi
fi
echo "1/6 controlli: OK"

# 2. venv e dipendenze
cd "$GAS"
if [ ! -f .venv/bin/activate ]; then
  python3 -m venv .venv || stop "non riesco a creare .venv."
fi
# shellcheck disable=SC1091
source .venv/bin/activate
# V-3 ve #323: requirements.txt fissa versioni che vogliono Python 3.11 o più.
python -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
  || stop "serve Python 3.11 o più nel .venv ($(python --version 2>&1)): installane uno nuovo, cancella .venv e riprova."
python -m pip install -q -r requirements.txt -r clients/voice/requirements-ascolto.txt \
  || stop "installazione delle dipendenze fallita."
echo "2/6 dipendenze: OK"

# 3. modello della parola di attivazione (in locale, nella cartella di openWakeWord)
python - <<'PY' || stop "download del modello di openWakeWord fallito."
import openwakeword.utils
openwakeword.utils.download_models(["hey_jarvis_v0.1"])
PY
echo "3/6 modello hey_jarvis: OK"

# 4. plist con la cartella vera
mkdir -p "$AGENTI" "$GAS/.gas_voce"
chmod 700 "$GAS/.gas_voce"
for s in "${SERVIZI[@]}"; do
  sed "s#CARTELLA_GAS#$GAS#g" "$QUI/$s.plist" > "$AGENTI/$s.plist"
  plutil -lint "$AGENTI/$s.plist" >/dev/null || stop "plist $s non valido."
done
echo "4/6 plist in $AGENTI: OK"

# 5. carica (togliendo prima le copie vecchie, se ci sono)
DOMINIO="gui/$(id -u)"
for s in "${SERVIZI[@]}"; do
  launchctl bootout "$DOMINIO/$s" 2>/dev/null || true
done
# Prova dal vero di M1 (2026-11-02): bootout è asincrono. Alla seconda esecuzione il
# servizio vecchio c'è ancora e bootstrap dà «Bootstrap failed: 5: Input/output error».
# Si aspetta che sparisca (launchctl print fallisce), al massimo 5 s per servizio…
for s in "${SERVIZI[@]}"; do
  ANDATO=no
  for _ in $(seq 1 50); do
    if ! launchctl print "$DOMINIO/$s" >/dev/null 2>&1; then ANDATO=si; break; fi
    sleep 0.1
  done
  [ "$ANDATO" = si ] \
    || stop "$s non si spegne (launchctl bootout): aspetta qualche secondo e rilancia lo script."
done
# …poi bootstrap, con due tentativi in più a distanza di un secondo.
for s in "${SERVIZI[@]}"; do
  CARICATO=no
  for tentativo in 1 2 3; do
    if launchctl bootstrap "$DOMINIO" "$AGENTI/$s.plist"; then CARICATO=si; break; fi
    if [ "$tentativo" -lt 3 ]; then
      echo "   $s non ancora caricato: riprovo tra 1 s (tentativo $((tentativo + 1)) di 3)."
      sleep 1
    fi
  done
  [ "$CARICATO" = si ] || stop "launchctl non carica $s (3 tentativi)."
done
echo "5/6 servizi caricati: OK"

# 6. controllo finale
sleep 5
for s in "${SERVIZI[@]}"; do
  # R-615-7: output salvato prima (con pipefail un SIGPIPE di grep -q darebbe un falso «non gira»)
  STATO="$(launchctl print "$DOMINIO/$s" 2>/dev/null || true)"
  case "$STATO" in
    *"state = running"*) ;;
    *) stop "$s non gira: guarda $GAS/.gas_voce/${s#com.gas.}.log" ;;
  esac
done
# R-615-1: senza GAS_VOICE_PORT nel .env grep esce con 1: `|| true`, se no set -e ferma
# lo script in silenzio (porta di default 8765). V-2 bot #323: vale la PRIMA riga, come
# per il server e per l'ascolto (gas._carica_dotenv).
# R-622-1: un commento in linea («9001 # era 8765») si toglie prima di tenere le cifre.
PORTA="$( { grep -E '^[[:space:]]*(export[[:space:]]+)?GAS_VOICE_PORT=' .env || true; } | head -1 | sed 's/[[:space:]]#.*//; s/.*=//; s/[^0-9]//g')"
# V-3 ve #323: il server può metterci qualche secondo ad ascoltare: si riprova per 30 s.
PRONTO=no
for _ in $(seq 1 30); do
  if nc -z 127.0.0.1 "${PORTA:-8765}" 2>/dev/null; then PRONTO=si; break; fi
  sleep 1
done
[ "$PRONTO" = si ] \
  || stop "il server voce non risponde su 127.0.0.1:${PORTA:-8765}: guarda $GAS/.gas_voce/voce.server.log"
# …e i servizi devono essere ancora accesi dopo l'attesa (uno che parte e cade subito).
for s in "${SERVIZI[@]}"; do
  STATO="$(launchctl print "$DOMINIO/$s" 2>/dev/null || true)"
  case "$STATO" in
    *"state = running"*) ;;
    *) stop "$s si è fermato dopo l'avvio: guarda $GAS/.gas_voce/${s#com.gas.}.log" ;;
  esac
done
if grep -Eq '^[[:space:]]*(export[[:space:]]+)?GAS_VOICE_URL=.+' .env; then
  echo "AVVISO: nel .env c'è GAS_VOICE_URL: l'ascolto manda le richieste lì, ma questo controllo ha guardato solo il server sul Mac."
fi
echo "6/6 tutto acceso: dì «Hey Jarvis» e aspetta il bip."
echo "La prima volta macOS chiede il permesso del microfono: rispondi «Consenti»."
