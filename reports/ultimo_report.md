# ULTIMO REPORT — 2026-10-20 — Dopo #222: README e cartelle di progetto alla firma, comando `gas fida-contatto`

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge di #222 (ok dell'operatore: «mergia 222 e parti con le due modifiche»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).

## Esito

- **R-ve222-4 — file letti dagli agenti alla firma dopo una lettura** — FATTA. Dopo che Gas ha letto un testo di terzi, write_file resta libero solo per documenti md/txt/csv in sottocartelle di lavoro (es. `dati/`). Vanno alla firma: i file nella radice del repo (README.md…), le cartelle di progetto (tests, tools, docs, clients, scripts, brains, modules) e i nomi di istruzioni per agenti in qualunque cartella (README, AGENT*, CLAUDE, GEMINI, SKILL, CONTRIBUTING, CONVENTIONS, copilot-instructions, requirements*). Review #377 APPROVATO CON RISERVE.
- **R-bot222-1 — comando `gas fida-contatto`** — FATTA. Senza chiave elenca i lead segnati «non fidati»; con la chiave mostra la scheda (da controllare) e chiede conferma y/N, poi toglie il segno scrivendo una riga di diario `contatto_fidato` nella stessa transazione. Solo comando umano, non tool dell'agente. Review #377.
- **Riserve di #377** — R-377-1 BASSA (un tool inventato «contatto_fidato» poteva falsificare la traccia nel diario) e R-377-2 COSMETICA (AGENT.md, CONVENTIONS.md liberi) CHIUSE. Review #378 APPROVATO CON RISERVE: R-378-1 BASSA, il prefisso «agent» manda alla firma anche file come `dati/agente_vendite.md` (solo attrito).
- **Test** — kernel 916 → 923 PASS, 0 FAIL; pytest tests/ 1519 passed.
