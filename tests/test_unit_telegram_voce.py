"""Voce via Telegram, fetta 1 (R8, opzione B dell'operatore, 7 nov 2026): un vocale della
chat autorizzata si trascrive e va a Gas come testo; la risposta è in testo, con la
trascrizione in cima. Telegram, download e Groq sono finti: nessuna rete."""
from __future__ import annotations

import io

import pytest

import modules.telegram.bot as bot
from modules.voice import stt

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
    monkeypatch.setenv("GROQ_API_KEY", "chiave-finta")
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    monkeypatch.delenv("GAS_TELEGRAM_VOCALI_ORA", raising=False)
    monkeypatch.setattr(bot, "_vocali_recenti", [])
    return stato


def _vocale(chat=CHAT, durata=5, chiave="message", **extra):
    voce = {"file_id": "F1", "duration": durata, "mime_type": "audio/ogg", **extra}
    return {"update_id": 1, chiave: {"chat": {"id": chat}, "voice": voce}}


def test_vocale_trascritto_va_a_gas_con_la_trascrizione_in_cima(tg):
    k = Kernel("Sono le dieci.")
    bot._handle_update(BASE, _vocale(), {CHAT}, k)
    assert k.turni == [("che ore sono", {})]
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
    assert k.turni == [("riassumi i lead di oggi", {"cervello": "forte"})]


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
    assert k.turni == [("/clear", {})]


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

