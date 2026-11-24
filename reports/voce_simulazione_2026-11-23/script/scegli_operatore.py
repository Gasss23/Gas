"""Punteggio grezzo di hey_jarvis per voci/varianti espeak, vicino e a distanza.
Serve a scegliere una voce «operatore» che dia 0,37-0,54 da vicino come quella vera."""
import itertools
import sys

import numpy as np
from openwakeword.model import Model

import lib_sim as L

m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")


def picco(x):
    m.reset()
    pre = L.rosa(2 * L.FREQ, L.RMS_STANZA, 1)
    y = np.concatenate([pre, x, np.zeros(L.FREQ, np.float32)])
    y = y + L.rosa(len(y), L.RMS_STANZA, 2)
    return max(float(m.predict(b)["hey_jarvis"]) for b in L.blocchi(y))


voci = ["it+m1", "it+m3", "it+m5", "it+m7", "it+f2", "it+f4", "it", "en-us", "en-us+f2",
        "en-gb+m3", "es+m2"]
for voce in voci:
    righe = []
    for testo in ["hey jarvis", "ehi jarvis", "ehi giarvis"]:
        for vel, pit in [(150, 40), (175, 55)]:
            x = L.normalizza(L.tts(testo, voce, vel, pit))
            s = [picco(L.a_distanza(x, d)) for d in L.DISTANZE]
            righe.append(f"{testo:12s} v{vel} p{pit}: " + " ".join(f"{v:.2f}" for v in s))
    print(voce)
    for r in righe:
        print("   ", r)
    sys.stdout.flush()
