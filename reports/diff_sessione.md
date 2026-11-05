# Diff della sessione — 2026-11-05 — Voce V14 (chat M2)

- `modules/voice/server.py` — `GET /voce/conferma` (`_conferma`, `conferma_cache`, `FRASE_CONFERMA`, docstring del modulo); filtro `_SOLO_ATTIVAZIONE` senza ok/okay e con la parola ripetuta.
- `tests/test_unit_voice_prova_voci.py` — 2 test V14 (una sintesi per voce, errori puliti senza cache); la fixture azzera la cache.
- `tests/test_unit_voice_stt.py` — casi del filtro: ripetizione riconosciuta, «Ok Gas.» al cervello.
- `.claude/agents/memoria_revisore.md` — review #669-M2, #670-M2 e #674-M2 (merge di main).
- Secondo merge di origin/main (PR #337 fetta bot, fetta 41 della chat Mani): conflitti risolti in `reports/stato_progetto.md`, `reports/ripartenza_m2.md` e nella memoria del revisore.
- Merge di origin/main (PR #333 della chat Mani): conflitti risolti in `reports/stato_progetto.md` e nella memoria del revisore; i file di Mani arrivano invariati.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
