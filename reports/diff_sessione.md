# DIFF SESSIONE — 2026-10-13 — Chiusura problemi aperti post #193

Base `04635d5` (merge della PR #197). Si riscrive a ogni sessione; la storia completa sta in git.

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/hooks/promemoria_end.sh` | A1: repo dal `cwd` del payload; contatore per `session_id` nel git-dir del worktree; `session_id` via ENVIRON (R-314-1). |
| `.claude/hooks/gate_matcher.py` | A2 (nuovo): decide se un comando è davvero un commit togliendo solo stringhe/heredoc inerti; nel dubbio testo grezzo. |
| `.claude/hooks/review_gate.sh` | A2: chiama `gate_matcher.py` dopo il grep grezzo; solo exit 3 lascia passare. |
| `scripts/bot_esito.py` | B1: niente gravità nuda nella prosa dopo NON VERIFICATO/RACCOMANDAZIONE; riserve con id alfabetico; id alfabetici anche in `_FINDING_GRAVE_A_PAROLE`. |
| `modules/gate/gate.py` | D1: nove buchi della denylist credenziali + varianti; pezzo di percorso > 255 caratteri negato. |
| `gas.py` | C1/C2/C5b: messaggio sui file grandi onesto; `letti` conta solo i file letti davvero; commento con le misure reali. |
| `tests/test_unit_hooks.py` | Test A1 (T-prom-wt-1..6) e A2 (TestGateMatcher). |
| `tests/test_unit_verifica_bot.py` | Test B1 (casi reali #193/#196 + forme che restano bloccanti). |
| `tests/test_unit_gate.py` | Test D1 (nuovi DENY e nomi simili leggibili). |
| `tests/test_unit_kernel.py` | Test C1/C2/R-326-1. |
| `.gitignore` | E1: `AGENTS.md`. |
| `.claude/agents/memoria_revisore.md` | Review #314–#327. |
| `reports/stato_progetto.md`, `reports/stato_storico.md` | Esito delle voci; lista originale spostata nello storico. |
| `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task. |
