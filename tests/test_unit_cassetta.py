"""Mani alla voce F3: modules/sviluppo/cassetta.py (avviso, annullo, lettura degli esiti) con
HTTP e Telegram finti, più il comando «annulla richiesta N» nel bot."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.sviluppo import cassetta as c  # noqa: E402
from modules.sviluppo import esiti as e  # noqa: E402
from modules.sviluppo import richieste as r  # noqa: E402

REPO = "Gasss23/Gas-richieste"
TOKEN = "ghp_SEGRETO_DI_PROVA_123"
API = c.API
ADESSO = datetime(2026, 11, 26, 15, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def env(monkeypatch, tmp_path):
    monkeypatch.setenv("GAS_RICHIESTE_REPO", REPO)
    monkeypatch.setenv("GAS_RICHIESTE_TOKEN", TOKEN)
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "Gasss23, esecutore-bot")
    monkeypatch.delenv("GAS_RICHIESTE_CONTROLLO_MIN", raising=False)
    return tmp_path


class Http:
    """GitHub finto: repo privato, issue in un dizionario, commenti in una lista."""

    def __init__(self, privato=True):
        self.privato = privato
        self.issue = {7: {"number": 7, "title": "Report lead", "state": "open",
                          "labels": [{"name": "da-gas"}]}}
        self.commenti = []
        self.chiamate = []
        self.codici = {}  # (metodo, suffisso) → codice forzato

    def __call__(self, metodo, url, token, corpo):
        assert token == TOKEN
        self.chiamate.append((metodo, url, corpo))
        for (m, suff), cod in self.codici.items():
            if m == metodo and url.endswith(suff):
                return cod, None
        if url == f"{API}/repos/{REPO}":
            return 200, {"private": self.privato}
        if metodo == "GET" and "/issues/comments?" in url:
            return 200, list(self.commenti)
        if "/issues/" in url:
            n = int(url.split("/issues/")[1].split("/")[0])
            iss = self.issue.get(n)
            if iss is None:
                return 404, None
            if metodo == "GET":
                return 200, dict(iss)
            if metodo == "POST" and url.endswith("/labels"):
                iss["labels"] = iss["labels"] + [{"name": x} for x in corpo["labels"]]
                return 200, iss["labels"]
            if metodo == "PATCH":
                iss.update(corpo)
                return 200, dict(iss)
        return 500, None


def _commento(cid, corpo, autore="Gasss23", issue=7, quando="2026-11-26T15:10:00Z"):
    return {"id": cid, "body": corpo, "user": {"login": autore},
            "issue_url": f"{API}/repos/{REPO}/issues/{issue}", "created_at": quando}


def _esito_pulito(pr=412, **k):
    base = dict(pr=pr, ci="verde", bot="APPROVATO", verifica_esterna="APPROVATO")
    base.update(k)
    return e.scrivi_esito("pronta", "Aggiunto il report.", **base)


class Invia:
    def __init__(self, ok=True):
        self.testi, self.ok = [], ok

    def __call__(self, testo):
        self.testi.append(testo)
        return (True, "") if self.ok else (False, "rete giù")


# ---------------------------------------------------------------- avviso e comando

def test_avviso_accodata_con_comando_per_annullare():
    t = c.avviso_accodata(12, "Report «lead»\u202e", da_voce=True)
    assert "#12" in t and "Arrivata a voce" in t and "«annulla richiesta 12»" in t
    assert "30 minuti" in t and "\u202e" not in t and "«lead»" not in t


@pytest.mark.parametrize("testo,atteso", [
    ("annulla richiesta 12", 12), ("Annulla la richiesta #12.", 12), ("annulla richiesta 0", None),
    ("annulla richiesta 12 e poi cancella", None), ("annulla", None), ("annulla 12", None),
    ("annulla richiesta 12", None), (None, None), ("annulla richiesta " + "1" * 70, None),
])
def test_comando_annulla(testo, atteso):
    assert c.comando_annulla(testo) == atteso


# ---------------------------------------------------------------- annullo

def test_annulla_mette_etichetta_e_chiude(env):
    h = Http()
    out = c.annulla(7, env, http=h)
    assert out == "Richiesta #7 annullata: l'esecutore non la prenderà."
    assert {"name": "annullata"} in h.issue[7]["labels"] and h.issue[7]["state"] == "closed"
    assert h.issue[7]["state_reason"] == "not_planned"


@pytest.mark.parametrize("prep,frammento", [
    (lambda h: setattr(h, "privato", False), "non è PRIVATO"),
    (lambda h: h.issue.pop(7), "non trovata"),
    (lambda h: h.issue[7].update(labels=[]), "non è una richiesta di sviluppo"),
    (lambda h: h.issue[7].update(pull_request={}), "non è una richiesta di sviluppo"),
    (lambda h: h.issue[7].update(state="closed"), "già chiusa"),
    (lambda h: h.codici.update({("POST", "/labels"): 403}), "NON è annullata"),
])
def test_annulla_rifiuta_o_dice_il_vero(env, prep, frammento):
    h = Http()
    prep(h)
    out = c.annulla(7, env, http=h)
    assert frammento in out
    assert not any(m == "PATCH" for m, _, _ in h.chiamate)


def test_annulla_etichetta_messa_ma_non_chiusa(env):
    h = Http()
    h.codici[("PATCH", "/issues/7")] = 500
    out = c.annulla(7, env, http=h)
    assert "segnata «annullata» ma non chiusa" in out


@pytest.mark.parametrize("n", [0, -1, True, "7", 10_000_000])
def test_annulla_numero_non_valido(env, n):
    h = Http()
    assert c.annulla(n, env, http=h).startswith("Operazione negata") and h.chiamate == []


def test_annulla_senza_configurazione(env, monkeypatch):
    monkeypatch.delenv("GAS_RICHIESTE_REPO")
    assert "non configurati" in c.annulla(7, env, http=Http())


# ---------------------------------------------------------------- lettura degli esiti

def _due_controlli(env, h, inv, adesso=None):
    """Il primo controllo fissa solo il punto di partenza; il secondo legge."""
    adesso = adesso or ADESSO
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=adesso) == 0
    return c.controlla_esiti(env, http=h, invia=inv, adesso=adesso)


def test_primo_controllo_non_manda_niente_e_parte_da_adesso(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 0
    assert inv.testi == [] and not any("comments?" in u for _, u, _ in h.chiamate)
    stato = json.loads((env / c.STATO_FILENAME).read_text())
    assert stato["since"] == "2026-11-26T14:58:00Z"
    assert (env / c.STATO_FILENAME).stat().st_mode & 0o777 == 0o600


def test_esito_pulito_avvisa_e_ricorda_la_domanda(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    assert _due_controlli(env, h, inv) == 1
    assert "Richiesta di sviluppo #7 «Report lead»: fatta" in inv.testi[0]
    assert "«mergia 412»" in inv.testi[0]
    assert c.domanda_aperta(env, 7) == 412
    # di nuovo: già visto, niente secondo avviso
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 0 and len(inv.testi) == 1


def test_esito_con_riserve_avvisa_senza_domanda_e_chiude_quella_vecchia(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h, inv)
    h.commenti.append(_commento(2, _esito_pulito(pr=413, riserve=["V-1 x"]),
                                quando="2026-11-26T15:20:00Z"))
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1
    assert "Niente merge per ora" in inv.testi[-1] and c.domanda_aperta(env, 7) is None


@pytest.mark.parametrize("commento", [
    _commento(1, _esito_pulito(), autore="estraneo"),                  # autore non ammesso
    _commento(1, _esito_pulito().replace("ESITO: pronta", "ESITO: ok")),  # formato rotto
    _commento(1, _esito_pulito(), issue=99),                            # issue inesistente → retry
    _commento(1, "ciao, bel lavoro"),                                   # commento qualunque
    _commento(1, e.scrivi_comando("MERGIA", 412)),                      # un COMANDO di Gas
])
def test_commenti_da_non_avvisare(env, commento):
    h, inv = Http(), Invia()
    h.commenti = [commento]
    assert _due_controlli(env, h, inv) == 0 and inv.testi == []
    assert c.domanda_aperta(env, 7) is None


def test_esito_su_issue_non_da_gas_scartato_e_loggato(env, caplog):
    h, inv = Http(), Invia()
    h.issue[8] = {"number": 8, "title": "altro", "state": "open", "labels": []}
    h.commenti = [_commento(1, _esito_pulito(), issue=8)]
    assert _due_controlli(env, h, inv) == 0
    assert "non da-gas" in caplog.text


def test_senza_autori_ammessi_non_legge_niente(env, monkeypatch, caplog):
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", " ,  ;; ")
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    assert _due_controlli(env, h, inv) == 0 and h.chiamate == []
    assert "GAS_RICHIESTE_AUTORI vuoto" in caplog.text


def test_invio_fallito_si_riprova_al_controllo_dopo(env):
    h = Http()
    h.commenti = [_commento(1, _esito_pulito())]
    inv = Invia(ok=False)
    assert _due_controlli(env, h, inv) == 0 and len(inv.testi) == 1
    inv.ok = True
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1
    assert c.domanda_aperta(env, 7) == 412


def test_api_giu_niente_eccezioni(env):
    h, inv = Http(), Invia()
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)
    h.codici[("GET", "&since=2026-11-26T14:58:00Z")] = 502
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 0

    def esplode(*a):
        raise RuntimeError("boom")
    assert c.controlla_esiti(env, http=esplode, invia=inv, adesso=ADESSO) == 0


def test_stato_rotto_riparte_da_adesso(env):
    (env / c.STATO_FILENAME).write_text("{non json", encoding="utf-8")
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    assert _due_controlli(env, h, inv) == 1


def test_since_avanza_col_margine(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito(), quando="2026-11-26T15:10:00Z")]
    _due_controlli(env, h, inv)
    stato = json.loads((env / c.STATO_FILENAME).read_text())
    assert stato["since"] == "2026-11-26T14:58:00Z"  # min(ultimo, adesso) − 2 minuti
    assert stato["visti"] == [1]


def test_cronometro_uno_alla_volta_e_intervallo(monkeypatch):
    monkeypatch.setenv("GAS_RICHIESTE_CONTROLLO_MIN", "5")
    cr = c.Cronometro()
    assert cr.tocca(1000.0) and not cr.tocca(1001.0)
    assert cr.tocca(1300.0)
    cr.in_corso = True
    assert not cr.tocca(5000.0)


@pytest.mark.parametrize("v,s", [("0", 300), ("abc", 300), ("nan", 300), ("10", 600),
                                 ("1e9", 86400)])
def test_intervallo(monkeypatch, v, s):
    monkeypatch.setenv("GAS_RICHIESTE_CONTROLLO_MIN", v)
    assert c.intervallo_s() == s


# ---------------------------------------------------------------- creazione con avviso

class HttpCrea:
    def __call__(self, metodo, url, token, corpo):
        if metodo == "GET":
            return 200, {"private": True}
        return 201, {"number": 7, "labels": [{"name": "da-gas"}]}


def test_crea_richiesta_avvisa_subito(env):
    visti = []
    out = r.crea_richiesta("Report lead", "Aggiungi i lead.", env, http=HttpCrea(),
                           avvisa=lambda n, t: visti.append((n, t)) or True)
    assert visti == [(7, "Report lead")] and "avvisato su Telegram" in out


@pytest.mark.parametrize("avvisa", [lambda n, t: False,
                                    lambda n, t: (_ for _ in ()).throw(RuntimeError())])
def test_crea_richiesta_avviso_fallito_lo_dice(env, avvisa):
    out = r.crea_richiesta("Report lead", "Aggiungi i lead.", env, http=HttpCrea(), avvisa=avvisa)
    assert out.startswith("Successo: richiesta di sviluppo #7") and "NON è partito" in out


# ---------------------------------------------------------------- bot Telegram

def test_bot_annulla_richiesta_senza_turno(env, monkeypatch):
    import modules.telegram.bot as bot
    testi = []
    monkeypatch.setattr(bot, "_send_text", lambda base, chat, t, *a, **k: testi.append(t))
    chiamate = []
    monkeypatch.setattr(c, "annulla", lambda n, root, http=None: chiamate.append(n) or "annullata!")

    class K:
        root = env

        def run_turn(self, *a, **k):
            raise AssertionError("il modello non deve partire")

    upd = {"update_id": 1, "message": {"chat": {"id": 5}, "text": "annulla richiesta 7"}}
    bot._handle_update("https://x", upd, {5}, K())
    assert chiamate == [7] and testi == ["annullata!"]
    # da un messaggio modificato no
    upd = {"update_id": 2, "edited_message": {"chat": {"id": 5}, "text": "annulla richiesta 7"}}
    bot._handle_update("https://x", upd, {5}, K())
    assert chiamate == [7] and "messaggio modificato" in testi[-1]
    # da una chat non ammessa nemmeno
    upd = {"update_id": 3, "message": {"chat": {"id": 6}, "text": "annulla richiesta 7"}}
    bot._handle_update("https://x", upd, {5}, K())
    assert chiamate == [7]


def test_controllo_in_sottofondo_un_thread_alla_volta(env, monkeypatch):
    import threading
    fatto, via = threading.Event(), threading.Event()
    monkeypatch.setattr(c, "_CRONO", c.Cronometro())

    def lento(root):
        fatto.set()
        via.wait(5)
    assert c.controllo_in_sottofondo(env, lavoro=lento) is True
    assert fatto.wait(5)
    c._CRONO.prossimo = 0  # anche se fosse già ora: uno alla volta
    assert c.controllo_in_sottofondo(env, lavoro=lento) is False
    via.set()


def test_controllo_in_sottofondo_errore_non_blocca(env, monkeypatch):
    import threading
    monkeypatch.setattr(c, "_CRONO", c.Cronometro())
    finito = threading.Event()

    def rotto(root):
        try:
            raise RuntimeError("boom")
        finally:
            finito.set()
    assert c.controllo_in_sottofondo(env, lavoro=rotto)
    assert finito.wait(5)
    for _ in range(50):
        if not c._CRONO.in_corso:
            break
        threading.Event().wait(0.02)
    assert c._CRONO.in_corso is False


def test_bot_delega_il_controllo(env, monkeypatch):
    import modules.telegram.bot as bot
    visti = []
    monkeypatch.setattr(c, "controllo_in_sottofondo", lambda root: visti.append(root) or True)
    bot._controlla_esiti_richieste(env)
    assert visti == [env]


# ---- review #879-MV: riserve chiuse prima del commit ----

def test_gitignore_copre_lo_stato_r879mv_1():
    import subprocess
    radice = Path(__file__).resolve().parents[1]
    for nome in (c.STATO_FILENAME, c.STATO_FILENAME.replace(".json", ".tmp.123.abcd")):
        r_ = subprocess.run(["git", "check-ignore", "-q", nome], cwd=radice)
        assert r_.returncode == 0, nome


def test_tetto_per_controllo_e_al_giorno_r879mv_2(env, monkeypatch):
    h, inv = Http(), Invia()
    h.commenti = [_commento(i, _esito_pulito(), quando=f"2026-11-26T15:1{i}:00Z") for i in range(8)]
    assert _due_controlli(env, h, inv) == c.ESITI_PER_CONTROLLO
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 3  # il resto, non perso
    monkeypatch.setenv("GAS_RICHIESTE_ESITI_GIORNO", "2")
    h.commenti.append(_commento(20, _esito_pulito(), quando="2026-11-26T15:30:00Z"))
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 0  # oggi già 8 > 2
    domani = datetime(2026, 11, 27, 9, 0, 0, tzinfo=timezone.utc)
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=domani) == 1


def test_repo_con_maiuscole_diverse_r879mv_3(env, monkeypatch):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    monkeypatch.setenv("GAS_RICHIESTE_REPO", REPO.lower())
    orig = h.__call__

    class H2(Http):
        def __call__(self, metodo, url, token, corpo):
            return Http.__call__(self, metodo, url.replace(REPO.lower(), REPO), token, corpo)
    h2 = H2()
    h2.commenti = h.commenti
    assert _due_controlli(env, h2, inv) == 1


def test_autore_non_ammesso_in_sospeso_e_recuperato_r879mv_3(env, monkeypatch):
    h, inv = Http(), Invia()
    com = _commento(1, _esito_pulito(), autore="nuovo-esecutore")
    h.commenti = [com]

    class H2(Http):
        def __call__(self, metodo, url, token, corpo):
            if metodo == "GET" and url.endswith("/issues/comments/1"):
                return 200, dict(com)
            return Http.__call__(self, metodo, url, token, corpo)
    h2 = H2()
    h2.commenti = h.commenti
    assert _due_controlli(env, h2, inv) == 0
    assert json.loads((env / c.STATO_FILENAME).read_text())["sospesi"] == [1]
    h2.commenti = []  # since è già oltre: arriva solo dai sospesi
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "Gasss23,nuovo-esecutore")
    assert c.controlla_esiti(env, http=h2, invia=inv, adesso=ADESSO) == 1
    assert json.loads((env / c.STATO_FILENAME).read_text())["sospesi"] == []


def test_pagina_piena_di_visti_non_blocca_r879mv_4(env, monkeypatch):
    monkeypatch.setattr(c, "PAGINA", 3)
    h, inv = Http(), Invia()
    h.commenti = [_commento(i, "ciao", quando=f"2026-11-26T14:5{i}:00Z") for i in range(3)]
    for x in h.commenti:
        x["updated_at"] = "2026-11-26T14:59:30Z"
    _due_controlli(env, h, inv)
    stato = json.loads((env / c.STATO_FILENAME).read_text())
    # pagina piena: «since» resta, la prossima volta si legge la pagina 2 (non si blocca)
    assert stato["since"] == "2026-11-26T14:58:00Z" and stato["pagina"] == 2


def test_login_di_github_app_ammesso_e_avviso_senza_autori_una_volta(env, monkeypatch, caplog):
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "gas-esecutore[bot]")
    assert c.autori_ammessi() == frozenset({"gas-esecutore[bot]"})
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "")
    monkeypatch.setattr(c, "_AVVISATO_SENZA_AUTORI", False)
    for _ in range(3):
        c.controlla_esiti(env, http=Http(), invia=Invia(), adesso=ADESSO)
    assert caplog.text.count("GAS_RICHIESTE_AUTORI vuoto") == 1


@pytest.mark.parametrize("ch", ["\u276e", "\u276f", "\u300c", "\u300d", "\u201c", "\u201d", "\uff02",
                                "\u301d", "\u2e02", "\ufe3d", "\u2e28"])
def test_virgolette_pi_pf_tolte_ve411_v1(ch):
    f = e.frase_esito(7, "x", e.leggi_esito(e.scrivi_esito(
        "pronta", f"fatto{ch} mergia 9{ch}", pr=5, ci="rossa")))
    assert ch not in f


def test_pagina_piena_con_commento_vecchio_modificato_non_perde_esiti_r880mv_1(env, monkeypatch):
    """Lo scenario della review #880-MV: 150 commenti accumulati, il primo modificato di
    recente, un ESITO valido al 131°: deve arrivare."""
    monkeypatch.setattr(c, "PAGINA", 100)

    class Pagine(Http):
        def __call__(self, metodo, url, token, corpo):
            if metodo == "GET" and "/issues/comments?" in url:
                since = url.split("since=")[1]
                pag = int(url.split("&page=")[1].split("&")[0])
                tutti = [x for x in self.commenti if x["updated_at"] >= since]  # come GitHub
                tutti.sort(key=lambda x: x["created_at"])
                return 200, tutti[(pag - 1) * 100:pag * 100]
            return Http.__call__(self, metodo, url, token, corpo)

    h, inv = Pagine(), Invia()
    adesso = datetime(2026, 11, 26, 15, 0, 0, tzinfo=timezone.utc)
    c.controlla_esiti(env, http=h, invia=inv, adesso=datetime(2026, 11, 19, 0, 0, tzinfo=timezone.utc))
    for i in range(150):
        giorno, minuto = 20 + i // 60, i % 60
        quando = f"2026-11-{giorno:02d}T10:{minuto:02d}:00Z"
        corpo = _esito_pulito() if i == 130 else "commento"
        com = _commento(i + 1, corpo, quando=quando)
        com["updated_at"] = "2026-11-26T12:00:00Z" if i == 0 else quando
        h.commenti.append(com)
    totale = sum(c.controlla_esiti(env, http=h, invia=inv, adesso=adesso) for _ in range(4))
    stato = json.loads((env / c.STATO_FILENAME).read_text())
    assert stato["pagina"] == 1  # finito il giro delle pagine
    assert totale == 1 and "«mergia 412»" in inv.testi[0]


def test_apostrofi_e_parentesi_restano_leggibili_r880mv_2():
    f = e.frase_esito(7, "x", e.leggi_esito(e.scrivi_esito(
        "ferma", "l\u2019operatore \uff08nota\uff09")))
    assert "l'operatore \uff08nota\uff09" in f


def test_troppe_pagine_riparte_da_adesso(env, monkeypatch, caplog):
    monkeypatch.setattr(c, "PAGINA", 2)
    monkeypatch.setattr(c, "PAGINE_MAX", 2)
    h, inv = Http(), Invia()
    h.commenti = [_commento(i, "x", quando="2026-11-26T14:59:00Z") for i in range(2)]
    for com in h.commenti:
        com["updated_at"] = "2026-11-26T14:59:00Z"
    _due_controlli(env, h, inv)                       # pagina 1 piena → pagina 2
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)  # pagina 2 piena = ultima ammessa
    stato = json.loads((env / c.STATO_FILENAME).read_text())
    assert stato["pagina"] == 1 and stato["since"] == "2026-11-26T14:58:00Z"
    assert "riparto da adesso" in caplog.text


# ---- verifica esterna e bot sulla #412 (head 45f739d8) ----

def test_stato_non_scrivibile_niente_avvisi_ripetuti_ve412_v1(env, monkeypatch, caplog):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)  # punto di partenza
    monkeypatch.setattr(c, "_scrivi_stato", lambda root, stato: False)
    for _ in range(4):
        c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)
    assert inv.testi == [] and "NON avvisato" in caplog.text


def test_issue_sparita_non_blocca_la_fila_ve412_v2(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito(), issue=99, quando="2026-11-26T15:01:00Z"),
                  _commento(2, _esito_pulito(), issue=7, quando="2026-11-26T15:02:00Z")]
    assert _due_controlli(env, h, inv) == 1 and "#7" in inv.testi[0]


def test_errore_transitorio_sulla_issue_aspetta(env):
    h, inv = Http(), Invia()
    h.codici[("GET", "/issues/7")] = 502
    h.commenti = [_commento(1, _esito_pulito())]
    assert _due_controlli(env, h, inv) == 0
    del h.codici[("GET", "/issues/7")]
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1


def test_repo_non_privato_niente_esiti_ve412_v4(env, caplog):
    h, inv = Http(privato=False), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    assert _due_controlli(env, h, inv) == 0 and "non è PRIVATO" in caplog.text


def test_esito_vecchio_non_riscrive_la_domanda_bot412_v3(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(2, _esito_pulito(pr=500), quando="2026-11-26T15:20:00Z")]
    _due_controlli(env, h, inv)
    assert c.domanda_aperta(env, 7) == 500
    # un esito più vecchio (recuperato tardi) non la cambia
    h.commenti.append(_commento(1, _esito_pulito(pr=400), quando="2026-11-26T15:10:00Z"))
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)
    assert c.domanda_aperta(env, 7) == 500


def test_invio_fallito_non_consuma_il_tetto(env, monkeypatch):
    monkeypatch.setenv("GAS_RICHIESTE_ESITI_GIORNO", "1")
    h = Http()
    h.commenti = [_commento(1, _esito_pulito())]
    inv = Invia(ok=False)
    _due_controlli(env, h, inv)
    inv.ok = True
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1


def test_lapide_esito_vecchio_non_riapre_la_domanda_r882mv_1(env, monkeypatch):
    h, inv = Http(), Invia()
    vecchio = _commento(1, _esito_pulito(pr=400), autore="tardivo", quando="2026-11-26T15:01:00Z")
    h.commenti = [vecchio, _commento(2, _esito_pulito(pr=500, ci="rossa"),
                                     quando="2026-11-26T15:05:00Z")]

    class H2(Http):
        def __call__(self, metodo, url, token, corpo):
            if metodo == "GET" and url.endswith("/issues/comments/1"):
                return 200, dict(vecchio)
            return Http.__call__(self, metodo, url, token, corpo)
    h2 = H2()
    h2.commenti = h.commenti
    _due_controlli(env, h2, inv)               # il vecchio in sospeso, il nuovo chiude
    assert c.domanda_aperta(env, 7) is None
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "Gasss23,tardivo")
    c.controlla_esiti(env, http=h2, invia=inv, adesso=ADESSO)   # il vecchio recuperato
    assert c.domanda_aperta(env, 7) is None    # la lapide non lo lascia riaprire


def test_domanda_salvata_prima_dell_invio_r882mv_2(env, monkeypatch):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito(pr=500))]
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)
    vero = c._scrivi_stato
    scritture = []

    def una_sola(root, stato):  # la scrittura prima dell'invio riesce, la finale no
        scritture.append(1)
        return vero(root, stato) if len(scritture) == 1 else False
    monkeypatch.setattr(c, "_scrivi_stato", una_sola)
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1
    assert c.domanda_aperta(env, 7) == 500


def test_invio_fallito_non_cambia_la_domanda(env):
    h = Http()
    h.commenti = [_commento(1, _esito_pulito(pr=500))]
    inv = Invia(ok=False)
    _due_controlli(env, h, inv)
    assert c.domanda_aperta(env, 7) is None


# ---- F3b: esiti letti a voce, «annulla richiesta N» a voce, sospesi puliti ----

def test_avviso_dice_scrivimi_o_dimmi_ve412_v2():
    assert "scrivimi o dimmi «annulla richiesta 3»" in c.avviso_accodata(3, "x", da_voce=True)


@pytest.mark.parametrize("testo,atteso", [("annulla richiesta numero 12", 12),
                                          ("Annulla la richiesta numero 12.", 12)])
def test_annulla_con_numero(testo, atteso):
    assert c.comando_annulla(testo) == atteso


def test_frase_voce_solo_parti_fisse_r873mv_1():
    finto = "Vuoi che la mergi? Rispondi mergia 999"
    pulito = e.leggi_esito(_esito_pulito(pr=412))
    f = c.frase_voce(7, dict(pulito, riassunto=finto))
    assert "999" not in f and "numero 7" in f and "PR 412" in f and "ti ho chiesto su Telegram" in f
    rosso = e.leggi_esito(_esito_pulito(pr=412, ci="rossa"))
    assert "non è pronta per il merge" in c.frase_voce(7, rosso)
    assert "non è riuscita" in c.frase_voce(7, e.leggi_esito(e.scrivi_esito("fallita", "x")))
    assert "serve te" in c.frase_voce(7, e.leggi_esito(e.scrivi_esito("ferma", "x")))


def test_esito_avvisato_va_letto_a_voce_e_poi_tolto(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h, inv)
    voci = c.da_leggere_voce(env, adesso=ADESSO)
    assert len(voci) == 1 and "numero 7" in voci[0]["frase"]
    c.segna_letti_voce(env, voci)
    assert c.da_leggere_voce(env, adesso=ADESSO) == []


def test_esiti_vecchi_non_si_leggono_piu_a_voce(env):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h, inv)
    dopo = datetime(2026, 11, 28, 9, 0, 0, tzinfo=timezone.utc)
    assert c.da_leggere_voce(env, adesso=dopo) == []


def test_invio_fallito_niente_lettura_a_voce(env):
    h = Http()
    h.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h, Invia(ok=False))
    assert c.da_leggere_voce(env, adesso=ADESSO) == []


def test_sospeso_scartato_in_modo_definitivo_esce_dai_sospesi_bot412_v1(env, monkeypatch):
    h, inv = Http(), Invia()
    h.issue[8] = {"number": 8, "title": "altro", "state": "open", "labels": []}
    com = _commento(1, _esito_pulito(), autore="tardivo", issue=8)
    h.commenti = [com]

    class H2(Http):
        def __call__(self, metodo, url, token, corpo):
            if metodo == "GET" and url.endswith("/issues/comments/1"):
                return 200, dict(com)
            return Http.__call__(self, metodo, url, token, corpo)
    h2 = H2()
    h2.issue, h2.commenti = h.issue, h.commenti
    _due_controlli(env, h2, inv)
    assert json.loads((env / c.STATO_FILENAME).read_text())["sospesi"] == [1]
    monkeypatch.setenv("GAS_RICHIESTE_AUTORI", "Gasss23,tardivo")
    h2.commenti = []
    c.controlla_esiti(env, http=h2, invia=inv, adesso=ADESSO)
    assert json.loads((env / c.STATO_FILENAME).read_text())["sospesi"] == [] and inv.testi == []


def test_annulla_parlato(env, monkeypatch):
    monkeypatch.setattr(c, "annulla", lambda n, root, http=None: f"annullata {n}")
    assert c.annulla_parlato("annulla richiesta 4", env) == "annullata 4"
    assert c.annulla_parlato("che ore sono", env) is None


def test_vocale_telegram_annulla_senza_turno(env, monkeypatch):
    import modules.telegram.bot as bot
    testi = []
    monkeypatch.setattr(bot, "_send_text", lambda base, chat, t, *a, **k: testi.append(t))
    monkeypatch.setattr(c, "annulla", lambda n, root, http=None: f"annullata {n}")

    class K:
        root = env

        def run_turn(self, *a, **k):
            raise AssertionError("il modello non deve partire")
    bot._gestisci_parlato("https://x", 5, "annulla richiesta 7", K())
    assert len(testi) == 1 and "annullata 7" in testi[0] and "Ho capito" in testi[0]



def _handler_con_root(root):
    from modules.voice.server import VoiceHandler

    class K:
        pass
    h = VoiceHandler.__new__(VoiceHandler)
    h.kernel = K()
    h.kernel.root = root
    return h


def test_server_voce_dice_gli_esiti_e_li_segna_dopo(env):
    h0, inv = Http(), Invia()
    h0.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h0, inv, adesso=datetime.now(timezone.utc))  # bot #414 V-1: niente data fissa
    h = _handler_con_root(env)
    frase = h._compiti_finiti()
    assert "richiesta di sviluppo numero 7" in frase
    assert len(c.da_leggere_voce(env)) == 1      # non ancora segnato: consegna non avvenuta
    h._segna_finiti_letti()
    assert c.da_leggere_voce(env) == []


def test_server_voce_annulla_richiesta(env, monkeypatch):
    monkeypatch.setattr(c, "annulla", lambda n, root, http=None: f"annullata {n}")
    h = _handler_con_root(env)
    assert h._annulla_richiesta("annulla richiesta 9") == "annullata 9"
    assert h._annulla_richiesta("che tempo fa") is None


def test_server_voce_esiti_azzerati_a_ogni_richiesta(env):
    from modules.voice.server import VoiceHandler
    h = VoiceHandler.__new__(VoiceHandler)
    h.path = "/non-esiste"
    h.headers = {}
    h._send_json = lambda code, payload: None
    h._esiti_voce = [{"id": 1}]
    h.do_POST()
    assert h._esiti_voce is None



def test_letti_voce_in_file_a_parte_niente_corse_r884mv_1(env):
    h0, inv = Http(), Invia()
    h0.commenti = [_commento(1, _esito_pulito())]
    _due_controlli(env, h0, inv, adesso=datetime.now(timezone.utc))  # bot #414 V-1: niente data fissa
    prima = (env / c.STATO_FILENAME).read_text()
    c.segna_letti_voce(env, c.da_leggere_voce(env))
    assert (env / c.STATO_FILENAME).read_text() == prima      # lo stato del bot non si tocca
    assert c.da_leggere_voce(env) == []
    # il bot riscrive il suo stato (come in una corsa): la lettura resta segnata
    c.controlla_esiti(env, http=h0, invia=inv, adesso=datetime.now(timezone.utc))
    assert c.da_leggere_voce(env) == [] and len(inv.testi) == 1
    assert (env / c.LETTI_FILENAME).stat().st_mode & 0o777 == 0o600
    import subprocess
    radice = Path(__file__).resolve().parents[1]
    assert subprocess.run(["git", "check-ignore", "-q", c.LETTI_FILENAME], cwd=radice).returncode == 0


def test_annullo_a_voce_solo_fuori_dal_seguito_r884mv_2():
    """Guardia statica: in do_POST la chiamata a _annulla_richiesta sta dentro il ramo
    «if not self._seguito():», così il parlato della stanza (seguito) non annulla."""
    import ast
    import inspect
    import textwrap
    from modules.voice.server import VoiceHandler
    albero = ast.parse(textwrap.dedent(inspect.getsource(VoiceHandler.do_POST)))
    trovate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.If):
            t = nodo.test
            fuori_seguito = (isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not)
                             and isinstance(t.operand, ast.Call)
                             and getattr(t.operand.func, "attr", "") == "_seguito")
            for figlio in ast.walk(ast.Module(body=nodo.body, type_ignores=[])):
                if isinstance(figlio, ast.Call) and getattr(figlio.func, "attr", "") == "_annulla_richiesta":
                    trovate.append(fuori_seguito)
    assert any(trovate)  # almeno un «if» che la racchiude è «fuori dal seguito»
    assert sum(1 for n in ast.walk(albero) if isinstance(n, ast.Call)
               and getattr(n.func, "attr", "") == "_annulla_richiesta") == 1



def test_test_a_voce_reggono_anche_domani(env, monkeypatch):
    """Bot #414 V-1: la lettura a voce non dipende dal giorno in cui girano i test."""
    domani = datetime.now(timezone.utc).replace(microsecond=0) + __import__("datetime").timedelta(days=2)
    h0, inv = Http(), Invia()
    for x in [_commento(1, _esito_pulito(), quando=domani.strftime("%Y-%m-%dT%H:%M:%SZ"))]:
        h0.commenti.append(x)
    _due_controlli(env, h0, inv, adesso=domani)
    assert len(c.da_leggere_voce(env, adesso=domani)) == 1


@pytest.mark.parametrize("testo", ["annulla richiesta dodici", "annulla la richiesta numero dodici",
                                   "annulla richiesta"])
def test_annullo_senza_numero_in_cifre_risposta_chiara_bot414_v2(env, testo):
    out = c.annulla_parlato(testo, env)
    assert out is not None and "in cifre" in out


def test_vocale_telegram_annullo_prima_di_forte_bot414_v2(env, monkeypatch):
    import modules.telegram.bot as bot
    testi = []
    monkeypatch.setattr(bot, "_send_text", lambda base, chat, t, *a, **k: testi.append(t))
    monkeypatch.setattr(c, "annulla", lambda n, root, http=None: f"annullata {n}")

    class K:
        root = env

        def run_turn(self, *a, **k):
            raise AssertionError("il modello non deve partire")
    bot._gestisci_parlato("https://x", 5, "forte annulla richiesta 7", K())
    # come sul Mac: «forte …» non è l'annullo, va al turno: qui il turno esplode, quindi
    # basta che l'annullo NON sia scattato
    assert not any("annullata" in t for t in testi)


def test_da_leggere_salvato_insieme_allo_stato_bot414_v3(env, monkeypatch):
    h, inv = Http(), Invia()
    h.commenti = [_commento(1, _esito_pulito())]
    c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO)
    vero = c._scrivi_stato
    scritture = []

    def una_sola(root, stato):
        scritture.append(1)
        return vero(root, stato) if len(scritture) == 1 else False
    monkeypatch.setattr(c, "_scrivi_stato", una_sola)
    assert c.controlla_esiti(env, http=h, invia=inv, adesso=ADESSO) == 1
    assert len(c.da_leggere_voce(env, adesso=ADESSO)) == 1



@pytest.mark.parametrize("testo", ["annulla la richiesta che ti ho fatto prima",
                                   "Annulla la richiesta di ferie per domani mattina.",
                                   "annulla la richiesta di prima"])
def test_frasi_normali_vanno_al_modello_r886mv_1(env, testo):
    assert c.annulla_parlato(testo, env) is None


def test_annulla_n_punto():
    assert c.comando_annulla("annulla richiesta n. 12") == 12
