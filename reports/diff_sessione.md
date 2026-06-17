# 🔀 DIFF DI SESSIONE — 2026-06-17 (Backup automatico del DB di memoria)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché
Implementata la **rete di sicurezza anti auto-corruzione** del DB di memoria
(`.gas_memory.db`), il dato più prezioso e meno rimpiazzabile del sistema, NON coperto
dagli snapshot git (item roadmap CLAUDE.md §10 FASE 2 "Backup della memoria").

## File toccati (commit motore `cb99d1c`, +225 / -5)
- **`modules/memory/store.py`**: `integrity_check()` (PRAGMA quick_check, fail-safe §9);
  `backup()` esteso con rotazione pura (`_backup_retention`, `keep=10`) + timestamp con
  microsecondi; `backup_auto(min_interval_sec)` THROTTLED (salta se non è ora o se
  l'integrità è KO → non propaga corruzione); `_backup_files`/`ultimo_backup`.
- **`gas.py`**: `_memoria_backup_auto()` fail-safe §9, chiamato UNA volta per turno in
  `run_turn` dopo `_memoria_pin()` (fuori dal loop); override env
  `GAS_MEMORY_BACKUP_EVERY_SEC`/`_KEEP`; `doctor` sezione 8 "Memoria" (integrità/FTS5/
  backup, apre il DB solo se esiste, zero token).
- **`tests/test_unit_kernel.py`**: T26a-e. Suite **123→128, 0 FAIL**.

## Processo
- Gate di review §3: subagent **revisore** invocato sul diff staged → **APPROVATO**
  (review #19, 2 note cosmetiche non bloccanti), validato dal vivo.
- Report `reports/ultimo_report.md` riscritto; `stato_progetto.md` aggiornato.

## Invarianti
`_get_window` / `_cap_window_chars` / `for _ in range(10)` / sandbox bwrap / snapshot
INVARIATI. Backup = copia in-process di file locale (codice fidato) → fuori dal sandbox.
