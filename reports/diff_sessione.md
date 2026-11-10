# Diff della sessione — 2026-11-10 — analisi notturna (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py`: B1 `_utf8_sicuro` (surrogati), B2 `_forma_storia_valida` (storia di forma sbagliata), B3 compressione al confine user, B2 conoscenza `continue`, B4 campi del pin capati; ripiego dichiarato (`_info_ripiego`, evento final, riga in CLI).
- `tools/ingest_knowledge.py`: chunk superseded quando la fonte si accorcia, `chunk_text` spezza i paragrafi lunghi, una fonte rotta non ferma le altre, exit 1 se una fonte fallisce.
- `modules/notte/notte.py`: `_stampa_sicura` al posto di print.
- `modules/telegram/bot.py`: `rendi_visibili` nel messaggio di firma; `/notte` e `/compito` da messaggio modificato rifiutati; riga del ripiego nel testo (mai a voce).
- `tests/test_unit_kernel.py`, `tests/test_unit_ingest_fonti.py`, `tests/test_unit_notte.py`, `tests/test_unit_telegram_voce.py`: test nuovi per ogni bug (mutanti presi).
- `reports/test_mattina.md`: bug trovati e prove manuali del mattino.
- `reports/stato_progetto.md`, `.claude/agents/memoria_revisore.md`: riserve e righe #744-M1, #748-M1, #749-M1, #750-M1, #751-M1, #752-M1; riserve del 3° giro di bot e verifica esterna.
- `reports/ripartenza_m1.md`, `reports/proposta_terminale_autonomia.md`, `reports/test_voce_mattina.md`: note di coordinamento M1.
- `reports/handoff.md`, `reports/ultimo_report.md`, `reports/diff_sessione.md`: report di fine sessione.
