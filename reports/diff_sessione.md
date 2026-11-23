# Diff della sessione — 2026-11-23 — Gas usa il CRM (comandi da Telegram e voce)

Si riscrive a ogni sessione; la storia completa sta in git. Ramo ripartito da main bf428441 (PR #394 mergiata).

- `modules/crm/agente.py` (nuovo): consulta (sola lettura), prepara (controlli senza scrivere, forma canonica con id e centesimi, importo solo se detto dall'operatore, nome cercato a inizio parola con avviso), applica (solo forma canonica, dopo la firma).
- `modules/crm/store.py`: tabella dei promemoria (mai cancellati; reclamo prima dell'invio, rilascio se fallisce), controlli dell'anagrafica condivisi, capitale prelevabile in sola lettura.
- `gas.py`: strumenti `crm_consulta` e `crm_modifica`; richieste e strumenti del CRM solo a Opus; modifica parcheggiata alla firma nella forma canonica, importi solo dal messaggio del turno, mai dal sottofondo; diario e progressi senza dati dei clienti; filtro delle parole e dei telefoni.
- `gas.py` (decisione 19): interruttore `GAS_SOLO_OPUS`, acceso di default: ogni turno va solo a Opus.
- `tests/conftest.py`: `GAS_SOLO_OPUS=0` per le suite che provano la cascata dei cervelli.
- `CLAUDE.md` §2: decisione «Sempre Opus» registrata.
- `modules/gate/gate.py`: `crm_consulta` SAFE (lettura non fidata), `crm_modifica` IRREVERSIBLE.
- `modules/telegram/bot.py`: promemoria del CRM mandati su Telegram ogni minuto.
- `tests/test_unit_crm.py`, `tests/test_unit_kernel.py`: test nuovi (T118, riserve #839-#842); T80 e T116h adattati alla regola nuova.
- `.claude/agents/memoria_revisore.md`: review #839-#848 e lezioni.
- `reports/crm/decisioni.md` (punti 18 e 19), `reports/crm/guida.md`, `reports/bacheca.md`, `reports/stato_progetto.md`, report di fine task.
