# DIFF SESSIONE — 2026-10-21 (chat Mani, fetta 4)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_TAG_NASCOSTI` unico per parser e ripiego (con math/object, senza `embed`), nome del tag intero; nel ripiego fine del tag come il tokenizzatore HTML (virgolette solo dopo «=», resto del nome), commenti vuoti e `--!>` lineari, titolo tolto.
- `tests/test_unit_web_leggi.py` — sonde delle review #431-#442 e delle note di bot e verifica esterna #238/#239, linearità in sottoprocesso (137 test).
- `.claude/agents/memoria_revisore.md` — righe #431, #432, #438, #439-#442, #444 (chat Mani), più quelle della chat Motore portate dal merge.
- Dal merge di main (PR #240, chat Motore, non di questa sessione): `gas.py`, `scripts/bot_esito.py`, test kernel e verifica_bot, `reports/da_mergiare.md`.
- `reports/stato_progetto.md` — blocco «Mani — fetta 4».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
