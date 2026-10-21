# DIFF SESSIONE — 2026-10-21 (chat Mani, fetta 1: leggi_pagina)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/__init__.py`, `modules/web/leggi.py` — nuovi: `leggi_pagina(url)`, lettura di una pagina web con le regole di sicurezza della fetta (R6); poi niente `titolo` fuori dai marcatori e niente redirect da https a http (V-1/V-2 bot #235).
- `tests/test_unit_web_leggi.py` — nuovo: 83 test con server e DNS finti; righe con IP di prova marcate `gasmerge-ip-ok` per il Gate IP.
- `.github/workflows/ci.yml` — passo nuovo «Run web suite».
- `.claude/agents/memoria_revisore.md` — righe #391, #392, #393, #406, #407, #408 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 1» con le riserve; data di aggiornamento.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
