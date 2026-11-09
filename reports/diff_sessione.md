# Diff della sessione — 2026-11-09 notte — Voce: cache delle frasi fisse (chat M2)

- `modules/voice/server.py` — `sintesi()` con cache delle frasi fisse; `_finiti_jobs` azzerato a inizio richiesta; funzione al posto della lambda; parentesi nella condizione del segno.
- `tests/test_unit_voice_server.py`, `tests/test_unit_sottofondo.py` — test della cache; test dell'azzeramento di `_finiti_jobs` (ve #356 V-1); righe vuote tolte; test che le risposte vere passano dalla cache (bot #356 V-3).
- `.claude/agents/memoria_revisore.md` — review #715, #716 (merge di main) #719 e #721.
- Merge di origin/main b827447 (#355 di Mani): entrano `modules/telegram/bot.py` e i suoi test, non toccati da M2.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
