# ULTIMO REPORT — 2026-10-13 — Merge PR #198 e stato aggiornato (PR #199)

## DECISIONI UMANE RICHIESTE

1. Secondo passaggio di sicurezza su PR #198 (denylist credenziali D1) nella chat claude.ai, col link della PR.
2. C4: decidere se `_e_log_kernel` va accoppiato a `handler.baseFilename` (sì/no).
3. E3: sostituire il token `gh` con quello senza Administration (`reports/setup_agente_non_admin.md`).
4. Sul Mac: `git checkout main && git pull` (era in detached HEAD).

## Esito

- **Merge PR #196** — FATTA (richiesta operatore; CI verde, bot neutral, nessuna ALTA/MEDIA).
- **Merge PR #198** — FATTA (richiesta operatore «mergia 198»; CI verde, bot neutral, verifica esterna APPROVATO CON RISERVE senza ALTA/MEDIA).
- **Riserve della verifica esterna #198 in `reports/stato_progetto.md`** — FATTA (V-2 e V-4 nuove; V-1 = R-161-1 esteso, V-3 = R-322-2). PR #199.
- **Note della verifica bot su #199** — FATTA (riserve della review del bot su #198 registrate come R-bot198-1..3; id stabili R-ve198-1..4).
- **Merge PR #199** — in corso, appena CI e bot sono verdi (richiesta operatore).
- **C3, C5a, C5c** — DEFERITE (fette a sé / sconsigliate dal revisore, vedi stato_progetto).

## Anomalie

- Un push con `-f` (non necessario) è stato bloccato dal classificatore dei permessi; rifatto come push normale.
