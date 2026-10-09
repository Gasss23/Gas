# Report di fine task — 2026-10-09 — merge #164 + test ermetici (PR #165)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #165 (https://github.com/Gasss23/Gas/pull/165): solo test. Per la regola di merge autonomo l'agente la mergia da solo SOLO se il verdetto testuale del bot sull'head è `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. V-2 bot #163 (ancora aperta): il gate B (`scripts/check_verdetto.py`) rifiuta i riferimenti `path:riga` a file fuori dal repo e spinge a riscrivere i verdetti del revisore. Cambiarlo tocca la macchina di controllo: decisione dell'operatore.
3. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi `reports/setup_notte.md`.

## Esito per fetta

- **Merge di #164** (test R-226-4 / R-227-1): `FATTA` — su richiesta esplicita dell'operatore, merge commit `82702af`.
- **T81 ermetico** (`tests/test_unit_kernel.py`, osservazione review #232): `FATTA` — isola GROQ/OPENROUTER/GAS_OLLAMA_URL/GAS_OLLAMA_TIMEOUT_SEC, T81d calcolato dentro l'isolamento. Prima, in ambiente ostile: T81b `[120, 120, 5]`, T81d `(5, 120)` → FAIL; ora 715/0 anche ostile.
- **Test della notte ermetici sui tetti** (`tests/test_unit_notte.py`, V-2 bot #164): `FATTA` — la fixture toglie `GAS_NOTTE_MAX_SEC_COMPITO/GIRO`. Prima, con `GIRO=30`, 2 test fallivano; ora 36 passed.
- Test: kernel 715 PASS in locale (invariato, solo isolamento), `pytest tests/` 787 passed.
- **V-4 verifica esterna #163** (voce 6 di `stato_progetto.md` troppo lunga): `DEFERITA` — cosmetica.

## Revisore

Review #234: APPROVATO (nessuna riserva). Verdetto integrale in `reports/handoff.md` §4.

## Anomalie

- `gh` nel container non è autenticato: la PR si apre e si legge con lo strumento GitHub collegato.
