# Diff della sessione — 2026-11-24 — Revisione in più sugli script del CRM

Si riscrive a ogni sessione; la storia completa sta in git. Ramo ripartito da main 96d5ae99 (PR #403 mergiata).

- `.claude/perimetro_review.txt`: aggiunta `scripts/crm/` (decisione 20: dati personali dei clienti, revisione in più).
- `reports/crm/decisioni.md`: punto 20.
- `scripts/crm/installa.sh`: funzione `togli_servizio` (bootout + rimozione del plist) a ogni STOP dopo la scrittura del plist; prova di `import gas` con uscita 4 e messaggio distinto.
- `modules/crm/store.py`: `CRMStore.backup` tiene la copia più recente di ognuno degli ultimi 30 giorni più le ultime 10 (prima: le ultime 30, che tanti riavvii in un giorno potevano consumare).
- `tests/test_unit_crm.py`: test nuovo sulla regola delle copie; test esistente adattato (`keep=2, ultime=2`).
- `reports/crm/guida.md`: regola nuova delle copie.
- `.claude/agents/memoria_revisore.md`: review #853 e #854.
- `reports/stato_progetto.md`, report di fine task.
