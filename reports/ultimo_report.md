# ULTIMO REPORT — 2026-10-15 — FASE 2.6 fetta 3: il ricordo giusto

## DECISIONI UMANE RICHIESTE

1. Merge della PR #213 (https://github.com/Gasss23/Gas/pull/213): tocca il motore, decide il verdetto del bot secondo la regola di merge.

## Esito

- **Recap pertinente al messaggio** — FATTA: tra i recap fidati sceglie quello con più parole in comune (almeno 2); altrimenti il più recente.
- **Scadenza del recap** (R-199-3) — FATTA: oltre `GAS_RECAP_MAX_GIORNI` giorni (default 7) il recap non viene più iniettato.
- **Seguito bot #213** — FATTA: tra i recap pertinenti vince il più recente (V-1 BASSA), intestazione «RECAP PERTINENTE» (V-2 cosmetica); test sul formato del ts (V-1 verifica esterna). Review #350 APPROVATO CON RISERVE (R-350-1 cosmetica tracciata).
- **Riga lunga in setup_notte.md** (cosmetica bot #212) — FATTA.
- **Test** — kernel 870 PASS in locale (T90a–j, T90c2, T90c3; la CI ne conta 2 in più, test del profilo sandbox); mutazioni mordono; pytest tests/ 1419 passed dopo il seguito del bot.
- **Review** — #348 APPROVATO CON RISERVE (R-348-1 chiusa nella stessa PR), #349 APPROVATO, #350 APPROVATO CON RISERVE.
- **Bot #213** — APPROVATO CON RISERVE: V-1, V-2 chiuse; V-3 (numeri di test nel dossier contro la CI) corretta qui. **Verifica esterna #213** — APPROVATO CON RISERVE: V-1 chiusa col test T90j, V-2 già dichiarata, V-3 tracciata (R-ve213-3).
- **Prova con conversazioni reali** — DEFERITA: nessun DB né chiave nel container.

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
