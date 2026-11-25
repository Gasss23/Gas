"""Valutazione testa a testa col rilevatore VERO dell'ascolto (clients/voice/ascolto.py di
una copia del repo: rilevatore_openwakeword, 1 o 4 fasi) e il VERO ciclo Ascolto.gira.

  python valuta.py tracce <repo> <flussi> <tracce> <modello> <fasi> <flusso...>
      punteggio di ogni blocco da 80 ms col rilevatore vero → <tracce>/<tag>_f<fasi>/<flusso>.npz
  python valuta.py griglia <repo> <flussi> <tracce> <tag> <fasi> <soglie> <flusso...>
      rigioca le tracce nel ciclo vero (Ascolto.gira) per ogni soglia (come sim_ascolto.py)
  python valuta.py validazione <dati> <modello...>
      falsi all'ora su validation_set_features (~11 h di audio generico, caratteristiche pronte)
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

os.environ["GAS_NO_DOTENV"] = "1"
logging.basicConfig(level=logging.ERROR)


def _ascolto(repo: str):
    sys.path.insert(0, repo)
    from clients.voice import ascolto as a
    return a


def tag_di(modello: str) -> str:
    return Path(modello).stem if modello.endswith(".onnx") else modello


def tracce(repo, flussi, cartella, modello, fasi, nomi):
    a = _ascolto(repo)
    fasi = int(fasi)
    d = Path(cartella) / f"{tag_di(modello)}_f{fasi}"
    d.mkdir(parents=True, exist_ok=True)
    for nome in nomi:
        x = np.load(Path(flussi) / f"{nome}.npy")
        punteggio, _ = a.rilevatore_openwakeword(modello, fasi=fasi)
        n = len(x) // a.BLOCCO
        raw = np.array([punteggio(x[i * a.BLOCCO:(i + 1) * a.BLOCCO]) for i in range(n)], np.float32)
        np.savez(d / f"{nome}.npz", raw=raw)
        print(d.name, nome, n, "blocchi", flush=True)


def esegui(a, x, gt, raw, soglia, blocchi_parola=1):
    class Ascolto2(a.Ascolto):
        def __init__(self, *k, **kw):
            super().__init__(*k, **kw)
            self.attivazioni = []

        def conversazione(self):
            self.attivazioni.append((self._blocchi_letti, self.punteggio_parola))
            super().conversazione()

    ref = [None]
    stato = {"zero_fino": -1}

    def punteggio(b):   # traccia registrata; dopo il reset 5 blocchi a zero (come Model.reset)
        i = ref[0]._blocchi_letti - 1
        return 0.0 if i <= stato["zero_fino"] or i >= len(raw) else float(raw[i])

    def azzera():
        stato["zero_fino"] = ref[0]._blocchi_letti + 4
    blocchi = iter([x[i:i + 1280] for i in range(0, len(x) - 1279, 1280)])
    asc = Ascolto2(blocchi, punteggio, lambda wav: (True, b"mp3", ""), lambda audio: None,
                   lambda t: None, azzera_rilevatore=azzera, soglia=soglia,
                   blocchi_parola=blocchi_parola, coda_eco_s=a.CODA_ECO_S,
                   subito_s=a.SUBITO_S, finestra_s=10.0, max_turni=1,
                   soglia_interruzione=0.8, blocchi_interruzione=3)
    ref[0] = asc
    asc.gira()
    sb = a.SEC_BLOCCO
    chiamate = gt["chiamate"]
    prese = [None] * len(chiamate)
    falsi = 0
    for blk, _p in asc.attivazioni:
        t = blk * sb
        for j, c in enumerate(chiamate):
            if c["inizio"] - 0.1 <= t <= c["fine"] + 1.2 and prese[j] is None:
                prese[j] = t - c["fine"]
                break
        else:
            falsi += 1
    per = {}
    for c, p in zip(chiamate, prese):
        tot, ok = per.get(c["distanza"], (0, 0))
        per[c["distanza"]] = (tot + 1, ok + (p is not None))
    lat = [p for p in prese if p is not None]
    return {"per_distanza": per, "falsi": falsi, "ore": gt["durata_s"] / 3600,
            "latenza_med": float(np.median(lat)) if lat else None}


def griglia(repo, flussi, cartella, tag, fasi, soglie, nomi):
    a = _ascolto(repo)
    soglie = [float(s) for s in soglie.split(",")]
    out = {}
    for nome in nomi:
        x = np.load(Path(flussi) / f"{nome}.npy")
        gt = json.load(open(Path(flussi) / f"{nome}.json"))
        raw = np.load(Path(cartella) / f"{tag}_f{fasi}" / f"{nome}.npz")["raw"]
        for s in soglie:
            out[f"{nome}|{s}"] = esegui(a, x, gt, raw, s)
    print(json.dumps({"tag": tag, "fasi": int(fasi), "ris": out}))


def validazione(dati, modelli):
    import onnxruntime as ort
    from numpy.lib.stride_tricks import sliding_window_view
    v = np.load(Path(dati) / "feat" / "validation_set_features.npy").astype(np.float32)
    w = sliding_window_view(v, (16, 96))[:, 0]
    ore = len(v) * 0.08 / 3600
    for m in modelli:
        if not m.endswith(".onnx"):
            import openwakeword
            m = str(Path(openwakeword.__file__).parent / "resources" / "models" / f"{m}_v0.1.onnx")
        so = ort.SessionOptions()
        so.intra_op_num_threads = 1
        s = ort.InferenceSession(m, so)
        nin = s.get_inputs()[0].name
        p = np.array([s.run(None, {nin: w[i:i + 1]})[0][0, 0] for i in range(len(w))], np.float32)
        r = {"modello": Path(m).stem, "ore": round(ore, 2)}
        for soglia in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
            sopra = p >= soglia
            r[str(soglia)] = round(float((sopra[1:] & ~sopra[:-1]).sum() + sopra[0]) / ore, 2)
        print(json.dumps(r), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "tracce":
        tracce(*sys.argv[2:7], sys.argv[7:])
    elif cmd == "griglia":
        griglia(*sys.argv[2:8], sys.argv[8:])
    elif cmd == "validazione":
        validazione(sys.argv[2], sys.argv[3:])
