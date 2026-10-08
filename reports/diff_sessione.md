# DIFF SESSIONE — 2026-10-08 — fix/bot-riserve-preesistenti (R-161-1, falsi NO)

- `scripts/bot_esito.py`: `_RISERVA_REGISTRATA` + `_gravita_nel_testo` toglie solo la parentesi delle citazioni di riserve registrate. Perché: due falsi NO definitivi sulla PR #149.
- `.github/workflows/verifica-bot.yml`: istruzione nel PROMPT su come citare le riserve preesistenti.
- `tests/test_unit_verifica_bot.py`: casi che non bloccano (citazioni) e che devono bloccare (gravità della PR accanto a una citazione, parentesi annidate, campo strutturato), prompt. 297 passed.
- `.claude/agents/memoria_revisore.md`: righe #205, #206.
- `reports/`: stato_progetto (R-161-1 parte falsi NO chiusa, R-205-1/2), ultimo_report, diff_sessione, handoff.
