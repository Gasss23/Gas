# Diff della sessione — 2026-11-25 — Mani alla voce (piano + F2)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `reports/mani_voce_piano.md` — nuovo: piano per dare le mani alla voce (esecutore delle richieste, avvisi, merge), rischi e decisioni.
- `modules/sviluppo/esiti.py` — nuovo: formato fisso e lettura stretta dei commenti ESITO/COMANDO sulle issue delle richieste (F2), non collegato a nulla. Dopo il bot: VERIFICA_ESTERNA a valori fissi, riempitivi vuoti tolti, domanda di merge solo con tutti i controlli buoni.
- `tests/test_unit_esiti.py` — nuovo: 46 test del formato (andata e ritorno, commenti malformati/ostili, invisibili, comandi dell'operatore); poi 55 dopo la correzione #866 e 61 dopo #867/#868.
- `.claude/agents/memoria_revisore.md` — righe #864, #865, #866, #867, #868 e #869-MERGE, più le righe di R7 arrivate col merge di main del revisore.
- `reports/stato_progetto.md` — voce «Mani alla voce» fra i finding aperti, con le riserve.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
