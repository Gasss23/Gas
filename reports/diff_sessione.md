# Diff della sessione — 2026-11-24 — Revisione in più sugli script del CRM

Si riscrive a ogni sessione; la storia completa sta in git. Ramo ripartito da main 96d5ae99 (PR #403 mergiata).

- `.claude/perimetro_review.txt`: aggiunta `scripts/crm/` (decisione 20: dati personali dei clienti, revisione in più).
- `reports/crm/decisioni.md`: punto 20.
- `reports/bacheca.md`: notizia per le altre chat (`scripts/crm/` nel perimetro); chiusa la notizia del 23-11 sul collegamento di Gas al CRM (PR #397 mergiata).
- `scripts/crm/installa.sh`: `togli_servizio` (prima il plist, poi il bootout) a ogni STOP dopo la scrittura del plist; prova di `import gas` con uscita 4; trap che toglie il servizio a ogni uscita prima che la dashboard risponda (anche Ctrl+C, anche un secondo Ctrl+C); riga «Aspetto che la dashboard risponda».
- `modules/crm/store.py`: `CRMStore.backup` tiene la copia più recente di ognuno degli ultimi 30 giorni più le ultime 10; non cancella mai la copia appena fatta; ignora i file con un nome fuori formato e quelli con data nel futuro (avviso nel registro).
- `modules/crm/copia_cifrata.py`: `_ruota` per le copie cifrate fuori dal Mac: stesse protezioni (copia appena fatta, nomi fuori formato, date nel futuro).
- `tests/test_unit_crm.py`: test delle copie locali e cifrate (riavvii, orologio indietro o avanti, margine di un giorno, copie a mano) e 17 test di `installa.sh`/`spegni.sh` con comandi finti.
- `reports/crm/guida.md`: regola nuova delle copie.
- Merge di main (PR #401 del funnel): report del ramo tenuti, memoria unita, riserve della #401 in `reports/stato_progetto.md`.
- `.claude/agents/memoria_revisore.md`: review #853–#859.
- `reports/stato_progetto.md`, report di fine task.
