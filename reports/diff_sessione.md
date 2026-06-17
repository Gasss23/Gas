# 🔀 DIFF DI SESSIONE — 2026-06-17 (doctor 402 onesto + backup automatico del DB)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Due interventi in sessione

### 1) doctor: 402 "crediti esauriti" su rung free opzionale → WARN (commit `7220c28`)
Il `doctor` mostrava `[KO]` allarmante per OpenRouter coi crediti esauriti (HTTP `402`),
ma è un rung OPZIONALE gratuito (paracadute). A runtime `run_turn` GIÀ scalava da sé al
rung successivo (§9, verificato dal vivo) → nessuna modifica lì.
- **`gas.py`**: nuovo helper PURO `_classify_provider_error` (429→QUOTA; 402 opzionale→
  WARN; 402 obbligatorio→KO; resto→KO troncato 60 char); il `doctor` ci delega.
- **`tests/test_unit_kernel.py`**: T27a-d. Exit code del doctor INVARIATO, zero token.
- Revisore **#20 APPROVATO**. Suite **128→132**.

### 2) Backup automatico del DB di memoria (commit `cb99d1c`)
Rete di sicurezza anti auto-corruzione del dato più prezioso (`.gas_memory.db`).
- **`modules/memory/store.py`**: `integrity_check()`, `backup()` con rotazione pura
  (`keep=10`) + timestamp con microsecondi, `backup_auto(min_interval_sec)` THROTTLED
  (salta se non è ora o se l'integrità è KO).
- **`gas.py`**: `_memoria_backup_auto()` fail-safe §9 (1×/turno, fuori dal loop) +
  override env `GAS_MEMORY_BACKUP_EVERY_SEC`/`_KEEP` + `doctor` sezione 8 "Memoria".
- **`tests/test_unit_kernel.py`**: T26a-e. Revisore **#19 APPROVATO**. Suite **123→128**.

## Invarianti
`_get_window` / `_cap_window_chars` / `for _ in range(10)` / sandbox bwrap / snapshot /
cascata `run_turn` INVARIATI in entrambi gli interventi.

## Azione UMANA in sospeso (non codice)
Ricarica crediti OpenRouter (`openrouter.ai/credits`) per riattivare il 4° rung free —
Gas funziona comunque senza (cascata su Gemini/Groq, Ollama sul VPS).
