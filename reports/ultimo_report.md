# ULTIMO REPORT — 2026-10-16 — Prova sul Mac e fetta «recap pertinente, lezioni non ripetute»

## DECISIONI UMANE RICHIESTE

1. Merge della PR #215 (https://github.com/Gasss23/Gas/pull/215): tocca il motore, decide il verdetto del bot secondo la regola di merge.

## Esito

- **PR #214 mergiata** (richiesta dell'operatore) — FATTA (`d0c7283`).
- **Prova FASE 2.6 sul Mac** — FATTA dall'operatore: riflessione a `clear` e Ctrl-C ok; recap fidato ripreso. Esito in stato_progetto.
- **Recap usato solo se pertinente** — FATTA: regola di `<recap_dati>` nel system prompt.
- **Niente lezioni quasi uguali** — FATTA: lezioni già decise nel prompt della riflessione (mai le `proposta`, R-352-1) + `_lezione_simile`.
- **Note rimaste da #214** (R-351-1, V-2 bot #214) — FATTA.
- **Bot #215 BOCCIATO (V-1 MEDIA)** — FATTA: le lezioni rifiutate nate da finestre non fidate non entrano più nel prompt della riflessione (review #354 APPROVATO, T91i).
- **Verifica esterna #215** — APPROVATO CON RISERVE: V-2 = V-1 del bot (chiusa), V-1 BASSA (somiglianza per parole, non per senso) tracciata come R-ve215-1.
- **Test** — kernel 879 PASS (T91a–i); pytest tests/ 1419 passed (prima delle correzioni R-352).
- **Review** — #352 APPROVATO CON RISERVE (R-352-1 MEDIA, R-352-2, R-352-3 chiuse), #353 APPROVATO, #354 APPROVATO.
- **Avviso knowledge_fts e risposta «win rate»** — SALTATA: fuori scope, registrati in stato_progetto.

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
