# ULTIMO REPORT — 2026-10-20 — Avviso sui file nuovi delicati (R-223-2), fonti di studio solo dentro knowledge/

Ramo `feat/merge-automatico-z1xjx2`, dopo il merge di #228 (operatore: «mergia 228 e fai tu la correzione su tools»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

## Esito

- **R-223-2 — avviso sui file nuovi delicati** (decisione del 19 ottobre) — FATTA. Quando Gas crea un file NUOVO libero che sembra delicato (configurazioni, script, chiavi, nomi da credenziali) arriva un avviso su Telegram, solo informativo, uno per turno e sempre sotto il limite di lunghezza. I documenti normali passano in silenzio. Review #386 BOCCIATO (R-386-1 MEDIA: messaggio oltre il limite che non partiva, chiusa; R-386-2 BASSA: falsi allarmi su nomi come «cronologia.md», chiusa) → #387 APPROVATO CON RISERVE (R-387-1 BASSA).
- **Fonti di studio solo dentro knowledge/** (V-1 bot #228, «fai tu la correzione su tools») — FATTA. L'ingest rifiuta le fonti fuori da `knowledge/`; nuovo test e step di CI.
- **Test** — kernel 944 → 947 PASS, 0 FAIL; pytest tests/ 1558 passed.
