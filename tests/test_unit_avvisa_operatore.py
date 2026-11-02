"""Strumento avvisa_operatore (R6, chat Mani): modules/telegram/avviso.py con invio finto,
e la sua classe nel cancello."""
import json
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.telegram import avviso as av  # noqa: E402
from modules.gate.gate import (  # noqa: E402
    GateClass, gate_classify, libero_dopo_lettura, lettura_consentita, livello_scrittura,
    LIVELLO_MAI,
)


@pytest.fixture
def env(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok-di-prova")
    monkeypatch.setenv("TELEGRAM_ALLOWED_IDS", "123")
    monkeypatch.delenv("GAS_NOTIFICHE_GIORNO", raising=False)
    return tmp_path


class Finto:
    def __init__(self, ok=True, motivo=""):
        self.testi, self.ok, self.motivo = [], ok, motivo

    def __call__(self, testo):
        self.testi.append(testo)
        return self.ok, self.motivo


def _uso(root):
    return json.loads((root / av.USO_FILENAME).read_text(encoding="utf-8"))


def test_invia_col_prefisso_e_conta(env):
    f = Finto()
    out = av.avvisa_operatore("Il lead Rossi ha risposto", env, invia=f)
    assert out.startswith("Successo") and "(1/5 oggi)" in out
    assert f.testi == [av.PREFISSO + "Il lead Rossi ha risposto"]
    assert _uso(env) == {"giorno": date.today().isoformat(), "n": 1}


def test_tetto_al_giorno(env, monkeypatch):
    monkeypatch.setenv("GAS_NOTIFICHE_GIORNO", "2")
    f = Finto()
    esiti = [av.avvisa_operatore(f"n{i}", env, invia=f) for i in range(3)]
    assert [e.startswith("Successo") for e in esiti] == [True, True, False]
    assert "tetto di 2 notifiche" in esiti[2] and len(f.testi) == 2


def test_tetto_predefinito_cinque(env):
    f = Finto()
    esiti = [av.avvisa_operatore("x", env, invia=f) for _ in range(6)]
    assert sum(e.startswith("Successo") for e in esiti) == 5 and len(f.testi) == 5


def test_il_conto_resta_al_riavvio(env):
    """Il conto sta su file: un nuovo processo (qui: una nuova chiamata) lo ritrova."""
    (env / av.USO_FILENAME).write_text(
        json.dumps({"giorno": date.today().isoformat(), "n": 5}), encoding="utf-8")
    f = Finto()
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata: tetto") and f.testi == []


def test_un_altro_giorno_riparte_da_zero(env):
    (env / av.USO_FILENAME).write_text(json.dumps({"giorno": "2000-01-01", "n": 99}),
                                       encoding="utf-8")
    out = av.avvisa_operatore("x", env, invia=Finto())
    assert out.startswith("Successo") and _uso(env)["n"] == 1


@pytest.mark.parametrize("contenuto", ["{rotto", "[]", '{"giorno": "x", "n": -1}',
                                       '{"giorno": "x", "n": true}', '{"giorno": "x"}'])
def test_conto_illeggibile_niente_invio(env, contenuto):
    (env / av.USO_FILENAME).write_text(contenuto, encoding="utf-8")
    f = Finto()
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata") and "illeggibile" in out and f.testi == []


def test_conto_non_scrivibile_niente_invio(env, monkeypatch):
    """Il posto si prenota prima dell'invio: se il conto non si scrive, niente notifica."""
    monkeypatch.setattr(av, "_registra_uso", lambda p, n: False)
    f = Finto()
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata") and "non scrivibile" in out and f.testi == []


def test_invio_fallito_consuma_il_posto(env):
    f = Finto(ok=False, motivo="invio fallito verso tutti i destinatari")
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata") and "non consegnata" in out
    assert _uso(env)["n"] == 1


@pytest.mark.parametrize("manca", ["TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_IDS"])
def test_telegram_non_configurato_non_consuma_posti(env, monkeypatch, manca):
    monkeypatch.delenv(manca)
    f = Finto()
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata: Telegram non configurato") and manca in out
    assert f.testi == [] and not (env / av.USO_FILENAME).exists()


def test_id_non_validi_come_mancanti(env, monkeypatch):
    monkeypatch.setenv("TELEGRAM_ALLOWED_IDS", "abc, ,x")
    out = av.avvisa_operatore("x", env, invia=Finto())
    assert out.startswith("Operazione negata: Telegram non configurato")


@pytest.mark.parametrize("testo", [None, "", "   ", chr(0x200B) + chr(0x202E), "\x00\x07",
                                   chr(0x3164) + chr(0x2028) + chr(0xA0)])
def test_testo_vuoto(env, testo):
    f = Finto()
    out = av.avvisa_operatore(testo, env, invia=f)
    assert out.startswith("Operazione negata: serve un 'testo'") and f.testi == []


@pytest.mark.parametrize("testo", [["x"], {"a": 1}, 5, True, b"x"])
def test_testo_non_stringa(env, testo):
    """V-2 ve #319: una lista o un numero non partono come repr e non consumano posti."""
    f = Finto()
    out, prenotato = av.avvisa_operatore_esito(testo, env, invia=f)
    assert out.startswith("Operazione negata: 'testo' deve essere una stringa")
    assert f.testi == [] and prenotato is False and not (env / av.USO_FILENAME).exists()


@pytest.mark.parametrize("valore", ["0", "-3"])
def test_zero_al_giorno_spegne(env, monkeypatch, valore):
    """V-3 ve #319: GAS_NOTIFICHE_GIORNO=0 spegne lo strumento (prima diventava 1)."""
    monkeypatch.setenv("GAS_NOTIFICHE_GIORNO", valore)
    f = Finto()
    out = av.avvisa_operatore("x", env, invia=f)
    assert out.startswith("Operazione negata: notifiche spente") and f.testi == []


def test_testo_troppo_lungo_non_si_tronca(env):
    f = Finto()
    assert av.avvisa_operatore("a" * av.TESTO_MAX, env, invia=f).startswith("Successo")
    out = av.avvisa_operatore("a" * (av.TESTO_MAX + 1), env, invia=f)
    assert out.startswith("Operazione negata") and "1000 caratteri" in out
    assert len(f.testi) == 1


def test_invisibili_e_controlli_resi_visibili(env):
    """R-611-3: stesso standard dei read-back (rendi_visibili): un testo iniettato non
    rigira il verso (U+202E) né nasconde caratteri; a-capo e tabulazione restano."""
    f = Finto()
    rlo, zw, ls, hangul, nbsp = chr(0x202E), chr(0x200B), chr(0x2028), chr(0x3164), chr(0xA0)
    av.avvisa_operatore(f"riga1\r\nri{rlo}ga2\x1b[31m{zw}\tfine{ls}{hangul}{nbsp}x",
                        env, invia=f)
    assert f.testi == [av.PREFISSO + "riga1\nri<U+202E>ga2<U+001B>[31m<U+200B>\tfine"
                       "<U+2028><U+3164><U+00A0>x"]


def test_esito_dice_se_il_posto_e_prenotato(env, monkeypatch):
    """R-611-4: il kernel conta per turno ogni invio partito, anche fallito."""
    assert av.avvisa_operatore_esito("x", env, invia=Finto())[1] is True
    assert av.avvisa_operatore_esito("x", env, invia=Finto(ok=False, motivo="giù"))[1] is True
    assert av.avvisa_operatore_esito("", env, invia=Finto())[1] is False
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN")
    assert av.avvisa_operatore_esito("x", env, invia=Finto())[1] is False


def test_eccezione_dell_invio_non_esce(env):
    def esplode(testo):
        raise RuntimeError("tok-di-prova")
    out = av.avvisa_operatore("x", env, invia=esplode)
    assert out.startswith("Operazione negata") and "tok-di-prova" not in out


def test_invio_vero_usa_invia_notifica(env, monkeypatch):
    """Senza invio finto si passa da bot.invia_notifica (solo TELEGRAM_ALLOWED_IDS)."""
    import modules.telegram.bot as bot
    visti = []
    monkeypatch.setattr(bot, "invia_notifica", lambda t: (visti.append(t), (True, ""))[1])
    assert av.avvisa_operatore("ciao", env).startswith("Successo")
    assert visti == [av.PREFISSO + "ciao"]


# ── cancello ──

def test_nel_cancello_e_incerto():
    assert gate_classify("avvisa_operatore", '{"testo": "t"}') == GateClass.UNCERTAIN


def test_a_finestra_contaminata_va_alla_firma():
    # una pagina o una mail lette nel turno non fanno partire un messaggio senza firma
    assert libero_dopo_lettura("avvisa_operatore", {"testo": "t"}) is False


def test_il_conto_non_si_scrive_ne_si_legge():
    assert livello_scrittura(av.USO_FILENAME) == LIVELLO_MAI
    assert lettura_consentita(av.USO_FILENAME) is False
