# Diff della sessione — 2026-11-06 — Voce rapida, fetta 2 (chat M2)

- `gas.py` — `run_turn(voce=True)`: finestra `_get_window(GAS_VOCE_FINESTRA=6)`, niente `recap_pin`, effort `GAS_VOCE_EFFORT=low` passato al forte.
- `brains/claude_cli.py` — `ClaudeCliClient(effort=…)` → `--effort`; ripiego senza l'opzione se la CLI la rifiuta.
- `modules/voice/server.py` — `voce=True` per ogni turno parlato; C1 «rispondi solo all'ultima» in `_CONTESTO_VOCE`.
- `tests/test_unit_kernel.py` (T104), `tests/test_unit_claude_cli.py`, `tests/test_unit_voice_stt.py`, `tests/test_unit_voice_contesto.py` — test del profilo voce.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
