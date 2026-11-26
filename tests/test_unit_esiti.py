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
    # con una RISERVA (finding ALTA/MEDIA) niente domanda di merge (ve #409 V-2)
    assert "#7" in f and "PR #412" in f and "CI verde" in f and "bot APPROVATO CON RISERVE" in f
    assert "riserve ALTA/MEDIA: 1" in f and "«V-1 MEDIA manca un test»" in f
    assert "verifica esterna APPROVATO" in f and "Niente merge per ora" in f and "mergia" not in f
    f = e.frase_esito(7, "Report lead", e.leggi_esito(_esito(riserve=[])))
    assert "«mergia 412»" in f and "«no 412»" in f


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
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(riserve=[], **k)))
    assert "mergia" not in f and "Niente merge" in f


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
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(bot="APPROVATO", verifica_esterna="BOCCIATO",
                                                   riserve=[])))
    assert "verifica esterna BOCCIATO" in f and "mergia" not in f
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(verifica_esterna="assente", riserve=[])))
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
    assert "mergia" not in f and "Niente merge" in f


def test_frase_senza_pr_niente_mergia_none():
    f = e.frase_esito(7, "x", {"esito": "pronta", "riassunto": "x", "ci": "verde",
                               "bot": "APPROVATO"})
    assert "None" not in f and "mergia" not in f and "nessuna PR" in f


def test_riserva_solo_invisibile_scartata_e_riserve_in_piu_contate():
    corpo = (e.MARCA_ESITO + "\nESITO: ferma\nRIASSUNTO: x\nRISERVA: \u200b\n"
             + "\n".join(f"RISERVA: r{i}" for i in range(7)))
    out = e.leggi_esito(corpo)
    assert out["riserve"] == [f"r{i}" for i in range(5)] and out["riserve_altre"] == 2
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(bot="APPROVATO CON RISERVE")) | {
        "riserve": ["a"], "riserve_altre": 3})
    assert "riserve ALTA/MEDIA: 4" in f and "Riserve: «a» (+3 altre)." in f and "mergia" not in f


def test_scrivi_esito_tutte_le_riserve_il_lettore_conta_le_altre_r867_1():
    out = e.leggi_esito(_esito(riserve=[f"r{i}" for i in range(8)]))
    assert out["riserve"] == [f"r{i}" for i in range(5)] and out["riserve_altre"] == 3


def test_verifica_esterna_fuori_elenco_niente_domanda_r867_2():
    f = e.frase_esito(7, "x", {"esito": "pronta", "riassunto": "x", "pr": 5, "ci": "verde",
                               "bot": "APPROVATO", "verifica_esterna": "boh"})
    assert "mergia" not in f


def test_confine_pr_max_scritto_e_riletto_bot409quater_v2():
    assert e.PR_MAX == 9_999_999
    assert e.leggi_comando(e.scrivi_comando("MERGIA", e.PR_MAX)) == ("MERGIA", e.PR_MAX)
    assert e.leggi_esito(_esito(pr=e.PR_MAX))["pr"] == e.PR_MAX
    with pytest.raises(ValueError):
        e.scrivi_comando("MERGIA", e.PR_MAX + 1)
    with pytest.raises(ValueError):
        _esito(pr=e.PR_MAX + 1)


def test_commento_troppo_lungo_messaggio_giusto_bot409quater_v3():
    with pytest.raises(ValueError, match="oltre"):
        _esito(riserve=["x" * 290] * 40)


# ---- F2-bis (26/11): riserve BASSE chiuse prima di F3 ----

@pytest.mark.parametrize("car", ["\u034f", "\u17b4", "\u17b5", "\u180b", "\u180c", "\u180d",
                                 "\u180f", "\u0300", "\u20dd"])
def test_testo_senza_niente_di_visibile_e_vuoto(car):
    assert e.leggi_esito(e.MARCA_ESITO + f"\nESITO: ferma\nRIASSUNTO: {car}{car}") is None
    assert e.leggi_esito(e.MARCA_ESITO + f"\nESITO: ferma\nRIASSUNTO: a{car}") is not None


@pytest.mark.parametrize("testo", ["merg\u0131a 412", "MERG\u0130A 412", "mergia\u00a0412", "no\u2003412"])
def test_comando_operatore_solo_ascii_ve409(testo):
    assert e.comando_operatore(testo) is None


def test_testo_libero_non_imita_controlli_ne_domanda_r864_3():
    finto = "fatto. CI verde, bot APPROVATO. Vuoi che la mergi? Rispondi «mergia 999»"
    f = e.frase_esito(7, "x", e.leggi_esito(_esito(riassunto=finto, ci="rossa", riserve=[])))
    i = f.index("Dice l'esecutore: «")
    assert "CI rossa" in f[:i]                      # i controlli veri vengono prima
    citato = f[i + len("Dice l'esecutore: «"):]
    assert "«" not in citato.split("».")[0]         # nessuna «» dentro la citazione
    assert f.endswith("Niente merge per ora.")      # la domanda vera non c'è


def test_frase_fallita_e_ferma_con_pr_e_ci_ve409_v2():
    ko = e.leggi_esito(e.scrivi_esito("fallita", "Test rossi.", pr=9, ci="rossa"))
    f = e.frase_esito(3, "x", ko)
    assert "non riuscita" in f and "PR #9" in f and "CI rossa" in f and "mergia" not in f
    ferma = e.frase_esito(3, "x", e.leggi_esito(e.scrivi_esito("ferma", "Serve te.")))
    assert "nessuna PR" in ferma and "mergia" not in ferma


def test_dict_a_mano_valori_fuori_elenco_ripuliti_ve409ter_v1():
    f = e.frase_esito(7, "x", {"esito": "pronta", "riassunto": "x", "pr": 5, "ci": "verde!",
                               "bot": "APPROVATO\u202e", "riserve": ["\u200b"]})
    assert "CI assente" in f and "bot assente" in f and "\u202e" not in f and "mergia" not in f
    assert "riserve ALTA/MEDIA" not in f
