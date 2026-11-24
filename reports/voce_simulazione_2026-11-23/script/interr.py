import json, numpy as np
from itertools import groupby
def runs(s, t):
    best=run=0
    for v in s:
        run = run+1 if v>=t else 0; best=max(best,run)
    return best
for flusso in ["E_sopra_gas","A_chiamate"]:
    tr=np.load(f"tracce/{flusso}.npz"); gt=json.load(open(f"flussi/{flusso}.json"))
    raw=tr["raw"]
    for nome,ks in [("noVER",[None]),("orig",[0,5,10])]:
        for t in (0.5,0.6,0.7,0.8):
            for b in (1,2,3):
                ok=fp=0; tot=0
                for k in ks:
                    s = raw if k is None else np.where(raw>=0.25, tr["prob"][k], raw)
                    mask=np.zeros(len(s),bool)
                    for c in gt["chiamate"]:
                        if c["distanza"] not in ("vicino","-6dB"): continue
                        i0,i1=int((c["inizio"]-0.1)/0.08),int((c["fine"]+1.2)/0.08)+1
                        tot+=1; ok += runs(s[i0:i1],t)>=b
                    for c in gt["chiamate"]:
                        i0,i1=int((c["inizio"]-0.1)/0.08),int((c["fine"]+1.2)/0.08)+1; mask[i0:i1]=True
                    # falsi: inneschi fuori dalle chiamate (voce di Gas da sola), contati per corsa
                    ss=np.where(mask,0,s); run=0
                    for v in ss:
                        run = run+1 if v>=t else 0
                        if run==b: fp+=1
                ore=len(raw)*0.08/3600*len(ks)
                print(flusso, nome, "soglia int %.1f blocchi %d: prese %d/%d (%.0f%%), auto-interruzioni/ora %.1f"%(t,b,ok,tot,100*ok/tot,fp/ore))
