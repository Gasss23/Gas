# Diff della sessione — 2026-11-10 — chat Mani, ascolto H24: meno attivazioni per sbaglio

File toccati (base main 695b759, dopo il merge della PR #359):
- `clients/voice/ascolto.py`: finestra 15 s, MAX_TURNI_PREDEFINITO 3, SOGLIA_PREDEFINITA 0,6, parola su `blocchi_parola` blocchi di fila (GAS_ASCOLTO_BLOCCHI_PAROLA, default 2), coda dell'eco di 0,5 s ignorata nella finestra.
- `tests/test_unit_voce_ascolto.py`: default aggiornati, 4 test nuovi.
- `scripts/voce/LEGGIMI.md`: tabella delle regolazioni e paragrafo privacy coi nuovi valori.
- `.claude/agents/memoria_revisore.md`: riga #736 e lezione.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
