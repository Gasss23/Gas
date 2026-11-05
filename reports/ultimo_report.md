# Ultimo report — 2026-11-05 — fetta 40 (chat Mani): soglia della voce predefinita 200

## DECISIONI UMANE RICHIESTE

1. Merge della PR #333 (https://github.com/Gasss23/Gas/pull/333): review #667 APPROVATO CON RISERVE e PR che tocca il perimetro, quindi decide l'operatore tramite M1.

## Esito

- **Fetta 40 — soglia della voce 200**: FATTA. `GAS_ASCOLTO_VOCE_RMS` predefinito da 500 a 200 (costante `VOCE_RMS_PREDEFINITO` in `clients/voice/ascolto.py`, usata da `Ascolto` e da `main`); tabella di `scripts/voce/LEGGIMI.md` a 200 con la nota per le stanze rumorose; 3 test nuovi (5 casi) in `tests/test_unit_voce_ascolto.py`, mutanti con 500 uccisi; suite voce 154 passed.
- **Ripartenza della chat Mani (b7f2c23)**: era sul branch remoto e nella PR #333 ma non in main; unita con un merge (niente force-push), resta nella stessa PR.
- Riserve basse della fetta 39 (thread di lettura, bip su errore TTS, lista bianca del formato, …): DEFERITE — M1 ha chiesto solo la soglia.

## Verdetti dopo la PR (giro su 2c8cd2a)

- Bot (verifica-bot): APPROVATO CON RISERVE, check neutral (PR nel perimetro: decide l'operatore). V-1 BASSA (privacy di R-667-1: rumore continuo → fino a ~150 s di audio della stanza inviati), V-2 COSMETICA (base della PR su GitHub vecchia).
- Verifica esterna: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/333#issuecomment-6665009996). V-1 BASSA (R-667-2 sovrastimata: un default a 50 fa fallire 3 test), V-2 BASSA (base vecchia), V-3 BASSA (= R-667-1), V-4 COSMETICA (§6 sulla CI di 4f80d9d).
- Tutte registrate in stato_progetto (blocco fetta 40) senza altri giri: nessuna ALTA o MEDIA.

## Merge di main e merge della PR

- Sì dell'operatore alla #333 (via M1, 5 novembre). Main era andata avanti con la PR #334 di M2 (voce V13): merge di main in b00c506, conflitti solo nei report (handoff, ultimo_report e diff_sessione dal lato Mani; memoria del revisore con le righe di entrambi i lati; stato_progetto riga 4 col prefisso della fetta 40). Il codice è quello di main più la fetta 40, senza altre modifiche. Review #670 APPROVATO. Suite voce (ascolto, server, stt): 358 passed.

## Anomalie

- Il revisore ha lanciato per errore `git stash --keep-index` sul repo vero; l'ha annullato subito, index intatto (verificato anche da me: stesso diff staged, nessuno stash).
- Nell'ambiente del revisore 21 test della suite voce fallivano per `openai` mancante (uguali sulla base); nel mio venv con requirements completi: 154 passed.
