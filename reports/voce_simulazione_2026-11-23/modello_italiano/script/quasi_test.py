"""Quasi-omofoni MAI visti in addestramento («ehi gioele», «ehi jenny», «ehi garvis»…) e
quelli della simulazione del 23/11 («ehi gianni», «hey jervis»…), detti da voci tenute da
parte (espeak it+m3, piper riccardo, 2 parlanti libritts di valutazione), vicino al Mac.
Per confronto le stesse voci dicono «ehi jarvis». Punteggio = massimo sul flusso, 4 sfasamenti.

Uso: python quasi_test.py <dati> <modello>...  (stampa la frazione di frasi sopra soglia)"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import genera as G  # noqa: E402
import lib_sim as L  # noqa: E402
import testi as T  # noqa: E402
from openwakeword.model import Model  # noqa: E402


def clip(testo: str, voce: str, r: random.Random) -> np.ndarray:
    if voce.startswith("it+"):
        return G.espeak_clip(voce, testo, r)
    nome, sp = voce.split("|")
    return G.piper_clip(nome, None if sp == "None" else int(sp), G.fonemizza_it(testo), r)


def main():
    G._DATI = str(Path(sys.argv[1]).resolve())
    modelli = sys.argv[2:]
    voci = ["it+m3", "it_IT-riccardo-x_low|None", "en_US-libritts_r-medium|812",
            "en_US-libritts_r-medium|877"]
    gruppi = {"positivi «ehi jarvis»": ["ehi jarvis", "ehi giarvis", "hei giàrvis", "hey jarvis"],
              "quasi-omofoni nuovi": [q for q in T.QUASI_VALUTAZIONE if "jarvis" not in q],
              "frasi con «jarvis» dentro": [q for q in T.QUASI_VALUTAZIONE if "jarvis" in q],
              "quasi-omofoni simulazione": L.QUASI_OMOFONI}
    r = random.Random(3)
    def flusso(t, v):   # 1 s di silenzio, la frase a livello «vicino», 1 s; rumore di stanza
        x = np.concatenate([np.zeros(16000), L.normalizza(clip(t, v, r).astype(np.float32)),
                            np.zeros(16000)])
        return L.a_int16(x + L.rosa(len(x), L.RMS_STANZA, 7))
    audio = {g: [flusso(t, v) for t in testi for v in voci] for g, testi in gruppi.items()}
    for mod in modelli:
        m = Model(wakeword_models=[mod], inference_framework="onnx")
        print(f"## {Path(mod).stem}")
        for g, clips in audio.items():
            best = []
            for x in clips:
                s = 0.0
                for off in (0, 320, 640, 960):
                    m.reset()
                    y = x[off:]
                    s = max(s, max(max(m.predict(y[i:i + 1280]).values())
                                   for i in range(0, len(y) - 1279, 1280)))
                best.append(s)
            best = np.array(best)
            print("  %-28s n=%3d  ≥0.5: %3d%%  ≥0.7: %3d%%  ≥0.9: %3d%%" % (
                g, len(best), round(100 * (best >= .5).mean()), round(100 * (best >= .7).mean()),
                round(100 * (best >= .9).mean())), flush=True)


if __name__ == "__main__":
    main()
