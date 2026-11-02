# Diff della sessione — 2026-11-02 — Voce V9, rumore (chat M2)

- `clients/voice/browser_client.html` — microfono filtrato (noiseSuppression, echoCancellation, AGC da `/config`), soglia che segue il rumore di fondo, grazia di 500 ms sull'interruzione.
- `clients/voice/browser_server.py` — `/config` porta anche `agc` (`GAS_VOICE_AGC=0` lo spegne).
- `tests/test_unit_voice_server.py` — test nel browser coi modi «rumore_costante» (grazia) e «rumore_forte» (soglia d'ascolto dal fondo) e test di `GAS_VOICE_AGC`.
- `reports/prova_voce_mac.md` — rimedio `GAS_VOICE_AGC=0` con ventola o TV.
- `.claude/agents/memoria_revisore.md` — review #630–#631-M2, #657-M2, #658-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
