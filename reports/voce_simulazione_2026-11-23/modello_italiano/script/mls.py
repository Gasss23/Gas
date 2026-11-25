"""Decodifica l'audio di parquet di Hugging Face (MLS italiano: opus; AMI: wav) in un unico
array 16 kHz int16. Uso: python mls.py <uscita.npy> <max_frasi> <parquet...>"""
import subprocess, sys
from multiprocessing import Pool
import numpy as np
import pyarrow.parquet as pq

def dec(b):
    r = subprocess.run(["ffmpeg", "-loglevel", "quiet", "-i", "pipe:0", "-ar", "16000", "-ac", "1",
                        "-f", "s16le", "pipe:1"], input=b, capture_output=True)
    return np.frombuffer(r.stdout, np.int16)

def main():
    dst, nmax, srcs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    audio, testi, parl = [], [], set()
    for src in srcs:
        t = pq.read_table(src)
        col_t = "transcript" if "transcript" in t.column_names else "text"
        audio += [a["bytes"] for a in t.column("audio").to_pylist()]
        testi += t.column(col_t).to_pylist()
        parl |= set(t.column("speaker_id").to_pylist())
    audio = audio[:nmax]
    assert not any("jarvis" in s.lower() for s in testi[:nmax])
    with Pool(2) as p:
        pezzi = p.map(dec, audio, chunksize=20)
    x = np.concatenate(pezzi)
    np.save(dst, x)
    print(dst, "%.2f ore" % (len(x) / 16000 / 3600), "parlanti", len(parl))

main()
