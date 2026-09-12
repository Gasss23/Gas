# DIFF SESSIONE — 2026-09-12 (fix/gasmerge-ip-guard-mac)

> Si riscrive a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `scripts/gasmerge.sh` | Sostituzione `\b` con ERE portabile `(^|[^0-9.])..([^0-9.]|$)` in git grep e grep; rimozione `\b` nel sed loopback-strip. Fix F-mac-4: su macOS POSIX ERE `\b` non riconosciuto → gate IP silenziosamente disabilitato. |
| `.claude/agents/memoria_revisore.md` | Lezione review #97 aggiunta dal revisore (commit autonomo `191fa8a`). |
| `reports/ultimo_report.md` | Report canonico del task. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `reports/diff_sessione.md` | Questo file. |
