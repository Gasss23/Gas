# DIFF DI SESSIONE — 23 novembre 2026, R7 fetta 2 (ripresa al boot)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/sottofondo/__init__.py`: nuova `riprendi_al_boot` — controllo dell'inizio turno lanciato all'avvio, frase con solo id/stato, mai eccezioni.
- `gas.py`: comando `sottofondo-riprendi`.
- `scripts/sottofondo/com.gas.sottofondo.plist`: servizio launchd solo RunAtLoad che lancia il comando; pretende `~/Gas/.venv` (R-839-1).
- `.claude/perimetro_review.txt`: `scripts/sottofondo/` nel perimetro di review.
- `tests/test_unit_sottofondo.py`: 8 test della ripresa al boot (ripresa, doppio lancio, riprese finite, fermato, vivo, nessun compito/fuori cartella, errore interno, già finito/file sparito, comando vero).
- `.claude/agents/memoria_revisore.md`: righe delle review #839 e #840.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
