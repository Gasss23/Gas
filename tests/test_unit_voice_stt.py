"""
Test suite STT — FASE 3, Fetta 2.

Copre:
  - Routing audio vs JSON in VoiceHandler.do_POST (TVA-route-*)
  - Parsing multipart e audio raw (TVA-parse-*)
  - transcribe_audio con transport iniettato (TVA-transcribe-*)
  - Tutti i rami d'errore (chiave assente, audio vuoto, Groq 400/5xx/429, rete)

Zero chiamate di rete reali: il transport HTTP è sempre iniettato.
Zero token LLM: il kernel è sempre un mock.
"""
from __future__ import annotations

import http.client
import json
import os
import struct
import time
import sys
import threading
from http.server import HTTPServer
from io import BytesIO
from pathlib import Path
from typing import Any, Generator, List, Optional
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.voice.server import VoiceHandler, _token_ok
from modules.voice.stt import (
    GroqSTTError,
    TrascrizioneIncerta,
    _parse_multipart_file,
    parse_audio_body,
    transcribe_audio,
)


# ─────────────────────────────── helpers comuni ──────────────────────────────

class _MockKernel:
    def __init__(self, events=None):
        self._events = events or [{"type": "final", "content": "ok kernel"}]

    def run_turn(self, prompt: str, **kw) -> Generator[dict, None, None]:
        self.kw = kw  # V3: istruzione_turno per i turni parlati
        yield from self._events

    def registra_seguito(self, domanda: str, risposta: str) -> bool:
        # V15 punto 1: il server registra i seguiti rivolti a Gas
        self.registrati = getattr(self, "registrati", []) + [(domanda, risposta)]
        return True


def _make_server(kernel: Any, token: str) -> tuple[HTTPServer, int]:
    class _H(VoiceHandler):
        pass
    _H.kernel = kernel
    _H.token = token
    srv = HTTPServer(("127.0.0.1", 0), _H)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, port


def _post_raw(port: int, body: bytes, headers: dict) -> tuple[int, dict]:
    import urllib.error
    import urllib.request
    url = f"http://127.0.0.1:{port}/voice"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        # R-384-1 (chat Voce): niente proxy verso 127.0.0.1, qualunque sia l'ambiente
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=5) as r:
            if r.headers.get("Content-Type", "").startswith("audio/"):
                return r.status, {"_raw_audio": True}  # V2: risposta sintetizzata
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


_TOKEN = "test-token-stt-abc"
_AUTH = {"Authorization": f"Bearer {_TOKEN}"}


def _wav_header(data_size: int = 0) -> bytes:
    """Genera un header WAV minimale valido (44 byte)."""
    return (
        b"RIFF" + struct.pack("<I", 36 + data_size) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16)
        + b"data" + struct.pack("<I", data_size)
    )


def _fake_wav(n_samples: int = 100) -> bytes:
    """WAV sintetico minimo con dati."""
    samples = bytes(n_samples * 2)  # silenzio PCM
    return _wav_header(len(samples)) + samples


# ─────────────────── Fake transport per transcribe_audio ─────────────────────

class _FakeResponse:
    def __init__(self, status: int, body: str | bytes):
        self.status = status
        self._body = body.encode() if isinstance(body, str) else body

    def read(self) -> bytes:
        return self._body


class _FakeConn:
    """Sostituisce http.client.HTTPSConnection nei test."""

    def __init__(self, status: int = 200, body: str = '{"text": "trascrizione di test"}'):
        self._resp = _FakeResponse(status, body)
        self.last_kwargs: dict = {}

    def request(self, method, path, body=None, headers=None):
        self.last_kwargs = {"method": method, "path": path, "body": body, "headers": headers}

    def getresponse(self) -> _FakeResponse:
        return self._resp

    def close(self) -> None:
        pass


def _factory(conn: _FakeConn):
    return lambda: conn


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-transcribe-*: test di transcribe_audio con transport iniettato
# ═══════════════════════════════════════════════════════════════════════════════

class TestTranscribeAudio:

    def test_success_returns_text(self):
        conn = _FakeConn(200, '{"text": "ciao mondo"}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == "ciao mondo"

    def test_sends_to_correct_endpoint(self):
        conn = _FakeConn()
        transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert conn.last_kwargs["path"] == "/openai/v1/audio/transcriptions"
        assert conn.last_kwargs["method"] == "POST"

    def test_sends_bearer_auth(self):
        conn = _FakeConn()
        transcribe_audio(_fake_wav(), "audio.wav", "my-secret-key", _conn_factory=_factory(conn))
        assert conn.last_kwargs["headers"]["Authorization"] == "Bearer my-secret-key"

    def test_groq_400_raises_groq_error(self):
        conn = _FakeConn(400, '{"error": "formato invalido"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 400

    def test_groq_429_raises_groq_error(self):
        conn = _FakeConn(429, '{"error": "quota"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 429

    def test_groq_500_raises_groq_error(self):
        conn = _FakeConn(500, '{"error": "server error"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 500

    def test_network_error_raises_oserror(self):
        class _BrokenConn:
            def request(self, *a, **kw): raise OSError("connection refused")
            def close(self): pass

        with pytest.raises(OSError):
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=lambda: _BrokenConn())

    def test_empty_text_in_response(self):
        conn = _FakeConn(200, '{"text": ""}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == ""

    def test_text_stripped(self):
        conn = _FakeConn(200, '{"text": "  ciao  "}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == "ciao"

    def test_groq_200_non_json_body_raises_groq_error(self):
        """R-stt-1: Groq 200 con body non-JSON → GroqSTTError (non JSONDecodeError nuda)."""
        conn = _FakeConn(200, b"<html>Cloudflare error</html>")
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 200
        assert "non JSON" in exc_info.value.message


# ── V6 (chat M2, «capire meglio»): parametri di Whisper e trascrizioni incerte ──

def _verbose(testo: str, segmenti: list) -> str:
    return json.dumps({"text": testo, "segments": segmenti})


def _seg(lp: float, ns: float, start: float = 0.0, end: float = 1.0) -> dict:
    return {"start": start, "end": end, "avg_logprob": lp, "no_speech_prob": ns}


class TestV6Trascrizione:

    def _trascrivi(self, body: str) -> str:
        return transcribe_audio(_fake_wav(), "audio.wav", "k", _conn_factory=_factory(_FakeConn(200, body)))

    def test_v6_parametri_inviati_a_groq(self):
        """Lingua italiana, temperatura 0, verbose_json e prompt con le parole di Gas."""
        conn = _FakeConn()
        transcribe_audio(_fake_wav(), "audio.wav", "k", _conn_factory=_factory(conn))
        corpo = conn.last_kwargs["body"]

        def campo(nome: str) -> bytes:
            return corpo.split(f'name="{nome}"\r\n\r\n'.encode(), 1)[1].split(b"\r\n", 1)[0]

        assert campo("model") == b"whisper-large-v3"
        assert campo("language") == b"it"
        assert campo("temperature") == b"0"
        assert campo("response_format") == b"verbose_json"
        prompt = campo("prompt").decode()
        assert all(p in prompt for p in ("Gas", "lead", "forte", "bozza", "firma"))

    def test_v6_trascrizione_sicura_passa(self):
        assert self._trascrivi(_verbose(" sì, mandala ", [_seg(-0.25, 0.05)])) == "sì, mandala"

    def test_v6_bassa_confidenza_scartata(self):
        with pytest.raises(TrascrizioneIncerta) as e:
            self._trascrivi(_verbose("gas fatti la lista", [_seg(-1.4, 0.2)]))
        assert e.value.testo == "gas fatti la lista" and "avg_logprob" in e.value.motivo

    def test_v6_silenzio_scartato(self):
        with pytest.raises(TrascrizioneIncerta) as e:
            self._trascrivi(_verbose("Ciao.", [_seg(-0.7, 0.95)]))
        assert "no_speech" in e.value.motivo

    def test_v6_si_breve_e_chiaro_passa_anche_con_no_speech_alto(self):
        """R-611-1-M2: su large-v3 no_speech_prob è alto anche su un «sì» vero: senza
        confidenza bassa non è silenzio (regola AND di Whisper)."""
        assert self._trascrivi(_verbose("Sì.", [_seg(-0.2, 0.85, 0.0, 0.4)])) == "Sì."

    @pytest.mark.parametrize("eco", ["Gas, forte, lead, bozza, firma.",
                                     "Conversazione in italiano con Gas."])
    def test_v6_eco_del_prompt_scartata(self, eco):
        """R-611-2-M2: sul silenzio Whisper ripete il prompt: non è una richiesta."""
        with pytest.raises(TrascrizioneIncerta) as e:
            self._trascrivi(_verbose(eco, [_seg(-0.3, 0.3)]))
        assert "prompt" in e.value.motivo

    @pytest.mark.parametrize("frase", ["Gas, prepara la bozza per il lead di oggi",
                                       "manda il report su Telegram",
                                       "Gas, forte, firma la bozza",       # R-612-1-M2
                                       "Gas forte report merge", "Gas forte memoria lead",
                                       "firma bozza lead forte"])
    def test_v6_richieste_vere_con_parole_del_prompt_passano(self, frase):
        assert self._trascrivi(_verbose(frase, [_seg(-0.3, 0.1)])) == frase

    def test_v6_media_pesata_per_durata(self):
        """Un pezzetto incerto in una frase lunga e sicura non la fa scartare."""
        segs = [_seg(-0.2, 0.05, 0.0, 4.0), _seg(-2.5, 0.3, 4.0, 4.4)]
        assert self._trascrivi(_verbose("frase lunga e chiara", segs)) == "frase lunga e chiara"

    @pytest.mark.parametrize("frase", ["Sottotitoli creati dalla comunità Amara.org",
                                       "Grazie per la visione!", "Sottotitoli e revisione a cura di QTSS"])
    def test_v6_frasi_inventate_da_whisper_scartate(self, frase):
        with pytest.raises(TrascrizioneIncerta):
            self._trascrivi(_verbose(frase, [_seg(-0.2, 0.1)]))

    @pytest.mark.parametrize("malformato", ["x", {"start": 0, "end": 1}, {"avg_logprob": "boh",
                                                                    "no_speech_prob": 0.1}])
    def test_v6_segmento_malformato_non_spegne_gli_altri(self, malformato):
        """V-1 ve #318 (2ª verifica): un segmento rotto si salta, il segmento cattivo accanto
        fa ancora scartare la trascrizione (come per i NaN, R-614-2-M2)."""
        corpo = json.dumps({"text": "ciao", "segments": [malformato, _seg(-2.0, 0.99, 1.0, 2.0)]})
        with pytest.raises(TrascrizioneIncerta):
            self._trascrivi(corpo)

    def test_v6_segmenti_senza_campi_non_scartano(self):
        """Risposta senza i dettagli attesi: si tiene il testo (non si scarta a caso)."""
        assert self._trascrivi(_verbose("ciao", [{"start": 0, "end": 1}])) == "ciao"
        assert self._trascrivi('{"text": "ciao"}') == "ciao"

    def test_v6_soglie_da_env(self):
        corpo = _verbose("ciao", [_seg(-0.9, 0.1)])
        assert self._trascrivi(corpo) == "ciao"
        with patch.dict(os.environ, {"GAS_VOICE_STT_LOGPROB_MIN": "-0.5"}):
            with pytest.raises(TrascrizioneIncerta):
                self._trascrivi(corpo)
        for sbagliato in ("non-numero", "nan", "-inf"):
            with patch.dict(os.environ, {"GAS_VOICE_STT_LOGPROB_MIN": sbagliato}):
                assert self._trascrivi(corpo) == "ciao"
        with patch.dict(os.environ, {"GAS_VOICE_STT_LOGPROB_MIN": "nan"}):
            with pytest.raises(TrascrizioneIncerta):   # nan → default, il controllo resta acceso
                self._trascrivi(_verbose("ciao", [_seg(-1.5, 0.1)]))

    def test_v6_eco_corta_del_prompt_sul_silenzio_scartata(self):
        """V-1 bot #318: «Gas, forte, lead.» con no_speech alto è un'eco, non un comando."""
        with pytest.raises(TrascrizioneIncerta) as e:
            self._trascrivi(_verbose("Gas, forte, lead.", [_seg(-0.3, 0.95)]))
        assert "eco corta" in e.value.motivo

    @pytest.mark.parametrize("frase", ["Gas, forte, lead.", "Gas forte", "PR merge.",
                                       "Report PR.", "Firma contatto."])
    @pytest.mark.parametrize("ns", [0.2, 0.85])
    def test_v6_eco_corta_con_voce_vera_passa(self, frase, ns):
        """V-1 bot #318 / R-614-1-M2: le stesse parole dette davvero passano, anche con il
        no_speech di un «Sì.» chiaro su large-v3 (0,85, vedi test del «sì» breve)."""
        assert self._trascrivi(_verbose(frase, [_seg(-0.2, ns)])) == frase

    def test_v6_eco_corta_soglia_da_env(self):
        corpo = _verbose("PR merge.", [_seg(-0.2, 0.85)])
        with patch.dict(os.environ, {"GAS_VOICE_STT_ECO_NO_SPEECH": "0.8"}):
            with pytest.raises(TrascrizioneIncerta):
                self._trascrivi(corpo)

    @pytest.mark.parametrize("campo", ["avg_logprob", "no_speech_prob", "end"])
    def test_v6_valori_nan_dei_segmenti_non_scartano_a_caso(self, campo):
        """V-1 ve #318: NaN in un segmento (json.loads lo accetta) non aggira i controlli
        dando un esito a caso: il dato è inutile, il testo si tiene come senza dettagli;
        e un testo sicuramente cattivo resta scartato dall'elenco delle frasi inventate."""
        seg = _seg(-1.5, 0.95)
        seg[campo] = float("nan")
        corpo = json.dumps({"text": "ciao", "segments": [seg]})
        assert "NaN" in corpo
        assert self._trascrivi(corpo) == "ciao"
        seg2 = dict(seg, avg_logprob=-0.2, no_speech_prob=0.1)
        with pytest.raises(TrascrizioneIncerta):
            self._trascrivi(json.dumps({"text": "Grazie per la visione", "segments": [seg2]}))
        # R-614-2-M2: un segmento NaN non spegne il controllo sugli altri
        cattivo = _seg(-2.0, 0.99, 1.0, 2.0)
        with pytest.raises(TrascrizioneIncerta):
            self._trascrivi(json.dumps({"text": "ciao", "segments": [seg, cattivo]}))

    def test_v6_json_non_oggetto_errore_groq(self):
        with pytest.raises(GroqSTTError):
            self._trascrivi("[1, 2]")


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-parse-*: test di parse_audio_body
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseAudioBody:

    def test_audio_wav_raw(self):
        raw = _fake_wav()
        audio, fname = parse_audio_body(raw, "audio/wav")
        assert audio == raw
        assert fname == "audio.wav"

    def test_audio_mp3_raw(self):
        raw = b"\xff\xfb\x90\x00" + bytes(100)
        audio, fname = parse_audio_body(raw, "audio/mpeg")
        assert audio == raw
        assert fname == "audio.mpeg"

    def test_audio_raw_empty_raises(self):
        with pytest.raises(ValueError, match="vuoto"):
            parse_audio_body(b"", "audio/wav")

    def test_multipart_extracts_file(self):
        wav = _fake_wav()
        boundary = "testboundary123"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="voce.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
        ).encode() + wav + (
            f"\r\n--{boundary}--\r\n"
        ).encode()

        audio, fname = parse_audio_body(body, f"multipart/form-data; boundary={boundary}")
        assert audio == wav
        assert fname == "voce.wav"

    def test_multipart_empty_raises(self):
        with pytest.raises(ValueError):
            parse_audio_body(b"", "multipart/form-data; boundary=x")

    def test_multipart_missing_file_field_raises(self):
        boundary = "testboundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="model"\r\n\r\n'
            f"whisper-large-v3\r\n"
            f"--{boundary}--\r\n"
        ).encode()
        with pytest.raises(ValueError, match="non trovato"):
            parse_audio_body(body, f"multipart/form-data; boundary={boundary}")

    def test_unsupported_content_type_raises(self):
        with pytest.raises(ValueError, match="non supportato"):
            parse_audio_body(b"...", "application/json")


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-route-*: test del routing audio vs JSON in VoiceHandler
# ═══════════════════════════════════════════════════════════════════════════════

class TestVoiceHandlerRouting:
    """Verifica che audio e JSON vengano instradati correttamente."""

    def setup_method(self):
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, _TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_json_path_unchanged(self):
        """JSON {"prompt": ...} → path attuale, nessuna STT."""
        hdrs = {**_AUTH, "Content-Type": "application/json"}
        body = json.dumps({"prompt": "ciao"}).encode()
        with patch("modules.voice.server.transcribe_audio") as mock_stt:
            status, resp = _post_raw(self.port, body, hdrs)
        mock_stt.assert_not_called()
        assert status == 200
        assert resp.get("content") == "ok kernel"

    def test_audio_wav_routes_to_stt(self):
        """Content-Type audio/wav → transcribe_audio invocata."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="testo audio") as mock_stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        mock_stt.assert_called_once()
        assert status == 200

    def test_v1_parola_forte_parlata_va_al_forte(self):
        """V1 (chat M2): «Gas, forte: …» trascritto → run_turn col solo cervello forte."""
        visti = []

        def _run_turn(prompt, **kw):
            visti.append((prompt, kw))
            yield {"type": "final", "content": "ok forte"}

        self.kernel.run_turn = _run_turn
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, forte: analizza i lead"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 200
        from modules.voice.server import ISTRUZIONE_VOCE
        assert len(visti) == 1 and visti[0][0] == "analizza i lead"
        assert visti[0][1]["cervello"] == "forte"
        assert visti[0][1]["istruzione_turno"].startswith(ISTRUZIONE_VOCE + " Adesso è ")  # V13

    def _uso_parlato(self, trascritto: str, extra_env: dict | None = None, accept: str | None = None):
        visti = []

        def _run_turn(prompt, **kw):
            visti.append(prompt)
            yield {"type": "final", "content": "no"}

        self.kernel.run_turn = _run_turn
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        if accept:
            hdrs["Accept"] = accept
        env = {"GROQ_API_KEY": "fake-key", **(extra_env or {})}
        with patch("modules.voice.server.transcribe_audio", return_value=trascritto):
            with patch.dict(os.environ, env):
                if "GAS_VOCE_FORTE" not in (extra_env or {}):
                    os.environ.pop("GAS_VOCE_FORTE", None)
                status, resp = _post_raw(self.port, wav, hdrs)
        return status, resp, visti

    def test_v1_parola_forte_parlata_senza_richiesta_istruzione_d_uso(self):
        """V2 (V-2 ve #304): «Forte.» trascritto senza richiesta → risposta d'uso da
        ascoltare (200, non un errore), nessun turno (mai ai gratuiti)."""
        status, resp, visti = self._uso_parlato("Forte.")
        assert status == 200 and resp.get("uso") is True
        assert "Dopo «forte» dimmi cosa fare" in resp["content"]
        assert "Non ho avviato nessun lavoro" in resp["content"]
        assert visti == []

    def test_v2_gas_forte_da_solo_con_interruttore_acceso(self):
        """V2: con GAS_VOCE_FORTE=1 «Gas, forte.» da solo dà la stessa istruzione d'uso,
        nessun turno vuoto al forte."""
        status, resp, visti = self._uso_parlato("Gas, forte.", {"GAS_VOCE_FORTE": "1"})
        assert status == 200 and "Dopo «forte» dimmi cosa fare" in resp["content"]
        assert visti == []

    def test_v2_istruzione_d_uso_sintetizzata_a_voce(self):
        """V2: col client che chiede audio l'istruzione d'uso arriva come MP3 (sintesi)."""
        with patch("modules.voice.server.synthesize_speech", return_value=b"ID3mp3") as tts:
            status, resp, visti = self._uso_parlato(
                "Forte!", {"ELEVENLABS_API_KEY": "fake-el"}, accept="audio/mpeg")
        assert status == 200 and resp == {"_raw_audio": True}
        assert "Dopo «forte» dimmi cosa fare" in tts.call_args[0][0]
        assert visti == []

    def test_v3_turno_parlato_ha_istruzione_voce_e_lo_scritto_no(self):
        """V3: il turno PARLATO passa istruzione_turno (risposte corte); quello scritto no."""
        from modules.voice.server import ISTRUZIONE_VOCE
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="che ne pensi?"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                status, _ = _post_raw(self.port, wav, hdrs)
        assert status == 200 and set(self.kernel.kw) == {"istruzione_turno"}
        assert self.kernel.kw["istruzione_turno"].startswith(ISTRUZIONE_VOCE + " Adesso è ")  # V13
        body = json.dumps({"prompt": "ciao"}).encode()
        with patch.dict(os.environ, {}):
            os.environ.pop("GAS_VOCE_FORTE", None)
            status, _ = _post_raw(self.port, body, {**_AUTH, "Content-Type": "application/json"})
        assert status == 200 and self.kernel.kw == {}

    def test_v4_con_schermo_istruzione_riassunto_e_dettaglio(self):
        """V4 (V-1 bot #311): con la pagina del browser (X-Gas-Formato: audio+testo) il turno
        parlato chiede «frasi da dire, poi il dettaglio dopo una riga vuota»."""
        from modules.voice.server import ISTRUZIONE_VOCE_SCHERMO
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+testo"}
        with patch("modules.voice.server.transcribe_audio", return_value="analizza i lead"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                os.environ.pop("ELEVENLABS_API_KEY", None)
                status, _ = _post_raw(self.port, wav, hdrs)
        assert status == 200 and set(self.kernel.kw) == {"istruzione_turno"}
        assert self.kernel.kw["istruzione_turno"].startswith(ISTRUZIONE_VOCE_SCHERMO + " Adesso è ")  # V13
        assert "riga vuota" in ISTRUZIONE_VOCE_SCHERMO

    def test_v4_tetto_orario_dei_turni_parlati(self):
        """V4 (V-2 ve #311): oltre GAS_VOICE_MAX_TURNI_ORA turni parlati nell'ultima ora →
        429 chiaro, nessun turno del kernel; il testo scritto non conta."""
        chiamate = []

        def _run_turn(prompt, **kw):
            chiamate.append(prompt)
            yield {"type": "final", "content": "ok"}

        self.kernel.run_turn = _run_turn
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        risultati = []
        with patch("modules.voice.server.transcribe_audio", return_value="ciao") as stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key", "GAS_VOICE_MAX_TURNI_ORA": "2"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                for _ in range(3):
                    risultati.append(_post_raw(self.port, wav, hdrs))
                scritto = _post_raw(self.port, json.dumps({"prompt": "ciao"}).encode(),
                                    {**_AUTH, "Content-Type": "application/json"})
        assert [r[0] for r in risultati] == [200, 200, 429]
        assert "GAS_VOICE_MAX_TURNI_ORA" in risultati[2][1]["error"]
        assert scritto[0] == 200
        assert chiamate == ["ciao", "ciao", "ciao"]  # 2 parlati + 1 scritto
        assert stt.call_count == 2  # R-580-2-M2: oltre il tetto niente trascrizione (Groq)

    def test_v5_tetto_conta_uso_e_trascrizioni_vuote(self):
        """V5 (R-581-2-M2): anche «forte» senza richiesta e la trascrizione vuota spendono
        Groq, quindi contano per GAS_VOICE_MAX_TURNI_ORA; la terza richiesta → 429 senza STT,
        e nessun turno del kernel parte in tutto il giro."""
        chiamate = []

        def _run_turn(prompt, **kw):
            chiamate.append(prompt)
            yield {"type": "final", "content": "ok"}

        self.kernel.run_turn = _run_turn
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=["Forte.", "", "ciao"]) as stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key", "GAS_VOICE_MAX_TURNI_ORA": "2"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                stati = [_post_raw(self.port, wav, hdrs)[0] for _ in range(3)]
        assert stati == [200, 400, 429], stati   # uso (istruzione), vuota (400), tetto
        assert stt.call_count == 2
        assert chiamate == []

    def test_v6_chiamata_groq_fallita_conta_nel_tetto(self):
        """V-1 bot #314: anche una chiamata a Groq che fallisce (500 → 502) spende e conta:
        con tetto 1 la richiesta dopo → 429 senza una seconda trascrizione."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio",
                   side_effect=[GroqSTTError(500, "Groq 500: guasto"), "ciao"]) as stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key", "GAS_VOICE_MAX_TURNI_ORA": "1"}):
                stati = [_post_raw(self.port, wav, hdrs)[0] for _ in range(2)]
        assert stati == [502, 429], stati
        assert stt.call_count == 1

    def test_v6_trascrizione_incerta_chiede_di_ripetere(self):
        """V6: testo incerto → «non ho capito, ripeti?», nessun turno, conta nel tetto, e la
        risposta dice cosa è stato sentito («capito»)."""
        chiamate = []

        def _run_turn(prompt, **kw):
            chiamate.append(prompt)
            yield {"type": "final", "content": "ok"}

        self.kernel.run_turn = _run_turn
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio",
                   side_effect=[TrascrizioneIncerta("gas fatti", "poco sicura"), "ciao"]):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key", "GAS_VOICE_MAX_TURNI_ORA": "1"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                primo = _post_raw(self.port, wav, hdrs)
                secondo = _post_raw(self.port, wav, hdrs)
        assert primo[0] == 200 and primo[1]["non_capito"] is True
        assert primo[1]["capito"] == "gas fatti" and "ripetere" in primo[1]["content"]
        assert chiamate == [] and secondo[0] == 429

    def test_v6_risposta_dice_cosa_ha_capito(self):
        """V6: la risposta del turno porta il testo trascritto, anche con «forte» davanti
        (si mostra quello che è stato sentito, non la richiesta ripulita)."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, forte: dimmi i lead"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                status, resp = _post_raw(self.port, wav, hdrs)
                kw_parlato = dict(self.kernel.kw)
                scritto = _post_raw(self.port, json.dumps({"prompt": "ciao"}).encode(),
                                    {**_AUTH, "Content-Type": "application/json"})
        assert status == 200 and resp["capito"] == "Gas, forte: dimmi i lead"
        assert kw_parlato.get("cervello") == "forte"  # «forte» tolto dalla richiesta, non dal «capito»
        assert "capito" not in scritto[1]  # testo scritto: niente da mostrare

    def test_v6_non_capito_solo_audio_senza_tts_resta_testo(self):
        """V-2 bot #318: client solo audio senza ElevenLabs → 200 JSON con il messaggio,
        non un 503 «TTS non disponibile» che nasconde la causa."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "Accept": "audio/mpeg"}
        with patch("modules.voice.server.transcribe_audio",
                   side_effect=TrascrizioneIncerta("boh", "poco sicura")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                os.environ.pop("ELEVENLABS_API_KEY", None)
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 200 and resp["non_capito"] is True and resp["capito"] == "boh"

    def test_v13_solo_parola_di_attivazione_nessun_turno(self):
        """V13 (prova sul Mac del 5 nov): una trascrizione fatta solo di «Hey Jarvis» (o «Gas»)
        riceve «Dimmi.» col segno «attivazione», senza turno del kernel; una richiesta vera
        che comincia con la parola di attivazione va al cervello come prima."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        for detto in ("Hey Jarvis!", "hey, jarvis.", "Jarvis", "Ehi Gas", "  Gus?  ", "Ciao Gas...",
                      "Hey Jarvis, Hey Jarvis!", "Jarvis Jarvis", "Gas, gas.",
                      "Jarvis Gas"):  # V15 (V-1 bot #335): due nomi di fila, voluto  # V14: ripetuta (R-668-2-M2)
            self.kernel.kw = "NESSUN TURNO"
            with patch("modules.voice.server.transcribe_audio", return_value=detto):
                with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                    os.environ.pop("ELEVENLABS_API_KEY", None)
                    os.environ.pop("GAS_VOCE_FORTE", None)
                    status, resp = _post_raw(self.port, wav, hdrs)
            assert status == 200 and resp["attivazione"] is True, detto
            assert resp["content"] == "Dimmi." and resp["capito"] == detto
            assert self.kernel.kw == "NESSUN TURNO", detto
        for detto in ("Hey Jarvis, che ore sono?", "Gas, ciao", "gasolio", "Ok Gas.", "Okay, Jarvis",
                      "Hey Jarvis, Hey Jarvis, accendi"):  # V14: «ok» è una conferma (V-1 bot #334)
            self.kernel.kw = "NESSUN TURNO"
            with patch("modules.voice.server.transcribe_audio", return_value=detto):
                with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                    os.environ.pop("ELEVENLABS_API_KEY", None)
                    os.environ.pop("GAS_VOCE_FORTE", None)
                    status, resp = _post_raw(self.port, wav, hdrs)
            assert status == 200 and "attivazione" not in resp, detto
            assert self.kernel.kw != "NESSUN TURNO", detto

    def test_v15_pausa_nessun_turno_e_comando(self):
        """V15 (contratto dell'operatore via M1): «pausa»/«standby»/«basta così», anche dopo la
        parola di attivazione, → «Va bene.» con X-Gas-Comando: pausa, senza turno;
        frasi che contengono «pausa» ma chiedono altro vanno al cervello, senza comando."""
        import http.client
        from modules.voice.server import RISPOSTA_PAUSA
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}

        def chiedi(detto):
            self.kernel.kw = "NESSUN TURNO"
            with patch("modules.voice.server.transcribe_audio", return_value=detto):
                with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                    os.environ.pop("ELEVENLABS_API_KEY", None)
                    os.environ.pop("GAS_VOCE_FORTE", None)
                    c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                    c.request("POST", "/voice", body=wav, headers=hdrs)
                    r = c.getresponse()
                    corpo = json.loads(r.read())
                    comando = r.getheader("X-Gas-Comando")
                    c.close()
            return r.status, corpo, comando

        for detto in ("Pausa.", "pausa", "Standby!", "stand by", "Stand-by.", "Jarvis, pausa",
                      "Hey Jarvis, standby", "Ehi Gas pausa.", "Jarvis Jarvis, pausa",
                      "Basta così.", "basta cosi", "Basta!", "Jarvis, basta così"):
            status, corpo, comando = chiedi(detto)
            assert status == 200 and comando == "pausa", detto
            assert corpo["content"] == RISPOSTA_PAUSA and corpo["pausa"] is True, detto
            assert self.kernel.kw == "NESSUN TURNO", detto
        for detto in ("Facciamo una pausa di dieci minuti", "pausa caffè", "metti in pausa la musica",
                      "Jarvis", "Gas, che ore sono?", "basta con questa storia",
                      "basta così poco per cambiare"):
            status, corpo, comando = chiedi(detto)
            assert status == 200 and comando is None and "pausa" not in corpo, detto
        # dopo una pausa la richiesta successiva non porta più il comando (stato per richiesta)
        assert chiedi("Pausa")[2] == "pausa" and chiedi("Gas, ciao")[2] is None
        # il client H24 (formato audio+pezzi) riceve lo stesso comando
        hdrs["X-Gas-Formato"] = "audio+pezzi"
        status, corpo, comando = chiedi("Jarvis, standby")
        assert status == 200 and comando == "pausa" and corpo["pausa"] is True

    def _seguito(self, risposta: str, seguito: bool = True, formato: str = "audio+pezzi"):
        import http.client
        self.kernel._events = [{"type": "final", "content": risposta}]
        self.kernel.kw = "NESSUN TURNO"
        self.kernel.registrati = []
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": formato}
        if seguito:
            hdrs["X-Gas-Seguito"] = "1"
        with patch("modules.voice.server.transcribe_audio", return_value="e poi gli ho detto di no"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                os.environ.pop("ELEVENLABS_API_KEY", None)
                os.environ.pop("GAS_VOCE_FORTE", None)
                c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                c.request("POST", "/voice", body=wav, headers=hdrs)
                r = c.getresponse()
                corpo = json.loads(r.read())
                comando = r.getheader("X-Gas-Comando")
                c.close()
        return r.status, corpo, comando

    def test_v15_seguito_non_per_me_chiude_senza_voce(self):
        """V15: turno di seguito (X-Gas-Seguito: 1) che il cervello giudica non rivolto a Gas:
        nessun testo né voce al client, X-Gas-Comando: fine; l'istruzione del turno chiede la
        decisione."""
        from modules.voice.server import ISTRUZIONE_SEGUITO, SEGNO_NON_PER_ME
        for risposta in (SEGNO_NON_PER_ME, f" {SEGNO_NON_PER_ME}\n", f"«{SEGNO_NON_PER_ME}»",
                         "NON_PER_ME", "Non per me.",  # R-675-3-M2
                         "[NON_PER_ME] (parlato fra persone)", "«[non_per_me]» la TV",  # V-2 ve #339
                         "Non è rivolto a me. [NON_PER_ME]", "La TV. «[non_per_me]».\n",  # V-1 bot 312cd86
                         "Non è rivolto a me [NON_PER_ME] (era la TV).",  # V-2 bot be60a21
                         "[NON PER ME] (fra persone)", "x [ non per me ] y"):  # R-676-1-M2
            status, corpo, comando = self._seguito(risposta)
            assert status == 200 and comando == "fine" and corpo["fine"] is True
            assert corpo["content"] == "" and "audio" not in corpo and "capito" not in corpo
            assert ISTRUZIONE_SEGUITO in self.kernel.kw["istruzione_turno"]
            assert self.kernel.kw["cervello"] == "forte"  # R-675-1-M2: mai ai gratuiti
            assert self.kernel.kw["effimero"] is True  # scelta A: niente storia, niente strumenti
            assert self.kernel.registrati == []  # punto 1: il parlato «non per me» resta fuori

    def test_v15_seguito_pausa_senza_voce(self):
        """V-2 bot #339 su 312cd86: nel seguito «Basta!» (anche dalla TV) chiude con
        X-Gas-Comando: pausa ma SENZA «Va bene.» a voce; nessun turno."""
        import http.client
        wav = _fake_wav()
        for formato in ("audio+pezzi", "audio+testo", ""):
            hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                    "X-Gas-Formato": formato, "X-Gas-Seguito": "1"}
            self.kernel.kw = "NESSUN TURNO"
            with patch("modules.voice.server.transcribe_audio", return_value="Basta!"):
                with patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
                    with patch("modules.voice.server.synthesize_speech",
                               side_effect=AssertionError("nessuna voce")):
                        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                        c.request("POST", "/voice", body=wav, headers=hdrs)
                        r = c.getresponse()
                        corpo = json.loads(r.read())
                        comando = r.getheader("X-Gas-Comando")
                        c.close()
            assert r.status == 200 and comando == "pausa", formato
            assert corpo["content"] == "" and corpo["pausa"] is True and "audio" not in corpo, formato
            assert self.kernel.kw == "NESSUN TURNO", formato

    def test_v15_seguito_forte_dalla_stanza_non_parla(self):
        """V-1 ve #339: in un turno di seguito il parlato che è solo «forte» (TV) non fa
        pronunciare il messaggio d'uso: si chiude la conversazione (fine), nessun turno."""
        import http.client
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+pezzi", "X-Gas-Seguito": "1"}
        self.kernel.kw = "NESSUN TURNO"
        with patch("modules.voice.server.transcribe_audio", return_value="Forte!"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                os.environ.pop("ELEVENLABS_API_KEY", None)
                os.environ.pop("GAS_VOCE_FORTE", None)
                c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                c.request("POST", "/voice", body=wav, headers=hdrs)
                r = c.getresponse()
                corpo = json.loads(r.read())
                comando = r.getheader("X-Gas-Comando")
                c.close()
        assert r.status == 200 and comando == "fine" and corpo["content"] == ""
        assert "uso" not in corpo and self.kernel.kw == "NESSUN TURNO"

    def test_v15_seguito_trascrizione_incerta_o_vuota_chiude(self):
        """R-676-3 (review Mani): nel seguito una trascrizione incerta o vuota (rumore della
        stanza) chiude la conversazione senza «Non ho capito» e senza turno; con la parola
        di attivazione (niente seguito) «Non ho capito» resta."""
        import http.client
        from modules.voice.stt import TrascrizioneIncerta
        wav = _fake_wav()
        for effetto in (TrascrizioneIncerta("bzz", "poco sicura"), "", TrascrizioneIncerta("x", "y")):
            for seguito in (True, False):
                hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                        "X-Gas-Formato": "audio+pezzi"}
                if seguito:
                    hdrs["X-Gas-Seguito"] = "1"
                self.kernel.kw = "NESSUN TURNO"
                kw = ({"side_effect": effetto} if isinstance(effetto, Exception)
                      else {"return_value": effetto})
                with patch("modules.voice.server.transcribe_audio", **kw):
                    with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                        os.environ.pop("ELEVENLABS_API_KEY", None)
                        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                        c.request("POST", "/voice", body=wav, headers=hdrs)
                        r = c.getresponse()
                        corpo = json.loads(r.read())
                        comando = r.getheader("X-Gas-Comando")
                        c.close()
                assert self.kernel.kw == "NESSUN TURNO"
                if seguito:
                    assert r.status == 200 and comando == "fine" and corpo["content"] == ""
                    assert "non_capito" not in corpo
                elif isinstance(effetto, Exception):
                    assert r.status == 200 and comando is None and corpo["non_capito"] is True
                else:
                    assert r.status == 400 and comando is None

    def test_v15_il_turno_viene_chiuso_subito(self):
        """R-677-1-M2: dopo il «final» il server chiude il generatore del kernel (il turno
        effimero rimette subito la storia vera), anche su errore del kernel."""
        chiusi = []
        tenuti = []  # un riferimento vivo: senza close() esplicito il finally non partirebbe

        class _K:
            def run_turn(self, prompt, **kw):
                def gen():
                    try:
                        yield {"type": "final", "content": "ok"}
                        yield {"type": "final", "content": "mai"}
                    finally:
                        chiusi.append(kw.get("effimero"))
                g = gen()
                tenuti.append(g)
                return g

        self.server.RequestHandlerClass.kernel = _K()
        try:
            status, corpo, comando = self._seguito("ignorato")
        finally:
            self.server.RequestHandlerClass.kernel = self.kernel
        assert chiusi == [True] and status == 200 and corpo["content"] == "ok"

    def test_v15_seguito_strumento_negato_chiede_la_parola(self):
        """V15: se nel seguito il forte chiede uno strumento (negato dal turno effimero), Gas
        non tace: dice di ripetere con la parola di attivazione; la conversazione resta."""
        from modules.voice.server import RISPOSTA_SERVE_ATTIVAZIONE
        self.kernel._events = [{"type": "final", "content": "", "strumento_negato": True}]
        import http.client
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+pezzi", "X-Gas-Seguito": "1"}
        with patch("modules.voice.server.transcribe_audio", return_value="salvalo come contatto"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k"}):
                os.environ.pop("ELEVENLABS_API_KEY", None)
                c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                c.request("POST", "/voice", body=wav, headers=hdrs)
                r = c.getresponse()
                corpo = json.loads(r.read())
                comando = r.getheader("X-Gas-Comando")
                c.close()
        assert r.status == 200 and comando is None
        assert corpo["content"] == RISPOSTA_SERVE_ATTIVAZIONE and corpo["serve_attivazione"] is True
        assert getattr(self.kernel, "registrati", []) == []  # la richiesta va ripetuta con Jarvis

    def test_v15_seguito_risposta_vuota_chiude(self):
        """V15: il turno effimero che ignora uno strumento finisce con risposta vuota: nel
        seguito la conversazione si chiude in silenzio (fine), niente voce."""
        status, corpo, comando = self._seguito("")
        assert status == 200 and comando == "fine" and corpo["content"] == ""
        assert self.kernel.registrati == []

    def test_v15_seguito_rivolto_a_gas_risponde_normalmente(self):
        from modules.voice.server import ISTRUZIONE_SEGUITO
        # V-2 ve #339 su a87d273: il seguito non ha strumenti e il modello deve saperlo
        assert "NON hai strumenti" in ISTRUZIONE_SEGUITO and "non dire mai" in ISTRUZIONE_SEGUITO
        status, corpo, comando = self._seguito("Certo, ci penso io.")
        assert status == 200 and comando is None and corpo["content"] == "Certo, ci penso io."
        frase = "Non per me è un problema, lo faccio subito."  # contiene le parole, non è il segno
        status, corpo, comando = self._seguito(frase)
        assert comando is None and corpo["content"] == frase
        # V15 punto 1 (sì dell'operatore): il seguito rivolto a Gas entra nella storia vera
        assert self.kernel.registrati == [("e poi gli ho detto di no", frase)]
        assert ISTRUZIONE_SEGUITO in self.kernel.kw["istruzione_turno"]

    def test_v15_senza_seguito_nessuna_decisione(self):
        """Senza l'intestazione l'istruzione non cambia e il segno non chiude nulla."""
        from modules.voice.server import ISTRUZIONE_SEGUITO, SEGNO_NON_PER_ME
        status, corpo, comando = self._seguito(SEGNO_NON_PER_ME, seguito=False)
        assert comando is None and ISTRUZIONE_SEGUITO not in self.kernel.kw["istruzione_turno"]
        assert "cervello" not in self.kernel.kw and "effimero" not in self.kernel.kw
        # un turno normale si salva da sé nel kernel: il server non lo registra di nuovo
        self._seguito("Certo.", seguito=False)
        assert self.kernel.registrati == []

    def test_v15_seguito_registrazione_che_fallisce_non_blocca(self):
        """§9: se la storia non si aggiorna (False o eccezione) la risposta parte lo stesso."""
        for esito in (False, RuntimeError("disco pieno")):
            def _reg(domanda, risposta, _e=esito):
                if isinstance(_e, Exception):
                    raise _e
                return _e
            self.kernel.registra_seguito = _reg
            try:
                status, corpo, comando = self._seguito("Certo, ci penso io.")
            finally:
                del self.kernel.registra_seguito
            assert status == 200 and comando is None and corpo["content"] == "Certo, ci penso io."

    def test_v15_seguito_a_testo_ignorato(self):
        """A TESTO l'intestazione non conta: nessuna istruzione, nessun «fine»."""
        from modules.voice.server import SEGNO_NON_PER_ME
        self.kernel._events = [{"type": "final", "content": SEGNO_NON_PER_ME}]
        body = json.dumps({"prompt": "ciao"}).encode()
        status, resp = _post_raw(self.port, body, {**_AUTH, "Content-Type": "application/json",
                                                  "X-Gas-Seguito": "1"})
        assert status == 200 and "fine" not in resp and self.kernel.kw == {}

    def test_v15_pausa_solo_dal_parlato(self):
        """V15: a TESTO «pausa» è una richiesta normale (il comando vale solo per la voce)."""
        self.kernel.kw = "NESSUN TURNO"
        body = json.dumps({"prompt": "pausa"}).encode()
        status, resp = _post_raw(self.port, body, {**_AUTH, "Content-Type": "application/json"})
        assert status == 200 and "pausa" not in resp and self.kernel.kw == {}

    def test_v13_attivazione_solo_dal_parlato(self):
        """V13: a TESTO «Hey Jarvis» resta una richiesta normale (il filtro vale per il parlato)."""
        self.kernel.kw = "NESSUN TURNO"
        body = json.dumps({"prompt": "Hey Jarvis"}).encode()
        status, resp = _post_raw(self.port, body, {**_AUTH, "Content-Type": "application/json"})
        assert status == 200 and "attivazione" not in resp and self.kernel.kw == {}

    def test_v6_capito_azzerato_a_ogni_richiesta(self):
        """V-3 bot #318: anche riusando lo stesso oggetto handler (come farebbe un
        keep-alive), una richiesta scritta non eredita il «capito» della precedente."""
        h = VoiceHandler.__new__(VoiceHandler)
        h._capito = "vecchio"
        h.path = "/altro"
        h._send_json = lambda code, payload: None
        h.do_POST()
        assert h._capito is None

    def test_v6_formato_pagina_porta_capito(self):
        """V6: col formato della pagina (audio+testo) il JSON ha «capito», anche quando
        chiede di ripetere (con il segno non_capito)."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+testo"}
        with patch("modules.voice.server.transcribe_audio",
                   side_effect=["Gas, ciao", TrascrizioneIncerta("boh", "poco sicura")]):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                os.environ.pop("ELEVENLABS_API_KEY", None)
                buono = _post_raw(self.port, wav, hdrs)
                incerto = _post_raw(self.port, wav, hdrs)
        assert buono[0] == 200 and buono[1]["capito"] == "Gas, ciao" and "non_capito" not in buono[1]
        assert incerto[0] == 200 and incerto[1]["capito"] == "boh" and incerto[1]["non_capito"] is True

    def test_v7_tempi_nella_risposta_e_nel_log(self, caplog):
        """V7: la risposta dice quanto sono durati trascrizione, cervello e server, e il log
        ne ha una riga (solo numeri); senza trascrizione (testo scritto) niente «trascrizione»."""
        import logging as _logging
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+testo"}
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, ciao"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                os.environ.pop("ELEVENLABS_API_KEY", None)
                with caplog.at_level(_logging.INFO, logger="gas.voce.tempi"):
                    status, resp = _post_raw(self.port, wav, hdrs)
                    scritto = _post_raw(self.port, json.dumps({"prompt": "ciao"}).encode(),
                                        {**_AUTH, "Content-Type": "application/json"})
        assert status == 200
        tempi = resp["tempi"]
        assert set(tempi) == {"trascrizione", "cervello", "server"}, tempi
        assert all(isinstance(v, (int, float)) and v >= 0 for v in tempi.values())
        assert tempi["server"] >= tempi["trascrizione"] and tempi["server"] >= tempi["cervello"]
        assert set(scritto[1]["tempi"]) == {"cervello", "server"}
        righe = [r for r in caplog.records if "tempi voce" in r.getMessage()]
        assert len(righe) == 2 and "trascrizione=" in righe[0].getMessage()
        assert "Gas, ciao" not in righe[0].getMessage()
        assert all(r.levelno == _logging.INFO and r.name == "gas.voce.tempi" for r in righe)  # R-614-3-M2

    def test_v7_tempi_della_voce_e_intestazione_con_mp3(self):
        """V7: con l'MP3 grezzo i tempi (voce compresa) arrivano nell'intestazione X-Gas-Tempi."""
        import urllib.request
        wav = _fake_wav()
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/voice", data=wav, method="POST",
            headers={**_AUTH, "Content-Type": "audio/wav", "Accept": "audio/mpeg"})
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, ciao"), \
             patch("modules.voice.server.synthesize_speech", return_value=b"ID3mp3"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=5) as r:
                    intestazione = r.headers.get("X-Gas-Tempi", "")
                    corpo = r.read()
        assert corpo == b"ID3mp3"
        chiavi = {p.split("=")[0] for p in intestazione.split(";")}
        assert chiavi == {"trascrizione", "cervello", "voce", "server"}, intestazione

    @pytest.mark.parametrize("tts", ["ok", "errore", "rete"])
    def test_v7_tempo_della_voce_nella_pagina_anche_se_fallisce(self, tts):
        """R-614-2-M2 / R-614-1-M2: col formato della pagina c'è anche il tempo della voce,
        pure quando ElevenLabs risponde errore o la rete cade (il caso lento da vedere)."""
        from modules.voice.tts import ElevenLabsTTSError
        effetto = {"ok": [b"ID3mp3"], "errore": ElevenLabsTTSError(500, "guasto"),
                   "rete": OSError("timeout")}[tts]
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "X-Gas-Formato": "audio+testo"}
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, ciao"), \
             patch("modules.voice.server.synthesize_speech", side_effect=effetto):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 200 and ("audio" in resp) == (tts == "ok")
        assert set(resp["tempi"]) == {"trascrizione", "cervello", "voce", "server"}, resp["tempi"]

    @pytest.mark.parametrize("guasto", ["errore", "rete"])
    def test_v7_tempo_della_voce_con_mp3_anche_se_fallisce(self, guasto):
        """R-615-1-M2: col formato MP3 un TTS fallito dà 502 JSON, con il tempo della voce."""
        from modules.voice.tts import ElevenLabsTTSError
        effetto = ElevenLabsTTSError(500, "guasto") if guasto == "errore" else OSError("timeout")
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav)),
                "Accept": "audio/mpeg"}
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, ciao"), \
             patch("modules.voice.server.synthesize_speech", side_effect=effetto):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502
        assert set(resp["tempi"]) == {"trascrizione", "cervello", "voce", "server"}, resp

    def test_v7_tempo_del_cervello_anche_se_si_rompe(self):
        """R-614-1-M2: un'eccezione del kernel (500) ha comunque il tempo del cervello."""
        def _rotto(prompt, **kw):
            raise RuntimeError("guasto")
            yield  # pragma: no cover

        self.kernel.run_turn = _rotto
        status, resp = _post_raw(self.port, json.dumps({"prompt": "ciao"}).encode(),
                                 {**_AUTH, "Content-Type": "application/json"})
        assert status == 500 and set(resp["tempi"]) == {"cervello", "server"}, resp

    def test_v7_tempo_del_cervello_anche_senza_risposta(self):
        """V-2 ve #322: un turno che finisce senza final né error (500) ha il tempo del cervello."""
        def _muto(prompt, **kw):
            yield {"type": "tool_res", "content": "x"}

        self.kernel.run_turn = _muto
        status, resp = _post_raw(self.port, json.dumps({"prompt": "ciao"}).encode(),
                                 {**_AUTH, "Content-Type": "application/json"})
        assert status == 500 and set(resp["tempi"]) == {"cervello", "server"}, resp

    def test_v7_caricamento_lento_non_conta_come_server(self):
        """V-2 bot #322: il tempo «server» parte dopo aver ricevuto il corpo: un caricamento
        lento dalla pagina resta nella «rete» (totale della pagina meno il server)."""
        import socket
        corpo = json.dumps({"prompt": "ciao"}).encode()
        testa = (f"POST /voice HTTP/1.0\r\nHost: 127.0.0.1\r\nAuthorization: {_AUTH['Authorization']}\r\n"
                 f"Content-Type: application/json\r\nContent-Length: {len(corpo)}\r\n\r\n").encode()
        with socket.create_connection(("127.0.0.1", self.port), timeout=10) as sk:
            sk.sendall(testa + corpo[:3])
            time.sleep(0.6)  # la pagina carica piano
            sk.sendall(corpo[3:])
            dati = b""
            while chunk := sk.recv(65536):
                dati += chunk
        tempi = json.loads(dati.split(b"\r\n\r\n", 1)[1])["tempi"]
        assert tempi["server"] < 0.5, tempi

    def test_v7_rifiuto_prima_di_spendere_senza_tempi(self):
        """V7: il 429 del tetto arriva prima di ogni lavoro: niente tempi né riga di log."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="ciao"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "k", "GAS_VOICE_MAX_TURNI_ORA": "1"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                primo = _post_raw(self.port, wav, hdrs)
                secondo = _post_raw(self.port, wav, hdrs)
        assert "tempi" in primo[1] and secondo[0] == 429 and "tempi" not in secondo[1]

    def test_v5_rifiuti_locali_non_consumano_il_tetto(self):
        """R-585-1-M2: un audio vuoto (400, nessuna chiamata a Groq) non conta: con tetto 1
        la richiesta valida dopo passa ancora."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav"}
        with patch("modules.voice.server.transcribe_audio", return_value="ciao") as stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key", "GAS_VOICE_MAX_TURNI_ORA": "1"}):
                os.environ.pop("GAS_VOCE_FORTE", None)
                vuoto = _post_raw(self.port, b"", {**hdrs, "Content-Length": "0"})
                buono = _post_raw(self.port, wav, {**hdrs, "Content-Length": str(len(wav))})
        assert vuoto[0] == 400 and buono[0] == 200
        assert stt.call_count == 1

    def test_multipart_routes_to_stt(self):
        """Content-Type multipart/form-data → transcribe_audio invocata."""
        wav = _fake_wav()
        boundary = "testbound"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="clip.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
        ).encode() + wav + f"\r\n--{boundary}--\r\n".encode()
        hdrs = {
            **_AUTH,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }
        with patch("modules.voice.server.transcribe_audio", return_value="testo multipart") as mock_stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, body, hdrs)
        mock_stt.assert_called_once()
        assert status == 200

    def test_audio_no_key_returns_503(self):
        """GROQ_API_KEY assente → 503 esplicito."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        env_without_key = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
        with patch.dict(os.environ, env_without_key, clear=True):
            status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 503
        assert "GROQ_API_KEY" in resp.get("error", "")

    def test_audio_empty_body_returns_400(self):
        """Body audio vuoto → 400."""
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": "0"}
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            status, resp = _post_raw(self.port, b"", hdrs)
        assert status == 400

    def test_groq_400_returns_400(self):
        """Groq risponde 400 → il server ritorna 400 al client."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(400, "Groq 400: bad audio")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 400

    def test_groq_429_returns_502(self):
        """Groq risponde 429 → il server ritorna 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(429, "Groq 429: quota")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_groq_500_returns_502(self):
        """Groq risponde 500 → il server ritorna 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(500, "Groq 500: server error")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_network_error_returns_502(self):
        """Errore di rete verso Groq → 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=OSError("connection refused")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_empty_transcription_returns_400(self):
        """Groq ritorna testo vuoto (silenzio) → 400."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value=""):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 400

    def test_transcribed_text_passed_to_kernel(self):
        """Il testo trascritto viene passato al kernel esattamente."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        received_prompts: List[str] = []
        original = self.kernel.run_turn
        self.kernel.run_turn = lambda p, **kw: received_prompts.append(p) or original(p, **kw)
        with patch("modules.voice.server.transcribe_audio", return_value="prompt trascritto"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 200
        assert received_prompts == ["prompt trascritto"]
