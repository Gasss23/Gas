# DIFF SESSIONE — 2026-10-29 (chat Motore: riserve della PR #293, PR #295)

- `gas.py`: `_DOTENV_INTERRUTTORI`; insieme `visti` in `_carica_dotenv`; WARN del doctor per `GAS_CLAUDE_BIN` scavalcato; messaggi su `GAS_CLAUDE_CLI` riferiti al giro del timer, con «.env non letto» sotto `GAS_NO_DOTENV`.
- `tests/test_unit_dotenv.py`: docstring corretta; nuovi test `test_interruttori_confrontati_come_flag_e_chiavi_ripetute` e `test_dal_dotenv_al_doctor`.
- `tests/test_unit_kernel.py`: T99w e T99x ripristinano gli insiemi e usano il testo nuovo del messaggio.
- `.claude/agents/memoria_revisore.md`: righe delle review #551 e #552.
- `reports/stato_progetto.md`: punto 3 della RIPARTENZA (riserve chiuse) e «Ultimo aggiornamento».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
