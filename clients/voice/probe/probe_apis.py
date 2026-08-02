"""
probe_apis.py — WSL / Linux
Sonda le API Groq Whisper + ElevenLabs Flash senza toccare il motore GAS.

Legge le chiavi dal .env nella root del progetto (o da variabili d'ambiente).
Richiede: GROQ_API_KEY, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

Uso:
    python probe_apis.py                                # usa il WAV di test incluso
    python probe_apis.py --wav mia_voce.wav             # WAV personalizzato
    python probe_apis.py --text "Ciao, sono Gas."       # testo TTS personalizzato
    python probe_apis.py --only stt                     # solo Whisper
    python probe_apis.py --only tts                     # solo ElevenLabs

Output: stampa STATUS per ogni API; salva mp3 TTS in probe_tts_output.mp3
"""

import argparse
import os
import sys
import struct
import math
import pathlib

# ---------- carica .env dalla root del progetto ----------
_ROOT = pathlib.Path(__file__).parent.parent.parent.parent  # Gas/
_ENV = _ROOT / ".env"
if _ENV.exists():
    for line in _ENV.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

try:
    import requests
except ImportError:
    print("[ERRORE] requests non installato. pip install requests")
    sys.exit(1)

# ---------- WAV sintetico di test (440Hz, 2s, 16kHz) ----------
def _make_test_wav(path: str, freq: float = 440.0, duration: float = 2.0, sr: int = 16000):
    """Genera un WAV sinusoidale minimale (non silenzioso, non parole)."""
    n_samples = int(sr * duration)
    samples = [int(32767 * math.sin(2 * math.pi * freq * i / sr)) for i in range(n_samples)]
    with open(path, "wb") as f:
        # WAV header
        data_size = n_samples * 2
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(struct.pack(f"<{n_samples}h", *samples))


# ---------- probe STT (Groq Whisper) ----------
def probe_stt(wav_path: str) -> dict:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return {"status": "PREREQUISITO_UMANO", "msg": "GROQ_API_KEY non trovata nel .env"}

    print(f"[STT] Invio {wav_path} a Groq Whisper large-v3-turbo ...")
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {key}"}
    try:
        with open(wav_path, "rb") as f:
            files = {"file": (os.path.basename(wav_path), f, "audio/wav")}
            data = {"model": "whisper-large-v3-turbo", "language": "it", "response_format": "json"}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        if resp.status_code == 200:
            text = resp.json().get("text", "")
            return {"status": "OK", "http": resp.status_code, "text": text or "(silenzio/nessun parlato rilevato)"}
        else:
            return {"status": "ERRORE_API", "http": resp.status_code, "body": resp.text[:300]}
    except Exception as e:
        return {"status": "ERRORE", "msg": str(e)}


# ---------- probe TTS (ElevenLabs Flash) ----------
def probe_tts(text: str, out_path: str) -> dict:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    if not key:
        return {"status": "PREREQUISITO_UMANO", "msg": "ELEVENLABS_API_KEY non trovata nel .env"}
    if not voice_id:
        return {"status": "PREREQUISITO_UMANO", "msg": "ELEVENLABS_VOICE_ID non trovata nel .env"}

    print(f"[TTS] Richiedo sintesi a ElevenLabs Flash (voice_id={voice_id}) ...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_flash_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(resp.content)
            size_kb = len(resp.content) / 1024
            return {"status": "OK", "http": resp.status_code, "file": out_path, "size_kb": round(size_kb, 1)}
        else:
            return {"status": "ERRORE_API", "http": resp.status_code, "body": resp.text[:300]}
    except Exception as e:
        return {"status": "ERRORE", "msg": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Sonda Groq Whisper + ElevenLabs Flash")
    parser.add_argument("--wav", default=None, help="WAV da trascrivere (default: WAV sintetico di test)")
    parser.add_argument("--text", default="Ciao, sono Gas, il tuo assistente vocale.", help="Testo da sintetizzare")
    parser.add_argument("--only", choices=["stt", "tts"], default=None, help="Esegui solo una delle due sonde")
    parser.add_argument("--out", default="probe_tts_output.mp3", help="File MP3 output TTS")
    args = parser.parse_args()

    results = {}

    # --- STT ---
    if args.only in (None, "stt"):
        wav = args.wav
        if wav is None:
            wav = "/tmp/probe_test_tone.wav"
            print(f"[INFO] Genero WAV sintetico di test: {wav}")
            _make_test_wav(wav)
        result = probe_stt(wav)
        results["stt"] = result
        status = result["status"]
        if status == "OK":
            print(f"[STT] STATUS=OK  HTTP={result['http']}")
            print(f"[STT] Testo: {result['text']}")
        elif status == "PREREQUISITO_UMANO":
            print(f"[STT] STATUS=PREREQUISITO_UMANO — {result['msg']}")
        else:
            print(f"[STT] STATUS={status}  {result.get('msg', result.get('body', ''))}")

    print()

    # --- TTS ---
    if args.only in (None, "tts"):
        result = probe_tts(args.text, args.out)
        results["tts"] = result
        status = result["status"]
        if status == "OK":
            print(f"[TTS] STATUS=OK  HTTP={result['http']}  file={result['file']}  size={result['size_kb']}KB")
        elif status == "PREREQUISITO_UMANO":
            print(f"[TTS] STATUS=PREREQUISITO_UMANO — {result['msg']}")
        else:
            print(f"[TTS] STATUS={status}  {result.get('msg', result.get('body', ''))}")

    print("\n=== RIEPILOGO ===")
    for k, v in results.items():
        print(f"  {k.upper():<5} {v['status']}")


if __name__ == "__main__":
    main()
