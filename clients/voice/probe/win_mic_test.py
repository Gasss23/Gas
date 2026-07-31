"""
win_mic_test.py — Windows only
Registra 3 secondi dal device scelto, salva un WAV, stampa durata + RMS.

Dipendenze (pip install):
    sounddevice numpy scipy

Uso:
    python win_mic_test.py                    # lista device, poi usa default
    python win_mic_test.py --device 1         # usa device indice 1
    python win_mic_test.py --device 1 --out rec.wav  # output personalizzato
"""

import argparse
import sys
import wave
import numpy as np

try:
    import sounddevice as sd
    from scipy.io.wavfile import write as wav_write
except ImportError as e:
    print(f"[ERRORE] Dipendenza mancante: {e}")
    print("Installa con:  pip install sounddevice numpy scipy")
    sys.exit(1)

DURATION = 3
SAMPLE_RATE = 16000


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


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(samples.astype(np.float64) ** 2)))


def main():
    parser = argparse.ArgumentParser(description="Registra 3s dal mic e misura RMS")
    parser.add_argument("--device", type=int, default=None, help="Indice device (vedi lista)")
    parser.add_argument("--out", default="mic_test.wav", help="Path WAV output (default: mic_test.wav)")
    args = parser.parse_args()

    list_devices()

    if args.device is None:
        d_info = sd.query_devices(kind="input")
        print(f"[INFO] Device default input: {d_info['name']}")
    else:
        d_info = sd.query_devices(args.device)
        print(f"[INFO] Device scelto: {d_info['name']}")

    print(f"[INFO] Registrazione {DURATION}s @ {SAMPLE_RATE}Hz ... parla!")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=args.device,
    )
    sd.wait()
    print("[INFO] Registrazione completata.")

    wav_write(args.out, SAMPLE_RATE, audio)

    samples = audio.flatten()
    duration_actual = len(samples) / SAMPLE_RATE
    rms_val = rms(samples)

    print(f"\n=== RISULTATO ===")
    print(f"  File       : {args.out}")
    print(f"  Durata     : {duration_actual:.2f}s")
    print(f"  RMS        : {rms_val:.1f}  (silenzio ~0-50, voce ~200-3000)")
    if rms_val < 50:
        print("  Diagnosi   : segnale basso — controlla il mic o il device")
    else:
        print("  Diagnosi   : segnale OK")


if __name__ == "__main__":
    main()
