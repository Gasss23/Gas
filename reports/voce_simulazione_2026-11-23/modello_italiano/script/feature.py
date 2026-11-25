"""Augmentation + caratteristiche openWakeWord (melspettrogramma + speech_embedding di Google,
in onnx, su CPU) delle clip generate. Finestra di 2 s (32000 campioni) → (16, 96).

Augmentation: velocità/tono (ricampionamento ±10%), livello (vicino … −26 dB), riverbero
(risposte all'impulso vere MIT o sintetiche come lib_sim.py), colorazione del microfono
(passa-alto / passa-basso), rumore di stanza rosa, a volte rumore colorato o parlato
italiano vero (MLS) sotto.

Uso: python feature.py <dati> <clip> <feat> [--giri_pos 3 --giri_neg 2 --mls_finestre 40000]"""
from __future__ import annotations

import argparse
import glob
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

FREQ = 16000
LUNG = 32000
RMS_VICINO = 2500.0
_G: dict = {}


def _init(dati: str) -> None:
    from openwakeword.utils import AudioFeatures
    _G["F"] = AudioFeatures(ncpu=1, inference_framework="onnx")
    rir = []
    for p in sorted(glob.glob(f"{dati}/rir/*.wav")):
        sr, h = wavfile.read(p)
        h = h.astype(np.float32)
        if h.ndim > 1:
            h = h[:, 0]
        if sr != FREQ:
            h = resample_poly(h, FREQ // 100, sr // 100)
        i = int(np.argmax(np.abs(h)))
        h = h[max(0, i - 16):]   # parti dal suono diretto
        rir.append((h / np.abs(h).max()).astype(np.float32))
    _G["rir"] = rir
    mls = Path(dati) / "mls_train.npy"
    _G["mls"] = np.load(mls, mmap_mode="r") if mls.exists() else None


def rms_attivo(x: np.ndarray) -> float:
    b = x[: len(x) // 320 * 320].reshape(-1, 320)
    if not len(b):
        return 1.0
    e = np.sqrt((b.astype(np.float64) ** 2).mean(1))
    att = e[e > e.max() * 0.1]
    return float(np.sqrt((att ** 2).mean())) if len(att) else 1.0


def rosa(n: int, rng, esp: float = 0.5) -> np.ndarray:
    f = np.fft.rfft(rng.standard_normal(n))
    k = np.arange(len(f), dtype=np.float64)
    k[0] = 1
    y = np.fft.irfft(f / k ** esp, n)
    return (y / (y.std() + 1e-9)).astype(np.float32)


def rir_sintetica(rng) -> np.ndarray:
    rt60 = rng.uniform(0.2, 0.8)
    drr = rng.uniform(-6, 20)
    n = int(rt60 * FREQ * 1.2)
    t = np.arange(n) / FREQ
    coda = rng.standard_normal(n) * np.exp(-6.9 * t / rt60)
    coda[: int(0.004 * FREQ)] = 0
    coda = np.convolve(coda, np.ones(4) / 4, mode="same")
    h = coda * np.sqrt(10 ** (-drr / 10) / (coda ** 2).sum())
    h[0] = 1.0
    return h.astype(np.float32)


def livello_db(rng) -> float:
    r = rng.random()
    if r < 0.40:
        return rng.uniform(-4, 4)
    if r < 0.60:
        return rng.uniform(-9, -3)
    if r < 0.80:
        return rng.uniform(-15, -9)
    if r < 0.95:
        return rng.uniform(-22, -15)
    return rng.uniform(-28, -22)


def aumenta(clip: np.ndarray, rng, allinea_fine: bool) -> np.ndarray:
    x = clip.astype(np.float32)
    if rng.random() < 0.5:   # velocità e tono insieme (±10%)
        f = rng.uniform(0.9, 1.1)
        x = resample_poly(x, 100, int(round(100 * f)))
    x = x * (RMS_VICINO * 10 ** (livello_db(rng) / 20) / max(rms_attivo(x), 1e-3))
    n_dry = len(x)
    if rng.random() < 0.75:   # riverbero
        h = _G["rir"][rng.integers(len(_G["rir"]))] if (_G["rir"] and rng.random() < 0.6) \
            else rir_sintetica(rng)
        y = fftconvolve(x, h)[: len(x) + int(0.5 * FREQ)].astype(np.float32)
        y *= np.sqrt((x ** 2).sum() / max((y[:n_dry] ** 2).sum(), 1e-6)) * rng.uniform(0.7, 1.0)
        x = y
    w = np.zeros(LUNG, np.float32)
    if allinea_fine:   # fine della parola (suono diretto) a 0–300 ms dalla fine della finestra
        fine = LUNG - int(rng.uniform(0, 0.3) * FREQ)
        ini = fine - n_dry
    else:
        ini = int(rng.integers(-n_dry // 2, LUNG - n_dry // 2)) if rng.random() < 0.6 \
            else LUNG - n_dry - int(rng.uniform(0, 0.3) * FREQ)
    a, b = max(0, ini), min(LUNG, ini + len(x))
    if b > a:
        w[a:b] += x[a - ini: b - ini]
    return w


def sfondo(w: np.ndarray, rng) -> np.ndarray:
    w = w + rosa(LUNG, rng) * rng.uniform(15, 90)   # stanza
    r = rng.random()
    if r < 0.2 and _G["mls"] is not None:   # parlato italiano vero sotto (TV, altre persone)
        m = _G["mls"]
        i = int(rng.integers(0, len(m) - LUNG))
        s = np.asarray(m[i:i + LUNG], np.float32)
        s *= RMS_VICINO * 10 ** (rng.uniform(-30, -12) / 20) / max(rms_attivo(s), 1e-3)
        w = w + s
    elif r < 0.4:   # rumore colorato (ventola, strada, elettrodomestici)
        w = w + rosa(LUNG, rng, rng.uniform(0, 1.0)) * RMS_VICINO * 10 ** (rng.uniform(-35, -15) / 20)
    if rng.random() < 0.5:   # colorazione del microfono
        sos = butter(2, [rng.uniform(60, 300), rng.uniform(3500, 7500)], "bandpass", fs=FREQ,
                     output="sos")
        w = sosfilt(sos, w).astype(np.float32)
    return np.clip(np.round(w), -32768, 32767).astype(np.int16)


def lavoro(arg):
    tipo, clip, seme = arg
    rng = np.random.default_rng(seme)
    fin = []
    for c in clip:
        if tipo in ("mls", "ami"):
            w = np.asarray(c, np.float32)
            w = w * (RMS_VICINO * 10 ** (livello_db(rng) / 20) / max(rms_attivo(w), 1e-3))
            if tipo == "mls" and rng.random() < 0.5:   # AMI è già registrato da lontano
                h = _G["rir"][rng.integers(len(_G["rir"]))] if _G["rir"] else rir_sintetica(rng)
                w = fftconvolve(w, h)[:LUNG].astype(np.float32)
        else:
            w = aumenta(c, rng, allinea_fine=(tipo == "pos"))
        fin.append(sfondo(w, rng))
    return _G["F"].embed_clips(np.stack(fin), batch_size=64).astype(np.float16)


def calcola(pool, tipo, clip, giri, seme0, uscita):
    compiti, k = [], 0
    for g in range(giri):
        for i in range(0, len(clip), 200):
            compiti.append((tipo, clip[i:i + 200], seme0 + k))
            k += 1
    out = np.concatenate(list(pool.imap(lavoro, compiti)))
    np.save(uscita, out)
    print(uscita, out.shape, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dati")
    ap.add_argument("clip")
    ap.add_argument("feat")
    ap.add_argument("--giri_pos", type=int, default=3)
    ap.add_argument("--giri_neg", type=int, default=2)
    ap.add_argument("--mls_finestre", type=int, default=40000)
    a = ap.parse_args()
    out = Path(a.feat)
    out.mkdir(parents=True, exist_ok=True)
    with Pool(4, initializer=_init, initargs=(a.dati,)) as pool:
        for nome, tipo, giri, seme in [("pos_train", "pos", a.giri_pos, 10**6),
                                       ("pos_test", "pos", a.giri_pos, 2 * 10**6),
                                       ("neg_train", "neg", a.giri_neg, 3 * 10**6),
                                       ("neg_test", "neg", a.giri_neg, 4 * 10**6),
                                       ("neg2_train", "neg", a.giri_neg, 7 * 10**6)]:
            if (out / f"{nome}.npy").exists() or not Path(a.clip, f"{nome}.npz").exists():
                continue
            clip = list(np.load(f"{a.clip}/{nome}.npz", allow_pickle=True)["clip"])
            calcola(pool, tipo, clip, giri, seme, out / f"{nome}.npy")
        for nome in ("mls_train", "ami_train"):   # parlato vero: finestre da 2 s a caso
            if (out / f"{nome}.npy").exists() or not Path(a.dati, f"{nome}.npy").exists():
                continue
            m = np.load(Path(a.dati, f"{nome}.npy"), mmap_mode="r")
            rng = np.random.default_rng(5 if nome == "mls_train" else 6)
            ini = rng.integers(0, len(m) - LUNG, a.mls_finestre)
            clip = [np.asarray(m[i:i + LUNG]) for i in ini]
            calcola(pool, "mls" if nome == "mls_train" else "ami", clip, 1,
                    (5 if nome == "mls_train" else 6) * 10**6, out / f"{nome}.npy")

if __name__ == "__main__":
    main()
