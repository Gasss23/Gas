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
