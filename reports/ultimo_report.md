# ULTIMO REPORT — 2026-10-14 — D4: cartelle di chiavi mai scrivibili (gate)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #204 (tocca il cancello: il bot darà riserve o neutral → decide l'operatore).
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai col link della PR #204.

## Esito

- **R-bot202-2** — FATTA: in `livello_scrittura` MAI se un pezzo intermedio del percorso è keys/, tokens/, passwd/, shadow/ (anche copie -, ~, .bak, .old). La lettura resta come in D3 (keys/readme.md, shadow/readme.md leggibili).
- **Commento fuori posto di `_COPIA_GH_RE`** (cosmetica, bot #202) — FATTA.
- **R-bot202-1** (`kubeconfig` senza bordo) — SALTATA: fuori dalla richiesta, resta riserva.
- **Misura su file reali** — nessun cambio di esito rispetto a origin/main (180 voci).
- **Test** — tests/test_unit_gate.py 565 passed (con il gate di main 8 failed); pytest tests/ 1371 passed.
- **Review** — #338 APPROVATO.
