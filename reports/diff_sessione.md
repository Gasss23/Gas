# Diff della sessione — 2026-10-30 — Voce V4 (chat M2)

- `clients/voice/browser_client.html` — interruzione mentre Gas parla (`vigila`), rumore di fondo a mediana bassa con tetto (`sogliaDaCampioni`, soglia ≤ 0,045), un solo contesto per i bip, microfono chiuso se l'audio fallisce, `riapri()` col tetto dei turni.
- `clients/voice/browser_server.py` — `GAS_VOICE_INTERRUZIONE` in `/config`.
- `modules/voice/server.py` — `ISTRUZIONE_VOCE_SCHERMO` (riassunto + dettaglio), parte parlata = primo paragrafo, tetto orario dei turni parlati (`GAS_VOICE_MAX_TURNI_ORA`, 429).
- `.github/workflows/ci.yml` — Node + Playwright 1.63.0 + Chromium; test della pagina obbligatori nella voice suite.
- `tests/test_unit_voice_server.py`, `tests/test_unit_voice_stt.py` — giri «interruzione» e «sì subito», paragrafi, istruzione con schermo, tetto orario, /config, browser obbligatorio.
- `.claude/agents/memoria_revisore.md` — lezioni delle review della fetta.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
