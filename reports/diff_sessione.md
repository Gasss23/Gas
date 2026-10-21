# DIFF SESSIONE — 2026-10-21 (chat Motore, R7 R-c4b3-3)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `recupera_esito_firma` (esito dal DB in storia dopo un'interruzione, mai una nuova esecuzione), helper `_tag_esito_firma`/`_esito_firma_in_storia`.
- `modules/telegram/bot.py` — `_riprova_orfana` chiama il recupero se l'azione era già reclamata; commento «un click alla volta» (R-445-2).
- `tests/test_unit_kernel.py` — T78l (crash simulato e riavvio), T78m (esiti OK/KO/incerto/dry-run/write_file), T78n (niente da recuperare).
- `.claude/agents/memoria_revisore.md` — righe #445, #446, #447.
- `reports/da_mergiare.md` — «Da fare domattina» per l'operatore e voce della PR #241.
- `reports/stato_progetto.md`, `reports/roadmap.md` — R-c4b3-3 chiusa.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
