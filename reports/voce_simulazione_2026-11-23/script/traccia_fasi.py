"""Rilevatore a più fasi: N modelli hey_jarvis sfalsati di 1280/N campioni sulla stessa
griglia da 80 ms; punteggio del blocco = max sulle fasi (con verificatore per fase).
Uso: python traccia_fasi.py <flusso> <N> <pkl...>  → tracce_fN_nover/ e tracce_fN_ver/"""
import os, pickle, sys
from pathlib import Path
import numpy as np
from openwakeword.model import Model
QUI = Path(__file__).resolve().parent
nome, N = sys.argv[1], int(sys.argv[2]); pkl = sys.argv[3:]
ver = [pickle.load(open(p, "rb")) for p in pkl]
x = np.load(QUI / "flussi" / f"{nome}.npy")
n = len(x) // 1280 - 1
BASE = 0.25
raws = np.zeros((N, n), np.float32); sc = np.zeros((len(ver), N, n), np.float32)
for f in range(N):
    off = f * 1280 // N
    m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
    for i in range(n):
        r = m.predict(x[off + i * 1280: off + (i + 1) * 1280])["hey_jarvis"]
        raws[f, i] = r
        sc[:, f, i] = r
        if r >= BASE and ver:
            ft = m.preprocessor.get_features(m.model_inputs["hey_jarvis"])
            for k, v in enumerate(ver):
                sc[k, f, i] = v.predict_proba(ft)[0][-1]
for suff, raw, prob in [("nover", raws.max(0), np.zeros((0, n))),
                        ("ver", np.ones(n, np.float32), sc.max(1))]:
    d = QUI / f"tracce_f{N}_{suff}"; d.mkdir(exist_ok=True)
    np.savez(d / f"{nome}.npz", raw=raw, prob=prob, pkl=np.array(pkl))
print(nome, N, "fasi ok")
