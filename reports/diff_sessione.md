# Diff sessione — 2026-09-02 (fix/tts-cap-testo)

> Fotografia dell'ultima sessione. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `modules/voice/tts.py` | Aggiunta funzione `_cap_text()` + chiamata all'inizio di `synthesize_speech()`. Cap deterministico `GAS_TTS_MAX_CHARS` (default 2000) per chiudere R-tts-1. Import `logging` e `os` aggiunti. |
| `tests/test_unit_voice_tts.py` | 7 nuovi test in classe `TestCapText` (TVT-cap-*). Import `_cap_text` aggiunto. 24/24 PASS. |
| `reports/stato_progetto.md` | R-tts-1 segnata CHIUSA; review count aggiornato a #96; voice suite count aggiornato a 24 PASS. |
| `reports/ultimo_report.md` | Report task corrente. |
| `reports/diff_sessione.md` | Questo file. |
| `reports/handoff.md` | Dossier di fine sessione. |

## Commit di sessione

- `a7f23e2` — fix(tts): cap deterministico GAS_TTS_MAX_CHARS su synthesize_speech — review #96 APPROVATO CON RISERVE
