# DIFF SESSIONE — 2026-10-04 — fix/gate-autoprotezione

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/perimetro_review.txt` | Nuovo: perimetro di review unico (motore + macchina di controllo). |
| `.claude/hooks/review_gate.sh` | Perimetro dal file, in unione con voci cablate, index e HEAD; `--no-renames -z`; exit code di git preservato; limiti dichiarati. |
| `scripts/check_verdetto.py` | Perimetro unito alla base; citazioni sempre verificate; citazioni di codice; regex dei verdetti e code fence. |
| `.claude/verifica_esterna.md` | Nuovo: protocollo fisso della verifica esterna. |
| `.claude/commands/fine-task.md` | §4quater: verifica esterna con un agente nuovo a ogni fetta. |
| `.claude/agents/revisore.md` | Perimetro nella descrizione; forma canonica del verdetto nullo; niente "Verdetto finale:". |
| `.claude/settings.json` | Promemoria post-compact aggiornato al perimetro. |
| `.github/workflows/ci.yml` | La suite del gate gira in CI; commento sui check required. |
| `CLAUDE.md` | §3 perimetro di review; istituzione E; lucchetto main con handoff-check required. |
| `tests/test_unit_handoff_check.py` | V-1, V-2, R-136-2, R-136-5, R-138-2, R-138-3. |
| `tests/test_unit_hooks.py` | V-1 (a-d), R-138-1 (P7/P8), R-138-2 (P1/P2), blocco #139 (git finto). |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #138, #139 e #140. |
| `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task. |

La storia completa sta in git.
