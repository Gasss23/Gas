"""Varianti dell'addestramento del verificatore sulle STESSE clip salvate dal vero
registra_voce (runs/rN/.gas_voce/verifica). Salva varianti/rN_<nome>.pkl.
  orig   : come registra_voce.addestra (LR C=0.001, tutti i blocchi negativi, base 0.25)
  bil    : C=0.01, class_weight=balanced
  duri   : bil + i negativi «duri» (grezzo >= 0.05) pesano 20 volte
  aug    : duri + positivi aumentati a distanza (-6/-12 dB con riverbero) dalle clip vicine
  aug15  : aug con soglia base 0.15 anche nell'addestramento"""
import os
import pickle
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI.parent / "sim"))
sys.path.insert(0, str(QUI))
os.environ["GAS_NO_DOTENV"] = "1"
from openwakeword.custom_verifier_model import flatten_features  # noqa: E402
from scripts.voce import registra_voce as rv  # noqa: E402
import lib_sim as L  # noqa: E402

(QUI / "varianti").mkdir(exist_ok=True)


def pipe(C, cw):
    return make_pipeline(FunctionTransformer(flatten_features), StandardScaler(),
                         LogisticRegression(random_state=0, max_iter=3000, C=C,
                                            class_weight=cw))


def feats(mot, p, rip, imb):
    return mot.blocchi(p, rip, imb)


def aug_clip(p, dist, seme):
    fr, d = wavfile.read(str(p))
    y = L.a_distanza(d.astype(np.float32), dist, seme)
    y = y + L.rosa(len(y), L.RMS_STANZA, seme + 7)
    q = QUI / "varianti" / ("tmp_aug_%d.wav" % os.getpid())
    wavfile.write(str(q), 16000, L.a_int16(y))
    return q


def main(run):
    radice = QUI / "runs" / run
    mot = rv.MotoreOWW("hey_jarvis")
    pos = rv.clip(radice, "positivi")
    neg = rv.clip(radice, "negativi")
    P = [feats(mot, p, 5, True) for p in pos]
    PA = []
    for k, p in enumerate(pos):
        for dist in ("-6dB", "-12dB"):
            PA.append(feats(mot, aug_clip(p, dist, k), 5, True))
    N = [(feats(mot, p, 1, rv._di_altre_voci(p))) for p in neg]
    nf = [f for c in N for _, f in c]
    ns = np.array([s for c in N for s, _ in c])

    def fit(nome, base, C, cw, peso_duri=1.0, aug=False):
        pf = [f for c in P for s, f in c if s >= base]
        if aug:
            pf += [f for c in PA for s, f in c if s >= base]
        x = np.vstack(pf + nf)
        y = np.array([1] * len(pf) + [0] * len(nf))
        w = np.concatenate([np.ones(len(pf)), np.where(ns >= 0.05, peso_duri, 1.0)])
        m = pipe(C, cw)
        m.fit(x, y, logisticregression__sample_weight=w)
        pickle.dump(m, open(QUI / "varianti" / f"{run}_{nome}.pkl", "wb"))
        print(run, nome, "pos", len(pf), "neg", len(nf), "duri", int((ns >= 0.05).sum()))

    if os.environ.get("SET3"):
        fit("o15", 0.15, 0.001, None)
        fit("o15aug", 0.15, 0.001, None, 1.0, True)
        return
    if os.environ.get("SET2"):
        fit("orig", 0.25, 0.001, None)
        fit("oduri", 0.25, 0.001, None, 20.0)
        fit("obal", 0.25, 0.001, "balanced")
        fit("oaug", 0.25, 0.001, None, 1.0, True)
        return
    fit("orig", 0.25, 0.001, None)
    fit("bil", 0.25, 0.01, "balanced")
    fit("duri", 0.25, 0.01, "balanced", 20.0)
    fit("aug", 0.25, 0.01, "balanced", 20.0, True)
    fit("aug15", 0.15, 0.01, "balanced", 20.0, True)


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
