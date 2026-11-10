#!/bin/bash
# Fetta 43 (standby) — mette in pausa SOLO l'ascolto sempre attivo di Gas sul Mac.
# Uso:  bash scripts/voce/pausa.sh
# Gas smette di ascoltare il microfono (anche «Hey Jarvis»). Il server voce resta acceso
# e il plist resta in ~/Library/LaunchAgents: per riprendere basta
#   bash scripts/voce/riprendi.sh
# La pausa dura fino a riprendi.sh o al prossimo riavvio del Mac (all'accesso l'ascolto
# riparte da solo). Per spegnere tutto per sempre: bash scripts/voce/spegni.sh
set -uo pipefail
[ "$(uname -s)" = "Darwin" ] || { echo "STOP: questo script è solo per il Mac." >&2; exit 1; }
S=com.gas.ascolto
DOMINIO="gui/$(id -u)"
if [ ! -f "$HOME/Library/LaunchAgents/$S.plist" ] \
   && ! launchctl print "$DOMINIO/$S" >/dev/null 2>&1; then
  # V-3 bot su #338: mai installato non è «in pausa»
  echo "L'ascolto di Gas non è installato: non c'è niente da mettere in pausa."
  echo "Per installarlo: bash scripts/voce/installa.sh"
  exit 0
fi
if ! launchctl print "$DOMINIO/$S" >/dev/null 2>&1; then
  echo "Gas era già in pausa: non sta ascoltando."
  echo "Per riprendere: bash scripts/voce/riprendi.sh"
  exit 0
fi
launchctl bootout "$DOMINIO/$S" 2>/dev/null || true
# bootout è asincrono (prova dal vero di M1, 2026-11-02): si aspetta che sparisca, al
# massimo 5 s, così il messaggio dice il vero.
for _ in $(seq 1 50); do
  if ! launchctl print "$DOMINIO/$S" >/dev/null 2>&1; then
    echo "PAUSA: Gas non ascolta più il microfono (nemmeno «Hey Jarvis»)."
    echo "Il server voce resta acceso. Per riprendere: bash scripts/voce/riprendi.sh"
    exit 0
  fi
  sleep 0.1
done
echo "ATTENZIONE: l'ascolto non si è fermato. Aspetta qualche secondo e rilancia" >&2
echo "  bash scripts/voce/pausa.sh   (oppure, per spegnere tutto: bash scripts/voce/spegni.sh)" >&2
exit 1
