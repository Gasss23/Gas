# Ultimo report — 2026-11-05 — fetta 40 (chat Mani): soglia della voce predefinita 200

## DECISIONI UMANE RICHIESTE

1. Merge della PR #333 (https://github.com/Gasss23/Gas/pull/333): review #667 APPROVATO CON RISERVE e PR che tocca il perimetro, quindi decide l'operatore tramite M1.

## Esito

- **Fetta 40 — soglia della voce 200**: FATTA. `GAS_ASCOLTO_VOCE_RMS` predefinito da 500 a 200 (costante `VOCE_RMS_PREDEFINITO` in `clients/voice/ascolto.py`, usata da `Ascolto` e da `main`); tabella di `scripts/voce/LEGGIMI.md` a 200 con la nota per le stanze rumorose; 3 test nuovi (5 casi) in `tests/test_unit_voce_ascolto.py`, mutanti con 500 uccisi; suite voce 154 passed.
- **Ripartenza della chat Mani (b7f2c23)**: era sul branch remoto e nella PR #333 ma non in main; unita con un merge (niente force-push), resta nella stessa PR.
- Riserve basse della fetta 39 (thread di lettura, bip su errore TTS, lista bianca del formato, …): DEFERITE — M1 ha chiesto solo la soglia.

## Anomalie

- Il revisore ha lanciato per errore `git stash --keep-index` sul repo vero; l'ha annullato subito, index intatto (verificato anche da me: stesso diff staged, nessuno stash).
- Nell'ambiente del revisore 21 test della suite voce fallivano per `openai` mancante (uguali sulla base); nel mio venv con requirements completi: 154 passed.
