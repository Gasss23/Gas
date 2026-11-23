# DIFF DI SESSIONE — 23 novembre 2026, R7 fetta 4 (tetto di tempo duro del sottofondo)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/sottofondo/__init__.py`: `_arma_tetto` (timer demone, attesa massima 30 giorni), `_termina_processo` (SIGTERM al proprio gruppo, poi os._exit di riserva), `_secondi_rimasti` (dalla prima creazione); in `_esegui` timer armato col tempo rimasto, «ko» subito se il tempo è già finito, lock perché timer e fine del turno scrivano un solo esito.
- `tests/test_unit_sottofondo.py`: 8 test del tetto duro (armato e tolto, scadenza con avviso, tempo già finito, scadenza dopo «ok», orologio indietro, timer vero, un solo esito, attesa enorme).
- `.claude/agents/memoria_revisore.md`: righe delle review #852-R7 e #853-R7.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
