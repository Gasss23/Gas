import numpy as np, sys
from openwakeword.model import Model
import lib_sim as L
from sim_registra import voce_operatore
m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
def picco(x, off=0):
    m.reset()
    y = np.concatenate([L.rosa(2*L.FREQ+off, L.RMS_STANZA, 1), x, np.zeros(L.FREQ, np.float32)])
    y = y + L.rosa(len(y), L.RMS_STANZA, 2)
    return max(float(m.predict(b)["hey_jarvis"]) for b in L.blocchi(y))
rng=np.random.default_rng(5)
for d in L.DISTANZE:
    s=[]
    for k in range(30):
        s.append(picco(L.a_distanza(voce_operatore(rng), d, k)))
    s=np.array(s); print(d, "mediana %.2f q25 %.2f q75 %.2f  >=0.25 %.2f >=0.5 %.2f"%(np.median(s),*np.percentile(s,[25,75]),(s>=.25).mean(),(s>=.5).mean()))
# sensibilità alla fase della griglia da 80 ms
x=L.a_distanza(voce_operatore(np.random.default_rng(1),"ehi jarvis"),"vicino",0)
print("fase:", " ".join("%.2f"%picco(x,off) for off in range(0,1280,128)))
x=L.a_distanza(voce_operatore(np.random.default_rng(2),"ehi jarvis"),"vicino",0)
print("fase:", " ".join("%.2f"%picco(x,off) for off in range(0,1280,128)))
