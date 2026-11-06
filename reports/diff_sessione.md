# Diff della sessione — 2026-11-05 — chat Mani, fetta 43 parte 2

File toccati (base main c131452, dopo i merge delle PR #340, #339 e #342; contiene anche la correzione V-1 del bot, 1792ab3):
- `clients/voice/ascolto.py`: rilevatore acceso nella finestra («Hey Jarvis, …» è un turno normale, V-1 bot #341), finestra di 40 s, tetto di 15 s e scarto dei turni di seguito, `X-Gas-Seguito`, comandi «fine»/«pausa» del server, chiusura silenziosa sugli errori di seguito.
- `scripts/voce/LEGGIMI.md`: finestra, difese, variabili e privacy.
- `tests/test_unit_voce_ascolto.py`: test dei turni di seguito, dei comandi, delle intestazioni e di main.
- `.claude/agents/memoria_revisore.md`: riga della review #676.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task (più le riserve della PR #340 mergiata).

Questo file si riscrive a ogni sessione; la storia completa sta in git.
