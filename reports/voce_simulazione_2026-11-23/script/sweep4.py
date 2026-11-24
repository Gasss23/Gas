"""Varianti del verificatore × regolazioni, sul VERO ciclo dell'ascolto (tracce), sommate
sui 3 operatori-registrazioni simulati (r0 r1 r2). Stampa anche quante chiamate potrebbero
INTERROMPERE Gas (3 blocchi di fila >= soglia interruzione 0,8, il valore di main)."""
import json
import sys
from multiprocessing import Pool

import numpy as np

from sim_ascolto import esegui

FLUSSI = ["A_chiamate", "B_parlato", "C_tv", "D_altri"]
NOMI = ["o15", "o15aug"]


def k_di(run, nome):
    return run * len(NOMI) + NOMI.index(nome)


def interrompe(k, base, soglia_int=0.8, blocchi=3):
    tr = np.load("tracce3/A_chiamate.npz")
    gt = json.load(open("flussi/A_chiamate.json"))
    raw, prob = tr["raw"], tr["prob"][k]
    s = np.where(raw >= base, prob, raw)
    n = 0
    for c in gt["chiamate"]:
        if c["distanza"] not in ("vicino", "-6dB"):
            continue
        i0, i1 = int((c["inizio"] - 0.1) / 0.08), int((c["fine"] + 1.2) / 0.08) + 1
        run = best = 0
        for v in s[i0:i1]:
            run = run + 1 if v >= soglia_int else 0
            best = max(best, run)
        n += best >= blocchi
    return n


def una(cfg):
    nome, base, soglia, blocchi = cfg
    tot = {}
    for run in range(3):
        k = None if nome == "noVER" else k_di(run, nome)
        for f in FLUSSI:
            r = esegui(f, soglia=soglia, blocchi_parola=blocchi, k=k, base=base)
            t = tot.setdefault(f, {"pd": {}, "falsi": 0, "ore": 0, "lat": []})
            for d, (n, ok) in r["per_distanza"].items():
                a = t["pd"].get(d, [0, 0])
                t["pd"][d] = [a[0] + n, a[1] + ok]
            t["falsi"] += r["falsi"]
            t["ore"] += r["durata_min"] / 60
            if r["latenza_med"] is not None:
                t["lat"].append(r["latenza_med"])
        if nome == "noVER":
            break
    intr = (0 if nome == "noVER" else
            sum(interrompe(k_di(r, nome), base) for r in range(3)))
    return cfg, tot, intr


if __name__ == "__main__":
    cfgs = []
    for s in (0.5, 0.7):
        for b in (1, 2):
            cfgs.append(("noVER", 0.25, s, b))
    for nome in NOMI:
        for base in (0.15,):
            for s in (0.4, 0.5, 0.6, 0.7):
                for b in (1, 2):
                    cfgs.append((nome, base, s, b))
    with Pool(4) as p:
        for (nome, base, s, b), t, intr in p.imap(una, cfgs):
            a = t["A_chiamate"]["pd"]
            pd = " ".join("%s %3d%%" % (d, round(100 * a[d][1] / a[d][0]))
                          for d in ["vicino", "-6dB", "-12dB", "-20dB"])
            fb = t["B_parlato"]["falsi"] / t["B_parlato"]["ore"]
            fc = t["C_tv"]["falsi"] / t["C_tv"]["ore"]
            d = t["D_altri"]["pd"]["vicino"]
            lat = np.mean(t["A_chiamate"]["lat"])
            nint = 60 if nome != "noVER" else 0
            print("%-6s base %.2f soglia %.2f blocchi %d | %s | FP/h parlato %5.1f TV %5.1f | "
                  "altre voci %3d%% | lat %.2f s | interrompe %s"
                  % (nome, base, s, b, pd, fb, fc, round(100 * d[1] / d[0]), lat,
                     "%d/%d" % (intr, 3 * nint) if nint else "-"), flush=True)
