"""Simulazione di scripts/voce/registra_voce.py con il VERO main(): microfono finto che dà
blocchi sintetici (voce «operatore» espeak a varie distanze + rumore di stanza), VERO
MotoreOWW (misura + addestra), altre voci generate con espeak al posto di `say`.

Uso: python sim_registra.py <radice_di_lavoro> [seme] [--variante X]
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import numpy as np

QUI = Path(__file__).resolve().parent
SIM = QUI.parent / "sim"            # copia del repo
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(QUI))
os.environ["GAS_NO_DOTENV"] = "1"

import lib_sim as L  # noqa: E402
from scripts.voce import registra_voce as rv  # noqa: E402
from clients.voice import ascolto as a  # noqa: E402

# gruppo di registra_voce → (guadagno dB in più, distanza)
MAPPA = [
    ("mezzo metro", "vicino", 0.0),
    ("voce bassa", "vicino", -8.0),
    ("3 metri", "-12dB", 0.0),
    ("altra stanza", "-20dB", 0.0),
    ("camminando", "-6dB", 0.0),
    ("di spalle", "-12dB", -3.0),
]


def voce_operatore(rng: np.random.Generator, testo: str | None = None,
                   valutazione: bool = False) -> np.ndarray:
    """Una chiamata dell'operatore simulato: it+m3, 80% «ehi jarvis» (accento italiano,
    punteggio ~0,4 da vicino come la voce vera), 20% «hey jarvis» (~0,9)."""
    if testo is None:
        testo = "ehi jarvis" if rng.random() < 0.85 else "hey jarvis"
    if valutazione:   # rese diverse da quelle della registrazione (niente sovrapposizione)
        vel = int(rng.choice([162, 167, 172, 177, 182, 187]))
        pit = int(rng.choice([42, 46, 50, 54, 58]))
    else:
        vel = int(rng.choice([160, 165, 170, 175, 180, 185, 190]))
        pit = int(rng.choice([40, 44, 48, 52, 56, 60]))
    return L.normalizza(L.tts(testo, "it+m3", vel, pit), L.RMS_VICINO * 10 ** (rng.uniform(-2, 2) / 20))


def parlato(rng, voci, frasi, secondi, distanza="vicino", gain_db=0.0, seme=0):
    """`secondi` di parlato continuo (frasi con pause di 0,2-0,8 s)."""
    out = []
    n = 0
    while n < secondi * L.FREQ:
        voce, pit = voci[int(rng.integers(len(voci)))]
        x = L.normalizza(L.tts(str(rng.choice(frasi)), voce, int(rng.integers(150, 190)), pit))
        x = L.a_distanza(x, distanza, seme) * 10 ** (gain_db / 20)
        out.append(x)
        out.append(np.zeros(int(rng.uniform(0.2, 0.8) * L.FREQ), np.float32))
        n += len(x) + len(out[-1])
    y = np.concatenate(out)[: int(secondi * L.FREQ)]
    return y


class MicFinto:
    """Il microfono di registra_voce: a ogni finestra (svuota + blocchi) genera rumore di
    stanza e, nei positivi, una chiamata dell'operatore a un ritardo realistico."""

    def __init__(self, rng: np.random.Generator) -> None:
        self.rng = rng
        self.fase = None      # (distanza, gain) | "parlato" | "tv"
        self.coda: list = []
        self.finestre = 0
        self.log: list = []

    def chiedi(self, testo: str) -> str:
        if "Vuoi registrare anche" in testo:
            return "s"
        if "parla normalmente" in testo:
            self.fase = "parlato"
        elif "Accendi la TV" in testo:
            self.fase = "tv"
        else:
            for chiave, dist, g in MAPPA:
                if chiave in testo:
                    self.fase = (dist, g, "Se da lì non senti il bip" in testo)
        return ""

    def svuota(self) -> None:
        self.coda = []

    def _genera(self, n_blocchi: int) -> np.ndarray:
        n = n_blocchi * a.BLOCCO
        rumore = L.rosa(n, L.RMS_STANZA, int(self.rng.integers(1 << 30)))
        if self.fase == "parlato":
            y = parlato(self.rng, [("it+m3", 50)], L.FRASI_IT + (L.QUASI_OMOFONI * 2 if os.environ.get("SIM_DURI") else []), n / L.FREQ, "vicino", -2)
            return rumore + y
        if self.fase == "tv":
            y = parlato(self.rng, L.ALTRE_VOCI, L.FRASI_TV, n / L.FREQ, "-12dB", 0, 3)
            return rumore + y
        dist, g, lontano = self.fase
        x = L.a_distanza(voce_operatore(self.rng), dist, int(self.rng.integers(5))) * 10 ** (g / 20)
        if lontano:   # il bip non si sente: parla quando capita (ogni ~9 s)
            inizio = int(self.rng.uniform(-0.5, 7.0) * L.FREQ)
        else:         # reazione al bip
            inizio = int(self.rng.uniform(0.3, 1.0) * L.FREQ)
        y = np.zeros(n, np.float32)
        i0, i1 = max(0, inizio), min(n, inizio + len(x))
        if i1 > i0:
            y[i0:i1] = x[i0 - inizio: i1 - inizio]
        self.log.append((dist, g, inizio / L.FREQ))
        return rumore + y

    def blocchi(self):
        # registra_voce chiede blocchi finché non ne ha abbastanza: ne generiamo 1 min
        # al più, a pezzi di 6 s (abbastanza per una finestra)
        while True:
            if not self.coda:
                n = 750 if self.fase in ("parlato", "tv") else 75
                self.coda = L.blocchi(self._genera(n))
            yield self.coda.pop(0)

    def chiudi(self) -> None:
        pass


def altre_voci_espeak(radice: Path) -> int:
    """Al posto di `say` del Mac: TESTI_ALTRE_VOCI con 12 voci espeak, due velocità."""
    d = rv._privata(rv.cartella(radice) / rv.ALTRE_VOCI / "negativi", radice)
    n = 0
    for i, (voce, pit) in enumerate(L.ALTRE_VOCI[: rv.MAX_ALTRE_VOCI]):
        for j, testo in enumerate(rv.TESTI_ALTRE_VOCI):
            for vel in (160, 210):
                x = L.normalizza(L.tts(testo, voce, vel, pit))
                p = d / ("voce%02d_%d_%d.wav" % (i, j, vel))
                rv._scrivi_privato(p, a.in_wav(L.blocchi(np.concatenate([x, np.zeros(1280, np.float32)]))))
                n += 1
    return n


def main() -> int:
    radice = Path(sys.argv[1]).resolve()
    seme = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    radice.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seme)
    mic = MicFinto(rng)
    codice = rv.main(["--secondi-negativi", "60"], microfono=lambda: mic,
                     altre_voci=altre_voci_espeak, radice=radice, chiedi=mic.chiedi,
                     dorme=lambda s: None, bip=lambda t: None)
    print("exit", codice, "finestre positive:", len(mic.log))
    return codice


if __name__ == "__main__":
    sys.exit(main())
