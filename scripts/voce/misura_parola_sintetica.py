#!/usr/bin/env python3
"""
scripts/voce/misura_parola_sintetica.py — la misura del 12/11/2026 (reports/
voce_taratura_2026-11-12.md), riproducibile (bot #378 V-2). NON fa parte dei test: serve
il modello vero e una voce sintetica.

Fa girare il modello `hey_jarvis` di openWakeWord (onnx, blocchi da 80 ms come
l'ascolto) su frasi lette da espeak-ng e stampa, per ogni regola (soglia × blocchi di
fila), quante chiamate vere scattano e quanti falsi su frasi comuni.

Serve: espeak-ng e ffmpeg nel PATH; `pip install openwakeword onnxruntime numpy` (su Linux
openwakeword 0.6 si installa con `--no-deps` perché chiede tflite-runtime); una volta
`python -c "import openwakeword.utils as u; u.download_models(['hey_jarvis_v0.1'])"`.

Uso: python3 scripts/voce/misura_parola_sintetica.py [--grezzi]   (--grezzi: una riga per prova)
Le voci sintetiche NON sono la voce dell'operatore: per quella c'è taratura_parola.py.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from typing import List, Tuple

CHIAMATE = ["hey jarvis", "hey jarvis, what time is it", "ehi jarvis"]
VOCI_CHIAMATE = ["en-us", "en-gb", "it"]
VELOCITA = [130, 170, 210]
CONDIZIONI = [(1.0, 0.0), (0.3, 0.0), (0.3, 300.0)]   # (volume, rumore gaussiano)
FRASI_IT = [
    "oggi fa freddo e devo andare a fare la spesa", "hai visto la partita di ieri sera",
    "domani ho una riunione con il cliente alle nove", "passami il caricabatterie per favore",
    "che ore sono adesso", "mi piace molto questa canzone", "stasera guardiamo un film",
    "giovanni ha chiamato prima", "ci vediamo dopo al bar", "il treno è in ritardo di dieci minuti",
    "jarvis è un nome strano per un assistente", "ehi giacomo vieni qui", "hai sentito marco",
    "harvey ha detto di sì", "ehi gervasio", "ehi jarno", "la jeep è nel garage",
    "service non disponibile", "hey davis come stai", "jack e jill", "ehi charlie",
    "garibaldi era un generale", "ehi gianni passa la palla", "hey jay vieni",
    "avvisami quando arrivi", "ascolta questa notizia del telegiornale",
    "previsioni del tempo per domani", "il presidente ha parlato in conferenza stampa",
    "e adesso la pubblicità", "grazie a tutti per l'attenzione"]
FRASI_EN = [
    "hey there how are you", "the service is not available", "have you seen harvey",
    "jar of jam", "hey travis", "hey jervis", "hey chavez", "a jar is on the table",
    "nervous system", "hey jarvis is a movie character", "hey jealous", "hey jasmine",
    "harvest season", "hey davis", "service charges apply"]
SOGLIE = (0.5, 0.6, 0.7)
BLOCCHI = (1, 2, 3)


def voce(testo: str, lingua: str, velocita: int):
    import numpy as np
    wav = subprocess.run(["espeak-ng", "-v", lingua, "-s", str(velocita), "-p", "50",
                          "--stdout", testo], capture_output=True, check=True).stdout
    grezzo = subprocess.run(["ffmpeg", "-loglevel", "quiet", "-i", "pipe:0", "-ar", "16000",
                             "-ac", "1", "-f", "s16le", "pipe:1"], input=wav,
                            capture_output=True, check=True).stdout
    return np.frombuffer(grezzo, dtype=np.int16)


def punteggi(audio, volume: float = 1.0, rumore: float = 0.0) -> List[float]:
    import numpy as np
    from openwakeword.model import Model
    m = Model(wakeword_models=["hey_jarvis_v0.1"], inference_framework="onnx")
    silenzio = np.zeros(16000 * 2, dtype=np.int16)
    a = np.concatenate([silenzio, (audio * volume).clip(-32768, 32767).astype(np.int16),
                        silenzio])
    if rumore:
        a = (a + np.random.default_rng(0).normal(0, rumore, len(a))).clip(
            -32768, 32767).astype(np.int16)
    out = []
    for i in range(0, len(a) - 1279, 1280):
        out.append(float(max(m.predict(a[i:i + 1280]).values())))
    return out


def di_fila(sc: List[float], soglia: float) -> int:
    meglio = corsa = 0
    for p in sc:
        corsa = corsa + 1 if p >= soglia else 0
        meglio = max(meglio, corsa)
    return meglio


def conta(prove: List[Tuple[str, List[float]]]) -> List[str]:
    righe = []
    for t in SOGLIE:
        for b in BLOCCHI:
            n = sum(1 for _, sc in prove if di_fila(sc, t) >= b)
            righe.append("  soglia %.1f · %d blocc%s: %d/%d" % (t, b, "o" if b == 1 else "hi",
                                                               n, len(prove)))
    return righe


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--grezzi", action="store_true")
    args = ap.parse_args(argv)
    chiamate = []
    for testo in CHIAMATE:
        for lingua in VOCI_CHIAMATE:
            for vel in VELOCITA:
                a = voce(testo, lingua, vel)
                for vol, rum in CONDIZIONI:
                    chiamate.append(("%s|%s|%d|%g|%g" % (testo, lingua, vel, vol, rum),
                                     punteggi(a, vol, rum)))
    falsi = []
    for frasi, lingue in ((FRASI_IT, ["it"]), (FRASI_EN, ["en-us", "en-gb"])):
        for testo in frasi:
            for lingua in lingue:
                for vel in (150, 190):
                    falsi.append(("%s|%s|%d" % (testo, lingua, vel),
                                  punteggi(voce(testo, lingua, vel))))
    if args.grezzi:
        for nome, sc in chiamate + falsi:
            print("%s|max %.2f|%s" % (nome, max(sc), " ".join(
                "%.1f:%d" % (t, di_fila(sc, t)) for t in SOGLIE)))
    print("Chiamate vere che scattano:")
    print("\n".join(conta(chiamate)))
    print("Falsi su frasi comuni:")
    print("\n".join(conta(falsi)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
