# Diff della sessione — 2026-11-12 notte — voce: prima frase subito (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/voice/server.py`: `AnticipoVoce(pronto=…)`; `_invia_anticipo`/`_prendi_risposta` (stato della risposta sotto lucchetto); `_send_json`/`_send_audio`/`_do_pezzi_response` consapevoli dell'anticipo; `_PAROLA_NELLA_FRASE`; niente anticipo con compiti finiti da dire.
- `clients/voice/ascolto.py`: `_Frasi.errore_turno` e bip d'errore se il turno fallisce dopo la prima frase.
- `tests/test_unit_voice_server.py`, `tests/test_unit_voce_ascolto.py`: test nuovi.
- `.claude/agents/memoria_revisore.md`, `reports/*`: righe #799/#801 e report.
