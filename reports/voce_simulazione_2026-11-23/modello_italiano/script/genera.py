"""Genera le clip sintetiche (16 kHz int16, senza augmentation): positivi e negativi avversari,
per addestramento (voci/parlanti di addestramento) e valutazione (voci tenute da parte).

Uso: python genera.py <cartella_dati> <cartella_clip> [--scala 1.0]
Scrive <cartella_clip>/{pos_train,pos_test,neg_train,neg_test}.npz (clip + metadati)."""
from __future__ import annotations

import argparse
import os
import random
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
import testi as T  # noqa: E402

FREQ = 16000
_VOCI: dict = {}
_DATI = ""


def _voce(nome):
    from piper import PiperVoice
    if nome not in _VOCI:
        _VOCI[nome] = PiperVoice.load(f"{_DATI}/piper/{nome}.onnx")
    return _VOCI[nome]


def _taglia(x: np.ndarray) -> np.ndarray:
    att = np.abs(x) > 0.02 * np.abs(x).max()
    if not att.any():
        return x
    i0, i1 = np.argmax(att), len(att) - np.argmax(att[::-1])
    return x[max(0, i0 - 1600): i1 + 1600]


def _a16(x: np.ndarray) -> np.ndarray:
    x = _taglia(x.astype(np.float32))
    x = x / max(np.abs(x).max(), 1e-6) * 0.5 * 32767
    return np.clip(x, -32768, 32767).astype(np.int16)


def piper_clip(nome: str, parlante, fonemi: str, rng: random.Random) -> np.ndarray:
    from piper.config import SynthesisConfig
    v = _voce(nome)
    ids = v.phonemes_to_ids(list(fonemi))
    cfg = SynthesisConfig(speaker_id=parlante, length_scale=rng.uniform(0.75, 1.35),
                          noise_scale=rng.uniform(0.4, 1.0), noise_w_scale=rng.uniform(0.4, 1.0))
    a = v.phoneme_ids_to_audio(ids, cfg)
    sr = v.config.sample_rate
    if sr != FREQ:
        a = resample_poly(a, FREQ // 100, sr // 100)
    return _a16(a)


def espeak_clip(voce: str, testo: str, rng: random.Random) -> np.ndarray:
    wav = subprocess.run(["espeak-ng", "-v", voce, "-s", str(rng.randint(125, 200)),
                          "-p", str(rng.randint(25, 75)), "--stdout", testo],
                         capture_output=True, check=True).stdout
    raw = subprocess.run(["ffmpeg", "-loglevel", "quiet", "-i", "pipe:0", "-ar", str(FREQ),
                          "-ac", "1", "-f", "s16le", "pipe:1"], input=wav,
                         capture_output=True, check=True).stdout
    return _a16(np.frombuffer(raw, dtype=np.int16).astype(np.float32))


def fonemizza_it(testo: str) -> str:
    v = _voce("it_IT-paola-medium")
    return " ".join("".join(s) for s in v.phonemize(testo))


def lavoro(arg):
    """Un compito: (tipo, seme, split, n). Restituisce lista di (clip, meta)."""
    tipo, seme, split, n = arg
    rng = random.Random(seme)
    out = []
    piper = [(nome, tr if split == "train" else te, w) for nome, tr, te, w in T.PIPER]
    piper = [p for p in piper if p[1]]
    pesi = [p[2] for p in piper]
    espeak = T.ESPEAK_IT_TRAIN if split == "train" else T.ESPEAK_IT_TEST
    neg = T.testi_negativi_nomi(seme) if tipo == "neg2" else T.testi_negativi(seme)
    cache_fon: dict = {}
    for _ in range(n):
        usa_espeak = rng.random() < 0.22
        if tipo == "pos":
            if usa_espeak:
                voce, testo = rng.choice(espeak), rng.choice(T.TESTI_POS_ESPEAK)
                out.append((espeak_clip(voce, testo, rng), f"espeak|{voce}|{testo}"))
                continue
            fon = rng.choice(T.FONEMI_POS_EN) if rng.random() < 0.15 else rng.choice(T.FONEMI_POS_IT)
        else:
            testo = rng.choice(neg)
            if usa_espeak:
                voce = rng.choice(espeak)
                out.append((espeak_clip(voce, testo, rng), f"espeak|{voce}|{testo}"))
                continue
            if testo not in cache_fon:
                cache_fon[testo] = fonemizza_it(testo)
            fon = cache_fon[testo]
        nome, parlanti, _ = rng.choices(piper, weights=pesi)[0]
        sp = rng.choice(parlanti)
        out.append((piper_clip(nome, sp, fon, rng), f"piper|{nome}|{sp}|{fon}"))
    return out


def main():
    global _DATI
    ap = argparse.ArgumentParser()
    ap.add_argument("dati")
    ap.add_argument("uscita")
    ap.add_argument("--scala", type=float, default=1.0)
    a = ap.parse_args()
    _DATI = os.path.abspath(a.dati)
    out = Path(a.uscita)
    out.mkdir(parents=True, exist_ok=True)
    piani = {"pos_train": ("pos", "train", 6000), "pos_test": ("pos", "test", 800),
             "neg_train": ("neg", "train", 6000), "neg_test": ("neg", "test", 800),
             "neg2_train": ("neg2", "train", 8000)}
    for nome, (tipo, split, n) in piani.items():
        if (out / f"{nome}.npz").exists():
            print("c'è già", nome)
            continue
        n = int(n * a.scala)
        pezzi = 40
        base = list(piani).index(nome) * 100003
        compiti = [(tipo, base + 7919 * (k + 1), split, n // pezzi) for k in range(pezzi)]
        with Pool(4, initializer=_init, initargs=(_DATI,)) as p:
            ris = [r for blocco in p.imap_unordered(lavoro, compiti) for r in blocco]
        clip = np.empty(len(ris), dtype=object)
        clip[:] = [r[0] for r in ris]
        np.savez(out / f"{nome}.npz", clip=clip, meta=np.array([r[1] for r in ris]))
        dur = np.mean([len(c) for c in clip]) / FREQ
        print(nome, len(ris), "clip, durata media %.2f s" % dur, flush=True)


def _init(d):
    global _DATI
    _DATI = d


if __name__ == "__main__":
    main()
