# ULTIMO REPORT — 2026-10-19 — Regola «fonte unica = il repo» (PR #219)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #219 (https://github.com/Gasss23/Gas/pull/219): tocca `CLAUDE.md`; l'agente la mergia solo con APPROVATO pulito del bot.
2. Incollare il testo di `claude/roadmap_completa.md` (solo nel progetto claude.ai): serve per aggiornare `reports/roadmap.md` con le decisioni del 19 ott.
3. Collegare il repo GitHub al progetto Gas su claude.ai (`reports/`, `CLAUDE.md`).

## Esito

- **Regola in CLAUDE.md** (§3): roadmap, decisioni e note di strategia vivono nel repo; il progetto claude.ai le legge da GitHub; un documento che sta solo nel progetto non va ricostruito a memoria — FATTA (PR #219, ramo `feat/merge-automatico-z1xjx2`).
- **Regola delle risposte brevi** — già presente in CLAUDE.md (§3, punto 4): non duplicata.
- **Aggiornamento della roadmap** — BLOCCATO: il file sorgente non è leggibile da questa sessione (nessuno strumento Projects/`project_read`; cercato su disco, nel repo e in tutti i rami: assente).

## Anomalie

- La sessione cloud non legge i documenti dei progetti claude.ai: è il motivo della nuova regola.
