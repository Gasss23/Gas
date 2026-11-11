# Ultimo report — 2026-11-11 — Audit dell'11 novembre: correzioni B1/B2/B4/S1 (chat M3)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #376 (https://github.com/Gasss23/Gas/pull/376): tocca la macchina di controllo (gate, hook, CI) → con riserve del bot decide l'operatore (via M1). Revisore APPROVATO (#767-M1).

## Esito
- **B1 MEDIA — gasmerge senza `timeout` sul Mac**: FATTA — `scripts/gasmerge.sh`: timeout → gtimeout → perl come processo padre che allo scadere uccide `gh` (Go ignora SIGALRM) ed esce 124. Il primo tentativo (`alarm; exec`) era stato BOCCIATO dal revisore (#766-M1) proprio per questo.
- **B2 MEDIA — maiuscole nei gate**: FATTA — `scripts/bot_esito.py`, `scripts/check_verdetto.py` con casefold; trovato lo stesso bug in `.claude/hooks/review_gate.sh` e corretto (`grep -qiE`, `GIT_ICASE_PATHSPECS=1`).
- **B4 BASSA — `sottofondo-ferma` fuori cartella**: FATTA — errore che dice di lanciarlo dalla cartella di Gas, exit 1; nella cartella di Gas senza compiti resta «Nessun compito».
- **S1 — CI con permessi di scrittura**: FATTA — `.github/workflows/ci.yml` `permissions: contents: read`.

## Test
Ogni correzione ha un test che fallisce senza (8 + 3 hooks, più il nuovo test del ripiego perl e quello sul file non tracciato). gasmerge + verifica_bot + handoff_check + sottofondo: 891 passed; hooks: 215 passed; kernel: 1135 PASS, 0 FAIL.

## Anomalie
Il push forzato del branch è stato negato dai permessi: non serviva (il branch di prima era tutto dentro main, push normale). Non provato su macOS reale.
