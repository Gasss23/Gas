# ULTIMO REPORT — 2026-10-03 — C4b-3: esito della firma nel contesto del modello

Branch `feat/cancello-c4b3` · PR #117 · commit motore `4065091` · review #133 + #134 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #117 (variante A: `gasmerge 117`, l'operatore conferma digitando il numero).
2. Prova reale di un click su Telegram: fattibile con il bot vivo (`gas telegram`) e un'azione innocua. Non è ancora stata provata, ed è l'ultimo passo prima di considerare M2 completa.

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
- **Click reale su Telegram**: DEFERITO alla decisione dell'operatore (punto 2).

## Test

- `python tests/test_unit_kernel.py`: 614 → **643 PASS / 5 FAIL**. I 5 FAIL sono F-mac-1 (T11c2, T11e, T12a, T12c, T12e: bwrap assente su macOS), invariati.
- `pytest tests --ignore=tests/test_unit_kernel.py`: **232 passed**, invariato.

## Riserve aperte

R-c4b3-3, R-c4b3-4, R-c4b3-5 (nuove, minori), più le R-c4b2-6/7/8/10 ancora aperte. Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- All'inizio della sessione il marcatore `.claude/.review_ok` era già presente (creato alle 19:26, prima della review #133): era un residuo della sessione C4b-2. Il gate deterministico era quindi aperto. Il commit motore è comunque passato dal revisore (#133/#134). Ho rimosso il marcatore dopo il commit.
- Il verdetto #133 cita `bot.py:282` e `bot.py:417/360`, file non presenti nel diff di sessione. Se `check_verdetto.py` segnala questi riferimenti, è il falso positivo noto F-controlli-auto. Il verdetto NON va ritoccato (F-verdetto-ritoccato).
