# Diff sessione — R-crm-1b Fetta 3: dedup telefono (2026-07-27)

> Riscritto a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `modules/memory/store.py` | Aggiunta `normalizza_telefono` (funzione pura, gate plausibilità IT) + `rileva_duplicati_telefono` (specchio 1:1 di `rileva_duplicati_email`, SOLA LETTURA, diario idempotente) |
| `modules/memory/__init__.py` | Aggiunta `normalizza_telefono` a import e `__all__` per esportarla dal modulo |
| `tests/test_unit_kernel.py` | Aggiunto import `normalizza_telefono` + 22 test T60a–T60m (12 unit su `normalizza_telefono`, 10 integration su `rileva_duplicati_telefono`) |
| `reports/stato_progetto.md` | R-crm-1b marcato ✅ CHIUSO; riserve R1/R2 tracciate |
| `reports/ultimo_report.md` | Report di fine task (sovrascritto da sessione precedente) |
| `.claude/agents/memoria_revisore.md` | Aggiornato dal revisore (#67, riga contatore aggiunta) |
