# DIFF SESSIONE — 2026-08-29

Sessione: Chiusura riserve calcola() — tetto anti-DoS + test stringenti
Branch: sonda/vps-stato-2026-08-26

## File toccati (da `git diff --stat BASE..HEAD`)

- `gas.py` — Fetta A: system prompt hardening (7 tool in chiaro, run_command ristretto, fallback universale, self-intro unificata); Fetta B: _calcola() parser AST whitelist; questa sessione: tetto anti-DoS (MAX_EXP/MAX_DIGITS/MAX_FACTORIAL, pow rimosso dai builtin), whitelist AST esplicitata in commento.
- `gas_identity.md` — lista 7 tool nativi aggiornata con bullet list.
- `tests/test_unit_kernel.py` — T62a-T62k (sessione precedente) + T62l-T62p (questa sessione, 8 nuovi test anti-DoS); T62f: condizione stringente solo "Rifiutato:".
- `.claude/agents/memoria_revisore.md` — review #93 (APPROVATO CON RISERVE) e #94 (APPROVATO) registrate.
- `reports/stato_progetto.md` — aggiornato: 94 review, suite 299 PASS.
- `reports/ultimo_report.md` — report canonico task chiusura riserve calcola().
- `reports/handoff.md` — dossier fine sessione (questo documento e il successivo).
- `reports/diff_sessione.md` — questo file (si riscrive a ogni sessione).
