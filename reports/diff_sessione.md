# DIFF SESSIONE — 2026-10-29 (chat Motore: «/forte@NomeBot» e test del doctor, PR #297)

- `modules/telegram/bot.py`: `togli_destinatario_forte` e chiamata nel gestore prima di `prefisso_forte` (bot #269); con il nome di Gas ignoto il testo resta invariato e va a «Uso» (V-1 bot #297).
- `tests/test_unit_notte.py`: `test_forte_con_destinatario_nei_gruppi` e `test_handle_update_forte_con_destinatario`.
- `tests/test_unit_dotenv.py`: casi «il .env lo spegne» e «.env non letto» in `test_dal_dotenv_al_doctor` (V-1 bot #295).
- `.claude/agents/memoria_revisore.md`: righe delle review #554, #555 e #556.
- `reports/stato_progetto.md`: punto 3 (riserve della #295) e punto 4 (bot #269 chiusa) della RIPARTENZA, «Ultimo aggiornamento».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
