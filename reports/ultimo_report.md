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
- **R-229-1 / V-1 verifica esterna #163** (manca l'analogo di T81f per `rifletti`): `FATTA` — T81g (mutation verificata). Kernel 713 → 714 PASS, 0 FAIL; `pytest tests/` 786 passed.
- **V-2 verifica esterna #163** (commento di `PROVIDER_TIMEOUT_SEC` diceva x3): `FATTA` — allineato a `PROVIDER_MAX_RETRIES`.
- **V-3 verifica esterna #163 + R-230-1** (~36 min presentato come limite): `FATTA` — docstring di notte.py e setup_notte.md lo dicono ordine di grandezza (timeout per fase di rete, Retry-After fino a 60s per ritentativo).
- **V-4 verifica esterna #163** (voce 6 di `stato_progetto.md` troppo lunga, §11): `DEFERITA` — COSMETICA, riordino del file di stato fuori scope.

## Revisore

Review #228 APPROVATO CON RISERVE (R-228-1, R-228-2 chiuse). Review #229: APPROVATO CON RISERVE (R-229-1 chiusa con T81g). Review #230: APPROVATO CON RISERVE (R-230-1 cosmetica, chiusa). Review #231: APPROVATO. Verdetti integrali in `reports/handoff.md` §4.

## Verifica esterna (#163, prima del secondo commit)

APPROVATO CON RISERVE: V-1, V-2, V-3 chiuse in `f3ff0c6`; V-4 cosmetica deferita. Verdetto integrale in `reports/handoff.md` §7.

## Anomalie

- `gh` nel container non è autenticato: la PR si apre e si legge con lo strumento GitHub collegato, la CI si legge dai check della PR.
- Nei verdetti del revisore incollati in `handoff.md` §4 ho cambiato solo il formato dei riferimenti a file dell'SDK esterno (es. `openai/_constants.py:9-10` → "righe 9-10 dell'SDK") e tolto il prefisso assoluto `/home/user/Gas/`. Motivo: il gate B (`check_verdetto`) controlla che ogni `path:riga` esista nel repo. Il resto del testo è integrale.
- I verdetti del bot e della verifica esterna dell'agente sono in §7 come estratto (FINDING e RACCOMANDAZIONE), con il link alla review integrale del bot sulla PR.
