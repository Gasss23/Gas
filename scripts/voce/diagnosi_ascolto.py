#!/usr/bin/env python3
"""
scripts/voce/diagnosi_ascolto.py — riassunto delle attivazioni dell'ascolto H24 (R8).

Legge il log dell'ascolto (`.gas_voce/ascolto.log`: solo eventi e numeri, mai audio né
testo) e dice, per ogni giorno, quante volte «Hey Jarvis» è scattato e com'è finita:
richiesta inviata, nessuna richiesta (di solito una falsa attivazione: TV, persone),
richiesta cortissima (sospetta), interruzioni, turni di seguito. Poi elenca le ultime
attivazioni con ora, punteggio della parola, secondi di voce ed esito.

Uso (sul Mac, dalla cartella di Gas):
    python3 scripts/voce/diagnosi_ascolto.py                 # ultimi 2 giorni, ultime 20
    python3 scripts/voce/diagnosi_ascolto.py --giorni 7 --ultime 50
    python3 scripts/voce/diagnosi_ascolto.py --log percorso/ascolto.log

Solo lettura: non tocca il log né l'ascolto. Exit 0 se il log c'è (anche vuoto), 1 se manca.
Euristica, non verità: «nessuna richiesta» può anche essere un «Hey Jarvis» vero a cui non
è seguita la domanda; «sospetta» è una richiesta con meno di VOCE_SOSPETTA_S di voce, il
caso in cui Whisper inventa frasi («Grazie»).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, List, Optional

RADICE = Path(__file__).resolve().parents[2]
LOG_PREDEFINITO = RADICE / ".gas_voce" / "ascolto.log"
VOCE_SOSPETTA_S = 0.6

_RIGA = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})[,.]\d+ \w+ (.*)$")
_PAROLA = re.compile(r"^parola di attivazione(?: \(punteggio ([\d.]+)"
                     r"(?:, picchi corti scartati prima: (\d+))?\))?$")
_RICHIESTA = re.compile(r"^richiesta registrata \(([\d.]+) s(?:, voce ([\d.]+) s)?")


@dataclass
class Attivazione:
    """Una conversazione: da «parola di attivazione» a «torno ad aspettare»."""
    giorno: date
    ora: str
    punteggio: Optional[float] = None
    picchi_scartati: int = 0
    richieste: int = 0
    seguiti: int = 0
    interruzioni: int = 0
    voce_s: List[float] = field(default_factory=list)
    prima_voce_s: Optional[float] = None   # voce della richiesta dopo la parola (se nota)
    eventi: List[str] = field(default_factory=list)

    def esito(self) -> str:
        if self.richieste == 0:
            return "nessuna richiesta"
        if self.prima_voce_s is not None and self.prima_voce_s < VOCE_SOSPETTA_S:
            return "richiesta sospetta (voce %.1f s)" % self.prima_voce_s
        extra = []
        if self.seguiti:
            extra.append("%d di seguito" % self.seguiti)
        if self.interruzioni:
            extra.append("%d interruzioni" % self.interruzioni)
        return "richiesta inviata" + (" (" + ", ".join(extra) + ")" if extra else "")


def leggi(righe: Iterable[str]) -> List[Attivazione]:
    """Raggruppa le righe del log in attivazioni. Righe che non sono del formato
    dell'ascolto (o rotte) si saltano senza errori."""
    tutte: List[Attivazione] = []
    corrente: Optional[Attivazione] = None
    for riga in righe:
        m = _RIGA.match(riga.rstrip("\n"))
        if not m:
            continue
        try:
            giorno = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        ora, msg = m.group(2), m.group(3)
        p = _PAROLA.match(msg)
        if p:
            corrente = Attivazione(giorno, ora)
            if p.group(1):
                corrente.punteggio = float(p.group(1))
            if p.group(2):
                corrente.picchi_scartati = int(p.group(2))
            tutte.append(corrente)
            continue
        if corrente is None:
            continue
        r = _RICHIESTA.match(msg)
        if r:
            corrente.richieste += 1
            if "(di seguito)" in msg:
                corrente.seguiti += 1
            if r.group(2):
                corrente.voce_s.append(float(r.group(2)))
                if corrente.richieste == 1:
                    corrente.prima_voce_s = float(r.group(2))
        elif msg.startswith("interrotto:"):
            corrente.interruzioni += 1
        elif msg.startswith("torno ad aspettare"):
            corrente = None
        elif any(msg.startswith(k) for k in ("voce subito", "dopo la parola solo",
                                               "parlato di", "turno di seguito non rivolto",
                                               "pausa a voce")):
            corrente.eventi.append(msg.split(":")[0])
    return tutte


def riassunto(attivazioni: List[Attivazione], giorni: int, ultime: int,
              oggi: Optional[date] = None) -> str:
    oggi = oggi or date.today()
    dal = oggi - timedelta(days=max(giorni, 1) - 1)
    scelte = [a for a in attivazioni if a.giorno >= dal]
    righe = ["Attivazioni di «Hey Jarvis» dal %s al %s" % (dal.isoformat(), oggi.isoformat())]
    if not scelte:
        righe.append("  nessuna attivazione nel periodo.")
        return "\n".join(righe)
    for g in sorted({a.giorno for a in scelte}):
        del_giorno = [a for a in scelte if a.giorno == g]
        conta = {k: 0 for k in ("inviata", "nessuna", "sospetta")}
        for a in del_giorno:
            e = a.esito()
            conta["nessuna" if e.startswith("nessuna") else
                  "sospetta" if "sospetta" in e else "inviata"] += 1
        picchi = sum(a.picchi_scartati for a in del_giorno)
        righe.append("  %s: %d attivazioni — %d con richiesta (di cui %d sospette), "
                     "%d senza richiesta (probabili false); picchi corti scartati: %d"
                     % (g.isoformat(), len(del_giorno), conta["inviata"] + conta["sospetta"],
                        conta["sospetta"], conta["nessuna"], picchi))
    punteggi = sorted(a.punteggio for a in scelte if a.punteggio is not None)
    if punteggi:
        n = len(punteggi)
        mediana = (punteggi[n // 2] if n % 2 else (punteggi[n // 2 - 1] + punteggi[n // 2]) / 2)
        righe.append("  punteggio della parola: min %.2f, mediana %.2f, max %.2f"
                     % (punteggi[0], mediana, punteggi[-1]))
    ultime = max(0, min(ultime, len(scelte)))
    righe.append("Ultime %d:" % ultime)
    for a in scelte[len(scelte) - ultime:]:   # R-761-1-M1: [-0:] darebbe tutta la lista
        voce = ("voce %.1f s" % a.prima_voce_s) if a.prima_voce_s is not None else "voce —"
        punt = ("%.2f" % a.punteggio) if a.punteggio is not None else "—"
        righe.append("  %s %s  punteggio %s  %s  → %s" % (a.giorno.isoformat(), a.ora, punt,
                                                       voce, a.esito()))
    return "\n".join(righe)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Riassunto delle attivazioni dell'ascolto H24.")
    ap.add_argument("--log", type=Path, default=LOG_PREDEFINITO)
    ap.add_argument("--giorni", type=int, default=2)
    ap.add_argument("--ultime", type=int, default=20)
    args = ap.parse_args(argv)
    if not args.log.is_file():
        print("✗ log dell'ascolto non trovato: %s" % args.log, file=sys.stderr)
        return 1
    with args.log.open(encoding="utf-8", errors="replace") as fh:
        print(riassunto(leggi(fh), args.giorni, max(args.ultime, 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
