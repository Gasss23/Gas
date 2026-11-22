# Diff della sessione — 2026-11-21 — Voce: microfono muto e secondi del messaggio

Si riscrive a ogni sessione; la storia completa sta in git. Ramo fix/voce-registra-microfono-muto-2 da main dcedea6a (PR #390 mergiata).

- `scripts/voce/registra_voce.py`: `Registratore.sentito_suono`; stop con `Errore` sul permesso del microfono se le prime prove di una clip non hanno mai sentito un suono; messaggio «ogni %d secondi» con `MARGINE_CICLO_S`.
- `scripts/voce/LEGGIMI.md`: 9 secondi e il comportamento col microfono muto.
- `tests/test_unit_voce_ascolto.py`: tre test nuovi (microfono muto, silenzio dopo un suono, messaggio con secondi interi).
- `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
