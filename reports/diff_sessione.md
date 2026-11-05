# Diff della sessione — 2026-11-05 — chat Mani, fetta 43

File toccati (base main 942e665, dopo il merge della PR #336):
- `scripts/voce/pausa.sh` (nuovo): ferma solo l'ascolto, aspettando che il bootout asincrono finisca.
- `scripts/voce/riprendi.sh` (nuovo): ricarica l'ascolto dal plist installato, con 3 tentativi.
- `scripts/voce/LEGGIMI.md`: sezione «Pausa (standby) e ripresa» al posto della riga col launchctl a mano.
- `tests/test_unit_voce_ascolto.py`: test di pausa.sh e riprendi.sh col launchctl finto.
- `.claude/agents/memoria_revisore.md`: riga della review #673.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task (più la fetta 42 pronta in locale e la PR #336 mergiata).

Questo file si riscrive a ogni sessione; la storia completa sta in git.
