# ULTIMO REPORT — 2026-10-20 — Avviso sui file delicati più preciso

Ramo `feat/merge-automatico-z1xjx2`, dopo il merge di #230 (operatore: «mergia 230 e continua con la roadmap»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

## Esito

- **R-387-1 + note di verifica esterna e bot su #230** — FATTA. L'avviso sui file nuovi delicati guarda tutto il nome (parole intere ed estensioni interne come «a.sh.txt»), riconosce più tipi di file (.sql, .db, .terminal, .fish, .go…) e mostra la coda del percorso, così il nome del file è sempre visibile. Review #388 (chat Motore) APPROVATO CON RISERVE (R-388-1 e R-388-2 della chat Motore).
- **Test** — kernel 947 → 949 PASS, 0 FAIL; pytest tests/ 1573 passed.
