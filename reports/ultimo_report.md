# ULTIMO REPORT — 2026-10-14 — D5: copie di cartelle e file di chiavi

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (tocca il cancello: il bot darà neutral → decide l'operatore).
2. Fetta di sicurezza: secondo passaggio claude.ai col link della PR (facoltativo, D5 nasce già da quello su #204).

## Esito

- **Copie con altri nomi** (MEDIA del secondo passaggio claude.ai su #204) — FATTA: «keys copy/», «keys (1)/», keys.backup/, keys_old/, keys2/, old_keys/, tokens copy/ trattate come keys/ in lettura e scrittura; stesso per passwd/, shadow/, .config/gh.
- **Tetto dei 255 caratteri prima di ogni regex** — FATTA.
- **Backslash su Windows** (BASSA) — SALTATA: Gas gira su Linux/Mac; tracciata.
- **Cartelle innocue key/, token/, shadow/ bloccate** (BASSA) — SALTATA: nessuna nel repo oggi; tracciata per FASE 4.
- **Misura su file reali** — nessun cambio di esito rispetto a origin/main (180 voci).
- **Test** — tests/test_unit_gate.py 590 passed (con il gate di main 20 failed); pytest tests/ 1406 passed.
- **Review** — #343 APPROVATO (cosmetica: tetto 255 ora doppio).

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
