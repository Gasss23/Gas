import sys, os
sys.path.insert(0, sys.argv[1]); os.environ["GAS_NO_DOTENV"]="1"
from scripts.voce import registra_voce as rv
from scipy.io import wavfile
from pathlib import Path
m=rv.MotoreOWW("hey_jarvis")
sotto=0; tot=0
for run in sys.argv[2:]:
    for p in sorted(Path(run).glob(".gas_voce/verifica/operatore/positivi/*.wav")):
        fr,d=wavfile.read(p); bl=[d[i:i+1280] for i in range(0,len(d)-1279,1280)]
        mis=m.misura(bl)[0]; tr=max(s for s,_ in m.blocchi(p,5,True))
        tot+=1; sotto += tr<0.25
        if tr<0.25: print(run, p.name[-7:], "misura %.2f addestra %.2f"%(mis,tr))
print("clip tenute dalla registrazione ma sotto 0,25 in addestra: %d/%d"%(sotto,tot))
