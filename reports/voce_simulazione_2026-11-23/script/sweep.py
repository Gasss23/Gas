"""Griglia di regolazioni sul VERO ciclo dell'ascolto (punteggi da traccia, validati
identici al rilevatore vero). Uso: python sweep.py [k1 k2 ...] (indici dei verificatori
nelle tracce; default 0 1 2)."""
import itertools
import sys
from multiprocessing import Pool

from sim_ascolto import esegui

FLUSSI = ["A_chiamate", "B_parlato", "C_tv", "D_altri"]


def una(cfg):
    k, base, soglia, blocchi = cfg
    out = {}
    for f in FLUSSI:
        out[f] = esegui(f, soglia=soglia, blocchi_parola=blocchi, k=k, base=base)
    return cfg, out


def riga(cfg, out):
    k, base, soglia, blocchi = cfg
    a = out["A_chiamate"]["per_distanza"]
    pd = " ".join("%s %2d/30" % (d, a[d][1]) for d in ["vicino", "-6dB", "-12dB", "-20dB"])
    fp_b = out["B_parlato"]["falsi_ora"]
    fp_c = out["C_tv"]["falsi_ora"]
    d = out["D_altri"]["per_distanza"]["vicino"]
    fa = out["A_chiamate"]["falsi"]
    lat = out["A_chiamate"]["latenza_med"]
    return ("%-6s base %.2f soglia %.2f blocchi %d | %s | FP/h parlato %5.1f TV %5.1f "
            "(+%d in A) | altre voci prese %2d/40 | lat %.2f s"
            % ("noVER" if k is None else "ver%d" % k, base, soglia, blocchi, pd, fp_b, fp_c,
               fa, d[1], lat if lat is not None else -1))


if __name__ == "__main__":
    ks = [int(x) for x in sys.argv[1:]] or [0, 1, 2]
    cfgs = [(None, 0.25, s, b) for s in (0.3, 0.35, 0.4, 0.5, 0.6, 0.7) for b in (1, 2)]
    cfgs += [(k, base, s, b) for k in ks for base in (0.15, 0.25) for s in (0.5, 0.7, 0.9)
             for b in (1, 2)]
    with Pool(4) as p:
        for cfg, out in p.imap(una, cfgs):
            print(riga(cfg, out), flush=True)
