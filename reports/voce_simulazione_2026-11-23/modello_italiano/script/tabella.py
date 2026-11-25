"""Tabella dai risultati di valuta.py griglia (uno o più file .json)."""
import json, sys
DIST = ["vicino", "-6dB", "-12dB", "-20dB"]
for f in sys.argv[1:]:
    r = json.load(open(f))
    ris = r["ris"]
    soglie = sorted({float(k.split("|")[1]) for k in ris})
    print(f"## {r['tag']} — {r['fasi']} fase/i")
    print("soglia | A (sim, it+m3): " + " ".join(DIST) + " | G (voci nuove): " + " ".join(DIST)
          + " | D altre voci | FP/h B parlato | FP/h C TV | FP/h H parlato vero")
    for s in soglie:
        def pd(fl):
            x = ris.get(f"{fl}|{s}")
            if not x:
                return "-"
            return " ".join("%3d%%" % round(100 * x["per_distanza"][d][1] / x["per_distanza"][d][0])
                            for d in DIST if d in x["per_distanza"])
        def fp(fl):
            x = ris.get(f"{fl}|{s}")
            return "-" if not x else "%.1f" % (x["falsi"] / x["ore"])
        d = ris.get(f"D_altri|{s}")
        dd = "-" if not d else "%d%%" % round(100 * d["per_distanza"]["vicino"][1] / d["per_distanza"]["vicino"][0])
        print(f"{s:.2f} | {pd('A_chiamate')} | {pd('G_chiamate_nuove')} | {dd} | {fp('B_parlato')} | {fp('C_tv')} | {fp('H_parlato_vero')}")
    print()
