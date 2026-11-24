"""Libreria della simulazione voce: sintesi espeak-ng, distanza (attenuazione+riverbero),
rumore rosa, TV. Tutto 16 kHz mono, float32 in scala int16."""
from __future__ import annotations

import functools
import hashlib
import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

FREQ = 16000
CACHE = Path(__file__).resolve().parent / "cache"
CACHE.mkdir(exist_ok=True)

# livello della voce "vicino al Mac" (mezzo metro): RMS sul parlato attivo, scala int16.
# ~ -22 dBFS: tipico di un MacBook con voce normale a 50 cm (AGC di macOS acceso).
RMS_VICINO = 2500.0
RMS_STANZA = 40.0   # rumore di fondo di una stanza tranquilla (~ -58 dBFS)

# distanze: (nome, attenuazione dB, RT60 s, rapporto diretto/riverbero dB)
DISTANZE = {
    "vicino": (0.0, 0.25, 25.0),
    "-6dB": (-6.0, 0.4, 4.0),
    "-12dB": (-12.0, 0.5, 0.0),
    "-20dB": (-20.0, 0.6, -6.0),
}


def tts(testo: str, voce: str, velocita: int = 160, pitch: int = 50) -> np.ndarray:
    chiave = hashlib.sha1(f"{testo}|{voce}|{velocita}|{pitch}".encode()).hexdigest()[:16]
    p = CACHE / f"{chiave}.npy"
    if p.exists():
        return np.load(p)
    wav = subprocess.run(["espeak-ng", "-v", voce, "-s", str(velocita), "-p", str(pitch),
                          "--stdout", testo], capture_output=True, check=True).stdout
    raw = subprocess.run(["ffmpeg", "-loglevel", "quiet", "-i", "pipe:0", "-ar", str(FREQ),
                          "-ac", "1", "-f", "s16le", "pipe:1"], input=wav,
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    # togli silenzio iniziale/finale di espeak
    att = np.abs(x) > 200
    if att.any():
        i0, i1 = np.argmax(att), len(att) - np.argmax(att[::-1])
        x = x[max(0, i0 - 800): i1 + 800]
    np.save(p, x)
    return x


def rms_attivo(x: np.ndarray) -> float:
    b = x[: len(x) // 320 * 320].reshape(-1, 320)
    e = np.sqrt((b ** 2).mean(1))
    soglia = e.max() * 0.1 if len(e) else 0
    att = e[e > soglia]
    return float(np.sqrt((att ** 2).mean())) if len(att) else 1.0


def normalizza(x: np.ndarray, rms: float = RMS_VICINO) -> np.ndarray:
    return x * (rms / max(rms_attivo(x), 1e-6))


@functools.lru_cache(maxsize=64)
def rir(rt60: float, drr_db: float, seme: int = 0) -> np.ndarray:
    """Risposta all'impulso sintetica: impulso diretto + coda esponenziale di rumore
    (riflessioni precoci a 5-25 ms), energia della coda fissata dal DRR."""
    rng = np.random.default_rng(seme)
    n = int(rt60 * FREQ * 1.2)
    t = np.arange(n) / FREQ
    coda = rng.standard_normal(n) * np.exp(-6.9 * t / rt60)
    coda[: int(0.004 * FREQ)] = 0
    # riflessioni precoci
    for _ in range(6):
        k = int(rng.uniform(0.005, 0.025) * FREQ)
        coda[k] += rng.uniform(-0.6, 0.6) * np.sqrt((coda ** 2).sum()) / 4
    # leggero passa-basso sulla coda (aria e pareti)
    coda = np.convolve(coda, np.ones(4) / 4, mode="same")
    e_coda = (coda ** 2).sum()
    k = np.sqrt(10 ** (-drr_db / 10) / e_coda)
    h = coda * k
    h[0] = 1.0
    return h.astype(np.float32)


def a_distanza(x: np.ndarray, distanza: str, seme: int = 0) -> np.ndarray:
    gain_db, rt60, drr = DISTANZE[distanza]
    if distanza != "vicino" or True:
        from scipy.signal import fftconvolve
        y = fftconvolve(x, rir(rt60, drr, seme % 5))[: len(x) + int(rt60 * FREQ)]
    # la riverberazione aggiunge energia: si rinormalizza il diretto al guadagno voluto
    y = y * (10 ** (gain_db / 20))
    return y.astype(np.float32)


def rosa(n: int, rms: float, seme: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seme)
    w = rng.standard_normal(n)
    f = np.fft.rfft(w)
    k = np.arange(len(f))
    k[0] = 1
    f = f / np.sqrt(k)
    y = np.fft.irfft(f, n)
    return (y / y.std() * rms).astype(np.float32)


def a_int16(x: np.ndarray) -> np.ndarray:
    return np.clip(np.round(x), -32768, 32767).astype(np.int16)


def blocchi(x: np.ndarray) -> List[np.ndarray]:
    x = a_int16(x)
    return [x[i:i + 1280] for i in range(0, len(x) - 1279, 1280)]


# ─────────────── voci e testi ──

# operatore simulato: voce italiana maschile (scelta con scegli_operatore.py)
OPERATORE = {"voce": "it+m3", "pitch": 45, "velocita": 165}

ALTRE_VOCI = [  # «altre persone» e TV
    ("it+f2", 60), ("it+m1", 50), ("it+f4", 65), ("it+m5", 40),
    ("en-us+f1", 60), ("en-gb+m2", 45), ("en-us+m7", 50), ("es+f3", 60),
    ("it+klatt", 50), ("en-us+f4", 65), ("it+m7", 55), ("pt-br+m1", 50),
]

CHIAMATE_OP = ["hey jarvis", "ehi jarvis", "ehi giarvis", "hei giàrvis", "hey jarvis,",
               "ehi, jarvis"]

FRASI_IT = [
    "oggi fa freddo e devo andare a fare la spesa", "hai visto la partita di ieri sera",
    "domani ho una riunione con il cliente alle nove", "passami il caricabatterie per favore",
    "che ore sono adesso", "mi piace molto questa canzone", "stasera guardiamo un film",
    "giovanni ha chiamato prima", "ci vediamo dopo al bar",
    "il treno è in ritardo di dieci minuti", "devo mandare la fattura al commercialista",
    "hai sentito marco oggi", "la riunione è spostata a giovedì pomeriggio",
    "metti su l'acqua per la pasta", "il gatto ha rovesciato il vaso",
    "non trovo più le chiavi della macchina", "ho finito il lavoro per il cliente nuovo",
    "domenica andiamo al mare se fa bello", "il preventivo va rivisto entro venerdì",
    "chiama tua madre che ti cercava", "ho comprato il pane e il latte",
    "questa settimana è stata pesantissima", "dobbiamo pagare la bolletta della luce",
    "ma dove hai messo il telecomando", "il sito del cliente non si apre",
    "aspetta che finisco questa mail", "hai già mangiato qualcosa",
    "andiamo a fare una passeggiata", "il meccanico ha detto che costa troppo",
    "domani piove tutto il giorno", "allora ci sentiamo stasera",
]
FRASI_TV = [
    "buonasera e benvenuti al telegiornale delle venti",
    "il presidente ha parlato in conferenza stampa questa mattina",
    "previsioni del tempo per domani nuvoloso al nord",
    "e adesso la pubblicità restate con noi", "grazie a tutti per l'attenzione",
    "la borsa di milano chiude in rialzo", "traffico intenso sull'autostrada del sole",
    "il campionato riprende domenica con il derby", "una nuova ricerca sul clima",
    "ascolta questa notizia del telegiornale", "the weather tomorrow will be sunny",
    "breaking news from the city center", "and now back to the studio",
]
QUASI_OMOFONI = [
    "jarvis è un nome strano per un assistente", "ehi giacomo vieni qui", "harvey ha detto di sì",
    "ehi gervasio", "ehi jarno", "hey davis come stai", "ehi charlie", "hey chavez",
    "hey jasmine", "hey travis", "hey jervis", "service charges apply", "ehi gianni",
    "a jar is on the table", "nervous system", "hey jealous", "ehi, sai chi è jarvis",
    "garibaldi era un generale", "ehi marvin", "hey harvest",
]
