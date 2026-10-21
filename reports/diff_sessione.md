# DIFF SESSIONE — 2026-10-21 (dopo il merge di #234: tre stati per un comando firmato)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `_run_command_avviato` (True da quando il comando parte, azzerato a ogni tool call e in applica_firma); `_esito_diario` «[KO] esito incerto»; applica_firma con `stato` finita/incerta/non_partita; testo d'errore «PARTITO… esito INCERTO» per il modello.
- `modules/telegram/bot.py` — messaggio «⚠️ Approvata e PARTITA, ma esito INCERTO».
- `tests/test_unit_kernel.py` — T77u, T77v, T77w.
- `.claude/agents/memoria_revisore.md` — righe #428, #429.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/da_mergiare.md`, `reports/roadmap.md` — report.
