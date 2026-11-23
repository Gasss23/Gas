"""Traccia per blocco da 80 ms: punteggio grezzo di hey_jarvis e probabilità di ogni
verificatore (calcolata sulle STESSE caratteristiche che usa openwakeword.Model.predict).
Uso: python traccia.py <flusso> <pkl1> [<pkl2> ...]  → tracce/<flusso>.npz"""
import pickle
import sys
from pathlib import Path

import numpy as np
from openwakeword.model import Model

QUI = Path(__file__).resolve().parent
(QUI / "tracce").mkdir(exist_ok=True)


def main():
    nome = sys.argv[1]
    pkl = sys.argv[2:]
    ver = [pickle.load(open(p, "rb")) for p in pkl]
    x = np.load(QUI / "flussi" / f"{nome}.npy")
    m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
    n = len(x) // 1280
    raw = np.zeros(n, np.float32)
    prob = np.full((len(ver), n), np.nan, np.float32)
    for i in range(n):
        raw[i] = m.predict(x[i * 1280:(i + 1) * 1280])["hey_jarvis"]
        if raw[i] >= 0.05 and ver:
            f = m.preprocessor.get_features(m.model_inputs["hey_jarvis"])
            for k, v in enumerate(ver):
                prob[k, i] = v.predict_proba(f)[0][-1]
    out = QUI / "tracce" / f"{nome}.npz"
    np.savez(out, raw=raw, prob=prob, pkl=np.array(pkl))
    print(nome, n, "blocchi; raw>=0.25:", int((raw >= 0.25).sum()))


if __name__ == "__main__":
    main()
