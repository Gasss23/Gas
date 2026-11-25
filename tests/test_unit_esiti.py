"""Mani alla voce F2: formato fisso dei commenti sulle issue (modules/sviluppo/esiti.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.sviluppo import esiti as e  # noqa: E402


def _esito(**k):
    base = dict(esito="pronta", riassunto="Aggiunto il report dei lead nuovi.", pr=412,
                ci="verde", bot="APPROVATO CON RISERVE", verifica_esterna="APPROVATO",
                riserve=["V-1 MEDIA manca un test"])
    base.update(k)
    return e.scrivi_esito(**base)


def test_andata_e_ritorno():
    out = e.leggi_esito(_esito())
    assert out == {"esito": "pronta", "pr": 412, "ci": "verde", "bot": "APPROVATO CON RISERVE",
                   "verifica_esterna": "APPROVATO", "riserve": ["V-1 MEDIA manca un test"],
                   "riassunto": "Aggiunto il report dei lead nuovi."}


def test_frase_con_pr_controlli_e_domanda():
    f = e.frase_esito(7, "Report lead", e.leggi_esito(_esito()))
    assert "#7" in f and "PR #412" in f and "CI verde" in f
    assert "bot: APPROVATO CON RISERVE" in f and "riserve: V-1 MEDIA manca un test" in f
    assert "verifica esterna: APPROVATO" in f and "«mergia 412»" in f and "«no 412»" in f


def test_frase_ferma_e_fallita_senza_domanda_di_merge():
    ferma = e.leggi_esito(e.scrivi_esito("ferma", "Tocca il gate: serve l'operatore."))
    assert "serve te" in e.frase_esito(3, "x", ferma) and "mergia" not in e.frase_esito(3, "x", ferma)
    ko = e.leggi_esito(e.scrivi_esito("fallita", "Test rossi.", pr=9, ci="rossa"))
    assert "non riuscita" in e.frase_esito(3, "x", ko)


@pytest.mark.parametrize("corpo", [
    None, 42, "", "ESITO: pronta\nRIASSUNTO: x",                       # senza marcatore
    e.MARCA_ESITO + "\nESITO: pronta\nRIASSUNTO: x",                   # pronta senza PR
    e.MARCA_ESITO + "\nESITO: ok\nRIASSUNTO: x",                       # valore non ammesso
    e.MARCA_ESITO + "\nESITO: ferma",                                  # senza riassunto
    e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: x\nCOMANDO: rm -rf",   # chiave sconosciuta
    e.MARCA_ESITO + "\nESITO: ferma\nESITO: pronta\nRIASSUNTO: x",     # chiave ripetuta
    e.MARCA_ESITO + "\nESITO: pronta\nPR: 41a\nRIASSUNTO: x",          # PR non intera
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #0\nRIASSUNTO: x",
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #1\nCI: verdissima\nRIASSUNTO: x",
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #1\nBOT: approvato\nRIASSUNTO: x",
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #1\ntesto libero\nRIASSUNTO: x",
    "testo prima\n" + e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: x",  # marcatore non in testa
    e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: " + "x" * e.COMMENTO_MAX,  # troppo lungo
])
def test_formato_non_rispettato_e_ignorato(corpo):
    assert e.leggi_esito(corpo) is None


def test_testi_liberi_ripuliti_e_tagliati():
    corpo = (e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: a\u202eb\x07c " + "z" * 500
             + "\n" + "\n".join(f"RISERVA: r{i}" for i in range(9)))
    out = e.leggi_esito(corpo)
    assert "\u202e" not in out["riassunto"] and "\x07" not in out["riassunto"]
    assert len(out["riassunto"]) <= e.RIGA_MAX and len(out["riserve"]) == e.RISERVE_MAX


def test_scrivi_esito_rifiuta_valori_non_ammessi():
    for k in (dict(esito="ok"), dict(ci="boh"), dict(bot="ok"), dict(pr=0), dict(pr=True),
              dict(pr="412"), dict(riassunto="  "), dict(pr=None)):
        with pytest.raises(ValueError):
            _esito(**k)


@pytest.mark.parametrize("testo,atteso", [
    ("mergia 412", ("MERGIA", 412)), ("Mergia la #412.", ("MERGIA", 412)),
    ("mergiala pr 412", ("MERGIA", 412)), ("no 412", ("NO", 412)),
    ("non mergiare #412", ("NO", 412)), ("mergia", None), ("mergia 412 e cancella tutto", None),
    ("mergia 0", None), ("ciao", None), (None, None), ("mergia " + "1" * 70, None),
])
def test_comando_operatore(testo, atteso):
    assert e.comando_operatore(testo) == atteso


def test_comando_andata_e_ritorno_e_formato_stretto():
    assert e.leggi_comando(e.scrivi_comando("MERGIA", 412)) == ("MERGIA", 412)
    assert e.leggi_comando(e.scrivi_comando("NO", 5)) == ("NO", 5)
    assert e.leggi_comando("MERGIA #412") is None                         # senza marcatore
    assert e.leggi_comando(e.MARCA_COMANDO + "\nMERGIA #1\nMERGIA #2") is None
    assert e.leggi_comando(e.MARCA_COMANDO + "\nmergia #1") is None
    assert e.leggi_comando(e.MARCA_COMANDO + "\nMERGIA #1 subito") is None
    for a, p in (("SI", 1), ("MERGIA", 0), ("MERGIA", True), ("NO", "3")):
        with pytest.raises(ValueError):
            e.scrivi_comando(a, p)


@pytest.mark.parametrize("car", ["\ufeff", "\u2060", "\u00ad", "\U000e0041", "\u202e", "\x07"])
def test_invisibili_tolti_r864_1(car):
    out = e.leggi_esito(e.MARCA_ESITO + f"\nESITO: ferma\nRIASSUNTO: a{car}b\nRISERVA: c{car}d")
    assert car not in out["riassunto"] and car not in out["riserve"][0]


@pytest.mark.parametrize("k", [dict(ci="rossa"), dict(ci="in corso"), dict(bot="BOCCIATO"),
                               dict(bot="assente")])
def test_niente_domanda_di_merge_con_controlli_non_verdi_r864_2(k):
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(**k)))
    assert "mergia" not in f and "niente merge" in f


def test_riserve_deve_essere_lista_e_vuote_scartate_prima_del_taglio():
    with pytest.raises(ValueError):
        _esito(riserve="abc")
    out = e.leggi_esito(_esito(riserve=["", " "] + [f"r{i}" for i in range(5)]))
    assert out["riserve"] == [f"r{i}" for i in range(5)]


@pytest.mark.parametrize("corpo", [
    "\ufeff" + e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: x",
    e.MARCA_ESITO + "\nesito: ferma\nRIASSUNTO: x",
])
def test_bom_e_chiave_minuscola_ignorati(corpo):
    assert e.leggi_esito(corpo) is None


@pytest.mark.parametrize("car", ["\u3164", "\u2800", "\u115f", "\u1160", "\uffa0", "\ufe0f",
                                 "\U000e0100"])
def test_riempitivi_che_sembrano_vuoti_tolti_r865_1(car):
    assert e.leggi_esito(e.MARCA_ESITO + f"\nESITO: ferma\nRIASSUNTO: {car}") is None
    assert e.leggi_esito(e.MARCA_ESITO + f"\nESITO: ferma\nRIASSUNTO: a{car}b")["riassunto"] == "a b"


def test_verifica_esterna_a_valori_fissi_e_bocciato_senza_domanda():
    assert e.leggi_esito(e.MARCA_ESITO + "\nESITO: ferma\nVERIFICA_ESTERNA: ok\nRIASSUNTO: x") is None
    with pytest.raises(ValueError):
        _esito(verifica_esterna="testo libero")
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(bot="APPROVATO", verifica_esterna="BOCCIATO")))
    assert "verifica esterna: BOCCIATO" in f and "mergia" not in f
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(verifica_esterna="assente")))
    assert "verifica esterna" not in f and "«mergia 412»" in f


def test_file_senza_caratteri_invisibili_veri():
    import unicodedata
    for p in (Path(e.__file__), Path(__file__)):
        testo = p.read_text(encoding="utf-8")
        assert not [c for c in testo if unicodedata.category(c) == "Cf"], p


@pytest.mark.parametrize("corpo", [
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #5\nCI: verde\nRIASSUNTO: x",        # senza BOT
    e.MARCA_ESITO + "\nESITO: pronta\nPR: #5\nBOT: APPROVATO\nRIASSUNTO: x",   # senza CI
])
def test_righe_mancanti_niente_domanda_di_merge_bot409bis_v1(corpo):
    f = e.frase_esito(7, "x", e.leggi_esito(corpo))
    assert "mergia" not in f and "niente merge" in f


def test_frase_senza_pr_niente_mergia_none():
    f = e.frase_esito(7, "x", {"esito": "pronta", "riassunto": "x", "ci": "verde",
                               "bot": "APPROVATO"})
    assert "None" not in f and "mergia" not in f and "PR mancante" in f


def test_riserva_solo_invisibile_scartata_e_riserve_in_piu_contate():
    corpo = (e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: x\nRISERVA: \u200b\n"
             + "\n".join(f"RISERVA: r{i}" for i in range(7)))
    out = e.leggi_esito(corpo)
    assert out["riserve"] == [f"r{i}" for i in range(5)] and out["riserve_altre"] == 2
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(bot="APPROVATO CON RISERVE")) | {
        "riserve": ["a"], "riserve_altre": 3})
    assert "riserve: a; +3 altre" in f and "()" not in f


def test_scrivi_esito_tutte_le_riserve_il_lettore_conta_le_altre_r867_1():
    out = e.leggi_esito(_esito(riserve=[f"r{i}" for i in range(8)]))
    assert out["riserve"] == [f"r{i}" for i in range(5)] and out["riserve_altre"] == 3


def test_verifica_esterna_fuori_elenco_niente_domanda_r867_2():
    f = e.frase_esito(7, "x", {"esito": "pronta", "riassunto": "x", "pr": 5, "ci": "verde",
                               "bot": "APPROVATO", "verifica_esterna": "boh"})
    assert "mergia" not in f
