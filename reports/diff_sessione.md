# DIFF SESSIONE — 2026-08-29

Sessione: Fetta A prompt hardening + Fetta B tool calcola()
Branch: sonda/vps-stato-2026-08-26

## File toccati (da `git diff --stat BASE..HEAD`)

- `gas.py` (+123 / -~) — Fetta A: system prompt aggiornato (7 tool in chiaro, run_command ristretto, fallback universale, self-intro unificata); Fetta B: importazioni `ast`+`math`, `_calcola_validate`, `_calcola_validate_func`, `_calcola`, schema `calcola` in tools_schema, dispatch in execute_tool_call.
- `gas_identity.md` (+11 / -1) — Fetta A: lista 7 tool nativi con bullet + descrizione per ciascuno; rimossa riga che elencava solo read_file/write_file/run_command.
- `tests/test_unit_kernel.py` (+35) — T62a-T62k: 16 nuovi test per tool calcola() (aritmetica, rifiuto exploit, edge case, dispatch kernel).
- `.claude/agents/memoria_revisore.md` (+1) — aggiornamento automatico dal revisore (#93 APPROVATO CON RISERVE).
- `reports/stato_progetto.md` — aggiornato: 93 review, suite 292 PASS, contatore aggiornato.
- `reports/ultimo_report.md` — report canonico task Fetta A+B.
- `reports/handoff.md` — dossier fine sessione (questo documento e il successivo).
- `reports/diff_sessione.md` — questo file (si riscrive a ogni sessione).
