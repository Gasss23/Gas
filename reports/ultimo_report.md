# ULTIMO REPORT — 2026-10-15 — Note rimaste su #213

## DECISIONI UMANE RICHIESTE

1. Merge della PR #214 (https://github.com/Gasss23/Gas/pull/214): tocca il motore, decide il verdetto del bot secondo la regola di merge.

## Esito

- **PR #213 mergiata** (richiesta dell'operatore, CI verde) — FATTA (`5dd2026`).
- **V-3 bot #213: ts del diario a larghezza fissa** — FATTA: microsecondi sempre presenti in `_now_iso` e nel limite della scadenza dei recap; righe vecchie non migrate (diario immutabile, errore <1 s).
- **R-350-1: T80x vacuo** — FATTA: cerca «RECAP PERTINENTE».
- **V-1 bot/verifica esterna #213: frasi vecchie in stato e roadmap** — FATTA.
- **Test** — kernel 870 PASS (T90j più stretto); pytest tests/ 1419 passed; mutazione su `_now_iso` → T90j fallisce.
- **Review** — #351 APPROVATO CON RISERVE: R-351-1 (COSMETICA, larghezza di `dal` senza test) tracciata; R-351-2 (stato da aggiornare) FATTA.

- **Promemoria per la prossima sessione** — FATTA: in `reports/stato_progetto.md` (inizio di «Prossimi passi») la lista di cosa verificare con l'operatore dopo la prova sul Mac (Mac aggiornato a `5dd2026`).

## Anomalie

- `gh` nella sessione cloud non è autenticato: stato PR/CI letto via MCP GitHub.
