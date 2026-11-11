# Diff della sessione — 2026-11-11 — chat Mani, ascolto più severo di default

File toccati (base main 904d9d6, dopo il merge della PR #368):
- `clients/voice/ascolto.py`: SOGLIA_PREDEFINITA 0,7, BLOCCHI_PAROLA_PREDEFINITO 3, MAX_TURNI_PREDEFINITO 1, FINESTRA_PREDEFINITA_S 10, SOGLIA_INTERRUZIONE_PREDEFINITA 0,8, TURNI_CON_INTERRUZIONE 2; costruttore coi valori dei test; commenti e docstring.
- `tests/test_unit_voce_ascolto.py`: default di main e del LEGGIMI, 3 test nuovi, test esistenti adattati.
- `scripts/voce/LEGGIMI.md`: intro, conversazione senza parola spenta di default, interruzione, privacy, tabella.
- `.claude/agents/memoria_revisore.md`: righe #757-M1, #758-M1 e lezione.
- `reports/*`: report di fine task e voce in stato_progetto.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
