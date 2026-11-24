"""Flussi di valutazione NUOVI, con voci mai viste in addestramento (stesso formato dei flussi
della simulazione del 23/11: <nome>.npy int16 16 kHz + <nome>.json con le chiamate).
  G_chiamate_nuove: 160 «ehi jarvis» (40 per distanza) di voci tenute da parte (riccardo,
      parlanti libritts/vctk/l2arctic/sharvard di valutazione, espeak it+m3), con richiesta dopo
  H_parlato_vero: parlato italiano VERO (MLS test, 10 lettori mai visti) vicino/−6/−12 dB
Uso: python flussi_nuovi.py <dati> <uscita> [--ore_mls 5]"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import genera as G  # noqa: E402
import lib_sim as L  # noqa: E402
import testi as T  # noqa: E402

RICHIESTE = ["che ore sono", "accendi la luce", "leggimi le mail", "che tempo fa domani",
             "ricordami di chiamare marco"]


def chiamate_nuove(out: Path):
    rng = np.random.default_rng(21)
    r = random.Random(21)
    piper = [(n, te, w) for n, tr, te, w in T.PIPER if te]
    pezzi, n, chiamate = [], 0, []
    ordine = [d for d in L.DISTANZE for _ in range(40)]
    rng.shuffle(ordine)
    for k, d in enumerate(ordine):
        sil = np.zeros(int(rng.uniform(3, 6) * L.FREQ), np.float32)
        pezzi.append(sil); n += len(sil)
        if r.random() < 0.12:
            voce = r.choice(T.ESPEAK_IT_TEST)
            x = G.espeak_clip(voce, r.choice(["ehi jarvis", "ehi giarvis", "hei giàrvis"]), r)
            rq = G.espeak_clip(voce, r.choice(RICHIESTE), r)
            chi = f"espeak|{voce}"
        else:
            nome, parl, _ = r.choices(piper, weights=[p[2] for p in piper])[0]
            sp = r.choice(parl)
            fon = r.choice(T.FONEMI_POS_EN) if r.random() < 0.15 else r.choice(T.FONEMI_POS_IT)
            x = G.piper_clip(nome, sp, fon, r)
            rq = G.piper_clip(nome, sp, G.fonemizza_it(r.choice(RICHIESTE)), r)
            chi = f"{nome}|{sp}|{fon}"
        x = L.a_distanza(L.normalizza(x.astype(np.float32), L.RMS_VICINO * 10 ** (rng.uniform(-2, 2) / 20)), d, k)
        t0 = n / L.FREQ
        pezzi.append(x); n += len(x)
        chiamate.append({"inizio": t0, "fine": t0 + len(x) / L.FREQ - L.DISTANZE[d][1],
                         "distanza": d, "voce": chi})
        sil = np.zeros(int(rng.uniform(0.2, 0.6) * L.FREQ), np.float32)
        pezzi.append(sil); n += len(sil)
        rq = L.a_distanza(L.normalizza(rq.astype(np.float32)), d, k)
        pezzi.append(rq); n += len(rq)
        pezzi.append(np.zeros(5 * L.FREQ, np.float32)); n += 5 * L.FREQ
    salva(out, "G_chiamate_nuove", pezzi, chiamate)


def parlato_vero(dati: Path, out: Path, ore: float):
    """A pezzi (int16) per stare nella memoria: rumore di stanza aggiunto pezzo per pezzo."""
    rng = np.random.default_rng(22)
    m = np.load(dati / "mls_test.npy", mmap_mode="r")
    pezzi, i, k = [], 0, 0
    fine = min(len(m), int(ore * 3600 * L.FREQ))
    while i < fine:
        lung = int(rng.uniform(10, 30) * L.FREQ)
        x = np.asarray(m[i:i + lung], np.float32)
        i += lung
        d = ["vicino", "-6dB", "-12dB"][int(rng.integers(3))]
        x = L.a_distanza(L.normalizza(x, L.RMS_VICINO * 10 ** (rng.uniform(-3, 3) / 20)), d, k)
        x = np.concatenate([x, np.zeros(int(rng.uniform(0.3, 2) * L.FREQ), np.float32)])
        pezzi.append(L.a_int16(x + L.rosa(len(x), L.RMS_STANZA, k)))
        k += 1
    y = np.concatenate(pezzi)
    np.save(out / "H_parlato_vero.npy", y)
    json.dump({"durata_s": len(y) / L.FREQ, "chiamate": []}, open(out / "H_parlato_vero.json", "w"))
    print("H_parlato_vero", "%.1f min" % (len(y) / L.FREQ / 60), flush=True)


def salva(out: Path, nome: str, pezzi, chiamate):
    y = np.concatenate(pezzi)
    y = y + L.rosa(len(y), L.RMS_STANZA, 99)
    np.save(out / f"{nome}.npy", L.a_int16(y))
    json.dump({"durata_s": len(y) / L.FREQ, "chiamate": chiamate}, open(out / f"{nome}.json", "w"), indent=0)
    print(nome, "%.1f min" % (len(y) / L.FREQ / 60), len(chiamate), "chiamate", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dati")
    ap.add_argument("uscita")
    ap.add_argument("--ore_mls", type=float, default=5.3)
    a = ap.parse_args()
    G._DATI = str(Path(a.dati).resolve())
    out = Path(a.uscita)
    out.mkdir(parents=True, exist_ok=True)
    if not (out / "G_chiamate_nuove.npy").exists():
        chiamate_nuove(out)
    parlato_vero(Path(a.dati), out, a.ore_mls)
