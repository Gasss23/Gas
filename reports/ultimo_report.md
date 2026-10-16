# ULTIMO REPORT — 2026-10-16 — Cultura generale e knowledge base solo nel log

## DECISIONI UMANE RICHIESTE

1. Merge della PR #216 (https://github.com/Gasss23/Gas/pull/216). L'operatore l'ha già autorizzato se CI e test sono verdi.

## Esito

- **PR #215 mergiata** (CI verde, ok dell'operatore) — FATTA (`1a979a8`).
- **Seconda prova sul Mac** — FATTA dall'operatore: fette 2–3 verificate dal vivo (vedi stato_progetto).
- **Cultura generale con le proprie conoscenze; sui dati dell'utente mai inventare** — FATTA (regola nel prompt + descrizione di `ricorda`).
- **Avviso knowledge_fts a schermo** — FATTA: logger `gas.knowledge` a INFO per «DB assente» e «no such table»; altri errori restano WARNING.
- **V-1 bot/verifica #215** (proposte non fidate come metro anti-doppioni) — FATTA.
- **V-2 bot #215** (`now_iso_da` pubblico) — FATTA.
- **Test** — kernel 887 PASS (T92a–h; T69-fts-d aggiornato); pytest tests/ 1419 passed.
- **Review** — #355 APPROVATO CON RISERVE (R-355-1 BASSA, R-355-2 COSMETICA chiuse), #356 APPROVATO.

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
