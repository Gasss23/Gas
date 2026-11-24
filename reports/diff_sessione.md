# Diff della sessione — 2026-11-24 — Dashboard del CRM sempre accesa sul Mac

Si riscrive a ogni sessione; la storia completa sta in git. Ramo ripartito da main 1b4954e2 (PR #397 mergiata).

- `scripts/crm/com.gas.crm.plist` (nuovo): LaunchAgent del CRM (parte all'avvio, si riavvia se cade, registro in `.gas_memory_crm_server.log`).
- `scripts/crm/installa.sh` (nuovo): installa il servizio dopo i controlli e mette l'icona «CRM Gas» sulla Scrivania.
- `scripts/crm/spegni.sh` (nuovo): toglie il servizio, i dati restano.
- `reports/crm/guida.md` §2: come accenderlo una volta per sempre.
- Merge di main (PR #398, #399, #400 di altre chat): codice identico a main.
- `.claude/agents/memoria_revisore.md`: review #852-MERGE.
- `reports/stato_progetto.md`, report di fine task.
