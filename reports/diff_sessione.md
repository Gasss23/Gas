# DIFF SESSIONE — 2026-10-25 sera (chat Motore, accensione del forte)

- `brains/claude_cli.py`: login scaduto riconosciuto con messaggio chiaro (limite prima, R-511-1); token limitati dentro `_costo_equivalente` (V-2 ve #265).
- `modules/notte/notte.py`: campo opzionale `cervello: forte` nel catalogo, passato a `run_turn`; campo vuoto → compito saltato (V-2 ve #269).
- `gas.py`: prefisso `/forte` nel terminale; `/forte` da solo → messaggio d'uso (V-3 ve #269).
- `tests/test_unit_claude_cli.py`, `tests/test_unit_kernel.py`, `tests/test_unit_notte.py`: test di login scaduto, limite con oauth, overflow, T99r, catalogo.
- `scripts/notte/catalogo_esempio.yaml`: spiegazione di `cervello: forte`.
- `reports/r2_regole_abbonamento.md`: passi di accensione sul Mac.
- `.claude/agents/memoria_revisore.md`: righe #511, #512 e #515 chat Motore (unite a quelle di main nel merge).
- `reports/stato_progetto.md`: punto 2 della RIPARTENZA chiuso.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
