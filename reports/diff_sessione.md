# Diff della sessione — 2026-10-31 — Voce V5 (chat M2)

- `modules/voice/server.py` — ogni richiesta parlata che passa il tetto orario viene contata prima della trascrizione (R-581-2-M2).
- `tests/test_unit_voice_stt.py` — test del tetto con «uso» e trascrizione vuota.
- `reports/prova_voce_mac.md` — nuova: guida di prova della voce sul Mac.
- Merge di main (01eba0d, PR #312): portati i file della chat Mani (proxy web e test), senza cambi da parte di questa sessione.
- `modules/voice/server.py`, `reports/prova_voce_mac.md` — V-2: il tetto parla di «richieste a voce» (conta le chiamate a Groq).
- `.claude/agents/memoria_revisore.md` — riga della review della fetta.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
