# Diff sessione — 2026-07-20 — scrub IP/SSH dai canonici + roadmap privatizzazione

> Fotografia della sessione corrente. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Cosa è cambiato | Perché |
|------|----------------|--------|
| `reports/stato_progetto.md` | §8: IP → `<VPS_IP>`, utente `gas` → `<VPS_USER>`, dropin → `<SSH_DROPIN>`, key type → `<KEY_TYPE>`; aggiunta riga ⚠️ SCRUB in cima a item §8 | Rimozione IP e superficie SSH dai file HEAD (MITIGATO) |
| `reports/runbook_s1_hardening.md` | 8 occorrenze del valore IP del VPS → `<VPS_IP>` | IP esposto nel runbook eseguito manualmente in sessione S1 |
| `reports/roadmap.md` | Voce 0 aggiunta in cima a PROSSIMI PASSI: 🔒 Privatizzare repo ALTA URGENZA | Tracciare l'azione necessaria a chiudere definitivamente la questione IP |
| `reports/ultimo_report.md` | Riscritto con esito task e decisioni umane richieste | Reporting canonico di fine task |
| `reports/handoff.md` | Riscritto con dossier sessione completo | Dossier autonomo per revisione esterna |
| `reports/diff_sessione.md` | Riscritto per questa sessione | Fotografia sessione corrente |

## Commit di sessione

```
1ce0148 chore(scrivi-rep): report task scrub IP/SSH (683cd08)
683cd08 docs(security): scrub IP/SSH dai canonici (MITIGATO) + roadmap privatizzazione
```
