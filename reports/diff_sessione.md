# Diff della sessione — 2026-11-05 — chat Mani, fetta 42

File toccati (base main 6a4cb2e, dopo il merge della PR #338):
- `clients/voice/ascolto.py`: «Sì, signore?» dopo la parola (`scarica_conferma`, classe `Conferma` in memoria con download in sottofondo, `_conferma_o_bip`, `conferma_attiva`), con ripiego sul bip su qualsiasi errore.
- `scripts/voce/LEGGIMI.md`: spiegazione di «Sì, signore?» e variabile `GAS_ASCOLTO_CONFERMA`.
- `tests/test_unit_voce_ascolto.py`: test della conferma (conversazione, server finto, classe, main) e test d'integrazione col VoiceHandler vero.
- `.claude/agents/memoria_revisore.md`: righe delle review #671, #672, #675.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task (più la PR #338 mergiata).

Questo file si riscrive a ogni sessione; la storia completa sta in git.
