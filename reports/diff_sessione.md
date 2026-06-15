# 🔀 DIFF DI SESSIONE — 2026-06-15 (Memoria FASE 2 fetta 1 + housekeeping)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché

### 1. Housekeeping (pre-task)
- **Stash droppato**: `stash@{0}` ("snapshot-autonomo snapshot_health + T15") era la
  vecchia bozza di una funzione già reincorporata in main (TASK C). Classificato cruft
  nella sessione precedente → `git stash drop` (commit `7d0fb70` riguarda solo la doc).
- **`CLAUDE.md` (roadmap FASE 1 + storico)**: la **sandbox OS bwrap** era già implementata
  e cablata in `run_command` ma la roadmap la dava ancora come "da fare". Allineata la doc
  al codice (✅ FATTO) e aggiunta ai "Completati (storico)". Commit `7d0fb70`.

### 2. Memoria FASE 2, fetta 1 — fondamenta storage (commit `8de2b0c`)
- **`modules/memory/__init__.py`** (nuovo): facciata del package.
- **`modules/memory/store.py`** (nuovo, ~300 righe): classe `MemoryStore`, schema SQLite
  (file singolo, no WAL), tabelle `diario` (append-only, immutabile via trigger DB) e
  `contatti` (upsert-abile, stato mutabile), API scrittura/lettura/backup, fail-safe §9.
- **`tests/test_unit_kernel.py`** (+110 righe): nuovi test T19a-j (append/lettura diario,
  upsert, transizione stato, immutabilità, backup, fail-safe DB assente/corrotto).
  Suite **75 → 85**, 0 FAIL, zero token.
- **`.gitignore`** (+3 righe): `.gas_memory.db` (+ `-wal`/`-shm`) — il DB vive fuori da git.
- **Perché**: posare le fondamenta del "cervello" di GAS (diario = ricorda tutto; rubrica =
  relazioni coi lead) come livello di persistenza isolato, robusto e con invarianti incise
  (diario immutabile, contatti aggiorna/invalida). **NON agganciato a run_turn**: il cablaggio
  è solo PROPOSTO nel report (§FINALE), da rivedere prima di toccare il loop blindato.

### Processo rispettato
- Gate di review: invocato il subagent **revisore** sul diff staged PRIMA del commit →
  **review #12 APPROVATO CON RISERVE** (R1 REPLACE/recursive_triggers, R2 costanti non
  configurabili). Riserve tracciate in `stato_progetto.md`. Hook deterministico onorato
  (marcatore `.claude/.review_ok` creato per il commit e rimosso subito dopo).

## File toccati (sintesi)
`modules/memory/__init__.py` (nuovo) · `modules/memory/store.py` (nuovo) ·
`tests/test_unit_kernel.py` (+T19a-j) · `.gitignore` (+3) · `CLAUDE.md` (roadmap) ·
`reports/ultimo_report.md` · `reports/stato_progetto.md` · `reports/diff_sessione.md` (questo).
Commit motore: `8de2b0c` · commit doc roadmap: `7d0fb70`.
