# Diff di sessione — 2026-10-20 — chat Voce, fetta 1

File toccati (base: punto di fork da origin/main):

- `.github/workflows/ci.yml` — lo step della voice suite lancia anche i test di trascrizione (stt) e sintesi (tts): prima non giravano in CI.
- `.claude/agents/memoria_revisore.md` — riga della review #384 (chat Voce), scritta dal revisore.
- `reports/stato_progetto.md` — riga «Voce — fetta 1» con le riserve R-384-1/R-384-2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine fetta.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
- Merge di origin/main (#227, #228) nel ramo (`5b90d69`): `.claude/agents/memoria_revisore.md` (voce #384 chat Voce dopo #384–#387 di main, voce #388), `reports/stato_progetto.md` (suffissi «chat Motore»/«chat Voce» su #384/R-384-x, riserve R-388-1/2).
- Correzione del bocciato del bot su `cf64653`: le modifiche a `reports/stato_progetto.md` dichiarate nel merge ora ci sono davvero; `reports/ultimo_report.md` allineato sull'etichetta.
