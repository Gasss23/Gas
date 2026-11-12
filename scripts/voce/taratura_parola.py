#!/usr/bin/env python3
"""
scripts/voce/taratura_parola.py — taratura di «Hey Jarvis» sulla voce vera dell'operatore.

Apre il microfono per qualche secondo, fa girare lo stesso rilevatore dell'ascolto
(openWakeWord, in locale) e per ogni «salita» del punteggio (da 0,30 in su) stampa il
punteggio massimo e quanti blocchi da 80 ms di fila ha passato le soglie 0,5 / 0,6 / 0,7 /
0,8. Alla fine consiglia la regolazione più severa che avrebbe preso TUTTE le chiamate
(GAS_ASCOLTO_SOGLIA e GAS_ASCOLTO_BLOCCHI_PAROLA nel .env).

Uso (sul Mac, dalla cartella di Gas, con l'ascolto acceso o spento: il microfono si può
leggere in due):
    python3 scripts/voce/taratura_parola.py               # 40 s: di' «Hey Jarvis» 5-6 volte
    python3 scripts/voce/taratura_parola.py --secondi 60

Privacy: l'audio resta in memoria e non si salva da nessuna parte; si stampano solo numeri.
Exit 0 a fine prova, 1 se microfono o modello non sono pronti.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

RADICE = Path(__file__).resolve().parents[2]
SOGLIA_SALITA = 0.3                      # da qui in su comincia una «salita» del punteggio
SOGLIE = (0.5, 0.6, 0.7, 0.8)            # soglie provate
BLOCCHI = (1, 2, 3)                      # blocchi di fila provati
SOGLIA_PREDEFINITA = 0.7                 # quella dell'ascolto (clients/voice/ascolto.py)
SEC_BLOCCO = 0.08
# Prova col modello vero (12/11): un solo «Hey Jarvis» a volte dà due salite staccate da
# 1-3 blocchi sotto 0,30. Una salita finisce solo dopo PAUSA_BLOCCHI blocchi di fila sotto
# SOGLIA_SALITA (0,4 s): fra due chiamate vere ci sono secondi.
PAUSA_BLOCCHI = 5


@dataclass
class Salita:
    """Una salita del punteggio da SOGLIA_SALITA in su (pause sotto PAUSA_BLOCCHI blocchi
    comprese): un «Hey Jarvis» (o un rumore)."""
    inizio_s: float
    massimo: float = 0.0
    blocchi: int = 0
    di_fila: Dict[float, int] = field(default_factory=dict)   # soglia → blocchi di fila

    def scatta(self, soglia: float, blocchi: int) -> bool:
        return self.di_fila.get(soglia, 0) >= blocchi


def salite(punteggi: Iterable[float]) -> Iterator[Salita]:
    """Le salite di una sequenza di punteggi (uno per blocco da 80 ms), man mano che
    finiscono. PURA: nessun microfono, nessun modello."""
    corrente: Optional[Salita] = None
    corse = {t: 0 for t in SOGLIE}
    sotto = 0   # blocchi di fila sotto SOGLIA_SALITA dentro la salita corrente
    for i, p in enumerate(punteggi):
        if p >= SOGLIA_SALITA:
            if corrente is None:
                corrente = Salita(inizio_s=round(i * SEC_BLOCCO, 2),
                                  di_fila={t: 0 for t in SOGLIE})
                corse = {t: 0 for t in SOGLIE}
            sotto = 0
            corrente.massimo = max(corrente.massimo, p)
            corrente.blocchi += 1
            for t in SOGLIE:
                corse[t] = corse[t] + 1 if p >= t else 0
                corrente.di_fila[t] = max(corrente.di_fila[t], corse[t])
        elif corrente is not None:
            corse = {t: 0 for t in SOGLIE}
            sotto += 1
            if sotto >= PAUSA_BLOCCHI:
                yield corrente
                corrente = None
                sotto = 0
    if corrente is not None:
        yield corrente


def descrivi(n: int, s: Salita) -> str:
    fila = ", ".join("%.1f: %d" % (t, s.di_fila[t]) for t in SOGLIE)
    return ("%2d) a %5.1f s  punteggio max %.2f  blocchi di fila sopra (soglia: blocchi) %s"
            % (n, s.inizio_s, s.massimo, fila))


def consiglio(trovate: Sequence[Salita], attese: int) -> List[str]:
    """La regolazione più severa che prende tutte le chiamate trovate; se le salite sono
    meno delle chiamate attese, lo dice (parola non sentita nemmeno a 0,3)."""
    righe: List[str] = []
    if not trovate:
        return ["Nessuna salita del punteggio: il microfono non sente la parola (volume, "
                "distanza, microfono sbagliato?). Nessun consiglio."]
    if attese and len(trovate) < attese:
        righe.append("Attenzione: %d salite su %d chiamate attese — %d chiamate non sono "
                     "arrivate nemmeno a %.1f (troppo piano o troppo lontano)."
                     % (len(trovate), attese, attese - len(trovate), SOGLIA_SALITA))
    if attese and len(trovate) > attese:
        righe.append("Attenzione: %d salite ma %d chiamate attese — le salite in più sono "
                     "probabilmente rumore o parlato: rifai la prova in silenzio."
                     % (len(trovate), attese))
    # R-795-1: una salita che non arriva nemmeno alla soglia più bassa provata è troppo
    # debole per essere tarata (spesso rumore): fuori dal consiglio, detto chiaramente
    deboli = [s for s in trovate if s.massimo < min(SOGLIE)]
    if deboli:
        righe.append("%d salit%s sotto %.1f (troppo debol%s o rumore): fuori dal consiglio."
                     % (len(deboli), "a" if len(deboli) == 1 else "e", min(SOGLIE),
                        "e" if len(deboli) == 1 else "i"))
        trovate = [s for s in trovate if s.massimo >= min(SOGLIE)]
        if not trovate:
            righe.append("Nessuna chiamata abbastanza forte: avvicinati al microfono e rifai.")
            return righe
    tabella: List[Tuple[float, int, int]] = []
    for t in SOGLIE:
        for b in BLOCCHI:
            tabella.append((t, b, sum(1 for s in trovate if s.scatta(t, b))))
    righe.append("Chiamate che scatterebbero (su %d salite):" % len(trovate))
    for b in BLOCCHI:
        righe.append("  %d blocc%s: %s" % (b, "o " if b == 1 else "hi", "  ".join(
            "soglia %.1f → %d" % (t, n) for (t, bb, n) in tabella if bb == b)))
    tutte = [(t, b) for (t, b, n) in tabella if n == len(trovate)]
    if tutte:
        # la più severa: soglia più alta, poi più blocchi
        t, b = max(tutte, key=lambda tb: (tb[0], tb[1]))
        righe.append("Consiglio: GAS_ASCOLTO_SOGLIA=%g e GAS_ASCOLTO_BLOCCHI_PAROLA=%d "
                     "(prende tutte le chiamate). Nel .env, poi bash scripts/voce/installa.sh."
                     % (t, b))
        if t < SOGLIA_PREDEFINITA:
            righe.append("Attenzione: soglia %g più permissiva del predefinito %g — più "
                         "rischio di risposte quando non lo chiami. Se una salita era un "
                         "rumore, rifai la prova in silenzio prima di cambiare il .env."
                         % (t, SOGLIA_PREDEFINITA))
    else:
        t, b, n = max(tabella, key=lambda x: (x[2], x[0], x[1]))
        righe.append("Nessuna regolazione le prende tutte: la migliore è "
                     "GAS_ASCOLTO_SOGLIA=%g e GAS_ASCOLTO_BLOCCHI_PAROLA=%d (%d su %d). "
                     "Prova più vicino al microfono o un po' più lento." % (t, b, n,
                                                                            len(trovate)))
    return righe


def _punteggi_dal_microfono(secondi: float, modello: str
                            ) -> Tuple[Iterator[float], Callable[[], None]]:
    sys.path.insert(0, str(RADICE))
    from clients.voice import ascolto  # noqa: E402 — stesso rilevatore e microfono dell'ascolto
    punteggio, _ = ascolto.rilevatore_openwakeword(modello)
    mic = ascolto.Microfono()
    n = int(secondi / SEC_BLOCCO)

    def gen() -> Iterator[float]:
        for i, b in enumerate(mic.blocchi()):
            if i >= n:
                return
            yield float(punteggio(b))
    return gen(), mic.chiudi


def main(argv: Optional[List[str]] = None,
         sorgente: Optional[Callable[[float, str],
                                     Tuple[Iterator[float], Callable[[], None]]]] = None
         ) -> int:
    ap = argparse.ArgumentParser(description="Taratura di «Hey Jarvis» sulla tua voce.")
    ap.add_argument("--secondi", type=float, default=40.0)
    ap.add_argument("--chiamate", type=int, default=0,
                    help="quante volte dirai la parola (per avvisare se qualcuna si perde)")
    ap.add_argument("--modello", default="hey_jarvis")
    args = ap.parse_args(argv)
    try:
        punteggi, chiudi = (sorgente or _punteggi_dal_microfono)(max(args.secondi, 1.0),
                                                                 args.modello)
    except Exception as e:  # microfono o modello non pronti
        print("✗ microfono o modello non pronti (%s): esegui prima "
              "bash scripts/voce/installa.sh" % type(e).__name__, file=sys.stderr)
        return 1
    print("Per %d secondi di' «Hey Jarvis» come lo diresti di solito, con 3-4 secondi di "
          "pausa fra una volta e l'altra (anche da lontano o più piano)." % args.secondi)
    trovate: List[Salita] = []
    try:
        for s in salite(punteggi):
            trovate.append(s)
            print(descrivi(len(trovate), s), flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        chiudi()
    print()
    for riga in consiglio(trovate, args.chiamate):
        print(riga)
    return 0


if __name__ == "__main__":
    sys.exit(main())
