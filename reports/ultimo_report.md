# Report di fine task — 2026-10-09 — merge #163 + test R-226-4 / R-227-1

## DECISIONI UMANE RICHIESTE

1. Merge della PR #164 (https://github.com/Gasss23/Gas/pull/164): solo test e `.gitignore`. Per la regola di merge autonomo l'agente la mergia da solo SOLO se il verdetto testuale del bot sull'head è `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi installare il timer notturno seguendo `reports/setup_notte.md`.

## Esito per fetta

- **Merge di #163** (riserve del bot su #162): `FATTA` — su richiesta esplicita dell'operatore, merge commit `17a2e9d`.
- **R-226-4 — test del tetto col kernel vero** (`tests/test_unit_notte.py`): `FATTA` — il tetto per compito chiude il `run_turn` reale a metà loop; riepilogo KO "tempo scaduto"; nel diario un solo `turno_fine` con `esito=ko`. Mutation (tetto disattivato) → FAIL.
- **R-227-1 — rung Ollama dentro run_turn** (`tests/test_unit_kernel.py` T81h): `FATTA` — con solo `GAS_OLLAMA_URL` il client nasce con timeout 600 e `max_retries` 1. Mutation (`_timeout_provider` fisso) → FAIL.
- **`.gitignore`**: `FATTA` — `gas_debug.log.*`.
- **V-1 bot #164 — il test non distingueva `gen.close()` esplicito dal garbage collector**: `FATTA` — il test asserisce anche che `turno_fine` abbia id minore della riga `notte` del compito. Mutation (`gen.close()` → `pass`) → FAIL.
- **V-2 bot #164 — numeri locali contro CI**: `FATTA` — nei report i conteggi del kernel sono indicati come locali (715) e CI (717): in CI girano 2 test del profilo sandbox che in locale sono saltati.
- Test: kernel 714 → 715 PASS in locale (716 → 717 in CI), 0 FAIL; `pytest tests/` 786 → 787 passed.
- **T81b/T81d non ermetici rispetto a `GAS_OLLAMA_TIMEOUT_SEC`** (osservazione del revisore #232, preesistente): `DEFERITA` — fuori scope, tracciata in `stato_progetto.md`.
- **V-4 verifica esterna #163** (voce 6 di `stato_progetto.md` troppo lunga): `DEFERITA` — cosmetica.
- **V-2 bot #163** (verdetti del revisore riscritti per passare il gate B): `DEFERITA` — tocca la macchina di controllo (`check_verdetto.py` o `revisore.md`): decisione dell'operatore.

## Revisore

Review #232: APPROVATO. Review #233 (V-1 bot #164): APPROVATO. Verdetti integrali in `reports/handoff.md` §4.

## Verifiche esterne

- Agente (contesto vergine, su `7743b07`): APPROVATO (note già tracciate).
- Bot su `7743b07`: APPROVATO CON RISERVE — V-1 e V-2 chiuse in `ef7b28e` e in questo commit di fine-task.

## Anomalie

- `gh` nel container non è autenticato: la PR si apre e si legge con lo strumento GitHub collegato.
