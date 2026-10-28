# ULTIMO REPORT — 2026-10-28 — Motivo vero dell'errore del cervello forte e avviso doctor per il PATH della notte

## DECISIONI UMANE RICHIESTE
1. Merge della PR #286 (https://github.com/Gasss23/Gas/pull/286) quando il bot e la CI hanno finito: la review #538 è APPROVATO CON RISERVE, quindi decide l'operatore (regola di merge di CLAUDE.md §10).

## Esito
- **Motivo vero dell'errore del forte nel report della notte**: FATTA. `brains/claude_cli.py` ha la nuova `ErroreClaudeCli`, che usa solo testi fissi. Il «Pipeline esausta» di `run_turn` ne mostra il testo; gli altri errori mostrano ancora solo il tipo. Il messaggio «non trovato» suggerisce `GAS_CLAUDE_BIN`.
- **Avviso doctor per il PATH della notte**: FATTA. Nuovo WARN «comando claude (notte)» quando `claude` si trova nel PATH del terminale ma non in quello di launchd (`PATH_TIMER_NOTTE`). L'avviso indica il percorso da mettere in `GAS_CLAUDE_BIN`.
- **Test**: T99v–T99z. Suite kernel: 1062 PASS, 0 FAIL. pytest (senza la suite kernel): 2265 passati, 61 saltati.
- **Giro della notte del Mac**: il giro delle 12:22 del 28 è andato OK (`punto_lead` OK, 1 tool, 11.2s). Il report di quel giro non dice quale cervello ha usato.

## Anomalie
- `gh` non è autenticato in questo ambiente: PR aperta e CI letta con lo strumento GitHub della sessione.
