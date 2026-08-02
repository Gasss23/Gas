"""
win_wakeword_test.py — Windows only
Ascolta dal device scelto e stampa un timestamp a ogni wake-word detection.

Modello pretrained: "hey_jarvis" (incluso in openwakeword).
Puoi sostituire con "alexa", "hey_mycroft", ecc. — vedi openwakeword.utils.get_pretrained_model_paths().

Dipendenze (pip install):
    openwakeword sounddevice numpy

Uso:
    python win_wakeword_test.py                  # device default
    python win_wakeword_test.py --device 1       # device indice 1
    python win_wakeword_test.py --device 1 --model hey_jarvis  # modello esplicito
    python win_wakeword_test.py --threshold 0.5  # soglia detection (0-1, default 0.5)

Premi Ctrl+C per uscire.
"""

import argparse
import sys
import time
import datetime
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    print("[ERRORE] sounddevice non installato. pip install sounddevice")
    sys.exit(1)

try:
    from openwakeword.model import Model as OWWModel
    import openwakeword
except ImportError:
    print("[ERRORE] openwakeword non installato. pip install openwakeword")
    sys.exit(1)

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms @ 16kHz — stride raccomandato da openwakeword


def list_devices():
    print("\n=== Device audio disponibili ===")
    for i, d in enumerate(sd.query_devices()):
        tag = ""
        if d["max_input_channels"] > 0:
            tag += "[IN]"
        if d["max_output_channels"] > 0:
            tag += "[OUT]"
        print(f"  {i:2d}  {tag:<8} {d['name']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Wake-word detection con openwakeword")
    parser.add_argument("--device", type=int, default=None)
    parser.add_argument("--model", default="hey_jarvis", help="Nome modello pretrained")
    parser.add_argument("--threshold", type=float, default=0.5, help="Soglia detection (0-1)")
    args = parser.parse_args()

    list_devices()

    # Download modello pretrained se non cached
    print(f"[INFO] Carico modello: {args.model}")
    openwakeword.utils.download_models()
    model = OWWModel(wakeword_models=[args.model], inference_framework="onnx")

    if args.device is None:
        d_info = sd.query_devices(kind="input")
        print(f"[INFO] Device default input: {d_info['name']}")
    else:
        d_info = sd.query_devices(args.device)
        print(f"[INFO] Device scelto: {d_info['name']}")

    print(f"[INFO] Soglia: {args.threshold}")
    print("[INFO] In ascolto... premi Ctrl+C per uscire.\n")

    detection_count = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        device=args.device,
    ) as stream:
        while True:
            chunk, _ = stream.read(CHUNK_SIZE)
            audio_chunk = chunk.flatten().astype(np.int16)

            prediction = model.predict(audio_chunk)

            for ww, score in prediction.items():
                if score >= args.threshold:
                    detection_count += 1
                    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(f"[{ts}] DETECTION #{detection_count}  model={ww}  score={score:.3f}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Fermato dall'utente.")
