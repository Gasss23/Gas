import json, numpy as np, sys
k=int(sys.argv[1]) if len(sys.argv)>1 else 0
tr=np.load("tracce/A_chiamate.npz"); gt=json.load(open("flussi/A_chiamate.json"))
raw,prob=tr["raw"],tr["prob"][k]
sb=0.08
per={}
for c in gt["chiamate"]:
    i0,i1=int((c["inizio"]-0.1)/sb), int((c["fine"]+1.2)/sb)+1
    r=raw[i0:i1]; p=np.where(r>=0.25, prob[i0:i1], np.nan)
    mp=np.nanmax(p) if np.isfinite(p).any() else 0
    # blocchi di fila >=0.8
    run=best=0
    for v in p:
        run = run+1 if (np.isfinite(v) and v>=0.8) else 0; best=max(best,run)
    per.setdefault(c["distanza"],[]).append((r.max(),mp,best))
for d in ["vicino","-6dB","-12dB","-20dB"]:
    a=np.array(per[d])
    print(d,"raw max mediana %.2f | prob max (raw>=.25) mediana %.2f q25 %.2f q75 %.2f max %.2f | chiamate con 3 blocchi di fila >=0.8: %d/30 | con 1: %d/30"%(np.median(a[:,0]),np.median(a[:,1]),*np.percentile(a[:,1],[25,75]),a[:,1].max(),(a[:,2]>=3).sum(),(a[:,2]>=1).sum()))
for f in ["B_parlato","C_tv","D_altri"]:
    t=np.load(f"tracce/{f}.npz"); r=t["raw"]; p=t["prob"][k][r>=0.25]
    print(f,"blocchi raw>=.25: %d, prob mediana %.2f, >=0.5: %d, >=0.7: %d, max %.2f"%(len(p),np.median(p),(p>=.5).sum(),(p>=.7).sum(),p.max()))
