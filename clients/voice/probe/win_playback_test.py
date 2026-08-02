"""
win_playback_test.py — Windows only
Riproduce un file WAV o MP3 sul device di output scelto.

Dipendenze (pip install):
    sounddevice numpy scipy
    # per MP3: pip install pydub    (richiede ffmpeg in PATH)

Uso:
    python win_playback_test.py audio.wav
    python win_playback_test.py audio.mp3 --device 3
    python win_playback_test.py --list            # solo lista device
"""

import argparse
import sys
import numpy as np

try:
    import sounddevice as sd
    from scipy.io.wavfile import read as wav_read
except ImportError as e:
    print(f"[ERRORE] Dipendenza mancante: {e}")
    print("Installa con:  pip install sounddevice numpy scipy")
    sys.exit(1)


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


def load_audio(path: str):
    """Carica WAV (nativo) o MP3 (tramite pydub se disponibile)."""
    if path.lower().endswith(".mp3"):
        try:
            from pydub import AudioSegment
        except ImportError:
            print("[ERRORE] pydub non installato. pip install pydub  (+ ffmpeg in PATH per MP3)")
            sys.exit(1)
        audio = AudioSegment.from_mp3(path).set_channels(1).set_frame_rate(16000)
        samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
        return 16000, samples
    else:
        return wav_read(path)


def main():
    parser = argparse.ArgumentParser(description="Riproduce un WAV/MP3 sul device scelto")
    parser.add_argument("file", nargs="?", help="File audio da riprodurre")
    parser.add_argument("--device", type=int, default=None, help="Indice device output")
    parser.add_argument("--list", action="store_true", help="Solo lista device")
    args = parser.parse_args()

    list_devices()

    if args.list or not args.file:
        if not args.list:
            print("[ERRORE] Specifica un file audio. Esempio: python win_playback_test.py audio.wav")
        sys.exit(0)

    print(f"[INFO] Carico: {args.file}")
    sample_rate, data = load_audio(args.file)

    if data.ndim == 1:
        channels = 1
    else:
        channels = data.shape[1]

    if args.device is None:
        d_info = sd.query_devices(kind="output")
        print(f"[INFO] Device default output: {d_info['name']}")
    else:
        d_info = sd.query_devices(args.device)
        print(f"[INFO] Device scelto: {d_info['name']}")

    duration = len(data) / sample_rate
    print(f"[INFO] Riproduco {duration:.2f}s @ {sample_rate}Hz, {channels}ch ...")

    sd.play(data, samplerate=sample_rate, device=args.device)
    sd.wait()

    print("[INFO] Riproduzione completata.")


if __name__ == "__main__":
    main()
