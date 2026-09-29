# DIFF SESSIONE — 2026-09-29 (K3+K4 sessione 2: re-review, E2E LLM, CI finale)

> Fotografia dell'ultima sessione. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Tipo | Cosa è cambiato e perché |
|------|------|--------------------------|
| `tests/e2e/e2e_k3k4_llm.py` | nuovo | FETTA B: E2E con provider LLM reali (3 domande + giro iniettivo); parsing tool calls da k.history; review #110 APPROVATO CON RISERVE. |
| `.claude/agents/memoria_revisore.md` | modificato | Review #109 e #110 aggiunte (APPROVATO CON RISERVE). |
| `reports/ultimo_report.md` | modificato | Report sessione 2: FETTA A/B/C, finding F-no-ricorda-1/F-like-1/F-inject-no-match. |
| `reports/handoff.md` | modificato | Dossier sessione 2: §0 PR #102, §2/§3 git aggiornati, §4 verdetti #109/#110, §5 delta test, §6 CI finale. |
| `reports/diff_sessione.md` | modificato | Questo file (sessione 2). |

## Commit di sessione (sessione 2, da BASE 57c5d90)

```
(vedere §3 handoff per log completo)
```

## Note

- `gas.py`, `brains/`, `modules/` NON toccati (FETTA B è sola misura).
- `tests/test_unit_kernel.py` NON toccato (suite invariata: 383 PASS, 5 FAIL F-mac-1).
- `tests/e2e/e2e_k3k4_llm.py` è il primo script E2E vero con provider reali del progetto.
- Provider detection "sconosciuto" è un limite tecnico (non esposto da run_turn): side effect atteso.
