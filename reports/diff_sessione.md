# Diff della sessione — 2026-11-25 — Scheda clienti da leggere offline

Si riscrive a ogni sessione; la storia completa sta in git. Ramo riallineato a main b7182a7c (PR #405 e #406 mergiate).

- `modules/crm/scheda.py` (nuovo): scheda clienti in PDF con password propria (AES-256) su iCloud Drive, rifatta solo quando cambiano i dati; rilettura della password dal `.env`.
- `modules/crm/server.py`: il guardiano rifà la scheda in un thread a parte (dopo l'avvio, dopo un cambio, una volta al giorno, riprova dopo un errore).
- `modules/crm/__main__.py`: comando `scheda [--forza]` e riga di stato all'avvio.
- `requirements.txt`: `pypdf`.
- `tests/conftest.py`: toglie anche `GAS_CRM_SCHEDA_PASSWORD` nei test.
- `tests/test_unit_crm.py`: test della scheda e del guardiano.
- `reports/crm/guida.md`, `reports/crm/decisioni.md` (punto 22).
- `.claude/agents/memoria_revisore.md`: review #864–#866.
- `reports/stato_progetto.md` (anche le riserve dell'ultimo verdetto del bot sulla #405, regola 3), report di fine task.
