# Diff della sessione — 2026-11-05 — chat Mani, fetta 40

File toccati (base origin/main 8b8012d):
- `clients/voice/ascolto.py`: soglia della voce predefinita 200 (costante `VOCE_RMS_PREDEFINITO`), usata da `Ascolto` e da `main`; docstring aggiornata. Motivo: prova sul MacBook Air del 5 novembre.
- `scripts/voce/LEGGIMI.md`: tabella delle regolazioni a 200, con la nota per alzarlo nelle stanze rumorose.
- `tests/test_unit_voce_ascolto.py`: test della voce piana col default, del valore passato da `main` e del LEGGIMI allineato al codice.
- `.claude/agents/memoria_revisore.md`: riga della review #667 e lezione del revisore.
- `reports/ripartenza_mani.md`: ripartenza della chat Mani (commit b7f2c23 della sessione precedente, unito con un merge).
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
