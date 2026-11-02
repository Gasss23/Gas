# Diff della sessione — 2026-11-02 — Mani, fetta 36 (PR #319)

Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/telegram/avviso.py` (nuovo): strumento avvisa_operatore — testo pulito, tetto al giorno su file con prenotazione, invio con `invia_notifica`.
- `gas.py`: spec dello strumento, prompt di riserva, ramo in execute_tool_call (una per turno), diario con la sola lunghezza, conto in `_SAFE_PATH_DENY_PREFIXES`.
- `modules/gate/gate.py`: avvisa_operatore UNCERTAIN; `.gas_notifiche_uso` in `_DENY_PREFIXES` e `_LIVELLO3_PREFISSI`.
- `gas_identity.md`: 13 strumenti, riga di avvisa_operatore.
- `.gitignore`: il conto e i suoi temporanei.
- `.github/workflows/ci.yml`: passo che lancia i test nuovi.
- `tests/test_unit_avvisa_operatore.py` (nuovo): 29 test (tetto, riavvio, fail-closed, invisibili, cancello).
- `tests/test_unit_kernel.py`: T102a-e (round-trip, diario, tetto per turno, invio fallito, firma a finestra contaminata), due voci in T68s.
- `tests/test_unit_gate.py`: il conto è livello 3.
- `.claude/agents/memoria_revisore.md`: righe #611 e #612 (commit del revisore).
- `reports/`: report di fine task, stato_progetto (blocco fetta 36), roadmap (riga della notifica), ripartenza_mani (punto g).
