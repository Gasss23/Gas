# Ultimo report — 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339), secondo la regola di merge di CLAUDE.md §10.
2. R-675-1-M2 parte storia (MEDIA, privacy): i turni di seguito giudicati «non per me» restano nella storia condivisa (li scrive gas.py). Decidere se toglierli nella fetta «profilo voce» (via su gas.py già dato) o subito.

## Esito delle fette

- **Pausa a voce** (contratto rivisto dall'operatore via M1): `FATTA` — «pausa»/«standby»/«basta così» (anche dopo Jarvis/Gas) → «Va bene.» + `X-Gas-Comando: pausa`, niente cervello.
- **Turni di seguito** (`X-Gas-Seguito: 1`): `FATTA` — solo cervello forte (mai i gratuiti); «[NON_PER_ME]» → JSON vuoto, niente voce, `X-Gas-Comando: fine`.
- **V-2 bot #335** (conferma che può bloccare il server): `FATTA` — timeout 5 s, errore in cache 60 s; chiusa anche R-669-1-M2 per la conferma.
- **V-1 bot #335** («Jarvis Gas»): `FATTA` — dichiarato voluto con un test.
- **Togliere dalla storia i turni «non per me»**: `DEFERITA — richiede gas.py` (fetta profilo voce).
- **C1**: `DEFERITA — prossima fetta` (ordine di M1).
- Test: suite voce 291 passed prima delle ultime due correzioni; dopo, voice_stt + voice_prova_voci 155 passed. Review #675-M2 APPROVATO CON RISERVE (bis, ter).

## Anomalie

- Il contratto della pausa è cambiato durante la fetta (prima «standby profondo», poi «chiude la conversazione»): la review copre l'ultima versione.
- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
