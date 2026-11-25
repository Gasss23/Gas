# Diff della sessione — 2026-11-25 — Mani alla voce (piano + F2)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `reports/mani_voce_piano.md` — nuovo: piano per dare le mani alla voce (esecutore delle richieste, avvisi, merge), rischi e decisioni.
- `modules/sviluppo/esiti.py` — nuovo: formato fisso e lettura stretta dei commenti ESITO/COMANDO sulle issue delle richieste (F2), non collegato a nulla. Dopo il bot: VERIFICA_ESTERNA a valori fissi, riempitivi vuoti tolti.
- `tests/test_unit_esiti.py` — nuovo: 46 test del formato (andata e ritorno, commenti malformati/ostili, invisibili, comandi dell'operatore); poi 55 dopo la correzione #866.
- `.claude/agents/memoria_revisore.md` — righe #864, #865 e #866 del revisore.
- `reports/stato_progetto.md` — voce «Mani alla voce» fra i finding aperti, con le riserve.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
