# Diff della sessione — 2026-11-25 — Dashboard del CRM anche dal telefono

Si riscrive a ogni sessione; la storia completa sta in git. Ramo ripartito da main b100f8d4 (PR #404 mergiata).

- `modules/crm/server.py`: `nome_tailscale_da_env` (solo nomi `*.ts.net`); `_host_ammesso` accetta il nome del Mac solo sulla 443 e rifiuta ogni richiesta con l'header del funnel; cookie `Secure` dal nome Tailscale.
- `modules/crm/__main__.py`: passa il nome allo stato del server e stampa l'indirizzo per il telefono.
- `scripts/crm/telefono.sh` (nuovo): accende, spegne e controlla l'accesso dal telefono con `tailscale serve`.
- `scripts/crm/spegni.sh`: spegne anche l'accesso dal telefono.
- `tests/test_unit_crm.py`: test del server e degli script con un Tailscale finto.
- `reports/crm/guida.md`, `reports/crm/decisioni.md` (punto 21).
- `.claude/agents/memoria_revisore.md`: review #860–#862.
- `reports/stato_progetto.md`, report di fine task.
