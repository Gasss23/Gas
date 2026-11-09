"""Voce via Telegram, fetta 1 (R8, opzione B dell'operatore, 7 nov 2026): un vocale della
chat autorizzata si trascrive e va a Gas come testo; la risposta è in testo, con la
trascrizione in cima. Telegram, download e Groq sono finti: nessuna rete."""
from __future__ import annotations

import io

import pytest

import modules.telegram.bot as bot
from modules.voice import stt, tts

CHAT = 4242
BASE = "https://api.telegram.org/botTOKEN"


class Kernel:
    def __init__(self, risposta="Ciao!"):
        self.turni, self.risposta = [], risposta

    def run_turn(self, testo, **kw):
        self.turni.append((testo, kw))
        yield {"type": "final", "content": self.risposta}


@pytest.fixture
def tg(monkeypatch):
    """Telegram finto: registra le chiamate, getFile risponde con un percorso valido."""
    stato = {"chiamate": [], "testi": [], "scaricati": [], "trascritti": [],
             "sintesi": [], "vocali_inviati": [], "esito_invio": {"ok": True}, "letti": [],
             "file": {"file_path": "voice/file_1.oga", "file_size": 1000},
             "audio": b"OGG" * 10, "trascrizione": "che ore sono"}

    def tg_post(base_url, method, payload=None, timeout=70):
        stato["chiamate"].append(method)
        if method == "sendMessage":
            stato["testi"].append(payload["text"])
        if method == "getFile":
            return {"ok": True, "result": dict(stato["file"])}
        return {"ok": True}

    class Risposta(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, n=-1):
            stato["letti"].append(n)  # V-1 ve #353: quanto si chiede di leggere
            return super().read(n)

    def sintetizza(testo, chiave, voce, **kw):
        stato["sintesi"].append(testo)
        e = stato.get("errore_sintesi")
        if e:
            raise e
        return b"MP3"

    def invia_file(base_url, method, campi, nome, nome_file, dati, mime, timeout=0):
        stato["vocali_inviati"].append((method, campi, nome, nome_file, dati, mime))
        return stato["esito_invio"]

    def urlopen(url, timeout=0):
        stato["scaricati"].append(url)
        return Risposta(stato["audio"])

    def trascrivi(audio, nome, chiave):
        stato["trascritti"].append((audio, nome))
        t = stato["trascrizione"]
        if isinstance(t, Exception):
            raise t
        return t

    monkeypatch.setattr(bot, "_tg_post", tg_post)
    monkeypatch.setattr(bot.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(stt, "transcribe_audio", trascrivi)
    monkeypatch.setattr(tts, "synthesize_speech", sintetizza)
    monkeypatch.setattr(bot, "_tg_post_file", invia_file)
    monkeypatch.setenv("ELEVENLABS_API_KEY", "chiave-finta")
    monkeypatch.delenv("ELEVENLABS_VOICE_ID", raising=False)
    monkeypatch.delenv("GAS_TELEGRAM_VOCE", raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "chiave-finta")
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    monkeypatch.delenv("GAS_TELEGRAM_VOCALI_ORA", raising=False)
    monkeypatch.setattr(bot, "_vocali_recenti", [])
    return stato


def _parlato(kw):
    """V-1 bot #355: il turno di un vocale ha l'istruzione del turno parlato con schermo."""
    from modules.voice.server import ISTRUZIONE_VOCE_SCHERMO
    return kw.get("istruzione_turno", "").startswith(ISTRUZIONE_VOCE_SCHERMO)


def _vocale(chat=CHAT, durata=5, chiave="message", **extra):
    voce = {"file_id": "F1", "duration": durata, "mime_type": "audio/ogg", **extra}
    return {"update_id": 1, chiave: {"chat": {"id": chat}, "voice": voce}}


def test_vocale_trascritto_va_a_gas_con_la_trascrizione_in_cima(tg):
    k = Kernel("Sono le dieci.")
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert [testo for testo, _ in k.turni] == ["che ore sono"]
    assert _parlato(k.turni[0][1]) and "cervello" not in k.turni[0][1]
    assert tg["testi"] == ["Ho capito: «che ore sono»\n\nSono le dieci."]
    assert tg["trascritti"] == [(b"OGG" * 10, "vocale.ogg")]
    # il file si scarica dall'URL dei file di Telegram, col percorso di getFile
    assert tg["scaricati"] == ["https://api.telegram.org/file/botTOKEN/voice/file_1.oga"]


def test_chat_non_autorizzata_niente_download_ne_trascrizione(tg):
    k = Kernel()
    bot._handle_update(BASE, _vocale(chat=999), {CHAT}, k)
    assert tg["chiamate"] == [] and tg["scaricati"] == [] and tg["trascritti"] == []
    assert k.turni == []


def test_vocale_modificato_si_ignora(tg):
    k = Kernel()
    bot._handle_update(BASE, _vocale(chiave="edited_message"), {CHAT}, k)
    assert tg["chiamate"] == [] and k.turni == []


@pytest.mark.parametrize("durata,atteso", [(61, "✗ Vocale troppo lungo"),
                                           (600, "✗ Vocale troppo lungo"),
                                           (None, "✗ Vocale senza durata"),
                                           ("5", "✗ Vocale senza durata"),
                                           (True, "✗ Vocale senza durata")])
def test_vocale_troppo_lungo_o_senza_durata_non_si_scarica(tg, durata, atteso):
    k = Kernel()
    bot._handle_update(BASE, _vocale(durata=durata), {CHAT}, k)
    assert tg["scaricati"] == [] and tg["trascritti"] == [] and k.turni == []
    assert len(tg["testi"]) == 1 and tg["testi"][0].startswith(atteso)


def test_vocale_di_60_secondi_passa(tg):
    k = Kernel()
    bot._handle_update(BASE, _vocale(durata=60), {CHAT}, k)
    assert len(k.turni) == 1


def test_vocale_troppo_grande_dal_messaggio_non_si_scarica(tg):
    k = Kernel()
    bot._handle_update(BASE, _vocale(file_size=bot.VOCALE_MAX_BYTES + 1), {CHAT}, k)
    assert tg["scaricati"] == [] and k.turni == []
    assert tg["testi"] == ["✗ Vocale troppo grande."]


def test_file_troppo_grande_da_getfile_non_si_scarica(tg):
    tg["file"]["file_size"] = bot.VOCALE_MAX_BYTES + 1
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert tg["scaricati"] == [] and k.turni == []
    assert "scaricare" in tg["testi"][0]


def test_download_oltre_il_tetto_si_scarta(tg, monkeypatch):
    monkeypatch.setattr(bot, "VOCALE_MAX_BYTES", 10)
    tg["file"]["file_size"] = None
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert tg["trascritti"] == [] and k.turni == []


@pytest.mark.parametrize("percorso", [None, "", "../segreti", 5])
def test_percorso_di_getfile_non_valido(tg, percorso):
    tg["file"]["file_path"] = percorso
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert tg["scaricati"] == [] and k.turni == []


def test_senza_chiave_groq_niente_download(tg, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY")
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert tg["scaricati"] == [] and k.turni == []
    assert "GROQ_API_KEY" in tg["testi"][0]


@pytest.mark.parametrize("errore,atteso", [
    (stt.TrascrizioneIncerta("bla", "poche parole"), "Non ho capito bene"),
    (stt.GroqSTTError(500, "giù"), "Trascrizione non riuscita (Groq)"),
    (OSError("rete"), "Trascrizione non riuscita."),
    ("   ", "non ho sentito parole"),
])
def test_errori_della_trascrizione_niente_turno(tg, errore, atteso):
    tg["trascrizione"] = errore
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [] and len(tg["testi"]) == 1 and atteso in tg["testi"][0]


def test_forte_detto_all_inizio_va_al_cervello_forte(tg):
    tg["trascrizione"] = "Forte, riassumi i lead di oggi"
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert [testo for testo, _ in k.turni] == ["riassumi i lead di oggi"]
    assert k.turni[0][1]["cervello"] == "forte" and _parlato(k.turni[0][1])


def test_forte_senza_richiesta_da_l_uso_e_nessun_turno(tg):
    tg["trascrizione"] = "Forte."
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == []
    assert tg["testi"][0].startswith("Ho capito: «Forte.»") and "Non ho avviato" in tg["testi"][0]


def test_i_comandi_non_valgono_a_voce(tg):
    """Un vocale trascritto come «/clear» non cancella la cronologia: va a Gas come testo."""
    tg["trascrizione"] = "/clear"
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert [testo for testo, _ in k.turni] == ["/clear"]


def test_errore_del_turno_non_fa_cadere_il_bot(tg):
    class Rotto:
        def run_turn(self, *a, **kw):
            raise RuntimeError("giù")
    bot._handle_update(BASE, _vocale(), {CHAT}, Rotto())
    assert tg["testi"][0].startswith("Ho capito: «che ore sono»") and "✗ Errore interno" in tg["testi"][0]


def test_i_messaggi_di_testo_restano_come_prima(tg):
    k = Kernel("ok")
    bot._handle_update(BASE, {"update_id": 2, "message": {"chat": {"id": CHAT}, "text": "ciao"}},
                       {CHAT}, k)
    assert k.turni == [("ciao", {})] and tg["testi"] == ["ok"]
    assert tg["scaricati"] == [] and tg["trascritti"] == []


def test_tetto_di_vocali_all_ora(tg, monkeypatch):
    """R-711-3: oltre GAS_TELEGRAM_VOCALI_ORA vocali nell'ultima ora niente download né
    Groq; passata l'ora si riparte."""
    monkeypatch.setenv("GAS_TELEGRAM_VOCALI_ORA", "2")
    adesso = [1000.0]
    monkeypatch.setattr(bot.time, "monotonic", lambda: adesso[0])
    k = Kernel()
    for _ in range(3):
        bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert len(k.turni) == 2 and len(tg["scaricati"]) == 2
    assert tg["testi"][-1].startswith("✗ Troppi vocali")
    adesso[0] += 3601
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert len(k.turni) == 3


@pytest.mark.parametrize("valore", ["abc", "0", "-3"])
def test_tetto_orario_non_valido_usa_il_predefinito(monkeypatch, valore):
    monkeypatch.setenv("GAS_TELEGRAM_VOCALI_ORA", valore)
    assert bot._vocali_ora() == bot.VOCALI_ORA_PREDEFINITO


def test_regole_della_voce_non_caricate_l_operatore_lo_sa(tg, monkeypatch):
    """R-711-4: se modules.voice.server non si carica, all'operatore arriva un errore."""
    import builtins
    vero = builtins.__import__

    def finto(nome, *a, **kw):
        if nome == "modules.voice.server":
            raise ImportError("rotto")
        return vero(nome, *a, **kw)
    monkeypatch.setattr(builtins, "__import__", finto)
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [] and "non posso gestire i vocali" in tg["testi"][-1]


# ── fetta 2: risposta anche a voce, solo dopo un vocale (decisione del 9 nov 2026) ──

def test_dopo_un_vocale_la_risposta_arriva_anche_a_voce(tg):
    k = Kernel("Sono le dieci.")
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert tg["testi"] == ["Ho capito: «che ore sono»\n\nSono le dieci."]
    assert tg["sintesi"] == ["Sono le dieci."]
    metodo, campi, nome, nome_file, dati, mime = tg["vocali_inviati"][0]
    assert (metodo, campi, nome, dati, mime) == ("sendVoice", {"chat_id": str(CHAT)}, "voice",
                                                 b"MP3", "audio/mpeg")


def test_dopo_un_testo_niente_voce(tg):
    k = Kernel("ok")
    bot._handle_update(BASE, {"update_id": 2, "message": {"chat": {"id": CHAT}, "text": "ciao"}},
                       {CHAT}, k)
    assert tg["sintesi"] == [] and tg["vocali_inviati"] == []


@pytest.mark.parametrize("valore", ["0", "false", "OFF", "no"])
def test_voce_spenta_resta_solo_il_testo(tg, monkeypatch, valore):
    monkeypatch.setenv("GAS_TELEGRAM_VOCE", valore)
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert tg["sintesi"] == [] and tg["vocali_inviati"] == [] and len(tg["testi"]) == 1


def test_si_dice_solo_la_risposta_finale_non_gli_strumenti(tg):
    class ConStrumenti:
        def run_turn(self, testo, **kw):
            yield {"type": "tool_res", "output": "dati riservati del file"}
            yield {"type": "final", "content": "Fatto."}
    bot._handle_update(BASE, _vocale(), {CHAT}, ConStrumenti())
    assert "[…] dati riservati del file" in tg["testi"][0]
    assert tg["sintesi"] == ["Fatto."]


def test_risposta_lunga_si_dice_solo_la_parte_parlata(tg):
    from modules.voice.server import parte_parlata
    lungo = " ".join(f"Frase numero {i} della risposta." for i in range(40))
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel(lungo))
    assert tg["sintesi"] == [parte_parlata(lungo)] and tg["sintesi"][0] != lungo


def test_turno_in_errore_niente_voce(tg):
    class Rotto:
        def run_turn(self, *a, **kw):
            yield {"type": "final", "content": "mezza"}
            yield {"type": "error", "content": "giù"}
    bot._handle_update(BASE, _vocale(), {CHAT}, Rotto())
    assert tg["sintesi"] == [] and tg["vocali_inviati"] == []


def test_forte_senza_richiesta_niente_voce(tg):
    tg["trascrizione"] = "Forte."
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel())
    assert tg["sintesi"] == [] and tg["vocali_inviati"] == []


def test_senza_chiave_elevenlabs_avviso_e_testo_gia_arrivato(tg, monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY")
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert tg["testi"][0].endswith("ok") and "ELEVENLABS_API_KEY" in tg["testi"][1]
    assert tg["sintesi"] == []


def test_sintesi_in_errore_avviso_breve(tg):
    tg["errore_sintesi"] = tts.ElevenLabsTTSError(500, "giù")
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert tg["vocali_inviati"] == [] and "Risposta vocale non riuscita" in tg["testi"][1]


def test_invio_del_vocale_rifiutato_avviso_breve(tg):
    tg["esito_invio"] = None
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert "Risposta vocale non inviata" in tg["testi"][1]


def test_voce_scelta_da_elevenlabs_voice_id(tg, monkeypatch):
    voci = []
    monkeypatch.setenv("ELEVENLABS_VOICE_ID", "VOCE1")
    monkeypatch.setattr(tts, "synthesize_speech", lambda t, k, v, **kw: (voci.append(v), b"MP3")[1])
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert voci == ["VOCE1"]


def test_tg_post_file_manda_un_multipart(monkeypatch):
    visti = {}

    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def urlopen(req, timeout=0):
        visti["url"], visti["corpo"] = req.full_url, req.data
        visti["tipo"] = req.get_header("Content-type")
        return R(b'{"ok": true}')
    monkeypatch.setattr(bot.urllib.request, "urlopen", urlopen)
    esito = bot._tg_post_file(BASE, "sendVoice", {"chat_id": "42"}, "voice", "r.mp3", b"\x00MP3",
                              "audio/mpeg")
    assert esito == {"ok": True} and visti["url"] == BASE + "/sendVoice"
    assert visti["tipo"].startswith("multipart/form-data; boundary=")
    assert b'name="chat_id"\r\n\r\n42\r\n' in visti["corpo"]
    assert b'name="voice"; filename="r.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n\x00MP3' in visti["corpo"]


def test_tg_post_file_errore_di_rete_none(monkeypatch):
    def urlopen(req, timeout=0):
        raise OSError("rete")
    monkeypatch.setattr(bot.urllib.request, "urlopen", urlopen)
    assert bot._tg_post_file(BASE, "sendVoice", {}, "voice", "r.mp3", b"", "audio/mpeg") is None


# ── riserve della #353 ──

def test_il_download_legge_al_massimo_il_tetto_piu_uno(tg):
    """V-1 ve #353: la lettura chiede al più VOCALE_MAX_BYTES + 1 byte, non tutto il file."""
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel())
    assert tg["letti"] == [bot.VOCALE_MAX_BYTES + 1]


def test_trascrizione_non_caricata_l_operatore_lo_sa(tg, monkeypatch):
    """V-1 bot #353: se modules.voice.stt non si carica arriva un errore, non il silenzio."""
    import builtins
    vero = builtins.__import__

    def finto(nome, *a, **kw):
        if nome == "modules.voice.stt":
            raise ImportError("rotto")
        return vero(nome, *a, **kw)
    monkeypatch.setattr(builtins, "__import__", finto)
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [] and "non posso trascrivere i vocali" in tg["testi"][-1]



def test_eccezione_nel_turno_niente_voce(tg):
    """R-717-1: un'eccezione dopo un final rende il turno in errore: niente voce."""
    class Esplode:
        def run_turn(self, *a, **kw):
            yield {"type": "final", "content": "mezza"}
            raise RuntimeError("giù")
    bot._handle_update(BASE, _vocale(), {CHAT}, Esplode())
    assert "✗ Errore interno" in tg["testi"][0]
    assert tg["sintesi"] == [] and tg["vocali_inviati"] == []


def test_invio_del_vocale_con_ok_false_avviso_breve(tg):
    """R-717-2: Telegram risponde 200 con ok:false → avviso, come per un errore di rete."""
    tg["esito_invio"] = {"ok": False, "description": "Bad Request"}
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert "Risposta vocale non inviata" in tg["testi"][1]


# ── fetta 3: istruzione del turno parlato, niente formattazione a voce, voce in un thread ──

def test_voce_spenta_niente_istruzione_parlata(tg, monkeypatch):
    """Con GAS_TELEGRAM_VOCE=0 la risposta è solo testo: niente istruzione del parlato."""
    monkeypatch.setenv("GAS_TELEGRAM_VOCE", "0")
    k = Kernel()
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [("che ore sono", {})]


def test_istruzione_non_caricata_il_turno_parte_lo_stesso(tg, monkeypatch):
    import builtins
    import modules.voice.server  # noqa: F401  (già caricato: il finto blocca solo il nome)
    vero = builtins.__import__

    def finto(nome, glob=None, loc=None, lista=(), *a, **kw):
        if nome == "modules.voice.server" and "istruzione_turno_voce" in (lista or ()):
            raise ImportError("rotto")
        return vero(nome, glob, loc, lista, *a, **kw)
    monkeypatch.setattr(builtins, "__import__", finto)
    k = Kernel("ok")
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [("che ore sono", {})] and tg["testi"][0].endswith("ok")


def test_a_voce_niente_formattazione_e_niente_indirizzi(tg):
    finale = ("Ho trovato **due** lead: `Rossi` e Bianchi, dettagli su https://esempio.it/x.\n\n"
              "- **Mario Rossi**, mario@x.it\n- Anna Bianchi")
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel(finale))
    detto = tg["sintesi"][0]
    assert "*" not in detto and "`" not in detto and "https" not in detto
    assert detto.startswith("Ho trovato due lead: Rossi e Bianchi, dettagli su link")
    assert "mario@x.it" not in detto  # il dettaglio dopo la riga vuota resta nel testo
    assert "mario@x.it" in tg["testi"][0]


@pytest.mark.parametrize("finale,atteso", [
    ("# Titolo\nTesto.", "Titolo Testo."),
    ("1. primo\n2) secondo", "primo secondo"),
    ("• uno\n* due", "uno due"),
    ("__forte__ e normale", "forte e normale"),
])
def test_testo_da_dire_toglie_i_segni(finale, atteso):
    assert bot.testo_da_dire(finale) == atteso


def test_voce_con_tempi_corti(tg, monkeypatch):
    """V-1 ve #355 (R-717-4): sintesi e invio con VOCE_TIMEOUT_S (15 s), non 30."""
    tempi = []
    monkeypatch.setattr(tts, "synthesize_speech",
                        lambda t, k, v, timeout=None: (tempi.append(("sintesi", timeout)), b"MP3")[1])
    monkeypatch.setattr(bot, "_tg_post_file",
                        lambda *a, timeout=None: (tempi.append(("invio", timeout)), {"ok": True})[1])
    bot._handle_update(BASE, _vocale(), {CHAT}, Kernel("ok"))
    assert tempi == [("sintesi", 15), ("invio", 15)] and bot.VOCE_TIMEOUT_S == 15
