# Diff della sessione — 2026-11-12 notte — voce: 1 blocco e taratura (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `clients/voice/ascolto.py`: `BLOCCHI_PAROLA_PREDEFINITO` 3 → 1 col perché (misure), docstring; riga «quasi sentita» con «N di fila sopra soglia» (`quasi_sopra`).
- `scripts/voce/diagnosi_ascolto.py`: regex `_QUASI` per i tre formati, campo `sopra`.
- `scripts/voce/taratura_parola.py` (nuovo): taratura di «Hey Jarvis» sulla voce vera, consiglio di soglia e blocchi, salite deboli escluse, avvisi.
- `scripts/voce/LEGGIMI.md`: predefinito 1, come usare la taratura.
- `tests/test_unit_voce_ascolto.py`: predefiniti aggiornati, test nuovi per «sopra soglia», picco corto e taratura.
- `reports/voce_taratura_2026-11-12.md` (nuovo): metodo e risultati della misura.
- `reports/stato_progetto.md`, `.claude/agents/memoria_revisore.md`: riserve e righe #795-#798.
