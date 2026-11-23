import os, sys
import numpy as np
from multiprocessing import Pool
FLUSSI = ["A_chiamate", "B_parlato", "C_tv", "D_altri"]
def una(cfg):
    N, ver, s, b = cfg
    os.environ["TRACCE"] = f"tracce_f{N}_{'ver' if ver else 'nover'}"
    from sim_ascolto import esegui
    tot = {}
    for k in ([0, 1, 2] if ver else [None]):
        for f in FLUSSI:
            r = esegui(f, soglia=s, blocchi_parola=b, k=k, base=0.25)
            t = tot.setdefault(f, {"pd": {}, "falsi": 0, "ore": 0, "lat": []})
            for d, (n, ok) in r["per_distanza"].items():
                a = t["pd"].get(d, [0, 0]); t["pd"][d] = [a[0] + n, a[1] + ok]
            t["falsi"] += r["falsi"]; t["ore"] += r["durata_min"] / 60
            if r["latenza_med"] is not None: t["lat"].append(r["latenza_med"])
    return cfg, tot
cfgs = [(N, v, s, 1) for v in (False, True) for N in (1, 2, 4)
        for s in ((0.5, 0.7) if not v else (0.5, 0.6, 0.7))]
with Pool(4) as p:
    for (N, v, s, b), t in p.imap(una, cfgs):
        a = t["A_chiamate"]["pd"]
        pd = " ".join("%s %3d%%" % (d, round(100 * a[d][1] / a[d][0])) for d in ["vicino", "-6dB", "-12dB", "-20dB"])
        d = t["D_altri"]["pd"]["vicino"]
        print("fasi %d %-5s soglia %.2f blocchi %d | %s | FP/h parlato %5.1f TV %5.1f | altre voci %3d%% | lat %.2f"
              % (N, "VER" if v else "noVER", s, b, pd, t["B_parlato"]["falsi"] / t["B_parlato"]["ore"],
                 t["C_tv"]["falsi"] / t["C_tv"]["ore"], round(100 * d[1] / d[0]), np.mean(t["A_chiamate"]["lat"])), flush=True)
