# Ultimo report — 2026-10-20 — Voce, fetta 1: test di trascrizione e sintesi in CI (chat Voce)

## DECISIONI UMANE RICHIESTE

1. Ok al merge della PR #229 (https://github.com/Gasss23/Gas/pull/229): tocca `ci.yml`, quindi `verifica-bot` darà neutral e il merge lo decidi tu.
2. Etichetta `verifica` sulla PR #229 (l'agente non ha `gh` autenticato in questa sessione cloud).

## Esito

- **Fetta 1 — test stt/tts nei test automatici**: `FATTA`. In `.github/workflows/ci.yml` lo step della voice suite lancia anche `tests/test_unit_voice_stt.py` e `tests/test_unit_voice_tts.py` (52 test, Groq ed ElevenLabs finti). Toccare `ci.yml` (fuori dall'area Voce) è stato autorizzato dall'operatore in sessione. Prove: 52/52 con la rete vera bloccata e senza chiavi; 72/72 le tre suite insieme.
- Review #384 (chat Voce): APPROVATO CON RISERVE — R-384-1 BASSA (urllib verso 127.0.0.1 segue `http_proxy`), R-384-2 COSMETICA (commento di ci.yml impreciso). Tracciate in `reports/stato_progetto.md`.
- **Fetta 2 — token a scadenza e limite richieste**: `DEFERITA` — parte dopo il merge della fetta 1 (una PR per fetta).
- **Fetta 3 — timer due secondi e frase di attesa**: `DEFERITA` — dopo la fetta 2.
- **Fetta 4 — revisione del client nel browser**: `DEFERITA` — dopo la fetta 3.

## Anomalie

- `reports/lavoro_parallelo.md` non è ancora su main: letto dal ramo `origin/feat/merge-automatico-z1xjx2`.
- Il comando `gas voice` citato in `modules/voice/server.py` non esiste in `gas.py`: `run_server` non è collegato a nessun comando (mai collegato, da git log). Vedi richiesta sotto.

## RICHIESTE ALLA CHAT MOTORE

1. (Non urgente, serve prima di R5) Collegare `modules.voice.server.run_server` a un comando `python gas.py voice`: oggi il server voce si avvia solo a mano (`python -c "from modules.voice.server import run_server; run_server()"`).
2. (Cosmetica) La docstring di `tests/test_unit_gate.py` dice che in CI gira solo voice_server: dopo il merge della PR #229 non è più vero.
