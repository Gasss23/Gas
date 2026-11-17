# Diff sessione — 2026-11-17 — Presentazione clienti (prima bozza)

File toccati (da `git diff --stat BASE..HEAD` + report di fine task):

- `presentazione_clienti/build.py` — nuovo: genera la presentazione HTML 16:9 (15 pagine, grafici SVG, segnaposto per i dati mancanti).
- `presentazione_clienti/render.js` — nuovo: stampa l'HTML in PDF con il Chromium di Playwright.
- `presentazione_clienti/titoli_svg.json` — nuovo: cache dei titoli sfumati convertiti in tracciati (il build funziona anche senza fonttools/uharfbuzz).
- `presentazione_clienti/Presentazione_Ecosistema.pdf` — nuovo: la bozza consegnata all'operatore.
- `presentazione_clienti/.gitignore` — nuovo: esclude l'HTML generato.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
