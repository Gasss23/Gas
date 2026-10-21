# ULTIMO REPORT — 2026-10-21 — Ultime riserve del bot sulla storia condivisa (dopo il merge di #236)

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge della PR #236 (operatore: «mergia 236 e mostrami cosa rimane da mergiare e continua con la roadmap»).

## DECISIONI UMANE RICHIESTE

1. Merge della nuova PR: pro e contro in `reports/da_mergiare.md`.

## Esito

- **Merge PR #236** — FATTO (`dec4ce9`) su richiesta dell'operatore.
- **V-1/V-2 bot #236 (5° giro) e R-436-1** — FATTA. A metà turno la storia dell'altro processo non entra mai nella finestra del modello, nemmeno al primo salvataggio del turno; i suoi messaggi già uniti a un salvataggio fallito non si duplicano; un test passa dal generatore vero di run_turn (turno finito senza risposta finale). Review #438 APPROVATO CON RISERVE (R-438-1 BASSA, R-438-2 nota).
- **Test** — kernel 992 → 994 PASS, 0 FAIL; pytest tests/ 1816 passed.

## Prossimi passi

1. R-438-1: `gas compress-history` con unione rimandata (stampa ok senza scrivere).
2. R7 / R-c4b3-3: crash tra reclamo e scrittura in storia.
3. R-408-1: potare il registro della notte solo se il file del catalogo è stato letto.
