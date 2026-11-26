# Diff della sessione — 2026-11-26 — Mani alla voce F3

> Si riscrive a ogni sessione; la storia completa sta in git. Il ramo contiene anche i commit della PR #411 (F2-bis), non ancora su main.

- `modules/sviluppo/cassetta.py` — nuovo: avviso alla creazione, «annulla richiesta N», lettura periodica degli esiti dalle issue, stato in `.gas_richieste_esiti.json`.
- `modules/sviluppo/richieste.py` — `crea_richiesta(..., avvisa=…)`: avviso subito dopo la creazione della issue.
- `modules/sviluppo/esiti.py` — (#411) regola unica `propone_merge`, frase per l'operatore; (F3) tutte le virgolette Pi/Pf e simili a «» tolte dalle citazioni.
- `gas.py` — `richiedi_sviluppo` passa l'avviso `_avvisa_richiesta_accodata`.
- `modules/telegram/bot.py` — «annulla richiesta N» prima del modello; controllo periodico degli esiti delegato a `cassetta`.
- `.gitignore` — file di stato degli esiti.
- `.github/workflows/ci.yml` — passo «Run cassetta suite».
- `tests/test_unit_cassetta.py` — nuovo (80 test); `tests/test_unit_kernel.py` — T100c/T100d; `tests/test_unit_esiti.py` — (#411).
- `reports/mani_voce_piano.md` — decisioni dell'operatore, F3 e F3b.
- `.claude/agents/memoria_revisore.md` — righe #873-MV … #883-MV.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
