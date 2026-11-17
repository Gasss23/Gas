# Diff della sessione — 2026-11-17 — CRM clienti, prima bozza (fetta 1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/crm/store.py`: tabelle `crm_*` nel file della memoria; soldi in centesimi; registro movimenti e diario CRM immutabili (trigger), storno per correggere; una proposta aperta per cliente (indice unico parziale); orologio iniettabile.
- `modules/crm/analisi.py`: conti puri (capitale, profitto per mese, commissioni, rendimento osservato, affinità tra servizi, panoramica della dashboard).
- `modules/crm/motore.py`: il CRM che legge se stesso — proposte da approvare (nuovo servizio → dopo un no aumento di capitale → presentazione di un amico), consenso, STOP, pause, tetti, insistenza crescente.
- `modules/crm/messaggi.py`: testi WhatsApp fissi (senza promesse, con nota sul rischio e riga STOP) e link wa.me.
- `modules/crm/server.py`, `modules/crm/web/*`: dashboard in tempo reale (SSE) solo su 127.0.0.1, token, cookie di sessione, CSP, anti-CSRF, controllo Host, blocco dei tentativi.
- `modules/crm/__main__.py`, `modules/crm/demo.py`, `modules/crm/__init__.py`: riga di comando, dati dimostrativi in un file separato.
- `tests/test_unit_crm.py`: suite nuova del CRM (101 test, comprese le regressioni dei giri #803/#806 e dei finding di bot e verifica esterna #381).
- Correzioni dopo bot e verifica esterna #381: proposta scartata = «non ora» per il motore; movimenti incoerenti rifiutati; riga STOP sempre in fondo; controlli e scritture in una transazione `BEGIN IMMEDIATE`; `anticipa_apertura`.
- `.github/workflows/ci.yml`: step «Run CRM suite».
- `.gitignore`: DB dimostrativo.
- `reports/crm.md` (nuovo), `reports/roadmap.md` (voce R11), `reports/*` di fine task, `.claude/agents/memoria_revisore.md`.
