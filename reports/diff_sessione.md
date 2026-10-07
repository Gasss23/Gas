# DIFF SESSIONE — 2026-10-07 — fix/verifica-bot-socat (PR #145)

- `.github/workflows/verifica-bot.yml`: lo step `sandbox` installa `bubblewrap socat ripgrep` e si ferma (DIPENDENZA_FAIL) se socat o rg mancano. Perché: terza prova reale su #142, la Bash del bot non partiva ("socat not installed") e il bot ha giudicato alla cieca.
- `tests/test_unit_verifica_bot.py`: test_bubblewrap_installato_prima_di_claude esteso (install con ripgrep, ciclo `command -v`). 270 passed.
- `.claude/agents/memoria_revisore.md`: righe #196/#197.
- `reports/`: stato_progetto (terza prova, R-196-1/3), ultimo_report, diff_sessione, handoff.
