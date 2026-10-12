# Diff della sessione — 2026-10-12 — messaggio «Pipeline esausta» col motivo

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `run_turn`: per ogni provider scartato registra il motivo (variabile non impostata, quota/HTTP, risposta vuota, 10 iterazioni senza risposta finale) e lo mette nell'errore finale e nel log. Perché: richiesta dell'operatore dopo il giro di notte di prova («Pipeline esausta» non diceva perché).
- `tests/test_unit_kernel.py` — T9b aggiornato, T87 nuovo.
- `.claude/agents/memoria_revisore.md` — review #292.
- `reports/` — report di fine task, stato del progetto.
