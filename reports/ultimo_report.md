# Report FETTA C2 + R-nw-1 — feat/cancello-c2

**Data:** 2026-10-01  
**Branch:** feat/cancello-c2

---

## DECISIONI UMANE RICHIESTE

Nessuna urgente. Prossima fetta raccomandata: **C3** (coda approvazioni SQLite) o **F-controlli-auto** (fix check_verdetto).

---

## Esito fette

**Sonda (passo 0):** FATTA — C1 confermato su origin/main (PR #107, `abb7aae`). Branch `feat/cancello-c2` creato da origin/main.

**R-nw-1 — Path hardening `_safe_path`:** FATTA
- `Path(...).resolve(strict=False)` esplicito
- Confinamento `is_relative_to(root_resolved)` PRIMA della denylist
- Denylist su `path.relative_to(root_resolved).parts` (fix R-c2-1: non sui componenti assoluti)
- Casefold + normalizzazione trattini/spazi (retro-compatibilità T6)
- Fail-closed: except → log eccezione + return None
- Rimosso check inline denylist in `execute_tool_call`/write_file (consolidato in `_safe_path`)

**C2 — Integrazione gate in `run_turn`:** FATTA
- Aggiunta costante `UNTRUSTED_INPUT_TOOLS` in `modules/gate/gate.py` (§3b)
- Aggiunto metodo puro `GasKernel._finestra_e_contaminata(window)` (R-c2-3)
- Calcolo `_finestra_contaminata` da `_get_window()` ad ogni iterazione del loop agentico
- Gate check prima di `execute_tool_call`: DENY → "Operazione negata", IRREVERSIBLE/UNCERTAIN+contaminata → stub approved (coda reale in C3), altrimenti esegui

**Test (passo 2):** FATTI
- T71a-T71h: R-nw-1 (symlink, traversal, case-insensitive, regressione root con prefisso negato)
- T72a-T72e: C2 (SAFE invariato, DENY senza crash, stub approved, UNTRUSTED_INPUT_TOOLS, `_finestra_e_contaminata` puro)
- Suite: **423 PASS, 5 FAIL** F-mac-1 bwrap macOS (invariati, baseline 400 PASS)
- Gate suite pytest: **74 PASS**

**Revisore Opus (passo 3):** FATTO — due round di review
- Review #118: APPROVATO CON RISERVE (6 riserve, R-c2-1 bloccante per correttezza)
- Fix R-c2-1 (relative_to), R-c2-3 (helper puro), R-c2-6 parziale applicati
- Review #119: APPROVATO CON RISERVE (riserve residue R-c2-2/R-c2-4/R-c2-5/R-c2-6/R-c2-7 non bloccanti)

**Doc (passo 4):** FATTO
- `reports/stato_progetto.md`: aggiornato con R-nw-1 CHIUSO, F-controlli-auto, riserve C2
- PR #108: https://github.com/Gasss23/Gas/pull/108

## Anomalie

- Review #118 ha trovato bug R-c2-1 (denylist su componenti assoluti invece che relativi): corretto prima del commit e ri-reviewato.
- `backup_gas_history.txt` (senza dot iniziale, nelle sotto-cartelle) ora passa il controllo — era bloccato dalla vecchia substring check. Registrato come R-c2-2 (minore, difesa in profondità). I file di sistema reali (`.gas_history.json`, `.gas_memory.db` ecc.) restano protetti.
