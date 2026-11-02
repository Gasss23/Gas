# Diff della sessione — 2026-11-02 — Mani, fetta 36 (PR #319)

Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/telegram/avviso.py` (nuovo): strumento avvisa_operatore — testo pulito (solo stringhe), tetto al giorno su file con prenotazione (0 = spento), `rifiuto_senza_costi` e `rifiuto_al_cancello` (tetto del giorno letto), invio con `invia_notifica`; valore non intero = spento.
- `gas.py`: spec dello strumento, prompt di riserva, ramo in execute_tool_call (una per turno), `_rifiuto_avviso_al_cancello` nel ramo del cancello (una per turno anche alla firma), diario con la sola lunghezza, conto in `_SAFE_PATH_DENY_PREFIXES`.
- `modules/gate/gate.py`: avvisa_operatore UNCERTAIN; `.gas_notifiche_uso` in `_DENY_PREFIXES` e `_LIVELLO3_PREFISSI`.
- `gas_identity.md`: 13 strumenti, riga di avvisa_operatore.
- `.gitignore`: il conto e i suoi temporanei.
- `.github/workflows/ci.yml`: passo che lancia i test nuovi.
- `tests/test_unit_avvisa_operatore.py` (nuovo): 42 test (tetto, riavvio, fail-closed, invisibili, non stringa, spento, valori non interi, cancello).
- `tests/test_unit_kernel.py`: T102a-j (round-trip, diario, tetto per turno, invio fallito, firma a finestra contaminata, una per turno alla firma, controlli e tetto del giorno prima della firma, firma end-to-end), due voci in T68s.
- `tests/test_unit_gate.py`: il conto è livello 3.
- `.claude/agents/memoria_revisore.md`: righe #611-#614 e #617 (commit del revisore).
- `reports/`: report di fine task, stato_progetto (blocco fetta 36), roadmap (riga della notifica), ripartenza_mani (punto g).
