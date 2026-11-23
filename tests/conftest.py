"""Collection di pytest (F-mac-3 / R-190-1): `tests/test_unit_kernel.py` NON è un modulo
pytest ma uno script (`python tests/test_unit_kernel.py`, così lo lancia la CI) che esegue
tutta la suite all'import e chiude con sys.exit: raccolto da `pytest` senza target mandava
la sessione in INTERNALERROR. Si esclude dalla collection; resta eseguito come script.
"""
collect_ignore = ["test_unit_kernel.py"]

# Prova reale 2026-10-11: gas.main() ora carica il `.env` dell'operatore all'avvio.
# Nella suite pytest no: niente chiavi/token reali nei test (stessa linea di R-c4b1-1).
import os as _os
_os.environ["GAS_NO_DOTENV"] = "1"
# Decisione dell'operatore del 2026-11-23: GAS_SOLO_OPUS è acceso di default (tutto a Opus).
# Le suite provano la cascata dei cervelli, quindi lo spengono; il caso acceso lo provano
# i test che lo accendono da sé (kernel T119).
_os.environ["GAS_SOLO_OPUS"] = "0"


# R-809-2: il kernel legge i clienti del CRM anche dalla cartella del repo
# (`gas._RADICE_REPO`, R-808-4). Sul Mac e sul VPS lì c'è il file VERO dei clienti: le suite
# pytest che costruiscono `GasKernel` (notte, manutenzione, voice_contesto…) non devono
# leggerlo, né ereditare un GAS_CRM_DB esportato dalla shell. La suite del kernel (script,
# non pytest) fa lo stesso da sé.
import sys as _sys

import pytest as _pytest


@_pytest.fixture(scope="session")
def _radice_repo_finta(tmp_path_factory):
    return tmp_path_factory.mktemp("repo_finto_crm")


@_pytest.fixture(autouse=True)
def _crm_vero_isolato(monkeypatch, _radice_repo_finta):
    monkeypatch.delenv("GAS_CRM_DB", raising=False)
    # la copia cifrata del CRM non deve mai finire nell'iCloud vero dell'operatore (il suo
    # ~/.zshrc esporta il .env in ogni terminale): senza password resta spenta
    monkeypatch.delenv("GAS_CRM_BACKUP_PASSWORD", raising=False)
    monkeypatch.delenv("GAS_CRM_BACKUP_CIFRATO_DIR", raising=False)
    gas = _sys.modules.get("gas")
    if gas is not None and hasattr(gas, "_RADICE_REPO"):
        monkeypatch.setattr(gas, "_RADICE_REPO", _radice_repo_finta)
