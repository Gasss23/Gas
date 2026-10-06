"""F-mac-3: i `win_*_test.py` di questa cartella sono PROBE MANUALI per Windows (microfono,
playback, wake-word, bridge), non test. Il loro nome combacia col pattern di pytest
(*_test.py) e alcuni fanno sys.exit(1) all'import se mancano le dipendenze audio: senza
questa esclusione `pytest` lanciato senza target andava in INTERNALERROR (SystemExit).
"""
collect_ignore_glob = ["win_*_test.py"]
