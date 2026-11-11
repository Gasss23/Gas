# Diff della sessione — 2026-11-11 notte — chat Mani, PR #371

File toccati (base main e3eb542, dopo i merge di #368, #369, #370 nel branch):
- `clients/voice/ascolto.py`: default più severi (soglia 0,7, 3 blocchi, seguiti spenti, finestra 10 s, interruzione 0,8, TURNI_CON_INTERRUZIONE 2); l'interruzione vuole blocchi di fila; costruttore coi valori dei test; misure nel log (punteggio della parola, picchi corti scartati, volume medio); regolazioni lette una volta e scritte all'avvio, con avviso se il .env le rende più facili.
- `tests/test_unit_voce_ascolto.py`: test dei default, dell'interruzione, delle misure, della diagnosi e delle regolazioni.
- `scripts/voce/diagnosi_ascolto.py`: nuovo, riassunto delle attivazioni dal log (solo lettura).
- `scripts/voce/LEGGIMI.md`: intro, seguiti spenti, interruzione, privacy, «il .env vince», sezione Log e diagnosi, tabella.
- `.claude/agents/memoria_revisore.md`: righe #757-M1…#764-M1 e lezioni.
- `reports/proposta_verifica_parlante.md`: proposta per l'operatore.
- `reports/*`: report di fine task e voce in stato_progetto.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
