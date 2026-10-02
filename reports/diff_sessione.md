# DIFF SESSIONE — 2026-10-02 — Fetta C3 cancello (feat/cancello-c3)

> Si riscrive a ogni sessione; la storia completa sta in git.

| File | Cosa è cambiato e perché |
|---|---|
| `modules/memory/store.py` | Tabella `approvals` (§4a) + trigger di immutabilità + metodi coda approvazioni fail-closed (Fetta C3). |
| `tests/test_unit_kernel.py` | Test reali T73a-g sulla coda (enqueue, risoluzione singola, hash, scadenza, DB corrotto/assente, nessun tool esposto, round-trip). |
| `reports/stato_progetto.md` | Finding F-verdetto-ritoccato, R-finale-1, nota handoff #109, voce C3 con riserve R-c3-1..5. |
| `.claude/agents/memoria_revisore.md` | Memoria review #125 (commit del revisore). |
| `reports/ultimo_report.md` | Report di fine task. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `reports/diff_sessione.md` | Questo file. |
