# Ultimo report — 2026-11-09 notte — Voce: cache delle frasi fisse (chat M2)

## DECISIONI UMANE RICHIESTE

- **Merge della #356: decide l'operatore** (CLAUDE.md §10: con riserve si aspetta il suo sì; nessuna regola notturna scritta nel repo). Prossima: server voce sicuro, resta aperta per l'operatore.

## Esito delle fette

- **PR #354**: `MERGIATA` (fa6b1f3).
- **Cache della sintesi per le frasi fisse**: `FATTA` (niente attesa né costo ElevenLabs per «Dimmi.» e simili).
- **Riserve BASSE della #354**: `FATTE`. Review #715-M2 APPROVATO CON RISERVE (R-715-1-M2 COSMETICA).
- Test: 243 passed.
- **Bot #356 (BOCCIATO su 6872080)**: MEDIA sul report (riga «nessuna decisione») corretta; log dell'handoff in ordine reale; test che le risposte vere usano la cache. Review #721-M2 APPROVATO.
- **Riserve della verifica esterna #356**: V-1 (test su `_finiti_jobs`), V-2 (righe vuote), V-3 (handoff) `FATTE`; V-4 BASSA registrata. Review #719-M2 APPROVATO.
- **Merge di main (#355 di Mani) nel branch**: `FATTO` (2580889), review #716-M2 APPROVATO; test dei 4 file toccati: 558 passed.
- #356 con riserve: resta per l'operatore (CLAUDE.md §10; nessuna regola notturna scritta nel repo).

## Anomalie

- Nessuna.
