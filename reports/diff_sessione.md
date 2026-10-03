# Diff sessione — 2026-10-03 — FETTA C4b-1 (feat/cancello-c4b1)

> Si riscrive a ogni sessione; la storia completa sta in git.

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/agents/revisore.md` | `model: opus` nel frontmatter (decisione operatore del 2026-10-01, mai applicata fino a oggi). |
| `.claude/agents/memoria_revisore.md` | Riga #128 e lezione sulla non-ermeticità dei test quando un percorso acquista un effetto di rete. |
| `gas.py` | Nuovo `_parcheggia_e_notifica`: accodamento con anti-doppioni/tetto, read-back Telegram, revoca + diniego se il read-back non parte; diario dei percorsi del cancello senza args. |
| `modules/memory/store.py` | `accoda_approvazione` atomica (doppione/tetto), `revoca_approval` (solo rejected/kernel_revoca), `_approval_max_pending`, `_serializza_args`; R-c3-3/R-c3-4 in `resolve_approval`. |
| `modules/telegram/bot.py` | `componi_read_back`, `invia_read_back` (via `_tg_post`, niente parse_mode, niente troncamento), `lunghezza_telegram` (UTF-16), `parse_allowed_ids` (riusato da run_bot). |
| `tests/test_unit_kernel.py` | Finto trasporto `_TgFinto`; nuovi T75a-f (51 check); T70f/T70g/T72c/T74a/T74b con finto trasporto; T74e con patch su `accoda_approvazione`. |
| `reports/stato_progetto.md` | Stato C4b-1, chiusura R-c3-3/R-c3-4, riserve R-c4b1-1..4, finding della verifica C4a. |
| `reports/ultimo_report.md` | Report del task. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `reports/diff_sessione.md` | Questo file. |
