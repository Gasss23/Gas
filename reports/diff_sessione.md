# Diff sessione — 2026-10-03 — Suite ermetica rispetto a Telegram (fix/c4b1-suite-ermetica)

> Si riscrive a ogni sessione; la storia completa sta in git.

| File | Cosa è cambiato e perché |
|---|---|
| `tests/test_unit_kernel.py` | Suite isolata da Telegram: pop di TELEGRAM_*, trasporto di default che fallisce, guardia urlopen (R-c4b1-1); T76a-d; T75c adeguato all'anteprima disattivata. |
| `modules/telegram/bot.py` | `link_preview_options.is_disabled` nel read-back (R-c4b1-2). |
| `.claude/agents/memoria_revisore.md` | Riga #130 e lezione. |
| `reports/stato_progetto.md` | Stato della fetta, esito del test di parità app/terminale, riserve R-erm-1/2, finding F-env-app. |
| `reports/ultimo_report.md` | Report del task. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `reports/diff_sessione.md` | Questo file. |
