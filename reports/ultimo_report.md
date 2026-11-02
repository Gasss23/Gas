# Ultimo report — 2026-11-02 — Mani: fetta 38, voce H24 sistemata dopo la prova dal vero sul Mac

## DECISIONI UMANE RICHIESTE
1. Merge della PR #328 della fetta 38: lo decide l'operatore, perché tocca `.claude/perimetro_review.txt` (aggiunge `scripts/voce/`).
2. Sul Mac, dopo il merge: `bash scripts/voce/installa.sh` due volte di fila (la seconda non deve fermarsi con «Bootstrap failed: 5»), poi una richiesta a voce e `grep "tempi voce" gas_debug.log` dalla cartella di Gas.

## Esito
- **PR #324 (piano mail)**: `FATTA` — mergiata (c6206d2) col sì dell'operatore sull'head 84b1422, dopo il merge di main (PR #326, review #630 APPROVATO).
- **Riserve della PR #324**: `FATTA` — V-1/V-2 BASSE del bot su 84b1422 e V-2 COSMETICA su 7346994 registrate in stato_progetto per la fetta 1 della mail; V-1/V-2 BASSE del bot su 922aac9 chiuse qui (questo punto e la registrazione).
- **Rilevatore sempre in errore (V-1 ve #323)**: `FATTA` — log a 1, 2, 4, 8… errori e pausa crescente con l'esponente limitato.
- **GAS_CLAUDE_BIN sotto launchd (V-1 bot #323) e token vuoto (V-4 bot #323)**: `FATTA` in installa.sh.
- **Seconda esecuzione di installa.sh (M1 sul Mac)**: `FATTA` — attesa dopo bootout e bootstrap con 3 tentativi, con 4 test.
- **Tempi della voce nel log (M1)**: `FATTA` — `grep "tempi voce" gas_debug.log`, scritto nella LEGGIMI.
- **scripts/voce/ nel perimetro di review (V-4 ve #323)**: `FATTA`.
- **Review**: #624 BOCCIATO (corretto), #625, #628, #629, #631 APPROVATO CON RISERVE; aperte solo R-625-1 BASSA e tre COSMETICHE (stato_progetto, fetta 38).
