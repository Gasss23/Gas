# ULTIMO REPORT — 2026-10-15 — FASE 2.6 fetta 3: il ricordo giusto

## DECISIONI UMANE RICHIESTE

1. Merge della PR #213 (https://github.com/Gasss23/Gas/pull/213): tocca il motore, decide il verdetto del bot secondo la regola di merge.

## Esito

- **Recap pertinente al messaggio** — FATTA: tra i recap fidati sceglie quello con più parole in comune (almeno 2); altrimenti il più recente.
- **Scadenza del recap** (R-199-3) — FATTA: oltre `GAS_RECAP_MAX_GIORNI` giorni (default 7) il recap non viene più iniettato.
- **Riga lunga in setup_notte.md** (cosmetica bot #212) — FATTA.
- **Test** — kernel 868 PASS (T90a–i, T90c2); tre mutazioni mordono; pytest tests/ 1419 passed (prima della correzione R-348-1, che tocca solo `_recap_pin` e aggiunge T90c2).
- **Review** — #348 APPROVATO CON RISERVE (R-348-1 chiusa nella stessa PR), #349 APPROVATO.
- **Prova con conversazioni reali** — DEFERITA: nessun DB né chiave nel container.

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
