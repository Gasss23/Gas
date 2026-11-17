# Diff della sessione — 2026-11-17 — voce: filtro sulla voce (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `scripts/voce/registra_voce.py` (nuovo): registrazione guidata e addestramento del verificatore.
- `clients/voice/ascolto.py`: verifica della voce (stato, caricamento sicuro del pkl, soglie base/verifica), fallback senza verifica, log.
- `scripts/voce/taratura_parola.py`: stesso rilevatore, messaggio `.venv/bin/python`.
- `scripts/voce/LEGGIMI.md`: sezione «Verifica della voce» e righe nuove della tabella.
- `tests/test_unit_voce_ascolto.py`: 27 test nuovi.
- `reports/guida_voce_in_giro.md` (nuovo).
- `.claude/agents/memoria_revisore.md`, `reports/*`: righe #803-#805 e report.
