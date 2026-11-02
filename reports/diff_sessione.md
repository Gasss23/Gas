# Diff della sessione — 2026-11-02 — Voce V7a, misura dei tempi (chat M2)

- `modules/voice/server.py` — `_segna`/`_chiudi_tempi` per richiesta; tempi nel JSON e in `X-Gas-Tempi`; riga `gas.voce.tempi` a INFO; convivenza col reset di `_capito` della V6; il tempo del server parte dopo la ricezione dell'audio.
- `clients/voice/browser_client.html` — riga «tempi: ascolto · cervello · voce · rete» (textContent, solo numeri finiti), anche sui guasti, fuori dal riquadro della risposta; il riquadro resta nascosto fino alla prima risposta.
- `tests/test_unit_voice_stt.py` — test V7: tempi nel JSON e nel log, MP3 con intestazione, TTS fallito, kernel che si rompe, 429 senza tempi.
- `tests/test_unit_voice_server.py` — la pagina mostra i tempi.
- `.claude/agents/memoria_revisore.md` — review #614–#616-M2, #643–#647-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
