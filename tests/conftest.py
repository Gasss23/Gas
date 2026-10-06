"""Collection di pytest (F-mac-3 / R-190-1): `tests/test_unit_kernel.py` NON è un modulo
pytest ma uno script (`python tests/test_unit_kernel.py`, così lo lancia la CI) che esegue
tutta la suite all'import e chiude con sys.exit: raccolto da `pytest` senza target mandava
la sessione in INTERNALERROR. Si esclude dalla collection; resta eseguito come script.
"""
collect_ignore = ["test_unit_kernel.py"]
