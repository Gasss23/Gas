# Diff della sessione — 2026-11-07 — chat Mani, fetta 44

File toccati (base main c1a4503, dopo il merge della PR #341):
- `clients/voice/ascolto.py`:
  - eco di «Hey Jarvis» detto da Gas;
  - finestra 0–120;
  - reset dei turni quando la parola è detta nella finestra;
  - tolleranza della pausa dopo la parola, con tetto.
- `scripts/voce/riprendi.sh`, `scripts/voce/pausa.sh`: controllo che l'ascolto resti acceso, messaggio «non installato».
- `scripts/voce/LEGGIMI.md`: pausa dopo la parola, conto dei turni, limiti della finestra, frase del bip.
- `tests/test_unit_voce_ascolto.py`: test della fetta 44 e delle riserve della #341.
- `reports/proposta_parola_gas.md`: proposta per addestrare «Hey Gas».
- `.claude/agents/memoria_revisore.md`: righe delle review #677, #678, #702 e #703.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
