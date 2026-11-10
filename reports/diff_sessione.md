# Diff della sessione — 2026-11-10 — chat Mani, ascolto H24: meno attivazioni per sbaglio

File toccati (base main 695b759, dopo il merge della PR #359; poi merge di origin/main 447195f, PR #360, in a13f442: codice di main senza modifiche, conflitti solo nei report):
- `clients/voice/ascolto.py`: finestra 15 s, MAX_TURNI_PREDEFINITO 3, SOGLIA_PREDEFINITA 0,6, parola su `blocchi_parola` blocchi di fila (GAS_ASCOLTO_BLOCCHI_PAROLA, default 2), coda dell'eco di 0,5 s ignorata nella finestra; poi (bc37ae5, V-1 verifica esterna #361) anche nella finestra la parola vale solo con 2 blocchi di fila, commento soglia 0,6.
- `tests/test_unit_voce_ascolto.py`: default aggiornati, 4 test nuovi + 3 per la finestra (V-1 #361, R-737-1).
- `scripts/voce/LEGGIMI.md`: tabella delle regolazioni e paragrafo privacy coi nuovi valori.
- `.claude/agents/memoria_revisore.md`: righe #736, #737, #738 e lezioni.
- `reports/stato_progetto.md`: voce Mani con l'esito della verifica esterna #361.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
