"""Ponte voce → sviluppo (R8, strada A): modules/sviluppo/richieste.py con HTTP finto."""
import json
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.sviluppo import richieste as r  # noqa: E402

TOKEN = "ghp_SEGRETO_DI_PROVA_123"


@pytest.fixture
def env(monkeypatch, tmp_path):
    monkeypatch.setenv("GAS_RICHIESTE_REPO", "Gasss23/Gas-richieste")
    monkeypatch.setenv("GAS_RICHIESTE_TOKEN", TOKEN)
    monkeypatch.delenv("GAS_RICHIESTE_MAX_GIORNO", raising=False)
    return tmp_path


class Finto:
    """HTTP finto: registra le chiamate; repo privato e issue #7 di default."""
    def __init__(self, privato=True, codice_get=200, codice_post=201):
        self.chiamate = []
        self.privato, self.codice_get, self.codice_post = privato, codice_get, codice_post

    def __call__(self, metodo, url, token, corpo):
        self.chiamate.append((metodo, url, token, corpo))
        if metodo == "GET":
            return self.codice_get, {"private": self.privato}
        return self.codice_post, ({"number": 7} if self.codice_post == 201 else None)


def test_crea_issue_con_etichetta_su_repo_privato(env):
    h = Finto()
    out = r.crea_richiesta("Report lead nuovi", "Aggiungi i lead nuovi al report.", env, http=h)
    assert out.startswith("Successo") and "#7" in out
    assert [c[0] for c in h.chiamate] == ["GET", "POST"]
    metodo, url, token, corpo = h.chiamate[1]
    assert url.endswith("/repos/Gasss23/Gas-richieste/issues") and token == TOKEN
    assert corpo["labels"] == ["da-gas"] and corpo["title"] == "Report lead nuovi"
    assert TOKEN not in out
    uso = json.loads((env / r.USO_FILENAME).read_text())
    assert uso == {"giorno": date.today().isoformat(), "n": 1}


def test_repo_pubblico_non_scrive(env):
    h = Finto(privato=False)
    out = r.crea_richiesta("t", "d", env, http=h)
    assert out.startswith("Operazione negata") and "PRIVATO" in out
    assert [c[0] for c in h.chiamate] == ["GET"]  # nessun POST


def test_privato_assente_o_non_booleano_non_scrive(env):
    class SenzaCampo(Finto):
        def __call__(self, metodo, url, token, corpo):
            self.chiamate.append((metodo, url, token, corpo))
            return 200, {"private": "true"}
    h = SenzaCampo()
    assert r.crea_richiesta("t", "d", env, http=h).startswith("Operazione negata")
    assert [c[0] for c in h.chiamate] == ["GET"]


@pytest.mark.parametrize("titolo,descrizione", [("", "d"), ("t", ""), ("  ", "d"), (None, "d")])
def test_campi_vuoti(env, titolo, descrizione):
    h = Finto()
    assert r.crea_richiesta(titolo, descrizione, env, http=h).startswith("Operazione negata")
    assert h.chiamate == []


def test_limiti_di_lunghezza(env):
    h = Finto()
    assert "titolo" in r.crea_richiesta("x" * 121, "d", env, http=h)
    assert "descrizione" in r.crea_richiesta("t", "x" * 4001, env, http=h)
    assert h.chiamate == []


@pytest.mark.parametrize("repo", ["", "solo-nome", "a/b/c", "../x", "a b/c"])
def test_repo_non_configurato_o_strano(env, monkeypatch, repo):
    monkeypatch.setenv("GAS_RICHIESTE_REPO", repo)
    h = Finto()
    assert "non configurato" in r.crea_richiesta("t", "d", env, http=h)
    assert h.chiamate == []


def test_token_da_file_e_assente(env, monkeypatch, tmp_path):
    monkeypatch.delenv("GAS_RICHIESTE_TOKEN")
    f = tmp_path / "tok"
    f.write_text(TOKEN + "\n")
    monkeypatch.setenv("GAS_RICHIESTE_TOKEN_FILE", str(f))
    h = Finto()
    assert r.crea_richiesta("t", "d", env, http=h).startswith("Successo")
    assert h.chiamate[0][2] == TOKEN
    monkeypatch.setenv("GAS_RICHIESTE_TOKEN_FILE", str(tmp_path / "manca"))
    assert "token" in r.crea_richiesta("t", "d", env, http=Finto())


def test_tetto_giornaliero_e_conto_rotto(env, monkeypatch):
    monkeypatch.setenv("GAS_RICHIESTE_MAX_GIORNO", "2")
    uso = env / r.USO_FILENAME
    uso.write_text(json.dumps({"giorno": date.today().isoformat(), "n": 2}))
    h = Finto()
    assert "tetto" in r.crea_richiesta("t", "d", env, http=h) and h.chiamate == []
    uso.write_text(json.dumps({"giorno": "2000-01-01", "n": 99}))  # altro giorno: si riparte
    assert r.crea_richiesta("t", "d", env, http=Finto()).startswith("Successo")
    for rotto in ("{rotto", "[1]", '{"giorno": "x", "n": -1}', '{"n": true}'):
        uso.write_text(rotto)
        h = Finto()
        assert "illeggibile" in r.crea_richiesta("t", "d", env, http=h) and h.chiamate == []


@pytest.mark.parametrize("codice_get,codice_post", [(404, 201), (0, 201), (200, 403), (200, 0)])
def test_errori_http_senza_eccezioni(env, codice_get, codice_post):
    out = r.crea_richiesta("t", "d", env, http=Finto(codice_get=codice_get, codice_post=codice_post))
    assert out.startswith("Operazione negata") and TOKEN not in out
    # R-557-2: il posto si prenota prima del POST, quindi anche un POST fallito conta
    # nel tetto (verso prudente); un GET fallito invece non prenota nulla
    uso = env / r.USO_FILENAME
    if codice_get == 200:
        assert json.loads(uso.read_text())["n"] == 1
    else:
        assert not uso.exists()


def test_http_che_solleva_non_esce(env):
    def esplode(*a):
        raise RuntimeError(TOKEN)
    out = r.crea_richiesta("t", "d", env, http=esplode)
    assert out.startswith("Operazione negata") and TOKEN not in out


def test_strumento_nel_cancello():
    from modules.gate.gate import GateClass, gate_classify, libero_dopo_lettura
    assert gate_classify("richiedi_sviluppo", '{"titolo": "t", "descrizione": "d"}') == GateClass.UNCERTAIN
    # a finestra contaminata va alla firma: una pagina non può chiedere sviluppo
    assert libero_dopo_lettura("richiedi_sviluppo", {"titolo": "t", "descrizione": "d"}) is False


def test_conto_non_scrivibile_niente_richiesta(env, monkeypatch):
    """R-557-2: il posto si prenota prima del POST; se il conto non si scrive, niente issue."""
    monkeypatch.setattr(r, "_registra_uso", lambda p, n: False)
    h = Finto()
    out = r.crea_richiesta("t", "d", env, http=h)
    assert out.startswith("Operazione negata") and "non scrivibile" in out
    assert [c[0] for c in h.chiamate] == ["GET"]


def test_redirect_non_seguiti():
    """R-557-3: l'opener non segue i redirect (il token non va mai su un altro host)."""
    assert r._NoRedirect().redirect_request(None, None, 302, "x", {}, "https://altro.example") is None


def test_token_predefinito_dedicato(monkeypatch):
    """R-557-1: senza configurazione il token si cerca nel file dedicato, mai in agente_token."""
    monkeypatch.delenv("GAS_RICHIESTE_TOKEN", raising=False)
    monkeypatch.delenv("GAS_RICHIESTE_TOKEN_FILE", raising=False)
    assert r._TOKEN_FILE_DEFAULT.endswith("richieste_token")
    assert "agente_token" not in r._TOKEN_FILE_DEFAULT
