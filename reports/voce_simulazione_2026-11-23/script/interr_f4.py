"""Interruzione con la configurazione predefinita della PR #400: filtro della voce attivo,
4 fasi col massimo (tracce_f4_ver, da traccia_fasi.py). Prese = chiamate vicino/-6 dB in cui
la soglia è superata per b blocchi di fila; auto-interruzioni = scatti sulla voce di Gas
fuori dalle chiamate (flusso E: Gas parla di continuo). Uso: python interr_f4.py"""
import json
import numpy as np


def runs(s, t):
    best = run = 0
    for v in s:
        run = run + 1 if v >= t else 0
        best = max(best, run)
    return best


for flusso in ["E_sopra_gas", "A_chiamate"]:
    tr = np.load(f"tracce_f4_ver/{flusso}.npz")
    gt = json.load(open(f"flussi/{flusso}.json"))
    prob = tr["prob"]
    for t, b in [(0.5, 1), (0.6, 1), (0.8, 3), (0.5, 2), (0.5, 3)]:
        ok = fp = tot = 0
        for k in range(prob.shape[0]):
            s = prob[k]
            mask = np.zeros(len(s), bool)
            for c in gt["chiamate"]:
                i0, i1 = int((c["inizio"] - 0.1) / 0.08), int((c["fine"] + 1.2) / 0.08) + 1
                mask[i0:i1] = True
                if c["distanza"] not in ("vicino", "-6dB"):
                    continue
                tot += 1
                ok += runs(s[i0:i1], t) >= b
            ss = np.where(mask, 0, s)
            run = 0
            for v in ss:
                run = run + 1 if v >= t else 0
                if run == b:
                    fp += 1
        ore = prob.shape[1] * 0.08 / 3600 * prob.shape[0]
        print("%s 4 fasi + filtro, soglia %.1f su %d blocchi: prese %d/%d (%.0f%%), "
              "scatti fuori dalle chiamate/ora %.1f" % (flusso, t, b, ok, tot,
                                                        100 * ok / max(tot, 1), fp / ore))
