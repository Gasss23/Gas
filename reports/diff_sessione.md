# Diff della sessione — 2026-11-02 — Mani: fetta 38, voce H24 dopo la prova sul Mac

Si riscrive a ogni sessione; la storia completa sta in git.

- `clients/voice/ascolto.py`: rilevatore sempre in errore con log limitato e pausa crescente (esponente limitato).
- `scripts/voce/installa.sh`: GAS_CLAUDE_BIN scritto se manca, token vuoto rifiutato, attesa dopo bootout e bootstrap con 3 tentativi.
- `scripts/voce/LEGGIMI.md`: dove stanno i log e i tempi della voce (`grep "tempi voce"`), chi ruota e chi no.
- `tests/test_unit_voce_ascolto.py`: da 73 a 93 test; launchctl finto con stato, sleep finto che registra.
- `.claude/perimetro_review.txt`: `scripts/voce/` nel perimetro di review.
- `.claude/agents/memoria_revisore.md`: righe delle review #624, #625, #628, #629, #631.
- `reports/stato_progetto.md`: blocco della fetta 38; riserve della PR #324 registrate.
- `reports/ultimo_report.md`, `reports/diff_sessione.md`, `reports/handoff.md`: report di fine task.
