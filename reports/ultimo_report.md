# Report di fine task — 2026-10-09 — merge #162 + riserve V-1/V-2/V-3 del bot su #162

## DECISIONI UMANE RICHIESTE

1. Merge della PR #163 (https://github.com/Gasss23/Gas/pull/163). Tocca il motore: per la regola di merge autonomo l'agente la mergia da solo SOLO se il verdetto testuale del bot sull'head è `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi installare il timer notturno seguendo `reports/setup_notte.md`.

## Esito per fetta

- **Merge di #162** (tetti di tempo di `gas notte` + timeout HTTP): `FATTA` — mergiata su richiesta esplicita dell'operatore (verdetto del bot APPROVATO CON RISERVE), merge commit `7995658`.
- **V-2 bot #162 — un solo tentativo extra dell'SDK** (`gas.py`): `FATTA` — `PROVIDER_MAX_RETRIES = 1` (override `GAS_PROVIDER_MAX_RETRIES`, min 0) passato come `max_retries` ai client OpenAI di `run_turn` e `rifletti`. Una risposta lenta oltre i 120s ora costa 2 attese (~4 min) invece di 3 (~6 min) prima di passare al modello successivo, anche di giorno; resta 1 tentativo extra per errori 429/5xx momentanei.
- **V-1 bot #162 — docstring di `modules/notte/notte.py`**: `FATTA` — caso peggiore reale con la formula (4 rung remoti × 2 × 120s + Ollama 2 × 600s ≈ 36 min); `reports/setup_notte.md` allineato. Chiude anche R-227-2.
- **V-3 bot #162 — riga di sintesi dello stat nell'handoff**: `FATTA` — in questo handoff la §2 dichiara che i conteggi di `reports/handoff.md` sono approssimati (il file conta se stesso), come prevede già il template.
- **Test**: `FATTA` — finti OpenAI accettano `max_retries`; T81e (default 1, override, minimo, valore sporco) e T81f (override 0 arriva al client di `run_turn`, mutation verificata). Kernel 711 → 713 PASS, 0 FAIL; `pytest tests/` 786 passed.
- **R-228-1, R-228-2** (riserve della review #228): `FATTA` — chiuse nella stessa fetta (T81f; testo di `stato_progetto.md` voce 6).
- **R-229-1** (manca l'analogo di T81f per `rifletti`): `DEFERITA` — BASSA, solo test; tracciata in `stato_progetto.md` voce 6.

## Revisore

Review #228 APPROVATO CON RISERVE (R-228-1 BASSA, R-228-2 COSMETICA, chiuse). Review #229 sul delta: APPROVATO CON RISERVE (R-229-1 BASSA aperta). Verdetti integrali in `reports/handoff.md` §4.

## Anomalie

- `gh` nel container non è autenticato: la PR si apre e si legge con lo strumento GitHub collegato, la CI si legge dai check della PR.
