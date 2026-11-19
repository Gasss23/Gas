# Diff sessione — 2026-11-19 — «PDF servizi ecosistema»: versione definitiva

File toccati (da `git diff --stat BASE..HEAD` + report di fine task):

- `presentazione_clienti/build.py` — niente nome azienda (solo «GasTradeFx» in chiusura), niente bagliori CSS, contatti letti solo da un file locale ignorato da git (`--senza-contatti` per la versione del repo), pag. 4 e pag. 7 riformulate, tutte le avvertenze del catalogo d'esempio, codice e CSS morti tolti.
- `presentazione_clienti/render.js` — nome del PDF in uscita come argomento (predefinito «PDF servizi ecosistema.pdf»).
- `presentazione_clienti/PDF servizi ecosistema.pdf` — PDF definitivo SENZA contatti (rinominato da Presentazione_Ecosistema.pdf).
- `presentazione_clienti/.gitignore` — ignora `contatti.local.json` e `privato/` (dati personali, repo pubblico).
- `reports/stato_progetto.md` — repo pubblico e dati personali; riserve del fix sandbox e del PDF; voce chiusa della CI tolta.
- `reports/stato_storico.md` — voce chiusa della CI 26.04 archiviata.
- `.claude/agents/memoria_revisore.md` — riga della review #815 (merge di main nel branch).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
