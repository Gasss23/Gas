# ULTIMO REPORT — 2026-10-03 — C4b-3: esito della firma nel contesto del modello

Branch `feat/cancello-c4b3` · PR #117 · commit motore `4065091` (review #133 + #134) · fix gate `9951563` (review #135) · tutti **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #117 (variante A: `gasmerge 117`, l'operatore conferma digitando il numero).
2. R-135-3: la regola di revisore.md "citare un file non nel diff invalida il verdetto" va riscritta? La proposta del revisore è "≥2 elementi nel diff, citazioni di contesto ammesse e verificate a HEAD", con il gate allineato a questa regola (chiuderebbe anche R-135-1/2).
3. Prova reale di un click su Telegram: fattibile con il bot vivo (`gas telegram`) e un'azione innocua. Non è ancora stata provata, ed è l'ultimo passo prima di considerare M2 completa.

## Esito per step

- **Esito della firma nella storia** (`GasKernel._storia_esito_firma`, R-c4b2-1): FATTA. Struttura del blocco:
  - notifica user del kernel: tool, ID, decisione; mai args né output; "non richiedere di nuovo";
  - solo dopo il reclamo: tool_call con gli args SALVATI e output reale nel ruolo tool, così la contaminazione §3b si calcola come nel loop;
  - presa d'atto del kernel.
  
  Il blocco è tutto-o-niente, salvato su `.gas_history.json`, scritto una volta per ID, senza chiamate LLM, fail-safe.
- **Casi coperti**: rifiuto, firma non riconosciuta, hash non integro, esito dopo il reclamo (eseguita, DENY al ricontrollo, diniego interno, dry-run). FATTA.
- **R-c4b2-9** (dry-run letto come "eseguita"): CHIUSA.
- **R-c4b3-1** (review #133: "eseguita" dedotto dal testo dell'output, falsificabile): CHIUSA. Per `run_command` l'esito ora viene da `_run_command_meta`, azzerato dopo il reclamo (T78k, T78k-bis).
- **R-c4b3-2** (dedup non provato da T78c): CHIUSA, con un nuovo check in T78d.
- **Notifica di scadenza al modello**: DEFERITA a C5 (design).
- **Click reale su Telegram**: DEFERITO alla decisione dell'operatore (punto 3).
- **Gate B `check_verdetto.py` (F-controlli-auto, parte "path corti")**: FATTA, su scelta dell'operatore. Il primo `fine_task_finale.sh` si era fermato perché il verdetto #133 cita `bot.py:282` e `bot.py:417`. Ora le citazioni di contesto e i nomi corti univoci si risolvono a HEAD; i casi ambigui o inesistenti danno exit 1. 5 test nuovi. Il verdetto NON è stato ritoccato.

## Test

- `python tests/test_unit_kernel.py`: 614 → **643 PASS / 5 FAIL**. I 5 FAIL sono F-mac-1 (T11c2, T11e, T12a, T12c, T12e: bwrap assente su macOS), invariati.
- `pytest tests --ignore=tests/test_unit_kernel.py`: 232 → **237 passed** (5 test nuovi del gate).

## Riserve aperte

R-c4b3-3, R-c4b3-4, R-c4b3-5 (nuove, minori); R-135-1, R-135-2, R-135-3 (gate B); più le R-c4b2-6/7/8/10 ancora aperte. Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- All'inizio della sessione il marcatore `.claude/.review_ok` era già presente (creato alle 19:26, prima della review #133): era un residuo della sessione C4b-2. Il gate deterministico era quindi aperto. Il commit motore è comunque passato dal revisore (#133/#134). Ho rimosso il marcatore dopo il commit.
- Il primo giro di fine-task (commit `af4b84d`, non pushato in quel momento) si è fermato sul gate B per il falso positivo F-controlli-auto. Il fine-task è stato rieseguito per intero dopo il fix `9951563`.
