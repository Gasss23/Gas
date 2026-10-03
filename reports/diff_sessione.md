# DIFF SESSIONE — 2026-10-03 — C4b-3 (feat/cancello-c4b3)

| File | Cosa è cambiato e perché |
|---|---|
| `gas.py` | Nuovo `_storia_esito_firma`: l'esito della firma entra nella storia come blocco del kernel, così il modello lo vede al turno dopo (R-c4b2-1). `applica_firma` lo chiama e, per `run_command`, ricava "eseguita" da `_run_command_meta` invece che dal testo dell'output (R-c4b2-9, R-c4b3-1). |
| `tests/test_unit_kernel.py` | Nuovi T78a-k: blocco in storia, persistenza, payload del turno dopo, round-trip §7, dedup, rifiuto, contaminazione, DENY, dry-run, output che imita il dry-run o un diniego, meta residuo, fail-safe. |
| `scripts/check_verdetto.py` | Gate B: risolve le citazioni di contesto (file a HEAD) e i nomi corti univoci, per chiudere il falso positivo F-controlli-auto che bloccava il fine-task. |
| `tests/test_unit_handoff_check.py` | 5 test sulla risoluzione: contesto, nome corto, riga fuori range, ambiguo, inesistente. |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #133, #134 e #135. |
| `reports/stato_progetto.md` | Voce C4b-3; R-c4b2-1, R-c4b2-9, R-c4b3-1 e R-c4b3-2 chiuse; aperte R-c4b3-3, R-c4b3-4 e R-c4b3-5; F-controlli-auto (path corti) chiusa con R-135-1/2/3. |
| `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task. |

La storia completa sta in git.
