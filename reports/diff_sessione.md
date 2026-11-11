# Diff di sessione — 2026-11-11 notte — voce: prima frase in anticipo (chat M2)

- `brains/claude_cli.py` — con `su_testo` il forte gira a flusso (stream-json): `_esegui_a_flusso` (Popen, fili per stdin/stderr, timeout che uccide il gruppo), `_TestoInArrivo` e `_stringa_parziale` (testo della risposta finale a pezzi, solo dopo `"chiamate": []`), schema con «chiamate» prima di «testo», riga dei tempi `gas.claude_cli.tempi`.
- `gas.py` — `run_turn(su_testo_voce=…)`, passato a ClaudeCliClient solo nei turni a voce.
- `modules/voice/server.py` — `AnticipoVoce`: voce della prima frase preparata in un filo, usata solo se identica alla risposta finale; mai nei seguiti.
- `tests/` — claude_cli (16 nuovi), voice_server (5 nuovi), kernel T104d/T104e.
- Merge di origin/main (#370).
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
