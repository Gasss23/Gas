# DIFF DI SESSIONE — 23 novembre 2026, R7 fetta 2 (ripresa al boot)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/sottofondo/__init__.py`: nuova `riprendi_al_boot` — controllo dell'inizio turno lanciato all'avvio, frase con solo id/stato, mai eccezioni; attesa della rete con tetto prima di toccare la coda (bot #398 V-1), exit 1 se il riavvio non parte (V-3).
- `gas.py`: comando `sottofondo-riprendi`.
- `scripts/sottofondo/com.gas.sottofondo.plist`: servizio launchd solo RunAtLoad che lancia il comando; pretende `~/Gas/.venv` (R-839-1).
- `.claude/perimetro_review.txt`: `scripts/sottofondo/` nel perimetro di review.
- `tests/test_unit_sottofondo.py`: 8 test della ripresa al boot (ripresa, doppio lancio, riprese finite, fermato, vivo, nessun compito/fuori cartella, errore interno, già finito/file sparito, comando vero) + 5 delle correzioni del bot (senza rete, rete che arriva, tetto dell'attesa, niente attesa senza compito, riavvio non partito).
- `.claude/agents/memoria_revisore.md`: righe delle review #839, #840, #841 e #849-MERGE-R7; più quelle della chat CRM arrivate col merge di main (4114b631). Dopo il merge la base del ramo è il main nuovo: i file della #397 non compaiono in questo diff.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
