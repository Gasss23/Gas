# Diff della sessione — 2026-11-21 — CRM: note minori

Si riscrive a ogni sessione; la storia completa sta in git. Le PR #388 e #389 sono mergiate; ramo ripartito da main f75e09a2.

- `modules/crm/copia_cifrata.py`: `_avvio_sistema` e `_leggi_boottime` (ora di avvio da /proc/stat o `/usr/sbin/sysctl`); `_pulisci_ripristini_interrotti` toglie anche i resti di prima dell'avvio; `ripristina` dà un messaggio chiaro se il file non si legge; motivo «errore durante la copia cifrata».
- `tests/test_unit_crm.py`: `test_note_minori_388`; due asserzioni aggiornate al nuovo motivo.
- `tests/test_unit_verifica_bot.py`: casi «Non: grave» e «Non, grave».
- `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
