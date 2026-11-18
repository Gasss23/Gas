# Diff sessione — 2026-11-17 — Presentazione clienti + CI rossa su Ubuntu 26.04

File toccati (da `git diff --stat BASE..HEAD` + report di fine task):

- `modules/web/browser.py` — nuova `_programmi_fuori`: nel sandbox bwrap del browser i programmi di /usr/bin che sono collegamenti a file fuori dalle cartelle permesse (coreutils di Ubuntu 26.04 in /usr/lib/cargo/…) tornano eseguibili: si rifanno i collegamenti intermedi e si monta in sola lettura il solo file eseguibile vero, se la catena sta sotto /usr (non /usr/local) o /etc/alternatives e fuori da Gas e dalla home. Motivo: CI rossa dal 17/11 (ubuntu-latest passato a 26.04, 7 test bwrap rossi).
- `tests/test_unit_web_browser.py` — elenco dei file ammessi nel sandbox esteso ai soli file raggiunti dai collegamenti di /usr/bin (calcolato dall'host); 2 test nuovi (esecuzione via catena in bwrap; casi rifiutati: Gas/home, rotto, fuori radici, ciclo, cartella-collegamento, non eseguibile, cartella esclusa).
- `.claude/agents/memoria_revisore.md` — lezioni delle review della sessione (scritte dal revisore).
- `presentazione_clienti/build.py` — generatore del PDF: versione 3, stile HUD scuro, 8 pagine, linguaggio per chi investe la prima volta (per ogni servizio: cos'è, come funziona, numeri); dati reali del copy trading Forex (catalogo TSF) invariati.
- `presentazione_clienti/render.js` — stampa l'HTML in PDF con il Chromium di Playwright.
- `presentazione_clienti/titoli_svg.json` — cache dei titoli sfumati convertiti in tracciati.
- `presentazione_clienti/Presentazione_Ecosistema.pdf` — il PDF consegnato all'operatore (versione 3).
- `presentazione_clienti/.gitignore` — esclude l'HTML generato.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
