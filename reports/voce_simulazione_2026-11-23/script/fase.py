import sys, os, numpy as np
sys.path.insert(0,"../sim"); os.environ["GAS_NO_DOTENV"]="1"
from scripts.voce import registra_voce as rv
from scipy.io import wavfile
from pathlib import Path
m=rv.MotoreOWW("hey_jarvis")
for p in sorted(Path(sys.argv[1]).glob("*.wav")):
    fr,d=wavfile.read(p)
    bl=[d[i:i+1280] for i in range(0,len(d)-1279,1280)]
    mis=m.misura(bl)[0]
    tr=max(s for s,_ in m.blocchi(p,5,True))
    fasi=[]
    for off in range(0,1280,160):
        m.oww.reset(); x=np.concatenate([np.zeros(16000+off,np.int16),d,np.zeros(8000,np.int16)])
        fasi.append(max(float(m.oww.predict(x[i:i+1280])["hey_jarvis"]) for i in range(0,len(x)-1279,1280)))
    print(p.name[-7:], "misura %.2f  addestra(5 rip) %.2f  fasi min %.2f max %.2f"%(mis,tr,min(fasi),max(fasi)))
