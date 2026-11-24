import numpy as np, itertools
from openwakeword.model import Model
import lib_sim as L
m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
def picco(x):
    m.reset()
    y = np.concatenate([L.rosa(2*L.FREQ, L.RMS_STANZA, 1), x, np.zeros(L.FREQ, np.float32)])
    y = y + L.rosa(len(y), L.RMS_STANZA, 2)
    return max(float(m.predict(b)["hey_jarvis"]) for b in L.blocchi(y))
for voce in ["it+m3","it","it+m5"]:
  for testo in ["hey jarvis","ehi jarvis"]:
    s=[]
    for vel in (160,170,180,190):
      for pit in (40,48,55,62):
        s.append(picco(L.normalizza(L.tts(testo,voce,vel,pit))))
    s=np.array(s); print(voce,testo,"vicino: mediana %.2f  q25 %.2f q75 %.2f  frac>=0.5 %.2f"%(np.median(s),*np.percentile(s,[25,75]),(s>=.5).mean()))
