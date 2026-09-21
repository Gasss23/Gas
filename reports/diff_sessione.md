# DIFF SESSIONE — 2026-09-15

Branch: `feat/voice-client-4b`
Sessione: FASE 3 Fetta 4b — Client Vocale Browser HTML5

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `clients/voice/browser_server.py` | NUOVO. Proxy HTTP stdlib (127.0.0.1:9000 → :8765): serve browser_client.html + forwarda POST /voice con Bearer auth aggiunto lato server. Approccio same-origin: zero CORS, zero modifiche a modules/. |
| `clients/voice/browser_client.html` | NUOVO. Client HTML5: getUserMedia → MediaRecorder(webm/opus) → POST /voice → play MP3. Tema dark/light, shortcut Space, status monospace con byte+tempo. Font Figtree + JetBrains Mono. |
| `reports/stato_progetto.md` | Aggiornato: data ultimo aggiornamento + aggiunta riga Fetta 4b (✅ FASE 3 Fetta 4b) con esito, byte e tempi reali. |
| `reports/ultimo_report.md` | Riscritto: report completo Fetta A (sonda) + Fetta B (client browser). Nuovi rispetto al precedente: tabella test E2E, istruzioni uso, analisi CORS. |
| `reports/handoff.md` | Riscritto per questa sessione (dossier autonomo fine-task). |
| `reports/diff_sessione.md` | Questo file — riepilogo sessione. |

## NON toccato

- `gas.py`, `brains/`, `modules/`, `tests/` — invariati
- `.env` — token ruotato su disco (gitignored, non committato)
- Suite test — invariata, 64 PASS precedenti confermati
