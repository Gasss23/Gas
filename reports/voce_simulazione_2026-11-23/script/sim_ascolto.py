"""Il VERO ciclo dell'ascolto (clients/voice/ascolto.py: Ascolto.gira → aspetta_parola →
conversazione → registra → turno) su flussi lunghi, con le parti esterne finte (invio,
riproduzione, bip) e due modi per il rilevatore:
  - «vero»: rilevatore_con_verifica / rilevatore_openwakeword del modulo (modello onnx);
  - «traccia»: punteggi registrati da traccia.py (per provare molte soglie in fretta).
Misura: chiamate prese per distanza, falsi positivi all'ora, latenza (attivazione − fine
della parola)."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI.parent / "sim"))
os.environ["GAS_NO_DOTENV"] = "1"
from clients.voice import ascolto as a  # noqa: E402

logging.basicConfig(level=logging.ERROR)


class Ascolto2(a.Ascolto):
    """Ascolto vero; si annota solo il blocco in cui scatta la parola."""
    def __init__(self, *k, **kw):
        super().__init__(*k, **kw)
        self.attivazioni = []
        self.invii = 0

    def conversazione(self):
        self.attivazioni.append((self._blocchi_letti, self.punteggio_parola))
        super().conversazione()


def rilevatore_da_traccia(tr, k, base, ascolto_ref):
    """score = prob del verificatore k se raw >= base, altrimenti raw (come Model.predict);
    k=None → senza verificatore. Il reset azzera i 5 blocchi dopo (come Model)."""
    raw = tr["raw"]
    prob = tr["prob"][k] if k is not None else None
    stato = {"zero_fino": -1}

    def punteggio(b):
        i = ascolto_ref[0]._blocchi_letti - 1
        if i <= stato["zero_fino"]:
            return 0.0
        r = float(raw[i])
        if prob is not None and r >= base:
            return float(prob[i])
        return r

    def azzera():
        stato["zero_fino"] = ascolto_ref[0]._blocchi_letti + 4
    return punteggio, azzera


def esegui(flusso: str, *, soglia, blocchi_parola=1, modo="traccia", k=None, base=0.25,
           pkl=None):
    x = np.load(QUI / "flussi" / f"{flusso}.npy")
    gt = json.load(open(QUI / "flussi" / f"{flusso}.json"))
    blocchi = iter([x[i:i + 1280] for i in range(0, len(x) - 1279, 1280)])
    ref = [None]
    if modo == "traccia":
        tr = np.load(QUI / os.environ.get("TRACCE", "tracce") / f"{flusso}.npz")
        punteggio, azzera = rilevatore_da_traccia(tr, k, base, ref)
    else:
        if pkl:
            v = a.Verifica("attiva", percorso=Path(pkl), soglia_base=base)
            punteggio, azzera = (a.rilevatore_openwakeword("hey_jarvis", Path(pkl), base, fasi=int(os.environ.get("FASI", "1"))))
            assert v.attiva, v.motivo
        else:
            punteggio, azzera = a.rilevatore_openwakeword("hey_jarvis", fasi=int(os.environ.get("FASI", "1")))
    asc = Ascolto2(blocchi, punteggio, lambda wav: (True, b"mp3", ""), lambda audio: None,
                   lambda t: None, azzera_rilevatore=azzera, soglia=soglia,
                   blocchi_parola=blocchi_parola, coda_eco_s=a.CODA_ECO_S,
                   subito_s=a.SUBITO_S, finestra_s=10.0, max_turni=1,
                   soglia_interruzione=0.8, blocchi_interruzione=3)
    ref[0] = asc
    asc.gira()
    return valuta(asc.attivazioni, gt)


def valuta(attivazioni, gt):
    sb = a.SEC_BLOCCO
    chiamate = gt["chiamate"]
    prese = [None] * len(chiamate)
    falsi = []
    for blk, _p in attivazioni:
        t = blk * sb
        for j, c in enumerate(chiamate):
            if c["inizio"] - 0.1 <= t <= c["fine"] + 1.2 and prese[j] is None:
                prese[j] = t - c["fine"]
                break
        else:
            falsi.append(t)
    per_dist = {}
    for c, p in zip(chiamate, prese):
        d = c["distanza"]
        tot, ok = per_dist.get(d, (0, 0))
        per_dist[d] = (tot + 1, ok + (p is not None))
    lat = [p for p in prese if p is not None]
    return {"per_distanza": per_dist, "falsi": len(falsi),
            "falsi_ora": len(falsi) / (gt["durata_s"] / 3600),
            "latenza_med": float(np.median(lat)) if lat else None,
            "latenza_max": float(np.max(lat)) if lat else None,
            "durata_min": gt["durata_s"] / 60}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("flusso")
    ap.add_argument("--soglia", type=float, default=0.5)
    ap.add_argument("--blocchi", type=int, default=1)
    ap.add_argument("--modo", default="traccia")
    ap.add_argument("--k", type=int, default=None)
    ap.add_argument("--base", type=float, default=0.25)
    ap.add_argument("--pkl", default=None)
    r = ap.parse_args()
    print(json.dumps(esegui(r.flusso, soglia=r.soglia, blocchi_parola=r.blocchi, modo=r.modo,
                            k=r.k, base=r.base, pkl=r.pkl)))
