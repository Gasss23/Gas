# Ultimo report — 2026-11-02 — Voce V7a: misura dei tempi (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #322 (https://github.com/Gasss23/Gas/pull/322), secondo la regola di merge di CLAUDE.md §10.
2. Sul Mac, dopo il merge: parlare a Gas dalla pagina del browser e leggere la riga «tempi: ascolto · cervello · voce · rete» (e in `gas_debug.log` le righe `gas.voce.tempi`): dicono dove si perde il tempo prima di scegliere V7b o il cervello «caldo».

## Esito delle fette

- **V7a — tempi della voce**: `FATTA` — ogni richiesta parlata misura trascrizione (Groq), cervello (`run_turn`) e voce (TTS), anche quando falliscono; il totale del server va nel JSON (`tempi`) o nell'intestazione `X-Gas-Tempi` (MP3); una riga INFO di soli numeri in `gas_debug.log` (logger `gas.voce.tempi`, non in console); la pagina mostra «tempi: ascolto · cervello · voce · rete». Review #614-M2 e #615-M2 CON RISERVE (chiuse), #616-M2 APPROVATO.
- **Merge di main** (PR #318 V6 e #321): `FATTA` — conflitto in `do_POST` risolto tenendo i tempi della V7a e il reset di `_capito` della V6; review #643-M2 APPROVATO.
- **Bot e verifica esterna su 33a0346**: V-1 bot (tempi a schermo anche sui guasti) e V-2 bot (il caricamento dell'audio è «rete», non server) `FATTE`, review #644/#645-M2; V-1 MEDIA ve (conflitto con main dopo la #320) `FATTA` col merge di main.
- **Bot su 8dc872e** (MEDIA: tempi di un guasto invisibili al primo turno): `FATTA` — tempi fuori dal riquadro della risposta, riquadro davvero nascosto prima della prima risposta, «Ho capito» vecchio nascosto sul guasto; review #646/#647-M2.
- **Bot e verifica esterna su 3a88f78**: conflitto con main dopo la #319 (MEDIA) `FATTA` col merge di main (#648-M2); «Ho capito» nascosto su ogni guasto e tempo del cervello anche senza risposta `FATTE` (#649-M2).
- Test: voce + claude_cli + dotenv 258 passed (browser compresi); kernel 1072 PASS, 0 FAIL (dopo il merge della #319).
- **V7b, V8, V9**: `DEFERITE` — PR in ordine dopo il merge della precedente (decisione dell'operatore riferita da M1).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- La latenza vera si misura solo sul Mac.
