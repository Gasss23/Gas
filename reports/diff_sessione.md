# Diff Sessione — 2026-08-18 — fix/gasmerge-loopback-ok

File toccati: da `git diff --stat ${BASE}..HEAD` (rigenerato al passo 4bis).

| File | Cosa è cambiato | Perché |
|------|-----------------|--------|
| `scripts/gasmerge.sh` | Invariante IP: logica a 2 stadi (loopback strip + gasmerge-ip-ok) | Blocco 127.0.0.0/8 deve essere sempre lecito senza marker per non bloccare la pipeline vocale FASE 3 su localhost |
| `tests/test_unit_gasmerge.py` | +130 righe: classe `TestLoopbackExemption` con 7 test reali | Coprono tutti i requisiti (127.0.0.1, 127.0.0.53, 0.0.0.0, IP pub, riga mista CRITICO, marker, regressione) |
| `.claude/agents/memoria_revisore.md` | +1 riga: entry #74 (APPROVATO 2026-08-18) | Aggiornamento contatore revisore post-review |
| `reports/ultimo_report.md` | Riscritto (fine-task) | Reporting canonico del task |
| `reports/handoff.md` | Riscritto (fine-task) | Dossier di sessione |
| `reports/diff_sessione.md` | Riscritto (fine-task) | Fotografia sessione corrente |
| `reports/stato_progetto.md` | Aggiornamento data, contatore review (72→74), stato corrente | Fotografia viva del progetto aggiornata a fine task |

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
