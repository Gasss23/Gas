"""Caricamento del `.env` all'avvio della CLI (`gas._carica_dotenv`, prova reale sul
Mac 2026-10-11: il giro notturno da launchd non vedeva GAS_DAILY_TOKEN_BUDGET)."""
import logging
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gas


@pytest.fixture
def env(monkeypatch):
    """Ambiente finto: il loader scrive in os.environ, che qui è una copia usa e getta."""
    finto = {k: v for k, v in os.environ.items() if k != "GAS_NO_DOTENV"}
    monkeypatch.setattr(os, "environ", finto)
    return finto


def _scrivi(tmp_path, testo: str) -> Path:
    p = tmp_path / ".env"
    p.write_text(testo, encoding="utf-8")
    return p


def test_formati_ammessi(env, tmp_path):
    p = _scrivi(tmp_path, (
        "# commento\n\n"
        "GAS_T_A=1\n"
        "export GAS_T_B = due \n"
        "GAS_T_C='tre # non commento'\n"
        'GAS_T_D="quattro"\n'
        "GAS_T_E=cinque # commento\n"
        "GAS_T_F=\n"
        "GAS_T_G=a#b\n"
    ))
    caricate = gas._carica_dotenv(p)
    assert caricate == ["GAS_T_A", "GAS_T_B", "GAS_T_C", "GAS_T_D", "GAS_T_E",
                        "GAS_T_F", "GAS_T_G"]
    assert env["GAS_T_A"] == "1" and env["GAS_T_B"] == "due"
    assert env["GAS_T_C"] == "tre # non commento" and env["GAS_T_D"] == "quattro"
    assert env["GAS_T_E"] == "cinque" and env["GAS_T_F"] == "" and env["GAS_T_G"] == "a#b"


def test_virgolette_seguite_da_commento_e_bom(env, tmp_path):
    """R-260-1 (zsh accettava `"v" # commento`) e R-260-2 (BOM UTF-8 in testa)."""
    p = tmp_path / ".env"
    p.write_bytes('\ufeffGAS_T_BOM=1\nGAS_T_QC="v # dentro" # fuori\n'
                  "GAS_T_QS='w'#attaccato\nGAS_T_QQ=\"a\" # c \"d\"\n".encode("utf-8"))
    assert gas._carica_dotenv(p) == ["GAS_T_BOM", "GAS_T_QC", "GAS_T_QQ"]
    assert env["GAS_T_QQ"] == "a"
    assert env["GAS_T_BOM"] == "1" and env["GAS_T_QC"] == "v # dentro"
    assert "GAS_T_QS" not in env


def test_non_sovrascrive_ambiente_esistente(env, tmp_path):
    """Shell, plist di launchd e systemd vincono sul file."""
    env["GAS_T_X"] = "dalla-shell"
    env["GAS_T_VUOTA"] = ""
    gas._carica_dotenv(_scrivi(tmp_path, "GAS_T_X=dal-file\nGAS_T_VUOTA=pieno\n"))
    assert env["GAS_T_X"] == "dalla-shell" and env["GAS_T_VUOTA"] == ""


def test_righe_malformate_ignorate_senza_valore_nel_log(env, tmp_path, caplog):
    p = _scrivi(tmp_path, "SENZA_UGUALE\n1NOME=x\nNOME-TRATTINO=x\n"
                          "GAS_T_Q='segreto-aperto\nGAS_T_OK=si\n")
    with caplog.at_level(logging.WARNING):
        assert gas._carica_dotenv(p) == ["GAS_T_OK"]
    assert "GAS_T_Q" not in env and "1NOME" not in env
    assert "segreto-aperto" not in caplog.text
    assert caplog.text.count("ignorata") == 4


def test_file_assente_o_illeggibile_fail_safe(env, tmp_path, caplog):
    assert gas._carica_dotenv(tmp_path / "manca.env") == []
    cartella = tmp_path / "dir.env"
    cartella.mkdir()
    with caplog.at_level(logging.WARNING):
        assert gas._carica_dotenv(cartella) == []
    assert "non leggibile" in caplog.text


def test_byte_non_utf8_fail_safe(env, tmp_path, caplog):
    p = tmp_path / ".env"
    p.write_bytes(b"GAS_T_L=caf\xe9\n")
    with caplog.at_level(logging.WARNING):
        assert gas._carica_dotenv(p) == []
    assert "GAS_T_L" not in env


def test_spento_con_gas_no_dotenv(env, tmp_path):
    env["GAS_NO_DOTENV"] = "1"
    assert gas._carica_dotenv(_scrivi(tmp_path, "GAS_T_S=1\n")) == []
    assert "GAS_T_S" not in env


def test_percorso_di_default_accanto_a_gas_py(env, monkeypatch, tmp_path):
    """Senza argomento legge il .env nella cartella di gas.py, non nella cwd."""
    letti = []
    orig = Path.read_text
    def spia(self, *a, **kw):
        letti.append(self)
        return "GAS_T_DEF=ok\n"
    monkeypatch.setattr(Path, "read_text", spia)
    monkeypatch.chdir(tmp_path)
    assert gas._carica_dotenv() == ["GAS_T_DEF"]
    assert letti == [Path(gas.__file__).resolve().parent / ".env"]


def test_main_carica_il_dotenv_prima_del_comando(monkeypatch):
    ordine = []
    monkeypatch.setattr(gas, "_carica_dotenv", lambda: ordine.append("dotenv") or [])
    monkeypatch.setattr(gas, "notte_cmd", lambda: ordine.append("notte") or 0)
    monkeypatch.setattr(sys, "argv", ["gas.py", "notte"])
    with pytest.raises(SystemExit):
        gas.main()
    assert ordine == ["dotenv", "notte"]


def test_suite_pytest_spegne_il_dotenv():
    """conftest.py: la suite non deve mai caricare il .env reale dell'operatore."""
    assert os.environ.get("GAS_NO_DOTENV") == "1"


def test_nomi_caricati_finiscono_in_dotenv_caricate(env, tmp_path, monkeypatch):
    """R-540-1: il doctor sa che GAS_CLAUDE_BIN viene dal `.env` solo se il loader lo
    registra; se vince la shell il nome non entra (il timer non lo vedrebbe)."""
    monkeypatch.setattr(gas, "_DOTENV_CARICATE", set())
    env["GAS_T_SHELL"] = "dalla-shell"
    gas._carica_dotenv(_scrivi(tmp_path, "GAS_T_FILE=1\nGAS_T_SHELL=dal-file\n"))
    assert gas._DOTENV_CARICATE == {"GAS_T_FILE"}


def test_valori_scavalcati_dalla_shell_finiscono_in_dotenv_scavalcate(env, tmp_path, monkeypatch):
    """V-1 ve #290: il doctor sa che la shell scavalca un valore DIVERSO del `.env`
    (di notte vale quello del `.env`). Stesso valore → niente; solo i nomi, mai i valori."""
    monkeypatch.setattr(gas, "_DOTENV_CARICATE", set())
    monkeypatch.setattr(gas, "_DOTENV_SCAVALCATE", set())
    env["GAS_T_DIVERSA"] = "0"
    env["GAS_T_UGUALE"] = "1"
    gas._carica_dotenv(_scrivi(tmp_path, "GAS_T_DIVERSA=1\nGAS_T_UGUALE=1\nGAS_T_NUOVA=x\n"))
    assert gas._DOTENV_SCAVALCATE == {"GAS_T_DIVERSA"}
    assert gas._DOTENV_CARICATE == {"GAS_T_NUOVA"}
    assert env["GAS_T_DIVERSA"] == "0"
