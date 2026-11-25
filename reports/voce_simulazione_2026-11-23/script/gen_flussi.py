"""Flussi lunghi per l'ascolto (16 kHz int16) con verità a terra.
  A_chiamate: 120 chiamate dell'operatore (30 per distanza) + richiesta, con chiacchiere
  B_parlato: 30 min di parlato dell'operatore (frasi italiane + quasi-omofoni detti da lui)
  C_tv: 30 min di TV (altre voci, it/en, frasi + quasi-omofoni) a -6/-12 dB riverberata
  D_altri: 40 «Hey Jarvis» detti da ALTRE voci vicino al Mac (chi non è registrato)
Salva flussi/<nome>.npy e flussi/<nome>.json (intervalli delle chiamate in secondi)."""
import json
import sys
from pathlib import Path

import numpy as np

import lib_sim as L
from sim_registra import voce_operatore, parlato

OUT = Path(__file__).resolve().parent / "flussi"
OUT.mkdir(exist_ok=True)
RICHIESTE = ["che ore sono", "accendi la luce", "leggimi le mail", "che tempo fa domani",
             "ricordami di chiamare marco"]
DIST = list(L.DISTANZE)


class Flusso:
    def __init__(self, seme):
        self.rng = np.random.default_rng(seme)
        self.pezzi, self.n, self.chiamate = [], 0, []

    def silenzio(self, s):
        self.add(np.zeros(int(s * L.FREQ), np.float32))

    def add(self, x):
        self.pezzi.append(x.astype(np.float32))
        self.n += len(x)

    def t(self):
        return self.n / L.FREQ

    def salva(self, nome, extra=None):
        y = np.concatenate(self.pezzi)
        y = y + L.rosa(len(y), L.RMS_STANZA, 99)
        np.save(OUT / f"{nome}.npy", L.a_int16(y))
        json.dump({"durata_s": len(y) / L.FREQ, "chiamate": self.chiamate, **(extra or {})},
                  open(OUT / f"{nome}.json", "w"), indent=0)
        print(nome, "%.1f min" % (len(y) / L.FREQ / 60), len(self.chiamate), "chiamate")


def chiamate():
    f = Flusso(10)
    ordine = [d for d in DIST for _ in range(30)]
    f.rng.shuffle(ordine)
    for k, d in enumerate(ordine):
        f.silenzio(f.rng.uniform(3, 6))
        if f.rng.random() < 0.3:   # chiacchiere dell'operatore prima (non per Gas)
            f.add(parlato(f.rng, [("it+m3", 50)], L.FRASI_IT, f.rng.uniform(3, 6), "-6dB", 0, k))
            f.silenzio(f.rng.uniform(1.5, 3))
        x = L.a_distanza(voce_operatore(f.rng, valutazione=True), d, k)
        t0 = f.t()
        f.add(x)
        # fine parola = fine dell'energia diretta (senza la coda di riverbero)
        f.chiamate.append({"inizio": t0, "fine": t0 + len(x) / L.FREQ - L.DISTANZE[d][1],
                           "distanza": d})
        f.silenzio(f.rng.uniform(0.2, 0.6))
        r = L.normalizza(L.tts(str(f.rng.choice(RICHIESTE)), "it+m3", 170, 50))
        f.add(L.a_distanza(r, d, k))
        f.silenzio(5.0)   # Gas risponde (risposta non simulata)
    f.salva("A_chiamate")


def parlato_op():
    f = Flusso(11)
    frasi = L.FRASI_IT + L.QUASI_OMOFONI
    while f.t() < 30 * 60:
        d = "vicino" if f.rng.random() < 0.5 else "-6dB"
        f.add(parlato(f.rng, [("it+m3", int(f.rng.choice([42, 50, 58])))], frasi,
                      f.rng.uniform(5, 20), d, 0, int(f.rng.integers(5))))
        f.silenzio(f.rng.uniform(0.5, 3))
    f.salva("B_parlato")


def tv():
    f = Flusso(12)
    frasi = L.FRASI_TV + L.FRASI_IT + L.QUASI_OMOFONI
    while f.t() < 30 * 60:
        d = "-6dB" if f.rng.random() < 0.5 else "-12dB"
        f.add(parlato(f.rng, L.ALTRE_VOCI, frasi, f.rng.uniform(10, 30), d, 0,
                      int(f.rng.integers(5))))
        f.silenzio(f.rng.uniform(0.2, 1))
    f.salva("C_tv")


def altri():
    f = Flusso(13)
    for k in range(40):
        f.silenzio(f.rng.uniform(4, 7))
        voce, pit = L.ALTRE_VOCI[k % len(L.ALTRE_VOCI)]
        testo = ["hey jarvis", "ehi jarvis"][k % 2]
        x = L.a_distanza(L.normalizza(L.tts(testo, voce, int(f.rng.integers(150, 190)), pit)),
                         "vicino", k)
        t0 = f.t()
        f.add(x)
        f.chiamate.append({"inizio": t0, "fine": t0 + len(x) / L.FREQ - 0.25,
                           "distanza": "vicino", "voce": voce})
        f.silenzio(5)
    f.salva("D_altri")




def sopra_gas():
    """E: Gas parla (voce it+m1 dalle casse, -6 dB riverberata, frasi lunghe) e l'operatore
    dice «ehi jarvis» sopra (vicino o -6 dB) per interromperlo: 60 chiamate."""
    f = Flusso(14)
    for k in range(60):
        gas = parlato(f.rng, [("it+m1", 50)], L.FRASI_TV + L.FRASI_IT, 8.0, "-6dB", 0, k)
        d = "vicino" if k % 2 == 0 else "-6dB"
        x = L.a_distanza(voce_operatore(f.rng, valutazione=True), d, k)
        o = int(f.rng.uniform(2, 5) * L.FREQ)
        t0 = f.t() + o / L.FREQ
        gas[o:o + len(x)] += x[: len(gas) - o]
        f.add(gas)
        f.chiamate.append({"inizio": t0, "fine": t0 + len(x) / L.FREQ - L.DISTANZE[d][1],
                           "distanza": d})
    f.salva("E_sopra_gas")


if __name__ == "__main__":
    for nome in (sys.argv[1:] or ["chiamate", "parlato_op", "tv", "altri"]):
        globals()[nome]()
