"""Punteggio massimo di un modello su ogni frase dei flussi della simulazione (espeak it+m3 e
altre voci), per capire QUALI frasi fanno scattare i falsi. Uso: python frasi_test.py <modello>..."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_sim as L
from openwakeword.model import Model
voci = [("it+m3", 50), ("it+f2", 60), ("en-us+f1", 60), ("it+m1", 50)]
frasi = [("Q", f) for f in L.QUASI_OMOFONI] + [("I", f) for f in L.FRASI_IT] + [("T", f) for f in L.FRASI_TV]
ris = {}
for mod in sys.argv[1:]:
    m = Model(wakeword_models=[mod], inference_framework="onnx")
    for tipo, f in frasi:
        best = 0
        for v, p in voci:
            for fase in (0, 640):
                x = L.a_int16(np.concatenate([np.zeros(16000 + fase), L.normalizza(L.tts(f, v, 165, p)), np.zeros(16000)]))
                m.reset()
                s = max(max(m.predict(x[i:i + 1280]).values()) for i in range(0, len(x) - 1279, 1280))
                best = max(best, s)
        ris.setdefault((tipo, f), []).append(best)
for (tipo, f), v in sorted(ris.items(), key=lambda kv: -max(kv[1])):
    if max(v) >= 0.3:
        print(tipo, " ".join("%.2f" % s for s in v), f)
