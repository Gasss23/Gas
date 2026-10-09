# Report di fine task — 2026-10-08 — R-220-3: tetti di tempo per `gas notte` + timeout HTTP dei provider

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (numero e URL in `reports/handoff.md` §0). Tocca il motore: secondo la regola di merge autonomo l'agente la mergia da solo SOLO se il bot dà `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi installare il timer notturno seguendo `reports/setup_notte.md` (ora con i tetti di tempo, §2c).

## Esito per fetta

- **Fetta 1 — timeout HTTP dei provider in `run_turn` e `rifletti`** (`gas.py`): `FATTA` — 120s (`GAS_PROVIDER_TIMEOUT_SEC`), Ollama locale 600s (`GAS_OLLAMA_TIMEOUT_SEC`, = default SDK, nessun peggioramento del paracadute offline). Prima l'SDK aspettava fino a 600s × 3 tentativi per rung.
- **Fetta 2 — tetti di tempo nel giro notturno** (`modules/notte/notte.py`): `FATTA` — 900s per compito, 7200s per giro, controllo cooperativo tra gli eventi di `run_turn` (generatore chiuso), compiti rimasti saltati con avviso ed exit 1; un `error` oltre il tetto conserva il messaggio vero.
- **Fetta 3 — test** : `FATTA` — kernel T81a–T81d (707 → 711 PASS, 0 FAIL); notte 26 → 35 test; `pytest tests/` 786 passed.
- **Fetta 4 — doc operatore** (`reports/setup_notte.md` §2c): `FATTA`, con il caso peggiore reale (~55 min di sforamento, R-227-2).
- **R-226-4, R-227-1, docstring di R-227-2**: `DEFERITE` — riserve BASSE (test/doc), candidate per GAS di notte; tracciate in `stato_progetto.md` voce 6.
- **Fetta 2 di FASE 4.5 (riepilogo del giro su Telegram al mattino)**: `DEFERITA` — prossima fetta.

## Revisore

Review #226 APPROVATO CON RISERVE (R-226-1 MEDIA, R-226-2, R-226-3 chiuse nella stessa fetta; R-226-4 aperta). Review #227 sulle correzioni: APPROVATO CON RISERVE (R-227-1, R-227-2 BASSE). Verdetti integrali in `reports/handoff.md` §4.

## Anomalie

- `gh` nel container non è autenticato (`GH_TOKEN` rifiutato): la PR si apre e si legge con lo strumento GitHub collegato, la CI si legge dai check della PR.
- Il primo tentativo di commit è stato bloccato dal gate (marcatore creato nello stesso comando del commit): rifatto in due passi, nessun effetto sul contenuto.
