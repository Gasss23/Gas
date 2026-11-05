# Diff della sessione — 2026-11-05 — chat Mani, fetta 41

File toccati (base main 830c5bf, dopo il merge della PR #333):
- `clients/voice/ascolto.py`: interruzione con la parola di attivazione mentre Gas parla (soglia 0.7, solo la parola), afplay in sottofondo (`RiproduzioneAfplay`), interruzioni sotto max_turni, `soglia_interruzione()` dall'ambiente.
- `scripts/voce/LEGGIMI.md`: come interrompere Gas, due righe nuove nella tabella delle regolazioni.
- `tests/test_unit_voce_ascolto.py`: test dell'interruzione, della riproduzione in sottofondo, delle guardie §9 e del tetto dei turni.
- `.claude/agents/memoria_revisore.md`: righe delle review #668 e #669 (con la lezione sui contatori azzerati dentro un ciclo con tetto).
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task (più l'esito della PR #333).

Questo file si riscrive a ogni sessione; la storia completa sta in git.
