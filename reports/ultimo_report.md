# ULTIMO REPORT — 2026-10-20 — Catalogo delle fonti alla firma, taglio degli avvisi, lavoro in parallelo

Ramo `feat/merge-automatico-z1xjx2`, dopo il merge di #226 (operatore: «mergia 226 quando è verde e continua con la roadmap»; poi «l'altra chat lavora sulla voce, tu resta sul motore»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

## Esito

- **R-383-1 — avvisi che nascondevano il testo dopo un «<»** — FATTA. Nuova `tronca_visibile` (bot.py) usata dagli avvisi dei lead e delle firme scadute: taglio che non spezza i caratteri resi visibili e non cancella il resto del valore (V-1 bot #226, V-2 verifica esterna #226). Review #384 APPROVATO CON RISERVE (R-384-1 COSMETICA).
- **Roadmap 5.3 — catalogo delle fonti di studio scrivibile da Gas** — FATTA. Ogni scrittura in `knowledge/` (catalogo `sources.yaml` e file delle fonti) va alla firma. Più due cosmetiche del bot #226 (nomi nei log, numerazione in doctor). Review #385 APPROVATO.
- **Lavoro in parallelo** — regole per due chat (Motore e Voce) in `reports/lavoro_parallelo.md`.
- **Test** — kernel 941 → 944 PASS, 0 FAIL; pytest tests/ 1529 passed.
