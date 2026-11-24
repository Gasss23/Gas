# Diff della sessione — 2026-11-24 — modello «ehi jarvis» italiano

Si riscrive a ogni sessione; la storia completa sta in git. Base: 7231d92d (origin/main).

- `clients/voice/ascolto.py`: `modello_della_parola()` e `MODELLO_DI_RISERVA`, `_modelli_pronti()` (ripiego col file assente o non fidato); `rilevatore_openwakeword` carica il modello da file se fidato.
- `clients/voice/modelli/ehi_jarvis_it.onnx`: modello addestrato (accento italiano).
- `clients/voice/modelli/LEGGIMI.md`: risultati, limiti, licenza CC BY-NC-SA, attribuzioni.
- `scripts/voce/installa.sh`: opzione `--italiano`; passo 3b, copia del modello; scelta nel `.env` (modello + soglia 0.5) se assente, e se c'è il filtro hey_jarvis solo con `--italiano`.
- `scripts/voce/LEGGIMI.md`: riga di `GAS_ASCOLTO_MODELLO` aggiornata.
- `tests/test_unit_voce_ascolto.py`: test per il modello da file, il ripiego, la copia, la scelta e l'avviso; i test «.env byte per byte» partono col modello già scelto.
- `reports/voce_simulazione_2026-11-23/modello_italiano/`: script di addestramento e valutazione, risultati grezzi, rapporto (LEGGIMI), metriche.
- `.claude/agents/memoria_revisore.md`: review #854–#857.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
